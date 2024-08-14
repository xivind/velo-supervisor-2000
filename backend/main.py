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

@app.post("/component_modify", response_class=HTMLResponse) #WORKING HERE NOW
async def modify_component(
    component_id: str = Form(...),
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

    #Process some of the data here, e.g. component_install status, id if missing.. Could be others
    new_component_data = {"component_installation_status": component_installation_status,
                      "component_updated_date": component_updated_date,
                      "component_name": component_name,
                      "component_type": component_type,
                      "component_bike_id": component_bike_id,
                      "expected_lifetime": expected_lifetime,
                      "service_interval": service_interval,
                      "cost": cost,
                      "offset": offset,
                      "component_notes": component_notes}
                           
    modify_records.update_component_details(component_id, new_component_data)
    modify_tables.update_component_distance(read_records.read_component(component_id))
    #Match variables with sqlite, see component types for inspiraton. update or create new. Must caluclate before writing to 

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


        template_path = "component_overview.html"
        return templates.TemplateResponse(template_path, {"request": request, "component_data": component_data})
    
    except Exception as error:
        # Handle other exceptions does not catch 404, error handling must also print to log / console
        if isinstance(error, HTTPException):
            # If the exception is an HTTPException, handle it accordingly
            if error.status_code == status.HTTP_503_SERVICE_UNAVAILABLE:
                # Handle 503 Service Unavailable error
                return render_error_page(request, error.status_code, str(error.detail))
            else:
                # Handle other HTTP errors
                return render_error_page(request, error.status_code, str(error.detail))
        else:
            # Handle other exceptions (e.g., internal server errors)
            return render_error_page(request, 500, str(error))

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
                    "bike_notes": bike.notes}
        
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
    try:
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
        
        payload = {
            "bikes_data": bikes_data,
            "component_types_data": component_types_data,
            "bike_component_data": bike_component_data,
            "bike_name": misc_methods.get_bike_name(bike_component.bike_id),
            }

        template_path = "component_details.html"
        return templates.TemplateResponse(template_path, {"request": request, "payload": payload})
    
    except Exception as error:
        # Handle other exceptions does not catch 404, error handling must also print to log / console
        if isinstance(error, HTTPException):
            # If the exception is an HTTPException, handle it accordingly
            if error.status_code == status.HTTP_503_SERVICE_UNAVAILABLE:
                # Handle 503 Service Unavailable error
                return render_error_page(request, error.status_code, str(error.detail))
            else:
                # Handle other HTTP errors
                return render_error_page(request, error.status_code, str(error.detail))
        else:
            # Handle other exceptions (e.g., internal server errors)
            return render_error_page(request, 500, str(error))

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

# todo
# Add error handling to all endpoints
# Check consistency all end points
# All endpoints that writes should print log
# Clean up HTML code
# Velo supervisor logo must be clickable, go to "/about"
# All notes in Strava should be in english
# Make sure all endpoints have same logic, variable naming conventions..
# Display banner on all pages if last ride is more than seven days ago
# Compute bike status, probably based on components
# Retired components must also unassign from bike
# Add favicon
# Cleanup html in all files
# Switch to show also retired bikes
# Must have action to delete component
# Component overview page should have summary section and delete button
# Improvement: component type must be defined in order to prefill og component details to work for component type
# Component type should specify suggested as prefix for variables
# Use the same name across endpoints, require change also to html files: bike_components_data
# Sort endpoints so they appear in a more logical order
# Add input validation on component details form

# 3. Modify update of distance to check for date installed
# 2. Modify installed status based on bike value
# 1. Handle offset upon change of installation status
# X. Code to calculate bike status
# Modify percentage bar to state exceeded with...

# Bug when date for ride is set further in the future than there is ride data. Dont fix now. 

