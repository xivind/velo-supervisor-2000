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

## Next Steps
Task 4 onwards per plan.

## Blockers / Open Questions
None.

## References
- Spec: `docs/superpowers/specs/2026-11-16-stage-1-foundation-design.md`
