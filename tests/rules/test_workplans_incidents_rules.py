"""Workplan, incident and history rules: links through services, titles, notes, retirement.

Each test states one rule and checks it on the recalculated synthetic dataset, through stored
values and the named derived values of snapshot_now. New IDs read new:<table>:<n> there.
Validation refusals are in test_validation.py.
"""

from fixtures.dataset import IDS

NEW_WORKPLAN = "new:workplans:1"


def test_retire_blocked_while_planned_services_exist(app, operation_delta):
    """The chain has svc-chain-planned: retiring is refused and changes nothing, uninstalling is
    allowed, and once the planned service is deleted the chain can be retired
    """
    result = app.business_logic.create_history_record(
        IDS.comp_chain_moved, "Retired", IDS.bike_road, "2026-11-01 08:00"
    )
    assert result == (False, "Chain has 1 planned service(s). Complete or delete them before retiring the component")
    assert operation_delta() == {}

    assert app.business_logic.create_history_record(
        IDS.comp_chain_moved, "Not installed", IDS.bike_road, "2026-11-01 08:00"
    )[0]
    assert app.business_logic.delete_record("Services", IDS.svc_chain_planned)[0]
    assert app.business_logic.create_history_record(IDS.comp_chain_moved, "Retired", IDS.bike_road, "2026-11-02 08:00")[
        0
    ]
    assert app.database_manager.read_component(IDS.comp_chain_moved).installation_status == "Retired"


def test_history_notes_are_stored_and_blank_is_null(app, snapshot_now):
    """A note is stored on the new record; a note of only spaces is stored as NULL, on create and
    on edit
    """
    logic = app.business_logic
    assert logic.create_history_record(
        IDS.comp_chain_moved, "Not installed", IDS.bike_road, "2026-10-01 08:00", "Moved to winter bike"
    )[0]
    assert logic.create_history_record(IDS.comp_chain_moved, "Installed", IDS.bike_gravel, "2026-10-15 08:00", "   ")[0]
    assert logic.update_history_record(IDS.hist_chain_gravel, "2025-08-01 08:00", "  ")[0]
    history = snapshot_now()["stored"]["component_history"]
    assert history["new:component_history:1"]["notes"] == "Moved to winter bike"
    assert history["new:component_history:2"]["notes"] is None
    assert history[IDS.hist_chain_gravel]["notes"] is None


def test_quick_swap_stores_notes_on_both_records(app, snapshot_now):
    """The cassette retired and replaced by a new one: both new history records carry the note"""
    new_cassette = {
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
        IDS.comp_cassette_serviced, "Retired", "2026-10-01 08:00", None, new_cassette, "Worn out"
    )
    assert success, message
    new_records = {
        key: row for key, row in snapshot_now()["stored"]["component_history"].items() if key.startswith("new:")
    }
    assert sorted((row["component_id"], row["update_reason"], row["notes"]) for row in new_records.values()) == [
        (IDS.comp_cassette_serviced, "Retired", "Worn out"),
        ("new:components:1", "Installed", "Worn out"),
    ]


def test_workplan_from_incident_plans_one_service_per_component(app, snapshot_now):
    """A workplan from inc-drivetrain plans one service for each of its components, described as
    the incident, and the incident and workplan are linked through those services
    """
    success, message, _ = app.business_logic.create_workplan(
        "2026-12-01 10:00", "Planned", "Medium", "Fix skipping", None, None, None, IDS.inc_drivetrain
    )
    assert success, message
    snapshot = snapshot_now()
    planned = [row for row in snapshot["stored"]["services"].values() if row["workplan_id"] == NEW_WORKPLAN]
    assert sorted((row["component_id"], row["incident_id"], row["description"], row["status"]) for row in planned) == [
        (IDS.comp_cassette_serviced, IDS.inc_drivetrain, "Chain skips under load", "Planned"),
        (IDS.comp_chain_moved, IDS.inc_drivetrain, "Chain skips under load", "Planned"),
    ]
    derived = snapshot["derived"]
    assert [workplan_id for workplan_id, _ in derived["incident"][IDS.inc_drivetrain]["incident_workplans"]] == [
        IDS.wp_drivetrain,
        NEW_WORKPLAN,
    ]
    assert [row["incident_id"] for row in derived["workplan"][NEW_WORKPLAN]["incidents"]] == [IDS.inc_drivetrain]


def test_workplan_from_incident_plans_only_selected_components(app, snapshot_now):
    """Only the cassette is selected, so the chain gets no service in the new workplan"""
    success, message, _ = app.business_logic.create_workplan(
        "2026-12-01 10:00",
        "Planned",
        "Small",
        "Cassette only",
        None,
        None,
        None,
        IDS.inc_drivetrain,
        [IDS.comp_cassette_serviced],
    )
    assert success, message
    assert snapshot_now()["derived"]["workplan"][NEW_WORKPLAN]["component_ids"] == [IDS.comp_cassette_serviced]


def test_workplan_name_replaces_generated_title(app, snapshot_now):
    """A given name is the workplan's title; saving it blank stores NULL and the generated title,
    here the description since the workplan has no services, is used again
    """
    success, message, workplan_id = app.business_logic.create_workplan(
        "2026-12-01 10:00", "Planned", "Small", "Spring service", None, None, "Sesongstart landeveissykkel"
    )
    assert success, message
    assert snapshot_now()["derived"]["workplan"][NEW_WORKPLAN]["workplan_title"] == "Sesongstart landeveissykkel"

    assert app.business_logic.update_workplan(
        workplan_id, "2026-12-01 10:00", "Planned", "Small", "Spring service", None, None, None, None, ""
    )[0]
    snapshot = snapshot_now()
    assert snapshot["stored"]["workplans"][NEW_WORKPLAN]["workplan_name"] is None
    assert snapshot["derived"]["workplan"][NEW_WORKPLAN]["workplan_title"] == "Spring service"


def test_reopening_done_workplan_is_not_validated(app, snapshot_now):
    """wp-brake-check set back to Planned with a full update; completion rules apply only to Done"""
    result = app.business_logic.update_workplan(
        IDS.wp_brake_check,
        "2025-04-01 10:00",
        "Planned",
        "Small",
        "Check the commuter brakes",
        None,
        None,
        None,
        None,
        "Brake check",
    )
    assert result == (True, f"Updated workplan with id {IDS.wp_brake_check}")
    workplan = snapshot_now()["stored"]["workplans"][IDS.wp_brake_check]
    assert (workplan["workplan_status"], workplan["completion_date"]) == ("Planned", None)


def test_workplan_context_derives_from_services(app, snapshot_now):
    """Components, bikes, progress and title of a workplan come from its services.

    A new workplan without services has none and its description as title. svc-chain-2, done
    on the gravel bike, linked to it counts on bike-gravel although the chain is on bike-road now;
    a planned cassette service counts on the cassette's bike, bike-road. Services are read planned
    first, so the cassette and bike-road come first and name the title. Progress 1 of 2.
    """
    success, message, workplan_id = app.business_logic.create_workplan(
        "2026-12-01 10:00", "Planned", "Small", "Winter check", None, None
    )
    assert success, message
    empty = snapshot_now()["derived"]["workplan"][NEW_WORKPLAN]
    assert (empty["component_ids"], empty["bike_ids"], empty["service_progress"], empty["workplan_title"]) == (
        [],
        [],
        None,
        "Winter check",
    )

    assert app.business_logic.update_service_record(
        IDS.comp_chain_moved, IDS.svc_chain_2, "2025-10-01 08:00", "Waxed", workplan_id, "Completed"
    )[0]
    assert snapshot_now()["derived"]["workplan"][NEW_WORKPLAN]["bike_ids"] == [IDS.bike_gravel]

    assert app.business_logic.create_planned_services([IDS.comp_cassette_serviced], "Check wear", workplan_id)[0]
    workplan = snapshot_now()["derived"]["workplan"][NEW_WORKPLAN]
    assert {
        field: workplan[field]
        for field in (
            "component_ids",
            "component_names",
            "bike_ids",
            "bike_names",
            "service_progress",
            "workplan_title",
        )
    } == {
        "component_ids": [IDS.comp_cassette_serviced, IDS.comp_chain_moved],
        "component_names": ["Cassette", "Chain"],
        "bike_ids": [IDS.bike_road, IDS.bike_gravel],
        "bike_names": ["Road bike", "Gravel bike"],
        "service_progress": {"completed": 1, "total": 2},
        "workplan_title": "Cassette (+1 more) - Winter check - Road bike",
    }


def test_incident_values_derive_from_services(snapshot_now):
    """inc-drivetrain reaches wp-drivetrain through its two services, one planned and one completed.
    A service's date is its own service date, else its effective planned date.
    """
    incident = snapshot_now()["derived"]["incident"][IDS.inc_drivetrain]
    title = "Chain (+1 more) - Drivetrain overhaul - Road bike"
    assert incident["incident_workplans"] == [[IDS.wp_drivetrain, title]]
    assert (incident["planned_service_count"], incident["completed_service_count"]) == (1, 1)
    assert incident["incident_services"] == [
        {
            "service_id": IDS.svc_chain_planned,
            "component_id": IDS.comp_chain_moved,
            "component_name": "Chain",
            "status": "Planned",
            "description": "Replace chain",
            "service_date": None,
            "planned_date": None,
            "date": "2026-11-01 10:00",
            "workplan_id": IDS.wp_drivetrain,
            "workplan_name": title,
            "workplan_status": "Planned",
        },
        {
            "service_id": IDS.svc_cassette_2,
            "component_id": IDS.comp_cassette_serviced,
            "component_name": "Cassette",
            "status": "Completed",
            "description": "Deep clean",
            "service_date": "2026-02-01 08:00",
            "planned_date": None,
            "date": "2026-02-01 08:00",
            "workplan_id": IDS.wp_drivetrain,
            "workplan_name": title,
            "workplan_status": "Planned",
        },
    ]


def test_page_values_with_planned_and_completed_services(snapshot_now):
    """The values the workplan, bike, component and collection pages show for planned and completed
    services, and the incident options of the service forms
    """
    derived = snapshot_now()["derived"]
    workplan = derived["workplan"][IDS.wp_drivetrain]
    assert (workplan["details"]["component_names"], workplan["details"]["bike_names"]) == (
        ["Chain", "Cassette"],
        ["Road bike"],
    )
    assert (workplan["details"]["completed_count"], workplan["details"]["total_count"]) == (1, 2)
    assert workplan["all_services_completed"] is False
    assert [row["service_id"] for row in workplan["planned_services"]] == [IDS.svc_chain_planned]
    assert [row["service_id"] for row in workplan["services"]] == [IDS.svc_cassette_2]
    assert [row["incident_id"] for row in workplan["incidents"]] == [IDS.inc_drivetrain]
    assert derived["workplan"][IDS.wp_brake_check]["planned_services"] is None

    bike = derived["bike"][IDS.bike_road]
    assert bike["plan_services_preselect"] == [IDS.comp_cassette_serviced, IDS.comp_wheel_offset, IDS.comp_chain_moved]
    assert [row["service_id"] for row in bike["planned_services"]] == [IDS.svc_chain_planned, IDS.svc_wheel_planned]
    assert bike["workplans"]["workplan_ids"] == [IDS.wp_drivetrain]

    chain = derived["component"][IDS.comp_chain_moved]
    assert chain["plan_services_preselect"] == [IDS.comp_chain_moved]
    assert (len(chain["planned_services"]), len(chain["service_history"])) == (1, 2)
    assert chain["oldest_history_date"] == "2025-01-01 08:00"
    assert sorted(
        (row["incident_id"], row["incident_status"], row["incident_component_ids"])
        for row in derived["overview"]["incident_reports"]["service_incident_options"]
    ) == [
        (IDS.inc_drivetrain, "Open", [IDS.comp_chain_moved, IDS.comp_cassette_serviced]),
        (IDS.inc_squeal, "Resolved", [IDS.comp_pads_retired]),
    ]

    assert derived["collection"][IDS.coll_gravel_set]["plan_services_preselect"] == [
        IDS.comp_tire_time,
        IDS.comp_pads_norwegian,
    ]
