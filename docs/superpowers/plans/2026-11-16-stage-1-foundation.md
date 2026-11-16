# Stage 1 Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Put a permanent safety net (result extractor, comparison against `master`, characterisation tests, CI) under the app, move it to a src layout and a current Docker image, and replace the broken release flow, without changing any calculation.

**Architecture:** An integrity package in `scripts/integrity/` loads either the flat `master` layout or the new package layout, recalculates under a fixed clock and snapshots every stored column plus every derived value as JSON. The same package drives the local comparison against `master` and the characterisation tests. Work is done in four phases on four feature branches off `dev`, in the order the spec fixes.

**Tech Stack:** Python 3.12, FastAPI, Peewee, SQLite, uv, hatchling + hatch-vcs, pytest, time-machine, pytest-cov, ruff, GitHub Actions, Docker.

**Spec:** `docs/superpowers/specs/2026-11-16-stage-1-foundation-design.md` (approved 2026-11-16). Read it before starting any task; this plan does not repeat its reasoning.

## Global Constraints

- No calculation logic changes. The only behaviour change is the config location (Task 6), in its own commit.
- `master`'s code is never changed. Tags and Releases on existing tags are allowed (Task 17).
- The production copy `/home/xivind/code/velo-supervisor-2000-2026-11-16.sqlite` is never written to and never enters the repository. Every run copies it into the session scratchpad.
- No production data in the repository, except the component type defaults the user approved for `template_db.sqlite` (Task 15).
- Fixed clock everywhere: `FIXED_NOW = 2026-11-16 12:00:00` UTC, with `TZ=UTC` set in the test and extractor process. All synthetic dates lie before it.
- Floats in snapshots are rounded to 6 decimals. `None` and `0` stay different.
- An expected-result file is written only when it does not exist yet (`RECORD_EXPECTED=1`). An existing one is never overwritten by tooling; changing one means deleting it by hand, visible in the diff, with a documented reason.
- Logging rule from CLAUDE.md: `logging.error` only for real failures.
- No inline code comments except where the file already has that pattern. No boilerplate docstrings.
- Suspected bugs found while testing: open a new GitHub issue, reference it from the test, commit with "Refs #N", never "Closes"/"Fixes". Never fix a calculation bug in this stage.
- Commits and pushes: the user authorised on 2026-11-16 committing on the Stage 1 feature branches, pushing them and opening pull requests to `dev`. Never commit to `dev`, `staging` or `master`, never merge; the user merges every pull request. Each phase starts from `dev` after the user has merged the previous phase's pull request.
- After any task that moves or changes code: `graphify update .`.

## Review Focus

1. **A shallow or tag-less checkout builds the image.** CI's default `fetch-depth: 1` has no tags, so hatch-vcs gives `0.1.dev1+g…` and the footer shows a wrong but plausible version. Expected: the docker job checks out with `fetch-depth: 0` and fails if the footer version does not start with the latest tag's major.minor. Pinned in Task 7, step 5.
2. **`.dockerignore` must not exclude `.git`.** The build stage needs it for the version. Pinned in Task 7, step 5 (the same footer check fails if it is excluded).
3. **The app is started from a directory without `config.json`, or `VELO_SUPERVISOR_CONFIG` points to a missing file.** Expected: the error names the path it tried. Pinned in Task 6 by `test_missing_config_error_names_path`.
4. **`None` versus `0.0` in a stored column** (for example `lifetime_remaining` on a component without a lifetime). Expected: the snapshot keeps them different, so a refactor that turns one into the other shows up. Pinned in Task 1 by `test_snapshot_keeps_null_and_zero_apart`.
5. **Non-ASCII names** (Norwegian component and bike names with æ, ø, å). Expected: snapshots, expected files and page renders handle them unchanged. Pinned by a dataset component named `Bremseklosser bak æøå` (Task 8) and `test_snapshot_round_trips_non_ascii` (Task 1).

---

## Phase A: extractor and baseline, branch `feature/stage1-extractor`

Built against today's flat layout. `backend/` is still where the code lives.

### Task 1: Integrity package: loader, clock, recalculation, stored-state snapshot

**Files:**
- Create: `scripts/integrity/__init__.py`, `scripts/integrity/clock.py`, `scripts/integrity/loader.py`, `scripts/integrity/recalculate.py`, `scripts/integrity/snapshot.py`
- Create: `tests/integrity/test_snapshot.py`, `tests/integrity/test_loader.py`
- Modify: `pyproject.toml` (dev dependencies, pytest config)

**Interfaces:**
- Produces:
  - `clock.FIXED_NOW: datetime` (aware, UTC, `2026-11-16 12:00`); `clock.frozen_clock() -> ContextManager` (sets `TZ=UTC`, calls `time.tzset()`, enters `time_machine.travel(FIXED_NOW, tick=False)`).
  - `loader.detect_layout(checkout: Path) -> Literal["flat", "package"]` (`backend/business_logic.py` → flat, `src/velo_supervisor/business_logic.py` → package, else `ValueError`).
  - `loader.load_app(checkout: Path, db_path: Path, workdir: Path) -> AppModules`. Writes `workdir/config.json` (`db_path`, `strava_tokens` = `workdir/strava_tokens.json`, `verbose_logging: false`), chdirs into `workdir`, sets `VELO_SUPERVISOR_CONFIG`, removes previously imported app modules from `sys.modules` (flat names `main`, `business_logic`, `database_manager`, `database_model`, `utils`, `strava`, `middleware`, `scheduler`, `db_migration`, and every `velo_supervisor*` name), puts `checkout/backend` or `checkout/src` first on `sys.path`, imports. It does not restore cwd, env or `sys.path`; test fixtures do that through `monkeypatch` (`chdir`, `setenv`, `syspath_prepend`).
  - `AppModules` (dataclass): `layout: str`, `business_logic` (a `BusinessLogic(SimpleNamespace(strava_last_pull=None, strava_days_since_last_pull=None, db_path=...))` instance), `bl_module`, `database_manager`, `utils`, `db_path: Path`.
  - `recalculate.recalculate(app: AppModules) -> None`: `update_components_distance_iterator(read_unique_bikes())`, then `process_history_records(id)` for every component, then `update_time_based_fields()`, then `update_component_type_count(t)` for every component type.
  - `snapshot.stored_state(db_path: Path) -> dict[str, dict[str, dict]]`: reads with `sqlite3` directly (not the models), every table except `sqlite_%`, every column, keyed `table → primary key → {column: value}`, floats rounded to 6 decimals.
  - `snapshot.normalise_new_ids(state: dict, baseline_ids: set[str]) -> dict`: every primary key not in `baseline_ids` is replaced everywhere in the state (including inside JSON strings such as `collections.components`) by `new:<table>:<n>`, numbered by SQLite `rowid` order per table.
  - `snapshot.dumps(state: dict) -> str`: `json.dumps(..., sort_keys=True, ensure_ascii=False, indent=1)`.

- [ ] **Step 1: Create the branch, commit the stage documents, add dev dependencies**

Run: `git switch dev && git pull && git switch -c feature/stage1-extractor`. Commit the approved spec, this plan and the roadmap change (uncommitted on `dev` when the plan was written): `git add docs/superpowers && git commit -m "Add Stage 1 foundation spec and plan; test duties for later stages in the roadmap"`. Then `uv add --dev time-machine pytest-cov`.
In `pyproject.toml` add `[tool.pytest.ini_options]` with `testpaths = ["tests"]` and `pythonpath = ["scripts"]`.
Expected: `uv run pytest -q` still shows 32 passed.

- [ ] **Step 2: Write the failing tests**

`tests/integrity/test_snapshot.py`, each on a copy of `backend/template_db.sqlite` with rows inserted through `sqlite3`:
- `test_snapshot_covers_every_table_and_column`: keys equal the set of tables in `sqlite_master`; every row has every column from `PRAGMA table_info`.
- `test_snapshot_keeps_null_and_zero_apart`: two components, `lifetime_remaining` `NULL` and `0.0`; snapshot values are `None` and `0.0`.
- `test_snapshot_rounds_floats_to_six_decimals`: `component_distance` `1.23456789` → `1.234568`.
- `test_snapshot_round_trips_non_ascii`: component name `Bremseklosser bak æøå` survives `dumps` → `json.loads` unchanged, and `dumps` output contains the literal characters.
- `test_normalise_new_ids_is_stable`: two snapshots where new rows got different random IDs normalise to equal dicts, and the ID inside a collection's `components` JSON is replaced too.

`tests/integrity/test_loader.py`:
- `test_detect_layout_flat` (repo root today → `"flat"`), `test_detect_layout_rejects_unknown` (`tmp_path` → `ValueError`).
- `test_load_app_binds_to_given_database`: after `load_app`, `app.database_manager` reads the bikes of the given copy (insert one bike first).
- `test_extraction_is_repeatable`: load, recalculate and snapshot the same dataset twice under `frozen_clock()`, results equal.

- [ ] **Step 3: Run to verify they fail**

Run: `uv run pytest tests/integrity -v`
Expected: FAIL, `ModuleNotFoundError: No module named 'integrity'`.

- [ ] **Step 4: Implement the five modules with the interfaces above**

- [ ] **Step 5: Run to verify they pass**

Run: `uv run pytest -q`
Expected: all integrity tests pass, the 32 existing tests still pass.

- [ ] **Step 6: Commit**

```bash
git add scripts/integrity tests/integrity pyproject.toml uv.lock
git commit -m "Add integrity extractor: loader, fixed clock, recalculation and stored-state snapshot"
```

### Task 2: Derived values

**Files:**
- Create: `scripts/integrity/derived.py`, `tests/integrity/test_derived.py`

**Interfaces:**
- Consumes: `AppModules` (Task 1).
- Produces: `derived.derived_values(app: AppModules) -> dict[str, dict[str, dict]]`, keyed `resource → id → {field: value}`, resources `bike`, `component`, `collection`, `workplan`, `incident`, `component_type`, `overview`.

Sources, called through `app.business_logic` and `app.utils`: `get_bike_overview`, `get_bike_details(id)`, `process_bike_compliance_report(id)`, `get_component_overview`, `get_component_details(id)`, `calculate_component_triggers(component)`, `calculate_percentage_reached`, `get_component_collection_mapping`, `get_all_collections`, `get_collection_details(id)`, `calculate_collection_status`, `get_incident_reports`, `process_incidents`, `get_workplans`, `process_workplans`, `get_workplan_details(id)`, `derive_workplan_context`, `get_component_types`.

- Every positional tuple is turned into named fields through an explicit name list per tuple builder in `derived.py` (`INCIDENT_FIELDS`, `WORKPLAN_FIELDS`, and so on). Names are taken from the template that unpacks the tuple. A tuple whose length differs from its name list raises `ValueError`, so a shape change fails loudly.
- Peewee model instances become their field dicts; floats are rounded to 6 decimals.
- A field that is display formatting only may be left out, with the reason in `derived.py`'s module docstring, one line per field. The module docstring also lists every source function and what it contributes; it is the record the spec asks for.

- [ ] **Step 1: Write the failing tests** in `tests/integrity/test_derived.py`, on a small dataset inserted with `sqlite3` (one bike, two installed components with lifetime and service intervals, one service, one collection, one workplan with a planned service, one incident):
  - `test_derived_has_every_resource`: keys equal the seven resource names; the bike, both components, the collection, the workplan and the incident are present by ID.
  - `test_tuple_shape_change_fails_loudly`: monkeypatch `app.bl_module.get_workplan_data_tuple` (business_logic imports the builders by name, so patching `utils` has no effect) to return one extra element; `derived_values` raises `ValueError`.
  - `test_derived_is_json_serialisable`: `snapshot.dumps(derived_values(app))` does not raise.
- [ ] **Step 2: Run to verify they fail.** Run: `uv run pytest tests/integrity/test_derived.py -v`. Expected: FAIL, `ModuleNotFoundError`.
- [ ] **Step 3: Implement `derived_values`.**
- [ ] **Step 4: Run to verify they pass.** Run: `uv run pytest -q`. Expected: all pass.
- [ ] **Step 5: Commit** `scripts/integrity/derived.py tests/integrity/test_derived.py`: "Add derived values to the integrity extractor".

### Task 3: Extract and compare CLIs, baseline against master

**Files:**
- Create: `scripts/integrity/extract.py`, `scripts/integrity/compare.py`, `tests/integrity/test_compare.py`
- Create: `.handovers/stages/stage-1-foundation-handover.md` (from `.handovers/TEMPLATE.md`; filled in as the stage goes, finalised in Task 19)

**Interfaces:**
- Consumes: Tasks 1 and 2.
- Produces:
  - `extract.extract(checkout: Path, db_path: Path, scenario: Callable[[AppModules], None] | None = None) -> dict`: copies the database into a temp dir, enters `frozen_clock()`, `load_app`, `recalculate`, records baseline IDs, runs `scenario` if given (never followed by another full recalculation, which would hide a wrong incremental update in the operation), then returns `{"stored": normalise_new_ids(stored_state(...)), "derived": derived_values(...)}`.
  - `python scripts/integrity/extract.py --checkout PATH --db PATH --out PATH`: runs `extract` and writes `snapshot.dumps` to `--out`.
  - `compare.diff(left: dict, right: dict) -> list[str]`: one line per difference, `path: left=… right=…`; tables, rows or fields present on one side only are reported as `only in left` / `only in right`.
  - `python scripts/integrity/compare.py --ref REF --db PATH [--out-dir PATH]`: `git archive REF` into a temp dir, runs `extract.py` once for that export and once for the working tree, each in its own subprocess with the current interpreter, prints the diff and a summary (rows per table compared), exit code 0 when identical, 1 otherwise. Outputs go to `--out-dir`, default a temp dir; never inside the repo.

- [ ] **Step 1: Write the failing tests** in `tests/integrity/test_compare.py`:
  - `test_identical_snapshots_have_no_diff`.
  - `test_changed_value_is_reported_with_path`: one component's `service_status` differs; the single line names table, ID, column and both values.
  - `test_missing_table_and_row_are_reported`: a table only on the left and a row only on the right are both reported.
- [ ] **Step 2: Run to verify they fail.** Run: `uv run pytest tests/integrity/test_compare.py -v`. Expected: FAIL, `ModuleNotFoundError`.
- [ ] **Step 3: Implement `extract.py` and `compare.py`.**
- [ ] **Step 4: Run to verify they pass.** Run: `uv run pytest -q`. Expected: all pass.
- [ ] **Step 5: Prove the comparison can fail.** Export `master` with `git archive` to the scratchpad, change `total_distance = current_distance + distance_offset` to `+ distance_offset + 1` in `update_component_distance` in its `business_logic.py` copy, run `extract.py` on it and on an untouched export, and diff with `compare.diff`. Expected: non-empty diff naming affected components. Record the command and outcome in the handover.
- [ ] **Step 6: Run the baseline.** Run: `uv run python scripts/integrity/compare.py --ref master --db /home/xivind/code/velo-supervisor-2000-2026-11-16.sqlite --out-dir <scratchpad>/baseline`. Expected: exit 0, "identical", row counts matching 17 bikes, 638 components, 7449 rides, 228 services, 12 workplans, 15 incidents, 14 collections. Record the summary in the handover.
- [ ] **Step 7: Commit** `scripts/integrity tests/integrity .handovers/stages`: "Add extract and compare tools; baseline against master is identical".
- [ ] **Step 8: Push and open a pull request to `dev`** with the baseline summary and the failing-comparison proof in the description. The user merges.

---

## Phase B: move, version, config, Docker, branch `feature/stage1-src-layout`

### Task 4: Move to the src layout

**Files:**
- Move (`git mv`): `backend/{__init__,main,business_logic,database_manager,database_model,db_migration,strava,middleware,scheduler,utils,healthcheck}.py` → `src/velo_supervisor/`; `frontend/templates` → `src/velo_supervisor/templates`; `frontend/static` → `src/velo_supervisor/static`; `backend/{config.json.example,strava_tokens.example.json,uvicorn_log_config.ini,template_db.sqlite}` → `config/`; `create-container-vs2000.sh` → `scripts/`; `diagrams` → `docs/diagrams`; `DOCKERFILE` → `Dockerfile`
- Modify: every moved module's imports; `src/velo_supervisor/main.py:53-54`; `src/velo_supervisor/db_migration.py:9-10`; `pyproject.toml`; `.gitignore`; `tests/conftest.py`; `tests/test_*.py` imports; `scripts/integrity/loader.py` only if the package path needs it

**Interfaces:**
- Produces: package `velo_supervisor` importable after `uv sync`; `velo_supervisor.main:app`; `PACKAGE_DIR = Path(__file__).parent` in `main.py`; templates at `PACKAGE_DIR / "templates"`, static at `PACKAGE_DIR / "static"`.

- [ ] **Step 1: Branch.** Run: `git switch dev && git pull && git switch -c feature/stage1-src-layout`.
- [ ] **Step 2: Move the files** with the `git mv` list above. `backend/version.py` and `backend/current_version.txt` stay until Task 5.
- [ ] **Step 3: Rewrite imports** to `from velo_supervisor.<module> import …` / `from velo_supervisor import <module>`. Remove the `sys.path.insert` in `db_migration.py`. Templates and static use `PACKAGE_DIR`.
- [ ] **Step 4: Declare the package** in `pyproject.toml`: `[build-system] requires = ["hatchling", "hatch-vcs"]`, `build-backend = "hatchling.build"`; `[tool.hatch.build.targets.wheel] packages = ["src/velo_supervisor"]`. Keep `version = "0.1.0"` static for now (Task 5 makes it dynamic). Run `uv lock && uv sync`.
- [ ] **Step 5: Point the existing tests at the package.** In `tests/conftest.py`, `TEMPLATE_DB = REPO_ROOT / "config" / "template_db.sqlite"`, drop the `BACKEND_DIR` path insert, pop `velo_supervisor.*` modules and import from the package. Same import change in the four test files and in `tests/integrity/` (template path `config/template_db.sqlite`). Change `test_detect_layout_flat` (Task 1) to `test_detect_layout_package`, expecting `"package"` for the repo root.
- [ ] **Step 6: Verify.** Run: `uv run pytest -q`. Expected: all pass (32 existing plus the integrity tests). Run `grep -rn "\.\./frontend\|backend/" src scripts tests pyproject.toml`; expected: no hits.
- [ ] **Step 7: Run the app on a copy of the production database.** Copy the production file into the scratchpad, write a `config.json` at the repo root pointing to it (gitignored after step 8), run `uv run uvicorn velo_supervisor.main:app --port 8001` from the repo root, and request `/`, one `/bike_details/{id}`, one `/component_details/{id}`, `/static/js/main.js`. Expected: 200 for each. Stop the server.
- [ ] **Step 8: Update `.gitignore`:** `backend/config.json` → `/config.json`; `backend/__pycache__/*` and `backend/.mypy_cache/*` removed. Check `git status --ignored backend frontend` lists only `__pycache__`, then delete the leftover `backend/` and `frontend/` directories.
- [ ] **Step 9: Compare against master.** Run: `uv run python scripts/integrity/compare.py --ref master --db /home/xivind/code/velo-supervisor-2000-2026-11-16.sqlite`. Expected: exit 0, identical. Record in the handover.
- [ ] **Step 10: Commit** all moved and modified files: "Move to src layout as package velo_supervisor (#364)". Then `graphify update .` and check that community labels survived; relabel only if lost, and commit `graphify-out` separately.

### Task 5: Version from the git tag

**Files:**
- Modify: `pyproject.toml`, `src/velo_supervisor/utils.py:18-24`
- Delete: `backend/version.py`, `backend/current_version.txt`, `.github/workflows/run_version_script.yml`
- Test: `tests/test_version.py`

**Interfaces:**
- Produces: `utils.get_current_version() -> str`, returns `version("velo-supervisor-2000")`, or `"Version unknown"` on `PackageNotFoundError`, with `from importlib.metadata import version, PackageNotFoundError` at the top of `utils.py` (the tests patch `velo_supervisor.utils.version`).

- [ ] **Step 1: Write the failing tests** in `tests/test_version.py`: `test_version_comes_from_package_metadata` (monkeypatch `velo_supervisor.utils.version` to return `"1.2.3"`; result `"1.2.3"`) and `test_version_unknown_when_not_installed` (raise `PackageNotFoundError`; result `"Version unknown"`).
- [ ] **Step 2: Run to verify they fail.** Run: `uv run pytest tests/test_version.py -v`. Expected: FAIL (it still reads `current_version.txt`).
- [ ] **Step 3: Implement.** `pyproject.toml`: remove `version`, add `dynamic = ["version"]`, `[tool.hatch.version] source = "vcs"`, and `[tool.uv] cache-keys = [{ file = "pyproject.toml" }, { git = { commit = true, tags = true } }]`. Change `get_current_version` as in Interfaces. Delete the three files. Run `uv lock && uv sync`.
- [ ] **Step 4: Verify.** Run: `uv run pytest -q` (all pass) and `uv run python -c "from velo_supervisor.utils import get_current_version; print(get_current_version())"`. Expected: `0.5.1.devN+g<hash>` (N = commits since `v0.5.0`). Check the `velo-supervisor-2000` entry in `uv.lock` has no fixed `version` (it is dynamic), so `uv sync --locked` keeps passing after a new tag; if uv writes one, stop and report before going on.
- [ ] **Step 5: Commit:** "Derive the version from the git tag with hatch-vcs; remove the version bot (#121)".

### Task 6: Config location from `VELO_SUPERVISOR_CONFIG`

**Files:**
- Modify: `src/velo_supervisor/utils.py:26-30` and `:115-117`
- Test: `tests/test_config.py`

**Interfaces:**
- Produces: `utils.config_path() -> Path` = `Path(os.environ.get("VELO_SUPERVISOR_CONFIG", "config.json"))`; `read_config()` and `write_config(...)` use it. `read_config()` raises `FileNotFoundError` whose message contains the resolved path.

Note: the spec says `db_migration.py` uses the same lookup. It does not read `config.json` at all (it searches for the database file and asks), so it needs no change. Record this departure in the handover, and correct README line 150, which claims it reads `config.json`, in Task 17.

- [ ] **Step 1: Open the issue.** `gh issue create` titled "Settings changed on the config page are lost on every redeploy", body: `config.json` is copied into the image, the config page writes inside the container, `create-container-vs2000.sh` removes container and image on deploy. Note its number N.
- [ ] **Step 2: Write the failing tests** in `tests/test_config.py`: `test_read_config_uses_env_path`, `test_read_config_defaults_to_working_directory`, `test_write_config_writes_to_env_path` (form type `system_settings`, then the file at the env path has `verbose_logging: true`), `test_missing_config_error_names_path`.
- [ ] **Step 3: Run to verify they fail.** Run: `uv run pytest tests/test_config.py -v`. Expected: the env-path tests FAIL.
- [ ] **Step 4: Implement `config_path` and use it in both places.**
- [ ] **Step 5: Verify.** Run: `uv run pytest -q`. Expected: all pass.
- [ ] **Step 6: Commit:** "Read config.json from VELO_SUPERVISOR_CONFIG, default working directory. Refs #N".

### Task 7: Docker image and first CI workflow

**Files:**
- Modify: `Dockerfile` (rewrite), `scripts/create-container-vs2000.sh`
- Create: `.dockerignore`, `.github/workflows/tests.yml`

**Interfaces:**
- Produces: image with `VELO_SUPERVISOR_CONFIG=/data/config.json`, user UID 1000, `CMD ["uvicorn", "velo_supervisor.main:app", "--host", "0.0.0.0", "--port", "8000", "--log-config", "/app/uvicorn_log_config.ini"]`, `HEALTHCHECK --interval=600s --timeout=5s --retries=3 CMD ["python", "-m", "velo_supervisor.healthcheck"]`. Workflow `tests.yml` with jobs `test` and `docker` (Task 16 adds `lint`).

- [ ] **Step 1: Write the Dockerfile.** Build stage: `python:3.12-slim`, `apt-get install -y --no-install-recommends git`, `COPY --from=ghcr.io/astral-sh/uv:<current release> /uv /usr/local/bin/uv`, `ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy UV_PYTHON_DOWNLOADS=0`, `WORKDIR /app`, copy the repo, `uv sync --locked --no-dev --no-editable`. Runtime stage: `python:3.12-slim`, `useradd --uid 1000 --create-home app`, `COPY --from=build /app/.venv /app/.venv`, `COPY config/uvicorn_log_config.ini /app/`, `ENV PATH="/app/.venv/bin:$PATH" VELO_SUPERVISOR_CONFIG=/data/config.json`, `WORKDIR /app`, `USER app`, `EXPOSE 8000`, CMD and HEALTHCHECK as above. Keep the file's existing section-comment pattern.
- [ ] **Step 2: Write `.dockerignore`:** `.venv`, `**/__pycache__`, `.pytest_cache`, `graphify-out`, `*.sqlite` except `config/template_db.sqlite`, `/config.json`. `.git` is NOT ignored.
- [ ] **Step 3: Update `scripts/create-container-vs2000.sh`:** `docker build -t velo-supervisor-2000 .` run from the repo root (script `cd`s to its parent directory first); mounts, `TZ`, port and restart policy unchanged.
- [ ] **Step 4: Write `.github/workflows/tests.yml`:** on `push` (all branches) and `pull_request`. Job `test`: checkout (current major), `astral-sh/setup-uv` (current major, pinned uv version), `uv sync --locked`, `uv run pytest --cov=velo_supervisor --cov-report=term`, then `uv run coverage report --format=markdown >> $GITHUB_STEP_SUMMARY`.
- [ ] **Step 5: Add job `docker`:** checkout with `fetch-depth: 0`; `docker build -t vs2000:ci .`; make `/tmp/data/logs`, copy `config/template_db.sqlite` to `/tmp/data/db.sqlite`, write `/tmp/data/config.json` (`db_path: /data/db.sqlite`, `strava_tokens: /secrets/strava_tokens.json`), `chown -R 1000:1000 /tmp/data`; run with `-v /tmp/data:/data -p 8000:8000`; poll `/health` up to 60 s, fail unless 200 (print `docker logs` on failure); fetch `/` and fail unless the footer version matches `^[0-9]+\.[0-9]+\.[0-9]+` and starts with the major.minor of `git describe --tags --abbrev=0`. If `/health` is 503, fix the cause in the job's setup, never by loosening the check.
- [ ] **Step 6: Commit:** "Multi-stage non-root Docker image with config on /data; CI test and docker jobs".
- [ ] **Step 7: Push the branch and watch CI.** Run: `git push -u origin feature/stage1-src-layout` and `gh run watch`. Expected: `test` and `docker` green.
- [ ] **Step 8: Final comparison for the phase** (as Task 4 step 9), then open the pull request to `dev`. The description lists the switch-over steps for the Pi: move `config.json` to `/data/config.json`, check `/data` and `/secrets` are owned by UID 1000.

---

## Phase C: tests, branch `feature/stage1-tests`

Every test in this phase is new. The old test files keep running until Task 14 deletes them after the mapping is done.

### Task 8: Test foundation and synthetic dataset

**Files:**
- Create: `tests/fixtures/__init__.py`, `tests/fixtures/dataset.py`, `tests/fixtures/expected.py`, `tests/fixtures/expected/` (empty), `tests/characterisation/__init__.py`
- Modify: `tests/conftest.py` (rewritten; the old fixtures `app_env`, `migrated_env`, `modules` stay only until Task 14)

**Interfaces:**
- Produces:
  - `dataset.build_dataset(db_path: Path) -> None`: starts from a copy of `config/template_db.sqlite` with `run_all_migrations` applied, deletes the template's component types and inserts its own fixed set (so expected files never depend on the template's seed data), then writes every row with `sqlite3` and readable fixed IDs. `dataset.IDS`: a frozen dataclass of those IDs.
  - Fixtures in `conftest.py`: `clock` (autouse, `frozen_clock()`), `dataset_db(tmp_path) -> Path`, `app(dataset_db, tmp_path, monkeypatch) -> AppModules` (`load_app(REPO_ROOT, dataset_db, tmp_path)`, then `recalculate(app)` once, so every test starts from a recalculated dataset; cwd, env and `sys.path` restored by `monkeypatch`), `snapshot_now(app) -> Callable[[], dict]` (returns `{"stored": normalise_new_ids(stored_state(...), dataset IDs), "derived": derived_values(app)}` without recalculating, so an operation test sees exactly what the operation left behind).
  - `expected.assert_matches_expected(name: str, result: dict) -> None`: compares with `tests/fixtures/expected/<name>.json`; when the file is missing, writes it if `RECORD_EXPECTED=1`, otherwise fails saying so; never overwrites.

Dataset content (all dates before `FIXED_NOW`): bikes `bike-road`, `bike-gravel`, `bike-retired`; rides on each across 2025-2026, including rides before and after every install and service date; components covering every recalculation case in the spec: moved across both active bikes (`comp-chain-moved`), time-based lifetime and service intervals (`comp-tire-time`), distance offset (`comp-wheel-offset`), no installation history (`comp-no-history`), retired (`comp-pads-retired`), completed services resetting the interval (`comp-cassette-serviced`), services across several installation records (`comp-chain-moved` gets services in two installation periods), a bike whose status comes from its worst component (`bike-gravel`), `Bremseklosser bak æøå`; a collection with mixed statuses; a workplan and an incident with planned and completed services.

- [ ] **Step 1: Write `test_dataset_builds_and_recalculates`** in `tests/characterisation/test_dataset.py`: the `app` fixture builds and recalculates, `snapshot_now()` does not raise, every ID in `IDS` is in the snapshot.
- [ ] **Step 2: Run to verify it fails** (`ModuleNotFoundError: fixtures.dataset`).
- [ ] **Step 3: Implement** `dataset.py`, `expected.py` and the new fixtures.
- [ ] **Step 4: Run to verify it passes.** Run: `uv run pytest -q`. Expected: all pass.
- [ ] **Step 5: Commit:** "Add test foundation: fixed clock, synthetic dataset, expected-result files".

### Task 9: Recalculation characterisation

**Files:**
- Create: `tests/characterisation/test_recalculation.py`, `tests/fixtures/expected/recalculation.json`

- [ ] **Step 1: Write `test_recalculation_matches_expected`:** `assert_matches_expected("recalculation", snapshot_now())`. Plus one focused test per spec case, each asserting the exact expected value worked out by hand from the dataset (for example `test_moved_component_distance_sums_rides_on_both_bikes`, `test_offset_added_to_distance`, `test_no_history_uses_alternate_method`, `test_retired_component_counts_days_to_retirement`, `test_service_resets_interval`, `test_services_across_installation_periods`, `test_bike_status_is_worst_component`). Write down the arithmetic in each test's docstring.
- [ ] **Step 2: Run** `uv run pytest tests/characterisation -v`. Expected: the expected-file test FAILS ("missing, run with RECORD_EXPECTED=1"); focused tests pass or reveal a disagreement.
- [ ] **Step 3: Record:** `RECORD_EXPECTED=1 uv run pytest tests/characterisation`. Check the recorded file against the focused tests and the rules. A disagreement where the code is wrong: open an issue, keep what the code does, mark the focused test with the issue reference.
- [ ] **Step 4: Run without recording.** Expected: all pass.
- [ ] **Step 5: Commit:** "Characterise the recalculation on the synthetic dataset".

### Task 10: Operation scenarios: components, history, quick swap, types, config

**Files:**
- Create: `tests/characterisation/test_operations_components.py`, expected files `tests/fixtures/expected/op_<name>.json`

Each test runs one operation on `app.business_logic`, then `assert_matches_expected("op_<name>", snapshot_now())`, and asserts the operation's own `(success, message)` result. Methods: `create_component`, `modify_component_details`, `create_history_record` (install, uninstall, retire: three tests), `update_history_record`, `quick_swap_orchestrator` (each `fate`), `modify_component_type`, `delete_record` once per `table_selector` value it supports, `utils.write_config` once per form type.

- [ ] **Step 1: Write the tests.** Read each method's signature in `business_logic.py` first; the list above is the minimum.
- [ ] **Step 2: Run, expect FAIL on missing expected files.**
- [ ] **Step 3: Record and check by hand,** as Task 9 step 3. Write in the pull request description, per operation, which values were checked and how.
- [ ] **Step 4: Run without recording, expect PASS.**
- [ ] **Step 5: Commit:** "Characterise component, history, quick swap, type and config operations".

### Task 11: Operation scenarios: services, workplans, incidents, collections

**Files:**
- Create: `tests/characterisation/test_operations_services.py`, expected files `op_<name>.json`

Methods: `create_service_record`, `create_planned_service`, `create_planned_services`, `complete_services`, `update_service_record` (edit, and revert to planned), `create_incident_record`, `update_incident_record`, `create_workplan` (plain and from an incident), `update_workplan` (edit and complete), `create_collection`, `update_collection`, `change_collection_status`.

- [ ] **Steps 1-5:** as Task 10. Commit: "Characterise service, workplan, incident and collection operations".

### Task 12: Strava sync

**Files:**
- Create: `tests/strava/__init__.py`, `tests/strava/fake_oauth.py`, `tests/strava/test_sync.py`, `tests/fixtures/strava/{activities_page1,activities_page2,activities_empty,athlete,gear_<id>,token_refresh}.json`

**Interfaces:**
- Produces: `FakeOAuth2Session(client_id, token=None)` with `get(url) -> FakeResponse` (routes by URL to the fixture files; records calls) and `refresh_token(token_url, refresh_token=None, **kwargs) -> dict` (the code passes `client_id` and `client_secret` as keywords); `FakeResponse` with `.json()`, `.status_code`, `.reason`. Installed by monkeypatching `velo_supervisor.strava.OAuth2Session`.

Responses hold only the fields the code reads: activities `id`, `name`, `type`, `gear_id`, `distance`, `moving_time`, `start_date_local`, `commute`; athlete bikes; gear. Fully synthetic, written from Strava's API docs.

- [ ] **Step 1: Write the tests:** `test_all_mode_reads_every_page_until_empty`, `test_recent_mode_collects_bikes_from_rides_with_gear`, `test_ride_without_gear_is_stored`, `test_non_ride_activities_follow_current_behaviour` (assert what the code does today), `test_expired_token_is_refreshed_and_saved`, `test_refresh_all_bikes_merges_athlete_and_known_bikes`, and characterisation `op_strava_recent` / `op_strava_all` (`asyncio.run(update_rides_bulk(mode))`, then `assert_matches_expected`). The token file in `tmp_path` has `expires_at` relative to `FIXED_NOW`.
- [ ] **Steps 2-5:** fail, implement the fake, record and check, pass. Commit: "Test the Strava sync against synthetic responses".

### Task 13: Page render tests

**Files:**
- Create: `tests/pages/__init__.py`, `tests/pages/test_render.py`

- [ ] **Step 1: Write the tests** with `TestClient(main.app, raise_server_exceptions=False)`, where `main = importlib.import_module("velo_supervisor.main")` after the `app` fixture has bound the modules to the dataset (no `with`, so the lifespan and scheduler do not start): `test_every_page_renders` parametrised over `/`, `/component_overview`, `/incident_reports`, `/workplans`, `/component_types_overview`, `/config_overview`, `/help`, and the detail pages for every bike, component, collection, workplan and incident ID in `IDS`, each expecting 200. Not requested, with the reason in the module docstring: `/refresh_all_bikes` and `/refresh_rides/{mode}` (Strava actions, covered by Task 12), `/get_filtered_log` (reads the fixed path `/data/logs/app.log`), `/health` (covered by `test_health.py`). `test_unknown_ids_today` for each detail route with ID `does-not-exist`, asserting today's status code (expected 500; record what it is and note in the handover that Stage 4 changes it to 404).
- [ ] **Steps 2-4:** fail, make pass (fixture work only, no app changes), pass. **Step 5: Commit:** "Check that every page renders for every resource".

### Task 14: Rules, health and migration rewritten; old tests removed

**Files:**
- Create: `tests/rules/__init__.py`, `tests/rules/test_validation.py`, `tests/rules/test_services_rules.py`, `tests/rules/test_workplans_incidents_rules.py`, new `tests/test_health.py`, new `tests/test_migration.py`
- Delete: `tests/test_service_status.py`, `tests/test_workplans_incidents.py`, old `tests/test_health.py`, old `tests/test_migration.py`, the old fixtures in `tests/conftest.py`

- [ ] **Step 1: Write the validation tests.** One test per refusal branch (`return False, …`) of `validate_history_record`, `validate_quick_swap`, `validate_collection`, `validate_service_record`, `validate_threshold_configuration`, `validate_workplan_completion`, named `test_<method>_refuses_<reason>`, asserting `success is False` and a message substring; plus `test_<method>_accepts_valid_input` each.
- [ ] **Step 2: Write the rule tests** that replace the 25 old service and workplan tests and the 10 health and migration tests, rule for rule, as listed under "Existing tests, vetted 2026-11-16" in the spec. Tuple reads become checks on `snapshot_now()["derived"]`.
- [ ] **Step 3: Write the mapping** old test → new test(s) in the pull request description. Every one of the 35 old tests appears.
- [ ] **Step 4: Run** `uv run pytest -q`. Expected: all pass.
- [ ] **Step 5: Delete the old files and fixtures; run again.** Expected: all pass; `grep -rn "app_env\|migrated_env\|get_.*_data_tuple" tests` finds nothing.
- [ ] **Step 6: Commit:** "Rewrite rule, health and migration tests; remove the old suites".
- [ ] **Step 7: Push, check CI green, open the pull request to `dev`** with the hand-check notes (Tasks 9-12) and the mapping (step 3).

---

## Phase D: template, CI, releases, cleanup, docs, branch `feature/stage1-finish`

### Task 15: Template database defaults

**Files:**
- Modify: `config/template_db.sqlite`
- Create: `tests/fixtures/component_type_defaults.json`, `tests/test_template_db.py`

- [ ] **Step 1: Open the issue** "template_db.sqlite carries leftover in_use counts" (46 types, 1-34, 464 in total; deleting a type is refused while `in_use > 0`, `business_logic.py` `delete_record`). Note its number.
- [ ] **Step 2: Write `component_type_defaults.json`** from the production copy's `component_types` (all 50 rows, every column except `in_use`). Read the copy read-only.
- [ ] **Step 3: Write the failing tests:** `test_template_types_have_no_usage` (every `in_use` is 0) and `test_template_types_match_defaults` (rows equal the JSON).
- [ ] **Step 4: Run, expect FAIL.**
- [ ] **Step 5: Update the template** with `sqlite3`: set `in_use = 0`, insert Frame lock, Groupset battery, Rimtape, Sealant, update the 6 changed types, all from the JSON. Check the schema is unchanged (`sqlite_master` identical before and after).
- [ ] **Step 6: Run, expect PASS** (whole suite, since the dataset starts from the template; expected files must not change, because the dataset sets its own component types; if they change, stop and investigate).
- [ ] **Step 7: Commit:** "Reset template component type counts and adopt production defaults. Refs #N".

### Task 16: CI made complete and permanent

**Files:**
- Modify: `.github/workflows/tests.yml`, `pyproject.toml`
- Create: `.github/dependabot.yml`, `.github/release.yml`

- [ ] **Step 1: Add ruff:** `uv add --dev ruff`; `[tool.ruff]` in `pyproject.toml` with `include = ["tests/**/*.py", "scripts/**/*.py"]`, line length 120; run `uv run ruff format tests scripts && uv run ruff check --fix tests scripts`. Expected: clean.
- [ ] **Step 2: Add the `lint` job** to `tests.yml`: `uv run ruff check` and `uv run ruff format --check`.
- [ ] **Step 3: Write `dependabot.yml`:** `github-actions` and `uv`, weekly, one group per ecosystem, target branch `dev`.
- [ ] **Step 4: Write `release.yml`:** categories in this order: "Breaking changes (migration required)" (label `breaking-change`), "Features" (`enhancement`), "Fixes" (`bug`), "Other" (`*`). Create the `breaking-change` label with `gh label create` if missing.
- [ ] **Step 5: Push and confirm all three jobs green.**
- [ ] **Step 6: Branch protection (ask the user first, it changes repository settings).** Required checks can only be required on a branch whose own workflow files run them; `master` and `staging` do not have `tests.yml` until `dev` is merged into them, and requiring the checks earlier would block every pull request, including a data-integrity hotfix to `master`. So, with approval, `gh api`: `master` gets "pull request required" now and the required checks at switch-over (Stage 6); `staging` gets "pull request required" now and the required checks `test`, `lint`, `docker` right after the user next merges `dev` into `staging`. Record the settings, and the Stage 6 step, in the handover and in the roadmap's Stage 6.
- [ ] **Step 7: Commit:** "Complete CI: lint, coverage summary, Dependabot, release note categories".

### Task 17: Release backfill and README

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Find the `v0.4.6` commit:** the `master` merge between `v0.4.5` (`ca9c5b3`, 2025-09-02) and `v0.4.7` (`462a859`, 2025-10-16) that added quick swap. Identify with `git log --merges --first-parent master v0.4.5..v0.4.7` and the quick swap files.
- [ ] **Step 2: Prepare all 15 releases** in a scratchpad file: tag, target commit, title, notes copied word for word from the README changelog. Show the user the file. **Wait for approval.**
- [ ] **Step 3: Create them,** oldest first: `git tag v0.4.6 <commit> && git push origin v0.4.6` (only if step 1 was certain; otherwise fold its notes into `v0.4.7` as the spec says), then `gh release create <tag> --title <tag> --notes-file <file>` per version, `--latest` on `v0.5.0` only. Check `gh release list` shows 15 (or 14).
- [ ] **Step 4: Rewrite the README:** changelog → link to Releases; remove the Q1 2025 pilot notice; versioning section rewritten for the Releases page flow; setup for `config/`, `config.json` at the root locally and `/data/config.json` in Docker, `uv run uvicorn velo_supervisor.main:app --log-config config/uvicorn_log_config.ini`; migration as `python -m velo_supervisor.db_migration` (and drop the claim that it reads `config.json`).
- [ ] **Step 5: Commit:** "Move release notes to GitHub Releases and tidy the README".

### Task 18: Legacy removed

**Files:**
- Delete: `docs/superpowers/specs/2026-09-18-service-integration-design.md`, `docs/superpowers/plans/2026-09-25-service-integration-test-findings.md`, `.handovers/fullstack/*`, `.handovers/review/*`, `.handovers/documentation/*`, `tests/test_protocol_services.md`

- [ ] **Step 1: Check off the rules.** List every domain rule stated in the two service integration documents and every case in `test_protocol_services.md`. For each, name the test that covers it, or add one (in `tests/rules/`), or, for a UI-only case, put it in the handover's "Stage 2 parity checklist" section.
- [ ] **Step 2: Run** `uv run pytest -q`. Expected: all pass.
- [ ] **Step 3: Delete the files;** run `graphify update .`.
- [ ] **Step 4: Update memory notes** that point at them (`project_service_integration_status.md`: evidence now in git history at the commit before deletion; `reference_prod_db_copy.md`: replace the sandbox recipe with `uv run uvicorn velo_supervisor.main:app` from the repo root and the `compare.py` command).
- [ ] **Step 5: Commit:** "Remove service integration docs, old handovers and the manual test protocol; rules now covered by tests".

### Task 19: Docs, final comparison, handover

**Files:**
- Modify: `tests/README.md` (rewrite), `CLAUDE.md`, `.claude/agents/*.md`, `docs/superpowers/specs/2026-11-15-rewrite-roadmap-design.md`, `.handovers/stages/stage-1-foundation-handover.md`, `.handovers/CLAUDE.md`

- [ ] **Step 1: Rewrite `tests/README.md`:** layout, `uv run pytest`, the fixed clock, the dataset builder, expected files and the rule for changing them, `RECORD_EXPECTED`, and the comparison command.
- [ ] **Step 2: Update CLAUDE.md:** project structure paths, run command, Testing section (replaces "WE NEED TO IMPLEMENT PIPELINE FOR TESTING"), release flow, config location, `stages/` handovers, CI and branch protection. Update every `backend/`, `frontend/` and `DOCKERFILE` reference in `.claude/agents/*.md` and CLAUDE.md (13 references found on 2026-11-16). Add `stages/` to the handover structure in CLAUDE.md and `.handovers/CLAUDE.md`.
- [ ] **Step 3: Roadmap:** add "every stage ends with a handover in `.handovers/stages/`" under Stages, and a status line for Stage 1 linking the handover.
- [ ] **Step 4: Final comparison** as Task 4 step 9. Expected: identical.
- [ ] **Step 5: Coverage:** `uv run pytest --cov=velo_supervisor --cov-report=term-missing`; put the per-module table and the named uncovered parts in the handover.
- [ ] **Step 6: Finalise the handover** (at most 100 lines): delivered, decisions and departures (including the `db_migration` config note), comparison results at all three points, issues opened, extractor and comparison usage, rules for expected files, Stage 2 parity items, switch-over steps for the Pi, open items.
- [ ] **Step 7: Commit, push, CI green, open the pull request to `dev`.**
