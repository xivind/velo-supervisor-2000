#!/usr/bin/env python3
"""Module with auxiliary functions"""

import json
from datetime import datetime

def get_current_version():
    """Function to get current program version"""
    try:
        with open('current_version.txt', 'r', encoding='utf-8') as file:
            return file.read().strip()
    except FileNotFoundError:
        return "Version unknown"

def read_parameters():
    """Function to read configuration file"""
    with open('config.json', 'r', encoding='utf-8') as file:
        config = json.load(file)
    return config

def set_time_strava_last_pull(app, read_records):
    """
    Function to set the date for last pull from Strava
    Args:
        app: FastAPI application instance
        read_records: ReadRecords instance for database access
    """
    if app.state.strava_last_pull:
        days_since = (datetime.now() - app.state.strava_last_pull).days
        app.state.strava_last_pull = app.state.strava_last_pull.strftime("%Y-%m-%d %H:%M")
        app.state.strava_days_since_last_pull = days_since
    
    elif app.state.strava_last_pull is None and read_records.read_latest_ride_record():
        app.state.strava_last_pull = datetime.strptime(read_records.read_latest_ride_record().record_time, "%Y-%m-%d %H:%M")
        app.state.strava_days_since_last_pull = (datetime.now() - app.state.strava_last_pull).days

    else:
        app.state.strava_last_pull = "never"
        app.state.strava_days_since_last_pull = None
