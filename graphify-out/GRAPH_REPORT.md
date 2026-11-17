# Graph Report - velo-supervisor-2000  (2026-11-17)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 1477 nodes · 2502 edges · 173 communities (90 shown, 83 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 186 edges (avg confidence: 0.94)
- Token cost: 82,804 input · 2,455 output

## Graph Freshness
- Built from commit: `c8ceb622`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- FastAPI POST Routes
- App Startup and Scheduler
- Fake Strava OAuth
- Release Notes and README
- Peewee Database Models
- Frozen Clock and Derived Tests
- Service and Workplan Characterisation
- Database Read Queries
- Expected-Result Assertions
- Component Creation Tests
- Component Status Recalculation
- Validation Refusal Tests
- Frontend Forms and Tables
- Integrity App Loader
- Docker Healthcheck Script
- FastAPI GET Page Routes
- Snapshot Delta Comparison
- Middleware and Exception Handling
- Single Record Reads
- Table Creation Migrations
- Page Render Tests
- Form Validation and Submission
- Dataset Serialisation Tests
- Service and Incident Creation
- Record Creation Scenarios
- Derived Values Extraction
- Synthetic Dataset Builder
- Strava Ride Updates
- Component and History Operations
- Database Snapshot Extraction
- Service Rules Tests
- Utility Functions
- Health Check Tests
- Src Layout, Version, Config
- Workplan and Incident Rules
- Sub-Agent Team
- Project Guidance Overview
- Bike Overview and Triggers
- Rewrite Roadmap
- Code Review and Recalculation
- Git Workflow Rules
- Health Endpoint
- Project Conventions Summary
- Development Commands
- Handover Template
- Incident-Service Link Migration
- Component Types Migration
- Database Expert Agent
- UX Designer Agent
- Stage 1 Decisions
- Service Completion and Updates
- Component Operation Characterisation
- Workplan Planned Services Migration
- Stage 1 Handover
- Refusal Leaves State Unchanged
- Migration Database Discovery
- Service Integration Column Migrations
- Handover Communication
- Fullstack Developer Agent
- Product Manager Agent
- Collection Refusal Tests
- Development Workflow
- Handovers Directory Guide
- Stage 1 Implementation Plan
- Architect Agent
- Architecture Overview
- Collection and Record Updates
- Retire Before Service Test
- Unknown History Record Test
- Rewrite Stages
- History Notes Migration
- Component Type Time Migration
- Test Fixtures and Dataset
- Business Logic Page Payloads
- Component Time Migration
- Service Workplan Link Migration
- Stage Design Specs
- Rewrite Approach Options
- Docs Maintainer Agent
- Stage 1 Approaches
- Table Sorting and Filtering
- Edit Before Previous Test
- Workplan Name Migration
- Database Connection Check
- Bike Record Access
- Component Record Access
- Edit After Next Test
- First Record Order Test
- Error Recorder Logging
- Form Field Validation
- History Record Accept Test
- Quick Swap Without Bike
- Quick Swap Planned Service
- Collection Unknown Validation
- Collection Unknown Component Check
- Collection Cross-Membership Check
- Read All Workplans
- Incidents By Workplan Query
- Bulk Status Confirmation
- Markdown Preview Rendering
- Issue Tracking and Project
- Incident Table Filtering
- Quick Swap Selection
- Container Creation Script
- Strava OAuth Token Setup
- Branching and Versioning
- Changelog and Project Board
- Component Type Usage Count
- Latest History Record Lookup
- Planned Services By Bike
- Recent Component Bike Lookup
- Filtered Log Endpoint
- Component Service History Subset
- Component Matching Rides
- Component Lifetime Status Write
- Open Incidents Query
- Workplan Write
- Component Type Update Test
- Services By Workplan Query
- Component Distance Write
- Component Service Status Write
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
- Incident Record Write
- Service Record Write
- Read All Component Objects
- History Unknown Component Validation
- Component Installation Test
- Collection Multi-Bike Validation
- Unknown Service Validation
- Service Unknown Component Validation
- Duplicate Planned Service Validation
- Service Date Before Creation
- Service Date After Workplan
- Workplan Remaining Services Validation
- Workplan Date Format Validation
- History Date Before Creation
- Workplan Completion Date Validation
- History Date Before Latest
- Retirement With Planned Services
- Oldest Ride Date Lookup
- Component Type Creation Test
- Development Notes
- Collection Write
- Code Style Standards
- Bulk Ride Write
- Delete Only History Record
- Collections ABC Import
- Integrity Module
- Test Conftest
- Test Fixtures
- Velo Supervisor Package

## God Nodes (most connected - your core abstractions)
1. `DatabaseManager` - 72 edges
2. `BusinessLogic` - 67 edges
3. `assert_matches_expected()` - 65 edges
4. `stored_state()` - 28 edges
5. `derived_values()` - 23 edges
6. `run_all_migrations()` - 22 edges
7. `Tests` - 21 edges
8. `Meta` - 20 edges
9. `_stored()` - 19 edges
10. `Task 2: Derived values` - 19 edges

## Surprising Connections (you probably didn't know these)
- `Blockers / Open Questions` --references--> `stored_state()`  [INFERRED]
  .handovers/stages/stage-1-foundation-handover.md → scripts/integrity/snapshot.py
- `Next Steps` --references--> `stored_state()`  [INFERRED]
  .handovers/stages/stage-1-foundation-handover.md → scripts/integrity/snapshot.py
- `Configuration file location` --references--> `read_config()`  [INFERRED]
  docs/superpowers/specs/2026-11-16-stage-1-foundation-design.md → src/velo_supervisor/utils.py
- `Task 1: Integrity package: loader, clock, recalculation, stored-state snapshot` --references--> `AppModules`  [INFERRED]
  docs/superpowers/plans/2026-11-16-stage-1-foundation.md → scripts/integrity/loader.py
- `Task 2: Derived values` --references--> `AppModules`  [INFERRED]
  docs/superpowers/plans/2026-11-16-stage-1-foundation.md → scripts/integrity/loader.py

## Import Cycles
- None detected.

## Communities (173 total, 83 thin omitted)

### Community 0 - "FastAPI POST Routes"
Cohesion: 0.06
Nodes (43): fastapi_responses, fastapi_staticfiles, fastapi_templating, post, add_collection(), add_incident_record(), add_planned_services(), add_service() (+35 more)

### Community 1 - "App Startup and Scheduler"
Cohesion: 0.09
Nodes (23): apscheduler_schedulers_asyncio, apscheduler_triggers_cron, apscheduler_triggers_interval, datetime, FastAPI, logging, requests_oauthlib, lifespan() (+15 more)

### Community 2 - "Fake Strava OAuth"
Cohesion: 0.08
Nodes (36): Task 12: Strava sync, FakeOAuth2Session, FakeResponse, load_fixture(), new_session_class(), A stand-in for requests_oauthlib.OAuth2Session that answers from…, A FakeOAuth2Session subclass with its own empty call records, _errors() (+28 more)

### Community 3 - "Release Notes and README"
Cohesion: 0.29
Nodes (5): Strava OAuth scope incl. profile:read_all, Switched from pip to uv, v0.5.0 release (service integration, health check, uv), GitHub action writes current_version.txt on master, Manual testing protocols approach

### Community 4 - "Peewee Database Models"
Cohesion: 0.10
Nodes (35): Model, peewee, Module for interaction with a Sqlite database, BaseModel, Bikes, Collections, ComponentHistory, Components (+27 more)

### Community 5 - "Frozen Clock and Derived Tests"
Cohesion: 0.19
Nodes (17): Review Focus, Task 1: Integrity package: loader, clock, recalculation, stored-state snapshot, frozen_clock(), Freeze time at FIXED_NOW in UTC so date-dependent calculations are reproducible, insert(), app(), fixture, test_dangling_collection_is_recorded_not_raised() (+9 more)

### Community 6 - "Service and Workplan Characterisation"
Cohesion: 0.06
Nodes (33): Characterisation of service, incident, workplan and collection operations. Each…, svc-chain-2 moved from 2025-10-01 to 2025-11-01 08:00 and its description…, svc-chain-2 reverted to planned for 2026-12-01 10:00: date, bike and marker are…, svc-wheel-planned completed through the edit form on 2026-11-01 08:00, keeping…, inc-drivetrain edited in full: severity Monitor, the cassette removed, a new…, inc-drivetrain resolved through a partial update; only the given fields change, wp-drivetrain edited in full: named, later due date, size and description…, wp-drivetrain completed on 2026-11-02 10:00 as the completion modal sends it,… (+25 more)

### Community 7 - "Database Read Queries"
Cohesion: 0.04
Nodes (24): DatabaseManager, Method to sum distance for a given set of rides, Method to read and sort content of component_types table, Method to read components for a specific bike, Class to interact with a SQLite database through Peewee, Method to read installed components for a specific bike, Method to read a subset of records from the component history table, Method to retrieve the oldest record from the installation log of a given… (+16 more)

### Community 8 - "Expected-Result Assertions"
Cohesion: 0.12
Nodes (18): expected_dir(), fixture, test_difference_fails(), test_existing_file_is_never_overwritten(), test_missing_file_fails_naming_record_expected(), test_missing_file_is_recorded_when_asked(), Chain uninstalled from bike-road 2026-10-01 08:00. New record marker: 440 +…, Cassette retired on 2026-10-01 08:00 and replaced by a new one created in the… (+10 more)

### Community 9 - "Component Creation Tests"
Cohesion: 0.29
Nodes (7): _assert_new_component(), Chain swapped for a spare chain on 2026-10-01 08:00; the old chain becomes not…, An installed component gets a history record and is recalculated at once. Road…, A component created as not installed gets no history; the alternate method sets…, test_create_installed_component(), test_create_not_installed_component(), test_quick_swap_to_not_installed_with_existing_component()

### Community 10 - "Component Status Recalculation"
Cohesion: 0.13
Nodes (13): Comparison against master (production copy, recalculation + derived values), Method to update component lifetime and service status when no installation…, Method to update status for a given bike based on component service and…, Method to calculate distance and bike id for history records, Method to recalculate a component after a completed service is deleted or…, Method to calculate distance and bike id for service records, Method to compute component status using threshold logic, Method to determine worst-case status between distance and days-based… (+5 more)

### Community 12 - "Frontend Forms and Tables"
Cohesion: 0.09
Nodes (9): editCollection(), handleUpdate(), initializeCollectionsSearch(), updateRowVisibility(), initializeComponentSelector(), NOTE: All collection details page handlers are in the "Functions used on…, IMPORTANT: Remove readonly - allow manual typing, showToast() (+1 more)

### Community 13 - "Integrity App Loader"
Cohesion: 0.16
Nodes (18): contextlib, os, pathlib, pytest, AppModules, detect_layout(), _forget_app_modules(), load_app() (+10 more)

### Community 14 - "Docker Healthcheck Script"
Cohesion: 0.50
Nodes (3): Health check run by the Docker daemon, exit code 0 means healthy and 1 means…, urllib_error, urllib_request

### Community 15 - "FastAPI GET Page Routes"
Cohesion: 0.08
Nodes (34): get, add_history_record(), bike_details(), collection_details(), component_details(), component_overview(), component_types_overview(), config_overview() (+26 more)

### Community 16 - "Snapshot Delta Comparison"
Cohesion: 0.25
Nodes (12): _leaves(), Every leaf path that differs between two snapshots, as {path: {"before": x,…, snapshot_delta(), test_added_and_removed_rows_list_every_leaf(), test_changed_value(), test_empty_dict_is_a_value(), test_key_with_slash_is_refused(), test_list_is_one_value() (+4 more)

### Community 17 - "Middleware and Exception Handling"
Cohesion: 0.08
Nodes (22): BaseHTTPMiddleware, Exception, exception_handler, Coverage (289 tests, total 80%), Method to read workplans reached through the services of a given incident, http_exception_handler(), Function to catch http errors from Uvicorn and return them to the middleware, Middleware (+14 more)

### Community 18 - "Single Record Reads"
Cohesion: 0.12
Nodes (8): Method to retrieve record for a single component type, Method to retrieve record for a specific entry in the installation log, Method to retrieve a specific service record, Method to retrieve record for a specific collection, Method to retrieve record for a specific incident report, Method to retrieve record for a specific workplan, Method to write component type record in database, Method to delete a given record and associated records

### Community 19 - "Table Creation Migrations"
Cohesion: 0.14
Nodes (14): create_collections_table(), create_incidents_table(), create_workplans_table(), populate_component_types_thresholds(), populate_components_thresholds(), Creates the incidents table if it doesn't exist., Creates the workplans table if it doesn't exist., Creates the collections table if it doesn't exist. (+6 more)

### Community 20 - "Page Render Tests"
Cohesion: 0.28
Nodes (7): Task 13: Page render tests, parametrize, Every page renders for every resource in the dataset, and unknown IDs fail the…, Stage 4 changes the unknown-ID status to 404 (#356), test_every_detail_page_renders(), test_every_overview_page_renders(), test_unknown_ids_today()

### Community 21 - "Form Validation and Submission"
Cohesion: 0.20
Nodes (9): initializeDatePickers(), initializeIncidentForm(), initializeWorkplanForm(), submitCollectionAjax(), submitComponentAjax(), validateCollectionStatusChange(), validateDateInput(), validateIncidentForm() (+1 more)

### Community 22 - "Dataset Serialisation Tests"
Cohesion: 0.22
Nodes (8): dataclasses, dumps(), Serialise a state deterministically, keeping non-ASCII characters readable, test_new_ids_are_normalised_in_both_layers(), test_only_the_component_without_history_fails_recalculation(), test_read_functions_raise_no_errors_on_the_dataset(), test_derived_is_json_serialisable(), test_no_source_errors()

### Community 23 - "Service and Incident Creation"
Cohesion: 0.19
Nodes (9): Task 11: Operation scenarios: services, workplans, incidents, collections, Method to create collection, Method to add service record, planned or completed, Method to add a planned service, which has no service date, bike or distance…, Method to create planned services for one or more components with the same…, Method to add incident record, Method to add workplan, optionally with planned services for components of a…, generate_unique_id() (+1 more)

### Community 24 - "Record Creation Scenarios"
Cohesion: 0.11
Nodes (18): _new_ids(), An open incident on bike-gravel for the tire; empty optional fields become…, A planned workplan with a name; no services, so it reaches no bike or component, A workplan from inc-drivetrain with no component selection plans a service for…, Only the selected incident components get a planned service: the cassette, not…, A workplan from inc-squeal, whose only component is the retired pads: the…, Primary keys of table that are not in the dataset, in row order, A selection with none of inc-drivetrain's components plans nothing; the… (+10 more)

### Community 25 - "Derived Values Extraction"
Cohesion: 0.17
Nodes (28): _bike_values(), details(), _by_first(), _collection_values(), details(), status(), _component_values(), details() (+20 more)

### Community 27 - "Synthetic Dataset Builder"
Cohesion: 0.17
Nodes (13): json, shutil, sqlite3, DatasetIds, monthly_rides(), _months(), Synthetic dataset that characterisation, rule, page and Strava tests start…, db_copy() (+5 more)

### Community 28 - "Strava Ride Updates"
Cohesion: 0.33
Nodes (3): Function to set the date for last pull from Strava, Method to create or update ride data in bulk to database, Method to determine which selection of components to update

### Community 29 - "Component and History Operations"
Cohesion: 0.13
Nodes (16): Phase C: tests, branch `feature/stage1-tests`, Task 10: Operation scenarios: components, history, quick swap, types, config, Task 14: Rules, health and migration rewritten; old tests removed, Tests, Method to create component, Method to update component details, Method to create installation history record, Method to validate history records before processing and storing in database (+8 more)

### Community 30 - "Database Snapshot Extraction"
Cohesion: 0.15
Nodes (20): re, extract(), main(), Path, Run one checkout against a copy of db_path and return its stored and derived…, new_id_map(), normalise_new_ids(), _normalise_value() (+12 more)

### Community 31 - "Service Rules Tests"
Cohesion: 0.07
Nodes (26): parametrize, Service rules: planned services stay out of health, completion and revert,…, Reverting a completed service to planned leaves the component, its other…, Stored changes other than those to the removed service's own row, Uninstalling the cassette reprocesses its services; svc-cassette-2, its newest,…, Setup: a newer cassette service without workplan on 2026-11-01 08:00. Deleting…, The chain's planned service in wp-drivetrain does not block one outside any…, svc-pads-retired cannot be reverted to planned, since its component is retired (+18 more)

### Community 32 - "Utility Functions"
Cohesion: 0.12
Nodes (20): asyncio, collections, build_incident_service_entry(), config_path(), generate_workplan_title(), get_effective_planned_date(), parse_button_sorting(), Module for auxiliary functions (+12 more)

### Community 33 - "Health Check Tests"
Cohesion: 0.10
Nodes (16): database(), logger(), fixture, The health rule: an error logged in the last 24 hours, a failing database or a…, SQLite creates an empty file for a wrong path, e.g. a missing Docker mount, An error logged anywhere reaches the recorder through the root logger, lifespan in main.py sets every root handler to INFO or DEBUG at startup, The recalculation of the dataset logs no error, so the fixture starts healthy (+8 more)

### Community 34 - "Src Layout, Version, Config"
Cohesion: 0.08
Nodes (30): Phase B: move, version, config, Docker, branch `feature/stage1-src-layout`, Task 4: Move to the src layout, Task 5: Version from the git tag, Task 6: Config location from `VELO_SUPERVISOR_CONFIG`, Task 7: Docker image and first CI workflow, importlib_metadata, build_dataset(), Path (+22 more)

### Community 35 - "Workplan and Incident Rules"
Cohesion: 0.09
Nodes (21): Workplan, incident and history rules: links through services, titles, notes,…, wp-brake-check set back to Planned with a full update; completion rules apply…, Components, bikes, progress and title of a workplan come from its services. A…, The chain has svc-chain-planned: retiring is refused and changes nothing,…, inc-drivetrain reaches wp-drivetrain through its two services, one planned and…, The values the workplan, bike, component and collection pages show for planned…, A note is stored on the new record; a note of only spaces is stored as NULL, on…, The cassette retired and replaced by a new one: both new history records carry… (+13 more)

### Community 36 - "Sub-Agent Team"
Cohesion: 0.67
Nodes (3): Available Agents, Direct Invocation, Sub-Agent Team

### Community 37 - "Project Guidance Overview"
Cohesion: 0.22
Nodes (8): Before Creating Handover, Communication & Output Rules, Debugging & Bug Fixing Rules, For fullstack-developer, graphify, Important Notes, Project Overview, Testing Requirements

### Community 38 - "Bike Overview and Triggers"
Cohesion: 0.20
Nodes (6): Result extractor, Method to determine which factor triggered a warning status, Calculate lifetime and service triggers for a component, Method to check if a bike has all mandatory components and respects max…, Method to update only the count of components for a given component type, Method to produce payload for page bike overview

### Community 39 - "Rewrite Roadmap"
Cohesion: 0.20
Nodes (10): Anti-goals, Branch policy during the freeze, Constraints, Goals, Issue map, Left to each stage, Non-goals, Rewrite roadmap: new UI, restructured backend, exposed API (+2 more)

### Community 40 - "Code Review and Recalculation"
Cohesion: 0.06
Nodes (59): Issues Found, Key Checks, Output Format, Recommendations, Review Philosophy, Review Process, Summary, Task 9: Recalculation characterisation (+51 more)

### Community 41 - "Git Workflow Rules"
Cohesion: 0.29
Nodes (7): Branch Strategy, Commit Process, For All Agents, For code-reviewer, For docs-maintainer, For fullstack-developer, Git Workflow Rules

### Community 42 - "Health Endpoint"
Cohesion: 0.50
Nodes (4): health(), Endpoint for the Docker health check, returns 503 if errors were logged the…, get_health_status(), Function to assess application health from errors logged the last 24 hours and…

### Community 43 - "Project Conventions Summary"
Cohesion: 0.22
Nodes (8): Change Management Rules, Debugging & bug fixing rules (root cause first), Docker HEALTHCHECK against /health, graphify knowledge graph usage rules, Agent handover documents (.handovers/), Log levels drive container health, Technical debt tracked in issue #356, TomSelect multi-select pattern

### Community 44 - "Development Commands"
Cohesion: 0.40
Nodes (5): Database Operations, Dependencies, Development Commands, Running the Application, Testing

### Community 45 - "Handover Template"
Cohesion: 0.25
Nodes (7): Blockers / Open Questions, Context, Decisions Made, Deliverables, Next Steps for [Target Agent], References, [Source Agent] -> [Target Agent] Handover

### Community 46 - "Incident-Service Link Migration"
Cohesion: 0.25
Nodes (8): check_incidents_workplan_column_present(), insert_planned_service_for_migration(), migrate_drop_incident_workplan_column(), migrate_incident_links_to_services(), Check if incidents table still has the workplan_id column, Insert a planned service with no date, bike or distance. Returns False if the…, Rebuild incident to workplan links through services, Rebuild incidents table without the workplan_id column

### Community 47 - "Component Types Migration"
Cohesion: 0.32
Nodes (7): check_component_types_columns(), count_component_types_in_use(), migrate_component_types(), Check if the component_types table needs migration, Migrate the component_types table to add new columns, Script to migrate the database, including adding new tables and fields, Count how many components use a specific component type

### Community 48 - "Database Expert Agent"
Cohesion: 0.29
Nodes (6): Constraints, Core Responsibilities, Pattern Consistency - CRITICAL, Query Optimization, Schema Changes, Workflow

### Community 49 - "UX Designer Agent"
Cohesion: 0.29
Nodes (6): Core Responsibilities, Design Principles, Specifications to Include, v1 (Before Architect), v2 (After Architect), Workflow

### Community 50 - "Stage 1 Decisions"
Cohesion: 0.15
Nodes (13): CI, Comparison against master, Configuration file location, Decided, Docker, Legacy files removed, Release notes backfill and README cleanup, Stage handover (+5 more)

### Community 51 - "Service Completion and Updates"
Cohesion: 0.25
Nodes (4): Method to build the report used by the plan services and complete services…, Method to complete planned services with one service date, keeping their…, Method to update a service record, including status changes in both directions, Method to validate service records before processing and storing in database

### Community 52 - "Component Operation Characterisation"
Cohesion: 0.06
Nodes (31): _execute(), parametrize, Characterisation of component, history, quick swap, component type, delete and…, Changing the type recounts both types: Saddle in_use 0, Bottle cage 1. Spare…, Bremseklosser bak æøå retired on bike-gravel 2026-10-01 08:00. Marker: gravel…, hist-chain-gravel moved from 2025-08-01 to 2025-07-15 08:00, with a note.…, Deleting a planned service recalculates nothing, Records current behaviour; see #374. Deleting a component's only history record… (+23 more)

### Community 53 - "Workplan Planned Services Migration"
Cohesion: 0.25
Nodes (8): check_workplans_affected_columns(), migrate_drop_workplan_affected_columns(), migrate_workplans_to_planned_services(), Check if workplans table still has the affected bike/component columns, Resolve bike and component names, marking components that no longer exist, Convert affected components on planned workplans into planned services,…, Rebuild workplans table without the affected bike/component columns, read_names_for_migration()

### Community 54 - "Stage 1 Handover"
Cohesion: 0.22
Nodes (9): Blockers / Open Questions, Context, Deliverables, Issues opened, Next Steps, References, Stage 1 Foundation Handover, Stage 2 parity checklist (from removed docs) (+1 more)

### Community 55 - "Refusal Leaves State Unchanged"
Cohesion: 0.67
Nodes (3): parametrize, Each validation refuses on the dataset as it is and leaves every value unchanged, test_refusal_changes_nothing()

### Community 56 - "Migration Database Discovery"
Cohesion: 0.33
Nodes (6): find_database_file(), migrate_database(), prompt_for_db_path(), Search for a database file in the user's home directory and subdirectories, Prompt user for database path or filename and verify it exists, Main function to handle the database migration.

### Community 57 - "Service Integration Column Migrations"
Cohesion: 0.25
Nodes (8): check_incidents_workplan_column(), check_services_integration_columns(), migrate_incidents_workplan_link(), migrate_services_integration_columns(), Check if Incidents table needs workplan_id column, Add workplan_id column to Incidents table for workplan hub integration, Check which service integration columns are missing on the services table, Add status, incident_id and planned_date to services, mark existing rows…

### Community 58 - "Handover Communication"
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

### Community 62 - "Development Workflow"
Cohesion: 0.50
Nodes (4): For Bug Fixes, For Documentation Updates, For New Features, Standard Development Workflow

### Community 63 - "Handovers Directory Guide"
Cohesion: 0.33
Nodes (5): Creating Handovers, Directory Structure, Finding Handovers, Handovers Directory, Rules

### Community 64 - "Stage 1 Implementation Plan"
Cohesion: 0.10
Nodes (27): argparse, Global Constraints, Phase A: extractor and baseline, branch `feature/stage1-extractor`, Phase D: template, CI, releases, cleanup, docs, branch `feature/stage1-finish`, Stage 1 Foundation Implementation Plan, Task 15: Template database defaults, Task 16: CI made complete and permanent, Task 17: Release backfill and README (+19 more)

### Community 65 - "Architect Agent"
Cohesion: 0.40
Nodes (4): Core Responsibilities, Handover Content, Principles, Workflow

### Community 66 - "Architecture Overview"
Cohesion: 0.40
Nodes (5): Architecture Overview, Configuration, Core Components, Key Features, Project Structure

### Community 67 - "Collection and Record Updates"
Cohesion: 0.10
Nodes (12): BusinessLogic, Method to update a component history record with validation, Method to update collection, Method to change status of all components in a collection, Method to update incident record (supports full or partial updates), Method to update workplan (supports full or partial updates), Method to refresh all bikes from Strava, Method to check the database connection for the health check (+4 more)

### Community 70 - "Rewrite Stages"
Cohesion: 0.29
Nodes (7): Stage 1: Foundation, Stage 2: Design, Stage 3: Architecture, Stage 4: Backend refactor, Stage 5: New frontend and features, Stage 6: Switch-over, Stages

### Community 71 - "History Notes Migration"
Cohesion: 0.50
Nodes (4): check_component_history_notes_column(), migrate_component_history_notes(), Check if component_history table needs notes column, Add notes column to component_history table

### Community 72 - "Component Type Time Migration"
Cohesion: 0.50
Nodes (4): check_component_types_time_columns(), migrate_component_types_time_fields(), Check if ComponentTypes table needs time-based fields migration, Add time-based fields to ComponentTypes table

### Community 73 - "Test Fixtures and Dataset"
Cohesion: 0.13
Nodes (25): Task 8: Test foundation and synthetic dataset, fastapi_testclient, Decisions Made, importlib, test_dataset_builds_and_recalculates(), app(), client(), clock() (+17 more)

### Community 74 - "Business Logic Page Payloads"
Cohesion: 0.08
Nodes (43): Task 2: Derived values, Module to handle business logic, Method to produce payload for page component overview, Method to produce payload for page component details, Method to create component-to-collection mapping dictionaries, Method to produce payload for displaying table of all collections, Method to produce payload for page incident reports, Method to build dictionaries of bike and component ids referenced in received… (+35 more)

### Community 75 - "Component Time Migration"
Cohesion: 0.50
Nodes (4): check_components_time_columns(), migrate_components_time_fields(), Check if Components table needs time-based fields migration, Add time-based fields to Components table and populate threshold_km

### Community 76 - "Service Workplan Link Migration"
Cohesion: 0.50
Nodes (4): check_services_workplan_column(), migrate_services_workplan_link(), Check if Services table needs workplan_id column, Add workplan_id column to Services table for workplan hub integration

### Community 77 - "Stage Design Specs"
Cohesion: 0.18
Nodes (8): Anti-goals, Constraints, Done when, Goals, Intent, Left to the builder, Non-goals, Stage 1: Foundation

### Community 78 - "Rewrite Approach Options"
Cohesion: 0.33
Nodes (6): API: separate API, or one set of resources with two formats, API style: FHIR-conformant or FHIR-inspired, Approaches considered, Delivery: side by side on master, or frozen master and long-running dev, Frontend: server-rendered with htmx, or a JSON API with a separate frontend app, Provenance actor: named user or source of change

### Community 79 - "Docs Maintainer Agent"
Cohesion: 0.50
Nodes (3): Core Responsibilities, Documentation Rules, Workflow

### Community 81 - "Stage 1 Approaches"
Cohesion: 0.33
Nodes (6): Approaches, Fixed clock, Order of work, Release mechanism, Synthetic dataset, Version source

### Community 82 - "Table Sorting and Filtering"
Cohesion: 0.29
Nodes (8): initializeCollectionsSorting(), sortColumn(), initializeWorkplanTable(), setupIncidentTableSorting(), setupWorkplanSearch(), setupWorkplanStatusFiltering(), setupWorkplanTableSorting(), updateWorkplansVisibility()

### Community 84 - "Workplan Name Migration"
Cohesion: 0.50
Nodes (4): check_workplans_name_column(), migrate_workplans_name_column(), Check if workplans table needs the workplan_name column, Add the optional user given name to the workplans table, existing workplans…

### Community 87 - "Bike Record Access"
Cohesion: 0.33
Nodes (3): Method to retrieve record for a specific bike, Method to create or update bike data to the database, Method to get the name of a bike based on bike id

### Community 88 - "Component Record Access"
Cohesion: 0.33
Nodes (3): Method to get component names based on list of ids, Method to retrieve record for a specific component, Method to create or update component data to the database

### Community 91 - "Error Recorder Logging"
Cohesion: 0.29
Nodes (4): ErrorRecorder, Logging handler that keeps the most recent error records in memory for the…, Method to store error records and ignore lower levels. Filters here instead of…, Method to get error records newer than the given number of hours

### Community 92 - "Form Field Validation"
Cohesion: 0.40
Nodes (5): addFormValidation(), clearValidationErrors(), showFieldError(), validateComponentThresholds(), validateQuickSwapForm()

### Community 102 - "Bulk Status Confirmation"
Cohesion: 0.50
Nodes (4): cleanup(), handleCancel(), handleConfirm(), performBulkStatusChange()

### Community 103 - "Markdown Preview Rendering"
Cohesion: 0.50
Nodes (4): containsMarkdown(), renderPreview(), setInitialMode(), updateCheckboxInText()

### Community 105 - "Incident Table Filtering"
Cohesion: 0.67
Nodes (4): initializeIncidentTable(), setupIncidentSearch(), setupIncidentStatusFiltering(), updateIncidentVisibility()

### Community 106 - "Quick Swap Selection"
Cohesion: 0.67
Nodes (3): filterNewComponentsByType(), handleOldComponentChange(), updateQuickSwapCollectionWarning()

### Community 115 - "Filtered Log Endpoint"
Cohesion: 0.50
Nodes (4): get_filtered_log(), Endpoint to read log and return only business events, Function to get filtered log records, read_filtered_logs()

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
- **163 isolated node(s):** `DatasetIds`, `GitHub Issues Tracker`, `Velo Supervisor 2000 (Project)`, `Strava OAuth Token Setup (Step 2)`, `Semantic Versioning (SemVer)` (+158 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 744 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **83 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `tests/conftest.py` and `Manual testing protocols approach`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **Why does `DatabaseManager` connect `Database Read Queries` to `Component Service Status Write`, `Peewee Database Models`, `Middleware and Exception Handling`, `Single Record Reads`, `Incident Record Write`, `Service Record Write`, `Read All Component Objects`, `Health Check Tests`, `Oldest Ride Date Lookup`, `Collection Write`, `Bulk Ride Write`, `Business Logic Page Payloads`, `Database Connection Check`, `Bike Record Access`, `Component Record Access`, `Read All Workplans`, `Incidents By Workplan Query`, `Component Type Usage Count`, `Latest History Record Lookup`, `Planned Services By Bike`, `Recent Component Bike Lookup`, `Component Service History Subset`, `Component Matching Rides`, `Component Lifetime Status Write`, `Open Incidents Query`, `Workplan Write`, `Services By Workplan Query`, `Component Distance Write`?**
  _High betweenness centrality (0.158) - this node is a cross-community bridge._
- **Why does `BusinessLogic` connect `Collection and Record Updates` to `FastAPI POST Routes`, `App Startup and Scheduler`, `Bike Overview and Triggers`, `Component Status Recalculation`, `Business Logic Page Payloads`, `Service Completion and Updates`, `Service and Incident Creation`, `Strava Ride Updates`, `Component and History Operations`?**
  _High betweenness centrality (0.089) - this node is a cross-community bridge._
- **Why does `assert_matches_expected()` connect `Expected-Result Assertions` to `Component Type Update Test`, `Fake Strava OAuth`, `Service and Workplan Characterisation`, `Code Review and Recalculation`, `Component Type Creation Test`, `Component Creation Tests`, `Test Fixtures and Dataset`, `Integrity App Loader`, `Delete Only History Record`, `Component Operation Characterisation`, `Dataset Serialisation Tests`, `Record Creation Scenarios`, `Component Installation Test`?**
  _High betweenness centrality (0.058) - this node is a cross-community bridge._
- **Are the 9 inferred relationships involving `DatabaseManager` (e.g. with `Bikes` and `Collections`) actually correct?**
  _`DatabaseManager` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `stored_state()` (e.g. with `Blockers / Open Questions` and `Next Steps`) actually correct?**
  _`stored_state()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `derived_values()` (e.g. with `Task 2: Derived values` and `bike_overview()`) actually correct?**
  _`derived_values()` has 5 INFERRED edges - model-reasoned connections that need verification._