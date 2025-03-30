#!/usr/bin/env python3
"""Module for auxiliary functions"""

import json
import asyncio
import uuid
import time
import sys
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

def write_config(db_path, strava_tokens):
    """Function to update configuration file"""
    try:
        updated_config = {"db_path": db_path,
                          "strava_tokens": strava_tokens}

        with open('config.json', 'w', encoding='utf-8') as file:
            json.dump(updated_config, file, indent=4)

        return True, f"Configuration updated. New database path is {db_path}. New strava tokens path is {strava_tokens}." 

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
    """Method to generates a random and unique ID"""
    unique_id_part1 = uuid.uuid4()
    unique_id_part2 = time.time()

    return f'{str(unique_id_part1)[:6]}{str(unique_id_part2)[-4:]}'

def format_component_status(status):
    """Method to display user friendly text for None values"""
    if status is not None:
        return status

    return "Not defined"
    
def format_cost(cost):
    """Method to display user friendly text for None values"""
    if cost is not None:
        return cost

    return "No estimate"

def get_component_statistics(component_list):
    """Method to summarise key data for a set of components"""
    component_statistics = {"count_installed": 0,
                            "count_not_installed": 0,
                            "count_retired": 0,
                            "count_lifetime_status_green": 0,
                            "count_lifetime_status_yellow": 0,
                            "count_lifetime_status_red": 0,
                            "count_lifetime_status_purple": 0,
                            "count_lifetime_status_grey": 0,
                            "count_service_status_green": 0,
                            "count_service_status_yellow": 0,
                            "count_service_status_red": 0,
                            "count_service_status_purple": 0,
                            "count_service_status_grey": 0,
                            "sum_cost": 0,
                            }
        
    for component in component_list:
        if component[0] == "Installed":
            component_statistics["count_installed"] += 1
        if component[0] == "Not installed":
            component_statistics["count_not_installed"] += 1
        if component[0] == "Retired":
            component_statistics["count_retired"] += 1
        if component[4] == "OK" and component[0] == "Installed":
            component_statistics["count_lifetime_status_green"] += 1
        if component[4] == "End of life approaching" and component[0] == "Installed":
            component_statistics["count_lifetime_status_yellow"] += 1
        if component[4] == "Due for replacement" and component[0] == "Installed":
            component_statistics["count_lifetime_status_red"] += 1
        if component[4] == "Lifetime exceeded" and component[0] == "Installed":
            component_statistics["count_lifetime_status_purple"] += 1
        if component[4] == "Not defined" and component[0] == "Installed":
            component_statistics["count_lifetime_status_grey"] += 1                
        if component[5] == "OK" and component[0] == "Installed":
            component_statistics["count_service_status_green"] += 1
        if component[5] == "Service approaching" and component[0] == "Installed":
            component_statistics["count_service_status_yellow"] += 1
        if component[5] == "Due for service" and component[0] == "Installed":
            component_statistics["count_service_status_red"] += 1
        if component[5] == "Service interval exceeded" and component[0] == "Installed":
            component_statistics["count_service_status_purple"] += 1
        if component[5] == "Not defined" and component[0] == "Installed":
            component_statistics["count_service_status_grey"] += 1
        if component[6] is not None and isinstance(component[6], int) and component[0] == "Installed":
            if ((component[4] == "Due for replacement" or component[4] == "Lifetime exceeded") or
                (component[5] == "Due for service" or component[5] == "Service interval exceeded")):
                component_statistics["sum_cost"] += component[6]

    if component_statistics["sum_cost"] == 0:
        component_statistics["sum_cost"] = "No estimate"
        
    return component_statistics

def get_formatted_bikes_list(bikes):
    """Method to get list of all bikes, with prefix for retired bikes"""
    bikes_data = [(bike.bike_name + (" (Retired)" if bike.bike_retired == "True" else ""),
                  bike.bike_id)
                  for bike in bikes]
    
    return sorted(bikes_data, key=lambda x: (("(Retired)" in x[0]), x[0].lower()))

def calculate_percentage_reached(total, remaining):
        """Method to calculate remaining service interval or remaining lifetime as percentage"""
        if isinstance(total, int) and isinstance(remaining, int):
            return round(((total - remaining) / total) * 100, 2)
        
        return 1000

def validate_date_format(date_string):
    """Validates that a date string matches the required format YYYY-MM-DD HH:MM"""
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
    """Calculates the number of days between two dates"""
    try:
        start_date = datetime.strptime(start_date, "%Y-%m-%d %H:%M")
        end_date = datetime.strptime(end_date, "%Y-%m-%d %H:%M")
        return True, (end_date - start_date).days
    except ValueError:
        return False, "Failed to calculate elapsed days"