# docs-maintainer -> Human Handover

**Feature/Task:** Post-release fixes to v0.5.0 (#351), on master
**Date:** 2026-09-30
**Status:** Complete, ready to commit

## Context
Reviewer approved (finding 1 applied via `CSS.escape`, finding 2 rejected on purpose: `incident_reports_data` holds only OPEN incidents on bike/component details, so `get_service_incident_options` stays). 32 tests pass.

## Docs changes
None needed.
- No `CHANGELOG.md` exists. Release notes live in the README version list (written at release time). CI bumps `backend/current_version.txt` ("Update version number [skip ci]"). Neither touched.
- `modal_service_record.html` help texts stay correct: they describe what can be picked for a NEW link, and those rules are unchanged.
- `help.html` does not describe the dropdown contents. Nothing wrong or misleading.
- Optional: when cutting the next version, add a README bullet such as "Fixed the service dialog showing 'Linked (id)' instead of the name for linked Done workplans and Resolved incidents".

## Files to commit
- backend/business_logic.py
- backend/utils.py
- frontend/static/css/custom_styles.css
- frontend/static/js/main.js
- frontend/templates/modal_service_record.html
- frontend/templates/workplan_details.html
- tests/test_workplans_incidents.py
- .handovers/review/post-release-fixes-reviewer-to-docs-maintainer.md
- .handovers/documentation/post-release-fixes-docs-maintainer-to-human.md

graphify-out/: history shows it is committed on its own as "Auto graphify changes" (1a6a9c6), not with feature commits. Leave it out.

## Option A: one commit
```
Fix service modal links, incident deep link and progress wheel after v0.5.0

Show the name of linked Done workplans and Resolved incidents in the
service modal instead of "Linked (id)". All workplans and incidents are
rendered as options, and the ones that cannot be newly selected are
hidden. Incident options are now provided on bike details, workplan
details and incident reports as well.

Open the incident when the page is reached through an #incident- link,
use Done/Planned wording for linked services in the incident modal, and
fix the alignment and hover state of the completed progress wheel.

Refs #351

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
```

## Option B: three commits (main.js needs `git add -p`)
1. Names of linked items in the service modal
   - Whole files: business_logic.py, utils.py, modal_service_record.html, tests/test_workplans_incidents.py
   - main.js hunks: `setServiceModalSelect` (signature, comment, new forEach block), its call in `openServiceRecordModal`, its call with `currentComponentId`
```
Show names of linked workplans and incidents in the service modal

Render all workplans and incidents as options and hide the ones that
cannot be newly selected, so linked Done workplans and Resolved
incidents show their name instead of "Linked (id)". Provide incident
options on bike details, workplan details and incident reports too.

Refs #351

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
```
2. Incident deep link
   - main.js hunk: the `location.hash` / `#incident-` block at the end
```
Open the incident from the View incident link in the service modal

Refs #351

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
```
3. Wording and progress wheel
   - Whole files: custom_styles.css, workplan_details.html
   - main.js hunk: `'Done' : 'Planned'` wording
```
Fix progress wheel alignment and checkmark, use Done/Planned wording

Refs #351

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
```
Put the two handover files in the last commit.

## Double-check
- main.js has 3 fixes in several small hunks; pick by content and verify with `git diff --cached`.
- JS and CSS changed: clear browser cache after deploy (already in the v0.5.0 README notice).
- Out of scope, not documented: #356, #361.
