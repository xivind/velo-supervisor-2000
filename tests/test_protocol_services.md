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
| M1 | Existing services are completed | Open a component with service history | All previous services appear under "Service history", none under "Planned services" |OK|
| M2 | Planned workplans converted | Open a planned workplan that had affected components | Each component that still exists has a planned service, described as migrated from workplan |OK, and it seems like it did not create planned services for affected components that already had completed services. Please confirm in the code that this is how it works thats ok.|
| M3 | Retired components not converted | Open a planned workplan that had a retired component | No planned service for it, its name is noted in the description |Not able to verify. Didnt find any such cases. Please verify source code instead. |
| M4 | Done workplans preserved | Open a completed workplan | Bike and component names appear in the description as a migration note |OK, but two workplans marked as done also lists component. Probably bacause they had completed services. Please verify that this is correct. |
| M5 | Incident links rebuilt | Open an incident that was linked to a workplan | Either the workplan appears in the workplan column, or the description notes the previous link |OK, appears either in description or in workpla colummn. How is this supposed to work? The workplan column is populated automatically based on planned services linked to a workplan, is that it? |
| M6 | Migration is repeatable | Run the migration script a second time | Reports no migrations needed |OK |
| **Planning services** |
| P1 | Plan from component | Component details, "Plan services" | Modal opens with that component preselected |OK |
| P2 | Plan from bike | Bike details, "Plan services" | Installed components preselected, retired ones absent |OK |
| P3 | Plan from collection | Collection details, "Plan services" | The collection's components preselected |OK |
| P4 | Plan from incident | Incidents page, 🧑‍🔧 on an open incident | The incident's components preselected, no workplan selected |OK |
| P5 | Plan from workplan | Workplan details, "Plan services" | Workplan preselected and locked |OK, but Plan services modal in this case shows no components under Components. The other tests above shows the components. |
| P6 | One description, several components | Select three components, enter one description, save | Three planned services created, report lists all three |OK |
| P7 | Planned date optional | Leave planned date blank, with a workplan selected | Planned services show the workplan due date, marked "(due date)" |OK |
| P8 | Planned date used | Enter a planned date | That date shows instead of the due date |OK, but there is an issue here. The date picker wont be set a planned date in the future. This is the correct behavior for completing services, but not for planning. We must fix. |
| P9 | Short description refused | Enter fewer than 5 characters | Validation message, nothing saved |OK |
| P10 | Duplicate refused | Plan a service for a component already planned in the same workplan | Refused with a message naming the component |OK |
| P11 | Retired excluded | Open the components dropdown | Retired components are not listed |OK |
| P12 | Planned service does not affect status | Note a component's service status, plan a service, reload | Status, distance and next service unchanged |OK |
| **Completing services** |
| C1 | Complete one | Planned services table, ✅ on one row | Modal lists only that service, ticked |OK |
| C2 | Complete several | Workplan details, "Complete services" | All planned services listed and ticked, one date applies to all |OK |
| C3 | Note appended | Enter a note and complete | Note appended to each description, original text kept |OK |
| C4 | Status updates | Complete a service on an installed component | Component service status and distance recalculate |OK |
| C5 | Future date refused | Enter tomorrow's date | Validation message, nothing saved |OK |
| C6 | Date before installation refused | Enter a date before the component was first installed | Refused with the installation date in the message |OK |
| C7 | Retired component locked | A planned service on a retired component | Row shown disabled, cannot be completed |OK, I dont understand what you mean by row, but the button to plan a service or complete a service is disabled. Also confirmed that components cannot be retired if they have planned services. |
| C8 | Incident hint | Complete the last planned service of an open incident | Report says the incident can be closed |OK, confirmed. But I think its a bug (or something missing in our design) that there seem to be no links from incidents to services. |
| **Workplans** |
| W1 | Empty workplan | Create a workplan without services | Banner says no services planned yet, bike and components empty |OK |
| W2 | Derived context | Plan services on two components of one bike | Header shows that bike and both components |OK. But title is not correct when mixing components from more than one bike. We can solve that by making the title something the user edits, instead of computing it. Push back if you disagree. |
| W3 | Progress | Complete one of two services | Header shows 1 of 2, list page wheel shows 1/2 |OK, but the workplan page should show something more like the list page, and renaming the label to Services completed, and then a wheel or something. |
| W4 | Completion blocked | Try to complete a workplan with a planned service left | Refused, button disabled, edit modal refuses too |OK, both approaches blocked. Good! |
| W5 | Completion allowed | Complete all services, then complete the workplan | Green banner first, then workplan set to Done |OK, both checks out. |
| W6 | Completion date rules | Enter a date before the latest service, then a future date | Both refused with explanatory messages |OK. Date before latest service is blocked by backend. Date picker restritcs picking a future date. |
| W7 | Close incidents | Complete a workplan with the checkbox ticked | Linked open incidents set to Resolved with a note |OK, but the whole system linking incidents, workplans and services seems a bit fragile |
| W8 | Done banner | Open a completed workplan | Banner states it is completed, action buttons disabled (#350) |OK |
| W9 | Reopen | Edit a done workplan back to Planned | Workplan editable again, services untouched |OK, dont see any changes to services. |
| W10 | Delete guard | Delete a workplan that has services | Refused with the number of services |OK, worked. I was however able to delete the workplan even though incidents were still linked. Is that a problem? |
| **Incidents** |
| I1 | No workplan dropdown | Open the incident modal | No workplan field, no flaky dropdown (#345) |OK, no dropdown. But isnt it a problem that you cannot see linked services or workplan from the incident? What are your thoughts? |
| I2 | Workplan from incident | Incidents page, 📝 on an open incident | Workplan modal opens with the description carried over; on save, planned services are created for its components |OK |
| I3 | Derived link | After I2, reload the incidents page | The new workplan shows in the workplan column with a service count |OK, it even shows more workplans. Looks a bit messy, but probably would improve if we instead used user defined names for workplans. Could be shorter than it is now when its auto-generated. |
| I4 | Several workplans | Plan services for one incident into two workplans | Both listed in the workplan column |OK, see also comment above. Would it be better if that column just indicated if one or more workplans are linked, and then have links to the actual workplans in the modal?  |
| I5 | Resolved incident | Look at a resolved incident row | 📝 and 🧑‍🔧 are disabled |OK |
| I6 | Delete keeps services | Delete an incident that has services | Services remain, their incident link is cleared |OK |
| **Component status notes (#349)** |
| N1 | Note on status change | Change a component status with a note | Note shown in the installation history Notes column |OK, but should the modal that allows user to edit the date of an install record, also let the user edit the note, and not just the date? Its correct that the actual status itself cannot be edited. Then the user have to delete the record instead, to ensure data integrity. |
| N2 | Blank note | Change status without a note | Column shows "-" |OK |
| N3 | Note on quick swap | Quick swap with a note | Note appears on the installation record of both components |OK, but capton on the new notes field should be "Notes for status change", to distinguis it from the notes field above |
| N4 | Retire blocked | Retire a component that has planned services | Refused, naming the number of planned services |OK |
| N5 | Retire via quick swap blocked | Quick swap to Retired with planned services | Refused before anything changes, no new component created |OK |
| N6 | Retire via collection blocked | Set a collection to Retired where one component has planned services | Refused, no changes made, component named |OK. But when changing collection status, I think it should be possible there also to add a note about why the status changes. User must be informed (perhaps in text under the notes field) that the same note will be applied to all installation records. Also remember the caption on the field, should be: "Notes for status change" |
| **Service record modal** |
| S1 | New completed service | Component details, "New service" | Status Completed, service date shown |OK |
| S2 | New planned service | Switch status to Planned | Service date hidden, planned date shown, saving creates a planned service |OK, works, but maybe this should be modified to "Leave blank to use the due date of the workplan, if workplan exists. |
| S3 | Edit keeps links | Edit a service that has a workplan and an incident | Both preselected, still set after saving |OK, but as mentioned before we used to have clickable links, so the user could actually go to the workplan or incident in question. Maybe our data model is too flexible here. We need to discuss the cardinality between services, workplans and incidents. |
| S4 | Revert to planned | Edit a completed service, set status to Planned | Date, bike and distance cleared, component status recalculates as if deleted |OK, solid. |
| S5 | Workplan list | Open the workplan dropdown | Only planned workplans listed, plus any workplan already linked |OK |
| **Regression** |
| R1 | Component health | Compare a component's distance and status before and after the upgrade | Unchanged |Claude verifies against baseline db |
| R2 | Service history | Open a component with several services | Distances and running totals unchanged |Claude verifies against baseline db |
| R3 | Pages load | Visit every page: index, components, bikes, collections, workplans, incidents, component types, config, help | All load without errors |OK |
| R4 | Strava sync | Run a manual sync from the configuration page | Rides and distances update as before |Claude verifies against baseline db

## Addtional notes
- Planned services on page Bike details now has a button to complete services, in the table. This breaks with our conventions. I think it should be placed on top of the page, with the other buttons. Next to Plan services. Should be disabled if there are no services to complete.
- Same issue as the point above, except now on the Component details page. Should rather be placed next to Plan Services button
- On the Workplan page, in the table Planned services, the column named Planned for should rather be called "Due date" I think. Also, now it say "(due date)" in paranthesis, why is that? Isnt it better to have an emoji after the date, it the due date for for the planned service date is passed? Or am I thinking about that the wrong way? We could use the exclamation emoji for example? What do you think?
- In the Edit service record modal, under linked incident, it says: Optional. Open incidents that reference this component. But it to link to click? View should implement something similar as we have in the same modal for workplan, where there is a link to View the workplan. Also, the caption can give the impression that there can be several linked incidents, but I thought it could be only one?
- From the workplan details page, in the first card, we should remove that logic that shows the banner/ticket for Tasks. We dont need to handle that anymore. Is there any place that we also need to remove that?
- From the workplan details page, in the first card, on the service ticket, can we have the same wheel as we have on the workplans overview page (the one that shows all worplan). And then use the same 2/7. Lets make it consistent.
- Questions, on the workpl overview page, where the wheel show progress, can you confirm that it shows progress according to completed services vs planned services, and not referencing tasks?
- Instead of auto-generating names for the workplans, maybe it would be better if the user could actually enter a name for the workplan? Can save us some code for generating title, but would require a new field probably.
- Edit service record modal validates that date is required when completing a service. But this is only done backend. It should be validated frontend as well, so the user is not able to submit if completed date is empty.
- Isnt it a problem that there is no link between services and incident, since incidens are the new integration point? And also, isnt it a bit strange that the inciden modal shows no link to the workplan?
- Since its possible to add components from multiple bikes in a workplan, the planned and completed service table on that page (but only on that page I think) should show the bike the component is installed to in parantheis. If its an unassigned component, it should say (Not assigned) in paranthesis.
- I have written about the link from incidents to workplan before. It seems like whats happening is that components mentioned in the incident is indeed referenced in the workplan, but without the user being able to control. That might be OK. But the user should at least be made aware of this then creating the workplan based on incident. And maybe also the modal should show which components being transferred. I am not sure though, so lets think about this.
