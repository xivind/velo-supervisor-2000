#!/usr/bin/env python3
"""Route handlers for Velo Supervisor 2000"""

from typing import Optional, List
import asyncio
import atexit
from middleware import Middleware
from scheduler import start_scheduler, stop_scheduler
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException
from business_logic import BusinessLogic
from utils import (read_config,
                   get_current_version,
                   write_config,
                   read_filtered_logs,
                   shutdown_server)

# Load configuration
CONFIG = read_config()

# Create application object
app = FastAPI()

# Setup static files and templates
app.mount("/static", StaticFiles(directory="../frontend/static"), name="static")
templates = Jinja2Templates(directory="../frontend/templates")

# Add middleware
app.add_middleware(Middleware, templates=templates)

# Configure application state
app.version = get_current_version()
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

# Startup event
@app.on_event("startup")
async def startup_event():
    """Function to register background tasks"""
    start_scheduler()
    asyncio.create_task(business_logic.pull_strava_background("recent"))

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Function to gracefully shutdown scheduler"""
    stop_scheduler()

atexit.register(lambda: stop_scheduler() if stop_scheduler else None)

# Route handlers
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Endpoint for landing page"""

    payload = business_logic.get_bike_overview()
    template_path = "index.html"

    return templates.TemplateResponse(template_path,
                                      {"request": request,
                                       "payload": payload})

@app.get("/bike_details/{bike_id}", response_class=HTMLResponse)
async def bike_details(request: Request,
                       bike_id: str):
    """Endpoint for bike details page"""

    payload = business_logic.get_bike_details(bike_id)
    template_path = "bike_details.html"

    return templates.TemplateResponse(template_path,
                                      {"request": request,
                                       "payload": payload})

@app.get("/component_overview", response_class=HTMLResponse)
async def component_overview(request: Request):
    """Endpoint for components overview page"""

    payload = business_logic.get_component_overview()
    template_path = "component_overview.html"

    return templates.TemplateResponse(template_path,
                                      {"request": request,
                                       "payload": payload})

@app.get("/incident_reports", response_class=HTMLResponse)
async def incident_reports(request: Request):
    """Endpoint for incident reports page"""

    payload = business_logic.get_incident_reports()
    template_path = "incident_reports.html"

    return templates.TemplateResponse(template_path,
                                      {"request": request,
                                       "payload": payload})

@app.get("/workplans", response_class=HTMLResponse)
async def workplans(request: Request):
    """Endpoint for workplans page"""

    payload = business_logic.get_workplans()
    template_path = "workplans.html"

    return templates.TemplateResponse(template_path,
                                      {"request": request,
                                       "payload": payload})

@app.get("/component_details/{component_id}", response_class=HTMLResponse)
async def component_details(request: Request,
                            component_id: str,
                            success: Optional[str] = None,
                            message: Optional[str] = None):
    """Endpoint for component details page"""

    payload = business_logic.get_component_details(component_id)
    template_path = "component_details.html"

    return templates.TemplateResponse(template_path,
                                      {"request": request,
                                       "payload": payload,
                                       "success": success,
                                       "message": message})

@app.get("/component_types_overview", response_class=HTMLResponse)
async def component_types_overview(request: Request,
                                   success: Optional[str] = None,
                                   message: Optional[str] = None):
    """Endpoint for component types page"""    

    payload = business_logic.get_component_types()
    template_path = "component_types.html"

    return templates.TemplateResponse(template_path,
                                      {"request": request,
                                       "payload": payload,
                                       "success": success,
                                       "message": message})

@app.get("/config_overview", response_class=HTMLResponse)
async def config_overview(request: Request,
                          success: Optional[str] = None,
                          message: Optional[str] = None):
    """Endpoint for component types page"""

    payload = {"strava_tokens": CONFIG['strava_tokens'],
               "db_path": CONFIG['db_path']}
    template_path = "config.html"

    return templates.TemplateResponse(template_path,
                                      {"request": request,
                                       "payload": payload,
                                       "success": success,
                                       "message": message})

@app.get("/help", response_class=HTMLResponse)
async def help_page(request: Request):
    """Endpoint for help page"""

    template_path = "help.html"

    return templates.TemplateResponse(template_path,
                                      {"request": request})

@app.post("/create_component", response_class=HTMLResponse)
async def create_component(component_id: Optional[str] = Form(None),
                           component_installation_status: str = Form(...),
                           component_updated_date: str = Form(...),
                           component_name: str = Form(...),
                           component_type: str = Form(...),
                           component_bike_id: str = Form(...),
                           expected_lifetime: Optional[str] = Form(None),
                           service_interval: Optional[str] = Form(None),
                           threshold_km: Optional[str] = Form(None),
                           lifetime_expected_days: Optional[str] = Form(None),
                           service_interval_days: Optional[str] = Form(None),
                           threshold_days: Optional[str] = Form(None),
                           cost: Optional[str] = Form(None),
                           offset: Optional[int] = Form(0),
                           component_notes: Optional[str] = Form(None)):
    """Endpoint to modify component types"""

    success, message, component_id = (business_logic.create_component
                                      (component_id,
                                       component_installation_status,
                                       component_updated_date,
                                       component_name,
                                       component_type,
                                       component_bike_id,
                                       expected_lifetime,
                                       service_interval,
                                       threshold_km,
                                       lifetime_expected_days,
                                       service_interval_days,
                                       threshold_days,
                                       cost,
                                       offset,
                                       component_notes))

    response = RedirectResponse(
        url=f"/component_details/{component_id}?success={success}&message={message}",
        status_code=303)

    return response

@app.post("/update_component_details", response_class=HTMLResponse)
async def component_modify(component_id: Optional[str] = Form(None),
                           component_installation_status: str = Form(...),
                           component_updated_date: str = Form(...),
                           component_name: str = Form(...),
                           component_type: str = Form(...),
                           component_bike_id: str = Form(...),
                           expected_lifetime: Optional[str] = Form(None),
                           service_interval: Optional[str] = Form(None),
                           threshold_km: Optional[str] = Form(None),
                           lifetime_expected_days: Optional[str] = Form(None),
                           service_interval_days: Optional[str] = Form(None),
                           threshold_days: Optional[str] = Form(None),
                           cost: Optional[str] = Form(None),
                           offset: Optional[int] = Form(0),
                           component_notes: Optional[str] = Form(None)):
    """Endpoint to modify component types"""

    success, message, component_id = (business_logic.modify_component_details
                                      (component_id,
                                       component_installation_status,
                                       component_updated_date,
                                       component_name,
                                       component_type,
                                       component_bike_id,
                                       expected_lifetime,
                                       service_interval,
                                       threshold_km,
                                       lifetime_expected_days,
                                       service_interval_days,
                                       threshold_days,
                                       cost,
                                       offset,
                                       component_notes))

    response = RedirectResponse(
        url=f"/component_details/{component_id}?success={success}&message={message}",
        status_code=303)

    return response

@app.post("/add_history_record", response_class=HTMLResponse)
async def add_history_record(component_id: str = Form(...),
                             component_installation_status: str = Form(...),
                             component_bike_id: str = Form(...),
                             component_updated_date: str = Form(...)):
    """Endpoint to update an existing component history record"""

    success, message = business_logic.create_history_record(component_id,
                                                            component_installation_status,
                                                            component_bike_id,
                                                            component_updated_date)

    response = RedirectResponse(
        url=f"/component_details/{component_id}?success={success}&message={message}",
        status_code=303)

    return response

@app.post("/update_history_record", response_class=HTMLResponse)
async def update_history_record(component_id: str = Form(...),
                                history_id: str = Form(...),
                                updated_date: str = Form(...)):
    """Endpoint to update an existing component history record"""

    success, message = business_logic.update_history_record(history_id, updated_date)

    response = RedirectResponse(
        url=f"/component_details/{component_id}?success={success}&message={message}",
        status_code=303)

    return response

@app.post("/quick_swap")
async def quick_swap(old_component_id: str = Form(...),
                     fate: str = Form(...),
                     swap_date: str = Form(...),
                     new_component_id: Optional[str] = Form(None),
                     create_new: Optional[str] = Form(None),
                     new_component_name: Optional[str] = Form(None),
                     new_component_type: Optional[str] = Form(None),
                     new_service_interval: Optional[str] = Form(None),
                     new_lifetime_expected: Optional[str] = Form(None),
                     new_threshold_km: Optional[str] = Form(None),
                     new_lifetime_expected_days: Optional[str] = Form(None),
                     new_service_interval_days: Optional[str] = Form(None),
                     new_threshold_days: Optional[str] = Form(None),
                     new_cost: Optional[str] = Form(None),
                     new_offset: Optional[int] = Form(0),
                     new_notes: Optional[str] = Form(None)):
    """Endpoint to swap one component with another"""

    if create_new == "true":
        new_component_data = {"component_name": new_component_name,
                              "component_type": new_component_type,
                              "service_interval": new_service_interval,
                              "lifetime_expected": new_lifetime_expected,
                              "threshold_km": new_threshold_km,
                              "lifetime_expected_days": new_lifetime_expected_days,
                              "service_interval_days": new_service_interval_days,
                              "threshold_days": new_threshold_days,
                              "cost": new_cost,
                              "offset": new_offset,
                              "notes": new_notes}

        success, message = business_logic.quick_swap_orchestrator(old_component_id,
                                                                  fate,
                                                                  swap_date,
                                                                  None,
                                                                  new_component_data)

    else:
        success, message = business_logic.quick_swap_orchestrator(old_component_id,
                                                                  fate,
                                                                  swap_date,
                                                                  new_component_id,
                                                                  None)

    return JSONResponse({"success": success, "message": message})

@app.post("/add_collection", response_class=HTMLResponse)
async def add_collection(collection_name: str = Form(...),
                            components: Optional[List[str]] = Form(None),
                            bike_id: Optional[str] = Form(None),
                            comment: Optional[str] = Form(None)):
    """Endpoint to add new collection"""

    success, message = business_logic.create_collection(collection_name,
                                                     components,
                                                     bike_id,
                                                     comment)

    response = RedirectResponse(
        url=f"/component_overview?success={success}&message={message}",
        status_code=303)

    return response

@app.post("/update_collection", response_class=HTMLResponse)
async def update_collection(collection_id: str = Form(...),
                            collection_name: str = Form(...),
                            components: Optional[List[str]] = Form(None),
                            bike_id: Optional[str] = Form(None),
                            comment: Optional[str] = Form(None)):
    """Endpoint to update existing collection"""

    success, message = business_logic.update_collection(collection_id,
                                                        collection_name,
                                                        components,
                                                        bike_id,
                                                        comment)

    response = RedirectResponse(
        url=f"/component_overview?success={success}&message={message}",
        status_code=303)

    return response

@app.post("/change_collection_status")
async def change_collection_status(collection_id: str = Form(...),
                                   new_status: str = Form(...),
                                   updated_date: str = Form(...),
                                   bike_id: Optional[str] = Form(None)):
    """Endpoint to change the status of all components in a collection"""

    success, message = business_logic.change_collection_status(collection_id,
                                                               new_status,
                                                               updated_date,
                                                               bike_id)

    return JSONResponse({"success": success, "message": message})

@app.post("/add_service_record", response_class=HTMLResponse)
async def add_service(component_id: str = Form(...),
                      service_date: str = Form(...),
                      service_description: str = Form(...)):
    """Endpoint to add service"""

    success, message = business_logic.create_service_record(component_id,
                                                            service_date,
                                                            service_description)

    response = RedirectResponse(
        url=f"/component_details/{component_id}?success={success}&message={message}",
        status_code=303)

    return response

@app.post("/update_service_record", response_class=HTMLResponse)
async def update_service_record(component_id: str = Form(...),
                                service_id: str = Form(...),
                                service_date: str = Form(...),
                                service_description: str = Form(...)):
    """Endpoint to update an existing service record"""

    success, message = business_logic.update_service_record(component_id,
                                                            service_id,
                                                            service_date,
                                                            service_description)

    response = RedirectResponse(
        url=f"/component_details/{component_id}?success={success}&message={message}",
        status_code=303)

    return response

@app.post("/add_incident_record", response_class=HTMLResponse)
async def add_incident_record(incident_date: str = Form(...),
                              incident_status: str = Form(...),
                              incident_severity: str = Form(...),
                              incident_affected_component_ids: Optional[List[str]] = Form(None),
                              incident_affected_bike_id: Optional[str] = Form(None),
                              incident_description: Optional[str] = Form(None),
                              resolution_date: Optional[str] = Form(None),
                              resolution_notes: Optional[str] = Form(None)):
    """Endpoint to create an incident record"""

    success, message = business_logic.create_incident_record(incident_date,
                                                             incident_status,
                                                             incident_severity,
                                                             incident_affected_component_ids,
                                                             incident_affected_bike_id,
                                                             incident_description,
                                                             resolution_date,
                                                             resolution_notes)

    response = RedirectResponse(
        url=f"/incident_reports?success={success}&message={message}",
        status_code=303)

    return response

@app.post("/update_incident_record", response_class=HTMLResponse)
async def update_incident_record(incident_id: str = Form(...),
                                 incident_date: str = Form(...),
                                 incident_status: str = Form(...),
                                 incident_severity: str = Form(...),
                                 incident_affected_component_ids: Optional[List[str]] = Form(None),
                                 incident_affected_bike_id: Optional[str] = Form(None),
                                 incident_description: Optional[str] = Form(None),
                                 resolution_date: Optional[str] = Form(None),
                                 resolution_notes: Optional[str] = Form(None)):
    """Endpoint to update an incident record"""

    success, message = business_logic.update_incident_record(incident_id,
                                                             incident_date,
                                                             incident_status,
                                                             incident_severity,
                                                             incident_affected_component_ids,
                                                             incident_affected_bike_id,
                                                             incident_description,
                                                             resolution_date,
                                                             resolution_notes)

    response = RedirectResponse(
        url=f"/incident_reports?success={success}&message={message}",
        status_code=303)

    return response

@app.post("/add_workplan", response_class=HTMLResponse)
async def add_workplan(due_date: str = Form(...),
                       workplan_status: str = Form(...),
                       workplan_size: str = Form(...),
                       workplan_affected_component_ids: Optional[List[str]] = Form(None),
                       workplan_affected_bike_id: Optional[str] = Form(None),
                       workplan_description: Optional[str] = Form(None),
                       completion_date: Optional[str] = Form(None),
                       completion_notes: Optional[str] = Form(None)):
    """Endpoint to create a workplan"""

    success, message = business_logic.create_workplan(due_date,
                                                      workplan_status,
                                                      workplan_size,
                                                      workplan_affected_component_ids,
                                                      workplan_affected_bike_id,
                                                      workplan_description,
                                                      completion_date,
                                                      completion_notes)

    response = RedirectResponse(
        url=f"/workplans?success={success}&message={message}",
        status_code=303)

    return response

@app.post("/update_workplan", response_class=HTMLResponse)
async def update_workplan(workplan_id: str = Form(...),
                          due_date: str = Form(...),
                          workplan_status: str = Form(...),
                          workplan_size: str = Form(...),
                          workplan_affected_component_ids: Optional[List[str]] = Form(None),
                          workplan_affected_bike_id: Optional[str] = Form(None),
                          workplan_description: Optional[str] = Form(None),
                          completion_date: Optional[str] = Form(None),
                          completion_notes: Optional[str] = Form(None)):
    """Endpoint to update a workplan"""

    success, message = business_logic.update_workplan(workplan_id,
                                                      due_date,
                                                      workplan_status,
                                                      workplan_size,
                                                      workplan_affected_component_ids,
                                                      workplan_affected_bike_id,
                                                      workplan_description,
                                                      completion_date,
                                                      completion_notes)

    response = RedirectResponse(
        url=f"/workplans?success={success}&message={message}",
        status_code=303)

    return response

@app.get("/refresh_all_bikes", response_class=HTMLResponse)
async def refresh_all_bikes(request: Request):
    """Endpoint to manually refresh data for all bikes"""

    success, message = await business_logic.refresh_all_bikes()

    return JSONResponse({"success": success,
                         "message": message})

@app.post("/component_types_modify", response_class=HTMLResponse)
async def component_types_modify(component_type: str = Form(...),
                                 expected_lifetime: Optional[str] = Form(None),
                                 lifetime_expected_days: Optional[str] = Form(None),
                                 service_interval: Optional[str] = Form(None),
                                 service_interval_days: Optional[str] = Form(None),
                                 threshold_km: Optional[str] = Form(None),
                                 threshold_days: Optional[str] = Form(None),
                                 mandatory: Optional[str] = Form(None),
                                 max_quantity: Optional[str] = Form(None),
                                 mode: str = Form("create")):
    """Endpoint to modify component types"""

    success, message = business_logic.modify_component_type(component_type,
                                                            expected_lifetime,
                                                            lifetime_expected_days,
                                                            service_interval,
                                                            service_interval_days,
                                                            threshold_km,
                                                            threshold_days,
                                                            mandatory,
                                                            max_quantity,
                                                            mode)

    response = RedirectResponse(
        url=f"/component_types_overview?success={success}&message={message}",
        status_code=303)

    return response


@app.get("/refresh_rides/{mode}", response_class=HTMLResponse)
async def refresh_rides(request: Request, mode: str):
    """Endpoint to refresh data for a subset or all rides"""

    success, message = await business_logic.update_rides_bulk(mode)

    return JSONResponse({"success": success,
                         "message": message})

@app.post("/delete_record", response_class=HTMLResponse)
async def delete_record(record_id: str = Form(...),
                        table_selector: str = Form(...),
                        source_page: str = Form(None)):
    """Endpoint to delete records"""

    success, message, component_id, bike_id = business_logic.delete_record(table_selector, record_id)

    redirect_url = "/"

    if table_selector == "ComponentTypes":
        redirect_url = "/component_types_overview"
    elif table_selector == "Components":
        if source_page == "component_overview":
            redirect_url = "/component_overview"
        elif source_page == "bike_details" and bike_id:
            redirect_url = f"/bike_details/{bike_id}"
        elif source_page == "component_details":
            if bike_id:
                redirect_url = f"/bike_details/{bike_id}"
            else:
                redirect_url = "/component_overview"
        else:
            redirect_url = "/component_overview"
    elif table_selector == "Collections":
        redirect_url = "/component_overview"
    elif table_selector == "Services" or table_selector == "ComponentHistory":
        redirect_url = f"/component_details/{component_id}"
    elif table_selector == "Incidents":
        redirect_url = "/incident_reports"
    elif table_selector == "Workplans":
        redirect_url = "/workplans"

    response = RedirectResponse(
        url=f"{redirect_url}?success={success}&message={message}",
        status_code=303)

    return response

@app.post("/update_config")
async def update_config(request: Request,
                        db_path: str = Form(...),
                        strava_tokens: str = Form(...)):
    """Endpoint to update config file"""

    success, message = write_config(db_path, strava_tokens)

    response = RedirectResponse(
        url=f"/config_overview?success={success}&message={message}",
        status_code=303)

    if success:
        asyncio.create_task(shutdown_server())

    return response

@app.get("/get_filtered_log")
async def get_filtered_log():
    """Endpoint to read log and return only business events""" 

    return read_filtered_logs()
