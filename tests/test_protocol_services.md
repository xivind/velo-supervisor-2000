# Test Protocol: Planned services, workplans and incidents

Covers issue #351 and sub-issues #345, #346, #348, #349, #350.

## Scope

Services are either planned or completed. Planned services have no date and do not affect component status. Workplans group services and derive their bike and components from them. Incidents reach workplans through services.

## Preparation

1. Back up the database
2. Run `python3 backend/db_migration.py` and confirm steps 12 to 16 report changes
3. Start the application and clear the browser cache (Ctrl + Shift + R)
4. Note the number of services, workplans and incidents before starting

| Id | Test case | Steps | Expected result | Pass |
|---|---|---|---|---|
| **Migration** |
| M1 | Existing services are completed | Open a component with service history | All previous services appear under "Service history", none under "Planned services" | |
| M2 | Planned workplans converted | Open a planned workplan that had affected components | Each component that still exists has a planned service, described as migrated from workplan | |
| M3 | Retired components not converted | Open a planned workplan that had a retired component | No planned service for it, its name is noted in the description | |
| M4 | Done workplans preserved | Open a completed workplan | Bike and component names appear in the description as a migration note | |
| M5 | Incident links rebuilt | Open an incident that was linked to a workplan | Either the workplan appears in the workplan column, or the description notes the previous link | |
| M6 | Migration is repeatable | Run the migration script a second time | Reports no migrations needed | |
| **Planning services** |
| P1 | Plan from component | Component details, "Plan services" | Modal opens with that component preselected | |
| P2 | Plan from bike | Bike details, "Plan services" | Installed components preselected, retired ones absent | |
| P3 | Plan from collection | Collection details, "Plan services" | The collection's components preselected | |
| P4 | Plan from incident | Incidents page, 🧑‍🔧 on an open incident | The incident's components preselected, no workplan selected | |
| P5 | Plan from workplan | Workplan details, "Plan services" | Workplan preselected and locked | |
| P6 | One description, several components | Select three components, enter one description, save | Three planned services created, report lists all three | |
| P7 | Planned date optional | Leave planned date blank, with a workplan selected | Planned services show the workplan due date, marked "(due date)" | |
| P8 | Planned date used | Enter a planned date | That date shows instead of the due date | |
| P9 | Short description refused | Enter fewer than 5 characters | Validation message, nothing saved | |
| P10 | Duplicate refused | Plan a service for a component already planned in the same workplan | Refused with a message naming the component | |
| P11 | Retired excluded | Open the components dropdown | Retired components are not listed | |
| P12 | Planned service does not affect status | Note a component's service status, plan a service, reload | Status, distance and next service unchanged | |
| **Completing services** |
| C1 | Complete one | Planned services table, ✅ on one row | Modal lists only that service, ticked | |
| C2 | Complete several | Workplan details, "Complete services" | All planned services listed and ticked, one date applies to all | |
| C3 | Note appended | Enter a note and complete | Note appended to each description, original text kept | |
| C4 | Status updates | Complete a service on an installed component | Component service status and distance recalculate | |
| C5 | Future date refused | Enter tomorrow's date | Validation message, nothing saved | |
| C6 | Date before installation refused | Enter a date before the component was first installed | Refused with the installation date in the message | |
| C7 | Retired component locked | A planned service on a retired component | Row shown disabled, cannot be completed | |
| C8 | Incident hint | Complete the last planned service of an open incident | Report says the incident can be closed | |
| **Workplans** |
| W1 | Empty workplan | Create a workplan without services | Banner says no services planned yet, bike and components empty | |
| W2 | Derived context | Plan services on two components of one bike | Header shows that bike and both components | |
| W3 | Progress | Complete one of two services | Header shows 1 of 2, list page wheel shows 1/2 | |
| W4 | Completion blocked | Try to complete a workplan with a planned service left | Refused, button disabled, edit modal refuses too | |
| W5 | Completion allowed | Complete all services, then complete the workplan | Green banner first, then workplan set to Done | |
| W6 | Completion date rules | Enter a date before the latest service, then a future date | Both refused with explanatory messages | |
| W7 | Close incidents | Complete a workplan with the checkbox ticked | Linked open incidents set to Resolved with a note | |
| W8 | Done banner | Open a completed workplan | Banner states it is completed, action buttons disabled (#350) | |
| W9 | Reopen | Edit a done workplan back to Planned | Workplan editable again, services untouched | |
| W10 | Delete guard | Delete a workplan that has services | Refused with the number of services | |
| **Incidents** |
| I1 | No workplan dropdown | Open the incident modal | No workplan field, no flaky dropdown (#345) | |
| I2 | Workplan from incident | Incidents page, 📝 on an open incident | Workplan modal opens with the description carried over; on save, planned services are created for its components | |
| I3 | Derived link | After I2, reload the incidents page | The new workplan shows in the workplan column with a service count | |
| I4 | Several workplans | Plan services for one incident into two workplans | Both listed in the workplan column | |
| I5 | Resolved incident | Look at a resolved incident row | 📝 and 🧑‍🔧 are disabled | |
| I6 | Delete keeps services | Delete an incident that has services | Services remain, their incident link is cleared | |
| **Component status notes (#349)** |
| N1 | Note on status change | Change a component status with a note | Note shown in the installation history Notes column | |
| N2 | Blank note | Change status without a note | Column shows "-" | |
| N3 | Note on quick swap | Quick swap with a note | Note appears on the installation record of both components | |
| N4 | Retire blocked | Retire a component that has planned services | Refused, naming the number of planned services | |
| N5 | Retire via quick swap blocked | Quick swap to Retired with planned services | Refused before anything changes, no new component created | |
| N6 | Retire via collection blocked | Set a collection to Retired where one component has planned services | Refused, no changes made, component named | |
| **Service record modal** |
| S1 | New completed service | Component details, "New service" | Status Completed, service date shown | |
| S2 | New planned service | Switch status to Planned | Service date hidden, planned date shown, saving creates a planned service | |
| S3 | Edit keeps links | Edit a service that has a workplan and an incident | Both preselected, still set after saving | |
| S4 | Revert to planned | Edit a completed service, set status to Planned | Date, bike and distance cleared, component status recalculates as if deleted | |
| S5 | Workplan list | Open the workplan dropdown | Only planned workplans listed, plus any workplan already linked | |
| **Regression** |
| R1 | Component health | Compare a component's distance and status before and after the upgrade | Unchanged | |
| R2 | Service history | Open a component with several services | Distances and running totals unchanged | |
| R3 | Pages load | Visit every page: index, components, bikes, collections, workplans, incidents, component types, config, help | All load without errors | |
| R4 | Strava sync | Run a manual sync from the configuration page | Rides and distances update as before | |
