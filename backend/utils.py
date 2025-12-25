#!/usr/bin/env python3
"""Module for auxiliary functions"""

import json
import asyncio
import uuid
import time
import sys
import re
from datetime import datetime

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
                                 'new-workplan',
                                 'new-incident'],
                'component_details': ['view-bike',
                                      'update-status',
                                      'update-details',
                                      'edit-collection',
                                      'quick-swap',
                                      'duplicate',
                                      'new-service',
                                      'new-workplan',
                                      'new-incident',
                                      'delete']}

    return config.get('button_sorting', {}).get(page_name, defaults.get(page_name, []))

def get_button_sorting_config(config):
    """Function to get button sorting configuration for config page"""
    default_button_sorting = {'bike_details': ['new-collection',
                                               'new-component',
                                               'install-existing',
                                               'new-workplan',
                                               'new-incident'],
                            'component_details': ['view-bike',
                                                  'update-status',
                                                  'update-details',
                                                  'edit-collection',
                                                  'quick-swap',
                                                  'duplicate',
                                                  'new-service',
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
                                                                 "new-workplan",
                                                                 "new-incident"],
                                                "component_details": ["view-bike",
                                                                      "update-status",
                                                                      "update-details",
                                                                      "edit-collection",
                                                                      "quick-swap",
                                                                      "duplicate",
                                                                      "new-service",
                                                                      "new-workplan",
                                                                      "new-incident",
                                                                      "delete"]}

        with open('config.json', 'w', encoding='utf-8') as file:
            json.dump(updated_config, file, indent=4)

        return True, message

    except OSError as error:
        return False, f"An error occured updating configuration: {str(error)}"

def read_filtered_logs():
    """Function to get filtered log records"""
    with open('/data/logs/app.log', 'r', encoding='utf-8') as log_file:
        logs = log_file.readlines()

    filtered_logs = [log for log in logs if "GET" not in log and "POST" not in log]
    subset_filtered_logs = filtered_logs[-100:]

    return {"logs": subset_filtered_logs}

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
        title_parts.append(f"({affected_bike_name})")

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
        clean_desc = workplan_description.replace('**', '').replace('*', '') \
                                       .replace('##', '').replace('#', '') \
                                       .replace('- [ ]', '').replace('- [x]', '') \
                                       .replace('`', '')
        desc_words = clean_desc.split()[:4]
        desc_part = " ".join(desc_words)
        if len(clean_desc.split()) > 4:
            desc_part += "..."
        title_parts.append(desc_part)

    if affected_bike_name and affected_bike_name != "Not assigned":
        title_parts.append(f"({affected_bike_name})")

    title = " - ".join(title_parts) if title_parts else "No workplan metadata"

    return title[:60] + "..." if len(title) > 80 else title

def parse_checkbox_progress(description):
    """Parse checkbox progress from markdown description"""
    if not description:
        return None

    total_checkboxes = len(re.findall(r'- \[[x ]\]', description))
    checked_checkboxes = len(re.findall(r'- \[x\]', description))

    if total_checkboxes > 0:
        return {'total': total_checkboxes,
                'checked': checked_checkboxes,
                'percentage': round((checked_checkboxes / total_checkboxes) * 100)}

    return None
