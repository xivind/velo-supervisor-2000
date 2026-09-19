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
