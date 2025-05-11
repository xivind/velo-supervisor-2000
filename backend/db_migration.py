#!/usr/bin/env python3
"""Script to migrate the database, including adding new tables and fields"""

import sqlite3
import json
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
        migrations_performed = 0
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Create the 'incidents' table if it doesn't exist
        incidents_created = create_incidents_table(cursor)
        if incidents_created:
            migrations_performed += 1
        
        # Migrate component_types table if needed
        component_types_updated = migrate_component_types(cursor, conn)
        if component_types_updated:
            migrations_performed += 1
        
        if migrations_performed == 0:
            print("\nNo migrations were needed - your database is already up to date!")
        else:
            print(f"\nDatabase migration completed successfully! {migrations_performed} changes applied.")
        
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