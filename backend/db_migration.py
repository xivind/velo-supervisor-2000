#!/usr/bin/env python3
"""Script to migrate the database, including adding new tables and fields"""

import sqlite3
import sys
import os

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
    print("Checking for the 'incidents' table...")
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='incidents'")
    if not cursor.fetchone():
        print("Table 'incidents' not found. Creating it now...")
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
        print("Table 'incidents' created successfully.")
        return True
    else:
        print("Table 'incidents' already exists. Skipping creation.")
        return False

def create_workplans_table(cursor):
    """Creates the workplans table if it doesn't exist."""
    print("Checking for the 'workplans' table...")
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='workplans'")
    if not cursor.fetchone():
        print("Table 'workplans' not found. Creating it now...")
        cursor.execute("""
            CREATE TABLE workplans (
                workplan_id TEXT PRIMARY KEY UNIQUE,
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
        print("Table 'workplans' created successfully.")
        return True
    else:
        print("Table 'workplans' already exists. Skipping creation.")
        return False

def create_collections_table(cursor):
    """Creates the collections table if it doesn't exist."""
    print("Checking for the 'collections' table...")
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='collections'")
    if not cursor.fetchone():
        print("Table 'collections' not found. Creating it now...")
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
        print("Table 'collections' created successfully.")
        return True
    else:
        print("Table 'collections' already exists. Skipping creation.")
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
        print("The component_types table already has all required columns.")
        print("No migration needed for component_types.")
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
        
    print("\nMigrating component_types table...")
    column_updates = []
    
    # Add new columns with specific default values
    if 'in_use' in columns_to_add:
        print("Adding 'in_use' column...")
        cursor.execute("ALTER TABLE component_types ADD COLUMN in_use INTEGER")
        # Set in_use to the actual count for each component type
        print("Counting components for each component type...")
        # Get all component types
        cursor.execute("SELECT component_type FROM component_types")
        component_types = [row[0] for row in cursor.fetchall()]
        
        # Update in_use count for each type
        for component_type in component_types:
            count = count_component_types_in_use(cursor, component_type)
            print(f"Component type '{component_type}' is used by {count} components")
            cursor.execute("UPDATE component_types SET in_use = ? WHERE component_type = ?", 
                           (count, component_type))
        conn.commit()
    
    if 'mandatory' in columns_to_add:
        print("Adding 'mandatory' column...")
        cursor.execute("ALTER TABLE component_types ADD COLUMN mandatory TEXT")
        # Set mandatory to "No" for existing records
        conn.commit()
        column_updates.append("UPDATE component_types SET mandatory = 'No'")
    
    if 'max_quantity' in columns_to_add:
        print("Adding 'max_quantity' column...")
        cursor.execute("ALTER TABLE component_types ADD COLUMN max_quantity INTEGER")
        conn.commit()
        # No update needed - SQLite defaults new columns to NULL
        print("Column 'max_quantity' added with NULL values for existing records")
    
    # Execute all update statements
    for update_sql in column_updates:
        print(f"Executing: {update_sql}")
        cursor.execute(update_sql)
    
    conn.commit()
    print("\nComponent types migration completed successfully.")
    print("New columns have been added to the component_types table.")
    print("Component counts have been populated in the 'in_use' column.")
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
        print("ComponentTypes table already has all time-based fields.")
        return False

    print("\nMigrating ComponentTypes table with time-based fields...")

    # Add new columns with NULL defaults
    if 'service_interval_days' in columns_to_add:
        print("Adding 'service_interval_days' column...")
        cursor.execute("ALTER TABLE component_types ADD COLUMN service_interval_days INTEGER")

    if 'lifetime_expected_days' in columns_to_add:
        print("Adding 'lifetime_expected_days' column...")
        cursor.execute("ALTER TABLE component_types ADD COLUMN lifetime_expected_days INTEGER")

    if 'threshold_km' in columns_to_add:
        print("Adding 'threshold_km' column...")
        cursor.execute("ALTER TABLE component_types ADD COLUMN threshold_km INTEGER")

    if 'threshold_days' in columns_to_add:
        print("Adding 'threshold_days' column...")
        cursor.execute("ALTER TABLE component_types ADD COLUMN threshold_days INTEGER")

    conn.commit()
    print("ComponentTypes time-based fields migration completed.")
    return True

def populate_component_types_thresholds(cursor, conn):
    """
    Populate threshold_km = 200 for existing component types with distance intervals.
    This ensures all component types have default thresholds.
    """
    print("\nPopulating threshold_km for existing component types...")

    cursor.execute("""
        UPDATE component_types
        SET threshold_km = 200
        WHERE (service_interval IS NOT NULL OR expected_lifetime IS NOT NULL)
        AND threshold_km IS NULL
    """)
    updated_count = cursor.rowcount
    conn.commit()

    if updated_count > 0:
        print(f"Set threshold_km = 200 for {updated_count} component types with distance intervals")
        return True
    else:
        print("All component types already have threshold_km set or no distance intervals defined")
        return False

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
        print("Components table already has all time-based fields.")
        return False

    print("\nMigrating Components table with time-based fields...")

    # Add new columns with NULL defaults
    if 'service_interval_days' in columns_to_add:
        print("Adding 'service_interval_days' column...")
        cursor.execute("ALTER TABLE components ADD COLUMN service_interval_days INTEGER")

    if 'lifetime_expected_days' in columns_to_add:
        print("Adding 'lifetime_expected_days' column...")
        cursor.execute("ALTER TABLE components ADD COLUMN lifetime_expected_days INTEGER")

    if 'threshold_km' in columns_to_add:
        print("Adding 'threshold_km' column...")
        cursor.execute("ALTER TABLE components ADD COLUMN threshold_km INTEGER")

    if 'threshold_days' in columns_to_add:
        print("Adding 'threshold_days' column...")
        cursor.execute("ALTER TABLE components ADD COLUMN threshold_days INTEGER")

    if 'lifetime_remaining_days' in columns_to_add:
        print("Adding 'lifetime_remaining_days' column...")
        cursor.execute("ALTER TABLE components ADD COLUMN lifetime_remaining_days INTEGER")

    if 'service_next_days' in columns_to_add:
        print("Adding 'service_next_days' column...")
        cursor.execute("ALTER TABLE components ADD COLUMN service_next_days INTEGER")

    conn.commit()
    print("Components time-based fields migration completed.")
    print("Note: New fields have NULL defaults - threshold_km will be populated in next step")
    return True

def populate_components_thresholds(cursor, conn):
    """
    Populate threshold_km = 200 for existing components with distance intervals.
    This ensures all components have default thresholds.
    """
    print("\nPopulating threshold_km for existing components...")

    cursor.execute("""
        UPDATE components
        SET threshold_km = 200
        WHERE (service_interval IS NOT NULL OR lifetime_expected IS NOT NULL)
        AND threshold_km IS NULL
    """)
    updated_count = cursor.rowcount
    conn.commit()

    if updated_count > 0:
        print(f"Set threshold_km = 200 for {updated_count} components with distance intervals")
        return True
    else:
        print("All components already have threshold_km set or no distance intervals defined")
        return False

def recalculate_distance_based_statuses(cursor, conn):
    """
    Recalculate lifetime_status and service_status for all components
    using the new threshold-based logic (distance only, no time).
    This converts old status strings to new ones and NULL to "Not defined".
    """
    print("\nRecalculating component statuses with new threshold logic...")

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
    print(f"Recalculated statuses for {updated_count} components")
    print("Note: Components without threshold_km or NULL values now have 'Not defined' status")
    return updated_count > 0

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
        migrations_performed = []
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        print("\n" + "="*70)
        print("STARTING DATABASE MIGRATION")
        print("="*70)

        # Create the 'incidents' table if it doesn't exist
        print("\n[1/9] Checking incidents table...")
        incidents_created = create_incidents_table(cursor)
        if incidents_created:
            migrations_performed.append("✓ Created incidents table")
        else:
            print("      → Already exists, skipping")

        # Create the 'workplans' table if it doesn't exist
        print("\n[2/9] Checking workplans table...")
        workplans_created = create_workplans_table(cursor)
        if workplans_created:
            migrations_performed.append("✓ Created workplans table")
        else:
            print("      → Already exists, skipping")

        # Create the 'collections' table if it doesn't exist
        print("\n[3/9] Checking collections table...")
        collections_created = create_collections_table(cursor)
        if collections_created:
            migrations_performed.append("✓ Created collections table")
        else:
            print("      → Already exists, skipping")

        # Migrate component_types table if needed
        print("\n[4/9] Checking component_types table (mandatory/max_quantity fields)...")
        component_types_updated = migrate_component_types(cursor, conn)
        if component_types_updated:
            migrations_performed.append("✓ Updated component_types table (mandatory/max_quantity)")
        else:
            print("      → Already up to date, skipping")

        # NEW: Migrate ComponentTypes with time-based fields
        print("\n[5/9] Migrating component_types table (time-based fields)...")
        component_types_time_updated = migrate_component_types_time_fields(cursor, conn)
        if component_types_time_updated:
            migrations_performed.append("✓ Added time-based fields to component_types")
        else:
            print("      → Already up to date, skipping")

        # NEW: Populate threshold_km for ComponentTypes
        print("\n[6/9] Populating threshold_km for component types...")
        component_types_thresholds_populated = populate_component_types_thresholds(cursor, conn)
        if component_types_thresholds_populated:
            migrations_performed.append("✓ Populated threshold_km for component_types")
        else:
            print("      → Already populated or no data to update")

        # NEW: Migrate Components with time-based fields
        print("\n[7/9] Migrating components table (time-based fields)...")
        components_time_updated = migrate_components_time_fields(cursor, conn)
        if components_time_updated:
            migrations_performed.append("✓ Added time-based fields to components")
        else:
            print("      → Already up to date, skipping")

        # NEW: Populate threshold_km for Components
        print("\n[8/9] Populating threshold_km for components...")
        components_thresholds_populated = populate_components_thresholds(cursor, conn)
        if components_thresholds_populated:
            migrations_performed.append("✓ Populated threshold_km for components")
        else:
            print("      → Already populated or no data to update")

        # NEW: Recalculate component statuses with new threshold logic
        print("\n[9/9] Recalculating component statuses...")
        statuses_recalculated = recalculate_distance_based_statuses(cursor, conn)
        if statuses_recalculated:
            migrations_performed.append("✓ Recalculated component statuses")
        else:
            print("      → No status updates needed")

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
        print("Migration failed. No changes were applied.")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        print("Migration failed. No changes were applied.")
        sys.exit(1)
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    migrate_database()