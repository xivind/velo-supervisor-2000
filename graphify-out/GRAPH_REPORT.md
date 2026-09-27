# Graph Report - velo-supervisor-2000  (2026-09-17)

## Corpus Check
- 71 files · ~129,418 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 670 nodes · 1021 edges · 94 communities (34 shown, 59 thin omitted)
- Extraction: 88% EXTRACTED · 11% INFERRED · 0% AMBIGUOUS · INFERRED: 117 edges (avg confidence: 0.87)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Workplan & Config Utilities
- Database Migration Checks
- Workplan Hub Templates
- Component & Bike Payloads
- Database ORM Models
- Scheduler & Module Overview
- Component Status Computation
- Frontend UI Initialization
- Page Route Endpoints
- Agent Team Documentation
- BusinessLogic Class Core
- Create & Modify Endpoints
- Database Manager Reads
- Core Concepts Documentation
- Service & History Validation
- Component Creation & Quick Swap
- Exception Handling Middleware
- App Startup & Routing
- Collection Status Logic
- Single Record Reads
- Form Init & Validation
- Table Sorting & Filtering
- Python Dependencies List
- Bike Data Access
- Component Data Access
- Detail Page Endpoints
- Form Validation Helpers
- Component Type Data Access
- Version Script
- Help Page Dev Docs
- Bulk Action Handlers
- Markdown Preview Rendering
- Incident Table Filtering
- Help Page Search
- Quick Swap Filters
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
- Component Type Modify Endpoint
- Delete Record Endpoint
- Update Incident Endpoint
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
8. `Bike Details Template` - 13 edges
9. `Component Details Template` - 13 edges
10. `Base Template` - 12 edges

## Surprising Connections (you probably didn't know these)
- `Version Script CI Workflow` --conceptually_related_to--> `Git Workflow Rules`  [AMBIGUOUS]
  .github/workflows/run_version_script.yml → CLAUDE.md
- `Opt-in Workplan Hub Pattern` --conceptually_related_to--> `Complete Workplan Modal Template`  [INFERRED]
  docs/plans/2026-01-11-workplan-hub-integration-incremental.md → frontend/templates/modal_complete_workplan.html
- `Manual Onboarding Setup Procedure` --conceptually_related_to--> `Getting Started: Define Component Types`  [INFERRED]
  README.md → frontend/templates/help.html
- `Getting Started: Define Component Types` --conceptually_related_to--> `v0.4.2 Release`  [INFERRED]
  frontend/templates/help.html → README.md
- `Incidents Page` --conceptually_related_to--> `v0.4.3 Release`  [INFERRED]
  frontend/templates/help.html → README.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Handover Documentation Pattern** — _handovers_template_handover_template, _claude_agents_architect_architect_agent, _claude_agents_code_reviewer_code_reviewer_agent, _claude_agents_database_expert_database_expert_agent, _claude_agents_docs_maintainer_docs_maintainer_agent, _claude_agents_fullstack_developer_fullstack_developer_agent, _claude_agents_product_manager_product_manager_agent, _claude_agents_ux_designer_ux_designer_agent [INFERRED 0.85]
- **Standard Feature Development Workflow** — claude_standard_development_workflow, _claude_agents_product_manager_product_manager_agent, _claude_agents_ux_designer_ux_designer_agent, _claude_agents_architect_architect_agent, _claude_agents_database_expert_database_expert_agent, _claude_agents_fullstack_developer_fullstack_developer_agent, _claude_agents_code_reviewer_code_reviewer_agent, _claude_agents_docs_maintainer_docs_maintainer_agent [EXTRACTED 1.00]
- **Breaking Database Schema Change Releases** — readme_v0_4_2, readme_v0_4_3, readme_v0_4_5, readme_v0_4_7, readme_v0_4_9, readme_db_migration_script [EXTRACTED 0.90]
- **Feature Introduction Documented in Help Page** — readme_v0_4_5, readme_v0_4_6, readme_v0_4_7, frontend_templates_help_core_concepts_collections, frontend_templates_help_common_tasks_quick_swap, frontend_templates_help_core_concepts_hybrid_tracking [INFERRED 0.85]
- **Workplan Hub Integration Flow** — docs_plans_2026_01_11_workplan_hub_integration_incremental_doc, frontend_templates_bike_details_template, frontend_templates_component_details_template, frontend_templates_incident_reports_template, frontend_templates_modal_complete_workplan_template [INFERRED 0.85]
- **CSS Inline-Style-to-Class Refactoring Files** — docs_plans_2026_01_11_workplan_hub_integration_incremental_css_refactor_concept, frontend_templates_collection_details_template, frontend_templates_index_template, frontend_templates_component_overview_template, frontend_templates_component_details_template, frontend_templates_bike_details_template, frontend_templates_config_template, frontend_templates_error_template [EXTRACTED 1.00]
- **Shared Status Legend Badge Pattern** — frontend_templates_component_overview_template, frontend_templates_collection_details_template, frontend_templates_index_template [INFERRED 0.85]
- **Help Topic Display and Search Flow** — frontend_templates_help_helptopics, frontend_templates_help_showhelptopic, frontend_templates_help_search_functionality [INFERRED 0.85]
- **Generic JS-Driven Utility Modals** — frontend_templates_modal_confirm_confirmmodal, frontend_templates_modal_validation_validationmodal, frontend_templates_modal_report_reportmodal, frontend_templates_modal_docs_docsmodal, frontend_templates_modal_loading_loadingmodal [INFERRED 0.85]
- **Templates Iterating payload.all_components_data** — frontend_templates_modal_incident_record_incidentrecordmodal, frontend_templates_modal_install_component_installcomponentmodal, frontend_templates_modal_quick_swap_quickswapmodal, frontend_templates_modal_workplan_record_workplanrecordmodal [INFERRED 0.90]
- **Workplan-Incident-Service Linking Flow** — frontend_templates_modal_workplan_record_workplanrecordmodal, frontend_templates_modal_incident_record_incidentrecordmodal, frontend_templates_modal_service_record_servicerecordmodal, frontend_templates_modal_link_incident_linkincidentsmodal, frontend_templates_modal_create_services_workplan_createservicesworkplanmodal, frontend_templates_workplan_details_workplandetailspage [INFERRED 0.85]

## Communities (94 total, 59 thin omitted)

### Community 0 - "Workplan & Config Utilities"
Cohesion: 0.07
Nodes (40): Method to produce payload for workplan details page, Method to check if all affected components have linked services, Method to get incidents that can be linked to a workplan, get_filtered_log(), Endpoint to update config file based on which form was submitted, Endpoint to read log and return only business events, update_config(), calculate_elapsed_days() (+32 more)

### Community 1 - "Database Migration Checks"
Cohesion: 0.07
Nodes (41): check_component_types_columns(), check_component_types_time_columns(), check_components_time_columns(), check_incidents_workplan_column(), check_services_workplan_column(), count_component_types_in_use(), create_collections_table(), create_incidents_table() (+33 more)

### Community 2 - "Workplan Hub Templates"
Cohesion: 0.10
Nodes (42): CSS Inline-Style-to-Class Refactoring, Workplan Hub Integration Plan, Opt-in Workplan Hub Pattern, Base Template, btn_new_incident Macro (Bike Details), btn_new_workplan Macro (Bike Details), Bike Details Template, Collection Details Template (+34 more)

### Community 3 - "Component & Bike Payloads"
Cohesion: 0.09
Nodes (21): Method to produce payload for page component overview, Method to produce payload for page component details, Method to determine which factor triggered a warning status, Calculate lifetime and service triggers for a component, Method to produce payload for page bike overview, Method to create component-to-collection mapping dictionaries, Method to produce payload for displaying table of all collections, Method to produce payload for page incident reports (+13 more)

### Community 4 - "Database ORM Models"
Cohesion: 0.09
Nodes (33): BaseModel, Bikes, Collections, ComponentHistory, Components, ComponentTypes, Incidents, Meta (+25 more)

### Community 5 - "Scheduler & Module Overview"
Cohesion: 0.08
Nodes (21): Module to handle business logic, Module for interaction with a Sqlite database, Initialize and start the APScheduler instance, Scheduler for automated maintenance tasks, Gracefully shutdown the APScheduler instance, Scheduled job to update time-based status fields for all non-retired components, Scheduled job to sync Strava activities, start_scheduler() (+13 more)

### Community 6 - "Component Status Computation"
Cohesion: 0.11
Nodes (16): Method to update component table with service status, Method to update component lifetime and service status when no installation…, Method to update status for a given bike based on component service and…, Method to update component details, Method to calculate distance and bike id for history records, Method to calculate distance and bike id for service records, Method to compute component status using threshold logic, Method to determine worst-case status between distance and days-based… (+8 more)

### Community 7 - "Frontend UI Initialization"
Cohesion: 0.08
Nodes (7): editCollection(), handleUpdate(), initializeComponentSelector(), NOTE: All collection details page handlers are in the "Functions used on…, IMPORTANT: Remove readonly - allow manual typing, showToast(), updateFormFields()

### Community 8 - "Page Route Endpoints"
Cohesion: 0.10
Nodes (26): add_history_record(), collection_details(), component_overview(), component_types_overview(), config_overview(), help_page(), incident_reports(), Request (+18 more)

### Community 9 - "Agent Team Documentation"
Cohesion: 0.20
Nodes (21): Architect Agent, Code Reviewer Agent, Database Expert Agent, Docs Maintainer Agent, Fullstack Developer Agent, Product Manager Agent, UX Designer Agent, Version Script CI Workflow (+13 more)

### Community 10 - "BusinessLogic Class Core"
Cohesion: 0.12
Nodes (11): BusinessLogic, Validate threshold configuration rules for component intervals, Method to update incident record (supports full or partial updates), Method to add workplan and optionally link to source incident, Method to update workplan (supports full or partial updates), Method to create or update component types, Function to set the date for last pull from Strava, Class that contains business logic (+3 more)

### Community 11 - "Create & Modify Endpoints"
Cohesion: 0.10
Nodes (21): add_collection(), add_service(), add_workplan(), change_collection_status(), component_modify(), create_component(), quick_swap(), Endpoint to modify component types (+13 more)

### Community 12 - "Database Manager Reads"
Cohesion: 0.11
Nodes (10): DatabaseManager, Method to read installed components for a specific bike, Class to interact with a SQLite database through Peewee, Method to read a subset of records from the component history table, Method to retrieve the oldest record from the service log of a given component, Method to read incident records with status 'Open, Method to create or update ride data in bulk in database, Method to update component distance in database (+2 more)

### Community 13 - "Core Concepts Documentation"
Cohesion: 0.13
Nodes (16): Collections (Core Concept), Component Types vs Components, Hybrid Time + Distance Tracking, Mileage Tracking, Understanding Thresholds, Getting Started: Define Component Types, Incidents Page, Workplans Page (+8 more)

### Community 14 - "Service & History Validation"
Cohesion: 0.14
Nodes (8): Method to update a component history record with validation, Method to validate history records before processing and storing in database, Method to add service record, Method to bulk create service records for multiple components linked to a…, Method to update a service record, Method to validate service records before processing and storing in database, Function to validate that a date string matches the required format YYYY-MM-DD…, validate_date_format()

### Community 15 - "Component Creation & Quick Swap"
Cohesion: 0.18
Nodes (8): Method to create component, Method to create installation history record, Method to orchestrate swap of one component with another, Method to validate quick swap operation, Method to check if a bike has all mandatory components and respects max…, Method to add incident record, generate_unique_id(), Function to generates a random and unique ID

### Community 16 - "Exception Handling Middleware"
Cohesion: 0.16
Nodes (11): http_exception_handler(), Function to catch http errors from Uvicorn and return them to the middleware, Middleware, Request, Class to handle exceptions that breaks the program and should be shown to the…, Method to dispatch intercepted requests, Method to catch and handle exceptions, BaseHTTPMiddleware (+3 more)

### Community 17 - "App Startup & Routing"
Cohesion: 0.18
Nodes (11): add_incident_record(), bulk_add_service_records(), lifespan(), Route handlers for Velo Supervisor 2000, Manage application startup and shutdown, Endpoint to bulk add service records for workplan components, Endpoint to create an incident record, Endpoint to update a workplan (supports full or partial updates) (+3 more)

### Community 18 - "Collection Status Logic"
Cohesion: 0.17
Nodes (6): Method to create collection, Method to update collection, Method to validate collections before allowing bulk operations, Method to change status of all components in a collection, Calculate status flags for a collection based on its components., Method to produce payload for collection details page

### Community 19 - "Single Record Reads"
Cohesion: 0.17
Nodes (6): Method to retrieve record for a specific entry in the installation log, Method to retrieve a specific service record, Method to retrieve record for a specific collection, Method to retrieve record for a specific incident report, Method to retrieve record for a specific workplan, Method to delete a given record and associated records

### Community 20 - "Form Init & Validation"
Cohesion: 0.20
Nodes (9): initializeDatePickers(), initializeIncidentForm(), initializeWorkplanForm(), submitCollectionAjax(), submitComponentAjax(), validateCollectionStatusChange(), validateDateInput(), validateIncidentForm() (+1 more)

### Community 21 - "Table Sorting & Filtering"
Cohesion: 0.29
Nodes (8): initializeCollectionsSorting(), sortColumn(), initializeWorkplanTable(), setupIncidentTableSorting(), setupWorkplanSearch(), setupWorkplanStatusFiltering(), setupWorkplanTableSorting(), updateWorkplansVisibility()

### Community 22 - "Python Dependencies List"
Cohesion: 0.25
Nodes (8): APScheduler, Python Requirements List, FastAPI, Jinja2, Peewee ORM, python-multipart, requests-oauthlib, Uvicorn

### Community 23 - "Bike Data Access"
Cohesion: 0.33
Nodes (3): Method to retrieve record for a specific bike, Method to get the name of a bike based on bike id, Method to create or update bike data to the database

### Community 24 - "Component Data Access"
Cohesion: 0.33
Nodes (3): Method to get component names based on list of ids, Method to retrieve record for a specific component, Method to create or update component data to the database

### Community 25 - "Detail Page Endpoints"
Cohesion: 0.33
Nodes (6): bike_details(), component_details(), Endpoint for component details page, Endpoint for bike details page, get_button_order(), Function to get button order for a specific page with defaults

### Community 26 - "Form Validation Helpers"
Cohesion: 0.33
Nodes (6): addFormValidation(), clearValidationErrors(), showFieldError(), showValidationModal(), validateComponentThresholds(), validateQuickSwapForm()

### Community 28 - "Version Script"
Cohesion: 0.50
Nodes (3): get_git_info(), Script to maintain version number, Function to get latest version number and commit hash

### Community 29 - "Help Page Dev Docs"
Cohesion: 0.50
Nodes (4): CLAUDE.md, Data Management Tips, Need More Help? (Troubleshooting), Handover Documents Directory (.handovers/)

### Community 30 - "Bulk Action Handlers"
Cohesion: 0.50
Nodes (4): cleanup(), handleCancel(), handleConfirm(), performBulkStatusChange()

### Community 31 - "Markdown Preview Rendering"
Cohesion: 0.50
Nodes (4): containsMarkdown(), renderPreview(), setInitialMode(), updateCheckboxInText()

### Community 32 - "Incident Table Filtering"
Cohesion: 0.67
Nodes (4): initializeIncidentTable(), setupIncidentSearch(), setupIncidentStatusFiltering(), updateIncidentVisibility()

### Community 33 - "Help Page Search"
Cohesion: 0.50
Nodes (4): helpTopics Data Object, Help Page Template, Help Search Functionality, showHelpTopic() Function

### Community 34 - "Quick Swap Filters"
Cohesion: 0.67
Nodes (3): filterNewComponentsByType(), handleOldComponentChange(), updateQuickSwapCollectionWarning()

## Ambiguous Edges - Review These
- `Version Script CI Workflow` → `Git Workflow Rules`  [AMBIGUOUS]
  .github/workflows/run_version_script.yml · relation: conceptually_related_to

## Knowledge Gaps
- **56 isolated node(s):** `backup_db.sh script`, `create-container-vs2000.sh script`, `velo-supervisor-2000`, `Version Script CI Workflow`, `Handover Template` (+51 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 330 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **59 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `Version Script CI Workflow` and `Git Workflow Rules`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **Why does `DatabaseManager` connect `Database Manager Reads` to `Component & Bike Payloads`, `Database ORM Models`, `Scheduler & Module Overview`, `Single Record Reads`, `Bike Data Access`, `Component Data Access`, `Component Type Data Access`, `Component Type Usage Count`, `Read All Collections`, `Read All Component Types`, `Read All Components`, `Read All Incidents`, `Read All Workplans`, `Recent Bike History Lookup`, `Read All Bikes`, `Collection Lookup By Component`, `Incidents By Workplan`, `Latest History Record`, `Latest Ride Record`, `Latest Service Record`, `Matching Rides Lookup`, `Oldest History Record`, `Planned Workplans Lookup`, `Recent Rides Lookup`, `Services By Workplan`, `Bike Component Subset`, `Service History Subset`, `Service Record Lookup`, `Ride Distance Summation`, `Unique Bikes Query`, `Write Bike Service Status`, `Write Collection Record`, `Write Lifetime Status`, `Write History Record`, `Write Incident Record`, `Write Service Record`, `Write Workplan Record`?**
  _High betweenness centrality (0.180) - this node is a cross-community bridge._
- **Why does `BusinessLogic` connect `BusinessLogic Class Core` to `Workplan & Config Utilities`, `Component & Bike Payloads`, `Scheduler & Module Overview`, `Component Status Computation`, `Service & History Validation`, `Component Creation & Quick Swap`, `Collection Status Logic`?**
  _High betweenness centrality (0.138) - this node is a cross-community bridge._
- **Are the 9 inferred relationships involving `DatabaseManager` (e.g. with `Bikes` and `Collections`) actually correct?**
  _`DatabaseManager` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `BusinessLogic` (e.g. with `strava_sync_job()` and `update_time_based_fields_job()`) actually correct?**
  _`BusinessLogic` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `backup_db.sh script`, `create-container-vs2000.sh script`, `velo-supervisor-2000` to the rest of the system?**
  _56 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Workplan & Config Utilities` be split into smaller, more focused modules?**
  _Cohesion score 0.06553911205073996 - nodes in this community are weakly interconnected._