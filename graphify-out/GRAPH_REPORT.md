# Graph Report - velo-supervisor-2000  (2026-09-09)

## Corpus Check
- 41 files · ~140,373 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 729 nodes · 1057 edges · 104 communities (56 shown, 48 thin omitted)
- Extraction: 89% EXTRACTED · 11% INFERRED · 0% AMBIGUOUS · INFERRED: 112 edges (avg confidence: 0.77)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `f97b9ebd`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- db_migration.py
- Base Template
- main.py
- utils.py
- main.js
- get
- BusinessLogic
- Fullstack Developer Agent
- Git Workflow Rules
- DatabaseManager
- .get_bike_details
- CLAUDE.md
- .calculate_component_triggers
- .create_component
- .process_history_records
- Strava
- Meta
- .create_service_record
- Middleware
- update_config
- .calculate_collection_status
- .write_delete_record
- validateDateInput
- scheduler.py
- Python Requirements List
- initializeWorkplanTable
- Workplan Details Page
- .read_bike_name
- .read_component
- What You Must Do When Invoked
- validateComponentThresholds
- .read_single_component_type
- config_overview
- get_filtered_log
- bike_details
- change_collection_status
- renderPreview
- refresh_all_bikes
- Create Component Modal
- get_git_info
- Agent Communication via Handovers
- Update Component Status Modal
- .count_component_types_in_use
- .read_all_collections
- .read_all_component_types
- .read_all_components_objects
- .read_all_incidents
- .read_all_workplans
- .read_bike_id_recent_component_history
- .read_bikes
- .read_collection_by_component
- .read_incidents_by_workplan
- .read_latest_history_record
- .read_latest_ride_record
- .read_latest_service_record
- .read_matching_rides
- .read_oldest_history_record
- .read_planned_workplans
- .read_recent_rides
- .read_services_by_workplan
- .read_subset_components
- .read_subset_service_history
- .read_subset_service_record
- .read_sum_distance_subset_rides
- .read_unique_bikes
- .write_bike_service_status
- .write_collection
- .write_component_lifetime_status
- .write_history_record
- .write_incident_record
- .write_service_record
- .write_workplan
- Architecture Overview
- backup_db.sh
- create-container-vs2000.sh
- initializeCollectionsSearch
- Development Commands
- .validate_threshold_configuration
- Confirm Action Modal
- Documentation Modal
- Edit Installation Record Modal
- Loading Modal
- Report Modal
- Validation Error Modal
- Code Style & Standards
- Development Notes
- Standard Development Workflow
- initializeIncidentTable
- add_history_record
- .claude/CLAUDE.md
- Sub-Agent Team
- Testing Requirements
- Handovers Directory Guide
- graphify reference: extra exports and benchmark
- graphify reference: query, path, explain
- graphify reference: add a URL and watch a folder
- graphify reference: commit hook and native CLAUDE.md integration
- graphify reference: incremental update and cluster-only
- graphify reference: GitHub clone and cross-repo merge
- graphify reference: transcribe video and audio
- extraction-spec.md
- quick_swap
- velo-supervisor-2000

## God Nodes (most connected - your core abstractions)
1. `DatabaseManager` - 65 edges
2. `BusinessLogic` - 61 edges
3. `Meta` - 20 edges
4. `migrate_database()` - 14 edges
5. `Base Template` - 14 edges
6. `BaseModel` - 13 edges
7. `get_workplan_data_tuple()` - 13 edges
8. `What You Must Do When Invoked` - 12 edges
9. `get_formatted_datetime_now()` - 10 edges
10. `get_incident_data_tuple()` - 10 edges

## Surprising Connections (you probably didn't know these)
- `Version Script CI Workflow` --conceptually_related_to--> `Git Workflow Rules`  [AMBIGUOUS]
  .github/workflows/run_version_script.yml → CLAUDE.md
- `Complete Workplan Modal Template` --conceptually_related_to--> `Opt-in Workplan Hub Pattern`  [INFERRED]
  frontend/templates/modal_complete_workplan.html → docs/plans/2026-01-11-workplan-hub-integration-incremental.md
- `Current Version File (v0.4.9.1f9734e)` --conceptually_related_to--> `Workplan Hub Integration Plan`  [INFERRED]
  backend/current_version.txt → docs/plans/2026-01-11-workplan-hub-integration-incremental.md
- `Workplan Hub Integration Plan` --conceptually_related_to--> `Test Protocols Documentation`  [INFERRED]
  docs/plans/2026-01-11-workplan-hub-integration-incremental.md → tests/README.md
- `get_filtered_log()` --calls--> `fetchLogs()`  [EXTRACTED]
  backend/main.py → frontend/static/js/main.js

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **CSS Inline-Style-to-Class Refactoring Files** — docs_plans_2026_01_11_workplan_hub_integration_incremental_css_refactor_concept, frontend_templates_collection_details_template, frontend_templates_index_template, frontend_templates_component_overview_template, frontend_templates_component_details_template, frontend_templates_bike_details_template, frontend_templates_config_template, frontend_templates_error_template [EXTRACTED 1.00]
- **Standard Feature Development Workflow** — claude_standard_development_workflow, _claude_agents_product_manager_product_manager_agent, _claude_agents_ux_designer_ux_designer_agent, _claude_agents_architect_architect_agent, _claude_agents_database_expert_database_expert_agent, _claude_agents_fullstack_developer_fullstack_developer_agent, _claude_agents_code_reviewer_code_reviewer_agent, _claude_agents_docs_maintainer_docs_maintainer_agent [EXTRACTED 1.00]
- **Generic JS-Driven Utility Modals** — frontend_templates_modal_confirm_confirmmodal, frontend_templates_modal_validation_validationmodal, frontend_templates_modal_report_reportmodal, frontend_templates_modal_docs_docsmodal, frontend_templates_modal_loading_loadingmodal [INFERRED 0.85]
- **Handover Documentation Pattern** — _handovers_template_handover_template, _claude_agents_architect_architect_agent, _claude_agents_code_reviewer_code_reviewer_agent, _claude_agents_database_expert_database_expert_agent, _claude_agents_docs_maintainer_docs_maintainer_agent, _claude_agents_fullstack_developer_fullstack_developer_agent, _claude_agents_product_manager_product_manager_agent, _claude_agents_ux_designer_ux_designer_agent [INFERRED 0.85]
- **Shared Status Legend Badge Pattern** — frontend_templates_component_overview_template, frontend_templates_collection_details_template, frontend_templates_index_template [INFERRED 0.85]
- **Workplan Hub Integration Flow** — docs_plans_2026_01_11_workplan_hub_integration_incremental_doc, frontend_templates_bike_details_template, frontend_templates_component_details_template, frontend_templates_incident_reports_template, frontend_templates_modal_complete_workplan_template [INFERRED 0.85]
- **Workplan-Incident-Service Linking Flow** — frontend_templates_modal_workplan_record_workplanrecordmodal, frontend_templates_modal_incident_record_incidentrecordmodal, frontend_templates_modal_service_record_servicerecordmodal, frontend_templates_modal_link_incident_linkincidentsmodal, frontend_templates_modal_create_services_workplan_createservicesworkplanmodal, frontend_templates_workplan_details_workplandetailspage [INFERRED 0.85]
- **Templates Iterating payload.all_components_data** — frontend_templates_modal_incident_record_incidentrecordmodal, frontend_templates_modal_install_component_installcomponentmodal, frontend_templates_modal_quick_swap_quickswapmodal, frontend_templates_modal_workplan_record_workplanrecordmodal [INFERRED 0.90]

## Communities (104 total, 48 thin omitted)

### Community 0 - "db_migration.py"
Cohesion: 0.07
Nodes (40): check_component_types_columns(), check_component_types_time_columns(), check_components_time_columns(), check_incidents_workplan_column(), check_services_workplan_column(), count_component_types_in_use(), create_collections_table(), create_incidents_table() (+32 more)

### Community 1 - "Base Template"
Cohesion: 0.08
Nodes (41): Current Version File (v0.4.9.1f9734e), CSS Inline-Style-to-Class Refactoring, Workplan Hub Integration Plan, Opt-in Workplan Hub Pattern, Error Page Illustration, Velo Supervisor Fox Mechanic Logo, Base Template, btn_new_incident Macro (Bike Details) (+33 more)

### Community 2 - "main.py"
Cohesion: 0.09
Nodes (32): add_collection(), add_incident_record(), add_service(), add_workplan(), bulk_add_service_records(), component_modify(), component_types_modify(), create_component() (+24 more)

### Community 3 - "utils.py"
Cohesion: 0.07
Nodes (40): Method to update component lifetime and service status when no installation…, Method to produce payload for page component details, Method to determine worst-case status between distance and days-based…, Method to produce payload for page incident reports, Method to produce payload for page of all workplans, Method to produce payload for workplan details page, Method to get incidents that can be linked to a workplan, Method to update component table with lifetime status (+32 more)

### Community 4 - "main.js"
Cohesion: 0.09
Nodes (8): editCollection(), filterNewComponentsByType(), handleOldComponentChange(), initializeComponentSelector(), NOTE: All collection details page handlers are in the "Functions used on…, IMPORTANT: Remove readonly - allow manual typing, updateFormFields(), updateQuickSwapCollectionWarning()

### Community 5 - "get"
Cohesion: 0.16
Nodes (18): collection_details(), component_overview(), component_types_overview(), help_page(), incident_reports(), Request, Endpoint for incident reports page, Endpoint for workplans page (+10 more)

### Community 6 - "BusinessLogic"
Cohesion: 0.13
Nodes (10): BusinessLogic, Method to update incident record (supports full or partial updates), Method to add workplan and optionally link to source incident, Method to update workplan (supports full or partial updates), Function to set the date for last pull from Strava, Class that contains business logic, Method to check if all affected components have linked services, Method to produce payload for page component types (+2 more)

### Community 7 - "Fullstack Developer Agent"
Cohesion: 0.38
Nodes (7): Architect Agent, Code Reviewer Agent, Database Expert Agent, Docs Maintainer Agent, Fullstack Developer Agent, Product Manager Agent, UX Designer Agent

### Community 8 - "Git Workflow Rules"
Cohesion: 0.25
Nodes (8): Version Script CI Workflow, Branch Strategy, Commit Process, For All Agents, For code-reviewer, For docs-maintainer, For fullstack-developer, Git Workflow Rules

### Community 9 - "DatabaseManager"
Cohesion: 0.11
Nodes (10): DatabaseManager, Method to read installed components for a specific bike, Class to interact with a SQLite database through Peewee, Method to read a subset of records from the component history table, Method to retrieve the oldest record from the service log of a given component, Method to read incident records with status 'Open, Method to create or update ride data in bulk in database, Method to update component distance in database (+2 more)

### Community 10 - ".get_bike_details"
Cohesion: 0.14
Nodes (12): Method to produce payload for page component overview, Method to produce payload for page bike overview, Method to create component-to-collection mapping dictionaries, Method to produce payload for displaying table of all collections, Method to build dictionaries of bike and component ids referenced in received…, Method to build dictionaries of bike and component ids referenced in received…, Method to produce payload for page bike details, Method to read content of components table as formatted tuples (+4 more)

### Community 11 - "CLAUDE.md"
Cohesion: 0.25
Nodes (6): Change Management Rules, Communication & Output Rules, Debugging & Bug Fixing Rules, graphify, Important Notes, Project Overview

### Community 12 - ".calculate_component_triggers"
Cohesion: 0.33
Nodes (3): Method to compute component status using threshold logic, Method to determine which factor triggered a warning status, Calculate lifetime and service triggers for a component

### Community 13 - ".create_component"
Cohesion: 0.18
Nodes (8): Method to create component, Method to create installation history record, Method to orchestrate swap of one component with another, Method to validate quick swap operation, Method to check if a bike has all mandatory components and respects max…, Method to add incident record, generate_unique_id(), Function to generates a random and unique ID

### Community 14 - ".process_history_records"
Cohesion: 0.15
Nodes (10): Method to update component table with service status, Method to update status for a given bike based on component service and…, Method to update component details, Method to calculate distance and bike id for history records, Method to calculate distance and bike id for service records, Method to update time-based status fields for all non-retired components, Method to update only the count of components for a given component type, Method to delete a given record and associated records (+2 more)

### Community 15 - "Strava"
Cohesion: 0.17
Nodes (8): Class to interact with Strava API, Method to prepare a list of rides, Method to prepare a list of bikes, Method to read oauth options from file, Method to save oauth options to file, Method to authenticate and get data from Stravas activities API, Method to authenticate and get data from Stravas gear API, Strava

### Community 16 - "Meta"
Cohesion: 0.08
Nodes (32): BaseModel, Bikes, Collections, ComponentHistory, Components, ComponentTypes, Incidents, Meta (+24 more)

### Community 17 - ".create_service_record"
Cohesion: 0.14
Nodes (8): Method to update a component history record with validation, Method to validate history records before processing and storing in database, Method to add service record, Method to bulk create service records for multiple components linked to a…, Method to update a service record, Method to validate service records before processing and storing in database, Function to validate that a date string matches the required format YYYY-MM-DD…, validate_date_format()

### Community 18 - "Middleware"
Cohesion: 0.16
Nodes (11): http_exception_handler(), Function to catch http errors from Uvicorn and return them to the middleware, Middleware, Request, Class to handle exceptions that breaks the program and should be shown to the…, Method to dispatch intercepted requests, Method to catch and handle exceptions, BaseHTTPMiddleware (+3 more)

### Community 19 - "update_config"
Cohesion: 0.50
Nodes (4): Endpoint to update config file based on which form was submitted, update_config(), Helper function to shutdown the server after a short delay, shutdown_server()

### Community 20 - ".calculate_collection_status"
Cohesion: 0.17
Nodes (6): Method to create collection, Method to update collection, Method to validate collections before allowing bulk operations, Method to change status of all components in a collection, Calculate status flags for a collection based on its components., Method to produce payload for collection details page

### Community 21 - ".write_delete_record"
Cohesion: 0.17
Nodes (6): Method to retrieve record for a specific entry in the installation log, Method to retrieve a specific service record, Method to retrieve record for a specific collection, Method to retrieve record for a specific incident report, Method to retrieve record for a specific workplan, Method to delete a given record and associated records

### Community 22 - "validateDateInput"
Cohesion: 0.25
Nodes (7): initializeDatePickers(), initializeIncidentForm(), initializeWorkplanForm(), validateCollectionStatusChange(), validateDateInput(), validateIncidentForm(), validateWorkplanForm()

### Community 23 - "scheduler.py"
Cohesion: 0.28
Nodes (8): Initialize and start the APScheduler instance, Gracefully shutdown the APScheduler instance, Scheduled job to update time-based status fields for all non-retired components, Scheduled job to sync Strava activities, start_scheduler(), stop_scheduler(), strava_sync_job(), update_time_based_fields_job()

### Community 24 - "Python Requirements List"
Cohesion: 0.22
Nodes (9): v0.4.8 Release Notes, APScheduler, Python Requirements List, FastAPI, Jinja2, Peewee ORM, python-multipart, requests-oauthlib (+1 more)

### Community 25 - "initializeWorkplanTable"
Cohesion: 0.29
Nodes (8): initializeCollectionsSorting(), sortColumn(), initializeWorkplanTable(), setupIncidentTableSorting(), setupWorkplanSearch(), setupWorkplanStatusFiltering(), setupWorkplanTableSorting(), updateWorkplansVisibility()

### Community 26 - "Workplan Details Page"
Cohesion: 0.48
Nodes (7): Create Services For Workplan Modal, Incident Record Modal, Link Incident To Workplan Modal, Service Record Modal, Workplan Record Modal, Workplan Details Page, Workplans List Page

### Community 27 - ".read_bike_name"
Cohesion: 0.33
Nodes (3): Method to retrieve record for a specific bike, Method to get the name of a bike based on bike id, Method to create or update bike data to the database

### Community 28 - ".read_component"
Cohesion: 0.33
Nodes (3): Method to get component names based on list of ids, Method to retrieve record for a specific component, Method to create or update component data to the database

### Community 29 - "What You Must Do When Invoked"
Cohesion: 0.08
Nodes (24): For /graphify add and --watch, For /graphify query, For the commit hook and native CLAUDE.md integration, For --update and --cluster-only, /graphify, Honesty Rules, Interpreter guard for subcommands, Part A - Structural extraction for code files (+16 more)

### Community 30 - "validateComponentThresholds"
Cohesion: 0.33
Nodes (6): addFormValidation(), clearValidationErrors(), showFieldError(), showValidationModal(), validateComponentThresholds(), validateQuickSwapForm()

### Community 32 - "config_overview"
Cohesion: 0.50
Nodes (4): config_overview(), Endpoint for component types page, get_button_sorting_config(), Function to get button sorting configuration for config page

### Community 33 - "get_filtered_log"
Cohesion: 0.40
Nodes (5): get_filtered_log(), Endpoint to read log and return only business events, Function to get filtered log records, read_filtered_logs(), fetchLogs()

### Community 34 - "bike_details"
Cohesion: 0.33
Nodes (6): bike_details(), component_details(), Endpoint for component details page, Endpoint for bike details page, get_button_order(), Function to get button order for a specific page with defaults

### Community 35 - "change_collection_status"
Cohesion: 0.29
Nodes (7): change_collection_status(), Endpoint to change the status of all components in a collection, cleanup(), handleCancel(), handleConfirm(), performBulkStatusChange(), submitCollectionAjax()

### Community 36 - "renderPreview"
Cohesion: 0.50
Nodes (4): containsMarkdown(), renderPreview(), setInitialMode(), updateCheckboxInText()

### Community 37 - "refresh_all_bikes"
Cohesion: 0.33
Nodes (6): Endpoint to manually refresh data for all bikes, Endpoint to refresh data for a subset or all rides, refresh_all_bikes(), refresh_rides(), handleUpdate(), showToast()

### Community 38 - "Create Component Modal"
Cohesion: 0.67
Nodes (4): Component Type Modal, Create Component Modal, Quick Swap Modal, Update Component Details Modal

### Community 40 - "Agent Communication via Handovers"
Cohesion: 0.33
Nodes (6): Agent Communication via Handovers, Creating Handovers, Detailed Instructions, Handover Structure, Naming Convention, Reading Handovers

### Community 41 - "Update Component Status Modal"
Cohesion: 0.67
Nodes (3): Install Component Modal, Update Collection Status Modal, Update Component Status Modal

### Community 72 - "Architecture Overview"
Cohesion: 0.40
Nodes (5): Architecture Overview, Configuration, Core Components, Key Features, Project Structure

### Community 77 - "Development Commands"
Cohesion: 0.40
Nodes (5): Database Operations, Dependencies, Development Commands, Running the Application, Testing

### Community 85 - "Code Style & Standards"
Cohesion: 0.50
Nodes (4): Code Style & Standards, Database, Frontend, Python (Backend)

### Community 86 - "Development Notes"
Cohesion: 0.50
Nodes (4): Database Schema Changes, Development Notes, Docker Development, Logging

### Community 87 - "Standard Development Workflow"
Cohesion: 0.50
Nodes (4): For Bug Fixes, For Documentation Updates, For New Features, Standard Development Workflow

### Community 88 - "initializeIncidentTable"
Cohesion: 0.67
Nodes (4): initializeIncidentTable(), setupIncidentSearch(), setupIncidentStatusFiltering(), updateIncidentVisibility()

### Community 89 - "add_history_record"
Cohesion: 0.67
Nodes (3): add_history_record(), Endpoint with conditional routing for redirects and AJAX to add an existing…, submitComponentAjax()

### Community 91 - "Sub-Agent Team"
Cohesion: 0.67
Nodes (3): Available Agents, Direct Invocation, Sub-Agent Team

### Community 92 - "Testing Requirements"
Cohesion: 0.67
Nodes (3): Before Creating Handover, For fullstack-developer, Testing Requirements

### Community 94 - "graphify reference: extra exports and benchmark"
Cohesion: 0.22
Nodes (8): graphify reference: extra exports and benchmark, Step 6b - Wiki (only if --wiki flag), Step 7 - Neo4j export (only if --neo4j or --neo4j-push flag), Step 7a - FalkorDB export (only if --falkordb or --falkordb-push flag), Step 7b - SVG export (only if --svg flag), Step 7c - GraphML export (only if --graphml flag), Step 7d - MCP server (only if --mcp flag), Step 8 - Token reduction benchmark (only if total_words > 5000)

### Community 95 - "graphify reference: query, path, explain"
Cohesion: 0.33
Nodes (5): For /graphify explain, For /graphify path, graphify reference: query, path, explain, Step 0 — Constrained query expansion (REQUIRED before traversal), Step 1 — Traversal

### Community 96 - "graphify reference: add a URL and watch a folder"
Cohesion: 0.50
Nodes (3): For /graphify add, For --watch, graphify reference: add a URL and watch a folder

### Community 97 - "graphify reference: commit hook and native CLAUDE.md integration"
Cohesion: 0.50
Nodes (3): For git commit hook, For native CLAUDE.md integration, graphify reference: commit hook and native CLAUDE.md integration

### Community 98 - "graphify reference: incremental update and cluster-only"
Cohesion: 0.50
Nodes (3): For --cluster-only, For --update (incremental re-extraction), graphify reference: incremental update and cluster-only

### Community 102 - "quick_swap"
Cohesion: 0.67
Nodes (3): quick_swap(), Endpoint to swap one component with another, performQuickSwap()

## Ambiguous Edges - Review These
- `Version Script CI Workflow` → `Git Workflow Rules`  [AMBIGUOUS]
  .github/workflows/run_version_script.yml · relation: conceptually_related_to

## Knowledge Gaps
- **111 isolated node(s):** `velo-supervisor-2000`, `Docs Maintainer Agent`, `Product Manager Agent`, `Version Script CI Workflow`, `Handovers Directory Guide` (+106 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **48 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `Version Script CI Workflow` and `Git Workflow Rules`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **Why does `DatabaseManager` connect `DatabaseManager` to `utils.py`, `.get_bike_details`, `Meta`, `.write_delete_record`, `.read_bike_name`, `.read_component`, `.read_single_component_type`, `.count_component_types_in_use`, `.read_all_collections`, `.read_all_component_types`, `.read_all_components_objects`, `.read_all_incidents`, `.read_all_workplans`, `.read_bike_id_recent_component_history`, `.read_bikes`, `.read_collection_by_component`, `.read_incidents_by_workplan`, `.read_latest_history_record`, `.read_latest_ride_record`, `.read_latest_service_record`, `.read_matching_rides`, `.read_oldest_history_record`, `.read_planned_workplans`, `.read_recent_rides`, `.read_services_by_workplan`, `.read_subset_components`, `.read_subset_service_history`, `.read_subset_service_record`, `.read_sum_distance_subset_rides`, `.read_unique_bikes`, `.write_bike_service_status`, `.write_collection`, `.write_component_lifetime_status`, `.write_history_record`, `.write_incident_record`, `.write_service_record`, `.write_workplan`?**
  _High betweenness centrality (0.175) - this node is a cross-community bridge._
- **Why does `BusinessLogic` connect `BusinessLogic` to `utils.py`, `.get_bike_details`, `.calculate_component_triggers`, `.create_component`, `.process_history_records`, `.validate_threshold_configuration`, `.create_service_record`, `.calculate_collection_status`, `scheduler.py`?**
  _High betweenness centrality (0.136) - this node is a cross-community bridge._
- **Why does `bulk_add_service_records()` connect `main.py` to `main.js`?**
  _High betweenness centrality (0.048) - this node is a cross-community bridge._
- **Are the 9 inferred relationships involving `DatabaseManager` (e.g. with `Bikes` and `Collections`) actually correct?**
  _`DatabaseManager` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `BusinessLogic` (e.g. with `strava_sync_job()` and `update_time_based_fields_job()`) actually correct?**
  _`BusinessLogic` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `velo-supervisor-2000`, `Docs Maintainer Agent`, `Product Manager Agent` to the rest of the system?**
  _111 weakly-connected nodes found - possible documentation gaps or missing edges._