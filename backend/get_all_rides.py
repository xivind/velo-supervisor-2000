#!/usr/bin/env python3
"""Module to get activities from Strava and send them on a MQTT broker"""

import json
import time
import logging
from datetime import datetime, timedelta
import argparse
from requests_oauthlib import OAuth2Session
from icecream import ic

ic.enable()

# Configuration of logging
CONSOLE_HANDLER = logging.StreamHandler()
CONSOLE_HANDLER.setFormatter(logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S"))
logging.getLogger().addHandler(CONSOLE_HANDLER)
logging.getLogger().setLevel(logging.INFO)


def read_parameters():
    """
    Function for reading variables for the script,
    for more on argparse, refer to https://zetcode.com/python/argparse/
    """
    parser = argparse.ArgumentParser(
        description="Configuration parameters")
    parser.add_argument("--oauth_file", type=str,
                        help="File with oauth user data", required=True)
    args = parser.parse_args()

    return args


def health_check(status, mode):
    """Function to write healthcheck data"""
    if mode == "reset":
        with open("status.txt", "w", encoding='utf-8') as file:
            file.write(status)

    if mode == "executing":
        with open("status.txt", "a", encoding='utf-8') as file:
            file.write(status + "\n")


class Strava:
    """Class to interact with Strava API"""
    def __init__(self, oauth_file):
        self.token = {}
        self.extra = {}
        self.json_response = ""
        self.oauth_file = oauth_file

    def token_loader(self):
        """Method to read oauth options from file"""
        with open(self.oauth_file, 'r', encoding='utf-8') as file:
            secrets_input = json.load(file)
        self.token = {
             'access_token': secrets_input['access_token'],
             'refresh_token': secrets_input['refresh_token'],
             'token_type': secrets_input['token_type'],
             'expires_at': secrets_input['expires_at']

        }
        self.extra = {
            'client_id': secrets_input['client_id'],
            'client_secret': secrets_input['client_secret']
        }

    def token_saver(self):
        """Method to save oauth options to file"""
        secrets_output = self.token
        secrets_output['client_id'] = self.extra["client_id"]
        secrets_output['client_secret'] = self.extra["client_secret"]
        with open(self.oauth_file,'w', encoding='utf-8') as file:
            file.write(json.dumps(secrets_output))

    def get_data(self):
        """Method to authenticate and get data from Strava API"""
        self.token_loader()
        before_date_epoch = (datetime.now() + timedelta(days=1)).timestamp()
        after_date_epoch = (datetime.now() - timedelta(days=3)).timestamp()
        refresh_url = "https://www.strava.com/oauth/token"
        protected_url = f"https://www.strava.com/api/v3/athlete/activities?page=20&per_page=200"

        if self.token["expires_at"] < datetime.now().timestamp():
            logging.info(f'Access token expired at {datetime.fromtimestamp(self.token["expires_at"])}. Refreshing tokens')

            try:
                client = OAuth2Session(self.extra["client_id"], token=self.token)
                self.token = client.refresh_token(refresh_url, refresh_token=self.token["refresh_token"], **self.extra)
                self.token_saver()
                self.token_loader()
                health_check("ok", "executing")

            except Exception as error:
                logging.error(f'An error occured refreshing tokens: {error}')
                health_check("error", "executing")

        try:
            logging.info(f'Access token valid. Expires at {datetime.fromtimestamp(self.token["expires_at"])}, in {datetime.fromtimestamp(self.token["expires_at"]) - datetime.now()}')
            client = OAuth2Session(self.extra["client_id"], token=self.token)
            raw_response = client.get(protected_url)
            logging.info(f'API Status: {raw_response.status_code} - {raw_response.reason}')
            logging.info(f'Fetched Strava activities after {datetime.fromtimestamp(after_date_epoch).strftime("%d.%m.%Y")} and before {datetime.fromtimestamp(before_date_epoch).strftime("%d.%m.%Y")}')
            self.json_response = ic(raw_response.json())
            health_check("ok", "executing")

        except Exception as error:
            logging.error(f'An error occured during API call: {error}')
            health_check("error", "executing")


class DataStore():
    """Class to interact with Mosquitto messagebroker"""
    def __init__(self):
        self.payload = {}
        self.message = ""

    def prepare_payload(self):
        """Method to prepare message to be sent via a Mosquitto message broker"""
        activity_counter = 0
        for activities in strava.json_response:

            try:
                self.payload.clear()
                self.payload.update({"id": int(activities["id"])})
                self.payload.update({"gear_id": str(activities["gear_id"])})
                self.payload.update({"name": str(activities["name"])})
                self.payload.update({"type": str(activities["type"])})
                self.payload.update({"start_date_local": str(activities["start_date_local"]).replace("Z","")})
                self.payload.update({"moving_time": str(timedelta(seconds=activities["moving_time"]))})
                self.payload.update({"distance": round(float(activities["distance"]/1000),2)})
                self.payload.update({"commute": bool(activities["commute"])})

                activity_counter = 1 + activity_counter

                self.update_payload()
                logging.info('Updated payload:')
                logging.info(self.payload)
                health_check("ok", "executing")

            except Exception as error:
                logging.error('An error ocurred preparing payload:')
                logging.error(self.payload)
                logging.error(f'More info about the error: {error}')
                health_check("error", "executing")

        logging.info(f'Got {len(strava.json_response)} Strava activities')
        logging.info(f'Sent {activity_counter} Strava activities')

    def update_payload(self):
        """Method to send message via a Mosquitto message broker"""
        #self.message = print(strava)


logging.info('Starting program...')
PARAMETERS = read_parameters()
strava = Strava(PARAMETERS.oauth_file)
datastore = DataStore()
strava.get_data()
datastore.prepare_payload()

# must have function to add bike and athlete if non-existent

# Returns dictionary of data