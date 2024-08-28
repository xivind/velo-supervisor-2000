#!/usr/bin/env python3
"""Main backend for velo supervisor 2000"""


from strava import Strava
from peewee_connector import ReadTables, ModifyTables, ReadRecords, ModifyRecords, MiscMethods
import argparse
import logging
import uvicorn
from time import sleep
from fastapi import FastAPI, HTTPException, Request, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from typing import Optional
from pathlib import Path
from datetime import datetime
from collections import Counter
import traceback


#def read_parameters():
#    """
#    Function for reading variables for the script,
#    for more on argparse, refer to https://zetcode.com/python/argparse/
#    """
#    parser = argparse.ArgumentParser(
#        description="Configuration parameters")
#    parser.add_argument("--oauth_file", type=str,
#                        help="File with oauth user data", required=True)
#    args = parser.parse_args()
#    # Include file path to db as argument, also include in git-ignore

#    return args





#PARAMETERS = read_parameters()
#strava = Strava(PARAMETERS.oauth_file)
read_tables = ReadTables()
modify_tables = ModifyTables()
read_records = ReadRecords()
modify_records = ModifyRecords()
misc_methods = MiscMethods()
#Initiate more classes

app = FastAPI()
templates = Jinja2Templates(directory="../frontend/templates")
app.mount("/static", StaticFiles(directory="../frontend/static"), name="static")
#template_dir = Path("../frontend/templates")

# Function to handle errors
def render_error_page(request: Request, status_code: int, error_message: str):
    return templates.TemplateResponse("error.html", {
        "request": request,
        "status_code": status_code,
        "error_message": error_message
    })


@app.get("/error", response_class=HTMLResponse)
async def error_page(request: Request):
    return render_error_page(request, 500, "Internal Server Error")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Endpoint for index / landing page"""
    bikes = read_tables.read_bikes()
    bikes_data = [(bike.bike_name,
                  bike.bike_id,
                  bike.bike_retired,
                  bike.service_status,
                  int(bike.total_distance)) for bike in bikes]

    template_path = "index.html"
    return templates.TemplateResponse(template_path, {"request": request, "bikes_data": bikes_data})

@app.get("/component_types_overview", response_class=HTMLResponse)
async def component_types_overview(request: Request):
    """Endpoint for component types page"""    
    component_types = read_tables.read_component_types()
    component_types_data = [(component_type.component_type,
                             component_type.expected_lifetime,
                             component_type.service_interval) for component_type in component_types]

    template_path = "component_types.html"
    return templates.TemplateResponse(template_path, {"request": request, "component_types_data": component_types_data})

@app.post("/component_types_overview/modify", response_class=HTMLResponse)
async def modify_component_type(
    component_type: str = Form(...),
    expected_lifetime: Optional[int] = Form("Not defined"),
    service_interval: Optional[int] = Form("Not defined")):
    """Endpoint to modify component types"""

    component_type_data = {"component_type": component_type, "service_interval": service_interval, "expected_lifetime": expected_lifetime}
    modify_records.update_component_type(component_type_data)

    return RedirectResponse(url="/component_types_overview", status_code=303)

@app.post("/add_service", response_class=HTMLResponse)
async def add_service(
    component_id: str = Form(...),
    service_date: str = Form(...),
    service_description: str = Form(...)):
    """Endpoint to add service"""

    component_data = read_records.read_component(component_id)
    service_id = misc_methods.generate_unique_id()
    
    service_data = {"service_id": service_id,
                    "component_id": component_id,
                    "service_date": service_date,
                    "description": service_description,
                    "component_name": component_data.component_name,
                    "bike_id": component_data.bike_id}
    
    latest_service_record = read_records.read_latest_service_record(component_id)
    
    if latest_service_record is None:
        latest_history_record = read_records.read_latest_history_record(component_id)
        distance_since_service = latest_history_record.distance_marker

        if latest_history_record.update_reason == "Installed":
            logging.info(f'Timespan for service distance query (triggered by new service): start date {latest_history_record.updated_date} stop date {service_date}')
            distance_since_service += misc_methods.sum_distanse_subset_rides(component_data.bike_id, latest_history_record.updated_date, service_date)
        
    elif latest_service_record:
        logging.info(f'Timespan for service distance query (triggered by new service): start date {latest_service_record.service_date} stop date {service_date}')
        distance_since_service = misc_methods.sum_distanse_subset_rides(component_data.bike_id, latest_service_record.service_date, service_date)

    service_data.update({"distance_marker": distance_since_service})
    modify_records.update_service_history(service_data)
    modify_tables.update_component_service_status(component_data)

    return RedirectResponse(url=f"/component_details/{component_id}", status_code=303)

@app.post("/component_modify", response_class=HTMLResponse)
async def modify_component(
    component_id: Optional[str] = Form(None),
    component_installation_status: str = Form(...),
    component_updated_date: str = Form(...),
    component_name: str = Form(...),
    component_type: str = Form(...),
    component_bike_id: Optional[str] = Form(None),
    expected_lifetime: Optional[int] = Form(None),
    service_interval: Optional[int] = Form(None),
    cost: Optional[int] = Form(None),
    offset: Optional[int] = Form(0),
    component_notes: Optional[str] = Form(None)):
    """Endpoint to modify component types"""

    new_component_data = {"installation_status": component_installation_status,
                      "updated_date": component_updated_date,
                      "component_name": component_name,
                      "component_type": component_type,
                      "bike_id": component_bike_id,
                      "lifetime_expected": expected_lifetime,
                      "service_interval": service_interval,
                      "cost": cost,
                      "component_distance_offset": offset,
                      "notes": component_notes}

    if component_id is None:
        component_id = misc_methods.generate_unique_id()
        modify_records.update_component_details(component_id, new_component_data)
            
    current_history_id = f'{component_updated_date} {component_id}'
    old_component_data = read_records.read_component(component_id)
    updated_bike_name = misc_methods.get_bike_name(component_bike_id)
    previous_bike_name = misc_methods.get_bike_name(old_component_data.bike_id) 
    latest_history_record = read_records.read_latest_history_record(component_id)
    
    if latest_history_record is not None and latest_history_record.history_id == current_history_id:
        if latest_history_record.update_reason == component_installation_status:
            logging.info(f"Only updating select component record details and service and lifetime status. Historic record already exist for component id {component_id} and record id {current_history_id}.")
            modify_records.update_component_details(component_id, new_component_data)
            updated_component_data = read_records.read_component(component_id)
            modify_tables.update_component_service_status(updated_component_data)
            modify_tables.update_component_lifetime_status(updated_component_data)
        else:
            logging.warning(f"Cannot change installation status when record date it the same as previous record. Historic record already exist for component id {component_id} and record id {current_history_id}. Skipping...")
    
    else:
        if latest_history_record is None:
            historic_distance = 0

        else:
            if component_installation_status != "Installed":
                logging.info(f'Timespan for historic distance query (triggered by component update): start date {latest_history_record.updated_date} stop date {component_updated_date}')
                historic_distance = misc_methods.sum_distanse_subset_rides(old_component_data.bike_id, latest_history_record.updated_date, component_updated_date)
                historic_distance += latest_history_record.distance_marker

            else:
                historic_distance = latest_history_record.distance_marker #This line is probably redundant..? 

        halt_update = modify_records.update_component_history_record(old_component_data, latest_history_record, current_history_id, component_id, previous_bike_name, updated_bike_name, component_installation_status, component_updated_date, historic_distance)
        
        if halt_update is False:
            modify_records.update_component_details(component_id, new_component_data)
            updated_component_data = read_records.read_component(component_id)
            latest_history_record = read_records.read_latest_history_record(component_id)
            
            if updated_component_data.installation_status == "Installed":
                logging.info(f'Timespan for current distance query (triggered by component update): start date {updated_component_data.updated_date} stop date {datetime.today()}')
                current_distance = misc_methods.sum_distanse_subset_rides(updated_component_data.bike_id, updated_component_data.updated_date, datetime.today())
                current_distance += latest_history_record.distance_marker
                modify_tables.update_component_distance(component_id, current_distance)

            else:
                current_distance = latest_history_record.distance_marker #Can this be made redundant by reordering function above?
                modify_tables.update_component_distance(component_id, current_distance)
        else:
            logging.warning(f"Update of component with id {component_id} skipped due to exceptions when updating history record")
        
    return RedirectResponse(url=f"/component_details/{component_id}", status_code=303)

@app.get("/component_overview", response_class=HTMLResponse)
async def component_overview(request: Request):
    """Endpoint for components page"""

    try:
        components = read_tables.read_all_components()
        component_data = [(component.component_id,
                        component.component_type,
                        component.component_name,
                        int(component.component_distance),
                        component.installation_status,
                        misc_methods.format_component_status(component.lifetime_status),
                        misc_methods.format_component_status(component.service_status),
                        misc_methods.get_bike_name(component.bike_id)
                        ) for component in components]
        
        bikes = read_tables.read_bikes()
        bikes_data = [(bike.bike_name,
                        bike.bike_id)
                        for bike in bikes if bike.bike_retired == "False"]

        component_types = read_tables.read_component_types()
        component_types_data = [(component_type.component_type,
                                component_type.expected_lifetime,
                                component_type.service_interval) for component_type in component_types]
            
        template_path = "component_overview.html"
        return templates.TemplateResponse(template_path, {"request": request,
                                                          "component_data": component_data,
                                                          "bikes_data": bikes_data,
                                                          "component_types_data": component_types_data})
    
    except Exception as error:
        # Get the full traceback
        error_traceback = traceback.format_exc()
        
        # Log the full traceback
        logging.error(f"An error occurred:\n{error_traceback}")

        if isinstance(error, HTTPException):
            if error.status_code == status.HTTP_503_SERVICE_UNAVAILABLE:
                return render_error_page(request, error.status_code, str(error.detail))
            else:
                return render_error_page(request, error.status_code, str(error.detail))
        else:
            # For non-HTTP exceptions, include the error message and the last line of the traceback
            error_lines = error_traceback.split('\n')
            return render_error_page(request, 500, error_lines)

@app.get("/bike_details/{bike_id}", response_class=HTMLResponse)
async def bike_details(request: Request, bike_id: str):
    """Endpoint for bike details page"""
    try:
        # Fetch bike details based on the bike_id
        bike = read_records.read_bike(bike_id)
        bike_data = {"bike_name": bike.bike_name,
                    "bike_id": bike.bike_id,
                    "bike_retired": bike.bike_retired,
                    "bike_service_status": bike.service_status,
                    "bike_total_distance": int(bike.total_distance),
                    "bike_notes": bike.notes,
                    "first_ride": misc_methods.get_first_ride(bike_id)}
        
        bike_components = read_tables.read_subset_components(bike_id)
        bike_components_data = [(component.component_id,
                        component.installation_status,
                        component.component_type,
                        component.component_name,
                        int(component.component_distance),
                        misc_methods.format_component_status(component.lifetime_status),
                        misc_methods.format_component_status(component.service_status),
                        misc_methods.format_cost(component.cost)
                        ) for component in bike_components]

        component_statistics = misc_methods.get_component_statistics([tuple(component[1:]) for component in bike_components_data])
        
        recent_rides = read_tables.read_recent_rides(bike_id)
        recent_rides_data = [(ride.ride_id,
                        misc_methods.format_datetime(ride.record_time),
                        ride.ride_name,
                        int(ride.ride_distance),
                        ride.commute
                        ) for ride in recent_rides]

        payload = {
            "recent_rides": recent_rides_data,
            "bike_data": bike_data,
            "bike_components_data": bike_components_data,
            "count_installed" : component_statistics["count_installed"],
            "count_lifetime_status_green" : component_statistics["count_lifetime_status_green"],
            "count_lifetime_status_yellow" : component_statistics["count_lifetime_status_yellow"],
            "count_lifetime_status_red" : component_statistics["count_lifetime_status_red"],
            "count_service_status_green" : component_statistics["count_service_status_green"],
            "count_service_status_yellow" : component_statistics["count_service_status_yellow"],
            "count_service_status_red" : component_statistics["count_service_status_red"],
            "sum_cost" : component_statistics["sum_cost"]
        }

        template_path = "bike_details.html"
        return templates.TemplateResponse(template_path, {"request": request, "payload": payload})
    
    except Exception as error:
        # Handle exceptions
        raise HTTPException(status_code=500, detail=str(error))
    

@app.get("/component_details/{component_id}", response_class=HTMLResponse)
async def component_details(request: Request, component_id: str):
    """Endpoint for component details page"""

    bikes = read_tables.read_bikes()
    bikes_data = [(bike.bike_name,
                    bike.bike_id)
                    for bike in bikes if bike.bike_retired == "False"]

    component_types = read_tables.read_component_types()
    component_types_data = [(component_type.component_type,
                            component_type.expected_lifetime,
                            component_type.service_interval) for component_type in component_types]
    
    bike_component = read_records.read_component(component_id)
    bike_component_data = {"bike_id": bike_component.bike_id,
                    "component_id": bike_component.component_id,
                    "updated_date": bike_component.updated_date,
                    "component_name": bike_component.component_name,
                    "component_type": bike_component.component_type,
                    "component_distance": int(bike_component.component_distance),
                    "installation_status": bike_component.installation_status,
                    "lifetime_expected": bike_component.lifetime_expected,
                    "lifetime_remaining": bike_component.lifetime_remaining,
                    "lifetime_status": misc_methods.format_component_status(bike_component.lifetime_status),
                    "lifetime_percentage": modify_tables.calculate_percentage_reached(bike_component.lifetime_expected, bike_component.lifetime_remaining),
                    "service_interval": bike_component.service_interval,
                    "service_next": bike_component.service_next,
                    "service_status": misc_methods.format_component_status(bike_component.service_status),
                    "service_percentage": modify_tables.calculate_percentage_reached(bike_component.service_interval, bike_component.service_next),
                    "offset": int(bike_component.component_distance_offset),
                    "component_notes": bike_component.notes,
                    "cost": misc_methods.format_cost(bike_component.cost)}
    
    component_history = read_tables.read_subset_component_history(bike_component.component_id)
    if component_history is not None:
        component_history_data = [(installation_record.updated_date,
                                   installation_record.update_reason,
                                   installation_record.bike_name,
                                   installation_record.distance_marker) for installation_record in component_history]
    else:
        component_history_data = None

    service_history = read_tables.read_subset_service_history(bike_component.component_id)
    if service_history is not None:
        service_history_data = [(service_record.service_date,
                                   service_record.description,
                                   misc_methods.get_bike_name(service_record.bike_id),
                                   service_record.distance_marker) for service_record in service_history]
    else:
        service_history_data = None


    payload = {
        "bikes_data": bikes_data,
        "component_types_data": component_types_data,
        "bike_component_data": bike_component_data,
        "bike_name": misc_methods.get_bike_name(bike_component.bike_id),
        "component_history_data": component_history_data,
        "service_history_data": service_history_data}

    template_path = "component_details.html"
    return templates.TemplateResponse(template_path, {"request": request, "payload": payload})

@app.post("/delete_record", response_class=HTMLResponse)
async def delete_record(
    record_id: str = Form(...),
    table_selector: str = Form(...)):
    """Endpoint to delete records"""

    modify_records.delete_record(table_selector, record_id)


# Endpoint get all rides and recent rides, make it possible also to call with "all" arg
#strava.get_rides("recent") 
#modify_tables.update_rides_bulk(strava.payload)

# Endpoints get all bikes (triggered when new rides are fetched, and should also be able to call manually), can also be called with this as arg strava.bike_ids_recent_rides or peewee_connector.list_unique_bikes(). Depends on context
#if len(strava.bike_ids_recent_rides) > 0:
#    strava.get_bikes(strava.bike_ids_recent_rides)
#    modify_tables.update_bikes(strava.payload)

# Code to update installed components distance and moving time (not callable as endpoint).
# Should be trigger by fetching of new rides and when components are added, should also be able to trigger manually with all
# This method should be called by main.
# Method should create a list of component ids to be submitted as arg to function below. Method should support operating on this list, single ID or all components.

#modify_tables.update_components_distance_selector(strava.bike_ids_recent_rides)
#modify_tables.update_components_distance_selector(misc_methods.list_unique_bikes())

# Code to update misc status fields of components (not callable as endpoint). Should be triggered by updating of installed components
# This method should be called by main

# Todo
# All endpoints that writes should print log
# Clean up HTML code and check consistency all end points, applies also to python scripts
# Velo supervisor logo must be clickable, go to "/about"
# All notes in Strava should be in english
# Make sure all endpoints have same logic, variable naming conventions..
# Display banner on all pages if last ride is more than seven days ago
# Add favicon
# Switch to show also retired bikes on bike overview
# Switch to show different component statuses on component overview
# Add function to delete associated records if a component is deleted
# Component type should specify suggested as prefix for variables
# Use the same name across endpoints, require change also to html files: bike_components_data
# Sort endpoints so they appear in a more logical order
# Add input validation on component details form, should have input validation on all forms
# Consider all export statement, maybe not needed?
# Update all diagrams to match code
# Review all doc strings
# Implement health check
# Clean up datatypes to avoid casting in script, most, if not all numbers, should be int
# Improvement: on bike change automatically uninstall and install, enhancement, not fix now, or some sort of validation
# Validation in form, cannot be "Not assigned" bike when status is installed
# Bike details page - summary of lifetime and service should filter out retired components and of course those not installed
# Give warning before selecting "Retired"
# Make issue for the use of halt_update, can be improved. Return after each statement instead
# old_component_data is only used for old bike_id, refactor to take this into account. 
# Update historic record should also include new component name. Review this before making issue. Not sure this is really a bug. Historic records should not be updated if no change is made to install status and record date.. Seems to work the way it is
# Consider different icon for installed - the cog is already used in navtab, change all places
# There is some kind of rounding issue, probably caused by int somewhere. Causes totals to be slightly off
# Updated readme with change log
# Component detail page should have delete button, maybe not relevant..
# Input validation on all forms (add component type, add component overview, add component detail, add service history)
# Bug when date for ride is set further in the future than there is ride data. Dont fix now. This is not a bug, it simply does nothing. This is solved already?
# Table installation history should use id and not name for bike..
# Check what to do if you try to add service status to a component that is not installed to any bike

# Fix these first
# Bug when offset is changed and record date is the same as newest history, total distance is not updated
# Bug: WARNING - Component Surly Test (id 2712c51234) is not assigned to any bike, defaulting to current component distance. This comes when only updating component detail, without changing date. Its related to this one: def update_component_service_status(self, component):
# Function to retrieve data from Strava
# FUnction to delete components and associated data
# Add installed component count on bike card (bike overview - all bikes)
# Check function that writes lifetime and service status, either NULL should be store or "Not defined". Right now its a mix..Applies to component table
# X. There is a bug somewhere in how distance is calculated for component, related to installation history probably.. Is it? This is not confirmed..
# X. Page bike details: table should show status for components: retired or installed
# X. Page bike details: column to the left should only include installed components, not retired.
# X. Page bike details: estimated cost should only calculate cost for approaching or exceeded
# X. Compute bike status, probably based on components, Function to calculate service status in bikes table
# X. Modify percentage bar to state exceeded with...




