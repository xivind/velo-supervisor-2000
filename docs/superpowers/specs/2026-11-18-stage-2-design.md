# Stage 2: Design

**Date:** 2026-11-18
**Roadmap:** [2026-11-15-rewrite-roadmap-design.md](2026-11-15-rewrite-roadmap-design.md), Stage 2
**Issues:** #194 (redesign), #363 (bike overview, workplans, incidents), #362 (several services per component in a workplan), #365 (plan service modal), #171 (phone feedback), #304 (attributions)
**Branch:** feature branches off `dev`, merged back to `dev`
**Status:** Approved 2026-11-18

## Intent

Decide how the new app looks and works, on phone and desktop, before anyone decides how it is built (Stage 3) or builds it (Stage 5). The users trust what the app calculates and dislike how it is used: it looks old-fashioned, takes too many steps and is close to unusable on a phone. Stage 2 fixes the "how", from scratch, ignoring the shape of the current pages and code.

The inputs (@thomiz's `bike-dashboard.html` and the requirements in #363, #362, #365, #171) are inspiration, not a template.

Stage 2 produces no application code. Its output is a design profile, approved prototypes, a parity checklist and a set of feature issues.

## Goals

- **A design profile** that every later stage consults: colours, type, icons, shape, building blocks, notifications and writing conventions.
- **Approved prototypes** for phone and desktop of every main page, every item view and the workshop flows.
- **A parity checklist** of everything the old UI can do, each item either covered by the new design or dropped with a reason.
- **Feature issues** on the Sprintboard for every place the design needs a rule or operation the backend does not have, decided before Stage 5.
- **The results in the repo**, so Stages 3 to 5 work from files, not from a private link.

## Non-goals

- Code, templates or CSS for the app. Stage 5 builds the pages.
- Stage 3 decisions: URL shapes, the frontend libraries (htmx is the direction, Stage 3 confirms it), the resource model in detail, the date picker and multi-select libraries.
- Dark mode. The app is light only.
- A separate phone interface or a native app. One responsive app.
- Icons per component type. Text names component types better than glyphs.
- Changing any calculation. Distances, service intervals, lifetimes and statuses stay as `master` calculates them.

## Anti-goals

Stage 2 has failed, even with approved prototypes, if:

- on a phone, the Bike page needs scrolling before the first (most urgent) components show;
- a prototype quietly relies on a rule change that has no feature issue;
- an item view (component, service, workplan, incident, collection) looks or behaves differently depending on whether it was opened from Bike or Inventory;
- the profile exists only on claude.ai at the end of the stage;
- production data ends up in the repository (it is public);
- emoji are used as icons.

## Constraints

- **Rules that protect data stay** (pinned in `tests/rules/` and the characterisation tests):
  - one bike per component at a time;
  - no future dates for installation, service, workplan completion, incident and resolution dates (the last two held only in the browser today, #340); planned dates and workplan due dates may be in the future;
  - service intervals and lifetimes as today: distance and days, thresholds, offsets, statuses;
  - no services can be planned, completed or changed on a retired component;
  - nothing is deleted or changed in bulk without the user confirming.
- **Every view has its own address.** Opening an item or a list pushes a URL. Back returns to the previous list with its filters and sort kept (#128), and links and bookmarks work. The design names things as the FHIR-inspired resources they will become (Bike, Component, Service, Workplan, Incident, Collection, ComponentType, Ride), so Stage 3 can map views onto resources.
- *My call, scope and addresses:* each resource has one canonical address (its data). The page address also carries the scope it is shown in (a bike, or Inventory), so a bookmark, a reload or Back shows exactly what was on screen, and no navigation state is kept on the server. A canonical address opened directly in a browser shows the item in Inventory scope. This follows FHIR: `/Component/{id}` is the resource, and a bike's lists are like a FHIR compartment search (`/Bike/{id}/Component`). Stage 3 sets the URL shapes.
- **The server holds all state.** The design must not need logic in the browser beyond the menu, date picker, multi-select and small interactions.
- **Prototypes use made-up data**, shaped like the synthetic test dataset (`tests/fixtures/`), never component names or rides from production.
- **One reviewer.** Every canvas must be reviewable in one sitting.

## Approaches considered

| | A. Profile first | B. Screens first | C. Look on one real screen, then outward (chosen) |
|---|---|---|---|
| How | Full design system, then every canvas | Rough canvases, profile distilled afterwards | Thin profile, two or three directions on the Bike page, refine it, extract profile v1, then the other canvases |
| Pro | Consistent from the first screen | Decisions come from real screens | Look judged where it matters, profile grounded before anything depends on it |
| Con | Colours and shapes chosen in the abstract, reworked once real screens show problems | Canvases drift apart, all redrawn at the end | One extra round on the Bike page |

**Chosen: C.** The Bike page carries the roadmap's anti-goal and is used most, so the look is chosen there, on real content, with phone and desktop side by side.

## The design, as decided

### Pages and menu

```
┌──────────┬─────────────────────────────────────────┐
│ VS 2000  │  TOP: the scope, always there           │
│          │  (what you look at, its status, actions)│
│ Bike     ├─────────────────────────────────────────┤
│ Inventory│  LOWER: a list, or one item's view      │
│ Stats    │  swapped as you work                    │
│ Config   │                                         │
│ Help     │                                         │
│ ──────── │                                         │
│ v0.5.0   │                                         │
│ Strava ↻ │                                         │
└──────────┴─────────────────────────────────────────┘
```

- **A global menu on the left** with five main pages: **Bike, Inventory, Stats, Config, Help**. On a phone it is a drawer.
- **Bike**: one bike is the scope.
- **Inventory**: everything is the scope: all components (installed, spare and retired), all services, workplans, incidents and collections, with filter, search and sort.
- **Stats**: numbers and charts, for example distance per bike, replacement-cost estimates and wear over time. No component table; that lives in Inventory.
- **Config**: what it has today (fetch new or all rides, refresh bikes, export dataset, reset database, file paths, verbose logging, latest log entries), plus **component types**.
- **Help**: the help pages, rewritten for the new UI in Stage 5 (#99).
- **The footer moves into the foot of the menu**: version and last Strava pull stay. "Submit issue" and the database path go. Load time goes to the browser console, only when debug is on.
- Workplans, incidents and collections are no longer pages of their own. They are lists and item views inside Bike and Inventory.

### One pattern for every page with data

- **The top** shows the scope: what you look at, its status and the actions that make sense there. It changes with the scope, both in what it shows and in which actions it offers.
- **The lower part** shows a list, or one item's view when you open one.
- **Lists:** components, services (planned and completed), workplans, incidents, collections, and on Bike also rides.
- **Item views** (component, service, workplan, incident, collection) are designed once and look the same from Bike and from Inventory. Each brings its own header, including where it belongs (for example the component's bike). The top does not jump to another scope when you open an item.
- **On a phone** the top shrinks to a slim bar once you are inside an item, so the item gets the screen.

### Bike page

**Top:**
- active or retired, total distance, number of installed components;
- components due for service, due for replacement, compliance issues;
- planned services, open workplans, open incidents.

Every count is a link that opens the matching list, filtered (for example "3 due service" opens those three components). The top doubles as the filter bar.

Dropped from today's bike page: retired components (they stay in Inventory), expected cost of the next service.

**Lower part, default:** installed components, most urgent first, in compact rows. Some scrolling is acceptable on a bike with many components, but the urgent ones must show without it on a phone.

**Most urgent first** means:
1. By status: exceeded, then due, then OK, then not defined. The status is `master`'s, which is already the worse of service and lifetime, and of distance and days (`determine_worst_status`).
2. Within a status, by km remaining, the worse of service and lifetime. Components whose status comes from time sort by days remaining within their status.

Status comes first because thresholds differ per component (300 km left can be OK on one component and due on another) and because a component can be overdue by days with plenty of km left. Sorting by km alone would bury both.

```
PHONE                              DESKTOP
┌────────────────────────────┐    ┌───────────────────────────────────────────────┐
│ ◂ Canyon Inflite   ● Active│    │ Canyon Inflite   ● Active      55,112 km      │
│ 55,112 km · 24 installed   │    │ ⚠ 3 due service · 2 due replacement           │
│ ⚠ 3 service · 2 replace    │    │ ◈ 1 compliance issue · 24 installed           │
│ ◈ 1 compliance             │    │ 2 planned · 1 workplan · 1 incident           │
│ 2 planned · 1 wp · 1 inc   │    │                       [ actions … ]           │
├────────────────────────────┤    ├───────────────────────────────────────────────┤
│ Components|Services|WP|…   │    │ Components | Services | Workplans | …         │
│ ☐ Chain          ⚠ service │    │ list, most urgent first                       │
│ ☐ Cassette       ⚠ replace │    │                                               │
├────────────────────────────┤    │                                               │
│ [ Service ]  [ Install ]  ⋯│    │                                               │
└────────────────────────────┘    └───────────────────────────────────────────────┘
```
(Glyphs in sketches are placeholders; the prototypes use Lucide icons.)

*My call:* choosing **Bike** in the menu with no bike chosen yet opens the list of bikes (active first, retired after), and the top of a chosen bike has a bike switcher. The canvas shows both.

### Services, incidents and workplans

- **A service is the unit of work.** One service, one component, planned or completed.
- **An incident** is a reported problem on a bike, on one or more components, or both. It must name at least one of them. That rule exists today, but only in the browser (`main.js`); the server accepts an incident that names neither (see browser-only rules below). Services are linked to it to fix it.
- **A workplan** groups services, and through them their incidents. It is where bulk work happens: complete everything, close linked incidents, see progress.
- **What belongs to a bike** follows `master` (`process_incidents`, `process_workplans`): an incident belongs to a bike when it names the bike or a component currently installed on it; a workplan belongs to a bike when one of its services is on a component currently installed on it. The Bike top counts and lists use this rule.
- Item views show these links both ways: a service shows its workplan and incident; an incident shows the services and workplans working on it.
- **Cost stays on the component** (its replacement price), and the only cost figure is `master`'s rule: the sum of replacement prices of components due for replacement or past their lifetime. A workplan shows it as "expected replacement cost", applied to the workplan's components. Services show no cost; there is no cost field on services. Stats shows replacement-cost estimates per bike, not service cost, since the app holds no data on what a service cost.

### Actions

What users do at the bike: work with components directly or through workplans; plan services, complete planned services, log a completed service directly, edit a service; install and uninstall components, singly, through a collection status change or with quick swap.

- **Log service** on a component is one flow: it first lists that component's planned services (tap one to complete it), or logs a new completed service.
- **Plan service** puts a planned service on one or more components and can attach it to a new or existing workplan in the same step (see feature issues).
- **Edit** a service from its view.
- **On a component:** Replace (quick swap), Uninstall, or Install on a bike when it is a spare.
- **On a collection:** Change status, which installs or uninstalls the whole set. The Bike top offers the bike's collections as shortcuts.
- **Selection:** tick components in a list and a bar offers Plan service, Log service and Uninstall for the selection. Nothing is preselected unless the user ticked it (#365).
- **Phone bottom bar:** `Service` and `Install`, each opening a short sheet with the choices above, and `⋯` for the rest (new component, new workplan, new incident, new collection). It follows the scope: inside a component view, the same buttons act on that component.

### Notifications

One consistent system, specified in the profile:
- **toast** for success;
- **an inline message on the field** for rejected input;
- **a banner** for errors;
- **a confirm dialog** before anything is deleted or changes data in bulk.

### Visual direction

- **Light only.**
- **Calm and tool-like as the base, lively from one strong accent colour and confident numbers.** Distances and wear figures are large, in tabular figures.
- **Decoration that tells you something is welcome, decoration for its own sake is not.** Allowed: an accent band or subtle tonal gradient behind the top section; coloured wear bars and progress rings; line illustrations in the icon style for empty states; small motion with meaning (a check that draws itself when a service completes); charts on Stats. Not allowed: gradient washes behind content, glossy shadows, stock imagery. Judged on the first canvas and adjusted.
- **No emoji.** Icons are SVG.
- **Language:** the UI stays in English, as today.

### Icons

- **Lucide** (ISC licence) is the icon set.
- **Tabler** (MIT) is the fallback, one glyph at a time, only where Lucide lacks one, drawn at the same stroke width.
- Icons ship with the app, not from a CDN.
- Icon-only buttons always carry an accessible label.

## The design profile

The profile covers:

1. **Colour:** background, ink, one accent, and status colours for the statuses `master` calculates, no new levels: service status and lifetime status (OK, Due for service / Due for replacement, Service interval exceeded / Lifetime exceeded, Not defined) and installation status (Installed, Not installed, Retired). Statuses also differ in lightness and icon, not in hue alone. Text meets 4.5:1 contrast.
2. **Type:** one sans family (SIL OFL or similar, shipped with the app), a short type scale, tabular figures for numbers.
3. **Icons:** the set, sizes, stroke width, the label rule.
4. **Shape and spacing:** corner radius, spacing steps, button kinds (primary, secondary, quiet, danger), touch targets at least 44 px, compact list rows.
5. **Badges**, in the spirit of GitHub Projects: rounded pills, tinted background, coloured text, optional dot or icon. Used for status, type and links to workplans and incidents. A fixed set of badge colours, each with one meaning.
6. **Progress:** a **progress ring** for counts (a workplan's n/m) and a **wear bar** for a component's lifetime and service interval, coloured by status, with a threshold marker.
7. **Building blocks:** menu and drawer, top section, tabs, list row, selection bar, bottom bar, sheet and dialog, form fields including the date picker, empty states, toast, banner.
8. **Notifications:** the system above.
9. **Writing:** tone, button labels (verbs), how dates, distances and counts are shown.
10. **Third-party assets and licences:** Lucide, Tabler, the font, and any other library. #304 turns this list into the attribution file in Stage 5.

The profile is expressed as tokens and plain SVG/CSS descriptions, not as classes of a CSS framework, because Stage 3 chooses the frontend libraries.

## Working with Claude Design

Standalone claude.ai/design closes on 14 December 2026; Claude Design now lives in Claude as two artifact types, created and revised from Claude Code:

- **The design profile** is a **Design System** artifact while we iterate: tokens (colours, type, spacing, radius), a README as the style guide, and live previews of the building blocks.
- **Prototypes** are **Design** canvases: one canvas per group of screens, phone artboards (390×844) beside desktop artboards (1440 wide). Workshop flows are clickable artboards linked into a sequence. Every canvas uses the design system.
- **Review:** the user and @thomiz comment on the canvas; Claude revises. Sharing a canvas with @thomiz is the user's step, and his review is asynchronous: it never blocks a step, and his input is carried into the next canvases.
- **Approval** is the user's alone, per canvas, including the visual direction in step 2, recorded in the stage handover with the date.

## Order of work

1. **Thin profile v0:** palette, font, Lucide, radius. No building blocks.
2. **Bike page, two or three visual directions,** same layout and content, phone and desktop side by side. The user picks one, or a mix, and checks with @thomiz afterwards.
3. **Bike page refined** in that direction: the bike list, the top, the component list, the component item view, and the workshop flows as clickable artboards (log service, plan service with a workplan, quick swap, collection status change, selection bar).
4. **Profile v1** extracted from it, with every building block in the profile list.
5. **Inventory**, its lists and filters.
6. **Item views:** service, workplan, incident, collection.
7. **Stats, Config** (with component types) **and Help.**
8. **Export and close:** profile and screenshots into the repo, parity checklist complete, feature issues opened, handover.

The profile grows wherever a later canvas needs something new, and is final at step 8.

## Deliverables in the repo

*My call* on the layout:

- `docs/design/README.md`: the design profile (from the design system's README), with links to the rest.
- `docs/design/tokens.json`: the tokens, in the design system's token format.
- `docs/design/screens/`: one PNG per approved artboard, made-up data only, named `<page>-<view>-<phone|desktop>.png`.
- `docs/design/parity-checklist.md`: the parity checklist.
- `.handovers/stages/stage-2-design-handover.md`: status, approvals, decisions, links to the canvases and the design system, feature issues opened.
- Updated at the end: the roadmap's Stage 2 status line, CLAUDE.md (where the profile lives and that UI work follows it), `.claude/agents/ux-designer.md` and `fullstack-developer.md`.

From the end of Stage 2 the repo is the source of truth for the profile. A change starts in `docs/design/`; the claude.ai design system is a working copy, updated from the repo when new canvases are needed.

## Parity checklist

Built during the stage by walking every page, modal and POST route on `master` (11 pages, 20 modals). Each item names what the old UI does and where the new design covers it (canvas and artboard), or why it is dropped. It starts from:

- the UI behaviour list in the Stage 1 handover ("Stage 2 parity checklist");
- #37, #128 and #145 from the roadmap's issue map;
- the two route-only rules from the Stage 1 handover: workplan due date is required; empty optional form fields are accepted on uninstall.

Already decided as dropped: submit-issue link, database path in the footer, load time in the footer, retired components and expected cost on the bike page, emoji. Probably dropped, decided when walking Config: the button order settings for the old bike and component pages, since the new pages choose actions by context.

Each browser-only rule found is marked as such (see [Browser-only rules](#browser-only-rules)).

## Feature issues

Every place a prototype needs a rule or operation the backend lacks becomes an issue on the Sprintboard (#2) with a Priority, referenced from the canvas and the parity checklist, and decided before Stage 5. Known now:

| Change | Issue |
|---|---|
| Several planned services on one component in the same workplan. Today one is allowed per workplan (`business_logic.py`, pinned in `tests/rules/test_validation.py`); outside workplans there is no limit | #362 (exists) |
| Create a workplan together with its planned services in one step | #384 |
| Component types get a stable ID; today the name is the primary key | #385 |
| Rules held only in the browser move to the server (see below) | #386, references #340 |

Candidates to confirm while prototyping (an issue only if the backend lacks the operation): logging completed services on several selected components at once; uninstalling several selected components at once.

New issues go on project #2 (Sprintboard Velo Supervisor 2000) with Priority P0. #384, #385 and #386 were opened on 2026-11-18.

### Browser-only rules

Some rules exist today only in `main.js`, and the server accepts what the browser refuses. The new design keeps all validation on the server, so these are not rule changes but rules that move. While walking the old UI, every such rule is listed in the parity checklist, and one issue moves them all to the server. The future-date checks are already covered by #340; the issue references it rather than repeating them. Known now:

- an incident must name a bike, at least one component, or both (all 15 incidents in the production copy of 2026-11-16 already do);
- workplan due date is required (held by the route, from the Stage 1 handover).

## Done when

- The design profile is in `docs/design/` and approved.
- Every main page, item view and workshop flow has approved phone and desktop prototypes, with screenshots in `docs/design/screens/`.
- The parity checklist has no open item.
- Every needed rule or operation change has a feature issue on the Sprintboard.
- The stage handover is written and the roadmap, CLAUDE.md and agent files are updated.

## Left to the builder

- The exact palette, font, type scale and radii (chosen in steps 1 to 4 with the user).
- Which visual directions to show in step 2.
- How many canvases a group needs, and the artboard set inside each.
- The made-up dataset used in prototypes, as long as it is shaped like the synthetic test dataset.
- Wording on the canvases.
