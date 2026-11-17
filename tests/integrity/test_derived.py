import json

import pytest
from conftest import REPO_ROOT, insert
from integrity.clock import frozen_clock
from integrity.derived import RESOURCES, derived_values
from integrity.loader import load_app
from integrity.snapshot import dumps
from test_loader import isolated  # noqa: F401


@pytest.fixture
def app(isolated, db_copy, tmp_path):  # noqa: F811
    insert(db_copy, "bikes", bike_id="b1", bike_name="Bike One", bike_retired="False", total_distance=100.5)
    insert(
        db_copy,
        "rides",
        ride_id="r1",
        bike_id="b1",
        record_time="2026-01-01 10:00:00",
        ride_name="Ride",
        ride_distance=12.5,
        moving_time="1:00:00",
        commute="False",
    )
    for component_id, name in (("c1", "Chain"), ("c2", "Cassette")):
        insert(
            db_copy,
            "components",
            component_id=component_id,
            bike_id="b1",
            component_name=name,
            component_type=name,
            installation_status="Installed",
            component_distance_offset=0,
            cost=100,
            lifetime_expected=1000,
            service_interval=500,
            component_distance=99.5,
            lifetime_remaining=900.123456789,
            service_next=400,
            updated_date="2026-01-01 00:00:00",
        )
        insert(
            db_copy,
            "component_history",
            history_id=f"h{component_id}",
            component_id=component_id,
            bike_id="b1",
            component_name=name,
            updated_date="2026-01-01 00:00:00",
            update_reason="Installed",
            distance_marker=0,
        )
    insert(
        db_copy,
        "services",
        service_id="s1",
        component_id="c1",
        bike_id="b1",
        service_date="2026-02-01 10:00",
        description="Lube",
        status="Completed",
        distance_marker=10,
    )
    insert(
        db_copy,
        "services",
        service_id="s2",
        component_id="c2",
        bike_id="b1",
        description="Check",
        status="Planned",
        workplan_id="w1",
        planned_date="2026-12-01 10:00",
        incident_id="i1",
    )
    insert(
        db_copy,
        "collections",
        collection_id="col1",
        collection_name="Set",
        components=json.dumps(["c1", "c2"]),
        bike_id="b1",
        updated_date="2026-01-01 00:00:00",
    )
    insert(
        db_copy,
        "workplans",
        workplan_id="w1",
        workplan_name="Plan",
        workplan_status="Planned",
        workplan_size="Small",
        due_date="2026-12-01 10:00",
    )
    insert(
        db_copy,
        "incidents",
        incident_id="i1",
        incident_date="2026-02-02 10:00",
        incident_status="Open",
        incident_severity="Low",
        incident_affected_component_ids=json.dumps(["c1"]),
        incident_affected_bike_id="b1",
        incident_description="Noise",
    )
    with frozen_clock():
        yield load_app(REPO_ROOT, db_copy, tmp_path / "work")


def test_derived_has_every_resource(app):
    result = derived_values(app)
    assert set(result) == set(RESOURCES)
    assert "b1" in result["bike"]
    assert {"c1", "c2"} <= set(result["component"])
    assert "col1" in result["collection"]
    assert "w1" in result["workplan"]
    assert "i1" in result["incident"]
    assert result["workplan"]["w1"]["planned_services"][0]["service_id"] == "s2"
    assert "error" not in result["bike"]["b1"]
    assert result["component"]["c1"]["list_row"]["lifetime_remaining"] == 900.123457


def test_tuple_shape_change_fails_loudly(app, monkeypatch):
    original = app.bl_module.get_workplan_data_tuple
    monkeypatch.setattr(app.bl_module, "get_workplan_data_tuple", lambda *args: original(*args) + ("extra",))
    with pytest.raises(ValueError):
        derived_values(app)


def test_derived_is_json_serialisable(app):
    assert dumps(derived_values(app))


def test_no_source_errors(app):
    text = dumps(derived_values(app))
    assert '"error"' not in text


def test_dangling_collection_is_recorded_not_raised(app):
    insert(
        app.db_path,
        "collections",
        collection_id="col2",
        collection_name="Gone",
        components=json.dumps(["gone"]),
        bike_id="b1",
        updated_date="2026-01-01 00:00:00",
    )
    result = derived_values(app)
    assert "error" in result["overview"]["collections"]
    assert "AttributeError" in result["overview"]["collections"]["error"]
    assert "col2" in result["collection"]
    assert {"c1", "c2"} <= set(result["component"])
    assert "b1" in result["bike"] and "w1" in result["workplan"] and "i1" in result["incident"]
