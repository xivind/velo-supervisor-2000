# Parity checklist

Everything the old UI on `master` does that a user can see or trigger, and where the new design covers it. Built for Stage 2 (spec: [2026-11-18-stage-2-design.md](../superpowers/specs/2026-11-18-stage-2-design.md), "Parity checklist").

- **Where on master:** template under `frontend/templates/`, `main.js` line, or route in `backend/main.py`.
- **New design:** canvas and artboard, filled in as canvases are approved.
- **State:** `open` (not yet placed), `covered` (placed on an approved canvas), `dropped` (with the reason), `browser-only` (a rule only `main.js` enforces; it moves to the server through #386 and the new design must still show it as an inline message).

## Pages and shared parts

| ID | Old behaviour | Where on master | New design | State | Note |
|---|---|---|---|---|---|
| P-001 | Bike overview: a card per bike with name, status and distance; links to the bike | `index.html`, `/` | | open | Becomes the bike list in Bike |
| P-002 | Bike overview: "Show retired bikes" toggle | `index.html` | | open | Bike list: active first, retired after |
| P-003 | Bike overview: card marks open workplans, open incidents and collections per bike | `index.html` | | open | |
| P-004 | Menu with the main pages, current page highlighted | `menu.html` | | open | Becomes the left menu / phone drawer |
| P-005 | Footer: version and last Strava pull | `footer.html` | | open | Moves to the menu foot |
| P-006 | Footer: "Submit issue" link | `footer.html` | | dropped | Spec: decided drop |
| P-007 | Footer: database path | `footer.html` | | dropped | Spec: decided drop |
| P-008 | Footer: page load time | `footer.html`, `main.js` 6357 | | dropped | Spec: goes to the browser console when debug is on |
| P-009 | Page shell: title, shared modals (validation, confirm, report, loading) | `base.html` | | open | Covered by the notification system |
| P-010 | Error page with status code and links to the log and repository | `error.html` | | open | |
| P-011 | Emoji as icons on buttons, labels and badges | all templates | | dropped | Spec: no emoji; Lucide icons |
| P-012 | Success or failure of every save shown in a report modal after the redirect (`?success=&message=`) | `modal_report.html`, `main.js` 259 | | open | Becomes toast (success) and banner (error) |
| P-013 | Loading modal while a long job runs (refresh bikes, get rides) | `modal_loading.html` | | open | |
| P-014 | Validation errors shown in a modal | `modal_validation.html` | | open | Becomes an inline message on the field |
| P-015 | Confirm modal before every delete ("This cannot be undone") | `modal_confirm.html`, `main.js` 1052 | | open | |
| P-016 | Markdown docs modal (help topics opened in place) | `modal_docs.html` | | open | |
| P-017 | Date fields: picker plus typed `YYYY-MM-DD HH:MM`; invalid format refused before sending | `main.js` 115, 664–723 | | open | Stage 3 picks the date picker |
| P-018 | Multi-select with search (TomSelect) for components | `main.js` 1685 | | open | Stage 3 picks the library |

## Bike details

| ID | Old behaviour | Where on master | New design | State | Note |
|---|---|---|---|---|---|
| P-020 | Bike header: active/retired, first ride, total distance, installed count | `bike_details.html`, `/bike_details/{bike_id}` | | open | Bike top |
| P-021 | Bike header: retired components count | `bike_details.html` | | dropped | Spec: retired components stay in Inventory |
| P-022 | Bike header: expected cost of next service | `bike_details.html` | | dropped | Spec: cost shows on workplans as expected replacement cost |
| P-023 | Bike header: collections on the bike, linked | `bike_details.html` | | open | Collection shortcuts in the top |
| P-024 | Bike header: notes and bike id | `bike_details.html` | | open | |
| P-025 | Banner: bike or installed components have open incidents | `bike_details.html` | | open | Count in the top |
| P-026 | Banner: unfinished workplans | `bike_details.html` | | open | Count in the top |
| P-027 | Banner: component type compliance (missing mandatory, over max quantity) | `bike_details.html` | | open | Compliance count in the top |
| P-028 | Components table: name, collection, type, distance, lifetime, service, km to go, days to go; trigger markers | `bike_details.html` | | open | Rows most urgent first |
| P-029 | Components table: show installed / show retired filters and search | `bike_details.html` 240 | | open | Retired toggle on the Bike page (user, 2026-11-19); search in Inventory |
| P-030 | Components table: sortable columns | `main.js` 3018 | | open | |
| P-031 | Component row markers: in a workplan, open incident, in a collection | `bike_details.html` | | open | Badges |
| P-032 | Component row actions: change status, quick swap, delete | `bike_details.html` | | open | |
| P-033 | Planned services table: due date (effective planned date, mark when passed), complete, edit, delete per row | `bike_details.html` | | open | |
| P-034 | Incidents table: severity, date, description, days open, workplans with progress | `bike_details.html` | | open | |
| P-035 | Workplans table: size, due date, name, days overdue, progress wheel, complete | `bike_details.html` | | open | |
| P-036 | Recent rides: date, name, distance, commute marker | `bike_details.html` | | open | |
| P-037 | Button row: new collection, new component, install existing, new workplan, new incident, plan services, complete services | `bike_details.html` | | open | Phone bottom bar and sheets |
| P-038 | Button order on bike details set in Config | `bike_details.html`, `config.html` | | open | Probably dropped, decide in Task 9 |

## Component details

| ID | Old behaviour | Where on master | New design | State | Note |
|---|---|---|---|---|---|
| P-040 | Header: type, total mileage, age, last service, last status change, cost, notes, id | `component_details.html`, `/component_details/{component_id}` | | open | |
| P-041 | Link to the bike, or to the previous bike when not installed | `component_details.html` | | open | |
| P-042 | Lifetime and service progress per distance and per days, with remaining and status | `component_details.html` | | open | Wear bars |
| P-043 | Banners: open incidents, unfinished workplans | `component_details.html` | | open | |
| P-044 | Actions: update status, update details, edit collection, quick swap, duplicate, new service, plan services, complete services, new workplan, new incident, delete | `component_details.html` | | open | |
| P-045 | Duplicate component: create form prefilled from this one | `modal_create_component.html` | | open | |
| P-046 | Installation history: date, bike, mileage, reason, notes; edit and delete per record | `component_details.html` | | open | |
| P-047 | Service history: date, description, workplan link | `component_details.html` | | open | |
| P-048 | Planned services, incidents and workplans tables as on bike details | `component_details.html` | | open | |
| P-049 | Retired component: service actions disabled | `component_details.html` | | open | Spec: no service actions, view says why |
| P-050 | Button order on component details set in Config | `component_details.html`, `config.html` | | open | Probably dropped, decide in Task 9 |

## Component overview, collections

| ID | Old behaviour | Where on master | New design | State | Note |
|---|---|---|---|---|---|
| P-060 | All components: name, type, distance, status, lifetime, service, bike; markers | `component_overview.html`, `/component_overview` | | open | Inventory components list |
| P-061 | Filters installed / not installed / retired, search, sort | `component_overview.html` 142 | | open | Three switches in the list toolbar (Task 7) |
| P-062 | Row actions: change status, quick swap | `component_overview.html` | | open | |
| P-063 | Collections table: name, components, bike, updated, health marker, delete; search | `component_overview.html` 46 | | open | Inventory collections list |
| P-064 | Buttons: new collection, new component, new workplan, new incident | `component_overview.html` | | open | |
| P-065 | Collection details: last status change, bike, components, description, id | `collection_details.html`, `/collection_details/{collection_id}` | | open | |
| P-066 | Collection warnings: empty, contains retired, mixed statuses, different bikes, bike mismatch; block bulk actions | `collection_details.html` | | open | |
| P-067 | Collection components table with per-row status change | `collection_details.html` | | open | |
| P-068 | Collection actions: edit, change status, plan services, delete | `collection_details.html` | | open | |
| P-069 | Back keeps sort and filters after a delete | #128 | | open | Spec: every view has an address |
| P-070 | Delete and retire in combination behave unpredictably | #145 | | open | New flows must not repeat it |
| P-071 | Opening an edit form scrolls to it | #37 | | open | Item views replace scrolled forms |

## Workplans, incidents

| ID | Old behaviour | Where on master | New design | State | Note |
|---|---|---|---|---|---|
| P-080 | Workplans list: bike, name, size, due, completion, days overdue, status, progress wheel (check at 100%), delete | `workplans.html`, `/workplans` | | open | |
| P-081 | Workplans list: show planned / done, search incl. component names | `workplans.html` | | open | |
| P-082 | Workplan details: size, due, services n/m, bikes, components with bike, description (Markdown), completion | `workplan_details.html`, `/workplan_details/{workplan_id}` | | open | |
| P-083 | Workplan banners: completed (actions disabled), all services completed, no services yet | `workplan_details.html` | | open | |
| P-084 | Workplan actions: edit, plan services, complete services, complete workplan (disabled while planned remain), delete | `workplan_details.html` | | open | |
| P-085 | Workplan: linked incidents table; services table with complete, edit, delete | `workplan_details.html` | | open | |
| P-086 | Incidents list: bike, components, severity, dates, days open, workplans with progress | `incident_reports.html`, `/incident_reports` | | open | |
| P-087 | Incidents list: show open / resolved, search, `#incident-<id>` opens one | `incident_reports.html`, `main.js` 4406 | | open | |
| P-088 | Incident row actions: new workplan from incident, plan services, edit, delete; first two disabled when resolved | `incident_reports.html` | | open | |

## Config, component types, help

| ID | Old behaviour | Where on master | New design | State | Note |
|---|---|---|---|---|---|
| P-090 | Get new rides / get all rides | `config.html`, `/refresh_rides/{mode}` | | open | |
| P-091 | Refresh all bikes | `config.html`, `/refresh_all_bikes` | | open | |
| P-092 | Export dataset, reset database buttons | `config.html` | | open | Empty links on master, no route behind them. Drawing them needs a feature issue (Task 9) |
| P-093 | Paths to database and OAuth file, save and restart | `config.html`, `/update_config`, `main.js` 6154 | | open | |
| P-094 | Verbose logging toggle | `config.html`, `/update_config` | | open | |
| P-095 | Latest log entries with filter | `config.html`, `/get_filtered_log` | | open | |
| P-096 | Config page | `/config_overview` | | open | |
| P-097 | Component types table: name, mandatory, max per bike, in use, lifetimes, intervals, thresholds; edit, delete | `component_types.html`, `/component_types_overview` | | open | Moves into Config; stable ID is #385 |
| P-098 | Help page: first steps, concepts, how-tos | `help.html`, `/help` | | open | Rewritten in Stage 5 (#99) |

## Forms (modals) and routes

| ID | Old behaviour | Where on master | New design | State | Note |
|---|---|---|---|---|---|
| P-100 | Create component: date, name, type (fills defaults), bike, status, intervals, thresholds, offset, cost, notes | `modal_create_component.html`, `/create_component` | | open | |
| P-101 | Update component details: name, type, cost, offset, intervals, thresholds, notes | `modal_update_component_details.html`, `/update_component_details` | | open | |
| P-102 | Update component status: status, bike, date, notes | `modal_update_component_status.html`, `/add_history_record` | | open | |
| P-103 | Edit installation record: date and note only | `modal_edit_installation_record.html`, `/update_history_record` | | open | |
| P-104 | Install existing: component or collection mode, only unassigned shown, date | `modal_install_component.html` | | open | Install sheet |
| P-105 | Quick swap: component out, fate, swap to existing of same type or create new (name and cost copied), date, notes | `modal_quick_swap.html`, `/quick_swap` | | open | |
| P-106 | Collection: name, description, components (retired and other collections' hidden) | `modal_collection.html`, `/add_collection`, `/update_collection` | | open | |
| P-107 | Change collection status: status, bike, one note for all, date | `modal_update_collection_status.html`, `/change_collection_status` | | open | |
| P-108 | Service record: completed or planned, dates, description, workplan, incident, view links | `modal_service_record.html`, `/add_service_record`, `/update_service_record` | | open | |
| P-109 | Plan services: description, components, planned date (blank uses workplan due date), workplan | `modal_plan_services.html`, `/add_planned_services` | | open | |
| P-110 | Complete services: one date for all, note, planned services ticked; retired rows disabled | `modal_complete_services.html`, `/complete_services` | | open | |
| P-111 | Workplan: name (blank gives generated title), due date, status, size, Markdown description, completion | `modal_workplan_record.html`, `/add_workplan`, `/update_workplan` | | open | |
| P-112 | Workplan from an incident: description prefilled, components ticked; a planned service is created per ticked component, linked to the incident | `modal_workplan_record.html`, `/add_workplan` | | open | The backend already creates a workplan with services in one step here; #384 widens it |
| P-113 | Complete workplan: date, notes, close linked incidents | `modal_complete_workplan.html`, `/update_workplan` | | open | |
| P-114 | Incident: date, open/resolved, severity, bike, components, description, resolution; read-only linked services | `modal_incident_record.html`, `/add_incident_record`, `/update_incident_record` | | open | |
| P-115 | Component type: name, max per bike, mandatory, default intervals and thresholds | `modal_component_type.html`, `/component_types_modify` | | open | |
| P-116 | Delete any record, after confirm; server refuses when dependants exist | `/delete_record` | | open | |

## Seed rows from the Stage 1 handover

| ID | Old behaviour | Where on master | New design | State | Note |
|---|---|---|---|---|---|
| P-120 | Plan services preselects by origin: component, bike (installed, non-retired), collection (members), incident (its components), workplan (locked); retired not listed | `modal_plan_services.html` | | open | Spec: nothing preselected unless ticked (#365); origin still limits the choices |
| P-121 | Planned and due dates accept future dates; service, completion and resolution dates do not | `main.js` | | open | |
| P-122 | Complete services: rows "component: description", date defaults to now; row action completes only that one; disabled when nothing planned or retired | `modal_complete_services.html` | | open | |
| P-123 | Planned services tables: effective planned date, mark when passed; row opens the component | `bike_details.html`, `component_details.html`, `workplan_details.html` | | open | |
| P-124 | Incident: resolving with planned services warns but saves; status radios fill and clear the resolution date | `modal_incident_record.html` | | open | |
| P-125 | Service record: Planned hides the service date; workplan options Planned only, incident options Open naming the component, plus the linked one | `modal_service_record.html` | | open | |
| P-126 | "Notes for status change" on status change, quick swap and collection status change | modals | | open | |
| P-127 | Workplan due date is required | `/add_workplan` | | open | Held by the route (Stage 1). Listed for #386 |
| P-128 | Uninstall with empty optional fields is accepted | `/add_history_record` | | open | |

## Rules held only in the browser

Found by checking every validation in `main.js` against `business_logic.py` on `master`. Each moves to the server through #386; future-date checks are #340.

| ID | Old behaviour | Where on master | New design | State | Note |
|---|---|---|---|---|---|
| P-140 | Incident date cannot be in the future | `main.js` 4724 | | browser-only | #340 |
| P-141 | Resolution date cannot be in the future | `main.js` 4734 | | browser-only | #340 |
| P-142 | Resolution date is required when the incident is Resolved | `main.js` 4741 | | browser-only | |
| P-143 | Resolution date must be after the incident date | `main.js` 4759 | | browser-only | |
| P-144 | An incident must name a bike, at least one component, or both | `main.js` 4780 | | browser-only | `create_incident_record` checks nothing |
| P-145 | Uninstalling (Not installed) a component or collection: the bike must be left blank | `main.js` 1852 | | browser-only | No server check refuses it |
| P-146 | Retiring: the bike cannot change at the same time | `main.js` 1861, 3976 | | browser-only | No server check refuses it |
