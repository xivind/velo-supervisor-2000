#!/usr/bin/env python3
"""Module for interaction with a Sqlite database"""

import peewee
import database_model

class DatabaseManager:
    """Class to interact with a SQL database through peewee"""
    def __init__(self):
        self.database = database_model.database

    def read_component_types(self):
        """Method to read and sort content of component_types table"""
        component_types = database_model.ComponentTypes.select()

        component_types_data = [(component_type.component_type,
                             component_type.expected_lifetime,
                             component_type.service_interval) for component_type in component_types]
    
        component_types_data.sort(key=lambda x: x[0])
        
        return component_types_data