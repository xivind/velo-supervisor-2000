#!/usr/bin/env python3
"""Main code for Velo Supervisor 2000"""

from middleware import Middleware
import logging
import json
from typing import Optional
from datetime import datetime
import sys
import asyncio
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException
from strava import Strava #Remove after refactoring
from business_logic import BusinessLogic
import utils #import explicitly
from database_manager import DatabaseManager #Remove this and all reference to it when code has been moved to business logic

# Load configuration
CONFIG = utils.read_config()

# Initialize database # Remove after refactoring
database_manager = DatabaseManager() #Remove this and all reference to it when code has been moved to business logic

# Create application object
app = FastAPI()

# Initialize Strava API
strava = Strava(CONFIG['strava_tokens']) # Remove after refactoring

# Setup static files and templates
app.mount("/static", StaticFiles(directory="../frontend/static"), name="static")
templates = Jinja2Templates(directory="../frontend/templates")

# Add middleware
app.add_middleware(Middleware, templates=templates)

# Configure application state
app.version = utils.get_current_version()
app.state.db_path = CONFIG['db_path']
app.state.strava_last_pull = None
app.state.strava_days_since_last_pull = None

# Create business logic object
business_logic = BusinessLogic(app.state)
business_logic.set_time_strava_last_pull()

# Exception handler
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Function to catch http errors from Uvicorn and return them to the middleware"""
    return await Middleware(app, templates=templates).handle_exception(exc, request)

#Startup event
@app.on_event("startup")
async def startup_event():
    """Function to register background tasks"""
    asyncio.create_task(utils.pull_strava_background("recent"))

# Route handlers
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Endpoint for index / landing page"""
    
    bikes = database_manager.read_bikes()
    bikes_data = [(bike.bike_name,
                   bike.bike_id,
                   bike.bike_retired,
                   bike.service_status,
                   int(bike.total_distance),
                   sum(1 for component in database_manager.read_subset_components(bike.bike_id) if component.installation_status == "Installed"),
                   sum(1 for component in database_manager.read_subset_components(bike.bike_id) if component.installation_status == "Retired")) for bike in bikes]

    payload = {"bikes_data": bikes_data}
    template_path = "index.html"
    
    return templates.TemplateResponse(template_path, {"request": request,
                                                      "payload": payload})

@app.get("/component_types_overview", response_class=HTMLResponse)
async def component_types_overview(request: Request):
    """Endpoint for component types page"""    
    
    payload = {"component_types": database_manager.read_all_component_types()}
    template_path = "component_types.html"
    
    return templates.TemplateResponse(template_path, {"request": request,
                                                      "payload": payload})


@app.post("/component_types_modify", response_class=HTMLResponse)
async def component_types_modify(
    component_type: str = Form(...),
    expected_lifetime: Optional[str] = Form(None),
    service_interval: Optional[str] = Form(None)):
    """Endpoint to modify component types"""

    business_logic.modify_component_type(component_type,
                                         expected_lifetime,
                                         service_interval)
    
    # This should return a message to the user, could use success, message

    return RedirectResponse(url="/component_types_overview", status_code=303)


@app.post("/add_service", response_class=HTMLResponse)
async def add_service(
    component_id: str = Form(...),
    service_date: str = Form(...),
    service_description: str = Form(...)):
    """Endpoint to add service"""

    business_logic.create_service_record(component_id,
                                         service_date,
                                         service_description)
    
    # This should return a message to the user, could use success, message = above

    return RedirectResponse(url=f"/component_details/{component_id}", status_code=303)


@app.post("/component_modify", response_class=HTMLResponse)
async def component_modify(
    component_id: Optional[str] = Form(None),
    component_installation_status: str = Form(...),
    component_updated_date: str = Form(...),
    component_name: str = Form(...),
    component_type: str = Form(...),
    component_bike_id: str = Form(...),
    expected_lifetime: Optional[str] = Form(None),
    service_interval: Optional[str] = Form(None),
    cost: Optional[str] = Form(None),
    offset: Optional[int] = Form(0),
    component_notes: Optional[str] = Form(None)):
    """Endpoint to modify component types"""

    success, message, component_id = (business_logic
                                      .modify_component_details
                                        (component_id,
                                        component_installation_status,
                                        component_updated_date,
                                        component_name,
                                        component_type,
                                        component_bike_id,
                                        expected_lifetime,
                                        service_interval,
                                        cost,
                                        offset,
                                        component_notes))

    # This should return a message to the user

    return RedirectResponse(url=f"/component_details/{component_id}", status_code=303)

@app.get("/component_overview", response_class=HTMLResponse)
async def component_overview(request: Request):
    """Endpoint for components page"""
    
    components = database_manager.read_all_components()
    component_data = [(component.component_id,
                    component.component_type,
                    component.component_name,
                    int(component.component_distance),
                    component.installation_status,
                    utils.format_component_status(component.lifetime_status),
                    utils.format_component_status(component.service_status),
                    database_manager.read_bike_name(component.bike_id),
                    utils.format_cost(component.cost)
                    ) for component in components]

    rearranged_component_data = [(comp[4],
                                    None,
                                    None,
                                    None,
                                    comp[5],
                                    comp[6],
                                    comp[8],
                                    None,
                                    comp[7]) for comp in component_data]

    component_statistics = utils.get_component_statistics(rearranged_component_data)

    bikes = database_manager.read_bikes()
    bikes_data = [(bike.bike_name,
                    bike.bike_id)
                    for bike in bikes if bike.bike_retired == "False"]

    component_types_data = database_manager.read_all_component_types()

    payload = {"request": request,
               "component_data": component_data,
               "bikes_data": bikes_data,
               "component_types_data": component_types_data,
               "count_installed" : component_statistics["count_installed"],
               "count_not_installed" : component_statistics["count_not_installed"],
               "count_retired" : component_statistics["count_retired"],
               "count_lifetime_status_green" : component_statistics["count_lifetime_status_green"],
               "count_lifetime_status_yellow" : component_statistics["count_lifetime_status_yellow"],
               "count_lifetime_status_red" : component_statistics["count_lifetime_status_red"],
               "count_lifetime_status_purple" : component_statistics["count_lifetime_status_purple"],
               "count_lifetime_status_grey" : component_statistics["count_lifetime_status_grey"],
               "count_service_status_green" : component_statistics["count_service_status_green"],
               "count_service_status_yellow" : component_statistics["count_service_status_yellow"],
               "count_service_status_red" : component_statistics["count_service_status_red"],
               "count_service_status_purple" : component_statistics["count_service_status_purple"],
               "count_service_status_grey" : component_statistics["count_service_status_grey"],
               "sum_cost" : component_statistics["sum_cost"]}
    template_path = "component_overview.html"
    
    return templates.TemplateResponse(template_path, {"request": request,
                                                      "payload": payload})


@app.get("/bike_details/{bike_id}", response_class=HTMLResponse)
async def bike_details(request: Request, bike_id: str):
    """Endpoint for bike details page"""
    
    bike = database_manager.read_single_bike(bike_id)
    bike_data = {"bike_name": bike.bike_name,
                "bike_id": bike.bike_id,
                "bike_retired": bike.bike_retired,
                "bike_service_status": bike.service_status,
                "bike_total_distance": int(bike.total_distance),
                "bike_notes": bike.notes,
                "oldest_ride": database_manager.read_date_oldest_ride(bike_id)}

    bike_components = database_manager.read_subset_components(bike_id)
    bike_components_data = [(component.component_id,
                    component.installation_status,
                    component.component_type,
                    component.component_name,
                    int(component.component_distance),
                    utils.format_component_status(component.lifetime_status),
                    utils.format_component_status(component.service_status),
                    utils.format_cost(component.cost)
                    ) for component in bike_components]

    component_statistics = utils.get_component_statistics([tuple(component[1:]) for component in bike_components_data])

    recent_rides = database_manager.read_recent_rides(bike_id)
    recent_rides_data = [(ride.ride_id,
                    ride.record_time,
                    ride.ride_name,
                    int(ride.ride_distance),
                    ride.commute
                    ) for ride in recent_rides]

    payload = {"recent_rides": recent_rides_data,
               "bike_data": bike_data,
               "bike_components_data": bike_components_data,
               "count_installed" : component_statistics["count_installed"],
               "count_lifetime_status_green" : component_statistics["count_lifetime_status_green"],
               "count_lifetime_status_yellow" : component_statistics["count_lifetime_status_yellow"],
               "count_lifetime_status_red" : component_statistics["count_lifetime_status_red"],
               "count_lifetime_status_purple" : component_statistics["count_lifetime_status_purple"],
               "count_lifetime_status_grey" : component_statistics["count_lifetime_status_grey"],
               "count_service_status_green" : component_statistics["count_service_status_green"],
               "count_service_status_yellow" : component_statistics["count_service_status_yellow"],
               "count_service_status_red" : component_statistics["count_service_status_red"],
               "count_service_status_purple" : component_statistics["count_service_status_purple"],
               "count_service_status_grey" : component_statistics["count_service_status_grey"],
               "sum_cost" : component_statistics["sum_cost"]}
    template_path = "bike_details.html"
    
    return templates.TemplateResponse(template_path, {"request": request,
                                                      "payload": payload})


@app.get("/component_details/{component_id}", response_class=HTMLResponse)
async def component_details(request: Request, component_id: str):
    """Endpoint for component details page"""

    bikes = database_manager.read_bikes()
    bikes_data = [(bike.bike_name,
                    bike.bike_id)
                    for bike in bikes if bike.bike_retired == "False"]
    
    component_types_data = database_manager.read_all_component_types()
    
    bike_component = database_manager.read_component(component_id)
    bike_component_data = {"bike_id": bike_component.bike_id,
                    "component_id": bike_component.component_id,
                    "updated_date": bike_component.updated_date,
                    "component_name": bike_component.component_name,
                    "component_type": bike_component.component_type,
                    "component_distance": int(bike_component.component_distance) 
                        if bike_component.component_distance is not None else None,
                    "installation_status": bike_component.installation_status,
                    "lifetime_expected": bike_component.lifetime_expected,
                    "lifetime_remaining": int(bike_component.lifetime_remaining)
                        if bike_component.lifetime_remaining is not None else None,
                    "lifetime_status": utils.format_component_status(bike_component.lifetime_status),
                    "lifetime_percentage": utils.calculate_percentage_reached(bike_component.lifetime_expected, int(bike_component.lifetime_remaining))
                        if bike_component.lifetime_remaining is not None else None,
                    "service_interval": bike_component.service_interval,
                    "service_next": int(bike_component.service_next)
                        if bike_component.service_next is not None else None,
                    "service_status": utils.format_component_status(bike_component.service_status),
                    "service_percentage": utils.calculate_percentage_reached(bike_component.service_interval, int(bike_component.service_next))
                        if bike_component.service_next is not None else None,
                    "offset": bike_component.component_distance_offset,
                    "component_notes": bike_component.notes,
                    "cost": utils.format_cost(bike_component.cost)}

    component_history = database_manager.read_subset_component_history(bike_component.component_id)
    if component_history is not None:
        component_history_data = [(installation_record.updated_date,
                                   installation_record.update_reason,
                                   database_manager.read_bike_name(installation_record.bike_id),
                                   int(installation_record.distance_marker)) for installation_record in component_history]
    else:
        component_history_data = None

    service_history = database_manager.read_subset_service_history(bike_component.component_id)
    if service_history is not None:
        service_history_data = [(service_record.service_date,
                                   service_record.description,
                                   database_manager.read_bike_name(service_record.bike_id),
                                   int(service_record.distance_marker)) for service_record in service_history]
    else:
        service_history_data = None

    payload = {"bikes_data": bikes_data,
               "component_types_data": component_types_data,
               "bike_component_data": bike_component_data,
               "bike_name": database_manager.read_bike_name(bike_component.bike_id),
               "component_history_data": component_history_data,
               "service_history_data": service_history_data}
    template_path = "component_details.html"

    return templates.TemplateResponse(template_path, {"request": request,
                                                      "payload": payload})


@app.get("/refresh_all_bikes", response_class=HTMLResponse)
async def refresh_all_bikes(request: Request):
    """Endpoint to manually refresh data for all bikes"""
    # Something is not right with this endpoint, only called by button in config
    logging.info("Refreshing all bikes from Strava (called directly)")
    await strava.get_bikes(database_manager.read_unique_bikes()) #Route handler should not call Strava
    database_manager.write_update_bikes(strava.payload_bikes) #Should not call db manager, but business logic

    for bike_id in database_manager.read_unique_bikes():
        business_logic.update_bike_status(bike_id) #Not sure why we need to call this here..?

    # This should return a message to the user


@app.get("/refresh_rides/{mode}", response_class=HTMLResponse)
async def refresh_rides(request: Request, mode: str):
    """Endpoint to refresh data for a subset or all rides"""

    await business_logic.update_rides_bulk(mode)
    # This should return a message to the user


@app.post("/delete_record", response_class=HTMLResponse)
async def delete_record(
    record_id: str = Form(...),
    table_selector: str = Form(...)):
    """Endpoint to delete records"""

    business_logic.delete_record(table_selector, record_id)
    # This should return a message to the user


@app.get("/config_overview", response_class=HTMLResponse)
async def config_overview(request: Request):
    """Endpoint for component types page"""

    payload = {"strava_tokens": CONFIG['strava_tokens'],
               "db_path": CONFIG['db_path']}
    template_path = "config.html"

    return templates.TemplateResponse(template_path, {"request": request,
                                                      "payload": payload})


@app.post("/update_config")
async def update_config(request: Request,
                        db_path: str = Form(...),
                        strava_tokens: str = Form(...)):
    """Endpoint to update config file"""

    success, message = utils.write_config(db_path, strava_tokens)
    
    if success:
        sys.exit(0)

    # This should return a message to the user

@app.get("/get_filtered_log")
async def get_filtered_logs():
    """Endpoint to read log and return only business events""" 
 #Move to utils and get data from there
    with open('/data/logs/app.log', 'r', encoding='utf-8') as log_file:
        logs = log_file.readlines()

    filtered_logs = [log for log in logs if "GET" not in log and "POST" not in log]
    subset_filtered_logs = filtered_logs[-100:]

    return {"logs": subset_filtered_logs}
