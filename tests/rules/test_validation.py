"""Every refusal of the six validate_* methods, plus one accepted case each.

A refusal is driven through the public operation that runs the validator when one reaches it,
and the test asserts that nothing changed (an empty operation_delta). Where the refusal needs
setup the dataset lacks, the setup's delta is taken first and the refusal must add nothing to
it. Where no operation reaches the branch, or the operation answers before the validator does,
the validator is called directly; the docstring says so.
"""

import pytest
from fixtures.dataset import IDS

DATE_FORMAT_HINT = "Expected format: YYYY-MM-DD HH:MM (e.g., 2024-12-14 23:34)"
NEW_CHAIN = {
    "component_name": "New chain",
    "component_type": "Chain",
    "service_interval": "500",
    "lifetime_expected": "3000",
    "threshold_km": "100",
    "lifetime_expected_days": None,
    "service_interval_days": None,
    "threshold_days": None,
    "cost": "400",
    "offset": 0,
    "notes": None,
}


def assert_refused_after_setup(operation_delta, refusal, expected):
    """The refusal returns expected and adds nothing to the delta the setup left"""
    setup_delta = operation_delta()
    assert refusal() == expected
    assert operation_delta() == setup_delta


def test_validate_history_record_refuses_unknown_component(app, operation_delta):
    """Records current behaviour: the not-found branch formats its message from the missing
    component, so create_history_record raises AttributeError instead of refusing. Nothing is
    written.
    """
    with pytest.raises(AttributeError):
        app.business_logic.create_history_record("comp-unknown", "Installed", IDS.bike_road, "2026-11-01 08:00")
    assert operation_delta() == {}


def test_validate_history_record_refuses_invalid_date_format(app, operation_delta):
    result = app.business_logic.create_history_record(
        IDS.comp_chain_moved, "Not installed", IDS.bike_road, "2026-11-01"
    )
    assert result == (False, f"Invalid date format: '2026-11-01'. {DATE_FORMAT_HINT}")
    assert operation_delta() == {}


def test_validate_history_record_refuses_future_date(app, operation_delta):
    result = app.business_logic.create_history_record(
        IDS.comp_chain_moved, "Not installed", IDS.bike_road, "2026-11-20 08:00"
    )
    assert result == (False, "Updated date cannot be in the future. Component: Chain")
    assert operation_delta() == {}


def test_validate_history_record_refuses_date_before_creation(app, operation_delta):
    """The chain's first record is 2025-01-01 08:00"""
    result = app.business_logic.create_history_record(
        IDS.comp_chain_moved, "Not installed", IDS.bike_road, "2024-12-01 08:00"
    )
    assert result == (
        False,
        "Date for new status cannot be at or before component creation date: 2025-01-01 08:00. Component: Chain",
    )
    assert operation_delta() == {}


def test_validate_history_record_refuses_retired_component(app, operation_delta):
    result = app.business_logic.create_history_record(
        IDS.comp_pads_retired, "Installed", IDS.bike_retired, "2026-11-01 08:00"
    )
    assert result == (False, "Status cannot be changed on a retired component: Commuter brake pads")
    assert operation_delta() == {}


def test_validate_history_record_refuses_date_before_latest_record(app, operation_delta):
    """After the chain's first record (2025-01-01) but before its latest (2026-04-01)"""
    result = app.business_logic.create_history_record(
        IDS.comp_chain_moved, "Not installed", IDS.bike_road, "2026-01-01 08:00"
    )
    assert result == (
        False,
        (
            "Component status changes must be done chronologically. Date for new status cannot "
            "be at or before date for the last status: 2026-04-01 08:00. Component: Chain"
        ),
    )
    assert operation_delta() == {}


def test_validate_history_record_refuses_same_status(app, operation_delta):
    result = app.business_logic.create_history_record(
        IDS.comp_chain_moved, "Installed", IDS.bike_road, "2026-11-01 08:00"
    )
    assert result == (False, "Component status for Chain is already set to: Installed.")
    assert operation_delta() == {}


def test_validate_history_record_refuses_uninstalling_never_installed(app, operation_delta):
    result = app.business_logic.create_history_record(IDS.comp_no_history, "Not installed", None, "2026-11-01 08:00")
    assert result == (False, "Component Spare saddle is not installed and can therefore not be set to 'Not installed'.")
    assert operation_delta() == {}


def test_validate_history_record_refuses_installing_without_bike(app, operation_delta):
    result = app.business_logic.create_history_record(IDS.comp_no_history, "Installed", "", "2026-11-01 08:00")
    assert result == (
        False,
        "Status cannot be set to Installed without specifying bike. Spare saddle is currently not assigned to a bike.",
    )
    assert operation_delta() == {}


def test_validate_history_record_refuses_retiring_with_planned_services(app, operation_delta):
    """The chain has svc-chain-planned"""
    result = app.business_logic.create_history_record(
        IDS.comp_chain_moved, "Retired", IDS.bike_road, "2026-11-01 08:00"
    )
    assert result == (False, "Chain has 1 planned service(s). Complete or delete them before retiring the component")
    assert operation_delta() == {}


def test_validate_history_record_refuses_retiring_before_latest_service(app, operation_delta):
    """The cassette's latest service is svc-cassette-2 on 2026-02-01 08:00"""
    result = app.business_logic.create_history_record(
        IDS.comp_cassette_serviced, "Retired", IDS.bike_road, "2026-01-01 08:00"
    )
    assert result == (
        False,
        "A retired component cannot be serviced. Set retire date after latest service date: 2026-02-01 08:00",
    )
    assert operation_delta() == {}


def test_validate_history_record_refuses_unknown_history_record(app):
    """Called directly: update_history_record reads the record before validating and raises on an
    unknown ID, so no operation reaches this branch.
    """
    result = app.business_logic.validate_history_record(
        "edit history", IDS.comp_chain_moved, "hist-unknown", "2026-11-01 08:00", "Installed", IDS.bike_road
    )
    assert result == (False, "History record not found: hist-unknown")


def test_validate_history_record_refuses_edit_before_previous_record(app, operation_delta):
    """hist-chain-off-road (2025-07-01) follows hist-chain-road-1 (2025-01-01)"""
    result = app.business_logic.update_history_record(IDS.hist_chain_off_road, "2025-01-01 08:00")
    assert result == (False, "Updated date must be after previous installation record date: 2025-01-01 08:00")
    assert operation_delta() == {}


def test_validate_history_record_refuses_edit_after_next_record(app, operation_delta):
    """hist-chain-off-road (2025-07-01) comes before hist-chain-gravel (2025-08-01)"""
    result = app.business_logic.update_history_record(IDS.hist_chain_off_road, "2025-08-01 08:00")
    assert result == (False, "Updated date must be before next installation record date: 2025-08-01 08:00")
    assert operation_delta() == {}


def test_validate_history_record_refuses_first_record_after_first_service(app, operation_delta):
    """hist-chain-road-1 moved to 2025-05-01: before the next record (2025-07-01) but after svc-chain-1
    (2025-04-01)
    """
    result = app.business_logic.update_history_record(IDS.hist_chain_road_1, "2025-05-01 08:00")
    assert result == (
        False,
        "First installation date for component Chain cannot be at or after first service date: 2025-04-01 08:00",
    )
    assert operation_delta() == {}


def test_validate_history_record_accepts_valid_input(app):
    """The message says "service record" although it validates a history record"""
    result = app.business_logic.validate_history_record(
        "create history", IDS.comp_chain_moved, "hist-new", "2026-11-01 08:00", "Not installed", IDS.bike_road
    )
    assert result == (True, "Validation of service record for Chain passed")


def test_validate_quick_swap_refuses_component_not_installed(app, operation_delta):
    result = app.business_logic.quick_swap_orchestrator(
        IDS.comp_no_history, "Not installed", "2026-11-01 08:00", None, NEW_CHAIN
    )
    assert result == (False, "Component must be installed to be swapped")
    assert operation_delta() == {}


def test_validate_quick_swap_refuses_invalid_fate(app, operation_delta):
    result = app.business_logic.quick_swap_orchestrator(
        IDS.comp_chain_moved, "Sold", "2026-11-01 08:00", None, NEW_CHAIN
    )
    assert result == (False, "Invalid fate selection")
    assert operation_delta() == {}


def test_validate_quick_swap_refuses_component_without_bike(app):
    """Called directly with the chain's bike cleared in memory: an installed component always has
    a bike in stored data, so no operation reaches this branch.
    """
    chain = app.database_manager.read_component(IDS.comp_chain_moved)
    chain.bike_id = None
    result = app.business_logic.validate_quick_swap(chain, "Not installed", None, NEW_CHAIN)
    assert result == (False, "Old component has no bike assignment")


def test_validate_quick_swap_refuses_retiring_with_planned_services(app, operation_delta):
    """The chain has svc-chain-planned. Refused before the new component is created"""
    result = app.business_logic.quick_swap_orchestrator(
        IDS.comp_chain_moved, "Retired", "2026-11-01 08:00", None, NEW_CHAIN
    )
    assert result == (
        False,
        (
            "Chain has 1 planned service(s). Complete or delete them before retiring the "
            "component. No changes have been made."
        ),
    )
    assert operation_delta() == {}


def test_validate_quick_swap_refuses_unknown_new_component(app, operation_delta):
    result = app.business_logic.quick_swap_orchestrator(
        IDS.comp_chain_moved, "Not installed", "2026-11-01 08:00", "comp-unknown", None
    )
    assert result == (False, "Selected component not found")
    assert operation_delta() == {}


def test_validate_quick_swap_refuses_new_component_not_available(app, operation_delta):
    result = app.business_logic.quick_swap_orchestrator(
        IDS.comp_chain_moved, "Not installed", "2026-11-01 08:00", IDS.comp_cassette_serviced, None
    )
    assert result == (False, "Selected component is not available for installation")
    assert operation_delta() == {}


def test_validate_quick_swap_refuses_new_component_of_other_type(app, operation_delta):
    result = app.business_logic.quick_swap_orchestrator(
        IDS.comp_chain_moved, "Not installed", "2026-11-01 08:00", IDS.comp_no_history, None
    )
    assert result == (False, "Components must be of the same type. Cannot swap Chain with Saddle.")
    assert operation_delta() == {}


def test_validate_quick_swap_refuses_new_component_without_name(app, operation_delta):
    result = app.business_logic.quick_swap_orchestrator(
        IDS.comp_chain_moved, "Not installed", "2026-11-01 08:00", None, {**NEW_CHAIN, "component_name": ""}
    )
    assert result == (False, "Component name is required")
    assert operation_delta() == {}


def test_validate_quick_swap_refuses_new_component_data_of_other_type(app, operation_delta):
    result = app.business_logic.quick_swap_orchestrator(
        IDS.comp_chain_moved, "Not installed", "2026-11-01 08:00", None, {**NEW_CHAIN, "component_type": "Cassette"}
    )
    assert result == (False, "New component type must match old component type: Chain")
    assert operation_delta() == {}


def test_validate_quick_swap_refuses_missing_new_component(app, operation_delta):
    result = app.business_logic.quick_swap_orchestrator(
        IDS.comp_chain_moved, "Not installed", "2026-11-01 08:00", None, None
    )
    assert result == (False, "Must provide either new_component_id or new_component_data")
    assert operation_delta() == {}


def test_validate_quick_swap_accepts_valid_input(app):
    chain = app.database_manager.read_component(IDS.comp_chain_moved)
    assert app.business_logic.validate_quick_swap(chain, "Not installed", None, NEW_CHAIN) == (True, "")


def test_validate_collection_refuses_unknown_collection(app):
    """Called directly: change_collection_status answers "Collection ... not found" itself before
    it validates
    """
    result = app.business_logic.validate_collection("coll-unknown", [IDS.comp_tire_time], None)
    assert result == (False, "Collection not found: coll-unknown")


def test_validate_collection_refuses_unknown_component(app):
    """Called directly: only a collection that lists a deleted component reaches this, and the
    collection pages fail on one first (#372)
    """
    result = app.business_logic.validate_collection(IDS.coll_mixed, ["comp-unknown"], None)
    assert result == (False, "Operation cancelled: Component comp-unknown not found. No changes have been made.")


def test_validate_collection_refuses_component_in_other_collection(app):
    """Called directly: through change_collection_status this needs a component listed in two
    collections, which update_collection allows (#375), but which of the two
    read_collection_by_component then returns is not defined
    """
    result = app.business_logic.validate_collection(IDS.coll_mixed, [IDS.comp_tire_time], None)
    assert result == (
        False,
        (
            "Operation cancelled: Component Gravel tire already belongs to collection Gravel set. "
            "Remove it from that collection first. No changes have been made."
        ),
    )


def test_validate_collection_refuses_retired_member(app, operation_delta):
    """Setup: coll-mixed reduced to the retired pads with update_collection, which does not
    validate (#375)
    """
    assert app.business_logic.update_collection(IDS.coll_mixed, "Mixed parts", [IDS.comp_pads_retired], None)[0]
    assert_refused_after_setup(
        operation_delta,
        lambda: app.business_logic.change_collection_status(IDS.coll_mixed, "Not installed", "2026-11-01 08:00", None),
        (
            False,
            (
                "Operation cancelled: Bulk operations cannot be performed on collections containing retired "
                "components. Retired components: Commuter brake pads. Remove retired components from this "
                "collection first. No changes have been made."
            ),
        ),
    )


def test_validate_collection_refuses_mixed_installation_statuses(app, operation_delta):
    result = app.business_logic.change_collection_status(IDS.coll_mixed, "Not installed", "2026-11-01 08:00", None)
    assert result == (
        False,
        (
            "Operation cancelled: Collection cannot contain both installed and not-installed "
            "components. Select components with the same installation status. No changes have been "
            "made."
        ),
    )
    assert operation_delta() == {}


def test_validate_collection_refuses_components_on_several_bikes(app, operation_delta):
    """Setup: the road cassette added to coll-gravel-set with update_collection. The bike names come
    from a set, so their order is not fixed and each is checked on its own.
    """
    assert app.business_logic.update_collection(
        IDS.coll_gravel_set, "Gravel set", [IDS.comp_tire_time, IDS.comp_cassette_serviced], None
    )[0]
    setup_delta = operation_delta()
    success, message = app.business_logic.change_collection_status(
        IDS.coll_gravel_set, "Not installed", "2026-11-01 08:00", None
    )
    assert success is False
    assert message.startswith(
        "Operation cancelled: All installed components in a collection must be on the same "
        "bike. Found components on bikes: "
    )
    assert "Road bike" in message and "Gravel bike" in message
    assert message.endswith(". Select components from the same bike. No changes have been made.")
    assert operation_delta() == setup_delta


def test_validate_collection_refuses_installing_without_bike(app, operation_delta):
    result = app.business_logic.change_collection_status(IDS.coll_gravel_set, "Installed", "2026-11-01 08:00", None)
    assert result == (
        False,
        (
            "Operation cancelled: Collections being changed to 'Installed' status must be assigned "
            "to a bike. Assign this collection to a bike. No changes have been made."
        ),
    )
    assert operation_delta() == {}


def test_validate_collection_refuses_retiring_with_planned_services(app, operation_delta):
    """Setup: coll-mixed reduced to the rear wheel, which has svc-wheel-planned. Refused before any
    member changes
    """
    assert app.business_logic.update_collection(IDS.coll_mixed, "Mixed parts", [IDS.comp_wheel_offset], None)[0]
    assert_refused_after_setup(
        operation_delta,
        lambda: app.business_logic.change_collection_status(
            IDS.coll_mixed, "Retired", "2026-11-01 08:00", IDS.bike_road
        ),
        (
            False,
            (
                "Operation cancelled: Components with planned services cannot be retired: Rear wheel. Complete or "
                "delete their planned services first. No changes have been made."
            ),
        ),
    )


def test_validate_collection_refuses_unknown_bike(app, operation_delta):
    result = app.business_logic.change_collection_status(
        IDS.coll_gravel_set, "Not installed", "2026-11-01 08:00", "bike-unknown"
    )
    assert result == (False, "Bike not found: bike-unknown")
    assert operation_delta() == {}


def test_change_collection_status_refuses_empty_collection(app, operation_delta):
    """Not a validate_collection branch: change_collection_status refuses before validating.
    Setup: coll-mixed emptied with update_collection.
    """
    assert app.business_logic.update_collection(IDS.coll_mixed, "Mixed parts", [], None)[0]
    assert_refused_after_setup(
        operation_delta,
        lambda: app.business_logic.change_collection_status(IDS.coll_mixed, "Not installed", "2026-11-01 08:00", None),
        (False, "No components found in collection"),
    )


def test_validate_collection_accepts_valid_input(app):
    result = app.business_logic.validate_collection(
        IDS.coll_gravel_set, [IDS.comp_tire_time, IDS.comp_pads_norwegian], IDS.bike_gravel, "Not installed"
    )
    assert result == (True, f"Validation of collection {IDS.coll_gravel_set} passed")


def test_validate_service_record_refuses_unknown_service(app):
    """Called directly: update_service_record and complete_services both look the service up and
    answer before validating
    """
    result = app.business_logic.validate_service_record(
        "edit service", IDS.comp_chain_moved, "svc-unknown", "2026-11-01 08:00"
    )
    assert result == (False, "Service record not found: svc-unknown")


def test_validate_service_record_refuses_unknown_component(app, operation_delta):
    """The message carries the generated service ID"""
    success, message = app.business_logic.create_service_record("comp-unknown", "2026-11-01 08:00", "Waxed")
    assert success is False
    assert message.startswith("Associated component for service record ") and message.endswith(" not found")
    assert operation_delta() == {}


def test_validate_service_record_refuses_retired_component(app, operation_delta):
    result = app.business_logic.create_service_record(IDS.comp_pads_retired, "2025-08-01 08:00", "Cleaned pads")
    assert result == (
        False,
        "Services cannot be planned, completed or changed on a retired component: Commuter brake pads",
    )
    assert operation_delta() == {}


def test_validate_service_record_refuses_short_description(app, operation_delta):
    result = app.business_logic.create_service_record(IDS.comp_tire_time, None, "Fix", status="Planned")
    assert result == (False, "Description must be at least 5 characters. Component: Gravel tire")
    assert operation_delta() == {}


def test_validate_service_record_refuses_invalid_planned_date(app, operation_delta):
    result = app.business_logic.create_service_record(
        IDS.comp_tire_time, None, "Replace tire", status="Planned", planned_date="next week"
    )
    assert result == (False, f"Invalid date format: 'next week'. {DATE_FORMAT_HINT}")
    assert operation_delta() == {}


def test_validate_service_record_refuses_second_planned_service_in_workplan(app, operation_delta):
    """The chain has svc-chain-planned in wp-drivetrain"""
    result = app.business_logic.create_service_record(
        IDS.comp_chain_moved, None, "Replace chain", IDS.wp_drivetrain, "Planned"
    )
    assert result == (False, "Component Chain already has a planned service in this workplan")
    assert operation_delta() == {}


def test_validate_service_record_refuses_completing_completed_service(app, operation_delta):
    success, message = app.business_logic.complete_services([IDS.svc_chain_2], "2026-11-01 08:00")
    assert success is False
    assert message["failed_components"] == [
        {"name": "Chain", "error": "Only planned services can be completed. Component: Chain"}
    ]
    assert operation_delta() == {}


def test_validate_service_record_refuses_invalid_service_date(app, operation_delta):
    result = app.business_logic.create_service_record(IDS.comp_chain_moved, "2026-11-01", "Waxed")
    assert result == (False, f"Invalid date format: '2026-11-01'. {DATE_FORMAT_HINT}")
    assert operation_delta() == {}


def test_validate_service_record_refuses_never_installed_component(app, operation_delta):
    result = app.business_logic.create_service_record(IDS.comp_no_history, "2026-11-01 08:00", "Cleaned saddle")
    assert result == (
        False,
        "Services cannot be registered to components that have never been installed. Component: Spare saddle",
    )
    assert operation_delta() == {}


def test_validate_service_record_refuses_date_before_creation(app, operation_delta):
    """Completing svc-wheel-planned before the wheel was installed (2025-03-01 08:00)"""
    success, message = app.business_logic.complete_services([IDS.svc_wheel_planned], "2025-02-01 08:00")
    assert success is False
    assert message["failed_components"] == [
        {
            "name": "Rear wheel",
            "error": "Service date cannot be at or before component creation date 2025-03-01 "
            "08:00. Component: Rear wheel",
        }
    ]
    assert operation_delta() == {}


def test_validate_service_record_refuses_future_date(app, operation_delta):
    success, message = app.business_logic.complete_services([IDS.svc_wheel_planned], "2026-11-20 08:00")
    assert success is False
    assert message["failed_components"] == [
        {"name": "Rear wheel", "error": "Service date cannot be in the future. Component: Rear wheel"}
    ]
    assert operation_delta() == {}


def test_validate_service_record_refuses_date_after_done_workplan(app, operation_delta):
    """wp-brake-check was completed on 2025-04-01 10:00"""
    result = app.business_logic.create_service_record(
        IDS.comp_chain_moved, "2026-11-01 08:00", "Waxed", IDS.wp_brake_check
    )
    assert result == (
        False,
        (
            "Service date cannot be after the completion date of its workplan (2025-04-01 10:00). "
            "Reopen the workplan first. Component: Chain"
        ),
    )
    assert operation_delta() == {}


def test_validate_service_record_refuses_empty_service_date(app, operation_delta):
    """Completing needs a service date, both in the complete services modal and when the service
    form switches a planned service to completed
    """
    empty_date = "Date cannot be empty. Expected format: YYYY-MM-DD HH:MM (e.g., 2024-12-14 23:34)"
    success, message = app.business_logic.complete_services([IDS.svc_wheel_planned], "")
    assert success is False
    assert message["failed_components"] == [{"name": "Rear wheel", "error": empty_date}]
    result = app.business_logic.update_service_record(
        IDS.comp_wheel_offset, IDS.svc_wheel_planned, None, "True rear wheel", None, "Completed"
    )
    assert result == (False, empty_date)
    assert operation_delta() == {}


def test_validate_service_record_accepts_valid_input(app):
    result = app.business_logic.validate_service_record(
        "create service", IDS.comp_chain_moved, "svc-new", "2026-11-01 08:00"
    )
    assert result == (True, "Validation of service record for Chain passed")


def test_validate_threshold_configuration_refuses_missing_km_threshold(app, operation_delta):
    result = app.business_logic.modify_component_type("Chainring", "15000", "", "", "", "", "", "No", "1", "create")
    assert result == (False, "Threshold (km) is required when distance-based intervals are configured")
    assert operation_delta() == {}


def test_validate_threshold_configuration_refuses_missing_days_threshold(app, operation_delta):
    result = app.business_logic.modify_component_type("Chainring", "", "365", "", "", "", "", "No", "1", "create")
    assert result == (False, "Threshold (days) is required when time-based intervals are configured")
    assert operation_delta() == {}


def test_validate_threshold_configuration_refuses_zero_km_threshold(app, operation_delta):
    result = app.business_logic.modify_component_type("Chainring", "15000", "", "", "", "0", "", "No", "1", "create")
    assert result == (False, "Threshold (km) must be greater than 0")
    assert operation_delta() == {}


def test_validate_threshold_configuration_refuses_km_threshold_above_interval(app, operation_delta):
    result = app.business_logic.modify_component_type(
        "Chainring", "15000", "", "500", "", "600", "", "No", "1", "create"
    )
    assert result == (False, "Threshold (km) must be less than or equal to the smallest interval (500 km)")
    assert operation_delta() == {}


def test_validate_threshold_configuration_refuses_zero_days_threshold(app, operation_delta):
    result = app.business_logic.modify_component_type("Chainring", "", "365", "", "", "", "0", "No", "1", "create")
    assert result == (False, "Threshold (days) must be greater than 0")
    assert operation_delta() == {}


def test_validate_threshold_configuration_refuses_days_threshold_above_interval(app, operation_delta):
    result = app.business_logic.modify_component_type("Chainring", "", "365", "", "90", "", "100", "No", "1", "create")
    assert result == (False, "Threshold (days) must be less than or equal to the smallest interval (90 days)")
    assert operation_delta() == {}


def test_validate_threshold_configuration_accepts_valid_input(app):
    assert app.business_logic.validate_threshold_configuration(3000, 500, 365, 90, 100, 30) == (
        True,
        "Validation passed",
    )


def test_validate_workplan_completion_refuses_remaining_planned_services(app, operation_delta):
    """wp-drivetrain still has svc-chain-planned"""
    result = app.business_logic.update_workplan(
        IDS.wp_drivetrain, None, "Done", None, None, "2026-11-01 10:00", None, "on", "partial"
    )
    assert result == (
        False,
        "Workplan cannot be completed while 1 planned service(s) remain. Complete or remove them first",
    )
    assert operation_delta() == {}


def test_validate_workplan_completion_refuses_invalid_date_format(app, operation_delta):
    """wp-brake-check is Done on 2025-04-01 10:00; a new completion date is validated again"""
    result = app.business_logic.update_workplan(
        IDS.wp_brake_check, None, "Done", None, None, "2025-04-01", None, None, "partial"
    )
    assert result == (False, f"Invalid date format: '2025-04-01'. {DATE_FORMAT_HINT}")
    assert operation_delta() == {}


def test_validate_workplan_completion_refuses_future_date(app, operation_delta):
    result = app.business_logic.update_workplan(
        IDS.wp_brake_check, None, "Done", None, None, "2026-11-20 10:00", None, None, "partial"
    )
    assert result == (False, "Completion date cannot be in the future")
    assert operation_delta() == {}


def test_validate_workplan_completion_refuses_date_before_latest_service(app, operation_delta):
    """The workplan's only service, svc-pads-retired, is on 2025-04-01 08:00"""
    result = app.business_logic.update_workplan(
        IDS.wp_brake_check, None, "Done", None, None, "2025-04-01 07:00", None, None, "partial"
    )
    assert result == (False, "Completion date cannot be before the latest service in this workplan (2025-04-01 08:00)")
    assert operation_delta() == {}


def test_validate_workplan_completion_accepts_valid_input(app):
    result = app.business_logic.validate_workplan_completion(IDS.wp_brake_check, "2025-04-01 10:00")
    assert result == (True, "Workplan can be completed")


def test_refusals_leave_the_app_healthy(app, client):
    """A refusal is logged as a warning, not an error, so it does not make the app unhealthy (#103).
    One refusal per validator, plus bulk and orchestrating callers that repeat a refusal from
    below them.
    """
    logic = app.business_logic
    refusals = [
        lambda: logic.create_history_record(IDS.comp_chain_moved, "Not installed", IDS.bike_road, "2026-11-20 08:00"),
        lambda: logic.create_history_record(IDS.comp_chain_moved, "Retired", IDS.bike_road, "2026-11-01 08:00"),
        lambda: logic.quick_swap_orchestrator(IDS.comp_chain_moved, "Retired", "2026-11-01 08:00", None, NEW_CHAIN),
        lambda: logic.quick_swap_orchestrator(
            IDS.comp_chain_moved, "Not installed", "2026-11-01 08:00", IDS.comp_no_history, None
        ),
        lambda: logic.change_collection_status(IDS.coll_mixed, "Not installed", "2026-11-01 08:00", None),
        lambda: logic.create_service_record(IDS.comp_chain_moved, "2026-11-20 08:00", "Waxed"),
        lambda: logic.create_planned_services([IDS.comp_chain_moved], "Replace chain", IDS.wp_drivetrain),
        lambda: logic.complete_services([IDS.svc_wheel_planned], "2026-11-20 08:00"),
        lambda: logic.update_workplan(
            IDS.wp_drivetrain, None, "Done", None, None, "2026-11-01 10:00", None, None, "partial"
        ),
        lambda: logic.modify_component_type("Chainring", "15000", "", "", "", "0", "", "No", "1", "create"),
        lambda: logic.delete_record("Workplans", IDS.wp_drivetrain),
    ]
    for refusal in refusals:
        assert refusal()[0] is False
    response = client.get("/health")
    assert (response.status_code, response.json()["latest_errors"]) == (200, [])
