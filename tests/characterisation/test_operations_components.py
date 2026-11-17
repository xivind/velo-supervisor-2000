"""Characterisation of component, history, quick swap, component type, delete and config operations.

Each test runs one operation on the recalculated synthetic dataset and compares the delta it
leaves, in stored values, derived values and the config file, with
tests/fixtures/expected/op_<name>.json (see the operation_delta fixture). The values in each
docstring are worked out by hand from tests/fixtures/dataset.py and the code as it is today.
Setup that an operation needs and the dataset lacks is named in the test's docstring; its
effects are part of the delta.
"""

import json
import sqlite3
from dataclasses import asdict

import pytest
from fixtures.dataset import IDS
from fixtures.expected import assert_matches_expected
from integrity.snapshot import stored_state

DATASET_IDS = set(asdict(IDS).values())
DELETE_REFUSALS = [
    (
        "Components",
        IDS.comp_wheel_offset,
        (
            False,
            (
                "Cannot delete component Rear wheel as it is part of collection: Mixed parts. Remove it from the "
                "collection first."
            ),
            IDS.comp_wheel_offset,
            IDS.bike_road,
            IDS.coll_mixed,
        ),
    ),
    (
        "Collections",
        IDS.coll_mixed,
        (
            False,
            (
                "Cannot delete collection Mixed parts as it still contains components. Remove all components from "
                "collection before deleting."
            ),
            None,
            None,
            None,
        ),
    ),
    (
        "ComponentTypes",
        "Chain",
        (False, "Component type Chain is in use by 1 components and cannot be deleted", None, None, None),
    ),
    (
        "Workplans",
        IDS.wp_drivetrain,
        (
            False,
            "Cannot delete workplan as it has 2 linked service(s). Remove or move these services before deleting.",
            None,
            None,
            None,
        ),
    ),
    (
        "ComponentHistory",
        IDS.hist_tire,
        (
            False,
            f"Cannot delete initial history record {IDS.hist_tire} for component Gravel tire as service records exist",
            IDS.comp_tire_time,
            IDS.bike_gravel,
            None,
        ),
    ),
]


def _execute(app, sql, parameters):
    connection = sqlite3.connect(app.db_path)
    try:
        connection.execute(sql, parameters)
        connection.commit()
    finally:
        connection.close()


def _assert_new_component(app, component_id):
    assert component_id not in DATASET_IDS
    assert component_id in stored_state(app.db_path)["components"]


def test_create_installed_component(app, operation_delta):
    """An installed component gets a history record and is recalculated at once.

    Road tire on bike-road from 2026-06-01 08:00: road rides Jun..Oct 2026, 5 x 50 = 250 km;
    lifetime remaining 4000 - 250 = 3750, OK (threshold 200); no service, so service next
    1000 - 250 = 750, OK. Days to the frozen now: 30+31+31+30+31 = 153 to 2026-11-01, plus 15 =
    168; remaining 365 - 168 = 197, OK (threshold 30). Tire is not mandatory and road has one,
    within the max of 2, so bike-road stays compliant and the result is True. Tire in_use 2.
    """
    success, message, component_id = app.business_logic.create_component(
        None,
        "Installed",
        "2026-06-01 08:00",
        "Road tire",
        "Tire",
        IDS.bike_road,
        "4000",
        "1000",
        "200",
        "365",
        "",
        "30",
        "450",
        0,
        "Tubeless",
    )
    assert (success, message) == (True, "Component Road tire successfully created")
    _assert_new_component(app, component_id)
    assert_matches_expected("op_create_component_installed", operation_delta())


def test_create_not_installed_component(app, operation_delta):
    """A component created as not installed gets no history; the alternate method sets its values.

    Spare cassette with a 200 km offset: distance 200, lifetime remaining 6000 - 200 = 5800, OK
    (threshold 100); service next is the full interval 1000, OK, as the offset does not count for
    service. No bike, so no compliance check. Cassette in_use 2.
    """
    success, message, component_id = app.business_logic.create_component(
        None,
        "Not installed",
        "2026-11-01 08:00",
        "Spare cassette",
        "Cassette",
        "None",
        "6000",
        "1000",
        "100",
        "",
        "",
        "",
        "700",
        200,
        None,
    )
    assert (success, message) == (True, "Component Spare cassette successfully created")
    _assert_new_component(app, component_id)
    assert_matches_expected("op_create_component_not_installed", operation_delta())


def test_modify_component_details(app, operation_delta):
    """Offset, name, cost and notes of the rear wheel change; distance follows the new offset.

    Ridden 2000 - 1000 (old offset) = 1000 km, plus the new 500 offset = 1500; lifetime remaining
    10000 - 1500 = 8500, OK. Service next stays 2000 - 1000 = 1000, OK. The message names the
    component as it was before the update ("Rear wheel"). The stored history record and planned
    service keep the old name in component_name; the derived values show the new one.
    """
    result = app.business_logic.modify_component_details(
        IDS.comp_wheel_offset,
        "Installed",
        "2025-03-01 08:00",
        "Rear wheel DT",
        "Rear wheel",
        IDS.bike_road,
        "10000",
        "2000",
        "200",
        "",
        "",
        "",
        "2300",
        500,
        "Bought used, offset corrected",
    )
    assert result == (True, "Component Rear wheel updated.", IDS.comp_wheel_offset)
    assert_matches_expected("op_modify_component_details", operation_delta())


def test_modify_component_details_type_change(app, operation_delta):
    """Changing the type recounts both types: Saddle in_use 0, Bottle cage 1.

    Spare saddle has no history, so the alternate method recalculates it: distance 300 - 300 + 300
    = 300 (the offset), lifetime remaining 20000 - 300 = 19700, OK. No bike, no compliance check.
    """
    result = app.business_logic.modify_component_details(
        IDS.comp_no_history,
        "Not installed",
        "2025-05-01 08:00",
        "Spare saddle",
        "Bottle cage",
        "None",
        "20000",
        "",
        "200",
        "",
        "",
        "",
        "1200",
        300,
        None,
    )
    assert result == (True, "Component Spare saddle updated.", IDS.comp_no_history)
    assert_matches_expected("op_modify_component_details_type_change", operation_delta())


def test_install_component(app, operation_delta):
    """Spare saddle installed on bike-gravel 2026-09-01 08:00, its first history record.

    Gravel rides Sep..Oct 2026, 2 x 20 = 40, plus the 300 offset: distance 340; lifetime remaining
    20000 - 340 = 19660, OK. bike-gravel still needs attention (the tire). bike-gravel lacks the
    mandatory Chain and Rear wheel, so the result is "warning". coll-mixed now holds components on
    two bikes.
    """
    success, message = app.business_logic.create_history_record(
        IDS.comp_no_history, "Installed", IDS.bike_gravel, "2026-09-01 08:00", "Fitted for a long ride"
    )
    assert (success, message) == (
        "warning",
        (
            "Successfully processed history records and related services for Spare saddle. Use of component "
            "types on Gravel bike are not compliant. See bike details for more information"
        ),
    )
    assert_matches_expected("op_history_install", operation_delta())


def test_uninstall_component(app, operation_delta):
    """Chain uninstalled from bike-road 2026-10-01 08:00.

    New record marker: 440 + road Apr..Sep 2026, 6 x 50 = 300, = 740; distance 740, lifetime
    remaining 2260, OK. Since svc-chain-2: gravel Oct 2025..Feb 2026, 5 x 20 = 100, plus road
    Apr..Sep 2026, 300, = 400; service next 100, equal to the threshold: OK. The record takes the
    component's bike (bike-road); the component is stored with no bike. bike-road keeps its OK
    cassette and wheel: "All components healthy".
    """
    success, message = app.business_logic.create_history_record(
        IDS.comp_chain_moved, "Not installed", IDS.bike_road, "2026-10-01 08:00"
    )
    assert (success, message) == (True, "Successfully processed history records and related services for Chain")
    assert_matches_expected("op_history_uninstall", operation_delta())


def test_retire_component(app, operation_delta):
    """Bremseklosser bak æøå retired on bike-gravel 2026-10-01 08:00.

    Marker: gravel Jan 2025..Sep 2026, 21 x 20 = 420; distance 420, lifetime remaining 1080, OK.
    The component keeps bike-gravel. coll-gravel-set now holds a retired member. bike-gravel lacks
    the mandatory Chain and Rear wheel, so the result is "warning".
    """
    success, message = app.business_logic.create_history_record(
        IDS.comp_pads_norwegian, "Retired", IDS.bike_gravel, "2026-10-01 08:00"
    )
    assert (success, message) == (
        "warning",
        (
            "Successfully processed history records and related services for Bremseklosser bak æøå. Use of "
            "component types on Gravel bike are not compliant. See bike details for more information"
        ),
    )
    assert_matches_expected("op_history_retire", operation_delta())


def test_update_history_record(app, operation_delta):
    """hist-chain-gravel moved from 2025-08-01 to 2025-07-15 08:00, with a note.

    Markers: gravel 300; off_gravel 300 + gravel Jul 2025..Feb 2026, 8 x 20 = 160, = 460; road_2
    460. Distance 460 + road Apr..Oct 2026, 350, = 810; lifetime remaining 2190, OK. svc-chain-2
    marker: road Apr..Jun 2025, 150, plus gravel Jul..Sep 2025, 60, = 210. Since svc-chain-2
    unchanged: 450, service next 50, "Due for service".
    """
    success, message = app.business_logic.update_history_record(
        IDS.hist_chain_gravel, "2025-07-15 08:00", "Moved early for a gravel trip"
    )
    assert (success, message) == (True, "Successfully processed history records and related services for Chain")
    assert_matches_expected("op_history_update", operation_delta())


def test_quick_swap_to_not_installed_with_existing_component(app, operation_delta):
    """Chain swapped for a spare chain on 2026-10-01 08:00; the old chain becomes not installed.

    Setup: the spare chain is created not installed with create_component (new:components:1). Old
    chain as in test_uninstall_component (distance 740, service next 100). Spare chain on road from
    2026-10-01: one 50 km ride; lifetime remaining 2950, service next 450, OK. The note goes on both
    new history records.
    """
    success, message, spare_id = app.business_logic.create_component(
        None,
        "Not installed",
        "2026-09-01 08:00",
        "Spare chain",
        "Chain",
        "None",
        "3000",
        "500",
        "100",
        "",
        "",
        "",
        "380",
        0,
        None,
    )
    assert (success, message) == (True, "Component Spare chain successfully created")
    _assert_new_component(app, spare_id)
    success, message = app.business_logic.quick_swap_orchestrator(
        IDS.comp_chain_moved, "Not installed", "2026-10-01 08:00", spare_id, None, "Worn, kept as spare"
    )
    assert (success, message) == (
        True,
        "Component swapped successfully: Chain set to Not installed. Spare chain installed on Road bike",
    )
    assert_matches_expected("op_quick_swap_not_installed", operation_delta())


def test_quick_swap_to_retired_with_new_component(app, operation_delta):
    """Cassette retired on 2026-10-01 08:00 and replaced by a new one created in the swap.

    Old cassette: road Jan 2025..Sep 2026, 21 x 50 = 1050; lifetime remaining 4950; since
    svc-cassette-2 to retirement: Feb..Sep 2026, 8 x 50 = 400, service next 600, OK; it keeps
    bike-road. New cassette: created not installed, then installed; one 50 km ride, lifetime
    remaining 5950, service next 950, OK. Cassette in_use 2.
    """
    new_component_data = {
        "component_name": "Cassette 11-34",
        "component_type": "Cassette",
        "service_interval": "1000",
        "lifetime_expected": "6000",
        "threshold_km": "100",
        "lifetime_expected_days": None,
        "service_interval_days": None,
        "threshold_days": None,
        "cost": "850",
        "offset": 0,
        "notes": None,
    }
    success, message = app.business_logic.quick_swap_orchestrator(
        IDS.comp_cassette_serviced, "Retired", "2026-10-01 08:00", None, new_component_data, "Worn out"
    )
    assert (success, message) == (
        True,
        "Component swapped successfully: Cassette set to Retired. Cassette 11-34 installed on Road bike",
    )
    assert_matches_expected("op_quick_swap_retired", operation_delta())


def test_create_component_type(app, operation_delta):
    """A new type is stored with its intervals and in_use 0.

    The type name is the primary key, so the expected file holds it as new:component_types:1;
    the name is checked here.
    """
    success, message = app.business_logic.modify_component_type(
        "Chainring", "15000", "", "", "", "500", "", "No", "2", "create"
    )
    assert (success, message) == (True, "Created component type Chainring")
    assert "Chainring" in stored_state(app.db_path)["component_types"]
    assert_matches_expected("op_component_type_create", operation_delta())


def test_update_component_type(app, operation_delta):
    """Chain type intervals change; existing chains keep their own (3000 km, 500 km); in_use 1"""
    success, message = app.business_logic.modify_component_type(
        "Chain", "2500", "", "400", "", "100", "", "Yes", "1", "update"
    )
    assert (success, message) == (True, "Updated component type Chain")
    assert_matches_expected("op_component_type_update", operation_delta())


def test_delete_completed_service(app, operation_delta):
    """Deleting svc-chain-2 recalculates the chain from svc-chain-1 (2025-04-01).

    Since svc-chain-1: road Apr..Jun 2025, 150, gravel Aug 2025..Feb 2026, 7 x 20 = 140, road
    Apr..Oct 2026, 350, = 640; service next 500 - 640 = -140, "Service interval exceeded", so
    bike-road needs attention.
    """
    result = app.business_logic.delete_record("Services", IDS.svc_chain_2)
    assert result == (
        True,
        f"Deleted service record with id {IDS.svc_chain_2}",
        IDS.comp_chain_moved,
        IDS.bike_road,
        None,
    )
    assert_matches_expected("op_delete_service_completed", operation_delta())


def test_delete_planned_service(app, operation_delta):
    """Deleting a planned service recalculates nothing"""
    result = app.business_logic.delete_record("Services", IDS.svc_wheel_planned)
    assert result == (
        True,
        f"Deleted service record with id {IDS.svc_wheel_planned}",
        IDS.comp_wheel_offset,
        IDS.bike_road,
        None,
    )
    assert_matches_expected("op_delete_service_planned", operation_delta())


def test_delete_history_record(app, operation_delta):
    """Deleting the chain's latest record (road_2) leaves it as uninstalled from bike-gravel on 2026-03-01.

    Distance 440, lifetime remaining 2560; since svc-chain-2 to uninstall: gravel Oct 2025..Feb
    2026, 100, service next 400, OK. The bike status updated is that of bike-gravel, the bike of
    the latest remaining record, not bike-road. The returned message is that of
    process_history_records.
    """
    result = app.business_logic.delete_record("ComponentHistory", IDS.hist_chain_road_2)
    assert result == (
        True,
        "Successfully processed history records and related services for Chain",
        IDS.comp_chain_moved,
        IDS.bike_road,
        None,
    )
    assert_matches_expected("op_delete_history", operation_delta())


def test_delete_only_history_record(app, operation_delta):
    """Deleting a component's only record (no services) makes it not installed through
    modify_component_details, dated now (2026-11-16 12:00) and with no bike; distance falls back to
    the offset, 0, so lifetime remaining 1500. The returned message is that of
    modify_component_details.
    """
    result = app.business_logic.delete_record("ComponentHistory", IDS.hist_pads_norwegian)
    assert result == (True, "Component Bremseklosser bak æøå updated.", IDS.comp_pads_norwegian, IDS.bike_gravel, None)
    assert_matches_expected("op_delete_history_only", operation_delta())


def test_delete_only_history_record_leaves_bike_status_unchanged(app):
    """Records current behaviour; see #374. Deleting a component's only history record does not
    update the status of the bike it leaves.

    Setup: svc-tire deleted first, since a first record with services cannot be deleted. Deleting
    hist-tire makes the tire not installed with no bike, leaving bike-gravel with only the OK
    pads, but bike-gravel keeps "Components need attention" from the exceeded tire until its
    status is updated again.
    """
    assert app.business_logic.delete_record("Services", IDS.svc_tire) == (
        True,
        f"Deleted service record with id {IDS.svc_tire}",
        IDS.comp_tire_time,
        IDS.bike_gravel,
        None,
    )
    result = app.business_logic.delete_record("ComponentHistory", IDS.hist_tire)
    assert result == (True, "Component Gravel tire updated.", IDS.comp_tire_time, IDS.bike_gravel, None)
    stored = stored_state(app.db_path)
    tire = stored["components"][IDS.comp_tire_time]
    assert (tire["installation_status"], tire["bike_id"]) == ("Not installed", None)
    assert stored["bikes"][IDS.bike_gravel]["service_status"] == "Components need attention"
    app.business_logic.update_bike_status(IDS.bike_gravel)
    assert stored_state(app.db_path)["bikes"][IDS.bike_gravel]["service_status"] == "All components healthy"


def test_delete_component(app, operation_delta):
    """Deleting the chain removes its 3 services and 5 history records; Chain in_use 0.

    bike-road keeps its OK cassette and wheel: "All components healthy".
    """
    result = app.business_logic.delete_record("Components", IDS.comp_chain_moved)
    assert result == (
        True,
        "Deleted component: Chain, related records deleted: 3 service(s), 5 history record(s)",
        None,
        IDS.bike_road,
        None,
    )
    assert_matches_expected("op_delete_component", operation_delta())


def test_delete_collection(app, operation_delta):
    """Setup: coll-gravel-set emptied in the database, since only an empty collection can be deleted"""
    _execute(app, "UPDATE collections SET components = NULL WHERE collection_id = ?", (IDS.coll_gravel_set,))
    result = app.business_logic.delete_record("Collections", IDS.coll_gravel_set)
    assert result == (True, f"Deleted collection with id {IDS.coll_gravel_set}", None, None, None)
    assert_matches_expected("op_delete_collection", operation_delta())


def test_delete_component_type(app, operation_delta):
    """Bottle cage is the one unused type"""
    result = app.business_logic.delete_record("ComponentTypes", "Bottle cage")
    assert result == (True, "Deleted component type: Bottle cage", None, None, None)
    assert_matches_expected("op_delete_component_type", operation_delta())


def test_delete_workplan(app, operation_delta):
    """Setup: svc-pads-retired unlinked from wp-brake-check in the database, since only a workplan
    without services can be deleted.
    """
    _execute(app, "UPDATE services SET workplan_id = NULL WHERE service_id = ?", (IDS.svc_pads_retired,))
    result = app.business_logic.delete_record("Workplans", IDS.wp_brake_check)
    assert result == (True, f"Deleted workplan with id {IDS.wp_brake_check}", None, None, None)
    assert_matches_expected("op_delete_workplan", operation_delta())


def test_delete_incident(app, operation_delta):
    """Deleting inc-drivetrain clears incident_id on its two services"""
    result = app.business_logic.delete_record("Incidents", IDS.inc_drivetrain)
    assert result == (True, f"Deleted incident report with id {IDS.inc_drivetrain}", None, None, None)
    assert_matches_expected("op_delete_incident", operation_delta())


@pytest.mark.parametrize(
    ("table_selector", "record_id", "expected"), DELETE_REFUSALS, ids=[refusal[0] for refusal in DELETE_REFUSALS]
)
def test_delete_refusal_changes_nothing(app, operation_delta, table_selector, record_id, expected):
    """Each guard of delete_record refuses on the dataset as it is and leaves every value unchanged"""
    assert app.business_logic.delete_record(table_selector, record_id) == expected
    assert operation_delta() == {}


def test_write_config_file_paths(app, operation_delta):
    """Both paths are replaced; button_sorting is added with the defaults, as the file had none"""
    success, message = app.utils.write_config(
        "file_paths", db_path="/data/vs2000.sqlite", strava_tokens="/secrets/strava_tokens.json"
    )
    assert (success, message) == (True, "File paths updated.")
    assert_matches_expected("op_config_file_paths", operation_delta())


def test_write_config_button_sorting(app, operation_delta):
    """Only bike_details is submitted, so button_sorting holds only bike_details: the defaults are
    added only when the file has no button_sorting at all.
    """
    order = [
        "new-component",
        "new-collection",
        "install-existing",
        "plan-services",
        "complete-services",
        "new-workplan",
        "new-incident",
    ]
    success, message = app.utils.write_config("button_sorting", button_sorting_bike_details=json.dumps(order))
    assert (success, message) == (True, "Button sorting updated.")
    assert_matches_expected("op_config_button_sorting", operation_delta())


def test_write_config_system_settings(app, operation_delta):
    """Verbose logging enabled; button_sorting added with the defaults"""
    success, message = app.utils.write_config("system_settings", verbose_logging=True)
    assert (success, message) == (True, "System settings updated. Verbose logging: enabled.")
    assert_matches_expected("op_config_system_settings", operation_delta())


def test_write_config_unknown_form_type_writes_nothing(app):
    before = app.utils.config_path().read_bytes()
    assert app.utils.write_config("unknown") == (False, "Unknown form type: unknown")
    assert app.utils.config_path().read_bytes() == before
