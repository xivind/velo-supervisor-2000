"""Shared fixtures: fixed clock, synthetic dataset, app modules bound to it, snapshots.

app_env, migrated_env and modules serve the old suites on a bare template copy and
are removed once those suites are rewritten.
"""

import sys
import json
import shutil
from pathlib import Path

import pytest

from fixtures.dataset import build_dataset
from integrity.clock import frozen_clock
from integrity.derived import derived_values
from integrity.loader import load_app
from integrity.recalculate import recalculate
from integrity.snapshot import new_id_map, normalise_new_ids, replace_ids, stored_state

REPO_ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_DB = REPO_ROOT / "config" / "template_db.sqlite"


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
        return {"stored": normalise_new_ids(stored, baseline_ids),
                "derived": replace_ids(derived_values(app), new_id_map(stored, baseline_ids))}

    return take


@pytest.fixture
def app_env(tmp_path, monkeypatch):
    """Copy template db to tmp dir, write config.json there, chdir into it"""
    db_path = tmp_path / "test_db.sqlite"
    shutil.copy(TEMPLATE_DB, db_path)
    config = {"db_path": str(db_path),
              "strava_tokens": str(tmp_path / "strava_tokens.json"),
              "verbose_logging": False}
    (tmp_path / "config.json").write_text(json.dumps(config), encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    return {"db_path": str(db_path), "tmp_path": tmp_path}


@pytest.fixture
def migrated_env(app_env):
    """Run db_migration against the copied template db so the schema is current"""
    from velo_supervisor import db_migration
    conn = db_migration.sqlite3.connect(app_env["db_path"])
    cursor = conn.cursor()
    db_migration.run_all_migrations(cursor, conn)
    conn.close()
    return app_env


@pytest.fixture
def modules(migrated_env):
    """Fresh imports of the app modules bound to the test database"""
    _forget_app_modules()
    from velo_supervisor import utils
    from velo_supervisor import database_model
    from velo_supervisor import business_logic
    from types import SimpleNamespace
    return SimpleNamespace(utils=utils,
                           database_model=database_model,
                           database_manager=business_logic.database_manager,
                           business_logic=business_logic.BusinessLogic(SimpleNamespace()))
