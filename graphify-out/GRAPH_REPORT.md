# Graph Report - velo-supervisor-2000  (2026-08-16)

## Corpus Check
- 80 files · ~139,901 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 644 nodes · 1007 edges · 85 communities (41 shown, 44 thin omitted)
- Extraction: 88% EXTRACTED · 11% INFERRED · 0% AMBIGUOUS · INFERRED: 115 edges (avg confidence: 0.78)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Backend Module Entry Points
- Strava API Integration
- Database Models: Bikes & Services
- Error Handling Middleware
- Database Models: Core Tables
- Business Logic Core
- Components Table Model
- Database Manager Core
- DB Migration Script
- Component Status Updates
- Creation & Validation Logic
- Record Update & Refresh Logic
- Service Record Validation
- Main API Routes
- Collection Status Logic
- Single-Record Reads
- Form Init & Validation JS
- APScheduler Jobs
- Table Sorting & Search JS
- Bike Data Access
- Component Data Access
- Details Page Endpoints
- Bike & Component Queries
- Form Validation Helpers JS
- Component Type Data Access
- Config Page Endpoint
- Log Filtering
- Config Update & Shutdown
- Bulk Action Handlers JS
- Markdown Preview JS
- Workplan Table Filtering JS
- Version Info
- Frontend JS Core
- Quick Swap Helpers JS
- Component Type Usage Count
- Read All Collections
- Read All Component Types
- Read All Components
- Read All Incidents
- Read All Workplans
- Bike From History
- Read Bikes Table
- Page Endpoint Handlers
- Collection By Component
- Incidents By Workplan
- Latest History Record
- Latest Ride Record
- Latest Service Record
- Matching Rides Query
- Oldest History Record
- Planned Workplans Query
- Recent Rides Query
- Services By Workplan
- Components By Bike
- Service History Subset
- Service Record Subset
- Ride Distance Sum
- Unique Bike IDs
- Bike Service Status Write
- Collection Write
- Component Lifetime Status Write
- History Record Write
- Incident Record Write
- Service Record Write
- Workplan Write
- Collections Search JS
- Workplan Business Logic
- DB Backup Script
- Docker Deploy Script
- Workplan Hub & Templates
- Graphify Skill Docs
- Python Dependencies
- Workplan-Related Modals
- Component Modals
- Status Update Modals
- Agent Team & Workflow
- Error Page Illustration
- App Logo
- Confirm Action Modal
- Documentation Modal
- Edit Installation Record Modal
- Loading Modal
- Report Modal
- Validation Error Modal

## God Nodes (most connected - your core abstractions)
1. `DatabaseManager` - 65 edges
2. `BusinessLogic` - 61 edges
3. `Meta` - 20 edges
4. `Velo Supervisor 2000 CLAUDE.md` - 17 edges
5. `migrate_database()` - 14 edges
6. `BaseModel` - 13 edges
7. `get_workplan_data_tuple()` - 13 edges
8. `Base Template` - 13 edges
9. `graphify Skill` - 11 edges
10. `get_formatted_datetime_now()` - 10 edges

## Surprising Connections (you probably didn't know these)
- `get_filtered_log()` --calls--> `fetchLogs()`  [EXTRACTED]
  backend/main.py → frontend/static/js/main.js
- `Complete Workplan Modal Template` --conceptually_related_to--> `Opt-in Workplan Hub Pattern`  [INFERRED]
  frontend/templates/modal_complete_workplan.html → docs/plans/2026-01-11-workplan-hub-integration-incremental.md
- `Current Version File (v0.4.9.1f9734e)` --conceptually_related_to--> `Workplan Hub Integration Plan`  [INFERRED]
  backend/current_version.txt → docs/plans/2026-01-11-workplan-hub-integration-incremental.md
- `Workplan Hub Integration Plan` --conceptually_related_to--> `Test Protocols Documentation`  [INFERRED]
  docs/plans/2026-01-11-workplan-hub-integration-incremental.md → tests/README.md
- `Git Workflow Rules` --conceptually_related_to--> `Version Script CI Workflow`  [AMBIGUOUS]
  CLAUDE.md → .github/workflows/run_version_script.yml

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **CSS Inline-Style-to-Class Refactoring Files** — docs_plans_2026_01_11_workplan_hub_integration_incremental_css_refactor_concept, frontend_templates_collection_details_template, frontend_templates_index_template, frontend_templates_component_overview_template, frontend_templates_component_details_template, frontend_templates_bike_details_template, frontend_templates_config_template, frontend_templates_error_template [EXTRACTED 1.00]
- **Semantic Extraction Subagent Pipeline** — _claude_skills_graphify_skill_graphify_skill, _claude_skills_graphify_references_extraction_spec_extraction_prompt_spec, _claude_skills_graphify_references_extraction_spec_node_id_format, _claude_skills_graphify_references_extraction_spec_confidence_rubric [EXTRACTED 1.00]
- **Standard Feature Development Workflow** — claude_standard_development_workflow, _claude_agents_product_manager_product_manager_agent, _claude_agents_ux_designer_ux_designer_agent, _claude_agents_architect_architect_agent, _claude_agents_database_expert_database_expert_agent, _claude_agents_fullstack_developer_fullstack_developer_agent, _claude_agents_code_reviewer_code_reviewer_agent, _claude_agents_docs_maintainer_docs_maintainer_agent [EXTRACTED 1.00]
- **Generic JS-Driven Utility Modals** — frontend_templates_modal_confirm_confirmmodal, frontend_templates_modal_validation_validationmodal, frontend_templates_modal_report_reportmodal, frontend_templates_modal_docs_docsmodal, frontend_templates_modal_loading_loadingmodal [INFERRED 0.85]
- **Handover Documentation Pattern** — _handovers_template_handover_template, _claude_agents_architect_architect_agent, _claude_agents_code_reviewer_code_reviewer_agent, _claude_agents_database_expert_database_expert_agent, _claude_agents_docs_maintainer_docs_maintainer_agent, _claude_agents_fullstack_developer_fullstack_developer_agent, _claude_agents_product_manager_product_manager_agent, _claude_agents_ux_designer_ux_designer_agent [INFERRED 0.85]
- **Shared Status Legend Badge Pattern** — frontend_templates_component_overview_template, frontend_templates_collection_details_template, frontend_templates_index_template [INFERRED 0.85]
- **Workplan Hub Integration Flow** — docs_plans_2026_01_11_workplan_hub_integration_incremental_doc, frontend_templates_bike_details_template, frontend_templates_component_details_template, frontend_templates_incident_reports_template, frontend_templates_modal_complete_workplan_template [INFERRED 0.85]
- **Workplan-Incident-Service Linking Flow** — frontend_templates_modal_workplan_record_workplanrecordmodal, frontend_templates_modal_incident_record_incidentrecordmodal, frontend_templates_modal_service_record_servicerecordmodal, frontend_templates_modal_link_incident_linkincidentsmodal, frontend_templates_modal_create_services_workplan_createservicesworkplanmodal, frontend_templates_workplan_details_workplandetailspage [INFERRED 0.85]
- **Templates Iterating payload.all_components_data** — frontend_templates_modal_incident_record_incidentrecordmodal, frontend_templates_modal_install_component_installcomponentmodal, frontend_templates_modal_quick_swap_quickswapmodal, frontend_templates_modal_workplan_record_workplanrecordmodal [INFERRED 0.90]

## Communities (85 total, 44 thin omitted)

### Community 11 - "Backend Module Entry Points"
Cohesion: 0.16
Nodes (12): Incidents, calculate_percentage_reached(), get_current_version(), parse_button_sorting(), read_config(), write_config(), Model for table: incidents, Function to get current program version (+4 more)

### Community 15 - "Strava API Integration"
Cohesion: 0.17
Nodes (8): Strava, Class to interact with Strava API, Method to prepare a list of rides, Method to prepare a list of bikes, Method to read oauth options from file, Method to save oauth options to file, Method to authenticate and get data from Stravas activities API, Method to authenticate and get data from Stravas gear API

### Community 16 - "Database Models: Bikes & Services"
Cohesion: 0.13
Nodes (15): Bikes, Meta, Services, Extends model with extra attributes, Extends model with extra attributes, Model for table: services, Extends model with extra attributes, Extends model with extra attributes (+7 more)

### Community 18 - "Error Handling Middleware"
Cohesion: 0.16
Nodes (11): Middleware, http_exception_handler(), Request, BaseHTTPMiddleware, Exception, exception_handler, StarletteHTTPException, Function to catch http errors from Uvicorn and return them to the middleware (+3 more)

### Community 19 - "Database Models: Core Tables"
Cohesion: 0.15
Nodes (13): BaseModel, Collections, ComponentHistory, ComponentTypes, Rides, Workplans, Model, Model for table: collections (+5 more)

### Community 6 - "Business Logic Core"
Cohesion: 0.11
Nodes (12): BusinessLogic, Method to determine which factor triggered a warning status, Validate threshold configuration rules for component intervals, Method to update incident record (supports full or partial updates), Method to add workplan and optionally link to source incident, Method to update workplan (supports full or partial updates), Method to create or update component types, Function to set the date for last pull from Strava (+4 more)

### Community 9 - "Database Manager Core"
Cohesion: 0.11
Nodes (10): DatabaseManager, Method to read installed components for a specific bike, Class to interact with a SQLite database through Peewee, Method to read a subset of records from the component history table, Method to retrieve the oldest record from the service log of a given component, Method to read incident records with status 'Open, Method to create or update ride data in bulk in database, Method to update component distance in database (+2 more)

### Community 0 - "DB Migration Script"
Cohesion: 0.07
Nodes (40): check_component_types_columns(), check_component_types_time_columns(), check_components_time_columns(), check_incidents_workplan_column(), check_services_workplan_column(), count_component_types_in_use(), create_collections_table(), create_incidents_table() (+32 more)

### Community 12 - "Component Status Updates"
Cohesion: 0.18
Nodes (10): calculate_elapsed_days(), get_formatted_datetime_now(), Method to update component table with service status, Method to update component lifetime and service status when no installation…, Method to compute component status using threshold logic, Method to determine worst-case status between distance and days-based…, Method to update time-based status fields for all non-retired components, Method to update component table with lifetime status (+2 more)

### Community 13 - "Creation & Validation Logic"
Cohesion: 0.15
Nodes (9): generate_unique_id(), Method to create component, Method to create installation history record, Method to orchestrate swap of one component with another, Method to validate quick swap operation, Method to create collection, Method to check if a bike has all mandatory components and respects max…, Method to add incident record (+1 more)

### Community 14 - "Record Update & Refresh Logic"
Cohesion: 0.18
Nodes (8): Method to update status for a given bike based on component service and…, Method to update component details, Method to calculate distance and bike id for history records, Method to calculate distance and bike id for service records, Method to update only the count of components for a given component type, Method to delete a given record and associated records, Method to refresh all bikes from Strava, Method to update component table with distance from ride table

### Community 17 - "Service Record Validation"
Cohesion: 0.14
Nodes (8): validate_date_format(), Method to update a component history record with validation, Method to validate history records before processing and storing in database, Method to add service record, Method to bulk create service records for multiple components linked to a…, Method to update a service record, Method to validate service records before processing and storing in database, Function to validate that a date string matches the required format YYYY-MM-DD…

### Community 2 - "Main API Routes"
Cohesion: 0.08
Nodes (36): add_collection(), add_incident_record(), add_service(), add_workplan(), bulk_add_service_records(), change_collection_status(), component_modify(), component_types_modify() (+28 more)

### Community 20 - "Collection Status Logic"
Cohesion: 0.17
Nodes (6): Method to update collection, Method to validate collections before allowing bulk operations, Method to change status of all components in a collection, Calculate status flags for a collection based on its components., Method to produce payload for displaying table of all collections, Method to produce payload for collection details page

### Community 21 - "Single-Record Reads"
Cohesion: 0.17
Nodes (6): Method to retrieve record for a specific entry in the installation log, Method to retrieve a specific service record, Method to retrieve record for a specific collection, Method to retrieve record for a specific incident report, Method to retrieve record for a specific workplan, Method to delete a given record and associated records

### Community 22 - "Form Init & Validation JS"
Cohesion: 0.20
Nodes (9): initializeDatePickers(), initializeIncidentForm(), initializeWorkplanForm(), submitCollectionAjax(), submitComponentAjax(), validateCollectionStatusChange(), validateDateInput(), validateIncidentForm() (+1 more)

### Community 23 - "APScheduler Jobs"
Cohesion: 0.28
Nodes (8): start_scheduler(), stop_scheduler(), strava_sync_job(), update_time_based_fields_job(), Initialize and start the APScheduler instance, Gracefully shutdown the APScheduler instance, Scheduled job to update time-based status fields for all non-retired components, Scheduled job to sync Strava activities

### Community 25 - "Table Sorting & Search JS"
Cohesion: 0.29
Nodes (8): initializeCollectionsSorting(), sortColumn(), initializeIncidentTable(), setupIncidentSearch(), setupIncidentStatusFiltering(), setupIncidentTableSorting(), setupWorkplanTableSorting(), updateIncidentVisibility()

### Community 27 - "Bike Data Access"
Cohesion: 0.33
Nodes (3): Method to retrieve record for a specific bike, Method to get the name of a bike based on bike id, Method to create or update bike data to the database

### Community 28 - "Component Data Access"
Cohesion: 0.33
Nodes (3): Method to get component names based on list of ids, Method to retrieve record for a specific component, Method to create or update component data to the database

### Community 29 - "Details Page Endpoints"
Cohesion: 0.33
Nodes (6): bike_details(), component_details(), get_button_order(), Endpoint for component details page, Endpoint for bike details page, Function to get button order for a specific page with defaults

### Community 3 - "Bike & Component Queries"
Cohesion: 0.11
Nodes (19): format_component_status(), format_cost(), get_formatted_bikes_list(), get_workplan_data_tuple(), Method to produce payload for page component overview, Method to produce payload for page component details, Calculate lifetime and service triggers for a component, Method to produce payload for page bike overview (+11 more)

### Community 30 - "Form Validation Helpers JS"
Cohesion: 0.33
Nodes (6): addFormValidation(), clearValidationErrors(), showFieldError(), showValidationModal(), validateComponentThresholds(), validateQuickSwapForm()

### Community 32 - "Config Page Endpoint"
Cohesion: 0.50
Nodes (4): config_overview(), get_button_sorting_config(), Endpoint for component types page, Function to get button sorting configuration for config page

### Community 33 - "Log Filtering"
Cohesion: 0.50
Nodes (4): get_filtered_log(), read_filtered_logs(), Endpoint to read log and return only business events, Function to get filtered log records

### Community 34 - "Config Update & Shutdown"
Cohesion: 0.50
Nodes (4): update_config(), shutdown_server(), Endpoint to update config file based on which form was submitted, Helper function to shutdown the server after a short delay

### Community 35 - "Bulk Action Handlers JS"
Cohesion: 0.50
Nodes (4): cleanup(), handleCancel(), handleConfirm(), performBulkStatusChange()

### Community 36 - "Markdown Preview JS"
Cohesion: 0.50
Nodes (4): containsMarkdown(), renderPreview(), setInitialMode(), updateCheckboxInText()

### Community 37 - "Workplan Table Filtering JS"
Cohesion: 0.67
Nodes (4): initializeWorkplanTable(), setupWorkplanSearch(), setupWorkplanStatusFiltering(), updateWorkplansVisibility()

### Community 4 - "Frontend JS Core"
Cohesion: 0.08
Nodes (9): editCollection(), fetchLogs(), handleUpdate(), initializeComponentSelector(), performQuickSwap(), showToast(), updateFormFields(), NOTE: All collection details page handlers are in the "Functions used on… (+1 more)

### Community 40 - "Quick Swap Helpers JS"
Cohesion: 0.67
Nodes (3): filterNewComponentsByType(), handleOldComponentChange(), updateQuickSwapCollectionWarning()

### Community 5 - "Page Endpoint Handlers"
Cohesion: 0.11
Nodes (24): add_history_record(), collection_details(), component_overview(), component_types_overview(), help_page(), incident_reports(), refresh_all_bikes(), refresh_rides() (+16 more)

### Community 8 - "Workplan Business Logic"
Cohesion: 0.13
Nodes (17): generate_incident_title(), generate_workplan_title(), get_incident_data_tuple(), get_workplan_names_dict(), parse_checkbox_progress(), parse_json_string(), strip_markdown_syntax(), Method to produce payload for workplan details page (+9 more)

### Community 1 - "Workplan Hub & Templates"
Cohesion: 0.09
Nodes (39): Base Template, btn_new_incident Macro (Bike Details), btn_new_workplan Macro (Bike Details), Bike Details Template, Collection Details Template, btn_new_incident Macro (Component Details), btn_new_workplan Macro (Component Details), btn_quick_swap Macro (+31 more)

### Community 10 - "Graphify Skill Docs"
Cohesion: 0.12
Nodes (18): graphify Skill Trigger, Hyperedges Rule, Semantic Similarity Edge Rule, graphify Native CLAUDE.md Integration, graphify Post-Commit Hook, Work Memory / Reflect Feedback Loop, Whisper Transcription Pipeline, graphify Integration Rules (+10 more)

### Community 24 - "Python Dependencies"
Cohesion: 0.22
Nodes (9): v0.4.8 Release Notes, APScheduler, FastAPI, Jinja2, Peewee ORM, python-multipart, requests-oauthlib, Uvicorn (+1 more)

### Community 26 - "Workplan-Related Modals"
Cohesion: 0.48
Nodes (7): Create Services For Workplan Modal, Incident Record Modal, Link Incident To Workplan Modal, Service Record Modal, Workplan Record Modal, Workplan Details Page, Workplans List Page

### Community 38 - "Component Modals"
Cohesion: 0.67
Nodes (4): Component Type Modal, Create Component Modal, Quick Swap Modal, Update Component Details Modal

### Community 41 - "Status Update Modals"
Cohesion: 0.67
Nodes (3): Install Component Modal, Update Collection Status Modal, Update Component Status Modal

### Community 7 - "Agent Team & Workflow"
Cohesion: 0.22
Nodes (20): Change Management Rules, Code Style & Standards, Communication & Output Rules, Debugging & Bug Fixing Rules, Git Workflow Rules, Agent Communication via Handovers, Standard Development Workflow, Sub-Agent Team (+12 more)

## Ambiguous Edges - Review These
- `Git Workflow Rules` → `Version Script CI Workflow`  [AMBIGUOUS]
  .github/workflows/run_version_script.yml · relation: conceptually_related_to

## Knowledge Gaps
- **41 isolated node(s):** `backup_db.sh script`, `create-container-vs2000.sh script`, `btn_quick_swap Macro`, `Complete Workplan Modal Template`, `Database Migration Script Reference` (+36 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **44 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `Git Workflow Rules` and `Version Script CI Workflow`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **Why does `DatabaseManager` connect `Database Manager Core` to `Bike & Component Queries`, `Backend Module Entry Points`, `Database Models: Bikes & Services`, `Database Models: Core Tables`, `Single-Record Reads`, `Bike Data Access`, `Component Data Access`, `Component Type Data Access`, `Component Type Usage Count`, `Read All Collections`, `Read All Component Types`, `Read All Components`, `Read All Incidents`, `Read All Workplans`, `Bike From History`, `Read Bikes Table`, `Collection By Component`, `Incidents By Workplan`, `Latest History Record`, `Latest Ride Record`, `Latest Service Record`, `Matching Rides Query`, `Oldest History Record`, `Planned Workplans Query`, `Recent Rides Query`, `Services By Workplan`, `Components By Bike`, `Service History Subset`, `Service Record Subset`, `Ride Distance Sum`, `Unique Bike IDs`, `Bike Service Status Write`, `Collection Write`, `Component Lifetime Status Write`, `History Record Write`, `Incident Record Write`, `Service Record Write`, `Workplan Write`, `Components Table Model`?**
  _High betweenness centrality (0.224) - this node is a cross-community bridge._
- **Why does `BusinessLogic` connect `Business Logic Core` to `Bike & Component Queries`, `Workplan Business Logic`, `Backend Module Entry Points`, `Component Status Updates`, `Creation & Validation Logic`, `Record Update & Refresh Logic`, `Service Record Validation`, `Collection Status Logic`, `APScheduler Jobs`?**
  _High betweenness centrality (0.174) - this node is a cross-community bridge._
- **Why does `bulk_add_service_records()` connect `Main API Routes` to `Frontend JS Core`?**
  _High betweenness centrality (0.061) - this node is a cross-community bridge._
- **Are the 9 inferred relationships involving `DatabaseManager` (e.g. with `ComponentTypes` and `Components`) actually correct?**
  _`DatabaseManager` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `BusinessLogic` (e.g. with `strava_sync_job()` and `update_time_based_fields_job()`) actually correct?**
  _`BusinessLogic` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `backup_db.sh script`, `create-container-vs2000.sh script`, `btn_quick_swap Macro` to the rest of the system?**
  _41 weakly-connected nodes found - possible documentation gaps or missing edges._