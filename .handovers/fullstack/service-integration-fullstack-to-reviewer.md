# Service integration (#351) - fullstack to code-reviewer

**Status:** Complete, awaiting review
**Branch:** `feature/service-integration` off `dev`, not pushed
**Spec:** `docs/superpowers/specs/2026-09-18-service-integration-design.md`
**Plan:** `docs/superpowers/plans/2026-09-18-service-integration.md`

## What was built

Services became the unit of work. A service is Planned or Completed. Planned services carry no date, bike or distance and are invisible to component health until completed. Workplans group services and derive bike, components and progress from them. Incidents reach workplans through services. Covers #351, #345, #346, #348, #349, #350.

## Key decisions

- Planned services have no service date. An optional `planned_date` falls back to the workplan due date (`utils.get_effective_planned_date`)
- Workplans lost `workplan_affected_component_ids` and `workplan_affected_bike_id`; incidents lost `workplan_id`. All derived through services
- Completed services contribute the bike recorded on the service, planned services follow the component's current bike
- Retired components are locked: no planning, completing, editing or reverting. A component cannot be retired while it has planned services, checked upfront in quick swap and collection changes so neither leaves a partial result
- A service date may not fall after the completion date of a Done workplan. Workplan completion requires no remaining planned services, a valid date, not in the future, not before the latest service

## Files

- `backend/database_model.py`: services gain `status`, `incident_id`, `planned_date`; component_history gains `notes`; workplans and incidents lose their link fields
- `backend/db_migration.py:530-860`: steps 12-16, all idempotent. Retired components are not converted
- `backend/database_manager.py:235-330`: three health reads filter on Completed; new reads for planned services and for links through services
- `backend/utils.py:187-315`: `derive_workplan_context`, `get_effective_planned_date`, `get_planned_service_data_tuple`, reshaped workplan (14 fields) and incident (16 fields) tuples
- `backend/business_logic.py:2148-2600`: `create_planned_service`, `create_planned_services`, `complete_services`, `update_service_record` with revert, `recalculate_component_after_service_removal`, all rules in `validate_service_record`
- `backend/main.py`: `/add_planned_services` and `/complete_services` replace `/bulk_add_service_records`; service, workplan, incident and history routes updated
- `frontend/templates/`: new `modal_plan_services.html` and `modal_complete_services.html`; removed `modal_create_services_workplan.html` and `modal_link_incident.html`; all pages that show services, workplans or incidents updated
- `frontend/static/js/main.js`: new shared subsection "Plan and complete services modals"; about 560 lines of per-page dropdown code removed

## Reuse

Existing patterns kept: the bulk report dict and report modal, redirect-with-toast, loading modal, TomSelect setup, date picker helpers, `validate_date_format`, `process_service_records` and `update_component_service_status` untouched.

## Bugs found and fixed

- A component status change or a service deletion silently removed the workplan link from the newest completed service. Root cause: `process_service_records` was called without `workplan_id` at two call sites (`business_logic.py:1771` and the post-delete recalculation). Confirmed on production data: all 38 linked services would have lost their link
- The unfinished workplans table on component details filtered on a removed field, rendering empty with no error
- Separate commit, unrelated to #351: the app did not run on current FastAPI and Starlette. Page routes used the old `TemplateResponse` argument order, removed in Starlette 1.6, and required form fields rejected empty values, which broke uninstalling a component

## Testing

- 23 automated tests in `tests/`: migration (3), service status and validation (13), workplans and incidents (7). Run with `uv run pytest tests/`
- Production data check on a copy of `prod_db.sqlite`: migration applied and repeated with no further changes; full recalculation with master code and branch code on the same day gives identical values for 636 components, 1032 installation records, 17 bikes and 201 services. The only difference is the 38 workplan links the branch preserves
- Twelve page types load against migrated production data, no console errors. Plan, complete, service record, workplan and incident modals exercised in a browser
- Manual protocol for the human tester: `tests/test_protocol_services.md`, 52 cases

## Known limitations

- Migrated done workplans show no bike or components, since they have no services. Original names are appended to the description
- Incidents whose components did not match a service in their old workplan lost the link; the description records it
- Planning is disabled for resolved incidents by design
- Action buttons stack vertically in incident tables, as they did before this work

## Next steps

1. Human runs `tests/test_protocol_services.md`
2. @code-reviewer reviews the diff against `dev`
3. Version bump and changelog entry are already drafted under "Planned for v0.5.0" in README.md
