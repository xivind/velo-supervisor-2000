"""Shared fixtures: fixed clock, synthetic dataset, app modules bound to it, snapshots, a test client"""

import importlib
import json
import logging
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from fixtures.dataset import build_dataset
from fixtures.expected import assert_matches_expected
from integrity.clock import frozen_clock
from integrity.delta import snapshot_delta
from integrity.derived import derived_values
from integrity.loader import load_app
from integrity.recalculate import recalculate
from integrity.snapshot import new_id_map, normalise_new_ids, replace_ids, stored_state

REPO_ROOT = Path(__file__).resolve().parents[1]


def _forget_app_modules():
    for name in list(sys.modules):
        if name == "velo_supervisor" or name.startswith("velo_supervisor."):
            del sys.modules[name]


@pytest.fixture(autouse=True)
def clock():
    """Every test runs at FIXED_NOW in UTC"""
    with frozen_clock():
        yield


@pytest.fixture
def dataset_db(tmp_path):
    db_path = tmp_path / "dataset.sqlite"
    build_dataset(db_path)
    return db_path


@pytest.fixture
def recalculated(dataset_db, tmp_path, monkeypatch):
    """App modules bound to the dataset and the failures of one full recalculation.

    load_app changes cwd, VELO_SUPERVISOR_CONFIG and sys.path; monkeypatch records
    them first so they are restored after the test.
    """
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("VELO_SUPERVISOR_CONFIG", str(tmp_path / "config.json"))
    monkeypatch.syspath_prepend(str(tmp_path))
    loaded = load_app(REPO_ROOT, dataset_db, tmp_path)
    failures = recalculate(loaded)
    yield loaded, failures
    _forget_app_modules()


@pytest.fixture
def app(recalculated):
    return recalculated[0]


@pytest.fixture
def recalculation_failures(recalculated):
    return recalculated[1]


@pytest.fixture
def snapshot_now(app):
    """Return a function that snapshots stored and derived values as they are, without recalculating.

    Primary keys that were not in the database when the test started are replaced by
    new:<table>:<n> labels in both layers.
    """
    baseline_ids = {key for rows in stored_state(app.db_path).values() for key in rows}

    def take():
        stored = stored_state(app.db_path)
        return {
            "stored": normalise_new_ids(stored, baseline_ids),
            "derived": replace_ids(derived_values(app), new_id_map(stored, baseline_ids)),
        }

    return take


def config_contents(app):
    """The config file as written, without the fixture's own db_path and strava_tokens, tmp paths that
    differ per run. The same keys set to other values are kept.
    """
    config = json.loads(app.utils.config_path().read_text(encoding="utf-8"))
    workdir = str(app.db_path.parent)
    return {
        key: value
        for key, value in config.items()
        if not (key in ("db_path", "strava_tokens") and value.startswith(workdir))
    }


@pytest.fixture
def operation_delta(app, snapshot_now):
    """Return a function giving the snapshot_delta from the recalculated dataset to now.

    The before state is taken when the fixture is set up, ahead of anything the test does, so
    setup shows in the delta. It must equal the recorded recalculation result, which pins the
    baseline the deltas are relative to. Both sides include the config contents.
    """
    before = snapshot_now()
    assert_matches_expected("recalculation", before)
    before["config"] = config_contents(app)

    def take():
        return snapshot_delta(before, {**snapshot_now(), "config": config_contents(app)})

    return take


@pytest.fixture
def client(app):
    """A client for main.app on the dataset, without the lifespan, so the scheduler does not start.

    Importing main adds utils.ERROR_RECORDER to the root logger; handlers added are removed after.
    """
    root_handlers = list(logging.getLogger().handlers)
    main = importlib.import_module("velo_supervisor.main")
    yield TestClient(main.app, raise_server_exceptions=False)
    for handler in list(logging.getLogger().handlers):
        if handler not in root_handlers:
            logging.getLogger().removeHandler(handler)
