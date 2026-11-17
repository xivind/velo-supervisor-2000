# Stage 1 Foundation Handover

**Feature/Task:** Stage 1 Foundation (rewrite): layout, Docker, CI, release flow, tests, integrity comparison
**Date:** 2026-11-17
**Status:** Complete

## Context
Stage 1 built the safety net later stages lean on: a result extractor and comparison against `master`, characterisation and rule tests, CI and a new release flow, on a standard src layout. No calculation logic changed. PRs #368, #370, #379 and this branch (`feature/stage1-finish`).

## Deliverables
- `src/velo_supervisor/` package (templates, static), `config/` starting files, `Dockerfile` (multi-stage, UID 1000, `VELO_SUPERVISOR_CONFIG=/data/config.json`), version from the git tag (hatch-vcs)
- `scripts/integrity/`: `extract.py` (stored + derived state as JSON, fixed clock), `compare.py` (ref vs working tree), `delta.py`
- `tests/`: characterisation, rules, pages, strava, integrity, `test_*.py`; dataset builder and expected files in `tests/fixtures/` (see `tests/README.md`)
- `.github/workflows/tests.yml` (test, lint, docker), `dependabot.yml`, `release.yml`; branch protection on `master` and `staging`
- Docs: README, `tests/README.md`, CLAUDE.md (incl. "CI and workflow"), every `.claude/agents/*.md`, `.handovers/CLAUDE.md`, roadmap

## Decisions Made
1. Operation expected files hold deltas (before/after per changed path, `<absent>` marker), and each test first asserts its "before" equals `recalculation.json`. Full snapshots per operation were 2.3 MB and unreviewable for one maintainer.
2. Recalculation failures are data: `extract` returns sorted `recalculation_failures` lines, and `compare.py` lists failures and derived errors "present on both sides", so an identical failure is seen rather than silently equal.
3. IDs created during a scenario are normalised to `new:<table>:<n>` in both the stored and the derived layer, so outputs repeat.
4. The Docker build restores tracked files hidden by `.dockerignore` before `uv sync`, so a tagged build shows a plain `0.5.x` without a dirty-tree suffix; CI fails on a dirty suffix and checks tag equality.
5. Releases are made on the GitHub Releases page, not a custom workflow (spec choice). Found: every existing tag points at the commit before its release content.
6. `db_migration` does not read `config.json` (it searches home folders and asks), so the config location needed no change there; the spec said otherwise.
7. Required checks can only be switched on where the workflow exists: `staging` after the next `dev` → `staging` merge, `master` at switch-over (Stage 6). Both require PRs, 0 approvals, admins included.
8. User decisions: all old tests rewritten (32 mapped), legacy docs and handovers deleted once covered; `httpx2` as dev dependency (starlette TestClient); issue references in docstrings, not comments.

## Comparison against master (production copy, recalculation + derived values)
| Point | Result |
|---|---|
| Baseline, before the move (Task 3) | identical |
| After the src move (Task 4), and end of Phase B | identical |
| End of stage (2026-11-17, HEAD of `feature/stage1-finish`) | identical |

Every run: same row counts (bikes 17, collections 14, component_history 1035, component_types 50, components 638, incidents 15, rides 7449, services 228, workplans 12); the same 10 `process_history_records` "No history records" failures on both sides; no derived errors. A mutation proof (+1 km in `update_component_distance`) gave 4739 differences.

## Using the extractor and comparison
- `uv run python scripts/integrity/compare.py --ref master --db <copy> --out-dir <folder outside the repo>`; exit 0 and "identical" means no difference. Run it whenever a change touches calculations, and at the end of Stages 4 and 6.
- Never commit the database copy or its outputs. Record counts and kinds only in public files.
- Expected files are never overwritten: a missing file is recorded only with `RECORD_EXPECTED=1`; changing one means deleting it by hand with a documented reason (issue or feature).

## Issues opened
#369 (config lost on redeploy; addressed on `dev` by config on `/data`), #371, #372, #373, #374, #375, #376, #377, #378, #380 (template `in_use`; addressed on `dev`). All on the Sprintboard with P0. Bugs are pinned as the code behaves, with the issue in the test docstring. #12 decided: count only `Ride`, `MountainBikeRide` and `GravelRide` (by `sport_type`); done as its own change right after Stage 1.

## Coverage (289 tests, total 80%)
| Module | Cover | Uncovered |
|---|---|---|
| business_logic | 89% | error and `except` branches; quick swap and collection status failure paths; time-based fallbacks in `update_component_lifetime_service_alternate`; compliance warning in `modify_component_details` |
| database_manager | 88% | `except` branches of `write_*`; `write_delete_record` not-found/invalid paths; `read_workplans_by_incident` |
| db_migration | 58% | interactive path finding and prompts; legacy migrations the template has already passed |
| main | 50% | POST route handlers (operations are tested at service level), `lifespan`, `delete_record` route |
| scheduler | 21% | not tested (jobs, start, stop) |
| strava | 81% | token refresh in `get_bikes`/`get_athlete_bikes`, error branches |
| utils | 92% | `read_filtered_logs` (fixed `/data/logs` path), some date validation branches |
| middleware | 92% | `handle_exception` branch |
| database_model | 100% | none |

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
1. Stage 4 route tests must cover two rules held only by routes today: workplan due date is required (`Form(...)`, no backend check); empty optional form fields are accepted on uninstall.
2. Switch-over on the Pi (Stage 6, also in the roadmap): move `config.json` to `/data/config.json` (container paths as in `config/config.json.example`); `chown -R 1000:1000` `/data` (including root-owned `/data/logs/app.log*`, which otherwise crash-loop the container at log config load) and `/secrets`; check `strava_tokens.json` ownership after sync-strava/update-strava run (if they rewrite it as root, token refresh fails); `git pull` so the tag reaches the build; run the migration with `docker exec -it velo-supervisor-2000 python -m velo_supervisor.db_migration` (or `uv run python -m ...` from a checkout); switch on required checks `test`, `lint`, `docker` for `master`.
3. Right after the next `dev` -> `staging` merge: switch on required checks `test`, `lint`, `docker` for `staging` (pending).
4. Stage 3/4 extractor guidance: (a) the stored layer and every expected file are keyed by raw table and column names, so a schema change needs a projection in `snapshot.stored_state` back onto master's tables and columns, or a documented re-record agreed with the user; (b) `compare.py` runs the working tree's `derived.py` against both sides, so derived-mapping changes must keep reading master's flat layout (branch on `AppModules.layout`); (c) when tables change, add a primary-key uniqueness assert in `stored_state` (it takes the first PK column and keys a PK-less table by its row JSON).
5. Stage 3/4 prerequisite: a CI test that extracts `git archive origin/master` and the working tree on the synthetic dataset and diffs them (fast master comparison on every PR; CI has fetch-depth 0). `tests/strava/` is a package named `strava` and would shadow master's flat `strava` module in an in-process flat-layout test: run it in a subprocess or rename the test package.

## Blockers / Open Questions
- [DONE 2026-11-17] Release backfill: every tag had been created one release early (tag, then merge). With the maintainer's approval 13 tags were moved to the first master commit that contains their release (README numbering wins), v0.4.6 was created at #315, v0.1.0 kept; 15 GitHub Releases published, v0.5.0 latest. Old clones need `git fetch --tags --force`.
- [DONE 2026-11-17] graphify: communities relabelled with descriptive names (183 communities) via `graphify label . --backend=claude-cli`; without a backend it falls back to file names.
- Deferred minors worth a later look: `stored_state` could open the database read-only; new-ID normalisation is keyed by bare value, so one new ID in two tables collapses; `create-container-vs2000.sh` has no `set -e`.

## References
- Spec: `docs/superpowers/specs/2026-11-16-stage-1-foundation-design.md`; roadmap: `docs/superpowers/specs/2026-11-15-rewrite-roadmap-design.md`
- Issues #364, #121, #11, #356
