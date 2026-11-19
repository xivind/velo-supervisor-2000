# Stage 2 Design Handover

**Feature/Task:** Stage 2 Design (rewrite): design profile, prototypes, parity checklist, feature issues
**Date:** 2026-11-19 (started)
**Status:** In progress

## Context
Stage 2 decides how the new app looks and works on phone and desktop. Spec: [2026-11-18-stage-2-design.md](../../docs/superpowers/specs/2026-11-18-stage-2-design.md). Plan: [2026-11-18-stage-2-design.md](../../docs/superpowers/plans/2026-11-18-stage-2-design.md). Execution: native (in session), chosen by the user on 2026-11-19. This file is a running log; each task appends to it.

## Status
| Phase | Branch | Tasks | State |
|---|---|---|---|
| Design system `Velo Supervisor 2000` | https://claude.ai/artifact/5sXBCurwjzfyN3YtktBKYA | 2026-11-19 | v0 2026-11-19 |
| Profile v0 preview (throwaway) | https://claude.ai/artifact/KrpinpiaJcbJwWcyVxLbM9 | 2026-11-19 | v0 choices 2026-11-19 |
| A | `feature/stage2-bike` | 1–6 | Tasks 1–3 done |
| B | `feature/stage2-screens` | 7–9 | not started |
| C | `feature/stage2-closeout` | 10 | not started |

## Canvases and design system
| Name | URL | Created | Approved |
|---|---|---|---|
| Design system `Velo Supervisor 2000` | https://claude.ai/artifact/5sXBCurwjzfyN3YtktBKYA | 2026-11-19 | v0 2026-11-19 |
| Profile v0 preview (throwaway) | https://claude.ai/artifact/KrpinpiaJcbJwWcyVxLbM9 | 2026-11-19 | v0 choices 2026-11-19 |

## Approvals
| Date | What |
|---|---|
| 2026-11-18 | Stage 2 spec (PR #387) |
| 2026-11-19 | Stage 2 plan (PR #388) |
| 2026-11-19 | Profile v0: blue accent, Inter, radii 4/8/12/pill, tinted status badges |

## Decisions
1. Retired components show their service and lifetime status badges and wear bars in neutral grey; spare (Not installed) components keep status colours (user, 2026-11-19).
2. `docs/design/prototype-data.json` follows today's rules: the open workplan has 3 planned services on 3 components. Two services on one component in one workplan (#362) is shown only in Task 5's flow artboard.
3. Profile v0 (user): accent `#1d4ed8`, Inter, light only. One colour per status for wear bars, rings and swatches (OK `#1a7f37`, Due `#e5a000`, Exceeded `#a8201a`); badges are a pale tint of it with text in the same hue. Due text is a darker amber (`#8a5a00`) to read on its tint. Trade-off: an amber bar is 2.2:1 on white, so the figure beside a bar always carries the value.
4. Token names add `status-<level>-text` (badge text) beside `status-<level>` (fill) and `-tint`; the checker tests text on tint. The plan assumed `status-<level>` as badge text.
5. The dataset carries master's two computed triggers, `service_trigger` and `lifetime_trigger`, rather than one `trigger`, and an `about` block with the fixed "today" (2026-11-16 12:00). Lists master stores as JSON text are plain lists.

## Prototype dataset
`docs/design/prototype-data.json`, made up. Road bike: 24 installed (3 exceeded, one by time with 2,400 km left; 4 due; 3 Not defined), one compliance issue (no Bell), the 55-character æøå chain name. Gravel bike: 10 installed, 2 collections, tires due by time. Old commuter retired; `Empty frame` has no components. 3 spares, 4 retired, 2 workplans, 6 planned and 6 completed services, 3 incidents (2 open), 15 rides.

## Parity checklist
`docs/design/parity-checklist.md`: 111 rows, 7 browser-only (posted on #386: https://github.com/xivind/velo-supervisor-2000/issues/386#issuecomment-7019679746). Found: Export dataset and Reset database are empty links on `master` with no route behind them (P-092), so drawing them in Config needs a feature issue (Task 9). Creating a workplan from an incident already creates its planned services in one step (P-112); #384 widens that.

## Issues opened
None yet. Known from the spec: #362, #384, #385, #386.

## Next steps
1. Task 4: two or three Bike page directions on a Design canvas `VS2000 Bike directions`; the user picks.
