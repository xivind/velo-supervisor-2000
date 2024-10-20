#!/usr/bin/env python3
"""Module for interaction with a Sqlite database"""

import database_model

class DatabaseManager:
    """Class to interact with a SQLite database through Peewee"""
    def __init__(self):
        self.database = database_model.database

    def read_bikes(self):
        """Method to read content of bikes table"""
        return database_model.Bikes.select()
    
    def read_single_bike(self, bike_id):
        """Method to retrieve record for a specific bike"""
        return (database_model.Bikes
                .get_or_none(database_model.Bikes.bike_id == bike_id))
    
    def read_recent_rides(self, bike_id):
        """Method to read recent rides for a specific bike"""
        return (database_model.Rides
                .select()
                .where(database_model.Rides.bike_id == bike_id)
                .order_by(database_model.Rides.record_time.desc())
                .limit(5))
    
    def read_latest_ride_record(self):
        """Method to retrieve the most recent ride"""
        return (database_model.Rides
                .select()
                .order_by(database_model.Rides.record_time.desc())
                .first())
    
    def get_date_oldest_ride(self, bike_id):
        """Method to get the date for the oldest ride for a given bike"""
        oldest_ride_record = (database_model.Rides
                              .select(database_model.Rides.record_time)
                              .where(database_model.Rides.bike_id == bike_id)
                              .order_by(database_model.Rides.record_time.asc()).first())
        
        if oldest_ride_record:
            return  oldest_ride_record.record_time.split('T')[0]
        
        return None
    
    def read_component_types(self):
        """Method to read and sort content of component_types table"""
        component_types = database_model.ComponentTypes.select()

        component_types_data = [(component_type.component_type,
                                 component_type.expected_lifetime,
                                 component_type.service_interval) for component_type in component_types]

        component_types_data.sort(key=lambda x: x[0])

        return component_types_data

    def read_all_components(self):
        """Method to read content of components table"""
        return database_model.Components.select()

    def read_subset_components(self, bike_id):
        """Method to read components for a specific bike"""
        return (database_model.Components
                .select()
                .where(database_model.Components.bike_id == bike_id))

    def read_component(self, component_id):
        """Method to retrieve record for a specific component"""
        return (database_model.Components
                .get_or_none(database_model.Components.component_id == component_id))
    
    def read_subset_component_history(self, component_id):
        """Method to read a subset of receords from the component history table"""
        return (database_model.ComponentHistory
                .select()
                .where(database_model.ComponentHistory.component_id == component_id)
                .order_by(database_model.ComponentHistory.updated_date.desc()))

    def read_history_record(self, history_id):
        """Method to retrieve record for a specific entry in installation log"""
        return (database_model.ComponentHistory
                .get_or_none(database_model.ComponentHistory.history_id == history_id))
    
    def read_latest_history_record(self, component_id):
        """Method to retrieve the most recent record from the installation log of a given component"""
        return (database_model.ComponentHistory
                .select().where(database_model.ComponentHistory.component_id == component_id)
                .order_by(database_model.ComponentHistory.updated_date.desc())
                .first())
    
    def read_subset_service_history(self, component_id):
        """Method to read a subset of receords from the component history table"""
        return (database_model.Services.
                select()
                .where(database_model.Services.component_id == component_id)
                .order_by(database_model.Services.service_date.desc()))

    def read_latest_service_record(self, component_id):
        """Method to retrieve the most recent record from the service log of a given component"""
        return (database_model.Services
                .select()
                .where(database_model.Services.component_id == component_id)
                .order_by(database_model.Services.service_date.desc())
                .first())
    
        