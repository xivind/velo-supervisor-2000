# Service integration (#351): findings from the manual test walkthrough

Source: user annotations in `tests/test_protocol_services.md`, walkthrough on 2026-09-25. Everything in the protocol passed functionally. This file lists what to change before the code review, grouped by type. Read the protocol for the user's exact wording.

Branch `feature/service-integration`, 19 commits, nothing pushed. Sandbox: `scratchpad/sandbox`, symlinks to the repo, its own config, migrated copy of `/home/xivind/code/prod_db_migrated.sqlite`. Baseline for comparisons: `/home/xivind/code/prod_db.sqlite`, unmigrated.

## A. Questions to answer from the code, no change expected

- **A1 (M2)** Confirm the migration skips components that already have a completed service in that workplan, and that this is intended
- **A2 (M3)** Confirm retired components get no planned service and are noted in the description. No such case existed in the data
- **A3 (M4)** Two done workplans list components. Confirm this is because they have completed services, which is correct
- **A4 (M5)** Explain how the workplan column on incidents is populated: through services linked to both the incident and a workplan
- **A5 (W10)** A workplan could be deleted while incidents were still linked. Decide whether that is a problem now that incident links run through services
- **A6 (R1, R2, R4)** Regression evidence against the baseline database, including a manual Strava sync

### Answers (read from the code 2026-09-25)

- **A1** Confirmed and intended. `migrate_workplans_to_planned_services` skips a component when a service row already exists for that workplan and component (`backend/db_migration.py:664`). Before this migration runs, the only such rows are service records the user linked to a workplan in the previous release, so in practice completed services. Adding a planned service would duplicate work already recorded. Note: the skip is silent, it produces no entry in the description note, unlike retired and deleted components
- **A2** Confirmed. `insert_planned_service_for_migration` returns False when the component row is missing or `installation_status == "Retired"` (`backend/db_migration.py:624`), and the caller appends `<name> (retired)` to the "components without planned service" note on the workplan description (`backend/db_migration.py:676`). Deleted components take the separate `missing_component_ids` path and appear as "Deleted component" in the same note
- **A3** Confirmed and correct. Only workplans with status `Planned` get planned services (`backend/db_migration.py:659`), done workplans get a description note only. The components shown on those two done workplans come from completed service records that already carried `services.workplan_id` from the earlier workplan hub release (`backend/db_migration.py:506`)
- **A4** Incident to services through `services.incident_id`, then the distinct non-null `service.workplan_id` of those services (`backend/utils.py:255`). The displayed title comes from `get_workplan_names_dict`, which generates each workplan title from that workplan's own services (`backend/utils.py:243`). The column also renders completed/total service counts (`frontend/templates/incident_reports.html:111`)
- **A5** No longer a problem. Deleting a workplan is blocked whenever it has any linked service (`backend/business_logic.py:3280`). Incident links exist only through services, so a workplan that can be deleted has no incident links either. The old dangling `incidents.workplan_id` column is dropped by the migration
- **A6** Done 2026-09-26, run on `/home/xivind/code/prod_db.sqlite`, which is a genuine pre-migration export (636 components, 1032 history records, 201 services, 17 bikes, 7357 rides). Working copies and scripts in the session scratchpad under `regression/`
  - **Migration** applies in 17 steps on the baseline copy and repeats cleanly, the second run reports no steps performed. It marked the 201 existing services Completed, created 15 planned services from the two planned workplans, and added `workplan_name`
  - **Recalculation, master against branch.** Both copies had the same recalculation run on the same day, `update_components_distance_iterator` over all 17 bikes then `process_history_records` for each of the 636 components, with pristine master code exported by `git archive`. Both processed 636 components and hit the same 10 components that have no history records, a pre-existing data condition. Comparing every distance and status field afterwards: bikes identical, components identical, component history identical, and the 201 services identical. The only difference in the whole database is the 15 planned services the migration created, all with no date, no bike and no distance marker, so they cannot affect health computation. That covers R1 and R2
  - **Strava sync, R4.** No Strava token file exists on this machine, only `strava_tokens.example.json`, so a live sync could not be run here. Evidence instead: `backend/strava.py` and `backend/scheduler.py` are byte identical to master, and `update_rides_bulk`, `refresh_all_bikes`, `write_update_rides_bulk`, `update_components_distance_iterator`, `update_component_distance` and `update_bike_status` are all identical at the syntax tree level, so nothing in the ingestion path changed. On top of that the database side of a sync was replayed on both copies with the same three new rides and the same post-fetch processing. It moved the distance of 61 components, and master and branch still agree on every field. What remains unverified is the live call to Strava itself, which needs the token file from the production host
  - **R3** rechecked after all the interface changes: index, components, workplans, incidents, component types, config, help, and the bike, component, collection and workplan detail pages all return 200

## B. Bugs to fix

- **B1 (P8)** The planned date picker refuses future dates. Correct when completing, wrong when planning. A planned date must allow the future
- **B2 (P5)** Opening the plan services modal from a workplan shows no components in the list. Other entry points show them
- **B3 (S2 area)** The service record modal requires a date when completing, but only the backend enforces it. Add the frontend check so submit is blocked

### Status (2026-09-26)

- **B1 fixed.** `initializeDatePickers` capped every field except `due_date` at the current time (`frontend/static/js/main.js:533`). The allowance now covers `planServicesPlannedDate` and `servicePlannedDate` as well. Verified in the sandbox: the planned date takes a date two weeks ahead, while `serviceDate` and `completeServicesDate` still refuse the future
- **B2 hint added.** The dropdown itself was never broken The dropdown is populated on the workplan page too, all 290 non-retired components are rendered and the list opens normally. What differs is that the workplan entry point preselects nothing, while the bike and component entry points preselect their own components. A workplan gives no component context to preselect, and preselecting its existing planned services would only trip the duplicate check, so the behaviour stands. The helper text under the Components field now reads "Select components which this service applies to. Retired components cannot be serviced and are not listed.", which says what the empty field is for without claiming anything is missing
- **B3 fixed, root cause was not the missing check.** The service modal already validated an empty completion date, but `initializeDatePickers` installed a `form.onsubmit` wrapper that called `form.submit()` itself once date formats looked valid (`frontend/static/js/main.js:653`), which bypasses `preventDefault` from every other submit listener. The wrapper now only blocks on invalid input and otherwise hands over to the existing handler or the browser. Verified in the sandbox: completing without a date is refused with no request sent, saving with a valid date still works, and the workplan form still refuses a malformed due date

## C. Interface changes the user asked for

- **C1** Move "Complete services" from inside the planned services table to the button row at the top, next to "Plan services", on bike details and component details. Disabled when there is nothing to complete
- **C2** Workplan details, planned services table: rename "Planned for" to "Due date". Replace the "(due date)" marker with an emoji when the date has passed, for example an exclamation mark
- **C3** Workplan details, first card: remove the Tasks badge and the markdown checkbox progress. Check for other places that still use it
- **C4** Workplan details, first card: show service progress with the same wheel as the workplans list, same "2/7" format
- **C5** Workplan details, both service tables: show the bike each component is installed on in parentheses, or "(Not assigned)". Only on this page, since a workplan can span bikes
- **C6** Quick swap and collection status change: caption the notes field "Notes for status change". On collection status change, add the notes field and explain that the same note goes on every installation record
- **C7** Edit installation record modal: allow editing the note as well as the date. Status stays uneditable
- **C8** Service record modal: add a "View incident" link next to the incident dropdown, like the existing "View workplan" link. Reword the helper text so it does not imply several incidents

### Status (2026-09-26)

All eight applied and checked in the sandbox.

- **C1** New `btn_complete_services` macro on bike details and component details, registered as `complete-services` in the button map and in both default orders in `backend/utils.py`, so it also appears on the config page for sorting. The button is disabled when there is nothing to complete, and on component details also when the component is retired. Removed from the planned services card header on both pages, the per row ✅ button is untouched
- **C2** Header renamed to "Due date". The "(due date)" marker is gone, an ❗ with the tooltip "Due date has passed" now shows when the effective date is earlier than the current time, which the payload passes as `today`. The marker on bike details and component details is left as it was, the change was asked for on this page only
- **C3** Tasks badge removed, together with `checkbox_progress` in the payload and `parse_checkbox_progress` in `backend/utils.py`. No other page used either
- **C4** The Services badge now renders the same donut and "0/4" text as the workplans list, driven by `completed_count` and `total_count`
- **C5** Both service tables show the bike in parentheses after the component name, "(Not assigned)" when the component is not installed. Built as `component_bike_names` in the workplan payload rather than extending the shared planned service tuple, which would have touched the other pages for no visible gain
- **C6** Quick swap notes field captioned "Notes for status change". The collection status modal has the same field, with the line "The same note is stored on the installation record of every component in the collection", and the note now travels through `/change_collection_status` into every history record. Verified on a collection of four components, all four installation records carried the note
- **C7** The edit installation record modal has a Notes field, prefilled from the record and saved through `/update_history_record`. Status stays read-only, and the modal says so. Verified by writing and clearing a note on a real record
- **C8** "View incident" sits next to the incident dropdown like "View workplan", pointing at `/incident_reports#incident-<id>`, and the incident rows carry that anchor id. Helper text now reads "Optional. A service can be linked to one open incident that references this component"

### Extra wording fixes asked for on 2026-09-26

- Workplan details: the "Edit workplan" button is now "Edit details", and the sentence about reopening a done workplan names the new label
- Workplan details: the line above the planned services table said planned services have no date until they are completed, which is wrong since a planned service shows its own planned date or the workplan due date. It now reads "Planned services do not affect component status. A due date that has passed is marked with ❗"

## D. Design questions to decide before coding

- **D1 (W2, I3, I4, and notes)** Replace generated workplan titles with a user-entered name. The generated title reads badly when a workplan spans bikes, and it makes the incidents workplan column long. Needs a new field, a form field, and a migration default. User leans yes
- **D2 (I1, C8, S3, and notes)** Visibility of links from an incident. Today an incident shows its workplans through services, but a service is not reachable from the incident, and the incident modal shows no links at all. Decide what an incident should display, and settle the cardinality between services, incidents and workplans
- **D3 (I4)** Incidents list, workplan column: show a simple indicator of one or more linked workplans, with the actual links inside the modal, rather than a list of long titles
- **D4 (notes, last item)** When creating a workplan from an incident, the components come across silently. Decide whether the modal should show which components will get planned services, and whether the user can choose

### Decisions (2026-09-26)

- **D1** Optional `workplan_name`. New field on the workplan form, may be left empty. When set it replaces the generated title everywhere the title is shown, when empty the generated title is used as today. No migration backfill
- **D2** The incident modal gets a read-only section listing the incident's linked services: component, status, date, and a link to the service's workplan. Cardinality stays as implemented: a service belongs to at most one incident and one workplan, an incident can span many services across many workplans
- **D3** Incidents list, workplan column: compact indicator only, a badge with the number of linked workplans plus the services completed counter. The links themselves move into the incident modal
- **D4** Create workplan from incident: the modal lists the incident's affected components preselected with checkboxes, the user can deselect before creating

### Status (2026-09-26)

All four implemented and checked in the sandbox.

- **D1** New optional `workplans.workplan_name`, added by migration step 17, which runs after the step that rebuilds the workplans table. `resolve_workplan_title` in `backend/utils.py` is now the single place that decides between the given name and the generated title, used by the workplan details payload, the workplan tuple and the workplan names dictionary. The modal has a Name field, `/add_workplan` and `/update_workplan` carry it, and an empty field clears the name so the generated title returns. The workplans list shows components rather than a title, so it is unaffected
- **D2** The incident modal has a read only "Linked services" table: component, status, date, and the workplan as a link. Fed by a 17th field on the incident tuple, built by `build_incident_service_entry`, and passed to the modal on the edit button of all four pages that list incidents. The date is the service date for completed services and the effective planned date for planned ones
- **D3** The workplan column on the incidents list is now a badge, "📝 2 workplans", above the unchanged services completed counter. The links live in the incident modal from D2
- **D4** Creating a workplan from an incident lists the incident's components as ticked checkboxes in the workplan modal. Unticking one leaves it out, `/add_workplan` receives `component_ids` and `create_workplan` narrows the incident's components to those still selected. Verified end to end: two components on the incident, one unticked, one planned service created and linked to the incident

Tests: 25 pass, including two new ones for the name fallback and for planning only the selected components, plus a migration assertion for the new column.

### Follow-up tweaks asked for on 2026-09-26

- Incidents list, workplan column: the badge is replaced by bold "N workplans" or "No workplan", with the progress wheel from the workplans list instead of the "n/m services completed" line. The wheel shows whenever the incident has services, also when none of them sit on a workplan
- Workplan modal: the checkbox caption reads "Components transferred from incident"
- Incident modal, linked services: the component is a link to its details page with a small grey "Service link" beneath it that closes the incident modal and opens that service in the service record modal. The workplan keeps its link and now shows the workplan's own status beneath it, "Open" while it is planned and "Completed" once it is done. The service modal population moved into `window.openServiceRecordModal`, shared by the edit buttons and this link, and the service modal is now included on the incidents and bike details pages so the link works from all four pages that list incidents

### Second round of tweaks, 2026-09-26

- Incident modal: the "Service link" no longer renders underlined, matching every other link in a table, and the Status column is now "Service status" so it is not confused with the workplan status beneath the workplan name
- Workplans list: the Components column is now "Workplan name" and shows the title. Component names moved to a `data-components` attribute on the row so the search still finds a workplan by the components it covers, and the helper text above the table says so
- Bike details and component details: the workplan tables already showed the title, only the column header said "Description". It now says "Workplan name"
- Bike details and component details, planned services: the due date treatment from C2 is applied here too, header "Due date" and ❗ when the date has passed. It was workplan details only before because the finding named that page, while C5, the bike in parentheses, stays workplan details only as asked. Both payloads now carry `today`

### Third round of tweaks, 2026-09-26

- Incidents list, workplan column: the count sits in its own block so the wheel always falls on the next line, and the column is centred, header included, the way the workplans list centres its progress cell
- Bike details, planned services: the table now has the same ✅ ✍ 🗑 row actions as the planned services tables on component details and workplan details, rather than making the description clickable. Modals open from a visible control everywhere, and the row keeps its single click target, which goes to the component. The edit button returns to the bike page after saving

### Warning when resolving an incident with open services, 2026-09-26

Decided not to block resolution, since the app only blocks where the data would end up inconsistent, completing a workplan, retiring a component, deleting a workplan, while an incident can genuinely be resolved with follow-up work still planned. Instead the incident modal shows the same warning banner pattern the workplan modal uses: with the status set to Resolved and planned services present, it reads "This incident has N planned services that stay planned on their workplans after you resolve it". Frontend only, the count comes from the service list the modal already carries.

Two details worth knowing:

- The banner reacts to the status radios through a delegated listener on the modal, and is refreshed once more after the form is populated, since setting `checked` in code fires no change event
- While building it I first reported a first-open bug, where picking Resolved did not auto-fill the resolution date. That was wrong. The browser automation was clicking before `shown.bs.modal` had fired, and that event is where `initializeIncidentForm` clears the resolution date as part of opening the modal. A person always clicks after the modal has opened, so the behaviour is correct
- What the digging did find, and what is now fixed, is that `initializeIncidentForm` runs on every modal open and attached another change listener to each status radio every time, three opens gave three listeners. The attachment is now guarded by a `data-incident-status-listener` attribute on the form, in the same style as the existing validation guard, so it attaches once. Verified: one listener after three opens, and the resolution date still fills and clears correctly

### Code review outcome, 2026-09-26

Approved with no blockers, review in `.handovers/review/service-integration-reviewer-to-docs-maintainer.md`. Five minor points, resolved as follows:

- Dead reads `read_all_services_by_component` and `read_all_planned_services` removed, together with the one test assertion that used the first
- `workplan_name` changed from `CharField(null=True)` to plain `CharField()`, matching the other fields this branch added. Verified that an empty name still writes SQL NULL, since the app never generates DDL from the models and the business logic normalises empty to None
- Comment added to the skip guard in `migrate_incidents_workplan_link`, that file uses comments, the other backend files do not
- `derive_workplan_context` running twice per render: discarded by the user, no practical impact at production scale
- `renderIncidentServices` now sends names through the new `window.escapeHtml`, so a workplan or component name containing markup renders as text. Verified with a crafted name in the DOM, tags came out as literal text and all three links still work

## Re-test list for the second round

The 2026-09-25 walkthrough still holds for everything the second round did not touch, in particular the migration cases M1 to M5, the workplan rules W1 to W10, retirement N1 to N6 and the regression cases, which were re-verified against the baseline database on 2026-09-26 instead. Worth walking again:

- **Every form that has a date field**, one save each: new and edited component, incident, workplan, service record, installation record, quick swap, collection status change, install component. The date picker submit wrapper changed for all of them, and the automated tests do not cover the browser side
- **P5, P7, P8** planned services from each entry point, with and without a planned date, including a date in the future
- **S1 to S4** service record modal, especially completing without a date, which must now be refused before anything is sent
- **C1, C2, C7** completing services from the new button in the button row on bike and component details, and from the ✅ on a row, including the new row actions on bike details
- **I1 to I4** the incident modal's linked services, the service link, the count and wheel in the list, and the warning when resolving an incident that still has planned services
- **W2, W3** creating and editing a workplan with and without a name, and creating one from an incident with a component unticked
- **N6** collection status change with a note, and the note on an edited installation record

## Suggested order

1. Answer A1 to A5 from the code, they may change what C and D need
2. Decide D1 and D2, since both touch the data model
3. Fix B1 to B3
4. Apply C1 to C8
5. Rerun the automated tests and the regression comparison, A6
6. Update the protocol and the handover, then the code review
