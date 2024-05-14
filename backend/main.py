"""Main backend for velo supervisor 2000"""

from fastapi import FastAPI
from strava import Strava
from peewee_connector import PeeweeConnector
import argparse
import logging

# Configuration of logging - might remove this later
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
    # Include file path to db as argument, also include in git-ignore

    return args





PARAMETERS = read_parameters()
strava = Strava(PARAMETERS.oauth_file)
peewee_connector = PeeweeConnector()






# Endpoint get all rides and recent rides, make it possible also to call with "all" arg
strava.get_rides("recent")
peewee_connector.commit_rides_bulk(strava.payload)

# Endpoints get all bikes (triggered by new rides, and should also be able to call manually)
if len(peewee_connector.list_unique_bikes()) > 0:
    strava.get_bikes(peewee_connector.list_unique_bikes())
    peewee_connector.commit_bikes(strava.payload)

# Code to update installed components distance and moving time (not callable as endpoint).
# Should be trigger by fetching of new rides and when components are added, should also be able to trigger manually with all
# This method should be called by main.
# Method should create a list of component ids to be submitted as arg to function below. Method should support operating on this list, single ID or all components.

peewee_connector.update_components_distance_time("b1997085")

# Code to update misc status fields of components (not callable as endpoint). Should be triggered by updating of installed components
# This method should be called by main

#app = FastAPI()

