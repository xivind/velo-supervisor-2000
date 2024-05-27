#!/usr/bin/env python3
"""Module to interact with a SQL database through peewee"""

import logging
from datetime import datetime
from peewee_models import database, Rides, Bikes, Components, Services #Match with export from peewee_models, maybe base_model is not needed since it is inherited?
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
                        action='REPLACE'
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
            bike_id_set = {
                ride.bike_id
                for ride in unique_bike_ids 
                if ride.bike_id != "None"}
            
            return bike_id_set

        except (peewee.OperationalError, ValueError) as error:
            logging.error(f"An error occurred while creating list of unique bike_ids: {error}")
            return {}
    
    def transform_dates(self):
        """..."""
        pass #Should process only dates, not time

    def update_components_distance_selector(self, delimiter):
        """Method to select which selection of components to update"""
        try:
            
            try:
                if delimiter == "all":
                    logging.info("All installed components selected")
                    with database.atomic():
                        for component in Components.select().where(Components.installation_status == 'Installed'):
                            self.update_component_distance(component)
            
            except (peewee.OperationalError, ValueError) as error:
                logging.error(f'An error occurred while selecting all installed components : {error}')
              
            try:
                if isinstance(delimiter, set):
                    logging.info("Components on recently used bikes selected")
                    with database.atomic():
                        for bike_id in delimiter:
                            for component in Components.select().where((Components.installation_status == 'Installed') & (Components.bike_id == bike_id)):
                                self.update_component_distance(component)
            
            except (peewee.OperationalError, ValueError) as error:
                logging.error(f'An error occurred while selecting components on recently used bikes : {error}')
            
            try:
                if "b" in delimiter: #This works, but probably only because it evaluates after delimiter set. Consider how to make this more resilient
                    logging.info(f"Components on bike with id {delimiter} selected")
                    with database.atomic():
                        for component in Components.select().where((Components.installation_status == 'Installed') & (Components.bike_id == delimiter)):
                            self.update_component_distance(component)

            except (peewee.OperationalError, ValueError) as error:
                logging.error(f'An error occurred while selecting components on a single bike : {error}') 
        
        except (peewee.OperationalError, ValueError) as error:
            logging.error(f'An error occurred while selecting which components to update: {error}')

    def update_component_distance(self, component):
        """Method to update component table with distance from ride table"""
        try:
            if component.updated_date:
                updated_date = datetime.strptime(component.updated_date, '%Y-%m-%d')
            else:
                updated_date = None

            record_time_query = Rides.select(Rides.record_time).where(Rides.bike_id == component.bike_id)
            record_time_value = record_time_query.scalar()
            record_time = datetime.strptime(record_time_value, '%Y-%m-%dT%H:%M:%S') if record_time_value else None

            matching_rides = Rides.select().where(
                (Rides.bike_id == component.bike_id) & (Rides.record_time >= updated_date))
            
            distance_offset = Components.get(Components.component_id == component.component_id).component_distance_offset
            total_distance_current = sum(ride.ride_distance for ride in matching_rides)
            total_distance = total_distance_current + distance_offset # More on distance_offset, should not always be used?
            
            
            # Update component_distance only if there are matching rides
            if matching_rides.exists() and record_time:
                component.component_distance = total_distance
                component.save() #Should be with database atomic?
                logging.info(f"Updated distance for component with id {component.component_id}")
                
                self.update_component_service_status(component) #Fix the date strip time thing before dealing with this function
                self.update_component_lifetime_status(component)

        
        except (peewee.OperationalError, ValueError) as error:
            logging.error(f'An error occurred while updating component distance for component with id {component.component_id} : {error}')

    def update_component_service_status(self, component):
        """Method to update component table with service status"""
        
        if component.service_interval:
            logging.info(f"Updating service status for component {component.component_name} (id {component.component_id})")

            try:
                services = Services.select().where((Services.component_id == component.component_id))
                service_list = [
                    service.service_date
                    for service in services 
                    if service.service_date != "None"]
                service_list = sorted(service_list, reverse=True)

                if len(service_list) > 0:
                    newest_service = service_list[0]
                    matching_rides = Rides.select().where((Rides.bike_id == component.bike_id) & (Rides.record_time >= newest_service))
                    
                elif len(service_list) == 0:
                    matching_rides = Rides.select().where((Rides.bike_id == component.bike_id))    
                
                service_next = component.service_interval- sum(ride.ride_distance for ride in matching_rides)

                with database.atomic():
                    component.service_next = service_next
                    component.service_status = self.compute_component_status("service", service_next)
                    component.save()

            except peewee.OperationalError as error:
                logging.error(f'An error occurred while updating service status for component with id {component.component_id} : {error}')
        
        else:
            logging.info(f"Component {component.component_name} (id {component.component_id}) has no service interval")

            with database.atomic(): #Include try / except, with error message as above
                component.service_next = None
                component.service_status = "No service defined"
                component.save()

    def update_component_lifetime_status(self, component):
        """Method to update component table with lifetime status"""
        
        #get component distance and compare that with lifetime
        # Add fault handling for this one somehow, component may have zero km

        component.service_status = self.compute_component_status("lifetime", service_next)
        # Exceeded lifetime
        # Approaching lifetime
        # Within lifetime

    def compute_component_status(self, mode, distance_since_service):
        """Method to compute service status"""

        Adjust function to handle two modes

        if int(distance_since_service) < 0:
            status = "Service overdue"
        elif int(distance_since_service) in range(0, 500):
            status = "Service approaching"
        elif int(distance_since_service) >= 500:
            status = "OK"
        
        return status



# Function to create random id, called by different functions. Consider making a toolbox for that and date functions
# Find a way to handle the offset value, it should not always be added..
# Consider all export statement