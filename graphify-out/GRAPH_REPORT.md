# Graph Report - velo-supervisor-2000  (2026-11-03)

## Corpus Check
- 44 files · ~89,237 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 12 file(s) not represented in the graph (top: (none) 5, .example 1, .sqlite 1)

## Summary
- 1074 nodes · 1779 edges · 141 communities (59 shown, 82 thin omitted)
- Extraction: 84% EXTRACTED · 16% INFERRED · 0% AMBIGUOUS · INFERRED: 279 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `2c69ba00`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- main.py
- scheduler.py
- get
- seed_component
- Meta
- main.js
- .get_bike_details
- middleware.py
- DatabaseManager
- database_manager.py
- Bike Details Template
- .process_service_records
- utils.py
- .recalculate_component_after_service_removal
- Strava
- 2026-09-18-service-integration-design.md
- migrate_component_types
- write_config
- run_all_migrations
- Health check for Docker daemon (#103)
- Fullstack Developer -> Code Reviewer Handover
- 2026-09-25-service-integration-test-findings.md
- Service integration: incidents, workplans and services
- test_migration.py
- code-reviewer -> docs-maintainer Handover
- validate_date_format
- add_planned_services
- test_health.py
- ErrorRecorder
- Code Reviewer -> Docs Maintainer Handover
- Code review -> docs-maintainer Handover
- D. Design questions to decide before coding
- Base Template
- .create_history_record
- migrate_incidents_workplan_link
- CLAUDE.md
- Git Workflow Rules
- db_migration.py
- check_workplans_affected_columns
- CLAUDE.md
- code-reviewer.md
- validateDateInput
- initializeWorkplanTable
- [Source Agent] -> [Target Agent] Handover
- health-check-reviewer-to-docs-maintainer.md
- database-expert.md
- ux-designer.md
- service-integration-fullstack-to-reviewer.md
- Service integration (#351) - fullstack to code-reviewer
- Results
- migrate_incident_links_to_services
- migrate_database
- Agent Communication via Handovers
- fullstack-developer.md
- product-manager.md
- validateComponentThresholds
- Handovers Directory
- version.py
- architect.md
- Architecture Overview
- Development Commands
- Development Notes
- migrate_component_history_notes
- migrate_component_types_time_fields
- migrate_services_workplan_link
- migrate_workplans_name_column
- get_filtered_log
- update_config
- docs-maintainer.md
- Code Style & Standards
- cleanup
- renderPreview
- initializeIncidentTable
- handleOldComponentChange
- Testing Requirements
- create-container-vs2000.sh
- Strava profile:read_all Scope Troubleshooting
- Dev/Staging/Master Branch Workflow
- Changelog Section
- Error Page Illustration
- Velo Supervisor Fox Mechanic Logo
- Collections (Core Concept)
- Component Types vs Components
- Hybrid Time + Distance Tracking
- Mileage Tracking
- Understanding Thresholds
- Getting Started: Define Component Types
- Component Types Page
- Config Page (Strava Sync)
- Incidents Page
- Workplans Page
- Data Management Tips
- Need More Help? (Troubleshooting)
- Confirm Action Modal
- Loading Modal
- Report Modal
- Validation Error Modal
- velo-supervisor-2000
- Manual Onboarding Setup Procedure
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
- v0.4.9 Release (Current)

## God Nodes (most connected - your core abstractions)
1. `DatabaseManager` - 71 edges
2. `BusinessLogic` - 65 edges
3. `run_all_migrations()` - 24 edges
4. `seed_component()` - 24 edges
5. `Meta` - 20 edges
6. `seed_rides()` - 20 edges
7. `Bike Details Template` - 19 edges
8. `Component Details Template` - 18 edges
9. `get_workplan_data_tuple()` - 17 edges
10. `get_incident_data_tuple()` - 15 edges

## Surprising Connections (you probably didn't know these)
- `Deliverables` --references--> `ErrorRecorder`  [INFERRED]
  .handovers/fullstack/health-check-fullstack-to-reviewer.md → backend/utils.py
- `Migration` --references--> `generate_unique_id()`  [INFERRED]
  docs/superpowers/specs/2026-09-18-service-integration-design.md → backend/utils.py
- `Warning when resolving an incident with open services, 2026-09-26` --references--> `initializeIncidentForm()`  [INFERRED]
  docs/superpowers/plans/2026-09-25-service-integration-test-findings.md → frontend/static/js/main.js
- `Convention check` --references--> `generate_incident_title()`  [INFERRED]
  .handovers/review/post-release-fixes-reviewer-to-docs-maintainer.md → backend/utils.py
- `Context` --references--> `get_service_incident_options()`  [INFERRED]
  .handovers/documentation/post-release-fixes-docs-maintainer-to-human.md → backend/utils.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Health check mechanism (#103)** — backend_utils_errorrecorder, backend_utils_get_health_status, backend_database_manager_databasemanager_check_database_connection, backend_main_health, backend_healthcheck, handovers_fullstack_health_check_fullstack_to_reviewer_health_check_feature [EXTRACTED 1.00]
- **Planned services invisible to health** — docs_superpowers_specs_2026_09_18_service_integration_design_planned_invisible_to_health, backend_database_manager_databasemanager_read_latest_service_record, backend_business_logic_businesslogic_process_service_records, backend_business_logic_businesslogic_update_component_service_status, backend_database_model_services [EXTRACTED 1.00]
- **Service integration spec, implementation, test and review cycle** — docs_superpowers_specs_2026_09_18_service_integration_design, handovers_fullstack_service_integration_fullstack_to_reviewer, docs_superpowers_plans_2026_09_25_service_integration_test_findings, tests_test_protocol_services, handovers_review_service_integration_reviewer_to_docs_maintainer [EXTRACTED 1.00]
- **Installation Status Change Forms** — frontend_templates_modal_install_component_installcomponentmodal, frontend_templates_modal_update_component_status_editcomponentstatusmodal, frontend_templates_modal_edit_installation_record_edithistorymodal, frontend_templates_modal_quick_swap_quickswapmodal, backend_main_add_history_record [INFERRED 0.85]
- **Incident to Workplan to Completed Services Flow** — frontend_templates_modal_incident_record_incidentrecordmodal, frontend_templates_modal_workplan_record_workplanrecordmodal, frontend_templates_modal_plan_services_planservicesmodal, frontend_templates_modal_complete_services_completeservicesmodal, frontend_templates_modal_complete_workplan_template, frontend_templates_help_common_tasks_incident_to_finished_work [INFERRED 0.85]
- **Plan and Complete Services Workflow** — frontend_templates_modal_plan_services_planservicesmodal, frontend_templates_modal_complete_services_completeservicesmodal, backend_main_add_planned_services, backend_main_complete_services, frontend_templates_modal_service_record_servicerecordmodal, frontend_templates_help_common_tasks_planning_service [INFERRED 0.85]

## Communities (141 total, 82 thin omitted)

### Community 0 - "main.py"
Cohesion: 0.07
Nodes (17): add_collection(), add_history_record(), add_incident_record(), add_service(), add_workplan(), change_collection_status(), component_modify(), component_types_modify() (+9 more)

### Community 1 - "scheduler.py"
Cohesion: 0.05
Nodes (9): http_exception_handler(), Middleware, start_scheduler(), stop_scheduler(), strava_sync_job(), update_time_based_fields_job(), app_env(), migrated_env() (+1 more)

### Community 2 - "get"
Cohesion: 0.09
Nodes (15): bike_details(), collection_details(), component_details(), component_overview(), component_types_overview(), config_overview(), help_page(), incident_reports() (+7 more)

### Community 3 - "seed_component"
Cohesion: 0.15
Nodes (26): add_twin_component(), seed_component(), seed_rides(), snapshot_health(), test_complete_after_workplan_done_is_refused(), test_complete_then_revert_matches_state_before_completion(), test_completed_only_reads_skip_planned(), test_delete_keeps_workplan_link_on_remaining_service() (+18 more)

### Community 4 - "Meta"
Cohesion: 0.08
Nodes (12): BaseModel, Bikes, Collections, ComponentHistory, Components, ComponentTypes, Incidents, Meta (+4 more)

### Community 5 - "main.js"
Cohesion: 0.09
Nodes (8): editCollection(), handleUpdate(), initializeCollectionsSearch(), updateRowVisibility(), initializeComponentSelector(), performQuickSwap(), showToast(), updateFormFields()

### Community 10 - "Bike Details Template"
Cohesion: 0.24
Nodes (23): Bike Details Template, Collection Details Template, Component Details Template, Component Overview Template, From Incident to Finished Work (Help), Planning Service Before You Do It (Help), Quick Swap Components, Incident Reports Template (+15 more)

### Community 11 - ".process_service_records"
Cohesion: 0.08
Nodes (4): BusinessLogic, Answers (read from the code 2026-09-25), Decisions, Reuse

### Community 12 - "utils.py"
Cohesion: 0.08
Nodes (23): calculate_elapsed_days(), calculate_percentage_reached(), derive_workplan_context(), generate_incident_title(), generate_workplan_title(), get_current_version(), get_formatted_bikes_list(), get_formatted_datetime_now() (+15 more)

### Community 13 - ".recalculate_component_after_service_removal"
Cohesion: 0.13
Nodes (5): Backend, business_logic.py, Completed to Planned revert uses deletion recalculation, main.py, Files

### Community 16 - "2026-09-18-service-integration-design.md"
Cohesion: 0.17
Nodes (7): Planned vs Completed service status, validate_service_record modes (plan/complete/edit/revert), Production DB regression comparison (master vs branch), Dead reads read_all_services_by_component / read_all_planned_services, Migration test cases M1-M7, Regression test cases R1-R4, Component status notes and retirement cases N1-N8

### Community 17 - "migrate_component_types"
Cohesion: 0.33
Nodes (3): check_component_types_columns(), count_component_types_in_use(), migrate_component_types()

### Community 18 - "write_config"
Cohesion: 0.33
Nodes (3): parse_button_sorting(), read_config(), write_config()

### Community 19 - "run_all_migrations"
Cohesion: 0.14
Nodes (8): create_collections_table(), create_workplans_table(), migrate_workplans_to_planned_services(), populate_component_types_thresholds(), read_names_for_migration(), recalculate_distance_based_statuses(), run_all_migrations(), Migration steps 12-16 (idempotent check_/migrate_ pairs)

### Community 20 - "Health check for Docker daemon (#103)"
Cohesion: 0.19
Nodes (4): health(), get_health_status(), Docker HEALTHCHECK against /health, Health check for Docker daemon (#103)

### Community 21 - "Fullstack Developer -> Code Reviewer Handover"
Cohesion: 0.22
Nodes (8): Blockers / Open Questions, Context, Decisions Made, Deliverables, Fullstack Developer -> Code Reviewer Handover, Next Steps for Code Reviewer, References, Verification done

### Community 22 - "2026-09-25-service-integration-test-findings.md"
Cohesion: 0.15
Nodes (13): A. Questions to answer from the code, no change expected, B3: service modal submittable without completion date, B. Bugs to fix, C. Interface changes the user asked for, D4: choose components when creating workplan from incident, Extra wording fixes asked for on 2026-09-26, Manual walkthrough findings (A/B/C/D groups), Re-test list for the second round (+5 more)

### Community 23 - "Service integration: incidents, workplans and services"
Cohesion: 0.18
Nodes (11): Data model, Error handling, Goal, main.js, Migration, Modals, Out of scope, Pages (+3 more)

### Community 24 - "test_migration.py"
Cohesion: 0.28
Nodes (8): columns(), create_old_schema(), run_migration(), seed_old_data(), snapshot(), test_migration_converts_old_model(), test_migration_is_idempotent(), test_migration_on_fresh_template()

### Community 25 - "code-reviewer -> docs-maintainer Handover"
Cohesion: 0.07
Nodes (23): v0.5.0.ca636f8, Context, Docs changes, docs-maintainer -> Human Handover, Double-check, Files to commit, Option A: one commit, Option B: three commits (main.js needs `git add -p`) (+15 more)

### Community 28 - "add_planned_services"
Cohesion: 0.40
Nodes (3): add_planned_services(), complete_services(), Plan and complete services modals sharing one JS helper

### Community 29 - "test_health.py"
Cohesion: 0.23
Nodes (6): Verification done, recording_logger(), test_missing_database_file_makes_app_unhealthy(), test_recorder_includes_exception_in_message(), test_recorder_keeps_errors_and_ignores_lower_levels(), test_recorder_keeps_errors_even_when_handler_level_is_reset()

### Community 30 - "ErrorRecorder"
Cohesion: 0.19
Nodes (4): ErrorRecorder, Technical debt tracked in issue #356, Stale ID 500 marks container unhealthy 24h (known limitation), ErrorRecorder thread safety under Handler.lock

### Community 31 - "Code Reviewer -> Docs Maintainer Handover"
Cohesion: 0.20
Nodes (8): Code Reviewer -> Docs Maintainer Handover, Context, Deliverables, Issues Found, Next Steps for Docs Maintainer, References, Resolution (2026-09-27, after review), test_failing_database_makes_app_unhealthy()

### Community 32 - "Code review -> docs-maintainer Handover"
Cohesion: 0.50
Nodes (4): Code review -> docs-maintainer Handover, Context, Recommendations, References

### Community 33 - "D. Design questions to decide before coding"
Cohesion: 0.20
Nodes (9): Code review outcome, 2026-09-26, D. Design questions to decide before coding, Decisions (2026-09-26), Follow-up tweaks asked for on 2026-09-26, Second round of tweaks, 2026-09-26, Third round of tweaks, 2026-09-26, Warning when resolving an incident with open services, 2026-09-26, renderIncidentServices() (+1 more)

### Community 34 - "Base Template"
Cohesion: 0.16
Nodes (15): Base Template, Component Types Template, Config Template, Error Page Template, Footer Template, helpTopics Data Object, Help Page Template, Help Search Functionality (+7 more)

### Community 36 - "migrate_incidents_workplan_link"
Cohesion: 0.25
Nodes (4): check_incidents_workplan_column(), check_services_integration_columns(), migrate_incidents_workplan_link(), migrate_services_integration_columns()

### Community 37 - "CLAUDE.md"
Cohesion: 0.22
Nodes (8): Available Agents, Communication & Output Rules, Debugging & Bug Fixing Rules, Direct Invocation, graphify, Important Notes, Project Overview, Sub-Agent Team

### Community 38 - "Git Workflow Rules"
Cohesion: 0.25
Nodes (8): Version Script CI Workflow, Branch Strategy, Commit Process, For All Agents, For code-reviewer, For docs-maintainer, For fullstack-developer, Git Workflow Rules

### Community 39 - "db_migration.py"
Cohesion: 0.22
Nodes (4): check_components_time_columns(), create_incidents_table(), migrate_components_time_fields(), populate_components_thresholds()

### Community 41 - "CLAUDE.md"
Cohesion: 0.20
Nodes (7): Change Management Rules, For Bug Fixes, For Documentation Updates, For New Features, graphify knowledge graph usage rules, Standard Development Workflow, TomSelect multi-select pattern

### Community 42 - "code-reviewer.md"
Cohesion: 0.25
Nodes (7): Issues Found, Key Checks, Output Format, Recommendations, Review Philosophy, Review Process, Summary

### Community 43 - "validateDateInput"
Cohesion: 0.17
Nodes (11): Validation, initializeIncidentForm(), initializeWorkplanForm(), submitCollectionAjax(), submitComponentAjax(), validateCollectionStatusChange(), validateDateInput(), validateIncidentForm() (+3 more)

### Community 44 - "initializeWorkplanTable"
Cohesion: 0.29
Nodes (8): initializeCollectionsSorting(), sortColumn(), initializeWorkplanTable(), setupIncidentTableSorting(), setupWorkplanSearch(), setupWorkplanStatusFiltering(), setupWorkplanTableSorting(), updateWorkplansVisibility()

### Community 45 - "[Source Agent] -> [Target Agent] Handover"
Cohesion: 0.25
Nodes (7): Blockers / Open Questions, Context, Decisions Made, Deliverables, Next Steps for [Target Agent], References, [Source Agent] -> [Target Agent] Handover

### Community 48 - "database-expert.md"
Cohesion: 0.29
Nodes (6): Constraints, Core Responsibilities, Pattern Consistency - CRITICAL, Query Optimization, Schema Changes, Workflow

### Community 49 - "ux-designer.md"
Cohesion: 0.29
Nodes (6): Core Responsibilities, Design Principles, Specifications to Include, v1 (Before Architect), v2 (After Architect), Workflow

### Community 50 - "service-integration-fullstack-to-reviewer.md"
Cohesion: 0.38
Nodes (5): FastAPI/Starlette TemplateResponse argument order fix, Workplan link silently lost bug (process_service_records without workplan_id), Optional workplan_name (migration step 17), db_migration step 16 rebuild before step 17 workplan_name, v0.5.0 release (service integration, health check, uv)

### Community 51 - "Service integration (#351) - fullstack to code-reviewer"
Cohesion: 0.15
Nodes (12): build_incident_service_entry(), get_effective_planned_date(), Effective planned date fallback, Bugs found and fixed, Key decisions, Known limitations, Next steps, Regression evidence, 2026-09-26 (+4 more)

### Community 52 - "Results"
Cohesion: 0.29
Nodes (7): 2026-09-25, first walkthrough, human, 2026-09-26, regression against the baseline database, Claude, 2026-09-27, second walkthrough, human, Preparation, Results, Scope, Test Protocol: Planned services, workplans and incidents

### Community 55 - "migrate_incident_links_to_services"
Cohesion: 0.25
Nodes (4): check_incidents_workplan_column_present(), insert_planned_service_for_migration(), migrate_drop_incident_workplan_column(), migrate_incident_links_to_services()

### Community 56 - "migrate_database"
Cohesion: 0.33
Nodes (3): find_database_file(), migrate_database(), prompt_for_db_path()

### Community 58 - "Agent Communication via Handovers"
Cohesion: 0.33
Nodes (6): Agent Communication via Handovers, Creating Handovers, Detailed Instructions, Handover Structure, Naming Convention, Reading Handovers

### Community 59 - "fullstack-developer.md"
Cohesion: 0.33
Nodes (5): Backend Patterns, Core Responsibilities, Frontend Patterns, Handover Content, Workflow

### Community 60 - "product-manager.md"
Cohesion: 0.33
Nodes (5): Boundaries, Core Responsibilities, Key Principle: You Are Interactive, Requirements Document, User Story Format

### Community 62 - "validateComponentThresholds"
Cohesion: 0.40
Nodes (5): addFormValidation(), clearValidationErrors(), showFieldError(), validateComponentThresholds(), validateQuickSwapForm()

### Community 63 - "Handovers Directory"
Cohesion: 0.33
Nodes (5): Creating Handovers, Directory Structure, Finding Handovers, Handovers Directory, Rules

### Community 65 - "architect.md"
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

### Community 79 - "docs-maintainer.md"
Cohesion: 0.50
Nodes (3): Core Responsibilities, Documentation Rules, Workflow

### Community 80 - "Code Style & Standards"
Cohesion: 0.50
Nodes (4): Code Style & Standards, Database, Frontend, Python (Backend)

### Community 82 - "cleanup"
Cohesion: 0.50
Nodes (4): cleanup(), handleCancel(), handleConfirm(), performBulkStatusChange()

### Community 83 - "renderPreview"
Cohesion: 0.50
Nodes (4): containsMarkdown(), renderPreview(), setInitialMode(), updateCheckboxInText()

### Community 84 - "initializeIncidentTable"
Cohesion: 0.67
Nodes (4): initializeIncidentTable(), setupIncidentSearch(), setupIncidentStatusFiltering(), updateIncidentVisibility()

### Community 85 - "handleOldComponentChange"
Cohesion: 0.67
Nodes (3): filterNewComponentsByType(), handleOldComponentChange(), updateQuickSwapCollectionWarning()

### Community 87 - "Testing Requirements"
Cohesion: 0.67
Nodes (3): Before Creating Handover, For fullstack-developer, Testing Requirements

## Ambiguous Edges - Review These
- `Version Script CI Workflow` → `Git Workflow Rules`  [AMBIGUOUS]
  .github/workflows/run_version_script.yml · relation: conceptually_related_to
- `conftest.py` → `Manual testing protocols approach`  [AMBIGUOUS]
  tests/README.md · relation: conceptually_related_to

## Knowledge Gaps
- **53 isolated node(s):** `Quick Swap Components`, `Strava OAuth Token Setup (Step 2)`, `Semantic Versioning (SemVer)`, `GitHub Project Board`, `Changelog Section` (+48 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 530 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **82 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `DatabaseManager` connect `DatabaseManager` to `Meta`, `.get_bike_details`, `database_manager.py`, `.read_latest_ride_record`, `.read_sum_distance_subset_rides`, `.write_component_lifetime_status`, `.write_component_service_status`, `.write_workplan`, `.write_delete_record`, `health-check-reviewer-to-docs-maintainer.md`, `.read_component`, `.read_single_bike`, `.read_single_component_type`, `.write_component_distance`, `.read_all_component_types`, `.read_all_components_objects`, `.read_all_workplans`, `.read_collection_by_component`, `.read_date_oldest_ride`, `.read_matching_rides`, `.read_recent_rides`, `.read_subset_component_history`, `.read_subset_components`, `.read_unique_bikes`, `.read_bike_id_recent_component_history`, `.write_collection`, `.write_incident_record`, `.read_incidents_by_workplan`?**
  _High betweenness centrality (0.205) - this node is a cross-community bridge._
- **Are the 9 inferred relationships involving `DatabaseManager` (e.g. with `Bikes` and `Collections`) actually correct?**
  _`DatabaseManager` has 9 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Quick Swap Components`, `Strava OAuth Token Setup (Step 2)`, `Semantic Versioning (SemVer)` to the rest of the system?**
  _53 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `main.py` be split into smaller, more focused modules?**
  _Cohesion score 0.06504065040650407 - nodes in this community are weakly interconnected._
- **Why does `BusinessLogic` connect `.process_service_records` to `scheduler.py`, `.create_history_record`, `.get_bike_details`, `utils.py`, `.recalculate_component_after_service_removal`, `.calculate_collection_status`, `validate_date_format`, `Code Reviewer -> Docs Maintainer Handover`?**
  _High betweenness centrality (0.118) - this node is a cross-community bridge._

### Low-confidence Hints
_AMBIGUOUS edges — the extractor was unsure. Verify before acting on these._

- **What is the exact relationship between `Version Script CI Workflow` and `Git Workflow Rules`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `conftest.py` and `Manual testing protocols approach`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._