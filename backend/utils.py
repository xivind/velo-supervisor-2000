#!/usr/bin/env python3
"""Module for auxiliary functions"""

import json
import asyncio
import logging
import uuid
import time
import sys
import re
from collections import deque
from datetime import datetime, timedelta

def get_formatted_datetime_now():
    """Function to get current datetime formatted as YYYY-MM-DD HH:MM"""
    return datetime.now().strftime("%Y-%m-%d %H:%M")

def get_current_version():
    """Function to get current program version"""
    try:
        with open('current_version.txt', 'r', encoding='utf-8') as file:
            return file.read().strip()
    except FileNotFoundError:
        return "Version unknown"

def read_config():
    """Function to read configuration file"""
    with open('config.json', 'r', encoding='utf-8') as file:
        config = json.load(file)
    return config

def get_button_order(config, page_name):
    """Function to get button order for a specific page with defaults"""
    defaults = {'bike_details': ['new-collection',
                                 'new-component',
                                 'install-existing',
                                 'plan-services',
                                 'complete-services',
                                 'new-workplan',
                                 'new-incident'],
                'component_details': ['view-bike',
                                      'update-status',
                                      'update-details',
                                      'edit-collection',
                                      'quick-swap',
                                      'duplicate',
                                      'new-service',
                                      'plan-services',
                                      'complete-services',
                                      'new-workplan',
                                      'new-incident',
                                      'delete']}

    default_order = defaults.get(page_name, [])
    configured_order = config.get('button_sorting', {}).get(page_name, default_order)

    missing_buttons = [button_id for button_id in default_order if button_id not in configured_order]

    return configured_order + missing_buttons

def get_button_sorting_config(config):
    """Function to get button sorting configuration for config page"""
    default_button_sorting = {'bike_details': ['new-collection',
                                               'new-component',
                                               'install-existing',
                                               'plan-services',
                                               'complete-services',
                                               'new-workplan',
                                               'new-incident'],
                            'component_details': ['view-bike',
                                                  'update-status',
                                                  'update-details',
                                                  'edit-collection',
                                                  'quick-swap',
                                                  'duplicate',
                                                  'new-service',
                                                  'plan-services',
                                                  'complete-services',
                                                  'new-workplan',
                                                  'new-incident',
                                                  'delete']}

    return config.get('button_sorting', default_button_sorting)

def parse_button_sorting(bike_details_json, component_details_json):
    """Function to parse button sorting data from form submission"""
    if not bike_details_json and not component_details_json:
        return None

    button_sorting = {}
    if bike_details_json:
        button_sorting['bike_details'] = json.loads(bike_details_json)
    if component_details_json:
        button_sorting['component_details'] = json.loads(component_details_json)

    return button_sorting

def write_config(form_type, db_path=None, strava_tokens=None, verbose_logging=None,
                 button_sorting_bike_details=None, button_sorting_component_details=None):
    """Function to update configuration file based on which form was submitted"""
    try:
        existing_config = {}
        try:
            existing_config = read_config()
        except (FileNotFoundError, json.JSONDecodeError):
            pass

        updated_config = existing_config.copy()

        if form_type == "file_paths":
            if db_path is not None:
                updated_config["db_path"] = db_path
            if strava_tokens is not None:
                updated_config["strava_tokens"] = strava_tokens
            message = "File paths updated."

        elif form_type == "button_sorting":
            button_sorting = parse_button_sorting(button_sorting_bike_details,
                                                  button_sorting_component_details)
            if button_sorting is not None:
                if "button_sorting" not in updated_config:
                    updated_config["button_sorting"] = {}
                updated_config["button_sorting"].update(button_sorting)
            message = "Button sorting updated."

        elif form_type == "system_settings":
            updated_config["verbose_logging"] = verbose_logging if verbose_logging is not None else False
            message = f"System settings updated. Verbose logging: {'enabled' if updated_config['verbose_logging'] else 'disabled'}."

        else:
            return False, f"Unknown form type: {form_type}"

        if "button_sorting" not in updated_config:
            updated_config["button_sorting"] = {"bike_details": ["new-collection",
                                                                 "new-component",
                                                                 "install-existing",
                                                                 "plan-services",
                                                                 "new-workplan",
                                                                 "new-incident"],
                                                "component_details": ["view-bike",
                                                                      "update-status",
                                                                      "update-details",
                                                                      "edit-collection",
                                                                      "quick-swap",
                                                                      "duplicate",
                                                                      "new-service",
                                                                      "plan-services",
                                                                      "new-workplan",
                                                                      "new-incident",
                                                                      "delete"]}

        with open('config.json', 'w', encoding='utf-8') as file:
            json.dump(updated_config, file, indent=4)

        return True, message

    except OSError as error:
        return False, f"An error occurred updating configuration: {str(error)}"

def read_filtered_logs():
    """Function to get filtered log records"""
    with open('/data/logs/app.log', 'r', encoding='utf-8') as log_file:
        logs = log_file.readlines()

    filtered_logs = [log for log in logs if "GET" not in log and "POST" not in log]
    subset_filtered_logs = filtered_logs[-100:]

    return {"logs": subset_filtered_logs}

class ErrorRecorder(logging.Handler):
    """Logging handler that keeps the most recent error records in memory for the health check"""
    def __init__(self):
        super().__init__()
        self.errors = deque(maxlen=20)

    def emit(self, record):
        """Method to store error records and ignore lower levels. Filters here instead of relying on the handler level,
        since lifespan in main.py resets the level of all root handlers"""
        if record.levelno < logging.ERROR:
            return

        message = record.getMessage()
        if record.exc_info and record.exc_info[1]:
            message = f"{message}: {type(record.exc_info[1]).__name__}: {record.exc_info[1]}"

        self.errors.append((datetime.fromtimestamp(record.created), message))

    def read_recent_errors(self, hours):
        """Method to get error records newer than the given number of hours"""
        cutoff = datetime.now() - timedelta(hours=hours)
        with self.lock:
            return [(error_time, message) for error_time, message in self.errors if error_time >= cutoff]

ERROR_RECORDER = ErrorRecorder()

def get_health_status(database_success, database_message):
    """Function to assess application health from errors logged the last 24 hours and the database check"""
    recent_errors = ERROR_RECORDER.read_recent_errors(24)
    healthy = database_success and not recent_errors

    health_status = {"status": "healthy" if healthy else "unhealthy",
                     "database": database_message,
                     "latest_errors": [{"time": error_time.strftime("%Y-%m-%d %H:%M:%S"),
                                        "message": message[:300]}
                                       for error_time, message in recent_errors[-3:]]}

    return healthy, health_status

async def shutdown_server():
    """Helper function to shutdown the server after a short delay"""
    await asyncio.sleep(2)
    sys.exit(0)

def generate_unique_id():
    """Function to generates a random and unique ID"""
    unique_id_part1 = uuid.uuid4()
    unique_id_part2 = time.time()

    return f'{str(unique_id_part1)[:6]}{str(unique_id_part2)[-4:]}'

def format_component_status(status):
    """Function to display user friendly text for None values"""
    if status is not None:
        return status

    return "Not defined"
    
def format_cost(cost):
    """Function to display user friendly text for None values"""
    if cost is not None:
        return cost

    return "No estimate"

def get_formatted_bikes_list(bikes):
    """Function to get list of all bikes, with prefix for retired bikes"""
    bikes_data = [(bike.bike_name + (" (Retired)" if bike.bike_retired == "True" else ""),
                  bike.bike_id)
                  for bike in bikes]

    return sorted(bikes_data, key=lambda x: (("(Retired)" in x[0]), x[0].lower()))

def derive_workplan_context(services, database_manager):
    """Derive bike, component and progress information for a workplan from its services"""
    bike_ids = []
    bike_names = []
    component_ids = []
    component_names = []
    completed_count = 0
    total_count = 0

    for service in services:
        total_count += 1
        if service.status == "Completed":
            completed_count += 1

        component = database_manager.read_component(service.component_id)
        if service.component_id not in component_ids:
            component_ids.append(service.component_id)
            component_names.append(component.component_name if component else "Deleted component")

        if service.status == "Completed":
            service_bike_id = service.bike_id
        else:
            service_bike_id = component.bike_id if component else None

        if service_bike_id and service_bike_id not in bike_ids:
            bike_ids.append(service_bike_id)
            bike_names.append(database_manager.read_bike_name(service_bike_id))

    return {"bike_ids": bike_ids,
            "bike_names": bike_names,
            "component_ids": component_ids,
            "component_names": component_names,
            "completed_count": completed_count,
            "total_count": total_count}

def get_effective_planned_date(service, workplan):
    """Return the service's own planned date, else the workplan due date, else None"""
    if service.planned_date:
        return service.planned_date

    if workplan and workplan.due_date:
        return workplan.due_date

    return None

def resolve_workplan_title(workplan, component_names, bike_name):
    """Return the name the user gave the workplan, or a generated title when there is none"""
    if workplan.workplan_name and workplan.workplan_name.strip():
        return workplan.workplan_name

    return generate_workplan_title(component_names, bike_name, workplan.workplan_description)

def get_workplan_names_dict(database_manager):
    """Build dictionary mapping workplan_id -> workplan_name for all workplans"""
    workplan_names = {}
    for workplan in database_manager.read_all_workplans():
        context = derive_workplan_context(database_manager.read_services_by_workplan(workplan.workplan_id),
                                          database_manager)
        workplan_names[workplan.workplan_id] = resolve_workplan_title(workplan,
                                                                      context["component_names"],
                                                                      context["bike_names"][0] if context["bike_names"] else None)

    return workplan_names

def build_incident_service_entry(service, database_manager, workplan_names):
    """Describe one service linked to an incident, for the read only list in the incident modal"""
    component = database_manager.read_component(service.component_id)
    workplan = database_manager.read_single_workplan(service.workplan_id) if service.workplan_id else None

    return {"service_id": service.service_id,
            "component_id": service.component_id,
            "component_name": component.component_name if component else "Deleted component",
            "status": service.status,
            "description": service.description,
            "service_date": service.service_date,
            "planned_date": service.planned_date,
            "date": service.service_date if service.status == "Completed" else get_effective_planned_date(service, workplan),
            "workplan_id": service.workplan_id,
            "workplan_name": workplan_names.get(service.workplan_id) if service.workplan_id else None,
            "workplan_status": workplan.workplan_status if workplan else None}

def get_incident_data_tuple(incident, database_manager, workplan_names):
    """Build standard incident data tuple for display (17 fields)"""
    incident_services = list(database_manager.read_services_by_incident(incident.incident_id))
    incident_workplans = []
    for service in incident_services:
        if service.workplan_id and service.workplan_id not in [workplan_id for workplan_id, _ in incident_workplans]:
            incident_workplans.append((service.workplan_id, workplan_names.get(service.workplan_id, None)))

    return (incident.incident_id,
            incident.incident_date,
            incident.incident_status,
            incident.incident_severity,
            parse_json_string(incident.incident_affected_component_ids),
            database_manager.read_component_names(incident.incident_affected_component_ids),
            incident.incident_affected_bike_id,
            database_manager.read_bike_name(incident.incident_affected_bike_id),
            incident.incident_description,
            incident.resolution_date,
            incident.resolution_notes,
            calculate_elapsed_days(incident.incident_date,
                                   incident.resolution_date if incident.resolution_date else get_formatted_datetime_now())[1],
            generate_incident_title(database_manager.read_component_names(incident.incident_affected_component_ids),
                                    database_manager.read_bike_name(incident.incident_affected_bike_id),
                                    incident.incident_description),
            incident_workplans,
            sum(1 for service in incident_services if service.status == "Planned"),
            sum(1 for service in incident_services if service.status == "Completed"),
            [build_incident_service_entry(service, database_manager, workplan_names)
             for service in incident_services])

def get_service_incident_options(database_manager):
    """Build incident options for the service modal (4 fields), all incidents so linked resolved ones keep their title"""
    return [(incident.incident_id,
             generate_incident_title(database_manager.read_component_names(incident.incident_affected_component_ids),
                                     database_manager.read_bike_name(incident.incident_affected_bike_id),
                                     incident.incident_description),
             incident.incident_status,
             parse_json_string(incident.incident_affected_component_ids) or [])
            for incident in database_manager.read_all_incidents()]

def get_workplan_data_tuple(workplan, database_manager):
    """Build standard workplan data tuple for display (14 fields)"""
    context = derive_workplan_context(database_manager.read_services_by_workplan(workplan.workplan_id),
                                      database_manager)
    service_progress = ({"completed": context["completed_count"], "total": context["total_count"]}
                        if context["total_count"] > 0 else None)

    return (workplan.workplan_id,
            workplan.due_date,
            workplan.workplan_status,
            workplan.workplan_size,
            context["component_ids"],
            context["component_names"],
            context["bike_ids"],
            context["bike_names"],
            workplan.workplan_description,
            workplan.completion_date,
            workplan.completion_notes,
            calculate_elapsed_days(workplan.due_date,
                                   workplan.completion_date if workplan.completion_date else get_formatted_datetime_now())[1],
            resolve_workplan_title(workplan,
                                   context["component_names"],
                                   context["bike_names"][0] if context["bike_names"] else None),
            service_progress)

def get_planned_service_data_tuple(service, database_manager, workplan_names):
    """Build standard planned service tuple for display (11 fields)"""
    workplan = database_manager.read_single_workplan(service.workplan_id) if service.workplan_id else None
    component = database_manager.read_component(service.component_id)
    oldest_history_record = database_manager.read_oldest_history_record(service.component_id)

    return (service.service_id,
            service.component_id,
            component.component_name if component else "Deleted component",
            service.description,
            service.workplan_id,
            workplan_names.get(service.workplan_id, None) if service.workplan_id else None,
            service.incident_id,
            get_effective_planned_date(service, workplan),
            service.planned_date,
            component.installation_status if component else "Deleted",
            oldest_history_record.updated_date if oldest_history_record else None)

def calculate_percentage_reached(total, remaining):
    """Function to calculate remaining service interval or remaining lifetime as percentage"""
    if isinstance(total, int) and isinstance(remaining, int):
        return round(((total - remaining) / total) * 100, 2)

    return 1000

def validate_date_format(date_string):
    """Function to validate that a date string matches the required format YYYY-MM-DD HH:MM"""
    if date_string is None:
        return False, "Date cannot be empty. Expected format: YYYY-MM-DD HH:MM (e.g., 2024-12-14 23:34)"

    if not date_string:
        return False, "Date cannot be empty. Expected format: YYYY-MM-DD HH:MM (e.g., 2024-12-14 23:34)"

    if date_string != date_string.strip():
        return False, f"Date '{date_string}' contains leading or trailing whitespace. Expected format: YYYY-MM-DD HH:MM (e.g., 2024-12-14 23:34)"

    if len(date_string) != 16:
        return False, f"Invalid date format: '{date_string}'. Expected format: YYYY-MM-DD HH:MM (e.g., 2024-12-14 23:34)"

    if (date_string[4] != '-' or date_string[7] != '-' or
        date_string[10] != ' ' or date_string[13] != ':'):
        return False, f"Invalid date format: '{date_string}'. Expected format: YYYY-MM-DD HH:MM (e.g., 2024-12-14 23:34)"

    for i, char in enumerate(date_string):
        if i in [4, 7, 10, 13]:
            continue
        if not char.isdigit():
            return False, f"Invalid date format: '{date_string}'. Expected format: YYYY-MM-DD HH:MM (e.g., 2024-12-14 23:34)"

    try:
        datetime.strptime(date_string, "%Y-%m-%d %H:%M")
        return True, "Date format is valid"
    except ValueError:
        return False, f"Invalid date: '{date_string}'. The date provided is invalid or does not match the expected format (YYYY-MM-DD HH:MM)"

def calculate_elapsed_days(start_date, end_date):
    """Function to calculate the number of days between two dates"""
    try:
        start_date = datetime.strptime(start_date, "%Y-%m-%d %H:%M")
        end_date = datetime.strptime(end_date, "%Y-%m-%d %H:%M")
        return True, (end_date - start_date).days
    except ValueError:
        return False, "Failed to calculate elapsed days"

def parse_json_string(raw_json_string):
    """Function to load a JSON string and return the parsed data as a python object"""
    if raw_json_string is None:
        return None

    return json.loads(raw_json_string)

def generate_incident_title(affected_component_names, affected_bike_name, incident_description):
    """Generate a concise title for an incident"""

    title_parts = []

    if affected_component_names and affected_component_names != ["Not assigned"]:
        component_part = affected_component_names[0]
        if len(affected_component_names) > 1:
            component_part += f" (+{len(affected_component_names) - 1} more)"
        title_parts.append(component_part)

    if incident_description and incident_description.strip():
        desc_words = incident_description.split()[:4]
        desc_part = " ".join(desc_words)
        if len(incident_description.split()) > 4:
            desc_part += "..."
        title_parts.append(desc_part)

    if affected_bike_name and affected_bike_name != "Not assigned":
        title_parts.append(affected_bike_name)

    title = " - ".join(title_parts) if title_parts else "No incident metadata"

    return title[:60] + "..." if len(title) > 80 else title

def generate_workplan_title(affected_component_names, affected_bike_name, workplan_description):
    """Generate a concise title for a workplan"""
    title_parts = []

    if affected_component_names and affected_component_names != ["Not assigned"]:
        component_part = affected_component_names[0]
        if len(affected_component_names) > 1:
            component_part += f" (+{len(affected_component_names) - 1} more)"
        title_parts.append(component_part)

    if workplan_description and workplan_description.strip():
        clean_desc = strip_markdown_syntax(workplan_description)
        desc_words = clean_desc.split()[:4]
        desc_part = " ".join(desc_words)
        if len(clean_desc.split()) > 4:
            desc_part += "..."
        title_parts.append(desc_part)

    if affected_bike_name and affected_bike_name != "Not assigned":
        title_parts.append(affected_bike_name)

    title = " - ".join(title_parts) if title_parts else "No workplan metadata"

    return title[:60] + "..." if len(title) > 80 else title

def strip_markdown_syntax(text):
    """Strip markdown syntax from text to produce clean plain text"""
    if not text:
        return ""

    clean_text = text

    clean_text = re.sub(r'!\[([^\]]*)\]\([^\)]+\)', '', clean_text)
    clean_text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', clean_text)
    clean_text = re.sub(r'```[a-z]*\n?(.+?)\n?```', r'\1', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'`([^`]+)`', r'\1', clean_text)
    clean_text = re.sub(r'~~(.+?)~~', r'\1', clean_text)
    clean_text = re.sub(r'\*\*(.+?)\*\*', r'\1', clean_text)
    clean_text = re.sub(r'__(.+?)__', r'\1', clean_text)
    clean_text = re.sub(r'\*([^\*]+)\*', r'\1', clean_text)
    clean_text = re.sub(r'\b_([^_]+)_\b', r'\1', clean_text)
    clean_text = re.sub(r'^#{1,6}\s+', '', clean_text, flags=re.MULTILINE)
    clean_text = re.sub(r'^>\s*', '', clean_text, flags=re.MULTILINE)
    clean_text = re.sub(r'^(\s*[-*_]\s*){3,}$', '', clean_text, flags=re.MULTILINE)
    clean_text = re.sub(r'^[\s]*-\s*\[[x ]\]\s*', '', clean_text, flags=re.MULTILINE)
    clean_text = re.sub(r'^[\s]*[-*+]\s+', '', clean_text, flags=re.MULTILINE)
    clean_text = re.sub(r'^[\s]*\d+\.\s+', '', clean_text, flags=re.MULTILINE)
    clean_text = re.sub(r'\|', ' ', clean_text)
    clean_text = re.sub(r'\\(.)', r'\1', clean_text)
    clean_text = re.sub(r'\s+', ' ', clean_text)
    
    clean_text = clean_text.strip()

    return clean_text
