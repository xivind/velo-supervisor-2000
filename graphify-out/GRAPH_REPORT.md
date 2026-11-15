# Graph Report - velo-supervisor-2000  (2026-11-15)

## Corpus Check
- 45 files · ~92,137 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 12 file(s) not represented in the graph (top: (none) 5, .example 1, .sqlite 1)

## Summary
- 1125 nodes · 1840 edges · 130 communities (58 shown, 72 thin omitted)
- Extraction: 85% EXTRACTED · 15% INFERRED · 0% AMBIGUOUS · INFERRED: 279 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `ad301f8a`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- API Route Handlers
- App Startup and Scheduler
- Page Endpoints
- Config Read and Write
- Database Models
- Frontend Forms and Search
- Bike and Component Details
- Version Bump Workflow
- Database Bulk Reads
- Service Record Queries
- Page Templates and Help
- Component Distance and Status Updates
- Workplan Details and Naming
- Service Creation and Completion
- Collections and Overview Logic
- Strava API Integration
- Service Integration Test Findings
- Component Types Migration
- Error Handling Middleware
- Initial Table Migrations
- Docker Health Check
- Help Page
- Incident Data and Workplan Creation
- Service Integration Design Spec
- Migration Tests
- Post-Release Review Handover
- Record Update Validation
- Rewrite Roadmap Design
- Development Workflows
- Component Creation and Quick Swap
- Release Docs Handover
- Code Review Handover
- Service Status Processing
- Base Layout Templates
- Utility Functions
- Service Integration Column Migrations
- Project Guidelines Overview
- Git Workflow Rules
- Component Time Fields Migration
- Workplan Affected Columns Migration
- Project Conventions
- Code Reviewer Agent
- Form Validation
- Table Sorting and Filtering
- Handover Template
- Planned Service Display
- Database Expert Agent
- UX Designer Agent
- Incident and Workplan Payloads
- Component History Model
- Collections Model
- Services Model
- Incident Workplan Link Migration
- Migration Entry Point
- Handover Communication
- Fullstack Developer Agent
- Product Manager Agent
- Field Validation Helpers
- Handovers Directory Guide
- Version Script
- Architect Agent
- Architecture Overview
- Development Commands
- Development Notes
- History Notes Migration
- Component Type Time Migration
- Services Workplan Link Migration
- Workplan Name Migration
- Log Filtering
- Config Update and Shutdown
- Docs Maintainer Agent
- Code Style Standards
- Bulk Status Change Modal
- Markdown Preview Editor
- Incident Table Filtering
- Quick Swap Form
- Testing Requirements
- Container Deploy Script
- Strava OAuth Setup
- Branching and Versioning
- Changelog and Project Board
- Error Page Illustration
- Project Logo
- Collections Concept
- Component Types Concept
- Time and Distance Tracking
- Mileage Tracking
- Understanding Thresholds
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
- `Context` --references--> `get_service_incident_options()`  [INFERRED]
  .handovers/documentation/post-release-fixes-docs-maintainer-to-human.md → backend/utils.py
- `Migration` --references--> `generate_unique_id()`  [INFERRED]
  docs/superpowers/specs/2026-09-18-service-integration-design.md → backend/utils.py
- `Warning when resolving an incident with open services, 2026-09-26` --references--> `initializeIncidentForm()`  [INFERRED]
  docs/superpowers/plans/2026-09-25-service-integration-test-findings.md → frontend/static/js/main.js
- `Deliverables` --references--> `ErrorRecorder`  [INFERRED]
  .handovers/fullstack/health-check-fullstack-to-reviewer.md → backend/utils.py
- `Optional workplan_name (migration step 17)` --references--> `Workplans`  [INFERRED]
  .handovers/fullstack/service-integration-fullstack-to-reviewer.md → backend/database_model.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Health check mechanism (#103)** — backend_utils_errorrecorder, backend_utils_get_health_status, backend_database_manager_databasemanager_check_database_connection, backend_main_health, backend_healthcheck, handovers_fullstack_health_check_fullstack_to_reviewer_health_check_feature [EXTRACTED 1.00]
- **Planned services invisible to health** — docs_superpowers_specs_2026_09_18_service_integration_design_planned_invisible_to_health, backend_database_manager_databasemanager_read_latest_service_record, backend_business_logic_businesslogic_process_service_records, backend_business_logic_businesslogic_update_component_service_status, backend_database_model_services [EXTRACTED 1.00]
- **Service integration spec, implementation, test and review cycle** — docs_superpowers_specs_2026_09_18_service_integration_design, handovers_fullstack_service_integration_fullstack_to_reviewer, docs_superpowers_plans_2026_09_25_service_integration_test_findings, tests_test_protocol_services, handovers_review_service_integration_reviewer_to_docs_maintainer [EXTRACTED 1.00]
- **Installation Status Change Forms** — frontend_templates_modal_install_component_installcomponentmodal, frontend_templates_modal_update_component_status_editcomponentstatusmodal, frontend_templates_modal_edit_installation_record_edithistorymodal, frontend_templates_modal_quick_swap_quickswapmodal, backend_main_add_history_record [INFERRED 0.85]
- **Incident to Workplan to Completed Services Flow** — frontend_templates_modal_incident_record_incidentrecordmodal, frontend_templates_modal_workplan_record_workplanrecordmodal, frontend_templates_modal_plan_services_planservicesmodal, frontend_templates_modal_complete_services_completeservicesmodal, frontend_templates_modal_complete_workplan_template, frontend_templates_help_common_tasks_incident_to_finished_work [INFERRED 0.85]
- **Plan and Complete Services Workflow** — frontend_templates_modal_plan_services_planservicesmodal, frontend_templates_modal_complete_services_completeservicesmodal, backend_main_add_planned_services, backend_main_complete_services, frontend_templates_modal_service_record_servicerecordmodal, frontend_templates_help_common_tasks_planning_service [INFERRED 0.85]

## Communities (130 total, 72 thin omitted)

### Community 0 - "API Route Handlers"
Cohesion: 0.06
Nodes (19): add_collection(), add_history_record(), add_incident_record(), add_planned_services(), add_service(), add_workplan(), change_collection_status(), complete_services() (+11 more)

### Community 1 - "App Startup and Scheduler"
Cohesion: 0.07
Nodes (11): lifespan(), start_scheduler(), stop_scheduler(), strava_sync_job(), update_time_based_fields_job(), Verification done, recording_logger(), test_missing_database_file_makes_app_unhealthy() (+3 more)

### Community 2 - "Page Endpoints"
Cohesion: 0.09
Nodes (14): bike_details(), collection_details(), component_details(), component_overview(), component_types_overview(), config_overview(), incident_reports(), refresh_all_bikes() (+6 more)

### Community 3 - "Config Read and Write"
Cohesion: 0.08
Nodes (32): parse_button_sorting(), read_config(), write_config(), app_env(), migrated_env(), modules(), add_twin_component(), seed_component() (+24 more)

### Community 4 - "Database Models"
Cohesion: 0.07
Nodes (14): BaseModel, Meta, Bikes, Meta, Components, Meta, ComponentTypes, Meta (+6 more)

### Community 5 - "Frontend Forms and Search"
Cohesion: 0.09
Nodes (8): editCollection(), handleUpdate(), initializeCollectionsSearch(), updateRowVisibility(), initializeComponentSelector(), performQuickSwap(), showToast(), updateFormFields()

### Community 6 - "Bike and Component Details"
Cohesion: 0.14
Nodes (4): calculate_percentage_reached(), format_component_status(), format_cost(), get_formatted_datetime_now()

### Community 7 - "Version Bump Workflow"
Cohesion: 0.11
Nodes (18): GITHUB_TOKEN, jobs, run-script, name, branches, branches, runs-on, steps (+10 more)

### Community 10 - "Page Templates and Help"
Cohesion: 0.24
Nodes (23): Bike Details Template, Collection Details Template, Component Details Template, Component Overview Template, From Incident to Finished Work (Help), Planning Service Before You Do It (Help), Quick Swap Components, Incident Reports Template (+15 more)

### Community 12 - "Workplan Details and Naming"
Cohesion: 0.22
Nodes (9): calculate_elapsed_days(), derive_workplan_context(), get_workplan_data_tuple(), get_workplan_names_dict(), resolve_workplan_title(), utils.py, derive_workplan_context computed twice per render, Issues found (none blocking) (+1 more)

### Community 13 - "Service Creation and Completion"
Cohesion: 0.15
Nodes (4): business_logic.py, Completed to Planned revert uses deletion recalculation, Plan and complete services modals sharing one JS helper, Files

### Community 16 - "Service Integration Test Findings"
Cohesion: 0.05
Nodes (40): A. Questions to answer from the code, no change expected, B3: service modal submittable without completion date, B. Bugs to fix, C. Interface changes the user asked for, D. Design questions to decide before coding, Decisions (2026-09-26), Extra wording fixes asked for on 2026-09-26, Follow-up tweaks asked for on 2026-09-26 (+32 more)

### Community 17 - "Component Types Migration"
Cohesion: 0.32
Nodes (3): check_component_types_columns(), count_component_types_in_use(), migrate_component_types()

### Community 19 - "Initial Table Migrations"
Cohesion: 0.14
Nodes (7): create_collections_table(), create_incidents_table(), create_workplans_table(), populate_component_types_thresholds(), populate_components_thresholds(), recalculate_distance_based_statuses(), run_all_migrations()

### Community 20 - "Docker Health Check"
Cohesion: 0.06
Nodes (25): health(), ErrorRecorder, get_health_status(), Docker HEALTHCHECK against /health, Technical debt tracked in issue #356, Blockers / Open Questions, Context, Decisions Made (+17 more)

### Community 21 - "Help Page"
Cohesion: 0.33
Nodes (6): help_page(), helpTopics Data Object, Help Page Template, Help Search Functionality, showHelpTopic() Function, Documentation Modal

### Community 22 - "Incident Data and Workplan Creation"
Cohesion: 0.20
Nodes (6): build_incident_service_entry(), get_incident_data_tuple(), parse_json_string(), D4: choose components when creating workplan from incident, Status (2026-09-26), Second round, 2026-09-26, after the manual walkthrough

### Community 23 - "Service Integration Design Spec"
Cohesion: 0.15
Nodes (13): Backend, Data model, Error handling, Goal, main.js, main.py, Migration, Modals (+5 more)

### Community 24 - "Migration Tests"
Cohesion: 0.35
Nodes (8): columns(), create_old_schema(), run_migration(), seed_old_data(), snapshot(), test_migration_converts_old_model(), test_migration_is_idempotent(), test_migration_on_fresh_template()

### Community 25 - "Post-Release Review Handover"
Cohesion: 0.13
Nodes (17): generate_incident_title(), get_service_incident_options(), Service integration: services as unit of work (#351), Post-release fixes to v0.5.0, Blockers / Open Questions, Checked and OK: setServiceModalSelect, code-reviewer -> docs-maintainer Handover, Context (+9 more)

### Community 28 - "Rewrite Roadmap Design"
Cohesion: 0.08
Nodes (23): Anti-goals, API: separate API, or one set of resources with two formats, API style: FHIR-conformant or FHIR-inspired, Approaches considered, Branch policy during the freeze, Constraints, Delivery: side by side on master, or frozen master and long-running dev, Frontend: server-rendered with htmx, or a JSON API with a separate frontend app (+15 more)

### Community 29 - "Development Workflows"
Cohesion: 0.50
Nodes (4): For Bug Fixes, For Documentation Updates, For New Features, Standard Development Workflow

### Community 31 - "Release Docs Handover"
Cohesion: 0.14
Nodes (10): v0.5.0.ca636f8, Context, Docs changes, docs-maintainer -> Human Handover, Double-check, Files to commit, Option A: one commit, Option B: three commits (main.js needs `git add -p`) (+2 more)

### Community 32 - "Code Review Handover"
Cohesion: 0.50
Nodes (4): Code review -> docs-maintainer Handover, Context, Recommendations, References

### Community 33 - "Service Status Processing"
Cohesion: 0.19
Nodes (9): Decisions, Bugs found and fixed, Known limitations, Next steps, Regression evidence, 2026-09-26, Reuse, Service integration (#351) - fullstack to code-reviewer, Testing (+1 more)

### Community 34 - "Base Layout Templates"
Cohesion: 0.24
Nodes (10): Base Template, Component Types Template, Config Template, Error Page Template, Footer Template, Bike Overview Template, nav_menu Macro, Navigation Menu Template (+2 more)

### Community 35 - "Utility Functions"
Cohesion: 0.24
Nodes (3): generate_workplan_title(), get_current_version(), strip_markdown_syntax()

### Community 36 - "Service Integration Column Migrations"
Cohesion: 0.22
Nodes (5): check_incidents_workplan_column(), check_services_integration_columns(), migrate_incidents_workplan_link(), migrate_services_integration_columns(), Code review outcome, 2026-09-26

### Community 37 - "Project Guidelines Overview"
Cohesion: 0.22
Nodes (8): Available Agents, Communication & Output Rules, Debugging & Bug Fixing Rules, Direct Invocation, graphify, Important Notes, Project Overview, Sub-Agent Team

### Community 38 - "Git Workflow Rules"
Cohesion: 0.29
Nodes (7): Branch Strategy, Commit Process, For All Agents, For code-reviewer, For docs-maintainer, For fullstack-developer, Git Workflow Rules

### Community 40 - "Workplan Affected Columns Migration"
Cohesion: 0.25
Nodes (4): check_workplans_affected_columns(), migrate_drop_workplan_affected_columns(), migrate_workplans_to_planned_services(), read_names_for_migration()

### Community 41 - "Project Conventions"
Cohesion: 0.33
Nodes (3): Change Management Rules, graphify knowledge graph usage rules, TomSelect multi-select pattern

### Community 42 - "Code Reviewer Agent"
Cohesion: 0.25
Nodes (7): Issues Found, Key Checks, Output Format, Recommendations, Review Philosophy, Review Process, Summary

### Community 43 - "Form Validation"
Cohesion: 0.17
Nodes (11): Validation, initializeIncidentForm(), initializeWorkplanForm(), submitCollectionAjax(), submitComponentAjax(), validateCollectionStatusChange(), validateDateInput(), validateIncidentForm() (+3 more)

### Community 44 - "Table Sorting and Filtering"
Cohesion: 0.29
Nodes (8): initializeCollectionsSorting(), sortColumn(), initializeWorkplanTable(), setupIncidentTableSorting(), setupWorkplanSearch(), setupWorkplanStatusFiltering(), setupWorkplanTableSorting(), updateWorkplansVisibility()

### Community 45 - "Handover Template"
Cohesion: 0.25
Nodes (7): Blockers / Open Questions, Context, Decisions Made, Deliverables, Next Steps for [Target Agent], References, [Source Agent] -> [Target Agent] Handover

### Community 47 - "Planned Service Display"
Cohesion: 0.29
Nodes (5): get_effective_planned_date(), get_planned_service_data_tuple(), Effective planned date fallback, Key decisions, Tuple shapes: incident 17, workplan 14, planned service 11 fields

### Community 48 - "Database Expert Agent"
Cohesion: 0.29
Nodes (6): Constraints, Core Responsibilities, Pattern Consistency - CRITICAL, Query Optimization, Schema Changes, Workflow

### Community 49 - "UX Designer Agent"
Cohesion: 0.29
Nodes (6): Core Responsibilities, Design Principles, Specifications to Include, v1 (Before Architect), v2 (After Architect), Workflow

### Community 51 - "Component History Model"
Cohesion: 0.40
Nodes (3): ComponentHistory, Meta, Notes on component status change (#349)

### Community 55 - "Incident Workplan Link Migration"
Cohesion: 0.25
Nodes (4): check_incidents_workplan_column_present(), insert_planned_service_for_migration(), migrate_drop_incident_workplan_column(), migrate_incident_links_to_services()

### Community 56 - "Migration Entry Point"
Cohesion: 0.33
Nodes (3): find_database_file(), migrate_database(), prompt_for_db_path()

### Community 58 - "Handover Communication"
Cohesion: 0.33
Nodes (6): Agent Communication via Handovers, Creating Handovers, Detailed Instructions, Handover Structure, Naming Convention, Reading Handovers

### Community 59 - "Fullstack Developer Agent"
Cohesion: 0.33
Nodes (5): Backend Patterns, Core Responsibilities, Frontend Patterns, Handover Content, Workflow

### Community 60 - "Product Manager Agent"
Cohesion: 0.33
Nodes (5): Boundaries, Core Responsibilities, Key Principle: You Are Interactive, Requirements Document, User Story Format

### Community 62 - "Field Validation Helpers"
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

### Community 83 - "Markdown Preview Editor"
Cohesion: 0.50
Nodes (4): containsMarkdown(), renderPreview(), setInitialMode(), updateCheckboxInText()

### Community 84 - "Incident Table Filtering"
Cohesion: 0.67
Nodes (4): initializeIncidentTable(), setupIncidentSearch(), setupIncidentStatusFiltering(), updateIncidentVisibility()

### Community 85 - "Quick Swap Form"
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
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 557 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **72 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `DatabaseManager` connect `Database Bulk Reads` to `Component History Query`, `Database Models`, `Unique Bikes Query`, `Bike and Component Details`, `Bike Record Access`, `Bike Service Status Write`, `Service Record Queries`, `Collection Write`, `Component History Model`, `Docker Health Check`, `Latest Ride Query`, `Component Record Access`, `Collections Model`, `Services Model`, `Component Types Read`, `Single Record Reads`, `Service Record Lookup`, `Installed Components Query`?**
  _High betweenness centrality (0.143) - this node is a cross-community bridge._
- **Are the 9 inferred relationships involving `DatabaseManager` (e.g. with `Bikes` and `Collections`) actually correct?**
  _`DatabaseManager` has 9 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Quick Swap Components`, `Strava OAuth Token Setup (Step 2)`, `Semantic Versioning (SemVer)` to the rest of the system?**
  _52 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `API Route Handlers` be split into smaller, more focused modules?**
  _Cohesion score 0.06161616161616162 - nodes in this community are weakly interconnected._
- **Why does `BusinessLogic` connect `Collections and Overview Logic` to `App Startup and Scheduler`, `Service Status Processing`, `Bike and Component Details`, `Component Distance and Status Updates`, `Workplan Details and Naming`, `Service Creation and Completion`, `Component Status Thresholds`, `Incident and Workplan Payloads`, `Docker Health Check`, `Incident Data and Workplan Creation`, `Record Update Validation`, `Component Creation and Quick Swap`?**
  _High betweenness centrality (0.093) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `BusinessLogic` (e.g. with `strava_sync_job()` and `update_time_based_fields_job()`) actually correct?**
  _`BusinessLogic` has 2 INFERRED edges - model-reasoned connections that need verification._

### Low-confidence Hints
_AMBIGUOUS edges — the extractor was unsure. Verify before acting on these._

- **What is the exact relationship between `conftest.py` and `Manual testing protocols approach`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._