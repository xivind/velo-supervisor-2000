#!/usr/bin/env python3
"""Module to interact with Strava APIs"""

import json
import logging
from datetime import datetime, timedelta
from requests_oauthlib import OAuth2Session

def health_check(status, mode): #Remove this function entirely, will not use
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
        self.payload_bikes = []
        self.payload_rides = []
        self.bike_ids_recent_rides = set()
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
        with open(self.oauth_file, 'w', encoding='utf-8') as file:
            file.write(json.dumps(secrets_output))

    async def get_rides(self, mode):
        """Method to authenticate and get data from Stravas activities API"""
        page = 1
        raw_response = ""
        self.bike_ids_recent_rides.clear()
        self.payload_rides.clear()
        self.token_loader()
        refresh_url = "https://www.strava.com/oauth/token"

        if self.token["expires_at"] < datetime.now().timestamp():
            logging.info(f'Access token expired at {datetime.fromtimestamp(self.token["expires_at"])}. Refreshing tokens.')

            try:
                client = OAuth2Session(self.extra["client_id"], token=self.token)
                self.token = client.refresh_token(refresh_url, refresh_token=self.token["refresh_token"], **self.extra)
                self.token_saver()
                self.token_loader()
                health_check("ok", "executing")

            except Exception as error:
                logging.error(f'An error occured refreshing tokens: {error}.')
                health_check("error", "executing")

        try:
            logging.info(f'Access token valid. Expires at {datetime.fromtimestamp(self.token["expires_at"])},in {datetime.fromtimestamp(self.token["expires_at"]) - datetime.now()}.')
            client = OAuth2Session(self.extra["client_id"], token=self.token)

            if mode == "all":
                while True:
                    protected_url = f"https://www.strava.com/api/v3/athlete/activities?page={page}&per_page=200"
                    raw_response = client.get(protected_url)
                    self.json_response = raw_response.json()

                    if not self.json_response:
                        logging.info(f'Reached last page. The last page with data was page {page-1}.')
                        break

                    logging.info(f'API status for page {page}: {raw_response.status_code} - {raw_response.reason}.')
                    logging.info(f'Page contained {len(self.json_response)} activities.')
                    page = page+1
                    self.prepare_payload_rides()
                    health_check("ok", "executing")

            if mode == "recent":
                protected_url = "https://www.strava.com/api/v3/athlete/activities?page=1&per_page=200"
                raw_response = client.get(protected_url)
                self.json_response = raw_response.json()
                logging.info(f'API status for page {page}: {raw_response.status_code} - {raw_response.reason}')
                logging.info(f'Page contained {len(self.json_response)} activities')
                self.prepare_payload_rides()
                health_check("ok", "executing")
                
                for activity in self.json_response:
                    if str(activity["type"]) == "Ride" and activity["gear_id"] != None:
                        self.bike_ids_recent_rides.add(activity["gear_id"])
                logging.info(f'Found {len(self.bike_ids_recent_rides)} bikes in recent rides.')

        except Exception as error:
            logging.error(f'An error occured during the API call to fetch rides: {error}.')
            health_check("error", "executing")

    async def get_bikes(self, bike_ids):
        """Method to authenticate and get data from Stravas gear API"""
        raw_response = ""
        self.payload_bikes.clear()
        self.token_loader()
        refresh_url = "https://www.strava.com/oauth/token"

        if self.token["expires_at"] < datetime.now().timestamp():
            logging.info(f'Access token expired at {datetime.fromtimestamp(self.token["expires_at"])}. Refreshing tokens.')

            try:
                client = OAuth2Session(self.extra["client_id"], token=self.token)
                self.token = client.refresh_token(refresh_url, refresh_token=self.token["refresh_token"], **self.extra)
                self.token_saver()
                self.token_loader()
                health_check("ok", "executing")

            except Exception as error:
                logging.error(f'An error occured refreshing tokens: {error}.')
                health_check("error", "executing")

        try:
            logging.info(f'Access token valid. Expires at {datetime.fromtimestamp(self.token["expires_at"])},in {datetime.fromtimestamp(self.token["expires_at"]) - datetime.now()}.')
            client = OAuth2Session(self.extra["client_id"], token=self.token)

            logging.info(f"Retrieving data for {len(bike_ids)} bikes")
            for bike in bike_ids:
                protected_url = f"https://www.strava.com/api/v3/gear/{bike}?page=1&per_page=50"
                raw_response = client.get(protected_url)
                self.json_response = raw_response.json()

                if self.json_response:
                    logging.info(f'API status for request: {raw_response.status_code} - {raw_response.reason}.')
                    self.prepare_payload_bikes()
                    health_check("ok", "executing")

                if not self.json_response:
                    logging.info(f'API returned {len(self.json_response)} bikes.')


        except Exception as error:
            logging.error(f'An error occured during the API call to fetch bikes: {error}.')
            health_check("error", "executing")

    def prepare_payload_rides(self):
        """Method to prepare a list of rides"""

        for activities in self.json_response:

            if str(activities["type"]) == "Ride":

                try:
                    ride = {}
                    ride.update({"ride_id": str(activities["id"])})
                    ride.update({"bike_id": str(activities["gear_id"])})
                    ride.update({"ride_name": str(activities["name"])})
                    ride.update({"record_time": datetime.strptime(activities["start_date_local"], "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d %H:%M")})
                    ride.update({"moving_time": str(timedelta(seconds=activities["moving_time"]))})
                    ride.update({"ride_distance": float(activities["distance"]/1000)})
                    ride.update({"commute": bool(activities["commute"])})

                    self.payload_rides.append(ride)
                    logging.info(f'Ride data written to list: {ride}.')
                    health_check("ok", "executing")

                except Exception as error:
                    logging.error(f'An error ocurred preparing payload for rides: {self.payload_rides}')
                    logging.error(f'More info about the error: {error}.')
                    health_check("error", "executing")

            else:
                logging.info("Activity is not of type Ride. Skipping.")

    def prepare_payload_bikes(self):
        """Method to prepare a list of bikes"""

        try:
            bike = {}
            bike.update({"bike_id": str(self.json_response["id"])})
            bike.update({"bike_name": str(self.json_response["name"])})
            bike.update({"bike_retired": bool(self.json_response["retired"])})
            bike.update({"total_distance": self.json_response["converted_distance"]})
            bike.update({"notes": str(self.json_response["description"])})

            self.payload_bikes.append(bike)
            logging.info(f'Bike data written to list: {bike}.')
            health_check("ok", "executing")

        except Exception as error:
            logging.error(f'An error ocurred preparing payload for bikes: {self.payload_bikes}')
            logging.error(f'More info about the error: {error}.')
            health_check("error", "executing")
