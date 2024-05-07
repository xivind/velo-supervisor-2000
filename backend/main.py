"""Main backend for velo supervisor 2000"""

from fastapi import FastAPI
from peewee_models import database, Rides, Bikes
import peewee

database.connect()





app = FastAPI()

