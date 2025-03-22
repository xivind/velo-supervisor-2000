#!/usr/bin/env python3
"""Script to migrate the database to add new component type fields"""

import sqlite3
import json
import sys

def read_config():
    """Function to read configuration file"""
    with open('config.json', 'r', encoding='utf-8') as file:
        config = json.load(file)
    return config

def migrate_component_types():
    # Safety check - require explicit backup confirmation
    print("IMPORTANT: This script will modify your database schema.")
    print("Please ensure you have taken a backup of your database before proceeding.")
    confirmation = input("Have you taken a backup? (yes/no): ").strip().lower()
    
    if confirmation != "yes":
        print("Migration cancelled. Please take a backup and run the script again.")
        sys.exit(1)
    
    config = read_config()
    db_path = config['db_path']
    
    print(f"Proceeding with migration on database: {db_path}")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check if columns already exist
    cursor.execute("PRAGMA table_info(component_types)")
    columns = [column[1] for column in cursor.fetchall()]
    
    column_updates = []
    
    # Add new columns with specific default values
    if 'in_use' not in columns:
        print("Adding 'in_use' column...")
        cursor.execute("ALTER TABLE component_types ADD COLUMN in_use TEXT")
        # Leave in_use blank for existing records
    else:
        print("Column 'in_use' already exists, skipping.")
    
    if 'mandatory' not in columns:
        print("Adding 'mandatory' column...")
        cursor.execute("ALTER TABLE component_types ADD COLUMN mandatory TEXT")
        # Set mandatory to "No" for existing records
        column_updates.append("UPDATE component_types SET mandatory = 'No'")
    else:
        print("Column 'mandatory' already exists, skipping.")
    
    if 'max_quantity' not in columns:
        print("Adding 'max_quantity' column...")
        cursor.execute("ALTER TABLE component_types ADD COLUMN max_quantity INTEGER")
        # Leave in_use blank for existing records
    else:
        print("Column 'max_quantity' already exists, skipping.")
    
    # Execute all update statements
    for update_sql in column_updates:
        print(f"Executing: {update_sql}")
        cursor.execute(update_sql)
    
    conn.commit()
    conn.close()
    
    print("\nDatabase migration completed successfully.")
    print("New columns have been added to the component_types table.")

if __name__ == "__main__":
    migrate_component_types()