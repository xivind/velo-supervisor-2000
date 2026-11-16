import sys
from pathlib import Path

import pytest

from conftest import REPO_ROOT, insert
from integrity.clock import frozen_clock
from integrity.loader import detect_layout, load_app
from integrity.recalculate import recalculate
from integrity.snapshot import stored_state


@pytest.fixture
def isolated(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("VELO_SUPERVISOR_CONFIG", "")
    monkeypatch.syspath_prepend(str(tmp_path))
    yield
    for name in ("main", "business_logic", "database_manager", "database_model", "utils", "strava"):
        sys.modules.pop(name, None)


def test_detect_layout_flat():
    assert detect_layout(REPO_ROOT) == "flat"


def test_detect_layout_rejects_unknown(tmp_path):
    with pytest.raises(ValueError):
        detect_layout(tmp_path)


def test_load_app_binds_to_given_database(isolated, db_copy, tmp_path):
    insert(db_copy, "bikes", bike_id="b1", bike_name="Bike One", bike_retired="False")
    app = load_app(REPO_ROOT, db_copy, tmp_path / "work")
    assert app.layout == "flat"
    assert [bike.bike_name for bike in app.database_manager.read_bikes()] == ["Bike One"]


def test_extraction_is_repeatable(isolated, db_copy, tmp_path):
    insert(db_copy, "bikes", bike_id="b1", bike_name="Bike", bike_retired="False")
    insert(db_copy, "rides", ride_id="r1", bike_id="b1", record_time="2026-01-01 10:00:00",
           ride_name="Ride", ride_distance=12.5, moving_time="1:00:00", commute="False")
    insert(db_copy, "components", component_id="c1", bike_id="b1", component_name="Chain",
           component_type="Chain", installation_status="Installed", component_distance_offset=0, cost=0, lifetime_expected=1000,
           service_interval=500, updated_date="2026-01-01 00:00:00")
    insert(db_copy, "component_history", history_id="h1", component_id="c1", bike_id="b1",
           component_name="Chain", updated_date="2026-01-01 00:00:00",
           update_reason="Installed", distance_marker=0)
    results = []
    for run in range(2):
        path = tmp_path / f"run{run}.sqlite"
        path.write_bytes(db_copy.read_bytes())
        with frozen_clock():
            app = load_app(REPO_ROOT, path, tmp_path / f"work{run}")
            recalculate(app)
        results.append(stored_state(path))
    assert results[0] == results[1]
    assert results[0]["components"]["c1"]["component_distance"] == 12.5


def test_recalculate_reports_failures_repeatably(isolated, db_copy, tmp_path):
    insert(db_copy, "bikes", bike_id="b1", bike_name="Bike", bike_retired="False")
    insert(db_copy, "rides", ride_id="r1", bike_id="b1", record_time="2026-01-01 10:00:00",
           ride_name="Ride", ride_distance=12.5, moving_time="1:00:00", commute="False")
    insert(db_copy, "components", component_id="c1", bike_id="b1", component_name="Chain",
           component_type="Chain", installation_status="Installed", component_distance_offset=0,
           cost=0, lifetime_expected=1000, service_interval=500)
    results = []
    for run in range(2):
        path = tmp_path / f"run{run}.sqlite"
        path.write_bytes(db_copy.read_bytes())
        with frozen_clock():
            app = load_app(REPO_ROOT, path, tmp_path / f"work{run}")
            results.append(recalculate(app))
    assert results[0] == results[1]
    assert any(line.startswith("distance_iterator:all_bikes: ") for line in results[0])
