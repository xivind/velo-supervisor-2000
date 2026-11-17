# Stage 1 Foundation Handover

**Feature/Task:** Stage 1 Foundation (rewrite), integrity extractor
**Date:** 2026-11-16
**Status:** In Progress

## Context
Stage 1 builds the integrity extractor and compare tools that prove later restructuring leaves results unchanged. Finalised in Task 19.

## Deliverables
- `scripts/integrity/extract.py` - extract(checkout, db, scenario) and CLI
- `scripts/integrity/compare.py` - diff, summary, "Present on both sides"
- `tests/integrity/test_compare.py`

## Progress log

### Task 3, step 5: failing-comparison proof
Exported `master` twice with `git archive`; in one copy changed `total_distance = current_distance + distance_offset` to `+ distance_offset + 1` in `update_component_distance`. Ran `scripts/integrity/extract.py --checkout <export> --db <prod copy> --out <json>` on both and `compare.diff`. Outcome: 4739 differences, 1207 in stored values; component distances shifted by 1 km. The comparison detects the change.

### Task 3, step 6: baseline dev vs master
`uv run python scripts/integrity/compare.py --ref master --db <prod copy> --out-dir <scratchpad>/baseline`. Exit code 0, "identical". Rows per table: bikes 17, collections 14, component_history 1035, component_types 50, components 638, incidents 15, rides 7449, services 228, workplans 12.

Present on both sides: 10 components without installation history, handled by process_history_records' 'No history records' path, identical on both sides. No derived errors.

### Task 4, step 9: src layout vs master
`uv run python scripts/integrity/compare.py --ref master --db <prod copy> --out-dir <scratchpad>/after-move`. Exit code 0, "identical". Rows per table: bikes 17, collections 14, component_history 1035, component_types 50, components 638, incidents 15, rides 7449, services 228, workplans 12, same as the baseline.

Present on both sides: the same 10 `process_history_records` 'No history records' lines. No derived errors.

### End of Phase B (after Tasks 5-7: version from git tag, config from `VELO_SUPERVISOR_CONFIG`, new Docker image)
Same command, `--out-dir <scratchpad>/phase-b-end`. "identical", same row counts, same 10 lines present on both sides, no derived errors. CI run 43971553671: `test` and `docker` green; footer version `0.5.1.dev90+g6b451009a`.

## Decisions Made
1. `extract` output carries `recalculation_failures`, so a failure shows in a diff.
2. `db_migration.py` does not read `config.json` (it searches for the database file and asks), so it needed no change for the config location; the spec said otherwise. README line 150 is corrected in Task 17.
3. The Docker build stage restores tracked files hidden by `.dockerignore` before `uv sync`, so the version has no dirty-tree suffix; CI fails on a dirty suffix and, on a tag, requires the version to equal the tag.
4. Curated graphify community labels (63 of 144 lost in the move) are relabelled once in Task 19.

## Switch-over steps for the Pi (Stage 6)
- Move `config.json` to `/data/config.json`.
- `/data`, `/data/logs` and `/secrets` writable by UID 1000. `strava_tokens.json` in `/secrets` is shared with the sync-strava and update-strava containers: if they rewrite it as root, VS2000 can no longer refresh the token. Check ownership after their next run.
- Turn on required checks for `master` branch protection.

## Stage 2 parity checklist (from removed docs)
UI-only behaviour from the #351 spec, findings and manual protocol (git history before the Task 18 deletion commit). The backend rules behind them are in `tests/rules/`.
- Plan services modal preselects: component (itself), bike (installed, non-retired), collection (members), incident (its components, no workplan), workplan (workplan locked, no components). Retired components are not listed.
- Date pickers: planned date and due date accept future dates; service, completion and resolution dates do not. Invalid or missing dates are refused before any request. One save through every form with a date field.
- Complete services modal: planned services listed ticked as "component: description", date defaults to now, retired rows disabled; the row ✅ lists only that service. "Complete services" sits in the button row on bike and component details, disabled when nothing is planned or the component is retired.
- Planned services tables (bike, component, workplan details): "Due date" shows the effective planned date, ❗ when passed; ✅ ✍ 🗑 row actions on all three; the row opens the component.
- Workplan details: bike and component badges, progress wheel "n/m", bike per component in parentheses or "(Not assigned)"; banners for no services, all services completed, and completed on <date> (actions disabled); "Complete workplan" disabled while planned services remain; close-linked-incidents checkbox; "Edit details" label.
- Workplans list: "Workplan name" column, search also matches component names, centred progress wheel with a checkmark at 100%.
- Workplan modal: no bike or component selects; optional name (empty gives the generated title); due date required; from an incident (📝) the description is prefilled and its components are ticked checkboxes, "Components transferred from incident".
- Incident modal: no workplan dropdown (#345); read-only linked services (component link, "Service link" that opens the service modal, service status, date, workplan link with Open/Completed), names escaped; resolving with planned services shows a warning but saves; the status radios fill and clear the resolution date.
- Incidents list: workplan column "N workplans" or "No workplan" plus progress wheel; 📝 and 🧑‍🔧 disabled on resolved incidents (the backend does not block planning for them).
- Service record modal: Planned hides the service date and shows the planned date; workplan options are Planned workplans and incident options Open incidents naming the component, plus the linked one with its name even when Done or Resolved; "View workplan" and "View incident" links; `#incident-<id>` opens that incident.
- Notes: installation history Notes column ("-" when blank); "Notes for status change" on status change, quick swap and collection status change (with the "same note on every component" line); the edit installation record modal edits the note, status read-only.
- Uninstalling from the status modal with no bike selected submits (empty optional form fields are accepted).

## Next Steps
Task 4 onwards per plan.

## Blockers / Open Questions
None.

## References
- Spec: `docs/superpowers/specs/2026-11-16-stage-1-foundation-design.md`
