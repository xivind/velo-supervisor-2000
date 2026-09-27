# Technical debt

Known weaknesses in the codebase, written down so they can be prioritised instead of rediscovered. Each item says what the risk is and what fixing it would involve. Ordered by risk, highest first.

Assessed 2026-09-20, after the service integration work for issue #351.

## 1. Thin automated test coverage

**What:** `tests/` holds 25 tests, added with issue #351. They cover the migration, planned and completed services, the validation rules and the workplan and incident derivations. Everything else is covered only by manual protocols.

**Risk:** `business_logic.py` is 3397 lines of arithmetic-heavy code that decides distances, service intervals and component status. A released bug went unnoticed for months: a component status change or a service deletion silently removed the workplan link from the newest service, because `process_service_records` was called without the workplan at two call sites.

**Fix:** grow coverage around the distance and status paths first, since those are hardest to verify by eye. Useful cases: a component moved between several bikes, components with time-based intervals, distance offsets, and a component with no installation history. The pattern to follow is in `tests/conftest.py`, which copies `template_db.sqlite` into a temporary directory.

## 2. Page payloads are positional tuples

**What:** templates unpack rows by position, for example the incident tuple with 17 fields and the workplan tuple with 14, built in `utils.py`.

**Risk:** renaming or reordering a field breaks pages, and Jinja renders an unknown name as empty rather than raising. During #351 the incidents page crashed on an unpack, and the unfinished workplans table on component details silently rendered empty because its filter used a removed field name. Neither produced an error in the log.

**Fix:** return dictionaries from the tuple builders in `utils.py` and access fields by name in templates. This can be done one builder at a time. Enabling Jinja's strict undefined mode would turn the silent case into a loud one. This could also apply to other payloads. Dicts should always be used to return payloads, instead of tuples. Claude must push back if this is not advisable.

## 3. Two very large files

**What:** `frontend/static/js/main.js` is 6337 lines and `backend/business_logic.py` is 3397 lines.

**Risk:** both are internally consistent, but a change requires locating code by line number rather than reading the file. That raises the chance of editing the wrong block.

**Fix:** main.js is organised into page sections already, so splitting it into one file per page plus a shared file would be mostly mechanical, at the cost of extra script tags in `base.html`. For business logic, the natural seams are services, components and collections.

## 4. Long functions

**What:** the longest are `get_component_details` at 186 lines, `update_component_service_status` at 160, `delete_record` at 133, `process_service_records` at 126 and `quick_swap_orchestrator` at 106.

**Risk:** they are hard to test in pieces, and the payload builders mix data gathering with formatting.

**Fix:** the payload builders are the easy win, since each block that builds one table could become its own function. The distance functions should be left alone until tests cover them properly, see item 1.

## 5. Duplication in templates and JavaScript

**What:** the block that formats the current date as `YYYY-MM-DD HH:MM` appears 13 times in main.js, three of them added with #351. The progress wheel markup is repeated in four templates. The incident table markup exists in four templates with small variations. Two TODO markers in main.js, at the quick swap and install component validation, ask for the not-in-future date check to be standardised, and #351 added three more copies of that check. A `window.escapeHtml` helper was added in the #351 second round for `renderIncidentServices`, the first `innerHTML` site to carry genuinely free-text, user-authored data (a workplan name). Eight other `innerHTML` template-literal sites in main.js still interpolate values unescaped, unchanged from before this branch.

**Risk:** changes get applied to some copies and not others. For the `innerHTML` sites, values that later become free text (as `workplan_name` did) start out unescaped until someone remembers to fix that one spot.

**Fix:** one helper in main.js for the formatted current date, and one for the not-in-future check the TODOs refer to. A Jinja macro for the progress wheel and for the incident row. Apply `window.escapeHtml` at the eight remaining `innerHTML` sites, as each is next touched.

## 6. Unpinned dependencies

**What:** `requirements.txt` lists names without versions, and the Docker image installs whatever is current at build time. `pyproject.toml` sets floors but the container does not use the lock file.

**Risk:** a rebuild can change behaviour without a code change. This already happened: the app stopped rendering pages entirely on Starlette 1.6, and required form fields began rejecting empty values on FastAPI 0.141. Both were fixed in the #351 branch, but the exposure remains.

**Fix:** pin versions in `requirements.txt`, or build the image from `uv.lock`. Either way, upgrades become a deliberate change with its own commit.

## 7. Smaller items

- Spelling in user-facing messages and docstrings. The 21 occurrences of "occured" were corrected on 2026-09-27, "receords" no longer exists in the code
- Lint noise: trailing whitespace, lines over 100 characters, missing final newlines
- `validate_service_record` now takes seven parameters, which is at the edge of readable
- `derive_workplan_context` (`backend/utils.py`) runs twice per page render on `bike_details`, `component_details`, `incident_reports` and `workplan_details`: once inside `get_workplan_names_dict` for title resolution, again inside `get_workplan_data_tuple` for the workplans table. Matches the approved design, and the #351 production regression run showed no problem at current scale (a few hundred services). Follow-up only: compute the context once per render and reuse it

## Cleared

- Debug leftovers, removed 2026-09-20: a `print` of the table selector in `delete_record`, two stored but unused submit handlers in the incident and workplan form initialisers, three `console.log` calls on the configuration page, and nine commented-out `console.log` lines. Found by sweeping for `print(`, `console.log(`, `TODO` and orphaned variables, which is worth repeating occasionally
