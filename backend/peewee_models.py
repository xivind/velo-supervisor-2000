#!/usr/bin/env python3
"""Module for configuration and mapping of an SQL database"""

from peewee import SqliteDatabase, Model, CharField, FloatField, IntegerField

database = SqliteDatabase('/home/xivind/SQLiteStudio/Test')  #Move to config


class BaseModel(Model):
    """Base model for inheritance"""
    class Meta:
        """Extra attributes for base model for inheritance"""
        database = database


class Athletes(BaseModel):
    """Model for table: athletes"""
    ahlete_id = CharField(primary_key=True, unique=True)
    athlete_name = CharField()

    class Meta:
        """Extends model with extra attributes"""
        table_name = "athletes"


class Bikes(BaseModel):
    """Model for table: bikes"""
    bike_id = CharField(primary_key=True, unique=True)
    athlete_id = CharField()
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
    component_distance_offset = FloatField()
    installation_status = CharField()
    service_interval = IntegerField()
    lifetime_expected = IntegerField()
    lifetime_remaining = IntegerField()
    lifetime_status = IntegerField()
    service_status = CharField()
    service_next = IntegerField()
    updated_date = CharField()
    update_reason = CharField()
    cost = IntegerField()
    notes = CharField()

    class Meta:
        """Extends model with extra attributes"""
        table_name = "components"


class ComponentHistory(BaseModel):
    """Model for table: component_history"""
    history_id = CharField(primary_key=True, unique=True)
    component_id = CharField()
    component_name = CharField()
    updated_date = CharField()
    update_reason = CharField()
    distance_marker = IntegerField()
    notes = CharField()

    class Meta:
        """Extends model with extra attributes"""
        table_name = "component_history"


class Services(BaseModel):
    """Model for table: services"""
    service_id = CharField(primary_key=True, unique=True)
    component_id = CharField()
    component_name = CharField()
    service_name = CharField()
    service_date = CharField()
    distance_marker = IntegerField()
    notes = CharField()

    class Meta:
        """Extends model with extra attributes"""
        table_name = "services"


__all__ = ['database',
           'BaseModel',
           'Athletes',
           'Bikes',
           'Rides',
           'ComponentTypes',
           'Components',
           'ComponentHistory',
           'Services']
