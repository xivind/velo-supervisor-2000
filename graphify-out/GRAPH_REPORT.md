# Graph Report - velo-supervisor-2000  (2026-09-27)

## Corpus Check
- 41 files · ~163,304 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 12 file(s) not represented in the graph (top: (none) 5, .example 1, .sqlite 1)

## Summary
- 984 nodes · 1581 edges · 119 communities (74 shown, 45 thin omitted)
- Extraction: 82% EXTRACTED · 18% INFERRED · 0% AMBIGUOUS · INFERRED: 291 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `59003d83`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- .get_component_overview
- run_all_migrations
- Bike Details Template
- .calculate_collection_status
- Meta
- scheduler.py
- BusinessLogic
- main.js
- get
- CLAUDE.md
- generate_unique_id
- Task 7: Routes
- DatabaseManager
- Database Migration Script (db_migration.py)
- .count_component_types_in_use
- validateDateInput
- sortColumn
- main.py
- Service integration: incidents, workplans and services
- .write_delete_record
- middleware.py
- get_filtered_log
- Python Requirements List
- .read_single_bike
- .read_component
- bike_details
- update_config
- Task 10: Workplan modal and workplans list
- version.py
- CLAUDE.md
- utils.py
- validateComponentThresholds
- migrate_components_time_fields
- helpTopics Data Object
- conftest.py
- Issues found (none blocking)
- insert_planned_service_for_migration
- seed_component
- test_migration.py
- db_migration.py
- .process_service_records
- validate_date_format
- migrate_component_history_notes
- check_services_integration_columns
- File map
- migrate_workplans_to_planned_services
- .read_oldest_history_record
- database_manager.py
- config_overview
- migrate_component_types
- migrate_services_workplan_link
- http_exception_handler
- Test Protocol: Planned services, workplans and incidents
- .write_component_service_status
- prompt_for_db_path
- cleanup
- renderPreview
- .read_subset_service_record
- .read_date_oldest_ride
- initializeWorkplanTable
- Request
- .read_all_components
- .read_subset_component_history
- .read_matching_rides
- .read_all_components_objects
- Git Workflow Rules
- .read_all_incidents
- code-reviewer.md
- backup_db.sh
- create-container-vs2000.sh
- [Source Agent] -> [Target Agent] Handover
- Quick Swap Components
- Config Page (Strava Sync)
- Strava profile:read_all Scope Troubleshooting
- Dev/Staging/Master Branch Workflow
- Changelog Section
- Error Page Illustration
- Velo Supervisor Fox Mechanic Logo
- Component Types Page
- Confirm Action Modal
- Documentation Modal
- Edit Installation Record Modal
- Loading Modal
- Report Modal
- Validation Error Modal
- velo-supervisor-2000
- v0.1.0 Release
- v0.2.0 Release
- v0.3.0 Release
- v0.3.1 Release
- v0.4.0 Release
- v0.4.1 Release
- v0.4.4 Release
- database-expert.md
- ux-designer.md
- .read_collection_by_component
- Agent Communication via Handovers
- fullstack-developer.md
- product-manager.md
- Handovers Directory
- architect.md
- Architecture Overview
- Development Commands
- Middleware
- .write_bike_service_status
- .write_component_lifetime_status
- docs-maintainer.md
- Code Style & Standards
- Development Notes
- Standard Development Workflow
- Sub-Agent Team
- Testing Requirements
- .write_update_rides_bulk
- .read_subset_components
- .read_subset_installed_components
- .write_component_distance
- .write_workplan
- Service integration (#351) - fullstack to code-reviewer

## God Nodes (most connected - your core abstractions)
1. `BusinessLogic` - 64 edges
2. `DatabaseManager` - 61 edges
3. `run_all_migrations()` - 24 edges
4. `seed_component()` - 24 edges
5. `File map` - 21 edges
6. `Meta` - 20 edges
7. `seed_rides()` - 20 edges
8. `get_workplan_data_tuple()` - 18 edges
9. `get_incident_data_tuple()` - 15 edges
10. `Task 6: Business logic, workplans, incidents and payloads` - 15 edges

## Surprising Connections (you probably didn't know these)
- `Migration` --references--> `generate_unique_id()`  [INFERRED]
  docs/superpowers/specs/2026-09-18-service-integration-design.md → backend/utils.py
- `Key decisions` --references--> `get_effective_planned_date()`  [INFERRED]
  .handovers/fullstack/service-integration-fullstack-to-reviewer.md → backend/utils.py
- `Files` --references--> `derive_workplan_context()`  [INFERRED]
  .handovers/fullstack/service-integration-fullstack-to-reviewer.md → backend/utils.py
- `Files` --references--> `get_effective_planned_date()`  [INFERRED]
  .handovers/fullstack/service-integration-fullstack-to-reviewer.md → backend/utils.py
- `Files` --references--> `get_planned_service_data_tuple()`  [INFERRED]
  .handovers/fullstack/service-integration-fullstack-to-reviewer.md → backend/utils.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Breaking Database Schema Change Releases** — readme_v0_4_2, readme_v0_4_3, readme_v0_4_5, readme_v0_4_7, readme_v0_4_9, readme_db_migration_script [EXTRACTED 0.90]
- **CSS Inline-Style-to-Class Refactoring Files** — docs_plans_2026_01_11_workplan_hub_integration_incremental_css_refactor_concept, frontend_templates_collection_details_template, frontend_templates_index_template, frontend_templates_component_overview_template, frontend_templates_component_details_template, frontend_templates_bike_details_template, frontend_templates_config_template, frontend_templates_error_template [EXTRACTED 1.00]
- **Feature Introduction Documented in Help Page** — readme_v0_4_5, readme_v0_4_6, readme_v0_4_7, frontend_templates_help_core_concepts_collections, frontend_templates_help_common_tasks_quick_swap, frontend_templates_help_core_concepts_hybrid_tracking [INFERRED 0.85]
- **Generic JS-Driven Utility Modals** — frontend_templates_modal_confirm_confirmmodal, frontend_templates_modal_validation_validationmodal, frontend_templates_modal_report_reportmodal, frontend_templates_modal_docs_docsmodal, frontend_templates_modal_loading_loadingmodal [INFERRED 0.85]
- **Help Topic Display and Search Flow** — frontend_templates_help_helptopics, frontend_templates_help_showhelptopic, frontend_templates_help_search_functionality [INFERRED 0.85]
- **Shared Status Legend Badge Pattern** — frontend_templates_component_overview_template, frontend_templates_collection_details_template, frontend_templates_index_template [INFERRED 0.85]
- **Workplan Hub Integration Flow** — docs_plans_2026_01_11_workplan_hub_integration_incremental_doc, frontend_templates_bike_details_template, frontend_templates_component_details_template, frontend_templates_incident_reports_template, frontend_templates_modal_complete_workplan_template [INFERRED 0.85]
- **Templates Iterating payload.all_components_data** — frontend_templates_modal_incident_record_incidentrecordmodal, frontend_templates_modal_install_component_installcomponentmodal, frontend_templates_modal_quick_swap_quickswapmodal, frontend_templates_modal_workplan_record_workplanrecordmodal [INFERRED 0.90]

## Communities (119 total, 45 thin omitted)

### Community 0 - ".get_component_overview"
Cohesion: 0.15
Nodes (7): Method to produce payload for page component overview, Method to determine which factor triggered a warning status, Calculate lifetime and service triggers for a component, Method to produce payload for page bike overview, Method to create component-to-collection mapping dictionaries, Method to build dictionaries of bike and component ids referenced in received…, Method to build dictionaries of bike and component ids referenced by services…

### Community 1 - "run_all_migrations"
Cohesion: 0.13
Nodes (17): create_collections_table(), create_workplans_table(), migrate_database(), migrate_incidents_workplan_link(), populate_component_types_thresholds(), populate_components_thresholds(), Creates the workplans table if it doesn't exist., Creates the collections table if it doesn't exist. (+9 more)

### Community 2 - "Bike Details Template"
Cohesion: 0.10
Nodes (40): CSS Inline-Style-to-Class Refactoring, Workplan Hub Integration Plan, Opt-in Workplan Hub Pattern, Base Template, btn_new_incident Macro (Bike Details), btn_new_workplan Macro (Bike Details), Bike Details Template, Collection Details Template (+32 more)

### Community 3 - ".calculate_collection_status"
Cohesion: 0.17
Nodes (6): Method to update collection, Method to validate collections before allowing bulk operations, Method to change status of all components in a collection, Calculate status flags for a collection based on its components., Method to produce payload for displaying table of all collections, Method to produce payload for collection details page

### Community 4 - "Meta"
Cohesion: 0.08
Nodes (36): Module for interaction with a Sqlite database, BaseModel, Bikes, Collections, ComponentHistory, Components, ComponentTypes, Incidents (+28 more)

### Community 5 - "scheduler.py"
Cohesion: 0.07
Nodes (26): apscheduler_schedulers_asyncio, apscheduler_triggers_cron, apscheduler_triggers_interval, Module to handle business logic, Initialize and start the APScheduler instance, Scheduler for automated maintenance tasks, Gracefully shutdown the APScheduler instance, Scheduled job to update time-based status fields for all non-retired components (+18 more)

### Community 6 - "BusinessLogic"
Cohesion: 0.07
Nodes (28): BusinessLogic, Method to update component lifetime and service status when no installation…, Method to update status for a given bike based on component service and…, Method to create component, Method to update component details, Method to create installation history record, Method to update a component history record with validation, Method to validate history records before processing and storing in database (+20 more)

### Community 7 - "main.js"
Cohesion: 0.09
Nodes (9): filterNewComponentsByType(), handleOldComponentChange(), handleUpdate(), initializeCollectionsSearch(), updateRowVisibility(), NOTE: All collection details page handlers are in the "Functions used on…, IMPORTANT: Remove readonly - allow manual typing, showToast() (+1 more)

### Community 8 - "get"
Cohesion: 0.13
Nodes (20): collection_details(), component_overview(), component_types_overview(), help_page(), incident_reports(), Endpoint for incident reports page, Endpoint for workplans page, Endpoint for collection details page (+12 more)

### Community 9 - "CLAUDE.md"
Cohesion: 0.25
Nodes (6): Change Management Rules, Communication & Output Rules, Debugging & Bug Fixing Rules, graphify, Important Notes, Project Overview

### Community 10 - "generate_unique_id"
Cohesion: 0.20
Nodes (7): Method to create collection, Method to add incident record, Method to add workplan, optionally with planned services for components of a…, generate_unique_id(), parse_json_string(), Function to generates a random and unique ID, Function to load a JSON string and return the parsed data as a python object

### Community 11 - "Task 7: Routes"
Cohesion: 0.18
Nodes (11): add_history_record(), add_incident_record(), add_service(), add_workplan(), quick_swap(), Endpoint with conditional routing for redirects and AJAX to add an existing…, Endpoint to swap one component with another, Endpoint to add service, planned or completed (+3 more)

### Community 12 - "DatabaseManager"
Cohesion: 0.07
Nodes (15): DatabaseManager, Method to read and sort content of component_types table, Class to interact with a SQLite database through Peewee, Method to retrieve the most recent record from the installation log of a given…, Method to read content of bikes table, Method to read all collections, Method to read all workplans, Method to read workplans reached through the services of a given incident (+7 more)

### Community 13 - "Database Migration Script (db_migration.py)"
Cohesion: 0.13
Nodes (16): Collections (Core Concept), Component Types vs Components, Hybrid Time + Distance Tracking, Mileage Tracking, Understanding Thresholds, Getting Started: Define Component Types, Incidents Page, Workplans Page (+8 more)

### Community 15 - "validateDateInput"
Cohesion: 0.18
Nodes (10): Task 8: Plan and complete services modals and shared JS, Warning when resolving an incident with open services, 2026-09-26, initializeDatePickers(), initializeIncidentForm(), submitCollectionAjax(), submitComponentAjax(), validateCollectionStatusChange(), validateDateInput() (+2 more)

### Community 16 - "sortColumn"
Cohesion: 0.29
Nodes (8): initializeCollectionsSorting(), sortColumn(), initializeIncidentTable(), setupIncidentSearch(), setupIncidentStatusFiltering(), setupIncidentTableSorting(), setupWorkplanTableSorting(), updateIncidentVisibility()

### Community 17 - "main.py"
Cohesion: 0.08
Nodes (34): asyncio, add_collection(), add_planned_services(), change_collection_status(), complete_services(), component_modify(), component_types_modify(), create_component() (+26 more)

### Community 18 - "Service integration: incidents, workplans and services"
Cohesion: 0.13
Nodes (14): Backend, Data model, Error handling, Goal, main.js, main.py, Migration, Modals (+6 more)

### Community 19 - ".write_delete_record"
Cohesion: 0.12
Nodes (8): Method to retrieve record for a single component type, Method to retrieve record for a specific entry in the installation log, Method to retrieve a specific service record, Method to retrieve record for a specific collection, Method to retrieve record for a specific incident report, Method to retrieve record for a specific workplan, Method to write component type record in database, Method to delete a given record and associated records

### Community 20 - "middleware.py"
Cohesion: 0.25
Nodes (7): lifespan(), Manage application startup and shutdown, Module for middleware, FastAPI, starlette_exceptions, starlette_middleware_base, traceback

### Community 21 - "get_filtered_log"
Cohesion: 0.50
Nodes (4): get_filtered_log(), Endpoint to read log and return only business events, Function to get filtered log records, read_filtered_logs()

### Community 22 - "Python Requirements List"
Cohesion: 0.25
Nodes (8): APScheduler, Python Requirements List, FastAPI, Jinja2, Peewee ORM, python-multipart, requests-oauthlib, Uvicorn

### Community 24 - ".read_component"
Cohesion: 0.33
Nodes (3): Method to get component names based on list of ids, Method to retrieve record for a specific component, Method to create or update component data to the database

### Community 25 - "bike_details"
Cohesion: 0.28
Nodes (9): bike_details(), component_details(), Endpoint for component details page, Endpoint for bike details page, get_button_order(), Function to get button order for a specific page with defaults, Task 13: Bike and collection details pages, Task 14: Component details page and status change notes (+1 more)

### Community 26 - "update_config"
Cohesion: 0.20
Nodes (10): Endpoint to update config file based on which form was submitted, update_config(), parse_button_sorting(), Helper function to shutdown the server after a short delay, Function to read configuration file, Function to parse button sorting data from form submission, Function to update configuration file based on which form was submitted, read_config() (+2 more)

### Community 27 - "Task 10: Workplan modal and workplans list"
Cohesion: 0.47
Nodes (6): Task 10: Workplan modal and workplans list, editCollection(), initializeComponentSelector(), initializeWorkplanForm(), updateFormFields(), validateWorkplanForm()

### Community 28 - "version.py"
Cohesion: 0.40
Nodes (4): get_git_info(), Script to maintain version number, Function to get latest version number and commit hash, subprocess

### Community 29 - "CLAUDE.md"
Cohesion: 0.50
Nodes (4): CLAUDE.md, Data Management Tips, Need More Help? (Troubleshooting), Handover Documents Directory (.handovers/)

### Community 30 - "utils.py"
Cohesion: 0.08
Nodes (46): Method to produce payload for page component details, Method to produce payload for page incident reports, Method to produce payload for page of all workplans, Method to produce payload for workplan details page, Method to produce payload for page bike details, calculate_elapsed_days(), calculate_percentage_reached(), derive_workplan_context() (+38 more)

### Community 31 - "validateComponentThresholds"
Cohesion: 0.33
Nodes (6): addFormValidation(), clearValidationErrors(), showFieldError(), showValidationModal(), validateComponentThresholds(), validateQuickSwapForm()

### Community 32 - "migrate_components_time_fields"
Cohesion: 0.50
Nodes (4): check_components_time_columns(), migrate_components_time_fields(), Check if Components table needs time-based fields migration, Add time-based fields to Components table and populate threshold_km

### Community 33 - "helpTopics Data Object"
Cohesion: 0.50
Nodes (4): helpTopics Data Object, Help Page Template, Help Search Functionality, showHelpTopic() Function

### Community 34 - "conftest.py"
Cohesion: 0.16
Nodes (14): Task 0: Branch and test harness, fixture, json, os, pytest, shutil, sys, app_env() (+6 more)

### Community 35 - "Issues found (none blocking)"
Cohesion: 0.20
Nodes (8): Method to get the name of a bike based on bike id, Endpoint for workplan details page, workplan_details(), Code review -> docs-maintainer Handover, Context, Issues found (none blocking), Recommendations, References

### Community 36 - "insert_planned_service_for_migration"
Cohesion: 0.25
Nodes (8): check_incidents_workplan_column_present(), insert_planned_service_for_migration(), migrate_drop_incident_workplan_column(), migrate_incident_links_to_services(), Check if incidents table still has the workplan_id column, Insert a planned service with no date, bike or distance. Returns False if the…, Rebuild incident to workplan links through services, Rebuild incidents table without the workplan_id column

### Community 37 - "seed_component"
Cohesion: 0.15
Nodes (31): add_twin_component(), Planned services must be invisible to health computation, Rides before and after the service dates used below, so distances are not zero, Second installed component on bike-1 with the same settings as comp-1, Create one bike and one installed component with an installation record, seed_component(), seed_rides(), snapshot_health() (+23 more)

### Community 38 - "test_migration.py"
Cohesion: 0.28
Nodes (12): sqlite3, columns(), create_old_schema(), Migration converts the old workplan/incident model to services, Seed workplans, incidents and services in the pre-#351 shape, Recreate services, workplans, incidents and component_history as they were…, run_migration(), seed_old_data() (+4 more)

### Community 39 - "db_migration.py"
Cohesion: 0.16
Nodes (13): check_component_types_time_columns(), check_incidents_workplan_column(), check_workplans_name_column(), create_incidents_table(), migrate_component_types_time_fields(), migrate_workplans_name_column(), Creates the incidents table if it doesn't exist., Script to migrate the database, including adding new tables and fields (+5 more)

### Community 40 - ".process_service_records"
Cohesion: 0.10
Nodes (20): Method to add service record, planned or completed, Method to add a planned service, which has no service date, bike or distance…, Method to build the report used by the plan services and complete services…, Method to create planned services for one or more components with the same…, Method to complete planned services with one service date, keeping their…, Method to update a service record, including status changes in both directions, Method to recalculate a component after a completed service is deleted or…, Method to validate service records before processing and storing in database (+12 more)

### Community 41 - "validate_date_format"
Cohesion: 0.25
Nodes (5): Method to update incident record (supports full or partial updates), Method to update workplan (supports full or partial updates), Method to validate that a workplan can be set to Done, Function to validate that a date string matches the required format YYYY-MM-DD…, validate_date_format()

### Community 42 - "migrate_component_history_notes"
Cohesion: 0.50
Nodes (4): check_component_history_notes_column(), migrate_component_history_notes(), Check if component_history table needs notes column, Add notes column to component_history table

### Community 43 - "check_services_integration_columns"
Cohesion: 0.50
Nodes (4): check_services_integration_columns(), migrate_services_integration_columns(), Check which service integration columns are missing on the services table, Add status, incident_id and planned_date to services, mark existing rows…

### Community 44 - "File map"
Cohesion: 0.15
Nodes (10): Method to read incidents that have at least one service in a given workplan, Method to read all services linked to a specific workplan, planned first, Method to read planned services for a component, File map, Task 11: Incident modal and incident reports page, Task 12: Service record modal, Task 15: Help page, README and docs, Task 16: Verification and handover (+2 more)

### Community 45 - "migrate_workplans_to_planned_services"
Cohesion: 0.25
Nodes (8): check_workplans_affected_columns(), migrate_drop_workplan_affected_columns(), migrate_workplans_to_planned_services(), Check if workplans table still has the affected bike/component columns, Resolve bike and component names, marking components that no longer exist, Convert affected components on planned workplans into planned services,…, Rebuild workplans table without the affected bike/component columns, read_names_for_migration()

### Community 47 - "database_manager.py"
Cohesion: 0.11
Nodes (10): Method to retrieve the most recent completed service of a given component, Method to retrieve the oldest completed service of a given component, Method to read incident records with status 'Open, Method to read workplans with status 'Planned, Method to read planned services linked to a specific workplan, Method to read all services linked to a specific incident, planned first, Method to read planned services for components installed on a bike, Method to write or update service record in database (+2 more)

### Community 48 - "config_overview"
Cohesion: 0.50
Nodes (4): config_overview(), Endpoint for component types page, get_button_sorting_config(), Function to get button sorting configuration for config page

### Community 49 - "migrate_component_types"
Cohesion: 0.33
Nodes (6): check_component_types_columns(), count_component_types_in_use(), migrate_component_types(), Count how many components use a specific component type, Check if the component_types table needs migration, Migrate the component_types table to add new columns

### Community 50 - "migrate_services_workplan_link"
Cohesion: 0.50
Nodes (4): check_services_workplan_column(), migrate_services_workplan_link(), Check if Services table needs workplan_id column, Add workplan_id column to Services table for workplan hub integration

### Community 51 - "http_exception_handler"
Cohesion: 0.50
Nodes (4): http_exception_handler(), Function to catch http errors from Uvicorn and return them to the middleware, exception_handler, StarletteHTTPException

### Community 52 - "Test Protocol: Planned services, workplans and incidents"
Cohesion: 0.40
Nodes (4): Addtional notes, Preparation, Scope, Test Protocol: Planned services, workplans and incidents

### Community 54 - "prompt_for_db_path"
Cohesion: 0.50
Nodes (4): find_database_file(), prompt_for_db_path(), Search for a database file in the user's home directory and subdirectories, Prompt user for database path or filename and verify it exists

### Community 55 - "cleanup"
Cohesion: 0.50
Nodes (4): cleanup(), handleCancel(), handleConfirm(), performBulkStatusChange()

### Community 56 - "renderPreview"
Cohesion: 0.50
Nodes (4): containsMarkdown(), renderPreview(), setInitialMode(), updateCheckboxInText()

### Community 59 - "initializeWorkplanTable"
Cohesion: 0.67
Nodes (4): initializeWorkplanTable(), setupWorkplanSearch(), setupWorkplanStatusFiltering(), updateWorkplansVisibility()

### Community 65 - "Git Workflow Rules"
Cohesion: 0.25
Nodes (8): Version Script CI Workflow, Branch Strategy, Commit Process, For All Agents, For code-reviewer, For docs-maintainer, For fullstack-developer, Git Workflow Rules

### Community 67 - "code-reviewer.md"
Cohesion: 0.25
Nodes (7): Issues Found, Key Checks, Output Format, Recommendations, Review Philosophy, Review Process, Summary

### Community 70 - "[Source Agent] -> [Target Agent] Handover"
Cohesion: 0.25
Nodes (7): Blockers / Open Questions, Context, Decisions Made, Deliverables, Next Steps for [Target Agent], References, [Source Agent] -> [Target Agent] Handover

### Community 94 - "database-expert.md"
Cohesion: 0.29
Nodes (6): Constraints, Core Responsibilities, Pattern Consistency - CRITICAL, Query Optimization, Schema Changes, Workflow

### Community 95 - "ux-designer.md"
Cohesion: 0.29
Nodes (6): Core Responsibilities, Design Principles, Specifications to Include, v1 (Before Architect), v2 (After Architect), Workflow

### Community 97 - "Agent Communication via Handovers"
Cohesion: 0.33
Nodes (6): Agent Communication via Handovers, Creating Handovers, Detailed Instructions, Handover Structure, Naming Convention, Reading Handovers

### Community 98 - "fullstack-developer.md"
Cohesion: 0.33
Nodes (5): Backend Patterns, Core Responsibilities, Frontend Patterns, Handover Content, Workflow

### Community 99 - "product-manager.md"
Cohesion: 0.33
Nodes (5): Boundaries, Core Responsibilities, Key Principle: You Are Interactive, Requirements Document, User Story Format

### Community 100 - "Handovers Directory"
Cohesion: 0.33
Nodes (5): Creating Handovers, Directory Structure, Finding Handovers, Handovers Directory, Rules

### Community 101 - "architect.md"
Cohesion: 0.40
Nodes (4): Core Responsibilities, Handover Content, Principles, Workflow

### Community 102 - "Architecture Overview"
Cohesion: 0.40
Nodes (5): Architecture Overview, Configuration, Core Components, Key Features, Project Structure

### Community 103 - "Development Commands"
Cohesion: 0.40
Nodes (5): Database Operations, Dependencies, Development Commands, Running the Application, Testing

### Community 104 - "Middleware"
Cohesion: 0.24
Nodes (7): Middleware, Request, Class to handle exceptions that breaks the program and should be shown to the…, Method to dispatch intercepted requests, Method to catch and handle exceptions, BaseHTTPMiddleware, Exception

### Community 107 - "docs-maintainer.md"
Cohesion: 0.50
Nodes (3): Core Responsibilities, Documentation Rules, Workflow

### Community 108 - "Code Style & Standards"
Cohesion: 0.50
Nodes (4): Code Style & Standards, Database, Frontend, Python (Backend)

### Community 109 - "Development Notes"
Cohesion: 0.50
Nodes (4): Database Schema Changes, Development Notes, Docker Development, Logging

### Community 110 - "Standard Development Workflow"
Cohesion: 0.50
Nodes (4): For Bug Fixes, For Documentation Updates, For New Features, Standard Development Workflow

### Community 111 - "Sub-Agent Team"
Cohesion: 0.67
Nodes (3): Available Agents, Direct Invocation, Sub-Agent Team

### Community 112 - "Testing Requirements"
Cohesion: 0.67
Nodes (3): Before Creating Handover, For fullstack-developer, Testing Requirements

### Community 119 - "Service integration (#351) - fullstack to code-reviewer"
Cohesion: 0.05
Nodes (36): build_incident_service_entry(), get_effective_planned_date(), Return the service's own planned date, else the workplan due date, else None, Describe one service linked to an incident, for the read only list in the…, A. Questions to answer from the code, no change expected, B. Bugs to fix, C. Interface changes the user asked for, Code review outcome, 2026-09-26 (+28 more)

## Ambiguous Edges - Review These
- `Version Script CI Workflow` → `Git Workflow Rules`  [AMBIGUOUS]
  .github/workflows/run_version_script.yml · relation: conceptually_related_to

## Knowledge Gaps
- **168 isolated node(s):** `What was built`, `Testing`, `Known limitations`, `Regression evidence, 2026-09-26`, `Next steps` (+163 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 505 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **45 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `Version Script CI Workflow` and `Git Workflow Rules`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **Why does `DatabaseManager` connect `DatabaseManager` to `Meta`, `.count_component_types_in_use`, `.write_delete_record`, `.read_single_bike`, `.read_component`, `Issues found (none blocking)`, `.process_service_records`, `File map`, `.read_oldest_history_record`, `database_manager.py`, `.write_component_service_status`, `.read_subset_service_record`, `.read_date_oldest_ride`, `.read_all_components`, `.read_subset_component_history`, `.read_matching_rides`, `.read_all_components_objects`, `.read_all_incidents`, `.read_collection_by_component`, `.write_bike_service_status`, `.write_component_lifetime_status`, `.write_update_rides_bulk`, `.read_subset_components`, `.read_subset_installed_components`, `.write_component_distance`, `.write_workplan`?**
  _High betweenness centrality (0.145) - this node is a cross-community bridge._
- **Why does `BusinessLogic` connect `BusinessLogic` to `.get_component_overview`, `.calculate_collection_status`, `scheduler.py`, `.process_service_records`, `validate_date_format`, `generate_unique_id`, `utils.py`?**
  _High betweenness centrality (0.099) - this node is a cross-community bridge._
- **Why does `renderIncidentServices()` connect `Service integration (#351) - fullstack to code-reviewer` to `Issues found (none blocking)`, `main.js`?**
  _High betweenness centrality (0.048) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `BusinessLogic` (e.g. with `strava_sync_job()` and `update_time_based_fields_job()`) actually correct?**
  _`BusinessLogic` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `run_all_migrations()` (e.g. with `Task 2: Database manager reads` and `Task 3: Migration`) actually correct?**
  _`run_all_migrations()` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `File map` (e.g. with `derive_workplan_context()` and `get_effective_planned_date()`) actually correct?**
  _`File map` has 3 INFERRED edges - model-reasoned connections that need verification._