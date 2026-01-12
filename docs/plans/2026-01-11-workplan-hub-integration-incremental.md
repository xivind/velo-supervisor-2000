# Workplan Hub Integration - Incremental Implementation

**Date:** 2026-01-11

---

## Purpose

The purpose of this feature is to integrate incidents, workplans, and services so they are no longer siloed as they are today, but work together to support users in their maintenance work.

The main flow is that users create incidents as they happen. Incidents may be added to workplans. And then from workplans, services can be created.

But still, this is an opt-in workflow, so users must still be able to work independently with both incidents, workplans, and services.

---

## Page Changes

### component_overview.html
[] The New workplan and New incident buttons on top of the page should contiue to work as before.
*Status:*

### component_details.html
[] The New workplan and New incident buttons on top of the page should contiue to work as before.
[] On the services table, add a column after Mileage, called Workplan. It should display the name of the associated workplan. The name of the workplan should be clickable, and take the user to the workplan_details.html page for the workplan in question. If there is no workplan assigned, show "-"
[] The table for open incidents should have a similar functionality
[] The table for unfinished workplans should no longer have an edit button that brings up the modal to edit workplans. Instead the entire row should be clickable and take the user to the workplan_details.html page for the workplan in question
*Status:*

### bike_details.html
[] The New workplan and New incident buttons on top of the page should contiue to work as before
[] On the table for open incidents, add a column after Days open, called Workplan. It should display the name of the associated workplan. The name of the workplan should be clickable, and take the user to the workplan_details.html page for the workplan in question. If there is no workplan assigned, show "-"
[] The table for unfinished workplans should no longer have an edit button that brings up the modal to edit workplans. Instead the entire row should be clickable and take the user to the workplan_details.html page for the workplan in question
*Status:*

### workplans.html
[] The New workplan button should contiue to work as before
[] The table for all workplans should no longer have an edit button that brings up the modal to edit workplans. Instead the entire row should be clickable and take the user to the workplan_details.html page for the workplan in question. However, the component names and bike names on the row should still be clickable, as they are today.
*Status:*

### incident_reports.html
[] The New incident button should continue to work as before
[] On the table for all incidents, add a column after Days open, called Workplan. It should display the name of the associated workplan. The name of the workplan should be clickable, and take the user to the workplan_details.html page for the workplan in question. If there is no workplan assigned, show "-"
[] Add a new action button, to the left of the edit button, with this emoji 📝. This button should bring up the modal to create a new workplan and prefill it with info from the incident. We will discuss at implementation time what info to prefill. On submit, the workplan will be created, and then the incident will be updated with the workplan_id with the newly created workplan. According to patterns elsewhere, this button should always be visible, but it should be disabled if the incident is already assigned to a workplan, meaning that the workplan_id field of the incident is not none

### workplan_details.html (new page)
[] Create this page and base it on the layout and looks of the collection_details.html page. 
[] There should be four buttons on top (in this order): 1. Edit workplan, 2. Create services, 3. Complete workplan, 4. Delete
[] The color of the header on the top most tile should be using the same palette and according to the status of the collections, see workplans.html for more details. There should be a legend just above the header, explaining the colors.
[] Tag content...
[] Table with incidents (edit button + disconnect)
[] Table with services (edit button + disconnect)
[] ... anything else..?
*Status:*

## Modal changes

### modal_workplan_record.html

### modal_incident_record.html

### modal_service_record.html

### modal_complete_workplan.html

### modal_create_services_workplan.html

--

## Backend changes

### database_model.py

### database_manager.py

### main.py

### business_logic.py