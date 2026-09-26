# Graph Report - velo-supervisor-2000  (2026-09-27)

## Corpus Check
- 41 files · ~163,304 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 12 file(s) not represented in the graph (top: (none) 5, .example 1, .sqlite 1)

## Summary
- 972 nodes · 1525 edges · 122 communities (75 shown, 47 thin omitted)
- Extraction: 84% EXTRACTED · 16% INFERRED · 0% AMBIGUOUS · INFERRED: 246 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `cee989a7`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- generate_unique_id
- run_all_migrations
- Bike Details Template
- .create_history_record
- Meta
- Strava
- BusinessLogic
- main.js
- get
- CLAUDE.md
- .create_workplan
- .calculate_component_triggers
- DatabaseManager
- Database Migration Script (db_migration.py)
- .count_component_types_in_use
- Service Integration Implementation Plan
- scheduler.py
- main.py
- Service integration: incidents, workplans and services
- .write_delete_record
- business_logic.py
- get_filtered_log
- Python Requirements List
- .read_all_components
- .read_component
- File map
- write_config
- Service integration (#351) - fullstack to code-reviewer
- version.py
- CLAUDE.md
- utils.py
- .read_all_collections
- migrate_components_time_fields
- helpTopics Data Object
- conftest.py
- .read_all_incidents
- migrate_incident_links_to_services
- seed_component
- test_migration.py
- db_migration.py
- .validate_service_record
- validate_date_format
- update_config
- .read_all_workplans
- Task 2: Database manager reads
- migrate_workplans_to_planned_services
- .read_oldest_history_record
- database_manager.py
- migrate_component_types_time_fields
- migrate_component_types
- migrate_services_workplan_link
- .read_unique_bikes
- Test Protocol: Planned services, workplans and incidents
- .write_component_service_status
- prompt_for_db_path
- .read_latest_history_record
- .read_subset_components
- .read_subset_service_record
- .write_incident_record
- .read_collection_by_component
- Request
- .read_recent_rides
- .read_subset_component_history
- .read_subset_installed_components
- .read_sum_distance_subset_rides
- Git Workflow Rules
- get_current_version
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
- .write_collection
- Agent Communication via Handovers
- fullstack-developer.md
- product-manager.md
- Handovers Directory
- architect.md
- Architecture Overview
- Development Commands
- Middleware
- .write_component_distance
- docs-maintainer.md
- Code Style & Standards
- Development Notes
- Standard Development Workflow
- Sub-Agent Team
- Testing Requirements
- Technical debt
- validateDateInput
- sortColumn
- D. Design questions to decide before coding
- Task 10: Workplan modal and workplans list
- validateComponentThresholds
- migrate_workplans_name_column
- cleanup
- renderPreview
- initializeWorkplanTable

## God Nodes (most connected - your core abstractions)
1. `BusinessLogic` - 64 edges
2. `DatabaseManager` - 61 edges
3. `seed_component()` - 24 edges
4. `run_all_migrations()` - 23 edges
5. `File map` - 21 edges
6. `seed_rides()` - 20 edges
7. `Meta` - 20 edges
8. `get_workplan_data_tuple()` - 15 edges
9. `Task 6: Business logic, workplans, incidents and payloads` - 15 edges
10. `get_incident_data_tuple()` - 14 edges

## Surprising Connections (you probably didn't know these)
- `Migration` --references--> `generate_unique_id()`  [INFERRED]
  docs/superpowers/specs/2026-09-18-service-integration-design.md → backend/utils.py
- `Task 5: Business logic, planned services and completion` --references--> `ComponentHistory`  [INFERRED]
  docs/superpowers/plans/2026-09-18-service-integration.md → backend/database_model.py
- `Task 5: Business logic, planned services and completion` --references--> `Incidents`  [INFERRED]
  docs/superpowers/plans/2026-09-18-service-integration.md → backend/database_model.py
- `Task 5: Business logic, planned services and completion` --references--> `Workplans`  [INFERRED]
  docs/superpowers/plans/2026-09-18-service-integration.md → backend/database_model.py
- `Task 0: Branch and test harness` --references--> `migrate_database()`  [INFERRED]
  docs/superpowers/plans/2026-09-18-service-integration.md → backend/db_migration.py

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

## Communities (122 total, 47 thin omitted)

### Community 0 - "generate_unique_id"
Cohesion: 0.14
Nodes (8): Method to create collection, Method to update collection, Method to add incident record, Calculate status flags for a collection based on its components., Method to produce payload for displaying table of all collections, Method to produce payload for collection details page, generate_unique_id(), Function to generates a random and unique ID

### Community 1 - "run_all_migrations"
Cohesion: 0.14
Nodes (17): check_services_integration_columns(), create_workplans_table(), migrate_database(), migrate_incidents_workplan_link(), migrate_services_integration_columns(), populate_components_thresholds(), Creates the workplans table if it doesn't exist., Populate threshold_km = 200 for existing components with distance intervals.… (+9 more)

### Community 2 - "Bike Details Template"
Cohesion: 0.10
Nodes (40): CSS Inline-Style-to-Class Refactoring, Workplan Hub Integration Plan, Opt-in Workplan Hub Pattern, Base Template, btn_new_incident Macro (Bike Details), btn_new_workplan Macro (Bike Details), Bike Details Template, Collection Details Template (+32 more)

### Community 3 - ".create_history_record"
Cohesion: 0.09
Nodes (12): Method to create component, Method to create installation history record, Method to orchestrate swap of one component with another, Method to validate quick swap operation, Method to validate collections before allowing bulk operations, Method to change status of all components in a collection, Validate threshold configuration rules for component intervals, Method to check if a bike has all mandatory components and respects max… (+4 more)

### Community 4 - "Meta"
Cohesion: 0.08
Nodes (36): Module for interaction with a Sqlite database, BaseModel, Bikes, Collections, ComponentHistory, Components, ComponentTypes, Incidents (+28 more)

### Community 5 - "Strava"
Cohesion: 0.18
Nodes (9): Class to interact with Strava API, Method to authenticate and get data from Stravas gear API, Method to prepare a list of rides, Method to prepare a list of bikes, Method to read oauth options from file, Method to save oauth options to file, Method to authenticate and get data from Stravas activities API, Method to authenticate and get the full list of bike ids from the athlete's… (+1 more)

### Community 6 - "BusinessLogic"
Cohesion: 0.08
Nodes (25): BusinessLogic, Method to update component lifetime and service status when no installation…, Method to update status for a given bike based on component service and…, Method to update component details, Method to calculate distance and bike id for history records, Method to update a service record, including status changes in both directions, Method to recalculate a component after a completed service is deleted or…, Method to calculate distance and bike id for service records (+17 more)

### Community 7 - "main.js"
Cohesion: 0.09
Nodes (9): filterNewComponentsByType(), handleOldComponentChange(), handleUpdate(), initializeCollectionsSearch(), updateRowVisibility(), NOTE: All collection details page handlers are in the "Functions used on…, IMPORTANT: Remove readonly - allow manual typing, showToast() (+1 more)

### Community 8 - "get"
Cohesion: 0.11
Nodes (24): collection_details(), component_overview(), component_types_overview(), config_overview(), help_page(), incident_reports(), Endpoint for incident reports page, Endpoint for workplans page (+16 more)

### Community 9 - "CLAUDE.md"
Cohesion: 0.25
Nodes (6): Change Management Rules, Communication & Output Rules, Debugging & Bug Fixing Rules, graphify, Important Notes, Project Overview

### Community 10 - ".create_workplan"
Cohesion: 0.20
Nodes (9): Method to add workplan, optionally with planned services for components of a…, build_incident_service_entry(), get_effective_planned_date(), parse_json_string(), Return the service's own planned date, else the workplan due date, else None, Describe one service linked to an incident, for the read only list in the…, Function to load a JSON string and return the parsed data as a python object, Status (2026-09-26) (+1 more)

### Community 12 - "DatabaseManager"
Cohesion: 0.07
Nodes (14): DatabaseManager, Method to read and sort content of component_types table, Method to read all component objects (not tuples), Class to interact with a SQLite database through Peewee, Method to read content of bikes table, Method to read workplans reached through the services of a given incident, Method to create or update ride data in bulk in database, Method to get bike id from most recent component history (+6 more)

### Community 13 - "Database Migration Script (db_migration.py)"
Cohesion: 0.13
Nodes (16): Collections (Core Concept), Component Types vs Components, Hybrid Time + Distance Tracking, Mileage Tracking, Understanding Thresholds, Getting Started: Define Component Types, Incidents Page, Workplans Page (+8 more)

### Community 16 - "scheduler.py"
Cohesion: 0.15
Nodes (15): apscheduler_schedulers_asyncio, apscheduler_triggers_cron, apscheduler_triggers_interval, lifespan(), Manage application startup and shutdown, Initialize and start the APScheduler instance, Scheduler for automated maintenance tasks, Gracefully shutdown the APScheduler instance (+7 more)

### Community 17 - "main.py"
Cohesion: 0.06
Nodes (47): asyncio, add_collection(), add_history_record(), add_incident_record(), add_planned_services(), add_service(), add_workplan(), change_collection_status() (+39 more)

### Community 18 - "Service integration: incidents, workplans and services"
Cohesion: 0.13
Nodes (14): Backend, Data model, Error handling, Goal, main.js, main.py, Migration, Modals (+6 more)

### Community 19 - ".write_delete_record"
Cohesion: 0.12
Nodes (8): Method to retrieve record for a single component type, Method to retrieve record for a specific entry in the installation log, Method to retrieve a specific service record, Method to retrieve record for a specific collection, Method to retrieve record for a specific incident report, Method to retrieve record for a specific workplan, Method to write component type record in database, Method to delete a given record and associated records

### Community 20 - "business_logic.py"
Cohesion: 0.21
Nodes (10): Module to handle business logic, Module for middleware, Module to interact with Strava APIs, datetime, json, logging, requests_oauthlib, starlette_exceptions (+2 more)

### Community 21 - "get_filtered_log"
Cohesion: 0.50
Nodes (4): get_filtered_log(), Endpoint to read log and return only business events, Function to get filtered log records, read_filtered_logs()

### Community 22 - "Python Requirements List"
Cohesion: 0.25
Nodes (8): APScheduler, Python Requirements List, FastAPI, Jinja2, Peewee ORM, python-multipart, requests-oauthlib, Uvicorn

### Community 23 - ".read_all_components"
Cohesion: 0.25
Nodes (4): Method to read content of components table as formatted tuples, Method to retrieve record for a specific bike, Method to get the name of a bike based on bike id, Method to create or update bike data to the database

### Community 24 - ".read_component"
Cohesion: 0.33
Nodes (3): Method to get component names based on list of ids, Method to retrieve record for a specific component, Method to create or update component data to the database

### Community 25 - "File map"
Cohesion: 0.16
Nodes (15): bike_details(), component_details(), Endpoint for component details page, Endpoint for bike details page, get_button_order(), Function to get button order for a specific page with defaults, File map, Task 11: Incident modal and incident reports page (+7 more)

### Community 26 - "write_config"
Cohesion: 0.33
Nodes (6): parse_button_sorting(), Function to read configuration file, Function to parse button sorting data from form submission, Function to update configuration file based on which form was submitted, read_config(), write_config()

### Community 27 - "Service integration (#351) - fullstack to code-reviewer"
Cohesion: 0.29
Nodes (6): Bugs found and fixed, Known limitations, Next steps, Service integration (#351) - fullstack to code-reviewer, Testing, What was built

### Community 28 - "version.py"
Cohesion: 0.40
Nodes (4): get_git_info(), Script to maintain version number, Function to get latest version number and commit hash, subprocess

### Community 29 - "CLAUDE.md"
Cohesion: 0.50
Nodes (4): CLAUDE.md, Data Management Tips, Need More Help? (Troubleshooting), Handover Documents Directory (.handovers/)

### Community 30 - "utils.py"
Cohesion: 0.08
Nodes (46): Method to produce payload for page component overview, Method to produce payload for page component details, Method to create component-to-collection mapping dictionaries, Method to produce payload for page incident reports, Method to produce payload for page of all workplans, Method to build dictionaries of bike and component ids referenced by services…, Method to produce payload for workplan details page, Method to produce payload for page bike details (+38 more)

### Community 32 - "migrate_components_time_fields"
Cohesion: 0.50
Nodes (4): check_components_time_columns(), migrate_components_time_fields(), Check if Components table needs time-based fields migration, Add time-based fields to Components table and populate threshold_km

### Community 33 - "helpTopics Data Object"
Cohesion: 0.50
Nodes (4): helpTopics Data Object, Help Page Template, Help Search Functionality, showHelpTopic() Function

### Community 34 - "conftest.py"
Cohesion: 0.18
Nodes (13): Task 0: Branch and test harness, fixture, os, pytest, shutil, sys, app_env(), migrated_env() (+5 more)

### Community 36 - "migrate_incident_links_to_services"
Cohesion: 0.33
Nodes (6): check_incidents_workplan_column_present(), migrate_drop_incident_workplan_column(), migrate_incident_links_to_services(), Check if incidents table still has the workplan_id column, Rebuild incident to workplan links through services, Rebuild incidents table without the workplan_id column

### Community 37 - "seed_component"
Cohesion: 0.15
Nodes (31): add_twin_component(), Planned services must be invisible to health computation, Rides before and after the service dates used below, so distances are not zero, Second installed component on bike-1 with the same settings as comp-1, Create one bike and one installed component with an installation record, seed_component(), seed_rides(), snapshot_health() (+23 more)

### Community 38 - "test_migration.py"
Cohesion: 0.28
Nodes (12): sqlite3, columns(), create_old_schema(), Migration converts the old workplan/incident model to services, Seed workplans, incidents and services in the pre-#351 shape, Recreate services, workplans, incidents and component_history as they were…, run_migration(), seed_old_data() (+4 more)

### Community 39 - "db_migration.py"
Cohesion: 0.15
Nodes (13): check_component_history_notes_column(), check_incidents_workplan_column(), create_collections_table(), create_incidents_table(), migrate_component_history_notes(), populate_component_types_thresholds(), Creates the incidents table if it doesn't exist., Creates the collections table if it doesn't exist. (+5 more)

### Community 40 - ".validate_service_record"
Cohesion: 0.20
Nodes (9): Method to add service record, planned or completed, Method to add a planned service, which has no service date, bike or distance…, Method to build the report used by the plan services and complete services…, Method to create planned services for one or more components with the same…, Method to complete planned services with one service date, keeping their…, Method to validate service records before processing and storing in database, Task 5: Business logic, planned services and completion, business_logic.py (+1 more)

### Community 41 - "validate_date_format"
Cohesion: 0.17
Nodes (7): Method to update a component history record with validation, Method to validate history records before processing and storing in database, Method to update incident record (supports full or partial updates), Method to update workplan (supports full or partial updates), Method to validate that a workplan can be set to Done, Function to validate that a date string matches the required format YYYY-MM-DD…, validate_date_format()

### Community 42 - "update_config"
Cohesion: 0.50
Nodes (4): Endpoint to update config file based on which form was submitted, update_config(), Helper function to shutdown the server after a short delay, shutdown_server()

### Community 44 - "Task 2: Database manager reads"
Cohesion: 0.29
Nodes (4): Method to read incidents that have at least one service in a given workplan, Method to read all services linked to a specific workplan, planned first, Method to read planned services for a component, Task 2: Database manager reads

### Community 45 - "migrate_workplans_to_planned_services"
Cohesion: 0.18
Nodes (12): check_workplans_affected_columns(), insert_planned_service_for_migration(), migrate_drop_workplan_affected_columns(), migrate_workplans_to_planned_services(), Check if workplans table still has the affected bike/component columns, Resolve bike and component names, marking components that no longer exist, Insert a planned service with no date, bike or distance. Returns False if the…, Convert affected components on planned workplans into planned services,… (+4 more)

### Community 47 - "database_manager.py"
Cohesion: 0.10
Nodes (11): Method to read completed services for a component, used by health computation, Method to retrieve the most recent completed service of a given component, Method to retrieve the oldest completed service of a given component, Method to read incident records with status 'Open, Method to read workplans with status 'Planned, Method to read planned services linked to a specific workplan, Method to read all services linked to a specific incident, planned first, Method to read planned services for components installed on a bike (+3 more)

### Community 48 - "migrate_component_types_time_fields"
Cohesion: 0.50
Nodes (4): check_component_types_time_columns(), migrate_component_types_time_fields(), Check if ComponentTypes table needs time-based fields migration, Add time-based fields to ComponentTypes table

### Community 49 - "migrate_component_types"
Cohesion: 0.33
Nodes (6): check_component_types_columns(), count_component_types_in_use(), migrate_component_types(), Count how many components use a specific component type, Check if the component_types table needs migration, Migrate the component_types table to add new columns

### Community 50 - "migrate_services_workplan_link"
Cohesion: 0.50
Nodes (4): check_services_workplan_column(), migrate_services_workplan_link(), Check if Services table needs workplan_id column, Add workplan_id column to Services table for workplan hub integration

### Community 52 - "Test Protocol: Planned services, workplans and incidents"
Cohesion: 0.40
Nodes (4): Addtional notes, Preparation, Scope, Test Protocol: Planned services, workplans and incidents

### Community 54 - "prompt_for_db_path"
Cohesion: 0.50
Nodes (4): find_database_file(), prompt_for_db_path(), Search for a database file in the user's home directory and subdirectories, Prompt user for database path or filename and verify it exists

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
Cohesion: 0.16
Nodes (11): http_exception_handler(), Function to catch http errors from Uvicorn and return them to the middleware, Middleware, Request, Class to handle exceptions that breaks the program and should be shown to the…, Method to dispatch intercepted requests, Method to catch and handle exceptions, BaseHTTPMiddleware (+3 more)

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

### Community 114 - "Technical debt"
Cohesion: 0.22
Nodes (8): 1. Thin automated test coverage, 2. Page payloads are positional tuples, 3. Two very large files, 5. Duplication in templates and JavaScript, 6. Unpinned dependencies, 7. Smaller items, Cleared, Technical debt

### Community 115 - "validateDateInput"
Cohesion: 0.22
Nodes (8): Task 8: Plan and complete services modals and shared JS, initializeDatePickers(), initializeIncidentForm(), submitCollectionAjax(), submitComponentAjax(), validateCollectionStatusChange(), validateDateInput(), validateIncidentForm()

### Community 117 - "sortColumn"
Cohesion: 0.29
Nodes (8): initializeCollectionsSorting(), sortColumn(), initializeIncidentTable(), setupIncidentSearch(), setupIncidentStatusFiltering(), setupIncidentTableSorting(), setupWorkplanTableSorting(), updateIncidentVisibility()

### Community 119 - "D. Design questions to decide before coding"
Cohesion: 0.15
Nodes (12): B. Bugs to fix, C. Interface changes the user asked for, D. Design questions to decide before coding, Decisions (2026-09-26), Extra wording fixes asked for on 2026-09-26, Follow-up tweaks asked for on 2026-09-26, Second round of tweaks, 2026-09-26, Service integration (#351): findings from the manual test walkthrough (+4 more)

### Community 120 - "Task 10: Workplan modal and workplans list"
Cohesion: 0.47
Nodes (6): Task 10: Workplan modal and workplans list, editCollection(), initializeComponentSelector(), initializeWorkplanForm(), updateFormFields(), validateWorkplanForm()

### Community 121 - "validateComponentThresholds"
Cohesion: 0.33
Nodes (6): addFormValidation(), clearValidationErrors(), showFieldError(), showValidationModal(), validateComponentThresholds(), validateQuickSwapForm()

### Community 122 - "migrate_workplans_name_column"
Cohesion: 0.50
Nodes (4): check_workplans_name_column(), migrate_workplans_name_column(), Check if workplans table needs the workplan_name column, Add the optional user given name to the workplans table, existing workplans…

### Community 124 - "cleanup"
Cohesion: 0.50
Nodes (4): cleanup(), handleCancel(), handleConfirm(), performBulkStatusChange()

### Community 125 - "renderPreview"
Cohesion: 0.50
Nodes (4): containsMarkdown(), renderPreview(), setInitialMode(), updateCheckboxInText()

### Community 126 - "initializeWorkplanTable"
Cohesion: 0.67
Nodes (4): initializeWorkplanTable(), setupWorkplanSearch(), setupWorkplanStatusFiltering(), updateWorkplansVisibility()

## Ambiguous Edges - Review These
- `Version Script CI Workflow` → `Git Workflow Rules`  [AMBIGUOUS]
  .github/workflows/run_version_script.yml · relation: conceptually_related_to

## Knowledge Gaps
- **164 isolated node(s):** `Scope`, `Preparation`, `Addtional notes`, `Collections (Core Concept)`, `Component Types vs Components` (+159 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 501 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **47 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `Version Script CI Workflow` and `Git Workflow Rules`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **Why does `DatabaseManager` connect `DatabaseManager` to `Meta`, `.count_component_types_in_use`, `.write_delete_record`, `.read_all_components`, `.read_component`, `.read_all_collections`, `.read_all_incidents`, `.read_all_workplans`, `Task 2: Database manager reads`, `.read_oldest_history_record`, `database_manager.py`, `.read_unique_bikes`, `.write_component_service_status`, `.read_latest_history_record`, `.read_subset_components`, `.read_subset_service_record`, `.write_incident_record`, `.read_collection_by_component`, `.read_recent_rides`, `.read_subset_component_history`, `.read_subset_installed_components`, `.read_sum_distance_subset_rides`, `.write_collection`, `.write_component_distance`?**
  _High betweenness centrality (0.155) - this node is a cross-community bridge._
- **Why does `BusinessLogic` connect `BusinessLogic` to `generate_unique_id`, `.create_history_record`, `.validate_service_record`, `validate_date_format`, `.create_workplan`, `.calculate_component_triggers`, `scheduler.py`, `business_logic.py`, `utils.py`?**
  _High betweenness centrality (0.113) - this node is a cross-community bridge._
- **Why does `File map` connect `File map` to `run_all_migrations`, `conftest.py`, `Meta`, `.validate_service_record`, `.create_workplan`, `Task 2: Database manager reads`, `Service Integration Implementation Plan`, `main.py`, `validateDateInput`, `Task 10: Workplan modal and workplans list`, `utils.py`?**
  _High betweenness centrality (0.060) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `BusinessLogic` (e.g. with `strava_sync_job()` and `update_time_based_fields_job()`) actually correct?**
  _`BusinessLogic` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `run_all_migrations()` (e.g. with `Task 2: Database manager reads` and `Task 3: Migration`) actually correct?**
  _`run_all_migrations()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `File map` (e.g. with `derive_workplan_context()` and `get_effective_planned_date()`) actually correct?**
  _`File map` has 3 INFERRED edges - model-reasoned connections that need verification._