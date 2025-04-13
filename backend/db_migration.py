#!/usr/bin/env python3
"""Script to migrate the database, including adding new tables and fields"""

import sqlite3
import json
import sys
import os

def read_config():
    """Function to read configuration file"""
    try:
        with open('config.json', 'r', encoding='utf-8') as file:
            config = json.load(file)
        return config
    except FileNotFoundError:
        print("Warning: config.json file not found.")
        return None
    except json.JSONDecodeError:
        print("Error: config.json file is not valid JSON.")
        return None

def get_db_path():
    """Get database path from config or by manual entry"""
    config = read_config()
    
    if config and 'db_path' in config:
        db_path = config['db_path']
        print(f"Database path found in config: {db_path}")
        
        # Verify that the database exists
        if not os.path.exists(db_path):
            print(f"Warning: Database file not found at {db_path}")
            manual_entry = input("Would you like to enter the database path manually? (yes/no): ").strip().lower()
            if manual_entry == "yes":
                return prompt_for_db_path()
            else:
                print("Migration cancelled.")
                sys.exit(1)
        
        return db_path
    else:
        print("No database configuration found.")
        return prompt_for_db_path()

def prompt_for_db_path():
    """Prompt user for database path and verify it exists"""
    while True:
        db_path = input("Please enter the full path to your SQLite database file: ").strip()
        
        if not db_path:
            print("No path entered. Migration cancelled.")
            sys.exit(1)
        
        if os.path.exists(db_path):
            # Verify it's a SQLite database
            try:
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                cursor.execute("PRAGMA database_list")
                conn.close()
                return db_path
            except sqlite3.Error:
                print("Error: The file exists but does not appear to be a valid SQLite database.")
                continue
        else:
            print(f"Error: File not found at '{db_path}'")
            retry = input("Would you like to try again? (yes/no): ").strip().lower()
            if retry != "yes":
                print("Migration cancelled.")
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
                affected_component_ids TEXT,
                affected_bike_id TEXT,
                incident_description TEXT,
                resolution_date TEXT,
                resolution_notes TEXT
            )
        """)
        print("Table 'incidents' created successfully.")
    else:
        print("Table 'incidents' already exists. Skipping creation.")

def migrate_component_types(cursor, conn):
    """Migrate the component_types table to add new columns"""
    # Safety check - require explicit backup confirmation
    print("IMPORTANT: This script will modify your database schema.")
    print("Please ensure you have taken a backup of your database before proceeding.")
    confirmation = input("Have you taken a backup? (yes/no): ").strip().lower()
    
    if confirmation != "yes":
        print("Migration cancelled. Please take a backup and run the script again.")
        sys.exit(1)
    
    try:
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
            
        # Check if columns already exist
        cursor.execute("PRAGMA table_info(component_types)")
        columns = [column[1] for column in cursor.fetchall()]
        
        column_updates = []
        
        # Add new columns with specific default values
        if 'in_use' not in columns:
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
        else:
            print("Column 'in_use' already exists, skipping.")
        
        if 'mandatory' not in columns:
            print("Adding 'mandatory' column...")
            cursor.execute("ALTER TABLE component_types ADD COLUMN mandatory TEXT")
            # Set mandatory to "No" for existing records
            conn.commit()
            column_updates.append("UPDATE component_types SET mandatory = 'No'")
        else:
            print("Column 'mandatory' already exists, skipping.")
        
        if 'max_quantity' not in columns:
            print("Adding 'max_quantity' column...")
            cursor.execute("ALTER TABLE component_types ADD COLUMN max_quantity INTEGER")
            conn.commit()
            # No update needed - SQLite defaults new columns to NULL
            print("Column 'max_quantity' added with NULL values for existing records")
        else:
            print("Column 'max_quantity' already exists, skipping.")
        
        # Execute all update statements
        for update_sql in column_updates:
            print(f"Executing: {update_sql}")
            cursor.execute(update_sql)
        
        conn.commit()
        print("\nComponent types migration completed successfully.")
        print("New columns have been added to the component_types table.")
        print("Component counts have been populated in the 'in_use' column.")
        
    except Exception as e:
        conn.rollback()
        print(f"Error during migration: {str(e)}")
        print("Migration failed, database rolled back to previous state.")
        sys.exit(1)

def migrate_database():
    """Main function to handle the database migration."""
    db_path = get_db_path()
    print(f"Proceeding with migration on database: {db_path}")
    
    # Connect to the database
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Create the 'incidents' table if it doesn't exist
        create_incidents_table(cursor)
        conn.commit()
        
        # Migrate component_types table
        migrate_component_types(cursor, conn)
        
        print("\nDatabase migration completed successfully!")
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    migrate_database()