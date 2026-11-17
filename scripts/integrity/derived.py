"""Values the application computes when it builds a page but never stores.

Result is resource -> id -> {field: value}, resources bike, component, collection,
workplan, incident, component_type and overview. Positional tuples are given names
from the templates that unpack them (INCIDENT_FIELDS and the other lists below); a
tuple whose length differs from its name list raises TupleShapeError, a ValueError.
Model instances become field dicts and floats are rounded to 6 decimals, as in
snapshot.stored_state. A source that fails is recorded as {"error": ...} in its slot,
per record or, for page level sources, under overview.<source>, so one broken record
does not hide the rest; shape errors still raise.

Sources and what they contribute:
- get_bike_overview: overview.bike_overview (bike rows, open incident and planned
  workplan indexes, assigned collections); bike.overview_row
- get_bike_details(id): bike.bike_data, component_rows, count_installed, count_retired,
  sum_cost, recent_rides, planned_services, plan_services_preselect
- process_bike_compliance_report(id): bike.compliance_report
- get_component_overview: overview.component_overview (component counts);
  component.overview_row, list_row
- get_component_details(id): component.details, history, service_history, bike_name,
  days_since_service, planned_services, plan_services_preselect, oldest_history_date
- calculate_component_triggers(component): component.triggers
- calculate_percentage_reached: contributes the percentage fields of component.details
- get_component_collection_mapping: overview.component_collection_mapping
- get_all_collections: collection.summary
- get_collection_details(id): collection.collection_data, warnings, component_rows,
  plan_services_preselect
- calculate_collection_status: collection.status
- get_incident_reports: incident.<id> rows; overview.incident_reports.service_incident_options
- process_incidents: bike.incidents, component.incidents
- get_workplans: workplan.<id> rows
- process_workplans: bike.workplans, component.workplans
- get_workplan_details(id): workplan.details, all_services_completed, latest_service_date,
  incidents, services, planned_services, component_bike_names
- derive_workplan_context: workplan.context
- get_component_types: component_type.<name> rows

Left out, with the reason:
- today (every details payload): the current time, not derived from data
- bikes_data, component_types_data, all_components_data, all_collections,
  workplans_data, incident_reports_data repeated inside the per-record payloads: the
  same values are recorded once from their own source above
- open_incidents, planned_workplans repeated inside the per-record payloads: recorded
  once from the unfiltered process_incidents and process_workplans calls
"""

import json

from peewee import Model

OVERVIEW_BIKE_FIELDS = (
    "name",
    "bike_id",
    "bike_status",
    "service_status",
    "distance",
    "count_installed",
    "exceeded_max_count",
    "due_past_threshold_count",
    "compliance_report",
)
BIKE_COMPONENT_FIELDS = (
    "component_id",
    "lifetime_remaining",
    "service_next",
    "installation_status",
    "type",
    "name",
    "component_distance",
    "lifetime_status",
    "service_status",
    "cost",
    "lifetime_trigger",
    "service_trigger",
    "lifetime_remaining_days",
    "service_next_days",
    "updated_date",
)
RIDE_FIELDS = ("ride_id", "date", "name", "ride_distance", "commute")
COMPONENT_DISPLAY_FIELDS = (
    "component_id",
    "type",
    "name",
    "component_distance",
    "installation_status",
    "lifetime_status",
    "service_status",
    "bike",
    "cost",
    "lifetime_trigger",
    "service_trigger",
    "bike_id",
    "updated_date",
)
COMPONENT_LIST_FIELDS = (
    "component_id",
    "type",
    "name",
    "distance",
    "status",
    "lifetime_status",
    "service_status",
    "bike",
    "cost",
    "lifetime_remaining",
    "lifetime_remaining_days",
    "service_next",
    "service_next_days",
    "threshold_km",
    "threshold_days",
    "bike_id",
    "updated_date",
)
COMPONENT_HISTORY_FIELDS = (
    "history_id",
    "updated_date",
    "update_reason",
    "bike_id",
    "bike_name",
    "bike_total_distance",
    "mileage",
    "notes",
)
SERVICE_HISTORY_FIELDS = (
    "service_id",
    "service_date",
    "description",
    "bike_name",
    "bike_total_distance",
    "distance_marker",
    "running_total",
    "workplan_id",
    "incident_id",
    "planned_date",
)
COLLECTION_FIELDS = (
    "collection_id",
    "collection_name",
    "bike_name",
    "updated_date",
    "components",
    "bike_id",
    "comment",
    "component_details",
    "status",
    "collection_bike_mismatch",
)
COLLECTION_MAPPING_FIELDS = ("collection_id", "collection_name", "components", "bike_id", "comment", "updated_date")
INCIDENT_FIELDS = (
    "incident_id",
    "incident_date",
    "incident_status",
    "incident_severity",
    "incident_affected_component_ids",
    "affected_component_names",
    "incident_affected_bike_id",
    "affected_bike_name",
    "incident_description",
    "resolution_date",
    "resolution_notes",
    "elapsed_days",
    "incident_title",
    "incident_workplans",
    "planned_service_count",
    "completed_service_count",
    "incident_services",
)
WORKPLAN_FIELDS = (
    "workplan_id",
    "due_date",
    "workplan_status",
    "workplan_size",
    "component_ids",
    "component_names",
    "bike_ids",
    "bike_names",
    "workplan_description",
    "completion_date",
    "completion_notes",
    "elapsed_days",
    "workplan_title",
    "service_progress",
)
PLANNED_SERVICE_FIELDS = (
    "service_id",
    "component_id",
    "component_name",
    "description",
    "workplan_id",
    "workplan_name",
    "incident_id",
    "effective_planned_date",
    "planned_date",
    "installation_status",
    "oldest_history_date",
)
WORKPLAN_SERVICE_FIELDS = (
    "service_id",
    "service_date",
    "description",
    "component_id",
    "component_name",
    "workplan_id",
    "incident_id",
    "planned_date",
    "installation_status",
)
SERVICE_INCIDENT_OPTION_FIELDS = ("incident_id", "incident_title", "incident_status", "incident_component_ids")
COMPONENT_TYPE_FIELDS = (
    "component_type",
    "suggested_lifetime_expected",
    "lifetime_expected_days",
    "suggested_service_interval",
    "service_interval_days",
    "threshold_km",
    "threshold_days",
    "in_use",
    "mandatory",
    "max_quantity",
)

RESOURCES = ("bike", "component", "collection", "workplan", "incident", "component_type", "overview")


class TupleShapeError(ValueError):
    pass


def _plain(value):
    if isinstance(value, Model):
        return _plain(value.__data__)
    if isinstance(value, dict):
        return {str(key): _plain(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_plain(item) for item in value]
    if isinstance(value, (set, frozenset)):
        return sorted(_plain(item) for item in value)
    if isinstance(value, float):
        return round(value, 6)
    return value


def _named(fields, row):
    if len(row) != len(fields):
        raise TupleShapeError(f"Expected {len(fields)} fields {fields[0]}..{fields[-1]}, got {len(row)}")
    return _plain(dict(zip(fields, row)))


def _named_list(fields, rows):
    if rows is None:
        return None
    return [_named(fields, row) for row in rows]


def _guard(target, key, build):
    try:
        target[key] = build()
    except TupleShapeError:
        raise
    except Exception as error:  # noqa: BLE001
        target[key] = {"error": f"{type(error).__name__}: {error}"}


def _merge(values, build):
    try:
        values.update(build())
    except TupleShapeError:
        raise
    except Exception as error:  # noqa: BLE001
        values["error"] = f"{type(error).__name__}: {error}"


def _by_first(fields, rows):
    named = _named_list(fields, rows)
    return {str(row[fields[0]]): row for row in named}


def _bike_values(app, bike_id, index_incidents, index_workplans):
    logic = app.business_logic
    values = {}

    def details():
        payload = logic.get_bike_details(bike_id)
        return {
            "bike_data": _plain(payload["bike_data"]),
            "component_rows": _named_list(BIKE_COMPONENT_FIELDS, payload["bike_component_data"]),
            "count_installed": payload["count_installed"],
            "count_retired": payload["count_retired"],
            "sum_cost": payload["sum_cost"],
            "recent_rides": _named_list(RIDE_FIELDS, payload["recent_rides"]),
            "planned_services": _named_list(PLANNED_SERVICE_FIELDS, payload["planned_services_data"]),
            "plan_services_preselect": _plain(payload["plan_services_preselect"]),
        }

    _merge(values, details)
    _guard(values, "compliance_report", lambda: _plain(logic.process_bike_compliance_report(bike_id)))
    values["incidents"] = _plain(index_incidents["bike_incidents"].get(bike_id))
    values["workplans"] = _plain(index_workplans["bike_workplans"].get(bike_id))
    return values


def _component_values(app, component, index_incidents, index_workplans, overview_rows, list_rows):
    logic = app.business_logic
    component_id = component.component_id
    values = {
        "overview_row": overview_rows.get(component_id),
        "list_row": list_rows.get(component_id),
        "incidents": _plain(index_incidents["component_incidents"].get(component_id)),
        "workplans": _plain(index_workplans["component_workplans"].get(component_id)),
    }
    _guard(values, "triggers", lambda: _plain(logic.calculate_component_triggers(component)))

    def details():
        payload = logic.get_component_details(component_id)
        return {
            "details": _plain(payload["bike_component_data"]),
            "history": _named_list(COMPONENT_HISTORY_FIELDS, payload["component_history_data"]),
            "service_history": _named_list(SERVICE_HISTORY_FIELDS, payload["service_history_data"]),
            "bike_name": payload["bike_name"],
            "days_since_service": payload["days_since_service"],
            "planned_services": _named_list(PLANNED_SERVICE_FIELDS, payload["planned_services_data"]),
            "plan_services_preselect": _plain(payload["plan_services_preselect"]),
            "oldest_history_date": payload["oldest_history_date"],
        }

    _merge(values, details)
    return values


def _collection_values(app, collection, all_rows):
    logic = app.business_logic
    values = {"summary": all_rows.get(collection.collection_id)}

    def status():
        component_ids = json.loads(collection.components) if collection.components else []
        return _plain(_sorted_bike_names(logic.calculate_collection_status(component_ids, collection.bike_id)))

    _guard(values, "status", status)

    def details():
        payload = logic.get_collection_details(collection.collection_id)
        return {
            "collection_data": _plain(payload["collection_data"]),
            "warnings": _plain(_sorted_bike_names(payload["warnings"])),
            "component_rows": _named_list(COMPONENT_DISPLAY_FIELDS, payload["all_components_display_data"]),
            "plan_services_preselect": _plain(payload["plan_services_preselect"]),
        }

    _merge(values, details)
    return values


def _sorted_bike_names(status):
    return {**status, "bike_names_list": sorted(status["bike_names_list"])}


def _workplan_values(app, workplan_id, rows):
    logic = app.business_logic
    values = dict(rows.get(workplan_id) or {})
    services = list(app.database_manager.read_services_by_workplan(workplan_id))
    _guard(values, "context", lambda: _plain(app.utils.derive_workplan_context(services, app.database_manager)))

    def details():
        payload = logic.get_workplan_details(workplan_id)
        return {
            "details": _plain(payload["workplan_data"]),
            "all_services_completed": payload["all_services_completed"],
            "latest_service_date": payload["latest_service_date"],
            "incidents": _named_list(INCIDENT_FIELDS, payload["incidents_data"]),
            "services": _named_list(WORKPLAN_SERVICE_FIELDS, payload["services_data"]),
            "planned_services": _named_list(PLANNED_SERVICE_FIELDS, payload["planned_services_data"]),
            "component_bike_names": _plain(payload["component_bike_names"]),
        }

    _merge(values, details)
    return values


def _source(overview, key, build, fallback=None):
    try:
        return build()
    except TupleShapeError:
        raise
    except Exception as error:  # noqa: BLE001
        overview[key] = {"error": f"{type(error).__name__}: {error}"}
        return fallback


def derived_values(app) -> dict[str, dict[str, dict]]:
    """Collect every value the pages derive from stored data, keyed resource, id, field"""
    logic = app.business_logic
    manager = app.database_manager
    result = {resource: {} for resource in RESOURCES}
    overview = result["overview"]

    bikes = list(manager.read_bikes())
    components = list(manager.read_all_components_objects())
    collections = list(manager.read_all_collections())
    workplans = list(manager.read_all_workplans())
    incidents = list(manager.read_all_incidents())

    index_incidents = _source(
        overview,
        "incident_index",
        lambda: logic.process_incidents(incidents),
        {"bike_incidents": {}, "component_incidents": {}},
    )
    index_workplans = _source(
        overview,
        "workplan_index",
        lambda: logic.process_workplans(workplans),
        {"bike_workplans": {}, "component_workplans": {}},
    )

    def bike_overview():
        payload = logic.get_bike_overview()
        rows = _named_list(OVERVIEW_BIKE_FIELDS, payload["bikes_data"])
        overview["bike_overview"] = {
            "bikes_data": rows,
            "open_incidents": _plain(payload["open_incidents"]),
            "planned_workplans": _plain(payload["planned_workplans"]),
            "assigned_collections": _plain(payload["assigned_collections"]),
        }
        return {row["bike_id"]: row for row in rows}

    overview_rows = _source(overview, "bike_overview", bike_overview, {})

    def component_overview():
        payload = logic.get_component_overview()
        overview["component_overview"] = {
            "count_installed": payload["count_installed"],
            "count_not_installed": payload["count_not_installed"],
            "count_retired": payload["count_retired"],
            "bikes_data": _named_list(("bike_name", "bike_id"), payload["bikes_data"]),
        }
        return (
            _by_first(COMPONENT_DISPLAY_FIELDS, payload["all_components_display_data"]),
            _by_first(COMPONENT_LIST_FIELDS, payload["all_components_data"]),
        )

    display_rows, list_rows = _source(overview, "component_overview", component_overview, ({}, {}))

    def collection_mapping():
        names, data = logic.get_component_collection_mapping()
        overview["component_collection_mapping"] = {
            "component_collection_names": _plain(names),
            "component_collection_data": {
                str(key): _named(COLLECTION_MAPPING_FIELDS, row) for key, row in data.items()
            },
        }

    _source(overview, "component_collection_mapping", collection_mapping)

    collection_rows = _source(
        overview, "collections", lambda: _by_first(COLLECTION_FIELDS, logic.get_all_collections()), {}
    )

    def incident_reports():
        payload = logic.get_incident_reports()
        overview["incident_reports"] = {
            "service_incident_options": _named_list(SERVICE_INCIDENT_OPTION_FIELDS, payload["service_incident_options"])
        }
        return _by_first(INCIDENT_FIELDS, payload["incident_reports_data"])

    result["incident"] = _source(overview, "incident_reports", incident_reports, {})
    workplan_rows = _source(
        overview, "workplans", lambda: _by_first(WORKPLAN_FIELDS, logic.get_workplans()["workplans_data"]), {}
    )
    result["component_type"] = _source(
        overview,
        "component_types",
        lambda: _by_first(COMPONENT_TYPE_FIELDS, logic.get_component_types()["component_types"]),
        {},
    )

    for bike in bikes:
        values = _bike_values(app, bike.bike_id, index_incidents, index_workplans)
        values["overview_row"] = overview_rows.get(bike.bike_id)
        result["bike"][bike.bike_id] = values
    for component in components:
        result["component"][component.component_id] = _component_values(
            app, component, index_incidents, index_workplans, display_rows, list_rows
        )
    for collection in collections:
        result["collection"][collection.collection_id] = _collection_values(app, collection, collection_rows)
    for workplan in workplans:
        result["workplan"][workplan.workplan_id] = _workplan_values(app, workplan.workplan_id, workplan_rows)
    return result
