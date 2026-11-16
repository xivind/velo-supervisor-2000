# Graph Report - velo-supervisor-2000  (2026-11-16)

## Corpus Check
- 61 files · ~165,544 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 12 file(s) not represented in the graph (top: (none) 5, .example 1, .sqlite 1)

## Summary
- 1231 nodes · 2014 edges · 126 communities (78 shown, 48 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 188 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `211bf439`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- main.py
- scheduler.py
- get
- seed_component
- Meta
- DatabaseManager
- Tests
- get_button_order
- .process_history_records
- main.js
- .process_service_records
- get_workplan_data_tuple
- service-integration-reviewer-to-docs-maintainer.md
- D. Design questions to decide before coding
- .create_history_record
- Strava
- 2026-09-18-service-integration-design.md
- .write_delete_record
- extract.py
- business_logic.py
- migrate_component_types
- db_migration.py
- Service integration: incidents, workplans and services
- test_migration.py
- README.md
- derived_values
- validateDateInput
- Decided
- insert
- compare.py
- Service integration (#351) - fullstack to code-reviewer
- GitHub Issues Tracker
- Task 2: Derived values
- sortColumn
- CLAUDE.md
- Git Workflow Rules
- test_loader.py
- .read_bike_name
- CLAUDE.md
- Code Reviewer Agent
- .read_component
- Phase B: move, version, config, Docker, branch `feature/stage1-src-layout`
- Handover Template
- 2026-09-25-service-integration-test-findings.md
- ErrorRecorder
- Database Expert Agent
- UX Designer Agent
- test_derived.py
- test_health.py
- test_config.py
- migrate_database
- validateComponentThresholds
- Handover Communication
- Fullstack Developer Agent
- Product Manager Agent
- service-integration-fullstack-to-reviewer.md
- Handovers Directory Guide
- Architect Agent
- Architecture Overview
- Development Commands
- Development Notes
- Results
- Standard Development Workflow
- Task 14: Rules, health and migration rewritten; old tests removed
- get_filtered_log
- Stage 1 Foundation Handover
- cleanup
- renderPreview
- initializeIncidentTable
- handleOldComponentChange
- Docs Maintainer Agent
- Code Style & Standards
- Middleware
- create-container-vs2000.sh
- .count_component_types_in_use
- .read_all_component_types
- .read_all_workplans
- .read_bike_id_recent_component_history
- .read_latest_history_record
- .read_latest_service_record
- .read_matching_rides
- .read_oldest_history_record
- .read_open_incidents
- .read_planned_services_by_workplan
- .read_recent_rides
- .read_services_by_incident
- .read_services_by_workplan
- .read_subset_components
- .read_subset_installed_components
- .write_bike_service_status
- .write_component_distance
- .write_component_service_status
- .write_history_record
- .write_incident_record
- .write_service_record
- .write_workplan
- utils.py
- BusinessLogic
- Strava OAuth Token Setup (Step 2)
- Branching and Versioning
- Changelog and Project Board
- Fullstack Developer -> Code Reviewer Handover
- .get_component_details
- get_formatted_bikes_list
- get_planned_service_data_tuple
- fixture
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

## God Nodes (most connected - your core abstractions)
1. `DatabaseManager` - 72 edges
2. `BusinessLogic` - 67 edges
3. `seed_component()` - 24 edges
4. `run_all_migrations()` - 22 edges
5. `Tests` - 21 edges
6. `Meta` - 20 edges
7. `derived_values()` - 20 edges
8. `seed_rides()` - 20 edges
9. `Task 2: Derived values` - 18 edges
10. `insert()` - 15 edges

## Surprising Connections (you probably didn't know these)
- `Decisions Made` --references--> `extract()`  [INFERRED]
  .handovers/stages/stage-1-foundation-handover.md → scripts/integrity/extract.py
- `Task 6: Config location from `VELO_SUPERVISOR_CONFIG`` --references--> `read_config()`  [INFERRED]
  docs/superpowers/plans/2026-11-16-stage-1-foundation.md → src/velo_supervisor/utils.py
- `Configuration file location` --references--> `read_config()`  [INFERRED]
  docs/superpowers/specs/2026-11-16-stage-1-foundation-design.md → src/velo_supervisor/utils.py
- `Task 3, step 5: failing-comparison proof` --references--> `diff()`  [INFERRED]
  .handovers/stages/stage-1-foundation-handover.md → scripts/integrity/compare.py
- `Task 1: Integrity package: loader, clock, recalculation, stored-state snapshot` --references--> `AppModules`  [INFERRED]
  docs/superpowers/plans/2026-11-16-stage-1-foundation.md → scripts/integrity/loader.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Service integration spec, implementation, test and review cycle** — docs_superpowers_specs_2026_09_18_service_integration_design, handovers_fullstack_service_integration_fullstack_to_reviewer, docs_superpowers_plans_2026_09_25_service_integration_test_findings, tests_test_protocol_services, handovers_review_service_integration_reviewer_to_docs_maintainer [EXTRACTED 1.00]

## Communities (126 total, 48 thin omitted)

### Community 0 - "main.py"
Cohesion: 0.07
Nodes (39): fastapi_responses, fastapi_staticfiles, fastapi_templating, post, add_collection(), add_incident_record(), add_planned_services(), add_service() (+31 more)

### Community 1 - "scheduler.py"
Cohesion: 0.15
Nodes (15): apscheduler_schedulers_asyncio, apscheduler_triggers_cron, apscheduler_triggers_interval, FastAPI, lifespan(), Manage application startup and shutdown, Initialize and start the APScheduler instance, Scheduler for automated maintenance tasks (+7 more)

### Community 2 - "get"
Cohesion: 0.09
Nodes (28): exception_handler, get, add_history_record(), collection_details(), component_overview(), component_types_overview(), help_page(), http_exception_handler() (+20 more)

### Community 3 - "seed_component"
Cohesion: 0.07
Nodes (52): Context, Docs changes, docs-maintainer -> Human Handover, Double-check, Files to commit, Option A: one commit, Option B: three commits (main.js needs `git add -p`), Post-release fixes to v0.5.0 (+44 more)

### Community 4 - "Meta"
Cohesion: 0.10
Nodes (35): Model, peewee, Module for interaction with a Sqlite database, BaseModel, Bikes, Collections, ComponentHistory, Components (+27 more)

### Community 5 - "DatabaseManager"
Cohesion: 0.04
Nodes (24): DatabaseManager, Method to sum distance for a given set of rides, Method to read all component objects (not tuples), Class to interact with a SQLite database through Peewee, Method to read a subset of records from the component history table, Method to read completed services for a component, used by health computation, Method to check that the database can be read. Reads a real table, since SELECT…, Method to retrieve record for a specific entry in the service log (+16 more)

### Community 6 - "Tests"
Cohesion: 0.16
Nodes (13): Task 11: Operation scenarios: services, workplans, incidents, collections, Constraints, Tests, Method to create collection, Method to add service record, planned or completed, Method to add a planned service, which has no service date, bike or distance…, Method to create planned services for one or more components with the same…, Method to validate service records before processing and storing in database (+5 more)

### Community 7 - "get_button_order"
Cohesion: 0.20
Nodes (10): bike_details(), component_details(), config_overview(), Endpoint for component details page, Endpoint for component types page, Endpoint for bike details page, get_button_order(), get_button_sorting_config() (+2 more)

### Community 8 - ".process_history_records"
Cohesion: 0.17
Nodes (9): Method to update component lifetime and service status when no installation…, Method to update status for a given bike based on component service and…, Method to calculate distance and bike id for history records, Method to compute component status using threshold logic, Method to determine worst-case status between distance and days-based…, Method to update time-based status fields for all non-retired components, Method to update component table with distance from ride table, Method to update component table with lifetime status (+1 more)

### Community 9 - "main.js"
Cohesion: 0.09
Nodes (9): editCollection(), handleUpdate(), initializeCollectionsSearch(), updateRowVisibility(), initializeComponentSelector(), NOTE: All collection details page handlers are in the "Functions used on…, IMPORTANT: Remove readonly - allow manual typing, showToast() (+1 more)

### Community 10 - ".process_service_records"
Cohesion: 0.22
Nodes (5): Method to build the report used by the plan services and complete services…, Method to complete planned services with one service date, keeping their…, Method to update a service record, including status changes in both directions, Method to recalculate a component after a completed service is deleted or…, Method to calculate distance and bike id for service records

### Community 11 - "get_workplan_data_tuple"
Cohesion: 0.14
Nodes (20): Method to produce payload for page incident reports, Method to produce payload for workplan details page, calculate_elapsed_days(), derive_workplan_context(), generate_workplan_title(), get_formatted_datetime_now(), get_incident_data_tuple(), get_workplan_data_tuple() (+12 more)

### Community 12 - "service-integration-reviewer-to-docs-maintainer.md"
Cohesion: 0.18
Nodes (10): Code review -> docs-maintainer Handover, Context, Dead reads read_all_services_by_component / read_all_planned_services, derive_workplan_context computed twice per render, Issues found (none blocking), Recommendations, References, Unescaped innerHTML in renderIncidentServices (+2 more)

### Community 13 - "D. Design questions to decide before coding"
Cohesion: 0.25
Nodes (8): Code review outcome, 2026-09-26, D. Design questions to decide before coding, Decisions (2026-09-26), Follow-up tweaks asked for on 2026-09-26, Second round of tweaks, 2026-09-26, Status (2026-09-26), Third round of tweaks, 2026-09-26, Warning when resolving an incident with open services, 2026-09-26

### Community 14 - ".create_history_record"
Cohesion: 0.15
Nodes (10): Task 10: Operation scenarios: components, history, quick swap, types, config, Method to create component, Method to update component details, Method to create installation history record, Method to orchestrate swap of one component with another, Validate threshold configuration rules for component intervals, Method to check if a bike has all mandatory components and respects max…, Method to create or update component types (+2 more)

### Community 15 - "Strava"
Cohesion: 0.18
Nodes (9): Class to interact with Strava API, Method to authenticate and get data from Stravas gear API, Method to prepare a list of rides, Method to prepare a list of bikes, Method to read oauth options from file, Method to save oauth options to file, Method to authenticate and get data from Stravas activities API, Method to authenticate and get the full list of bike ids from the athlete's… (+1 more)

### Community 16 - "2026-09-18-service-integration-design.md"
Cohesion: 0.13
Nodes (17): Blank values always NULL, never empty strings, Completed to Planned revert uses deletion recalculation, Notes on component status change (#349), Workplan bike/components derived through services, Effective planned date fallback, Migration steps 12-16 (idempotent check_/migrate_ pairs), Plan and complete services modals sharing one JS helper, Planned services invisible to component health (+9 more)

### Community 17 - ".write_delete_record"
Cohesion: 0.12
Nodes (8): Method to retrieve record for a single component type, Method to retrieve record for a specific entry in the installation log, Method to retrieve a specific service record, Method to retrieve record for a specific collection, Method to retrieve record for a specific incident report, Method to retrieve record for a specific workplan, Method to write component type record in database, Method to delete a given record and associated records

### Community 18 - "extract.py"
Cohesion: 0.12
Nodes (24): contextlib, dataclasses, importlib, os, frozen_clock(), Freeze time at FIXED_NOW in UTC so date-dependent calculations are reproducible, extract(), main() (+16 more)

### Community 19 - "business_logic.py"
Cohesion: 0.14
Nodes (15): datetime, logging, requests_oauthlib, Module to handle business logic, Module for middleware, Module to interact with Strava APIs, generate_incident_title(), get_service_incident_options() (+7 more)

### Community 20 - "migrate_component_types"
Cohesion: 0.33
Nodes (6): check_component_types_columns(), count_component_types_in_use(), migrate_component_types(), Check if the component_types table needs migration, Migrate the component_types table to add new columns, Count how many components use a specific component type

### Community 21 - "db_migration.py"
Cohesion: 0.05
Nodes (59): check_component_history_notes_column(), check_component_types_time_columns(), check_components_time_columns(), check_incidents_workplan_column(), check_incidents_workplan_column_present(), check_services_integration_columns(), check_services_workplan_column(), check_workplans_affected_columns() (+51 more)

### Community 23 - "Service integration: incidents, workplans and services"
Cohesion: 0.11
Nodes (18): Backend, business_logic.py, Data model, database_manager.py, Decisions, Error handling, Goal, main.js (+10 more)

### Community 24 - "test_migration.py"
Cohesion: 0.32
Nodes (11): columns(), create_old_schema(), Migration converts the old workplan/incident model to services, Seed workplans, incidents and services in the pre-#351 shape, Recreate services, workplans, incidents and component_history as they were…, run_migration(), seed_old_data(), snapshot() (+3 more)

### Community 25 - "README.md"
Cohesion: 0.50
Nodes (3): Strava OAuth scope incl. profile:read_all, Switched from pip to uv, GitHub action writes current_version.txt on master

### Community 26 - "derived_values"
Cohesion: 0.20
Nodes (26): _bike_values(), details(), _by_first(), _collection_values(), details(), status(), _component_values(), details() (+18 more)

### Community 27 - "validateDateInput"
Cohesion: 0.20
Nodes (9): initializeDatePickers(), initializeIncidentForm(), initializeWorkplanForm(), submitCollectionAjax(), submitComponentAjax(), validateCollectionStatusChange(), validateDateInput(), validateIncidentForm() (+1 more)

### Community 28 - "Decided"
Cohesion: 0.04
Nodes (46): Anti-goals, API: separate API, or one set of resources with two formats, API style: FHIR-conformant or FHIR-inspired, Approaches considered, Branch policy during the freeze, Constraints, Delivery: side by side on master, or frozen master and long-running dev, Frontend: server-rendered with htmx, or a JSON API with a separate frontend app (+38 more)

### Community 29 - "insert"
Cohesion: 0.19
Nodes (20): Review Focus, Task 1: Integrity package: loader, clock, recalculation, stored-state snapshot, re, normalise_new_ids(), _normalise_value(), Path, Read every table and column straight from SQLite, keyed table, primary key,…, Replace primary keys absent from baseline_ids with new:<table>:<n>. Only whole… (+12 more)

### Community 30 - "compare.py"
Cohesion: 0.09
Nodes (30): argparse, Global Constraints, Phase A: extractor and baseline, branch `feature/stage1-extractor`, Phase C: tests, branch `feature/stage1-tests`, Phase D: template, CI, releases, cleanup, docs, branch `feature/stage1-finish`, Stage 1 Foundation Implementation Plan, Task 12: Strava sync, Task 15: Template database defaults (+22 more)

### Community 33 - "Service integration (#351) - fullstack to code-reviewer"
Cohesion: 0.18
Nodes (11): Bugs found and fixed, Files, Key decisions, Known limitations, Next steps, Regression evidence, 2026-09-26, Reuse, Second round, 2026-09-26, after the manual walkthrough (+3 more)

### Community 35 - "Task 2: Derived values"
Cohesion: 0.14
Nodes (13): Task 2: Derived values, Result extractor, Method to produce payload for page component overview, Calculate lifetime and service triggers for a component, Method to produce payload for page bike overview, Method to create component-to-collection mapping dictionaries, Method to build dictionaries of bike and component ids referenced in received…, Method to build dictionaries of bike and component ids referenced by services… (+5 more)

### Community 36 - "sortColumn"
Cohesion: 0.29
Nodes (8): initializeCollectionsSorting(), sortColumn(), initializeWorkplanTable(), setupIncidentTableSorting(), setupWorkplanSearch(), setupWorkplanStatusFiltering(), setupWorkplanTableSorting(), updateWorkplansVisibility()

### Community 37 - "CLAUDE.md"
Cohesion: 0.17
Nodes (11): Available Agents, Before Creating Handover, Communication & Output Rules, Debugging & Bug Fixing Rules, Direct Invocation, For fullstack-developer, graphify, Important Notes (+3 more)

### Community 38 - "Git Workflow Rules"
Cohesion: 0.29
Nodes (7): Branch Strategy, Commit Process, For All Agents, For code-reviewer, For docs-maintainer, For fullstack-developer, Git Workflow Rules

### Community 39 - "test_loader.py"
Cohesion: 0.14
Nodes (12): conftest, Task 4: Move to the src layout, integrity_clock, integrity_loader, integrity_recalculate, integrity_snapshot, Health check run by the Docker daemon, exit code 0 means healthy and 1 means…, sys (+4 more)

### Community 40 - ".read_bike_name"
Cohesion: 0.33
Nodes (3): Method to retrieve record for a specific bike, Method to create or update bike data to the database, Method to get the name of a bike based on bike id

### Community 41 - "CLAUDE.md"
Cohesion: 0.12
Nodes (15): Change Management Rules, Debugging & bug fixing rules (root cause first), Docker HEALTHCHECK against /health, graphify knowledge graph usage rules, Agent handover documents (.handovers/), Log levels drive container health, Technical debt tracked in issue #356, TomSelect multi-select pattern (+7 more)

### Community 42 - "Code Reviewer Agent"
Cohesion: 0.25
Nodes (7): Issues Found, Key Checks, Output Format, Recommendations, Review Philosophy, Review Process, Summary

### Community 43 - ".read_component"
Cohesion: 0.33
Nodes (3): Method to get component names based on list of ids, Method to retrieve record for a specific component, Method to create or update component data to the database

### Community 44 - "Phase B: move, version, config, Docker, branch `feature/stage1-src-layout`"
Cohesion: 0.29
Nodes (7): Phase B: move, version, config, Docker, branch `feature/stage1-src-layout`, Task 5: Version from the git tag, Task 6: Config location from `VELO_SUPERVISOR_CONFIG`, Task 7: Docker image and first CI workflow, Version and releases, get_current_version(), Function to get current program version

### Community 45 - "Handover Template"
Cohesion: 0.25
Nodes (7): Blockers / Open Questions, Context, Decisions Made, Deliverables, Next Steps for [Target Agent], References, [Source Agent] -> [Target Agent] Handover

### Community 46 - "2026-09-25-service-integration-test-findings.md"
Cohesion: 0.12
Nodes (17): A5: workplan delete blocked while services linked, A. Questions to answer from the code, no change expected, Answers (read from the code 2026-09-25), B3: service modal submittable without completion date, B. Bugs to fix, C. Interface changes the user asked for, D2: incident modal lists linked services, D4: choose components when creating workplan from incident (+9 more)

### Community 47 - "ErrorRecorder"
Cohesion: 0.18
Nodes (8): health(), Endpoint for the Docker health check, returns 503 if errors were logged the…, ErrorRecorder, get_health_status(), Logging handler that keeps the most recent error records in memory for the…, Method to store error records and ignore lower levels. Filters here instead of…, Method to get error records newer than the given number of hours, Function to assess application health from errors logged the last 24 hours and…

### Community 48 - "Database Expert Agent"
Cohesion: 0.29
Nodes (6): Constraints, Core Responsibilities, Pattern Consistency - CRITICAL, Query Optimization, Schema Changes, Workflow

### Community 49 - "UX Designer Agent"
Cohesion: 0.29
Nodes (6): Core Responsibilities, Design Principles, Specifications to Include, v1 (Before Architect), v2 (After Architect), Workflow

### Community 50 - "test_derived.py"
Cohesion: 0.10
Nodes (25): Task 13: Page render tests, Task 8: Test foundation and synthetic dataset, fixture, json, pathlib, pytest, dumps(), Serialise a state deterministically, keeping non-ASCII characters readable (+17 more)

### Community 51 - "test_health.py"
Cohesion: 0.10
Nodes (22): Database check reads bikes table, not SELECT 1, Rename read_database_connection to check_database_connection, Code Reviewer -> Docs Maintainer Handover, Context, Deliverables, ErrorRecorder deque bounded to maxlen=20, ErrorRecorder thread safety under Handler.lock, Issues Found (+14 more)

### Community 52 - "test_config.py"
Cohesion: 0.17
Nodes (3): importlib_metadata, test_version_unknown_when_not_installed(), velo_supervisor

### Community 53 - "migrate_database"
Cohesion: 0.33
Nodes (6): find_database_file(), migrate_database(), prompt_for_db_path(), Search for a database file in the user's home directory and subdirectories, Prompt user for database path or filename and verify it exists, Main function to handle the database migration.

### Community 54 - "validateComponentThresholds"
Cohesion: 0.40
Nodes (5): addFormValidation(), clearValidationErrors(), showFieldError(), validateComponentThresholds(), validateQuickSwapForm()

### Community 58 - "Handover Communication"
Cohesion: 0.33
Nodes (6): Agent Communication via Handovers, Creating Handovers, Detailed Instructions, Handover Structure, Naming Convention, Reading Handovers

### Community 59 - "Fullstack Developer Agent"
Cohesion: 0.33
Nodes (5): Backend Patterns, Core Responsibilities, Frontend Patterns, Handover Content, Workflow

### Community 60 - "Product Manager Agent"
Cohesion: 0.33
Nodes (5): Boundaries, Core Responsibilities, Key Principle: You Are Interactive, Requirements Document, User Story Format

### Community 61 - "service-integration-fullstack-to-reviewer.md"
Cohesion: 0.31
Nodes (8): D1: optional user-entered workplan name, Service integration: services as unit of work (#351), data-incident-status-listener guard, FastAPI/Starlette TemplateResponse argument order fix, Workplan link silently lost bug (process_service_records without workplan_id), Optional workplan_name (migration step 17), db_migration step 16 rebuild before step 17 workplan_name, v0.5.0 release (service integration, health check, uv)

### Community 63 - "Handovers Directory Guide"
Cohesion: 0.33
Nodes (5): Creating Handovers, Directory Structure, Finding Handovers, Handovers Directory, Rules

### Community 65 - "Architect Agent"
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

### Community 69 - "Results"
Cohesion: 0.29
Nodes (7): 2026-09-25, first walkthrough, human, 2026-09-26, regression against the baseline database, Claude, 2026-09-27, second walkthrough, human, Preparation, Results, Scope, Test Protocol: Planned services, workplans and incidents

### Community 70 - "Standard Development Workflow"
Cohesion: 0.50
Nodes (4): For Bug Fixes, For Documentation Updates, For New Features, Standard Development Workflow

### Community 71 - "Task 14: Rules, health and migration rewritten; old tests removed"
Cohesion: 0.17
Nodes (8): Task 14: Rules, health and migration rewritten; old tests removed, Method to update a component history record with validation, Method to validate history records before processing and storing in database, Method to validate quick swap operation, Method to validate collections before allowing bulk operations, Method to validate that a workplan can be set to Done, Function to validate that a date string matches the required format YYYY-MM-DD…, validate_date_format()

### Community 72 - "get_filtered_log"
Cohesion: 0.50
Nodes (4): get_filtered_log(), Endpoint to read log and return only business events, Function to get filtered log records, read_filtered_logs()

### Community 73 - "Stage 1 Foundation Handover"
Cohesion: 0.14
Nodes (13): Blockers / Open Questions, Context, Decisions Made, Deliverables, End of Phase B (after Tasks 5-7: version from git tag, config from `VELO_SUPERVISOR_CONFIG`, new Docker image), Next Steps, Progress log, References (+5 more)

### Community 75 - "cleanup"
Cohesion: 0.50
Nodes (4): cleanup(), handleCancel(), handleConfirm(), performBulkStatusChange()

### Community 76 - "renderPreview"
Cohesion: 0.50
Nodes (4): containsMarkdown(), renderPreview(), setInitialMode(), updateCheckboxInText()

### Community 77 - "initializeIncidentTable"
Cohesion: 0.67
Nodes (4): initializeIncidentTable(), setupIncidentSearch(), setupIncidentStatusFiltering(), updateIncidentVisibility()

### Community 78 - "handleOldComponentChange"
Cohesion: 0.67
Nodes (3): filterNewComponentsByType(), handleOldComponentChange(), updateQuickSwapCollectionWarning()

### Community 79 - "Docs Maintainer Agent"
Cohesion: 0.50
Nodes (3): Core Responsibilities, Documentation Rules, Workflow

### Community 80 - "Code Style & Standards"
Cohesion: 0.50
Nodes (4): Code Style & Standards, Database, Frontend, Python (Backend)

### Community 81 - "Middleware"
Cohesion: 0.24
Nodes (7): BaseHTTPMiddleware, Exception, Middleware, Request, Class to handle exceptions that breaks the program and should be shown to the…, Method to dispatch intercepted requests, Method to catch and handle exceptions

### Community 105 - "utils.py"
Cohesion: 0.15
Nodes (16): asyncio, collections, Endpoint to update config file based on which form was submitted, update_config(), config_path(), parse_button_sorting(), Helper function to shutdown the server after a short delay, Module for auxiliary functions (+8 more)

### Community 107 - "BusinessLogic"
Cohesion: 0.10
Nodes (13): BusinessLogic, Method to update collection, Method to change status of all components in a collection, Method to determine which factor triggered a warning status, Method to update incident record (supports full or partial updates), Method to update workplan (supports full or partial updates), Method to refresh all bikes from Strava, Function to set the date for last pull from Strava (+5 more)

### Community 111 - "Fullstack Developer -> Code Reviewer Handover"
Cohesion: 0.25
Nodes (8): Blockers / Open Questions, Context, Decisions Made, Deliverables, Fullstack Developer -> Code Reviewer Handover, Next Steps for Code Reviewer, References, Verification done

### Community 113 - ".get_component_details"
Cohesion: 0.22
Nodes (8): Method to produce payload for page component details, Method to read content of components table as formatted tuples, calculate_percentage_reached(), format_component_status(), format_cost(), Function to display user friendly text for None values, Function to display user friendly text for None values, Function to calculate remaining service interval or remaining lifetime as…

### Community 114 - "get_formatted_bikes_list"
Cohesion: 0.50
Nodes (3): Method to produce payload for page of all workplans, get_formatted_bikes_list(), Function to get list of all bikes, with prefix for retired bikes

### Community 115 - "get_planned_service_data_tuple"
Cohesion: 0.33
Nodes (6): build_incident_service_entry(), get_effective_planned_date(), get_planned_service_data_tuple(), Return the service's own planned date, else the workplan due date, else None, Describe one service linked to an incident, for the read only list in the…, Build standard planned service tuple for display (11 fields)

## Ambiguous Edges - Review These
- `tests/conftest.py` → `Manual testing protocols approach`  [AMBIGUOUS]
  tests/README.md · relation: conceptually_related_to

## Knowledge Gaps
- **253 isolated node(s):** `Context`, `Deliverables`, `Task 3, step 6: baseline dev vs master`, `End of Phase B (after Tasks 5-7: version from git tag, config from `VELO_SUPERVISOR_CONFIG`, new Docker image)`, `Switch-over steps for the Pi (Stage 6)` (+248 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 644 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **48 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `tests/conftest.py` and `Manual testing protocols approach`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **Why does `DatabaseManager` connect `DatabaseManager` to `Meta`, `.write_delete_record`, `business_logic.py`, `.read_bike_name`, `.read_component`, `.count_component_types_in_use`, `.read_all_component_types`, `.read_all_workplans`, `.read_bike_id_recent_component_history`, `.read_latest_history_record`, `.read_latest_service_record`, `.read_matching_rides`, `.read_oldest_history_record`, `.read_open_incidents`, `.read_planned_services_by_workplan`, `.read_recent_rides`, `.read_services_by_incident`, `.read_services_by_workplan`, `.read_subset_components`, `.read_subset_installed_components`, `.write_bike_service_status`, `.write_component_distance`, `.write_component_service_status`, `.write_history_record`, `.write_incident_record`, `.write_service_record`, `.write_workplan`, `.get_component_details`?**
  _High betweenness centrality (0.194) - this node is a cross-community bridge._
- **Why does `BusinessLogic` connect `BusinessLogic` to `main.py`, `scheduler.py`, `Task 2: Derived values`, `Tests`, `Task 14: Rules, health and migration rewritten; old tests removed`, `.process_history_records`, `.process_service_records`, `get_workplan_data_tuple`, `.create_history_record`, `.get_component_details`, `get_formatted_bikes_list`, `business_logic.py`?**
  _High betweenness centrality (0.094) - this node is a cross-community bridge._
- **Why does `Manual testing protocols approach` connect `2026-09-18-service-integration-design.md` to `test_derived.py`?**
  _High betweenness centrality (0.087) - this node is a cross-community bridge._
- **Are the 9 inferred relationships involving `DatabaseManager` (e.g. with `Bikes` and `Collections`) actually correct?**
  _`DatabaseManager` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Are the 20 inferred relationships involving `Tests` (e.g. with `.create_collection()` and `.create_history_record()`) actually correct?**
  _`Tests` has 20 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Context`, `Deliverables`, `Task 3, step 6: baseline dev vs master` to the rest of the system?**
  _253 weakly-connected nodes found - possible documentation gaps or missing edges._