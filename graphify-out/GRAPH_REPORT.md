# Graph Report - velo-supervisor-2000  (2026-11-17)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 1478 nodes · 2493 edges · 183 communities (96 shown, 87 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 176 edges (avg confidence: 0.93)
- Token cost: 85,657 input · 2,527 output

## Graph Freshness
- Built from commit: `0ce8dd31`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Write Route Handlers
- App Lifespan and Scheduler
- Fake Strava OAuth Session
- README and Release Notes
- Peewee ORM Models
- Frozen Clock Fixtures
- Service and Collection Characterisation
- Database Read Queries
- Expected Result Assertions
- Exception Handling Middleware
- Component Status Recalculation
- Validation Refusal Tests
- Collection and Component Frontend
- App Loader and Extractor
- Docker Healthcheck Script
- Page Endpoints
- Snapshot Delta
- Strava API Client
- Single Record Reads
- Migration Table Creation
- Stage 1 Foundation Plan
- Form Validation and Date Pickers
- Extract and Compare CLIs
- Service and Workplan Creation
- Create Operation Scenarios
- Derived Values Module
- Core Module Imports
- Detail Pages and Button Sorting
- Component Update and Validation
- Stored State Snapshot
- Service Rules Tests
- Utilities and Configuration
- Health Check Tests
- Migration Tests
- Workplan and Incident Rules
- Sub-Agent Team
- Project Instructions Overview
- Component Creation and Quick Swap
- Rewrite Roadmap Principles
- Code Review and Recalculation Tests
- Git Workflow Rules
- Workplan Details Helpers
- Project Conventions Rules
- Development Commands
- Handover Template
- Incident Link Migration
- Component Type Migration
- Database Expert Agent
- UX Designer Agent
- Stage 1 Handover Topics
- Service Record Processing
- Component Operation Characterisation
- Workplan Affected Columns Migration
- Stage Handover Documents
- Incident Report Helpers
- Database Migration Entry
- Service Integration Columns Migration
- Agent Handover Communication
- Fullstack Developer Agent
- Product Manager Agent
- Collection Refusal Tests
- Development Workflows
- Handovers Directory Guide
- Integrity Comparison Script
- Architect Agent
- Architecture Overview
- Collection and Bulk Updates
- Retire Before Service Validation
- Unknown History Record Validation
- Rewrite Stages
- History Notes Migration
- Component Type Time Migration
- Test Foundation and Fixtures
- Derived Values and Payloads
- Component Time Migration
- Service Workplan Link Migration
- Stage 1 Design Goals
- Rewrite Approaches Considered
- Docs Maintainer Agent
- Stage 1 Approach Decisions
- Table Sorting and Filtering
- History Edit Order Validation
- Workplan Name Migration
- Planned Service Helpers
- Bike Database Access
- Component Database Access
- History Edit Ordering Validation
- History Record Date Order
- Health Endpoint and Error Recorder
- Component Form Validation
- History Record Valid Input
- Quick Swap Without Bike
- Quick Swap Planned Service Guard
- Unknown Collection Validation
- Collection Unknown Component Check
- Collection Component Conflict Check
- Stage 1 Progress Log
- Config Update and Shutdown
- Bulk Status Change Modal
- Markdown Preview Editor
- Issue Tracking and Project
- Incident Table Filtering
- Quick Swap Form
- Container Creation Script
- Strava OAuth Token Setup
- Branching and Versioning
- Changelog and Project Board
- Component Type Usage Count
- Delete Operation Tests
- Workplans Overview Payload
- Recent Component Bike Lookup
- Filtered Log Reading
- Delete Refusal Tests
- Component Ride Matching
- Collection Reads
- Open Incident Reads
- Bike Table Reads
- Latest Service Record Read
- Planned Workplan Reads
- Services by Workplan
- Bike Component Subset Reads
- Installed Component Reads
- Workplans by Incident
- Component Distance Writes
- Component Service Status Writes
- Bike Service Status Writes
- Velo Supervisor Project
- Graphify Auto-Update
- Manual Onboarding Setup
- Q1 2025 Pilot Program
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
- Incident Record Writes
- Service Record Writes
- Component Object Reads
- Unknown Component History Validation
- History Record Writes
- Component Install Test
- Collection Multi-Bike Validation
- Unknown Service Validation
- Service Unknown Component Check
- Duplicate Planned Service Check
- Service Date Before Creation
- Service Date After Workplan
- Workplan Remaining Services Check
- Workplan Completion Date Format
- History Date Before Creation
- Workplan Completion Date Order
- History Date Before Latest
- Retirement Planned Service Guard
- Oldest Ride Date Lookup
- Component Uninstall Test
- Component Type Creation Test
- Development Notes
- Collection Record Writes
- Code Style Standards
- Bulk Ride Writes
- Planned Service Deletion Test
- Only History Record Deletion
- Incident Update Test
- Workplan Completion Test
- Collections ABC Module
- Integrity Scripts
- Test Configuration
- Test Fixtures
- Velo Supervisor Package

## God Nodes (most connected - your core abstractions)
1. `DatabaseManager` - 72 edges
2. `BusinessLogic` - 67 edges
3. `assert_matches_expected()` - 65 edges
4. `stored_state()` - 26 edges
5. `derived_values()` - 23 edges
6. `run_all_migrations()` - 22 edges
7. `Tests` - 21 edges
8. `Meta` - 20 edges
9. `_stored()` - 19 edges
10. `Task 2: Derived values` - 19 edges

## Surprising Connections (you probably didn't know these)
- `Task 1: Integrity package: loader, clock, recalculation, stored-state snapshot` --references--> `AppModules`  [INFERRED]
  docs/superpowers/plans/2026-11-16-stage-1-foundation.md → scripts/integrity/loader.py
- `Task 2: Derived values` --references--> `AppModules`  [INFERRED]
  docs/superpowers/plans/2026-11-16-stage-1-foundation.md → scripts/integrity/loader.py
- `Task 1: Integrity package: loader, clock, recalculation, stored-state snapshot` --references--> `load_app()`  [INFERRED]
  docs/superpowers/plans/2026-11-16-stage-1-foundation.md → scripts/integrity/loader.py
- `Task 3: Extract and compare CLIs, baseline against master` --references--> `load_app()`  [INFERRED]
  docs/superpowers/plans/2026-11-16-stage-1-foundation.md → scripts/integrity/loader.py
- `Task 4: Move to the src layout` --references--> `test_detect_layout_package()`  [INFERRED]
  docs/superpowers/plans/2026-11-16-stage-1-foundation.md → tests/integrity/test_loader.py

## Import Cycles
- None detected.

## Communities (183 total, 87 thin omitted)

### Community 0 - "Write Route Handlers"
Cohesion: 0.07
Nodes (39): fastapi_responses, fastapi_staticfiles, fastapi_templating, post, add_collection(), add_incident_record(), add_planned_services(), add_service() (+31 more)

### Community 1 - "App Lifespan and Scheduler"
Cohesion: 0.11
Nodes (19): apscheduler_schedulers_asyncio, apscheduler_triggers_cron, apscheduler_triggers_interval, FastAPI, lifespan(), Manage application startup and shutdown, Module for middleware, Initialize and start the APScheduler instance (+11 more)

### Community 2 - "Fake Strava OAuth Session"
Cohesion: 0.08
Nodes (36): Task 12: Strava sync, FakeOAuth2Session, FakeResponse, load_fixture(), new_session_class(), A stand-in for requests_oauthlib.OAuth2Session that answers from…, A FakeOAuth2Session subclass with its own empty call records, _errors() (+28 more)

### Community 3 - "README and Release Notes"
Cohesion: 0.29
Nodes (5): Strava OAuth scope incl. profile:read_all, Switched from pip to uv, v0.5.0 release (service integration, health check, uv), GitHub action writes current_version.txt on master, Manual testing protocols approach

### Community 4 - "Peewee ORM Models"
Cohesion: 0.10
Nodes (35): Model, peewee, Module for interaction with a Sqlite database, BaseModel, Bikes, Collections, ComponentHistory, Components (+27 more)

### Community 5 - "Frozen Clock Fixtures"
Cohesion: 0.16
Nodes (17): contextlib, os, frozen_clock(), Freeze time at FIXED_NOW in UTC so date-dependent calculations are reproducible, db_copy(), insert(), fixture, app() (+9 more)

### Community 6 - "Service and Collection Characterisation"
Cohesion: 0.06
Nodes (31): pytest, parametrize, Characterisation of service, incident, workplan and collection operations. Each…, svc-chain-2 moved from 2025-10-01 to 2025-11-01 08:00 and its description…, svc-wheel-planned completed through the edit form on 2026-11-01 08:00, keeping…, inc-drivetrain resolved through a partial update; only the given fields change, wp-drivetrain edited in full: named, later due date, size and description…, coll-mixed renamed and left with the rear wheel only, so it is healthy;… (+23 more)

### Community 7 - "Database Read Queries"
Cohesion: 0.04
Nodes (24): DatabaseManager, Method to sum distance for a given set of rides, Method to read and sort content of component_types table, Class to interact with a SQLite database through Peewee, Method to read a subset of records from the component history table, Method to retrieve the most recent record from the installation log of a given…, Method to retrieve the oldest record from the installation log of a given…, Method to read completed services for a component, used by health computation (+16 more)

### Community 8 - "Expected Result Assertions"
Cohesion: 0.12
Nodes (18): expected_dir(), fixture, test_difference_fails(), test_existing_file_is_never_overwritten(), test_missing_file_fails_naming_record_expected(), test_missing_file_is_recorded_when_asked(), hist-chain-gravel moved from 2025-08-01 to 2025-07-15 08:00, with a note.…, Cassette retired on 2026-10-01 08:00 and replaced by a new one created in the… (+10 more)

### Community 9 - "Exception Handling Middleware"
Cohesion: 0.16
Nodes (11): BaseHTTPMiddleware, Exception, exception_handler, http_exception_handler(), Function to catch http errors from Uvicorn and return them to the middleware, Middleware, Request, Class to handle exceptions that breaks the program and should be shown to the… (+3 more)

### Community 10 - "Component Status Recalculation"
Cohesion: 0.13
Nodes (11): Method to update component lifetime and service status when no installation…, Method to update status for a given bike based on component service and…, Method to calculate distance and bike id for history records, Method to compute component status using threshold logic, Method to determine worst-case status between distance and days-based…, Method to update time-based status fields for all non-retired components, Method to delete a given record and associated records, Method to refresh all bikes from Strava (+3 more)

### Community 12 - "Collection and Component Frontend"
Cohesion: 0.09
Nodes (9): editCollection(), handleUpdate(), initializeCollectionsSearch(), updateRowVisibility(), initializeComponentSelector(), NOTE: All collection details page handlers are in the "Functions used on…, IMPORTANT: Remove readonly - allow manual typing, showToast() (+1 more)

### Community 13 - "App Loader and Extractor"
Cohesion: 0.20
Nodes (14): pathlib, AppModules, detect_layout(), _forget_app_modules(), load_app(), Path, Tell the pre-restructure flat layout from the package layout, Import the application from a checkout bound to db_path. The application reads… (+6 more)

### Community 14 - "Docker Healthcheck Script"
Cohesion: 0.50
Nodes (3): Health check run by the Docker daemon, exit code 0 means healthy and 1 means…, urllib_error, urllib_request

### Community 15 - "Page Endpoints"
Cohesion: 0.11
Nodes (24): get, add_history_record(), collection_details(), component_overview(), component_types_overview(), help_page(), incident_reports(), Request (+16 more)

### Community 16 - "Snapshot Delta"
Cohesion: 0.25
Nodes (12): _leaves(), Every leaf path that differs between two snapshots, as {path: {"before": x,…, snapshot_delta(), test_added_and_removed_rows_list_every_leaf(), test_changed_value(), test_empty_dict_is_a_value(), test_key_with_slash_is_refused(), test_list_is_one_value() (+4 more)

### Community 17 - "Strava API Client"
Cohesion: 0.18
Nodes (9): Class to interact with Strava API, Method to authenticate and get data from Stravas gear API, Method to prepare a list of rides, Method to prepare a list of bikes, Method to read oauth options from file, Method to save oauth options to file, Method to authenticate and get data from Stravas activities API, Method to authenticate and get the full list of bike ids from the athlete's… (+1 more)

### Community 18 - "Single Record Reads"
Cohesion: 0.12
Nodes (8): Method to retrieve record for a single component type, Method to retrieve record for a specific entry in the installation log, Method to retrieve a specific service record, Method to retrieve record for a specific collection, Method to retrieve record for a specific incident report, Method to retrieve record for a specific workplan, Method to write component type record in database, Method to delete a given record and associated records

### Community 19 - "Migration Table Creation"
Cohesion: 0.14
Nodes (14): create_collections_table(), create_incidents_table(), create_workplans_table(), populate_component_types_thresholds(), populate_components_thresholds(), Creates the incidents table if it doesn't exist., Creates the workplans table if it doesn't exist., Creates the collections table if it doesn't exist. (+6 more)

### Community 20 - "Stage 1 Foundation Plan"
Cohesion: 0.07
Nodes (28): Global Constraints, Phase B: move, version, config, Docker, branch `feature/stage1-src-layout`, Phase C: tests, branch `feature/stage1-tests`, Phase D: template, CI, releases, cleanup, docs, branch `feature/stage1-finish`, Stage 1 Foundation Implementation Plan, Task 13: Page render tests, Task 15: Template database defaults, Task 16: CI made complete and permanent (+20 more)

### Community 21 - "Form Validation and Date Pickers"
Cohesion: 0.20
Nodes (9): initializeDatePickers(), initializeIncidentForm(), initializeWorkplanForm(), submitCollectionAjax(), submitComponentAjax(), validateCollectionStatusChange(), validateDateInput(), validateIncidentForm() (+1 more)

### Community 22 - "Extract and Compare CLIs"
Cohesion: 0.13
Nodes (16): dataclasses, Phase A: extractor and baseline, branch `feature/stage1-extractor`, Task 3: Extract and compare CLIs, baseline against master, extract(), main(), Path, Run one checkout against a copy of db_path and return its stored and derived…, Run the full recalculation chain and return one sorted line per failed call.… (+8 more)

### Community 23 - "Service and Workplan Creation"
Cohesion: 0.17
Nodes (10): Task 11: Operation scenarios: services, workplans, incidents, collections, Constraints, Method to create collection, Method to add service record, planned or completed, Method to add a planned service, which has no service date, bike or distance…, Method to create planned services for one or more components with the same…, Method to add incident record, Method to add workplan, optionally with planned services for components of a… (+2 more)

### Community 24 - "Create Operation Scenarios"
Cohesion: 0.11
Nodes (18): _new_ids(), An open incident on bike-gravel for the tire; empty optional fields become…, A planned workplan with a name; no services, so it reaches no bike or component, A workplan from inc-drivetrain with no component selection plans a service for…, Only the selected incident components get a planned service: the cassette, not…, A workplan from inc-squeal, whose only component is the retired pads: the…, Primary keys of table that are not in the dataset, in row order, A selection with none of inc-drivetrain's components plans nothing; the… (+10 more)

### Community 25 - "Derived Values Module"
Cohesion: 0.20
Nodes (26): _bike_values(), details(), _by_first(), _collection_values(), details(), status(), _component_values(), details() (+18 more)

### Community 27 - "Core Module Imports"
Cohesion: 0.36
Nodes (6): datetime, json, logging, requests_oauthlib, Module to handle business logic, Module to interact with Strava APIs

### Community 28 - "Detail Pages and Button Sorting"
Cohesion: 0.20
Nodes (10): bike_details(), component_details(), config_overview(), Endpoint for component details page, Endpoint for component types page, Endpoint for bike details page, get_button_order(), get_button_sorting_config() (+2 more)

### Community 29 - "Component Update and Validation"
Cohesion: 0.14
Nodes (12): Task 14: Rules, health and migration rewritten; old tests removed, Tests, Method to update component details, Method to update a component history record with validation, Method to validate history records before processing and storing in database, Method to validate quick swap operation, Method to validate collections before allowing bulk operations, Validate threshold configuration rules for component intervals (+4 more)

### Community 30 - "Stored State Snapshot"
Cohesion: 0.16
Nodes (22): Review Focus, Task 1: Integrity package: loader, clock, recalculation, stored-state snapshot, new_id_map(), normalise_new_ids(), _normalise_value(), Path, Read every table and column straight from SQLite, keyed table, primary key,…, Map each primary key absent from baseline_ids to new:<table>:<n>, numbered in… (+14 more)

### Community 31 - "Service Rules Tests"
Cohesion: 0.07
Nodes (26): parametrize, Service rules: planned services stay out of health, completion and revert,…, Reverting a completed service to planned leaves the component, its other…, Stored changes other than those to the removed service's own row, Uninstalling the cassette reprocesses its services; svc-cassette-2, its newest,…, Setup: a newer cassette service without workplan on 2026-11-01 08:00. Deleting…, The chain's planned service in wp-drivetrain does not block one outside any…, svc-pads-retired cannot be reverted to planned, since its component is retired (+18 more)

### Community 32 - "Utilities and Configuration"
Cohesion: 0.13
Nodes (18): asyncio, collections, Configuration file location, re, config_path(), generate_workplan_title(), parse_button_sorting(), Module for auxiliary functions (+10 more)

### Community 33 - "Health Check Tests"
Cohesion: 0.11
Nodes (15): database(), logger(), fixture, The health rule: an error logged in the last 24 hours, a failing database or a…, SQLite creates an empty file for a wrong path, e.g. a missing Docker mount, An error logged anywhere reaches the recorder through the root logger, lifespan in main.py sets every root handler to INFO or DEBUG at startup, The recalculation of the dataset logs no error, so the fixture starts healthy (+7 more)

### Community 34 - "Migration Tests"
Cohesion: 0.18
Nodes (18): build_dataset(), Path, Write the dataset into a migrated copy of the template database at db_path, columns(), description(), old_db(), fixture, query() (+10 more)

### Community 35 - "Workplan and Incident Rules"
Cohesion: 0.09
Nodes (21): Workplan, incident and history rules: links through services, titles, notes,…, wp-brake-check set back to Planned with a full update; completion rules apply…, Components, bikes, progress and title of a workplan come from its services. A…, The chain has svc-chain-planned: retiring is refused and changes nothing,…, inc-drivetrain reaches wp-drivetrain through its two services, one planned and…, The values the workplan, bike, component and collection pages show for planned…, A note is stored on the new record; a note of only spaces is stored as NULL, on…, The cassette retired and replaced by a new one: both new history records carry… (+13 more)

### Community 36 - "Sub-Agent Team"
Cohesion: 0.67
Nodes (3): Available Agents, Direct Invocation, Sub-Agent Team

### Community 37 - "Project Instructions Overview"
Cohesion: 0.22
Nodes (8): Before Creating Handover, Communication & Output Rules, Debugging & Bug Fixing Rules, For fullstack-developer, graphify, Important Notes, Project Overview, Testing Requirements

### Community 38 - "Component Creation and Quick Swap"
Cohesion: 0.20
Nodes (8): Task 10: Operation scenarios: components, history, quick swap, types, config, Result extractor, Method to create component, Method to create installation history record, Method to orchestrate swap of one component with another, Method to check if a bike has all mandatory components and respects max…, Method to update only the count of components for a given component type, Method to produce payload for page bike overview

### Community 39 - "Rewrite Roadmap Principles"
Cohesion: 0.20
Nodes (10): Anti-goals, Branch policy during the freeze, Constraints, Goals, Issue map, Left to each stage, Non-goals, Rewrite roadmap: new UI, restructured backend, exposed API (+2 more)

### Community 40 - "Code Review and Recalculation Tests"
Cohesion: 0.05
Nodes (66): Issues Found, Key Checks, Output Format, Recommendations, Review Philosophy, Review Process, Summary, Task 9: Recalculation characterisation (+58 more)

### Community 41 - "Git Workflow Rules"
Cohesion: 0.29
Nodes (7): Branch Strategy, Commit Process, For All Agents, For code-reviewer, For docs-maintainer, For fullstack-developer, Git Workflow Rules

### Community 42 - "Workplan Details Helpers"
Cohesion: 0.21
Nodes (13): Method to produce payload for workplan details page, calculate_elapsed_days(), derive_workplan_context(), get_formatted_datetime_now(), get_workplan_data_tuple(), get_workplan_names_dict(), Function to get current datetime formatted as YYYY-MM-DD HH:MM, Derive bike, component and progress information for a workplan from its services (+5 more)

### Community 43 - "Project Conventions Rules"
Cohesion: 0.22
Nodes (8): Change Management Rules, Debugging & bug fixing rules (root cause first), Docker HEALTHCHECK against /health, graphify knowledge graph usage rules, Agent handover documents (.handovers/), Log levels drive container health, Technical debt tracked in issue #356, TomSelect multi-select pattern

### Community 44 - "Development Commands"
Cohesion: 0.40
Nodes (5): Database Operations, Dependencies, Development Commands, Running the Application, Testing

### Community 45 - "Handover Template"
Cohesion: 0.25
Nodes (7): Blockers / Open Questions, Context, Decisions Made, Deliverables, Next Steps for [Target Agent], References, [Source Agent] -> [Target Agent] Handover

### Community 46 - "Incident Link Migration"
Cohesion: 0.25
Nodes (8): check_incidents_workplan_column_present(), insert_planned_service_for_migration(), migrate_drop_incident_workplan_column(), migrate_incident_links_to_services(), Check if incidents table still has the workplan_id column, Insert a planned service with no date, bike or distance. Returns False if the…, Rebuild incident to workplan links through services, Rebuild incidents table without the workplan_id column

### Community 47 - "Component Type Migration"
Cohesion: 0.32
Nodes (7): check_component_types_columns(), count_component_types_in_use(), migrate_component_types(), Check if the component_types table needs migration, Migrate the component_types table to add new columns, Script to migrate the database, including adding new tables and fields, Count how many components use a specific component type

### Community 48 - "Database Expert Agent"
Cohesion: 0.29
Nodes (6): Constraints, Core Responsibilities, Pattern Consistency - CRITICAL, Query Optimization, Schema Changes, Workflow

### Community 49 - "UX Designer Agent"
Cohesion: 0.29
Nodes (6): Core Responsibilities, Design Principles, Specifications to Include, v1 (Before Architect), v2 (After Architect), Workflow

### Community 50 - "Stage 1 Handover Topics"
Cohesion: 0.17
Nodes (12): CI, Comparison against master, Decided, Docker, Legacy files removed, Release notes backfill and README cleanup, Stage handover, Target layout (+4 more)

### Community 51 - "Service Record Processing"
Cohesion: 0.20
Nodes (6): Method to build the report used by the plan services and complete services…, Method to complete planned services with one service date, keeping their…, Method to update a service record, including status changes in both directions, Method to recalculate a component after a completed service is deleted or…, Method to validate service records before processing and storing in database, Method to calculate distance and bike id for service records

### Community 52 - "Component Operation Characterisation"
Cohesion: 0.07
Nodes (30): _assert_new_component(), Characterisation of component, history, quick swap, component type, delete and…, Changing the type recounts both types: Saddle in_use 0, Bottle cage 1. Spare…, Bremseklosser bak æøå retired on bike-gravel 2026-10-01 08:00. Marker: gravel…, Chain swapped for a spare chain on 2026-10-01 08:00; the old chain becomes not…, Chain type intervals change; existing chains keep their own (3000 km, 500 km);…, Deleting the chain's latest record (road_2) leaves it as uninstalled from bike-…, Records current behaviour; see #374. Deleting a component's only history record… (+22 more)

### Community 53 - "Workplan Affected Columns Migration"
Cohesion: 0.25
Nodes (8): check_workplans_affected_columns(), migrate_drop_workplan_affected_columns(), migrate_workplans_to_planned_services(), Check if workplans table still has the affected bike/component columns, Resolve bike and component names, marking components that no longer exist, Convert affected components on planned workplans into planned services,…, Rebuild workplans table without the affected bike/component columns, read_names_for_migration()

### Community 54 - "Stage Handover Documents"
Cohesion: 0.20
Nodes (7): Blockers / Open Questions, Context, Deliverables, Next Steps, References, Stage 1 Foundation Handover, Switch-over steps for the Pi (Stage 6)

### Community 55 - "Incident Report Helpers"
Cohesion: 0.24
Nodes (9): Method to produce payload for page incident reports, generate_incident_title(), get_incident_data_tuple(), get_service_incident_options(), parse_json_string(), Build standard incident data tuple for display (17 fields), Build incident options for the service modal (4 fields), all incidents so…, Function to load a JSON string and return the parsed data as a python object (+1 more)

### Community 56 - "Database Migration Entry"
Cohesion: 0.33
Nodes (6): find_database_file(), migrate_database(), prompt_for_db_path(), Search for a database file in the user's home directory and subdirectories, Prompt user for database path or filename and verify it exists, Main function to handle the database migration.

### Community 57 - "Service Integration Columns Migration"
Cohesion: 0.25
Nodes (8): check_incidents_workplan_column(), check_services_integration_columns(), migrate_incidents_workplan_link(), migrate_services_integration_columns(), Check if Incidents table needs workplan_id column, Add workplan_id column to Incidents table for workplan hub integration, Check which service integration columns are missing on the services table, Add status, incident_id and planned_date to services, mark existing rows…

### Community 58 - "Agent Handover Communication"
Cohesion: 0.33
Nodes (6): Agent Communication via Handovers, Creating Handovers, Detailed Instructions, Handover Structure, Naming Convention, Reading Handovers

### Community 59 - "Fullstack Developer Agent"
Cohesion: 0.33
Nodes (5): Backend Patterns, Core Responsibilities, Frontend Patterns, Handover Content, Workflow

### Community 60 - "Product Manager Agent"
Cohesion: 0.33
Nodes (5): Boundaries, Core Responsibilities, Key Principle: You Are Interactive, Requirements Document, User Story Format

### Community 61 - "Collection Refusal Tests"
Cohesion: 0.25
Nodes (8): assert_refused_after_setup(), The refusal returns expected and adds nothing to the delta the setup left, Setup: coll-mixed reduced to the retired pads with update_collection, which…, Setup: coll-mixed reduced to the rear wheel, which has svc-wheel-planned.…, Not a validate_collection branch: change_collection_status refuses before…, test_change_collection_status_refuses_empty_collection(), test_validate_collection_refuses_retired_member(), test_validate_collection_refuses_retiring_with_planned_services()

### Community 62 - "Development Workflows"
Cohesion: 0.50
Nodes (4): For Bug Fixes, For Documentation Updates, For New Features, Standard Development Workflow

### Community 63 - "Handovers Directory Guide"
Cohesion: 0.33
Nodes (5): Creating Handovers, Directory Structure, Finding Handovers, Handovers Directory, Rules

### Community 64 - "Integrity Comparison Script"
Cohesion: 0.18
Nodes (17): argparse, diff(), _error_paths(), main(), present_on_both_sides(), Path, One line per difference as 'path: left=... right=...', paths joined with '/, Recalculation failures and derived error entries that appear identically on… (+9 more)

### Community 65 - "Architect Agent"
Cohesion: 0.40
Nodes (4): Core Responsibilities, Handover Content, Principles, Workflow

### Community 66 - "Architecture Overview"
Cohesion: 0.40
Nodes (5): Architecture Overview, Configuration, Core Components, Key Features, Project Structure

### Community 67 - "Collection and Bulk Updates"
Cohesion: 0.11
Nodes (12): BusinessLogic, Method to update collection, Method to change status of all components in a collection, Method to update incident record (supports full or partial updates), Method to update workplan (supports full or partial updates), Function to set the date for last pull from Strava, Method to check the database connection for the health check, Class that contains business logic (+4 more)

### Community 70 - "Rewrite Stages"
Cohesion: 0.29
Nodes (7): Stage 1: Foundation, Stage 2: Design, Stage 3: Architecture, Stage 4: Backend refactor, Stage 5: New frontend and features, Stage 6: Switch-over, Stages

### Community 71 - "History Notes Migration"
Cohesion: 0.50
Nodes (4): check_component_history_notes_column(), migrate_component_history_notes(), Check if component_history table needs notes column, Add notes column to component_history table

### Community 72 - "Component Type Time Migration"
Cohesion: 0.50
Nodes (4): check_component_types_time_columns(), migrate_component_types_time_fields(), Check if ComponentTypes table needs time-based fields migration, Add time-based fields to ComponentTypes table

### Community 73 - "Test Foundation and Fixtures"
Cohesion: 0.13
Nodes (25): Task 8: Test foundation and synthetic dataset, fastapi_testclient, Decisions Made, importlib, test_dataset_builds_and_recalculates(), app(), client(), clock() (+17 more)

### Community 74 - "Derived Values and Payloads"
Cohesion: 0.10
Nodes (20): Task 2: Derived values, Method to produce payload for page component overview, Method to produce payload for page component details, Method to determine which factor triggered a warning status, Calculate lifetime and service triggers for a component, Method to create component-to-collection mapping dictionaries, Method to produce payload for displaying table of all collections, Method to build dictionaries of bike and component ids referenced in received… (+12 more)

### Community 75 - "Component Time Migration"
Cohesion: 0.50
Nodes (4): check_components_time_columns(), migrate_components_time_fields(), Check if Components table needs time-based fields migration, Add time-based fields to Components table and populate threshold_km

### Community 76 - "Service Workplan Link Migration"
Cohesion: 0.50
Nodes (4): check_services_workplan_column(), migrate_services_workplan_link(), Check if Services table needs workplan_id column, Add workplan_id column to Services table for workplan hub integration

### Community 77 - "Stage 1 Design Goals"
Cohesion: 0.29
Nodes (7): Anti-goals, Done when, Goals, Intent, Left to the builder, Non-goals, Stage 1: Foundation

### Community 78 - "Rewrite Approaches Considered"
Cohesion: 0.33
Nodes (6): API: separate API, or one set of resources with two formats, API style: FHIR-conformant or FHIR-inspired, Approaches considered, Delivery: side by side on master, or frozen master and long-running dev, Frontend: server-rendered with htmx, or a JSON API with a separate frontend app, Provenance actor: named user or source of change

### Community 79 - "Docs Maintainer Agent"
Cohesion: 0.50
Nodes (3): Core Responsibilities, Documentation Rules, Workflow

### Community 81 - "Stage 1 Approach Decisions"
Cohesion: 0.33
Nodes (6): Approaches, Fixed clock, Order of work, Release mechanism, Synthetic dataset, Version source

### Community 82 - "Table Sorting and Filtering"
Cohesion: 0.29
Nodes (8): initializeCollectionsSorting(), sortColumn(), initializeWorkplanTable(), setupIncidentTableSorting(), setupWorkplanSearch(), setupWorkplanStatusFiltering(), setupWorkplanTableSorting(), updateWorkplansVisibility()

### Community 84 - "Workplan Name Migration"
Cohesion: 0.50
Nodes (4): check_workplans_name_column(), migrate_workplans_name_column(), Check if workplans table needs the workplan_name column, Add the optional user given name to the workplans table, existing workplans…

### Community 85 - "Planned Service Helpers"
Cohesion: 0.33
Nodes (6): build_incident_service_entry(), get_effective_planned_date(), get_planned_service_data_tuple(), Return the service's own planned date, else the workplan due date, else None, Describe one service linked to an incident, for the read only list in the…, Build standard planned service tuple for display (11 fields)

### Community 87 - "Bike Database Access"
Cohesion: 0.33
Nodes (3): Method to retrieve record for a specific bike, Method to create or update bike data to the database, Method to get the name of a bike based on bike id

### Community 88 - "Component Database Access"
Cohesion: 0.33
Nodes (3): Method to get component names based on list of ids, Method to retrieve record for a specific component, Method to create or update component data to the database

### Community 91 - "Health Endpoint and Error Recorder"
Cohesion: 0.18
Nodes (8): health(), Endpoint for the Docker health check, returns 503 if errors were logged the…, ErrorRecorder, get_health_status(), Logging handler that keeps the most recent error records in memory for the…, Method to store error records and ignore lower levels. Filters here instead of…, Method to get error records newer than the given number of hours, Function to assess application health from errors logged the last 24 hours and…

### Community 92 - "Component Form Validation"
Cohesion: 0.40
Nodes (5): addFormValidation(), clearValidationErrors(), showFieldError(), validateComponentThresholds(), validateQuickSwapForm()

### Community 99 - "Stage 1 Progress Log"
Cohesion: 0.40
Nodes (5): End of Phase B (after Tasks 5-7: version from git tag, config from `VELO_SUPERVISOR_CONFIG`, new Docker image), Progress log, Task 3, step 5: failing-comparison proof, Task 3, step 6: baseline dev vs master, Task 4, step 9: src layout vs master

### Community 101 - "Config Update and Shutdown"
Cohesion: 0.50
Nodes (4): Endpoint to update config file based on which form was submitted, update_config(), Helper function to shutdown the server after a short delay, shutdown_server()

### Community 102 - "Bulk Status Change Modal"
Cohesion: 0.50
Nodes (4): cleanup(), handleCancel(), handleConfirm(), performBulkStatusChange()

### Community 103 - "Markdown Preview Editor"
Cohesion: 0.50
Nodes (4): containsMarkdown(), renderPreview(), setInitialMode(), updateCheckboxInText()

### Community 105 - "Incident Table Filtering"
Cohesion: 0.67
Nodes (4): initializeIncidentTable(), setupIncidentSearch(), setupIncidentStatusFiltering(), updateIncidentVisibility()

### Community 106 - "Quick Swap Form"
Cohesion: 0.67
Nodes (3): filterNewComponentsByType(), handleOldComponentChange(), updateQuickSwapCollectionWarning()

### Community 112 - "Delete Operation Tests"
Cohesion: 0.40
Nodes (5): _execute(), Setup: coll-gravel-set emptied in the database, since only an empty collection…, Setup: svc-pads-retired unlinked from wp-brake-check in the database, since…, test_delete_collection(), test_delete_workplan()

### Community 113 - "Workplans Overview Payload"
Cohesion: 0.50
Nodes (3): Method to produce payload for page of all workplans, get_formatted_bikes_list(), Function to get list of all bikes, with prefix for retired bikes

### Community 115 - "Filtered Log Reading"
Cohesion: 0.50
Nodes (4): get_filtered_log(), Endpoint to read log and return only business events, Function to get filtered log records, read_filtered_logs()

### Community 116 - "Delete Refusal Tests"
Cohesion: 0.67
Nodes (3): parametrize, Each guard of delete_record refuses on the dataset as it is and leaves every…, test_delete_refusal_changes_nothing()

### Community 170 - "Development Notes"
Cohesion: 0.40
Nodes (5): Database Schema Changes, Development Notes, Docker Development, Logging, Technical Debt

### Community 172 - "Code Style Standards"
Cohesion: 0.50
Nodes (4): Code Style & Standards, Database, Frontend, Python (Backend)

## Ambiguous Edges - Review These
- `tests/conftest.py` → `Manual testing protocols approach`  [AMBIGUOUS]
  tests/README.md · relation: conceptually_related_to

## Knowledge Gaps
- **165 isolated node(s):** `DatasetIds`, `GitHub Issues Tracker`, `Velo Supervisor 2000 (Project)`, `Strava OAuth Token Setup (Step 2)`, `Semantic Versioning (SemVer)` (+160 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 746 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **87 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `tests/conftest.py` and `Manual testing protocols approach`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **Why does `DatabaseManager` connect `Database Read Queries` to `Component Service Status Writes`, `Bike Service Status Writes`, `Peewee ORM Models`, `Single Record Reads`, `Incident Record Writes`, `Service Record Writes`, `Component Object Reads`, `History Record Writes`, `Core Module Imports`, `Health Check Tests`, `Oldest Ride Date Lookup`, `Collection Record Writes`, `Bulk Ride Writes`, `Derived Values and Payloads`, `Bike Database Access`, `Component Database Access`, `Component Type Usage Count`, `Recent Component Bike Lookup`, `Component Ride Matching`, `Collection Reads`, `Open Incident Reads`, `Bike Table Reads`, `Latest Service Record Read`, `Planned Workplan Reads`, `Services by Workplan`, `Bike Component Subset Reads`, `Installed Component Reads`, `Workplans by Incident`, `Component Distance Writes`?**
  _High betweenness centrality (0.135) - this node is a cross-community bridge._
- **Why does `BusinessLogic` connect `Collection and Bulk Updates` to `Write Route Handlers`, `App Lifespan and Scheduler`, `Component Creation and Quick Swap`, `Component Status Recalculation`, `Derived Values and Payloads`, `Workplan Details Helpers`, `Workplans Overview Payload`, `Service Record Processing`, `Incident Report Helpers`, `Service and Workplan Creation`, `Core Module Imports`, `Component Update and Validation`?**
  _High betweenness centrality (0.088) - this node is a cross-community bridge._
- **Why does `assert_matches_expected()` connect `Expected Result Assertions` to `Fake Strava OAuth Session`, `Service and Collection Characterisation`, `Component Uninstall Test`, `Component Type Creation Test`, `Code Review and Recalculation Tests`, `Test Foundation and Fixtures`, `Planned Service Deletion Test`, `Only History Record Deletion`, `Delete Operation Tests`, `Workplan Completion Test`, `Incident Update Test`, `Component Operation Characterisation`, `Extract and Compare CLIs`, `Create Operation Scenarios`, `Component Install Test`?**
  _High betweenness centrality (0.046) - this node is a cross-community bridge._
- **Are the 9 inferred relationships involving `DatabaseManager` (e.g. with `Bikes` and `Collections`) actually correct?**
  _`DatabaseManager` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `derived_values()` (e.g. with `Task 2: Derived values` and `bike_overview()`) actually correct?**
  _`derived_values()` has 5 INFERRED edges - model-reasoned connections that need verification._
- **What connects `DatasetIds`, `GitHub Issues Tracker`, `Velo Supervisor 2000 (Project)` to the rest of the system?**
  _165 weakly-connected nodes found - possible documentation gaps or missing edges._