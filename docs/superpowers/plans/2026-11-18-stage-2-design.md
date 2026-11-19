# Stage 2 Design Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce the approved design profile, phone and desktop prototypes, parity checklist and feature issues that Stage 2 of the rewrite requires, and record them in the repo.

**Architecture:** The look is chosen on the Bike page, then built outward (approach C). The profile lives in a claude.ai Design System artifact and the prototypes in Design canvases while we iterate. The repo holds the record: a running stage handover, a made-up prototype dataset, the parity checklist, a token checker, and at the end the exported profile and screenshots. Work runs in three phases on three feature branches off `dev`.

**Tech Stack:** claude.ai Design System and Design artifact types (via the Artifact tool), Lucide icons (Tabler as fallback), Python 3.12 and pytest for the token checker, `gh` for issues and the Sprintboard.

**Spec:** `docs/superpowers/specs/2026-11-18-stage-2-design.md` (approved 2026-11-18). Read it before any task; this plan does not repeat its reasoning.

## Global Constraints

- No application code, templates or CSS. The only code is `scripts/design/check_tokens.py` and its test.
- Made-up data only, from `docs/design/prototype-data.json`. Never production names or rides. The repository is public.
- Statuses are exactly `master`'s: OK, Due for service, Due for replacement, Service interval exceeded, Lifetime exceeded, Not defined; installation statuses Installed, Not installed, Retired. No new levels.
- Light only. English UI. No emoji anywhere on a canvas. Icons are Lucide; Tabler only for a glyph Lucide lacks.
- Artboards: phone 390×844, desktop 1440 wide. Every screen is drawn for both.
- Text contrast at least 4.5:1 (3:1 at 24 px and up). Touch targets at least 44 px.
- Rules that protect data (spec, Constraints) are never relaxed on a canvas. A canvas that needs a rule or operation the backend lacks gets a feature issue first.
- New issues: project #2 "Sprintboard Velo Supervisor 2000", Priority P0, Status Ready. Commit messages use "Refs #N", never "Closes" or "Fixes".
- Approval is the user's alone, per canvas. @thomiz's review never blocks a task. Every approval is recorded in the handover with its date.
- The handover stays within CLAUDE.md's 100 lines. Detail belongs in the parity checklist and the design system, not the handover.
- Canvas and design-system files are built in the session scratchpad, never in the repo, and published with the Artifact tool. Every canvas and design-system URL is written into the handover as soon as it exists, because sessions are fresh.
- Where `.claude/agents/ux-designer.md` conflicts with the spec (Bootstrap-first, follow existing templates), the spec wins. That file is updated in Task 10.
- Commits and pushes: the user authorised committing on the Stage 2 feature branches, pushing them and opening pull requests to `dev`. Never commit to `dev`, `staging` or `master`, never merge. Each phase starts from `dev` after the user has merged the previous phase.
- Tests and lint pass before every pull request: `uv run pytest -q`, `uv run ruff check && uv run ruff format --check`.

## Review Focus

1. **Long names with æ, ø, å** (a 55-character Norwegian component name, as in real use). Expected: the row wraps or truncates cleanly on a 390 px phone, and the full name shows in the item view. Pinned by the dataset (Task 1) and checked on every list artboard (Tasks 4, 5, 7).
2. **Empty states:** a bike with no components, no planned services, no open incidents. Expected: a short explanation and the action that fills it, not a blank area. Pinned by the dataset's empty bike (Task 1) and its artboards (Tasks 5, 7, 8).
3. **"Not defined" components** (no interval or lifetime set). Expected: shown with their own badge, sorted after OK, never shown as OK. Pinned by the dataset (Task 1) and the sort check (Task 4).
4. **A component overdue by days with plenty of km left.** Expected: sorted among the exceeded ones, with the badge saying time triggered it. Pinned by the dataset (Task 1) and the sort check (Task 4).
5. **Actions refused:** a future service date, or planning a service on a retired component. Expected: the refused date shows an inline message on the field; on a retired component the service actions are not offered, and the view says why. Pinned in Task 5's flow artboards.

---

## Phase A: setup, parity inventory, profile and Bike page, branch `feature/stage2-bike`

### Task 1: Handover log and prototype dataset

**Files:**
- Create: `.handovers/stages/stage-2-design-handover.md`
- Create: `docs/design/prototype-data.json`

**Interfaces:**
- Produces: the handover with sections `Status`, `Canvases and design system` (table: name, URL, created, approved), `Approvals` (date, what), `Decisions`, `Issues opened`, `Next steps`. Every later task appends to it.
- Produces: `prototype-data.json` with top-level keys `bikes`, `components`, `component_types`, `services`, `workplans`, `incidents`, `collections`, `rides`, each a list of objects whose field names match `master`'s table columns (`bike_id`, `bike_name`, `component_name`, `component_type`, `installation_status`, `service_status`, `lifetime_status`, `service_next`, `lifetime_remaining`, `service_next_days`, `lifetime_remaining_days`, …) plus a display-only `trigger` (`distance`, `time`, `both`, or null).

- [ ] **Step 1:** Write the handover skeleton from `.handovers/TEMPLATE.md`, status "In progress", with the spec and plan linked and the PR #387 approval of the spec recorded (2026-11-18).
- [ ] **Step 2:** Write the dataset, built on the synthetic bikes in `tests/fixtures/dataset.py` (Road bike, Gravel bike, Old commuter). It must contain:
  - Road bike active with 24 installed components covering every service and lifetime status, including at least 2 exceeded, 3 due, 2 Not defined, and 1 overdue by days with more than 1,000 km left (`trigger: "time"`);
  - component types with `mandatory` and `max_quantity` (master's columns), set so Road bike has one compliance issue: one mandatory type missing (master's `process_bike_compliance_report` counts missing mandatory types and types over their max quantity);
  - one component named `Kjede Shimano CN-HG701 11-delt «Grønn» bakhjul æøå 2026` (longer than 50 characters);
  - 3 spare components (Not installed), 4 retired;
  - Gravel bike active with 2 collections (a wheelset and a drivetrain);
  - Old commuter retired, and one new bike `Empty frame` with no components;
  - 2 workplans (one with 3 planned services across 2 components, one completed), 3 planned services outside workplans, 6 completed services;
  - 2 open incidents (one naming only the bike, one naming 2 components), 1 resolved;
  - 10 rides on Road bike and 5 on Gravel bike, so Stats has more than one bike to compare.
- [ ] **Step 3: Check the dataset**

Run: `python3 -I -c "import json;d=json.load(open('docs/design/prototype-data.json'));c=d['components'];print(sorted({x['service_status'] for x in c}|{x['lifetime_status'] for x in c}), sorted({x['installation_status'] for x in c}), max(len(x['component_name']) for x in c))"`
Expected: all six statuses, all three installation statuses, and a name length above 50.

- [ ] **Step 4: Commit**

```bash
git add .handovers/stages/stage-2-design-handover.md docs/design/prototype-data.json
git commit -m "Start the Stage 2 handover and the prototype dataset"
```

### Task 2: Parity inventory

**Files:**
- Create: `docs/design/parity-checklist.md`

**Interfaces:**
- Produces: one table with columns `ID | Old behaviour | Where on master | New design | State | Note`. `ID` is `P-001`, `P-002`, …; `State` is one of `open`, `covered`, `dropped`, `browser-only`. Later tasks change `New design` (canvas name and artboard) and `State`.

- [ ] **Step 1:** Walk `master` (`git show master:frontend/templates/<file>`, `master:frontend/static/js/main.js`, `master:backend/main.py`). Write one row per user-visible behaviour of every page (11), every modal (20), every POST route (19), and the two GET routes that change data (`/refresh_all_bikes`, `/refresh_rides/{mode}`).
- [ ] **Step 2:** Add the seed rows the spec names: the Stage 1 handover list "Stage 2 parity checklist", #37, #128, #145, workplan due date required, empty optional fields accepted on uninstall. Mark the spec's decided drops `dropped` with the reason (submit-issue link, database path, load time, retired components and expected cost on the bike page, emoji). Leave the Config button order settings `open` with the note "probably dropped, decide in Task 9".
- [ ] **Step 3:** For every validation in `main.js` that the server does not check, add a row with `State` `browser-only`. Post the list as a comment on #386.
- [ ] **Step 4: Check coverage**

Run: `for f in $(git ls-tree --name-only master frontend/templates/ | xargs -n1 basename); do grep -q "$f" docs/design/parity-checklist.md || echo "missing $f"; done; for r in $(git show master:backend/main.py | grep -oP '@app\.(get|post)\("\K[^"]+' | grep -vx '/health'); do grep -q "$r" docs/design/parity-checklist.md || echo "missing $r"; done`
Expected: no output.

- [ ] **Step 5:** Record in the handover: row count, browser-only count, the #386 comment link.
- [ ] **Step 6: Commit**

```bash
git add docs/design/parity-checklist.md .handovers/stages/stage-2-design-handover.md
git commit -m "Add the Stage 2 parity inventory" -m "Refs #386"
```

### Task 3: Thin profile v0 and the token checker

**Files:**
- Create: `scripts/design/check_tokens.py`
- Create: `scripts/design/__init__.py` (empty)
- Create: `tests/design_profile/test_check_tokens.py` (no `__init__.py`, like `tests/integrity/`; a test package named `design` would shadow `scripts/design`, which pytest reaches through `pythonpath = ["scripts"]`). Import: `from design.check_tokens import PAIRS, check, contrast_ratio`
- Scratch: the design system's `project/` folder

**Interfaces:**
- Produces: a Design System artifact titled `Velo Supervisor 2000`, holding `tokens.json`, a one-paragraph `README.md` and the cover. Colour token names, used by every later task: `surface`, `surface-raised`, `ink`, `ink-muted`, `line` (dividers only; control borders and focus rings use `ink-muted` and `accent`, which meet 3:1), `accent`, `on-accent`, `accent-tint` (a background for `ink` text, such as a selected row or tab), and per status `status-ok`, `status-due`, `status-exceeded`, `status-undefined`, `status-retired`, each with a `-tint` partner (badge background). Radius tokens `radius-sm`, `radius-md`, `radius-lg`; one font family token `sans`.
- Produces: `contrast_ratio(a: str, b: str) -> float` (WCAG 2.1 relative luminance, hex input), `check(tokens: dict) -> list[str]` (one message per failing pair, formatted `"<fg>/<bg>: <ratio> < <minimum>"`, plus `"missing <name>"` for a token named in `PAIRS` but absent; empty when all pass; a token's value is either a string or `{"light": …}`, and an alias `"{other-token}"` is resolved, as the design system allows both), and `PAIRS: list[tuple[str, str, float]]` in `scripts/design/check_tokens.py`; `main()` reads a path argument, prints failures, exits 1 on any.
- `PAIRS`: `ink`/`surface` 4.5, `ink`/`surface-raised` 4.5, `ink`/`accent-tint` 4.5, `ink-muted`/`surface` 4.5, `ink-muted`/`surface-raised` 4.5, `on-accent`/`accent` 4.5, `accent`/`surface` 3.0, and `status-X`/`status-X-tint` 4.5 for each of the five statuses. Also in `PAIRS`: `status-ok`/`status-due`, `status-ok`/`status-exceeded` and `status-due`/`status-exceeded` at 1.3, so they differ in lightness.
- Status mapping, fixed for every canvas: OK → `status-ok`; Due for service and Due for replacement → `status-due`; Service interval exceeded and Lifetime exceeded → `status-exceeded`; Not defined → `status-undefined`; Retired → `status-retired`. Each of the five also has its own Lucide icon, named in the README (spec, profile item 1: lightness and icon, not hue alone). Installed and Not installed use neutral badges (`ink-muted` on `surface-raised`). The badge label always names the exact status, so the shared colour never hides which one it is.
- *Decided with the user (2026-11-19):* a retired component shows the Retired badge, and its service and lifetime status badges and wear bars stay visible but in neutral grey. `master` keeps computing them (the production copy has 122 retired components at "Service interval exceeded"), and the warning colour would look like work to do. A Not installed (spare) component keeps its status colours, because it can be installed again.

- [ ] **Step 1: Write the failing tests**

```python
def test_contrast_ratio_black_on_white():
    assert round(contrast_ratio("#000000", "#ffffff"), 1) == 21.0

def test_check_reports_failing_pair():
    tokens = tokens_with(ink="#777777", surface="#ffffff")
    assert any("ink/surface" in m for m in check(tokens))

def test_check_passes_valid_profile():
    assert check(tokens_with()) == []

def test_status_colours_must_differ_in_lightness():
    tokens = tokens_with(**{"status-ok": "#1a7f37", "status-due": "#1b7f38"})
    assert any("status-ok/status-due" in m for m in check(tokens))

def test_check_resolves_alias():
    tokens = tokens_with(**{"on-accent": "{surface}"})
    assert not any("on-accent" in m for m in check(tokens))
```

`tokens_with(**overrides)` builds a minimal valid `tokens.json` dict in the design system's list shape (`{"color": {"themes": [{"id": "light"}], "tokens": [{"name", "value": {"light": hex}}]}}`).

- [ ] **Step 2:** Run `uv run pytest tests/design_profile -q`. Expected: FAIL (module not found).
- [ ] **Step 3:** Implement `scripts/design/check_tokens.py` with the interfaces above. It reads the `light` value of each token.
- [ ] **Step 4:** Run `uv run pytest tests/design_profile -q && uv run ruff check scripts tests && uv run ruff format --check scripts tests`. Expected: PASS.
- [ ] **Step 5:** Choose the v0 palette (calm base, one strong sporty accent), font (open licence, tabular figures) and radii, and propose them to the user in one message. Then create the Design System artifact and publish it with the chosen values.
- [ ] **Step 6:** Run `uv run python scripts/design/check_tokens.py <scratch>/project/tokens.json`. Expected: exit 0, no output.
- [ ] **Step 7:** Write the design system URL into the handover.
- [ ] **Step 8: Commit**

```bash
git add scripts/design tests/design_profile .handovers/stages/stage-2-design-handover.md
git commit -m "Add the design token contrast checker and profile v0"
```

### Task 4: Bike page directions

**Interfaces:**
- Consumes: the design system (Task 3), the dataset (Task 1).
- Produces: a Design canvas `VS2000 Bike directions` with 2 or 3 directions. Each direction has a phone and a desktop artboard of the Bike page (top section and component list, same content), plus the menu drawer on phone.

- [ ] **Step 1:** Build the canvas, install the design system, and draw every direction from the same Road bike data. Directions differ in look (accent use, density, top-section treatment), not in layout or content.
- [ ] **Step 2: Check each phone artboard.** At least 5 component rows show above the bottom bar without scrolling. The long æøå name is handled. The rows follow "most urgent first" (spec): exceeded, then due, then OK, then Not defined; within a status by km remaining (worse of service and lifetime); the time-triggered component is among the exceeded rows.
- [ ] **Step 3:** Write the canvas URL into the handover. Send the user the link with one line per direction.
- [ ] **Step 4:** The user picks a direction, or a mix. Record the choice and date in the handover and update the tokens to the pick. `check_tokens.py` passes on the updated tokens.
- [ ] **Step 5: Commit**

```bash
git add .handovers/stages/stage-2-design-handover.md
git commit -m "Record the chosen Stage 2 visual direction"
```

### Task 5: Bike page refined, with component view and workshop flows

**Interfaces:**
- Consumes: the chosen direction (Task 4).
- Produces: a Design canvas `VS2000 Bike`. Phone and desktop artboards for:
  - the bike list (active first, retired after) and the bike switcher;
  - the Bike top section and every lower list (components, services, workplans, incidents, collections, rides). Tapping a count in the top (for example "3 due service") opens that list filtered; the compliance count shows which type is missing or over its maximum. The bike's collections show as shortcuts in the top;
  - the phone bottom bar: `Service` and `Install`, each opening its sheet, and `⋯` for the rest (spec, Actions), shown on the bike and inside a component view, where it acts on that component;
  - the component item view, including a retired component. On phone the top shrinks to a slim bar inside the item;
  - empty states for `Empty frame`;
  - the menu drawer.
- Clickable flows (`is_interactive`, linked artboards):
  - Log service: complete a planned one, or log a new one;
  - Plan service on 2 components into a new workplan (#384), and 2 services on one component in one workplan (#362);
  - quick swap;
  - install a spare component on the bike;
  - collection status change;
  - the selection bar with Plan, Log and Uninstall, with nothing preselected that the user did not tick (#365);
  - refused input (future service date) with its inline message;
  - the confirm dialog for bulk uninstall;
  - a success toast;
  - an error banner (for example "Strava could not be reached").

- [ ] **Step 1:** Build the canvas and write its URL into the handover.
- [ ] **Step 2:** Check that every artboard and flow in the list above exists in both phone and desktop. Check that the retired component offers no service actions and says why (Review Focus 5).
- [ ] **Step 3:** For bulk Log service and bulk Uninstall on a selection, check `src/velo_supervisor/business_logic.py` on `dev`. For each operation the backend lacks, open an issue (Global Constraints) and link it from the flow artboard.
- [ ] **Step 4:** Update the parity checklist: rows these artboards cover become `covered`, with canvas and artboard named.
- [ ] **Step 5:** The user approves. Record the approval and date in the handover.
- [ ] **Step 6: Commit**

```bash
git add docs/design/parity-checklist.md .handovers/stages/stage-2-design-handover.md
git commit -m "Record the approved Bike page and workshop flows"
```

### Task 6: Profile v1

**Interfaces:**
- Consumes: the approved Bike canvas (Task 5).
- Produces: the design system with a component entry (guidelines and live preview) for each of:
  - buttons (primary, secondary, quiet, danger);
  - badge;
  - progress ring;
  - wear bar;
  - list row;
  - top section;
  - tabs;
  - menu and drawer;
  - selection bar;
  - bottom bar;
  - sheet and dialog;
  - form field (with date picker);
  - empty state;
  - toast;
  - banner.

  Its README covers every item in the spec's profile list (1 to 10), including the notifications system, writing rules and the third-party licence list (Lucide ISC, Tabler MIT, the font's licence).

- [ ] **Step 1:** Extract every building block above from the Bike canvas into the design system. Values must be those already on the canvas.
- [ ] **Step 2:** Run `check_tokens.py` on the design system's `tokens.json`. Expected: exit 0.
- [ ] **Step 3:** Check that the README has a section for each of the spec's profile items 1 to 10.
- [ ] **Step 4:** The user approves the profile. Record it in the handover.
- [ ] **Step 5:** Commit the handover, push, and open the Phase A pull request to `dev` with "Refs #194, #363".

---

## Phase B: the remaining screens, branch `feature/stage2-screens`

Every canvas in this phase uses the design system. Where a canvas needs a building block that isn't there yet, add it to the design system first (guidelines and preview), and note it in the handover.

### Task 7: Inventory

**Produces:** a Design canvas `VS2000 Inventory`. Phone and desktop artboards for:
- the Inventory top section;
- every list, with its filter, search and sort (components including spares and retired, services, workplans, incidents, collections);
- Back returning to a filtered list with its filters kept (#128);
- the component view opened from Inventory.

- [ ] **Step 1:** Build the canvas and write its URL into the handover. The long name and the Not defined components show in the component list.
- [ ] **Step 2:** Check the component view here differs from Task 5's only in the top section (anti-goal: an item view looks the same from Bike and Inventory).
- [ ] **Step 3:** Update the parity checklist rows these artboards cover.
- [ ] **Step 4:** The user approves. Record it in the handover. Commit.

### Task 8: Item views

**Produces:** a Design canvas `VS2000 Item views`. Phone and desktop artboards for:
- the service, workplan, incident and collection views, each with its links both ways (spec, Services, incidents and workplans);
- editing a service from its view;
- the workplan's progress ring and its "expected replacement cost";
- completing a workplan with its linked incidents closed;
- creating an incident (bike only, components only, both), and the inline message when neither is named (#386).

One view (the workplan) is drawn once in Bike scope and once in Inventory scope, side by side, to show they are the same.

- [ ] **Step 1:** Build the canvas and write its URL into the handover.
- [ ] **Step 2:** Check the two workplan artboards differ only in the top section.
- [ ] **Step 3:** Update the parity checklist. The user approves. Record it in the handover. Commit.

### Task 9: Stats, Config and Help

**Produces:** a Design canvas `VS2000 Stats Config Help`. Phone and desktop artboards for:
- **Stats:** distance per bike, replacement-cost estimates per bike, and wear over time;
- **Config:** today's content, plus the component types list and the component type view;
- **Help:** a help page;
- the menu foot, with version and last Strava pull.

- [ ] **Step 1:** Build the canvas and write its URL into the handover.
- [ ] **Step 2:** Decide the Config button order settings with the user. Set that parity row to `dropped` or `covered`.
- [ ] **Step 3:** Check that no parity row is left `open`. Run `grep -c "| open |" docs/design/parity-checklist.md`. Expected: `0`.
- [ ] **Step 4:** The user approves. Record it in the handover. Commit, push, and open the Phase B pull request to `dev`.

---

## Phase C: export and close, branch `feature/stage2-closeout`

### Task 10: Profile and screens into the repo, docs, handover

**Files:**
- Create: `docs/design/README.md`, `docs/design/tokens.json`, `docs/design/screens/*.png`
- Create: `tests/design_profile/test_profile_tokens.py`
- Modify: `.handovers/stages/stage-2-design-handover.md`, `docs/superpowers/specs/2026-11-15-rewrite-roadmap-design.md` (Stage 2 status line), `CLAUDE.md`, `.claude/agents/ux-designer.md`, `.claude/agents/fullstack-developer.md`

**Interfaces:**
- Consumes: `check(tokens: dict) -> list[str]` (Task 3).

- [ ] **Step 1: Write the failing test**

```python
import json
from pathlib import Path

from design.check_tokens import check

TOKENS = Path(__file__).resolve().parents[2] / "docs" / "design" / "tokens.json"

def test_profile_tokens_pass_contrast():
    assert check(json.loads(TOKENS.read_text())) == []
```

- [ ] **Step 2:** Run `uv run pytest tests/design_profile/test_profile_tokens.py -q`. Expected: FAIL (file missing).
- [ ] **Step 3:** Read the design system's `project/README.md` and `project/tokens.json`. Write them as `docs/design/README.md` (adding links to the screens and the checklist) and `docs/design/tokens.json`.
- [ ] **Step 4:** Run `uv run pytest tests/design_profile -q`. Expected: PASS.
- [ ] **Step 5:** Export one PNG per approved artboard into `docs/design/screens/`, named `<page>-<view>-<phone|desktop>.png`. Use the canvas export when it offers per-artboard PNGs. Otherwise ask the user first, then capture each artboard at its size with Claude in Chrome. Check that every artboard in the handover's canvases has a file.
- [ ] **Step 6:** Update the docs:
  - the roadmap's Stage 2 status line, linking the handover;
  - CLAUDE.md: where the profile lives, that UI work follows `docs/design/`, and that the repo is the source of truth. The "Code Style, Frontend" lines (Bootstrap utility classes only, small incremental UI changes) get a note that they apply to the current app until Stage 5; Stage 3 decides what replaces them;
  - `ux-designer.md`: follow `docs/design/`, no Bootstrap-first, no copying old templates;
  - `fullstack-developer.md`: build pages from `docs/design/` and the screens.
- [ ] **Step 7:** Complete the handover: set its status to "Complete", list the canvases with their approval dates, the issues opened, the decisions, and next steps for Stage 3 (the URL shapes and libraries the design assumes).
- [ ] **Step 8:** Run `uv run pytest -q && uv run ruff check && uv run ruff format --check`. Expected: all pass.
- [ ] **Step 9: Commit**, push, and open the Phase C pull request to `dev` with "Refs #194, #363, #304".

```bash
git add docs/design tests/design_profile .handovers/stages/stage-2-design-handover.md docs/superpowers/specs/2026-11-15-rewrite-roadmap-design.md CLAUDE.md .claude/agents/ux-designer.md .claude/agents/fullstack-developer.md
git commit -m "Close out Stage 2: design profile, screens and docs in the repo"
```
