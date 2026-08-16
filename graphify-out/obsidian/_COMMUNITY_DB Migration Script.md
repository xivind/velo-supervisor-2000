---
type: community
members: 41
---

# DB Migration Script

**Members:** 41 nodes

## Members
- [[Add time-based fields to ComponentTypes table]] - rationale - backend/db_migration.py
- [[Add time-based fields to Components table and populate threshold_km]] - rationale - backend/db_migration.py
- [[Add workplan_id column to Incidents table for workplan hub integration]] - rationale - backend/db_migration.py
- [[Add workplan_id column to Services table for workplan hub integration]] - rationale - backend/db_migration.py
- [[Check if ComponentTypes table needs time-based fields migration]] - rationale - backend/db_migration.py
- [[Check if Components table needs time-based fields migration]] - rationale - backend/db_migration.py
- [[Check if Incidents table needs workplan_id column]] - rationale - backend/db_migration.py
- [[Check if Services table needs workplan_id column]] - rationale - backend/db_migration.py
- [[Check if the component_types table needs migration]] - rationale - backend/db_migration.py
- [[Count how many components use a specific component type]] - rationale - backend/db_migration.py
- [[Creates the collections table if it doesn't exist.]] - rationale - backend/db_migration.py
- [[Creates the incidents table if it doesn't exist.]] - rationale - backend/db_migration.py
- [[Creates the workplans table if it doesn't exist.]] - rationale - backend/db_migration.py
- [[Main function to handle the database migration.]] - rationale - backend/db_migration.py
- [[Migrate the component_types table to add new columns]] - rationale - backend/db_migration.py
- [[Populate threshold_km = 200 for existing component types with distance…]] - rationale - backend/db_migration.py
- [[Populate threshold_km = 200 for existing components with distance intervals.…]] - rationale - backend/db_migration.py
- [[Prompt user for database path or filename and verify it exists]] - rationale - backend/db_migration.py
- [[Recalculate lifetime_status and service_status for all components using the new…]] - rationale - backend/db_migration.py
- [[Search for a database file in the user's home directory and subdirectories]] - rationale - backend/db_migration.py
- [[check_component_types_columns()]] - code - backend/db_migration.py
- [[check_component_types_time_columns()]] - code - backend/db_migration.py
- [[check_components_time_columns()]] - code - backend/db_migration.py
- [[check_incidents_workplan_column()]] - code - backend/db_migration.py
- [[check_services_workplan_column()]] - code - backend/db_migration.py
- [[count_component_types_in_use()]] - code - backend/db_migration.py
- [[create_collections_table()]] - code - backend/db_migration.py
- [[create_incidents_table()]] - code - backend/db_migration.py
- [[create_workplans_table()]] - code - backend/db_migration.py
- [[db_migration.py]] - code - backend/db_migration.py
- [[find_database_file()]] - code - backend/db_migration.py
- [[migrate_component_types()]] - code - backend/db_migration.py
- [[migrate_component_types_time_fields()]] - code - backend/db_migration.py
- [[migrate_components_time_fields()]] - code - backend/db_migration.py
- [[migrate_database()]] - code - backend/db_migration.py
- [[migrate_incidents_workplan_link()]] - code - backend/db_migration.py
- [[migrate_services_workplan_link()]] - code - backend/db_migration.py
- [[populate_component_types_thresholds()]] - code - backend/db_migration.py
- [[populate_components_thresholds()]] - code - backend/db_migration.py
- [[prompt_for_db_path()]] - code - backend/db_migration.py
- [[recalculate_distance_based_statuses()]] - code - backend/db_migration.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/DB_Migration_Script
SORT file.name ASC
```
