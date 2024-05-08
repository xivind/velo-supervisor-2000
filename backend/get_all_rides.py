#!/usr/bin/env python3
"""Module to get activities from Strava and send them on a MQTT broker"""

import json
import logging
from datetime import datetime, timedelta
from requests_oauthlib import OAuth2Session
from peewee_models import database, Rides
import peewee

# Review all doc strings

# Configuration of logging
CONSOLE_HANDLER = logging.StreamHandler()
CONSOLE_HANDLER.setFormatter(logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S"))
logging.getLogger().addHandler(CONSOLE_HANDLER)
logging.getLogger().setLevel(logging.INFO)


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
        self.payload = []
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

    def get_data(self):
        """Method to authenticate and get data from Strava API"""
        page = 1
        raw_response = ""
        self.payload.clear()
        self.token_loader()
        refresh_url = "https://www.strava.com/oauth/token"
        
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
            logging.info(f'Access token valid. Expires at {datetime.fromtimestamp(self.token["expires_at"])},in {datetime.fromtimestamp(self.token["expires_at"]) - datetime.now()}')
            client = OAuth2Session(self.extra["client_id"], token=self.token)
            while True:
                protected_url = f"https://www.strava.com/api/v3/athlete/activities?page={page}&per_page=200"
                raw_response = client.get(protected_url)
                logging.info(f'API status on request for page {page}: {raw_response.status_code} - {raw_response.reason}')
                self.json_response = raw_response.json()
                if (not self.json_response):
                    logging.info(f'Reached last page. The last page with data was page {page-1}')
                    break

                logging.info(f'Page contained {len(self.json_response)} Strava activities')
                page = page+1
                self.prepare_payload()
                health_check("ok", "executing")


        except Exception as error:
            logging.error(f'An error occured during API call: {error}')
            health_check("error", "executing")
    
    def prepare_payload(self):
        """Method to prepare message to be sent via a Mosquitto message broker"""
        
        for activities in self.json_response:

            if str(activities["type"]) == "Ride":

                try:
                    ride = {}
                    ride.update({"ride_id": str(activities["id"])})
                    ride.update({"bike_id": str(activities["gear_id"])})
                    ride.update({"ride_name": str(activities["name"])})
                    
                    ride.update({"record_time": str(activities["start_date_local"]).replace("Z","")})
                    ride.update({"moving_time": str(timedelta(seconds=activities["moving_time"]))})
                    ride.update({"ride_distance": round(float(activities["distance"]/1000),2)})
                    ride.update({"commute": bool(activities["commute"])})

                    self.payload.append(ride)
                    logging.info('Ride info:')
                    logging.info(ride)
                    health_check("ok", "executing")

                except Exception as error:
                    logging.error('An error ocurred preparing payload:')
                    logging.error(self.payload)
                    logging.error(f'More info about the error: {error}')
                    health_check("error", "executing")

            else:
                logging.info("Activity is not of type Ride, skipping...")
                   

class PeeweeConnector():
    """Class to interact with Mosquitto messagebroker"""
    def __init__(self):
        pass

    def commit_data_bulk(self, ride_list):
        """Method to send message via a Mosquitto message broker"""
        print(f'There are {len(ride_list)} rides in the list')
        
        try:
            # Open a transaction
            with database.atomic():
                # Split the data into batches (adjust batch size as needed)
                batch_size = 50
                for i in range(0, len(ride_list), batch_size):
                    batch = ride_list[i:i + batch_size]
                    # Convert the batch of dictionaries into a list of tuples
                    rides_tuples_list = [(d['ride_id'],
                                          d['bike_id'],
                                          d['record_time'],
                                          d['ride_name'],
                                          d['ride_distance'],
                                          d['moving_time'],
                                          d['commute']) for d in batch]
                    
                    # Bulk insert/update the batch using IGNORE conflict resolution
                    Rides.insert_many(rides_tuples_list).on_conflict(
                        conflict_target=[Rides.ride_id],  # Specify the unique constraint to determine conflicts
                        action='IGNORE'  # Use IGNORE conflict resolution strategy
                    ).execute()

                    print("Bikes table updated successfully!")
        
        except peewee.OperationalError as error:
            print("An error occurred while updating the bikes table:", error)
            
        
        






# must have function to add bike and athlete if non-existent
# Export statement
# Returns dictionary of data