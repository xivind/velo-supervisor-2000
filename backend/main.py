"""Main backend for velo supervisor 2000"""

from fastapi import FastAPI
from peewee_models import database, Components, Rides

database.connect()

def test1():
    """Function to test database connectivity"""
    counter = 0
    try:
        with database.atomic():
            table_data = Rides.select().where(Rides.ride_distance > 200)
            for component in table_data:
                print(component.ride_name)
                counter = counter+1

            print(counter)
    except Exception as error:
        print(error)


test1()


#app = FastAPI()

