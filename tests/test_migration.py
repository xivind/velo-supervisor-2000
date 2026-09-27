"""Migration converts the old workplan/incident model to services"""

import sqlite3


def create_old_schema(cursor):
    """Recreate services, workplans, incidents and component_history as they were before #351"""
    for table in ["services", "workplans", "incidents", "component_history"]:
        cursor.execute(f"DROP TABLE IF EXISTS {table}")
    cursor.execute("""CREATE TABLE services (service_id TEXT PRIMARY KEY UNIQUE, component_id TEXT, component_name TEXT,
                      bike_id TEXT, service_date TEXT, distance_marker NUMERIC, description TEXT, workplan_id VARCHAR)""")
    cursor.execute("""CREATE TABLE workplans (workplan_id TEXT PRIMARY KEY UNIQUE, due_date TEXT, workplan_status TEXT,
                      workplan_size TEXT, workplan_affected_component_ids TEXT, workplan_affected_bike_id TEXT,
                      workplan_description TEXT, completion_date TEXT, completion_notes TEXT)""")
    cursor.execute("""CREATE TABLE incidents (incident_id TEXT PRIMARY KEY UNIQUE, incident_date TEXT, incident_status TEXT,
                      incident_severity TEXT, incident_affected_component_ids TEXT, incident_affected_bike_id TEXT,
                      incident_description TEXT, resolution_date TEXT, resolution_notes TEXT, workplan_id VARCHAR)""")
    cursor.execute("""CREATE TABLE component_history (history_id TEXT PRIMARY KEY UNIQUE, component_id TEXT, bike_id TEXT,
                      component_name TEXT, updated_date TEXT, update_reason TEXT, distance_marker NUMERIC)""")


def seed_old_data(db_path):
    """Seed workplans, incidents and services in the pre-#351 shape"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    create_old_schema(cursor)
    cursor.execute("INSERT INTO bikes (bike_id, bike_name, bike_retired, service_status, total_distance, notes) VALUES ('bike-1', 'Road bike', 'False', NULL, 0, NULL)")
    for component_id, name in [("comp-1", "Chain"), ("comp-2", "Cassette"), ("comp-3", "Brake pads")]:
        cursor.execute("""INSERT INTO components (component_id, bike_id, component_name, component_type,
                          component_distance, component_distance_offset, installation_status, service_interval,
                          lifetime_expected, updated_date)
                          VALUES (?, 'bike-1', ?, 'Type', 0, 0, 'Installed', 1000, 3000, '2026-01-01 10:00')""",
                       (component_id, name))
    cursor.execute("""INSERT INTO components (component_id, bike_id, component_name, component_type,
                      component_distance, component_distance_offset, installation_status, service_interval,
                      lifetime_expected, updated_date)
                      VALUES ('comp-retired', NULL, 'Old chain', 'Type', 0, 0, 'Retired', 1000, 3000, '2026-01-01 10:00')""")
    cursor.execute("""INSERT INTO workplans VALUES ('wp-planned', '2026-03-01 10:00', 'Planned', 'Small',
                      '["comp-1", "comp-2", "comp-3", "comp-gone", "comp-retired"]', 'bike-1', 'Spring service', NULL, NULL)""")
    cursor.execute("""INSERT INTO workplans VALUES ('wp-done', '2025-03-01 10:00', 'Done', 'Small',
                      '["comp-1"]', 'bike-1', 'Last year', '2025-03-02 10:00', 'All good')""")
    cursor.execute("""INSERT INTO services VALUES ('svc-1', 'comp-1', 'Chain', 'bike-1', '2026-02-01 10:00', 0,
                      'Already waxed in plan', 'wp-planned')""")
    cursor.execute("""INSERT INTO incidents VALUES ('inc-comp', '2026-02-10 10:00', 'Open', 'Priority',
                      '["comp-2"]', 'bike-1', 'Cassette skips', NULL, NULL, 'wp-planned')""")
    cursor.execute("""INSERT INTO incidents VALUES ('inc-bike', '2026-02-11 10:00', 'Open', 'Monitor',
                      NULL, 'bike-1', 'Creaking', NULL, NULL, 'wp-planned')""")
    cursor.execute("""INSERT INTO incidents VALUES ('inc-new-work', '2026-02-12 10:00', 'Open', 'Priority',
                      '["comp-1"]', 'bike-1', 'Chain snapped', NULL, NULL, 'wp-empty')""")
    cursor.execute("""INSERT INTO workplans VALUES ('wp-empty', '2026-04-01 10:00', 'Planned', 'Small',
                      NULL, NULL, 'Emergency fix', NULL, NULL)""")
    cursor.execute("""INSERT INTO incidents VALUES ('inc-retired-only', '2026-02-13 10:00', 'Open', 'Monitor',
                      '["comp-retired"]', 'bike-1', 'Old chain rusty', NULL, NULL, 'wp-empty')""")
    cursor.execute("""INSERT INTO incidents VALUES ('inc-done', '2025-02-11 10:00', 'Resolved', 'Monitor',
                      '["comp-1"]', 'bike-1', 'Old', '2025-03-02 10:00', 'Fixed', 'wp-done')""")
    conn.commit()
    conn.close()


def columns(db_path, table):
    conn = sqlite3.connect(db_path)
    names = [row[1] for row in conn.execute(f"PRAGMA table_info({table})")]
    conn.close()
    return names


def snapshot(db_path):
    conn = sqlite3.connect(db_path)
    data = {table: conn.execute(f"SELECT * FROM {table} ORDER BY 1").fetchall()
            for table in ["services", "workplans", "incidents", "component_history"]}
    conn.close()
    return data


def run_migration(db_path):
    import db_migration
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    performed = db_migration.run_all_migrations(cursor, conn)
    conn.close()
    return performed


def test_migration_converts_old_model(app_env):
    db_path = app_env["db_path"]
    run_migration(db_path)
    seed_old_data(db_path)

    run_migration(db_path)

    assert {"status", "incident_id", "planned_date", "workplan_id"} <= set(columns(db_path, "services"))
    assert "notes" in columns(db_path, "component_history")
    assert "workplan_name" in columns(db_path, "workplans")
    assert "workplan_affected_component_ids" not in columns(db_path, "workplans")
    assert "workplan_affected_bike_id" not in columns(db_path, "workplans")
    assert "workplan_id" not in columns(db_path, "incidents")

    conn = sqlite3.connect(db_path)
    assert conn.execute("SELECT status, incident_id FROM services WHERE service_id='svc-1'").fetchone() == ("Completed", None)

    planned = conn.execute("""SELECT component_id, service_date, bike_id, distance_marker, incident_id, planned_date
                              FROM services WHERE workplan_id='wp-planned' AND status='Planned'
                              ORDER BY component_id""").fetchall()
    assert [row[0] for row in planned] == ["comp-2", "comp-3"]
    assert all(row[1] is None and row[2] is None and row[3] is None and row[5] is None for row in planned)
    assert planned[0][4] == "inc-comp"
    assert planned[1][4] is None

    new_work = conn.execute("""SELECT component_id, status, incident_id FROM services
                               WHERE workplan_id='wp-empty'""").fetchall()
    assert new_work == [("comp-1", "Planned", "inc-new-work")]

    done_description = conn.execute("SELECT workplan_description FROM workplans WHERE workplan_id='wp-done'").fetchone()[0]
    assert done_description.startswith("Last year")
    assert "Road bike" in done_description and "Chain" in done_description

    planned_description = conn.execute("SELECT workplan_description FROM workplans WHERE workplan_id='wp-planned'").fetchone()[0]
    assert "Deleted component" in planned_description and "Old chain (retired)" in planned_description
    assert "Road bike" not in planned_description

    assert conn.execute("SELECT COUNT(*) FROM services WHERE component_id='comp-retired'").fetchone()[0] == 0
    retired_incident_description = conn.execute("SELECT incident_description FROM incidents WHERE incident_id='inc-retired-only'").fetchone()[0]
    assert "wp-empty" in retired_incident_description

    bike_incident_description = conn.execute("SELECT incident_description FROM incidents WHERE incident_id='inc-bike'").fetchone()[0]
    assert bike_incident_description.startswith("Creaking") and "wp-planned" in bike_incident_description

    done_incident_description = conn.execute("SELECT incident_description FROM incidents WHERE incident_id='inc-done'").fetchone()[0]
    assert "wp-done" in done_incident_description
    conn.close()


def test_migration_is_idempotent(app_env):
    db_path = app_env["db_path"]
    run_migration(db_path)
    seed_old_data(db_path)
    run_migration(db_path)

    before = snapshot(db_path)
    performed = run_migration(db_path)

    assert performed == []
    assert snapshot(db_path) == before
    assert "workplan_id" not in columns(db_path, "incidents")


def test_migration_on_fresh_template(app_env):
    db_path = app_env["db_path"]
    run_migration(db_path)

    assert {"status", "incident_id", "planned_date", "workplan_id"} <= set(columns(db_path, "services"))
    assert "workplan_id" not in columns(db_path, "incidents")
    assert "workplan_affected_bike_id" not in columns(db_path, "workplans")
    assert run_migration(db_path) == []
