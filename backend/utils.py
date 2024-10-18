#!/usr/bin/env python3
"""Module with auxiliary functions"""

import json
import logging
import httpx
import asyncio
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

async def pull_strava_background(mode): #Move to strava module
    """Function to pull data from Strava in the background"""
    while True:
        try:
            logging.info(f"Retrieving rides from Strava as background task. Mode set to: {mode}")
            async with httpx.AsyncClient() as client:
                pass #Remove this before deploy
                # await client.get(f"http://localhost:8000/refresh_rides/{mode}") Activate before deploying

        except Exception as error:
            logging.error(f"An error occured calling refresh rides endpoint: {error}")

        logging.info("Next pull from Strava is in two hours")
        await asyncio.sleep(7200)
