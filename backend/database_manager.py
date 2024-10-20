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

    def get_bike_name(self, bike_id):
        """Method to get the name of a bike based on bike id"""
        bike = self.read_single_bike(bike_id)

        if bike:
            if bike.bike_name is not None:
                return bike.bike_name

        return "Not assigned"

    def get_unique_bikes(self):
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

    def read_latest_ride_record(self):
        """Method to retrieve the most recent ride"""
        return (Rides
                .select()
                .order_by(Rides.record_time.desc())
                .first())

    def get_date_oldest_ride(self, bike_id):
        """Method to get the date for the oldest ride for a given bike"""
        oldest_ride_record = (Rides
                              .select(Rides.record_time)
                              .where(Rides.bike_id == bike_id)
                              .order_by(Rides.record_time.asc()).first())

        if oldest_ride_record:
            return  oldest_ride_record.record_time.split('T')[0]

        return None

    def sum_distanse_subset_rides(self, bike_id, start_date, stop_date):
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
    
    def delete_record(self, table_selector, record_id):
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
            return False, f"Database operation failed: {str(error)}"
        