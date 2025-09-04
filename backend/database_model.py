#!/usr/bin/env python3
"""Module for configuration and mapping of a Sqlite database"""

from utils import read_config
from peewee import (SqliteDatabase,
                    Model,
                    CharField,
                    FloatField,
                    IntegerField)

CONFIG = read_config()

database = SqliteDatabase(CONFIG['db_path'])

class BaseModel(Model):
    """Base model for inheritance"""
    class Meta:
        """Extra attributes for base model for inheritance"""
        database = database


class Bikes(BaseModel):
    """Model for table: bikes"""
    bike_id = CharField(primary_key=True, unique=True)
    bike_name = CharField()
    bike_retired = CharField()
    service_status = CharField()
    total_distance = FloatField()
    notes = CharField()

    class Meta:
        """Extends model with extra attributes"""
        table_name = "bikes"


class Rides(BaseModel):
    """Model for table: rides"""
    ride_id = CharField(primary_key=True, unique=True)
    bike_id = CharField()
    record_time = CharField()
    ride_name = CharField()
    ride_distance = FloatField()
    moving_time = CharField()
    commute = CharField()

    class Meta:
        """Extends model with extra attributes"""
        table_name = "rides"


class ComponentTypes(BaseModel):
    """Model for table: component_types"""
    component_type = CharField(primary_key=True, unique=True)
    service_interval = IntegerField()
    expected_lifetime = IntegerField()
    in_use = IntegerField()
    mandatory = CharField()
    max_quantity = IntegerField()

    class Meta:
        """Extends model with extra attributes"""
        table_name = "component_types"


class Components(BaseModel):
    """Model for table: components"""
    component_id = CharField(primary_key=True, unique=True)
    bike_id = CharField()
    component_name = CharField()
    component_type = CharField()
    component_distance = FloatField()
    component_distance_offset = IntegerField()
    installation_status = CharField()
    service_interval = IntegerField()
    lifetime_expected = IntegerField()
    lifetime_remaining = FloatField()
    lifetime_status = CharField()
    service_status = CharField()
    service_next = FloatField()
    updated_date = CharField()
    cost = IntegerField()
    notes = CharField()

    class Meta:
        """Extends model with extra attributes"""
        table_name = "components"


class Collections(BaseModel):
    """Model for table: collections"""
    collection_id = CharField(primary_key=True, unique=True)
    collection_name = CharField()
    components = CharField()
    bike_id = CharField(null=True)
    sub_collections = CharField()
    updated_date = CharField()
    comment = CharField()
    
    class Meta:
        """Extends model with extra attributes"""
        table_name = "collections"


class ComponentHistory(BaseModel):
    """Model for table: component_history"""
    history_id = CharField(primary_key=True, unique=True)
    component_id = CharField()
    bike_id = CharField()
    component_name = CharField()
    updated_date = CharField()
    update_reason = CharField()
    distance_marker = FloatField()

    class Meta:
        """Extends model with extra attributes"""
        table_name = "component_history"


class Services(BaseModel):
    """Model for table: services"""
    service_id = CharField(primary_key=True, unique=True)
    component_id = CharField()
    component_name = CharField()
    bike_id = CharField()
    service_date = CharField()
    distance_marker = FloatField()
    description = CharField()

    class Meta:
        """Extends model with extra attributes"""
        table_name = "services"


class Incidents(BaseModel):
    """Model for table: incidents"""
    incident_id = CharField(primary_key=True, unique=True)
    incident_date = CharField()
    incident_status = CharField()
    incident_severity = CharField()
    incident_affected_component_ids = CharField()
    incident_affected_bike_id = CharField()
    incident_description = CharField()
    resolution_date = CharField()
    resolution_notes = CharField()

    class Meta:
        """Extends model with extra attributes"""
        table_name = "incidents"


class Workplans(BaseModel):
    """Model for table: workplans"""
    workplan_id = CharField(primary_key=True, unique=True)
    due_date = CharField()
    workplan_status = CharField()
    workplan_size = CharField()
    workplan_affected_component_ids = CharField()
    workplan_affected_bike_id = CharField()
    workplan_description = CharField()
    completion_date = CharField()
    completion_notes = CharField()

    class Meta:
        """Extends model with extra attributes"""
        table_name = "workplans"