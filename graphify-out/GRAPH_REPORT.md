# Graph Report - velo-supervisor-2000  (2026-09-17)

## Corpus Check
- 71 files · ~129,418 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 671 nodes · 997 edges · 105 communities (47 shown, 57 thin omitted)
- Extraction: 88% EXTRACTED · 12% INFERRED · 0% AMBIGUOUS · INFERRED: 118 edges (avg confidence: 0.87)
- Token cost: 0 input · 98,321 output

## Community Hubs (Navigation)
- Database Migration Checks
- Core Write Endpoints
- Database ORM Models
- Frontend UI Initialization
- Workplan Hub Templates
- Page Route Endpoints
- Agent Team Documentation
- Database Manager Reads
- Component Overview Payloads
- Core Concepts Documentation
- Strava API Integration
- Scheduler & Module Overview
- Component Status Computation
- Workplan & Incident Payloads
- Component History Processing
- Exception Handling Middleware
- Config & Version Utilities
- BusinessLogic Class Core
- Create Record Operations
- Single Record Reads
- Collection Status Logic
- Component Creation & Quick Swap
- Bike & Component Payloads
- Form Init & Validation
- Service Record Operations
- Incident Data Helpers
- Table Sorting & Filtering
- Python Dependencies List
- Workplan & Incident Modals
- History Record Validation
- Bike Data Access
- Component Data Access
- Detail Page Endpoints
- Form Validation Helpers
- Workplans & Bikes Lists
- Component Type Validation
- Component Type Data Access
- Config Page Endpoint
- Filtered Log Endpoint
- Version Script
- Help Page Dev Docs
- Bulk Action Handlers
- Markdown Preview Rendering
- Incident Table Filtering
- Help Page Search
- Component Modals
- Quick Swap Filters
- Status Update Modals
- Project Meta Info
- Component Type Usage Count
- Read All Collections
- Read All Component Types
- Read All Components
- Read All Incidents
- Read All Workplans
- Recent Bike History Lookup
- Read All Bikes
- Collection Lookup By Component
- Incidents By Workplan
- Latest History Record
- Latest Ride Record
- Latest Service Record
- Matching Rides Lookup
- Oldest History Record
- Planned Workplans Lookup
- Recent Rides Lookup
- Services By Workplan
- Bike Component Subset
- Service History Subset
- Service Record Lookup
- Ride Distance Summation
- Unique Bikes Query
- Write Bike Service Status
- Write Collection Record
- Write Lifetime Status
- Write History Record
- Write Incident Record
- Write Service Record
- Write Workplan Record
- Database Backup Script
- Docker Build Script
- Collections Search UI
- Quick Swap Feature Release
- Strava Sync Config Release
- Strava OAuth Troubleshooting
- Branching & Versioning
- Changelog & Project Board
- Error Page Illustration
- Velo Supervisor Logo
- Component Types Help Page
- Confirm Action Modal
- Documentation Modal
- Edit Installation Modal
- Loading Modal
- Report Modal
- Validation Error Modal
- Project Package Metadata
- v0.1.0 Release Notes
- v0.2.0 Release Notes
- v0.3.0 Release Notes
- v0.3.1 Release Notes
- v0.4.0 Release Notes
- v0.4.1 Release Notes
- v0.4.4 Release Notes

## God Nodes (most connected - your core abstractions)
1. `DatabaseManager` - 65 edges
2. `BusinessLogic` - 61 edges
3. `Meta` - 20 edges
4. `Velo Supervisor 2000 CLAUDE.md` - 17 edges
5. `migrate_database()` - 14 edges
6. `BaseModel` - 13 edges
7. `get_workplan_data_tuple()` - 13 edges
8. `Base Template` - 12 edges
9. `Strava` - 10 edges
10. `get_formatted_datetime_now()` - 10 edges

## Surprising Connections (you probably didn't know these)
- `Version Script CI Workflow` --conceptually_related_to--> `Git Workflow Rules`  [AMBIGUOUS]
  .github/workflows/run_version_script.yml → CLAUDE.md
- `Opt-in Workplan Hub Pattern` --conceptually_related_to--> `Complete Workplan Modal Template`  [INFERRED]
  docs/plans/2026-01-11-workplan-hub-integration-incremental.md → frontend/templates/modal_complete_workplan.html
- `Test Protocols Documentation` --conceptually_related_to--> `Workplan Hub Integration Plan`  [INFERRED]
  tests/README.md → docs/plans/2026-01-11-workplan-hub-integration-incremental.md
- `Opt-in Workplan Hub Pattern` --conceptually_related_to--> `Bike Details Template`  [INFERRED]
  docs/plans/2026-01-11-workplan-hub-integration-incremental.md → frontend/templates/bike_details.html
- `Opt-in Workplan Hub Pattern` --conceptually_related_to--> `Component Details Template`  [INFERRED]
  docs/plans/2026-01-11-workplan-hub-integration-incremental.md → frontend/templates/component_details.html

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Handover Documentation Pattern** — _handovers_template_handover_template, _claude_agents_architect_architect_agent, _claude_agents_code_reviewer_code_reviewer_agent, _claude_agents_database_expert_database_expert_agent, _claude_agents_docs_maintainer_docs_maintainer_agent, _claude_agents_fullstack_developer_fullstack_developer_agent, _claude_agents_product_manager_product_manager_agent, _claude_agents_ux_designer_ux_designer_agent [INFERRED 0.85]
- **Standard Feature Development Workflow** — claude_standard_development_workflow, _claude_agents_product_manager_product_manager_agent, _claude_agents_ux_designer_ux_designer_agent, _claude_agents_architect_architect_agent, _claude_agents_database_expert_database_expert_agent, _claude_agents_fullstack_developer_fullstack_developer_agent, _claude_agents_code_reviewer_code_reviewer_agent, _claude_agents_docs_maintainer_docs_maintainer_agent [EXTRACTED 1.00]
- **Workplan Hub Integration Flow** — docs_plans_2026_01_11_workplan_hub_integration_incremental_doc, frontend_templates_bike_details_template, frontend_templates_component_details_template, frontend_templates_incident_reports_template, frontend_templates_modal_complete_workplan_template [INFERRED 0.85]
- **CSS Inline-Style-to-Class Refactoring Files** — docs_plans_2026_01_11_workplan_hub_integration_incremental_css_refactor_concept, frontend_templates_collection_details_template, frontend_templates_index_template, frontend_templates_component_overview_template, frontend_templates_component_details_template, frontend_templates_bike_details_template, frontend_templates_config_template, frontend_templates_error_template [EXTRACTED 1.00]
- **Shared Status Legend Badge Pattern** — frontend_templates_component_overview_template, frontend_templates_collection_details_template, frontend_templates_index_template [INFERRED 0.85]
- **Generic JS-Driven Utility Modals** — frontend_templates_modal_confirm_confirmmodal, frontend_templates_modal_validation_validationmodal, frontend_templates_modal_report_reportmodal, frontend_templates_modal_docs_docsmodal, frontend_templates_modal_loading_loadingmodal [INFERRED 0.85]
- **Templates Iterating payload.all_components_data** — frontend_templates_modal_incident_record_incidentrecordmodal, frontend_templates_modal_install_component_installcomponentmodal, frontend_templates_modal_quick_swap_quickswapmodal, frontend_templates_modal_workplan_record_workplanrecordmodal [INFERRED 0.90]
- **Workplan-Incident-Service Linking Flow** — frontend_templates_modal_workplan_record_workplanrecordmodal, frontend_templates_modal_incident_record_incidentrecordmodal, frontend_templates_modal_service_record_servicerecordmodal, frontend_templates_modal_link_incident_linkincidentsmodal, frontend_templates_modal_create_services_workplan_createservicesworkplanmodal, frontend_templates_workplan_details_workplandetailspage [INFERRED 0.85]
- **Help Topic Display and Search Flow** — frontend_templates_help_helptopics, frontend_templates_help_showhelptopic, frontend_templates_help_search_functionality [INFERRED 0.85]
- **Breaking Database Schema Change Releases** — readme_v0_4_2, readme_v0_4_3, readme_v0_4_5, readme_v0_4_7, readme_v0_4_9, readme_db_migration_script [EXTRACTED 0.90]
- **Feature Introduction Documented in Help Page** — readme_v0_4_5, readme_v0_4_6, readme_v0_4_7, frontend_templates_help_core_concepts_collections, frontend_templates_help_common_tasks_quick_swap, frontend_templates_help_core_concepts_hybrid_tracking [INFERRED 0.85]

## Communities (105 total, 57 thin omitted)

### Community 0 - "Database Migration Checks"
Cohesion: 0.07
Nodes (41): check_component_types_columns(), check_component_types_time_columns(), check_components_time_columns(), check_incidents_workplan_column(), check_services_workplan_column(), count_component_types_in_use(), create_collections_table(), create_incidents_table() (+33 more)

### Community 1 - "Core Write Endpoints"
Cohesion: 0.07
Nodes (38): add_collection(), add_incident_record(), add_service(), add_workplan(), bulk_add_service_records(), change_collection_status(), component_modify(), component_types_modify() (+30 more)

### Community 2 - "Database ORM Models"
Cohesion: 0.09
Nodes (33): BaseModel, Bikes, Collections, ComponentHistory, Components, ComponentTypes, Incidents, Meta (+25 more)

### Community 3 - "Frontend UI Initialization"
Cohesion: 0.08
Nodes (7): editCollection(), handleUpdate(), initializeComponentSelector(), NOTE: All collection details page handlers are in the "Functions used on…, IMPORTANT: Remove readonly - allow manual typing, showToast(), updateFormFields()

### Community 4 - "Workplan Hub Templates"
Cohesion: 0.14
Nodes (25): CSS Inline-Style-to-Class Refactoring, Workplan Hub Integration Plan, Opt-in Workplan Hub Pattern, Base Template, btn_new_incident Macro (Bike Details), btn_new_workplan Macro (Bike Details), Bike Details Template, Collection Details Template (+17 more)

### Community 5 - "Page Route Endpoints"
Cohesion: 0.11
Nodes (24): add_history_record(), collection_details(), component_overview(), component_types_overview(), help_page(), incident_reports(), Request, Endpoint for incident reports page (+16 more)

### Community 6 - "Agent Team Documentation"
Cohesion: 0.20
Nodes (21): Architect Agent, Code Reviewer Agent, Database Expert Agent, Docs Maintainer Agent, Fullstack Developer Agent, Product Manager Agent, UX Designer Agent, Version Script CI Workflow (+13 more)

### Community 7 - "Database Manager Reads"
Cohesion: 0.11
Nodes (10): DatabaseManager, Method to read installed components for a specific bike, Class to interact with a SQLite database through Peewee, Method to read a subset of records from the component history table, Method to retrieve the oldest record from the service log of a given component, Method to read incident records with status 'Open, Method to create or update ride data in bulk in database, Method to update component distance in database (+2 more)

### Community 8 - "Component Overview Payloads"
Cohesion: 0.14
Nodes (11): Method to produce payload for page component overview, Method to determine which factor triggered a warning status, Calculate lifetime and service triggers for a component, Method to create component-to-collection mapping dictionaries, Method to produce payload for displaying table of all collections, Method to produce payload for page bike details, Method to read content of components table as formatted tuples, format_component_status() (+3 more)

### Community 9 - "Core Concepts Documentation"
Cohesion: 0.12
Nodes (17): Current Version Marker (v0.4.9.6efc337), Collections (Core Concept), Component Types vs Components, Hybrid Time + Distance Tracking, Mileage Tracking, Understanding Thresholds, Getting Started: Define Component Types, Incidents Page (+9 more)

### Community 10 - "Strava API Integration"
Cohesion: 0.18
Nodes (9): Class to interact with Strava API, Method to authenticate and get data from Stravas gear API, Method to prepare a list of rides, Method to prepare a list of bikes, Method to read oauth options from file, Method to save oauth options to file, Method to authenticate and get data from Stravas activities API, Method to authenticate and get the full list of bike ids from the athlete's… (+1 more)

### Community 11 - "Scheduler & Module Overview"
Cohesion: 0.14
Nodes (12): Module to handle business logic, Module for interaction with a Sqlite database, Initialize and start the APScheduler instance, Scheduler for automated maintenance tasks, Gracefully shutdown the APScheduler instance, Scheduled job to update time-based status fields for all non-retired components, Scheduled job to sync Strava activities, start_scheduler() (+4 more)

### Community 12 - "Component Status Computation"
Cohesion: 0.18
Nodes (10): Method to update component table with service status, Method to update component lifetime and service status when no installation…, Method to compute component status using threshold logic, Method to determine worst-case status between distance and days-based…, Method to update time-based status fields for all non-retired components, Method to update component table with lifetime status, calculate_elapsed_days(), get_formatted_datetime_now() (+2 more)

### Community 13 - "Workplan & Incident Payloads"
Cohesion: 0.17
Nodes (13): Method to produce payload for page incident reports, Method to produce payload for workplan details page, Method to check if all affected components have linked services, generate_workplan_title(), get_workplan_data_tuple(), get_workplan_names_dict(), parse_checkbox_progress(), Build dictionary mapping workplan_id -> workplan_name for all workplans (+5 more)

### Community 14 - "Component History Processing"
Cohesion: 0.22
Nodes (7): Method to update status for a given bike based on component service and…, Method to update component details, Method to calculate distance and bike id for history records, Method to calculate distance and bike id for service records, Method to update only the count of components for a given component type, Method to delete a given record and associated records, Method to update component table with distance from ride table

### Community 15 - "Exception Handling Middleware"
Cohesion: 0.16
Nodes (11): http_exception_handler(), Function to catch http errors from Uvicorn and return them to the middleware, Middleware, Request, Class to handle exceptions that breaks the program and should be shown to the…, Method to dispatch intercepted requests, Method to catch and handle exceptions, BaseHTTPMiddleware (+3 more)

### Community 16 - "Config & Version Utilities"
Cohesion: 0.18
Nodes (13): Endpoint to update config file based on which form was submitted, update_config(), get_current_version(), parse_button_sorting(), Helper function to shutdown the server after a short delay, Function to get current program version, Module for auxiliary functions, Function to read configuration file (+5 more)

### Community 17 - "BusinessLogic Class Core"
Cohesion: 0.18
Nodes (7): BusinessLogic, Method to refresh all bikes from Strava, Function to set the date for last pull from Strava, Class that contains business logic, Method to produce payload for page component types, Method to create or update ride data in bulk to database, Method to determine which selection of components to update

### Community 18 - "Create Record Operations"
Cohesion: 0.17
Nodes (7): Method to create collection, Method to add incident record, Method to update incident record (supports full or partial updates), Method to add workplan and optionally link to source incident, Method to update workplan (supports full or partial updates), generate_unique_id(), Function to generates a random and unique ID

### Community 19 - "Single Record Reads"
Cohesion: 0.17
Nodes (6): Method to retrieve record for a specific entry in the installation log, Method to retrieve a specific service record, Method to retrieve record for a specific collection, Method to retrieve record for a specific incident report, Method to retrieve record for a specific workplan, Method to delete a given record and associated records

### Community 20 - "Collection Status Logic"
Cohesion: 0.20
Nodes (5): Method to update collection, Method to validate collections before allowing bulk operations, Method to change status of all components in a collection, Calculate status flags for a collection based on its components., Method to produce payload for collection details page

### Community 21 - "Component Creation & Quick Swap"
Cohesion: 0.24
Nodes (5): Method to create component, Method to create installation history record, Method to orchestrate swap of one component with another, Method to validate quick swap operation, Method to check if a bike has all mandatory components and respects max…

### Community 22 - "Bike & Component Payloads"
Cohesion: 0.22
Nodes (6): Method to produce payload for page component details, Method to produce payload for page bike overview, Method to build dictionaries of bike and component ids referenced in received…, Method to build dictionaries of bike and component ids referenced in received…, calculate_percentage_reached(), Function to calculate remaining service interval or remaining lifetime as…

### Community 23 - "Form Init & Validation"
Cohesion: 0.20
Nodes (9): initializeDatePickers(), initializeIncidentForm(), initializeWorkplanForm(), submitCollectionAjax(), submitComponentAjax(), validateCollectionStatusChange(), validateDateInput(), validateIncidentForm() (+1 more)

### Community 24 - "Service Record Operations"
Cohesion: 0.25
Nodes (4): Method to add service record, Method to bulk create service records for multiple components linked to a…, Method to update a service record, Method to validate service records before processing and storing in database

### Community 25 - "Incident Data Helpers"
Cohesion: 0.29
Nodes (7): Method to get incidents that can be linked to a workplan, generate_incident_title(), get_incident_data_tuple(), parse_json_string(), Build standard incident data tuple for display (15 fields), Function to load a JSON string and return the parsed data as a python object, Generate a concise title for an incident

### Community 26 - "Table Sorting & Filtering"
Cohesion: 0.29
Nodes (8): initializeCollectionsSorting(), sortColumn(), initializeWorkplanTable(), setupIncidentTableSorting(), setupWorkplanSearch(), setupWorkplanStatusFiltering(), setupWorkplanTableSorting(), updateWorkplansVisibility()

### Community 27 - "Python Dependencies List"
Cohesion: 0.25
Nodes (8): APScheduler, Python Requirements List, FastAPI, Jinja2, Peewee ORM, python-multipart, requests-oauthlib, Uvicorn

### Community 28 - "Workplan & Incident Modals"
Cohesion: 0.48
Nodes (7): Create Services For Workplan Modal, Incident Record Modal, Link Incident To Workplan Modal, Service Record Modal, Workplan Record Modal, Workplan Details Page, Workplans List Page

### Community 29 - "History Record Validation"
Cohesion: 0.33
Nodes (4): Method to update a component history record with validation, Method to validate history records before processing and storing in database, Function to validate that a date string matches the required format YYYY-MM-DD…, validate_date_format()

### Community 30 - "Bike Data Access"
Cohesion: 0.33
Nodes (3): Method to retrieve record for a specific bike, Method to get the name of a bike based on bike id, Method to create or update bike data to the database

### Community 31 - "Component Data Access"
Cohesion: 0.33
Nodes (3): Method to get component names based on list of ids, Method to retrieve record for a specific component, Method to create or update component data to the database

### Community 32 - "Detail Page Endpoints"
Cohesion: 0.33
Nodes (6): bike_details(), component_details(), Endpoint for component details page, Endpoint for bike details page, get_button_order(), Function to get button order for a specific page with defaults

### Community 33 - "Form Validation Helpers"
Cohesion: 0.33
Nodes (6): addFormValidation(), clearValidationErrors(), showFieldError(), showValidationModal(), validateComponentThresholds(), validateQuickSwapForm()

### Community 34 - "Workplans & Bikes Lists"
Cohesion: 0.50
Nodes (3): Method to produce payload for page of all workplans, get_formatted_bikes_list(), Function to get list of all bikes, with prefix for retired bikes

### Community 37 - "Config Page Endpoint"
Cohesion: 0.50
Nodes (4): config_overview(), Endpoint for component types page, get_button_sorting_config(), Function to get button sorting configuration for config page

### Community 38 - "Filtered Log Endpoint"
Cohesion: 0.50
Nodes (4): get_filtered_log(), Endpoint to read log and return only business events, Function to get filtered log records, read_filtered_logs()

### Community 39 - "Version Script"
Cohesion: 0.50
Nodes (3): get_git_info(), Script to maintain version number, Function to get latest version number and commit hash

### Community 40 - "Help Page Dev Docs"
Cohesion: 0.50
Nodes (4): CLAUDE.md, Data Management Tips, Need More Help? (Troubleshooting), Handover Documents Directory (.handovers/)

### Community 41 - "Bulk Action Handlers"
Cohesion: 0.50
Nodes (4): cleanup(), handleCancel(), handleConfirm(), performBulkStatusChange()

### Community 42 - "Markdown Preview Rendering"
Cohesion: 0.50
Nodes (4): containsMarkdown(), renderPreview(), setInitialMode(), updateCheckboxInText()

### Community 43 - "Incident Table Filtering"
Cohesion: 0.67
Nodes (4): initializeIncidentTable(), setupIncidentSearch(), setupIncidentStatusFiltering(), updateIncidentVisibility()

### Community 44 - "Help Page Search"
Cohesion: 0.50
Nodes (4): helpTopics Data Object, Help Page Template, Help Search Functionality, showHelpTopic() Function

### Community 45 - "Component Modals"
Cohesion: 0.67
Nodes (4): Component Type Modal, Create Component Modal, Quick Swap Modal, Update Component Details Modal

### Community 46 - "Quick Swap Filters"
Cohesion: 0.67
Nodes (3): filterNewComponentsByType(), handleOldComponentChange(), updateQuickSwapCollectionWarning()

### Community 47 - "Status Update Modals"
Cohesion: 0.67
Nodes (3): Install Component Modal, Update Collection Status Modal, Update Component Status Modal

### Community 48 - "Project Meta Info"
Cohesion: 0.67
Nodes (3): GitHub Issues Tracker, Graphify Knowledge Graph Auto-Update Mechanism, Velo Supervisor 2000 (Project)

## Ambiguous Edges - Review These
- `Version Script CI Workflow` → `Git Workflow Rules`  [AMBIGUOUS]
  .github/workflows/run_version_script.yml · relation: conceptually_related_to

## Knowledge Gaps
- **61 isolated node(s):** `backup_db.sh script`, `create-container-vs2000.sh script`, `velo-supervisor-2000`, `Version Script CI Workflow`, `Handover Template` (+56 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 335 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **57 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `Version Script CI Workflow` and `Git Workflow Rules`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **Why does `DatabaseManager` connect `Database Manager Reads` to `Database ORM Models`, `Component Overview Payloads`, `Scheduler & Module Overview`, `Single Record Reads`, `Bike Data Access`, `Component Data Access`, `Component Type Data Access`, `Component Type Usage Count`, `Read All Collections`, `Read All Component Types`, `Read All Components`, `Read All Incidents`, `Read All Workplans`, `Recent Bike History Lookup`, `Read All Bikes`, `Collection Lookup By Component`, `Incidents By Workplan`, `Latest History Record`, `Latest Ride Record`, `Latest Service Record`, `Matching Rides Lookup`, `Oldest History Record`, `Planned Workplans Lookup`, `Recent Rides Lookup`, `Services By Workplan`, `Bike Component Subset`, `Service History Subset`, `Service Record Lookup`, `Ride Distance Summation`, `Unique Bikes Query`, `Write Bike Service Status`, `Write Collection Record`, `Write Lifetime Status`, `Write History Record`, `Write Incident Record`, `Write Service Record`, `Write Workplan Record`?**
  _High betweenness centrality (0.179) - this node is a cross-community bridge._
- **Why does `BusinessLogic` connect `BusinessLogic Class Core` to `Workplans & Bikes Lists`, `Component Type Validation`, `Component Overview Payloads`, `Scheduler & Module Overview`, `Component Status Computation`, `Workplan & Incident Payloads`, `Component History Processing`, `Create Record Operations`, `Collection Status Logic`, `Component Creation & Quick Swap`, `Bike & Component Payloads`, `Service Record Operations`, `Incident Data Helpers`, `History Record Validation`?**
  _High betweenness centrality (0.137) - this node is a cross-community bridge._
- **Why does `Strava` connect `Strava API Integration` to `Scheduler & Module Overview`?**
  _High betweenness centrality (0.030) - this node is a cross-community bridge._
- **Are the 9 inferred relationships involving `DatabaseManager` (e.g. with `Bikes` and `Collections`) actually correct?**
  _`DatabaseManager` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `BusinessLogic` (e.g. with `strava_sync_job()` and `update_time_based_fields_job()`) actually correct?**
  _`BusinessLogic` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `backup_db.sh script`, `create-container-vs2000.sh script`, `velo-supervisor-2000` to the rest of the system?**
  _61 weakly-connected nodes found - possible documentation gaps or missing edges._