"""Characterisation of service, incident, workplan and collection operations.

Each test runs one operation on the recalculated synthetic dataset and compares the delta it
leaves, in stored values, derived values and the config file, with
tests/fixtures/expected/op_<name>.json (see the operation_delta fixture). The values in each
docstring are worked out by hand from tests/fixtures/dataset.py and the code as it is today.
Setup that an operation needs and the dataset lacks is named in the test's docstring; its
effects are part of the delta. A refusal test asserts the result and an empty delta.
"""
from dataclasses import asdict

import pytest

from fixtures.dataset import IDS
from fixtures.expected import assert_matches_expected
from integrity.snapshot import stored_state

DATASET_IDS = set(asdict(IDS).values())
DATE_FORMAT_HINT = "Expected format: YYYY-MM-DD HH:MM (e.g., 2024-12-14 23:34)"


def _new_ids(app, table):
    """Primary keys of table that are not in the dataset, in row order"""
    return [key for key in stored_state(app.db_path)[table] if key not in DATASET_IDS]


def test_create_completed_service(app, operation_delta):
    """A completed chain service on 2026-11-01 08:00, linked to wp-drivetrain.

    Marker since svc-chain-2 (2025-10-01): gravel Oct 2025..Feb 2026, 5 x 20 = 100, plus road
    Apr..Oct 2026, 7 x 50 = 350, = 450, on bike-road. No ride since, so service next 500, OK
    (was 50, "Due for service"). bike-road stays "All components healthy".
    """
    result = app.business_logic.create_service_record(
        IDS.comp_chain_moved, "2026-11-01 08:00", "Replaced chain", IDS.wp_drivetrain, "Completed", None, None)
    assert result == (True, "All service records successfully processed")
    assert len(_new_ids(app, "services")) == 1
    assert_matches_expected("op_service_create_completed", operation_delta())


def test_create_service_record_as_planned(app, operation_delta):
    """status Planned routes to create_planned_service; the empty strings a form sends become None.

    The tire gets a planned service with no workplan, incident or planned date; no service
    date, bike or distance marker, and nothing is recalculated.
    """
    result = app.business_logic.create_service_record(
        IDS.comp_tire_time, None, "Replace tire", "", "Planned", "", "")
    assert result == (True, "Created service record for component Gravel tire.")
    assert_matches_expected("op_service_create_planned", operation_delta())


def test_create_planned_service(app, operation_delta):
    """A planned cassette service in wp-drivetrain for inc-drivetrain, planned for 2026-12-01 10:00.

    The cassette's completed svc-cassette-2 is in the workplan too, but only planned services
    count for the one-per-workplan rule. Nothing is recalculated.
    """
    result = app.business_logic.create_planned_service(
        "svc-new-planned", IDS.comp_cassette_serviced, "Replace cassette", IDS.wp_drivetrain, IDS.inc_drivetrain,
        "2026-12-01 10:00")
    assert result == (True, "Created service record for component Cassette.")
    assert_matches_expected("op_service_create_planned_direct", operation_delta())


def test_create_planned_services(app, operation_delta):
    """Planned services for the cassette and the rear wheel in wp-drivetrain.

    The wheel already has svc-wheel-planned, but outside any workplan, so it gets a second one.
    Nothing is recalculated.
    """
    success, message = app.business_logic.create_planned_services(
        [IDS.comp_cassette_serviced, IDS.comp_wheel_offset], "Check wear", IDS.wp_drivetrain, None, None)
    assert (success, message) == (True, {
        "type": "success", "summary": "Successfully planned services for all 2 components", "total_count": 2,
        "success_count": 2, "successful_components": ["Cassette", "Rear wheel"], "failed_components": [],
        "incident_hints": []})
    assert_matches_expected("op_services_create_planned", operation_delta())


def test_create_planned_services_partial_failure(app, operation_delta):
    """The chain already has a planned service in wp-drivetrain, so only the cassette gets one.

    The result is False although the cassette's service is stored.
    """
    success, message = app.business_logic.create_planned_services(
        [IDS.comp_chain_moved, IDS.comp_cassette_serviced], "Check wear", IDS.wp_drivetrain, None, None)
    assert (success, message) == (False, {
        "type": "partial_failure", "summary": "Only 1 of 2 services were planned", "total_count": 2,
        "success_count": 1, "successful_components": ["Cassette"],
        "failed_components": [{"name": "Chain",
                               "error": "Component Chain already has a planned service in this workplan"}],
        "incident_hints": []})
    assert_matches_expected("op_services_create_planned_partial", operation_delta())


def test_complete_services(app, operation_delta):
    """svc-chain-planned and svc-wheel-planned completed on 2026-11-01 08:00 with one note.

    Chain: marker 450 and service next 500, OK, as in test_create_completed_service. Wheel,
    its first service: road Mar 2025..Oct 2026, 20 x 50 = 1000 (the offset does not count);
    service next 2000 (was 1000). The note is appended to each description on a new line.
    inc-drivetrain has no planned service left, so a hint says it can be closed; wp-drivetrain
    has every service completed. bike-road stays "All components healthy".
    """
    success, message = app.business_logic.complete_services(
        [IDS.svc_chain_planned, IDS.svc_wheel_planned], "2026-11-01 08:00", "Done at the shop")
    assert (success, message) == (True, {
        "type": "success", "summary": "Successfully completed services for all 2 components", "total_count": 2,
        "success_count": 2, "successful_components": ["Chain", "Rear wheel"], "failed_components": [],
        "incident_hints": ["Incident 'Chain (+1 more) - Chain skips under load - Road bike' has no remaining "
                           "planned services and can be closed"]})
    assert_matches_expected("op_services_complete", operation_delta())


def test_update_completed_service(app, operation_delta):
    """svc-chain-2 moved from 2025-10-01 to 2025-11-01 08:00 and its description changed.

    svc-chain-2 marker since svc-chain-1 (2025-04-01): road Apr..Jun 2025, 150, plus gravel
    Aug..Oct 2025, 60, = 210 (was 190). Since svc-chain-2: gravel Nov 2025..Feb 2026, 80, plus
    road Apr..Oct 2026, 350, = 430; service next 70, still "Due for service" (threshold 100).
    """
    result = app.business_logic.update_service_record(
        IDS.comp_chain_moved, IDS.svc_chain_2, "2025-11-01 08:00", "Waxed and checked", None, "Completed", None,
        None)
    assert result == (True, "All service records successfully processed")
    assert_matches_expected("op_service_update_completed", operation_delta())


def test_update_service_revert_to_planned(app, operation_delta):
    """svc-chain-2 reverted to planned for 2026-12-01 10:00: date, bike and marker are cleared.

    The chain is recalculated from svc-chain-1 as when svc-chain-2 is deleted: since
    2025-04-01, 150 + 140 + 350 = 640, service next -140, "Service interval exceeded", so
    bike-road needs attention. The chain now has two planned services.
    """
    result = app.business_logic.update_service_record(
        IDS.comp_chain_moved, IDS.svc_chain_2, None, "Wax again", None, "Planned", None, "2026-12-01 10:00")
    assert result == (True, "Recalculated service records for Chain")
    assert_matches_expected("op_service_revert_to_planned", operation_delta())


def test_update_service_complete_planned(app, operation_delta):
    """svc-wheel-planned completed through the edit form on 2026-11-01 08:00, keeping its planned date.

    As for the wheel in test_complete_services: marker 1000, service next 2000. No incident or
    workplan, so nothing else changes.
    """
    result = app.business_logic.update_service_record(
        IDS.comp_wheel_offset, IDS.svc_wheel_planned, "2026-11-01 08:00", "Trued rear wheel", None, "Completed",
        None, "2026-10-15 10:00")
    assert result == (True, "All service records successfully processed")
    assert_matches_expected("op_service_update_complete_planned", operation_delta())


def test_create_incident(app, operation_delta):
    """An open incident on bike-gravel for the tire; empty optional fields become None.

    The message carries the new ID, so it is checked against the stored row.
    """
    success, message = app.business_logic.create_incident_record(
        "2026-11-10 10:00", "Open", "Priority", [IDS.comp_tire_time], IDS.bike_gravel, "Sidewall cut", "", "")
    (incident_id,) = _new_ids(app, "incidents")
    assert (success, message) == (True, f"Created new incident report with id {incident_id}")
    assert_matches_expected("op_incident_create", operation_delta())


def test_update_incident(app, operation_delta):
    """inc-drivetrain edited in full: severity Monitor, the cassette removed, a new description"""
    result = app.business_logic.update_incident_record(
        IDS.inc_drivetrain, "2026-01-15 10:00", "Open", "Monitor", [IDS.comp_chain_moved], IDS.bike_road,
        "Chain skips on climbs", "", "", None)
    assert result == (True, f"Updated incident report with id {IDS.inc_drivetrain}")
    assert_matches_expected("op_incident_update", operation_delta())


def test_update_incident_partial(app, operation_delta):
    """inc-drivetrain resolved through a partial update; only the given fields change"""
    result = app.business_logic.update_incident_record(
        IDS.inc_drivetrain, incident_status="Resolved", resolution_date="2026-11-10 10:00",
        resolution_notes="New chain fitted", update_mode="partial")
    assert result == (True, f"Updated incident report with id {IDS.inc_drivetrain}")
    assert_matches_expected("op_incident_update_partial", operation_delta())


def test_create_workplan(app, operation_delta):
    """A planned workplan with a name; no services, so it reaches no bike or component"""
    success, message, workplan_id = app.business_logic.create_workplan(
        "2026-12-01 10:00", "Planned", "Small", "Winter preparation", "", "", "Winter prep", None, None)
    assert _new_ids(app, "workplans") == [workplan_id]
    assert (success, message) == (True, f"Created new workplan with id {workplan_id}")
    assert_matches_expected("op_workplan_create", operation_delta())


def test_create_workplan_from_incident(app, operation_delta):
    """A workplan from inc-drivetrain with no component selection plans a service for both its components.

    Chain and cassette each get a planned service with the incident's description, the new
    workplan and inc-drivetrain. The chain's planned service in wp-drivetrain does not block
    one in another workplan.
    """
    success, message, workplan_id = app.business_logic.create_workplan(
        "2026-12-01 10:00", "Planned", "Medium", None, None, None, None, IDS.inc_drivetrain, None)
    assert _new_ids(app, "workplans") == [workplan_id]
    assert (success, message) == (
        True, f"Created new workplan with id {workplan_id} and planned 2 service(s) from incident")
    assert_matches_expected("op_workplan_create_from_incident", operation_delta())


def test_create_workplan_from_incident_with_selection(app, operation_delta):
    """Only the selected incident components get a planned service: the cassette, not the chain"""
    success, message, workplan_id = app.business_logic.create_workplan(
        "2026-12-01 10:00", "Planned", "Small", "Cassette only", None, None, None, IDS.inc_drivetrain,
        [IDS.comp_cassette_serviced])
    assert _new_ids(app, "workplans") == [workplan_id]
    assert (success, message) == (
        True, f"Created new workplan with id {workplan_id} and planned 1 service(s) from incident")
    assert_matches_expected("op_workplan_create_from_incident_selection", operation_delta())


def test_update_workplan(app, operation_delta):
    """wp-drivetrain edited in full: named, later due date, size and description changed; still Planned"""
    result = app.business_logic.update_workplan(
        IDS.wp_drivetrain, "2026-12-15 10:00", "Planned", "Large", "Replace chain, check cassette", None, None,
        None, None, "Drivetrain")
    assert result == (True, f"Updated workplan with id {IDS.wp_drivetrain}")
    assert_matches_expected("op_workplan_update", operation_delta())


def test_complete_workplan(app, operation_delta):
    """wp-drivetrain completed on 2026-11-02 10:00 as the completion modal sends it, closing inc-drivetrain.

    Setup: svc-chain-planned completed on 2026-11-01 08:00 with complete_services, since a
    workplan with planned services cannot be completed; the chain is as in
    test_create_completed_service. The completion date is after the latest service
    (2026-11-01 08:00) and not in the future. inc-drivetrain is resolved on the completion
    date with a note naming the workplan's description and ID.
    """
    success, message = app.business_logic.complete_services([IDS.svc_chain_planned], "2026-11-01 08:00")
    assert (success, message["type"]) == (True, "success")
    result = app.business_logic.update_workplan(
        IDS.wp_drivetrain, None, "Done", None, None, "2026-11-02 10:00", "All parts replaced", "on", "partial")
    assert result == (True, f"Updated workplan with id {IDS.wp_drivetrain} and closed 1 linked incident(s)")
    assert_matches_expected("op_workplan_complete", operation_delta())


def test_create_collection(app, operation_delta):
    """A collection of the road cassette and chain takes bike-road from them; updated_date stays None"""
    success, message, collection_id = app.business_logic.create_collection(
        "Drivetrain", [IDS.comp_cassette_serviced, IDS.comp_chain_moved], "")
    assert _new_ids(app, "collections") == [collection_id]
    assert (success, message) == (True, "Created collection Drivetrain")
    assert_matches_expected("op_collection_create", operation_delta())


def test_update_collection(app, operation_delta):
    """coll-mixed renamed and left with the rear wheel only, so it is healthy; updated_date is unchanged"""
    result = app.business_logic.update_collection(IDS.coll_mixed, "Road wheels", [IDS.comp_wheel_offset], "")
    assert result == (True, "Updated collection Road wheels")
    assert_matches_expected("op_collection_update", operation_delta())


def test_change_collection_status_not_installed(app, operation_delta):
    """coll-gravel-set uninstalled on 2026-11-01 08:00 with no bike given.

    Each record takes its component's bike (bike-gravel); the components are stored with no
    bike, and so is the collection. Tire: lifetime days to now unchanged, 365 - 350 = 15;
    service days since svc-tire unchanged. Pads: gravel Jan 2025..Oct 2026, 22 x 20 = 440,
    lifetime remaining 1060, unchanged. updated_date 2026-11-01 08:00.
    """
    success, message = app.business_logic.change_collection_status(
        IDS.coll_gravel_set, "Not installed", "2026-11-01 08:00", None, "Winter storage")
    assert (success, message) == (True, {
        "type": "success", "summary": "Successfully updated status for all 2 components", "total_count": 2,
        "success_count": 2, "successful_components": ["Gravel tire", "Bremseklosser bak æøå"],
        "failed_components": []})
    assert_matches_expected("op_collection_status_not_installed", operation_delta())


def test_change_collection_status_retired(app, operation_delta):
    """coll-gravel-set retired on bike-gravel on 2026-11-01 08:00.

    Each create_history_record returns "warning" (bike-gravel lacks Chain and Rear wheel),
    which counts as success. Tire: lifetime days to retirement 2025-12-01..2026-11-01 = 335,
    remaining 30; service days svc-tire 2026-08-01..2026-11-01 = 92, next -2. The collection
    has retired members, so its bike is None. bike-gravel has no installed component left.
    """
    success, message = app.business_logic.change_collection_status(
        IDS.coll_gravel_set, "Retired", "2026-11-01 08:00", IDS.bike_gravel, None)
    assert (success, message) == (True, {
        "type": "success", "summary": "Successfully updated status for all 2 components", "total_count": 2,
        "success_count": 2, "successful_components": ["Gravel tire", "Bremseklosser bak æøå"],
        "failed_components": []})
    assert_matches_expected("op_collection_status_retired", operation_delta())


def test_change_collection_status_installed(app, operation_delta):
    """coll-mixed, reduced to the spare saddle, installed on bike-road on 2026-09-01 08:00.

    Setup: update_collection leaves only the not installed saddle, since a collection mixing
    installed and not installed components is refused. Saddle: road Sep..Oct 2026, 2 x 50 =
    100, plus the 300 offset, distance 400; lifetime remaining 19600, OK. bike-road keeps
    both mandatory types, so the history call returns True. The setup clears the collection's
    bike and the status change sets it to bike-road again, so only updated_date (2026-09-01
    08:00) and the components show for the collection.
    """
    assert app.business_logic.update_collection(
        IDS.coll_mixed, "Mixed parts", [IDS.comp_no_history], "Installed and spare parts") == (
        True, "Updated collection Mixed parts")
    success, message = app.business_logic.change_collection_status(
        IDS.coll_mixed, "Installed", "2026-09-01 08:00", IDS.bike_road, "Fitted for the season")
    assert (success, message) == (True, {
        "type": "success", "summary": "Successfully updated status for all 1 components", "total_count": 1,
        "success_count": 1, "successful_components": ["Spare saddle"], "failed_components": []})
    assert_matches_expected("op_collection_status_installed", operation_delta())


REFUSALS = {
    "service_future_date": (
        lambda logic: logic.create_service_record(IDS.comp_chain_moved, "2026-11-20 08:00", "Waxed"),
        (False, "Service date cannot be in the future. Component: Chain")),
    "service_retired_component": (
        lambda logic: logic.create_service_record(IDS.comp_pads_retired, "2025-08-01 08:00", "Cleaned pads"),
        (False, "Services cannot be planned, completed or changed on a retired component: Commuter brake pads")),
    "service_never_installed": (
        lambda logic: logic.create_service_record(IDS.comp_no_history, "2026-11-01 08:00", "Cleaned saddle"),
        (False, "Services cannot be registered to components that have never been installed. Component: Spare "
         "saddle")),
    "service_before_creation": (
        lambda logic: logic.create_service_record(IDS.comp_tire_time, "2025-12-01 08:00", "Sealant top-up"),
        (False, "Service date cannot be at or before component creation date 2025-12-01 08:00. Component: Gravel "
         "tire")),
    "service_after_done_workplan": (
        lambda logic: logic.create_service_record(IDS.comp_chain_moved, "2026-11-01 08:00", "Waxed",
                                                  IDS.wp_brake_check),
        (False, "Service date cannot be after the completion date of its workplan (2025-04-01 10:00). Reopen the "
         "workplan first. Component: Chain")),
    "planned_short_description": (
        lambda logic: logic.create_service_record(IDS.comp_tire_time, None, "Fix", status="Planned"),
        (False, "Description must be at least 5 characters. Component: Gravel tire")),
    "planned_bad_date": (
        lambda logic: logic.create_service_record(IDS.comp_tire_time, None, "Replace tire", status="Planned",
                                                  planned_date="2026-12-01"),
        (False, f"Invalid date format: '2026-12-01'. {DATE_FORMAT_HINT}")),
    "planned_duplicate_in_workplan": (
        lambda logic: logic.create_service_record(IDS.comp_chain_moved, None, "Replace chain", IDS.wp_drivetrain,
                                                  "Planned"),
        (False, "Component Chain already has a planned service in this workplan")),
    "planned_services_none_selected": (
        lambda logic: logic.create_planned_services([], "Check wear"),
        (False, "No components selected")),
    "complete_services_none_selected": (
        lambda logic: logic.complete_services([], "2026-11-01 08:00"),
        (False, "No services selected")),
    "complete_services_already_completed": (
        lambda logic: logic.complete_services([IDS.svc_chain_2], "2026-11-01 08:00"),
        (False, {"type": "complete_failure", "summary": "No services were completed", "total_count": 1,
                 "success_count": 0, "successful_components": [],
                 "failed_components": [{"name": "Chain",
                                        "error": "Only planned services can be completed. Component: Chain"}],
                 "incident_hints": []})),
    "update_service_not_found": (
        lambda logic: logic.update_service_record(IDS.comp_chain_moved, "svc-unknown", "2026-11-01 08:00",
                                                  "Waxed"),
        (False, "Service record not found: svc-unknown")),
    "update_service_retired_component": (
        lambda logic: logic.update_service_record(IDS.comp_pads_retired, IDS.svc_pads_retired, "2025-05-01 08:00",
                                                  "Cleaned pads", IDS.wp_brake_check, "Completed", IDS.inc_squeal),
        (False, "Services cannot be planned, completed or changed on a retired component: Commuter brake pads")),
    "update_service_future_date": (
        lambda logic: logic.update_service_record(IDS.comp_chain_moved, IDS.svc_chain_2, "2026-11-20 08:00",
                                                  "Waxed"),
        (False, "Service date cannot be in the future. Component: Chain")),
    "workplan_not_found": (
        lambda logic: logic.update_workplan("wp-unknown", None, "Done", None, None, "2026-11-01 10:00", None, None,
                                            "partial"),
        (False, "Workplan not found: wp-unknown")),
    "workplan_complete_with_planned_services": (
        lambda logic: logic.update_workplan(IDS.wp_drivetrain, None, "Done", None, None, "2026-11-01 10:00", None,
                                            "on", "partial"),
        (False, "Workplan cannot be completed while 1 planned service(s) remain. Complete or remove them first")),
    "collection_not_found": (
        lambda logic: logic.change_collection_status("coll-unknown", "Not installed", "2026-11-01 08:00", None),
        (False, "Collection coll-unknown not found")),
    "collection_mixed_statuses": (
        lambda logic: logic.change_collection_status(IDS.coll_mixed, "Not installed", "2026-11-01 08:00", None),
        (False, "Operation cancelled: Collection cannot contain both installed and not-installed components. "
         "Select components with the same installation status. No changes have been made.")),
    "collection_installed_without_bike": (
        lambda logic: logic.change_collection_status(IDS.coll_gravel_set, "Installed", "2026-11-01 08:00", None),
        (False, "Operation cancelled: Collections being changed to 'Installed' status must be assigned to a bike. "
         "Assign this collection to a bike. No changes have been made.")),
    "collection_unknown_bike": (
        lambda logic: logic.change_collection_status(IDS.coll_gravel_set, "Not installed", "2026-11-01 08:00",
                                                     "bike-unknown"),
        (False, "Bike not found: bike-unknown")),
    "collection_already_installed": (
        lambda logic: logic.change_collection_status(IDS.coll_gravel_set, "Installed", "2026-11-01 08:00",
                                                     IDS.bike_road),
        (False, {"type": "complete_failure", "summary": "Failed to update any components in collection",
                 "total_count": 2, "success_count": 0, "successful_components": [],
                 "failed_components": [
                     {"name": "Gravel tire", "error": "Component status for Gravel tire is already set to: Installed."},
                     {"name": "Bremseklosser bak æøå",
                      "error": "Component status for Bremseklosser bak æøå is already set to: Installed."}]})),
}


@pytest.mark.parametrize("name", list(REFUSALS))
def test_refusal_changes_nothing(app, operation_delta, name):
    """Each validation refuses on the dataset as it is and leaves every value unchanged"""
    operation, expected = REFUSALS[name]
    assert operation(app.business_logic) == expected
    assert operation_delta() == {}
