# Workplan Hub Integration - Incremental Implementation

**Date:** 2026-01-25 (CSS refactoring: Moved all inline styles to CSS classes in custom_styles.css, 22 HTML files updated)

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
[X] The New workplan and New incident buttons on top of the page should continue to work as before.
[X] Added data-workplans attribute to "New incident" button for workplan dropdown functionality

*Status:* Complete - Buttons working, workplan dropdown now functional on this page
*Testing:* Manual testing successful

### component_details.html
[X] The New workplan and New incident buttons on top of the page should continue to work as before.
[X] On the services table, add a column after Mileage, called Workplan. It should display the name of the associated workplan. The name of the workplan should be clickable, and navigate to `/workplan_details/{workplan_id}`. If there is no workplan assigned, show "-"
[X] The table for open incidents should have a similar functionality
[X] The table for unfinished workplans should no longer have an edit button that brings up the modal to edit workplans. Instead the entire row should be clickable and take the user to the workplan_details.html page for the workplan in question

*Status:* Complete - Workplan column added to services and incidents tables with clickable links, workplan rows now clickable (edit button removed), updated business_logic.py to include workplan_id/workplan_name in tuples
*Testing:* TBD

### bike_details.html
[X] The New workplan and New incident buttons on top of the page should continue to work as before
[X] On the table for open incidents, add a column after Days open, called Workplan. It should display the name of the associated workplan. The name of the workplan should be clickable, and navigate to `/workplan_details/{workplan_id}`. If there is no workplan assigned, show "-"
[X] The table for unfinished workplans should no longer have an edit button that brings up the modal to edit workplans. Instead the entire row should be clickable and take the user to the workplan_details.html page for the workplan in question

*Status:* Complete - Workplan column added to incidents table with clickable links, workplan rows now clickable (edit button removed), updated business_logic.py get_bike_details to include workplan_id/workplan_name
*Testing:* TBD

### workplans.html
[X] The New workplan button should continue to work as before
[X] The table for all workplans should no longer have an edit button that brings up the modal to edit workplans. Instead the entire row should be clickable and take the user to the workplan_details.html page for the workplan in question. However, the component names and bike names on the row should still be clickable, as they are today.

*Status:* Removed edit button, kept delete button, added event.stopPropagation() to bike and component links
*Testing:* TBD

### incident_reports.html
[X] The New incident button should continue to work as before
[X] On the table for all incidents, add a column after Days open, called Workplan. It should display the name of the associated workplan. The name of the workplan should be clickable, and take the user to the workplan_details.html page for the workplan in question. If there is no workplan assigned, show "-"
[X] Add a new action button, to the left of the edit button, with this emoji 📝. This button should bring up the modal to create a new workplan and prefill it with info from the incident. We will discuss at implementation time what info to prefill. On submit, the workplan will be created, and then the incident will be updated with the workplan_id with the newly created workplan. According to patterns elsewhere, this button should always be visible, but it should be disabled if the incident is already assigned to a workplan, meaning that the workplan_id field of the incident is not none
[X] Search function now includes workplan column
[X] Sorting support added for workplan column (case-insensitive alphabetical)

*Status:* Complete - Workplan column added, 📝 button creates workplan from incident with prefilled bike/components/description, automatic linking on creation, search/sort support added
*Testing:* Manual testing successful - workplan creation and linking verified

### workplan_details.html (new page)
[X] Create this page and base it on the layout and looks of the collection_details.html page.
[X] There should be four buttons on top (in this order): 1. Edit workplan, 2. Create services, 3. Complete workplan, 4. Delete
[X] Create services button opens modal_create_services_workplan.html with all affected components pre-selected. User can then select one or more components to create services for.
[X] Complete workplan, Link incident, and Create services buttons should be disabled when workplan status is "Done". Otherwise enabled (even if not all components are serviced).
[X] The color of the header on the top most tile should be using the same palette and according to the status of the collections, see workplans.html for more details. There should be a legend just above the header, explaining the colors.
[X] In the header, below the workplan name, we should have badges for size (use the same palette as other places for workplan size)
[X] The badges in the content field of the topmost card should contain the following info (in this order): Due date, Affected bike, Affected Components, Description
[X] If all components associated with the workplan has a service, that is linked to the workplan, a banner should display, with green color (probably bootstrap success), that informs the user that workplan can be closed by clicking Complete workplan. This should also close any incidents linked to the workplan.
[X] Below the banner, it should be a table listing incidents that references the current workplan. This table should have the same appearance as the table on the incident_reports.html page, however it should not have the search functionality. It should however have the same actions button for each row (edit incident + delete incident). In contrast to the incident table on bike details and component details, that only shows open incidents, this one should show all incidents connected to the workplan, regardless of the incident status.
[X] Below the incident table, there should be a table listing services that references the workplan. This table should have the same appearance as the services table on the component_details.html page, however it should not have a workplan column, since that context is already established. It should however have the same actions button for each row (edit service + delete service).
[X] Service table rows are now clickable (except buttons) to navigate to component_details page

*Status:* Page created with all required elements, button disable logic for completed workplans (Link incident, Create services, Complete workplan)
*Testing:* TBD

## Frontend changes - modal changes

### modal_workplan_record.html
[X] Remove the workplan id and move it to the topmost card on the workplan details plan instead. Except for this, no change required in this modal.

*Status:* Workplan ID display removed from modal bottom
*Testing:* TBD

### modal_incident_record.html
[X] Add a single value dropdown box below the Description field, to allow the user to link the incident to a workplan. We must discuss how the user is supposed to search for such workplans.
[X] Added redirect_url hidden field for proper routing on edit
[X] Added data-workplans attribute support to "New incident" buttons on bike_details, component_details, component_overview
[X] Added data-redirect-url to edit buttons on incident_reports, bike_details, component_details, workplan_details

*Status:* Complete - Dropdown working on all pages, routing fixed: CREATE always goes to workplan_details (if linked) or incident_reports, EDIT returns to source page
*Testing:* Manual testing successful - dropdown populates from all pages, edit routing verified on all pages

### modal_service_record.html
[X] Add a single value dropdown box below the Description field, to allow the user to link the service to a workplan. We must discuss how the user is supposed to search for such workplans.
[X] Added redirect_url hidden field for proper routing on edit
[X] Added data-redirect-url to edit buttons on component_details and workplan_details

*Status:* Complete - Dropdown working, routing fixed: CREATE single service always goes to component_details, CREATE bulk services stays on workplan_details, EDIT returns to source page
*Testing:* Manual testing successful - routing verified on both pages

### modal_complete_workplan.html
[X] Make a modal that allows the user to complete a workplan and associated incidents. Modal stub was reviewed and enhanced
[X] Include a checkbox that also allows users to close linked incidents that are open. Incidents get resolution date matching workplan completion date
[X] Resolution notes for incidents: "Closed from workplan with description: {workplan_description or 'None'} (workplan id: {workplan_id})"
[X] Muted help text explaining checkbox behavior, visible always but disabled if no open incidents
[X] Toast message shown on completion (standard redirect pattern used by existing /update_workplan endpoint)
[X] JavaScript handler added at line 5787-5861 in main.js, complete workplan button data attributes added to workplan_details.html
[X] Updated business_logic.py (lines 2839-2841) to construct auto-generated resolution notes for incidents

*Status:* Complete - modal, backend, JavaScript handlers working, checkbox disabled when no open incidents
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
[X] Added service workplan dropdown population (lines 3573-3726) with component filtering, works on both component_details and workplan_details pages
[X] Added workplan column to incident search (lines 4617, 4624)
[X] Added sorting support for workplan column (case 7, lines 4541-4546) with case-insensitive alphabetical sorting
[X] Updated incident edit handler to capture and populate redirect_url from data-redirect-url attribute
[X] Updated service edit handler to capture and populate redirect_url from data-redirect-url attribute
[X] Added redirect_url clearing in new incident/service handlers

*Status:* Complete - all handlers working, routing logic implemented for both incidents and services
*Testing:* Manual testing successful - all modal routing verified on all pages

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
[X] Updated /add_service_record - now always redirects to component_details (removed workplan_id redirect logic)
[X] Updated /update_service_record - added redirect_url parameter support, falls back to component_details if not provided
[X] Route /update_incident_record already supports redirect_url parameter

*Status:* Complete - all routing logic implemented for incidents and services
*Testing:* Manual testing successful - all redirects working as specified

### business_logic.py
[X] Implemented get_workplan_details method - fetches workplan, incidents, services, checks service completion status
[X] Added bikes_data and all_components_data to payload for modal dropdowns
[X] Added workplan_components_info to payload for bulk service creation modal
[X] Implemented bulk_create_service_records method - creates multiple service records with same date/description
[X] Updated get_component_details - added workplan_id to service_history_data tuple, added workplan_id/workplan_name to incident_reports_data tuple
[X] Updated get_bike_details - added workplan_id/workplan_name to incident_reports_data tuple
[X] Updated get_component_overview - added workplans_data to payload for incident modal dropdown functionality
[X] Add check in delete_record to prevent workplans from being deleted if they have linked incidents or services

*Status:* Complete - all payload updates implemented, deletion checks in place
*Testing:* Manual testing successful - workplan dropdown works from component_overview page

### utils.py
[] Improve function generate_incident_title to gracefully handle markdown syntax if detected. Fix for workplan_title_generator as well

*Status:*
*Testing:* TBD

---

## Code Quality Improvements

### CSS Refactoring - Move inline styles to CSS classes
[X] Created CSS classes in custom_styles.css for common inline styles
[X] Updated all HTML templates to use CSS classes instead of inline styles
[X] Updated JavaScript in main.js to use classList instead of style.display
[X] Preserved dynamic inline styles (progress bars, CSS custom properties)
[X] Fixed legend badge rendering by adding border-radius: 50% to CSS (removed Bootstrap badge class)

**CSS classes added:**
- .legend-badge - for status legend indicators
- .legend-badge-table - for table status indicators with margin
- .clickable - for elements with pointer cursor
- .badge-info - for info badges with line-height
- .scrollable-checkboxes - for modal checkbox containers
- .scrollable-logs - for log display container
- .error-image - for error page image

**Files updated (24 files):**
- Legend badges: workplan_details.html, collection_details.html, index.html, component_overview.html
- Info badges: workplan_details.html, component_details.html, collection_details.html, bike_details.html
- Clickable: component_details.html, workplans.html, bike_details.html, component_overview.html
- Display none → .d-none: modal_create_services_workplan.html, modal_service_record.html, modal_incident_record.html, modal_update_component_status.html, modal_quick_swap.html (updated with swap-bike-context), modal_install_component.html, modal_link_incident.html, modal_workplan_record.html (updated with workplan_preview_mode)
- Scrollable: modal_create_services_workplan.html, config.html
- Error image: error.html
- JavaScript updates: main.js (11 elements updated to use classList: collection-warning-banner, create_new_form, no_matching_components_warning, collection_preview, serviceViewWorkplanLink, incidentViewWorkplanLink, multipleSelectionBanner, noIncidentsWarning, workplan_edit_mode, workplan_preview_mode, swap-bike-context)

*Status:* Complete - all inline styles moved to CSS classes, JavaScript updated to use classList (11 elements), guideline "all styling goes in custom_styles.css" now followed
*Testing:* TBD - need to retest: workplan description preview/edit toggle, quick swap bike context display

---

## Issues requiring clarification
[] Add as needed