# Graph Report - velo-supervisor-2000  (2026-11-17)

## Corpus Check
- 131 files · ~223,095 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 13 file(s) not represented in the graph (top: (none) 6, .example 1, .sqlite 1)

## Summary
- 1503 nodes · 2531 edges · 164 communities (82 shown, 82 thin omitted)
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 190 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `c67ffc7d`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- main.py
- scheduler.py
- test_sync.py
- README.md
- Meta
- test_derived.py
- test_operations_services.py
- DatabaseManager
- assert_matches_expected
- Middleware
- BusinessLogic
- test_validation.py
- main.js
- extract.py
- healthcheck.py
- get
- snapshot_delta
- Stage 1 Foundation Handover
- .write_delete_record
- run_all_migrations
- Decided
- validateDateInput
- dataset.py
- test_render.py
- _new_ids
- derived_values
- logging
- get_button_order
- Tests
- stored_state
- test_services_rules.py
- utils.py
- test_health.py
- test_migration.py
- test_workplans_incidents_rules.py
- Sub-Agent Team
- CLAUDE.md
- json
- Rewrite roadmap: new UI, restructured backend, exposed API
- test_recalculation.py
- Git Workflow Rules
- _assert_new_component
- CLAUDE.md
- Development Commands
- Handover Template
- insert_planned_service_for_migration
- db_migration.py
- database-expert.md
- ux-designer.md
- Path
- parametrize
- test_operations_components.py
- migrate_workplans_to_planned_services
- ErrorRecorder
- migrate_database
- migrate_incidents_workplan_link
- Handover Communication
- fullstack-developer.md
- product-manager.md
- assert_refused_after_setup
- Standard Development Workflow
- Handovers Directory Guide
- compare.py
- architect.md
- Architecture Overview
- .update_rides_bulk
- test_validate_history_record_refuses_retiring_before_latest_service
- test_validate_history_record_refuses_unknown_history_record
- migrate_component_history_notes
- migrate_component_types_time_fields
- tests/conftest.py
- Task 2: Derived values
- migrate_components_time_fields
- migrate_services_workplan_link
- .update_workplan
- test_validate_service_record_refuses_empty_service_date
- docs-maintainer.md
- test_refusals_leave_the_app_healthy
- sortColumn
- test_validate_history_record_refuses_edit_before_previous_record
- migrate_workplans_name_column
- .check_database_connection
- .read_bike_name
- .read_component
- test_validate_history_record_refuses_edit_after_next_record
- test_validate_history_record_refuses_first_record_after_first_service
- get_health_status
- validateComponentThresholds
- test_validate_history_record_accepts_valid_input
- test_validate_quick_swap_refuses_component_without_bike
- test_validate_quick_swap_refuses_retiring_with_planned_services
- test_validate_collection_refuses_unknown_collection
- test_validate_collection_refuses_unknown_component
- test_validate_collection_refuses_component_in_other_collection
- .read_all_workplans
- update_config
- cleanup
- renderPreview
- GitHub Issues Tracker
- initializeIncidentTable
- handleOldComponentChange
- create-container-vs2000.sh
- Strava OAuth Token Setup (Step 2)
- Branching and Versioning
- Changelog and Project Board
- .count_component_types_in_use
- .read_incidents_by_workplan
- .read_latest_history_record
- .read_bike_id_recent_component_history
- .read_planned_services_by_bike
- .read_subset_service_history
- .read_matching_rides
- .read_open_incidents
- .write_component_lifetime_status
- .write_workplan
- .read_services_by_workplan
- .write_component_distance
- .write_component_service_status
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
- .write_incident_record
- .write_service_record
- .read_all_components_objects
- test_validate_history_record_refuses_unknown_component
- test_validate_collection_refuses_components_on_several_bikes
- test_validate_service_record_refuses_unknown_service
- test_validate_service_record_refuses_unknown_component
- test_validate_service_record_refuses_second_planned_service_in_workplan
- test_validate_service_record_refuses_date_before_creation
- test_validate_service_record_refuses_date_after_done_workplan
- test_validate_workplan_completion_refuses_remaining_planned_services
- test_validate_workplan_completion_refuses_invalid_date_format
- test_validate_history_record_refuses_date_before_creation
- test_validate_workplan_completion_refuses_date_before_latest_service
- test_validate_history_record_refuses_date_before_latest_record
- test_validate_history_record_refuses_retiring_with_planned_services
- .read_date_oldest_ride
- Development Notes
- .write_collection
- Code Style & Standards
- .write_update_rides_bulk
- conftest
- fixtures

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
- `Next Steps` --references--> `stored_state()`  [INFERRED]
  .handovers/stages/stage-1-foundation-handover.md → scripts/integrity/snapshot.py
- `Blockers / Open Questions` --references--> `stored_state()`  [INFERRED]
  .handovers/stages/stage-1-foundation-handover.md → scripts/integrity/snapshot.py
- `Task 8: Test foundation and synthetic dataset` --references--> `test_dataset_builds_and_recalculates()`  [INFERRED]
  docs/superpowers/plans/2026-11-16-stage-1-foundation.md → tests/characterisation/test_dataset.py
- `Configuration file location` --references--> `read_config()`  [INFERRED]
  docs/superpowers/specs/2026-11-16-stage-1-foundation-design.md → src/velo_supervisor/utils.py
- `Decisions Made` --references--> `extract()`  [INFERRED]
  .handovers/stages/stage-1-foundation-handover.md → scripts/integrity/extract.py

## Import Cycles
- None detected.

## Communities (164 total, 82 thin omitted)

### Community 0 - "main.py"
Cohesion: 0.07
Nodes (41): asyncio, contextlib, fastapi_responses, fastapi_staticfiles, fastapi_templating, post, add_collection(), add_incident_record() (+33 more)

### Community 1 - "scheduler.py"
Cohesion: 0.15
Nodes (15): apscheduler_schedulers_asyncio, apscheduler_triggers_cron, apscheduler_triggers_interval, FastAPI, lifespan(), Manage application startup and shutdown, Initialize and start the APScheduler instance, Scheduler for automated maintenance tasks (+7 more)

### Community 2 - "test_sync.py"
Cohesion: 0.11
Nodes (31): Task 12: Strava sync, new_session_class(), A FakeOAuth2Session subclass with its own empty call records, _errors(), _gear_requested(), _install(), fixture, The Strava sync against synthetic Strava responses. FakeOAuth2Session… (+23 more)

### Community 3 - "README.md"
Cohesion: 0.29
Nodes (5): Strava OAuth scope incl. profile:read_all, Switched from pip to uv, v0.5.0 release (service integration, health check, uv), GitHub action writes current_version.txt on master, Manual testing protocols approach

### Community 4 - "Meta"
Cohesion: 0.10
Nodes (35): Model, peewee, Module for interaction with a Sqlite database, BaseModel, Bikes, Collections, ComponentHistory, Components (+27 more)

### Community 5 - "test_derived.py"
Cohesion: 0.13
Nodes (15): Task 4: Move to the src layout, os, detect_layout(), Path, Tell the pre-restructure flat layout from the package layout, shutil, db_copy(), fixture (+7 more)

### Community 6 - "test_operations_services.py"
Cohesion: 0.06
Nodes (35): pytest, parametrize, Characterisation of service, incident, workplan and collection operations. Each…, svc-chain-planned and svc-wheel-planned completed on 2026-11-01 08:00 with one…, svc-chain-2 moved from 2025-10-01 to 2025-11-01 08:00 and its description…, svc-chain-2 reverted to planned for 2026-12-01 10:00: date, bike and marker are…, svc-wheel-planned completed through the edit form on 2026-11-01 08:00, keeping…, inc-drivetrain edited in full: severity Monitor, the cassette removed, a new… (+27 more)

### Community 7 - "DatabaseManager"
Cohesion: 0.04
Nodes (24): DatabaseManager, Method to sum distance for a given set of rides, Method to read and sort content of component_types table, Method to read components for a specific bike, Class to interact with a SQLite database through Peewee, Method to read installed components for a specific bike, Method to read a subset of records from the component history table, Method to retrieve the oldest record from the installation log of a given… (+16 more)

### Community 8 - "assert_matches_expected"
Cohesion: 0.09
Nodes (22): expected_dir(), fixture, test_difference_fails(), test_existing_file_is_never_overwritten(), test_missing_file_fails_naming_record_expected(), test_missing_file_is_recorded_when_asked(), Chain uninstalled from bike-road 2026-10-01 08:00. New record marker: 440 +…, A new type is stored with its intervals and in_use 0. The type name is the… (+14 more)

### Community 9 - "Middleware"
Cohesion: 0.16
Nodes (11): BaseHTTPMiddleware, Exception, exception_handler, http_exception_handler(), Function to catch http errors from Uvicorn and return them to the middleware, Middleware, Request, Class to handle exceptions that breaks the program and should be shown to the… (+3 more)

### Community 10 - "BusinessLogic"
Cohesion: 0.08
Nodes (27): Comparison against master (production copy, recalculation + derived values), BusinessLogic, Method to update component lifetime and service status when no installation…, Method to update status for a given bike based on component service and…, Method to update component details, Method to update a component history record with validation, Method to calculate distance and bike id for history records, Method to build the report used by the plan services and complete services… (+19 more)

### Community 12 - "main.js"
Cohesion: 0.09
Nodes (9): editCollection(), handleUpdate(), initializeCollectionsSearch(), updateRowVisibility(), initializeComponentSelector(), NOTE: All collection details page handlers are in the "Functions used on…, IMPORTANT: Remove readonly - allow manual typing, showToast() (+1 more)

### Community 13 - "extract.py"
Cohesion: 0.15
Nodes (20): collections_abc, pathlib, frozen_clock(), Freeze time at FIXED_NOW in UTC so date-dependent calculations are reproducible, extract(), main(), Path, Run one checkout against a copy of db_path and return its stored and derived… (+12 more)

### Community 14 - "healthcheck.py"
Cohesion: 0.50
Nodes (3): Health check run by the Docker daemon, exit code 0 means healthy and 1 means…, urllib_error, urllib_request

### Community 15 - "get"
Cohesion: 0.10
Nodes (26): get, add_history_record(), collection_details(), component_overview(), component_types_overview(), get_filtered_log(), help_page(), incident_reports() (+18 more)

### Community 16 - "snapshot_delta"
Cohesion: 0.25
Nodes (12): _leaves(), Every leaf path that differs between two snapshots, as {path: {"before": x,…, snapshot_delta(), test_added_and_removed_rows_list_every_leaf(), test_changed_value(), test_empty_dict_is_a_value(), test_key_with_slash_is_refused(), test_list_is_one_value() (+4 more)

### Community 17 - "Stage 1 Foundation Handover"
Cohesion: 0.08
Nodes (23): Blockers / Open Questions, Context, Coverage (287 tests, total 80%), Decisions Made, Deliverables, Issues opened, Next Steps, References (+15 more)

### Community 18 - ".write_delete_record"
Cohesion: 0.12
Nodes (8): Method to retrieve record for a single component type, Method to retrieve record for a specific entry in the installation log, Method to retrieve a specific service record, Method to retrieve record for a specific collection, Method to retrieve record for a specific incident report, Method to retrieve record for a specific workplan, Method to write component type record in database, Method to delete a given record and associated records

### Community 19 - "run_all_migrations"
Cohesion: 0.14
Nodes (14): create_collections_table(), create_incidents_table(), create_workplans_table(), populate_component_types_thresholds(), populate_components_thresholds(), Creates the incidents table if it doesn't exist., Creates the workplans table if it doesn't exist., Creates the collections table if it doesn't exist. (+6 more)

### Community 20 - "Decided"
Cohesion: 0.06
Nodes (32): Global Constraints, Phase A: extractor and baseline, branch `feature/stage1-extractor`, Phase B: move, version, config, Docker, branch `feature/stage1-src-layout`, Phase D: template, CI, releases, cleanup, docs, branch `feature/stage1-finish`, Stage 1 Foundation Implementation Plan, Task 16: CI made complete and permanent, Task 17: Release backfill and README, Task 18: Legacy removed (+24 more)

### Community 21 - "validateDateInput"
Cohesion: 0.20
Nodes (9): initializeDatePickers(), initializeIncidentForm(), initializeWorkplanForm(), submitCollectionAjax(), submitComponentAjax(), validateCollectionStatusChange(), validateDateInput(), validateIncidentForm() (+1 more)

### Community 22 - "dataset.py"
Cohesion: 0.14
Nodes (16): dataclasses, Task 15: Template database defaults, dumps(), Serialise a state deterministically, keeping non-ASCII characters readable, sqlite3, test_dataset_builds_and_recalculates(), test_new_ids_are_normalised_in_both_layers(), test_read_functions_raise_no_errors_on_the_dataset() (+8 more)

### Community 23 - "test_render.py"
Cohesion: 0.28
Nodes (7): Task 13: Page render tests, parametrize, Every page renders for every resource in the dataset, and unknown IDs fail the…, Stage 4 changes the unknown-ID status to 404 (#356), test_every_detail_page_renders(), test_every_overview_page_renders(), test_unknown_ids_today()

### Community 24 - "_new_ids"
Cohesion: 0.11
Nodes (18): _new_ids(), An open incident on bike-gravel for the tire; empty optional fields become…, Primary keys of table that are not in the dataset, in row order, A planned workplan with a name; no services, so it reaches no bike or component, A workplan from inc-drivetrain with no component selection plans a service for…, Only the selected incident components get a planned service: the cassette, not…, A completed chain service on 2026-11-01 08:00, linked to wp-drivetrain. Marker…, A workplan from inc-squeal, whose only component is the retired pads: the… (+10 more)

### Community 25 - "derived_values"
Cohesion: 0.17
Nodes (29): _bike_values(), details(), _by_first(), _collection_values(), details(), status(), _component_values(), details() (+21 more)

### Community 27 - "logging"
Cohesion: 0.22
Nodes (8): datetime, logging, requests_oauthlib, Module for middleware, Module to interact with Strava APIs, starlette_exceptions, starlette_middleware_base, traceback

### Community 28 - "get_button_order"
Cohesion: 0.20
Nodes (10): bike_details(), component_details(), config_overview(), Endpoint for component details page, Endpoint for component types page, Endpoint for bike details page, get_button_order(), get_button_sorting_config() (+2 more)

### Community 29 - "Tests"
Cohesion: 0.08
Nodes (27): Phase C: tests, branch `feature/stage1-tests`, Task 10: Operation scenarios: components, history, quick swap, types, config, Task 11: Operation scenarios: services, workplans, incidents, collections, Task 14: Rules, health and migration rewritten; old tests removed, Constraints, Tests, Method to create component, Method to create installation history record (+19 more)

### Community 30 - "stored_state"
Cohesion: 0.17
Nodes (26): Review Focus, Task 1: Integrity package: loader, clock, recalculation, stored-state snapshot, new_id_map(), normalise_new_ids(), _normalise_value(), Path, Read every table and column straight from SQLite, keyed table, primary key,…, Map each primary key absent from baseline_ids to new:<table>:<n>, numbered in… (+18 more)

### Community 31 - "test_services_rules.py"
Cohesion: 0.06
Nodes (32): parametrize, Service rules: planned services stay out of health, completion and revert,…, svc-chain-planned (wp-drivetrain, inc-drivetrain) completed on 2026-11-01 08:00…, Stored changes other than those to the removed service's own row, Reverting a completed service to planned leaves the component, its other…, Uninstalling the cassette reprocesses its services; svc-cassette-2, its newest,…, Setup: a newer cassette service without workplan on 2026-11-01 08:00. Deleting…, The chain has two completed services and svc-chain-planned; only the planned… (+24 more)

### Community 32 - "utils.py"
Cohesion: 0.08
Nodes (44): collections, re, Module to handle business logic, Method to produce payload for page incident reports, Method to produce payload for page of all workplans, Method to produce payload for workplan details page, build_incident_service_entry(), config_path() (+36 more)

### Community 33 - "test_health.py"
Cohesion: 0.09
Nodes (19): importlib, database(), logger(), fixture, The health rule: an error logged in the last 24 hours, a failing database or a…, SQLite creates an empty file for a wrong path, e.g. a missing Docker mount, An error logged anywhere reaches the recorder through the root logger, lifespan in main.py sets every root handler to INFO or DEBUG at startup (+11 more)

### Community 34 - "test_migration.py"
Cohesion: 0.20
Nodes (16): columns(), description(), old_db(), fixture, query(), db_migration converts the pre-#351 workplan and incident model to links through…, The dataset with the four tables in their pre-#351 shape and old-model rows, Old columns become the service integration schema and old links become… (+8 more)

### Community 35 - "test_workplans_incidents_rules.py"
Cohesion: 0.08
Nodes (23): Workplan, incident and history rules: links through services, titles, notes,…, Only the cassette is selected, so the chain gets no service in the new workplan, A given name is the workplan's title; saving it blank stores NULL and the…, wp-brake-check set back to Planned with a full update; completion rules apply…, The chain has svc-chain-planned: retiring is refused and changes nothing,…, Components, bikes, progress and title of a workplan come from its services. A…, inc-drivetrain reaches wp-drivetrain through its two services, one planned and…, The values the workplan, bike, component and collection pages show for planned… (+15 more)

### Community 36 - "Sub-Agent Team"
Cohesion: 0.67
Nodes (3): Available Agents, Direct Invocation, Sub-Agent Team

### Community 37 - "CLAUDE.md"
Cohesion: 0.22
Nodes (8): Before Creating Handover, Communication & Output Rules, Debugging & Bug Fixing Rules, For fullstack-developer, graphify, Important Notes, Project Overview, Testing Requirements

### Community 38 - "json"
Cohesion: 0.19
Nodes (7): json, FakeOAuth2Session, FakeResponse, load_fixture(), A stand-in for requests_oauthlib.OAuth2Session that answers from…, typing, urllib_parse

### Community 39 - "Rewrite roadmap: new UI, restructured backend, exposed API"
Cohesion: 0.05
Nodes (36): Anti-goals, API: separate API, or one set of resources with two formats, API style: FHIR-conformant or FHIR-inspired, Approaches considered, Branch policy during the freeze, Constraints, Delivery: side by side on master, or frozen master and long-running dev, Frontend: server-rendered with htmx, or a JSON API with a separate frontend app (+28 more)

### Community 40 - "test_recalculation.py"
Cohesion: 0.06
Nodes (58): CI and workflow, Issues Found, Key Checks, Output Format, Recommendations, Review Philosophy, Review Process, Summary (+50 more)

### Community 41 - "Git Workflow Rules"
Cohesion: 0.29
Nodes (7): Branch Strategy, Commit Process, For All Agents, For code-reviewer, For docs-maintainer, For fullstack-developer, Git Workflow Rules

### Community 42 - "_assert_new_component"
Cohesion: 0.29
Nodes (7): _assert_new_component(), A component created as not installed gets no history; the alternate method sets…, Chain swapped for a spare chain on 2026-10-01 08:00; the old chain becomes not…, An installed component gets a history record and is recalculated at once. Road…, test_create_installed_component(), test_create_not_installed_component(), test_quick_swap_to_not_installed_with_existing_component()

### Community 43 - "CLAUDE.md"
Cohesion: 0.22
Nodes (8): Change Management Rules, Debugging & bug fixing rules (root cause first), Docker HEALTHCHECK against /health, graphify knowledge graph usage rules, Agent handover documents (.handovers/), Log levels drive container health, Technical debt tracked in issue #356, TomSelect multi-select pattern

### Community 44 - "Development Commands"
Cohesion: 0.40
Nodes (5): Database Operations, Dependencies, Development Commands, Running the Application, Testing

### Community 45 - "Handover Template"
Cohesion: 0.25
Nodes (7): Blockers / Open Questions, Context, Decisions Made, Deliverables, Next Steps for [Target Agent], References, [Source Agent] -> [Target Agent] Handover

### Community 46 - "insert_planned_service_for_migration"
Cohesion: 0.25
Nodes (8): check_incidents_workplan_column_present(), insert_planned_service_for_migration(), migrate_drop_incident_workplan_column(), migrate_incident_links_to_services(), Check if incidents table still has the workplan_id column, Insert a planned service with no date, bike or distance. Returns False if the…, Rebuild incident to workplan links through services, Rebuild incidents table without the workplan_id column

### Community 47 - "db_migration.py"
Cohesion: 0.32
Nodes (7): check_component_types_columns(), count_component_types_in_use(), migrate_component_types(), Check if the component_types table needs migration, Migrate the component_types table to add new columns, Script to migrate the database, including adding new tables and fields, Count how many components use a specific component type

### Community 48 - "database-expert.md"
Cohesion: 0.25
Nodes (7): CI and workflow, Constraints, Core Responsibilities, Pattern Consistency - CRITICAL, Query Optimization, Schema Changes, Workflow

### Community 49 - "ux-designer.md"
Cohesion: 0.25
Nodes (7): CI and workflow, Core Responsibilities, Design Principles, Specifications to Include, v1 (Before Architect), v2 (After Architect), Workflow

### Community 52 - "test_operations_components.py"
Cohesion: 0.05
Nodes (37): _execute(), parametrize, Characterisation of component, history, quick swap, component type, delete and…, Offset, name, cost and notes of the rear wheel change; distance follows the new…, Changing the type recounts both types: Saddle in_use 0, Bottle cage 1. Spare…, Spare saddle installed on bike-gravel 2026-09-01 08:00, its first history…, Bremseklosser bak æøå retired on bike-gravel 2026-10-01 08:00. Marker: gravel…, hist-chain-gravel moved from 2025-08-01 to 2025-07-15 08:00, with a note.… (+29 more)

### Community 53 - "migrate_workplans_to_planned_services"
Cohesion: 0.25
Nodes (8): check_workplans_affected_columns(), migrate_drop_workplan_affected_columns(), migrate_workplans_to_planned_services(), Check if workplans table still has the affected bike/component columns, Resolve bike and component names, marking components that no longer exist, Convert affected components on planned workplans into planned services,…, Rebuild workplans table without the affected bike/component columns, read_names_for_migration()

### Community 54 - "ErrorRecorder"
Cohesion: 0.40
Nodes (3): ErrorRecorder, Logging handler that keeps the most recent error records in memory for the…, Method to store error records and ignore lower levels. Filters here instead of…

### Community 56 - "migrate_database"
Cohesion: 0.33
Nodes (6): find_database_file(), migrate_database(), prompt_for_db_path(), Search for a database file in the user's home directory and subdirectories, Prompt user for database path or filename and verify it exists, Main function to handle the database migration.

### Community 57 - "migrate_incidents_workplan_link"
Cohesion: 0.25
Nodes (8): check_incidents_workplan_column(), check_services_integration_columns(), migrate_incidents_workplan_link(), migrate_services_integration_columns(), Check if Incidents table needs workplan_id column, Add workplan_id column to Incidents table for workplan hub integration, Check which service integration columns are missing on the services table, Add status, incident_id and planned_date to services, mark existing rows…

### Community 58 - "Handover Communication"
Cohesion: 0.33
Nodes (6): Agent Communication via Handovers, Creating Handovers, Detailed Instructions, Handover Structure, Naming Convention, Reading Handovers

### Community 59 - "fullstack-developer.md"
Cohesion: 0.29
Nodes (6): Backend Patterns, CI and workflow, Core Responsibilities, Frontend Patterns, Handover Content, Workflow

### Community 60 - "product-manager.md"
Cohesion: 0.29
Nodes (6): Boundaries, CI and workflow, Core Responsibilities, Key Principle: You Are Interactive, Requirements Document, User Story Format

### Community 61 - "assert_refused_after_setup"
Cohesion: 0.25
Nodes (8): assert_refused_after_setup(), The refusal returns expected and adds nothing to the delta the setup left, Setup: coll-mixed reduced to the retired pads with update_collection, which…, Setup: coll-mixed reduced to the cassette, which has no planned service, and…, Not a validate_collection branch: change_collection_status refuses before…, test_change_collection_status_refuses_empty_collection(), test_validate_collection_refuses_retired_member(), test_validate_collection_refuses_retiring_with_planned_services()

### Community 62 - "Standard Development Workflow"
Cohesion: 0.50
Nodes (4): For Bug Fixes, For Documentation Updates, For New Features, Standard Development Workflow

### Community 63 - "Handovers Directory Guide"
Cohesion: 0.33
Nodes (5): Creating Handovers, Directory Structure, Finding Handovers, Handovers Directory, Rules

### Community 64 - "compare.py"
Cohesion: 0.15
Nodes (21): argparse, Task 3: Extract and compare CLIs, baseline against master, integrity, Path, diff(), _error_paths(), main(), present_on_both_sides() (+13 more)

### Community 65 - "architect.md"
Cohesion: 0.33
Nodes (5): CI and workflow, Core Responsibilities, Handover Content, Principles, Workflow

### Community 66 - "Architecture Overview"
Cohesion: 0.40
Nodes (5): Architecture Overview, Configuration, Core Components, Key Features, Project Structure

### Community 71 - "migrate_component_history_notes"
Cohesion: 0.50
Nodes (4): check_component_history_notes_column(), migrate_component_history_notes(), Check if component_history table needs notes column, Add notes column to component_history table

### Community 72 - "migrate_component_types_time_fields"
Cohesion: 0.50
Nodes (4): check_component_types_time_columns(), migrate_component_types_time_fields(), Check if ComponentTypes table needs time-based fields migration, Add time-based fields to ComponentTypes table

### Community 73 - "tests/conftest.py"
Cohesion: 0.13
Nodes (24): Task 8: Test foundation and synthetic dataset, fastapi_testclient, app(), client(), clock(), config_contents(), dataset_db(), _forget_app_modules() (+16 more)

### Community 74 - "Task 2: Derived values"
Cohesion: 0.08
Nodes (25): Task 2: Derived values, Result extractor, Method to update collection, Method to produce payload for page component overview, Method to produce payload for page component details, Method to determine which factor triggered a warning status, Calculate lifetime and service triggers for a component, Method to check if a bike has all mandatory components and respects max… (+17 more)

### Community 75 - "migrate_components_time_fields"
Cohesion: 0.50
Nodes (4): check_components_time_columns(), migrate_components_time_fields(), Check if Components table needs time-based fields migration, Add time-based fields to Components table and populate threshold_km

### Community 76 - "migrate_services_workplan_link"
Cohesion: 0.50
Nodes (4): check_services_workplan_column(), migrate_services_workplan_link(), Check if Services table needs workplan_id column, Add workplan_id column to Services table for workplan hub integration

### Community 79 - "docs-maintainer.md"
Cohesion: 0.40
Nodes (4): CI and workflow, Core Responsibilities, Documentation Rules, Workflow

### Community 82 - "sortColumn"
Cohesion: 0.29
Nodes (8): initializeCollectionsSorting(), sortColumn(), initializeWorkplanTable(), setupIncidentTableSorting(), setupWorkplanSearch(), setupWorkplanStatusFiltering(), setupWorkplanTableSorting(), updateWorkplansVisibility()

### Community 84 - "migrate_workplans_name_column"
Cohesion: 0.50
Nodes (4): check_workplans_name_column(), migrate_workplans_name_column(), Check if workplans table needs the workplan_name column, Add the optional user given name to the workplans table, existing workplans…

### Community 87 - ".read_bike_name"
Cohesion: 0.33
Nodes (3): Method to retrieve record for a specific bike, Method to create or update bike data to the database, Method to get the name of a bike based on bike id

### Community 88 - ".read_component"
Cohesion: 0.33
Nodes (3): Method to get component names based on list of ids, Method to retrieve record for a specific component, Method to create or update component data to the database

### Community 91 - "get_health_status"
Cohesion: 0.33
Nodes (5): health(), Endpoint for the Docker health check, returns 503 if errors were logged the…, get_health_status(), Method to get error records newer than the given number of hours, Function to assess application health from errors logged the last 24 hours and…

### Community 92 - "validateComponentThresholds"
Cohesion: 0.40
Nodes (5): addFormValidation(), clearValidationErrors(), showFieldError(), validateComponentThresholds(), validateQuickSwapForm()

### Community 101 - "update_config"
Cohesion: 0.50
Nodes (4): Endpoint to update config file based on which form was submitted, update_config(), Helper function to shutdown the server after a short delay, shutdown_server()

### Community 102 - "cleanup"
Cohesion: 0.50
Nodes (4): cleanup(), handleCancel(), handleConfirm(), performBulkStatusChange()

### Community 103 - "renderPreview"
Cohesion: 0.50
Nodes (4): containsMarkdown(), renderPreview(), setInitialMode(), updateCheckboxInText()

### Community 105 - "initializeIncidentTable"
Cohesion: 0.67
Nodes (4): initializeIncidentTable(), setupIncidentSearch(), setupIncidentStatusFiltering(), updateIncidentVisibility()

### Community 106 - "handleOldComponentChange"
Cohesion: 0.67
Nodes (3): filterNewComponentsByType(), handleOldComponentChange(), updateQuickSwapCollectionWarning()

### Community 170 - "Development Notes"
Cohesion: 0.40
Nodes (5): Database Schema Changes, Development Notes, Docker Development, Logging, Technical Debt

### Community 172 - "Code Style & Standards"
Cohesion: 0.50
Nodes (4): Code Style & Standards, Database, Frontend, Python (Backend)

## Ambiguous Edges - Review These
- `tests/conftest.py` → `Manual testing protocols approach`  [AMBIGUOUS]
  tests/README.md · relation: conceptually_related_to

## Knowledge Gaps
- **169 isolated node(s):** `Review Philosophy`, `Review Process`, `Summary`, `Issues Found`, `Recommendations` (+164 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 760 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **82 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `tests/conftest.py` and `Manual testing protocols approach`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **Why does `DatabaseManager` connect `DatabaseManager` to `.write_component_service_status`, `Meta`, `Stage 1 Foundation Handover`, `.write_delete_record`, `.write_incident_record`, `.write_service_record`, `.read_all_components_objects`, `utils.py`, `test_health.py`, `.read_date_oldest_ride`, `.write_collection`, `.write_update_rides_bulk`, `Task 2: Derived values`, `.check_database_connection`, `.read_bike_name`, `.read_component`, `.read_all_workplans`, `.count_component_types_in_use`, `.read_incidents_by_workplan`, `.read_latest_history_record`, `.read_bike_id_recent_component_history`, `.read_planned_services_by_bike`, `.read_subset_service_history`, `.read_matching_rides`, `.read_open_incidents`, `.write_component_lifetime_status`, `.write_workplan`, `.read_services_by_workplan`, `.write_component_distance`?**
  _High betweenness centrality (0.176) - this node is a cross-community bridge._
- **Why does `BusinessLogic` connect `BusinessLogic` to `utils.py`, `main.py`, `scheduler.py`, `.update_rides_bulk`, `Task 2: Derived values`, `.update_workplan`, `Tests`?**
  _High betweenness centrality (0.076) - this node is a cross-community bridge._
- **Why does `assert_matches_expected()` connect `assert_matches_expected` to `test_sync.py`, `test_operations_services.py`, `test_recalculation.py`, `tests/conftest.py`, `_assert_new_component`, `test_operations_components.py`, `dataset.py`, `_new_ids`?**
  _High betweenness centrality (0.054) - this node is a cross-community bridge._
- **Are the 9 inferred relationships involving `DatabaseManager` (e.g. with `Bikes` and `Collections`) actually correct?**
  _`DatabaseManager` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `stored_state()` (e.g. with `Blockers / Open Questions` and `Next Steps`) actually correct?**
  _`stored_state()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `derived_values()` (e.g. with `Task 2: Derived values` and `bike_overview()`) actually correct?**
  _`derived_values()` has 5 INFERRED edges - model-reasoned connections that need verification._