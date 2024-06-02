#!/usr/bin/env python3
"""Module to interact with a SQL database through Peewee"""

import logging
from datetime import datetime
import peewee
import uuid
import time
from peewee_models import database, Rides, Bikes, Components, Services, ComponentTypes #Match with export from peewee_models, maybe base_model is not needed since it is inherited?


# Implement health check

class ReadTables(): #rename to something else, internal logic or something, might split into separate classes
    """Class to interact with a SQL database through peewee""" #Modify this description
    def __init__(self):
        pass #Check out this one..

    def read_component_types(self):
        """Method to read content of component_types table"""
        component_types = ComponentTypes.select()
        return component_types
    
    def read_components(self):
        """Method to read content of components table"""
        components = Components.select()
        return components
    
    def read_bikes(self):
        """Method to read content of bikes table"""
        bikes = Bikes.select()
        return bikes


class ModifyTables(): #rename to something else, internal logic or something, might split into separate classes
    """Class to interact with a SQL database through peewee""" #Modify this description
    def __init__(self):
        pass #Check out this one..

    def update_rides_bulk(self, ride_list):
        """Method to create or update ride data in bulk to database"""
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

    def update_bikes(self, bike_list):
        """Method to create or update bike data to the database"""
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


    def update_components_distance_selector(self, delimiter):
        """Method to determine which selection of components to update"""
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
            total_distance = total_distance_current + distance_offset

            if matching_rides.exists() and record_time:
                with database.atomic():
                    component.component_distance = total_distance
                    component.save()

                logging.info(f"Updated distance for component {component.component_name} (id {component.component_id})")

                self.update_component_service_status(component)
                self.update_component_lifetime_status(component)

        except (peewee.OperationalError, ValueError) as error:
            logging.error(f'An error occurred while updating component distance for component {component.component_name} (id {component.component_id}): {error}')

    def update_component_service_status(self, component):
        """Method to update component table with service status"""
        if component.service_interval:
            try:
                logging.info(f"Updating service status for component {component.component_name} (id {component.component_id})")

                services = Services.select().where((Services.component_id == component.component_id))
                service_list = [
                    service.service_date
                    for service in services
                    if service.service_date != "None"]
                service_list = sorted(service_list, reverse=True)

                if len(service_list) > 0:
                    newest_service = service_list[0]
                    matching_rides = Rides.select().where((Rides.bike_id == component.bike_id) & (Rides.record_time >= newest_service))
                    distance_since_service = sum(ride.ride_distance for ride in matching_rides)

                elif len(service_list) == 0:
                    distance_since_service = component.component_distance

                service_next = component.service_interval- distance_since_service

                with database.atomic():
                    component.service_next = service_next
                    component.service_status = self.compute_component_status("service", service_next)
                    component.save()

            except peewee.OperationalError as error:
                logging.error(f'An error occurred while updating service status for component {component.component_name} (id {component.component_id}): {error}')

        else:
            try:
                logging.info(f"Component {component.component_name} (id {component.component_id}) has no service interval, setting NULL values for service")
                with database.atomic():
                    component.service_next = None
                    component.service_status = "Service not defined"
                    component.save()

            except peewee.OperationalError as error:
                logging.error(f'An error occurred while setting blank service status for component {component.component_name} (id {component.component_id}): {error}')

    def update_component_lifetime_status(self, component):
        """Method to update component table with lifetime status"""
        if component.lifetime_expected:
            try:
                logging.info(f"Updating lifetime status for component {component.component_name} (id {component.component_id})")

                with database.atomic():
                    component.lifetime_remaining = component.lifetime_expected - component.component_distance
                    component.lifetime_status = self.compute_component_status("lifetime", component.lifetime_remaining)
                    component.save()

            except peewee.OperationalError as error:
                logging.error(f'An error occurred while updating lifetime status for component {component.component_name} (id {component.component_id}): {error}')

        else:
            try:
                logging.info(f"Component {component.component_name} (id {component.component_id}) has no expected lifetime, setting NULL values for lifetime")

                with database.atomic():
                    component.lifetime_remaining = None
                    component.lifetime_status = "Lifetime not defined"
                    component.save()

            except peewee.OperationalError as error:
                logging.error(f'An error occurred while setting blank lifetime status for component {component.component_name} (id {component.component_id}): {error}')

    def compute_component_status(self, mode, distance):
        """Method to compute service status"""

        if mode == "service":
            if int(distance) < 0:
                status = "Service overdue"
            elif int(distance) in range(0, 500):
                status = "Service approaching"
            elif int(distance) >= 500:
                status = "OK"

        if mode == "lifetime":
            if int(distance) < 0:
                status = "Lifetime exceeded"
            elif int(distance) in range(0, 1000):
                status = "End of lifetime approaching"
            elif int(distance) >= 1000:
                status = "OK"

        return status


class ReadRecords():
    """Class to interact with a SQL database through peewee""" #Modify this description
    def __init__(self):
        pass #Check out this one.


class ModifyRecords():
    """Class to interact with a SQL database through peewee""" #Modify this description
    def __init__(self):
        pass #Check out this one.

    def update_component_type(self, component_type_data):
        """Method to create or update component types"""
    
        try:
            logging.info(f"Creating or updating component type {component_type_data['component_type']}")
            with database.atomic():
                component_type = ComponentTypes.get_or_none(ComponentTypes.component_type == component_type_data["component_type"])

                if component_type:
                    component_type.component_type = component_type_data["component_type"]
                    component_type.service_interval = component_type_data["service_interval"]
                    component_type.expected_lifetime = component_type_data["expected_lifetime"]
                    component_type.save()
            
                else:
                    ComponentTypes.create(
                        component_type = component_type_data["component_type"],
                        service_interval = component_type_data["service_interval"],
                        expected_lifetime = component_type_data["expected_lifetime"])
        
        except peewee.OperationalError as error:
                logging.error(f'An error occurred while creating or updating component type {component_type_data["component_type"]}: {error}')
    
    def delete_record(self, table_selector, record_id):
        """Method to delete any record"""

        try:
            logging.info(f"Deleting record with id {record_id} from table {table_selector}")
            if table_selector == str("ComponentTypes"):
                query = ComponentTypes.get_or_none(ComponentTypes.component_type == record_id)
                table_found = True
            elif table_selector == str("Services"):
                query = Services.get_or_none(Services.service_id == record_id)
                table_found = True
            else:
                logging.error(f'Error looking up table for deletion of record, non-existing table: {table_selector}')
                table_found = False
        
            if table_found:
                with database.atomic():
                    record = query
                    if record:
                        record.delete_instance()

        except peewee.OperationalError as error:
                logging.error(f'An error occurred while deleting record with id {record_id} from table {table_selector}: {error}')

class MiscMethods():
    """Class to interact with a SQL database through peewee""" #Modify this description
    def __init__(self):
        pass #Check out this one.

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
        
    def generate_unique_id(self):
        """Function to generates a random and unique ID"""
        unique_id_part1 = uuid.uuid4()
        unique_id_part2 = time.time()

        return f'{str(unique_id_part1)[:6]}{str(unique_id_part2)[-4:]}'

# Function to calculate service status in bikes table
# Find a way to handle the offset value, it should not always be added, but should be saved when a component is uninstalled
# Consider all export statement, maybe not needed?
