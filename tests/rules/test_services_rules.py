"""Service rules: planned services stay out of health, completion and revert, workplan links.

Each test states one rule and checks it on the recalculated synthetic dataset, through stored
values and the named derived values of snapshot_now. Validation refusals are in
test_validation.py.
"""
import pytest

from fixtures.dataset import IDS


def removal_effect(delta, service_id):
    """Stored changes other than those to the removed service's own row"""
    return {path: change for path, change in delta.items()
            if path.startswith("stored/") and not path.startswith(f"stored/services/{service_id}/")}


def test_completed_service_reads_skip_planned_services(app):
    """The chain has two completed services and svc-chain-planned; only the planned read returns it"""
    manager = app.database_manager
    assert manager.read_latest_service_record(IDS.comp_chain_moved).service_id == IDS.svc_chain_2
    assert manager.read_oldest_service_record(IDS.comp_chain_moved).service_id == IDS.svc_chain_1
    assert [service.service_id for service in manager.read_subset_service_history(IDS.comp_chain_moved)] == [
        IDS.svc_chain_2, IDS.svc_chain_1]
    assert [service.service_id for service in manager.read_planned_services_by_component(IDS.comp_chain_moved)] == [
        IDS.svc_chain_planned]


def test_completed_service_history_and_planned_services_are_listed_apart(snapshot_now):
    """The component page lists completed services as history and planned ones on their own"""
    chain = snapshot_now()["derived"]["component"][IDS.comp_chain_moved]
    assert [row["service_id"] for row in chain["service_history"]] == [IDS.svc_chain_2, IDS.svc_chain_1]
    assert chain["planned_services"] == [
        {"service_id": IDS.svc_chain_planned, "component_id": IDS.comp_chain_moved, "component_name": "Chain",
         "description": "Replace chain", "workplan_id": IDS.wp_drivetrain,
         "workplan_name": "Chain (+1 more) - Drivetrain overhaul - Road bike", "incident_id": IDS.inc_drivetrain,
         "effective_planned_date": "2026-11-01 10:00", "planned_date": None, "installation_status": "Installed",
         "oldest_history_date": "2025-01-01 08:00"}]


def test_effective_planned_date_prefers_the_service_then_the_workplan(app, snapshot_now):
    """A service's own planned date wins over its workplan's due date, which is used when it has none.

    Dataset: svc-chain-planned has no date and wp-drivetrain is due 2026-11-01 10:00;
    svc-wheel-planned has its own date and no workplan. Setup: a cassette service in wp-drivetrain
    planned for 2026-12-01 10:00, and a tire service with neither, which has no date at all.
    """
    assert app.business_logic.create_planned_service(
        "svc-cassette-planned", IDS.comp_cassette_serviced, "Replace cassette", IDS.wp_drivetrain, None,
        "2026-12-01 10:00")[0]
    assert app.business_logic.create_planned_service(
        "svc-tire-planned", IDS.comp_tire_time, "Replace tire", None, None, None)[0]
    components = snapshot_now()["derived"]["component"]

    def effective(component_id):
        return [row["effective_planned_date"] for row in components[component_id]["planned_services"]]

    assert effective(IDS.comp_chain_moved) == ["2026-11-01 10:00"]
    assert effective(IDS.comp_wheel_offset) == ["2026-10-15 10:00"]
    assert effective(IDS.comp_cassette_serviced) == ["2026-12-01 10:00"]
    assert effective(IDS.comp_tire_time) == [None]


def test_planned_services_do_not_touch_health(app, operation_delta, snapshot_now):
    """Planning a service changes no component, bike or existing service; the new row has no
    service date, bike or distance marker
    """
    success, message = app.business_logic.create_planned_services(
        [IDS.comp_cassette_serviced], "Plan new clean", planned_date="2026-12-01 10:00")
    assert success, message
    stored_changes = {path.split("/")[1] for path in operation_delta() if path.startswith("stored/")}
    assert stored_changes == {"services"}
    services = snapshot_now()["stored"]["services"]
    assert services["new:services:1"] == {
        "service_id": "new:services:1", "component_id": IDS.comp_cassette_serviced, "component_name": "Cassette",
        "bike_id": None, "service_date": None, "distance_marker": None, "description": "Plan new clean",
        "workplan_id": None, "status": "Planned", "incident_id": None, "planned_date": "2026-12-01 10:00"}


def test_complete_then_revert_restores_state_before_completion(app, operation_delta, snapshot_now):
    """svc-chain-planned (wp-drivetrain, inc-drivetrain) completed on 2026-11-01 08:00 with a note,
    then reverted to planned with its original description.

    Completed: date, bike-road and marker 450 (as in test_create_completed_service), the note on
    a new line, links kept, the chain's latest service, and a hint that inc-drivetrain can be
    closed. Reverted: every stored and derived value is as before completion.
    """
    success, message = app.business_logic.complete_services([IDS.svc_chain_planned], "2026-11-01 08:00", "done early")
    assert success, message
    assert message["incident_hints"] == ["Incident 'Chain (+1 more) - Chain skips under load - Road bike' has no "
                                         "remaining planned services and can be closed"]
    completed = snapshot_now()["stored"]["services"][IDS.svc_chain_planned]
    assert completed == {
        "service_id": IDS.svc_chain_planned, "component_id": IDS.comp_chain_moved, "component_name": "Chain",
        "bike_id": IDS.bike_road, "service_date": "2026-11-01 08:00", "distance_marker": 450,
        "description": "Replace chain\ndone early", "workplan_id": IDS.wp_drivetrain, "status": "Completed",
        "incident_id": IDS.inc_drivetrain, "planned_date": None}
    assert app.database_manager.read_latest_service_record(IDS.comp_chain_moved).service_id == IDS.svc_chain_planned
    assert "stored/components/comp-chain-moved/service_next" in operation_delta()

    result = app.business_logic.update_service_record(
        IDS.comp_chain_moved, IDS.svc_chain_planned, None, "Replace chain", IDS.wp_drivetrain, "Planned",
        IDS.inc_drivetrain)
    assert result == (True, "Recalculated service records for Chain")
    assert operation_delta() == {}


REMOVAL_CASES = {
    "chain": (IDS.comp_chain_moved, IDS.svc_chain_2, "Waxed", {
        "stored/bikes/bike-road/service_status": {"before": "All components healthy",
                                                  "after": "Components need attention"},
        "stored/components/comp-chain-moved/service_next": {"before": 50, "after": -140},
        "stored/components/comp-chain-moved/service_status": {"before": "Due for service",
                                                              "after": "Service interval exceeded"}}),
    "tire_only_service": (IDS.comp_tire_time, IDS.svc_tire, "Sealant top-up", {
        "stored/components/comp-tire-time/service_next_days": {"before": -17, "after": -260}}),
}


@pytest.mark.parametrize("action", ["revert", "delete"])
@pytest.mark.parametrize("case", list(REMOVAL_CASES))
def test_revert_to_planned_matches_deletion(app, operation_delta, case, action):
    """Reverting a completed service to planned leaves the component, its other services and the
    bike as deleting the service does; both actions are held to the same expected changes.

    Chain: recalculated from svc-chain-1 (see test_update_service_revert_to_planned). Tire:
    svc-tire (2026-08-01, 107 days ago, next 90 - 107 = -17) is its only completed service, so
    days count from installation on 2025-12-01, 350 days: next 90 - 350 = -260, still exceeded.
    """
    component_id, service_id, description, expected = REMOVAL_CASES[case]
    if action == "revert":
        success, message = app.business_logic.update_service_record(
            component_id, service_id, None, description, status="Planned")
    else:
        success, message, *_ = app.business_logic.delete_record("Services", service_id)
    assert success, message
    assert removal_effect(operation_delta(), service_id) == expected
    latest = app.database_manager.read_latest_service_record(component_id)
    assert latest is None or latest.service_id != service_id


def test_status_change_keeps_workplan_link_on_newest_service(app, operation_delta):
    """Uninstalling the cassette reprocesses its services; svc-cassette-2, its newest, keeps
    wp-drivetrain and inc-drivetrain
    """
    success, message = app.business_logic.create_history_record(
        IDS.comp_cassette_serviced, "Not installed", IDS.bike_road, "2026-10-01 08:00")
    assert success, message
    changed = [path for path in operation_delta() if path.startswith("stored/services/")]
    assert not [path for path in changed if path.endswith(("/workplan_id", "/incident_id"))]


def test_deleting_newest_service_keeps_workplan_link_on_remaining(app, operation_delta, snapshot_now):
    """Setup: a newer cassette service without workplan on 2026-11-01 08:00. Deleting it
    recalculates from svc-cassette-2, which keeps wp-drivetrain and inc-drivetrain
    """
    assert app.business_logic.create_service_record(IDS.comp_cassette_serviced, "2026-11-01 08:00", "Quick clean")[0]
    (new_id,) = [service.service_id for service in app.database_manager.read_subset_service_history(
        IDS.comp_cassette_serviced) if service.service_date == "2026-11-01 08:00"]
    assert app.business_logic.delete_record("Services", new_id)[0]
    remaining = snapshot_now()["stored"]["services"][IDS.svc_cassette_2]
    assert (remaining["workplan_id"], remaining["incident_id"]) == (IDS.wp_drivetrain, IDS.inc_drivetrain)
    assert app.database_manager.read_latest_service_record(IDS.comp_cassette_serviced).service_id == IDS.svc_cassette_2
    assert operation_delta() == {}


def test_planned_service_once_per_workplan_only(app):
    """The chain's planned service in wp-drivetrain does not block one outside any workplan or in
    another workplan
    """
    validate = app.business_logic.validate_service_record
    assert validate("plan service", IDS.comp_chain_moved, "svc-new", None, workplan_id=None,
                    service_description="Replace chain")[0]
    assert validate("plan service", IDS.comp_chain_moved, "svc-new", None, workplan_id=IDS.wp_brake_check,
                    service_description="Replace chain")[0]


def test_revert_on_retired_component_is_refused(app, operation_delta):
    """svc-pads-retired cannot be reverted to planned, since its component is retired"""
    result = app.business_logic.update_service_record(
        IDS.comp_pads_retired, IDS.svc_pads_retired, None, "Cleaned pads", IDS.wp_brake_check, "Planned",
        IDS.inc_squeal)
    assert result == (False, "Services cannot be planned, completed or changed on a retired component: Commuter "
                             "brake pads")
    assert operation_delta() == {}


def test_completing_in_done_workplan_only_up_to_its_completion_date(app, snapshot_now):
    """Setup: a cassette service planned in wp-brake-check (Done, completed 2025-04-01 10:00).
    Completing it after that date is refused; on 2025-03-01 08:00, before it, it is completed.
    """
    success, message = app.business_logic.create_planned_services(
        [IDS.comp_cassette_serviced], "Reverted clean", IDS.wp_brake_check)
    assert success, message
    planned_id = "new:services:1"
    (service_id,) = [service.service_id for service in app.database_manager.read_planned_services_by_workplan(
        IDS.wp_brake_check)]

    success, message = app.business_logic.complete_services([service_id], "2026-11-01 08:00")
    assert success is False
    assert message["failed_components"] == [
        {"name": "Cassette", "error": "Service date cannot be after the completion date of its workplan "
                                      "(2025-04-01 10:00). Reopen the workplan first. Component: Cassette"}]

    success, message = app.business_logic.complete_services([service_id], "2025-03-01 08:00")
    assert success, message
    completed = snapshot_now()["stored"]["services"][planned_id]
    assert (completed["status"], completed["service_date"]) == ("Completed", "2025-03-01 08:00")
