# Graph Report - velo-supervisor-2000  (2026-09-27)

## Corpus Check
- 38 files · ~144,428 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 12 file(s) not represented in the graph (top: (none) 5, .example 1, .sqlite 1)

## Summary
- 953 nodes · 1453 edges · 123 communities (76 shown, 47 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 198 edges (avg confidence: 0.9)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `18ec65fe`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- .get_bike_details
- migrate_incidents_workplan_link
- Base Template
- scheduler.py
- Meta
- Strava
- .process_service_records
- main.js
- get
- CLAUDE.md
- .create_history_record
- BusinessLogic
- DatabaseManager
- Database Migration Script (db_migration.py)
- Service integration (#351) - fullstack to code-reviewer
- validateDateInput
- sortColumn
- main.py
- Service integration: incidents, workplans and services
- .write_delete_record
- business_logic.py
- get_filtered_log
- Python Requirements List
- .read_single_bike
- .read_component
- What was checked and held up
- utils.py
- initializeWorkplanTable
- version.py
- CLAUDE.md
- get_workplan_data_tuple
- validateComponentThresholds
- migrate_components_time_fields
- helpTopics Data Object
- conftest.py
- get_planned_service_data_tuple
- insert_planned_service_for_migration
- seed_component
- test_migration.py
- migrate_component_types_time_fields
- generate_unique_id
- validate_date_format
- D. Design questions to decide before coding
- get_incident_data_tuple
- .read_incidents_by_workplan
- migrate_workplans_to_planned_services
- .complete_services
- database_manager.py
- migrate_workplans_name_column
- db_migration.py
- run_all_migrations
- update_config
- Results
- get_formatted_bikes_list
- migrate_database
- .read_all_workplans
- renderPreview
- migrate_services_workplan_link
- .read_bike_id_recent_component_history
- .read_bikes
- Request
- config_overview
- .read_subset_component_history
- .read_matching_rides
- .read_all_components_objects
- Git Workflow Rules
- initializeComponentSelector
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
- .read_recent_rides
- Agent Communication via Handovers
- fullstack-developer.md
- product-manager.md
- Handovers Directory
- architect.md
- Architecture Overview
- Development Commands
- Middleware
- .read_unique_bikes
- .write_component_lifetime_status
- docs-maintainer.md
- Code Style & Standards
- Development Notes
- Standard Development Workflow
- Sub-Agent Team
- Testing Requirements
- .write_incident_record
- .count_component_types_in_use
- .read_date_oldest_ride
- .write_component_distance
- .read_workplans_by_incident
- .write_collection
- Service integration (#351): findings from the manual test walkthrough
- .write_component_service_status
- Collections Test Protocol
- Complete Workplan Modal Template

## God Nodes (most connected - your core abstractions)
1. `BusinessLogic` - 64 edges
2. `DatabaseManager` - 61 edges
3. `seed_component()` - 24 edges
4. `run_all_migrations()` - 22 edges
5. `Meta` - 20 edges
6. `seed_rides()` - 20 edges
7. `get_workplan_data_tuple()` - 15 edges
8. `What was checked and held up` - 15 edges
9. `database_manager.py` - 14 edges
10. `BaseModel` - 13 edges

## Surprising Connections (you probably didn't know these)
- `Key decisions` --references--> `get_effective_planned_date()`  [INFERRED]
  .handovers/fullstack/service-integration-fullstack-to-reviewer.md → backend/utils.py
- `Files` --references--> `derive_workplan_context()`  [INFERRED]
  .handovers/fullstack/service-integration-fullstack-to-reviewer.md → backend/utils.py
- `Files` --references--> `get_effective_planned_date()`  [INFERRED]
  .handovers/fullstack/service-integration-fullstack-to-reviewer.md → backend/utils.py
- `Files` --references--> `get_planned_service_data_tuple()`  [INFERRED]
  .handovers/fullstack/service-integration-fullstack-to-reviewer.md → backend/utils.py
- `Reuse` --references--> `validate_date_format()`  [INFERRED]
  .handovers/fullstack/service-integration-fullstack-to-reviewer.md → backend/utils.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Breaking Database Schema Change Releases** — readme_v0_4_2, readme_v0_4_3, readme_v0_4_5, readme_v0_4_7, readme_v0_4_9, readme_db_migration_script [EXTRACTED 0.90]
- **Feature Introduction Documented in Help Page** — readme_v0_4_5, readme_v0_4_6, readme_v0_4_7, frontend_templates_help_core_concepts_collections, frontend_templates_help_common_tasks_quick_swap, frontend_templates_help_core_concepts_hybrid_tracking [INFERRED 0.85]
- **Generic JS-Driven Utility Modals** — frontend_templates_modal_confirm_confirmmodal, frontend_templates_modal_validation_validationmodal, frontend_templates_modal_report_reportmodal, frontend_templates_modal_docs_docsmodal, frontend_templates_modal_loading_loadingmodal [INFERRED 0.85]
- **Help Topic Display and Search Flow** — frontend_templates_help_helptopics, frontend_templates_help_showhelptopic, frontend_templates_help_search_functionality [INFERRED 0.85]
- **Shared Status Legend Badge Pattern** — frontend_templates_component_overview_template, frontend_templates_collection_details_template, frontend_templates_index_template [INFERRED 0.85]
- **Templates Iterating payload.all_components_data** — frontend_templates_modal_incident_record_incidentrecordmodal, frontend_templates_modal_install_component_installcomponentmodal, frontend_templates_modal_quick_swap_quickswapmodal, frontend_templates_modal_workplan_record_workplanrecordmodal [INFERRED 0.90]

## Communities (123 total, 47 thin omitted)

### Community 0 - ".get_bike_details"
Cohesion: 0.12
Nodes (15): Method to produce payload for page component overview, Method to produce payload for page component details, Method to produce payload for page bike overview, Method to create component-to-collection mapping dictionaries, Method to produce payload for displaying table of all collections, Method to build dictionaries of bike and component ids referenced in received…, Method to build dictionaries of bike and component ids referenced by services…, Method to produce payload for page bike details (+7 more)

### Community 1 - "migrate_incidents_workplan_link"
Cohesion: 0.25
Nodes (8): check_incidents_workplan_column(), check_services_integration_columns(), migrate_incidents_workplan_link(), migrate_services_integration_columns(), Check if Incidents table needs workplan_id column, Add workplan_id column to Incidents table for workplan hub integration, Check which service integration columns are missing on the services table, Add status, incident_id and planned_date to services, mark existing rows…

### Community 2 - "Base Template"
Cohesion: 0.12
Nodes (34): Base Template, btn_new_incident Macro (Bike Details), btn_new_workplan Macro (Bike Details), Bike Details Template, Collection Details Template, btn_new_incident Macro (Component Details), btn_new_workplan Macro (Component Details), btn_quick_swap Macro (+26 more)

### Community 3 - "scheduler.py"
Cohesion: 0.15
Nodes (15): apscheduler_schedulers_asyncio, apscheduler_triggers_cron, apscheduler_triggers_interval, lifespan(), Manage application startup and shutdown, Initialize and start the APScheduler instance, Scheduler for automated maintenance tasks, Gracefully shutdown the APScheduler instance (+7 more)

### Community 4 - "Meta"
Cohesion: 0.09
Nodes (34): BaseModel, Bikes, Collections, ComponentHistory, Components, ComponentTypes, Incidents, Meta (+26 more)

### Community 5 - "Strava"
Cohesion: 0.18
Nodes (9): Class to interact with Strava API, Method to authenticate and get data from Stravas gear API, Method to prepare a list of rides, Method to prepare a list of bikes, Method to read oauth options from file, Method to save oauth options to file, Method to authenticate and get data from Stravas activities API, Method to authenticate and get the full list of bike ids from the athlete's… (+1 more)

### Community 6 - ".process_service_records"
Cohesion: 0.12
Nodes (15): Method to update component lifetime and service status when no installation…, Method to update status for a given bike based on component service and…, Method to calculate distance and bike id for history records, Method to calculate distance and bike id for service records, Method to compute component status using threshold logic, Method to determine worst-case status between distance and days-based…, Method to update time-based status fields for all non-retired components, Method to determine which selection of components to update (+7 more)

### Community 7 - "main.js"
Cohesion: 0.08
Nodes (13): cleanup(), filterNewComponentsByType(), handleCancel(), handleConfirm(), handleOldComponentChange(), handleUpdate(), initializeCollectionsSearch(), updateRowVisibility() (+5 more)

### Community 8 - "get"
Cohesion: 0.09
Nodes (32): Method to get the name of a bike based on bike id, add_history_record(), bike_details(), collection_details(), component_details(), component_overview(), component_types_overview(), help_page() (+24 more)

### Community 9 - "CLAUDE.md"
Cohesion: 0.25
Nodes (6): Change Management Rules, Communication & Output Rules, Debugging & Bug Fixing Rules, graphify, Important Notes, Project Overview

### Community 10 - ".create_history_record"
Cohesion: 0.13
Nodes (10): Method to create component, Method to update component details, Method to create installation history record, Method to orchestrate swap of one component with another, Method to validate quick swap operation, Validate threshold configuration rules for component intervals, Method to check if a bike has all mandatory components and respects max…, Method to create or update component types (+2 more)

### Community 11 - "BusinessLogic"
Cohesion: 0.09
Nodes (14): BusinessLogic, Method to create collection, Method to update collection, Method to validate collections before allowing bulk operations, Method to change status of all components in a collection, Method to determine which factor triggered a warning status, Calculate lifetime and service triggers for a component, Method to refresh all bikes from Strava (+6 more)

### Community 12 - "DatabaseManager"
Cohesion: 0.07
Nodes (15): DatabaseManager, Method to read and sort content of component_types table, Method to read components for a specific bike, Method to read installed components for a specific bike, Class to interact with a SQLite database through Peewee, Method to retrieve the most recent record from the installation log of a given…, Method to retrieve the oldest record from the installation log of a given…, Method to retrieve record for a specific entry in the service log (+7 more)

### Community 13 - "Database Migration Script (db_migration.py)"
Cohesion: 0.13
Nodes (16): Collections (Core Concept), Component Types vs Components, Hybrid Time + Distance Tracking, Mileage Tracking, Understanding Thresholds, Getting Started: Define Component Types, Incidents Page, Workplans Page (+8 more)

### Community 14 - "Service integration (#351) - fullstack to code-reviewer"
Cohesion: 0.12
Nodes (13): Method to add a planned service, which has no service date, bike or distance…, Method to update a service record, including status changes in both directions, Method to recalculate a component after a completed service is deleted or…, Method to validate service records before processing and storing in database, Validation, Bugs found and fixed, Files, Known limitations (+5 more)

### Community 15 - "validateDateInput"
Cohesion: 0.33
Nodes (6): initializeWorkplanForm(), submitCollectionAjax(), submitComponentAjax(), validateCollectionStatusChange(), validateDateInput(), validateWorkplanForm()

### Community 16 - "sortColumn"
Cohesion: 0.29
Nodes (8): initializeCollectionsSorting(), sortColumn(), initializeIncidentTable(), setupIncidentSearch(), setupIncidentStatusFiltering(), setupIncidentTableSorting(), setupWorkplanTableSorting(), updateIncidentVisibility()

### Community 17 - "main.py"
Cohesion: 0.07
Nodes (41): add_collection(), add_incident_record(), add_planned_services(), add_service(), add_workplan(), change_collection_status(), complete_services(), component_modify() (+33 more)

### Community 18 - "Service integration: incidents, workplans and services"
Cohesion: 0.18
Nodes (10): Data model, Error handling, Goal, main.js, Modals, Out of scope, Pages, Service integration: incidents, workplans and services (+2 more)

### Community 19 - ".write_delete_record"
Cohesion: 0.12
Nodes (8): Method to retrieve record for a single component type, Method to retrieve record for a specific entry in the installation log, Method to retrieve a specific service record, Method to retrieve record for a specific collection, Method to retrieve record for a specific incident report, Method to retrieve record for a specific workplan, Method to write component type record in database, Method to delete a given record and associated records

### Community 20 - "business_logic.py"
Cohesion: 0.18
Nodes (11): Module to handle business logic, Module for interaction with a Sqlite database, Module for middleware, Module to interact with Strava APIs, datetime, json, logging, requests_oauthlib (+3 more)

### Community 21 - "get_filtered_log"
Cohesion: 0.50
Nodes (4): get_filtered_log(), Endpoint to read log and return only business events, Function to get filtered log records, read_filtered_logs()

### Community 22 - "Python Requirements List"
Cohesion: 0.25
Nodes (8): APScheduler, Python Requirements List, FastAPI, Jinja2, Peewee ORM, python-multipart, requests-oauthlib, Uvicorn

### Community 24 - ".read_component"
Cohesion: 0.33
Nodes (3): Method to get component names based on list of ids, Method to retrieve record for a specific component, Method to create or update component data to the database

### Community 25 - "What was checked and held up"
Cohesion: 0.17
Nodes (8): Method to read completed services for a component, used by health computation, Method to retrieve the most recent completed service of a given component, Method to retrieve the oldest completed service of a given component, Code review -> docs-maintainer Handover, Context, Recommendations, References, What was checked and held up

### Community 26 - "utils.py"
Cohesion: 0.16
Nodes (13): asyncio, get_current_version(), parse_button_sorting(), Function to get current program version, Module for auxiliary functions, Function to read configuration file, Function to parse button sorting data from form submission, Function to update configuration file based on which form was submitted (+5 more)

### Community 27 - "initializeWorkplanTable"
Cohesion: 0.67
Nodes (4): initializeWorkplanTable(), setupWorkplanSearch(), setupWorkplanStatusFiltering(), updateWorkplansVisibility()

### Community 28 - "version.py"
Cohesion: 0.40
Nodes (4): get_git_info(), Script to maintain version number, Function to get latest version number and commit hash, subprocess

### Community 29 - "CLAUDE.md"
Cohesion: 0.50
Nodes (4): CLAUDE.md, Data Management Tips, Need More Help? (Troubleshooting), Handover Documents Directory (.handovers/)

### Community 30 - "get_workplan_data_tuple"
Cohesion: 0.16
Nodes (17): Method to produce payload for page incident reports, Method to produce payload for workplan details page, calculate_elapsed_days(), derive_workplan_context(), generate_workplan_title(), get_workplan_data_tuple(), get_workplan_names_dict(), Derive bike, component and progress information for a workplan from its services (+9 more)

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
Cohesion: 0.18
Nodes (12): fixture, os, pytest, shutil, sys, app_env(), migrated_env(), modules() (+4 more)

### Community 35 - "get_planned_service_data_tuple"
Cohesion: 0.25
Nodes (8): build_incident_service_entry(), get_effective_planned_date(), get_planned_service_data_tuple(), Return the service's own planned date, else the workplan due date, else None, Describe one service linked to an incident, for the read only list in the…, Build standard planned service tuple for display (11 fields), Status (2026-09-26), Key decisions

### Community 36 - "insert_planned_service_for_migration"
Cohesion: 0.25
Nodes (8): check_incidents_workplan_column_present(), insert_planned_service_for_migration(), migrate_drop_incident_workplan_column(), migrate_incident_links_to_services(), Check if incidents table still has the workplan_id column, Insert a planned service with no date, bike or distance. Returns False if the…, Rebuild incident to workplan links through services, Rebuild incidents table without the workplan_id column

### Community 37 - "seed_component"
Cohesion: 0.15
Nodes (31): add_twin_component(), Planned services must be invisible to health computation, Rides before and after the service dates used below, so distances are not zero, Second installed component on bike-1 with the same settings as comp-1, Create one bike and one installed component with an installation record, seed_component(), seed_rides(), snapshot_health() (+23 more)

### Community 38 - "test_migration.py"
Cohesion: 0.28
Nodes (12): sqlite3, columns(), create_old_schema(), Migration converts the old workplan/incident model to services, Seed workplans, incidents and services in the pre-#351 shape, Recreate services, workplans, incidents and component_history as they were…, run_migration(), seed_old_data() (+4 more)

### Community 39 - "migrate_component_types_time_fields"
Cohesion: 0.50
Nodes (4): check_component_types_time_columns(), migrate_component_types_time_fields(), Check if ComponentTypes table needs time-based fields migration, Add time-based fields to ComponentTypes table

### Community 40 - "generate_unique_id"
Cohesion: 0.16
Nodes (10): Method to add service record, planned or completed, Method to create planned services for one or more components with the same…, Method to add incident record, Method to add workplan, optionally with planned services for components of a…, generate_unique_id(), Function to generates a random and unique ID, Backend, business_logic.py (+2 more)

### Community 41 - "validate_date_format"
Cohesion: 0.17
Nodes (7): Method to update a component history record with validation, Method to validate history records before processing and storing in database, Method to update incident record (supports full or partial updates), Method to update workplan (supports full or partial updates), Method to validate that a workplan can be set to Done, Function to validate that a date string matches the required format YYYY-MM-DD…, validate_date_format()

### Community 42 - "D. Design questions to decide before coding"
Cohesion: 0.18
Nodes (11): Code review outcome, 2026-09-26, D. Design questions to decide before coding, Decisions (2026-09-26), Follow-up tweaks asked for on 2026-09-26, Second round of tweaks, 2026-09-26, Third round of tweaks, 2026-09-26, Warning when resolving an incident with open services, 2026-09-26, initializeIncidentForm() (+3 more)

### Community 43 - "get_incident_data_tuple"
Cohesion: 0.25
Nodes (8): generate_incident_title(), get_formatted_datetime_now(), get_incident_data_tuple(), parse_json_string(), Function to get current datetime formatted as YYYY-MM-DD HH:MM, Build standard incident data tuple for display (17 fields), Function to load a JSON string and return the parsed data as a python object, Generate a concise title for an incident

### Community 45 - "migrate_workplans_to_planned_services"
Cohesion: 0.25
Nodes (8): check_workplans_affected_columns(), migrate_drop_workplan_affected_columns(), migrate_workplans_to_planned_services(), Check if workplans table still has the affected bike/component columns, Resolve bike and component names, marking components that no longer exist, Convert affected components on planned workplans into planned services,…, Rebuild workplans table without the affected bike/component columns, read_names_for_migration()

### Community 47 - "database_manager.py"
Cohesion: 0.11
Nodes (10): Method to read incident records with status 'Open, Method to read workplans with status 'Planned, Method to read all services linked to a specific workplan, planned first, Method to read planned services linked to a specific workplan, Method to read all services linked to a specific incident, planned first, Method to read planned services for a component, Method to read planned services for components installed on a bike, Method to write or update service record in database (+2 more)

### Community 48 - "migrate_workplans_name_column"
Cohesion: 0.50
Nodes (4): check_workplans_name_column(), migrate_workplans_name_column(), Check if workplans table needs the workplan_name column, Add the optional user given name to the workplans table, existing workplans…

### Community 49 - "db_migration.py"
Cohesion: 0.21
Nodes (11): check_component_history_notes_column(), check_component_types_columns(), count_component_types_in_use(), migrate_component_history_notes(), migrate_component_types(), Count how many components use a specific component type, Check if the component_types table needs migration, Migrate the component_types table to add new columns (+3 more)

### Community 50 - "run_all_migrations"
Cohesion: 0.14
Nodes (14): create_collections_table(), create_incidents_table(), create_workplans_table(), populate_component_types_thresholds(), populate_components_thresholds(), Creates the incidents table if it doesn't exist., Creates the workplans table if it doesn't exist., Creates the collections table if it doesn't exist. (+6 more)

### Community 51 - "update_config"
Cohesion: 0.50
Nodes (4): Endpoint to update config file based on which form was submitted, update_config(), Helper function to shutdown the server after a short delay, shutdown_server()

### Community 52 - "Results"
Cohesion: 0.25
Nodes (7): 2026-09-25, first walkthrough, human, 2026-09-26, regression against the baseline database, Claude, 2026-09-27, second walkthrough, human, Preparation, Results, Scope, Test Protocol: Planned services, workplans and incidents

### Community 53 - "get_formatted_bikes_list"
Cohesion: 0.50
Nodes (3): Method to produce payload for page of all workplans, get_formatted_bikes_list(), Function to get list of all bikes, with prefix for retired bikes

### Community 54 - "migrate_database"
Cohesion: 0.33
Nodes (6): find_database_file(), migrate_database(), prompt_for_db_path(), Search for a database file in the user's home directory and subdirectories, Prompt user for database path or filename and verify it exists, Main function to handle the database migration.

### Community 56 - "renderPreview"
Cohesion: 0.50
Nodes (4): containsMarkdown(), renderPreview(), setInitialMode(), updateCheckboxInText()

### Community 57 - "migrate_services_workplan_link"
Cohesion: 0.50
Nodes (4): check_services_workplan_column(), migrate_services_workplan_link(), Check if Services table needs workplan_id column, Add workplan_id column to Services table for workplan hub integration

### Community 61 - "config_overview"
Cohesion: 0.50
Nodes (4): config_overview(), Endpoint for component types page, get_button_sorting_config(), Function to get button sorting configuration for config page

### Community 65 - "Git Workflow Rules"
Cohesion: 0.25
Nodes (8): Version Script CI Workflow, Branch Strategy, Commit Process, For All Agents, For code-reviewer, For docs-maintainer, For fullstack-developer, Git Workflow Rules

### Community 66 - "initializeComponentSelector"
Cohesion: 0.67
Nodes (3): editCollection(), initializeComponentSelector(), updateFormFields()

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
Cohesion: 0.40
Nodes (5): Database Schema Changes, Development Notes, Docker Development, Logging, Technical Debt

### Community 110 - "Standard Development Workflow"
Cohesion: 0.50
Nodes (4): For Bug Fixes, For Documentation Updates, For New Features, Standard Development Workflow

### Community 111 - "Sub-Agent Team"
Cohesion: 0.67
Nodes (3): Available Agents, Direct Invocation, Sub-Agent Team

### Community 112 - "Testing Requirements"
Cohesion: 0.67
Nodes (3): Before Creating Handover, For fullstack-developer, Testing Requirements

### Community 119 - "Service integration (#351): findings from the manual test walkthrough"
Cohesion: 0.17
Nodes (10): A. Questions to answer from the code, no change expected, B. Bugs to fix, C. Interface changes the user asked for, Extra wording fixes asked for on 2026-09-26, Re-test list for the second round, Service integration (#351): findings from the manual test walkthrough, Status (2026-09-26), Status (2026-09-26) (+2 more)

## Ambiguous Edges - Review These
- `Version Script CI Workflow` → `Git Workflow Rules`  [AMBIGUOUS]
  .github/workflows/run_version_script.yml · relation: conceptually_related_to

## Knowledge Gaps
- **165 isolated node(s):** `What was built`, `Testing`, `Known limitations`, `Regression evidence, 2026-09-26`, `Next steps` (+160 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 501 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **47 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `Version Script CI Workflow` and `Git Workflow Rules`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **Why does `DatabaseManager` connect `DatabaseManager` to `.get_bike_details`, `.process_service_records`, `get`, `.write_delete_record`, `business_logic.py`, `.read_single_bike`, `.read_component`, `What was checked and held up`, `.read_incidents_by_workplan`, `database_manager.py`, `.read_all_workplans`, `.read_bike_id_recent_component_history`, `.read_bikes`, `.read_subset_component_history`, `.read_matching_rides`, `.read_all_components_objects`, `.read_recent_rides`, `.read_unique_bikes`, `.write_component_lifetime_status`, `.write_incident_record`, `.count_component_types_in_use`, `.read_date_oldest_ride`, `.write_component_distance`, `.read_workplans_by_incident`, `.write_collection`, `.write_component_service_status`?**
  _High betweenness centrality (0.153) - this node is a cross-community bridge._
- **Why does `BusinessLogic` connect `BusinessLogic` to `.get_bike_details`, `scheduler.py`, `.process_service_records`, `generate_unique_id`, `validate_date_format`, `.create_history_record`, `.complete_services`, `Service integration (#351) - fullstack to code-reviewer`, `business_logic.py`, `get_formatted_bikes_list`, `get_workplan_data_tuple`?**
  _High betweenness centrality (0.107) - this node is a cross-community bridge._
- **Why does `renderIncidentServices()` connect `D. Design questions to decide before coding` to `get`, `main.js`?**
  _High betweenness centrality (0.066) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `BusinessLogic` (e.g. with `strava_sync_job()` and `update_time_based_fields_job()`) actually correct?**
  _`BusinessLogic` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `What was built`, `Testing`, `Known limitations` to the rest of the system?**
  _165 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `.get_bike_details` be split into smaller, more focused modules?**
  _Cohesion score 0.12318840579710146 - nodes in this community are weakly interconnected._