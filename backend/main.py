#!/usr/bin/env python3
"""Main backend for velo supervisor 2000"""


from strava import Strava
from peewee_connector import ReadTables, ModifyTables, ReadRecords, ModifyRecords, MiscMethods
import argparse
import logging
import uvicorn
from time import sleep
from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import Optional
from pathlib import Path
from datetime import datetime


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
#modify_tables = ModifyTables()
#read_records = ReadRecords()
modify_records = ModifyRecords()
misc_methods = MiscMethods()
#Initiate more classes

app = FastAPI()
templates = Jinja2Templates(directory="../frontend/templates")
#template_dir = Path("../frontend/templates")
# Add static dir


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Endpoint for index / landing page"""
    bikes = read_tables.read_bikes()
    bike_data = [(bike.bike_name,
                  bike.bike_retired,
                  bike.service_status,
                  int(bike.total_distance)) for bike in bikes]

    template_path = "index.html"
    return templates.TemplateResponse(template_path, {"request": request, "bike_data": bike_data})

@app.get("/component_types_overview", response_class=HTMLResponse)
async def component_types_overview(request: Request):
    """Endpoint for component types page"""    
    component_types = read_tables.read_component_types()
    component_types_data = [(component_type.component_type,
                             component_type.service_interval,
                             component_type.expected_lifetime) for component_type in component_types]

    template_path = "component_types.html"
    return templates.TemplateResponse(template_path, {"request": request, "component_types_data": component_types_data})

@app.post("/component_types_overview/modify", response_class=HTMLResponse)
async def modify_component_type(
    component_type: str = Form(...),
    service_interval: Optional[int] = Form("Not defined"),
    expected_lifetime: Optional[int] = Form("Not defined")):
    """Endpoint to modify component types"""

    component_type_data = {"component_type": component_type, "service_interval": service_interval, "expected_lifetime": expected_lifetime}
    modify_records.update_component_type(component_type_data)

    return RedirectResponse(url="/component_types_overview", status_code=303)

@app.get("/component_overview", response_class=HTMLResponse)
async def component_overview(request: Request):
    """Endpoint for components page"""

    components = read_tables.read_components()
    component_data = [(component.component_type,
                       component.component_name,
                       component.component_distance) for component in components]


    template_path = "component_overview.html"
    return templates.TemplateResponse(template_path, {"request": request, "component_data": component_data})

@app.post("/delete_record", response_class=HTMLResponse)
async def delete_record(
    record_id: str = Form(...),
    table_selector: str = Form(...)):
    """Endpoint to delete records"""

    modify_records.delete_record(table_selector, record_id)


# Include pop ups to indicate success or failure 
#Create a separate template to handle all errors, also 500
#include excpetion handling, e.g raise HTTPException(status_code=404, detail="Page not found")
#sorting of tables

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



