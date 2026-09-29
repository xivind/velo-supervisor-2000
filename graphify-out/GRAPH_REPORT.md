# Graph Report - velo-supervisor-2000  (2026-09-30)

## Corpus Check
- 48 files · ~148,218 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1062 nodes · 1769 edges · 148 communities (85 shown, 63 thin omitted)
- Extraction: 84% EXTRACTED · 16% INFERRED · 0% AMBIGUOUS · INFERRED: 277 edges (avg confidence: 0.91)
- Token cost: 184,062 input · 0 output

## Community Hubs (Navigation)
- POST Route Handlers
- Backend Module Wiring
- GET Page Routes
- Service and Workplan Tests
- Database Models and Schema
- Component and Collection JS
- Page Payload Builders
- Post-release Fixes Handovers
- DatabaseManager Core Reads
- Service Record Queries
- Detail Page Templates
- Distance and Service Status
- Workplan and Incident Tuples
- Service Creation and Validation
- Collection Management
- Strava API Client
- Service Integration Design Decisions
- Component and History Creation
- Config and Utility Helpers
- Table Creation Migrations
- Docker Health Check
- Health Check Implementation Notes
- Date Picker and Modal Fixes
- Service Integration Spec
- Migration Tests
- Incident Options and Titles
- Date and Record Validation
- Single Record Reads and Deletes
- Test Fixtures
- Health Check Tests
- Error Recorder and Log Levels
- Database Connection Check
- Workplan Titles and Service Entries
- Incident Form and Resolve Warning
- Base Layout Templates
- Component Modification and Deletion
- Services Integration Migration
- CLAUDE.md Agent Team
- Git and Versioning Workflow
- Component Types Migration
- Workplans to Planned Services Migration
- Change Management and Tech Debt
- Code Reviewer Directive
- Form Date Validation
- Incident Table Sorting and Search
- Handover Template
- Database Check Review
- Help Page
- Database Expert Directive
- UX Designer Directive
- v0.5.0 Release Notes
- Service Integration Handover
- Services Test Protocol
- Strava Ride Sync
- Component Reads and Writes
- Incident Link Migration
- Migration Entry Point
- Effective Planned Date
- Handover Conventions
- Fullstack Developer Directive
- Product Manager Directive
- Incident Modal Linked Services
- Form Field Validation
- Handovers Directory Guide
- Version Script
- Architect Directive
- Architecture Overview
- Development Commands
- Development Notes
- Workplans Page Payload
- Bike Reads and Writes
- Component Type Reads and Writes
- History Notes Migration
- Component Type Time Fields Migration
- Component Time Fields Migration
- Service Workplan Link Migration
- Workplan Name Migration
- Log Viewer
- Config Update and Shutdown
- Docs Maintainer Directive
- Code Style Standards
- Development Workflow
- Bulk Status Change Modal
- Markdown Preview
- Workplan Table Filtering
- Service Integration Review
- Component Distance Writes
- Testing Requirements
- Read All Collections
- Read All Component Types
- Read All Components
- Read All Workplans
- Collection by Component
- Oldest Ride Date
- Latest History Record
- Matching Rides
- Oldest History Record
- Recent Rides
- Component History Subset
- Components Subset
- Service Record Subset
- Unique Bikes
- Bike Service Status Write
- Collection Write
- Incident Record Write
- Bulk Ride Write
- Database Backup Script
- Container Build Script
- Strava OAuth Setup
- Branching and Versioning
- Changelog and Project Board
- Error Page Illustration
- App Logo
- Collections Concept
- Component Types Concept
- Hybrid Time and Distance
- Mileage Tracking
- Thresholds Concept
- Getting Started Guide
- Component Types Help
- Config Page Help
- Incidents Help
- Workplans Help
- Data Management Tips
- Troubleshooting Help
- Confirm Modal
- Loading Modal
- Report Modal
- Validation Modal
- Project Metadata
- Graphify Auto-update
- Manual Onboarding
- Piloting Program
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
- v0.4.9 Release

## God Nodes (most connected - your core abstractions)
1. `DatabaseManager` - 71 edges
2. `BusinessLogic` - 65 edges
3. `run_all_migrations()` - 24 edges
4. `seed_component()` - 24 edges
5. `seed_rides()` - 20 edges
6. `Bike Details Template` - 19 edges
7. `Component Details Template` - 18 edges
8. `get_workplan_data_tuple()` - 17 edges
9. `What was checked and held up` - 15 edges
10. `Base Template` - 15 edges

## Surprising Connections (you probably didn't know these)
- `Context` --references--> `get_service_incident_options()`  [INFERRED]
  .handovers/documentation/post-release-fixes-docs-maintainer-to-human.md → backend/utils.py
- `Convention check` --references--> `generate_incident_title()`  [INFERRED]
  .handovers/review/post-release-fixes-reviewer-to-docs-maintainer.md → backend/utils.py
- `Deliverables (files reviewed)` --references--> `get_service_incident_options()`  [INFERRED]
  .handovers/review/post-release-fixes-reviewer-to-docs-maintainer.md → backend/utils.py
- `Findings` --references--> `get_service_incident_options()`  [INFERRED]
  .handovers/review/post-release-fixes-reviewer-to-docs-maintainer.md → backend/utils.py
- `Deliverables` --references--> `ErrorRecorder`  [INFERRED]
  .handovers/fullstack/health-check-fullstack-to-reviewer.md → backend/utils.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Health check mechanism (#103)** — backend_utils_errorrecorder, backend_utils_get_health_status, backend_database_manager_databasemanager_check_database_connection, backend_main_health, backend_healthcheck, handovers_fullstack_health_check_fullstack_to_reviewer_health_check_feature [EXTRACTED 1.00]
- **Planned services invisible to health** — docs_superpowers_specs_2026_09_18_service_integration_design_planned_invisible_to_health, backend_database_manager_databasemanager_read_latest_service_record, backend_business_logic_businesslogic_process_service_records, backend_business_logic_businesslogic_update_component_service_status, backend_database_model_services [EXTRACTED 1.00]
- **Service integration spec, implementation, test and review cycle** — docs_superpowers_specs_2026_09_18_service_integration_design, handovers_fullstack_service_integration_fullstack_to_reviewer, docs_superpowers_plans_2026_09_25_service_integration_test_findings, tests_test_protocol_services, handovers_review_service_integration_reviewer_to_docs_maintainer [EXTRACTED 1.00]
- **Plan and Complete Services Workflow** — frontend_templates_modal_plan_services_planservicesmodal, frontend_templates_modal_complete_services_completeservicesmodal, backend_main_add_planned_services, backend_main_complete_services, frontend_templates_modal_service_record_servicerecordmodal, frontend_templates_help_common_tasks_planning_service [INFERRED 0.85]
- **Incident to Workplan to Completed Services Flow** — frontend_templates_modal_incident_record_incidentrecordmodal, frontend_templates_modal_workplan_record_workplanrecordmodal, frontend_templates_modal_plan_services_planservicesmodal, frontend_templates_modal_complete_services_completeservicesmodal, frontend_templates_modal_complete_workplan_template, frontend_templates_help_common_tasks_incident_to_finished_work [INFERRED 0.85]
- **Installation Status Change Forms** — frontend_templates_modal_install_component_installcomponentmodal, frontend_templates_modal_update_component_status_editcomponentstatusmodal, frontend_templates_modal_edit_installation_record_edithistorymodal, frontend_templates_modal_quick_swap_quickswapmodal, backend_main_add_history_record [INFERRED 0.85]

## Communities (148 total, 63 thin omitted)

### Community 0 - "POST Route Handlers"
Cohesion: 0.07
Nodes (41): asyncio, add_collection(), add_incident_record(), add_planned_services(), add_service(), add_workplan(), change_collection_status(), complete_services() (+33 more)

### Community 1 - "Backend Module Wiring"
Cohesion: 0.07
Nodes (29): apscheduler_schedulers_asyncio, apscheduler_triggers_cron, apscheduler_triggers_interval, Module to handle business logic, Middleware, Request, Class to handle exceptions that breaks the program and should be shown to the…, Method to dispatch intercepted requests (+21 more)

### Community 2 - "GET Page Routes"
Cohesion: 0.08
Nodes (35): add_history_record(), bike_details(), collection_details(), component_details(), component_overview(), component_types_overview(), config_overview(), http_exception_handler() (+27 more)

### Community 3 - "Service and Workplan Tests"
Cohesion: 0.15
Nodes (31): add_twin_component(), Planned services must be invisible to health computation, Rides before and after the service dates used below, so distances are not zero, Second installed component on bike-1 with the same settings as comp-1, Create one bike and one installed component with an installation record, seed_component(), seed_rides(), snapshot_health() (+23 more)

### Community 4 - "Database Models and Schema"
Cohesion: 0.11
Nodes (28): Module for interaction with a Sqlite database, BaseModel, Bikes, Collections, ComponentHistory, Components, ComponentTypes, Incidents (+20 more)

### Community 5 - "Component and Collection JS"
Cohesion: 0.08
Nodes (13): editCollection(), filterNewComponentsByType(), handleOldComponentChange(), handleUpdate(), initializeCollectionsSearch(), updateRowVisibility(), initializeComponentSelector(), performQuickSwap() (+5 more)

### Community 6 - "Page Payload Builders"
Cohesion: 0.11
Nodes (15): Method to produce payload for page component overview, Method to produce payload for page component details, Method to determine which factor triggered a warning status, Calculate lifetime and service triggers for a component, Method to produce payload for page bike overview, Method to create component-to-collection mapping dictionaries, Method to produce payload for displaying table of all collections, Method to build dictionaries of bike and component ids referenced in received… (+7 more)

### Community 7 - "Post-release Fixes Handovers"
Cohesion: 0.08
Nodes (23): v0.5.0.ca636f8, Context, Docs changes, docs-maintainer -> Human Handover, Double-check, Files to commit, Option A: one commit, Option B: three commits (main.js needs `git add -p`) (+15 more)

### Community 8 - "DatabaseManager Core Reads"
Cohesion: 0.08
Nodes (13): DatabaseManager, Method to sum distance for a given set of rides, Method to count how many components that references a given component type, Class to interact with a SQLite database through Peewee, Method to read installed components for a specific bike, Method to read all incident records, Method to read incidents that have at least one service in a given workplan, Method to read workplans reached through the services of a given incident (+5 more)

### Community 9 - "Service Record Queries"
Cohesion: 0.08
Nodes (13): Method to read completed services for a component, used by health computation, Method to retrieve the most recent completed service of a given component, Method to retrieve the oldest completed service of a given component, Method to read incident records with status 'Open, Method to read workplans with status 'Planned, Method to read all services linked to a specific workplan, planned first, Method to read planned services linked to a specific workplan, Method to read all services linked to a specific incident, planned first (+5 more)

### Community 10 - "Detail Page Templates"
Cohesion: 0.24
Nodes (24): Bike Details Template, Collection Details Template, Page Warning Cards Pattern, Component Details Template, Component Overview Template, From Incident to Finished Work (Help), Planning Service Before You Do It (Help), Quick Swap Components (+16 more)

### Community 11 - "Distance and Service Status"
Cohesion: 0.15
Nodes (13): Method to update component lifetime and service status when no installation…, Method to update status for a given bike based on component service and…, Method to calculate distance and bike id for history records, Method to calculate distance and bike id for service records, Method to compute component status using threshold logic, Method to determine worst-case status between distance and days-based…, Method to update time-based status fields for all non-retired components, Method to update component table with distance from ride table (+5 more)

### Community 12 - "Workplan and Incident Tuples"
Cohesion: 0.17
Nodes (20): Method to produce payload for page incident reports, Method to produce payload for workplan details page, calculate_elapsed_days(), derive_workplan_context(), get_formatted_datetime_now(), get_incident_data_tuple(), get_workplan_data_tuple(), get_workplan_names_dict() (+12 more)

### Community 13 - "Service Creation and Validation"
Cohesion: 0.15
Nodes (12): Method to add service record, planned or completed, Method to add a planned service, which has no service date, bike or distance…, Method to build the report used by the plan services and complete services…, Method to create planned services for one or more components with the same…, Method to complete planned services with one service date, keeping their…, Method to update a service record, including status changes in both directions, Method to recalculate a component after a completed service is deleted or…, Method to validate service records before processing and storing in database (+4 more)

### Community 14 - "Collection Management"
Cohesion: 0.13
Nodes (10): BusinessLogic, Method to create collection, Method to update collection, Method to validate collections before allowing bulk operations, Method to change status of all components in a collection, Method to refresh all bikes from Strava, Class that contains business logic, Calculate status flags for a collection based on its components. (+2 more)

### Community 15 - "Strava API Client"
Cohesion: 0.18
Nodes (9): Class to interact with Strava API, Method to authenticate and get data from Stravas gear API, Method to prepare a list of rides, Method to prepare a list of bikes, Method to read oauth options from file, Method to save oauth options to file, Method to authenticate and get data from Stravas activities API, Method to authenticate and get the full list of bike ids from the athlete's… (+1 more)

### Community 16 - "Service Integration Design Decisions"
Cohesion: 0.17
Nodes (13): Blank values always NULL, never empty strings, Migration steps 12-16 (idempotent check_/migrate_ pairs), Planned services invisible to component health, Planned vs Completed service status, Retired components locked (no service status changes), validate_service_record modes (plan/complete/edit/revert), Production DB regression comparison (master vs branch), Retirement blocked while planned services exist (+5 more)

### Community 17 - "Component and History Creation"
Cohesion: 0.15
Nodes (10): Method to create component, Method to create installation history record, Method to orchestrate swap of one component with another, Method to validate quick swap operation, Method to check if a bike has all mandatory components and respects max…, Method to add incident record, insert_planned_service_for_migration(), Insert a planned service with no date, bike or distance. Returns False if the… (+2 more)

### Community 18 - "Config and Utility Helpers"
Cohesion: 0.14
Nodes (15): calculate_percentage_reached(), get_current_version(), parse_button_sorting(), Function to update configuration file based on which form was submitted, Function to get current program version, Module for auxiliary functions, Function to read configuration file, Function to calculate remaining service interval or remaining lifetime as… (+7 more)

### Community 19 - "Table Creation Migrations"
Cohesion: 0.14
Nodes (14): create_collections_table(), create_incidents_table(), create_workplans_table(), populate_component_types_thresholds(), populate_components_thresholds(), Creates the incidents table if it doesn't exist., Creates the workplans table if it doesn't exist., Creates the collections table if it doesn't exist. (+6 more)

### Community 20 - "Docker Health Check"
Cohesion: 0.19
Nodes (12): Health check run by the Docker daemon, exit code 0 means healthy and 1 means…, health(), Endpoint for the Docker health check, returns 503 if errors were logged the…, get_health_status(), Function to assess application health from errors logged the last 24 hours and…, Docker HEALTHCHECK against /health, Health check for Docker daemon (#103), Separate healthcheck.py instead of curl (+4 more)

### Community 21 - "Health Check Implementation Notes"
Cohesion: 0.17
Nodes (12): lifespan(), Manage application startup and shutdown, Method to store error records and ignore lower levels. Filters here instead of…, FastAPI, Blockers / Open Questions, Context, Decisions Made, Deliverables (+4 more)

### Community 22 - "Date Picker and Modal Fixes"
Cohesion: 0.18
Nodes (12): A. Questions to answer from the code, no change expected, B3: service modal submittable without completion date, B. Bugs to fix, C. Interface changes the user asked for, Extra wording fixes asked for on 2026-09-26, Re-test list for the second round, Service integration (#351): findings from the manual test walkthrough, Status (2026-09-26) (+4 more)

### Community 23 - "Service Integration Spec"
Cohesion: 0.15
Nodes (13): Backend, Data model, Error handling, Goal, main.js, main.py, Migration, Modals (+5 more)

### Community 24 - "Migration Tests"
Cohesion: 0.28
Nodes (12): sqlite3, columns(), create_old_schema(), Migration converts the old workplan/incident model to services, Seed workplans, incidents and services in the pre-#351 shape, Recreate services, workplans, incidents and component_history as they were…, run_migration(), seed_old_data() (+4 more)

### Community 25 - "Incident Options and Titles"
Cohesion: 0.20
Nodes (11): Method to add workplan, optionally with planned services for components of a…, generate_incident_title(), get_service_incident_options(), parse_json_string(), Build incident options for the service modal (4 fields), all incidents so…, Function to load a JSON string and return the parsed data as a python object, Generate a concise title for an incident, D4: choose components when creating workplan from incident (+3 more)

### Community 26 - "Date and Record Validation"
Cohesion: 0.17
Nodes (7): Method to update a component history record with validation, Method to validate history records before processing and storing in database, Method to update incident record (supports full or partial updates), Method to update workplan (supports full or partial updates), Method to validate that a workplan can be set to Done, Function to validate that a date string matches the required format YYYY-MM-DD…, validate_date_format()

### Community 27 - "Single Record Reads and Deletes"
Cohesion: 0.17
Nodes (6): Method to delete a given record and associated records, Method to retrieve record for a specific entry in the installation log, Method to retrieve a specific service record, Method to retrieve record for a specific collection, Method to retrieve record for a specific incident report, Method to retrieve record for a specific workplan

### Community 28 - "Test Fixtures"
Cohesion: 0.20
Nodes (11): fixture, os, pytest, shutil, app_env(), migrated_env(), modules(), Shared fixtures: every test gets its own copy of the template database (+3 more)

### Community 29 - "Health Check Tests"
Cohesion: 0.23
Nodes (9): Verification done, Health check: errors logged the last 24 hours or a failing database make the…, lifespan in main.py sets every root handler to INFO or DEBUG at startup, SQLite creates an empty file for a wrong path, e.g. a missing Docker mount, recording_logger(), test_missing_database_file_makes_app_unhealthy(), test_recorder_includes_exception_in_message(), test_recorder_keeps_errors_and_ignores_lower_levels() (+1 more)

### Community 30 - "Error Recorder and Log Levels"
Cohesion: 0.24
Nodes (8): ErrorRecorder, Logging handler that keeps the most recent error records in memory for the…, Method to get error records newer than the given number of hours, Log levels drive container health, Level filtering inside ErrorRecorder.emit(), In-memory 24h error record, ERROR vs WARNING log level rule, ErrorRecorder thread safety under Handler.lock

### Community 31 - "Database Connection Check"
Cohesion: 0.20
Nodes (9): Method to check the database connection for the health check, Code Reviewer -> Docs Maintainer Handover, Context, Deliverables, Issues Found, Next Steps for Docs Maintainer, References, Resolution (2026-09-27, after review) (+1 more)

### Community 32 - "Workplan Titles and Service Entries"
Cohesion: 0.22
Nodes (10): build_incident_service_entry(), generate_workplan_title(), Return the name the user gave the workplan, or a generated title when there is…, Describe one service linked to an incident, for the read only list in the…, Generate a concise title for a workplan, Strip markdown syntax from text to produce clean plain text, resolve_workplan_title(), strip_markdown_syntax() (+2 more)

### Community 33 - "Incident Form and Resolve Warning"
Cohesion: 0.20
Nodes (10): D. Design questions to decide before coding, Decisions (2026-09-26), Follow-up tweaks asked for on 2026-09-26, Warn (not block) when resolving incident with planned services, Second round of tweaks, 2026-09-26, Third round of tweaks, 2026-09-26, Warning when resolving an incident with open services, 2026-09-26, initializeIncidentForm() (+2 more)

### Community 34 - "Base Layout Templates"
Cohesion: 0.24
Nodes (10): Base Template, Component Types Template, Config Template, Error Page Template, Footer Template, Bike Overview Template, nav_menu Macro, Navigation Menu Template (+2 more)

### Community 35 - "Component Modification and Deletion"
Cohesion: 0.25
Nodes (4): Method to update component details, Validate threshold configuration rules for component intervals, Method to create or update component types, Method to update only the count of components for a given component type

### Community 36 - "Services Integration Migration"
Cohesion: 0.22
Nodes (9): check_incidents_workplan_column(), check_services_integration_columns(), migrate_incidents_workplan_link(), migrate_services_integration_columns(), Check if Incidents table needs workplan_id column, Add workplan_id column to Incidents table for workplan hub integration, Check which service integration columns are missing on the services table, Add status, incident_id and planned_date to services, mark existing rows… (+1 more)

### Community 37 - "CLAUDE.md Agent Team"
Cohesion: 0.22
Nodes (8): Available Agents, Communication & Output Rules, Debugging & Bug Fixing Rules, Direct Invocation, graphify, Important Notes, Project Overview, Sub-Agent Team

### Community 38 - "Git and Versioning Workflow"
Cohesion: 0.25
Nodes (8): Version Script CI Workflow, Branch Strategy, Commit Process, For All Agents, For code-reviewer, For docs-maintainer, For fullstack-developer, Git Workflow Rules

### Community 39 - "Component Types Migration"
Cohesion: 0.32
Nodes (7): check_component_types_columns(), count_component_types_in_use(), migrate_component_types(), Count how many components use a specific component type, Check if the component_types table needs migration, Migrate the component_types table to add new columns, Script to migrate the database, including adding new tables and fields

### Community 40 - "Workplans to Planned Services Migration"
Cohesion: 0.25
Nodes (8): check_workplans_affected_columns(), migrate_drop_workplan_affected_columns(), migrate_workplans_to_planned_services(), Check if workplans table still has the affected bike/component columns, Resolve bike and component names, marking components that no longer exist, Convert affected components on planned workplans into planned services,…, Rebuild workplans table without the affected bike/component columns, read_names_for_migration()

### Community 41 - "Change Management and Tech Debt"
Cohesion: 0.25
Nodes (7): Change Management Rules, Debugging & bug fixing rules (root cause first), graphify knowledge graph usage rules, Agent handover documents (.handovers/), Technical debt tracked in issue #356, TomSelect multi-select pattern, Stale ID 500 marks container unhealthy 24h (known limitation)

### Community 42 - "Code Reviewer Directive"
Cohesion: 0.25
Nodes (7): Issues Found, Key Checks, Output Format, Recommendations, Review Philosophy, Review Process, Summary

### Community 43 - "Form Date Validation"
Cohesion: 0.25
Nodes (8): Validation, initializeWorkplanForm(), submitCollectionAjax(), submitComponentAjax(), validateCollectionStatusChange(), validateDateInput(), validateWorkplanForm(), Update Collection Status Modal

### Community 44 - "Incident Table Sorting and Search"
Cohesion: 0.29
Nodes (8): initializeCollectionsSorting(), sortColumn(), initializeIncidentTable(), setupIncidentSearch(), setupIncidentStatusFiltering(), setupIncidentTableSorting(), setupWorkplanTableSorting(), updateIncidentVisibility()

### Community 45 - "Handover Template"
Cohesion: 0.25
Nodes (7): Blockers / Open Questions, Context, Decisions Made, Deliverables, Next Steps for [Target Agent], References, [Source Agent] -> [Target Agent] Handover

### Community 46 - "Database Check Review"
Cohesion: 0.38
Nodes (5): Method to check that the database can be read. Reads a real table, since SELECT…, Database check reads bikes table, not SELECT 1, Rename read_database_connection to check_database_connection, ErrorRecorder deque bounded to maxlen=20, Catching peewee.DatabaseError for corrupt file

### Community 47 - "Help Page"
Cohesion: 0.33
Nodes (7): help_page(), Endpoint for help page, helpTopics Data Object, Help Page Template, Help Search Functionality, showHelpTopic() Function, Documentation Modal

### Community 48 - "Database Expert Directive"
Cohesion: 0.29
Nodes (6): Constraints, Core Responsibilities, Pattern Consistency - CRITICAL, Query Optimization, Schema Changes, Workflow

### Community 49 - "UX Designer Directive"
Cohesion: 0.29
Nodes (6): Core Responsibilities, Design Principles, Specifications to Include, v1 (Before Architect), v2 (After Architect), Workflow

### Community 50 - "v0.5.0 Release Notes"
Cohesion: 0.38
Nodes (6): D1: optional user-entered workplan name, FastAPI/Starlette TemplateResponse argument order fix, Workplan link silently lost bug (process_service_records without workplan_id), Optional workplan_name (migration step 17), db_migration step 16 rebuild before step 17 workplan_name, v0.5.0 release (service integration, health check, uv)

### Community 51 - "Service Integration Handover"
Cohesion: 0.29
Nodes (7): Bugs found and fixed, Known limitations, Next steps, Regression evidence, 2026-09-26, Service integration (#351) - fullstack to code-reviewer, Testing, What was built

### Community 52 - "Services Test Protocol"
Cohesion: 0.29
Nodes (7): 2026-09-25, first walkthrough, human, 2026-09-26, regression against the baseline database, Claude, 2026-09-27, second walkthrough, human, Preparation, Results, Scope, Test Protocol: Planned services, workplans and incidents

### Community 53 - "Strava Ride Sync"
Cohesion: 0.33
Nodes (3): Function to set the date for last pull from Strava, Method to create or update ride data in bulk to database, Method to determine which selection of components to update

### Community 54 - "Component Reads and Writes"
Cohesion: 0.33
Nodes (3): Method to get component names based on list of ids, Method to retrieve record for a specific component, Method to create or update component data to the database

### Community 55 - "Incident Link Migration"
Cohesion: 0.33
Nodes (6): check_incidents_workplan_column_present(), migrate_drop_incident_workplan_column(), migrate_incident_links_to_services(), Check if incidents table still has the workplan_id column, Rebuild incident to workplan links through services, Rebuild incidents table without the workplan_id column

### Community 56 - "Migration Entry Point"
Cohesion: 0.33
Nodes (6): find_database_file(), migrate_database(), prompt_for_db_path(), Search for a database file in the user's home directory and subdirectories, Prompt user for database path or filename and verify it exists, Main function to handle the database migration.

### Community 57 - "Effective Planned Date"
Cohesion: 0.33
Nodes (6): get_effective_planned_date(), get_planned_service_data_tuple(), Return the service's own planned date, else the workplan due date, else None, Build standard planned service tuple for display (11 fields), Effective planned date fallback, Key decisions

### Community 58 - "Handover Conventions"
Cohesion: 0.33
Nodes (6): Agent Communication via Handovers, Creating Handovers, Detailed Instructions, Handover Structure, Naming Convention, Reading Handovers

### Community 59 - "Fullstack Developer Directive"
Cohesion: 0.33
Nodes (5): Backend Patterns, Core Responsibilities, Frontend Patterns, Handover Content, Workflow

### Community 60 - "Product Manager Directive"
Cohesion: 0.33
Nodes (5): Boundaries, Core Responsibilities, Key Principle: You Are Interactive, Requirements Document, User Story Format

### Community 61 - "Incident Modal Linked Services"
Cohesion: 0.33
Nodes (5): A5: workplan delete blocked while services linked, D2: incident modal lists linked services, Manual walkthrough findings (A/B/C/D groups), renderIncidentServices(), Unescaped innerHTML in renderIncidentServices

### Community 62 - "Form Field Validation"
Cohesion: 0.33
Nodes (6): addFormValidation(), clearValidationErrors(), showFieldError(), showValidationModal(), validateComponentThresholds(), validateQuickSwapForm()

### Community 63 - "Handovers Directory Guide"
Cohesion: 0.33
Nodes (5): Creating Handovers, Directory Structure, Finding Handovers, Handovers Directory, Rules

### Community 64 - "Version Script"
Cohesion: 0.40
Nodes (4): get_git_info(), Script to maintain version number, Function to get latest version number and commit hash, subprocess

### Community 65 - "Architect Directive"
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

### Community 69 - "Workplans Page Payload"
Cohesion: 0.50
Nodes (3): Method to produce payload for page of all workplans, get_formatted_bikes_list(), Function to get list of all bikes, with prefix for retired bikes

### Community 72 - "History Notes Migration"
Cohesion: 0.50
Nodes (4): check_component_history_notes_column(), migrate_component_history_notes(), Check if component_history table needs notes column, Add notes column to component_history table

### Community 73 - "Component Type Time Fields Migration"
Cohesion: 0.50
Nodes (4): check_component_types_time_columns(), migrate_component_types_time_fields(), Check if ComponentTypes table needs time-based fields migration, Add time-based fields to ComponentTypes table

### Community 74 - "Component Time Fields Migration"
Cohesion: 0.50
Nodes (4): check_components_time_columns(), migrate_components_time_fields(), Check if Components table needs time-based fields migration, Add time-based fields to Components table and populate threshold_km

### Community 75 - "Service Workplan Link Migration"
Cohesion: 0.50
Nodes (4): check_services_workplan_column(), migrate_services_workplan_link(), Check if Services table needs workplan_id column, Add workplan_id column to Services table for workplan hub integration

### Community 76 - "Workplan Name Migration"
Cohesion: 0.50
Nodes (4): check_workplans_name_column(), migrate_workplans_name_column(), Check if workplans table needs the workplan_name column, Add the optional user given name to the workplans table, existing workplans…

### Community 77 - "Log Viewer"
Cohesion: 0.50
Nodes (4): get_filtered_log(), Endpoint to read log and return only business events, Function to get filtered log records, read_filtered_logs()

### Community 78 - "Config Update and Shutdown"
Cohesion: 0.50
Nodes (4): Endpoint to update config file based on which form was submitted, update_config(), Helper function to shutdown the server after a short delay, shutdown_server()

### Community 79 - "Docs Maintainer Directive"
Cohesion: 0.50
Nodes (3): Core Responsibilities, Documentation Rules, Workflow

### Community 80 - "Code Style Standards"
Cohesion: 0.50
Nodes (4): Code Style & Standards, Database, Frontend, Python (Backend)

### Community 81 - "Development Workflow"
Cohesion: 0.50
Nodes (4): For Bug Fixes, For Documentation Updates, For New Features, Standard Development Workflow

### Community 82 - "Bulk Status Change Modal"
Cohesion: 0.50
Nodes (4): cleanup(), handleCancel(), handleConfirm(), performBulkStatusChange()

### Community 83 - "Markdown Preview"
Cohesion: 0.50
Nodes (4): containsMarkdown(), renderPreview(), setInitialMode(), updateCheckboxInText()

### Community 84 - "Workplan Table Filtering"
Cohesion: 0.67
Nodes (4): initializeWorkplanTable(), setupWorkplanSearch(), setupWorkplanStatusFiltering(), updateWorkplansVisibility()

### Community 85 - "Service Integration Review"
Cohesion: 0.50
Nodes (4): Code review -> docs-maintainer Handover, Context, Recommendations, References

### Community 87 - "Testing Requirements"
Cohesion: 0.67
Nodes (3): Before Creating Handover, For fullstack-developer, Testing Requirements

## Ambiguous Edges - Review These
- `Version Script CI Workflow` → `Git Workflow Rules`  [AMBIGUOUS]
  .github/workflows/run_version_script.yml · relation: conceptually_related_to
- `conftest.py` → `Manual testing protocols approach`  [AMBIGUOUS]
  tests/README.md · relation: conceptually_related_to

## Knowledge Gaps
- **184 isolated node(s):** `Collections (Core Concept)`, `Component Types vs Components`, `Hybrid Time + Distance Tracking`, `Mileage Tracking`, `Understanding Thresholds` (+179 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 513 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **63 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `Version Script CI Workflow` and `Git Workflow Rules`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `conftest.py` and `Manual testing protocols approach`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **Why does `DatabaseManager` connect `DatabaseManager Core Reads` to `Database Models and Schema`, `Page Payload Builders`, `Service Record Queries`, `Single Record Reads and Deletes`, `Database Check Review`, `Component Reads and Writes`, `Bike Reads and Writes`, `Component Type Reads and Writes`, `Component Distance Writes`, `Read All Collections`, `Read All Component Types`, `Read All Components`, `Read All Workplans`, `Collection by Component`, `Oldest Ride Date`, `Latest History Record`, `Matching Rides`, `Oldest History Record`, `Recent Rides`, `Component History Subset`, `Components Subset`, `Service Record Subset`, `Unique Bikes`, `Bike Service Status Write`, `Collection Write`, `Incident Record Write`, `Bulk Ride Write`?**
  _High betweenness centrality (0.199) - this node is a cross-community bridge._
- **Why does `BusinessLogic` connect `Collection Management` to `Backend Module Wiring`, `Component Modification and Deletion`, `Workplans Page Payload`, `Page Payload Builders`, `Distance and Service Status`, `Workplan and Incident Tuples`, `Service Creation and Validation`, `Component and History Creation`, `Strava Ride Sync`, `Incident Options and Titles`, `Date and Record Validation`, `Database Connection Check`?**
  _High betweenness centrality (0.108) - this node is a cross-community bridge._
- **Why does `Issues found (none blocking)` connect `Workplan and Incident Tuples` to `GET Page Routes`, `Page Payload Builders`, `Service Integration Review`, `Component Reads and Writes`, `Incident Modal Linked Services`?**
  _High betweenness centrality (0.054) - this node is a cross-community bridge._
- **Are the 9 inferred relationships involving `DatabaseManager` (e.g. with `Bikes` and `Collections`) actually correct?**
  _`DatabaseManager` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `BusinessLogic` (e.g. with `strava_sync_job()` and `update_time_based_fields_job()`) actually correct?**
  _`BusinessLogic` has 2 INFERRED edges - model-reasoned connections that need verification._