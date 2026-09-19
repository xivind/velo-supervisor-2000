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
