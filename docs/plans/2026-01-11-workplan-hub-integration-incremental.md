# Workplan Hub Integration - Incremental Implementation

**Date:** 2026-01-17 (Create Services modal complete)

---

## Instruction to Claude for using this file

- This file is the guidance for implementing the feature for workplan integration with incident and services
- When claude is asked to assist in making a new feature, and this file is read, Claude should also read the directives for architect, ux-designer, fullstack-developer and database-expert and act according to these
- For each item, Claude should ask for confirmation on what changes to apply
- For each item, Claude should make sure to act with this document as context. If Claude needs more information, it should ask the user.
- After each level three section (###) is completed, Claude should update the *Status*: field with a short description of whats done
- Claude should keep the descriptions and all texts added or edited to this document super short
- If Claude discovers more tasks that are required, these should be added in the appropriate section
- If Claude discovers issues that cannot be easily resolved, these should be added to the section Issues requiring clarification
- Claude should update the **Date:** field each time this file is updated
- Claude should not commit anything, unless explicitly asked to do so

---

## Purpose

The purpose of this feature is to integrate incidents, workplans, and services so they are no longer siloed as they are today, but work together to support users in their maintenance work.

The main flow is that users create incidents as they happen. Incidents may be added to workplans. And then from workplans, services can be created.

But still, this is an opt-in workflow, so users must be able to work independently with both incidents, workplans, and services.

---

## Frontend changes - html pages

### component_overview.html
[] The New workplan and New incident buttons on top of the page should continue to work as before.

*Status:*
*Testing:* TBD

### component_details.html
[] The New workplan and New incident buttons on top of the page should continue to work as before.
[] On the services table, add a column after Mileage, called Workplan. It should display the name of the associated workplan. The name of the workplan should be clickable, and navigate to `/workplan_details/{workplan_id}`. If there is no workplan assigned, show "-"
[] The table for open incidents should have a similar functionality
[] The table for unfinished workplans should no longer have an edit button that brings up the modal to edit workplans. Instead the entire row should be clickable and take the user to the workplan_details.html page for the workplan in question

*Status:*
*Testing:* TBD

### bike_details.html
[] The New workplan and New incident buttons on top of the page should continue to work as before
[] On the table for open incidents, add a column after Days open, called Workplan. It should display the name of the associated workplan. The name of the workplan should be clickable, and navigate to `/workplan_details/{workplan_id}`. If there is no workplan assigned, show "-"
[] The table for unfinished workplans should no longer have an edit button that brings up the modal to edit workplans. Instead the entire row should be clickable and take the user to the workplan_details.html page for the workplan in question

*Status:*
*Testing:* TBD

### workplans.html
[X] The New workplan button should continue to work as before
[X] The table for all workplans should no longer have an edit button that brings up the modal to edit workplans. Instead the entire row should be clickable and take the user to the workplan_details.html page for the workplan in question. However, the component names and bike names on the row should still be clickable, as they are today.

*Status:* Removed edit button, kept delete button, added event.stopPropagation() to bike and component links
*Testing:* TBD

### incident_reports.html
[] The New incident button should continue to work as before
[] On the table for all incidents, add a column after Days open, called Workplan. It should display the name of the associated workplan. The name of the workplan should be clickable, and take the user to the workplan_details.html page for the workplan in question. If there is no workplan assigned, show "-"
[] Add a new action button, to the left of the edit button, with this emoji 📝. This button should bring up the modal to create a new workplan and prefill it with info from the incident. We will discuss at implementation time what info to prefill. On submit, the workplan will be created, and then the incident will be updated with the workplan_id with the newly created workplan. According to patterns elsewhere, this button should always be visible, but it should be disabled if the incident is already assigned to a workplan, meaning that the workplan_id field of the incident is not none

*Status:*
*Testing:* TBD

### workplan_details.html (new page)
[X] Create this page and base it on the layout and looks of the collection_details.html page.
[X] There should be four buttons on top (in this order): 1. Edit workplan, 2. Create services, 3. Complete workplan, 4. Delete
[X] Create services button opens modal_create_services_workplan.html with all affected components pre-selected. User can then select one or more components to create services for.
[X] Complete workplan button should be disabled when workplan status is "Done". Otherwise it should be enabled (even if not all components are serviced).
[X] The color of the header on the top most tile should be using the same palette and according to the status of the collections, see workplans.html for more details. There should be a legend just above the header, explaining the colors.
[X] In the header, below the workplan name, we should have badges for size (use the same palette as other places for workplan size)
[X] The badges in the content field of the topmost card should contain the following info (in this order): Due date, Affected bike, Affected Components, Description
[X] If all components associated with the workplan has a service, that is linked to the workplan, a banner should display, with green color (probably bootstrap success), that informs the user that workplan can be closed by clicking Complete workplan. This should also close any incidents linked to the workplan.
[X] Below the banner, it should be a table listing incidents that references the current workplan. This table should have the same appearance as the table on the incident_reports.html page, however it should not have the search functionality. It should however have the same actions button for each row (edit incident + delete incident). In contrast to the incident table on bike details and component details, that only shows open incidents, this one should show all incidents connected to the workplan, regardless of the incident status.
[X] Below the incident table, there should be a table listing services that references the workplan. This table should have the same appearance as the services table on the component_details.html page, however it should not have a workplan column, since that context is already established. It should however have the same actions button for each row (edit service + delete service).

*Status:* Page created with all required elements following collection_details.html layout pattern
*Testing:* TBD

## Frontend changes - modal changes

### modal_workplan_record.html
[X] Remove the workplan id and move it to the topmost card on the workplan details plan instead. Except for this, no change required in this modal.

*Status:* Workplan ID display removed from modal bottom
*Testing:* TBD

### modal_incident_record.html
[] Add a single value dropdown box below the Description field, to allow the user to link the incident to a workplan. We must discuss how the user is supposed to search for such workplans.

*Status:*
*Testing:* TBD

### modal_service_record.html
[] Add a single value dropdown box below the Description field, to allow the user to link the service to a workplan. We must discuss how the user is supposed to search for such workplans.

*Status:*
*Testing:* TBD

### modal_complete_workplan.html
[] Make a modal that allows the user to comlpete a workplan and associated incidents. We must discuss implementation together.

*Status:*
*Testing:* TBD

### modal_create_services_workplan.html
[X] Make a modal that allows the user to create services for a give component. We must discuss implementation together.

*Status:* Complete - checkbox list, yellow banner, validation, loading/report modals working
*Testing:* Manual testing successful


## Frontend changes - other files

### main.js
**IMPORTANT**
- Do not make API calls from javascript. Data required should always be access through payload sent from the backend
- Pay attention to the use of headers in main.js and make sure to use appropriate headers and place new js code in the right places

[X] Make changes as necessary to support the changes in pages and modals
[X] Added clickable-row handler in Workplan page functions section (line 4710-4723) to navigate to workplan_details page
[X] Removed edit button handlers from workplans.html page section
[X] Removed reference to workplan-id-display element
[X] Added edit button handler in workplan_details page section
[X] Added bulk service creation handler in workplan_details page section
[X] Moved forceCloseLoadingModal to global scope for availability across all pages
[X] Cleaned up verbose logging and matched existing code patterns

*Status:* Complete - all handlers working, code cleaned and production-ready
*Testing:* Manual testing successful - bulk service creation, loading/report modals working

---

## Backend changes

### database_model.py
[X] Services and Incidents table need a new field: workplan_id = CharField()

*Status:* Field already added in both tables and the migration script is also updated.
*Testing:* TBD

### database_manager.py
[X] Methods already exist: read_single_workplan, read_incidents_by_workplan, read_services_by_workplan

*Status:* Methods confirmed available in database_manager
*Testing:* TBD

### main.py
[X] Route /workplan_details/{workplan_id} already exists and calls business_logic.get_workplan_details
[X] Route /bulk_add_service_records implemented with parameters: workplan_id, component_ids, service_date, service_description

*Status:* Complete - workplan_details route functional, bulk service creation route implemented
*Testing:* TBD

### business_logic.py
[X] Implemented get_workplan_details method - fetches workplan, incidents, services, checks service completion status
[X] Added bikes_data and all_components_data to payload for modal dropdowns
[X] Added workplan_components_info to payload for bulk service creation modal
[X] Implemented bulk_create_service_records method - creates multiple service records with same date/description
[] Add check in delete_record to prevent workplans from being deleted if they have linked incidents or services

*Status:* Complete - get_workplan_details with full payload, bulk_create_service_records implemented
*Testing:* TBD

### utils.py
[] Improve function generate_incident_title to gracefully handle markdown syntax if detected

*Status:*
*Testing:* TBD

---

## Issues requiring clarification
[] Add as needed