"""db_migration converts the pre-#351 workplan and incident model to links through services,
changes nothing when run again, and runs on a fresh template.

The pre-#351 database is the synthetic dataset with services, workplans, incidents and
component_history rebuilt in their old shape and filled with old-model rows that point at the
dataset's bikes and components. The test lives until Stage 6 replaces the migration path.
"""

import shutil
import sqlite3

import pytest
from fixtures.dataset import IDS, TEMPLATE_DB, build_dataset

from velo_supervisor import db_migration

OLD_SCHEMA = [
    """CREATE TABLE services (service_id TEXT PRIMARY KEY UNIQUE, component_id TEXT, component_name TEXT,
       bike_id TEXT, service_date TEXT, distance_marker NUMERIC, description TEXT, workplan_id VARCHAR)""",
    """CREATE TABLE workplans (workplan_id TEXT PRIMARY KEY UNIQUE, due_date TEXT, workplan_status TEXT,
       workplan_size TEXT, workplan_affected_component_ids TEXT, workplan_affected_bike_id TEXT,
       workplan_description TEXT, completion_date TEXT, completion_notes TEXT)""",
    """CREATE TABLE incidents (incident_id TEXT PRIMARY KEY UNIQUE, incident_date TEXT, incident_status TEXT,
       incident_severity TEXT, incident_affected_component_ids TEXT, incident_affected_bike_id TEXT,
       incident_description TEXT, resolution_date TEXT, resolution_notes TEXT, workplan_id VARCHAR)""",
    """CREATE TABLE component_history (history_id TEXT PRIMARY KEY UNIQUE, component_id TEXT, bike_id TEXT,
       component_name TEXT, updated_date TEXT, update_reason TEXT, distance_marker NUMERIC)""",
]

OLD_WORKPLANS = [
    (
        "wp-spring",
        "2026-03-01 10:00",
        "Planned",
        "Small",
        (
            f'["{IDS.comp_chain_moved}", "{IDS.comp_cassette_serviced}", "{IDS.comp_wheel_offset}", "comp-gone", '
            f'"{IDS.comp_pads_retired}"]'
        ),
        IDS.bike_road,
        "Spring service",
        None,
        None,
    ),
    (
        "wp-last-year",
        "2025-03-01 10:00",
        "Done",
        "Small",
        f'["{IDS.comp_chain_moved}"]',
        IDS.bike_road,
        "Last year",
        "2025-03-02 10:00",
        "All good",
    ),
    ("wp-emergency", "2026-04-01 10:00", "Planned", "Small", None, None, "Emergency fix", None, None),
]
OLD_SERVICES = [
    (
        "svc-in-plan",
        IDS.comp_chain_moved,
        "Chain",
        IDS.bike_road,
        "2026-02-01 08:00",
        0,
        "Already waxed in plan",
        "wp-spring",
    ),
]
OLD_INCIDENTS = [
    (
        "inc-cassette",
        "2026-02-10 10:00",
        "Open",
        "Priority",
        f'["{IDS.comp_cassette_serviced}"]',
        IDS.bike_road,
        "Cassette skips",
        None,
        None,
        "wp-spring",
    ),
    ("inc-bike-only", "2026-02-11 10:00", "Open", "Monitor", None, IDS.bike_road, "Creaking", None, None, "wp-spring"),
    (
        "inc-new-work",
        "2026-02-12 10:00",
        "Open",
        "Priority",
        f'["{IDS.comp_chain_moved}"]',
        IDS.bike_road,
        "Chain snapped",
        None,
        None,
        "wp-emergency",
    ),
    (
        "inc-retired-only",
        "2026-02-13 10:00",
        "Open",
        "Monitor",
        f'["{IDS.comp_pads_retired}"]',
        IDS.bike_retired,
        "Pads rusty",
        None,
        None,
        "wp-emergency",
    ),
    (
        "inc-last-year",
        "2025-02-11 10:00",
        "Resolved",
        "Monitor",
        f'["{IDS.comp_chain_moved}"]',
        IDS.bike_road,
        "Old",
        "2025-03-02 10:00",
        "Fixed",
        "wp-last-year",
    ),
]
TABLES = ["services", "workplans", "incidents", "component_history"]


def run_migration(db_path):
    connection = sqlite3.connect(db_path)
    try:
        return db_migration.run_all_migrations(connection.cursor(), connection)
    finally:
        connection.close()


def query(db_path, sql, parameters=()):
    connection = sqlite3.connect(db_path)
    try:
        return connection.execute(sql, parameters).fetchall()
    finally:
        connection.close()


def columns(db_path, table):
    return {row[1] for row in query(db_path, f"PRAGMA table_info({table})")}


def tables_content(db_path):
    return {table: query(db_path, f"SELECT * FROM {table} ORDER BY 1") for table in TABLES}


@pytest.fixture
def old_db(tmp_path):
    """The dataset with the four tables in their pre-#351 shape and old-model rows"""
    db_path = tmp_path / "old.sqlite"
    build_dataset(db_path)
    connection = sqlite3.connect(db_path)
    try:
        for table in TABLES:
            connection.execute(f"DROP TABLE {table}")
        for statement in OLD_SCHEMA:
            connection.execute(statement)
        connection.executemany("INSERT INTO workplans VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", OLD_WORKPLANS)
        connection.executemany("INSERT INTO services VALUES (?, ?, ?, ?, ?, ?, ?, ?)", OLD_SERVICES)
        connection.executemany("INSERT INTO incidents VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", OLD_INCIDENTS)
        connection.commit()
    finally:
        connection.close()
    return db_path


def description(db_path, table, key, record_id):
    column = "workplan_description" if table == "workplans" else "incident_description"
    return query(db_path, f"SELECT {column} FROM {table} WHERE {key} = ?", (record_id,))[0][0]


def test_migration_converts_old_model(old_db):
    """Old columns become the service integration schema and old links become services.

    wp-spring (planned) lists chain, cassette, wheel, a deleted and the retired component: the
    chain already has a service in it, so only cassette and wheel get planned services, with no
    date, bike, marker or planned date; the cassette's is linked to inc-cassette, which names it.
    The deleted and retired ones are named in the description, the bike is not. wp-last-year
    (done) gets bike and component names in its description. inc-new-work on the empty planned
    wp-emergency gets a planned chain service; the retired-only, bike-only and done-workplan
    incidents get no service and a note naming their old workplan.
    """
    assert run_migration(old_db)

    assert {"status", "incident_id", "planned_date", "workplan_id"} <= columns(old_db, "services")
    assert "notes" in columns(old_db, "component_history")
    assert "workplan_name" in columns(old_db, "workplans")
    assert not {"workplan_affected_component_ids", "workplan_affected_bike_id"} & columns(old_db, "workplans")
    assert "workplan_id" not in columns(old_db, "incidents")

    assert query(old_db, "SELECT status, incident_id FROM services WHERE service_id = 'svc-in-plan'") == [
        ("Completed", None)
    ]
    assert query(
        old_db,
        """SELECT component_id, service_date, bike_id, distance_marker, incident_id, planned_date
                            FROM services WHERE workplan_id = 'wp-spring' AND status = 'Planned'
                            ORDER BY component_id""",
    ) == [
        (IDS.comp_cassette_serviced, None, None, None, "inc-cassette", None),
        (IDS.comp_wheel_offset, None, None, None, None, None),
    ]
    assert query(
        old_db, "SELECT component_id, status, incident_id FROM services WHERE workplan_id = 'wp-emergency'"
    ) == [(IDS.comp_chain_moved, "Planned", "inc-new-work")]
    assert query(old_db, "SELECT COUNT(*) FROM services WHERE component_id = ?", (IDS.comp_pads_retired,)) == [(0,)]

    spring = description(old_db, "workplans", "workplan_id", "wp-spring")
    assert spring.startswith("Spring service")
    assert "Deleted component" in spring and "Commuter brake pads (retired)" in spring
    assert "Road bike" not in spring
    last_year = description(old_db, "workplans", "workplan_id", "wp-last-year")
    assert last_year.startswith("Last year") and "Road bike" in last_year and "Chain" in last_year

    for incident_id, workplan_id in [
        ("inc-retired-only", "wp-emergency"),
        ("inc-bike-only", "wp-spring"),
        ("inc-last-year", "wp-last-year"),
    ]:
        assert f"previously linked to workplan {workplan_id}" in description(
            old_db, "incidents", "incident_id", incident_id
        )
    assert description(old_db, "incidents", "incident_id", "inc-bike-only").startswith("Creaking")
    assert description(old_db, "incidents", "incident_id", "inc-cassette") == "Cassette skips"


def test_migration_is_idempotent(old_db):
    """A second run performs no step and leaves the converted tables as they were"""
    run_migration(old_db)
    before = tables_content(old_db)
    assert run_migration(old_db) == []
    assert tables_content(old_db) == before


def test_migration_on_fresh_template(tmp_path):
    """The template as shipped migrates to the current schema; a second run performs no step"""
    db_path = tmp_path / "template.sqlite"
    shutil.copy(TEMPLATE_DB, db_path)
    run_migration(db_path)
    assert {"status", "incident_id", "planned_date", "workplan_id"} <= columns(db_path, "services")
    assert "notes" in columns(db_path, "component_history")
    assert "workplan_name" in columns(db_path, "workplans")
    assert "workplan_id" not in columns(db_path, "incidents")
    assert "workplan_affected_bike_id" not in columns(db_path, "workplans")
    assert run_migration(db_path) == []
