#!/usr/bin/env python3
"""Script to migrate the database, including adding new tables and fields"""

import sqlite3
import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils import generate_unique_id

def find_database_file(filename):
    """Search for a database file in the user's home directory and subdirectories"""
    print(f"Searching for database file named '{filename}'...")
    matches = []
    
    # Start search from home directory
    home_dir = os.path.expanduser("~")
    print(f"Searching in home directory: {home_dir}")
    
    try:
        for root, _, files in os.walk(home_dir):
            if filename in files:
                full_path = os.path.abspath(os.path.join(root, filename))
                matches.append(full_path)
    except PermissionError:
        print("Some directories couldn't be searched due to permission errors.")
    except Exception as e:
        print(f"Error during search: {e}")
    
    if not matches:
        return None
    
    if len(matches) == 1:
        print(f"Found database at: {matches[0]}")
        return matches[0]
    
    # If multiple matches, let user choose
    print(f"Found multiple databases named '{filename}':")
    for i, path in enumerate(matches):
        print(f"  [{i+1}] {path}")
    
    while True:
        choice = input(f"Enter the number of the database to migrate [1-{len(matches)}]: ")
        try:
            index = int(choice) - 1
            if 0 <= index < len(matches):
                return matches[index]
        except ValueError:
            pass
        print("Invalid selection. Please try again.")

def prompt_for_db_path():
    """Prompt user for database path or filename and verify it exists"""
    db_name = input("Please enter the name of your SQLite database file (e.g., prod_db.sqlite): ").strip()
    
    if not db_name:
        print("No database name entered. Migration cancelled.")
        sys.exit(1)
    
    # Try to find the database by name
    db_path = find_database_file(db_name)
    
    if db_path:
        # Verify it's a SQLite database
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("PRAGMA database_list")
            conn.close()
            return db_path
        except sqlite3.Error:
            print(f"Error: Found file at {db_path} but it does not appear to be a valid SQLite database.")
    else:
        print(f"Could not find database file named '{db_name}' in the current directory tree.")
    
    # If automatic search failed, ask for full path
    full_path = input("Please enter the full path to your SQLite database file: ").strip()
    
    if not full_path:
        print("No path entered. Migration cancelled.")
        sys.exit(1)
    
    if os.path.exists(full_path):
        # Verify it's a SQLite database
        try:
            conn = sqlite3.connect(full_path)
            cursor = conn.cursor()
            cursor.execute("PRAGMA database_list")
            conn.close()
            return full_path
        except sqlite3.Error:
            print("Error: The file exists but does not appear to be a valid SQLite database.")
            sys.exit(1)
    else:
        print(f"Error: File not found at '{full_path}'")
        sys.exit(1)

def count_component_types_in_use(cursor, component_type):
    """Count how many components use a specific component type"""
    cursor.execute(
        "SELECT COUNT(*) FROM components WHERE component_type = ?", 
        (component_type,)
    )
    return cursor.fetchone()[0]

def create_incidents_table(cursor):
    """Creates the incidents table if it doesn't exist."""
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='incidents'")
    if not cursor.fetchone():
        cursor.execute("""
            CREATE TABLE incidents (
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
        print("      → Created incidents table")
        return True
    else:
        print("      → Table already exists, skipping")
        return False

def create_workplans_table(cursor):
    """Creates the workplans table if it doesn't exist."""
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='workplans'")
    if not cursor.fetchone():
        cursor.execute("""
            CREATE TABLE workplans (
                workplan_id TEXT PRIMARY KEY UNIQUE,
                workplan_name TEXT,
                due_date TEXT,
                workplan_status TEXT,
                workplan_size TEXT,
                workplan_affected_component_ids TEXT,
                workplan_affected_bike_id TEXT,
                workplan_description TEXT,
                completion_date TEXT,
                completion_notes TEXT
            )
        """)
        print("      → Created workplans table")
        return True
    else:
        print("      → Table already exists, skipping")
        return False

def create_collections_table(cursor):
    """Creates the collections table if it doesn't exist."""
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='collections'")
    if not cursor.fetchone():
        cursor.execute("""
            CREATE TABLE collections (
                collection_id TEXT PRIMARY KEY UNIQUE,
                collection_name TEXT,
                components TEXT,
                bike_id TEXT,
                sub_collections TEXT,
                updated_date TEXT,
                comment TEXT
            )
        """)
        print("      → Created collections table")
        return True
    else:
        print("      → Table already exists, skipping")
        return False

def check_component_types_columns(cursor):
    """Check if the component_types table needs migration"""
    cursor.execute("PRAGMA table_info(component_types)")
    columns = [column[1] for column in cursor.fetchall()]
    
    # Check if any of the new columns are missing
    columns_to_add = []
    if 'in_use' not in columns:
        columns_to_add.append('in_use')
    if 'mandatory' not in columns:
        columns_to_add.append('mandatory')
    if 'max_quantity' not in columns:
        columns_to_add.append('max_quantity')
    
    return columns_to_add

def migrate_component_types(cursor, conn):
    """Migrate the component_types table to add new columns"""
    # Check if the table needs migration
    columns_to_add = check_component_types_columns(cursor)

    if not columns_to_add:
        print("      → Table is compliant, all required columns present")
        return False

    # Check if the component_types table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='component_types'")
    if not cursor.fetchone():
        print("Error: component_types table not found in the database.")
        print("Make sure you're using the correct database file.")
        sys.exit(1)

    # Check if components table exists (needed for counting)
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='components'")
    if not cursor.fetchone():
        print("Error: components table not found in the database.")
        print("Make sure you're using the correct database file.")
        sys.exit(1)

    column_updates = []

    # Add new columns with specific default values
    if 'in_use' in columns_to_add:
        cursor.execute("ALTER TABLE component_types ADD COLUMN in_use INTEGER")
        # Set in_use to the actual count for each component type
        cursor.execute("SELECT component_type FROM component_types")
        component_types = [row[0] for row in cursor.fetchall()]

        # Update in_use count for each type
        for component_type in component_types:
            count = count_component_types_in_use(cursor, component_type)
            cursor.execute("UPDATE component_types SET in_use = ? WHERE component_type = ?",
                           (count, component_type))
        conn.commit()

    if 'mandatory' in columns_to_add:
        cursor.execute("ALTER TABLE component_types ADD COLUMN mandatory TEXT")
        conn.commit()
        column_updates.append("UPDATE component_types SET mandatory = 'No'")

    if 'max_quantity' in columns_to_add:
        cursor.execute("ALTER TABLE component_types ADD COLUMN max_quantity INTEGER")
        conn.commit()

    # Execute all update statements
    for update_sql in column_updates:
        cursor.execute(update_sql)

    conn.commit()
    print(f"      → Added {len(columns_to_add)} column(s) to component_types")
    return True

def check_component_types_time_columns(cursor):
    """Check if ComponentTypes table needs time-based fields migration"""
    cursor.execute("PRAGMA table_info(component_types)")
    columns = [column[1] for column in cursor.fetchall()]

    columns_to_add = []
    if 'service_interval_days' not in columns:
        columns_to_add.append('service_interval_days')
    if 'lifetime_expected_days' not in columns:
        columns_to_add.append('lifetime_expected_days')
    if 'threshold_km' not in columns:
        columns_to_add.append('threshold_km')
    if 'threshold_days' not in columns:
        columns_to_add.append('threshold_days')

    return columns_to_add

def migrate_component_types_time_fields(cursor, conn):
    """Add time-based fields to ComponentTypes table"""
    columns_to_add = check_component_types_time_columns(cursor)

    if not columns_to_add:
        print("      → Table is compliant, all time-based fields present")
        return False

    # Add new columns with NULL defaults
    if 'service_interval_days' in columns_to_add:
        cursor.execute("ALTER TABLE component_types ADD COLUMN service_interval_days INTEGER")

    if 'lifetime_expected_days' in columns_to_add:
        cursor.execute("ALTER TABLE component_types ADD COLUMN lifetime_expected_days INTEGER")

    if 'threshold_km' in columns_to_add:
        cursor.execute("ALTER TABLE component_types ADD COLUMN threshold_km INTEGER")

    if 'threshold_days' in columns_to_add:
        cursor.execute("ALTER TABLE component_types ADD COLUMN threshold_days INTEGER")

    conn.commit()
    print(f"      → Added {len(columns_to_add)} time-based column(s) to component_types")
    return True

def populate_component_types_thresholds(cursor, conn):
    """
    Populate threshold_km = 200 for existing component types with distance intervals.
    This ensures all component types have default thresholds.
    """
    # Check if component_types table has threshold_km column
    cursor.execute("PRAGMA table_info(component_types)")
    columns = [column[1] for column in cursor.fetchall()]

    if 'threshold_km' not in columns:
        print("      → Table is compliant, threshold_km column not yet added")
        return False

    # Check if any rows need updating
    cursor.execute("""
        SELECT COUNT(*)
        FROM component_types
        WHERE (service_interval IS NOT NULL OR expected_lifetime IS NOT NULL)
        AND threshold_km IS NULL
    """)
    rows_to_update = cursor.fetchone()[0]

    if rows_to_update == 0:
        print("      → Table is compliant, all threshold_km values already populated")
        return False

    # Perform the update
    cursor.execute("""
        UPDATE component_types
        SET threshold_km = 200
        WHERE (service_interval IS NOT NULL OR expected_lifetime IS NOT NULL)
        AND threshold_km IS NULL
    """)
    updated_count = cursor.rowcount
    conn.commit()

    print(f"      → Set threshold_km = 200 for {updated_count} component types")
    return True

def check_components_time_columns(cursor):
    """Check if Components table needs time-based fields migration"""
    cursor.execute("PRAGMA table_info(components)")
    columns = [column[1] for column in cursor.fetchall()]

    columns_to_add = []
    if 'service_interval_days' not in columns:
        columns_to_add.append('service_interval_days')
    if 'lifetime_expected_days' not in columns:
        columns_to_add.append('lifetime_expected_days')
    if 'threshold_km' not in columns:
        columns_to_add.append('threshold_km')
    if 'threshold_days' not in columns:
        columns_to_add.append('threshold_days')
    if 'lifetime_remaining_days' not in columns:
        columns_to_add.append('lifetime_remaining_days')
    if 'service_next_days' not in columns:
        columns_to_add.append('service_next_days')

    return columns_to_add

def migrate_components_time_fields(cursor, conn):
    """Add time-based fields to Components table and populate threshold_km"""
    columns_to_add = check_components_time_columns(cursor)

    if not columns_to_add:
        print("      → Table is compliant, all time-based fields present")
        return False

    # Add new columns with NULL defaults
    if 'service_interval_days' in columns_to_add:
        cursor.execute("ALTER TABLE components ADD COLUMN service_interval_days INTEGER")

    if 'lifetime_expected_days' in columns_to_add:
        cursor.execute("ALTER TABLE components ADD COLUMN lifetime_expected_days INTEGER")

    if 'threshold_km' in columns_to_add:
        cursor.execute("ALTER TABLE components ADD COLUMN threshold_km INTEGER")

    if 'threshold_days' in columns_to_add:
        cursor.execute("ALTER TABLE components ADD COLUMN threshold_days INTEGER")

    if 'lifetime_remaining_days' in columns_to_add:
        cursor.execute("ALTER TABLE components ADD COLUMN lifetime_remaining_days INTEGER")

    if 'service_next_days' in columns_to_add:
        cursor.execute("ALTER TABLE components ADD COLUMN service_next_days INTEGER")

    conn.commit()
    print(f"      → Added {len(columns_to_add)} time-based column(s) to components")
    return True

def populate_components_thresholds(cursor, conn):
    """
    Populate threshold_km = 200 for existing components with distance intervals.
    This ensures all components have default thresholds.
    """
    # Check if components table has threshold_km column
    cursor.execute("PRAGMA table_info(components)")
    columns = [column[1] for column in cursor.fetchall()]

    if 'threshold_km' not in columns:
        print("      → Table is compliant, threshold_km column not yet added")
        return False

    # Check if any rows need updating
    cursor.execute("""
        SELECT COUNT(*)
        FROM components
        WHERE (service_interval IS NOT NULL OR lifetime_expected IS NOT NULL)
        AND threshold_km IS NULL
    """)
    rows_to_update = cursor.fetchone()[0]

    if rows_to_update == 0:
        print("      → Table is compliant, all threshold_km values already populated")
        return False

    # Perform the update
    cursor.execute("""
        UPDATE components
        SET threshold_km = 200
        WHERE (service_interval IS NOT NULL OR lifetime_expected IS NOT NULL)
        AND threshold_km IS NULL
    """)
    updated_count = cursor.rowcount
    conn.commit()

    print(f"      → Set threshold_km = 200 for {updated_count} components")
    return True

def recalculate_distance_based_statuses(cursor, conn):
    """
    Recalculate lifetime_status and service_status for all components
    using the new threshold-based logic (distance only, no time).
    This converts old status strings to new ones and NULL to "Not defined".
    """
    # Fetch all components
    cursor.execute("""
        SELECT component_id, threshold_km, lifetime_remaining, service_next,
               lifetime_status, service_status
        FROM components
    """)
    components = cursor.fetchall()

    updated_count = 0

    for component in components:
        component_id, threshold_km, lifetime_remaining, service_next, old_lifetime_status, old_service_status = component
        needs_update = False
        new_lifetime_status = old_lifetime_status
        new_service_status = old_service_status

        # Recalculate lifetime_status
        if threshold_km is not None and lifetime_remaining is not None:
            if lifetime_remaining <= 0:
                new_lifetime_status = "Lifetime exceeded"
            elif lifetime_remaining < threshold_km:
                new_lifetime_status = "Due for replacement"
            else:
                new_lifetime_status = "OK"
        else:
            # If no threshold or no remaining value, set to "Not defined"
            new_lifetime_status = "Not defined"

        if old_lifetime_status != new_lifetime_status:
            needs_update = True

        # Recalculate service_status
        if threshold_km is not None and service_next is not None:
            if service_next <= 0:
                new_service_status = "Service interval exceeded"
            elif service_next < threshold_km:
                new_service_status = "Due for service"
            else:
                new_service_status = "OK"
        else:
            # If no threshold or no service_next value, set to "Not defined"
            new_service_status = "Not defined"

        if old_service_status != new_service_status:
            needs_update = True

        # Update if status changed
        if needs_update:
            cursor.execute("""
                UPDATE components
                SET lifetime_status = ?, service_status = ?
                WHERE component_id = ?
            """, (new_lifetime_status, new_service_status, component_id))
            updated_count += 1

    conn.commit()
    if updated_count > 0:
        print(f"      → Recalculated statuses for {updated_count} components")
    return updated_count > 0

def check_services_workplan_column(cursor):
    """Check if Services table needs workplan_id column"""
    cursor.execute("PRAGMA table_info(services)")
    columns = [column[1] for column in cursor.fetchall()]

    columns_to_add = []
    if 'workplan_id' not in columns:
        columns_to_add.append('workplan_id')

    return columns_to_add

def check_incidents_workplan_column(cursor):
    """Check if Incidents table needs workplan_id column"""
    cursor.execute("PRAGMA table_info(incidents)")
    columns = [column[1] for column in cursor.fetchall()]

    columns_to_add = []
    if 'workplan_id' not in columns:
        columns_to_add.append('workplan_id')

    return columns_to_add

def migrate_services_workplan_link(cursor, conn):
    """Add workplan_id column to Services table for workplan hub integration"""
    columns_to_add = check_services_workplan_column(cursor)

    if not columns_to_add:
        print("      → Table is compliant, workplan_id column already present")
        return False

    cursor.execute("ALTER TABLE services ADD COLUMN workplan_id VARCHAR")
    conn.commit()
    print("      → Added workplan_id column to services table")
    return True

def migrate_incidents_workplan_link(cursor, conn):
    """Add workplan_id column to Incidents table for workplan hub integration"""
    # An empty list means no service integration columns are missing, so step 12 has already run
    if not check_services_integration_columns(cursor):
        print("      → Skipping, superseded by service integration (links are derived through services)")
        return False

    columns_to_add = check_incidents_workplan_column(cursor)

    if not columns_to_add:
        print("      → Table is compliant, workplan_id column already present")
        return False

    cursor.execute("ALTER TABLE incidents ADD COLUMN workplan_id VARCHAR")
    conn.commit()
    print("      → Added workplan_id column to incidents table")
    return True

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
    """Resolve bike and component names, marking components that no longer exist"""
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

def insert_planned_service_for_migration(cursor, component_id, description, workplan_id, incident_id):
    """Insert a planned service with no date, bike or distance. Returns False if the component is deleted or retired"""
    cursor.execute("SELECT component_name, installation_status FROM components WHERE component_id = ?", (component_id,))
    row = cursor.fetchone()
    if not row or row[1] == "Retired":
        return False

    cursor.execute("""INSERT INTO services (service_id, component_id, component_name, bike_id,
                                            service_date, distance_marker, description, workplan_id,
                                            status, incident_id, planned_date)
                      VALUES (?, ?, ?, NULL, NULL, NULL, ?, ?, 'Planned', ?, NULL)""",
                   (generate_unique_id(), component_id, row[0], description, workplan_id, incident_id))
    return True

def migrate_workplans_to_planned_services(cursor, conn):
    """Convert affected components on planned workplans into planned services, preserve names in descriptions"""
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

        planned_count = 0
        if workplan_status == "Planned":
            not_converted_names = []
            for component_id, component_name in zip(affected_component_ids, component_names):
                if component_id in missing_component_ids:
                    not_converted_names.append(component_name)
                    continue
                cursor.execute("SELECT 1 FROM services WHERE workplan_id = ? AND component_id = ?",
                               (workplan_id, component_id))
                if cursor.fetchone():
                    continue
                if insert_planned_service_for_migration(cursor, component_id,
                                                        "Planned service (migrated from workplan)",
                                                        workplan_id, None):
                    planned_count += 1
                else:
                    not_converted_names.append(f"{component_name} (retired)")

            note_parts = []
            if not_converted_names:
                note_parts.append(f"components without planned service: {', '.join(not_converted_names)}")
        else:
            note_parts = []
            if bike_name:
                note_parts.append(f"bike: {bike_name}")
            if component_names:
                note_parts.append(f"components: {', '.join(component_names)}")

        if note_parts and "Migrated from earlier version" not in (description or ""):
            migration_note = f"\n\nMigrated from earlier version, affected {'; '.join(note_parts)}"
            cursor.execute("UPDATE workplans SET workplan_description = ? WHERE workplan_id = ?",
                           ((description or "") + migration_note, workplan_id))

        converted += 1
        print(f"      → Converted workplan {workplan_id} ({workplan_status}, {planned_count} planned service(s) added)")

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

        cursor.execute("SELECT COUNT(*) FROM services WHERE workplan_id = ? AND incident_id = ?",
                       (workplan_id, incident_id))
        linked = cursor.fetchone()[0]

        if linked == 0 and affected_component_ids:
            placeholders = ",".join("?" * len(affected_component_ids))
            cursor.execute(f"""UPDATE services SET incident_id = ?
                               WHERE workplan_id = ? AND incident_id IS NULL
                               AND component_id IN ({placeholders})""",
                           [incident_id, workplan_id] + affected_component_ids)
            linked = cursor.rowcount

        if linked == 0 and affected_component_ids and workplan_status == "Planned" and incident_status == "Open":
            for component_id in affected_component_ids:
                if insert_planned_service_for_migration(cursor, component_id,
                                                        "Planned service (migrated from incident)",
                                                        workplan_id, incident_id):
                    linked += 1

        if linked == 0 and "Migrated from earlier version" not in (description or ""):
            migration_note = f"\n\nMigrated from earlier version, previously linked to workplan {workplan_id}"
            cursor.execute("UPDATE incidents SET incident_description = ? WHERE incident_id = ?",
                           ((description or "") + migration_note, incident_id))

        converted += 1
        print(f"      → Converted incident {incident_id} ({linked} service link(s))")

    conn.commit()
    print(f"      → Converted {converted} incident(s)")
    return converted > 0

def check_workplans_name_column(cursor):
    """Check if workplans table needs the workplan_name column"""
    cursor.execute("PRAGMA table_info(workplans)")
    columns = [column[1] for column in cursor.fetchall()]

    return 'workplan_name' not in columns

def migrate_workplans_name_column(cursor, conn):
    """Add the optional user given name to the workplans table, existing workplans keep the generated title"""
    if not check_workplans_name_column(cursor):
        print("      → Table is compliant, workplan_name column already present")
        return False

    cursor.execute("ALTER TABLE workplans ADD COLUMN workplan_name TEXT")
    conn.commit()
    print("      → Added workplan_name column to workplans table")
    return True

def migrate_drop_workplan_affected_columns(cursor, conn):
    """Rebuild workplans table without the affected bike/component columns"""
    if not check_workplans_affected_columns(cursor):
        print("      → Table is compliant, affected columns already dropped from workplans")
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
        print("      → Table is compliant, workplan_id already dropped from incidents")
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

def run_all_migrations(cursor, conn):
    """Run every migration step in order and return the list of steps that changed something"""
    migrations_performed = []

    print("\n" + "="*70)
    print("STARTING DATABASE MIGRATION")
    print("="*70)

    # Create the 'incidents' table if it doesn't exist
    print("\n[1/17] Checking incidents table...")
    incidents_created = create_incidents_table(cursor)
    if incidents_created:
        migrations_performed.append("✓ Created incidents table")

    # Create the 'workplans' table if it doesn't exist
    print("\n[2/17] Checking workplans table...")
    workplans_created = create_workplans_table(cursor)
    if workplans_created:
        migrations_performed.append("✓ Created workplans table")

    # Create the 'collections' table if it doesn't exist
    print("\n[3/17] Checking collections table...")
    collections_created = create_collections_table(cursor)
    if collections_created:
        migrations_performed.append("✓ Created collections table")

    # Migrate component_types table if needed
    print("\n[4/17] Checking component_types table (mandatory/max_quantity fields)...")
    component_types_updated = migrate_component_types(cursor, conn)
    if component_types_updated:
        migrations_performed.append("✓ Updated component_types table (mandatory/max_quantity)")

    # Migrate ComponentTypes with time-based fields
    print("\n[5/17] Checking component_types table (time-based fields)...")
    component_types_time_updated = migrate_component_types_time_fields(cursor, conn)
    if component_types_time_updated:
        migrations_performed.append("✓ Added time-based fields to component_types")

    # Populate threshold_km for ComponentTypes
    print("\n[6/17] Populating threshold_km for component types...")
    component_types_thresholds_populated = populate_component_types_thresholds(cursor, conn)
    if component_types_thresholds_populated:
        migrations_performed.append("✓ Populated threshold_km for component_types")

    # Migrate Components with time-based fields
    print("\n[7/17] Checking components table (time-based fields)...")
    components_time_updated = migrate_components_time_fields(cursor, conn)
    if components_time_updated:
        migrations_performed.append("✓ Added time-based fields to components")

    # Populate threshold_km for Components
    print("\n[8/17] Populating threshold_km for components...")
    components_thresholds_populated = populate_components_thresholds(cursor, conn)
    if components_thresholds_populated:
        migrations_performed.append("✓ Populated threshold_km for components")

    # Recalculate component statuses with new threshold logic
    # Only needed if threshold and time-based fields were just added in steps 5 or 7
    print("\n[9/17] Recalculating component statuses...")
    if component_types_time_updated or components_time_updated:
        statuses_recalculated = recalculate_distance_based_statuses(cursor, conn)
        if statuses_recalculated:
            migrations_performed.append("✓ Recalculated component statuses")
        else:
            print("      → No status updates needed")
    else:
        print("      → Skipping, time-based fields already present")

    # Add workplan_id to Services table
    print("\n[10/17] Checking services table (workplan hub integration)...")
    services_workplan_link = migrate_services_workplan_link(cursor, conn)
    if services_workplan_link:
        migrations_performed.append("✓ Added workplan_id to services table")

    # Add workplan_id to Incidents table (skipped once service integration is applied)
    print("\n[11/17] Checking incidents table (workplan hub integration)...")
    incidents_workplan_link = migrate_incidents_workplan_link(cursor, conn)
    if incidents_workplan_link:
        migrations_performed.append("✓ Added workplan_id to incidents table")

    # NEW: Service integration (issue #351). Steps 14 and 15 must run before 16 drops the columns they read
    print("\n[12/17] Checking services table (service integration columns)...")
    if migrate_services_integration_columns(cursor, conn):
        migrations_performed.append("✓ Added status, incident_id and planned_date to services (service integration)")

    print("\n[13/17] Checking component_history table (notes column)...")
    if migrate_component_history_notes(cursor, conn):
        migrations_performed.append("✓ Added notes to component_history (service integration)")

    print("\n[14/17] Converting workplan affected components to planned services...")
    if migrate_workplans_to_planned_services(cursor, conn):
        migrations_performed.append("✓ Converted workplans to planned services (service integration)")

    print("\n[15/17] Rebuilding incident links through services...")
    if migrate_incident_links_to_services(cursor, conn):
        migrations_performed.append("✓ Rebuilt incident links through services (service integration)")

    print("\n[16/17] Dropping superseded workplan and incident columns...")
    workplans_columns_dropped = migrate_drop_workplan_affected_columns(cursor, conn)
    incidents_column_dropped = migrate_drop_incident_workplan_column(cursor, conn)
    if workplans_columns_dropped or incidents_column_dropped:
        migrations_performed.append("✓ Dropped superseded workplan and incident columns (service integration)")

    # Runs after the rebuild above, which recreates the workplans table from a fixed column list
    print("\n[17/17] Checking workplans table (workplan name)...")
    if migrate_workplans_name_column(cursor, conn):
        migrations_performed.append("✓ Added workplan_name to workplans table (service integration)")

    return migrations_performed

def migrate_database():
    """Main function to handle the database migration."""
    print("=== Velo Supervisor 2000 Database Migration Tool ===\n")

    # Get database path
    db_path = prompt_for_db_path()
    print(f"\nProceeding with migration on database: {db_path}")

    # Safety check - require explicit backup confirmation
    print("\nIMPORTANT: This script will modify your database schema.")
    print("Please ensure you have taken a backup of your database before proceeding.")
    confirmation = input("Have you taken a backup? (yes/no): ").strip().lower()

    if confirmation != "yes":
        print("Migration cancelled. Please take a backup and run the script again.")
        sys.exit(1)

    # Connect to the database
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        migrations_performed = run_all_migrations(cursor, conn)

        # Print summary
        print("\n" + "="*70)
        print("MIGRATION SUMMARY")
        print("="*70)

        if len(migrations_performed) == 0:
            print("\n✓ No migrations were needed - your database is already up to date!")
        else:
            print(f"\n✓ Successfully applied {len(migrations_performed)} migration(s):\n")
            for migration in migrations_performed:
                print(f"  {migration}")

        print("\n" + "="*70)
        print("MIGRATION COMPLETED SUCCESSFULLY")
        print("="*70 + "\n")
        
    except sqlite3.Error as e:
        print(f"\nDatabase error: {e}")
        print("Migration failed. Some changes may have been applied.")
        print("You can safely re-run the migration script - already-completed steps will be skipped.")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        print("Migration failed. Some changes may have been applied.")
        print("You can safely re-run the migration script - already-completed steps will be skipped.")
        sys.exit(1)
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    migrate_database()