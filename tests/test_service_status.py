"""Planned services must be invisible to health computation"""


def seed_component(modules, component_id="comp-1", bike_id="bike-1"):
    """Create one bike and one installed component with an installation record"""
    Bikes = modules.database_model.Bikes
    Components = modules.database_model.Components
    ComponentHistory = modules.database_model.ComponentHistory
    Bikes.create(bike_id=bike_id, bike_name="Test bike", bike_retired="False",
                 service_status=None, total_distance=0, notes=None)
    Components.create(component_id=component_id, bike_id=bike_id, component_name="Chain",
                      component_type="Chain", component_distance=0, component_distance_offset=0,
                      installation_status="Installed", service_interval=1000, service_interval_days=None,
                      service_next=None, service_next_days=None, service_status=None,
                      lifetime_expected=3000, lifetime_expected_days=None, lifetime_remaining=None,
                      lifetime_remaining_days=None, lifetime_status=None, threshold_km=100,
                      threshold_days=None, updated_date="2026-01-01 10:00", cost=None, notes=None)
    ComponentHistory.create(history_id="hist-1", component_id=component_id, bike_id=bike_id,
                            component_name="Chain", updated_date="2026-01-01 10:00",
                            update_reason="Installed", distance_marker=0, notes=None)
    return modules.database_manager


def test_completed_only_reads_skip_planned(modules):
    database_manager = seed_component(modules)
    Services = modules.database_model.Services
    Services.create(service_id="svc-planned", component_id="comp-1", component_name="Chain",
                    bike_id=None, service_date=None, distance_marker=None, description="Planned wax",
                    workplan_id=None, status="Planned", incident_id=None, planned_date=None)
    Services.create(service_id="svc-done", component_id="comp-1", component_name="Chain",
                    bike_id="bike-1", service_date="2026-02-01 10:00", distance_marker=0,
                    description="Waxed", workplan_id=None, status="Completed", incident_id=None,
                    planned_date=None)

    assert database_manager.read_latest_service_record("comp-1").service_id == "svc-done"
    assert database_manager.read_oldest_service_record("comp-1").service_id == "svc-done"
    assert [service.service_id for service in database_manager.read_subset_service_history("comp-1")] == ["svc-done"]
    assert [service.service_id for service in database_manager.read_planned_services_by_component("comp-1")] == ["svc-planned"]
    assert [service.service_id for service in database_manager.read_all_services_by_component("comp-1")] == ["svc-planned", "svc-done"]


def test_effective_planned_date_prefers_service(modules):
    from types import SimpleNamespace
    utils = modules.utils
    workplan = SimpleNamespace(due_date="2026-05-01 10:00")
    assert utils.get_effective_planned_date(SimpleNamespace(planned_date="2026-04-01 10:00"), workplan) == "2026-04-01 10:00"
    assert utils.get_effective_planned_date(SimpleNamespace(planned_date=None), workplan) == "2026-05-01 10:00"
    assert utils.get_effective_planned_date(SimpleNamespace(planned_date=None), None) is None


def test_workplan_and_incident_tuples_derive_from_services(modules):
    database_manager = seed_component(modules)
    utils = modules.utils
    model = modules.database_model
    model.Bikes.create(bike_id="bike-2", bike_name="Winter bike", bike_retired="False",
                       service_status=None, total_distance=0, notes=None)
    model.Workplans.create(workplan_id="wp-1", due_date="2026-03-01 10:00", workplan_status="Planned",
                           workplan_size="Small", workplan_description="Spring service",
                           completion_date=None, completion_notes=None)
    model.Workplans.create(workplan_id="wp-empty", due_date="2026-03-01 10:00", workplan_status="Planned",
                           workplan_size="Small", workplan_description="Nothing yet",
                           completion_date=None, completion_notes=None)
    model.Incidents.create(incident_id="inc-1", incident_date="2026-02-10 10:00", incident_status="Open",
                           incident_severity="Monitor", incident_affected_component_ids='["comp-1"]',
                           incident_affected_bike_id=None, incident_description="Chain skips",
                           resolution_date=None, resolution_notes=None)
    model.Services.create(service_id="svc-done", component_id="comp-1", component_name="Chain",
                          bike_id="bike-2", service_date="2026-02-01 10:00", distance_marker=0,
                          description="Waxed on winter bike", workplan_id="wp-1", status="Completed",
                          incident_id=None, planned_date=None)
    model.Services.create(service_id="svc-planned", component_id="comp-1", component_name="Chain",
                          bike_id=None, service_date=None, distance_marker=None, description="Replace chain",
                          workplan_id="wp-1", status="Planned", incident_id="inc-1", planned_date=None)

    workplan_tuple = utils.get_workplan_data_tuple(database_manager.read_single_workplan("wp-1"), database_manager)
    assert len(workplan_tuple) == 14
    assert workplan_tuple[4] == ["comp-1"] and workplan_tuple[5] == ["Chain"]
    assert workplan_tuple[6] == ["bike-1", "bike-2"] and workplan_tuple[7] == ["Test bike", "Winter bike"]
    assert workplan_tuple[12] == "Chain - Spring service - Test bike"
    assert workplan_tuple[13] == {"completed": 1, "total": 2}

    empty_tuple = utils.get_workplan_data_tuple(database_manager.read_single_workplan("wp-empty"), database_manager)
    assert empty_tuple[4] == [] and empty_tuple[6] == [] and empty_tuple[13] is None
    assert empty_tuple[12] == "Nothing yet"

    workplan_names = utils.get_workplan_names_dict(database_manager)
    incident_tuple = utils.get_incident_data_tuple(database_manager.read_single_incident_report("inc-1"),
                                                   database_manager, workplan_names)
    assert len(incident_tuple) == 16
    assert incident_tuple[13] == [("wp-1", "Chain - Spring service - Test bike")]
    assert incident_tuple[14:] == (1, 0)

    planned_tuple = utils.get_planned_service_data_tuple(database_manager.read_single_service_record("svc-planned"),
                                                         database_manager, workplan_names)
    assert planned_tuple == ("svc-planned", "comp-1", "Chain", "Replace chain", "wp-1",
                             "Chain - Spring service - Test bike", "inc-1", "2026-03-01 10:00", None,
                             "Installed", "2026-01-01 10:00")


def seed_rides(modules, bike_id="bike-1"):
    """Rides before and after the service dates used below, so distances are not zero"""
    Rides = modules.database_model.Rides
    for ride_id, record_time, distance in [("ride-1", "2026-01-10 10:00", 100.0),
                                           ("ride-2", "2026-02-15 10:00", 200.0),
                                           ("ride-3", "2026-03-10 10:00", 50.0)]:
        Rides.create(ride_id=ride_id, bike_id=bike_id, record_time=record_time, ride_name=ride_id,
                     ride_distance=distance, moving_time="1:00:00", commute="False")


def snapshot_health(modules, component_id="comp-1"):
    component = modules.database_manager.read_component(component_id)
    return (component.service_next, component.service_status, component.component_distance)


def test_status_change_keeps_workplan_link_on_newest_service(modules):
    seed_component(modules)
    seed_rides(modules)
    business_logic = modules.business_logic
    database_manager = modules.database_manager
    assert business_logic.create_service_record("comp-1", "2026-02-01 10:00", "Waxed chain", workplan_id="wp-1")[0]

    success, message = business_logic.create_history_record("comp-1", "Not installed", "bike-1", "2026-02-20 10:00")
    assert success, message

    assert database_manager.read_latest_service_record("comp-1").workplan_id == "wp-1"


def test_delete_keeps_workplan_link_on_remaining_service(modules):
    seed_component(modules)
    seed_rides(modules)
    business_logic = modules.business_logic
    database_manager = modules.database_manager
    assert business_logic.create_service_record("comp-1", "2026-02-01 10:00", "First wax", workplan_id="wp-1")[0]
    assert business_logic.create_service_record("comp-1", "2026-03-01 10:00", "Second wax")[0]
    newest_id = database_manager.read_latest_service_record("comp-1").service_id

    success, message, _, _, _ = business_logic.delete_record("Services", newest_id)
    assert success, message

    assert database_manager.read_latest_service_record("comp-1").workplan_id == "wp-1"


def test_planned_services_do_not_touch_health(modules):
    seed_component(modules)
    seed_rides(modules)
    business_logic = modules.business_logic
    database_manager = modules.database_manager
    success, message = business_logic.create_service_record("comp-1", "2026-02-01 10:00", "Waxed chain")
    assert success, message
    before = snapshot_health(modules)
    service_before = database_manager.read_latest_service_record("comp-1")

    success, message = business_logic.create_planned_services(["comp-1"], "Plan new wax", planned_date="2026-04-01 10:00")
    assert success, message

    assert snapshot_health(modules) == before
    assert database_manager.read_latest_service_record("comp-1").distance_marker == service_before.distance_marker
    planned = list(database_manager.read_planned_services_by_component("comp-1"))
    assert len(planned) == 1
    assert (planned[0].service_date, planned[0].bike_id, planned[0].distance_marker) == (None, None, None)
    assert (planned[0].component_name, planned[0].planned_date, planned[0].incident_id) == ("Chain", "2026-04-01 10:00", None)


def test_complete_then_revert_matches_state_before_completion(modules):
    seed_component(modules)
    seed_rides(modules)
    business_logic = modules.business_logic
    database_manager = modules.database_manager
    model = modules.database_model
    model.Incidents.create(incident_id="inc-1", incident_date="2026-02-10 10:00", incident_status="Open",
                           incident_severity="Monitor", incident_affected_component_ids='["comp-1"]',
                           incident_affected_bike_id=None, incident_description="Chain skips",
                           resolution_date=None, resolution_notes=None)
    assert business_logic.create_service_record("comp-1", "2026-02-01 10:00", "First wax")[0]
    baseline = snapshot_health(modules)

    success, message = business_logic.create_planned_services(["comp-1"], "Second wax", workplan_id="wp-1", incident_id="inc-1")
    assert success, message
    planned_id = list(database_manager.read_planned_services_by_component("comp-1"))[0].service_id

    success, message = business_logic.complete_services([planned_id], "2026-03-01 10:00", "done early")
    assert success, message
    assert message["incident_hints"] and "can be closed" in message["incident_hints"][0]
    completed = database_manager.read_single_service_record(planned_id)
    assert (completed.status, completed.service_date, completed.bike_id) == ("Completed", "2026-03-01 10:00", "bike-1")
    assert (completed.workplan_id, completed.incident_id) == ("wp-1", "inc-1")
    assert completed.description == "Second wax\ndone early"
    assert completed.distance_marker == 200.0
    assert database_manager.read_latest_service_record("comp-1").service_id == planned_id
    assert snapshot_health(modules) != baseline

    success, message = business_logic.update_service_record("comp-1", planned_id, None, completed.description,
                                                             workplan_id="wp-1", status="Planned", incident_id="inc-1")
    assert success, message
    reverted = database_manager.read_single_service_record(planned_id)
    assert (reverted.status, reverted.service_date, reverted.bike_id, reverted.distance_marker) == ("Planned", None, None, None)
    assert (reverted.workplan_id, reverted.incident_id) == ("wp-1", "inc-1")
    assert snapshot_health(modules) == baseline


def add_twin_component(modules, component_id):
    """Second installed component on bike-1 with the same settings as comp-1"""
    modules.database_model.Components.create(component_id=component_id, bike_id="bike-1", component_name="Chain twin",
                                             component_type="Chain", component_distance=0, component_distance_offset=0,
                                             installation_status="Installed", service_interval=1000,
                                             service_interval_days=None, service_next=None, service_next_days=None,
                                             service_status=None, lifetime_expected=3000, lifetime_expected_days=None,
                                             lifetime_remaining=None, lifetime_remaining_days=None, lifetime_status=None,
                                             threshold_km=100, threshold_days=None, updated_date="2026-01-01 10:00",
                                             cost=None, notes=None)
    modules.database_model.ComponentHistory.create(history_id=f"hist-{component_id}", component_id=component_id,
                                                   bike_id="bike-1", component_name="Chain twin",
                                                   updated_date="2026-01-01 10:00", update_reason="Installed",
                                                   distance_marker=0, notes=None)


def test_revert_matches_deletion(modules):
    seed_component(modules)
    add_twin_component(modules, "comp-2")
    seed_rides(modules)
    business_logic = modules.business_logic
    database_manager = modules.database_manager
    for component_id in ["comp-1", "comp-2"]:
        assert business_logic.create_service_record(component_id, "2026-02-01 10:00", "First wax")[0]
        assert business_logic.create_service_record(component_id, "2026-03-01 10:00", "Second wax")[0]

    reverted_id = database_manager.read_latest_service_record("comp-1").service_id
    success, message = business_logic.update_service_record("comp-1", reverted_id, None, "Second wax", status="Planned")
    assert success, message

    deleted_id = database_manager.read_latest_service_record("comp-2").service_id
    success, message, _, _, _ = business_logic.delete_record("Services", deleted_id)
    assert success, message

    assert snapshot_health(modules, "comp-1") == snapshot_health(modules, "comp-2")
    assert snapshot_health(modules, "comp-1")[0] is not None
    assert (database_manager.read_latest_service_record("comp-1").distance_marker ==
            database_manager.read_latest_service_record("comp-2").distance_marker)

    only_id = database_manager.read_latest_service_record("comp-1").service_id
    assert business_logic.update_service_record("comp-1", only_id, None, "First wax", status="Planned")[0]
    only_deleted_id = database_manager.read_latest_service_record("comp-2").service_id
    assert business_logic.delete_record("Services", only_deleted_id)[0]
    assert database_manager.read_latest_service_record("comp-1") is None
    assert snapshot_health(modules, "comp-1") == snapshot_health(modules, "comp-2")


def test_service_validation_rules(modules):
    seed_component(modules)
    seed_rides(modules)
    business_logic = modules.business_logic
    database_manager = modules.database_manager
    assert business_logic.create_service_record("comp-1", "2026-02-01 10:00", "First wax")[0]

    success, message = business_logic.create_planned_services(["comp-1"], "abc")
    assert not success and "at least 5" in str(message)

    success, message = business_logic.create_planned_services(["comp-1"], "Plan with bad date", planned_date="next week")
    assert not success and "format" in str(message).lower()

    assert business_logic.create_planned_services(["comp-1"], "Plan A", workplan_id="wp-x")[0]
    success, message = business_logic.create_planned_services(["comp-1"], "Plan B", workplan_id="wp-x")
    assert not success and "already has a planned service" in str(message)
    assert business_logic.create_planned_services(["comp-1"], "Plan C without workplan")[0]

    planned_id = list(database_manager.read_planned_services_by_workplan("wp-x"))[0].service_id
    success, message = business_logic.complete_services([planned_id], "2025-12-01 10:00")
    assert not success and "creation date" in str(message)
    success, message = business_logic.complete_services([planned_id], "2099-01-01 10:00")
    assert not success and "future" in str(message)

    completed_id = database_manager.read_latest_service_record("comp-1").service_id
    success, message = business_logic.complete_services([completed_id], "2026-03-01 10:00")
    assert not success and "Only planned services" in str(message)

    database_manager.write_component_details("comp-1", {"installation_status": "Retired"})
    success, message = business_logic.complete_services([planned_id], "2026-03-01 10:00")
    assert not success and "retired" in str(message).lower()
    success, message = business_logic.create_planned_services(["comp-1"], "Plan on retired")
    assert not success and "retired" in str(message).lower()
    success, message = business_logic.update_service_record("comp-1", completed_id, None, "First wax", status="Planned")
    assert not success and "retired" in str(message).lower()
    assert database_manager.read_single_service_record(completed_id).status == "Completed"


def test_complete_after_workplan_done_is_refused(modules):
    seed_component(modules)
    seed_rides(modules)
    business_logic = modules.business_logic
    database_manager = modules.database_manager
    model = modules.database_model
    model.Workplans.create(workplan_id="wp-done", due_date="2026-02-01 10:00", workplan_status="Done",
                           workplan_size="Small", workplan_description="Finished",
                           completion_date="2026-02-20 10:00", completion_notes=None)
    assert business_logic.create_planned_services(["comp-1"], "Reverted wax", workplan_id="wp-done")[0]
    planned_id = list(database_manager.read_planned_services_by_workplan("wp-done"))[0].service_id

    success, message = business_logic.complete_services([planned_id], "2026-03-01 10:00")
    assert not success and "Reopen the workplan" in str(message)

    success, message = business_logic.complete_services([planned_id], "2026-02-15 10:00")
    assert success, message
