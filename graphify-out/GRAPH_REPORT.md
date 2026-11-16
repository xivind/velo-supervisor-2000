# Graph Report - velo-supervisor-2000  (2026-11-16)

## Corpus Check
- 60 files · ~165,080 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 12 file(s) not represented in the graph (top: (none) 5, .example 1, .sqlite 1)

## Summary
- 1238 nodes · 2019 edges · 135 communities (80 shown, 55 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 175 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `b27fd46c`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- main.py
- scheduler.py
- get
- seed_component
- Meta
- DatabaseManager
- .update_rides_bulk
- Version Bump Workflow
- get_formatted_datetime_now
- main.js
- Task 2: Derived values
- .complete_services
- service-integration-reviewer-to-docs-maintainer.md
- insert
- BusinessLogic
- Strava
- 2026-09-18-service-integration-design.md
- .write_delete_record
- extract.py
- Middleware
- health-check-fullstack-to-reviewer.md
- db_migration.py
- Stage 1 Foundation Handover
- Service integration: incidents, workplans and services
- test_migration.py
- code-reviewer -> docs-maintainer Handover
- derived_values
- validateDateInput
- Rewrite roadmap: new UI, restructured backend, exposed API
- Task 1: Integrity package: loader, clock, recalculation, stored-state snapshot
- compare.py
- Stage 1: Foundation
- Decided
- Service integration (#351) - fullstack to code-reviewer
- GitHub Issues Tracker
- utils.py
- sortColumn
- CLAUDE.md
- Git Workflow Rules
- Stages
- .read_bike_name
- CLAUDE.md
- Code Reviewer Agent
- .read_component
- Phase D: template, CI, releases, cleanup, docs, branch `feature/stage1-finish`
- Handover Template
- Service integration (#351): findings from the manual test walkthrough
- get_health_status
- Database Expert Agent
- UX Designer Agent
- Task 8: Test foundation and synthetic dataset
- test_health.py
- Code Reviewer -> Docs Maintainer Handover
- Fullstack Developer -> Code Reviewer Handover
- validateComponentThresholds
- ErrorRecorder
- Approaches considered
- Approaches
- Handover Communication
- Fullstack Developer Agent
- Product Manager Agent
- service-integration-fullstack-to-reviewer.md
- health-check-reviewer-to-docs-maintainer.md
- Handovers Directory Guide
- version.py
- Architect Agent
- Architecture Overview
- Development Commands
- Development Notes
- Results
- Standard Development Workflow
- .update_workplan
- get_filtered_log
- update_config
- 2026-09-25-service-integration-test-findings.md
- cleanup
- renderPreview
- initializeIncidentTable
- handleOldComponentChange
- Docs Maintainer Agent
- Code Style & Standards
- D. Design questions to decide before coding
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
- read_config
- Testing Requirements
- .check_database_connection
- Strava OAuth Token Setup (Step 2)
- Branching and Versioning
- Changelog and Project Board
- integrity_clock
- integrity_loader
- integrity_recalculate
- integrity_snapshot
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
6. `derived_values()` - 20 edges
7. `Meta` - 20 edges
8. `seed_rides()` - 20 edges
9. `Task 2: Derived values` - 18 edges
10. `insert()` - 16 edges

## Surprising Connections (you probably didn't know these)
- `Decisions Made` --references--> `extract()`  [INFERRED]
  .handovers/stages/stage-1-foundation-handover.md → scripts/integrity/extract.py
- `Task 1: Integrity package: loader, clock, recalculation, stored-state snapshot` --references--> `frozen_clock()`  [INFERRED]
  docs/superpowers/plans/2026-11-16-stage-1-foundation.md → scripts/integrity/clock.py
- `Task 3: Extract and compare CLIs, baseline against master` --references--> `frozen_clock()`  [INFERRED]
  docs/superpowers/plans/2026-11-16-stage-1-foundation.md → scripts/integrity/clock.py
- `Task 8: Test foundation and synthetic dataset` --references--> `frozen_clock()`  [INFERRED]
  docs/superpowers/plans/2026-11-16-stage-1-foundation.md → scripts/integrity/clock.py
- `Task 3, step 5: failing-comparison proof` --references--> `diff()`  [INFERRED]
  .handovers/stages/stage-1-foundation-handover.md → scripts/integrity/compare.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Service integration spec, implementation, test and review cycle** — docs_superpowers_specs_2026_09_18_service_integration_design, handovers_fullstack_service_integration_fullstack_to_reviewer, docs_superpowers_plans_2026_09_25_service_integration_test_findings, tests_test_protocol_services, handovers_review_service_integration_reviewer_to_docs_maintainer [EXTRACTED 1.00]

## Communities (135 total, 55 thin omitted)

### Community 0 - "main.py"
Cohesion: 0.07
Nodes (40): asyncio, fastapi_responses, fastapi_staticfiles, fastapi_templating, post, add_collection(), add_incident_record(), add_planned_services() (+32 more)

### Community 1 - "scheduler.py"
Cohesion: 0.09
Nodes (23): apscheduler_schedulers_asyncio, apscheduler_triggers_cron, apscheduler_triggers_interval, datetime, FastAPI, logging, requests_oauthlib, lifespan() (+15 more)

### Community 2 - "get"
Cohesion: 0.08
Nodes (34): get, add_history_record(), bike_details(), collection_details(), component_details(), component_overview(), component_types_overview(), config_overview() (+26 more)

### Community 3 - "seed_component"
Cohesion: 0.15
Nodes (31): add_twin_component(), Planned services must be invisible to health computation, Rides before and after the service dates used below, so distances are not zero, Second installed component on bike-1 with the same settings as comp-1, Create one bike and one installed component with an installation record, seed_component(), seed_rides(), snapshot_health() (+23 more)

### Community 4 - "Meta"
Cohesion: 0.10
Nodes (35): Model, peewee, Module for interaction with a Sqlite database, BaseModel, Bikes, Collections, ComponentHistory, Components (+27 more)

### Community 5 - "DatabaseManager"
Cohesion: 0.04
Nodes (24): DatabaseManager, Method to sum distance for a given set of rides, Method to read all component objects (not tuples), Class to interact with a SQLite database through Peewee, Method to read a subset of records from the component history table, Method to read completed services for a component, used by health computation, Method to check that the database can be read. Reads a real table, since SELECT…, Method to retrieve record for a specific entry in the service log (+16 more)

### Community 7 - "Version Bump Workflow"
Cohesion: 0.11
Nodes (18): GITHUB_TOKEN, jobs, run-script, name, branches, branches, runs-on, steps (+10 more)

### Community 8 - "get_formatted_datetime_now"
Cohesion: 0.10
Nodes (17): Constraints, Method to update component lifetime and service status when no installation…, Method to update status for a given bike based on component service and…, Method to calculate distance and bike id for history records, Method to update a service record, including status changes in both directions, Method to recalculate a component after a completed service is deleted or…, Method to calculate distance and bike id for service records, Method to compute component status using threshold logic (+9 more)

### Community 9 - "main.js"
Cohesion: 0.09
Nodes (9): editCollection(), handleUpdate(), initializeCollectionsSearch(), updateRowVisibility(), initializeComponentSelector(), NOTE: All collection details page handlers are in the "Functions used on…, IMPORTANT: Remove readonly - allow manual typing, showToast() (+1 more)

### Community 10 - "Task 2: Derived values"
Cohesion: 0.10
Nodes (17): Task 2: Derived values, Result extractor, Method to update collection, Method to produce payload for page component overview, Method to determine which factor triggered a warning status, Calculate lifetime and service triggers for a component, Method to produce payload for page bike overview, Calculate status flags for a collection based on its components. (+9 more)

### Community 12 - "service-integration-reviewer-to-docs-maintainer.md"
Cohesion: 0.18
Nodes (10): Code review -> docs-maintainer Handover, Context, Dead reads read_all_services_by_component / read_all_planned_services, derive_workplan_context computed twice per render, Issues found (none blocking), Recommendations, References, Unescaped innerHTML in renderIncidentServices (+2 more)

### Community 13 - "insert"
Cohesion: 0.12
Nodes (23): contextlib, Task 13: Page render tests, json, os, pathlib, pytest, frozen_clock(), Freeze time at FIXED_NOW in UTC so date-dependent calculations are reproducible (+15 more)

### Community 14 - "BusinessLogic"
Cohesion: 0.07
Nodes (36): Phase C: tests, branch `feature/stage1-tests`, Task 10: Operation scenarios: components, history, quick swap, types, config, Task 11: Operation scenarios: services, workplans, incidents, collections, Task 12: Strava sync, Task 14: Rules, health and migration rewritten; old tests removed, Task 9: Recalculation characterisation, Tests, BusinessLogic (+28 more)

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
Cohesion: 0.11
Nodes (24): dataclasses, Task 4: Move to the src layout, importlib, extract(), main(), Path, Run one checkout against a copy of db_path and return its stored and derived…, AppModules (+16 more)

### Community 19 - "Middleware"
Cohesion: 0.16
Nodes (11): BaseHTTPMiddleware, Exception, exception_handler, http_exception_handler(), Function to catch http errors from Uvicorn and return them to the middleware, Middleware, Request, Class to handle exceptions that breaks the program and should be shown to the… (+3 more)

### Community 20 - "health-check-fullstack-to-reviewer.md"
Cohesion: 0.22
Nodes (7): Docker HEALTHCHECK against /health, Log levels drive container health, Health check for Docker daemon (#103), In-memory 24h error record, ERROR vs WARNING log level rule, Separate healthcheck.py instead of curl, get_health_status in utils, DB read in database_manager

### Community 21 - "db_migration.py"
Cohesion: 0.04
Nodes (71): check_component_history_notes_column(), check_component_types_columns(), check_component_types_time_columns(), check_components_time_columns(), check_incidents_workplan_column(), check_incidents_workplan_column_present(), check_services_integration_columns(), check_services_workplan_column() (+63 more)

### Community 22 - "Stage 1 Foundation Handover"
Cohesion: 0.17
Nodes (11): Blockers / Open Questions, Context, Decisions Made, Deliverables, Next Steps, Progress log, References, Stage 1 Foundation Handover (+3 more)

### Community 23 - "Service integration: incidents, workplans and services"
Cohesion: 0.11
Nodes (18): Backend, business_logic.py, Data model, database_manager.py, Decisions, Error handling, Goal, main.js (+10 more)

### Community 24 - "test_migration.py"
Cohesion: 0.32
Nodes (11): columns(), create_old_schema(), Migration converts the old workplan/incident model to services, Seed workplans, incidents and services in the pre-#351 shape, Recreate services, workplans, incidents and component_history as they were…, run_migration(), seed_old_data(), snapshot() (+3 more)

### Community 25 - "code-reviewer -> docs-maintainer Handover"
Cohesion: 0.07
Nodes (28): v0.5.0.ca636f8, Technical debt tracked in issue #356, Context, Docs changes, docs-maintainer -> Human Handover, Double-check, Files to commit, Option A: one commit (+20 more)

### Community 26 - "derived_values"
Cohesion: 0.17
Nodes (28): _bike_values(), details(), _by_first(), _collection_values(), details(), status(), _component_values(), details() (+20 more)

### Community 27 - "validateDateInput"
Cohesion: 0.20
Nodes (9): initializeDatePickers(), initializeIncidentForm(), initializeWorkplanForm(), submitCollectionAjax(), submitComponentAjax(), validateCollectionStatusChange(), validateDateInput(), validateIncidentForm() (+1 more)

### Community 28 - "Rewrite roadmap: new UI, restructured backend, exposed API"
Cohesion: 0.20
Nodes (10): Anti-goals, Branch policy during the freeze, Constraints, Goals, Issue map, Left to each stage, Non-goals, Rewrite roadmap: new UI, restructured backend, exposed API (+2 more)

### Community 29 - "Task 1: Integrity package: loader, clock, recalculation, stored-state snapshot"
Cohesion: 0.12
Nodes (24): Global Constraints, Phase A: extractor and baseline, branch `feature/stage1-extractor`, Review Focus, Stage 1 Foundation Implementation Plan, Task 1: Integrity package: loader, clock, recalculation, stored-state snapshot, re, dumps(), normalise_new_ids() (+16 more)

### Community 30 - "compare.py"
Cohesion: 0.19
Nodes (17): argparse, Task 3: Extract and compare CLIs, baseline against master, diff(), _error_paths(), main(), present_on_both_sides(), Path, One line per difference as 'path: left=... right=...', paths joined with '/ (+9 more)

### Community 31 - "Stage 1: Foundation"
Cohesion: 0.22
Nodes (7): Anti-goals, Done when, Goals, Intent, Left to the builder, Non-goals, Stage 1: Foundation

### Community 32 - "Decided"
Cohesion: 0.22
Nodes (9): CI, Comparison against master, Decided, Docker, Legacy files removed, Release notes backfill and README cleanup, Stage handover, Target layout (+1 more)

### Community 33 - "Service integration (#351) - fullstack to code-reviewer"
Cohesion: 0.18
Nodes (11): Bugs found and fixed, Files, Key decisions, Known limitations, Next steps, Regression evidence, 2026-09-26, Reuse, Second round, 2026-09-26, after the manual walkthrough (+3 more)

### Community 35 - "utils.py"
Cohesion: 0.08
Nodes (46): collections, Module to handle business logic, Method to produce payload for page component details, Method to produce payload for page incident reports, Method to produce payload for workplan details page, Method to read content of components table as formatted tuples, build_incident_service_entry(), calculate_elapsed_days() (+38 more)

### Community 36 - "sortColumn"
Cohesion: 0.29
Nodes (8): initializeCollectionsSorting(), sortColumn(), initializeWorkplanTable(), setupIncidentTableSorting(), setupWorkplanSearch(), setupWorkplanStatusFiltering(), setupWorkplanTableSorting(), updateWorkplansVisibility()

### Community 37 - "CLAUDE.md"
Cohesion: 0.22
Nodes (8): Available Agents, Communication & Output Rules, Debugging & Bug Fixing Rules, Direct Invocation, graphify, Important Notes, Project Overview, Sub-Agent Team

### Community 38 - "Git Workflow Rules"
Cohesion: 0.29
Nodes (7): Branch Strategy, Commit Process, For All Agents, For code-reviewer, For docs-maintainer, For fullstack-developer, Git Workflow Rules

### Community 39 - "Stages"
Cohesion: 0.29
Nodes (7): Stage 1: Foundation, Stage 2: Design, Stage 3: Architecture, Stage 4: Backend refactor, Stage 5: New frontend and features, Stage 6: Switch-over, Stages

### Community 40 - ".read_bike_name"
Cohesion: 0.33
Nodes (3): Method to retrieve record for a specific bike, Method to create or update bike data to the database, Method to get the name of a bike based on bike id

### Community 41 - "CLAUDE.md"
Cohesion: 0.33
Nodes (5): Change Management Rules, Debugging & bug fixing rules (root cause first), graphify knowledge graph usage rules, Agent handover documents (.handovers/), TomSelect multi-select pattern

### Community 42 - "Code Reviewer Agent"
Cohesion: 0.25
Nodes (7): Issues Found, Key Checks, Output Format, Recommendations, Review Philosophy, Review Process, Summary

### Community 43 - ".read_component"
Cohesion: 0.33
Nodes (3): Method to get component names based on list of ids, Method to retrieve record for a specific component, Method to create or update component data to the database

### Community 44 - "Phase D: template, CI, releases, cleanup, docs, branch `feature/stage1-finish`"
Cohesion: 0.33
Nodes (6): Phase D: template, CI, releases, cleanup, docs, branch `feature/stage1-finish`, Task 15: Template database defaults, Task 16: CI made complete and permanent, Task 17: Release backfill and README, Task 18: Legacy removed, Task 19: Docs, final comparison, handover

### Community 45 - "Handover Template"
Cohesion: 0.25
Nodes (7): Blockers / Open Questions, Context, Decisions Made, Deliverables, Next Steps for [Target Agent], References, [Source Agent] -> [Target Agent] Handover

### Community 46 - "Service integration (#351): findings from the manual test walkthrough"
Cohesion: 0.22
Nodes (9): A. Questions to answer from the code, no change expected, Answers (read from the code 2026-09-25), B. Bugs to fix, C. Interface changes the user asked for, Extra wording fixes asked for on 2026-09-26, Service integration (#351): findings from the manual test walkthrough, Status (2026-09-26), Status (2026-09-26) (+1 more)

### Community 47 - "get_health_status"
Cohesion: 0.33
Nodes (5): health(), Endpoint for the Docker health check, returns 503 if errors were logged the…, get_health_status(), Method to get error records newer than the given number of hours, Function to assess application health from errors logged the last 24 hours and…

### Community 48 - "Database Expert Agent"
Cohesion: 0.29
Nodes (6): Constraints, Core Responsibilities, Pattern Consistency - CRITICAL, Query Optimization, Schema Changes, Workflow

### Community 49 - "UX Designer Agent"
Cohesion: 0.29
Nodes (6): Core Responsibilities, Design Principles, Specifications to Include, v1 (Before Architect), v2 (After Architect), Workflow

### Community 50 - "Task 8: Test foundation and synthetic dataset"
Cohesion: 0.32
Nodes (8): Task 8: Test foundation and synthetic dataset, app_env(), migrated_env(), modules(), fixture, Copy template db to tmp dir, write config.json there, chdir into it, Run db_migration against the copied template db so the schema is current, Fresh imports of the app modules bound to the test database

### Community 51 - "test_health.py"
Cohesion: 0.23
Nodes (9): Verification done, Health check: errors logged the last 24 hours or a failing database make the…, lifespan in main.py sets every root handler to INFO or DEBUG at startup, SQLite creates an empty file for a wrong path, e.g. a missing Docker mount, recording_logger(), test_missing_database_file_makes_app_unhealthy(), test_recorder_includes_exception_in_message(), test_recorder_keeps_errors_and_ignores_lower_levels() (+1 more)

### Community 52 - "Code Reviewer -> Docs Maintainer Handover"
Cohesion: 0.25
Nodes (8): Code Reviewer -> Docs Maintainer Handover, Context, Deliverables, Issues Found, Next Steps for Docs Maintainer, References, Resolution (2026-09-27, after review), test_failing_database_makes_app_unhealthy()

### Community 53 - "Fullstack Developer -> Code Reviewer Handover"
Cohesion: 0.25
Nodes (8): Blockers / Open Questions, Context, Decisions Made, Deliverables, Fullstack Developer -> Code Reviewer Handover, Next Steps for Code Reviewer, References, Verification done

### Community 54 - "validateComponentThresholds"
Cohesion: 0.40
Nodes (5): addFormValidation(), clearValidationErrors(), showFieldError(), validateComponentThresholds(), validateQuickSwapForm()

### Community 55 - "ErrorRecorder"
Cohesion: 0.40
Nodes (3): ErrorRecorder, Logging handler that keeps the most recent error records in memory for the…, Method to store error records and ignore lower levels. Filters here instead of…

### Community 56 - "Approaches considered"
Cohesion: 0.33
Nodes (6): API: separate API, or one set of resources with two formats, API style: FHIR-conformant or FHIR-inspired, Approaches considered, Delivery: side by side on master, or frozen master and long-running dev, Frontend: server-rendered with htmx, or a JSON API with a separate frontend app, Provenance actor: named user or source of change

### Community 57 - "Approaches"
Cohesion: 0.33
Nodes (6): Approaches, Fixed clock, Order of work, Release mechanism, Synthetic dataset, Version source

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

### Community 62 - "health-check-reviewer-to-docs-maintainer.md"
Cohesion: 0.33
Nodes (5): Database check reads bikes table, not SELECT 1, Rename read_database_connection to check_database_connection, ErrorRecorder deque bounded to maxlen=20, ErrorRecorder thread safety under Handler.lock, Catching peewee.DatabaseError for corrupt file

### Community 63 - "Handovers Directory Guide"
Cohesion: 0.33
Nodes (5): Creating Handovers, Directory Structure, Finding Handovers, Handovers Directory, Rules

### Community 64 - "version.py"
Cohesion: 0.40
Nodes (4): get_git_info(), Script to maintain version number, Function to get latest version number and commit hash, subprocess

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

### Community 72 - "get_filtered_log"
Cohesion: 0.50
Nodes (4): get_filtered_log(), Endpoint to read log and return only business events, Function to get filtered log records, read_filtered_logs()

### Community 73 - "update_config"
Cohesion: 0.50
Nodes (4): Endpoint to update config file based on which form was submitted, update_config(), Helper function to shutdown the server after a short delay, shutdown_server()

### Community 74 - "2026-09-25-service-integration-test-findings.md"
Cohesion: 0.25
Nodes (8): A5: workplan delete blocked while services linked, B3: service modal submittable without completion date, D2: incident modal lists linked services, D4: choose components when creating workplan from incident, Manual walkthrough findings (A/B/C/D groups), Re-test list for the second round, Warn (not block) when resolving incident with planned services, Date picker form.onsubmit wrapper fix

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

### Community 81 - "D. Design questions to decide before coding"
Cohesion: 0.25
Nodes (8): Code review outcome, 2026-09-26, D. Design questions to decide before coding, Decisions (2026-09-26), Follow-up tweaks asked for on 2026-09-26, Second round of tweaks, 2026-09-26, Status (2026-09-26), Third round of tweaks, 2026-09-26, Warning when resolving an incident with open services, 2026-09-26

### Community 105 - "read_config"
Cohesion: 0.20
Nodes (10): Phase B: move, version, config, Docker, branch `feature/stage1-src-layout`, Task 5: Version from the git tag, Task 6: Config location from `VELO_SUPERVISOR_CONFIG`, Task 7: Docker image and first CI workflow, Configuration file location, Version and releases, get_current_version(), Function to get current program version (+2 more)

### Community 106 - "Testing Requirements"
Cohesion: 0.67
Nodes (3): Before Creating Handover, For fullstack-developer, Testing Requirements

## Ambiguous Edges - Review These
- `tests/conftest.py` → `Manual testing protocols approach`  [AMBIGUOUS]
  tests/README.md · relation: conceptually_related_to

## Knowledge Gaps
- **260 isolated node(s):** `velo-supervisor-2000`, `create-container-vs2000.sh script`, `Core Responsibilities`, `Workflow`, `Handover Content` (+255 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 642 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **55 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `tests/conftest.py` and `Manual testing protocols approach`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **Why does `DatabaseManager` connect `DatabaseManager` to `Meta`, `.write_delete_record`, `utils.py`, `.read_bike_name`, `.read_component`, `.count_component_types_in_use`, `.read_all_component_types`, `.read_all_workplans`, `.read_bike_id_recent_component_history`, `.read_latest_history_record`, `.read_latest_service_record`, `.read_matching_rides`, `.read_oldest_history_record`, `.read_open_incidents`, `.read_planned_services_by_workplan`, `.read_recent_rides`, `.read_services_by_incident`, `.read_services_by_workplan`, `.read_subset_components`, `.read_subset_installed_components`, `.write_bike_service_status`, `.write_component_distance`, `.write_component_service_status`, `.write_history_record`, `.write_incident_record`, `.write_service_record`, `.write_workplan`?**
  _High betweenness centrality (0.146) - this node is a cross-community bridge._
- **Why does `BusinessLogic` connect `BusinessLogic` to `main.py`, `scheduler.py`, `utils.py`, `.update_rides_bulk`, `.update_workplan`, `get_formatted_datetime_now`, `Task 2: Derived values`, `.complete_services`, `.check_database_connection`?**
  _High betweenness centrality (0.132) - this node is a cross-community bridge._
- **Why does `Manual testing protocols approach` connect `2026-09-18-service-integration-design.md` to `insert`?**
  _High betweenness centrality (0.113) - this node is a cross-community bridge._
- **Are the 9 inferred relationships involving `DatabaseManager` (e.g. with `Bikes` and `Collections`) actually correct?**
  _`DatabaseManager` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Are the 20 inferred relationships involving `Tests` (e.g. with `.create_collection()` and `.create_history_record()`) actually correct?**
  _`Tests` has 20 INFERRED edges - model-reasoned connections that need verification._
- **What connects `velo-supervisor-2000`, `create-container-vs2000.sh script`, `Core Responsibilities` to the rest of the system?**
  _260 weakly-connected nodes found - possible documentation gaps or missing edges._