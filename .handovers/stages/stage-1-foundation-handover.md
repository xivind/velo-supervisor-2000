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

## Decisions Made
1. `extract` output carries `recalculation_failures`, so a failure shows in a diff.

## Next Steps
Task 4 onwards per plan.

## Blockers / Open Questions
None.

## References
- Spec: `docs/superpowers/specs/2026-11-16-stage-1-foundation-design.md`
