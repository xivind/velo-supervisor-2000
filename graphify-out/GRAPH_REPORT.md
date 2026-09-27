# Graph Report - velo-supervisor-2000  (2026-09-27)

## Corpus Check
- 38 files · ~144,335 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 12 file(s) not represented in the graph (top: (none) 5, .example 1, .sqlite 1)

## Summary
- 952 nodes · 1462 edges · 118 communities (70 shown, 48 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 207 edges (avg confidence: 0.9)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `06b70d4b`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- .get_bike_details
- migrate_incidents_workplan_link
- Base Template
- utils.py
- Meta
- Strava
- What was checked and held up
- main.js
- get
- CLAUDE.md
- .calculate_collection_status
- BusinessLogic
- DatabaseManager
- Database Migration Script (db_migration.py)
- Service integration (#351) - fullstack to code-reviewer
- validateDateInput
- sortColumn
- main.py
- Service integration: incidents, workplans and services
- .write_delete_record
- .read_single_component_type
- get_filtered_log
- Python Requirements List
- .read_single_bike
- .read_component
- Issues found (none blocking)
- cleanup
- initializeIncidentTable
- version.py
- CLAUDE.md
- .get_component_details
- validateComponentThresholds
- migrate_components_time_fields
- helpTopics Data Object
- conftest.py
- .read_all_incidents
- insert_planned_service_for_migration
- seed_component
- test_migration.py
- migrate_component_types_time_fields
- generate_unique_id
- validate_date_format
- D. Design questions to decide before coding
- .read_collection_by_component
- .read_incidents_by_workplan
- migrate_workplans_to_planned_services
- .read_latest_ride_record
- database_manager.py
- migrate_workplans_name_column
- db_migration.py
- run_all_migrations
- .read_subset_components
- Results
- .read_subset_service_record
- migrate_database
- .read_sum_distance_subset_rides
- renderPreview
- migrate_services_workplan_link
- .write_workplan
- .read_bikes
- config_overview
- .read_subset_component_history
- .read_all_components_objects
- Git Workflow Rules
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
- Service integration (#351): findings from the manual test walkthrough
- .write_component_service_status
- Collections Test Protocol
- Complete Workplan Modal Template

## God Nodes (most connected - your core abstractions)
1. `DatabaseManager` - 70 edges
2. `BusinessLogic` - 64 edges
3. `seed_component()` - 24 edges
4. `run_all_migrations()` - 22 edges
5. `Meta` - 20 edges
6. `seed_rides()` - 20 edges
7. `get_workplan_data_tuple()` - 15 edges
8. `What was checked and held up` - 15 edges
9. `database_manager.py` - 14 edges
10. `BaseModel` - 13 edges

## Surprising Connections (you probably didn't know these)
- `Code review outcome, 2026-09-26` --references--> `migrate_incidents_workplan_link()`  [INFERRED]
  docs/superpowers/plans/2026-09-25-service-integration-test-findings.md → backend/db_migration.py
- `Answers (read from the code 2026-09-25)` --references--> `insert_planned_service_for_migration()`  [INFERRED]
  docs/superpowers/plans/2026-09-25-service-integration-test-findings.md → backend/db_migration.py
- `Answers (read from the code 2026-09-25)` --references--> `migrate_workplans_to_planned_services()`  [INFERRED]
  docs/superpowers/plans/2026-09-25-service-integration-test-findings.md → backend/db_migration.py
- `What was checked and held up` --references--> `run_all_migrations()`  [INFERRED]
  .handovers/review/service-integration-reviewer-to-docs-maintainer.md → backend/db_migration.py
- `Migration` --references--> `generate_unique_id()`  [INFERRED]
  docs/superpowers/specs/2026-09-18-service-integration-design.md → backend/utils.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Breaking Database Schema Change Releases** — readme_v0_4_2, readme_v0_4_3, readme_v0_4_5, readme_v0_4_7, readme_v0_4_9, readme_db_migration_script [EXTRACTED 0.90]
- **Feature Introduction Documented in Help Page** — readme_v0_4_5, readme_v0_4_6, readme_v0_4_7, frontend_templates_help_core_concepts_collections, frontend_templates_help_common_tasks_quick_swap, frontend_templates_help_core_concepts_hybrid_tracking [INFERRED 0.85]
- **Generic JS-Driven Utility Modals** — frontend_templates_modal_confirm_confirmmodal, frontend_templates_modal_validation_validationmodal, frontend_templates_modal_report_reportmodal, frontend_templates_modal_docs_docsmodal, frontend_templates_modal_loading_loadingmodal [INFERRED 0.85]
- **Help Topic Display and Search Flow** — frontend_templates_help_helptopics, frontend_templates_help_showhelptopic, frontend_templates_help_search_functionality [INFERRED 0.85]
- **Shared Status Legend Badge Pattern** — frontend_templates_component_overview_template, frontend_templates_collection_details_template, frontend_templates_index_template [INFERRED 0.85]
- **Templates Iterating payload.all_components_data** — frontend_templates_modal_incident_record_incidentrecordmodal, frontend_templates_modal_install_component_installcomponentmodal, frontend_templates_modal_quick_swap_quickswapmodal, frontend_templates_modal_workplan_record_workplanrecordmodal [INFERRED 0.90]

## Communities (118 total, 48 thin omitted)

### Community 0 - ".get_bike_details"
Cohesion: 0.14
Nodes (12): Method to produce payload for page component overview, Method to check if a bike has all mandatory components and respects max…, Method to produce payload for page bike overview, Method to create component-to-collection mapping dictionaries, Method to build dictionaries of bike and component ids referenced in received…, Method to build dictionaries of bike and component ids referenced by services…, Method to produce payload for page bike details, Method to read content of components table as formatted tuples (+4 more)

### Community 1 - "migrate_incidents_workplan_link"
Cohesion: 0.25
Nodes (8): check_incidents_workplan_column(), check_services_integration_columns(), migrate_incidents_workplan_link(), migrate_services_integration_columns(), Check if Incidents table needs workplan_id column, Add workplan_id column to Incidents table for workplan hub integration, Check which service integration columns are missing on the services table, Add status, incident_id and planned_date to services, mark existing rows…

### Community 2 - "Base Template"
Cohesion: 0.12
Nodes (34): Base Template, btn_new_incident Macro (Bike Details), btn_new_workplan Macro (Bike Details), Bike Details Template, Collection Details Template, btn_new_incident Macro (Component Details), btn_new_workplan Macro (Component Details), btn_quick_swap Macro (+26 more)

### Community 3 - "utils.py"
Cohesion: 0.05
Nodes (44): apscheduler_schedulers_asyncio, apscheduler_triggers_cron, apscheduler_triggers_interval, Module to handle business logic, Module for interaction with a Sqlite database, lifespan(), Manage application startup and shutdown, Endpoint to update config file based on which form was submitted (+36 more)

### Community 4 - "Meta"
Cohesion: 0.09
Nodes (34): BaseModel, Bikes, Collections, ComponentHistory, Components, ComponentTypes, Incidents, Meta (+26 more)

### Community 5 - "Strava"
Cohesion: 0.18
Nodes (9): Class to interact with Strava API, Method to authenticate and get data from Stravas gear API, Method to prepare a list of rides, Method to prepare a list of bikes, Method to read oauth options from file, Method to save oauth options to file, Method to authenticate and get data from Stravas activities API, Method to authenticate and get the full list of bike ids from the athlete's… (+1 more)

### Community 6 - "What was checked and held up"
Cohesion: 0.09
Nodes (21): Method to update status for a given bike based on component service and…, Method to create installation history record, Method to calculate distance and bike id for history records, Method to update a service record, including status changes in both directions, Method to recalculate a component after a completed service is deleted or…, Method to calculate distance and bike id for service records, Method to determine worst-case status between distance and days-based…, Method to update time-based status fields for all non-retired components (+13 more)

### Community 7 - "main.js"
Cohesion: 0.08
Nodes (12): editCollection(), filterNewComponentsByType(), handleOldComponentChange(), handleUpdate(), initializeCollectionsSearch(), updateRowVisibility(), initializeComponentSelector(), NOTE: All collection details page handlers are in the "Functions used on… (+4 more)

### Community 8 - "get"
Cohesion: 0.10
Nodes (24): add_history_record(), collection_details(), component_overview(), component_types_overview(), help_page(), http_exception_handler(), Request, Endpoint for workplans page (+16 more)

### Community 9 - "CLAUDE.md"
Cohesion: 0.25
Nodes (6): Change Management Rules, Communication & Output Rules, Debugging & Bug Fixing Rules, graphify, Important Notes, Project Overview

### Community 10 - ".calculate_collection_status"
Cohesion: 0.17
Nodes (6): Method to update collection, Method to validate collections before allowing bulk operations, Method to change status of all components in a collection, Calculate status flags for a collection based on its components., Method to produce payload for displaying table of all collections, Method to produce payload for collection details page

### Community 11 - "BusinessLogic"
Cohesion: 0.08
Nodes (17): BusinessLogic, Method to update component lifetime and service status when no installation…, Method to create component, Method to update component details, Method to orchestrate swap of one component with another, Method to validate quick swap operation, Method to compute component status using threshold logic, Method to determine which factor triggered a warning status (+9 more)

### Community 12 - "DatabaseManager"
Cohesion: 0.08
Nodes (13): DatabaseManager, Method to read and sort content of component_types table, Method to read installed components for a specific bike, Class to interact with a SQLite database through Peewee, Method to retrieve the most recent record from the installation log of a given…, Method to retrieve the oldest record from the installation log of a given…, Method to read all collections, Method to read all workplans (+5 more)

### Community 13 - "Database Migration Script (db_migration.py)"
Cohesion: 0.13
Nodes (16): Collections (Core Concept), Component Types vs Components, Hybrid Time + Distance Tracking, Mileage Tracking, Understanding Thresholds, Getting Started: Define Component Types, Incidents Page, Workplans Page (+8 more)

### Community 14 - "Service integration (#351) - fullstack to code-reviewer"
Cohesion: 0.08
Nodes (22): Method to add service record, planned or completed, Method to add a planned service, which has no service date, bike or distance…, Method to build the report used by the plan services and complete services…, Method to create planned services for one or more components with the same…, Method to complete planned services with one service date, keeping their…, Method to validate service records before processing and storing in database, generate_incident_title(), get_effective_planned_date() (+14 more)

### Community 15 - "validateDateInput"
Cohesion: 0.33
Nodes (6): initializeWorkplanForm(), submitCollectionAjax(), submitComponentAjax(), validateCollectionStatusChange(), validateDateInput(), validateWorkplanForm()

### Community 16 - "sortColumn"
Cohesion: 0.29
Nodes (8): initializeCollectionsSorting(), sortColumn(), initializeWorkplanTable(), setupIncidentTableSorting(), setupWorkplanSearch(), setupWorkplanStatusFiltering(), setupWorkplanTableSorting(), updateWorkplansVisibility()

### Community 17 - "main.py"
Cohesion: 0.06
Nodes (42): asyncio, add_collection(), add_incident_record(), add_planned_services(), add_service(), add_workplan(), change_collection_status(), complete_services() (+34 more)

### Community 18 - "Service integration: incidents, workplans and services"
Cohesion: 0.18
Nodes (10): Data model, Error handling, Goal, main.js, Modals, Out of scope, Pages, Service integration: incidents, workplans and services (+2 more)

### Community 19 - ".write_delete_record"
Cohesion: 0.17
Nodes (6): Method to retrieve record for a specific entry in the installation log, Method to retrieve a specific service record, Method to retrieve record for a specific collection, Method to retrieve record for a specific incident report, Method to retrieve record for a specific workplan, Method to delete a given record and associated records

### Community 21 - "get_filtered_log"
Cohesion: 0.50
Nodes (4): get_filtered_log(), Endpoint to read log and return only business events, Function to get filtered log records, read_filtered_logs()

### Community 22 - "Python Requirements List"
Cohesion: 0.25
Nodes (8): APScheduler, Python Requirements List, FastAPI, Jinja2, Peewee ORM, python-multipart, requests-oauthlib, Uvicorn

### Community 24 - ".read_component"
Cohesion: 0.33
Nodes (3): Method to get component names based on list of ids, Method to retrieve record for a specific component, Method to create or update component data to the database

### Community 25 - "Issues found (none blocking)"
Cohesion: 0.12
Nodes (16): Method to get the name of a bike based on bike id, bike_details(), component_details(), incident_reports(), Endpoint for incident reports page, Endpoint for workplan details page, Endpoint for component details page, Endpoint for bike details page (+8 more)

### Community 26 - "cleanup"
Cohesion: 0.50
Nodes (4): cleanup(), handleCancel(), handleConfirm(), performBulkStatusChange()

### Community 27 - "initializeIncidentTable"
Cohesion: 0.67
Nodes (4): initializeIncidentTable(), setupIncidentSearch(), setupIncidentStatusFiltering(), updateIncidentVisibility()

### Community 28 - "version.py"
Cohesion: 0.40
Nodes (4): get_git_info(), Script to maintain version number, Function to get latest version number and commit hash, subprocess

### Community 29 - "CLAUDE.md"
Cohesion: 0.50
Nodes (4): CLAUDE.md, Data Management Tips, Need More Help? (Troubleshooting), Handover Documents Directory (.handovers/)

### Community 30 - ".get_component_details"
Cohesion: 0.11
Nodes (27): Method to produce payload for page component details, Method to produce payload for page incident reports, Method to produce payload for page of all workplans, Method to produce payload for workplan details page, calculate_elapsed_days(), derive_workplan_context(), generate_workplan_title(), get_formatted_bikes_list() (+19 more)

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
Cohesion: 0.14
Nodes (11): Method to create collection, Method to add incident record, Method to add workplan, optionally with planned services for components of a…, build_incident_service_entry(), generate_unique_id(), parse_json_string(), Function to generates a random and unique ID, Describe one service linked to an incident, for the read only list in the… (+3 more)

### Community 41 - "validate_date_format"
Cohesion: 0.17
Nodes (7): Method to update a component history record with validation, Method to validate history records before processing and storing in database, Method to update incident record (supports full or partial updates), Method to update workplan (supports full or partial updates), Method to validate that a workplan can be set to Done, Function to validate that a date string matches the required format YYYY-MM-DD…, validate_date_format()

### Community 42 - "D. Design questions to decide before coding"
Cohesion: 0.18
Nodes (11): Code review outcome, 2026-09-26, D. Design questions to decide before coding, Decisions (2026-09-26), Follow-up tweaks asked for on 2026-09-26, Second round of tweaks, 2026-09-26, Third round of tweaks, 2026-09-26, Warning when resolving an incident with open services, 2026-09-26, initializeIncidentForm() (+3 more)

### Community 45 - "migrate_workplans_to_planned_services"
Cohesion: 0.25
Nodes (8): check_workplans_affected_columns(), migrate_drop_workplan_affected_columns(), migrate_workplans_to_planned_services(), Check if workplans table still has the affected bike/component columns, Resolve bike and component names, marking components that no longer exist, Convert affected components on planned workplans into planned services,…, Rebuild workplans table without the affected bike/component columns, read_names_for_migration()

### Community 47 - "database_manager.py"
Cohesion: 0.09
Nodes (12): Method to read completed services for a component, used by health computation, Method to retrieve the oldest completed service of a given component, Method to read incident records with status 'Open, Method to read workplans with status 'Planned, Method to read all services linked to a specific workplan, planned first, Method to read planned services linked to a specific workplan, Method to read all services linked to a specific incident, planned first, Method to read planned services for a component (+4 more)

### Community 48 - "migrate_workplans_name_column"
Cohesion: 0.50
Nodes (4): check_workplans_name_column(), migrate_workplans_name_column(), Check if workplans table needs the workplan_name column, Add the optional user given name to the workplans table, existing workplans…

### Community 49 - "db_migration.py"
Cohesion: 0.21
Nodes (11): check_component_history_notes_column(), check_component_types_columns(), count_component_types_in_use(), migrate_component_history_notes(), migrate_component_types(), Count how many components use a specific component type, Check if the component_types table needs migration, Migrate the component_types table to add new columns (+3 more)

### Community 50 - "run_all_migrations"
Cohesion: 0.14
Nodes (14): create_collections_table(), create_incidents_table(), create_workplans_table(), populate_component_types_thresholds(), populate_components_thresholds(), Creates the incidents table if it doesn't exist., Creates the workplans table if it doesn't exist., Creates the collections table if it doesn't exist. (+6 more)

### Community 52 - "Results"
Cohesion: 0.25
Nodes (7): 2026-09-25, first walkthrough, human, 2026-09-26, regression against the baseline database, Claude, 2026-09-27, second walkthrough, human, Preparation, Results, Scope, Test Protocol: Planned services, workplans and incidents

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
Cohesion: 0.24
Nodes (7): Middleware, Request, Class to handle exceptions that breaks the program and should be shown to the…, Method to dispatch intercepted requests, Method to catch and handle exceptions, BaseHTTPMiddleware, Exception

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
Cohesion: 0.18
Nodes (9): B. Bugs to fix, C. Interface changes the user asked for, Extra wording fixes asked for on 2026-09-26, Re-test list for the second round, Service integration (#351): findings from the manual test walkthrough, Status (2026-09-26), Status (2026-09-26), Suggested order (+1 more)

## Ambiguous Edges - Review These
- `Git Workflow Rules` → `Version Script CI Workflow`  [AMBIGUOUS]
  .github/workflows/run_version_script.yml · relation: conceptually_related_to

## Knowledge Gaps
- **165 isolated node(s):** `backup_db.sh script`, `create-container-vs2000.sh script`, `velo-supervisor-2000`, `Core Responsibilities`, `Workflow` (+160 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 500 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **48 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `Git Workflow Rules` and `Version Script CI Workflow`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **Why does `DatabaseManager` connect `DatabaseManager` to `.get_bike_details`, `utils.py`, `Meta`, `What was checked and held up`, `.write_delete_record`, `.read_single_component_type`, `.read_single_bike`, `.read_component`, `Issues found (none blocking)`, `.read_all_incidents`, `.read_collection_by_component`, `.read_incidents_by_workplan`, `.read_latest_ride_record`, `database_manager.py`, `.read_subset_components`, `.read_subset_service_record`, `.read_sum_distance_subset_rides`, `.write_workplan`, `.read_bikes`, `.read_subset_component_history`, `.read_all_components_objects`, `.read_recent_rides`, `.read_unique_bikes`, `.write_incident_record`, `.count_component_types_in_use`, `.read_date_oldest_ride`, `.write_component_distance`, `.read_workplans_by_incident`, `.write_component_service_status`?**
  _High betweenness centrality (0.165) - this node is a cross-community bridge._
- **Why does `BusinessLogic` connect `BusinessLogic` to `.get_bike_details`, `utils.py`, `What was checked and held up`, `generate_unique_id`, `validate_date_format`, `.calculate_collection_status`, `Service integration (#351) - fullstack to code-reviewer`, `.get_component_details`?**
  _High betweenness centrality (0.107) - this node is a cross-community bridge._
- **Why does `renderIncidentServices()` connect `D. Design questions to decide before coding` to `Issues found (none blocking)`, `main.js`?**
  _High betweenness centrality (0.068) - this node is a cross-community bridge._
- **Are the 9 inferred relationships involving `DatabaseManager` (e.g. with `Bikes` and `Collections`) actually correct?**
  _`DatabaseManager` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `BusinessLogic` (e.g. with `strava_sync_job()` and `update_time_based_fields_job()`) actually correct?**
  _`BusinessLogic` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `backup_db.sh script`, `create-container-vs2000.sh script`, `velo-supervisor-2000` to the rest of the system?**
  _165 weakly-connected nodes found - possible documentation gaps or missing edges._