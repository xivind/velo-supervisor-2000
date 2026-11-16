# Graph Report - velo-supervisor-2000  (2026-11-16)

## Corpus Check
- 60 files · ~164,991 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 12 file(s) not represented in the graph (top: (none) 5, .example 1, .sqlite 1)

## Summary
- 1302 nodes · 2248 edges · 144 communities (92 shown, 52 thin omitted)
- Extraction: 82% EXTRACTED · 18% INFERRED · 0% AMBIGUOUS · INFERRED: 396 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `1358dcf4`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- main.py
- scheduler.py
- get
- seed_component
- database_model.py
- main.js
- validateDateInput
- Version Bump Workflow
- DatabaseManager
- Service Record Queries
- Bike Details Template
- BusinessLogic
- utils.py
- Tests
- Result extractor
- Strava API Integration
- 2026-09-18-service-integration-design.md
- db_migration.py
- .create_history_record
- run_all_migrations
- Fullstack Developer -> Code Reviewer Handover
- tests/conftest.py
- 2026-09-25-service-integration-test-findings.md
- Service integration: incidents, workplans and services
- Migration Tests
- derived.py
- test_loader.py
- .write_delete_record
- Rewrite roadmap: new UI, restructured backend, exposed API
- Code Reviewer -> Docs Maintainer Handover
- loader.py
- get_service_incident_options
- Code review -> docs-maintainer Handover
- test_health.py
- Workplans
- Decided
- check_services_integration_columns
- CLAUDE.md
- extract
- .validate_workplan_completion
- migrate_workplans_to_planned_services
- Git Workflow Rules
- Code Reviewer Agent
- CLAUDE.md
- Development Commands
- Handover Template
- initializeWorkplanTable
- Middleware
- Database Expert Agent
- UX Designer Agent
- Health check for Docker daemon (#103)
- health-check-reviewer-to-docs-maintainer.md
- Help Page Template
- ErrorRecorder
- Component Record Access
- migrate_incident_links_to_services
- diff
- update_config
- Handover Communication
- Fullstack Developer Agent
- Product Manager Agent
- Code Style & Standards
- Standard Development Workflow
- Handovers Directory Guide
- Stage 1 Foundation Handover
- Architect Agent
- Architecture Overview
- Testing Requirements
- Development Notes
- version.py
- .read_bike_name
- write_config
- History Notes Migration
- .read_all_components_objects
- service-integration-fullstack-to-reviewer.md
- Services Workplan Link Migration
- Workplan Name Migration
- Log Filtering
- stored_state
- Docs Maintainer Agent
- .read_all_workplans
- Results
- .read_bike_id_recent_component_history
- .read_date_oldest_ride
- Service integration (#351) - fullstack to code-reviewer
- fixture
- validateComponentThresholds
- .read_matching_rides
- .read_sum_distance_subset_rides
- .read_workplans_by_incident
- clock.py
- Path
- migrate_component_types_time_fields
- D. Design questions to decide before coding
- migrate_components_time_fields
- cleanup
- Component History Query
- renderPreview
- initializeIncidentTable
- GitHub Issues Tracker
- handleOldComponentChange
- Container Deploy Script
- Strava OAuth Setup
- Branching and Versioning
- Changelog and Project Board
- Error Page Illustration
- Project Logo
- Collections Concept
- Component Types Concept
- Time and Distance Tracking
- Mileage Tracking
- Understanding Thresholds
- Defining Component Types
- Component Types Page
- Config and Strava Sync
- Incidents Page
- Workplans Page
- Data Management Tips
- Help and Troubleshooting
- Confirm Action Modal
- Loading Modal
- Report Modal
- Validation Error Modal
- Project Root
- Graphify Auto-Update Mechanism
- Manual Onboarding Setup
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
- v0.4.9 Current Release
- compare.py

## God Nodes (most connected - your core abstractions)
1. `DatabaseManager` - 71 edges
2. `BusinessLogic` - 65 edges
3. `run_all_migrations()` - 25 edges
4. `seed_component()` - 24 edges
5. `Tests` - 21 edges
6. `seed_rides()` - 20 edges
7. `Bike Details Template` - 19 edges
8. `get_workplan_data_tuple()` - 18 edges
9. `derived_values()` - 18 edges
10. `Component Details Template` - 18 edges

## Surprising Connections (you probably didn't know these)
- `Decisions Made` --references--> `extract()`  [INFERRED]
  .handovers/stages/stage-1-foundation-handover.md → scripts/integrity/extract.py
- `Deliverables` --references--> `ErrorRecorder`  [INFERRED]
  .handovers/fullstack/health-check-fullstack-to-reviewer.md → backend/utils.py
- `Migration` --references--> `generate_unique_id()`  [INFERRED]
  docs/superpowers/specs/2026-09-18-service-integration-design.md → backend/utils.py
- `Warning when resolving an incident with open services, 2026-09-26` --references--> `initializeIncidentForm()`  [INFERRED]
  docs/superpowers/plans/2026-09-25-service-integration-test-findings.md → frontend/static/js/main.js
- `Task 3, step 5: failing-comparison proof` --references--> `diff()`  [INFERRED]
  .handovers/stages/stage-1-foundation-handover.md → scripts/integrity/compare.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Health check mechanism (#103)** — backend_utils_errorrecorder, backend_utils_get_health_status, backend_database_manager_databasemanager_check_database_connection, backend_main_health, backend_healthcheck, handovers_fullstack_health_check_fullstack_to_reviewer_health_check_feature [EXTRACTED 1.00]
- **Planned services invisible to health** — docs_superpowers_specs_2026_09_18_service_integration_design_planned_invisible_to_health, backend_database_manager_databasemanager_read_latest_service_record, backend_business_logic_businesslogic_process_service_records, backend_business_logic_businesslogic_update_component_service_status, backend_database_model_services [EXTRACTED 1.00]
- **Service integration spec, implementation, test and review cycle** — docs_superpowers_specs_2026_09_18_service_integration_design, handovers_fullstack_service_integration_fullstack_to_reviewer, docs_superpowers_plans_2026_09_25_service_integration_test_findings, tests_test_protocol_services, handovers_review_service_integration_reviewer_to_docs_maintainer [EXTRACTED 1.00]
- **Installation Status Change Forms** — frontend_templates_modal_install_component_installcomponentmodal, frontend_templates_modal_update_component_status_editcomponentstatusmodal, frontend_templates_modal_edit_installation_record_edithistorymodal, frontend_templates_modal_quick_swap_quickswapmodal, backend_main_add_history_record [INFERRED 0.85]
- **Incident to Workplan to Completed Services Flow** — frontend_templates_modal_incident_record_incidentrecordmodal, frontend_templates_modal_workplan_record_workplanrecordmodal, frontend_templates_modal_plan_services_planservicesmodal, frontend_templates_modal_complete_services_completeservicesmodal, frontend_templates_modal_complete_workplan_template, frontend_templates_help_common_tasks_incident_to_finished_work [INFERRED 0.85]
- **Plan and Complete Services Workflow** — frontend_templates_modal_plan_services_planservicesmodal, frontend_templates_modal_complete_services_completeservicesmodal, backend_main_add_planned_services, backend_main_complete_services, frontend_templates_modal_service_record_servicerecordmodal, frontend_templates_help_common_tasks_planning_service [INFERRED 0.85]

## Communities (144 total, 52 thin omitted)

### Community 0 - "main.py"
Cohesion: 0.07
Nodes (42): add_collection(), add_history_record(), add_incident_record(), add_planned_services(), add_service(), add_workplan(), change_collection_status(), complete_services() (+34 more)

### Community 1 - "scheduler.py"
Cohesion: 0.10
Nodes (24): apscheduler_schedulers_asyncio, apscheduler_triggers_cron, apscheduler_triggers_interval, Module to handle business logic, lifespan(), Manage application startup and shutdown, Module for middleware, Initialize and start the APScheduler instance (+16 more)

### Community 2 - "get"
Cohesion: 0.07
Nodes (36): bike_details(), collection_details(), component_details(), component_overview(), component_types_overview(), config_overview(), help_page(), http_exception_handler() (+28 more)

### Community 3 - "seed_component"
Cohesion: 0.15
Nodes (32): json, add_twin_component(), Planned services must be invisible to health computation, Rides before and after the service dates used below, so distances are not zero, Second installed component on bike-1 with the same settings as comp-1, Create one bike and one installed component with an installation record, seed_component(), seed_rides() (+24 more)

### Community 4 - "database_model.py"
Cohesion: 0.06
Nodes (37): Module for interaction with a Sqlite database, BaseModel, Meta, Bikes, Meta, Collections, Meta, ComponentHistory (+29 more)

### Community 5 - "main.js"
Cohesion: 0.09
Nodes (10): editCollection(), handleUpdate(), initializeCollectionsSearch(), updateRowVisibility(), initializeComponentSelector(), performQuickSwap(), NOTE: All collection details page handlers are in the "Functions used on…, IMPORTANT: Remove readonly - allow manual typing (+2 more)

### Community 6 - "validateDateInput"
Cohesion: 0.17
Nodes (12): Warn (not block) when resolving incident with planned services, Validation, initializeIncidentForm(), initializeWorkplanForm(), submitCollectionAjax(), submitComponentAjax(), validateCollectionStatusChange(), validateDateInput() (+4 more)

### Community 7 - "Version Bump Workflow"
Cohesion: 0.11
Nodes (18): GITHUB_TOKEN, jobs, run-script, name, branches, branches, runs-on, steps (+10 more)

### Community 8 - "DatabaseManager"
Cohesion: 0.04
Nodes (25): DatabaseManager, Method to read and sort content of component_types table, Method to count how many components that references a given component type, Method to read components for a specific bike, Class to interact with a SQLite database through Peewee, Method to read installed components for a specific bike, Method to retrieve the most recent record from the installation log of a given…, Method to retrieve the oldest record from the installation log of a given… (+17 more)

### Community 9 - "Service Record Queries"
Cohesion: 0.08
Nodes (13): Method to read completed services for a component, used by health computation, Method to retrieve the most recent completed service of a given component, Method to retrieve the oldest completed service of a given component, Method to read incident records with status 'Open, Method to read workplans with status 'Planned, Method to read all services linked to a specific workplan, planned first, Method to read planned services linked to a specific workplan, Method to read all services linked to a specific incident, planned first (+5 more)

### Community 10 - "Bike Details Template"
Cohesion: 0.18
Nodes (30): Base Template, Bike Details Template, Collection Details Template, Page Warning Cards Pattern, Component Details Template, Component Overview Template, Component Types Template, Config Template (+22 more)

### Community 11 - "BusinessLogic"
Cohesion: 0.08
Nodes (25): BusinessLogic, Method to update component lifetime and service status when no installation…, Method to update status for a given bike based on component service and…, Method to update a component history record with validation, Method to calculate distance and bike id for history records, Method to update a service record, including status changes in both directions, Method to recalculate a component after a completed service is deleted or…, Method to calculate distance and bike id for service records (+17 more)

### Community 12 - "utils.py"
Cohesion: 0.08
Nodes (43): Method to produce payload for page component details, Method to produce payload for page incident reports, Method to produce payload for page of all workplans, Method to produce payload for workplan details page, Method to produce payload for page bike details, Method to read content of components table as formatted tuples, calculate_elapsed_days(), derive_workplan_context() (+35 more)

### Community 13 - "Tests"
Cohesion: 0.11
Nodes (20): Method to create collection, Method to add service record, planned or completed, Method to add a planned service, which has no service date, bike or distance…, Method to build the report used by the plan services and complete services…, Method to create planned services for one or more components with the same…, Method to complete planned services with one service date, keeping their…, Method to validate service records before processing and storing in database, Method to add incident record (+12 more)

### Community 14 - "Result extractor"
Cohesion: 0.09
Nodes (19): Method to update collection, Method to produce payload for page component overview, Method to determine which factor triggered a warning status, Calculate lifetime and service triggers for a component, Method to produce payload for page bike overview, Calculate status flags for a collection based on its components., Method to create component-to-collection mapping dictionaries, Method to produce payload for displaying table of all collections (+11 more)

### Community 15 - "Strava API Integration"
Cohesion: 0.18
Nodes (9): Class to interact with Strava API, Method to authenticate and get data from Stravas gear API, Method to prepare a list of rides, Method to prepare a list of bikes, Method to read oauth options from file, Method to save oauth options to file, Method to authenticate and get data from Stravas activities API, Method to authenticate and get the full list of bike ids from the athlete's… (+1 more)

### Community 16 - "2026-09-18-service-integration-design.md"
Cohesion: 0.17
Nodes (13): Blank values always NULL, never empty strings, Migration steps 12-16 (idempotent check_/migrate_ pairs), Planned services invisible to component health, Planned vs Completed service status, Retired components locked (no service status changes), validate_service_record modes (plan/complete/edit/revert), Production DB regression comparison (master vs branch), Retirement blocked while planned services exist (+5 more)

### Community 17 - "db_migration.py"
Cohesion: 0.19
Nodes (13): check_component_types_columns(), count_component_types_in_use(), find_database_file(), migrate_component_types(), migrate_database(), prompt_for_db_path(), Count how many components use a specific component type, Search for a database file in the user's home directory and subdirectories (+5 more)

### Community 18 - ".create_history_record"
Cohesion: 0.12
Nodes (13): Method to create component, Method to update component details, Method to create installation history record, Method to validate history records before processing and storing in database, Method to orchestrate swap of one component with another, Method to validate quick swap operation, Method to validate collections before allowing bulk operations, Method to change status of all components in a collection (+5 more)

### Community 19 - "run_all_migrations"
Cohesion: 0.14
Nodes (14): create_collections_table(), create_incidents_table(), create_workplans_table(), populate_component_types_thresholds(), populate_components_thresholds(), Creates the incidents table if it doesn't exist., Creates the workplans table if it doesn't exist., Creates the collections table if it doesn't exist. (+6 more)

### Community 20 - "Fullstack Developer -> Code Reviewer Handover"
Cohesion: 0.18
Nodes (10): Method to store error records and ignore lower levels. Filters here instead of…, Method to get error records newer than the given number of hours, Blockers / Open Questions, Context, Decisions Made, Deliverables, Fullstack Developer -> Code Reviewer Handover, Next Steps for Code Reviewer (+2 more)

### Community 21 - "tests/conftest.py"
Cohesion: 0.22
Nodes (12): Task 8: Test foundation and synthetic dataset, fixture, shutil, app_env(), migrated_env(), modules(), Shared fixtures: every test gets its own copy of the template database, Copy template db to tmp dir, write config.json there, chdir into it (+4 more)

### Community 22 - "2026-09-25-service-integration-test-findings.md"
Cohesion: 0.15
Nodes (15): A5: workplan delete blocked while services linked, A. Questions to answer from the code, no change expected, B3: service modal submittable without completion date, B. Bugs to fix, C. Interface changes the user asked for, D4: choose components when creating workplan from incident, Extra wording fixes asked for on 2026-09-26, Manual walkthrough findings (A/B/C/D groups) (+7 more)

### Community 23 - "Service integration: incidents, workplans and services"
Cohesion: 0.15
Nodes (13): Backend, Data model, Error handling, Goal, main.js, main.py, Migration, Modals (+5 more)

### Community 24 - "Migration Tests"
Cohesion: 0.35
Nodes (12): sqlite3, columns(), create_old_schema(), Migration converts the old workplan/incident model to services, Seed workplans, incidents and services in the pre-#351 shape, Recreate services, workplans, incidents and component_history as they were…, run_migration(), seed_old_data() (+4 more)

### Community 25 - "derived.py"
Cohesion: 0.17
Nodes (29): _bike_values(), details(), _by_first(), _collection_values(), details(), status(), _component_values(), details() (+21 more)

### Community 26 - "test_loader.py"
Cohesion: 0.20
Nodes (11): conftest, pathlib, pytest, main(), dumps(), _normalise_value(), Serialise a state deterministically, keeping non-ASCII characters readable, db_copy() (+3 more)

### Community 27 - ".write_delete_record"
Cohesion: 0.12
Nodes (8): Method to retrieve record for a single component type, Method to retrieve record for a specific entry in the installation log, Method to retrieve a specific service record, Method to retrieve record for a specific collection, Method to retrieve record for a specific incident report, Method to retrieve record for a specific workplan, Method to write component type record in database, Method to delete a given record and associated records

### Community 28 - "Rewrite roadmap: new UI, restructured backend, exposed API"
Cohesion: 0.05
Nodes (36): Anti-goals, API: separate API, or one set of resources with two formats, API style: FHIR-conformant or FHIR-inspired, Approaches considered, Branch policy during the freeze, Constraints, Delivery: side by side on master, or frozen master and long-running dev, Frontend: server-rendered with htmx, or a JSON API with a separate frontend app (+28 more)

### Community 29 - "Code Reviewer -> Docs Maintainer Handover"
Cohesion: 0.20
Nodes (9): Method to check the database connection for the health check, Code Reviewer -> Docs Maintainer Handover, Context, Deliverables, Issues Found, Next Steps for Docs Maintainer, References, Resolution (2026-09-27, after review) (+1 more)

### Community 30 - "loader.py"
Cohesion: 0.19
Nodes (13): dataclasses, importlib, AppModules, detect_layout(), _forget_app_modules(), load_app(), Path, Tell the pre-restructure flat layout from the package layout (+5 more)

### Community 31 - "get_service_incident_options"
Cohesion: 0.07
Nodes (32): v0.5.0.ca636f8, generate_incident_title(), get_service_incident_options(), Build incident options for the service modal (4 fields), all incidents so…, Generate a concise title for an incident, Technical debt tracked in issue #356, Context, Docs changes (+24 more)

### Community 32 - "Code review -> docs-maintainer Handover"
Cohesion: 0.50
Nodes (4): Code review -> docs-maintainer Handover, Context, Recommendations, References

### Community 33 - "test_health.py"
Cohesion: 0.23
Nodes (9): Verification done, Health check: errors logged the last 24 hours or a failing database make the…, lifespan in main.py sets every root handler to INFO or DEBUG at startup, SQLite creates an empty file for a wrong path, e.g. a missing Docker mount, recording_logger(), test_missing_database_file_makes_app_unhealthy(), test_recorder_includes_exception_in_message(), test_recorder_keeps_errors_and_ignores_lower_levels() (+1 more)

### Community 34 - "Workplans"
Cohesion: 0.22
Nodes (9): Incidents, Meta, Model for table: incidents, Extends model with extra attributes, Model for table: workplans, Extends model with extra attributes, Workplans, Meta (+1 more)

### Community 35 - "Decided"
Cohesion: 0.06
Nodes (33): get_current_version(), Function to get current program version, Function to read configuration file, read_config(), Global Constraints, Phase B: move, version, config, Docker, branch `feature/stage1-src-layout`, Phase C: tests, branch `feature/stage1-tests`, Phase D: template, CI, releases, cleanup, docs, branch `feature/stage1-finish` (+25 more)

### Community 36 - "check_services_integration_columns"
Cohesion: 0.50
Nodes (4): check_services_integration_columns(), migrate_services_integration_columns(), Check which service integration columns are missing on the services table, Add status, incident_id and planned_date to services, mark existing rows…

### Community 37 - "CLAUDE.md"
Cohesion: 0.22
Nodes (8): Available Agents, Communication & Output Rules, Debugging & Bug Fixing Rules, Direct Invocation, graphify, Important Notes, Project Overview, Sub-Agent Team

### Community 38 - "extract"
Cohesion: 0.22
Nodes (9): AppModules, frozen_clock(), Freeze time at FIXED_NOW in UTC so date-dependent calculations are reproducible, extract(), Path, Run one checkout against a copy of db_path and return its stored and derived…, Run the full recalculation chain and return one sorted line per failed call.…, recalculate() (+1 more)

### Community 39 - ".validate_workplan_completion"
Cohesion: 0.25
Nodes (5): Method to update incident record (supports full or partial updates), Method to update workplan (supports full or partial updates), Method to validate that a workplan can be set to Done, Function to validate that a date string matches the required format YYYY-MM-DD…, validate_date_format()

### Community 40 - "migrate_workplans_to_planned_services"
Cohesion: 0.25
Nodes (8): check_workplans_affected_columns(), migrate_drop_workplan_affected_columns(), migrate_workplans_to_planned_services(), Check if workplans table still has the affected bike/component columns, Resolve bike and component names, marking components that no longer exist, Convert affected components on planned workplans into planned services,…, Rebuild workplans table without the affected bike/component columns, read_names_for_migration()

### Community 41 - "Git Workflow Rules"
Cohesion: 0.29
Nodes (7): Branch Strategy, Commit Process, For All Agents, For code-reviewer, For docs-maintainer, For fullstack-developer, Git Workflow Rules

### Community 42 - "Code Reviewer Agent"
Cohesion: 0.25
Nodes (7): Issues Found, Key Checks, Output Format, Recommendations, Review Philosophy, Review Process, Summary

### Community 43 - "CLAUDE.md"
Cohesion: 0.33
Nodes (5): Change Management Rules, Debugging & bug fixing rules (root cause first), graphify knowledge graph usage rules, Agent handover documents (.handovers/), TomSelect multi-select pattern

### Community 44 - "Development Commands"
Cohesion: 0.40
Nodes (5): Database Operations, Dependencies, Development Commands, Running the Application, Testing

### Community 45 - "Handover Template"
Cohesion: 0.25
Nodes (7): Blockers / Open Questions, Context, Decisions Made, Deliverables, Next Steps for [Target Agent], References, [Source Agent] -> [Target Agent] Handover

### Community 46 - "initializeWorkplanTable"
Cohesion: 0.29
Nodes (8): initializeCollectionsSorting(), sortColumn(), initializeWorkplanTable(), setupIncidentTableSorting(), setupWorkplanSearch(), setupWorkplanStatusFiltering(), setupWorkplanTableSorting(), updateWorkplansVisibility()

### Community 47 - "Middleware"
Cohesion: 0.24
Nodes (7): Middleware, Request, Class to handle exceptions that breaks the program and should be shown to the…, Method to dispatch intercepted requests, Method to catch and handle exceptions, BaseHTTPMiddleware, Exception

### Community 48 - "Database Expert Agent"
Cohesion: 0.29
Nodes (6): Constraints, Core Responsibilities, Pattern Consistency - CRITICAL, Query Optimization, Schema Changes, Workflow

### Community 49 - "UX Designer Agent"
Cohesion: 0.29
Nodes (6): Core Responsibilities, Design Principles, Specifications to Include, v1 (Before Architect), v2 (After Architect), Workflow

### Community 50 - "Health check for Docker daemon (#103)"
Cohesion: 0.21
Nodes (11): Health check run by the Docker daemon, exit code 0 means healthy and 1 means…, health(), Endpoint for the Docker health check, returns 503 if errors were logged the…, get_health_status(), Function to assess application health from errors logged the last 24 hours and…, Docker HEALTHCHECK against /health, Health check for Docker daemon (#103), Separate healthcheck.py instead of curl (+3 more)

### Community 51 - "health-check-reviewer-to-docs-maintainer.md"
Cohesion: 0.32
Nodes (6): Method to check that the database can be read. Reads a real table, since SELECT…, Database check reads bikes table, not SELECT 1, Rename read_database_connection to check_database_connection, ErrorRecorder deque bounded to maxlen=20, ErrorRecorder thread safety under Handler.lock, Catching peewee.DatabaseError for corrupt file

### Community 52 - "Help Page Template"
Cohesion: 0.50
Nodes (5): helpTopics Data Object, Help Page Template, Help Search Functionality, showHelpTopic() Function, Documentation Modal

### Community 53 - "ErrorRecorder"
Cohesion: 0.32
Nodes (6): ErrorRecorder, Logging handler that keeps the most recent error records in memory for the…, Log levels drive container health, Level filtering inside ErrorRecorder.emit(), In-memory 24h error record, ERROR vs WARNING log level rule

### Community 54 - "Component Record Access"
Cohesion: 0.33
Nodes (3): Method to get component names based on list of ids, Method to retrieve record for a specific component, Method to create or update component data to the database

### Community 55 - "migrate_incident_links_to_services"
Cohesion: 0.33
Nodes (6): check_incidents_workplan_column_present(), migrate_drop_incident_workplan_column(), migrate_incident_links_to_services(), Check if incidents table still has the workplan_id column, Rebuild incident to workplan links through services, Rebuild incidents table without the workplan_id column

### Community 56 - "diff"
Cohesion: 0.52
Nodes (6): diff(), One line per difference as 'path: left=... right=...', paths joined with '/, snapshot(), test_changed_value_is_reported_with_path(), test_identical_snapshots_have_no_diff(), test_missing_table_and_row_are_reported()

### Community 57 - "update_config"
Cohesion: 0.50
Nodes (5): asyncio, Endpoint to update config file based on which form was submitted, update_config(), Helper function to shutdown the server after a short delay, shutdown_server()

### Community 58 - "Handover Communication"
Cohesion: 0.33
Nodes (6): Agent Communication via Handovers, Creating Handovers, Detailed Instructions, Handover Structure, Naming Convention, Reading Handovers

### Community 59 - "Fullstack Developer Agent"
Cohesion: 0.33
Nodes (5): Backend Patterns, Core Responsibilities, Frontend Patterns, Handover Content, Workflow

### Community 60 - "Product Manager Agent"
Cohesion: 0.33
Nodes (5): Boundaries, Core Responsibilities, Key Principle: You Are Interactive, Requirements Document, User Story Format

### Community 61 - "Code Style & Standards"
Cohesion: 0.50
Nodes (4): Code Style & Standards, Database, Frontend, Python (Backend)

### Community 62 - "Standard Development Workflow"
Cohesion: 0.50
Nodes (4): For Bug Fixes, For Documentation Updates, For New Features, Standard Development Workflow

### Community 63 - "Handovers Directory Guide"
Cohesion: 0.33
Nodes (5): Creating Handovers, Directory Structure, Finding Handovers, Handovers Directory, Rules

### Community 64 - "Stage 1 Foundation Handover"
Cohesion: 0.18
Nodes (10): Blockers / Open Questions, Context, Decisions Made, Deliverables, Next Steps, Progress log, References, Stage 1 Foundation Handover (+2 more)

### Community 65 - "Architect Agent"
Cohesion: 0.40
Nodes (4): Core Responsibilities, Handover Content, Principles, Workflow

### Community 66 - "Architecture Overview"
Cohesion: 0.40
Nodes (5): Architecture Overview, Configuration, Core Components, Key Features, Project Structure

### Community 67 - "Testing Requirements"
Cohesion: 0.67
Nodes (3): Before Creating Handover, For fullstack-developer, Testing Requirements

### Community 68 - "Development Notes"
Cohesion: 0.40
Nodes (5): Database Schema Changes, Development Notes, Docker Development, Logging, Technical Debt

### Community 69 - "version.py"
Cohesion: 0.50
Nodes (4): get_git_info(), Script to maintain version number, Function to get latest version number and commit hash, subprocess

### Community 70 - ".read_bike_name"
Cohesion: 0.33
Nodes (3): Method to retrieve record for a specific bike, Method to create or update bike data to the database, Method to get the name of a bike based on bike id

### Community 71 - "write_config"
Cohesion: 0.50
Nodes (4): parse_button_sorting(), Function to parse button sorting data from form submission, Function to update configuration file based on which form was submitted, write_config()

### Community 72 - "History Notes Migration"
Cohesion: 0.50
Nodes (4): check_component_history_notes_column(), migrate_component_history_notes(), Check if component_history table needs notes column, Add notes column to component_history table

### Community 74 - "service-integration-fullstack-to-reviewer.md"
Cohesion: 0.38
Nodes (6): D1: optional user-entered workplan name, FastAPI/Starlette TemplateResponse argument order fix, Workplan link silently lost bug (process_service_records without workplan_id), Optional workplan_name (migration step 17), db_migration step 16 rebuild before step 17 workplan_name, v0.5.0 release (service integration, health check, uv)

### Community 75 - "Services Workplan Link Migration"
Cohesion: 0.50
Nodes (4): check_services_workplan_column(), migrate_services_workplan_link(), Check if Services table needs workplan_id column, Add workplan_id column to Services table for workplan hub integration

### Community 76 - "Workplan Name Migration"
Cohesion: 0.50
Nodes (4): check_workplans_name_column(), migrate_workplans_name_column(), Check if workplans table needs the workplan_name column, Add the optional user given name to the workplans table, existing workplans…

### Community 77 - "Log Filtering"
Cohesion: 0.50
Nodes (4): get_filtered_log(), Endpoint to read log and return only business events, Function to get filtered log records, read_filtered_logs()

### Community 78 - "stored_state"
Cohesion: 0.25
Nodes (14): Path, normalise_new_ids(), Read every table and column straight from SQLite, keyed table, primary key,…, Replace primary keys absent from baseline_ids with new:<table>:<n>. Only whole…, stored_state(), insert(), test_extraction_is_repeatable(), test_normalise_new_ids_is_stable() (+6 more)

### Community 79 - "Docs Maintainer Agent"
Cohesion: 0.50
Nodes (3): Core Responsibilities, Documentation Rules, Workflow

### Community 81 - "Results"
Cohesion: 0.29
Nodes (7): 2026-09-25, first walkthrough, human, 2026-09-26, regression against the baseline database, Claude, 2026-09-27, second walkthrough, human, Preparation, Results, Scope, Test Protocol: Planned services, workplans and incidents

### Community 84 - "Service integration (#351) - fullstack to code-reviewer"
Cohesion: 0.14
Nodes (15): build_incident_service_entry(), get_effective_planned_date(), Return the service's own planned date, else the workplan due date, else None, Describe one service linked to an incident, for the read only list in the…, Status (2026-09-26), Effective planned date fallback, Bugs found and fixed, Key decisions (+7 more)

### Community 86 - "validateComponentThresholds"
Cohesion: 0.40
Nodes (5): addFormValidation(), clearValidationErrors(), showFieldError(), validateComponentThresholds(), validateQuickSwapForm()

### Community 90 - "clock.py"
Cohesion: 0.40
Nodes (4): contextlib, os, time, time_machine

### Community 93 - "migrate_component_types_time_fields"
Cohesion: 0.50
Nodes (4): check_component_types_time_columns(), migrate_component_types_time_fields(), Check if ComponentTypes table needs time-based fields migration, Add time-based fields to ComponentTypes table

### Community 94 - "D. Design questions to decide before coding"
Cohesion: 0.14
Nodes (14): check_incidents_workplan_column(), migrate_incidents_workplan_link(), Check if Incidents table needs workplan_id column, Add workplan_id column to Incidents table for workplan hub integration, Code review outcome, 2026-09-26, D2: incident modal lists linked services, D. Design questions to decide before coding, Decisions (2026-09-26) (+6 more)

### Community 95 - "migrate_components_time_fields"
Cohesion: 0.50
Nodes (4): check_components_time_columns(), migrate_components_time_fields(), Check if Components table needs time-based fields migration, Add time-based fields to Components table and populate threshold_km

### Community 97 - "cleanup"
Cohesion: 0.50
Nodes (4): cleanup(), handleCancel(), handleConfirm(), performBulkStatusChange()

### Community 99 - "renderPreview"
Cohesion: 0.50
Nodes (4): containsMarkdown(), renderPreview(), setInitialMode(), updateCheckboxInText()

### Community 102 - "initializeIncidentTable"
Cohesion: 0.67
Nodes (4): initializeIncidentTable(), setupIncidentSearch(), setupIncidentStatusFiltering(), updateIncidentVisibility()

### Community 104 - "GitHub Issues Tracker"
Cohesion: 0.50
Nodes (4): Error Page Template, Footer Template, GitHub Issues Tracker, Velo Supervisor 2000 (Project)

### Community 105 - "handleOldComponentChange"
Cohesion: 0.67
Nodes (3): filterNewComponentsByType(), handleOldComponentChange(), updateQuickSwapCollectionWarning()

### Community 151 - "compare.py"
Cohesion: 0.21
Nodes (12): argparse, _error_paths(), main(), present_on_both_sides(), Path, Recalculation failures and derived error entries that appear identically on…, rows_per_table(), _run_extract() (+4 more)

## Ambiguous Edges - Review These
- `tests/conftest.py` → `Manual testing protocols approach`  [AMBIGUOUS]
  tests/README.md · relation: conceptually_related_to

## Knowledge Gaps
- **249 isolated node(s):** `Context`, `Deliverables`, `Task 3, step 6: baseline dev vs master`, `Next Steps`, `Blockers / Open Questions` (+244 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 618 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **52 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `tests/conftest.py` and `Manual testing protocols approach`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **Why does `DatabaseManager` connect `DatabaseManager` to `Component History Query`, `Workplans`, `database_model.py`, `.read_bike_name`, `.read_all_components_objects`, `Service Record Queries`, `utils.py`, `.read_all_workplans`, `.read_bike_id_recent_component_history`, `health-check-reviewer-to-docs-maintainer.md`, `.read_date_oldest_ride`, `Component Record Access`, `.read_matching_rides`, `.read_sum_distance_subset_rides`, `.read_workplans_by_incident`, `.write_delete_record`?**
  _High betweenness centrality (0.136) - this node is a cross-community bridge._
- **Why does `BusinessLogic` connect `BusinessLogic` to `scheduler.py`, `.validate_workplan_completion`, `utils.py`, `Tests`, `Result extractor`, `.create_history_record`, `Code Reviewer -> Docs Maintainer Handover`?**
  _High betweenness centrality (0.103) - this node is a cross-community bridge._
- **Why does `Issues found (none blocking)` connect `utils.py` to `Code review -> docs-maintainer Handover`, `get`, `.read_bike_name`, `Component Record Access`, `D. Design questions to decide before coding`?**
  _High betweenness centrality (0.064) - this node is a cross-community bridge._
- **Are the 9 inferred relationships involving `DatabaseManager` (e.g. with `Bikes` and `Collections`) actually correct?**
  _`DatabaseManager` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `BusinessLogic` (e.g. with `strava_sync_job()` and `update_time_based_fields_job()`) actually correct?**
  _`BusinessLogic` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `run_all_migrations()` (e.g. with `Task 8: Test foundation and synthetic dataset` and `Migration steps 12-16 (idempotent check_/migrate_ pairs)`) actually correct?**
  _`run_all_migrations()` has 3 INFERRED edges - model-reasoned connections that need verification._