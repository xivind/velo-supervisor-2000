# Service Integration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make services the actionable unit linking incidents and workplans: planned services with no date, completed on a date, workplans and incidents deriving their links through services.

**Architecture:** Services gain `status`, `incident_id` and `planned_date`. Workplans lose their affected bike/component fields and incidents lose `workplan_id`; both derive context from services. Health computation is untouched because the three date-ordered service reads in the database manager return only Completed rows. Two modals (plan, complete) share one JavaScript helper.

**Tech Stack:** Python 3.11, FastAPI, Peewee, SQLite, Jinja2, Bootstrap 5, vanilla JS, TomSelect, pytest (new, dev only).

**Spec:** `docs/superpowers/specs/2026-09-18-service-integration-design.md`

## Global Constraints

- Blank values are written as `None` (NULL), never empty strings.
- New model fields are plain `CharField()` with no `null=True`, matching `backend/database_model.py`.
- Business logic returns `(success, message)` tuples; routes stay thin; no DB queries in business_logic; no formatting in database_manager.
- `process_service_records` and `update_component_service_status` in `backend/business_logic.py` are never edited.
- Match existing naming (`read_*`, `write_*`, `get_*`, `create_*`, `update_*`, `process_*`), full variable names, no decorators or new idioms.
- main.js: `// ====` L1 sections, `// -----` L2 subsections, every block guarded by element existence, `window.functionName` for globals, TomSelect pattern `new TomSelect(el, {plugins: ['remove_button'], maxItems: null}); el.tomSelect = ts;`.
- No `git commit`, `git push` or `git merge` by the agent. Each task ends with a checkpoint where the human reviews and commits.
- Work on branch `feature/service-integration` created from `dev`.
- Run `graphify update .` after code changes.
- Run the app from `backend/` with `uvicorn main:app --log-config uvicorn_log_config.ini`. Tests run from repo root with `uv run pytest`.

---

## File map

| File | Responsibility in this plan |
|---|---|
| `backend/database_model.py` | Add `status`, `incident_id`, `planned_date` to Services; `notes` to ComponentHistory; remove affected fields from Workplans and `workplan_id` from Incidents |
| `backend/db_migration.py` | Steps 12 to 16 |
| `backend/database_manager.py` | Completed-only filters, planned-service reads, incident-service reads |
| `backend/utils.py` | `derive_workplan_context`, `get_effective_planned_date`, `get_planned_service_data_tuple`, updated tuple builders |
| `backend/business_logic.py` | Planned/complete/revert services, validation modes, derived workplan/incident payloads, history notes |
| `backend/main.py` | Route changes |
| `frontend/templates/modal_plan_services.html` | New (renamed from `modal_create_services_workplan.html`) |
| `frontend/templates/modal_complete_services.html` | New |
| `frontend/templates/modal_service_record.html`, `modal_workplan_record.html`, `modal_incident_record.html`, `modal_update_component_status.html`, `modal_quick_swap.html` | Field changes |
| `frontend/templates/modal_link_incident.html` | Deleted |
| `frontend/templates/workplan_details.html`, `workplans.html`, `incident_reports.html`, `bike_details.html`, `collection_details.html`, `component_details.html`, `help.html` | Page changes |
| `frontend/static/js/main.js` | New shared subsection for plan/complete modals; removals; simplifications |
| `tests/conftest.py`, `tests/test_migration.py`, `tests/test_service_status.py` | Automated tests |
| `tests/test_protocol_services.md` | Manual protocol |
| `pyproject.toml` | pytest dev dependency |

---

### Task 0: Branch and test harness

**Files:**
- Create: `tests/conftest.py`
- Modify: `pyproject.toml`

**Interfaces:**
- Produces: pytest fixtures `app_env` (chdir to temp dir containing `config.json` and a fresh copy of `backend/template_db.sqlite`) and `modules` (imported `database_manager`, `business_logic`, `utils` objects bound to that DB).

- [ ] **Step 1: Create the feature branch (human confirms first)**

```bash
git checkout dev && git checkout -b feature/service-integration
```

- [ ] **Step 2: Add pytest as a dev dependency**

In `pyproject.toml` add after the `dependencies` list:

```toml
[dependency-groups]
dev = [
    "pytest>=8.0",
]
```

Run: `uv sync` and then `uv run pytest --version`. Expected: a pytest version line.

- [ ] **Step 3: Write the conftest**

`tests/conftest.py`:

```python
"""Shared fixtures: every test gets its own copy of the template database"""

import os
import sys
import json
import shutil
import importlib
import pytest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BACKEND_DIR = os.path.join(REPO_ROOT, "backend")
TEMPLATE_DB = os.path.join(BACKEND_DIR, "template_db.sqlite")


@pytest.fixture
def app_env(tmp_path, monkeypatch):
    """Copy template db to tmp dir, write config.json there, chdir into it"""
    db_path = tmp_path / "test_db.sqlite"
    shutil.copy(TEMPLATE_DB, db_path)
    config = {"db_path": str(db_path),
              "strava_tokens": str(tmp_path / "strava_tokens.json"),
              "verbose_logging": False}
    (tmp_path / "config.json").write_text(json.dumps(config), encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    if BACKEND_DIR not in sys.path:
        sys.path.insert(0, BACKEND_DIR)
    return {"db_path": str(db_path), "tmp_path": tmp_path}


@pytest.fixture
def migrated_env(app_env):
    """Run db_migration against the copied template db so the schema is current"""
    import db_migration
    conn = db_migration.sqlite3.connect(app_env["db_path"])
    cursor = conn.cursor()
    db_migration.run_all_migrations(cursor, conn)
    conn.close()
    return app_env


@pytest.fixture
def modules(migrated_env):
    """Fresh imports of the app modules bound to the test database"""
    for name in ["database_model", "database_manager", "utils", "business_logic"]:
        sys.modules.pop(name, None)
    import utils
    import database_model
    import database_manager
    import business_logic
    from types import SimpleNamespace
    return SimpleNamespace(utils=utils,
                           database_model=database_model,
                           database_manager=business_logic.database_manager,
                           business_logic=business_logic.BusinessLogic(SimpleNamespace()))
```

Note: `run_all_migrations(cursor, conn)` does not exist yet. Task 3 extracts it from `migrate_database()` so tests can call the migration without the interactive prompts.

- [ ] **Step 4: Checkpoint**

Human reviews `pyproject.toml`, `uv.lock` and `tests/conftest.py` and commits with message `Add pytest harness for service integration work`.

---

### Task 1: Database model

**Files:**
- Modify: `backend/database_model.py:129-176`

**Interfaces:**
- Produces: `Services.status`, `Services.incident_id`, `Services.planned_date`, `ComponentHistory.notes`. Removes `Workplans.workplan_affected_component_ids`, `Workplans.workplan_affected_bike_id`, `Incidents.workplan_id`.

- [ ] **Step 1: Edit the models**

In `ComponentHistory` add after `distance_marker = FloatField()`:

```python
    notes = CharField()
```

In `Services` add after `workplan_id = CharField()`:

```python
    status = CharField()
    incident_id = CharField()
    planned_date = CharField()
```

In `Incidents` remove the line `workplan_id = CharField()`.

In `Workplans` remove the lines `workplan_affected_component_ids = CharField()` and `workplan_affected_bike_id = CharField()`.

- [ ] **Step 2: Verify import still works**

Run from `backend/` with a config present, or rely on Task 3's tests. `python3 -c "import ast,sys; ast.parse(open('backend/database_model.py').read())"` from repo root. Expected: no output.

- [ ] **Step 3: Checkpoint**

Human reviews and commits: `Add service status, incident link and planned date to model`.

---

### Task 2: Database manager reads

**Files:**
- Modify: `backend/database_manager.py:235-262` (three completed-only reads), `:316-329` (add new reads after `read_services_by_workplan`)
- Test: `tests/test_service_status.py` (first tests, extended in Task 6)

**Interfaces:**
- Produces:
  - `read_subset_service_history(component_id)` returns Completed only, newest first
  - `read_latest_service_record(component_id)`, `read_oldest_service_record(component_id)` Completed only
  - `read_all_services_by_component(component_id)` all statuses, planned first then by date desc
  - `read_planned_services_by_component(component_id)`
  - `read_planned_services_by_workplan(workplan_id)`
  - `read_services_by_incident(incident_id)`
  - `read_planned_services_by_bike(bike_id)` planned services whose component is installed on the bike
  - `read_all_planned_services()`
  - `read_incidents_by_workplan(workplan_id)` now derived: incidents that have at least one service in the workplan
  - `read_workplans_by_incident(incident_id)` workplans reached through the incident's services

- [ ] **Step 1: Write the failing test**

`tests/test_service_status.py`:

```python
"""Planned services must be invisible to health computation"""

import pytest


def seed_component(modules, component_id="comp-1", bike_id="bike-1"):
    dbm = modules.database_manager
    Bikes = modules.database_model.Bikes
    Components = modules.database_model.Components
    ComponentHistory = modules.database_model.ComponentHistory
    Bikes.create(bike_id=bike_id, bike_name="Test bike", bike_retired="False",
                 service_status=None, total_distance=0, notes=None)
    Components.create(component_id=component_id, bike_id=bike_id, component_name="Chain",
                      component_type="Chain", component_distance=0, component_distance_offset=0,
                      installation_status="Installed", service_interval=1000, service_interval_days=None,
                      service_next=None, service_next_days=None, service_status=None,
                      lifetime_expected=3000, lifetime_expected_days=None, lifetime_remaining=None,
                      lifetime_remaining_days=None, lifetime_status=None, threshold_km=100,
                      threshold_days=None, updated_date="2026-01-01 10:00", cost=None, notes=None)
    ComponentHistory.create(history_id="hist-1", component_id=component_id, bike_id=bike_id,
                            component_name="Chain", updated_date="2026-01-01 10:00",
                            update_reason="Installed", distance_marker=0, notes=None)
    return dbm


def test_completed_only_reads_skip_planned(modules):
    dbm = seed_component(modules)
    Services = modules.database_model.Services
    Services.create(service_id="svc-planned", component_id="comp-1", component_name="Chain",
                    bike_id=None, service_date=None, distance_marker=None, description="Planned wax",
                    workplan_id=None, status="Planned", incident_id=None, planned_date=None)
    Services.create(service_id="svc-done", component_id="comp-1", component_name="Chain",
                    bike_id="bike-1", service_date="2026-02-01 10:00", distance_marker=0,
                    description="Waxed", workplan_id=None, status="Completed", incident_id=None,
                    planned_date=None)

    assert dbm.read_latest_service_record("comp-1").service_id == "svc-done"
    assert dbm.read_oldest_service_record("comp-1").service_id == "svc-done"
    assert [service.service_id for service in dbm.read_subset_service_history("comp-1")] == ["svc-done"]
    assert [service.service_id for service in dbm.read_planned_services_by_component("comp-1")] == ["svc-planned"]
    assert [service.service_id for service in dbm.read_all_services_by_component("comp-1")] == ["svc-planned", "svc-done"]
```

- [ ] **Step 2: Run it to confirm it fails**

Run: `uv run pytest tests/test_service_status.py -v`
Expected: FAIL (either `run_all_migrations` missing from Task 3, or `read_planned_services_by_component` missing). If it fails on `run_all_migrations`, do Task 3 Step 1 first, then return.

- [ ] **Step 3: Edit the three completed-only reads**

Replace `backend/database_manager.py:235-262` with:

```python
    def read_subset_service_history(self, component_id):
        """Method to read completed services for a component, used by health computation"""
        return (Services.
                select()
                .where((Services.component_id == component_id) &
                       (Services.status == "Completed"))
                .order_by(Services.service_date.desc()))

    def read_subset_service_record(self, service_id):
        """Method to retrieve record for a specific entry in the service log"""
        return (Services
                .get_or_none(Services.service_id == service_id))

    def read_latest_service_record(self, component_id):
        """Method to retrieve the most recent completed service for a given component"""
        return (Services
                .select()
                .where((Services.component_id == component_id) &
                       (Services.status == "Completed"))
                .order_by(Services.service_date.desc())
                .first())

    def read_oldest_service_record(self, component_id):
        """Method to retrieve the oldest completed service for a given component"""
        return (Services
                .select()
                .where((Services.component_id == component_id) &
                       (Services.status == "Completed"))
                .order_by(Services.service_date.asc())
                .first())
```

- [ ] **Step 4: Replace `read_incidents_by_workplan` and add the new reads**

Replace `backend/database_manager.py:316-329` with:

```python
    def read_incidents_by_workplan(self, workplan_id):
        """Method to read incidents that have at least one service in a given workplan"""
        incident_ids = (Services
                        .select(Services.incident_id)
                        .where((Services.workplan_id == workplan_id) &
                               (Services.incident_id.is_null(False))))
        return (Incidents
                .select()
                .where(Incidents.incident_id.in_(incident_ids))
                .order_by(Incidents.incident_date.desc()))

    def read_workplans_by_incident(self, incident_id):
        """Method to read workplans reached through the services of a given incident"""
        workplan_ids = (Services
                        .select(Services.workplan_id)
                        .where((Services.incident_id == incident_id) &
                               (Services.workplan_id.is_null(False))))
        return (Workplans
                .select()
                .where(Workplans.workplan_id.in_(workplan_ids))
                .order_by(Workplans.due_date.desc()))

    def read_services_by_workplan(self, workplan_id):
        """Method to read all services linked to a specific workplan, planned first"""
        return (Services
                .select()
                .where(Services.workplan_id == workplan_id)
                .order_by(Services.status.desc(), Services.service_date.desc()))

    def read_planned_services_by_workplan(self, workplan_id):
        """Method to read planned services linked to a specific workplan"""
        return (Services
                .select()
                .where((Services.workplan_id == workplan_id) &
                       (Services.status == "Planned")))

    def read_services_by_incident(self, incident_id):
        """Method to read all services linked to a specific incident"""
        return (Services
                .select()
                .where(Services.incident_id == incident_id)
                .order_by(Services.status.desc(), Services.service_date.desc()))

    def read_all_services_by_component(self, component_id):
        """Method to read all services for a component regardless of status, planned first"""
        return (Services
                .select()
                .where(Services.component_id == component_id)
                .order_by(Services.status.desc(), Services.service_date.desc()))

    def read_planned_services_by_component(self, component_id):
        """Method to read planned services for a component"""
        return (Services
                .select()
                .where((Services.component_id == component_id) &
                       (Services.status == "Planned")))

    def read_planned_services_by_bike(self, bike_id):
        """Method to read planned services for components installed on a bike"""
        component_ids = (Components
                         .select(Components.component_id)
                         .where((Components.bike_id == bike_id) &
                                (Components.installation_status == "Installed")))
        return (Services
                .select()
                .where((Services.component_id.in_(component_ids)) &
                       (Services.status == "Planned")))

    def read_all_planned_services(self):
        """Method to read all planned services"""
        return (Services
                .select()
                .where(Services.status == "Planned"))
```

Note: `"Planned" > "Completed"` alphabetically, so `status.desc()` puts planned first.

- [ ] **Step 5: Run the test**

Run: `uv run pytest tests/test_service_status.py -v`
Expected: PASS (once Task 3 Step 1 exists).

- [ ] **Step 6: Checkpoint**

Human reviews and commits: `Filter health-computation service reads to completed services`.

---

### Task 3: Migration

**Files:**
- Modify: `backend/db_migration.py` (imports at top, new functions after line 526, `migrate_database` body)
- Test: `tests/test_migration.py`

**Interfaces:**
- Produces: `run_all_migrations(cursor, conn)` returning the `migrations_performed` list; `migrate_database()` keeps prompts and calls it.

- [ ] **Step 1: Extract `run_all_migrations`**

In `backend/db_migration.py`, add after the imports:

```python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils import generate_unique_id
```

Move the body of `migrate_database()` from `migrations_performed = []` through the last `if incidents_workplan_link:` block into a new function placed directly above `migrate_database`:

```python
def run_all_migrations(cursor, conn):
    """Run every migration step in order and return the list of steps that changed something"""
    migrations_performed = []

    print("\n" + "="*70)
    print("STARTING DATABASE MIGRATION")
    print("="*70)
```

followed by the existing eleven steps unchanged except that every `[n/11]` label becomes `[n/16]`, and ending with:

```python
    return migrations_performed
```

Then `migrate_database()` becomes:

```python
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        migrations_performed = run_all_migrations(cursor, conn)

        # Print summary
```

with the summary printing block kept as it is.

- [ ] **Step 2: Write the failing migration test**

`tests/test_migration.py`:

```python
"""Migration converts the old workplan/incident model to services"""

import sqlite3
import pytest


def seed_old_schema(db_path):
    """Seed the template db (old schema, plus workplan_id columns added by steps 10 and 11)"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("ALTER TABLE services ADD COLUMN workplan_id VARCHAR")
    cursor.execute("ALTER TABLE incidents ADD COLUMN workplan_id VARCHAR")
    cursor.execute("INSERT INTO bikes VALUES ('bike-1', 'Road bike', 'False', NULL, 0, NULL)")
    for component_id, name in [("comp-1", "Chain"), ("comp-2", "Cassette"), ("comp-3", "Brake pads")]:
        cursor.execute("""INSERT INTO components (component_id, bike_id, component_name, component_type,
                          component_distance, component_distance_offset, installation_status, service_interval,
                          lifetime_expected, updated_date) VALUES (?, 'bike-1', ?, 'Type', 0, 0, 'Installed', 1000, 3000, '2026-01-01 10:00')""",
                       (component_id, name))
    cursor.execute("""INSERT INTO workplans VALUES ('wp-planned', '2026-03-01 10:00', 'Planned', 'Small',
                      '["comp-1", "comp-2", "comp-3", "comp-gone"]', 'bike-1', 'Spring service', NULL, NULL)""")
    cursor.execute("""INSERT INTO workplans VALUES ('wp-done', '2025-03-01 10:00', 'Done', 'Small',
                      '["comp-1"]', 'bike-1', 'Last year', '2025-03-02 10:00', 'All good')""")
    cursor.execute("""INSERT INTO services (service_id, component_id, component_name, bike_id, service_date,
                      distance_marker, description, workplan_id) VALUES ('svc-1', 'comp-1', 'Chain', 'bike-1',
                      '2026-02-01 10:00', 0, 'Already waxed in plan', 'wp-planned')""")
    cursor.execute("""INSERT INTO incidents VALUES ('inc-comp', '2026-02-10 10:00', 'Open', 'Priority',
                      '["comp-2"]', 'bike-1', 'Cassette skips', NULL, NULL, 'wp-planned')""")
    cursor.execute("""INSERT INTO incidents VALUES ('inc-bike', '2026-02-11 10:00', 'Open', 'Monitor',
                      NULL, 'bike-1', 'Creaking', NULL, NULL, 'wp-planned')""")
    cursor.execute("""INSERT INTO incidents VALUES ('inc-done', '2025-02-11 10:00', 'Resolved', 'Monitor',
                      '["comp-1"]', 'bike-1', 'Old', '2025-03-02 10:00', 'Fixed', 'wp-done')""")
    conn.commit()
    conn.close()


def columns(db_path, table):
    conn = sqlite3.connect(db_path)
    names = [row[1] for row in conn.execute(f"PRAGMA table_info({table})")]
    conn.close()
    return names


def run_migration(db_path):
    import db_migration
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    performed = db_migration.run_all_migrations(cursor, conn)
    conn.close()
    return performed


def test_migration_converts_and_is_idempotent(app_env):
    db_path = app_env["db_path"]
    seed_old_schema(db_path)

    run_migration(db_path)

    assert {"status", "incident_id", "planned_date"} <= set(columns(db_path, "services"))
    assert "notes" in columns(db_path, "component_history")
    assert "workplan_affected_component_ids" not in columns(db_path, "workplans")
    assert "workplan_affected_bike_id" not in columns(db_path, "workplans")
    assert "workplan_id" not in columns(db_path, "incidents")

    conn = sqlite3.connect(db_path)
    assert conn.execute("SELECT status FROM services WHERE service_id='svc-1'").fetchone()[0] == "Completed"

    planned = conn.execute("""SELECT component_id, service_date, bike_id, distance_marker, incident_id
                              FROM services WHERE workplan_id='wp-planned' AND status='Planned'
                              ORDER BY component_id""").fetchall()
    assert [row[0] for row in planned] == ["comp-2", "comp-3"]
    assert all(row[1] is None and row[2] is None and row[3] is None for row in planned)
    assert planned[0][4] == "inc-comp"
    assert planned[1][4] is None

    done_description = conn.execute("SELECT workplan_description FROM workplans WHERE workplan_id='wp-done'").fetchone()[0]
    assert "Road bike" in done_description and "Chain" in done_description

    planned_description = conn.execute("SELECT workplan_description FROM workplans WHERE workplan_id='wp-planned'").fetchone()[0]
    assert "Deleted component" in planned_description

    bike_incident_description = conn.execute("SELECT incident_description FROM incidents WHERE incident_id='inc-bike'").fetchone()[0]
    assert "wp-planned" in bike_incident_description

    assert conn.execute("SELECT incident_id FROM services WHERE service_id='svc-1'").fetchone()[0] is None
    conn.close()

    snapshot = sqlite3.connect(db_path).execute("SELECT * FROM services ORDER BY service_id").fetchall()
    performed = run_migration(db_path)
    assert not [step for step in performed if "service integration" in step]
    assert sqlite3.connect(db_path).execute("SELECT * FROM services ORDER BY service_id").fetchall() == snapshot
```

- [ ] **Step 3: Run it to confirm it fails**

Run: `uv run pytest tests/test_migration.py -v`
Expected: FAIL on the `status` column assertion.

- [ ] **Step 4: Write the migration functions**

Add after `migrate_incidents_workplan_link` in `backend/db_migration.py`:

```python
def check_services_integration_columns(cursor):
    """Check which service integration columns are missing on the services table"""
    cursor.execute("PRAGMA table_info(services)")
    columns = [column[1] for column in cursor.fetchall()]

    columns_to_add = []
    for column_name in ['status', 'incident_id', 'planned_date']:
        if column_name not in columns:
            columns_to_add.append(column_name)

    return columns_to_add

def check_component_history_notes_column(cursor):
    """Check if component_history table needs notes column"""
    cursor.execute("PRAGMA table_info(component_history)")
    columns = [column[1] for column in cursor.fetchall()]

    columns_to_add = []
    if 'notes' not in columns:
        columns_to_add.append('notes')

    return columns_to_add

def check_workplans_affected_columns(cursor):
    """Check if workplans table still has the affected bike/component columns"""
    cursor.execute("PRAGMA table_info(workplans)")
    columns = [column[1] for column in cursor.fetchall()]

    return 'workplan_affected_component_ids' in columns or 'workplan_affected_bike_id' in columns

def check_incidents_workplan_column_present(cursor):
    """Check if incidents table still has the workplan_id column"""
    cursor.execute("PRAGMA table_info(incidents)")
    columns = [column[1] for column in cursor.fetchall()]

    return 'workplan_id' in columns

def migrate_services_integration_columns(cursor, conn):
    """Add status, incident_id and planned_date to services, mark existing rows Completed"""
    columns_to_add = check_services_integration_columns(cursor)

    if not columns_to_add:
        print("      → Table is compliant, service integration columns already present")
        return False

    for column_name in columns_to_add:
        cursor.execute(f"ALTER TABLE services ADD COLUMN {column_name} VARCHAR")
        print(f"      → Added {column_name} column to services table")

    cursor.execute("UPDATE services SET status = 'Completed' WHERE status IS NULL")
    print(f"      → Marked {cursor.rowcount} existing services as Completed")
    conn.commit()
    return True

def migrate_component_history_notes(cursor, conn):
    """Add notes column to component_history table"""
    columns_to_add = check_component_history_notes_column(cursor)

    if not columns_to_add:
        print("      → Table is compliant, notes column already present")
        return False

    cursor.execute("ALTER TABLE component_history ADD COLUMN notes VARCHAR")
    conn.commit()
    print("      → Added notes column to component_history table")
    return True

def read_names_for_migration(cursor, bike_id, component_ids):
    """Resolve bike and component names for migration messages"""
    bike_name = None
    if bike_id:
        cursor.execute("SELECT bike_name FROM bikes WHERE bike_id = ?", (bike_id,))
        row = cursor.fetchone()
        bike_name = row[0] if row else "Deleted bike"

    component_names = []
    missing_component_ids = []
    for component_id in component_ids:
        cursor.execute("SELECT component_name FROM components WHERE component_id = ?", (component_id,))
        row = cursor.fetchone()
        if row:
            component_names.append(row[0])
        else:
            component_names.append("Deleted component")
            missing_component_ids.append(component_id)

    return bike_name, component_names, missing_component_ids

def migrate_workplans_to_planned_services(cursor, conn):
    """Convert affected components on workplans into planned services, preserve names in description"""
    if not check_workplans_affected_columns(cursor):
        print("      → Workplans already converted, affected columns not present")
        return False

    cursor.execute("""SELECT workplan_id, workplan_status, workplan_affected_component_ids,
                             workplan_affected_bike_id, workplan_description
                      FROM workplans""")
    workplans = cursor.fetchall()

    converted = 0
    for workplan_id, workplan_status, affected_component_ids_raw, affected_bike_id, description in workplans:
        affected_component_ids = json.loads(affected_component_ids_raw) if affected_component_ids_raw else []
        if not affected_component_ids and not affected_bike_id:
            continue

        bike_name, component_names, missing_component_ids = read_names_for_migration(cursor,
                                                                                     affected_bike_id,
                                                                                     affected_component_ids)

        if workplan_status == "Planned":
            for component_id in affected_component_ids:
                if component_id in missing_component_ids:
                    continue
                cursor.execute("""SELECT 1 FROM services
                                  WHERE workplan_id = ? AND component_id = ?""", (workplan_id, component_id))
                if cursor.fetchone():
                    continue
                cursor.execute("SELECT component_name FROM components WHERE component_id = ?", (component_id,))
                component_name = cursor.fetchone()[0]
                cursor.execute("""INSERT INTO services (service_id, component_id, component_name, bike_id,
                                                        service_date, distance_marker, description, workplan_id,
                                                        status, incident_id, planned_date)
                                  VALUES (?, ?, ?, NULL, NULL, NULL, ?, ?, 'Planned', NULL, NULL)""",
                               (generate_unique_id(), component_id, component_name,
                                "Planned service (migrated from workplan)", workplan_id))
            names_to_note = ["Deleted component"] * len(missing_component_ids)
        else:
            names_to_note = component_names

        if workplan_status != "Planned" or names_to_note:
            note_parts = []
            if bike_name and workplan_status != "Planned":
                note_parts.append(f"bike: {bike_name}")
            if names_to_note:
                note_parts.append(f"components: {', '.join(names_to_note)}")
            if note_parts:
                migration_note = f"\n\nMigrated from earlier version, affected {'; '.join(note_parts)}"
                new_description = (description or "") + migration_note
                cursor.execute("UPDATE workplans SET workplan_description = ? WHERE workplan_id = ?",
                               (new_description, workplan_id))

        converted += 1
        print(f"      → Converted workplan {workplan_id} ({workplan_status})")

    conn.commit()
    print(f"      → Converted {converted} workplan(s)")
    return converted > 0

def migrate_incident_links_to_services(cursor, conn):
    """Rebuild incident to workplan links through services"""
    if not check_incidents_workplan_column_present(cursor):
        print("      → Incidents already converted, workplan_id column not present")
        return False

    cursor.execute("""SELECT incident_id, incident_status, incident_affected_component_ids,
                             incident_description, workplan_id
                      FROM incidents WHERE workplan_id IS NOT NULL""")
    incidents = cursor.fetchall()

    converted = 0
    for incident_id, incident_status, affected_component_ids_raw, description, workplan_id in incidents:
        affected_component_ids = json.loads(affected_component_ids_raw) if affected_component_ids_raw else []

        cursor.execute("SELECT workplan_status FROM workplans WHERE workplan_id = ?", (workplan_id,))
        row = cursor.fetchone()
        workplan_status = row[0] if row else None

        linked = 0
        if affected_component_ids:
            placeholders = ",".join("?" * len(affected_component_ids))
            cursor.execute(f"""UPDATE services SET incident_id = ?
                               WHERE workplan_id = ? AND incident_id IS NULL
                               AND component_id IN ({placeholders})""",
                           [incident_id, workplan_id] + affected_component_ids)
            linked = cursor.rowcount

        if linked == 0 and affected_component_ids and workplan_status == "Planned" and incident_status == "Open":
            for component_id in affected_component_ids:
                cursor.execute("SELECT component_name FROM components WHERE component_id = ?", (component_id,))
                row = cursor.fetchone()
                if not row:
                    continue
                cursor.execute("""INSERT INTO services (service_id, component_id, component_name, bike_id,
                                                        service_date, distance_marker, description, workplan_id,
                                                        status, incident_id, planned_date)
                                  VALUES (?, ?, ?, NULL, NULL, NULL, ?, ?, 'Planned', ?, NULL)""",
                               (generate_unique_id(), component_id, row[0],
                                "Planned service (migrated from incident)", workplan_id, incident_id))
                linked += 1

        if linked == 0:
            migration_note = f"\n\nMigrated from earlier version, previously linked to workplan {workplan_id}"
            cursor.execute("UPDATE incidents SET incident_description = ? WHERE incident_id = ?",
                           ((description or "") + migration_note, incident_id))

        converted += 1
        print(f"      → Converted incident {incident_id} ({linked} service link(s))")

    conn.commit()
    print(f"      → Converted {converted} incident(s)")
    return converted > 0

def migrate_drop_workplan_affected_columns(cursor, conn):
    """Rebuild workplans table without the affected bike/component columns"""
    if not check_workplans_affected_columns(cursor):
        print("      → Table is compliant, affected columns already dropped")
        return False

    cursor.execute("""
        CREATE TABLE workplans_new (
            workplan_id TEXT PRIMARY KEY UNIQUE,
            due_date TEXT,
            workplan_status TEXT,
            workplan_size TEXT,
            workplan_description TEXT,
            completion_date TEXT,
            completion_notes TEXT
        )
    """)
    cursor.execute("""INSERT INTO workplans_new
                      SELECT workplan_id, due_date, workplan_status, workplan_size,
                             workplan_description, completion_date, completion_notes
                      FROM workplans""")
    cursor.execute("DROP TABLE workplans")
    cursor.execute("ALTER TABLE workplans_new RENAME TO workplans")
    conn.commit()
    print("      → Dropped workplan_affected_component_ids and workplan_affected_bike_id from workplans")
    return True

def migrate_drop_incident_workplan_column(cursor, conn):
    """Rebuild incidents table without the workplan_id column"""
    if not check_incidents_workplan_column_present(cursor):
        print("      → Table is compliant, workplan_id column already dropped")
        return False

    cursor.execute("""
        CREATE TABLE incidents_new (
            incident_id TEXT PRIMARY KEY UNIQUE,
            incident_date TEXT,
            incident_status TEXT,
            incident_severity TEXT,
            incident_affected_component_ids TEXT,
            incident_affected_bike_id TEXT,
            incident_description TEXT,
            resolution_date TEXT,
            resolution_notes TEXT
        )
    """)
    cursor.execute("""INSERT INTO incidents_new
                      SELECT incident_id, incident_date, incident_status, incident_severity,
                             incident_affected_component_ids, incident_affected_bike_id,
                             incident_description, resolution_date, resolution_notes
                      FROM incidents""")
    cursor.execute("DROP TABLE incidents")
    cursor.execute("ALTER TABLE incidents_new RENAME TO incidents")
    conn.commit()
    print("      → Dropped workplan_id from incidents")
    return True
```

Add `import json` to the imports at the top of the file.

- [ ] **Step 5: Wire the steps into `run_all_migrations`**

Append after the `[11/16]` block, before `return migrations_performed`:

```python
        # NEW: Service integration (issue #351)
        print("\n[12/16] Checking services table (service integration columns)...")
        if migrate_services_integration_columns(cursor, conn):
            migrations_performed.append("✓ Added status, incident_id, planned_date to services (service integration)")

        print("\n[13/16] Checking component_history table (notes column)...")
        if migrate_component_history_notes(cursor, conn):
            migrations_performed.append("✓ Added notes to component_history (service integration)")

        print("\n[14/16] Converting workplan affected components to planned services...")
        if migrate_workplans_to_planned_services(cursor, conn):
            migrations_performed.append("✓ Converted workplans to planned services (service integration)")

        print("\n[15/16] Rebuilding incident links through services...")
        if migrate_incident_links_to_services(cursor, conn):
            migrations_performed.append("✓ Rebuilt incident links through services (service integration)")

        print("\n[16/16] Dropping superseded columns...")
        workplans_dropped = migrate_drop_workplan_affected_columns(cursor, conn)
        incidents_dropped = migrate_drop_incident_workplan_column(cursor, conn)
        if workplans_dropped or incidents_dropped:
            migrations_performed.append("✓ Dropped superseded workplan and incident columns (service integration)")
```

Important ordering: 14 and 15 run before 16, since they read the columns that 16 drops. The `[11/16]` incidents step must still run before 15, since 15 reads `incidents.workplan_id`; on a database that never had it, step 11 adds it empty and 15 converts nothing.

- [ ] **Step 6: Run the tests**

Run: `uv run pytest tests/ -v`
Expected: both test files PASS.

- [ ] **Step 7: Update the template database**

From repo root: `cp backend/template_db.sqlite /tmp/claude-scratch-template-backup.sqlite` then run the migration against the template non-interactively:

```bash
cd backend && uv run python -c "
import sqlite3, db_migration
conn = sqlite3.connect('template_db.sqlite'); cursor = conn.cursor()
print(db_migration.run_all_migrations(cursor, conn)); conn.close()"
```

Expected: printed list includes the service integration steps. Then verify with `uv run python -c "import sqlite3; print([r[1] for r in sqlite3.connect('backend/template_db.sqlite').execute('PRAGMA table_info(services)')])"` from repo root. Expected: includes `status`, `incident_id`, `planned_date`.

- [ ] **Step 8: Checkpoint**

Human reviews and commits: `Add migration for service integration model`.

---

### Task 4: Utils helpers

**Files:**
- Modify: `backend/utils.py:187-241` (`get_workplan_names_dict`, `get_incident_data_tuple`, `get_workplan_data_tuple`), add new functions after `get_workplan_data_tuple`

**Interfaces:**
- Produces:
  - `derive_workplan_context(services, database_manager)` -> dict `{"bike_ids": [...], "bike_names": [...], "component_ids": [...], "component_names": [...], "completed_count": int, "total_count": int}`
  - `get_effective_planned_date(service, workplan)` -> str or None
  - `get_planned_service_data_tuple(service, database_manager, workplan_names)` -> 11-tuple `(service_id, component_id, component_name, description, workplan_id, workplan_name, incident_id, effective_planned_date, planned_date, component_installation_status, component_oldest_history_date)`
  - `get_workplan_data_tuple` now 14-tuple: `(workplan_id, due_date, workplan_status, workplan_size, component_ids, component_names, bike_ids, bike_names, workplan_description, completion_date, completion_notes, elapsed_days, workplan_title, service_progress)` where `service_progress` is `{"completed": n, "total": m}` or None when the workplan has no services. Templates that unpacked `checkbox_progress` now unpack `service_progress`; checkbox progress from the description is still available through `parse_checkbox_progress` in `get_workplan_details`.
  - `get_incident_data_tuple` now 16-tuple: old 13 fields, then `workplans` (list of `(workplan_id, workplan_name)`), `planned_service_count`, `completed_service_count`.

- [ ] **Step 1: Write the helpers**

Replace `backend/utils.py:187-241` with:

```python
def derive_workplan_context(services, database_manager):
    """Derive bike, component and progress information for a workplan from its services"""
    bike_ids = []
    bike_names = []
    component_ids = []
    component_names = []
    completed_count = 0
    total_count = 0

    for service in services:
        total_count += 1
        if service.status == "Completed":
            completed_count += 1

        if service.component_id not in component_ids:
            component_ids.append(service.component_id)
            component = database_manager.read_component(service.component_id)
            component_names.append(component.component_name if component else "Deleted component")

            component_bike_id = component.bike_id if component and component.bike_id else None
            if component_bike_id and component_bike_id not in bike_ids:
                bike_ids.append(component_bike_id)
                bike_names.append(database_manager.read_bike_name(component_bike_id))

    return {"bike_ids": bike_ids,
            "bike_names": bike_names,
            "component_ids": component_ids,
            "component_names": component_names,
            "completed_count": completed_count,
            "total_count": total_count}

def get_effective_planned_date(service, workplan):
    """Return the service's own planned date, else the workplan due date, else None"""
    if service.planned_date:
        return service.planned_date

    if workplan and workplan.due_date:
        return workplan.due_date

    return None

def get_workplan_names_dict(database_manager):
    """Build dictionary mapping workplan_id -> workplan_name for all workplans"""
    workplan_names = {}
    for workplan in database_manager.read_all_workplans():
        context = derive_workplan_context(database_manager.read_services_by_workplan(workplan.workplan_id),
                                          database_manager)
        workplan_names[workplan.workplan_id] = generate_workplan_title(context["component_names"],
                                                                       context["bike_names"][0] if context["bike_names"] else None,
                                                                       workplan.workplan_description)

    return workplan_names

def get_incident_data_tuple(incident, database_manager, workplan_names):
    """Build standard incident data tuple for display (16 fields)"""
    incident_services = list(database_manager.read_services_by_incident(incident.incident_id))
    incident_workplans = []
    for service in incident_services:
        if service.workplan_id and service.workplan_id not in [workplan_id for workplan_id, _ in incident_workplans]:
            incident_workplans.append((service.workplan_id, workplan_names.get(service.workplan_id, None)))

    return (incident.incident_id,
            incident.incident_date,
            incident.incident_status,
            incident.incident_severity,
            parse_json_string(incident.incident_affected_component_ids),
            database_manager.read_component_names(incident.incident_affected_component_ids),
            incident.incident_affected_bike_id,
            database_manager.read_bike_name(incident.incident_affected_bike_id),
            incident.incident_description,
            incident.resolution_date,
            incident.resolution_notes,
            calculate_elapsed_days(incident.incident_date,
                                   incident.resolution_date if incident.resolution_date else get_formatted_datetime_now())[1],
            generate_incident_title(database_manager.read_component_names(incident.incident_affected_component_ids),
                                    database_manager.read_bike_name(incident.incident_affected_bike_id),
                                    incident.incident_description),
            incident_workplans,
            sum(1 for service in incident_services if service.status == "Planned"),
            sum(1 for service in incident_services if service.status == "Completed"))

def get_workplan_data_tuple(workplan, database_manager):
    """Build standard workplan data tuple for display (14 fields)"""
    context = derive_workplan_context(database_manager.read_services_by_workplan(workplan.workplan_id),
                                      database_manager)
    service_progress = ({"completed": context["completed_count"], "total": context["total_count"]}
                        if context["total_count"] > 0 else None)

    return (workplan.workplan_id,
            workplan.due_date,
            workplan.workplan_status,
            workplan.workplan_size,
            context["component_ids"],
            context["component_names"],
            context["bike_ids"],
            context["bike_names"],
            workplan.workplan_description,
            workplan.completion_date,
            workplan.completion_notes,
            calculate_elapsed_days(workplan.due_date,
                                   workplan.completion_date if workplan.completion_date else get_formatted_datetime_now())[1],
            generate_workplan_title(context["component_names"],
                                    context["bike_names"][0] if context["bike_names"] else None,
                                    workplan.workplan_description),
            service_progress)

def get_planned_service_data_tuple(service, database_manager, workplan_names):
    """Build standard planned service tuple for display (11 fields)"""
    workplan = database_manager.read_single_workplan(service.workplan_id) if service.workplan_id else None
    component = database_manager.read_component(service.component_id)
    oldest_history_record = database_manager.read_oldest_history_record(service.component_id)

    return (service.service_id,
            service.component_id,
            component.component_name if component else "Deleted component",
            service.description,
            service.workplan_id,
            workplan_names.get(service.workplan_id, None) if service.workplan_id else None,
            service.incident_id,
            get_effective_planned_date(service, workplan),
            service.planned_date,
            component.installation_status if component else "Deleted",
            oldest_history_record.updated_date if oldest_history_record else None)
```

Note: `generate_workplan_title` and `generate_incident_title` check `names != ["Not assigned"]`. `derive_workplan_context` returns `[]` for no components, which the title functions treat as falsy, so titles fall back to description. No change needed to them.

- [ ] **Step 2: Add a unit test**

Append to `tests/test_service_status.py`:

```python
def test_effective_planned_date_prefers_service(modules):
    from types import SimpleNamespace
    utils = modules.utils
    workplan = SimpleNamespace(due_date="2026-05-01 10:00")
    assert utils.get_effective_planned_date(SimpleNamespace(planned_date="2026-04-01 10:00"), workplan) == "2026-04-01 10:00"
    assert utils.get_effective_planned_date(SimpleNamespace(planned_date=None), workplan) == "2026-05-01 10:00"
    assert utils.get_effective_planned_date(SimpleNamespace(planned_date=None), None) is None
```

Run: `uv run pytest tests/test_service_status.py -v`. Expected: PASS.

- [ ] **Step 3: Checkpoint**

Human reviews and commits: `Derive workplan and incident context from services in utils`.

---

### Task 5: Business logic, planned services and completion

**Files:**
- Modify: `backend/business_logic.py:2148-2331` (`create_service_record`, `bulk_create_service_records` replaced, `update_service_record`, `validate_service_record`), `:3040-3070` (delete recalculation extraction)
- Test: `tests/test_service_status.py`

**Interfaces:**
- Produces:
  - `create_service_record(component_id, service_date, service_description, workplan_id=None, status="Completed", incident_id=None, planned_date=None)`
  - `create_planned_services(component_ids, service_description, workplan_id=None, incident_id=None, planned_date=None)` -> `(success, message_dict)` same dict shape as old bulk create, with keys `type`, `summary`, `total_count`, `success_count`, `successful_components`, `failed_components`, plus `incident_hints` list (empty here)
  - `complete_services(service_ids, service_date, completion_note=None)` -> `(success, message_dict)` with `successful_components`, `failed_components` (name is the component name) and `incident_hints` (list of strings)
  - `update_service_record(component_id, service_id, service_date, service_description, workplan_id=None, status="Completed", incident_id=None, planned_date=None)`
  - `validate_service_record(mode, component_id, service_id, service_date)` with modes `"create service"`, `"edit service"`, `"plan service"`, `"complete service"`
  - `recalculate_component_after_service_removal(component_id)` -> `(success, message)`

- [ ] **Step 1: Write the failing tests**

Append to `tests/test_service_status.py`:

```python
def snapshot_health(modules, component_id="comp-1"):
    component = modules.database_manager.read_component(component_id)
    return (component.service_next, component.service_status, component.component_distance)


def test_planned_services_do_not_touch_health(modules):
    seed_component(modules)
    bl = modules.business_logic
    success, _ = bl.create_service_record("comp-1", "2026-02-01 10:00", "Waxed chain")
    assert success
    before = snapshot_health(modules)

    success, message = bl.create_planned_services(["comp-1"], "Plan new wax")
    assert success, message
    assert snapshot_health(modules) == before

    planned = list(modules.database_manager.read_planned_services_by_component("comp-1"))
    assert len(planned) == 1
    assert planned[0].service_date is None and planned[0].bike_id is None and planned[0].distance_marker is None


def test_complete_then_revert_matches_deletion(modules):
    seed_component(modules)
    bl = modules.business_logic
    dbm = modules.database_manager
    assert bl.create_service_record("comp-1", "2026-02-01 10:00", "First wax")[0]
    baseline = snapshot_health(modules)

    success, message = bl.create_planned_services(["comp-1"], "Second wax")
    assert success, message
    planned_id = list(dbm.read_planned_services_by_component("comp-1"))[0].service_id

    success, message = bl.complete_services([planned_id], "2026-03-01 10:00", "done early")
    assert success, message
    completed = dbm.read_single_service_record(planned_id)
    assert completed.status == "Completed" and completed.service_date == "2026-03-01 10:00"
    assert "done early" in completed.description
    assert dbm.read_latest_service_record("comp-1").service_id == planned_id

    success, message = bl.update_service_record("comp-1", planned_id, None, completed.description, status="Planned")
    assert success, message
    reverted = dbm.read_single_service_record(planned_id)
    assert reverted.status == "Planned" and reverted.service_date is None and reverted.distance_marker is None
    assert snapshot_health(modules) == baseline


def test_validation_rules(modules):
    seed_component(modules)
    bl = modules.business_logic
    dbm = modules.database_manager
    assert bl.create_service_record("comp-1", "2026-02-01 10:00", "First wax")[0]

    success, message = bl.create_planned_services(["comp-1"], "abc")
    assert not success and "at least 5" in str(message)

    assert bl.create_planned_services(["comp-1"], "Plan A", workplan_id="wp-x")[0]
    success, message = bl.create_planned_services(["comp-1"], "Plan B", workplan_id="wp-x")
    assert not success and "already" in str(message)

    planned_id = list(dbm.read_planned_services_by_component("comp-1"))[0].service_id
    success, message = bl.complete_services([planned_id], "2025-12-01 10:00")
    assert not success and "creation date" in str(message)
    success, message = bl.complete_services([planned_id], "2099-01-01 10:00")
    assert not success and "future" in str(message)

    dbm.write_component_details("comp-1", {"installation_status": "Retired"})
    success, message = bl.complete_services([planned_id], "2026-03-01 10:00")
    assert not success and "retired" in str(message).lower()
```

- [ ] **Step 2: Run to confirm failure**

Run: `uv run pytest tests/test_service_status.py -v`
Expected: the three new tests FAIL with attribute errors.

- [ ] **Step 3: Rewrite `validate_service_record`**

Replace the method at `backend/business_logic.py:2295-2330` with:

```python
    def validate_service_record(self, mode, component_id, service_id, service_date):
        """Method to validate service records before processing and storing in database"""
        logging.debug(f"Running validation rules for service records: {service_id}.")

        current_service = database_manager.read_single_service_record(service_id)
        if mode in ("edit service", "complete service") and not current_service:
            logging.warning(f"Service record not found: {service_id}")
            return False, f"Service record not found: {service_id}"

        component = database_manager.read_component(component_id)
        if not component:
            logging.warning(f"Associated component for service record {service_id} not found")
            return False, f"Associated component for service record {service_id} not found"

        if component.installation_status == "Retired":
            logging.warning(f"Services cannot be changed on a retired component: {component.component_name}")
            return False, f"Services cannot be changed on a retired component: {component.component_name}"

        if mode == "complete service" and current_service.status != "Planned":
            logging.warning(f"Only planned services can be completed. Component: {component.component_name}")
            return False, f"Only planned services can be completed. Component: {component.component_name}"

        if mode == "plan service":
            logging.debug(f"Validation of planned service for {component.component_name} passed")
            return True, f"Validation of planned service for {component.component_name} passed"

        success, message = validate_date_format(service_date)
        if not success:
            logging.warning(message)
            return False, message

        history_records = database_manager.read_subset_component_history(component.component_id)
        if not history_records:
            logging.warning(f"Services cannot be registered to components that have never been installed. Component: {component.component_name}")
            return False, f"Services cannot be registered to components that have never been installed. Component: {component.component_name}"

        oldest_history_record_date = database_manager.read_oldest_history_record(component.component_id).updated_date

        if service_date <= oldest_history_record_date:
            logging.warning(f"Service date cannot be at or before component creation date: {oldest_history_record_date}. Component: {component.component_name}")
            return False, f"Service date cannot be at or before component creation date {oldest_history_record_date}. Component: {component.component_name}"

        if service_date > datetime.now().strftime("%Y-%m-%d %H:%M"):
            logging.warning(f"Service date cannot be in the future. Component: {component.component_name}")
            return False, f"Service date cannot be in the future. Component: {component.component_name}"

        if mode == "complete service" and current_service.workplan_id:
            workplan = database_manager.read_single_workplan(current_service.workplan_id)
            if workplan and workplan.workplan_status == "Done" and workplan.completion_date and service_date > workplan.completion_date:
                logging.warning(f"Service date cannot be after the completion date of its workplan: {workplan.completion_date}. Reopen the workplan first. Component: {component.component_name}")
                return False, f"Service date cannot be after the completion date of its workplan ({workplan.completion_date}). Reopen the workplan first. Component: {component.component_name}"

        logging.debug(f"Validation of service record for {component.component_name} passed")
        return True, f"Validation of service record for {component.component_name} passed"
```

- [ ] **Step 4: Rewrite `create_service_record`, replace bulk create, add `complete_services`**

Replace `backend/business_logic.py:2148-2261` (from `def create_service_record` through the end of `bulk_create_service_records`) with:

```python
    def create_service_record(self,
                              component_id,
                              service_date,
                              service_description,
                              workplan_id=None,
                              status="Completed",
                              incident_id=None,
                              planned_date=None):
        """Method to add service record, planned or completed"""
        try:
            service_id = generate_unique_id()

            workplan_id = workplan_id if workplan_id and workplan_id.strip() else None
            incident_id = incident_id if incident_id and incident_id.strip() else None
            planned_date = planned_date if planned_date and planned_date.strip() else None
            service_description = service_description if service_description and service_description.strip() else None

            if status == "Planned":
                return self.create_planned_service(service_id, component_id, service_description,
                                                   workplan_id, incident_id, planned_date)

            success, message = self.validate_service_record("create service", component_id, service_id, service_date)
            if not success:
                logging.error(f"Validation of service record failed: {message}")
                return success, message

            service_data = {"service_id": service_id,
                            "component_id": component_id,
                            "component_name": "",
                            "service_date": service_date,
                            "description": service_description,
                            'bike_id': "",
                            'distance_marker': 0,
                            'workplan_id': workplan_id,
                            'status': "Completed",
                            'incident_id': incident_id,
                            'planned_date': planned_date}

            success, message = database_manager.write_service_record(service_data)
            if not success:
                logging.error(f"Error creating service record: {message}")
                return success, message

            success, message = self.process_service_records(component_id, service_id, service_date, service_description, workplan_id)
            if not success:
                logging.error(f"Error processing service record: {message}")
                return success, message

            logging.info(f"Creation of service record successful: {message}")
            return success, message

        except Exception as error:
            logging.error(f"An error occured creating service record for component with id {component_id}: {str(error)}")
            return False, f"Error creating service record for {component_id}: {str(error)}"

    def create_planned_service(self, service_id, component_id, service_description, workplan_id, incident_id, planned_date):
        """Method to add a single planned service, no date, no distance, no bike"""
        success, message = self.validate_service_record("plan service", component_id, service_id, None)
        if not success:
            logging.error(f"Validation of planned service failed: {message}")
            return success, message

        component = database_manager.read_component(component_id)

        if not service_description or len(service_description.strip()) < 5:
            logging.warning(f"Description must be at least 5 characters. Component: {component.component_name}")
            return False, f"Description must be at least 5 characters. Component: {component.component_name}"

        if planned_date:
            success, message = validate_date_format(planned_date)
            if not success:
                logging.warning(message)
                return False, message

        if workplan_id:
            for existing_service in database_manager.read_planned_services_by_workplan(workplan_id):
                if existing_service.component_id == component_id:
                    logging.warning(f"Component {component.component_name} already has a planned service in this workplan")
                    return False, f"Component {component.component_name} already has a planned service in this workplan"

        service_data = {"service_id": service_id,
                        "component_id": component_id,
                        "component_name": component.component_name,
                        "service_date": None,
                        "description": service_description,
                        'bike_id': None,
                        'distance_marker': None,
                        'workplan_id': workplan_id,
                        'status': "Planned",
                        'incident_id': incident_id,
                        'planned_date': planned_date}

        success, message = database_manager.write_service_record(service_data)
        if success:
            logging.info(f"Creation of planned service successful: {message}")
        else:
            logging.error(f"Creation of planned service failed: {message}")

        return success, message

    def build_bulk_service_message(self, action_label, successful_components, failed_components, incident_hints):
        """Method to build the report dict used by the plan and complete services modals"""
        total_count = len(successful_components) + len(failed_components)
        success_count = len(successful_components)

        if success_count == total_count:
            message_type = "success"
            summary = f"Successfully {action_label} services for all {success_count} components"
        elif success_count > 0:
            message_type = "partial_failure"
            summary = f"Only {success_count} of {total_count} services were {action_label}"
        else:
            message_type = "complete_failure"
            summary = f"No services were {action_label}"

        return {"type": message_type,
                "summary": summary,
                "total_count": total_count,
                "success_count": success_count,
                "successful_components": successful_components,
                "failed_components": failed_components,
                "incident_hints": incident_hints}

    def create_planned_services(self, component_ids, service_description, workplan_id=None, incident_id=None, planned_date=None):
        """Method to create planned services for multiple components"""
        try:
            logging.info(f"Starting planned service creation for {len(component_ids)} components")

            if not component_ids:
                return False, "No components selected"

            successful_components = []
            failed_components = []

            for component_id in component_ids:
                component = database_manager.read_component(component_id)
                component_name = component.component_name if component else f"Component {component_id}"

                success, message = self.create_service_record(component_id=component_id,
                                                              service_date=None,
                                                              service_description=service_description,
                                                              workplan_id=workplan_id,
                                                              status="Planned",
                                                              incident_id=incident_id,
                                                              planned_date=planned_date)

                if success:
                    successful_components.append(component_name)
                    logging.info(f"Created planned service for {component_name}")
                else:
                    failed_components.append({"name": component_name, "error": message})
                    logging.error(f"Failed to create planned service for {component_id}: {message}")

            message = self.build_bulk_service_message("planned", successful_components, failed_components, [])
            return message["type"] == "success", message

        except Exception as error:
            logging.error(f"Error in planned service creation: {str(error)}")
            return False, f"Error creating planned services: {str(error)}"

    def complete_services(self, service_ids, service_date, completion_note=None):
        """Method to complete planned services with one date, keeping their descriptions"""
        try:
            logging.info(f"Starting completion of {len(service_ids)} services")

            if not service_ids:
                return False, "No services selected"

            completion_note = completion_note if completion_note and completion_note.strip() else None

            successful_components = []
            failed_components = []
            touched_incident_ids = []

            for service_id in service_ids:
                service = database_manager.read_single_service_record(service_id)
                if not service:
                    failed_components.append({"name": f"Service {service_id}", "error": "Service record not found"})
                    continue

                component = database_manager.read_component(service.component_id)
                component_name = component.component_name if component else f"Component {service.component_id}"

                success, message = self.validate_service_record("complete service", service.component_id, service_id, service_date)
                if not success:
                    failed_components.append({"name": component_name, "error": message})
                    logging.error(f"Failed to complete service {service_id}: {message}")
                    continue

                service_description = service.description
                if completion_note:
                    service_description = f"{service.description}\n{completion_note}"

                service_data = {"service_id": service_id,
                                "component_id": service.component_id,
                                "component_name": component_name,
                                "service_date": service_date,
                                "description": service_description,
                                'status': "Completed"}

                success, message = database_manager.write_service_record(service_data)
                if not success:
                    failed_components.append({"name": component_name, "error": message})
                    logging.error(f"Failed to write completed service {service_id}: {message}")
                    continue

                success, message = self.process_service_records(service.component_id, service_id, service_date, service_description, service.workplan_id)
                if not success:
                    failed_components.append({"name": component_name, "error": message})
                    logging.error(f"Failed to process completed service {service_id}: {message}")
                    continue

                successful_components.append(component_name)
                if service.incident_id and service.incident_id not in touched_incident_ids:
                    touched_incident_ids.append(service.incident_id)

            incident_hints = []
            for incident_id in touched_incident_ids:
                incident = database_manager.read_single_incident_report(incident_id)
                if not incident or incident.incident_status != "Open":
                    continue
                remaining_planned = [service for service in database_manager.read_services_by_incident(incident_id)
                                     if service.status == "Planned"]
                if not remaining_planned:
                    incident_hints.append(f"Incident from {incident.incident_date.split(' ')[0]} has no remaining planned services and can be closed")

            message = self.build_bulk_service_message("completed", successful_components, failed_components, incident_hints)
            return message["type"] == "success", message

        except Exception as error:
            logging.error(f"Error completing services: {str(error)}")
            return False, f"Error completing services: {str(error)}"
```

Note: `process_service_records` builds `current_service_data` without `status`, `incident_id`, `planned_date` and writes it through `write_service_record`, which does an `update(**service_data)` of only the given keys. So the fields written before the call survive. This is why it needs no change.

- [ ] **Step 5: Rewrite `update_service_record` and extract the recalculation**

Replace `update_service_record` (the method that follows `create_planned_services` after your edit) with:

```python
    def update_service_record(self,
                              component_id,
                              service_id,
                              service_date,
                              service_description,
                              workplan_id=None,
                              status="Completed",
                              incident_id=None,
                              planned_date=None):
        """Method to update a service record, including status changes in both directions"""
        try:
            workplan_id = workplan_id if workplan_id and workplan_id.strip() else None
            incident_id = incident_id if incident_id and incident_id.strip() else None
            planned_date = planned_date if planned_date and planned_date.strip() else None
            service_description = service_description if service_description and service_description.strip() else None

            current_service = database_manager.read_single_service_record(service_id)
            if not current_service:
                logging.warning(f"Service record not found: {service_id}")
                return False, f"Service record not found: {service_id}"

            if status == "Planned":
                success, message = self.validate_service_record("plan service", component_id, service_id, None)
                if not success:
                    logging.error(f"Validation of service record failed: {message}")
                    return success, message

                if planned_date:
                    success, message = validate_date_format(planned_date)
                    if not success:
                        logging.warning(message)
                        return False, message

                service_data = {"service_id": service_id,
                                "component_id": component_id,
                                "component_name": current_service.component_name,
                                "service_date": None,
                                "description": service_description,
                                'bike_id': None,
                                'distance_marker': None,
                                'workplan_id': workplan_id,
                                'status': "Planned",
                                'incident_id': incident_id,
                                'planned_date': planned_date}

                success, message = database_manager.write_service_record(service_data)
                if not success:
                    logging.error(f"Error updating service record: {message}")
                    return success, message

                if current_service.status == "Completed":
                    success, message = self.recalculate_component_after_service_removal(component_id)
                    if not success:
                        return success, message

                logging.info(f"Update of service record successful: {message}")
                return success, message

            validation_mode = "complete service" if current_service.status == "Planned" else "edit service"
            success, message = self.validate_service_record(validation_mode, component_id, service_id, service_date)
            if not success:
                logging.error(f"Validation of service record failed: {message}")
                return success, message

            service_data = {"service_id": service_id,
                            "component_id": component_id,
                            "component_name": current_service.component_name,
                            'workplan_id': workplan_id,
                            'status': "Completed",
                            'incident_id': incident_id,
                            'planned_date': planned_date}

            success, message = database_manager.write_service_record(service_data)
            if not success:
                logging.error(f"Error updating service record: {message}")
                return success, message

            success, message = self.process_service_records(component_id, service_id, service_date, service_description, workplan_id)
            if not success:
                logging.error(f"Error processing service record: {message}")
                return success, message

            logging.info(f"Update of service record successful: {message}")
            return success, message

        except Exception as error:
            logging.error(f"An error occured updating service records for component with id {component_id}: {str(error)}")
            return False, f"Error updating service records for component with id {component_id}: {str(error)}"

    def recalculate_component_after_service_removal(self, component_id):
        """Method to recalculate a component after a completed service is deleted or reverted to planned"""
        component = database_manager.read_component(component_id)
        logging.debug(f"Recalculating service records for component {component.component_name} after removal of a completed service")

        service_records = database_manager.read_subset_service_history(component_id)
        if service_records:
            first_service = service_records.first()
            success, message = self.process_service_records(component_id,
                                                            first_service.service_id,
                                                            first_service.service_date,
                                                            first_service.description)
            if not success:
                logging.error(f"An error occured triggering update of service records for {component.component_name}: {message}")
                return False, f"An error occured triggering update of service records for {component.component_name}: {message}"

            return True, f"Recalculated service records for {component.component_name}"

        self.update_component_distance(component_id, component.component_distance - component.component_distance_offset)
        return True, f"No completed services left for {component.component_name}, distance reset"
```

Then in `delete_record`, replace the block `if table_selector == "Services":` ... through `self.update_component_distance(...)` (the services branch under `if success:`) with:

```python
            if table_selector == "Services":
                if deleted_service_status == "Completed":
                    success, message = self.recalculate_component_after_service_removal(component_id)
                    if not success:
                        return False, message, component_id, bike_id, collection_id
```

and at the top of `delete_record`, change the services lookup to remember the status:

```python
        if table_selector == "Services":
            deleted_service = database_manager.read_single_service_record(record_id)
            deleted_service_status = deleted_service.status
            component_id = deleted_service.component_id
            component = database_manager.read_component(component_id)
            bike_id = component.bike_id
```

Also in `delete_record`, the `Incidents` branch is new. Add before the `elif table_selector == "Workplans":` branch:

```python
        elif table_selector == "Incidents":
            for service in database_manager.read_services_by_incident(record_id):
                database_manager.write_service_record({"service_id": service.service_id,
                                                       "component_name": service.component_name,
                                                       "incident_id": None})
```

And the `Workplans` branch becomes:

```python
        elif table_selector == "Workplans":
            linked_services = database_manager.read_services_by_workplan(record_id)

            if linked_services:
                service_count = linked_services.count()
                logging.warning(f"Cannot delete workplan as it has linked services ({service_count})")
                return False, f"Cannot delete workplan as it has {service_count} linked service(s). Remove or move these services before deleting.", component_id, bike_id, collection_id
```

Note the `ComponentHistory` deletion branch at `delete_record` uses `read_subset_service_history` to block deleting the initial history record when services exist. That read now returns Completed only, so a component with only planned services can have its initial record deleted; the planned services then reference a component with no history, which is allowed since planned services have no date. Acceptable.

- [ ] **Step 6: Run the tests**

Run: `uv run pytest tests/ -v`
Expected: all PASS.

- [ ] **Step 7: Checkpoint**

Human reviews and commits: `Add planned services, completion and revert to business logic`.

---

### Task 6: Business logic, workplans, incidents and payloads

**Files:**
- Modify: `backend/business_logic.py`: `get_bike_details` (92-190), `get_component_overview` (188-246), `get_component_details` (246-416), `get_collection_details` (554-586), `get_incident_reports` (587-606), `process_workplans` (669-712), `get_workplan_details` (714-789), remove `workplan_check_component_services` and `workplan_get_linkable_incidents` (791-840), `create_incident_record` and `update_incident_record` (2674-2775), `create_workplan` and `update_workplan` (2777-2905), `create_history_record` (1505-1560) and its callers.

**Interfaces:**
- Produces:
  - `create_workplan(due_date, workplan_status, workplan_size, workplan_description, completion_date, completion_notes, source_incident_id=None)` -> `(success, message, workplan_id)`
  - `update_workplan(workplan_id, due_date=None, workplan_status=None, workplan_size=None, workplan_description=None, completion_date=None, completion_notes=None, close_linked_incidents=None, update_mode=None)`
  - `create_incident_record(...)` and `update_incident_record(...)` without `workplan_id`
  - `create_history_record(component_id, installation_status, component_bike_id, component_updated_date, notes=None)`
  - `quick_swap_orchestrator(old_component_id, fate, swap_date, new_component_id, new_component_data, notes=None)`
  - Payload keys added: `planned_services_data` (list of 11-tuples from `get_planned_service_data_tuple`) on bike details, component details, workplan details; `plan_services_preselect` (list of component ids) on bike, collection, component details; `latest_service_date` on workplan details; `open_incidents_for_component` on component details (list of `(incident_id, incident_title)`).
  - Payload keys removed: `linkable_incidents_data`, `workplan_components_info`, `all_components_serviced` (replaced by `all_services_completed`).

- [ ] **Step 1: Incidents**

In `create_incident_record` remove the `workplan_id=None` parameter, the `workplan_id = ...` line and the `"workplan_id": workplan_id` dict entry. In `update_incident_record` remove the `workplan_id=None` parameter, the `workplan_id = ...` line, the `if workplan_id is not None:` partial block and the `"workplan_id": workplan_id` dict entry.

- [ ] **Step 2: Workplans**

Replace `create_workplan` with:

```python
    def create_workplan(self,
                        due_date,
                        workplan_status,
                        workplan_size,
                        workplan_description,
                        completion_date,
                        completion_notes,
                        source_incident_id=None):
        """Method to add workplan, optionally with planned services from a source incident"""
        try:
            workplan_id = generate_unique_id()

            workplan_description = workplan_description if workplan_description else None
            completion_date = completion_date if completion_date else None
            completion_notes = completion_notes if completion_notes else None
            source_incident_id = source_incident_id if source_incident_id and source_incident_id.strip() else None

            workplan_data = {"workplan_id": workplan_id,
                             "due_date": due_date,
                             "workplan_status": workplan_status,
                             "workplan_size": workplan_size,
                             "workplan_description": workplan_description,
                             "completion_date": completion_date,
                             "completion_notes": completion_notes}

            success, message = database_manager.write_workplan(workplan_data)

            if not success:
                logging.error(f"Creation of workplan failed: {message}")
                return success, message, None

            logging.info(f"Creation of workplan successful: {message}")

            if source_incident_id:
                incident = database_manager.read_single_incident_report(source_incident_id)
                incident_component_ids = parse_json_string(incident.incident_affected_component_ids) if incident else None
                if incident_component_ids:
                    planned_description = incident.incident_description if incident.incident_description else "Planned service from incident"
                    planned_success, planned_message = self.create_planned_services(incident_component_ids,
                                                                                    planned_description,
                                                                                    workplan_id=workplan_id,
                                                                                    incident_id=source_incident_id)
                    if planned_success:
                        message += f" and planned {planned_message['success_count']} service(s) from incident"
                    else:
                        logging.warning(f"Workplan {workplan_id} created but planned services from incident {source_incident_id} failed: {planned_message}")
                        message += ". Planned services from incident could not all be created, see planned services on the workplan"
                else:
                    message += ". Incident has no components, so no services were planned"

            return success, message, workplan_id

        except Exception as error:
            logging.error(f"Error creating workplan with id {workplan_id}: {str(error)}")
            return False, f"Error creating workplan with id {workplan_id}: {str(error)}", None
```

Replace `update_workplan` with:

```python
    def update_workplan(self,
                        workplan_id,
                        due_date=None,
                        workplan_status=None,
                        workplan_size=None,
                        workplan_description=None,
                        completion_date=None,
                        completion_notes=None,
                        close_linked_incidents=None,
                        update_mode=None):
        """Method to update workplan (supports full or partial updates)"""
        try:
            close_linked_incidents = close_linked_incidents == "on"
            completion_date = completion_date if completion_date else None
            completion_notes = completion_notes if completion_notes else None

            if workplan_status == "Done":
                success, message = self.validate_workplan_completion(workplan_id, completion_date)
                if not success:
                    logging.warning(f"Workplan {workplan_id} cannot be completed: {message}")
                    return False, message

            if update_mode == "partial":
                workplan_data = {"workplan_id": workplan_id,
                                 "workplan_status": workplan_status,
                                 "completion_date": completion_date,
                                 "completion_notes": completion_notes}

            else:
                workplan_description = workplan_description if workplan_description else None

                workplan_data = {"workplan_id": workplan_id,
                                 "due_date": due_date,
                                 "workplan_status": workplan_status,
                                 "workplan_size": workplan_size,
                                 "workplan_description": workplan_description,
                                 "completion_date": completion_date,
                                 "completion_notes": completion_notes}

            success, message = database_manager.write_workplan(workplan_data)

            if success and workplan_status == "Done" and close_linked_incidents and completion_date:
                workplan = database_manager.read_single_workplan(workplan_id)
                workplan_description_transfer = workplan.workplan_description if workplan and workplan.workplan_description else "No description provided"
                incidents_resolution_notes_auto = f"Closed from workplan with description: {workplan_description_transfer} (workplan id: {workplan_id})"

                linked_incidents = database_manager.read_incidents_by_workplan(workplan_id)

                incidents_closed = 0
                for incident in linked_incidents:
                    if incident.incident_status == "Open":
                        incident_success, incident_message = self.update_incident_record(incident_id=incident.incident_id,
                                                                                         incident_status="Resolved",
                                                                                         resolution_date=completion_date,
                                                                                         resolution_notes=incidents_resolution_notes_auto,
                                                                                         update_mode="partial")

                        if incident_success:
                            incidents_closed += 1
                        else:
                            logging.warning(f"Failed to close incident {incident.incident_id}: {incident_message}")

                if incidents_closed > 0:
                    logging.info(f"Closed {incidents_closed} linked incidents for workplan {workplan_id}")
                    message += f" and closed {incidents_closed} linked incident(s)"

            if success:
                logging.info(f"Update of workplan successful: {message}")
            else:
                logging.error(f"Update of workplan failed: {message}")

            return success, message

        except Exception as error:
            logging.error(f"Error updating workplan with id {workplan_id}: {str(error)}")
            return False, f"Error updating workplan with id {workplan_id}: {str(error)}"

    def validate_workplan_completion(self, workplan_id, completion_date):
        """Method to validate that a workplan can be set to Done"""
        planned_services = list(database_manager.read_planned_services_by_workplan(workplan_id))
        if planned_services:
            return False, f"Workplan cannot be completed while {len(planned_services)} planned service(s) remain. Complete or remove them first"

        success, message = validate_date_format(completion_date)
        if not success:
            return False, message

        if completion_date > datetime.now().strftime("%Y-%m-%d %H:%M"):
            return False, "Completion date cannot be in the future"

        latest_service_date = None
        for service in database_manager.read_services_by_workplan(workplan_id):
            if service.service_date and (latest_service_date is None or service.service_date > latest_service_date):
                latest_service_date = service.service_date

        if latest_service_date and completion_date < latest_service_date:
            return False, f"Completion date cannot be before the latest service in this workplan ({latest_service_date})"

        return True, "Workplan can be completed"
```

Replace `process_workplans` (669-712) with:

```python
    def process_workplans(self, workplans):
        """Method to build dictionaries of bike and component ids referenced by planned services in received workplans"""
        bike_workplans = {}
        component_workplans = {}

        if workplans:
            for workplan in workplans:
                workplan_id = workplan.workplan_id

                for service in database_manager.read_services_by_workplan(workplan_id):
                    component_id = service.component_id

                    if component_id not in component_workplans:
                        component_workplans[component_id] = {"workplan_count": 0, "workplan_ids": []}

                    if workplan_id not in component_workplans[component_id]["workplan_ids"]:
                        component_workplans[component_id]["workplan_count"] += 1
                        component_workplans[component_id]["workplan_ids"].append(workplan_id)

                    component = database_manager.read_component(component_id)
                    if component and component.installation_status != "Not installed" and component.bike_id:
                        bike_id = component.bike_id

                        if bike_id not in bike_workplans:
                            bike_workplans[bike_id] = {"workplan_count": 0,
                                                       "workplan_ids": []}

                        if workplan_id not in bike_workplans[bike_id]["workplan_ids"]:
                            bike_workplans[bike_id]["workplan_count"] += 1
                            bike_workplans[bike_id]["workplan_ids"].append(workplan_id)

        return {"bike_workplans": bike_workplans,
                "component_workplans": component_workplans}
```

- [ ] **Step 3: Workplan details payload**

Replace `get_workplan_details`, `workplan_check_component_services` and `workplan_get_linkable_incidents` (714-840) with:

```python
    def get_workplan_details(self, workplan_id):
        """Method to produce payload for workplan details page"""
        bikes = database_manager.read_bikes()
        bikes_data = get_formatted_bikes_list(bikes)
        all_components_data = database_manager.read_all_components()

        workplan = database_manager.read_single_workplan(workplan_id)
        services = list(database_manager.read_services_by_workplan(workplan_id))
        context = derive_workplan_context(services, database_manager)

        workplan_data = {"workplan_id": workplan.workplan_id,
                         "workplan_name": generate_workplan_title(context["component_names"],
                                                                  context["bike_names"][0] if context["bike_names"] else None,
                                                                  workplan.workplan_description),
                         "due_date": workplan.due_date,
                         "workplan_status": workplan.workplan_status,
                         "workplan_size": workplan.workplan_size,
                         "component_ids": context["component_ids"],
                         "component_names": context["component_names"],
                         "bike_ids": context["bike_ids"],
                         "bike_names": context["bike_names"],
                         "completed_count": context["completed_count"],
                         "total_count": context["total_count"],
                         "description": workplan.workplan_description,
                         "description_display": strip_markdown_syntax(workplan.workplan_description) if workplan.workplan_description else None,
                         "completion_date": workplan.completion_date,
                         "completion_notes": workplan.completion_notes,
                         "elapsed_days": calculate_elapsed_days(workplan.due_date,
                                                                workplan.completion_date if workplan.completion_date else get_formatted_datetime_now())[1],
                         "checkbox_progress": parse_checkbox_progress(workplan.workplan_description)}

        all_services_completed = context["total_count"] > 0 and context["completed_count"] == context["total_count"]

        latest_service_date = None
        for service in services:
            if service.service_date and (latest_service_date is None or service.service_date > latest_service_date):
                latest_service_date = service.service_date

        workplan_names = get_workplan_names_dict(database_manager)

        incidents = database_manager.read_incidents_by_workplan(workplan_id)
        incidents_data = [get_incident_data_tuple(incident, database_manager, workplan_names)
                         for incident in incidents]

        services_data = []
        planned_services_data = []
        for service in services:
            component = database_manager.read_component(service.component_id)
            if service.status == "Planned":
                planned_services_data.append(get_planned_service_data_tuple(service, database_manager, workplan_names))
            else:
                services_data.append((service.service_id,
                                      service.service_date,
                                      service.description,
                                      service.component_id,
                                      component.component_name if component else "Deleted component",
                                      service.workplan_id,
                                      service.incident_id,
                                      service.planned_date,
                                      component.installation_status if component else "Deleted"))

        workplans_data = [get_workplan_data_tuple(workplan, database_manager)
                          for workplan in database_manager.read_all_workplans()]

        payload = {"workplan_data": workplan_data,
                   "all_services_completed": all_services_completed,
                   "latest_service_date": latest_service_date,
                   "incidents_data": incidents_data if incidents_data else None,
                   "services_data": services_data if services_data else None,
                   "planned_services_data": planned_services_data if planned_services_data else None,
                   "bikes_data": bikes_data,
                   "all_components_data": all_components_data,
                   "workplans_data": workplans_data}

        return payload
```

Add `derive_workplan_context`, `get_planned_service_data_tuple` to the `from utils import (...)` list at the top of `business_logic.py`.

- [ ] **Step 4: Bike, collection, component payloads**

In `get_bike_details`, after `workplans_data = [...]`, add:

```python
        planned_services_data = [get_planned_service_data_tuple(service, database_manager, workplan_names)
                                 for service in database_manager.read_planned_services_by_bike(bike_id)]

        plan_services_preselect = [component.component_id for component in bike_components
                                   if component.installation_status == "Installed"]
```

and add to the payload dict:

```python
                   "planned_services_data": planned_services_data if planned_services_data else None,
                   "plan_services_preselect": plan_services_preselect,
```

In `get_collection_details`, after `warnings = ...`, add:

```python
        overview_payload['plan_services_preselect'] = [component[0] for component in filtered_components
                                                       if component[4] != "Retired"]
```

In `get_component_details`, replace the `service_history = ...` block's loop source so it stays on completed services (it already calls `read_subset_service_history`, unchanged), and extend the tuple appended to `enhanced_service_data` with two trailing fields:

```python
                                              service_record.workplan_id,
                                              service_record.incident_id,
                                              service_record.planned_date))
```

After `workplans_data = [...]` in `get_component_details`, add:

```python
        planned_services_data = [get_planned_service_data_tuple(service, database_manager, workplan_names)
                                 for service in database_manager.read_planned_services_by_component(component_id)]

        open_incidents_for_component = [(incident[0], incident[12]) for incident in incident_reports_data
                                        if incident[4] and component_id in incident[4]]

        plan_services_preselect = [component_id] if bike_component.installation_status != "Retired" else []
```

and add to the payload (`oldest_history_record` is already computed near the top of the method):

```python
                   "planned_services_data": planned_services_data if planned_services_data else None,
                   "open_incidents_for_component": open_incidents_for_component,
                   "plan_services_preselect": plan_services_preselect,
                   "oldest_history_date": oldest_history_record.updated_date if oldest_history_record else None,
```

`get_component_overview` and `get_incident_reports` need no change beyond what the utils tuples already do.

- [ ] **Step 5: History notes (#349)**

Change `create_history_record` signature to:

```python
    def create_history_record(self,
                              component_id,
                              installation_status,
                              component_bike_id,
                              component_updated_date,
                              notes=None):
```

and inside, after `component = database_manager.read_component(component_id)`, add `notes = notes if notes and notes.strip() else None`, and add `"notes": notes` to `history_data`.

Change `quick_swap_orchestrator` signature to add `notes=None` as the last parameter and pass `notes=notes` in both `self.create_history_record(...)` calls inside it (lines 1857 and 1873). The other two callers (1379 in `create_component`, 2077 in the collection bulk status change) stay as they are, which leaves `notes` as None.

In `get_component_details`, extend the `component_history_data` tuple with `installation_record.notes` as the last field (so it has 8 fields).

- [ ] **Step 6: Run tests and a smoke import**

Run: `uv run pytest tests/ -v`. Expected: PASS.

Write a quick test appended to `tests/test_service_status.py`:

```python
def test_workplan_completion_blocked_by_planned_services(modules):
    seed_component(modules)
    bl = modules.business_logic
    success, message, workplan_id = bl.create_workplan("2026-03-01 10:00", "Planned", "Small", "Spring", None, None)
    assert success
    assert bl.create_planned_services(["comp-1"], "Wax chain", workplan_id=workplan_id)[0]

    success, message = bl.update_workplan(workplan_id, workplan_status="Done", completion_date="2026-03-02 10:00", update_mode="partial")
    assert not success and "planned service" in message

    planned_id = list(modules.database_manager.read_planned_services_by_workplan(workplan_id))[0].service_id
    assert bl.complete_services([planned_id], "2026-03-05 10:00")[0]

    success, message = bl.update_workplan(workplan_id, workplan_status="Done", completion_date="2026-03-04 10:00", update_mode="partial")
    assert not success and "latest service" in message

    success, message = bl.update_workplan(workplan_id, workplan_status="Done", completion_date="2026-03-05 12:00", update_mode="partial")
    assert success, message
```

Run again. Expected: PASS.

- [ ] **Step 7: Checkpoint**

Human reviews and commits: `Derive workplan and incident payloads from services, add history notes`.

---

### Task 7: Routes

**Files:**
- Modify: `backend/main.py:282-334` (`add_history_record`), `:334-380` (`quick_swap`), `:439-620` (service, incident, workplan routes)

- [ ] **Step 1: Service routes**

Replace `add_service`, `bulk_add_service_records` and `update_service_record` with:

```python
@app.post("/add_service_record", response_class=HTMLResponse)
async def add_service(component_id: str = Form(...),
                      service_date: Optional[str] = Form(None),
                      service_description: str = Form(...),
                      workplan_id: Optional[str] = Form(None),
                      status: Optional[str] = Form("Completed"),
                      incident_id: Optional[str] = Form(None),
                      planned_date: Optional[str] = Form(None)):
    """Endpoint to add service, planned or completed"""

    success, message = business_logic.create_service_record(component_id,
                                                            service_date,
                                                            service_description,
                                                            workplan_id,
                                                            status,
                                                            incident_id,
                                                            planned_date)

    redirect_url = f"/component_details/{component_id}"

    response = RedirectResponse(
        url=f"{redirect_url}?success={success}&message={message}",
        status_code=303)

    return response

@app.post("/add_planned_services")
async def add_planned_services(component_ids: List[str] = Form(...),
                               service_description: str = Form(...),
                               workplan_id: Optional[str] = Form(None),
                               incident_id: Optional[str] = Form(None),
                               planned_date: Optional[str] = Form(None)):
    """Endpoint to add planned services for one or more components"""

    success, message = business_logic.create_planned_services(component_ids=component_ids,
                                                              service_description=service_description,
                                                              workplan_id=workplan_id,
                                                              incident_id=incident_id,
                                                              planned_date=planned_date)

    return JSONResponse({"success": success, "message": message})

@app.post("/complete_services")
async def complete_services(service_ids: List[str] = Form(...),
                            service_date: str = Form(...),
                            completion_note: Optional[str] = Form(None)):
    """Endpoint to complete one or more planned services"""

    success, message = business_logic.complete_services(service_ids=service_ids,
                                                        service_date=service_date,
                                                        completion_note=completion_note)

    return JSONResponse({"success": success, "message": message})

@app.post("/update_service_record", response_class=HTMLResponse)
async def update_service_record(component_id: str = Form(...),
                                service_id: str = Form(...),
                                service_date: Optional[str] = Form(None),
                                service_description: str = Form(...),
                                workplan_id: Optional[str] = Form(None),
                                status: Optional[str] = Form("Completed"),
                                incident_id: Optional[str] = Form(None),
                                planned_date: Optional[str] = Form(None),
                                redirect_url: Optional[str] = Form(None)):
    """Endpoint to update an existing service record"""

    success, message = business_logic.update_service_record(component_id,
                                                            service_id,
                                                            service_date,
                                                            service_description,
                                                            workplan_id,
                                                            status,
                                                            incident_id,
                                                            planned_date)

    if not redirect_url or not redirect_url.strip():
        redirect_url = f"/component_details/{component_id}"

    response = RedirectResponse(
        url=f"{redirect_url}?success={success}&message={message}",
        status_code=303)

    return response
```

- [ ] **Step 2: Incident routes**

In `add_incident_record` and `update_incident_record` remove the `workplan_id: Optional[str] = Form(None)` parameter and the `workplan_id` argument in the business logic call. In `add_incident_record` replace the redirect block with `redirect_url = "/incident_reports"`.

- [ ] **Step 3: Workplan routes**

In `add_workplan` and `update_workplan` remove `workplan_affected_component_ids` and `workplan_affected_bike_id` parameters and arguments. In `update_workplan`, the redirect stays as it is. Because a failed completion must not lose the user's place, verify the existing redirect after the call goes to `/workplan_details/{workplan_id}` (it does today).

- [ ] **Step 4: History notes routes**

In `add_history_record` add `notes: Optional[str] = Form(None)` and pass `notes` as the last argument to `create_history_record`. In `quick_swap` add `notes: Optional[str] = Form(None)` and pass `notes=notes` to both `quick_swap_orchestrator` calls.

- [ ] **Step 5: Boot check**

From `backend/` with a real `config.json` present: `uv run uvicorn main:app --log-config uvicorn_log_config.ini`. Expected: server starts, `GET /workplans` returns 200 (templates are updated in later tasks; if a template errors, that is expected until Task 9 onward). Stop the server.

- [ ] **Step 6: Checkpoint**

Human reviews and commits: `Update routes for planned and completed services`.

---

### Task 8: Plan and complete services modals and shared JS

**Files:**
- Create: `frontend/templates/modal_plan_services.html`, `frontend/templates/modal_complete_services.html`
- Delete: `frontend/templates/modal_create_services_workplan.html`, `frontend/templates/modal_link_incident.html`
- Modify: `frontend/static/js/main.js` (new L2 subsection after `// ----- Global helper function to forcefully close loading modal -----` block ending at line 1140; delete the two IIFEs "Function to handle bulk service creation for workplan" at 5719-5919 and "Function to handle linking incidents to workplan" at 5989-6069)

**Interfaces:**
- Produces: `window.submitBulkServiceAction(url, formData, loadingText, titles)` and `window.formatBulkServiceMessage(messageData)`. Trigger buttons for the plan modal carry `data-bs-target="#planServicesModal"`, `data-preselect='["id", ...]'`, `data-workplan-id`, `data-incident-id`, `data-lock-workplan` ("true" locks the dropdown to the given workplan). Trigger buttons for the complete modal carry `data-bs-target="#completeServicesModal"`, `data-planned-services='[[service_id, component_name, description, oldest_history_date, installation_status, workplan_completion_date], ...]'`.

- [ ] **Step 1: Plan services modal**

Create `frontend/templates/modal_plan_services.html`:

```html
<div class="modal fade" id="planServicesModal" tabindex="-1" aria-labelledby="planServicesModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered modal-lg">
        <div class="modal-content">
            <div class="modal-header input-modal-header">
                <h5 class="modal-title input-modal-title" id="planServicesModalLabel">Plan services</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
                <div id="planServicesMultipleBanner" class="alert alert-warning d-none">
                    <strong>Multiple components selected</strong><br>
                    The same description, planned date, workplan and incident will be set for all selected components.
                </div>
                <input type="hidden" id="planServicesIncidentId" value="">

                <div class="mb-3">
                    <label for="planServicesDescription" class="form-label fw-bold">Description</label>
                    <textarea class="form-control" id="planServicesDescription" rows="2" required minlength="5" placeholder="e.g., Replace chain, Bleed brakes"></textarea>
                </div>

                <div class="mb-3">
                    <label for="planServicesComponents" class="form-label fw-bold">Components</label>
                    <select class="form-select" id="planServicesComponents" multiple placeholder="Search to add components...">
                        {% for component_id, type, name, distance, status, lifetime_status, service_status, bike, cost, lifetime_remaining, lifetime_remaining_days, service_next, service_next_days, threshold_km, threshold_days, bike_id, updated_date in payload.all_components_data %}
                            {% if status != "Retired" %}
                            <option value="{{ component_id }}">{{ name }} ({{ type }}) - {{ bike }}</option>
                            {% endif %}
                        {% endfor %}
                    </select>
                    <small class="form-text text-muted">Retired components cannot be serviced and are not listed.</small>
                </div>

                <div class="mb-3">
                    <label for="planServicesPlannedDate" class="form-label fw-bold">Planned date (optional)</label>
                    <div class="input-group date-input-group">
                        <input type="text" class="form-control datepicker-input" id="planServicesPlannedDate">
                        <span class="input-group-text datepicker-toggle">🗓</span>
                    </div>
                    <small class="form-text text-muted">Leave blank to use the due date of the workplan.</small>
                </div>

                <div class="mb-3">
                    <label for="planServicesWorkplanId" class="form-label fw-bold">Workplan</label>
                    <select class="form-select" id="planServicesWorkplanId">
                        <option value="">No workplan</option>
                        {% for workplan_id, due_date, workplan_status, workplan_size, component_ids, component_names, bike_ids, bike_names, workplan_description, completion_date, completion_notes, elapsed_days, workplan_title, service_progress in payload.workplans_data %}
                            {% if workplan_status == "Planned" %}
                            <option value="{{ workplan_id }}">{{ workplan_title }}</option>
                            {% endif %}
                        {% endfor %}
                    </select>
                </div>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                <button type="button" class="btn btn-primary" id="planServicesSubmitBtn">Plan services</button>
            </div>
        </div>
    </div>
</div>
```

Every page including this modal must provide `payload.all_components_data` and `payload.workplans_data`. Bike, collection, component, incident and workplan pages already do (collection through `get_component_overview`).

- [ ] **Step 2: Complete services modal**

Create `frontend/templates/modal_complete_services.html`:

```html
<div class="modal fade" id="completeServicesModal" tabindex="-1" aria-labelledby="completeServicesModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered modal-lg">
        <div class="modal-content">
            <div class="modal-header input-modal-header">
                <h5 class="modal-title input-modal-title" id="completeServicesModalLabel">Complete services</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
                <div class="mb-3">
                    <label for="completeServicesDate" class="form-label fw-bold">Service date</label>
                    <div class="input-group date-input-group">
                        <input type="text" class="form-control datepicker-input" id="completeServicesDate" required>
                        <span class="input-group-text datepicker-toggle">🗓</span>
                    </div>
                </div>

                <div class="mb-3">
                    <label for="completeServicesNote" class="form-label fw-bold">Note (optional)</label>
                    <textarea class="form-control" id="completeServicesNote" rows="2" placeholder="Added to the description of each selected service"></textarea>
                </div>

                <div class="mb-3">
                    <label class="form-label fw-bold">Planned services to complete</label>
                    <div id="completeServicesCheckboxes" class="border rounded p-3 scrollable-checkboxes">
                        <!-- Checkboxes inserted by main.js -->
                    </div>
                    <small class="form-text text-muted">Descriptions are kept as planned. Services on retired components cannot be completed.</small>
                </div>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                <button type="button" class="btn btn-success" id="completeServicesSubmitBtn">Complete services</button>
            </div>
        </div>
    </div>
</div>
```

- [ ] **Step 3: Delete the two old modals**

```bash
git rm frontend/templates/modal_create_services_workplan.html frontend/templates/modal_link_incident.html
```

(Staging the deletion is fine; the commit is the human's.)

- [ ] **Step 4: Remove the old JS blocks**

In `frontend/static/js/main.js` delete the IIFE that begins with `// Function to handle bulk service creation for workplan` (starts at line 5719, ends with `})();` before `// Function to handle completing workplan from workplan_details page`) and the IIFE that begins with `// Function to handle linking incidents to workplan` (starts at 5989, ends at the `})();` before the `// ====` header of Component types page functions).

- [ ] **Step 5: Add the shared subsection**

Insert after the block ending at line 1140 (the `forceCloseLoadingModal` helper) and before `// Function to initialize collection features`:

```javascript
// ----- Plan and complete services modals -----
// Used on workplan details, incident reports, bike details, collection details and component details pages

// Function to format the report dict returned by /add_planned_services and /complete_services
window.formatBulkServiceMessage = function(messageData) {
    if (typeof messageData === 'string') {
        return messageData;
    }

    let html = `<strong>${messageData.summary}</strong><br><br>`;

    if (messageData.successful_components.length > 0) {
        html += '<strong>Done for:</strong><br>';
        html += messageData.successful_components.map(name => `• ${name}`).join('<br>');
        html += '<br><br>';
    }

    if (messageData.failed_components.length > 0) {
        html += '<strong>Failed for:</strong><br>';
        html += messageData.failed_components.map(failed => `• ${failed.name}: ${failed.error}`).join('<br>');
        html += '<br><br>';
    }

    if (messageData.incident_hints && messageData.incident_hints.length > 0) {
        html += '<strong>Incidents:</strong><br>';
        html += messageData.incident_hints.map(hint => `• ${hint}`).join('<br>');
    }

    return html;
};

// Function to post a bulk service action and report the result, then reload the page
window.submitBulkServiceAction = function(url, formData, loadingText, titles) {
    document.getElementById('loadingMessage').textContent = loadingText;

    setTimeout(() => {
        loadingModal.show();

        fetch(url, {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            forceCloseLoadingModal();

            setTimeout(() => {
                const isPartialFailure = data.message && data.message.type === 'partial_failure';
                const title = data.success ? titles.success : isPartialFailure ? titles.partial : titles.failure;
                const formattedMessage = formatBulkServiceMessage(data.message);

                showReportModal(title, formattedMessage, data.success, isPartialFailure, function() {
                    const pageUrl = window.location.pathname;
                    window.history.replaceState({}, document.title, pageUrl);
                    window.location.reload();
                });
            }, 500);
        })
        .catch(error => {
            console.error('Bulk service action error:', error);
            forceCloseLoadingModal();

            setTimeout(() => {
                showReportModal('❌ Application error', 'An error occurred. Give it another go.', false, false, function() {
                    const pageUrl = window.location.pathname;
                    window.history.replaceState({}, document.title, pageUrl);
                    window.location.reload();
                });
            }, 400);
        });
    }, 300);
};

// Function to show the validation modal from the services modals
function showServicesValidationModal(message) {
    const validationModalElement = document.getElementById('validationModal');
    const modalInstance = bootstrap.Modal.getInstance(validationModalElement) || new bootstrap.Modal(validationModalElement);
    document.getElementById('validationModalLabel').textContent = 'Validation error';
    document.getElementById('validationModalBody').textContent = message;
    modalInstance.show();
}

// Plan services modal
(function() {
    if (!document.getElementById('planServicesModal')) {
        return;
    }

    document.addEventListener('DOMContentLoaded', function() {
        const planServicesModal = document.getElementById('planServicesModal');
        const componentSelect = document.getElementById('planServicesComponents');
        const workplanSelect = document.getElementById('planServicesWorkplanId');
        const multipleBanner = document.getElementById('planServicesMultipleBanner');

        function updateMultipleBanner() {
            const selectedCount = componentSelect.tomSelect ? componentSelect.tomSelect.getValue().length : 0;
            if (selectedCount > 1) {
                multipleBanner.classList.remove('d-none');
            } else {
                multipleBanner.classList.add('d-none');
            }
        }

        planServicesModal.addEventListener('shown.bs.modal', function(event) {
            const button = event.relatedTarget;
            const preselect = JSON.parse(button.dataset.preselect || '[]');
            const workplanId = button.dataset.workplanId || '';
            const incidentId = button.dataset.incidentId || '';
            const lockWorkplan = button.dataset.lockWorkplan === 'true';

            initializeDatePickers(planServicesModal);

            if (!componentSelect.tomSelect) {
                const ts = new TomSelect(componentSelect, {plugins: ['remove_button'], maxItems: null});
                componentSelect.tomSelect = ts;
                ts.on('change', updateMultipleBanner);
            }

            componentSelect.tomSelect.clear();
            componentSelect.tomSelect.setValue(preselect);
            updateMultipleBanner();

            document.getElementById('planServicesDescription').value = '';
            document.getElementById('planServicesPlannedDate').value = '';
            document.getElementById('planServicesIncidentId').value = incidentId;

            workplanSelect.value = workplanId;
            workplanSelect.disabled = lockWorkplan;
        });

        document.getElementById('planServicesSubmitBtn').addEventListener('click', function() {
            const serviceDescription = document.getElementById('planServicesDescription').value;
            const plannedDate = document.getElementById('planServicesPlannedDate').value;
            const selectedComponents = componentSelect.tomSelect ? componentSelect.tomSelect.getValue() : [];

            if (!serviceDescription || serviceDescription.trim().length < 5) {
                showServicesValidationModal('Please enter a description (minimum 5 characters).');
                return;
            }

            if (selectedComponents.length === 0) {
                showServicesValidationModal('Please select at least one component.');
                return;
            }

            if (plannedDate && !validateDateInput(document.getElementById('planServicesPlannedDate'))) {
                showServicesValidationModal('Please enter a valid planned date in format YYYY-MM-DD HH:MM, or leave it blank.');
                return;
            }

            const modalInstance = bootstrap.Modal.getInstance(planServicesModal);
            if (modalInstance) {
                modalInstance.hide();
            }

            const formData = new FormData();
            formData.append('service_description', serviceDescription);
            formData.append('planned_date', plannedDate);
            formData.append('workplan_id', workplanSelect.value);
            formData.append('incident_id', document.getElementById('planServicesIncidentId').value);
            selectedComponents.forEach(componentId => {
                formData.append('component_ids', componentId);
            });

            submitBulkServiceAction('/add_planned_services', formData, 'Planning services...', {
                success: '✅ Services planned',
                partial: '⚠️ Services partially planned',
                failure: '❌ Planning services failed'
            });
        });
    });
})();

// Complete services modal
(function() {
    if (!document.getElementById('completeServicesModal')) {
        return;
    }

    document.addEventListener('DOMContentLoaded', function() {
        const completeServicesModal = document.getElementById('completeServicesModal');
        const checkboxContainer = document.getElementById('completeServicesCheckboxes');

        completeServicesModal.addEventListener('shown.bs.modal', function(event) {
            const button = event.relatedTarget;
            const plannedServices = JSON.parse(button.dataset.plannedServices || '[]');

            initializeDatePickers(completeServicesModal);

            const now = new Date();
            const formattedDate = now.getFullYear() + '-' +
                String(now.getMonth() + 1).padStart(2, '0') + '-' +
                String(now.getDate()).padStart(2, '0') + ' ' +
                String(now.getHours()).padStart(2, '0') + ':' +
                String(now.getMinutes()).padStart(2, '0');
            document.getElementById('completeServicesDate').value = formattedDate;
            document.getElementById('completeServicesNote').value = '';

            checkboxContainer.innerHTML = '';

            if (plannedServices.length === 0) {
                checkboxContainer.innerHTML = '<p class="text-muted">No planned services</p>';
                return;
            }

            plannedServices.forEach(([serviceId, componentName, description, oldestHistoryDate, installationStatus, workplanCompletionDate]) => {
                const isRetired = installationStatus === 'Retired';
                const label = isRetired ? `${componentName}: ${description} (retired, cannot be completed)` : `${componentName}: ${description}`;
                const checkboxHtml = `
                    <div class="form-check mb-2">
                        <input class="form-check-input complete-service-checkbox" type="checkbox"
                               value="${serviceId}" id="complete_service_${serviceId}"
                               data-oldest-history-date="${oldestHistoryDate || ''}"
                               data-workplan-completion-date="${workplanCompletionDate || ''}"
                               data-component-name="${componentName}"
                               ${isRetired ? 'disabled' : 'checked'}>
                        <label class="form-check-label" for="complete_service_${serviceId}">${label}</label>
                    </div>
                `;
                checkboxContainer.insertAdjacentHTML('beforeend', checkboxHtml);
            });
        });

        document.getElementById('completeServicesSubmitBtn').addEventListener('click', function() {
            const dateInput = document.getElementById('completeServicesDate');
            const serviceDate = dateInput.value;
            const completionNote = document.getElementById('completeServicesNote').value;
            const selectedCheckboxes = Array.from(document.querySelectorAll('.complete-service-checkbox:checked'));

            if (!serviceDate || !validateDateInput(dateInput)) {
                showServicesValidationModal('Please enter a valid service date in format YYYY-MM-DD HH:MM.');
                return;
            }

            if (new Date(serviceDate) > new Date()) {
                showServicesValidationModal('Service date cannot be in the future.');
                return;
            }

            if (selectedCheckboxes.length === 0) {
                showServicesValidationModal('Please select at least one service.');
                return;
            }

            for (const checkbox of selectedCheckboxes) {
                const oldestHistoryDate = checkbox.dataset.oldestHistoryDate;
                const workplanCompletionDate = checkbox.dataset.workplanCompletionDate;
                if (oldestHistoryDate && serviceDate <= oldestHistoryDate) {
                    showServicesValidationModal(`Service date cannot be at or before the creation date of ${checkbox.dataset.componentName} (${oldestHistoryDate}).`);
                    return;
                }
                if (workplanCompletionDate && serviceDate > workplanCompletionDate) {
                    showServicesValidationModal(`Service date cannot be after the completion date of its workplan (${workplanCompletionDate}). Reopen the workplan first.`);
                    return;
                }
            }

            const modalInstance = bootstrap.Modal.getInstance(completeServicesModal);
            if (modalInstance) {
                modalInstance.hide();
            }

            const formData = new FormData();
            formData.append('service_date', serviceDate);
            formData.append('completion_note', completionNote);
            selectedCheckboxes.forEach(checkbox => {
                formData.append('service_ids', checkbox.value);
            });

            submitBulkServiceAction('/complete_services', formData, 'Completing services...', {
                success: '✅ Services completed',
                partial: '⚠️ Services partially completed',
                failure: '❌ Completing services failed'
            });
        });
    });
})();
```

Note: `loadingModal` is the module-level instance created at the top of main.js (line 11 area); `showReportModal` and `forceCloseLoadingModal` are globals already. `validateDateInput` is a global function at line 432.

- [ ] **Step 6: Syntax check**

Run: `node --check frontend/static/js/main.js` (if node is available) or load any page in the browser and confirm no console errors. Expected: clean.

- [ ] **Step 7: Checkpoint**

Human reviews and commits: `Add plan and complete services modals with shared handler`.

---

### Task 9: Workplan details page

**Files:**
- Modify: `frontend/templates/workplan_details.html` (whole file), `frontend/static/js/main.js` workplan details section (edit workplan handler at 5578-5717, complete workplan handler at 5921-5987)

- [ ] **Step 1: Template**

Replace the includes at the top with:

```html
{% include "modal_workplan_record.html" %}
{% include "modal_complete_workplan.html" %}
{% include "modal_plan_services.html" %}
{% include "modal_complete_services.html" %}
{% include "modal_service_record.html" %}
{% include "modal_incident_record.html" %}
```

Replace the action buttons block with:

```html
<div class="d-flex flex-wrap gap-2 mb-3">
    <button type="button" class="btn btn-outline-primary edit-workplan-btn"
            data-workplan-id="{{ payload.workplan_data.workplan_id }}"
            data-due-date="{{ payload.workplan_data.due_date }}"
            data-workplan-status="{{ payload.workplan_data.workplan_status }}"
            data-workplan-size="{{ payload.workplan_data.workplan_size }}"
            data-description="{{ payload.workplan_data.description|replace('\r\n', '&#10;')|replace('\n', '&#10;')|replace('"', '&quot;') if payload.workplan_data.description else '' }}"
            data-completion-date="{{ payload.workplan_data.completion_date if payload.workplan_data.completion_date else '' }}"
            data-completion-notes="{{ payload.workplan_data.completion_notes|replace('\r\n', '&#10;')|replace('\n', '&#10;')|replace('"', '&quot;') if payload.workplan_data.completion_notes else '' }}"
            data-linked-incidents-count="{{ payload.incidents_data|length if payload.incidents_data else 0 }}"
            data-linked-services-count="{{ payload.workplan_data.total_count }}"
            data-planned-services-count="{{ payload.workplan_data.total_count - payload.workplan_data.completed_count }}"
            data-latest-service-date="{{ payload.latest_service_date if payload.latest_service_date else '' }}">
        <span>✍ Edit workplan</span>
    </button>
    <button type="button" class="btn btn-outline-primary" data-bs-toggle="modal" data-bs-target="#planServicesModal"
            data-workplan-id="{{ payload.workplan_data.workplan_id }}"
            data-lock-workplan="true"
            data-preselect="[]"
            {% if payload.workplan_data.workplan_status == "Done" %}disabled{% endif %}>
        <span>🧑‍🔧 Plan services</span>
    </button>
    <button type="button" class="btn btn-outline-primary" data-bs-toggle="modal" data-bs-target="#completeServicesModal"
            data-planned-services='{{ complete_rows | tojson }}'
            {% if not payload.planned_services_data or payload.workplan_data.workplan_status == "Done" %}disabled{% endif %}>
        <span>✅ Complete services</span>
    </button>
    <button type="button" class="btn btn-outline-primary" data-bs-toggle="modal" data-bs-target="#completeWorkplanModal"
            data-workplan-id="{{ payload.workplan_data.workplan_id }}"
            data-latest-service-date="{{ payload.latest_service_date if payload.latest_service_date else '' }}"
            {% if payload.workplan_data.workplan_status == "Done" or not payload.all_services_completed %}disabled{% endif %}>
        <span>🏁 Complete workplan</span>
    </button>
    <button type="button" class="btn btn-outline-danger delete-record"
            data-workplan-id="{{ payload.workplan_data.workplan_id }}">
        <span>🗑 Delete</span>
    </button>
</div>
```

The complete-services button needs the 11-tuple reduced to the six fields the modal reads, so build `complete_rows` in the template directly above the buttons block:

```html
{% set complete_rows = [] %}
{% if payload.planned_services_data %}
    {% for service_id, component_id, component_name, description, workplan_id, workplan_name, incident_id, effective_planned_date, planned_date, installation_status, oldest_history_date in payload.planned_services_data %}
        {% set _ = complete_rows.append([service_id, component_name, description, oldest_history_date, installation_status, payload.workplan_data.completion_date]) %}
    {% endfor %}
{% endif %}
```

In the info card, replace the "Progress", "Affected bike" and "Affected components" badges with:

```html
                    <span class="badge bg-light text-dark border fs-6 text-wrap text-start fw-normal badge-info">
                        📊 <strong>Services:</strong> {{ payload.workplan_data.completed_count }} of {{ payload.workplan_data.total_count }} completed
                    </span>
                    {% if payload.workplan_data.checkbox_progress %}
                    <span class="badge bg-light text-dark border fs-6 text-wrap text-start fw-normal badge-info">
                        ☑ <strong>Tasks:</strong> {{ payload.workplan_data.checkbox_progress.checked }}/{{ payload.workplan_data.checkbox_progress.total }} completed
                    </span>
                    {% endif %}
                    <span class="badge bg-light text-dark border fs-6 text-wrap text-start fw-normal badge-info">
                        🚴 <strong>Bikes:</strong>
                        {% if payload.workplan_data.bike_ids %}
                            {% for bike_id in payload.workplan_data.bike_ids %}
                                <a href="/bike_details/{{ bike_id }}" class="text-decoration-none text-reset">{{ payload.workplan_data.bike_names[loop.index0] }}</a>{% if not loop.last %}, {% endif %}
                            {% endfor %}
                        {% else %}
                            None
                        {% endif %}
                    </span>
                    <span class="badge bg-light text-dark border fs-6 text-wrap text-start fw-normal badge-info">
                        ⚙ <strong>Components:</strong>
                        {% if payload.workplan_data.component_ids %}
                            {% for component_id in payload.workplan_data.component_ids %}
                                {% set component_name = payload.workplan_data.component_names[loop.index0] %}
                                {% if component_name != "Deleted component" %}
                                    <a href="/component_details/{{ component_id }}" class="text-decoration-none text-reset">{{ component_name }}</a>{% if not loop.last %}, {% endif %}
                                {% else %}
                                    {{ component_name }}{% if not loop.last %}, {% endif %}
                                {% endif %}
                            {% endfor %}
                        {% else %}
                            None
                        {% endif %}
                    </span>
```

Replace the success banner block with:

```html
        {% if payload.workplan_data.workplan_status == "Done" %}
        <div class="card shadow mb-4">
            <div class="alert alert-secondary m-0">
                <div class="d-flex align-items-center">
                    <div class="fs-2 me-3">🏁</div>
                    <div>
                        <h5 class="card-title mb-2">Workplan completed</h5>
                        <p class="mb-1">This workplan was completed on {{ payload.workplan_data.completion_date.split(' ')[0] if payload.workplan_data.completion_date else 'an unknown date' }}. Edit the workplan to reopen it.</p>
                    </div>
                </div>
            </div>
        </div>
        {% elif payload.all_services_completed %}
        <div class="card shadow mb-4">
            <div class="alert alert-success m-0">
                <div class="d-flex align-items-center">
                    <div class="fs-2 me-3">✅</div>
                    <div>
                        <h5 class="card-title mb-2">All services completed</h5>
                        <p class="mb-1">Every service in this workplan is completed. Choose "Complete workplan" to mark it as done and close any related incidents that are still open.</p>
                    </div>
                </div>
            </div>
        </div>
        {% elif not payload.workplan_data.total_count %}
        <div class="card shadow mb-4">
            <div class="alert alert-info m-0">
                <div class="d-flex align-items-center">
                    <div class="fs-2 me-3">🧑‍🔧</div>
                    <div>
                        <h5 class="card-title mb-2">No services planned yet</h5>
                        <p class="mb-1">Choose "Plan services" to add the work this workplan should cover. The workplan gets its bike and components from its services.</p>
                    </div>
                </div>
            </div>
        </div>
        {% endif %}
```

In the incidents table: change the helper text above it to "Incidents are linked to this workplan through their services", change the unpack to the 16-tuple (`..., incident_title, incident_workplans, planned_service_count, completed_service_count`), remove `data-workplan-id` and `data-workplans` from the edit button.

Replace the services table with a planned services table followed by the completed services table:

```html
        <div class="card shadow mb-4">
            <div class="card-header fw-bold">Planned services</div>
            <div class="card-body">
                <div class="table-responsive">
                <table class="table table-hover">
                    <thead>
                        <tr>
                            <th>Planned for</th>
                            <th>Description</th>
                            <th>Component</th>
                            <th class="text-end"></th>
                        </tr>
                    </thead>
                    <tbody>
                        {% if payload.planned_services_data %}
                            {% for service_id, component_id, component_name, description, workplan_id, workplan_name, incident_id, effective_planned_date, planned_date, installation_status, oldest_history_date in payload.planned_services_data %}
                                <tr {% if component_name != "Deleted component" %}role="button" onclick="window.location='/component_details/{{ component_id }}';"{% endif %}>
                                    <td>{{ effective_planned_date.split(' ')[0] if effective_planned_date else "-" }}</td>
                                    <td>{{ description }}</td>
                                    <td>{{ component_name }}</td>
                                    <td class="text-end">
                                        <button type="button" class="mb-1 btn btn-outline-success btn-sm" data-bs-toggle="modal" data-bs-target="#completeServicesModal"
                                                data-planned-services='{{ [[service_id, component_name, description, oldest_history_date, installation_status, payload.workplan_data.completion_date]] | tojson }}'
                                                onclick="event.stopPropagation();"
                                                {% if installation_status == "Retired" or payload.workplan_data.workplan_status == "Done" %}disabled{% endif %}>✅
                                        </button>
                                        <button class="mb-1 btn btn-outline-primary btn-sm edit-service-btn"
                                                data-service-id="{{ service_id }}"
                                                data-service-date=""
                                                data-service-description="{{ description }}"
                                                data-component-id="{{ component_id }}"
                                                data-workplan-id="{{ workplan_id if workplan_id else '' }}"
                                                data-incident-id="{{ incident_id if incident_id else '' }}"
                                                data-planned-date="{{ planned_date if planned_date else '' }}"
                                                data-status="Planned"
                                                data-redirect-url="/workplan_details/{{ payload.workplan_data.workplan_id }}"
                                                onclick="event.stopPropagation();"
                                                {% if installation_status == "Retired" %}disabled{% endif %}>✍
                                        </button>
                                        <button type="button" class="mb-1 btn btn-outline-danger btn-sm delete-record"
                                                data-service-id="{{ service_id }}"
                                                onclick="event.stopPropagation();"
                                                {% if installation_status == "Retired" %}disabled{% endif %}>🗑
                                        </button>
                                    </td>
                                </tr>
                            {% endfor %}
                        {% else %}
                            <tr>
                                <td colspan="4" class="text-center">No planned services in this workplan</td>
                            </tr>
                        {% endif %}
                    </tbody>
                </table>
                </div>
            </div>
        </div>

        <div class="card shadow mb-4">
            <div class="card-header fw-bold">Completed services</div>
            <div class="card-body">
                <div class="table-responsive">
                <table class="table table-hover">
                    <thead>
                        <tr>
                            <th>Date</th>
                            <th>Description</th>
                            <th>Component</th>
                            <th class="text-end"></th>
                        </tr>
                    </thead>
                    <tbody>
                        {% if payload.services_data %}
                            {% for service_id, service_date, description, component_id, component_name, workplan_id, incident_id, planned_date, installation_status in payload.services_data %}
                                <tr {% if component_name != "Deleted component" %}role="button" onclick="window.location='/component_details/{{ component_id }}';"{% endif %}>
                                    <td>{{ service_date }}</td>
                                    <td>{{ description }}</td>
                                    <td>{{ component_name }}</td>
                                    <td class="text-end">
                                        <button class="mb-1 btn btn-outline-primary btn-sm edit-service-btn"
                                                data-service-id="{{ service_id }}"
                                                data-service-date="{{ service_date }}"
                                                data-service-description="{{ description }}"
                                                data-component-id="{{ component_id }}"
                                                data-workplan-id="{{ workplan_id if workplan_id else '' }}"
                                                data-incident-id="{{ incident_id if incident_id else '' }}"
                                                data-planned-date="{{ planned_date if planned_date else '' }}"
                                                data-status="Completed"
                                                data-redirect-url="/workplan_details/{{ payload.workplan_data.workplan_id }}"
                                                onclick="event.stopPropagation();"
                                                {% if installation_status == "Retired" %}disabled{% endif %}>✍
                                        </button>
                                        <button type="button" class="mb-1 btn btn-outline-danger btn-sm delete-record"
                                                data-service-id="{{ service_id }}"
                                                onclick="event.stopPropagation();"
                                                {% if installation_status == "Retired" %}disabled{% endif %}>🗑
                                        </button>
                                    </td>
                                </tr>
                            {% endfor %}
                        {% else %}
                            <tr>
                                <td colspan="4" class="text-center">No completed services in this workplan</td>
                            </tr>
                        {% endif %}
                    </tbody>
                </table>
                </div>
            </div>
        </div>
```

The service modal's edit handler (Task 12) reads `data-status`, `data-incident-id`, `data-planned-date`.

- [ ] **Step 2: JS, edit workplan handler**

In the IIFE "Function to handle workplan editing from workplan_details page" (main.js 5578-5717): remove `workplanAffectedComponents` and `workplanAffectedBikeId` from `pendingFormData`; remove the "Set bike dropdown" line and the whole "Handle component selection" block inside `shown.bs.modal`. Add after the warning banner logic:

```javascript
                // Pass counts used by the workplan form validation
                document.getElementById('workplan_form').dataset.plannedServicesCount = this.dataset.plannedServicesCount || '0';
                document.getElementById('workplan_form').dataset.latestServiceDate = this.dataset.latestServiceDate || '';
```

- [ ] **Step 3: JS, complete workplan handler**

In the IIFE "Function to handle completing workplan from workplan_details page", inside `shown.bs.modal` after the completion date default, add:

```javascript
            // Remember latest service date for validation on submit
            completeWorkplanModal.dataset.latestServiceDate = completeWorkplanBtn.dataset.latestServiceDate || '';
```

and after the `shown.bs.modal` listener add:

```javascript
        // Validate completion date before the form posts
        document.getElementById('completeWorkplanForm').addEventListener('submit', function(event) {
            const completionDateInput = document.getElementById('completeWorkplanCompletionDate');
            const completionDate = completionDateInput.value;
            const latestServiceDate = completeWorkplanModal.dataset.latestServiceDate || '';

            if (!validateDateInput(completionDateInput)) {
                event.preventDefault();
                showServicesValidationModal('Please enter a valid completion date in format YYYY-MM-DD HH:MM.');
                return;
            }

            if (new Date(completionDate) > new Date()) {
                event.preventDefault();
                showServicesValidationModal('Completion date cannot be in the future.');
                return;
            }

            if (latestServiceDate && completionDate < latestServiceDate) {
                event.preventDefault();
                showServicesValidationModal(`Completion date cannot be before the latest service in this workplan (${latestServiceDate}).`);
            }
        });
```

- [ ] **Step 4: Manual check**

Start the app, open a workplan. Expected: page renders, plan services opens with workplan locked, complete services lists planned rows ticked, complete workplan disabled until all completed, banner text per state.

- [ ] **Step 5: Checkpoint**

Human reviews and commits: `Rebuild workplan details page around services`.

---

### Task 10: Workplan modal and workplans list

**Files:**
- Modify: `frontend/templates/modal_workplan_record.html`, `frontend/templates/workplans.html`, `frontend/static/js/main.js` workplans page section (4807-5350)

- [ ] **Step 1: Modal**

In `modal_workplan_record.html` delete the whole "Second row" block (the two `col-md-6` divs for bike and components) and the hidden `initial_workplan_component_id` input. Change the warning banner text to "This workplan has <span id="warning_linked_items"></span>." only (drop the sentence about changing bike or components).

- [ ] **Step 2: Workplans list template**

In `workplans.html` change the loop unpack to `workplan_id, due_date, workplan_status, workplan_size, component_ids, component_names, bike_ids, bike_names, workplan_description, completion_date, completion_notes, elapsed_days, workplan_title, service_progress`. Replace the bike cell with:

```html
                            <td>
                                {% if bike_ids %}
                                    {% for bike_id in bike_ids %}
                                        <a href="/bike_details/{{ bike_id }}" class="text-decoration-none text-reset" onclick="event.stopPropagation();">{{ bike_names[loop.index0] }}</a>{% if not loop.last %}, {% endif %}
                                    {% endfor %}
                                {% else %}
                                    Not assigned
                                {% endif %}
                            </td>
```

Replace the components cell's variables (`workplan_affected_component_ids` to `component_ids`, `affected_component_names` to `component_names`, and the else branch to `Not assigned`). In the size cell replace the `checkbox_progress` block with:

```html
                                {% if service_progress %}
                                    <div class="checkbox-progress-container">
                                        {% set percentage = (service_progress.completed / service_progress.total * 100) | round | int %}
                                        <span class="checkbox-progress-donut {% if percentage == 100 %}complete{% endif %}"
                                            style="--progress: {{ percentage }}"
                                            title="Services: {{ service_progress.completed }} of {{ service_progress.total }} completed">
                                        </span>
                                        <span class="checkbox-progress-text {% if percentage == 100 %}complete{% endif %}">
                                            {{ service_progress.completed }}/{{ service_progress.total }}
                                        </span>
                                    </div>
                                {% endif %}
```

- [ ] **Step 3: JS**

In the workplans page IIFE (4807 onward):

- In `shown.bs.modal`: remove all three `initializeComponentSelector(...)` calls and the `workplan_affected_bike_id` assignment in the from-incident branch. Keep the due date defaulting and description prefill.
- In `hidden.bs.modal`: remove the TomSelect cleanup block for `workplan_affected_component_ids`.
- In the new workplan button handler: remove the "Clear TomSelect" block.
- In the from-incident handler: `pendingIncidentData` becomes `{ description: 'Transferred from incident description: ' + incidentDescription }`.
- Delete `initializeComponentSelector` entirely.
- In `updateFormFields`: remove the `workplan_affected_bike_id` line and the `workplan-id-display` line (no template contains that element, so the line is dead code).
- In `initializeWorkplanForm`: remove the "Add handler for bike select validation" block.
- In `validateWorkplanForm`: remove the `workplanAffectedComponents`, `componentSelect` and `workplanAffectedBikeId` reads and the "Either affected components or affected bike must be selected" rule. Add after the "completion date should be empty when Planned" rule:

```javascript
    // Cannot complete while planned services remain (count passed from the edit button)
    const plannedServicesCount = parseInt(form.dataset.plannedServicesCount || '0');
    if (workplanStatus === "Done" && plannedServicesCount > 0) {
        errorMessage = `Workplan cannot be completed while ${plannedServicesCount} planned service(s) remain`;
        isValid = false;
    }

    // Completion date cannot be before the latest completed service
    const latestServiceDate = form.dataset.latestServiceDate || '';
    if (workplanStatus === "Done" && completionDate && latestServiceDate && completionDate < latestServiceDate) {
        form.querySelector('#completion_date').classList.add('is-invalid');
        errorMessage = `Completion date cannot be before the latest service in this workplan (${latestServiceDate})`;
        isValid = false;
    }
```

- In the sorting function for the workplans table (search for `case` blocks in `initializeWorkplanTable`), no column indexes change.

- [ ] **Step 4: Manual check**

Open /workplans, create a workplan with only date/size/description. Expected: created, redirected to details with the "No services planned yet" banner.

- [ ] **Step 5: Checkpoint**

Human reviews and commits: `Remove bike and component fields from workplan modal`.

---

### Task 11: Incident modal and incident reports page

**Files:**
- Modify: `frontend/templates/modal_incident_record.html`, `frontend/templates/incident_reports.html`, `frontend/static/js/main.js` incident section (4132-4298 removal, 4564-4720 sort/search)

- [ ] **Step 1: Modal**

Delete the "Workplan link (optional)" `col-12` block from `modal_incident_record.html`.

- [ ] **Step 2: Incident reports template**

Add `{% include "modal_plan_services.html" %}` after the workplan modal include. Change the loop unpack to end with `incident_title, incident_workplans, planned_service_count, completed_service_count`. Replace the workplan cell with:

```html
                            <td>
                                {% if incident_workplans %}
                                    {% for workplan_id, workplan_name in incident_workplans %}
                                        <a href="/workplan_details/{{ workplan_id }}" class="text-decoration-none text-reset">{{ workplan_name if workplan_name else 'Workplan ' ~ workplan_id }}</a>{% if not loop.last %}, {% endif %}
                                    {% endfor %}
                                {% else %}
                                    -
                                {% endif %}
                                {% if planned_service_count or completed_service_count %}
                                    <br><small class="text-muted">{{ completed_service_count }}/{{ planned_service_count + completed_service_count }} services</small>
                                {% endif %}
                            </td>
```

Replace the 📝 button with these two buttons:

```html
                                <button type="button" class="mb-1 btn btn-outline-secondary btn-sm create-workplan-from-incident-btn"
                                    data-incident-id="{{ incident_id }}"
                                    data-description="{{ incident_description|replace('\r\n', '&#10;')|replace('\n', '&#10;')|replace('"', '&quot;') }}"
                                    title="New workplan with planned services for this incident"
                                    {% if incident_status == "Resolved" or not incident_affected_component_ids %}disabled{% endif %}
                                    onclick="event.stopPropagation();">📝
                                </button>
                                <button type="button" class="mb-1 btn btn-outline-secondary btn-sm" data-bs-toggle="modal" data-bs-target="#planServicesModal"
                                    data-incident-id="{{ incident_id }}"
                                    data-preselect='{{ incident_affected_component_ids|tojson if incident_affected_component_ids else "[]" }}'
                                    title="Plan services for this incident"
                                    {% if incident_status == "Resolved" %}disabled{% endif %}
                                    onclick="event.stopPropagation();">🧑‍🔧
                                </button>
```

Remove `data-workplan-id` and `data-workplans` from the edit button. Update the helper text above the search box to "Search includes incident descriptions, resolution notes and workplan titles" (unchanged) since the workplan cell still holds titles.

- [ ] **Step 3: JS removals**

Delete from main.js the block starting at `// ----- Workplan Dropdown Population in Incident Modal -----` (line 4130) through the end of that `document.addEventListener('DOMContentLoaded', ...)` at line 4297, keeping the closing `})();` of the enclosing IIFE. Also in the incident-page `[data-bs-target="#incidentRecordModal"]` new-incident handler (search `isNewIncident = true`), nothing references the workplan dropdown, so no change.

Sorting: the workplan column is still index 7 and the `case 7` text compare still works with multiple links.

- [ ] **Step 4: Manual check**

Open /incident_reports, click 🧑‍🔧 on an open incident. Expected: plan modal opens with the incident's components preselected and no workplan selected. Submit. Expected: report modal, then reload shows "0/1 services" under the workplan column dash.

- [ ] **Step 5: Checkpoint**

Human reviews and commits: `Link incidents to services, remove incident workplan dropdown`.

---

### Task 12: Service record modal

**Files:**
- Modify: `frontend/templates/modal_service_record.html`, `frontend/static/js/main.js:766-795` (shared edit handler) and `:3640-3815` (component details service modal handlers)

- [ ] **Step 1: Modal**

Replace the body of `modal_service_record.html` (inside the form) with:

```html
                <div class="modal-body">
                    <input type="hidden" id="serviceComponentId" name="component_id" value="{% if payload.bike_component_data is defined and payload.bike_component_data %}{{ payload.bike_component_data['component_id'] }}{% endif %}">
                    <input type="hidden" id="serviceId" name="service_id">
                    <input type="hidden" id="service_redirect_url" name="redirect_url">

                    <div class="mb-3">
                        <div class="form-label fw-bold d-block">Status</div>
                        <div class="form-check form-check-inline mt-2">
                            <input class="form-check-input" type="radio" name="status" id="service_status_completed" value="Completed" checked>
                            <label class="form-check-label" for="service_status_completed">Completed</label>
                        </div>
                        <div class="form-check form-check-inline">
                            <input class="form-check-input" type="radio" name="status" id="service_status_planned" value="Planned">
                            <label class="form-check-label" for="service_status_planned">Planned</label>
                        </div>
                    </div>
                    <div class="mb-3" id="serviceDateGroup">
                        <label for="serviceDate" class="form-label fw-bold">Service date</label>
                        <div class="input-group date-input-group">
                            <input type="text" class="form-control datepicker-input" id="serviceDate" name="service_date">
                            <span class="input-group-text datepicker-toggle">🗓</span>
                        </div>
                    </div>
                    <div class="mb-3 d-none" id="servicePlannedDateGroup">
                        <label for="servicePlannedDate" class="form-label fw-bold">Planned date (optional)</label>
                        <div class="input-group date-input-group">
                            <input type="text" class="form-control datepicker-input" id="servicePlannedDate" name="planned_date">
                            <span class="input-group-text datepicker-toggle">🗓</span>
                        </div>
                        <small class="form-text text-muted">Leave blank to use the due date of the workplan.</small>
                    </div>
                    <div class="mb-3">
                        <label for="serviceDescription" class="form-label fw-bold">Description</label>
                        <textarea class="form-control" id="serviceDescription" name="service_description" rows="3" required minlength="5"></textarea>
                    </div>
                    <div class="mb-3">
                        <div class="d-flex justify-content-between align-items-center">
                            <label for="serviceWorkplanId" class="form-label fw-bold mb-0">Workplan</label>
                            <a href="#" id="serviceViewWorkplanLink" class="text-primary d-none" target="_blank">View workplan</a>
                        </div>
                        <select class="form-select mt-2" id="serviceWorkplanId" name="workplan_id">
                            <option value="">No workplan</option>
                            {% if payload.workplans_data is defined and payload.workplans_data %}
                            {% for workplan_id, due_date, workplan_status, workplan_size, component_ids, component_names, bike_ids, bike_names, workplan_description, completion_date, completion_notes, elapsed_days, workplan_title, service_progress in payload.workplans_data %}
                                <option value="{{ workplan_id }}" data-status="{{ workplan_status }}">{{ workplan_title }}{% if workplan_status == "Done" %} (done){% endif %}</option>
                            {% endfor %}
                            {% endif %}
                        </select>
                        <small class="form-text text-muted">Done workplans are listed so existing links can be kept, but new links should go to planned workplans.</small>
                    </div>
                    <div class="mb-3">
                        <label for="serviceIncidentId" class="form-label fw-bold">Incident</label>
                        <select class="form-select" id="serviceIncidentId" name="incident_id">
                            <option value="">No incident</option>
                            {% if payload.open_incidents_for_component is defined and payload.open_incidents_for_component %}
                            {% for incident_id, incident_title in payload.open_incidents_for_component %}
                                <option value="{{ incident_id }}">{{ incident_title }}</option>
                            {% endfor %}
                            {% endif %}
                        </select>
                        <small class="form-text text-muted">Open incidents that reference this component.</small>
                    </div>
                    <div>
                        <div class="text-end">
                            <small class="text-muted">
                                🔑 <strong>Service id:</strong>
                                <span id="service-id-display">Not created yet</span>
                            </small>
                        </div>
                    </div>
                </div>
```

The workplan list is now server-rendered, which removes the need for `populateServiceWorkplanDropdown` and its `data-workplans` attributes. On the workplan details page, `open_incidents_for_component` is not in the payload, so the incident dropdown shows only "No incident" there, plus the current value set by JS (Step 3 adds the option if missing).

- [ ] **Step 2: Shared edit handler (main.js 766-795)**

This handler runs on every page with `.edit-service-btn`. Replace its body with:

```javascript
    // Service record edit button
    document.querySelectorAll('.edit-service-btn').forEach(button => {
        button.addEventListener('click', function(e) {
            const serviceId = this.dataset.serviceId;
            const serviceDate = this.dataset.serviceDate;
            const serviceDescription = this.dataset.serviceDescription;
            const componentId = this.dataset.componentId;
            const status = this.dataset.status || 'Completed';
            const plannedDate = this.dataset.plannedDate || '';
            const workplanId = this.dataset.workplanId || '';
            const incidentId = this.dataset.incidentId || '';
            const redirectUrl = this.dataset.redirectUrl || '';

            document.getElementById('serviceRecordModalLabel').textContent = 'Edit service record';
            document.getElementById('serviceRecordForm').action = '/update_service_record';
            document.getElementById('serviceId').value = serviceId;
            document.getElementById('serviceComponentId').value = componentId || '';
            document.getElementById('serviceDescription').value = serviceDescription;
            document.getElementById('service_redirect_url').value = redirectUrl;
            document.getElementById('service-id-display').textContent = serviceId || 'Not created yet';

            setServiceModalStatus(status);
            setServiceModalSelect('serviceWorkplanId', workplanId);
            setServiceModalSelect('serviceIncidentId', incidentId);

            const isOnWorkplanDetailsPage = document.getElementById('workplan-details') !== null;
            const viewLink = document.getElementById('serviceViewWorkplanLink');
            if (viewLink && workplanId && !isOnWorkplanDetailsPage) {
                viewLink.href = `/workplan_details/${workplanId}`;
                viewLink.classList.remove('d-none');
            } else if (viewLink) {
                viewLink.classList.add('d-none');
            }

            const serviceModal = new bootstrap.Modal(document.getElementById('serviceRecordModal'));
            serviceModal.show();

            // Set date values after the modal is shown so the pickers keep them
            setTimeout(() => {
                document.getElementById('serviceDate').value = serviceDate || '';
                document.getElementById('servicePlannedDate').value = plannedDate;
            }, 100);
        });
    });
```

and add above the `document.addEventListener('DOMContentLoaded', ...)` at line 769 these two globals:

```javascript
// Function to toggle date fields in the service modal based on status
window.setServiceModalStatus = function(status) {
    const isPlanned = status === 'Planned';
    document.getElementById('service_status_planned').checked = isPlanned;
    document.getElementById('service_status_completed').checked = !isPlanned;
    document.getElementById('serviceDateGroup').classList.toggle('d-none', isPlanned);
    document.getElementById('servicePlannedDateGroup').classList.toggle('d-none', !isPlanned);
    document.getElementById('serviceDate').required = !isPlanned;
};

// Function to select a value in a service modal dropdown, adding it if the option is missing
window.setServiceModalSelect = function(selectId, value) {
    const select = document.getElementById(selectId);
    if (!select) return;
    if (value && !Array.from(select.options).some(option => option.value === value)) {
        const option = document.createElement('option');
        option.value = value;
        option.textContent = `Linked (${value})`;
        select.appendChild(option);
    }
    select.value = value || '';
};
```

Also attach the status radio listener once, inside the same `DOMContentLoaded`:

```javascript
    // Toggle service modal date fields when status changes
    document.querySelectorAll('input[name="status"]').forEach(radio => {
        radio.addEventListener('change', function() {
            setServiceModalStatus(this.value);
        });
    });

    // Validate service modal before it posts
    const serviceRecordForm = document.getElementById('serviceRecordForm');
    if (serviceRecordForm) {
        serviceRecordForm.addEventListener('submit', function(event) {
            const status = document.querySelector('input[name="status"]:checked').value;
            const serviceDateInput = document.getElementById('serviceDate');
            const plannedDateInput = document.getElementById('servicePlannedDate');

            if (status === 'Completed') {
                if (!serviceDateInput.value || !validateDateInput(serviceDateInput)) {
                    event.preventDefault();
                    showServicesValidationModal('Please enter a valid service date in format YYYY-MM-DD HH:MM.');
                    return;
                }
                if (new Date(serviceDateInput.value) > new Date()) {
                    event.preventDefault();
                    showServicesValidationModal('Service date cannot be in the future.');
                    return;
                }
                const oldestHistoryDate = serviceRecordForm.dataset.oldestHistoryDate || '';
                if (oldestHistoryDate && serviceDateInput.value <= oldestHistoryDate) {
                    event.preventDefault();
                    showServicesValidationModal(`Service date cannot be at or before component creation date (${oldestHistoryDate}).`);
                    return;
                }
            } else if (plannedDateInput.value && !validateDateInput(plannedDateInput)) {
                event.preventDefault();
                showServicesValidationModal('Please enter a valid planned date in format YYYY-MM-DD HH:MM, or leave it blank.');
            }
        });
    }
```

`showServicesValidationModal` is defined in the shared subsection added in Task 8, which sits later in the file but is a function declaration, so hoisting makes it available. Keep the "Service and history record edit buttons" subsection where it is.

For `oldestHistoryDate`, add `data-oldest-history-date="{{ payload.oldest_history_date if payload.oldest_history_date is defined and payload.oldest_history_date else '' }}"` to the `<form id="serviceRecordForm">` tag in the modal. On pages without that payload key (workplan details), the attribute is empty and the check is skipped; the backend still enforces it.

- [ ] **Step 3: Component details handlers (main.js 3640-3815)**

Delete `populateServiceWorkplanDropdown` and the `currentComponentId` line above it. In the "Handle 'New Service' button click" handler: remove the `workplansData` parse and `populateServiceWorkplanDropdown` call; add `setServiceModalStatus('Completed'); setServiceModalSelect('serviceWorkplanId', ''); setServiceModalSelect('serviceIncidentId', ''); document.getElementById('servicePlannedDate').value = '';` after the form action line. Delete the second `.edit-service-btn` handler block in this section entirely (the shared one from Step 2 now does everything). Keep the `serviceWorkplanSelect` change listener and the history edit handler.

- [ ] **Step 4: Manual check**

On component details, click New service, switch status to Planned. Expected: date hides, planned date shows, submit creates a planned service and the page shows it in the planned services table (Task 14).

- [ ] **Step 5: Checkpoint**

Human reviews and commits: `Add status, incident and planned date to service record modal`.

---

### Task 13: Bike and collection details pages

**Files:**
- Modify: `frontend/templates/bike_details.html` (macros 53-64, button map 69-75, incidents table 331-405, workplans table 408-472, new planned services table after workplans), `frontend/templates/collection_details.html` (includes and buttons), `backend/utils.py:30-49` (`get_button_order` defaults)

- [ ] **Step 1: Bike details**

Add includes near the top:

```html
{% include "modal_plan_services.html" %}
{% include "modal_complete_services.html" %}
```

Add a macro after `btn_new_incident`:

```html
{% macro btn_plan_services() %}
<button type="button" id="btn-plan-services" class="btn btn-outline-primary" data-bs-toggle="modal" data-bs-target="#planServicesModal"
        data-preselect='{{ payload.plan_services_preselect | tojson }}'>
    <span>🧑‍🔧 Plan services</span>
</button>
{% endmacro %}
```

Add `'plan-services': btn_plan_services` to `button_map`, and in `backend/utils.py` `get_button_order` defaults add `'plan-services'` after `'install-existing'` in the `bike_details` list. Remove `data-workplans` from `btn_new_incident`.

Incidents table: change the loop unpack to the 16-tuple; replace the workplan cell with the multi-link version from Task 11 Step 2 (without the services count line); remove `data-workplan-id` and `data-workplans` from the edit button.

Workplans table: change the loop unpack to the new 14-tuple (`..., workplan_title, service_progress`); replace the `checkbox_progress` block with the `service_progress` block from Task 10 Step 2.

Add after the workplans card:

```html
        <div class="card shadow mb-4 mt-2">
            <div class="card-header d-flex justify-content-between align-items-center">
                <span class="fw-bold">Planned services</span>
                <button type="button" class="btn btn-outline-success btn-sm" data-bs-toggle="modal" data-bs-target="#completeServicesModal"
                        data-planned-services='{{ complete_rows | tojson }}'
                        {% if not payload.planned_services_data %}disabled{% endif %}>✅ Complete services</button>
            </div>
            <div class="card-body">
                <div class="table-responsive">
                <table class="table table-hover">
                    <thead>
                        <tr>
                            <th>Planned for</th>
                            <th>Description</th>
                            <th>Component</th>
                            <th>Workplan</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% if payload.planned_services_data %}
                            {% for service_id, component_id, component_name, description, workplan_id, workplan_name, incident_id, effective_planned_date, planned_date, installation_status, oldest_history_date in payload.planned_services_data %}
                                <tr role="button" onclick="window.location='/component_details/{{ component_id }}';">
                                    <td>{{ effective_planned_date.split(' ')[0] if effective_planned_date else "-" }}</td>
                                    <td>{{ description }}</td>
                                    <td>{{ component_name }}</td>
                                    <td>
                                        {% if workplan_id %}
                                            <a href="/workplan_details/{{ workplan_id }}" class="text-decoration-none text-reset" onclick="event.stopPropagation();">{{ workplan_name if workplan_name else 'Workplan ' ~ workplan_id }}</a>
                                        {% else %}
                                            -
                                        {% endif %}
                                    </td>
                                </tr>
                            {% endfor %}
                        {% else %}
                            <tr>
                                <td colspan="4" class="text-center">No planned services for components on this bike</td>
                            </tr>
                        {% endif %}
                    </tbody>
                </table>
                </div>
            </div>
        </div>
```

with this set block placed above the card:

```html
{% set complete_rows = [] %}
{% if payload.planned_services_data %}
    {% for service_id, component_id, component_name, description, workplan_id, workplan_name, incident_id, effective_planned_date, planned_date, installation_status, oldest_history_date in payload.planned_services_data %}
        {% set _ = complete_rows.append([service_id, component_name, description, oldest_history_date, installation_status, none]) %}
    {% endfor %}
{% endif %}
```

The last element is `none` because the bike page doesn't know each service's workplan completion date; the backend check still applies.

- [ ] **Step 2: Collection details**

Add `{% include "modal_plan_services.html" %}` to the includes. Add a button after "Update collection status":

```html
    <button type="button" class="btn btn-outline-primary" data-bs-toggle="modal" data-bs-target="#planServicesModal"
            data-preselect='{{ payload.plan_services_preselect | tojson }}'
            {% if not payload.plan_services_preselect %}disabled{% endif %}>
        <span>🧑‍🔧 Plan services</span>
    </button>
```

- [ ] **Step 3: Manual check**

Open a bike, click Plan services. Expected: installed components preselected. Open a collection, same with its components.

- [ ] **Step 4: Checkpoint**

Human reviews and commits: `Add plan services entry points on bike and collection pages`.

---

### Task 14: Component details page and status change notes

**Files:**
- Modify: `frontend/templates/component_details.html` (includes, macros 97-102, service history table 449-513, installation history 519-560, new planned services table), `frontend/templates/modal_update_component_status.html`, `frontend/templates/modal_quick_swap.html`, `frontend/static/js/main.js` (change status handler 823-905, quick swap submit 2046-2064)

- [ ] **Step 1: Component details template**

Add includes: `{% include "modal_plan_services.html" %}` and `{% include "modal_complete_services.html" %}`. In `btn_new_service` remove `data-workplans`. Add a macro and button-map entry `'plan-services'`:

```html
{% macro btn_plan_services() %}
<button type="button" id="btn-plan-services" class="btn btn-outline-primary" data-bs-toggle="modal" data-bs-target="#planServicesModal"
        data-preselect='{{ payload.plan_services_preselect | tojson }}'
        {% if payload.bike_component_data['installation_status'] == "Retired" %}disabled{% endif %}>
    <span>🧑‍🔧 Plan services</span>
</button>
{% endmacro %}
```

and in `backend/utils.py` `get_button_order` defaults add `'plan-services'` after `'new-service'` in the `component_details` list.

Insert a planned services card directly above the "Service history" card, same structure as the bike page table but with an actions column holding the per-row ✅, ✍ and 🗑 buttons exactly as in Task 9's planned services table, with `data-redirect-url="/component_details/{{ payload.bike_component_data['component_id'] }}"` and all three buttons disabled when the component is Retired. Build `complete_rows` the same way as on the bike page.

In the service history table: change the loop unpack to add `incident_id, planned_date` at the end; on the edit button add `data-status="Completed"`, `data-incident-id="{{ incident_id if incident_id else '' }}"`, `data-planned-date="{{ planned_date if planned_date else '' }}"` and remove `data-workplans`. Replace the workplan cell's nested loop with a simple lookup using the tuple's workplan name: since `workplans_data` no longer exposes `checkbox_progress`, the inner loop unpack must change to the new 14 names (`..., workplan_title, service_progress`).

Installation history: change the unpack to add `notes` at the end and add a "Notes" column after Mileage showing `{{ notes if notes else "-" }}`.

- [ ] **Step 2: Status change modal**

In `modal_update_component_status.html` add after the date group:

```html
                    <div class="mb-3">
                        <label for="component_status_notes" class="form-label fw-bold">Notes (optional)</label>
                        <textarea class="form-control" id="component_status_notes" name="notes" rows="2" placeholder="Why the status changes, e.g., worn out, moved to winter bike"></textarea>
                    </div>
```

In main.js change-status handler (line 823 block), after `if (dateInput) dateInput.value = updatedDate;` add:

```javascript
                const notesInput = modal.querySelector('#component_status_notes');
                if (notesInput) notesInput.value = '';
```

- [ ] **Step 3: Quick swap modal**

In `modal_quick_swap.html` add after the swap date group (line 161 area):

```html
                    <div class="mb-3">
                        <label for="swap_notes" class="form-label fw-bold">Notes (optional)</label>
                        <textarea class="form-control" id="swap_notes" name="swap_notes" rows="2" placeholder="Stored on both installation records"></textarea>
                    </div>
```

In main.js `performQuickSwap` after `formData.append('swap_date', ...)` add `formData.append('notes', document.getElementById('swap_notes').value);`.

- [ ] **Step 4: Manual check**

Change a component's status with a note. Expected: note shows in the installation history. Quick swap with a note. Expected: note on both components' history rows.

- [ ] **Step 5: Checkpoint**

Human reviews and commits: `Show planned services on component details, add status change notes`.

---

### Task 15: Help page, README and docs

**Files:**
- Modify: `frontend/templates/help.html:218` and `:466` (workplan descriptions), README changelog section
- Create: `tests/test_protocol_services.md`

- [ ] **Step 1: Help text**

Replace line 218's paragraph with: "Schedule and track maintenance. A workplan groups planned services and gets its bike and components from them. Plan services from an incident, a bike, a collection, a component or the workplan itself, complete them with one date, then complete the workplan." Replace line 466's bullet with "Use planned services to turn incidents into work, and workplans to group them".

- [ ] **Step 2: README changelog**

Under the changelog section add an entry for the next version (the human picks the number) with bullets: services now planned or completed; workplans and incidents linked through services; plan services from incidents, bikes, collections, components; notes on component status changes; migration required, backup first.

- [ ] **Step 3: Manual test protocol**

Create `tests/test_protocol_services.md` following `tests/README.md`: sections for Planning (from each of five pages, preselection, duplicate rule, retired exclusion), Completing (single, bulk, note appended, date rules, retired lock, incident hint), Workplans (banner states, completion blocked by planned services, completion date rules, reopen and revert), Incidents (📝 creates workplan plus services, 🧑‍🔧 plans, multiple workplans shown, delete nulls links), Service modal (status switch, revert recalculates), Status notes, Migration (run on a copy, counts before and after). Each test case: id, steps, expected result, pass/fail column.

- [ ] **Step 4: Checkpoint**

Human reviews and commits: `Document service integration`.

---

### Task 16: Verification and handover

- [ ] **Step 1: Automated tests**

Run: `uv run pytest tests/ -v`. Expected: all PASS.

- [ ] **Step 2: Migration on a copy of the real database**

Copy the production database to the scratchpad, run `python3 backend/db_migration.py` against the copy, compare counts:

```bash
python3 -c "
import sqlite3
c = sqlite3.connect('/path/to/copy.sqlite')
for t in ['services','workplans','incidents','component_history']:
    print(t, c.execute(f'select count(*) from {t}').fetchone()[0])
print('planned', c.execute(\"select count(*) from services where status='Planned'\").fetchone()[0])"
```

Expected: services count grew by the number of converted affected components, no other table lost rows.

- [ ] **Step 3: Walk the manual protocol** against the app running on the migrated copy. Record results in the protocol file.

- [ ] **Step 4: Update the knowledge graph**

Run: `graphify update .`

- [ ] **Step 5: Handover**

Write `.handovers/fullstack/service-integration-fullstack-to-reviewer.md` from `.handovers/TEMPLATE.md`, max 100 lines: files changed with line ranges, tests run, protocol results, known limitations. Then the human decides on `@code-reviewer`.

---

## Self-review notes

- Spec coverage: data model (T1), migration (T3), completed-only reads (T2), utils (T4), planned/complete/revert/validation (T5), workplan and incident logic, payloads, history notes (T6), routes (T7), modals and shared JS (T8, T12), workplan page (T9), workplan modal and list (T10), incident page (T11), bike and collection (T13), component page and #349 (T14), help and protocol (T15), verification (T16). Cross-date rules: backend in T6 `validate_workplan_completion` and T5 `validate_service_record`; frontend in T8 (complete modal), T9 (complete workplan), T10 (edit modal), T12 (service modal).
- Type consistency: `get_workplan_data_tuple` 14 fields ending `workplan_title, service_progress` used in T8, T9, T10, T12, T13, T14. `get_incident_data_tuple` 16 fields ending `incident_title, incident_workplans, planned_service_count, completed_service_count` used in T9, T11, T13. `get_planned_service_data_tuple` 11 fields used in T9, T13, T14. Complete modal rows are 6-element lists `[service_id, component_name, description, oldest_history_date, installation_status, workplan_completion_date]` in T8, T9, T13, T14.
