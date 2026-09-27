# Graph Report - velo-supervisor-2000  (2026-09-27)

## Corpus Check
- 30 files · ~129,405 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 12 file(s) not represented in the graph (top: (none) 5, .example 1, .sqlite 1)

## Summary
- 780 nodes · 1117 edges · 115 communities (58 shown, 57 thin omitted)
- Extraction: 89% EXTRACTED · 11% INFERRED · 0% AMBIGUOUS · INFERRED: 122 edges (avg confidence: 0.86)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `f45e8b7c`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- utils.py
- db_migration.py
- Bike Details Template
- .get_component_overview
- Meta
- scheduler.py
- .process_history_records
- main.js
- get
- CLAUDE.md
- BusinessLogic
- post
- DatabaseManager
- Database Migration Script (db_migration.py)
- .create_service_record
- .create_component
- Middleware
- main.py
- .calculate_collection_status
- .write_delete_record
- validateDateInput
- sortColumn
- Python Requirements List
- .read_bike_name
- .read_component
- bike_details
- validateComponentThresholds
- .read_single_component_type
- version.py
- CLAUDE.md
- cleanup
- renderPreview
- initializeIncidentTable
- helpTopics Data Object
- handleOldComponentChange
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
- Git Workflow Rules
- .modify_component_details
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
- .calculate_component_triggers
- Agent Communication via Handovers
- fullstack-developer.md
- product-manager.md
- Handovers Directory
- architect.md
- Architecture Overview
- Development Commands
- config_overview
- get_filtered_log
- update_config
- docs-maintainer.md
- Code Style & Standards
- Development Notes
- Standard Development Workflow
- Sub-Agent Team
- Testing Requirements
- initializeComponentSelector
- update_workplan

## God Nodes (most connected - your core abstractions)
1. `DatabaseManager` - 65 edges
2. `BusinessLogic` - 61 edges
3. `Meta` - 20 edges
4. `migrate_database()` - 14 edges
5. `BaseModel` - 13 edges
6. `get_workplan_data_tuple()` - 13 edges
7. `Bike Details Template` - 13 edges
8. `Component Details Template` - 13 edges
9. `Base Template` - 12 edges
10. `Strava` - 10 edges

## Surprising Connections (you probably didn't know these)
- `Version Script CI Workflow` --conceptually_related_to--> `Git Workflow Rules`  [AMBIGUOUS]
  .github/workflows/run_version_script.yml → CLAUDE.md
- `Opt-in Workplan Hub Pattern` --conceptually_related_to--> `Complete Workplan Modal Template`  [INFERRED]
  docs/plans/2026-01-11-workplan-hub-integration-incremental.md → frontend/templates/modal_complete_workplan.html
- `Collections (Core Concept)` --conceptually_related_to--> `v0.4.5 Release`  [INFERRED]
  frontend/templates/help.html → README.md
- `Hybrid Time + Distance Tracking` --conceptually_related_to--> `v0.4.7 Release`  [INFERRED]
  frontend/templates/help.html → README.md
- `Understanding Thresholds` --conceptually_related_to--> `v0.4.7 Release`  [INFERRED]
  frontend/templates/help.html → README.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Breaking Database Schema Change Releases** — readme_v0_4_2, readme_v0_4_3, readme_v0_4_5, readme_v0_4_7, readme_v0_4_9, readme_db_migration_script [EXTRACTED 0.90]
- **CSS Inline-Style-to-Class Refactoring Files** — docs_plans_2026_01_11_workplan_hub_integration_incremental_css_refactor_concept, frontend_templates_collection_details_template, frontend_templates_index_template, frontend_templates_component_overview_template, frontend_templates_component_details_template, frontend_templates_bike_details_template, frontend_templates_config_template, frontend_templates_error_template [EXTRACTED 1.00]
- **Feature Introduction Documented in Help Page** — readme_v0_4_5, readme_v0_4_6, readme_v0_4_7, frontend_templates_help_core_concepts_collections, frontend_templates_help_common_tasks_quick_swap, frontend_templates_help_core_concepts_hybrid_tracking [INFERRED 0.85]
- **Generic JS-Driven Utility Modals** — frontend_templates_modal_confirm_confirmmodal, frontend_templates_modal_validation_validationmodal, frontend_templates_modal_report_reportmodal, frontend_templates_modal_docs_docsmodal, frontend_templates_modal_loading_loadingmodal [INFERRED 0.85]
- **Help Topic Display and Search Flow** — frontend_templates_help_helptopics, frontend_templates_help_showhelptopic, frontend_templates_help_search_functionality [INFERRED 0.85]
- **Shared Status Legend Badge Pattern** — frontend_templates_component_overview_template, frontend_templates_collection_details_template, frontend_templates_index_template [INFERRED 0.85]
- **Workplan Hub Integration Flow** — docs_plans_2026_01_11_workplan_hub_integration_incremental_doc, frontend_templates_bike_details_template, frontend_templates_component_details_template, frontend_templates_incident_reports_template, frontend_templates_modal_complete_workplan_template [INFERRED 0.85]
- **Workplan-Incident-Service Linking Flow** — frontend_templates_modal_workplan_record_workplanrecordmodal, frontend_templates_modal_incident_record_incidentrecordmodal, frontend_templates_modal_service_record_servicerecordmodal, frontend_templates_modal_link_incident_linkincidentsmodal, frontend_templates_modal_create_services_workplan_createservicesworkplanmodal, frontend_templates_workplan_details_workplandetailspage [INFERRED 0.85]
- **Templates Iterating payload.all_components_data** — frontend_templates_modal_incident_record_incidentrecordmodal, frontend_templates_modal_install_component_installcomponentmodal, frontend_templates_modal_quick_swap_quickswapmodal, frontend_templates_modal_workplan_record_workplanrecordmodal [INFERRED 0.90]

## Communities (115 total, 57 thin omitted)

### Community 0 - "utils.py"
Cohesion: 0.06
Nodes (50): asyncio, Method to produce payload for page component details, Method to create component-to-collection mapping dictionaries, Method to produce payload for page incident reports, Method to produce payload for page of all workplans, Method to produce payload for workplan details page, Method to check if all affected components have linked services, Method to get incidents that can be linked to a workplan (+42 more)

### Community 1 - "db_migration.py"
Cohesion: 0.06
Nodes (44): check_component_types_columns(), check_component_types_time_columns(), check_components_time_columns(), check_incidents_workplan_column(), check_services_workplan_column(), count_component_types_in_use(), create_collections_table(), create_incidents_table() (+36 more)

### Community 2 - "Bike Details Template"
Cohesion: 0.10
Nodes (42): CSS Inline-Style-to-Class Refactoring, Workplan Hub Integration Plan, Opt-in Workplan Hub Pattern, Base Template, btn_new_incident Macro (Bike Details), btn_new_workplan Macro (Bike Details), Bike Details Template, Collection Details Template (+34 more)

### Community 3 - ".get_component_overview"
Cohesion: 0.18
Nodes (6): Method to produce payload for page component overview, Method to produce payload for page bike overview, Method to produce payload for displaying table of all collections, Method to produce payload for collection details page, Method to build dictionaries of bike and component ids referenced in received…, Method to build dictionaries of bike and component ids referenced in received…

### Community 4 - "Meta"
Cohesion: 0.08
Nodes (35): Module for interaction with a Sqlite database, BaseModel, Bikes, Collections, ComponentHistory, Components, ComponentTypes, Incidents (+27 more)

### Community 5 - "scheduler.py"
Cohesion: 0.07
Nodes (27): apscheduler_schedulers_asyncio, apscheduler_triggers_cron, apscheduler_triggers_interval, Module to handle business logic, Initialize and start the APScheduler instance, Scheduler for automated maintenance tasks, Gracefully shutdown the APScheduler instance, Scheduled job to update time-based status fields for all non-retired components (+19 more)

### Community 6 - ".process_history_records"
Cohesion: 0.16
Nodes (10): Method to update component table with service status, Method to update component lifetime and service status when no installation…, Method to update status for a given bike based on component service and…, Method to calculate distance and bike id for history records, Method to calculate distance and bike id for service records, Method to determine worst-case status between distance and days-based…, Method to update time-based status fields for all non-retired components, Method to delete a given record and associated records (+2 more)

### Community 7 - "main.js"
Cohesion: 0.08
Nodes (6): handleUpdate(), initializeCollectionsSearch(), updateRowVisibility(), NOTE: All collection details page handlers are in the "Functions used on…, IMPORTANT: Remove readonly - allow manual typing, showToast()

### Community 8 - "get"
Cohesion: 0.11
Nodes (24): add_history_record(), collection_details(), component_overview(), component_types_overview(), help_page(), incident_reports(), Request, Endpoint for incident reports page (+16 more)

### Community 9 - "CLAUDE.md"
Cohesion: 0.25
Nodes (6): Change Management Rules, Communication & Output Rules, Debugging & Bug Fixing Rules, graphify, Important Notes, Project Overview

### Community 10 - "BusinessLogic"
Cohesion: 0.13
Nodes (10): BusinessLogic, Method to update incident record (supports full or partial updates), Method to add workplan and optionally link to source incident, Method to update workplan (supports full or partial updates), Method to refresh all bikes from Strava, Function to set the date for last pull from Strava, Class that contains business logic, Method to produce payload for page component types (+2 more)

### Community 11 - "post"
Cohesion: 0.07
Nodes (27): add_collection(), add_incident_record(), add_service(), add_workplan(), bulk_add_service_records(), change_collection_status(), component_modify(), create_component() (+19 more)

### Community 12 - "DatabaseManager"
Cohesion: 0.11
Nodes (10): DatabaseManager, Method to read installed components for a specific bike, Class to interact with a SQLite database through Peewee, Method to read a subset of records from the component history table, Method to retrieve the oldest record from the service log of a given component, Method to read incident records with status 'Open, Method to create or update ride data in bulk in database, Method to update component distance in database (+2 more)

### Community 13 - "Database Migration Script (db_migration.py)"
Cohesion: 0.13
Nodes (16): Collections (Core Concept), Component Types vs Components, Hybrid Time + Distance Tracking, Mileage Tracking, Understanding Thresholds, Getting Started: Define Component Types, Incidents Page, Workplans Page (+8 more)

### Community 14 - ".create_service_record"
Cohesion: 0.14
Nodes (8): Method to update a component history record with validation, Method to validate history records before processing and storing in database, Method to add service record, Method to bulk create service records for multiple components linked to a…, Method to update a service record, Method to validate service records before processing and storing in database, Function to validate that a date string matches the required format YYYY-MM-DD…, validate_date_format()

### Community 15 - ".create_component"
Cohesion: 0.18
Nodes (8): Method to create component, Method to create installation history record, Method to orchestrate swap of one component with another, Method to validate quick swap operation, Method to check if a bike has all mandatory components and respects max…, Method to add incident record, generate_unique_id(), Function to generates a random and unique ID

### Community 16 - "Middleware"
Cohesion: 0.16
Nodes (11): http_exception_handler(), Function to catch http errors from Uvicorn and return them to the middleware, Middleware, Request, Class to handle exceptions that breaks the program and should be shown to the…, Method to dispatch intercepted requests, Method to catch and handle exceptions, BaseHTTPMiddleware (+3 more)

### Community 17 - "main.py"
Cohesion: 0.12
Nodes (17): component_types_modify(), lifespan(), Route handlers for Velo Supervisor 2000, Manage application startup and shutdown, Endpoint to update an incident record (supports full or partial updates), Endpoint to modify component types, update_incident_record(), Module for middleware (+9 more)

### Community 18 - ".calculate_collection_status"
Cohesion: 0.20
Nodes (5): Method to create collection, Method to update collection, Method to validate collections before allowing bulk operations, Method to change status of all components in a collection, Calculate status flags for a collection based on its components.

### Community 19 - ".write_delete_record"
Cohesion: 0.17
Nodes (6): Method to retrieve record for a specific entry in the installation log, Method to retrieve a specific service record, Method to retrieve record for a specific collection, Method to retrieve record for a specific incident report, Method to retrieve record for a specific workplan, Method to delete a given record and associated records

### Community 20 - "validateDateInput"
Cohesion: 0.20
Nodes (9): initializeDatePickers(), initializeIncidentForm(), initializeWorkplanForm(), submitCollectionAjax(), submitComponentAjax(), validateCollectionStatusChange(), validateDateInput(), validateIncidentForm() (+1 more)

### Community 21 - "sortColumn"
Cohesion: 0.29
Nodes (8): initializeCollectionsSorting(), sortColumn(), initializeWorkplanTable(), setupIncidentTableSorting(), setupWorkplanSearch(), setupWorkplanStatusFiltering(), setupWorkplanTableSorting(), updateWorkplansVisibility()

### Community 22 - "Python Requirements List"
Cohesion: 0.25
Nodes (8): APScheduler, Python Requirements List, FastAPI, Jinja2, Peewee ORM, python-multipart, requests-oauthlib, Uvicorn

### Community 23 - ".read_bike_name"
Cohesion: 0.33
Nodes (3): Method to retrieve record for a specific bike, Method to get the name of a bike based on bike id, Method to create or update bike data to the database

### Community 24 - ".read_component"
Cohesion: 0.33
Nodes (3): Method to get component names based on list of ids, Method to retrieve record for a specific component, Method to create or update component data to the database

### Community 25 - "bike_details"
Cohesion: 0.33
Nodes (6): bike_details(), component_details(), Endpoint for component details page, Endpoint for bike details page, get_button_order(), Function to get button order for a specific page with defaults

### Community 26 - "validateComponentThresholds"
Cohesion: 0.33
Nodes (6): addFormValidation(), clearValidationErrors(), showFieldError(), showValidationModal(), validateComponentThresholds(), validateQuickSwapForm()

### Community 28 - "version.py"
Cohesion: 0.40
Nodes (4): get_git_info(), Script to maintain version number, Function to get latest version number and commit hash, subprocess

### Community 29 - "CLAUDE.md"
Cohesion: 0.50
Nodes (4): CLAUDE.md, Data Management Tips, Need More Help? (Troubleshooting), Handover Documents Directory (.handovers/)

### Community 30 - "cleanup"
Cohesion: 0.50
Nodes (4): cleanup(), handleCancel(), handleConfirm(), performBulkStatusChange()

### Community 31 - "renderPreview"
Cohesion: 0.50
Nodes (4): containsMarkdown(), renderPreview(), setInitialMode(), updateCheckboxInText()

### Community 32 - "initializeIncidentTable"
Cohesion: 0.67
Nodes (4): initializeIncidentTable(), setupIncidentSearch(), setupIncidentStatusFiltering(), updateIncidentVisibility()

### Community 33 - "helpTopics Data Object"
Cohesion: 0.50
Nodes (4): helpTopics Data Object, Help Page Template, Help Search Functionality, showHelpTopic() Function

### Community 34 - "handleOldComponentChange"
Cohesion: 0.67
Nodes (3): filterNewComponentsByType(), handleOldComponentChange(), updateQuickSwapCollectionWarning()

### Community 65 - "Git Workflow Rules"
Cohesion: 0.25
Nodes (8): Version Script CI Workflow, Branch Strategy, Commit Process, For All Agents, For code-reviewer, For docs-maintainer, For fullstack-developer, Git Workflow Rules

### Community 66 - ".modify_component_details"
Cohesion: 0.25
Nodes (4): Method to update component details, Validate threshold configuration rules for component intervals, Method to create or update component types, Method to update only the count of components for a given component type

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

### Community 96 - ".calculate_component_triggers"
Cohesion: 0.33
Nodes (3): Method to compute component status using threshold logic, Method to determine which factor triggered a warning status, Calculate lifetime and service triggers for a component

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

### Community 104 - "config_overview"
Cohesion: 0.50
Nodes (4): config_overview(), Endpoint for component types page, get_button_sorting_config(), Function to get button sorting configuration for config page

### Community 105 - "get_filtered_log"
Cohesion: 0.50
Nodes (4): get_filtered_log(), Endpoint to read log and return only business events, Function to get filtered log records, read_filtered_logs()

### Community 106 - "update_config"
Cohesion: 0.50
Nodes (4): Endpoint to update config file based on which form was submitted, update_config(), Helper function to shutdown the server after a short delay, shutdown_server()

### Community 107 - "docs-maintainer.md"
Cohesion: 0.50
Nodes (3): Core Responsibilities, Documentation Rules, Workflow

### Community 108 - "Code Style & Standards"
Cohesion: 0.50
Nodes (4): Code Style & Standards, Database, Frontend, Python (Backend)

### Community 109 - "Development Notes"
Cohesion: 0.50
Nodes (4): Database Schema Changes, Development Notes, Docker Development, Logging

### Community 110 - "Standard Development Workflow"
Cohesion: 0.50
Nodes (4): For Bug Fixes, For Documentation Updates, For New Features, Standard Development Workflow

### Community 111 - "Sub-Agent Team"
Cohesion: 0.67
Nodes (3): Available Agents, Direct Invocation, Sub-Agent Team

### Community 112 - "Testing Requirements"
Cohesion: 0.67
Nodes (3): Before Creating Handover, For fullstack-developer, Testing Requirements

### Community 113 - "initializeComponentSelector"
Cohesion: 0.67
Nodes (3): editCollection(), initializeComponentSelector(), updateFormFields()

## Ambiguous Edges - Review These
- `Git Workflow Rules` → `Version Script CI Workflow`  [AMBIGUOUS]
  .github/workflows/run_version_script.yml · relation: conceptually_related_to

## Knowledge Gaps
- **130 isolated node(s):** `backup_db.sh script`, `create-container-vs2000.sh script`, `velo-supervisor-2000`, `Core Responsibilities`, `Workflow` (+125 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 422 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **57 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `Git Workflow Rules` and `Version Script CI Workflow`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **Why does `DatabaseManager` connect `DatabaseManager` to `utils.py`, `Meta`, `.write_delete_record`, `.read_bike_name`, `.read_component`, `.read_single_component_type`, `.count_component_types_in_use`, `.read_all_collections`, `.read_all_component_types`, `.read_all_components_objects`, `.read_all_incidents`, `.read_all_workplans`, `.read_bike_id_recent_component_history`, `.read_bikes`, `.read_collection_by_component`, `.read_incidents_by_workplan`, `.read_latest_history_record`, `.read_latest_ride_record`, `.read_latest_service_record`, `.read_matching_rides`, `.read_oldest_history_record`, `.read_planned_workplans`, `.read_recent_rides`, `.read_services_by_workplan`, `.read_subset_components`, `.read_subset_service_history`, `.read_subset_service_record`, `.read_sum_distance_subset_rides`, `.read_unique_bikes`, `.write_bike_service_status`, `.write_collection`, `.write_component_lifetime_status`, `.write_history_record`, `.write_incident_record`, `.write_service_record`, `.write_workplan`?**
  _High betweenness centrality (0.155) - this node is a cross-community bridge._
- **Why does `BusinessLogic` connect `BusinessLogic` to `.calculate_component_triggers`, `utils.py`, `.modify_component_details`, `.get_component_overview`, `scheduler.py`, `.process_history_records`, `.create_service_record`, `.create_component`, `.calculate_collection_status`?**
  _High betweenness centrality (0.113) - this node is a cross-community bridge._
- **Are the 9 inferred relationships involving `DatabaseManager` (e.g. with `Bikes` and `Collections`) actually correct?**
  _`DatabaseManager` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `BusinessLogic` (e.g. with `strava_sync_job()` and `update_time_based_fields_job()`) actually correct?**
  _`BusinessLogic` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `backup_db.sh script`, `create-container-vs2000.sh script`, `velo-supervisor-2000` to the rest of the system?**
  _130 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `utils.py` be split into smaller, more focused modules?**
  _Cohesion score 0.0576271186440678 - nodes in this community are weakly interconnected._