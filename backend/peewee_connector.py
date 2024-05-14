#!/usr/bin/env python3
"""Module to interact with a SQL database through peewee"""

import logging
from datetime import datetime
from peewee_models import database, Rides, Bikes, Components
import peewee

# Implement health check

class PeeweeConnector():
    """Class to interact with a SQL database through peewee"""
    def __init__(self):
        pass #Check out this one.. 

    def commit_rides_bulk(self, ride_list):
        """Method to commit ride data in bulk to database"""
        logging.info(f'There are {len(ride_list)} rides in the list')

        try:
            with database.atomic():
                batch_size = 50
                for i in range(0, len(ride_list), batch_size):
                    batch = ride_list[i:i + batch_size]
                    rides_tuples_list = [(dictionary['ride_id'],
                                          dictionary['bike_id'],
                                          dictionary['record_time'],
                                          dictionary['ride_name'],
                                          dictionary['ride_distance'],
                                          dictionary['moving_time'],
                                          dictionary['commute'])
                                         for dictionary in batch]

                    Rides.insert_many(rides_tuples_list).on_conflict(
                        conflict_target=[Rides.ride_id],
                        action='IGNORE'
                    ).execute()

                    logging.info("Rides table updated successfully")

        except peewee.OperationalError as error:
            logging.error(f"An error occurred while updating the rides table: {error}")

    def commit_bikes(self, bike_list):
        """Method to commit bike data to the database"""
        try:
            with database.atomic():
                for bike_data in bike_list:
                    existing_bike = Bikes.get_or_none(Bikes.bike_id == bike_data["bike_id"])

                    if existing_bike:
                        filtered_bike_data = {key: value for key, value in bike_data.items() if key != 'bike_id'}
                        query = Bikes.update(**filtered_bike_data).where(Bikes.bike_id == bike_data["bike_id"])
                        query.execute()
                        logging.info(f'Record for bike with id {bike_data["bike_id"]} updated')

                    else:
                        query = Bikes.insert(**bike_data)
                        query.execute()
                        logging.info(f'Record for bike with id {bike_data["bike_id"]} inserted')

        except peewee.OperationalError as error:
            logging.error(f'An error occurred while updating the bikes table: {error}')

    def list_unique_bikes(self):
        """Method to query database and create list of unique bike ids"""
        try:
            unique_bike_ids = Rides.select(Rides.bike_id).distinct()
            bike_id_list = [
                ride.bike_id
                for ride in unique_bike_ids 
                if ride.bike_id != "None"]
            
            return bike_id_list

        except peewee.OperationalError as error:
            logging.error(f"An error occurred while creating list of unique bike_ids: {error}")
            return []
    
    def transform_dates(self):
        """..."""
        pass #Should process only dates, not time

    def update_components_distance_time(self, delimiter):
        """Method to update component table with distance and time from ride table"""
        try: # Make if statement, to deal with params in delimiter; all, list of bikes, or specific component id
            
            if delimiter == "all":
                with database.atomic():
                    for component in Components.select().where(Components.installation_status == 'Installed'): #bike_id in set?
                        print("Loop enter all")
                        if component.updated_date:
                            updated_date = datetime.strptime(component.updated_date, '%Y-%m-%dT%H:%M:%S')
                        else:
                            updated_date = None
                        
                        # Fetch the record_time value from the query result
                        record_time_query = Rides.select(Rides.record_time).where(Rides.bike_id == component.bike_id)
                        record_time_value = record_time_query.scalar()  # Get the value from the query result
                        record_time = datetime.strptime(record_time_value, '%Y-%m-%dT%H:%M:%S') if record_time_value else None

                        # Filter rides based on the condition record_time >= updated_date
                        matching_rides = Rides.select().where(
                            (Rides.bike_id == component.bike_id) &
                            (Rides.record_time >= updated_date)
                        )
                        
                        distance_offset = Components.get(Components.component_id == component.component_id).component_distance_offset
                        total_distance_current = sum(ride.ride_distance for ride in matching_rides)
                        total_distance = total_distance_current + distance_offset
                        
                        
                        # Update component_distance and component_moving_time only if there are matching rides
                        if matching_rides.exists() and record_time:
                            component.component_distance = total_distance
                            component.save()
                            # Call function here to calculate service and so on
            
            if isinstance(delimiter, set):
                with database.atomic():
                    for bike_id in delimiter:
                        for component in Components.select().where((Components.installation_status == 'Installed') & (Components.bike_id == bike_id)):
                            print("Loop enter set")
                            if component.updated_date:
                                updated_date = datetime.strptime(component.updated_date, '%Y-%m-%dT%H:%M:%S')
                            else:
                                updated_date = None
                            
                            # Fetch the record_time value from the query result
                            record_time_query = Rides.select(Rides.record_time).where(Rides.bike_id == component.bike_id)
                            record_time_value = record_time_query.scalar()  # Get the value from the query result
                            record_time = datetime.strptime(record_time_value, '%Y-%m-%dT%H:%M:%S') if record_time_value else None

                            # Filter rides based on the condition record_time >= updated_date
                            matching_rides = Rides.select().where(
                                (Rides.bike_id == component.bike_id) &
                                (Rides.record_time >= updated_date)
                            )
                            
                            distance_offset = Components.get(Components.component_id == component.component_id).component_distance_offset
                            total_distance_current = sum(ride.ride_distance for ride in matching_rides)
                            total_distance = total_distance_current + distance_offset
                            
                            
                            # Update component_distance and component_moving_time only if there are matching rides
                            if matching_rides.exists() and record_time:
                                component.component_distance = total_distance
                                component.save()
                                # Call function here to calculate service and so on
            
            if "b" in delimiter:
                with database.atomic():
                    for component in Components.select().where((Components.installation_status == 'Installed') & (Components.bike_id == delimiter)):
                        print("Loop enter single")
                        if component.updated_date:
                            updated_date = datetime.strptime(component.updated_date, '%Y-%m-%dT%H:%M:%S')
                        else:
                            updated_date = None
                        
                        # Fetch the record_time value from the query result
                        record_time_query = Rides.select(Rides.record_time).where(Rides.bike_id == component.bike_id)
                        record_time_value = record_time_query.scalar()  # Get the value from the query result
                        record_time = datetime.strptime(record_time_value, '%Y-%m-%dT%H:%M:%S') if record_time_value else None

                        # Filter rides based on the condition record_time >= updated_date
                        matching_rides = Rides.select().where(
                            (Rides.bike_id == component.bike_id) &
                            (Rides.record_time >= updated_date)
                        )
                        
                        distance_offset = Components.get(Components.component_id == component.component_id).component_distance_offset
                        total_distance_current = sum(ride.ride_distance for ride in matching_rides)
                        total_distance = total_distance_current + distance_offset
                        
                        
                        # Update component_distance and component_moving_time only if there are matching rides
                        if matching_rides.exists() and record_time:
                            component.component_distance = total_distance
                            component.save()
                            # Call function here to calculate service and so on 

        
        # there is a problem with performance, use bulk instead, add one except to each if above, and make this one for all
        except (peewee.OperationalError, ValueError) as error:
            logging.error(f'An error occurred while updating the components table with distance and time: {error}')

        
# Find a way to handle the offset value, it should not always be added..