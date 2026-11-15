# Graph Report - velo-supervisor-2000  (2026-11-15)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 1101 nodes · 1817 edges · 137 communities (56 shown, 81 thin omitted)
- Extraction: 85% EXTRACTED · 15% INFERRED · 0% AMBIGUOUS · INFERRED: 279 edges (avg confidence: 0.91)
- Token cost: 77,335 input · 1,827 output

## Graph Freshness
- Built from commit: `dce93544`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- API Route Handlers
- App Startup and Scheduler
- Page Endpoints
- Config and Test Fixtures
- Database ORM Models
- Frontend Forms and Search
- Overview Payloads and Triggers
- Version Workflow CI
- Database Read Queries
- Service and History Queries
- Page Templates and Help
- Component Lifecycle Logic
- Detail Page Payloads
- Service Record Processing
- Strava API Client
- Service Integration Design
- Component Type Migration
- Error Handling Middleware
- Initial Table Migrations
- Health Check System
- Help Page
- Service Integration Test Findings
- Service Integration Spec
- Migration Tests
- Release Notes and Incident Titles
- Record Updates and Validation
- Date Picker Fixes
- Development Workflows
- Service Integration Code Review
- Service Design Decisions
- Base Layout Templates
- Incident and Workplan Creation
- Service Integration Migrations
- Project Guide Overview
- Git Workflow Rules
- Component Time Fields Migration
- Workplan Planned Service Migration
- Project Conventions
- Code Reviewer Agent
- Form Validation JS
- Table Sorting and Filtering
- Handover Template
- Database Expert Agent
- UX Designer Agent
- Service Integration Implementation
- Service Test Protocol
- Incident Link Migration
- Migration Entry Point
- Handover Communication Guide
- Fullstack Developer Agent
- Product Manager Agent
- Form Field Validation
- Handovers Directory Guide
- Version Script
- Architect Agent
- Architecture Overview
- Development Commands
- Development Notes
- History Notes Migration
- Component Type Time Migration
- Service Workplan Link Migration
- Workplan Name Migration
- Log Filtering
- Config Update and Shutdown
- Docs Maintainer Agent
- Code Style Standards
- Bulk Status Change Modal
- Markdown Preview Rendering
- Incident Table Filtering
- Quick Swap Logic
- Testing Requirements
- Container Build Script
- Strava OAuth Setup
- Branching and Versioning
- Changelog and Project Board
- Error Page Illustration
- Fox Mechanic Logo
- Component Collections
- Component Types vs Components
- Hybrid Time-Distance Tracking
- Mileage Tracking
- Lifetime and Service Thresholds
- Defining Component Types
- Component Types Page
- Config and Strava Sync
- Incidents Page
- Workplans Page
- Data Management Tips
- Help and Troubleshooting
- Confirm Action Modal
- Loading Modal
- Report Modal
- Validation Error Modal
- Project Root
- Manual Onboarding Setup
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
1. `DatabaseManager` - 71 edges
2. `BusinessLogic` - 65 edges
3. `run_all_migrations()` - 24 edges
4. `seed_component()` - 24 edges
5. `seed_rides()` - 20 edges
6. `Bike Details Template` - 19 edges
7. `Component Details Template` - 18 edges
8. `get_workplan_data_tuple()` - 17 edges
9. `get_incident_data_tuple()` - 15 edges
10. `What was checked and held up` - 15 edges

## Surprising Connections (you probably didn't know these)
- `Migration` --references--> `generate_unique_id()`  [INFERRED]
  docs/superpowers/specs/2026-09-18-service-integration-design.md → backend/utils.py
- `Warning when resolving an incident with open services, 2026-09-26` --references--> `initializeIncidentForm()`  [INFERRED]
  docs/superpowers/plans/2026-09-25-service-integration-test-findings.md → frontend/static/js/main.js
- `Deliverables` --references--> `ErrorRecorder`  [INFERRED]
  .handovers/fullstack/health-check-fullstack-to-reviewer.md → backend/utils.py
- `Optional workplan_name (migration step 17)` --references--> `Workplans`  [INFERRED]
  .handovers/fullstack/service-integration-fullstack-to-reviewer.md → backend/database_model.py
- `Verification done` --references--> `modules()`  [INFERRED]
  .handovers/review/health-check-reviewer-to-docs-maintainer.md → tests/conftest.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Health check mechanism (#103)** — backend_utils_errorrecorder, backend_utils_get_health_status, backend_database_manager_databasemanager_check_database_connection, backend_main_health, backend_healthcheck, handovers_fullstack_health_check_fullstack_to_reviewer_health_check_feature [EXTRACTED 1.00]
- **Planned services invisible to health** — docs_superpowers_specs_2026_09_18_service_integration_design_planned_invisible_to_health, backend_database_manager_databasemanager_read_latest_service_record, backend_business_logic_businesslogic_process_service_records, backend_business_logic_businesslogic_update_component_service_status, backend_database_model_services [EXTRACTED 1.00]
- **Service integration spec, implementation, test and review cycle** — docs_superpowers_specs_2026_09_18_service_integration_design, handovers_fullstack_service_integration_fullstack_to_reviewer, docs_superpowers_plans_2026_09_25_service_integration_test_findings, tests_test_protocol_services, handovers_review_service_integration_reviewer_to_docs_maintainer [EXTRACTED 1.00]
- **Installation Status Change Forms** — frontend_templates_modal_install_component_installcomponentmodal, frontend_templates_modal_update_component_status_editcomponentstatusmodal, frontend_templates_modal_edit_installation_record_edithistorymodal, frontend_templates_modal_quick_swap_quickswapmodal, backend_main_add_history_record [INFERRED 0.85]
- **Incident to Workplan to Completed Services Flow** — frontend_templates_modal_incident_record_incidentrecordmodal, frontend_templates_modal_workplan_record_workplanrecordmodal, frontend_templates_modal_plan_services_planservicesmodal, frontend_templates_modal_complete_services_completeservicesmodal, frontend_templates_modal_complete_workplan_template, frontend_templates_help_common_tasks_incident_to_finished_work [INFERRED 0.85]
- **Plan and Complete Services Workflow** — frontend_templates_modal_plan_services_planservicesmodal, frontend_templates_modal_complete_services_completeservicesmodal, backend_main_add_planned_services, backend_main_complete_services, frontend_templates_modal_service_record_servicerecordmodal, frontend_templates_help_common_tasks_planning_service [INFERRED 0.85]

## Communities (137 total, 81 thin omitted)

### Community 0 - "API Route Handlers"
Cohesion: 0.06
Nodes (19): add_collection(), add_incident_record(), add_planned_services(), add_service(), add_workplan(), change_collection_status(), complete_services(), component_modify() (+11 more)

### Community 1 - "App Startup and Scheduler"
Cohesion: 0.07
Nodes (11): lifespan(), start_scheduler(), stop_scheduler(), strava_sync_job(), update_time_based_fields_job(), Verification done, recording_logger(), test_missing_database_file_makes_app_unhealthy() (+3 more)

### Community 2 - "Page Endpoints"
Cohesion: 0.08
Nodes (15): add_history_record(), bike_details(), collection_details(), component_details(), component_overview(), component_types_overview(), config_overview(), incident_reports() (+7 more)

### Community 3 - "Config and Test Fixtures"
Cohesion: 0.08
Nodes (32): parse_button_sorting(), read_config(), write_config(), app_env(), migrated_env(), modules(), add_twin_component(), seed_component() (+24 more)

### Community 4 - "Database ORM Models"
Cohesion: 0.05
Nodes (21): BaseModel, Meta, Bikes, Meta, Collections, Meta, ComponentHistory, Meta (+13 more)

### Community 5 - "Frontend Forms and Search"
Cohesion: 0.09
Nodes (8): editCollection(), handleUpdate(), initializeCollectionsSearch(), updateRowVisibility(), initializeComponentSelector(), performQuickSwap(), showToast(), updateFormFields()

### Community 7 - "Version Workflow CI"
Cohesion: 0.11
Nodes (18): GITHUB_TOKEN, jobs, run-script, name, branches, branches, runs-on, steps (+10 more)

### Community 10 - "Page Templates and Help"
Cohesion: 0.24
Nodes (23): Bike Details Template, Collection Details Template, Component Details Template, Component Overview Template, From Incident to Finished Work (Help), Planning Service Before You Do It (Help), Quick Swap Components, Incident Reports Template (+15 more)

### Community 12 - "Detail Page Payloads"
Cohesion: 0.12
Nodes (14): calculate_elapsed_days(), derive_workplan_context(), get_formatted_bikes_list(), get_formatted_datetime_now(), get_incident_data_tuple(), get_planned_service_data_tuple(), get_workplan_data_tuple(), get_workplan_names_dict() (+6 more)

### Community 13 - "Service Record Processing"
Cohesion: 0.09
Nodes (14): Backend, business_logic.py, Completed to Planned revert uses deletion recalculation, Decisions, main.py, Bugs found and fixed, Files, Known limitations (+6 more)

### Community 16 - "Service Integration Design"
Cohesion: 0.19
Nodes (7): Migration steps 12-16 (idempotent check_/migrate_ pairs), Planned vs Completed service status, validate_service_record modes (plan/complete/edit/revert), Production DB regression comparison (master vs branch), Migration test cases M1-M7, Regression test cases R1-R4, Component status notes and retirement cases N1-N8

### Community 17 - "Component Type Migration"
Cohesion: 0.32
Nodes (3): check_component_types_columns(), count_component_types_in_use(), migrate_component_types()

### Community 19 - "Initial Table Migrations"
Cohesion: 0.14
Nodes (7): create_collections_table(), create_incidents_table(), create_workplans_table(), populate_component_types_thresholds(), populate_components_thresholds(), recalculate_distance_based_statuses(), run_all_migrations()

### Community 20 - "Health Check System"
Cohesion: 0.06
Nodes (23): health(), ErrorRecorder, get_health_status(), Docker HEALTHCHECK against /health, Blockers / Open Questions, Context, Decisions Made, Deliverables (+15 more)

### Community 21 - "Help Page"
Cohesion: 0.33
Nodes (6): help_page(), helpTopics Data Object, Help Page Template, Help Search Functionality, showHelpTopic() Function, Documentation Modal

### Community 22 - "Service Integration Test Findings"
Cohesion: 0.20
Nodes (9): A. Questions to answer from the code, no change expected, C. Interface changes the user asked for, D4: choose components when creating workplan from incident, Extra wording fixes asked for on 2026-09-26, Manual walkthrough findings (A/B/C/D groups), Re-test list for the second round, Service integration (#351): findings from the manual test walkthrough, Status (2026-09-26) (+1 more)

### Community 23 - "Service Integration Spec"
Cohesion: 0.18
Nodes (11): Data model, Error handling, Goal, main.js, Migration, Modals, Out of scope, Pages (+3 more)

### Community 24 - "Migration Tests"
Cohesion: 0.35
Nodes (8): columns(), create_old_schema(), run_migration(), seed_old_data(), snapshot(), test_migration_converts_old_model(), test_migration_is_idempotent(), test_migration_on_fresh_template()

### Community 25 - "Release Notes and Incident Titles"
Cohesion: 0.07
Nodes (28): v0.5.0.ca636f8, generate_incident_title(), get_service_incident_options(), Technical debt tracked in issue #356, Context, Docs changes, docs-maintainer -> Human Handover, Double-check (+20 more)

### Community 28 - "Date Picker Fixes"
Cohesion: 0.40
Nodes (4): B3: service modal submittable without completion date, B. Bugs to fix, Status (2026-09-26), initializeDatePickers()

### Community 29 - "Development Workflows"
Cohesion: 0.50
Nodes (4): For Bug Fixes, For Documentation Updates, For New Features, Standard Development Workflow

### Community 32 - "Service Integration Code Review"
Cohesion: 0.22
Nodes (7): renderIncidentServices(), Code review -> docs-maintainer Handover, Context, Dead reads read_all_services_by_component / read_all_planned_services, Recommendations, References, Unescaped innerHTML in renderIncidentServices

### Community 33 - "Service Design Decisions"
Cohesion: 0.33
Nodes (6): D. Design questions to decide before coding, Decisions (2026-09-26), Follow-up tweaks asked for on 2026-09-26, Second round of tweaks, 2026-09-26, Third round of tweaks, 2026-09-26, Warning when resolving an incident with open services, 2026-09-26

### Community 34 - "Base Layout Templates"
Cohesion: 0.24
Nodes (10): Base Template, Component Types Template, Config Template, Error Page Template, Footer Template, Bike Overview Template, nav_menu Macro, Navigation Menu Template (+2 more)

### Community 35 - "Incident and Workplan Creation"
Cohesion: 0.08
Nodes (13): build_incident_service_entry(), calculate_percentage_reached(), generate_unique_id(), generate_workplan_title(), get_current_version(), get_effective_planned_date(), parse_json_string(), resolve_workplan_title() (+5 more)

### Community 36 - "Service Integration Migrations"
Cohesion: 0.22
Nodes (5): check_incidents_workplan_column(), check_services_integration_columns(), migrate_incidents_workplan_link(), migrate_services_integration_columns(), Code review outcome, 2026-09-26

### Community 37 - "Project Guide Overview"
Cohesion: 0.22
Nodes (8): Available Agents, Communication & Output Rules, Debugging & Bug Fixing Rules, Direct Invocation, graphify, Important Notes, Project Overview, Sub-Agent Team

### Community 38 - "Git Workflow Rules"
Cohesion: 0.29
Nodes (7): Branch Strategy, Commit Process, For All Agents, For code-reviewer, For docs-maintainer, For fullstack-developer, Git Workflow Rules

### Community 40 - "Workplan Planned Service Migration"
Cohesion: 0.25
Nodes (4): check_workplans_affected_columns(), migrate_drop_workplan_affected_columns(), migrate_workplans_to_planned_services(), read_names_for_migration()

### Community 41 - "Project Conventions"
Cohesion: 0.33
Nodes (3): Change Management Rules, graphify knowledge graph usage rules, TomSelect multi-select pattern

### Community 42 - "Code Reviewer Agent"
Cohesion: 0.25
Nodes (7): Issues Found, Key Checks, Output Format, Recommendations, Review Philosophy, Review Process, Summary

### Community 43 - "Form Validation JS"
Cohesion: 0.17
Nodes (11): Validation, initializeIncidentForm(), initializeWorkplanForm(), submitCollectionAjax(), submitComponentAjax(), validateCollectionStatusChange(), validateDateInput(), validateIncidentForm() (+3 more)

### Community 44 - "Table Sorting and Filtering"
Cohesion: 0.29
Nodes (8): initializeCollectionsSorting(), sortColumn(), initializeWorkplanTable(), setupIncidentTableSorting(), setupWorkplanSearch(), setupWorkplanStatusFiltering(), setupWorkplanTableSorting(), updateWorkplansVisibility()

### Community 45 - "Handover Template"
Cohesion: 0.25
Nodes (7): Blockers / Open Questions, Context, Decisions Made, Deliverables, Next Steps for [Target Agent], References, [Source Agent] -> [Target Agent] Handover

### Community 48 - "Database Expert Agent"
Cohesion: 0.29
Nodes (6): Constraints, Core Responsibilities, Pattern Consistency - CRITICAL, Query Optimization, Schema Changes, Workflow

### Community 49 - "UX Designer Agent"
Cohesion: 0.29
Nodes (6): Core Responsibilities, Design Principles, Specifications to Include, v1 (Before Architect), v2 (After Architect), Workflow

### Community 50 - "Service Integration Implementation"
Cohesion: 0.38
Nodes (5): FastAPI/Starlette TemplateResponse argument order fix, Workplan link silently lost bug (process_service_records without workplan_id), Optional workplan_name (migration step 17), db_migration step 16 rebuild before step 17 workplan_name, v0.5.0 release (service integration, health check, uv)

### Community 52 - "Service Test Protocol"
Cohesion: 0.29
Nodes (7): 2026-09-25, first walkthrough, human, 2026-09-26, regression against the baseline database, Claude, 2026-09-27, second walkthrough, human, Preparation, Results, Scope, Test Protocol: Planned services, workplans and incidents

### Community 55 - "Incident Link Migration"
Cohesion: 0.25
Nodes (4): check_incidents_workplan_column_present(), insert_planned_service_for_migration(), migrate_drop_incident_workplan_column(), migrate_incident_links_to_services()

### Community 56 - "Migration Entry Point"
Cohesion: 0.33
Nodes (3): find_database_file(), migrate_database(), prompt_for_db_path()

### Community 58 - "Handover Communication Guide"
Cohesion: 0.33
Nodes (6): Agent Communication via Handovers, Creating Handovers, Detailed Instructions, Handover Structure, Naming Convention, Reading Handovers

### Community 59 - "Fullstack Developer Agent"
Cohesion: 0.33
Nodes (5): Backend Patterns, Core Responsibilities, Frontend Patterns, Handover Content, Workflow

### Community 60 - "Product Manager Agent"
Cohesion: 0.33
Nodes (5): Boundaries, Core Responsibilities, Key Principle: You Are Interactive, Requirements Document, User Story Format

### Community 62 - "Form Field Validation"
Cohesion: 0.40
Nodes (5): addFormValidation(), clearValidationErrors(), showFieldError(), validateComponentThresholds(), validateQuickSwapForm()

### Community 63 - "Handovers Directory Guide"
Cohesion: 0.33
Nodes (5): Creating Handovers, Directory Structure, Finding Handovers, Handovers Directory, Rules

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

### Community 79 - "Docs Maintainer Agent"
Cohesion: 0.50
Nodes (3): Core Responsibilities, Documentation Rules, Workflow

### Community 80 - "Code Style Standards"
Cohesion: 0.50
Nodes (4): Code Style & Standards, Database, Frontend, Python (Backend)

### Community 82 - "Bulk Status Change Modal"
Cohesion: 0.50
Nodes (4): cleanup(), handleCancel(), handleConfirm(), performBulkStatusChange()

### Community 83 - "Markdown Preview Rendering"
Cohesion: 0.50
Nodes (4): containsMarkdown(), renderPreview(), setInitialMode(), updateCheckboxInText()

### Community 84 - "Incident Table Filtering"
Cohesion: 0.67
Nodes (4): initializeIncidentTable(), setupIncidentSearch(), setupIncidentStatusFiltering(), updateIncidentVisibility()

### Community 85 - "Quick Swap Logic"
Cohesion: 0.67
Nodes (3): filterNewComponentsByType(), handleOldComponentChange(), updateQuickSwapCollectionWarning()

### Community 87 - "Testing Requirements"
Cohesion: 0.67
Nodes (3): Before Creating Handover, For fullstack-developer, Testing Requirements

## Ambiguous Edges - Review These
- `conftest.py` → `Manual testing protocols approach`  [AMBIGUOUS]
  tests/README.md · relation: conceptually_related_to

## Knowledge Gaps
- **52 isolated node(s):** `Quick Swap Components`, `Strava OAuth Token Setup (Step 2)`, `Semantic Versioning (SemVer)`, `GitHub Project Board`, `Changelog Section` (+47 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 536 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **81 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `DatabaseManager` connect `Database Read Queries` to `Database ORM Models`, `Overview Payloads and Triggers`, `Service and History Queries`, `Health Check System`, `Latest Ride Read`, `Ride Distance Sum`, `Lifetime Status Write`, `Service Status Write`, `Workplan Write`, `Single Record Reads and Deletes`, `Component Read and Write`, `Bike Read and Write`, `Component Type Read and Write`, `Component Distance Update`, `Component Types Read`, `Component Objects Read`, `Workplans Read`, `Collection by Component Lookup`, `Oldest Ride Date`, `Matching Rides Read`, `Recent Rides Read`, `Component History Subset`, `Bike Components Read`, `Unique Bike IDs`, `Recent History Bike Lookup`, `Collection Write`, `Incident Record Write`, `Incidents by Workplan`?**
  _High betweenness centrality (0.210) - this node is a cross-community bridge._
- **Are the 9 inferred relationships involving `DatabaseManager` (e.g. with `Bikes` and `Collections`) actually correct?**
  _`DatabaseManager` has 9 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Quick Swap Components`, `Strava OAuth Token Setup (Step 2)`, `Semantic Versioning (SemVer)` to the rest of the system?**
  _52 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `API Route Handlers` be split into smaller, more focused modules?**
  _Cohesion score 0.06342494714587738 - nodes in this community are weakly interconnected._
- **Why does `BusinessLogic` connect `Component Lifecycle Logic` to `App Startup and Scheduler`, `Incident and Workplan Creation`, `Overview Payloads and Triggers`, `Detail Page Payloads`, `Service Record Processing`, `Collection Management`, `Health Check System`, `Record Updates and Validation`?**
  _High betweenness centrality (0.096) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `BusinessLogic` (e.g. with `strava_sync_job()` and `update_time_based_fields_job()`) actually correct?**
  _`BusinessLogic` has 2 INFERRED edges - model-reasoned connections that need verification._

### Low-confidence Hints
_AMBIGUOUS edges — the extractor was unsure. Verify before acting on these._

- **What is the exact relationship between `conftest.py` and `Manual testing protocols approach`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._