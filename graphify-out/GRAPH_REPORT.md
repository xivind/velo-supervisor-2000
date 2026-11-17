# Graph Report - velo-supervisor-2000  (2026-11-17)

## Corpus Check
- 138 files · ~232,013 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 13 file(s) not represented in the graph (top: (none) 6, .example 1, .sqlite 1)

## Summary
- 1622 nodes · 2654 edges · 196 communities (102 shown, 94 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 236 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `89001362`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- main.py
- scheduler.py
- Tests
- code-reviewer -> docs-maintainer Handover
- Meta
- replace_ids
- assert_matches_expected
- DatabaseManager
- Task 2: Derived values
- Middleware
- get_formatted_datetime_now
- test_validation.py
- main.js
- extract.py
- test_operations_services.py
- get
- 2026-09-18-service-integration-design.md
- .get_bikes
- .write_delete_record
- run_all_migrations
- Decided
- validateDateInput
- 2026-09-25-service-integration-test-findings.md
- Service integration: incidents, workplans and services
- test_migration.py
- derived_values
- test_sync.py
- Rewrite roadmap: new UI, restructured backend, exposed API
- dumps
- stored_state
- test_services_rules.py
- utils.py
- test_health.py
- service-integration-reviewer-to-docs-maintainer.md
- test_workplans_incidents_rules.py
- service-integration-fullstack-to-reviewer.md
- CLAUDE.md
- test_ride_at_install_and_service_timestamps_counts_on_both_sides
- health-check-reviewer-to-docs-maintainer.md
- test_recalculation.py
- Git Workflow Rules
- Fullstack Developer -> Code Reviewer Handover
- CLAUDE.md
- Development Commands
- Handover Template
- insert_planned_service_for_migration
- db_migration.py
- Database Expert Agent
- UX Designer Agent
- D. Design questions to decide before coding
- _new_ids
- test_operations_components.py
- migrate_workplans_to_planned_services
- test_render.py
- Code Reviewer -> Docs Maintainer Handover
- migrate_database
- migrate_incidents_workplan_link
- Handover Communication
- Fullstack Developer Agent
- Product Manager Agent
- assert_refused_after_setup
- Standard Development Workflow
- Handovers Directory Guide
- compare.py
- Architect Agent
- Architecture Overview
- fake_oauth.py
- test_validate_history_record_refuses_retiring_before_latest_service
- test_validate_history_record_refuses_unknown_history_record
- code-reviewer.md
- migrate_component_history_notes
- migrate_component_types_time_fields
- snapshot_delta
- BusinessLogic
- migrate_components_time_fields
- migrate_services_workplan_link
- get_button_order
- healthcheck.py
- Docs Maintainer Agent
- Results
- sortColumn
- test_validate_history_record_refuses_edit_before_previous_record
- migrate_workplans_name_column
- Service integration (#351) - fullstack to code-reviewer
- .read_bike_name
- .read_component
- test_validate_history_record_refuses_edit_after_next_record
- test_validate_history_record_refuses_first_record_after_first_service
- ErrorRecorder
- validateComponentThresholds
- test_validate_history_record_accepts_valid_input
- test_validate_quick_swap_refuses_component_without_bike
- test_validate_quick_swap_refuses_retiring_with_planned_services
- test_validate_collection_refuses_unknown_collection
- test_validate_collection_refuses_unknown_component
- test_validate_collection_refuses_component_in_other_collection
- get_filtered_log
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
- .write_workplan
- test_validate_history_record_refuses_unknown_component
- conftest
- health-check-fullstack-to-reviewer.md
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
- Service integration (#351): findings from the manual test walkthrough
- read_config
- Stage 1 Foundation Handover
- dataset.py
- _assert_new_component
- build_dataset
- detect_layout
- Development Notes
- Code Style & Standards
- Testing Requirements
- test_refusal_changes_nothing
- test_install_component
- test_uninstall_component
- test_retire_component
- test_update_history_record
- test_create_component_type
- test_update_component_type
- test_delete_completed_service
- test_delete_component_type
- test_write_config_button_sorting
- test_write_config_system_settings
- test_modify_component_details
- test_update_completed_service
- test_update_service_revert_to_planned
- test_update_collection
- test_change_collection_status_installed
- test_create_service_record_as_planned
- test_complete_services
- test_missing_database_file_makes_app_unhealthy

## God Nodes (most connected - your core abstractions)
1. `DatabaseManager` - 72 edges
2. `BusinessLogic` - 67 edges
3. `assert_matches_expected()` - 62 edges
4. `stored_state()` - 26 edges
5. `derived_values()` - 23 edges
6. `run_all_migrations()` - 22 edges
7. `Tests` - 21 edges
8. `Meta` - 20 edges
9. `_stored()` - 19 edges
10. `Task 2: Derived values` - 19 edges

## Surprising Connections (you probably didn't know these)
- `Task 12: Strava sync` --references--> `assert_matches_expected()`  [INFERRED]
  docs/superpowers/plans/2026-11-16-stage-1-foundation.md → tests/fixtures/expected.py
- `Task 1: Integrity package: loader, clock, recalculation, stored-state snapshot` --references--> `AppModules`  [INFERRED]
  docs/superpowers/plans/2026-11-16-stage-1-foundation.md → scripts/integrity/loader.py
- `Task 2: Derived values` --references--> `AppModules`  [INFERRED]
  docs/superpowers/plans/2026-11-16-stage-1-foundation.md → scripts/integrity/loader.py
- `Task 3: Extract and compare CLIs, baseline against master` --references--> `extract()`  [INFERRED]
  docs/superpowers/plans/2026-11-16-stage-1-foundation.md → scripts/integrity/extract.py
- `Decisions Made` --references--> `extract()`  [INFERRED]
  .handovers/stages/stage-1-foundation-handover.md → scripts/integrity/extract.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Service integration spec, implementation, test and review cycle** — docs_superpowers_specs_2026_09_18_service_integration_design, handovers_fullstack_service_integration_fullstack_to_reviewer, docs_superpowers_plans_2026_09_25_service_integration_test_findings, tests_test_protocol_services, handovers_review_service_integration_reviewer_to_docs_maintainer [EXTRACTED 1.00]

## Communities (196 total, 94 thin omitted)

### Community 0 - "main.py"
Cohesion: 0.07
Nodes (41): contextlib, fastapi_responses, fastapi_staticfiles, fastapi_templating, post, add_collection(), add_incident_record(), add_planned_services() (+33 more)

### Community 1 - "scheduler.py"
Cohesion: 0.11
Nodes (19): apscheduler_schedulers_asyncio, apscheduler_triggers_cron, apscheduler_triggers_interval, FastAPI, lifespan(), Manage application startup and shutdown, Module for middleware, Initialize and start the APScheduler instance (+11 more)

### Community 2 - "Tests"
Cohesion: 0.08
Nodes (28): Phase C: tests, branch `feature/stage1-tests`, Task 10: Operation scenarios: components, history, quick swap, types, config, Task 11: Operation scenarios: services, workplans, incidents, collections, Task 12: Strava sync, Task 13: Page render tests, Task 14: Rules, health and migration rewritten; old tests removed, Constraints, Tests (+20 more)

### Community 3 - "code-reviewer -> docs-maintainer Handover"
Cohesion: 0.07
Nodes (27): Technical debt tracked in issue #356, Context, Docs changes, docs-maintainer -> Human Handover, Double-check, Files to commit, Option A: one commit, Option B: three commits (main.js needs `git add -p`) (+19 more)

### Community 4 - "Meta"
Cohesion: 0.10
Nodes (35): Model, peewee, Module for interaction with a Sqlite database, BaseModel, Bikes, Collections, ComponentHistory, Components (+27 more)

### Community 5 - "replace_ids"
Cohesion: 0.12
Nodes (22): Task 8: Test foundation and synthetic dataset, Decisions Made, Replace new IDs in dict keys and values, lists and tuples, at any depth. Only…, replace_ids(), _replace_text(), test_dataset_builds_and_recalculates(), app(), client() (+14 more)

### Community 6 - "assert_matches_expected"
Cohesion: 0.07
Nodes (28): expected_dir(), fixture, test_difference_fails(), test_existing_file_is_never_overwritten(), test_missing_file_fails_naming_record_expected(), test_missing_file_is_recorded_when_asked(), svc-wheel-planned completed through the edit form on 2026-11-01 08:00, keeping…, inc-drivetrain edited in full: severity Monitor, the cassette removed, a new… (+20 more)

### Community 7 - "DatabaseManager"
Cohesion: 0.04
Nodes (24): DatabaseManager, Method to sum distance for a given set of rides, Method to read all component objects (not tuples), Class to interact with a SQLite database through Peewee, Method to read a subset of records from the component history table, Method to read completed services for a component, used by health computation, Method to check that the database can be read. Reads a real table, since SELECT…, Method to retrieve record for a specific entry in the service log (+16 more)

### Community 8 - "Task 2: Derived values"
Cohesion: 0.10
Nodes (23): Task 2: Derived values, Result extractor, Method to produce payload for page component overview, Method to produce payload for page component details, Calculate lifetime and service triggers for a component, Method to check if a bike has all mandatory components and respects max…, Method to produce payload for page bike overview, Method to create component-to-collection mapping dictionaries (+15 more)

### Community 9 - "Middleware"
Cohesion: 0.16
Nodes (11): BaseHTTPMiddleware, Exception, exception_handler, http_exception_handler(), Function to catch http errors from Uvicorn and return them to the middleware, Middleware, Request, Class to handle exceptions that breaks the program and should be shown to the… (+3 more)

### Community 10 - "get_formatted_datetime_now"
Cohesion: 0.09
Nodes (22): End of Phase B (after Tasks 5-7: version from git tag, config from `VELO_SUPERVISOR_CONFIG`, new Docker image), Progress log, Task 3, step 5: failing-comparison proof, Task 3, step 6: baseline dev vs master, Task 4, step 9: src layout vs master, Method to update component lifetime and service status when no installation…, Method to update status for a given bike based on component service and…, Method to update component details (+14 more)

### Community 12 - "main.js"
Cohesion: 0.09
Nodes (9): editCollection(), handleUpdate(), initializeCollectionsSearch(), updateRowVisibility(), initializeComponentSelector(), NOTE: All collection details page handlers are in the "Functions used on…, IMPORTANT: Remove readonly - allow manual typing, showToast() (+1 more)

### Community 13 - "extract.py"
Cohesion: 0.16
Nodes (19): frozen_clock(), Freeze time at FIXED_NOW in UTC so date-dependent calculations are reproducible, extract(), main(), Path, Run one checkout against a copy of db_path and return its stored and derived…, AppModules, _forget_app_modules() (+11 more)

### Community 14 - "test_operations_services.py"
Cohesion: 0.18
Nodes (15): dataclasses, fastapi_testclient, importlib, json, os, pathlib, pytest, sys (+7 more)

### Community 15 - "get"
Cohesion: 0.11
Nodes (24): get, add_history_record(), collection_details(), component_overview(), component_types_overview(), help_page(), incident_reports(), Request (+16 more)

### Community 16 - "2026-09-18-service-integration-design.md"
Cohesion: 0.13
Nodes (17): Blank values always NULL, never empty strings, Completed to Planned revert uses deletion recalculation, Notes on component status change (#349), Workplan bike/components derived through services, Effective planned date fallback, Migration steps 12-16 (idempotent check_/migrate_ pairs), Plan and complete services modals sharing one JS helper, Planned services invisible to component health (+9 more)

### Community 17 - ".get_bikes"
Cohesion: 0.16
Nodes (7): Method to authenticate and get data from Stravas gear API, Method to prepare a list of rides, Method to prepare a list of bikes, Method to read oauth options from file, Method to save oauth options to file, Method to authenticate and get data from Stravas activities API, Method to authenticate and get the full list of bike ids from the athlete's…

### Community 18 - ".write_delete_record"
Cohesion: 0.12
Nodes (8): Method to retrieve record for a single component type, Method to retrieve record for a specific entry in the installation log, Method to retrieve a specific service record, Method to retrieve record for a specific collection, Method to retrieve record for a specific incident report, Method to retrieve record for a specific workplan, Method to write component type record in database, Method to delete a given record and associated records

### Community 19 - "run_all_migrations"
Cohesion: 0.14
Nodes (14): create_collections_table(), create_incidents_table(), create_workplans_table(), populate_component_types_thresholds(), populate_components_thresholds(), Creates the incidents table if it doesn't exist., Creates the workplans table if it doesn't exist., Creates the collections table if it doesn't exist. (+6 more)

### Community 20 - "Decided"
Cohesion: 0.06
Nodes (32): Global Constraints, Phase A: extractor and baseline, branch `feature/stage1-extractor`, Phase B: move, version, config, Docker, branch `feature/stage1-src-layout`, Phase D: template, CI, releases, cleanup, docs, branch `feature/stage1-finish`, Stage 1 Foundation Implementation Plan, Task 15: Template database defaults, Task 16: CI made complete and permanent, Task 17: Release backfill and README (+24 more)

### Community 21 - "validateDateInput"
Cohesion: 0.20
Nodes (9): initializeDatePickers(), initializeIncidentForm(), initializeWorkplanForm(), submitCollectionAjax(), submitComponentAjax(), validateCollectionStatusChange(), validateDateInput(), validateIncidentForm() (+1 more)

### Community 22 - "2026-09-25-service-integration-test-findings.md"
Cohesion: 0.25
Nodes (8): A5: workplan delete blocked while services linked, B3: service modal submittable without completion date, D2: incident modal lists linked services, D4: choose components when creating workplan from incident, Manual walkthrough findings (A/B/C/D groups), Re-test list for the second round, Warn (not block) when resolving incident with planned services, Date picker form.onsubmit wrapper fix

### Community 23 - "Service integration: incidents, workplans and services"
Cohesion: 0.11
Nodes (18): Backend, business_logic.py, Data model, database_manager.py, Decisions, Error handling, Goal, main.js (+10 more)

### Community 24 - "test_migration.py"
Cohesion: 0.26
Nodes (13): columns(), description(), query(), db_migration converts the pre-#351 workplan and incident model to links through…, Old columns become the service integration schema and old links become…, A second run performs no step and leaves the converted tables as they were, The template as shipped migrates to the current schema; a second run performs…, run_migration() (+5 more)

### Community 25 - "derived_values"
Cohesion: 0.17
Nodes (28): _bike_values(), details(), _by_first(), _collection_values(), details(), status(), _component_values(), details() (+20 more)

### Community 27 - "test_sync.py"
Cohesion: 0.11
Nodes (30): fixture, new_session_class(), A FakeOAuth2Session subclass with its own empty call records, _errors(), _gear_requested(), _install(), The Strava sync against synthetic Strava responses. FakeOAuth2Session…, Every activity whose type is not exactly "Ride" is skipped with a warning and… (+22 more)

### Community 28 - "Rewrite roadmap: new UI, restructured backend, exposed API"
Cohesion: 0.05
Nodes (36): Anti-goals, API: separate API, or one set of resources with two formats, API style: FHIR-conformant or FHIR-inspired, Approaches considered, Branch policy during the freeze, Constraints, Delivery: side by side on master, or frozen master and long-running dev, Frontend: server-rendered with htmx, or a JSON API with a separate frontend app (+28 more)

### Community 29 - "dumps"
Cohesion: 0.33
Nodes (5): dumps(), Serialise a state deterministically, keeping non-ASCII characters readable, test_new_ids_are_normalised_in_both_layers(), test_only_the_component_without_history_fails_recalculation(), test_read_functions_raise_no_errors_on_the_dataset()

### Community 30 - "stored_state"
Cohesion: 0.21
Nodes (20): Review Focus, Task 1: Integrity package: loader, clock, recalculation, stored-state snapshot, new_id_map(), normalise_new_ids(), _normalise_value(), Path, Read every table and column straight from SQLite, keyed table, primary key,…, Map each primary key absent from baseline_ids to new:<table>:<n>, numbered in… (+12 more)

### Community 31 - "test_services_rules.py"
Cohesion: 0.07
Nodes (26): parametrize, Service rules: planned services stay out of health, completion and revert,…, Reverting a completed service to planned leaves the component, its other…, Stored changes other than those to the removed service's own row, Uninstalling the cassette reprocesses its services; svc-cassette-2, its newest,…, Setup: a newer cassette service without workplan on 2026-11-01 08:00. Deleting…, The chain's planned service in wp-drivetrain does not block one outside any…, svc-pads-retired cannot be reverted to planned, since its component is retired (+18 more)

### Community 32 - "utils.py"
Cohesion: 0.07
Nodes (46): asyncio, collections, datetime, logging, re, requests_oauthlib, Module to handle business logic, Method to produce payload for page incident reports (+38 more)

### Community 33 - "test_health.py"
Cohesion: 0.14
Nodes (14): database(), logger(), fixture, The health rule: an error logged in the last 24 hours, a failing database or a…, An error logged anywhere reaches the recorder through the root logger, lifespan in main.py sets every root handler to INFO or DEBUG at startup, The recalculation of the dataset logs no error, so the fixture starts healthy, An error logged at the frozen now counts until 24 hours have passed (+6 more)

### Community 34 - "service-integration-reviewer-to-docs-maintainer.md"
Cohesion: 0.18
Nodes (10): Code review -> docs-maintainer Handover, Context, Dead reads read_all_services_by_component / read_all_planned_services, derive_workplan_context computed twice per render, Issues found (none blocking), Recommendations, References, Unescaped innerHTML in renderIncidentServices (+2 more)

### Community 35 - "test_workplans_incidents_rules.py"
Cohesion: 0.09
Nodes (21): Workplan, incident and history rules: links through services, titles, notes,…, wp-brake-check set back to Planned with a full update; completion rules apply…, Components, bikes, progress and title of a workplan come from its services. A…, The chain has svc-chain-planned: retiring is refused and changes nothing,…, inc-drivetrain reaches wp-drivetrain through its two services, one planned and…, The values the workplan, bike, component and collection pages show for planned…, A note is stored on the new record; a note of only spaces is stored as NULL, on…, The cassette retired and replaced by a new one: both new history records carry… (+13 more)

### Community 36 - "service-integration-fullstack-to-reviewer.md"
Cohesion: 0.31
Nodes (8): D1: optional user-entered workplan name, Service integration: services as unit of work (#351), data-incident-status-listener guard, FastAPI/Starlette TemplateResponse argument order fix, Workplan link silently lost bug (process_service_records without workplan_id), Optional workplan_name (migration step 17), db_migration step 16 rebuild before step 17 workplan_name, v0.5.0 release (service integration, health check, uv)

### Community 37 - "CLAUDE.md"
Cohesion: 0.22
Nodes (8): Available Agents, Communication & Output Rules, Debugging & Bug Fixing Rules, Direct Invocation, graphify, Important Notes, Project Overview, Sub-Agent Team

### Community 38 - "test_ride_at_install_and_service_timestamps_counts_on_both_sides"
Cohesion: 0.18
Nodes (21): _bike(), _insert(), Ride time filters are inclusive at both ends, so a ride at an event's exact…, An installed component with no lifetime or service interval rates "Not defined"…, A component uninstalled from a bike is stored with no bike, and the bike status…, Remaining lifetime of zero already counts as exceeded, and an exceeded…, A retired member blocks operations: retired pads plus the installed gravel…, Members installed on two bikes block operations and no single bike is shown:… (+13 more)

### Community 39 - "health-check-reviewer-to-docs-maintainer.md"
Cohesion: 0.25
Nodes (7): Database check reads bikes table, not SELECT 1, Rename read_database_connection to check_database_connection, ErrorRecorder deque bounded to maxlen=20, ErrorRecorder thread safety under Handler.lock, Issues Found, Catching peewee.DatabaseError for corrupt file, test_failing_database_makes_app_unhealthy()

### Community 40 - "test_recalculation.py"
Cohesion: 0.11
Nodes (28): Task 9: Recalculation characterisation, Characterisation of the full recalculation on the synthetic dataset. Every…, A component without installation history keeps the values the alternate method…, Day-based lifetime of a retired component stops at retirement, not at now.…, Each completed service restarts the service interval; lifetime keeps counting.…, Service distances follow the chain across bikes and skip the months it was off.…, Day-based values of an active component count to the frozen now, 2026-11-16…, Bremseklosser bak æøå on gravel since 2025-01-01: 22 x 20 = 440 km; lifetime… (+20 more)

### Community 41 - "Git Workflow Rules"
Cohesion: 0.29
Nodes (7): Branch Strategy, Commit Process, For All Agents, For code-reviewer, For docs-maintainer, For fullstack-developer, Git Workflow Rules

### Community 42 - "Fullstack Developer -> Code Reviewer Handover"
Cohesion: 0.25
Nodes (8): Blockers / Open Questions, Context, Decisions Made, Deliverables, Fullstack Developer -> Code Reviewer Handover, Next Steps for Code Reviewer, References, Verification done

### Community 43 - "CLAUDE.md"
Cohesion: 0.33
Nodes (5): Change Management Rules, Debugging & bug fixing rules (root cause first), graphify knowledge graph usage rules, Agent handover documents (.handovers/), TomSelect multi-select pattern

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

### Community 48 - "Database Expert Agent"
Cohesion: 0.29
Nodes (6): Constraints, Core Responsibilities, Pattern Consistency - CRITICAL, Query Optimization, Schema Changes, Workflow

### Community 49 - "UX Designer Agent"
Cohesion: 0.29
Nodes (6): Core Responsibilities, Design Principles, Specifications to Include, v1 (Before Architect), v2 (After Architect), Workflow

### Community 50 - "D. Design questions to decide before coding"
Cohesion: 0.25
Nodes (8): Code review outcome, 2026-09-26, D. Design questions to decide before coding, Decisions (2026-09-26), Follow-up tweaks asked for on 2026-09-26, Second round of tweaks, 2026-09-26, Status (2026-09-26), Third round of tweaks, 2026-09-26, Warning when resolving an incident with open services, 2026-09-26

### Community 51 - "_new_ids"
Cohesion: 0.11
Nodes (18): _new_ids(), An open incident on bike-gravel for the tire; empty optional fields become…, A planned workplan with a name; no services, so it reaches no bike or component, A workplan from inc-drivetrain with no component selection plans a service for…, Only the selected incident components get a planned service: the cassette, not…, A workplan from inc-squeal, whose only component is the retired pads: the…, Primary keys of table that are not in the dataset, in row order, A selection with none of inc-drivetrain's components plans nothing; the… (+10 more)

### Community 52 - "test_operations_components.py"
Cohesion: 0.08
Nodes (24): _execute(), Characterisation of component, history, quick swap, component type, delete and…, Changing the type recounts both types: Saddle in_use 0, Bottle cage 1. Spare…, Cassette retired on 2026-10-01 08:00 and replaced by a new one created in the…, Deleting a planned service recalculates nothing, Deleting the chain's latest record (road_2) leaves it as uninstalled from bike-…, Deleting a component's only record (no services) makes it not installed through…, Records current behaviour; see #374. Deleting a component's only history record… (+16 more)

### Community 53 - "migrate_workplans_to_planned_services"
Cohesion: 0.25
Nodes (8): check_workplans_affected_columns(), migrate_drop_workplan_affected_columns(), migrate_workplans_to_planned_services(), Check if workplans table still has the affected bike/component columns, Resolve bike and component names, marking components that no longer exist, Convert affected components on planned workplans into planned services,…, Rebuild workplans table without the affected bike/component columns, read_names_for_migration()

### Community 54 - "test_render.py"
Cohesion: 0.24
Nodes (8): parametrize, Each guard of delete_record refuses on the dataset as it is and leaves every…, test_delete_refusal_changes_nothing(), Every page renders for every resource in the dataset, and unknown IDs fail the…, Stage 4 changes the unknown-ID status to 404 (#356), test_every_detail_page_renders(), test_every_overview_page_renders(), test_unknown_ids_today()

### Community 55 - "Code Reviewer -> Docs Maintainer Handover"
Cohesion: 0.25
Nodes (8): Code Reviewer -> Docs Maintainer Handover, Context, Deliverables, Next Steps for Docs Maintainer, References, Resolution (2026-09-27, after review), Verification done, test_recorder_includes_exception_in_message()

### Community 56 - "migrate_database"
Cohesion: 0.33
Nodes (6): find_database_file(), migrate_database(), prompt_for_db_path(), Search for a database file in the user's home directory and subdirectories, Prompt user for database path or filename and verify it exists, Main function to handle the database migration.

### Community 57 - "migrate_incidents_workplan_link"
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

### Community 61 - "assert_refused_after_setup"
Cohesion: 0.25
Nodes (8): assert_refused_after_setup(), The refusal returns expected and adds nothing to the delta the setup left, Setup: coll-mixed reduced to the retired pads with update_collection, which…, Setup: coll-mixed reduced to the rear wheel, which has svc-wheel-planned.…, Not a validate_collection branch: change_collection_status refuses before…, test_change_collection_status_refuses_empty_collection(), test_validate_collection_refuses_retired_member(), test_validate_collection_refuses_retiring_with_planned_services()

### Community 62 - "Standard Development Workflow"
Cohesion: 0.50
Nodes (4): For Bug Fixes, For Documentation Updates, For New Features, Standard Development Workflow

### Community 63 - "Handovers Directory Guide"
Cohesion: 0.33
Nodes (5): Creating Handovers, Directory Structure, Finding Handovers, Handovers Directory, Rules

### Community 64 - "compare.py"
Cohesion: 0.18
Nodes (18): argparse, Task 3: Extract and compare CLIs, baseline against master, diff(), _error_paths(), main(), present_on_both_sides(), Path, One line per difference as 'path: left=... right=...', paths joined with '/ (+10 more)

### Community 65 - "Architect Agent"
Cohesion: 0.40
Nodes (4): Core Responsibilities, Handover Content, Principles, Workflow

### Community 66 - "Architecture Overview"
Cohesion: 0.40
Nodes (5): Architecture Overview, Configuration, Core Components, Key Features, Project Structure

### Community 67 - "fake_oauth.py"
Cohesion: 0.23
Nodes (5): FakeOAuth2Session, FakeResponse, load_fixture(), A stand-in for requests_oauthlib.OAuth2Session that answers from…, urllib_parse

### Community 70 - "code-reviewer.md"
Cohesion: 0.22
Nodes (8): Issues Found, Key Checks, Output Format, Recommendations, Review Philosophy, Review Process, Summary, service()

### Community 71 - "migrate_component_history_notes"
Cohesion: 0.50
Nodes (4): check_component_history_notes_column(), migrate_component_history_notes(), Check if component_history table needs notes column, Add notes column to component_history table

### Community 72 - "migrate_component_types_time_fields"
Cohesion: 0.50
Nodes (4): check_component_types_time_columns(), migrate_component_types_time_fields(), Check if ComponentTypes table needs time-based fields migration, Add time-based fields to ComponentTypes table

### Community 73 - "snapshot_delta"
Cohesion: 0.25
Nodes (12): _leaves(), Every leaf path that differs between two snapshots, as {path: {"before": x,…, snapshot_delta(), test_added_and_removed_rows_list_every_leaf(), test_changed_value(), test_empty_dict_is_a_value(), test_key_with_slash_is_refused(), test_list_is_one_value() (+4 more)

### Community 74 - "BusinessLogic"
Cohesion: 0.07
Nodes (17): BusinessLogic, Method to update a component history record with validation, Method to update collection, Method to change status of all components in a collection, Method to build the report used by the plan services and complete services…, Method to complete planned services with one service date, keeping their…, Method to determine which factor triggered a warning status, Method to update incident record (supports full or partial updates) (+9 more)

### Community 75 - "migrate_components_time_fields"
Cohesion: 0.50
Nodes (4): check_components_time_columns(), migrate_components_time_fields(), Check if Components table needs time-based fields migration, Add time-based fields to Components table and populate threshold_km

### Community 76 - "migrate_services_workplan_link"
Cohesion: 0.50
Nodes (4): check_services_workplan_column(), migrate_services_workplan_link(), Check if Services table needs workplan_id column, Add workplan_id column to Services table for workplan hub integration

### Community 77 - "get_button_order"
Cohesion: 0.20
Nodes (10): bike_details(), component_details(), config_overview(), Endpoint for component details page, Endpoint for component types page, Endpoint for bike details page, get_button_order(), get_button_sorting_config() (+2 more)

### Community 78 - "healthcheck.py"
Cohesion: 0.50
Nodes (3): Health check run by the Docker daemon, exit code 0 means healthy and 1 means…, urllib_error, urllib_request

### Community 79 - "Docs Maintainer Agent"
Cohesion: 0.50
Nodes (3): Core Responsibilities, Documentation Rules, Workflow

### Community 81 - "Results"
Cohesion: 0.29
Nodes (7): 2026-09-25, first walkthrough, human, 2026-09-26, regression against the baseline database, Claude, 2026-09-27, second walkthrough, human, Preparation, Results, Scope, Test Protocol: Planned services, workplans and incidents

### Community 82 - "sortColumn"
Cohesion: 0.29
Nodes (8): initializeCollectionsSorting(), sortColumn(), initializeWorkplanTable(), setupIncidentTableSorting(), setupWorkplanSearch(), setupWorkplanStatusFiltering(), setupWorkplanTableSorting(), updateWorkplansVisibility()

### Community 84 - "migrate_workplans_name_column"
Cohesion: 0.50
Nodes (4): check_workplans_name_column(), migrate_workplans_name_column(), Check if workplans table needs the workplan_name column, Add the optional user given name to the workplans table, existing workplans…

### Community 85 - "Service integration (#351) - fullstack to code-reviewer"
Cohesion: 0.18
Nodes (11): Bugs found and fixed, Files, Key decisions, Known limitations, Next steps, Regression evidence, 2026-09-26, Reuse, Second round, 2026-09-26, after the manual walkthrough (+3 more)

### Community 87 - ".read_bike_name"
Cohesion: 0.33
Nodes (3): Method to retrieve record for a specific bike, Method to create or update bike data to the database, Method to get the name of a bike based on bike id

### Community 88 - ".read_component"
Cohesion: 0.33
Nodes (3): Method to get component names based on list of ids, Method to retrieve record for a specific component, Method to create or update component data to the database

### Community 91 - "ErrorRecorder"
Cohesion: 0.18
Nodes (8): health(), Endpoint for the Docker health check, returns 503 if errors were logged the…, ErrorRecorder, get_health_status(), Logging handler that keeps the most recent error records in memory for the…, Method to store error records and ignore lower levels. Filters here instead of…, Method to get error records newer than the given number of hours, Function to assess application health from errors logged the last 24 hours and…

### Community 92 - "validateComponentThresholds"
Cohesion: 0.40
Nodes (5): addFormValidation(), clearValidationErrors(), showFieldError(), validateComponentThresholds(), validateQuickSwapForm()

### Community 99 - "get_filtered_log"
Cohesion: 0.50
Nodes (4): get_filtered_log(), Endpoint to read log and return only business events, Function to get filtered log records, read_filtered_logs()

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

### Community 153 - "health-check-fullstack-to-reviewer.md"
Cohesion: 0.22
Nodes (7): Docker HEALTHCHECK against /health, Log levels drive container health, Health check for Docker daemon (#103), In-memory 24h error record, ERROR vs WARNING log level rule, Separate healthcheck.py instead of curl, get_health_status in utils, DB read in database_manager

### Community 167 - "Service integration (#351): findings from the manual test walkthrough"
Cohesion: 0.22
Nodes (9): A. Questions to answer from the code, no change expected, Answers (read from the code 2026-09-25), B. Bugs to fix, C. Interface changes the user asked for, Extra wording fixes asked for on 2026-09-26, Service integration (#351): findings from the manual test walkthrough, Status (2026-09-26), Status (2026-09-26) (+1 more)

### Community 168 - "read_config"
Cohesion: 0.25
Nodes (9): Configuration file location, config_path(), parse_button_sorting(), Function to get the configuration file path from VELO_SUPERVISOR_CONFIG,…, Function to read configuration file, Function to parse button sorting data from form submission, Function to update configuration file based on which form was submitted, read_config() (+1 more)

### Community 169 - "Stage 1 Foundation Handover"
Cohesion: 0.25
Nodes (7): Blockers / Open Questions, Context, Deliverables, Next Steps, References, Stage 1 Foundation Handover, Switch-over steps for the Pi (Stage 6)

### Community 170 - "dataset.py"
Cohesion: 0.33
Nodes (6): shutil, sqlite3, DatasetIds, monthly_rides(), _months(), Synthetic dataset that characterisation, rule, page and Strava tests start…

### Community 171 - "_assert_new_component"
Cohesion: 0.29
Nodes (7): _assert_new_component(), Chain swapped for a spare chain on 2026-10-01 08:00; the old chain becomes not…, An installed component gets a history record and is recalculated at once. Road…, A component created as not installed gets no history; the alternate method sets…, test_create_installed_component(), test_create_not_installed_component(), test_quick_swap_to_not_installed_with_existing_component()

### Community 172 - "build_dataset"
Cohesion: 0.29
Nodes (7): dataset_db(), build_dataset(), Path, Write the dataset into a migrated copy of the template database at db_path, old_db(), fixture, The dataset with the four tables in their pre-#351 shape and old-model rows

### Community 173 - "detect_layout"
Cohesion: 0.33
Nodes (6): Task 4: Move to the src layout, detect_layout(), Path, Tell the pre-restructure flat layout from the package layout, test_detect_layout_package(), test_detect_layout_rejects_unknown()

### Community 174 - "Development Notes"
Cohesion: 0.40
Nodes (5): Database Schema Changes, Development Notes, Docker Development, Logging, Technical Debt

### Community 175 - "Code Style & Standards"
Cohesion: 0.50
Nodes (4): Code Style & Standards, Database, Frontend, Python (Backend)

### Community 176 - "Testing Requirements"
Cohesion: 0.67
Nodes (3): Before Creating Handover, For fullstack-developer, Testing Requirements

### Community 177 - "test_refusal_changes_nothing"
Cohesion: 0.67
Nodes (3): parametrize, Each validation refuses on the dataset as it is and leaves every value unchanged, test_refusal_changes_nothing()

## Ambiguous Edges - Review These
- `tests/conftest.py` → `Manual testing protocols approach`  [AMBIGUOUS]
  tests/README.md · relation: conceptually_related_to

## Knowledge Gaps
- **252 isolated node(s):** `DatasetIds`, `GitHub Issues Tracker`, `Velo Supervisor 2000 (Project)`, `Strava OAuth Token Setup (Step 2)`, `Semantic Versioning (SemVer)` (+247 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 836 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **94 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `tests/conftest.py` and `Manual testing protocols approach`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **Why does `DatabaseManager` connect `DatabaseManager` to `.write_component_service_status`, `.write_history_record`, `Meta`, `Task 2: Derived values`, `.write_delete_record`, `.write_incident_record`, `.write_service_record`, `.write_workplan`, `utils.py`, `.read_bike_name`, `.read_component`, `.count_component_types_in_use`, `.read_all_component_types`, `.read_all_workplans`, `.read_bike_id_recent_component_history`, `.read_latest_history_record`, `.read_latest_service_record`, `.read_matching_rides`, `.read_oldest_history_record`, `.read_open_incidents`, `.read_planned_services_by_workplan`, `.read_recent_rides`, `.read_services_by_incident`, `.read_services_by_workplan`, `.read_subset_components`, `.read_subset_installed_components`, `.write_bike_service_status`, `.write_component_distance`?**
  _High betweenness centrality (0.123) - this node is a cross-community bridge._
- **Why does `Manual testing protocols approach` connect `2026-09-18-service-integration-design.md` to `test_operations_services.py`?**
  _High betweenness centrality (0.117) - this node is a cross-community bridge._
- **Why does `test_failing_database_makes_app_unhealthy()` connect `health-check-reviewer-to-docs-maintainer.md` to `test_health.py`?**
  _High betweenness centrality (0.082) - this node is a cross-community bridge._
- **Are the 9 inferred relationships involving `DatabaseManager` (e.g. with `Bikes` and `Collections`) actually correct?**
  _`DatabaseManager` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Are the 28 inferred relationships involving `assert_matches_expected()` (e.g. with `Task 12: Strava sync` and `test_change_collection_status_installed()`) actually correct?**
  _`assert_matches_expected()` has 28 INFERRED edges - model-reasoned connections that need verification._
- **Are the 6 inferred relationships involving `stored_state()` (e.g. with `_new_ids()` and `snapshot_now()`) actually correct?**
  _`stored_state()` has 6 INFERRED edges - model-reasoned connections that need verification._