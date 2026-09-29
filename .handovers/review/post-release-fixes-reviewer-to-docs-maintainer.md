# code-reviewer -> docs-maintainer Handover

**Feature/Task:** Post-release fixes to v0.5.0 (#351), uncommitted on master
**Date:** 2026-09-30
**Status:** Complete. Verdict: Approved with Minor Issues

## Context
Reviewed `git diff` (excl. graphify-out): service modal dropdowns show all workplans/incidents, incident hash deep link, wording change, progress wheel alignment and 100% state, one test update. 32 tests reported passing. No pattern violations or security problems found.

## Deliverables (files reviewed)
- `backend/utils.py:354` `get_service_incident_options`
- `backend/business_logic.py` four payload builders
- `frontend/static/js/main.js:766` `setServiceModalSelect`, `:4403` hash handler, `:4337` wording
- `frontend/templates/modal_service_record.html`, `workplan_details.html:117`
- `frontend/static/css/custom_styles.css:400,438`
- `tests/test_workplans_incidents.py:258`

## Findings
1. Minor, `main.js:4403-4404`: selector is built by string interpolation from `location.hash`. A hash like `#incident-"]` makes `querySelector` throw a SyntaxError inside the DOMContentLoaded callback (uncaught, page otherwise fine, it is the last statement). Percent-encoded values are not decoded either. Fix: `CSS.escape(...)` on the id, or find the button with `Array.from(document.querySelectorAll('.edit-incident-btn')).find(button => button.dataset.incidentId === incidentId)`. Real ids are safe, so low urgency.
2. Minor, `utils.py:354` / `business_logic.py`: on incident reports (and bike details) the payload already contains `incident_reports_data` with id, status, component ids and title. `get_service_incident_options` recomputes titles with 2-3 queries per incident (read_component_names does one query per component, read_bike_name one). At ~15 incidents this is roughly 50-100 small SQLite queries per page load on four pages: acceptable, not a blocker. Where `incident_reports_data` is already built, the template could derive options from it (fields 0, 2, 4, 12) with no extra queries. Workplan details uses `incidents_data`, which is scoped to that workplan, so it still needs the new helper. Optional; note as tech debt in #356 if not done.
3. Minor, `modal_service_record.html:73`: `data-component-ids='{{ ...|tojson }}'` is safe (Jinja `tojson` escapes `'`, `<`, `&`), just relies on that. Leave as is.
4. Minor, `main.js:766` comment says "showing only options selectable for the component plus the linked one". Fine, but the fallback "Linked (id)" option, once appended, stays in the select for the page session. It is correctly re-hidden on the next call (no dataset, not the linked value), so no bug.

## Checked and OK: setServiceModalSelect
- New service (value ''): every option with a value is hidden and disabled unless selectable; `select.value = ''`. Correct.
- Edit, linked selectable value: option visible and enabled, submitted. Correct.
- Edit, linked non-selectable value (Done workplan, Resolved incident): kept visible and enabled, name shown, submitted. Correct.
- Switching services: every call recomputes hidden/disabled for all options, so a previously linked option is re-hidden. Correct.
- Workplan call without `componentId`: `componentIds` is null for workplan options, so only `data-selectable` decides. Correct.
- Incident with empty component list and status Open: `'[]'` parses to `[]` (truthy), `includes` false, hidden. Intended.
- `componentId` undefined (no component context): only the linked incident shows. Acceptable; `openServiceRecordModal` callers (`:849` dataset, `:4350` incident modal) both pass componentId.
- Status strings "Open"/"Planned" match the values used elsewhere in templates.

## Convention check
- Layer separation OK: helper in utils takes `database_manager` per #282 precedent, payload value assigned to a variable first, no DB in routes.
- Helper uses `parse_json_string(...) or []` and existing `generate_incident_title`; no reuse gap except finding 2.
- No new inline comments beyond the existing `// Function to ...` header style in main.js; the one added comment at `:4402` follows the file's pattern. All JS in main.js, all CSS in custom_styles.css.
- Bootstrap utilities used for the wheel fix (`mt-0 align-text-bottom`); the two CSS additions are necessary (mask and hover specificity cannot be done with utilities).
- No logging changes needed; nothing new can fail silently.
- Test change is adequate; a one-line assertion for a Resolved incident (kept in the options) would document the reason for the change. Optional.

## Next Steps for docs-maintainer
1. CHANGELOG entry under next patch version (v0.5.1): fix names of linked Done workplans / Resolved incidents in service modal; incident selectable on bike, workplan and incident pages; "View incident" opens the incident; wording Done/Planned; progress wheel alignment and checkmark.
2. Suggested commits (human commits; use Refs, never Closes):
   - `Show names of linked workplans and incidents in the service modal` body: all workplans and incidents rendered as options, non-selectable ones hidden; incident options added to bike, incident and workplan pages. `Refs #351`
   - `Open the incident from the View incident link in the service modal` `Refs #351`
   - `Fix progress wheel alignment and checkmark, use Done/Planned wording for linked services` `Refs #351`
   Or one combined commit "Post-release fixes for service integration" `Refs #351`.
3. Optionally add finding 2 to #356.

## Blockers / Open Questions
- None.

## References
- Issue #351 (service integration), #356 (tech debt), #282 (database_manager in utils precedent)
- Related handover: `.handovers/review/` earlier #351 review
