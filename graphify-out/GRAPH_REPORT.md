# Graph Report - velo-supervisor-2000  (2026-10-01)

## Corpus Check
- 44 files · ~148,274 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 12 file(s) not represented in the graph (top: (none) 5, .example 1, .sqlite 1)

## Summary
- 1076 nodes · 1780 edges · 150 communities (86 shown, 64 thin omitted)
- Extraction: 84% EXTRACTED · 16% INFERRED · 0% AMBIGUOUS · INFERRED: 279 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `886eaae4`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- main.py
- scheduler.py
- get
- seed_component
- Meta
- main.js
- .get_bike_details
- README.md
- DatabaseManager
- database_manager.py
- Bike Details Template
- .process_service_records
- get_workplan_data_tuple
- .recalculate_component_after_service_removal
- BusinessLogic
- Strava
- 2026-09-18-service-integration-design.md
- generate_unique_id
- utils.py
- run_all_migrations
- Health check for Docker daemon (#103)
- Fullstack Developer -> Code Reviewer Handover
- 2026-09-25-service-integration-test-findings.md
- Service integration: incidents, workplans and services
- test_migration.py
- code-reviewer -> docs-maintainer Handover
- validate_date_format
- .write_delete_record
- conftest.py
- test_health.py
- ErrorRecorder
- Code Reviewer -> Docs Maintainer Handover
- .create_workplan
- D. Design questions to decide before coding
- Base Template
- .create_component
- migrate_incidents_workplan_link
- CLAUDE.md
- Git Workflow Rules
- db_migration.py
- migrate_workplans_to_planned_services
- CLAUDE.md
- code-reviewer.md
- validateDateInput
- initializeWorkplanTable
- [Source Agent] -> [Target Agent] Handover
- health-check-reviewer-to-docs-maintainer.md
- help_page
- database-expert.md
- ux-designer.md
- service-integration-fullstack-to-reviewer.md
- Service integration (#351) - fullstack to code-reviewer
- Results
- .update_components_distance_iterator
- .read_component
- migrate_incident_links_to_services
- migrate_database
- get_planned_service_data_tuple
- Agent Communication via Handovers
- fullstack-developer.md
- product-manager.md
- get_incident_data_tuple
- validateComponentThresholds
- Handovers Directory
- version.py
- architect.md
- Architecture Overview
- Development Commands
- Development Notes
- get_service_incident_options
- .read_single_bike
- .read_single_component_type
- migrate_component_history_notes
- migrate_component_types_time_fields
- initializeDatePickers
- migrate_services_workplan_link
- migrate_workplans_name_column
- get_filtered_log
- update_config
- docs-maintainer.md
- Code Style & Standards
- Standard Development Workflow
- cleanup
- renderPreview
- initializeIncidentTable
- handleOldComponentChange
- .write_component_distance
- Testing Requirements
- Middleware
- .read_all_component_types
- .read_all_components_objects
- .read_all_workplans
- .read_collection_by_component
- .read_date_oldest_ride
- .read_matching_rides
- .read_recent_rides
- .read_subset_component_history
- .read_subset_components
- .read_unique_bikes
- .read_bike_id_recent_component_history
- .write_collection
- .write_incident_record
- .read_incidents_by_workplan
- backup_db.sh
- create-container-vs2000.sh
- Strava profile:read_all Scope Troubleshooting
- Dev/Staging/Master Branch Workflow
- Changelog Section
- Error Page Illustration
- Velo Supervisor Fox Mechanic Logo
- Collections (Core Concept)
- Component Types vs Components
- Hybrid Time + Distance Tracking
- Mileage Tracking
- Understanding Thresholds
- Getting Started: Define Component Types
- Component Types Page
- Config Page (Strava Sync)
- Incidents Page
- Workplans Page
- Data Management Tips
- Need More Help? (Troubleshooting)
- Confirm Action Modal
- Loading Modal
- Report Modal
- Validation Error Modal
- velo-supervisor-2000
- Graphify Knowledge Graph Auto-Update Mechanism
- Manual Onboarding Setup Procedure
- Q1 2025 Piloting Program
- v0.1.0 Release
- v0.2.0 Release
- v0.3.0 Release
- v0.3.1 Release
- v0.4.0 Release
- v0.4.1 Release
- v0.4.2 Release
- v0.4.3 Release
- v0.4.4 Release
- v0.4.5 Release
- v0.4.6 Release
- v0.4.7 Release
- v0.4.8 Release
- v0.4.9 Release (Current)
- .read_latest_ride_record
- .read_sum_distance_subset_rides
- .write_component_lifetime_status
- .write_component_service_status
- .write_workplan

## God Nodes (most connected - your core abstractions)
1. `DatabaseManager` - 71 edges
2. `BusinessLogic` - 65 edges
3. `run_all_migrations()` - 24 edges
4. `seed_component()` - 24 edges
5. `Meta` - 20 edges
6. `seed_rides()` - 20 edges
7. `Bike Details Template` - 19 edges
8. `Component Details Template` - 18 edges
9. `get_workplan_data_tuple()` - 17 edges
10. `get_incident_data_tuple()` - 15 edges

## Surprising Connections (you probably didn't know these)
- `Deliverables` --references--> `ErrorRecorder`  [INFERRED]
  .handovers/fullstack/health-check-fullstack-to-reviewer.md → backend/utils.py
- `Migration` --references--> `generate_unique_id()`  [INFERRED]
  docs/superpowers/specs/2026-09-18-service-integration-design.md → backend/utils.py
- `Context` --references--> `get_service_incident_options()`  [INFERRED]
  .handovers/documentation/post-release-fixes-docs-maintainer-to-human.md → backend/utils.py
- `Deliverables (files reviewed)` --references--> `get_service_incident_options()`  [INFERRED]
  .handovers/review/post-release-fixes-reviewer-to-docs-maintainer.md → backend/utils.py
- `Findings` --references--> `get_service_incident_options()`  [INFERRED]
  .handovers/review/post-release-fixes-reviewer-to-docs-maintainer.md → backend/utils.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Health check mechanism (#103)** — backend_utils_errorrecorder, backend_utils_get_health_status, backend_database_manager_databasemanager_check_database_connection, backend_main_health, backend_healthcheck, handovers_fullstack_health_check_fullstack_to_reviewer_health_check_feature [EXTRACTED 1.00]
- **Planned services invisible to health** — docs_superpowers_specs_2026_09_18_service_integration_design_planned_invisible_to_health, backend_database_manager_databasemanager_read_latest_service_record, backend_business_logic_businesslogic_process_service_records, backend_business_logic_businesslogic_update_component_service_status, backend_database_model_services [EXTRACTED 1.00]
- **Service integration spec, implementation, test and review cycle** — docs_superpowers_specs_2026_09_18_service_integration_design, handovers_fullstack_service_integration_fullstack_to_reviewer, docs_superpowers_plans_2026_09_25_service_integration_test_findings, tests_test_protocol_services, handovers_review_service_integration_reviewer_to_docs_maintainer [EXTRACTED 1.00]
- **Installation Status Change Forms** — frontend_templates_modal_install_component_installcomponentmodal, frontend_templates_modal_update_component_status_editcomponentstatusmodal, frontend_templates_modal_edit_installation_record_edithistorymodal, frontend_templates_modal_quick_swap_quickswapmodal, backend_main_add_history_record [INFERRED 0.85]
- **Incident to Workplan to Completed Services Flow** — frontend_templates_modal_incident_record_incidentrecordmodal, frontend_templates_modal_workplan_record_workplanrecordmodal, frontend_templates_modal_plan_services_planservicesmodal, frontend_templates_modal_complete_services_completeservicesmodal, frontend_templates_modal_complete_workplan_template, frontend_templates_help_common_tasks_incident_to_finished_work [INFERRED 0.85]
- **Plan and Complete Services Workflow** — frontend_templates_modal_plan_services_planservicesmodal, frontend_templates_modal_complete_services_completeservicesmodal, backend_main_add_planned_services, backend_main_complete_services, frontend_templates_modal_service_record_servicerecordmodal, frontend_templates_help_common_tasks_planning_service [INFERRED 0.85]

## Communities (150 total, 64 thin omitted)

### Community 0 - "main.py"
Cohesion: 0.06
Nodes (43): asyncio, add_collection(), add_incident_record(), add_planned_services(), add_service(), add_workplan(), change_collection_status(), complete_services() (+35 more)

### Community 1 - "scheduler.py"
Cohesion: 0.09
Nodes (26): apscheduler_schedulers_asyncio, apscheduler_triggers_cron, apscheduler_triggers_interval, Module to handle business logic, Module for interaction with a Sqlite database, lifespan(), Manage application startup and shutdown, Module for middleware (+18 more)

### Community 2 - "get"
Cohesion: 0.08
Nodes (32): add_history_record(), bike_details(), collection_details(), component_details(), component_overview(), component_types_overview(), config_overview(), incident_reports() (+24 more)

### Community 3 - "seed_component"
Cohesion: 0.15
Nodes (31): add_twin_component(), Planned services must be invisible to health computation, Rides before and after the service dates used below, so distances are not zero, Second installed component on bike-1 with the same settings as comp-1, Create one bike and one installed component with an installation record, seed_component(), seed_rides(), snapshot_health() (+23 more)

### Community 4 - "Meta"
Cohesion: 0.08
Nodes (36): BaseModel, Bikes, Collections, ComponentHistory, Components, ComponentTypes, Incidents, Meta (+28 more)

### Community 5 - "main.js"
Cohesion: 0.09
Nodes (10): editCollection(), handleUpdate(), initializeCollectionsSearch(), updateRowVisibility(), initializeComponentSelector(), performQuickSwap(), NOTE: All collection details page handlers are in the "Functions used on…, IMPORTANT: Remove readonly - allow manual typing (+2 more)

### Community 6 - ".get_bike_details"
Cohesion: 0.10
Nodes (18): Method to produce payload for page component overview, Method to produce payload for page component details, Method to determine which factor triggered a warning status, Calculate lifetime and service triggers for a component, Method to produce payload for page bike overview, Method to create component-to-collection mapping dictionaries, Method to produce payload for displaying table of all collections, Method to build dictionaries of bike and component ids referenced in received… (+10 more)

### Community 7 - "README.md"
Cohesion: 0.33
Nodes (5): v0.5.0.ca636f8, Release notes live in README version list (no CHANGELOG.md), Strava OAuth scope incl. profile:read_all, Switched from pip to uv, GitHub action writes current_version.txt on master

### Community 8 - "DatabaseManager"
Cohesion: 0.08
Nodes (13): DatabaseManager, Method to count how many components that references a given component type, Class to interact with a SQLite database through Peewee, Method to read installed components for a specific bike, Method to retrieve the most recent record from the installation log of a given…, Method to retrieve the oldest record from the installation log of a given…, Method to retrieve record for a specific entry in the service log, Method to read all collections (+5 more)

### Community 9 - "database_manager.py"
Cohesion: 0.08
Nodes (13): Method to read completed services for a component, used by health computation, Method to retrieve the most recent completed service of a given component, Method to retrieve the oldest completed service of a given component, Method to read incident records with status 'Open, Method to read workplans with status 'Planned, Method to read all services linked to a specific workplan, planned first, Method to read planned services linked to a specific workplan, Method to read all services linked to a specific incident, planned first (+5 more)

### Community 10 - "Bike Details Template"
Cohesion: 0.24
Nodes (24): Bike Details Template, Collection Details Template, Page Warning Cards Pattern, Component Details Template, Component Overview Template, From Incident to Finished Work (Help), Planning Service Before You Do It (Help), Quick Swap Components (+16 more)

### Community 11 - ".process_service_records"
Cohesion: 0.13
Nodes (14): Method to update component lifetime and service status when no installation…, Method to update status for a given bike based on component service and…, Method to calculate distance and bike id for history records, Method to calculate distance and bike id for service records, Method to compute component status using threshold logic, Method to determine worst-case status between distance and days-based…, Method to update time-based status fields for all non-retired components, Method to delete a given record and associated records (+6 more)

### Community 12 - "get_workplan_data_tuple"
Cohesion: 0.15
Nodes (21): Method to produce payload for workplan details page, derive_workplan_context(), generate_workplan_title(), get_workplan_data_tuple(), get_workplan_names_dict(), Derive bike, component and progress information for a workplan from its services, Return the name the user gave the workplan, or a generated title when there is…, Build dictionary mapping workplan_id -> workplan_name for all workplans (+13 more)

### Community 13 - ".recalculate_component_after_service_removal"
Cohesion: 0.15
Nodes (12): Method to add service record, planned or completed, Method to add a planned service, which has no service date, bike or distance…, Method to build the report used by the plan services and complete services…, Method to create planned services for one or more components with the same…, Method to complete planned services with one service date, keeping their…, Method to update a service record, including status changes in both directions, Method to recalculate a component after a completed service is deleted or…, Method to validate service records before processing and storing in database (+4 more)

### Community 14 - "BusinessLogic"
Cohesion: 0.11
Nodes (13): BusinessLogic, Method to create installation history record, Method to orchestrate swap of one component with another, Method to validate quick swap operation, Method to create collection, Method to update collection, Method to validate collections before allowing bulk operations, Method to change status of all components in a collection (+5 more)

### Community 15 - "Strava"
Cohesion: 0.18
Nodes (9): Class to interact with Strava API, Method to authenticate and get data from Stravas gear API, Method to prepare a list of rides, Method to prepare a list of bikes, Method to read oauth options from file, Method to save oauth options to file, Method to authenticate and get data from Stravas activities API, Method to authenticate and get the full list of bike ids from the athlete's… (+1 more)

### Community 16 - "2026-09-18-service-integration-design.md"
Cohesion: 0.17
Nodes (13): Blank values always NULL, never empty strings, Migration steps 12-16 (idempotent check_/migrate_ pairs), Planned services invisible to component health, Planned vs Completed service status, Retired components locked (no service status changes), validate_service_record modes (plan/complete/edit/revert), Production DB regression comparison (master vs branch), Retirement blocked while planned services exist (+5 more)

### Community 17 - "generate_unique_id"
Cohesion: 0.33
Nodes (5): Method to add incident record, insert_planned_service_for_migration(), Insert a planned service with no date, bike or distance. Returns False if the…, generate_unique_id(), Function to generates a random and unique ID

### Community 18 - "utils.py"
Cohesion: 0.16
Nodes (13): get_current_version(), parse_button_sorting(), Function to get current program version, Module for auxiliary functions, Function to read configuration file, Function to parse button sorting data from form submission, Function to update configuration file based on which form was submitted, read_config() (+5 more)

### Community 19 - "run_all_migrations"
Cohesion: 0.14
Nodes (14): create_collections_table(), create_incidents_table(), create_workplans_table(), populate_component_types_thresholds(), populate_components_thresholds(), Creates the incidents table if it doesn't exist., Creates the workplans table if it doesn't exist., Creates the collections table if it doesn't exist. (+6 more)

### Community 20 - "Health check for Docker daemon (#103)"
Cohesion: 0.21
Nodes (11): Health check run by the Docker daemon, exit code 0 means healthy and 1 means…, health(), Endpoint for the Docker health check, returns 503 if errors were logged the…, get_health_status(), Function to assess application health from errors logged the last 24 hours and…, Docker HEALTHCHECK against /health, Health check for Docker daemon (#103), Separate healthcheck.py instead of curl (+3 more)

### Community 21 - "Fullstack Developer -> Code Reviewer Handover"
Cohesion: 0.18
Nodes (10): Method to store error records and ignore lower levels. Filters here instead of…, Method to get error records newer than the given number of hours, Blockers / Open Questions, Context, Decisions Made, Deliverables, Fullstack Developer -> Code Reviewer Handover, Next Steps for Code Reviewer (+2 more)

### Community 22 - "2026-09-25-service-integration-test-findings.md"
Cohesion: 0.17
Nodes (12): A5: workplan delete blocked while services linked, A. Questions to answer from the code, no change expected, C. Interface changes the user asked for, D2: incident modal lists linked services, Extra wording fixes asked for on 2026-09-26, Manual walkthrough findings (A/B/C/D groups), Re-test list for the second round, Service integration (#351): findings from the manual test walkthrough (+4 more)

### Community 23 - "Service integration: incidents, workplans and services"
Cohesion: 0.15
Nodes (13): Backend, Data model, Error handling, Goal, main.js, main.py, Migration, Modals (+5 more)

### Community 24 - "test_migration.py"
Cohesion: 0.28
Nodes (12): sqlite3, columns(), create_old_schema(), Migration converts the old workplan/incident model to services, Seed workplans, incidents and services in the pre-#351 shape, Recreate services, workplans, incidents and component_history as they were…, run_migration(), seed_old_data() (+4 more)

### Community 25 - "code-reviewer -> docs-maintainer Handover"
Cohesion: 0.10
Nodes (20): Context, Docs changes, docs-maintainer -> Human Handover, Double-check, Files to commit, Option A: one commit, Option B: three commits (main.js needs `git add -p`), Post-release fixes to v0.5.0 (+12 more)

### Community 26 - "validate_date_format"
Cohesion: 0.17
Nodes (7): Method to update a component history record with validation, Method to validate history records before processing and storing in database, Method to update incident record (supports full or partial updates), Method to update workplan (supports full or partial updates), Method to validate that a workplan can be set to Done, Function to validate that a date string matches the required format YYYY-MM-DD…, validate_date_format()

### Community 27 - ".write_delete_record"
Cohesion: 0.17
Nodes (6): Method to retrieve record for a specific entry in the installation log, Method to retrieve a specific service record, Method to retrieve record for a specific collection, Method to retrieve record for a specific incident report, Method to retrieve record for a specific workplan, Method to delete a given record and associated records

### Community 28 - "conftest.py"
Cohesion: 0.18
Nodes (12): fixture, os, pytest, shutil, sys, app_env(), migrated_env(), modules() (+4 more)

### Community 29 - "test_health.py"
Cohesion: 0.23
Nodes (9): Verification done, Health check: errors logged the last 24 hours or a failing database make the…, lifespan in main.py sets every root handler to INFO or DEBUG at startup, SQLite creates an empty file for a wrong path, e.g. a missing Docker mount, recording_logger(), test_missing_database_file_makes_app_unhealthy(), test_recorder_includes_exception_in_message(), test_recorder_keeps_errors_and_ignores_lower_levels() (+1 more)

### Community 30 - "ErrorRecorder"
Cohesion: 0.32
Nodes (6): ErrorRecorder, Logging handler that keeps the most recent error records in memory for the…, Log levels drive container health, Level filtering inside ErrorRecorder.emit(), In-memory 24h error record, ERROR vs WARNING log level rule

### Community 31 - "Code Reviewer -> Docs Maintainer Handover"
Cohesion: 0.20
Nodes (9): Method to check the database connection for the health check, Code Reviewer -> Docs Maintainer Handover, Context, Deliverables, Issues Found, Next Steps for Docs Maintainer, References, Resolution (2026-09-27, after review) (+1 more)

### Community 32 - ".create_workplan"
Cohesion: 0.22
Nodes (8): Method to add workplan, optionally with planned services for components of a…, build_incident_service_entry(), parse_json_string(), Describe one service linked to an incident, for the read only list in the…, Function to load a JSON string and return the parsed data as a python object, D4: choose components when creating workplan from incident, Status (2026-09-26), Second round, 2026-09-26, after the manual walkthrough

### Community 33 - "D. Design questions to decide before coding"
Cohesion: 0.33
Nodes (6): D. Design questions to decide before coding, Decisions (2026-09-26), Follow-up tweaks asked for on 2026-09-26, Second round of tweaks, 2026-09-26, Third round of tweaks, 2026-09-26, Warning when resolving an incident with open services, 2026-09-26

### Community 34 - "Base Template"
Cohesion: 0.24
Nodes (10): Base Template, Component Types Template, Config Template, Error Page Template, Footer Template, Bike Overview Template, nav_menu Macro, Navigation Menu Template (+2 more)

### Community 35 - ".create_component"
Cohesion: 0.20
Nodes (6): Method to create component, Method to update component details, Validate threshold configuration rules for component intervals, Method to check if a bike has all mandatory components and respects max…, Method to create or update component types, Method to update only the count of components for a given component type

### Community 36 - "migrate_incidents_workplan_link"
Cohesion: 0.22
Nodes (9): check_incidents_workplan_column(), check_services_integration_columns(), migrate_incidents_workplan_link(), migrate_services_integration_columns(), Check if Incidents table needs workplan_id column, Add workplan_id column to Incidents table for workplan hub integration, Check which service integration columns are missing on the services table, Add status, incident_id and planned_date to services, mark existing rows… (+1 more)

### Community 37 - "CLAUDE.md"
Cohesion: 0.22
Nodes (8): Available Agents, Communication & Output Rules, Debugging & Bug Fixing Rules, Direct Invocation, graphify, Important Notes, Project Overview, Sub-Agent Team

### Community 38 - "Git Workflow Rules"
Cohesion: 0.25
Nodes (8): Version Script CI Workflow, Branch Strategy, Commit Process, For All Agents, For code-reviewer, For docs-maintainer, For fullstack-developer, Git Workflow Rules

### Community 39 - "db_migration.py"
Cohesion: 0.21
Nodes (11): check_component_types_columns(), check_components_time_columns(), count_component_types_in_use(), migrate_component_types(), migrate_components_time_fields(), Count how many components use a specific component type, Check if the component_types table needs migration, Migrate the component_types table to add new columns (+3 more)

### Community 40 - "migrate_workplans_to_planned_services"
Cohesion: 0.25
Nodes (8): check_workplans_affected_columns(), migrate_drop_workplan_affected_columns(), migrate_workplans_to_planned_services(), Check if workplans table still has the affected bike/component columns, Resolve bike and component names, marking components that no longer exist, Convert affected components on planned workplans into planned services,…, Rebuild workplans table without the affected bike/component columns, read_names_for_migration()

### Community 41 - "CLAUDE.md"
Cohesion: 0.25
Nodes (7): Change Management Rules, Debugging & bug fixing rules (root cause first), graphify knowledge graph usage rules, Agent handover documents (.handovers/), Technical debt tracked in issue #356, TomSelect multi-select pattern, Stale ID 500 marks container unhealthy 24h (known limitation)

### Community 42 - "code-reviewer.md"
Cohesion: 0.25
Nodes (7): Issues Found, Key Checks, Output Format, Recommendations, Review Philosophy, Review Process, Summary

### Community 43 - "validateDateInput"
Cohesion: 0.17
Nodes (12): Warn (not block) when resolving incident with planned services, Validation, initializeIncidentForm(), initializeWorkplanForm(), submitCollectionAjax(), submitComponentAjax(), validateCollectionStatusChange(), validateDateInput() (+4 more)

### Community 44 - "initializeWorkplanTable"
Cohesion: 0.29
Nodes (8): initializeCollectionsSorting(), sortColumn(), initializeWorkplanTable(), setupIncidentTableSorting(), setupWorkplanSearch(), setupWorkplanStatusFiltering(), setupWorkplanTableSorting(), updateWorkplansVisibility()

### Community 45 - "[Source Agent] -> [Target Agent] Handover"
Cohesion: 0.25
Nodes (7): Blockers / Open Questions, Context, Decisions Made, Deliverables, Next Steps for [Target Agent], References, [Source Agent] -> [Target Agent] Handover

### Community 46 - "health-check-reviewer-to-docs-maintainer.md"
Cohesion: 0.32
Nodes (6): Method to check that the database can be read. Reads a real table, since SELECT…, Database check reads bikes table, not SELECT 1, Rename read_database_connection to check_database_connection, ErrorRecorder deque bounded to maxlen=20, ErrorRecorder thread safety under Handler.lock, Catching peewee.DatabaseError for corrupt file

### Community 47 - "help_page"
Cohesion: 0.33
Nodes (7): help_page(), Endpoint for help page, helpTopics Data Object, Help Page Template, Help Search Functionality, showHelpTopic() Function, Documentation Modal

### Community 48 - "database-expert.md"
Cohesion: 0.29
Nodes (6): Constraints, Core Responsibilities, Pattern Consistency - CRITICAL, Query Optimization, Schema Changes, Workflow

### Community 49 - "ux-designer.md"
Cohesion: 0.29
Nodes (6): Core Responsibilities, Design Principles, Specifications to Include, v1 (Before Architect), v2 (After Architect), Workflow

### Community 50 - "service-integration-fullstack-to-reviewer.md"
Cohesion: 0.36
Nodes (7): D1: optional user-entered workplan name, Service integration: services as unit of work (#351), FastAPI/Starlette TemplateResponse argument order fix, Workplan link silently lost bug (process_service_records without workplan_id), Optional workplan_name (migration step 17), db_migration step 16 rebuild before step 17 workplan_name, v0.5.0 release (service integration, health check, uv)

### Community 51 - "Service integration (#351) - fullstack to code-reviewer"
Cohesion: 0.29
Nodes (7): Bugs found and fixed, Known limitations, Next steps, Regression evidence, 2026-09-26, Service integration (#351) - fullstack to code-reviewer, Testing, What was built

### Community 52 - "Results"
Cohesion: 0.29
Nodes (7): 2026-09-25, first walkthrough, human, 2026-09-26, regression against the baseline database, Claude, 2026-09-27, second walkthrough, human, Preparation, Results, Scope, Test Protocol: Planned services, workplans and incidents

### Community 53 - ".update_components_distance_iterator"
Cohesion: 0.33
Nodes (3): Function to set the date for last pull from Strava, Method to create or update ride data in bulk to database, Method to determine which selection of components to update

### Community 54 - ".read_component"
Cohesion: 0.33
Nodes (3): Method to get component names based on list of ids, Method to retrieve record for a specific component, Method to create or update component data to the database

### Community 55 - "migrate_incident_links_to_services"
Cohesion: 0.33
Nodes (6): check_incidents_workplan_column_present(), migrate_drop_incident_workplan_column(), migrate_incident_links_to_services(), Check if incidents table still has the workplan_id column, Rebuild incident to workplan links through services, Rebuild incidents table without the workplan_id column

### Community 56 - "migrate_database"
Cohesion: 0.33
Nodes (6): find_database_file(), migrate_database(), prompt_for_db_path(), Search for a database file in the user's home directory and subdirectories, Prompt user for database path or filename and verify it exists, Main function to handle the database migration.

### Community 57 - "get_planned_service_data_tuple"
Cohesion: 0.29
Nodes (7): get_effective_planned_date(), get_planned_service_data_tuple(), Return the service's own planned date, else the workplan due date, else None, Build standard planned service tuple for display (11 fields), Effective planned date fallback, Key decisions, Tuple shapes: incident 17, workplan 14, planned service 11 fields

### Community 58 - "Agent Communication via Handovers"
Cohesion: 0.33
Nodes (6): Agent Communication via Handovers, Creating Handovers, Detailed Instructions, Handover Structure, Naming Convention, Reading Handovers

### Community 59 - "fullstack-developer.md"
Cohesion: 0.33
Nodes (5): Backend Patterns, Core Responsibilities, Frontend Patterns, Handover Content, Workflow

### Community 60 - "product-manager.md"
Cohesion: 0.33
Nodes (5): Boundaries, Core Responsibilities, Key Principle: You Are Interactive, Requirements Document, User Story Format

### Community 61 - "get_incident_data_tuple"
Cohesion: 0.33
Nodes (6): calculate_elapsed_days(), get_formatted_datetime_now(), get_incident_data_tuple(), Function to get current datetime formatted as YYYY-MM-DD HH:MM, Build standard incident data tuple for display (17 fields), Function to calculate the number of days between two dates

### Community 62 - "validateComponentThresholds"
Cohesion: 0.40
Nodes (5): addFormValidation(), clearValidationErrors(), showFieldError(), validateComponentThresholds(), validateQuickSwapForm()

### Community 63 - "Handovers Directory"
Cohesion: 0.33
Nodes (5): Creating Handovers, Directory Structure, Finding Handovers, Handovers Directory, Rules

### Community 64 - "version.py"
Cohesion: 0.40
Nodes (4): get_git_info(), Script to maintain version number, Function to get latest version number and commit hash, subprocess

### Community 65 - "architect.md"
Cohesion: 0.40
Nodes (4): Core Responsibilities, Handover Content, Principles, Workflow

### Community 66 - "Architecture Overview"
Cohesion: 0.40
Nodes (5): Architecture Overview, Configuration, Core Components, Key Features, Project Structure

### Community 67 - "Development Commands"
Cohesion: 0.40
Nodes (5): Database Operations, Dependencies, Development Commands, Running the Application, Testing

### Community 68 - "Development Notes"
Cohesion: 0.40
Nodes (5): Database Schema Changes, Development Notes, Docker Development, Logging, Technical Debt

### Community 69 - "get_service_incident_options"
Cohesion: 0.20
Nodes (9): Method to produce payload for page incident reports, Method to produce payload for page of all workplans, generate_incident_title(), get_formatted_bikes_list(), get_service_incident_options(), Function to get list of all bikes, with prefix for retired bikes, Build incident options for the service modal (4 fields), all incidents so…, Generate a concise title for an incident (+1 more)

### Community 72 - "migrate_component_history_notes"
Cohesion: 0.50
Nodes (4): check_component_history_notes_column(), migrate_component_history_notes(), Check if component_history table needs notes column, Add notes column to component_history table

### Community 73 - "migrate_component_types_time_fields"
Cohesion: 0.50
Nodes (4): check_component_types_time_columns(), migrate_component_types_time_fields(), Check if ComponentTypes table needs time-based fields migration, Add time-based fields to ComponentTypes table

### Community 74 - "initializeDatePickers"
Cohesion: 0.40
Nodes (5): B3: service modal submittable without completion date, B. Bugs to fix, Status (2026-09-26), initializeDatePickers(), Date picker form.onsubmit wrapper fix

### Community 75 - "migrate_services_workplan_link"
Cohesion: 0.50
Nodes (4): check_services_workplan_column(), migrate_services_workplan_link(), Check if Services table needs workplan_id column, Add workplan_id column to Services table for workplan hub integration

### Community 76 - "migrate_workplans_name_column"
Cohesion: 0.50
Nodes (4): check_workplans_name_column(), migrate_workplans_name_column(), Check if workplans table needs the workplan_name column, Add the optional user given name to the workplans table, existing workplans…

### Community 77 - "get_filtered_log"
Cohesion: 0.50
Nodes (4): get_filtered_log(), Endpoint to read log and return only business events, Function to get filtered log records, read_filtered_logs()

### Community 78 - "update_config"
Cohesion: 0.50
Nodes (4): Endpoint to update config file based on which form was submitted, update_config(), Helper function to shutdown the server after a short delay, shutdown_server()

### Community 79 - "docs-maintainer.md"
Cohesion: 0.50
Nodes (3): Core Responsibilities, Documentation Rules, Workflow

### Community 80 - "Code Style & Standards"
Cohesion: 0.50
Nodes (4): Code Style & Standards, Database, Frontend, Python (Backend)

### Community 81 - "Standard Development Workflow"
Cohesion: 0.50
Nodes (4): For Bug Fixes, For Documentation Updates, For New Features, Standard Development Workflow

### Community 82 - "cleanup"
Cohesion: 0.50
Nodes (4): cleanup(), handleCancel(), handleConfirm(), performBulkStatusChange()

### Community 83 - "renderPreview"
Cohesion: 0.50
Nodes (4): containsMarkdown(), renderPreview(), setInitialMode(), updateCheckboxInText()

### Community 84 - "initializeIncidentTable"
Cohesion: 0.67
Nodes (4): initializeIncidentTable(), setupIncidentSearch(), setupIncidentStatusFiltering(), updateIncidentVisibility()

### Community 85 - "handleOldComponentChange"
Cohesion: 0.67
Nodes (3): filterNewComponentsByType(), handleOldComponentChange(), updateQuickSwapCollectionWarning()

### Community 87 - "Testing Requirements"
Cohesion: 0.67
Nodes (3): Before Creating Handover, For fullstack-developer, Testing Requirements

### Community 88 - "Middleware"
Cohesion: 0.16
Nodes (11): http_exception_handler(), Function to catch http errors from Uvicorn and return them to the middleware, Middleware, Request, Class to handle exceptions that breaks the program and should be shown to the…, Method to dispatch intercepted requests, Method to catch and handle exceptions, BaseHTTPMiddleware (+3 more)

## Ambiguous Edges - Review These
- `conftest.py` → `Manual testing protocols approach`  [AMBIGUOUS]
  tests/README.md · relation: conceptually_related_to
- `Version Script CI Workflow` → `Git Workflow Rules`  [AMBIGUOUS]
  .github/workflows/run_version_script.yml · relation: conceptually_related_to

## Knowledge Gaps
- **184 isolated node(s):** `backup_db.sh script`, `create-container-vs2000.sh script`, `velo-supervisor-2000`, `Core Responsibilities`, `Workflow` (+179 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 532 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **64 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `conftest.py` and `Manual testing protocols approach`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `Version Script CI Workflow` and `Git Workflow Rules`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **Why does `DatabaseManager` connect `DatabaseManager` to `scheduler.py`, `Meta`, `.get_bike_details`, `database_manager.py`, `.read_latest_ride_record`, `.read_sum_distance_subset_rides`, `.write_component_lifetime_status`, `.write_component_service_status`, `.write_workplan`, `.write_delete_record`, `health-check-reviewer-to-docs-maintainer.md`, `.read_component`, `.read_single_bike`, `.read_single_component_type`, `.write_component_distance`, `.read_all_component_types`, `.read_all_components_objects`, `.read_all_workplans`, `.read_collection_by_component`, `.read_date_oldest_ride`, `.read_matching_rides`, `.read_recent_rides`, `.read_subset_component_history`, `.read_subset_components`, `.read_unique_bikes`, `.read_bike_id_recent_component_history`, `.write_collection`, `.write_incident_record`, `.read_incidents_by_workplan`?**
  _High betweenness centrality (0.206) - this node is a cross-community bridge._
- **Why does `BusinessLogic` connect `BusinessLogic` to `.create_workplan`, `scheduler.py`, `.create_component`, `get_service_incident_options`, `.get_bike_details`, `.process_service_records`, `get_workplan_data_tuple`, `.recalculate_component_after_service_removal`, `generate_unique_id`, `.update_components_distance_iterator`, `validate_date_format`, `Code Reviewer -> Docs Maintainer Handover`?**
  _High betweenness centrality (0.123) - this node is a cross-community bridge._
- **Why does `Issues found (none blocking)` connect `get_workplan_data_tuple` to `.read_component`, `get`, `.get_bike_details`, `2026-09-25-service-integration-test-findings.md`?**
  _High betweenness centrality (0.055) - this node is a cross-community bridge._
- **Are the 9 inferred relationships involving `DatabaseManager` (e.g. with `Bikes` and `Collections`) actually correct?**
  _`DatabaseManager` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `BusinessLogic` (e.g. with `strava_sync_job()` and `update_time_based_fields_job()`) actually correct?**
  _`BusinessLogic` has 2 INFERRED edges - model-reasoned connections that need verification._