#!/usr/bin/env python3
"""Module for interaction with a Sqlite database"""

import peewee
from database_model import (database,
                            Bikes,
                            Rides,
                            ComponentTypes,
                            Components,
                            ComponentHistory,
                            Services)

class DatabaseManager:
    """Class to interact with a SQLite database through Peewee"""
    def __init__(self):
        self.database = database

    def read_bikes(self):
        """Method to read content of bikes table"""
        return Bikes.select()

    def read_single_bike(self, bike_id):
        """Method to retrieve record for a specific bike"""
        return (Bikes
                .get_or_none(Bikes.bike_id == bike_id))

    def read_bike_name(self, bike_id):
        """Method to get the name of a bike based on bike id"""
        bike = self.read_single_bike(bike_id)

        if bike:
            if bike.bike_name is not None:
                return bike.bike_name

        return "Not assigned"

    def read_bike_id_recent_component_history(self, component_id):
        """Method to get bike id from most recent component history"""
        return (ComponentHistory
                .select()
                .where(ComponentHistory.component_id == component_id)
                .order_by(ComponentHistory.updated_date.desc())
                .first()
                .bike_id)
    
    def read_unique_bikes(self):
        """Method to query database and create list of unique bike ids"""
        unique_bike_ids = (Rides
                           .select(Rides.bike_id)
                           .distinct())
        
        bike_id_set = {ride.bike_id
                       for ride in unique_bike_ids
                       if ride.bike_id != "None"}

        return bike_id_set
    
    def read_recent_rides(self, bike_id):
        """Method to read recent rides for a specific bike"""
        return (Rides
                .select()
                .where(Rides.bike_id == bike_id)
                .order_by(Rides.record_time.desc())
                .limit(5))

    def read_matching_rides(self, bike_id, latest_updated_date):
        """Method to read rides associated with a given component aftere a given date"""
        return (Rides
                .select()
                .where((Rides.bike_id == bike_id) &
                (Rides.record_time >= latest_updated_date)))
    
    def read_latest_ride_record(self):
        """Method to retrieve the most recent ride"""
        return (Rides
                .select()
                .order_by(Rides.record_time.desc())
                .first())

    def read_date_oldest_ride(self, bike_id):
        """Method to get the date for the oldest ride for a given bike"""
        oldest_ride_record = (Rides
                              .select(Rides.record_time)
                              .where(Rides.bike_id == bike_id)
                              .order_by(Rides.record_time.asc()).first())

        if oldest_ride_record:
            return  oldest_ride_record.record_time.split('T')[0]

        return None

    def read_sum_distanse_subset_rides(self, bike_id, start_date, stop_date):
        """Method to sum distance for a given set of rides"""
        matching_rides = (Rides.select()
                          .where((Rides.bike_id == bike_id) &
                                 (Rides.record_time >= start_date) &
                                 (Rides.record_time <= stop_date)))
        if matching_rides:
            return sum(ride.ride_distance for ride in matching_rides)
                   
        return 0
    
    def read_component_types(self):
        """Method to read and sort content of component_types table"""
        component_types = ComponentTypes.select()

        component_types_data = [(component_type.component_type,
                                 component_type.expected_lifetime,
                                 component_type.service_interval) for component_type in component_types]

        component_types_data.sort(key=lambda x: x[0])

        return component_types_data

    def read_all_components(self):
        """Method to read content of components table"""
        return Components.select()

    def read_subset_components(self, bike_id):
        """Method to read components for a specific bike"""
        return (Components
                .select()
                .where(Components.bike_id == bike_id))

    def read_subset_installed_components(self, bike_id):
        """Method to read installed components for a specific bike"""
        return (Components
                .select()
                .where((Components.installation_status == 'Installed') &
                (Components.bike_id == bike_id)))
                
    def read_component(self, component_id):
        """Method to retrieve record for a specific component"""
        return (Components
                .get_or_none(Components.component_id == component_id))
    
    def read_subset_component_history(self, component_id):
        """Method to read a subset of receords from the component history table"""
        return (ComponentHistory
                .select()
                .where(ComponentHistory.component_id == component_id)
                .order_by(ComponentHistory.updated_date.desc()))

    def read_history_record(self, history_id):
        """Method to retrieve record for a specific entry in installation log"""
        return (ComponentHistory
                .get_or_none(ComponentHistory.history_id == history_id))
    
    def read_latest_history_record(self, component_id):
        """Method to retrieve the most recent record from the installation log of a given component"""
        return (ComponentHistory
                .select().where(ComponentHistory.component_id == component_id)
                .order_by(ComponentHistory.updated_date.desc())
                .first())
    
    def read_subset_service_history(self, component_id):
        """Method to read a subset of receords from the component history table"""
        return (Services.
                select()
                .where(Services.component_id == component_id)
                .order_by(Services.service_date.desc()))

    def read_latest_service_record(self, component_id):
        """Method to retrieve the most recent record from the service log of a given component"""
        return (Services
                .select()
                .where(Services.component_id == component_id)
                .order_by(Services.service_date.desc())
                .first())

    def write_update_rides_bulk(self, ride_list):
        """Method to create or update ride data in bulk to database"""
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

                    return True, "Rides table updated successfully"

        except peewee.OperationalError as error:
            return False, f"An error occurred during bulk update of rides table: {str(error)}"

    def write_update_bikes(self, bike_list):
        """Method to create or update bike data to the database"""
        try:
            with database.atomic():
                for bike_data in bike_list:
                    existing_bike = self.read_single_bike(bike_data["bike_id"])

                    if existing_bike:
                        filtered_bike_data = {key: value for key, value in bike_data.items() if key != 'bike_id'}
                        query = Bikes.update(**filtered_bike_data).where(Bikes.bike_id == bike_data["bike_id"])
                        query.execute()

                    else:
                        query = Bikes.insert(**bike_data)
                        query.execute()

            return True, f'Records for {len(bike_list)} bikes updated'

        except peewee.OperationalError as error:
            return False, f"Update of bike records failed: {str(error)}"
    
    def write_component_distance(self, component, total_distance): #Should have peewee op error and return statement
        """Method to update component distance in database"""
        with database.atomic():
            component.component_distance = total_distance
            component.save()

    def write_component_lifetime_status(self, component, lifetime_remaining, lifetime_status): #Should have peewee op error and return statement
        """Method to update component lifetime status in database"""
        with database.atomic():
            component.lifetime_remaining = lifetime_remaining
            component.lifetime_status = lifetime_status
            component.save()

    def write_component_service_status(self, component, service_next, service_status): #Should have peewee op error and return statement
        """Method to update component service status in database"""
        with database.atomic():
            component.service_next = service_next
            component.service_status = service_status
            component.save()

    def write_bike_service_status(self, bike, service_status): #Should have peewee op error and return statement
        """Method to update bike service status in database"""
        with database.atomic():
            bike.service_status = service_status
            bike.save()
    
    def write_delete_record(self, table_selector, record_id):
        """Method to delete a given record and associated records"""
        try:
            with self.database.atomic():
                if table_selector == "ComponentTypes":
                    record = ComponentTypes.get_or_none(ComponentTypes.component_type == record_id)
                    if record:
                        record.delete_instance()
                        return True, f"Deleted component type: {record_id}"
                
                elif table_selector == "Components":
                    record = Components.get_or_none(Components.component_id == record_id)
                    if record:
                        services_deleted = Services.delete().where(Services.component_id == record_id).execute()
                        history_deleted = ComponentHistory.delete().where(ComponentHistory.component_id == record_id).execute()
                        record.delete_instance()
                        return True, f"Deleted component: {record.component_name} ({record_id}), related records deleted: {services_deleted} service(s), {history_deleted} history record(s)"
                else:
                    return False, "Invalid table selector"

                if not record:
                    return False, f"Record not found: {record_id}"

        except peewee.OperationalError as error:
            return False, f"Deletion of records failed: {str(error)}"
