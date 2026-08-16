# Graph Report - velo-supervisor-2000  (2026-08-16)

## Corpus Check
- 80 files · ~139,891 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 682 nodes · 1021 edges · 94 communities (51 shown, 43 thin omitted)
- Extraction: 89% EXTRACTED · 11% INFERRED · 0% AMBIGUOUS · INFERRED: 113 edges (avg confidence: 0.77)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Strava API Integration
- Database Models & Backend Utils
- Error Handling Middleware
- Business Logic Core
- Database Manager Core
- DB Migration Script
- Component Status Updates
- Creation & Validation Logic
- Record Update & Refresh Logic
- Service Record Validation
- Database Models: Core Tables
- Main API Routes
- Collection Status Logic
- Single-Record Reads
- Form Init & Validation JS
- APScheduler Jobs
- Workplan Table Sorting JS
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
- Component Type Validation Logic
- Incident Table Search JS
- Add Component via AJAX
- Quick Swap via AJAX
- Graphify Skill Docs
- Agent Team & Workflow
- Git & Handover Rules
- Handovers Directory Guide
- CLAUDE.md Meta & Conventions
- Agent Handover Process
- Project Architecture Docs
- DB Backup Script
- Docker Deploy Script
- Dev Commands & Setup
- Code Style Guidelines
- Deployment & Logging Notes
- Feature & Bugfix Workflows
- Sub-Agent Roster
- Handover Testing Checklist
- Workplan Hub & Templates
- Python Dependencies
- Workplan-Related Modals
- Component Modals
- Status Update Modals
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
4. `migrate_database()` - 14 edges
5. `BaseModel` - 13 edges
6. `get_workplan_data_tuple()` - 13 edges
7. `Base Template` - 13 edges
8. `graphify Skill` - 11 edges
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
- **Semantic Extraction Subagent Pipeline** — _claude_skills_graphify_skill_graphify_skill, _claude_skills_graphify_references_extraction_spec_extraction_prompt_spec, _claude_skills_graphify_references_extraction_spec_node_id_format, _claude_skills_graphify_references_extraction_spec_confidence_rubric [EXTRACTED 1.00]
- **Standard Feature Development Workflow** — claude_standard_development_workflow, _claude_agents_product_manager_product_manager_agent, _claude_agents_ux_designer_ux_designer_agent, _claude_agents_architect_architect_agent, _claude_agents_database_expert_database_expert_agent, _claude_agents_fullstack_developer_fullstack_developer_agent, _claude_agents_code_reviewer_code_reviewer_agent, _claude_agents_docs_maintainer_docs_maintainer_agent [EXTRACTED 1.00]
- **Generic JS-Driven Utility Modals** — frontend_templates_modal_confirm_confirmmodal, frontend_templates_modal_validation_validationmodal, frontend_templates_modal_report_reportmodal, frontend_templates_modal_docs_docsmodal, frontend_templates_modal_loading_loadingmodal [INFERRED 0.85]
- **Handover Documentation Pattern** — _handovers_template_handover_template, _claude_agents_architect_architect_agent, _claude_agents_code_reviewer_code_reviewer_agent, _claude_agents_database_expert_database_expert_agent, _claude_agents_docs_maintainer_docs_maintainer_agent, _claude_agents_fullstack_developer_fullstack_developer_agent, _claude_agents_product_manager_product_manager_agent, _claude_agents_ux_designer_ux_designer_agent [INFERRED 0.85]
- **Shared Status Legend Badge Pattern** — frontend_templates_component_overview_template, frontend_templates_collection_details_template, frontend_templates_index_template [INFERRED 0.85]
- **Workplan Hub Integration Flow** — docs_plans_2026_01_11_workplan_hub_integration_incremental_doc, frontend_templates_bike_details_template, frontend_templates_component_details_template, frontend_templates_incident_reports_template, frontend_templates_modal_complete_workplan_template [INFERRED 0.85]
- **Workplan-Incident-Service Linking Flow** — frontend_templates_modal_workplan_record_workplanrecordmodal, frontend_templates_modal_incident_record_incidentrecordmodal, frontend_templates_modal_service_record_servicerecordmodal, frontend_templates_modal_link_incident_linkincidentsmodal, frontend_templates_modal_create_services_workplan_createservicesworkplanmodal, frontend_templates_workplan_details_workplandetailspage [INFERRED 0.85]
- **Templates Iterating payload.all_components_data** — frontend_templates_modal_incident_record_incidentrecordmodal, frontend_templates_modal_install_component_installcomponentmodal, frontend_templates_modal_quick_swap_quickswapmodal, frontend_templates_modal_workplan_record_workplanrecordmodal [INFERRED 0.90]

## Communities (94 total, 43 thin omitted)

### Community 15 - "Strava API Integration"
Cohesion: 0.17
Nodes (8): Strava, Class to interact with Strava API, Method to prepare a list of rides, Method to prepare a list of bikes, Method to read oauth options from file, Method to save oauth options to file, Method to authenticate and get data from Stravas activities API, Method to authenticate and get data from Stravas gear API

### Community 16 - "Database Models & Backend Utils"
Cohesion: 0.07
Nodes (40): BaseModel, Bikes, Collections, ComponentHistory, Components, ComponentTypes, Incidents, Meta (+32 more)

### Community 18 - "Error Handling Middleware"
Cohesion: 0.16
Nodes (11): Middleware, http_exception_handler(), Request, BaseHTTPMiddleware, Exception, exception_handler, StarletteHTTPException, Function to catch http errors from Uvicorn and return them to the middleware (+3 more)

### Community 6 - "Business Logic Core"
Cohesion: 0.13
Nodes (10): BusinessLogic, Method to update incident record (supports full or partial updates), Method to add workplan and optionally link to source incident, Method to update workplan (supports full or partial updates), Method to refresh all bikes from Strava, Function to set the date for last pull from Strava, Class that contains business logic, Method to produce payload for page component types (+2 more)

### Community 9 - "Database Manager Core"
Cohesion: 0.11
Nodes (10): DatabaseManager, Method to read installed components for a specific bike, Class to interact with a SQLite database through Peewee, Method to read a subset of records from the component history table, Method to retrieve the oldest record from the service log of a given component, Method to read incident records with status 'Open, Method to create or update ride data in bulk in database, Method to update component distance in database (+2 more)

### Community 0 - "DB Migration Script"
Cohesion: 0.07
Nodes (40): check_component_types_columns(), check_component_types_time_columns(), check_components_time_columns(), check_incidents_workplan_column(), check_services_workplan_column(), count_component_types_in_use(), create_collections_table(), create_incidents_table() (+32 more)

### Community 12 - "Component Status Updates"
Cohesion: 0.29
Nodes (4): Method to update component lifetime and service status when no installation…, Method to compute component status using threshold logic, Method to determine worst-case status between distance and days-based…, Method to update component table with lifetime status

### Community 13 - "Creation & Validation Logic"
Cohesion: 0.18
Nodes (8): generate_unique_id(), Method to create component, Method to create installation history record, Method to orchestrate swap of one component with another, Method to validate quick swap operation, Method to check if a bike has all mandatory components and respects max…, Method to add incident record, Function to generates a random and unique ID

### Community 14 - "Record Update & Refresh Logic"
Cohesion: 0.18
Nodes (9): Method to update component table with service status, Method to update status for a given bike based on component service and…, Method to update component details, Method to calculate distance and bike id for history records, Method to calculate distance and bike id for service records, Method to update time-based status fields for all non-retired components, Method to update only the count of components for a given component type, Method to delete a given record and associated records (+1 more)

### Community 17 - "Service Record Validation"
Cohesion: 0.25
Nodes (4): Method to add service record, Method to bulk create service records for multiple components linked to a…, Method to update a service record, Method to validate service records before processing and storing in database

### Community 19 - "Database Models: Core Tables"
Cohesion: 0.33
Nodes (4): validate_date_format(), Method to update a component history record with validation, Method to validate history records before processing and storing in database, Function to validate that a date string matches the required format YYYY-MM-DD…

### Community 2 - "Main API Routes"
Cohesion: 0.09
Nodes (32): add_collection(), add_incident_record(), add_service(), add_workplan(), bulk_add_service_records(), component_modify(), component_types_modify(), create_component() (+24 more)

### Community 20 - "Collection Status Logic"
Cohesion: 0.17
Nodes (6): Method to create collection, Method to update collection, Method to validate collections before allowing bulk operations, Method to change status of all components in a collection, Calculate status flags for a collection based on its components., Method to produce payload for collection details page

### Community 21 - "Single-Record Reads"
Cohesion: 0.17
Nodes (6): Method to retrieve record for a specific entry in the installation log, Method to retrieve a specific service record, Method to retrieve record for a specific collection, Method to retrieve record for a specific incident report, Method to retrieve record for a specific workplan, Method to delete a given record and associated records

### Community 22 - "Form Init & Validation JS"
Cohesion: 0.25
Nodes (7): initializeDatePickers(), initializeIncidentForm(), initializeWorkplanForm(), validateCollectionStatusChange(), validateDateInput(), validateIncidentForm(), validateWorkplanForm()

### Community 23 - "APScheduler Jobs"
Cohesion: 0.28
Nodes (8): start_scheduler(), stop_scheduler(), strava_sync_job(), update_time_based_fields_job(), Initialize and start the APScheduler instance, Gracefully shutdown the APScheduler instance, Scheduled job to update time-based status fields for all non-retired components, Scheduled job to sync Strava activities

### Community 25 - "Workplan Table Sorting JS"
Cohesion: 0.29
Nodes (8): initializeCollectionsSorting(), sortColumn(), initializeWorkplanTable(), setupIncidentTableSorting(), setupWorkplanSearch(), setupWorkplanStatusFiltering(), setupWorkplanTableSorting(), updateWorkplansVisibility()

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
Cohesion: 0.06
Nodes (44): calculate_elapsed_days(), calculate_percentage_reached(), format_component_status(), format_cost(), generate_incident_title(), generate_workplan_title(), get_formatted_bikes_list(), get_formatted_datetime_now() (+36 more)

### Community 30 - "Form Validation Helpers JS"
Cohesion: 0.33
Nodes (6): addFormValidation(), clearValidationErrors(), showFieldError(), showValidationModal(), validateComponentThresholds(), validateQuickSwapForm()

### Community 32 - "Config Page Endpoint"
Cohesion: 0.50
Nodes (4): config_overview(), get_button_sorting_config(), Endpoint for component types page, Function to get button sorting configuration for config page

### Community 33 - "Log Filtering"
Cohesion: 0.40
Nodes (5): get_filtered_log(), read_filtered_logs(), fetchLogs(), Endpoint to read log and return only business events, Function to get filtered log records

### Community 34 - "Config Update & Shutdown"
Cohesion: 0.50
Nodes (4): update_config(), shutdown_server(), Endpoint to update config file based on which form was submitted, Helper function to shutdown the server after a short delay

### Community 35 - "Bulk Action Handlers JS"
Cohesion: 0.29
Nodes (7): change_collection_status(), cleanup(), handleCancel(), handleConfirm(), performBulkStatusChange(), submitCollectionAjax(), Endpoint to change the status of all components in a collection

### Community 36 - "Markdown Preview JS"
Cohesion: 0.50
Nodes (4): containsMarkdown(), renderPreview(), setInitialMode(), updateCheckboxInText()

### Community 37 - "Workplan Table Filtering JS"
Cohesion: 0.33
Nodes (6): refresh_all_bikes(), refresh_rides(), handleUpdate(), showToast(), Endpoint to manually refresh data for all bikes, Endpoint to refresh data for a subset or all rides

### Community 4 - "Frontend JS Core"
Cohesion: 0.09
Nodes (8): editCollection(), filterNewComponentsByType(), handleOldComponentChange(), initializeComponentSelector(), updateFormFields(), updateQuickSwapCollectionWarning(), NOTE: All collection details page handlers are in the "Functions used on…, IMPORTANT: Remove readonly - allow manual typing

### Community 5 - "Page Endpoint Handlers"
Cohesion: 0.16
Nodes (18): collection_details(), component_overview(), component_types_overview(), help_page(), incident_reports(), root(), workplan_details(), workplans() (+10 more)

### Community 88 - "Incident Table Search JS"
Cohesion: 0.67
Nodes (4): initializeIncidentTable(), setupIncidentSearch(), setupIncidentStatusFiltering(), updateIncidentVisibility()

### Community 89 - "Add Component via AJAX"
Cohesion: 0.67
Nodes (3): add_history_record(), submitComponentAjax(), Endpoint with conditional routing for redirects and AJAX to add an existing…

### Community 90 - "Quick Swap via AJAX"
Cohesion: 0.67
Nodes (3): quick_swap(), performQuickSwap(), Endpoint to swap one component with another

### Community 10 - "Graphify Skill Docs"
Cohesion: 0.12
Nodes (17): graphify Skill Trigger, Hyperedges Rule, Semantic Similarity Edge Rule, graphify Native CLAUDE.md Integration, graphify Post-Commit Hook, Work Memory / Reflect Feedback Loop, Whisper Transcription Pipeline, graphify add & --watch Reference (+9 more)

### Community 7 - "Agent Team & Workflow"
Cohesion: 0.38
Nodes (7): Architect Agent, Code Reviewer Agent, Database Expert Agent, Docs Maintainer Agent, Fullstack Developer Agent, Product Manager Agent, UX Designer Agent

### Community 8 - "Git & Handover Rules"
Cohesion: 0.25
Nodes (8): Version Script CI Workflow, Branch Strategy, Commit Process, For All Agents, For code-reviewer, For docs-maintainer, For fullstack-developer, Git Workflow Rules

### Community 11 - "CLAUDE.md Meta & Conventions"
Cohesion: 0.25
Nodes (6): Change Management Rules, Communication & Output Rules, Debugging & Bug Fixing Rules, graphify, Important Notes, Project Overview

### Community 40 - "Agent Handover Process"
Cohesion: 0.33
Nodes (6): Agent Communication via Handovers, Creating Handovers, Detailed Instructions, Handover Structure, Naming Convention, Reading Handovers

### Community 72 - "Project Architecture Docs"
Cohesion: 0.40
Nodes (5): Architecture Overview, Configuration, Core Components, Key Features, Project Structure

### Community 77 - "Dev Commands & Setup"
Cohesion: 0.40
Nodes (5): Database Operations, Dependencies, Development Commands, Running the Application, Testing

### Community 85 - "Code Style Guidelines"
Cohesion: 0.50
Nodes (4): Code Style & Standards, Database, Frontend, Python (Backend)

### Community 86 - "Deployment & Logging Notes"
Cohesion: 0.50
Nodes (4): Database Schema Changes, Development Notes, Docker Development, Logging

### Community 87 - "Feature & Bugfix Workflows"
Cohesion: 0.50
Nodes (4): For Bug Fixes, For Documentation Updates, For New Features, Standard Development Workflow

### Community 91 - "Sub-Agent Roster"
Cohesion: 0.67
Nodes (3): Available Agents, Direct Invocation, Sub-Agent Team

### Community 92 - "Handover Testing Checklist"
Cohesion: 0.67
Nodes (3): Before Creating Handover, For fullstack-developer, Testing Requirements

### Community 1 - "Workplan Hub & Templates"
Cohesion: 0.08
Nodes (41): Base Template, btn_new_incident Macro (Bike Details), btn_new_workplan Macro (Bike Details), Bike Details Template, Collection Details Template, btn_new_incident Macro (Component Details), btn_new_workplan Macro (Component Details), btn_quick_swap Macro (+33 more)

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

## Ambiguous Edges - Review These
- `Version Script CI Workflow` → `Git Workflow Rules`  [AMBIGUOUS]
  .github/workflows/run_version_script.yml · relation: conceptually_related_to

## Knowledge Gaps
- **78 isolated node(s):** `graphify Skill Trigger`, `Hyperedges Rule`, `Semantic Similarity Edge Rule`, `Work Memory / Reflect Feedback Loop`, `Whisper Transcription Pipeline` (+73 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **43 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `Version Script CI Workflow` and `Git Workflow Rules`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **Why does `DatabaseManager` connect `Database Manager Core` to `Bike & Component Queries`, `Database Models & Backend Utils`, `Single-Record Reads`, `Bike Data Access`, `Component Data Access`, `Component Type Data Access`, `Component Type Usage Count`, `Read All Collections`, `Read All Component Types`, `Read All Components`, `Read All Incidents`, `Read All Workplans`, `Bike From History`, `Read Bikes Table`, `Collection By Component`, `Incidents By Workplan`, `Latest History Record`, `Latest Ride Record`, `Latest Service Record`, `Matching Rides Query`, `Oldest History Record`, `Planned Workplans Query`, `Recent Rides Query`, `Services By Workplan`, `Components By Bike`, `Service History Subset`, `Service Record Subset`, `Ride Distance Sum`, `Unique Bike IDs`, `Bike Service Status Write`, `Collection Write`, `Component Lifetime Status Write`, `History Record Write`, `Incident Record Write`, `Service Record Write`, `Workplan Write`?**
  _High betweenness centrality (0.200) - this node is a cross-community bridge._
- **Why does `BusinessLogic` connect `Business Logic Core` to `Bike & Component Queries`, `Component Status Updates`, `Creation & Validation Logic`, `Record Update & Refresh Logic`, `Component Type Validation Logic`, `Database Models & Backend Utils`, `Service Record Validation`, `Database Models: Core Tables`, `Collection Status Logic`, `APScheduler Jobs`?**
  _High betweenness centrality (0.155) - this node is a cross-community bridge._
- **Why does `bulk_add_service_records()` connect `Main API Routes` to `Frontend JS Core`?**
  _High betweenness centrality (0.054) - this node is a cross-community bridge._
- **Are the 9 inferred relationships involving `DatabaseManager` (e.g. with `Bikes` and `Collections`) actually correct?**
  _`DatabaseManager` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `BusinessLogic` (e.g. with `update_time_based_fields_job()` and `strava_sync_job()`) actually correct?**
  _`BusinessLogic` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `graphify Skill Trigger`, `Hyperedges Rule`, `Semantic Similarity Edge Rule` to the rest of the system?**
  _78 weakly-connected nodes found - possible documentation gaps or missing edges._