"""Workplans and incidents derive their links through services; retirement is blocked by planned services"""

import json
from test_service_status import seed_component, seed_rides, add_twin_component


def add_incident(modules, incident_id, component_ids, status="Open", description="Chain skips"):
    modules.database_model.Incidents.create(incident_id=incident_id, incident_date="2026-02-10 10:00",
                                            incident_status=status, incident_severity="Monitor",
                                            incident_affected_component_ids=json.dumps(component_ids) if component_ids else None,
                                            incident_affected_bike_id="bike-1", incident_description=description,
                                            resolution_date=None, resolution_notes=None)


def test_retire_blocked_while_planned_services_exist(modules):
    seed_component(modules)
    seed_rides(modules)
    business_logic = modules.business_logic
    database_manager = modules.database_manager
    assert business_logic.create_planned_services(["comp-1"], "Replace chain")[0]

    success, message = business_logic.create_history_record("comp-1", "Retired", "bike-1", "2026-03-01 10:00")
    assert not success and "planned service" in message
    assert database_manager.read_component("comp-1").installation_status == "Installed"

    success, message = business_logic.create_history_record("comp-1", "Not installed", "bike-1", "2026-03-01 10:00")
    assert success, message

    planned_id = list(database_manager.read_planned_services_by_component("comp-1"))[0].service_id
    assert business_logic.delete_record("Services", planned_id)[0]
    success, message = business_logic.create_history_record("comp-1", "Retired", "bike-1", "2026-03-02 10:00")
    assert success, message


def test_quick_swap_to_retired_refused_before_any_change(modules):
    seed_component(modules)
    seed_rides(modules)
    business_logic = modules.business_logic
    database_manager = modules.database_manager
    assert business_logic.create_planned_services(["comp-1"], "Replace chain")[0]
    component_count = database_manager.read_all_components_objects().count()

    new_component_data = {"component_name": "New chain", "component_type": "Chain", "service_interval": "1000",
                          "lifetime_expected": "3000", "threshold_km": "100", "lifetime_expected_days": "",
                          "service_interval_days": "", "threshold_days": "", "cost": "", "offset": 0, "notes": ""}
    success, message = business_logic.quick_swap_orchestrator("comp-1", "Retired", "2026-03-01 10:00", None, new_component_data)

    assert not success and "planned service" in message
    assert database_manager.read_all_components_objects().count() == component_count
    assert database_manager.read_component("comp-1").installation_status == "Installed"


def test_collection_retire_refused_before_any_change(modules):
    seed_component(modules)
    add_twin_component(modules, "comp-2")
    seed_rides(modules)
    business_logic = modules.business_logic
    database_manager = modules.database_manager
    modules.database_model.Collections.create(collection_id="col-1", collection_name="Wheelset",
                                              components=json.dumps(["comp-1", "comp-2"]), bike_id="bike-1",
                                              sub_collections=None, updated_date=None, comment=None)
    assert business_logic.create_planned_services(["comp-2"], "True the wheel")[0]

    success, message = business_logic.change_collection_status("col-1", "Retired", "2026-03-01 10:00", None)

    assert not success and "Chain twin" in message and "No changes have been made" in message
    assert database_manager.read_component("comp-1").installation_status == "Installed"


def test_history_notes_are_stored_and_blank_is_null(modules):
    seed_component(modules)
    seed_rides(modules)
    business_logic = modules.business_logic
    database_manager = modules.database_manager

    assert business_logic.create_history_record("comp-1", "Not installed", "bike-1", "2026-02-20 10:00", notes="Moved to winter bike")[0]
    assert business_logic.create_history_record("comp-1", "Installed", "bike-1", "2026-02-25 10:00", notes="   ")[0]

    notes_by_reason = {record.update_reason: record.notes for record in database_manager.read_subset_component_history("comp-1")}
    assert notes_by_reason["Not installed"] == "Moved to winter bike"
    assert notes_by_reason["Installed"] is None


def test_quick_swap_stores_notes_on_both_records(modules):
    seed_component(modules)
    seed_rides(modules)
    business_logic = modules.business_logic
    database_manager = modules.database_manager
    new_component_data = {"component_name": "New chain", "component_type": "Chain", "service_interval": "1000",
                          "lifetime_expected": "3000", "threshold_km": "100", "lifetime_expected_days": "",
                          "service_interval_days": "", "threshold_days": "", "cost": "", "offset": 0, "notes": ""}

    success, message = business_logic.quick_swap_orchestrator("comp-1", "Retired", "2026-03-01 10:00", None,
                                                              new_component_data, notes="Worn out")
    assert success, message

    assert database_manager.read_latest_history_record("comp-1").notes == "Worn out"
    new_component = [component for component in database_manager.read_all_components_objects()
                     if component.component_name == "New chain"][0]
    assert database_manager.read_latest_history_record(new_component.component_id).notes == "Worn out"


def test_workplan_from_incident_plans_services_once(modules):
    seed_component(modules)
    seed_rides(modules)
    add_incident(modules, "inc-1", ["comp-1"], description="Chain skips under load")
    business_logic = modules.business_logic
    database_manager = modules.database_manager

    success, message, workplan_id = business_logic.create_workplan("2026-04-01 10:00", "Planned", "Small",
                                                                   "Fix skipping", None, None, source_incident_id="inc-1")
    assert success, message

    planned = list(database_manager.read_planned_services_by_workplan(workplan_id))
    assert [(service.component_id, service.incident_id, service.description) for service in planned] == \
        [("comp-1", "inc-1", "Chain skips under load")]
    assert [workplan.workplan_id for workplan in database_manager.read_workplans_by_incident("inc-1")] == [workplan_id]
    assert [incident.incident_id for incident in database_manager.read_incidents_by_workplan(workplan_id)] == ["inc-1"]


def test_workplan_completion_rules(modules):
    seed_component(modules)
    seed_rides(modules)
    add_incident(modules, "inc-1", ["comp-1"])
    business_logic = modules.business_logic
    database_manager = modules.database_manager
    success, message, workplan_id = business_logic.create_workplan("2026-03-01 10:00", "Planned", "Small",
                                                                   "Spring", None, None, source_incident_id="inc-1")
    assert success, message

    success, message = business_logic.update_workplan(workplan_id, workplan_status="Done",
                                                      completion_date="2026-03-02 10:00", update_mode="partial")
    assert not success and "planned service" in message

    planned_id = list(database_manager.read_planned_services_by_workplan(workplan_id))[0].service_id
    assert business_logic.complete_services([planned_id], "2026-03-05 10:00")[0]

    success, message = business_logic.update_workplan(workplan_id, workplan_status="Done",
                                                      completion_date="2026-03-04 10:00", update_mode="partial")
    assert not success and "latest service" in message

    success, message = business_logic.update_workplan(workplan_id, workplan_status="Done",
                                                      completion_date="2099-01-01 10:00", update_mode="partial")
    assert not success and "future" in message

    success, message = business_logic.update_workplan(workplan_id, workplan_status="Done", completion_date="2026-03-05 12:00",
                                                      close_linked_incidents="on", update_mode="partial")
    assert success, message
    assert database_manager.read_single_workplan(workplan_id).workplan_status == "Done"
    assert database_manager.read_single_incident_report("inc-1").incident_status == "Resolved"

    success, message = business_logic.update_workplan(workplan_id, "2026-03-01 10:00", "Planned", "Small",
                                                      "Spring reopened", None, None)
    assert success, message
    assert database_manager.read_single_workplan(workplan_id).workplan_status == "Planned"


def test_incident_create_and_update_without_workplan(modules):
    seed_component(modules)
    business_logic = modules.business_logic
    database_manager = modules.database_manager

    success, message = business_logic.create_incident_record("2026-02-10 10:00", "Open", "Monitor", ["comp-1"],
                                                             "bike-1", "Rattle", None, None)
    assert success, message
    incident = list(database_manager.read_all_incidents())[0]

    success, message = business_logic.update_incident_record(incident.incident_id, "2026-02-10 10:00", "Resolved",
                                                             "Monitor", ["comp-1"], "bike-1", "Rattle",
                                                             "2026-02-11 10:00", "Tightened")
    assert success, message
    assert database_manager.read_single_incident_report(incident.incident_id).incident_status == "Resolved"


def test_deleting_incident_keeps_services_but_unlinks_them(modules):
    seed_component(modules)
    add_incident(modules, "inc-1", ["comp-1"])
    business_logic = modules.business_logic
    database_manager = modules.database_manager
    assert business_logic.create_planned_services(["comp-1"], "Replace chain", incident_id="inc-1")[0]

    assert business_logic.delete_record("Incidents", "inc-1")[0]

    planned = list(database_manager.read_planned_services_by_component("comp-1"))
    assert len(planned) == 1 and planned[0].incident_id is None


def test_page_payloads_build_with_planned_and_completed_services(modules):
    seed_component(modules)
    seed_rides(modules)
    add_incident(modules, "inc-1", ["comp-1"])
    business_logic = modules.business_logic
    database_manager = modules.database_manager
    modules.database_model.Collections.create(collection_id="col-1", collection_name="Drivetrain",
                                              components=json.dumps(["comp-1"]), bike_id="bike-1",
                                              sub_collections=None, updated_date=None, comment=None)
    assert business_logic.create_service_record("comp-1", "2026-02-01 10:00", "First wax")[0]
    success, message, workplan_id = business_logic.create_workplan("2026-04-01 10:00", "Planned", "Small",
                                                                   "Spring", None, None, source_incident_id="inc-1")
    assert success, message

    workplan_payload = business_logic.get_workplan_details(workplan_id)
    assert workplan_payload["workplan_data"]["component_names"] == ["Chain"]
    assert workplan_payload["workplan_data"]["bike_names"] == ["Test bike"]
    assert (workplan_payload["workplan_data"]["completed_count"], workplan_payload["workplan_data"]["total_count"]) == (0, 1)
    assert workplan_payload["all_services_completed"] is False
    assert len(workplan_payload["planned_services_data"]) == 1
    assert workplan_payload["services_data"] is None
    assert [incident[0] for incident in workplan_payload["incidents_data"]] == ["inc-1"]

    bike_payload = business_logic.get_bike_details("bike-1")
    assert bike_payload["plan_services_preselect"] == ["comp-1"]
    assert len(bike_payload["planned_services_data"]) == 1
    assert workplan_id in bike_payload["planned_workplans"]["bike_workplans"]["bike-1"]["workplan_ids"]

    component_payload = business_logic.get_component_details("comp-1")
    assert len(component_payload["planned_services_data"]) == 1
    assert len(component_payload["service_history_data"]) == 1
    assert component_payload["plan_services_preselect"] == ["comp-1"]
    assert component_payload["open_incidents_for_component"][0][0] == "inc-1"
    assert component_payload["oldest_history_date"] == "2026-01-01 10:00"
    assert len(component_payload["component_history_data"][0]) == 8

    collection_payload = business_logic.get_collection_details("col-1")
    assert collection_payload["plan_services_preselect"] == ["comp-1"]

    for payload in [business_logic.get_incident_reports(), business_logic.get_workplans(),
                    business_logic.get_bike_overview(), business_logic.get_component_overview()]:
        assert payload
