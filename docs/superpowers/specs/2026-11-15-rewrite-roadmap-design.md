# Rewrite roadmap: new UI, restructured backend, exposed API

**Date:** 2026-11-15
**Issues:** the 20 open P0 issues on the Sprintboard, see [Issue map](#issue-map)
**Branch:** all work on `dev`, which is long-running. `master` is frozen as the reference.
**Status:** Approved 2026-11-15. Each stage gets its own design and plan before work starts.

This is a roadmap, not a build spec. It fixes the order of work, the decisions already made and what each stage must hand over to the next. Each stage is designed in detail when it starts.

## Why

The app has been in use for a couple of years and the users are happy with what it does. They complain about how it does it: the UI looks old-fashioned, takes too many steps and is close to unusable on a phone. From #363: what the user wants to change most (the components) sits so far down the page that it needs scrolling on most screens, and especially on mobile.

The backend logic is solid and is the reason the app is trusted. The frontend is 6,367 lines of JavaScript in one file, with the sort, filter, search and validation code copied per table and per form (#356). Test coverage is thin and CI only bumps the version number.

## Goals

- A completely new UI that works well on both phone and desktop. The workshop flows (changing component status, creating and editing services, quick swap, workplans) are comfortable on a phone.
- The backend reorganised to be maintainable and in line with common practice, including the repo layout (#364).
- All state, validation and orchestration on the server. The browser only renders.
- Everything the UI can do is also reachable as data through the same URLs, so others can build on it. A read-only MCP server is offered as an option.
- Every change carries provenance (#352): when, in what context and from which source.

## Non-goals

- User accounts or logins. This is a single-user app. Provenance records the source of a change, not a person.
- FHIR conformance. The API is FHIR-inspired only (see Stage 3).
- Writing through MCP. MCP is read-only.
- A separate public API product. We expose the API the app itself uses, nothing extra.
- Replacing FastAPI, SQLite or Peewee. Nothing asks for it and it would add risk without helping integrity.
- A native mobile app.

## Anti-goals

The rewrite has failed, even if it works, if any of these happen:

- A distance, service interval, lifetime or status is calculated differently from `master` without that being a deliberate, documented change.
- A refactor and a behaviour change are made in the same step, so a failing test can't tell which one caused it.
- Data is changed or deleted without the user confirming it (CLAUDE.md, Database).
- Logic ends up in an HTML route, in a template or in browser JavaScript instead of the service layer.
- The new UI still needs scrolling to reach the components on a bike page on a phone.

## Constraints

- Information integrity comes first. The existing calculations in `business_logic.py` define correct behaviour until a deliberate change says otherwise.
- Single maintainer working with Claude. Every stage must be reviewable by one person.
- The app is self-hosted in Docker on a home network, with a SQLite database file and a Strava token file mounted from outside the container.
- The project allows breaking schema changes between versions, with `db_migration.py` as the upgrade path and a backup first.
- `logging.error` drives container health (CLAUDE.md, Logging). New code must keep to that rule.

## Approaches considered

### Delivery: side by side on master, or frozen master and long-running dev

| | Side by side on master | Frozen master, build on dev (chosen) |
|---|---|---|
| How | New pages at their own URLs next to the old ones, released as each is done | Old UI frozen. New app built on `dev`, released once at the end |
| Backend | Must serve both UIs until the switch | Free to change shape |
| Releases | Small and frequent | None until the switch |
| Risk | Spread out, more total work | Concentrated in the switch-over |

**Chosen: frozen master.** The users have agreed to wait. It frees the backend from serving the old UI, and an untouched `master` is a reference to compare against for integrity (see [Verifying integrity](#verifying-integrity)).

### Frontend: server-rendered with htmx, or a JSON API with a separate frontend app

**Direction: server-rendered with htmx.** The user wants all state and orchestration on the server. htmx swaps server-rendered HTML fragments into the page, so validation exists once, on the server, and most of `main.js` goes away. A separate frontend app (React, Vue, Svelte) would move state into the browser, add a build step and bring back the duplicated validation. Confirmed or revised in Stage 3.

### API: separate API, or one set of resources with two formats

**Direction: one set of resources answering in two formats.** Each URL returns HTML to a browser and JSON to a script or the MCP server, chosen by the `Accept` header (content negotiation). Both formats come from the same service call, so there is no second API to keep in sync. A separate JSON API would mean the UI and the API could drift apart.

### API style: FHIR-conformant or FHIR-inspired

**Direction: FHIR-inspired.** Take the patterns (resources, standard interactions, named operations, a structured error format, search result lists, a capability statement, a Provenance resource) and leave the rest (profiles, extensions, terminology). Full conformance is built for healthcare and would bury a single-user app.

### Provenance actor: named user or source of change

**Chosen: source of change.** Values such as `ui`, `api`, `mcp`, `strava-sync`, `scheduler`, `migration`. Named users would need accounts, which is a non-goal.

## Stages

Every stage ends with CLAUDE.md and the agent files in `.claude/agents/` updated to match the new state, so agents never work from rules that no longer apply. Each stage starts with its own design (brainstorm, written spec) and plan. Every stage ends with a handover in `.handovers/stages/` (status, decisions, comparison results, open items), and its status line below links to it.

### Stage 1: Foundation

**Status:** Delivered 2026-11-17; the release backfill for existing tags is pending. Handover: [stage-1-foundation-handover.md](../../../.handovers/stages/stage-1-foundation-handover.md)

**Purpose:** a safety net that proves later stages didn't change the logic.

- Bring `dev` and `staging` up to date with `master` first. On 2026-11-15 they are 21 and 19 commits behind, and 0 ahead.
- Stage 1 lives on `dev`, like everything else. It contains no logic changes, only moved files, configuration and tests. That makes `dev` at the end of Stage 1 the baseline, and the comparison against `master` proves it behaves the same (see [Verifying integrity](#verifying-integrity)).
- Reorganise the repo layout (#364), before CI is written, so paths are set once.
- Build the Docker image from `uv.lock` and pin dependencies (#356 item 6).
- CI on GitHub Actions: run the test suite on every push and pull request to `dev` and `master`. Fix the version script that crashes now and then (#121). *My call:* the version workflow keeps its current trigger (pushes to `master`), so during the freeze it only runs on hotfixes. Its crash and its Python 3.8 runtime are fixed in this stage.
- Result-based ("characterisation") tests of the calculations: a database and rides go in, distances, service intervals, lifetime and status come out. Cover the cases #356 item 1 lists: a component moved between bikes, time-based intervals, distance offsets, a component with no installation history.
- *My call, what the tests look at:* one small **result extractor** that takes a database and returns the calculated results per bike and component as plain data (JSON). The expected results are stored as files. Later stages may rewrite the extractor to read from the new structure, but they may never change the expected results, except through a documented feature change. That way the tests survive schema changes (Stage 3), new function boundaries (Stage 4) and the new UI (Stage 5).
- *My call, how rides get in:* calculation tests write rides straight into the database. The Strava sync gets its own tests against recorded Strava responses, so Stage 4 is covered when it refactors the sync.
- The same extractor is the comparison tool against `master`. It is built in this stage, with a version for `master`'s code and a version for `dev`'s.
- A test dataset (#11) for CI. It must not contain production data, because the repository is public. *My call:* a synthetic dataset built for the cases above, committed to the repo. Comparisons against a copy of the production database run locally only.
- The existing pytest suites (`test_service_status.py`, `test_workplans_incidents.py`, `test_migration.py`, `test_health.py`) are kept and run in CI. They count towards coverage.
- Update `tests/README.md` and the Testing section of CLAUDE.md (#356).

**Done when:** CI runs the tests on every push to `dev`, the calculation paths are covered by result-based tests, and a comparison on a copy of the production database shows `dev` and `master` give identical results.

### Stage 2: Design

**Purpose:** settle how the app should look and work, ignoring how the current code and pages are shaped.

- Prototype the key screens and flows for phone and desktop with Claude Design.
- Inputs: @thomiz's `bike-dashboard.html` and the requirements in #363, the workplan flow in #362 and #365, the phone feedback in #171, and the two menus (main menu and bike actions) described in #363. These are only inputs for inspiration and not necessarily how it should look. We decide that on our own. 
- Ignore the current code. Keep the domain rules that protect data: one bike per component at a time, no future dates, how service intervals and lifetimes work.
- Every place the design needs a rule changed (for example #362, several services on one component in one workplan, or creating a workplan with its services in one step) becomes an explicit feature issue, decided before Stage 5.
- The design stage should also result in a design profile, that the rest of the work will consult and adhere to. The design profile should deal with for example color palettes, fonts, the use of icons, how buttons should be shaped, and other visual conventions. 

**Done when:** approved prototypes for phone and desktop, a list of required behaviour changes as feature issues, and a parity checklist of everything the old UI can do and the new UI must cover. The design profile should also be done as part of this stage.

### Stage 3: Architecture

**Purpose:** decide how the design gets built.

- Layers: a service layer holding all logic, validation and provenance, with thin adapters on top. HTML routes for htmx pages, the same routes answering JSON, and a read-only MCP server over the same services. An HTML route that contains logic is a bug.
- Confirm htmx, and choose the small amount of browser JavaScript still needed (date picker, multi-select, menu), possibly Alpine.js.
- FHIR-inspired resource model: resource names and URLs (`/Component/{id}`, `/Component?bike=...`), standard interactions (read, search, create, update, delete), named operations for multi-step work (`POST /Component/{id}/$swap`, completing a workplan, recalculating distances), errors as a structured outcome, search results as a list wrapper, a capability statement.
- Provenance model based on W3C PROV-O (#352), with the source-of-change agents above. Schema changes and the migration path for them.
- Payloads as named fields, never positional tuples. Jinja strict undefined mode, so a missing field fails loudly (#356 item 2).
- Open here: whether the JSON side and MCP need a token on a home network, and how MCP is run (inside the app or as its own process).
- The test strategy for the new layers: route tests for every resource in both formats (HTML and JSON), MCP tests, and how the new UI is tested in a browser.

**Done when:** a written architecture document approved by the user.

### Stage 4: Backend refactor

**Purpose:** reshape the backend to the Stage 3 architecture without changing behaviour.

- One area at a time: services, components, collections, Strava sync. The natural seams are listed in #356 item 3.
- Split the long functions (#356 item 4). The distance functions are only touched once Stage 1 tests cover them.
- Detail routes return 404 for unknown IDs instead of 500 (#356 comment of 2026-09-27).
- Every resource route gets tests in both formats as it is built, following the Stage 3 test strategy. A refactored function keeps the Stage 1 tests that cover it green, and gets unit tests of its own where the split makes that possible.
- Every step is behaviour-preserving. A real bug found in current logic is written down as an issue and fixed later as a separate change, never inside the refactor.
- The frozen old UI is not kept working on `dev`. `master` is the reference instead.

**Done when:** the architecture is in place and every Stage 1 test and integrity comparison matches `master`.

### Stage 5: New frontend and features

**Purpose:** build the new UI page by page, and make the deliberate behaviour changes.

- Two tracks, never mixed in one step:
  - **Pages:** built from the approved prototypes and checked off against the parity checklist. Each page gets browser tests for its workshop flows, following the Stage 3 test strategy, before it is checked off.
  - **Features:** each with its own issue, tests and release note. Provenance (#352) together with recently changed components (#180), several services per component in a workplan (#362), the #365 behaviours, the no-future-dates rule as one server-side check (#340), blocked dates in the date picker (#218), a loading indicator (#234), the help page (#99), and the data normalisation items in #356 (blank strings to NULL).
- A preview container runs `staging` against a copy of the production data, so the user and @thomiz can try it early. `dev` is merged into `staging` whenever there is something worth trying.

**Done when:** every item on the parity checklist works in the new UI, on a real phone and on desktop.

### Stage 6: Switch-over

**Purpose:** replace the old app with the new one.

- Migration from the `master` schema to the `dev` schema, tested on a copy of the production database, with a backup first.
- Integrity comparison against `master` on that copy, with differences explained by documented feature changes only.
- Release, then remove the old templates and `main.js`, merge `dev` into `master`.
- Switch on the required checks (`test`, `lint`, `docker`) in the branch protection for `master`.
- On the Pi: move `config.json` to `/data/config.json`, and check that `/data`, `/data/logs` and `/secrets` are writable by UID 1000. `strava_tokens.json` in `/secrets` is shared with the sync-strava and update-strava containers; if they rewrite it as root, the app can no longer refresh the token.
- Final sweep of CLAUDE.md, the agent files, README and the help page.

## Verifying integrity

Two checks, both needed:

- **Result-based tests** (Stage 1) run in CI on the synthetic dataset. They catch regressions on every push.
- **Comparison against `master`.** Load the same copy of the production database into `master` and into `dev`, run both and compare the calculated results per bike and component: distances, service intervals, lifetime, status, service due. The result extractor from Stage 1 produces those results from both sides. The schemas will diverge (provenance), so the comparison uses calculated results, not raw tables. Run locally only, since it uses production data. Run at the end of Stages 1, 4 and 6, and whenever a step touches the calculations. Any difference must trace back to a documented feature change.

## Branch policy during the freeze

- `master` is not changed, with one exception: a data-integrity bug in production is fixed on `master` and the fix is ported to `dev`. Other bugs wait for the new app.
- `dev` always runs and always passes its tests.
- `staging` is the preview branch. It only receives merges from `dev`, never direct commits, and feeds the preview container (Stage 5). It is brought up to date with `master` in Stage 1 along with `dev`, and CI runs on it too.
- Feature branches come off `dev` and merge back to `dev` (CLAUDE.md, Branch Strategy).

## Issue map

| Issue | Where it goes |
|---|---|
| #11 Configure unit tests | Stage 1 |
| #121 Dev branch and CI pipeline | Stage 1 |
| #364 Repo structure | Stage 1 |
| #356 Technical debt | Split: tests and dependencies in Stage 1, payloads and Jinja strict mode in Stage 3, large and long functions and 404s in Stage 4, blank strings to NULL in Stage 5. The `main.js` items go away with the old UI |
| #100 Docstrings | Written as code is rewritten in Stages 4 and 5, not as a pass over the old code |
| #194 Total redesign of GUI | Stages 2 and 5. Replaces the CSS-only direction in the comment of 2026-11-14 |
| #363 Bike overview, workplans and incidents | Stage 2 input, built in Stage 5 |
| #362 Several services per component in a workplan | Stage 2 decides the rule, Stage 5 feature |
| #365 Plan service modal | Stage 2 input, Stage 5 feature. The incident-closing description bug is checked against current logic in Stage 1 |
| #352 Provenance | Stage 3 model, Stage 5 feature |
| #180 Recently changed components | Stage 5, built on #352 |
| #340 No-future-dates check | Stage 5, one server-side rule |
| #218 Date picker blocks invalid dates | Stage 5 |
| #234 Loading indicator | Stage 5 |
| #99 Help page | Stage 5, rewritten for the new UI |
| #37 Scroll to form on edit | Goes away with the old UI. Parity checklist item |
| #128 Filters reset on delete | Goes away with the old UI. Parity checklist item |
| #145 Delete then retire acts as delete | Goes away with the old UI. Parity checklist item |
| #190 Clean up main.js | Goes away with the old UI |
| #198 HTML formatting | Goes away with the old UI |

## Left to each stage

- Stage 1: the test layout, how the synthetic dataset is built, and the target repo layout.
- Stage 2: which screens get prototyped first.
- Stage 3: everything listed as open there.
- Stage 5: the order of pages and features.
