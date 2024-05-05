"""Main backend for velo supervisor 2000"""

from fastapi import FastAPI
from peewee_models import database, Components, Rides

database.connect()

def test():
    """Function to test database connectivity"""
    counter = 0
    try:
        with database.atomic():
            table = Rides.select()
            for component in table:
                print(component.ride_name)
                counter = counter+1

            print(counter)
    except Exception as error:
        print(error)


test()


#app = FastAPI()

