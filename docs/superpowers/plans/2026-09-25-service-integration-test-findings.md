# Service integration (#351): findings from the manual test walkthrough

Source: user annotations in `tests/test_protocol_services.md`, walkthrough on 2026-09-25. Everything in the protocol passed functionally. This file lists what to change before the code review, grouped by type. Read the protocol for the user's exact wording.

Branch `feature/service-integration`, 19 commits, nothing pushed. Sandbox: `scratchpad/sandbox`, symlinks to the repo, its own config, migrated copy of `/home/xivind/code/prod_db_migrated.sqlite`. Baseline for comparisons: `/home/xivind/code/prod_db.sqlite`, unmigrated.

## A. Questions to answer from the code, no change expected

- **A1 (M2)** Confirm the migration skips components that already have a completed service in that workplan, and that this is intended
- **A2 (M3)** Confirm retired components get no planned service and are noted in the description. No such case existed in the data
- **A3 (M4)** Two done workplans list components. Confirm this is because they have completed services, which is correct
- **A4 (M5)** Explain how the workplan column on incidents is populated: through services linked to both the incident and a workplan
- **A5 (W10)** A workplan could be deleted while incidents were still linked. Decide whether that is a problem now that incident links run through services
- **A6 (R1, R2, R4)** Regression evidence against the baseline database, including a manual Strava sync

## B. Bugs to fix

- **B1 (P8)** The planned date picker refuses future dates. Correct when completing, wrong when planning. A planned date must allow the future
- **B2 (P5)** Opening the plan services modal from a workplan shows no components in the list. Other entry points show them
- **B3 (S2 area)** The service record modal requires a date when completing, but only the backend enforces it. Add the frontend check so submit is blocked

## C. Interface changes the user asked for

- **C1** Move "Complete services" from inside the planned services table to the button row at the top, next to "Plan services", on bike details and component details. Disabled when there is nothing to complete
- **C2** Workplan details, planned services table: rename "Planned for" to "Due date". Replace the "(due date)" marker with an emoji when the date has passed, for example an exclamation mark
- **C3** Workplan details, first card: remove the Tasks badge and the markdown checkbox progress. Check for other places that still use it
- **C4** Workplan details, first card: show service progress with the same wheel as the workplans list, same "2/7" format
- **C5** Workplan details, both service tables: show the bike each component is installed on in parentheses, or "(Not assigned)". Only on this page, since a workplan can span bikes
- **C6** Quick swap and collection status change: caption the notes field "Notes for status change". On collection status change, add the notes field and explain that the same note goes on every installation record
- **C7** Edit installation record modal: allow editing the note as well as the date. Status stays uneditable
- **C8** Service record modal: add a "View incident" link next to the incident dropdown, like the existing "View workplan" link. Reword the helper text so it does not imply several incidents

## D. Design questions to decide before coding

- **D1 (W2, I3, I4, and notes)** Replace generated workplan titles with a user-entered name. The generated title reads badly when a workplan spans bikes, and it makes the incidents workplan column long. Needs a new field, a form field, and a migration default. User leans yes
- **D2 (I1, C8, S3, and notes)** Visibility of links from an incident. Today an incident shows its workplans through services, but a service is not reachable from the incident, and the incident modal shows no links at all. Decide what an incident should display, and settle the cardinality between services, incidents and workplans
- **D3 (I4)** Incidents list, workplan column: show a simple indicator of one or more linked workplans, with the actual links inside the modal, rather than a list of long titles
- **D4 (notes, last item)** When creating a workplan from an incident, the components come across silently. Decide whether the modal should show which components will get planned services, and whether the user can choose

## Suggested order

1. Answer A1 to A5 from the code, they may change what C and D need
2. Decide D1 and D2, since both touch the data model
3. Fix B1 to B3
4. Apply C1 to C8
5. Rerun the automated tests and the regression comparison, A6
6. Update the protocol and the handover, then the code review
