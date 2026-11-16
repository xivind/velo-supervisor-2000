# Stage 1: Foundation

**Date:** 2026-11-16, revised 2026-11-16 after the user's review
**Roadmap:** [2026-11-15-rewrite-roadmap-design.md](2026-11-15-rewrite-roadmap-design.md), Stage 1
**Issues:** #364 (repo structure), #121 (CI), #11 (unit tests), #356 items 1 and 6
**Branch:** feature branches off `dev`, merged back to `dev`
**Status:** Approved 2026-11-16

## Intent

Build the safety net that later stages lean on, so that Stages 3 to 6 can show they did not change any calculation. At the same time, move the repository and the Docker image to standard Python practice, so that every path written in CI and the tests is final.

Everything built here is permanent: CI, the release flow, the tests and the comparison tool are how the project works from now on, not scaffolding for the rewrite.

Stage 1 changes no calculation logic. It moves files, edits the lines the move forces (imports, file paths, how templates, static files, config and the version are found), adds configuration and tests, and removes legacy files.

## Goals

- A standard **src layout**, with the code as the package `velo_supervisor`.
- A **Docker image built to current practice**: multi-stage, non-root, only the installed package in the final image, config and data on mounted volumes.
- A **result extractor**: one tool that takes a database and a version of the code, runs a full recalculation with the clock fixed, and returns everything the app stores and derives, as JSON.
- A **comparison** against `master` on a copy of the production database, run locally. It proves the move changed nothing, and is reused in Stages 4 and 6 and whenever a change touches the calculations.
- **Characterisation tests**: a synthetic dataset goes in, recalculations and operations run, and the results must equal stored expected-result files.
- **Page render tests**

- Every GET page in `main.py` (overview, bike, component, collection, workplan and incident pages, component types, config, help) is requested through FastAPI's `TestClient` for every resource in the synthetic dataset, and must answer 200. This catches the move breaking a template, a static path or a payload, which the extractor cannot see.
- Unknown IDs are requested too, and today's answer (500) is recorded as it is. Stage 4 changes it to 404 as a documented change (#356).
- These check that pages render, not what they show; the values are checked by the extractor. The page list changes with the new UI in Stage 5, the rule stays: every page renders for every resource in the dataset.

**Strava sync tests** against synthetic Strava responses.
- **Permanent CI** on GitHub Actions: tests, lint for new code, and an image build with a health check, on every push and pull request.
- **A new release flow** (#121): releases made in GitHub's Releases page, the version derived from the git tag. No bot commits on `master`.
- **Release notes moved to GitHub Releases**, including the existing ones, and the README tidied up.
- **Legacy removed**: the old test protocol, the service integration spec and plan, and the old handovers, once their content is covered.
- **A stage handover** that carries status, decisions and knowledge to the following stages.
- **Docs updated:** `tests/README.md`, README, CLAUDE.md and `.claude/agents/` match the new layout, testing and release setup.

## Non-goals

- Splitting or reshaping the modules (`business_logic.py` and the rest). That is Stage 4, after Stage 3 decides the architecture.
- Fixing calculation bugs found while writing tests. They become issues and are fixed later as separate changes.
- Coverage targets or a coverage gate. Coverage is reported, not enforced.
- Linting the existing modules. Lint covers new code (`tests/`, `scripts/`) now and grows to each module as Stage 4 rewrites it, so Stage 1 does not reformat the whole codebase.

## Anti-goals

Stage 1 has failed, even if CI is green, if:

- the comparison against `master` shows any difference;
- an expected-result file was edited to make a test pass;
- the repository gains any production data (it is public);
- a test can pass or fail depending on the date it runs;
- a legacy file is deleted before what it protects is covered elsewhere.

## Constraints

- `master` is frozen and is the reference. Its code is never changed by this stage. Tags and GitHub Releases on existing tags do not change its code.
- The day-based values (`lifetime_remaining_days`, `service_next_days` and the statuses they drive) are counted up to "now". The code reads the current time in about 15 places, through `utils.get_formatted_datetime_now()` and direct `datetime.now()` calls in `business_logic.py` and `utils.py`.
- Calculated results live as columns on `components`, `bikes`, `component_history`, `services` and `component_types`. A recalculation writes them, so it needs a database it is allowed to change. Other values (collection status, workplan and incident context, compliance report, percentages, triggers) are derived when a page is built and never stored.
- IDs come from `utils.generate_unique_id()`: six random UUID characters plus the last four digits of `time.time()`. They are not repeatable between runs.
- Today the app reads `config.json` and `current_version.txt` from its working directory. In Docker that is `/app/backend`, and `backend/config.json` (gitignored) is copied into the image at build time. The config page writes `config.json` inside the container, and `create-container-vs2000.sh` removes the container and image on every deploy, so settings changed on the config page appear to be lost on every redeploy (see [Docker](#docker)).
- The comparison uses a migrated copy of the production database at `/home/xivind/code/velo-supervisor-2000-2026-11-16.sqlite` (exported 2026-11-16: 17 bikes, 638 components, 7449 rides, 228 services, 12 workplans, 15 incidents, 14 collections), supplied by the user. It stays there, outside the repository, and is used unchanged for every comparison in the rewrite. It is never changed directly; each run copies it. A fresh export may be needed in Stage 6 to test the migration on current data. No Strava token file exists on the dev machine.
- Neither Docker nor Podman is installed on the dev machine, and production (the Pi) keeps running `master` until switch-over.
- `template_db.sqlite` has the same schema as the production copy (checked 2026-11-16, every table and index identical). It is not read by the app; it is the starting database for new installs (README) and for the tests.

## Approaches

### Order of work

- **A. Roadmap order:** move, then CI, then tests and comparison. Paths are written once. But the riskiest step, touching every import, is checked only by the existing suites, which do not cover distances or lifetime.
- **B. Extractor first (chosen):** build the extractor and comparison against today's flat layout, and run a baseline against `master`. Then move, and compare again. Then CI, dataset and tests, written once on the new paths. The extractor has to read `master`'s flat layout anyway, so building it first costs nothing extra.
- **C. All tests first, then move:** test paths are written twice. Dropped.

### Fixed clock

- **time-machine (chosen):** a test-only library that changes the time inside the test or extractor process only. No app code changes, nothing on the machine changes. It is a dev dependency, so it stays out of the Docker image.
- Leaving day-based values out of the expected results was rejected: time-based intervals are one of the cases #356 asks to cover.

### Synthetic dataset

- **Built by a Python script at test time (chosen):** readable, reviewable in a diff, no binary file in the repo.
- A committed `.sqlite` file was rejected: its changes cannot be reviewed.

### Version source

- **From the git tag through the package version (chosen):** `hatch-vcs` sets the package version from `git describe` when the package is built, and the app reads it with `importlib.metadata`. One source of truth, nothing committed, and it works the same locally and in Docker.
- Writing `current_version.txt` at image build time was the first proposal. It works, but keeps a generated file and a second mechanism next to the package version, and shows "Version unknown" when running locally.
- A bot committing the version file (today) was rejected: it is what breaks, and what makes `dev` and `staging` drift behind `master`.

### Release mechanism

- **GitHub's Releases page (chosen):** "Draft a new release", type the new tag, pick `master`, "Generate release notes", edit, publish. GitHub creates the tag on publish. Nothing to maintain or test.
- A custom Release workflow with a version input was the first proposal. It only adds a SemVer check that the user does by eye anyway, and a workflow that can only really be tested by releasing. Dropped, together with its `dry_run` option.

## Decided

### Target layout

```
src/velo_supervisor/        ← was backend/*.py
    __init__.py, main.py, business_logic.py, database_manager.py,
    database_model.py, db_migration.py, strava.py, middleware.py,
    scheduler.py, utils.py, healthcheck.py
    templates/              ← was frontend/templates/
    static/                 ← was frontend/static/
config/                     ← what an installation starts from
    config.json.example, strava_tokens.example.json,
    uvicorn_log_config.ini, template_db.sqlite
tests/                      ← see Tests
scripts/                    ← create-container-vs2000.sh, comparison tooling
docs/                       ← diagrams/ moves in
.github/                    ← workflows, dependabot.yml, release.yml
Dockerfile                  ← renamed from DOCKERFILE
.dockerignore
pyproject.toml, uv.lock, README.md, CLAUDE.md
```

- Imports become package imports: `from velo_supervisor import utils`, `from velo_supervisor.database_model import ...`.
- The app starts with `uvicorn velo_supervisor.main:app`. The migration runs as `python -m velo_supervisor.db_migration`, the health check as `python -m velo_supervisor.healthcheck`.
- Templates and static files are found relative to the package (`Path(__file__).parent / "templates"`), not relative to the working directory.
- `pyproject.toml` declares the package with `hatchling` and `hatch-vcs`, so `uv sync` installs it into `.venv` and tests import it without `sys.path` tricks. `[tool.uv] cache-keys` includes git commit and tags, so a new tag gives a new version on the next `uv sync`.
- `version.py`, `current_version.txt` and `run_version_script.yml` are deleted.
- `.gitignore`, the Dockerfile, `create-container-vs2000.sh` and README instructions follow the new paths.
- *My call:* after the move, `graphify update .` rebuilds the graph on the new paths (AST only, no token cost). The community labels are checked, and relabelled only if the rebuild lost them.

### Configuration file location

- `utils.read_config()` and the config writer read the path from the environment variable `VELO_SUPERVISOR_CONFIG`, defaulting to `config.json` in the working directory. `db_migration.py` uses the same lookup. This is the only change to how the app behaves in this stage, and it is made as its own commit, with its own issue for the lost-settings bug.
- Locally, `config.json` (gitignored) sits at the root of the checkout and the app is started from there.
- In Docker, `VELO_SUPERVISOR_CONFIG=/data/config.json`. The file lives on the mounted `/data` volume, next to the database and logs, instead of being copied into the image. Settings written by the config page then survive a redeploy.
- Moving `config.json` into `/data` on the Pi is a switch-over step (Stage 6), written into the release notes.

### Docker

The image follows current practice for a Python app built with uv:

- **Multi-stage build.** The build stage has uv (pinned, `ghcr.io/astral-sh/uv:<fixed version>`, not `:latest`) and git, copies the source and `.git`, and runs `uv sync --locked --no-dev --no-editable`. That installs `velo_supervisor`, with its templates and static files, into `/app/.venv`, and `hatch-vcs` reads the version from `.git`. The runtime stage is `python:3.12-slim` and copies only `/app/.venv` and `config/uvicorn_log_config.ini`. No source tree, no `.git`, no uv in the final image.
- **Non-root user.** The app runs as an unprivileged user. Its UID matches the owner of the bind-mounted `/data` and `/secrets` on the Pi (normally 1000), which is checked at switch-over.
- **Paths:** `WORKDIR /app`. Data, database and logs on `/data`; Strava tokens on `/secrets`; config at `/data/config.json`. `PYTHONPATH` is no longer set.
- **Unchanged:** port 8000, the log config, the `HEALTHCHECK` interval and its rule (now `python -m velo_supervisor.healthcheck`), `TZ` from the run command.
- `.dockerignore` keeps `.venv`, caches, `graphify-out` and local databases out of the build context.
- *My call:* CI verifies the image, since there is no Docker on the dev machine (see [CI](#ci)).

### Version and releases

Confirmed from the Actions logs on 2026-11-16: every run since 2026-11-14 fails at setup because Python 3.8 is gone from the runners; runs on `pull_request` events fail at `git push origin master` on the temporary merge commit; and the bot's "Update version number" commits on `master` are why `dev` and `staging` fall behind after every merge.

Today's manual process: write release notes in the README, create and push the tag, merge `staging` into `master`.

New flow:

1. Merge as now: `dev` → `staging` → `master`, through pull requests with CI green.
2. Release from GitHub's Releases page: draft a new release, type the new tag (`vX.Y.Z`), target `master`, generate the notes, edit them, publish. GitHub creates the tag.
3. `.github/release.yml` sorts the generated notes by pull request label, with a "Breaking changes (migration required)" section first, so a migration is flagged the way the README does today.
4. The footer shows the package version: `0.5.0` on a tagged build, and for example `0.5.1.dev3+g8fec699` for a build three commits after a tag. That is the same information as today's `v0.5.0.8cf8715`. `utils.get_current_version()` reads it with `importlib.metadata` and keeps its "Version unknown" fallback.
5. On the Pi, `create-container-vs2000.sh` builds from the checkout as now; `git pull` fetches the tag with the release.

- The new flow lives on `dev` and reaches `master` at switch-over. The user confirmed that is fine: users keep running their current containers during the freeze.

### Release notes backfill and README cleanup

- The 14 existing tags (`v0.1.0` to `v0.5.0`) have no GitHub Releases. Each gets one, with the notes copied word for word from the README changelog. `v0.5.0` is marked latest.
- `v0.4.6` has notes in the README but no tag. *My call:* find the `master` commit that shipped it (the merge that added quick swap), tag it `v0.4.6` and give it a release too, so the history has no gaps. If that commit can't be identified with confidence, its notes are added to the `v0.4.7` release under a "v0.4.6" heading instead.
- Creating releases publishes to GitHub, so the builder shows the user the full list of releases and notes before creating any of them.
- The README changelog is replaced by a link to the Releases page. The rest of the README is tidied up: the outdated Q1 2025 pilot notice, the versioning section (rewritten for the new flow), setup instructions for the new layout, `config/` and the config location.

### Result extractor

- Input: a path to a code checkout (flat `master` layout or package `dev` layout), a database file, a fixed date and time, and optionally a scenario of operations to run first.
- It copies the database to a temporary folder, writes a `config.json` pointing at the copy, and runs in a separate Python process with the clock fixed by time-machine.
- The recalculation is the same on both sides: `update_components_distance_iterator` over every bike, then `process_history_records` for every component, then `update_time_based_fields`, then `update_component_type_count` for every component type.
- The output has two layers, as JSON sorted by table and ID, so two outputs can be compared with a plain diff:
  - **Stored state:** every column of every row of every table (`bikes`, `components`, `component_types`, `component_history`, `services`, `collections`, `workplans`, `incidents`, `rides`). Taking all columns, rather than a chosen list, means nothing the app stores can change unnoticed.
  - **Derived values:** what the read functions compute when a page is built, as named fields per resource. Per component: percentages reached and triggers (`calculate_component_triggers`, `calculate_percentage_reached`), and its collection. Per bike: the compliance report (`process_bike_compliance_report`) and the values `get_bike_details` and `get_bike_overview` compute. Per collection: its status (`calculate_collection_status`). Per workplan and incident: the context from `process_workplans`, `process_incidents` and `derive_workplan_context` (linked services and components, status, elapsed days, resolved title). The builder lists every derived value the read functions produce and includes each one, or writes down why it is display formatting only.
- Floats are compared after rounding to a fixed number of decimals, so floating-point noise does not count as a difference.
- IDs created during a scenario are replaced by stable labels in order of creation, so outputs are repeatable.
- The extractor has two loaders, one for the flat layout and one for the package layout. Later stages may rewrite the loaders and the mapping of derived values to read a new structure. They may never change an expected result except through a documented feature change.

### Comparison against master

- A script in `scripts/` exports a given commit with `git archive`, runs the extractor against it and against the working tree on the same database copy and the same fixed date, and prints a diff.
- Run locally only, against `velo-supervisor-2000-2026-11-16.sqlite`. Nothing it produces is committed.
- On the production copy it runs the recalculation and the derived values, not operations. Real data matters most for the recalculation, where years of history, moved components and odd records live. Operations behave the same on any data and are covered by scenarios in the characterisation tests, which run in CI on every push.
- Run in Stage 1 at three points: a baseline before the move (`dev` against `master`, expected to be identical because the code is identical), after the move, and at the end of the stage.

### Tests

Structure (folder names are the builder's call within this split):

```
tests/
    conftest.py               ← shared fixtures: database copy, fixed clock, app modules
    fixtures/
        dataset.py            ← synthetic dataset builder
        strava/               ← synthetic Strava responses
        expected/             ← expected-result files
    characterisation/         ← recalculation and operation scenarios against expected results
    rules/                    ← business rules: validation, refusals, workplan and incident rules
    pages/                    ← every page renders for every resource
    strava/                   ← Strava sync
    test_health.py, test_migration.py   ← rewritten, not moved
```

**Characterisation tests**

- The dataset builder starts from `config/template_db.sqlite` with all migrations applied and writes bikes, rides, components, history records, services, collections, workplans and incidents straight into the tables. All dates are fixed and lie before the fixed test date.
- Recalculation cases, at least: a component moved between several bikes; time-based lifetime and service intervals; distance offsets; a component with no installation history; a retired component; completed services resetting the service interval; service records across several installation records of the same component; a bike whose status depends on its worst component; a collection with mixed component statuses; workplans and incidents with planned and completed services.
- Operation scenarios, each followed by a full extraction. **Every public method in `business_logic.py` that writes data gets at least one scenario**, not only a chosen few. As of 2026-11-16 these are: `create_component`, `modify_component_details`, `create_history_record` (install, uninstall, retire), `update_history_record`, `quick_swap_orchestrator`, `create_collection`, `update_collection`, `change_collection_status`, `create_service_record`, `create_planned_service`, `create_planned_services`, `complete_services`, `update_service_record` (including revert to planned), `create_incident_record`, `update_incident_record`, `create_workplan` (including from an incident), `update_workplan` (including completion), `modify_component_type`, `delete_record` (once per kind of record it deletes), `refresh_all_bikes` and `update_rides_bulk` ("recent" and "all", on the synthetic Strava responses), and `utils.write_config` for each form type.
- **Every `validate_*` method gets a rule test for each refusal it can give** (`validate_history_record`, `validate_quick_swap`, `validate_collection`, `validate_service_record`, `validate_threshold_configuration`, `validate_workplan_completion`), plus one accepted case.
- The builder checks this list against the code when starting, and the pull request carries the mapping from each write and validate method to its tests. A method left out needs a written reason.
- The expected results are recorded from the current code once, then checked by hand against the rules before they are committed. If the current code is wrong somewhere, the file records what the code does, and an issue is opened. The test is not "fixed".
- *My call:* the builder does that check against the code and the existing specs, and writes in the pull request which values were checked and how. The user reviews the files in the pull request like any other change. A suspected bug becomes a new GitHub issue, referenced from the test with a comment; commits use "Refs #N", never "Closes".

**Strava sync tests**

- `strava.py` calls Strava through an `OAuth2Session`. The tests replace the HTTP layer with synthetic responses shaped like Strava's activities, athlete and gear responses, only with the fields the code reads.
- The responses are written by hand from Strava's API documentation, not recorded from the real account, because the repository is public.
- Cover: a paged activities response, rides with and without gear, a token that needs refreshing, and the "recent" and "all" modes of `update_rides_bulk`.

**Existing tests, vetted 2026-11-16** (32 tests, all passing)

The user decided on 2026-11-16 that every test in the folder is new: all four existing test files are rewritten from scratch on the new fixtures and dataset builder, and the old files are deleted. Nothing is carried over unread. What the old tests protect is kept:

- `test_health.py` (7 tests): the health rule. Errors logged in the last 24 hours, a failing database or a missing database file make the app unhealthy; warnings do not; the error recorder survives the log level being reset at startup. Rewritten as `test_health.py` on the shared fixtures.
- `test_service_status.py` and `test_workplans_incidents.py` (25 tests): planned services never touch health; retirement blocked by planned services; completion and revert rules; workplan links on the newest service; validation rules; notes stored and blank as NULL. Rewritten into `rules/` and `characterisation/`. Checks that read positional tuples (`get_incident_data_tuple`, `get_workplan_data_tuple`, page payloads) become checks on the extractor's named derived values, since Stage 3 removes the tuples.
- `test_migration.py` (3 tests): converting the pre-#351 model, running twice changes nothing, and running on a fresh template works. Rewritten as `test_migration.py`; it lives until Stage 6 replaces the migration path.
- Before an old file is deleted, each of its tests is mapped to the new test that covers the same rule. The mapping goes in the pull request. No rule is dropped without the user agreeing.
- `test_protocol_services.md` (manual protocol for #351): deleted once each of its cases is either covered by an automated test or, for UI-only cases, listed in the stage handover for the Stage 2 parity checklist.
- `tests/README.md`: rewritten: how the tests are organised, how to run them, the fixed clock, the dataset builder, how expected results may and may not change, and how to run the comparison against `master`.

### Template database

- Schema checked against the production copy on 2026-11-16: identical.
- Found: all 46 component types in the template have `in_use` counts (1 to 34, 464 in total) although the template has no components. They are left over from real data. A new install starts with wrong counts, and deleting a component type is refused while `in_use > 0` (`business_logic.py` line 3307). This gets its own issue and is fixed in Stage 1 as its own commit, after the move: `in_use` set to 0. It is seed data, not calculation logic.
- The production copy has 4 component types the template lacks (Frame lock, Groupset battery, Rimtape, Sealant) and 6 with different settings (cables, tubes, jockey wheels). The user decided on 2026-11-16 that they become the defaults: the template gets the 4 types and the 6 settings exactly as in the production copy, with `in_use` 0. Same commit as the `in_use` fix, same issue.

### CI

Permanent setup, in `.github/`:

- **`tests.yml`**, on every push to any branch and every pull request. Jobs:
  - **test:** checkout, install uv (pinned), `uv sync --locked`, `uv run pytest` with a coverage report in the job summary.
  - **lint:** `ruff check` and `ruff format --check` on `tests/` and `scripts/`. Each module is added to the lint scope when Stage 4 rewrites it. The ruff configuration lives in `pyproject.toml`.
  - **docker:** builds the image, starts it with a throwaway `/data/config.json` and an empty migrated database, waits for `/health` to answer 200, and checks that the footer version is not "Version unknown".
- **Branch protection** on `master` and `staging`: changes only through pull requests, with the three jobs required to pass. A branch can only require checks its own workflow files run, so the required checks are switched on for `staging` when `dev` is next merged into it, and for `master` at switch-over (Stage 6); until then both require pull requests only (found while checking the plan, 2026-11-16). `dev` runs the same CI without protection, so day-to-day work is not slowed down. The builder sets this up with the user's confirmation, since it changes repository settings.
- **`dependabot.yml`:** weekly updates for GitHub Actions and for uv dependencies, grouped into one pull request per ecosystem. Each update goes through CI like any other change, which is what makes upgrades deliberate (#356 item 6).
- Actions are pinned to their current major versions (the existing workflow uses versions that GitHub already warns about).
- Dev dependencies added with `uv add --dev`: `time-machine`, `pytest-cov`, `ruff`.

### Legacy files removed

Deleted at the end of the stage, once what they protect is covered. Git history keeps them.

- `docs/superpowers/specs/2026-09-18-service-integration-design.md` and `docs/superpowers/plans/2026-09-25-service-integration-test-findings.md`. Before deleting, each domain rule they state is checked off against a test in `rules/` or `characterisation/`. Rules without a test get one.
- `.handovers/fullstack/`, `.handovers/review/` and `.handovers/documentation/` (health check, service integration and post-release fixes). Their decisions are already in the code, CLAUDE.md (logging rules) and the tests. `.handovers/CLAUDE.md` and `TEMPLATE.md` stay.
- `tests/test_protocol_services.md`, as above.
- The memory notes that point to these files are updated.

### Stage handover

- At the end of the stage, a handover at `.handovers/stages/stage-1-foundation-handover.md`, from `.handovers/TEMPLATE.md`, at most 100 lines (CLAUDE.md).
- It covers: what was delivered and where; decisions made during the work and why, including any departure from this spec; the comparison results; issues opened for bugs found; how to use the extractor and the comparison, and the rules for changing expected results; UI-only cases for the Stage 2 parity checklist; anything left open.
- The roadmap gets a rule that every stage ends with such a handover, and a status line per stage linking to it. CLAUDE.md's handover section gets the `stages/` folder.

## Left to the builder

- Where exactly the comparison tooling lives inside `scripts/` or `tests/`.
- The decimal precision used when comparing floats, as long as it is the same everywhere and documented.
- The fixed date used by the tests and the comparison.
- How the synthetic dataset builder and the test folders are organised, within the split above.
- The pinned versions of uv, the actions and the base image.
- The split into feature branches and pull requests, as long as the order is: extractor and baseline; move (with Docker, config location and version source) and comparison; then CI, tests, cleanup and docs.

## Done when

- `dev` has the src layout, the app runs locally, and the CI docker job is green.
- The comparison against `master` on `velo-supervisor-2000-2026-11-16.sqlite` shows no difference, after the move and at the end of the stage.
- CI (test, lint, docker) runs on every push and is green on `dev`; both branches require pull requests, and the required checks are in place on `staging` or scheduled for its next merge from `dev`, and for `master` in Stage 6.
- Every case listed under characterisation tests, page render tests and Strava sync tests is covered, every write and validate method is mapped to its tests, and every rule from the existing tests and the deleted specs has a test.
- The coverage report per module is recorded in the stage handover, with the uncovered parts named, so later stages know where the gaps are.
- Every existing version has a GitHub Release, and the README changelog links to the Releases page.
- The legacy files are removed, the stage handover is written, and `tests/README.md`, README, CLAUDE.md and `.claude/agents/` describe the new layout, testing and release setup.
