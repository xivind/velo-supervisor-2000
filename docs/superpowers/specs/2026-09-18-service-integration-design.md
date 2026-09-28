# Service integration: incidents, workplans and services

**Date:** 2026-09-18
**Issue:** #351, with sub-issues #345, #346, #348, #349, #350
**Branch:** feature branch off `dev`
**Status:** Design approved in conversation, pending written review

## Goal

Make services the actionable unit that connects incidents and workplans, so the user never enters the same information twice. An incident produces planned services. A workplan groups planned services and derives its bike and components from them. Completing services completes the workplan and surfaces incidents that can be closed.

## Decisions

| Decision | Choice |
|---|---|
| Service date while planned | NULL. Date entered on completion, only then affects component health. |
| Planned date | Optional `planned_date` on services. Service date wins over workplan due date when both set. Workplan due date stays required as today. |
| Incident to workplan link | Dropped. Derived through services. |
| Workplan bike and components | Dropped. Derived through services. |
| Migration depth | Convert everything possible (see Migration). |
| Sub-issue scope | #346, #348, #349 included. #345 and #350 resolved by the redesign. |
| #349 model | `notes` column on component_history. |
| Plan and complete modals | Two modals sharing one JavaScript helper. |
| Completed back to Planned | Allowed. Same recalculation as deletion. |
| Retired components | Locked. No service status changes at all. |
| Blank values | Always NULL in the database, never empty strings. |
| Code style | Match existing naming and patterns. No decorators or new idioms. |
| Distance calculations | `process_service_records` and `update_component_service_status` are not modified. |

## Data model

All new fields declared as plain `CharField()` in `backend/database_model.py`, matching existing style.

| Table | Change |
|---|---|
| services | add `status` ("Planned" or "Completed") |
| services | add `incident_id` (NULL when not from an incident) |
| services | add `planned_date` (optional target date, NULL when blank, kept after completion) |
| services | `service_date`, `bike_id`, `distance_marker` are NULL while Planned |
| workplans | drop `workplan_affected_component_ids`, `workplan_affected_bike_id` |
| incidents | drop `workplan_id` |
| component_history | add `notes` (NULL when blank) |

## Migration

Added to `backend/db_migration.py` as steps 12 to 16 using the existing `check_*` / `migrate_*` function pairs. Each step is idempotent. The script imports `generate_unique_id` from `utils` (add backend directory to `sys.path`; utils has only standard library imports).

1. **Add columns.** `status`, `incident_id` and `planned_date` on services, `notes` on component_history. Set `status = 'Completed'` where NULL.
2. **Planned workplans to planned services.** For each affected component that still exists and has no service in that workplan, insert a service with status Planned, description "Planned service (migrated from workplan)", NULL date, bike and distance, component_name filled.
3. **Preserve Done workplans.** Append a line to `workplan_description` with the bike name and component names that were on the workplan, resolved to names at migration time. Planned workplans get the line only for components that no longer exist.
4. **Rebuild incident links.** For each incident with a `workplan_id`: set `incident_id` on services in that workplan whose component is in the incident's affected components. If the workplan is Planned, the incident is Open and nothing matched, insert Planned services for the incident's components into that workplan with `incident_id` set. If the incident has no components, append "Previously linked to workplan <id>" to `incident_description`.
5. **Drop old columns** on workplans and incidents by table rebuild (create new, copy, drop, rename). Works on every SQLite version. Runs after steps 2 to 4.
6. **Update `backend/template_db.sqlite`** by running the finished script against it.

Each converted workplan and incident is printed. Steps skip rows already converted so reruns are safe.

## Backend

### database_manager.py

- `read_latest_service_record`, `read_subset_service_history`, `read_oldest_service_record`: add `Services.status == "Completed"` to the where clause. These feed health computation, validation and deletion recalculation. Existing pattern: `read_open_incidents`, `read_planned_workplans`.
- `read_services_by_workplan`, `read_single_service_record`: unchanged, return all statuses.
- New: `read_planned_services_by_component`, `read_planned_services_by_workplan`, `read_services_by_incident`, `read_planned_services_by_bike` (via components installed on the bike).
- `write_service_record`, `write_history_record`: unchanged, accept the new keys.

### business_logic.py

- `create_planned_services(component_ids, description, workplan_id=None, incident_id=None, planned_date=None)`: replaces `bulk_create_service_records`. One Planned service per component. Returns the existing success / partial_failure / complete_failure dict.
- `complete_services(service_ids, service_date, completion_note=None)`: for each service, `validate_service_record("complete service", ...)`, set status Completed and date, append note to description if given, then call `process_service_records` unchanged. Returns the bulk dict. After the loop, for each touched incident that is Open with no Planned services left, add a hint to the result summary naming the incident.
- `create_service_record`, `update_service_record`: gain `status`, `incident_id` and `planned_date`. Planned goes through the planned path. Completed to Planned sets date, bike, distance to NULL and calls `recalculate_component_after_service_removal`.
- `recalculate_component_after_service_removal(component_id)`: extracted from the services branch at the end of `delete_record`. Called from delete and revert. No logic change.
- `validate_service_record(mode, ...)`: new modes and rules, see Validation.
- `create_workplan(..., source_incident_id=None)`: drop affected fields. When `source_incident_id` is given, also call `create_planned_services` for the incident's components with the workplan and incident ids set.
- `update_workplan`: drop affected fields. Refuse status Done while Planned services remain, with the count in the message. Refuse a completion date that is in the future or earlier than the latest service date in the workplan. Close-linked-incidents finds incidents through services.
- `get_workplan_details`: derive bike, components, progress via `derive_workplan_context`. Banner flag becomes "has services and none Planned". Drop `linkable_incidents_data` and `workplan_check_component_services`. Add per-service data needed by the complete modal: oldest installation date and retired flag per component.
- `process_workplans`: derive bike per planned service's component.
- `process_incidents`: unchanged.
- `delete_record`: Workplans blocked while services exist (unchanged). Incidents set `incident_id` NULL on their services before delete. Services with status Planned skip recalculation.
- `create_history_record`, quick swap path: accept `notes`, stored NULL when blank.

### utils.py

- `derive_workplan_context(services, database_manager)`: returns bike name(s), component ids and names, completed count, total count.
- `get_effective_planned_date(service, workplan)`: returns `service.planned_date` if set, else `workplan.due_date` if the service has a workplan, else None. Used by every planned services table.
- `get_workplan_data_tuple`: uses derived context, adds progress. `generate_workplan_title` receives derived names.
- `get_incident_data_tuple`: replaces `workplan_id` / `workplan_name` with a list of (workplan_id, workplan_name) reached through services, plus planned and completed counts.
- `get_workplan_names_dict`: unchanged.

### main.py

| Route | Change |
|---|---|
| `POST /add_planned_services` | replaces `/bulk_add_service_records`. Form: `component_ids` list, `service_description`, `workplan_id` optional, `incident_id` optional, `planned_date` optional. JSON response. |
| `POST /complete_services` | new. Form: `service_ids` list, `service_date`, `completion_note` optional. JSON response. |
| `POST /add_service_record`, `/update_service_record` | add `status`, `incident_id`, `planned_date`. Redirect unchanged. |
| `POST /add_workplan`, `/update_workplan` | drop affected bike and component params. |
| `POST /add_incident_record`, `/update_incident_record` | drop `workplan_id`. |
| `POST /add_history_record`, `/quick_swap` | add `notes` optional. |

Routes stay thin. All logic in business_logic.

## Validation

In `validate_service_record`, mirrored in main.js where data is available.

| Mode | Rules |
|---|---|
| all | component exists; component not Retired |
| plan | description at least 5 characters; `planned_date` blank or valid format (future allowed); no other Planned service for the same component in the same workplan (no workplan: duplicates allowed) |
| complete | service is Planned; date required, format YYYY-MM-DD HH:MM, not in future, after component's first installation; component has installation history; if the workplan is Done, date not later than the workplan completion date (message: reopen the workplan first) |
| complete workplan (in `update_workplan`) | no Planned services remain; completion date valid format, not in the future, and not earlier than the latest service date among its services |
| edit completed | existing date rules |
| revert to planned | none beyond "all" |

Frontend: date via existing `validateDateInput`; first installation date, retired flag and workplan completion date via data attributes per service or component; latest service date via data attribute on the complete workplan button; at least one row selected; description length as today.

## UI

### Modals

- `modal_plan_services.html` (renamed from `modal_create_services_workplan.html`): description, optional planned date applied to all selected services, TomSelect of components preselected from context, dropdown of Planned workplans with "No workplan", hidden `incident_id`. Launch button carries preselection and context in `data-*` attributes.
- `modal_complete_services.html` (new): date defaulting to now, optional note, checklist of Planned services as "component: description", all ticked. Rows for retired components shown disabled.
- `modal_service_record.html`: Planned/Completed radio; Planned hides the service date and shows an optional planned date. Workplan dropdown lists all Planned workplans, no component filter. Incident dropdown of Open incidents referencing the component.
- `modal_workplan_record.html`: bike and component selects removed. From incident 📝 button: description prefilled, hidden `source_incident_id`, backend creates workplan plus planned services.
- `modal_incident_record.html`: workplan dropdown removed (#345).
- `modal_link_incident.html`: removed.
- `modal_update_component_status.html`, `modal_quick_swap.html`: optional notes textarea (#349).

### Pages

- `workplan_details.html`: derived badges for bike, components, "n of m services completed". Buttons: Edit, Plan services, Complete services, Complete workplan, Delete. Banner: "all services completed" when none Planned; "completed on <date>" when Done (#350). Services table: Status column, "Planned for" column showing the effective planned date or "-", per-row complete button. Incidents table derived.
- `workplans.html`: bike and component columns derived, progress column added.
- `incident_reports.html`: workplan column shows one or more links. 📝 creates workplan plus services. New "Plan services" row button.
- `bike_details.html`: "Plan services" button preselecting installed, non-retired components (#348). Planned services table with "Planned for" column.
- `collection_details.html`: "Plan services" button preselecting collection components (#346).
- `component_details.html`: planned services table above service history with complete, edit, delete. Service history shows Completed only. Installation history gains Notes column. Buttons disabled when Retired, as today.
- `index.html`: no template change; icons derived server side.
- `help.html`: text updated.

### main.js

- New L2 subsection under "Functions used on multiple pages": `// ----- Plan and complete services modals -----`. Contains the shared helper (post form data, loading modal, report modal via `showReportModal`, reload) and both modal handlers. Existing bulk create code moves here and is adapted.
- Removed: `populateIncidentWorkplanDropdown` and its listeners, link incident modal code, workplan modal bike and component TomSelect setup.
- Simplified: `populateServiceWorkplanDropdown` lists Planned workplans without component filtering.
- Every block keeps its element-existence guard. Header hierarchy, `window.functionName` for globals, TomSelect pattern per CLAUDE.md. Nothing else in the file changes.

## Error handling

- Bulk operations return existing success / partial_failure / complete_failure dicts; partial failures name each failed item. No rollback, matching current bulk behaviour.
- Single service form uses redirect-with-toast.
- Component deletion cascades planned services as today. Names fall back to "Deleted component".
- Workplan deletion blocked while services exist. Incident deletion nulls `incident_id` on its services.
- Reverting a service in a Done workplan leaves the workplan Done.
- Migration runs inside the existing try block and is rerunnable.

## Testing

- **Automated, pytest** (`tests/test_migration.py`): copy template DB to temp dir, seed a Planned workplan with three components and one existing service, a Done workplan, an incident per workplan, a bike-only incident; run migration twice; assert planned services, incident links, appended descriptions, dropped columns, and no change on second run. Pytest added to requirements as dev dependency.
- **Automated, pytest** (`tests/test_service_status.py`): component with installation history and one Completed service; record service_next, distance, status; add a Planned service and assert unchanged; revert a Completed service and assert values match post-deletion values.
- **Manual** (`tests/test_protocol_services.md`, structured per `tests/README.md`): plan from all five pages with preselection; complete singly and in bulk; incident to workplan to services with one description; banner and workplan completion; incident hint on last completion; retired lock; revert; status change notes; every validation message backend and frontend.
- **Before handover**: run app locally, walk the manual protocol, run migration on a copy of the real database and compare row counts.

## Out of scope

- Merged installation and service timeline (#349 second idea).
- Automatic closing of incidents outside workplan completion.
