#!/usr/bin/env python3
"""Module for configuration and mapping of an SQL database"""

from peewee import SqliteDatabase, Model, CharField, FloatField, IntegerField

database = SqliteDatabase('/home/xivind/SQLiteStudio/Test')  #Move to config


class BaseModel(Model):
    """Base model for inheritance"""
    class Meta:
        """Extra attributes for base model for inheritance"""
        database = database


class Bikes(BaseModel):
    """Model for table: bikes"""
    bike_id = CharField(primary_key=True, unique=True)
    athlete_id = CharField()
    bike_name = CharField()
    bike_retired = CharField()
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


class Components(BaseModel):
    """Model for table: components"""
    component_id = CharField(primary_key=True, unique=True)
    bike_id = CharField()
    component_type = CharField()
    component_name = CharField()
    component_distance = FloatField()
    installation_status = CharField()
    service_interval = IntegerField()
    service_next = IntegerField()
    service_status = CharField()
    updated_date = CharField()

    class Meta:
        """Extends model with extra attributes"""
        table_name = "components"


class Athletes(BaseModel):
    """Model for table: athletes"""
    ahlete_id = CharField(primary_key=True, unique=True)

    class Meta:
        """Extends model with extra attributes"""
        table_name = "athletes"


class Services(BaseModel):
    """Model for table: services"""
    service_id = CharField(primary_key=True, unique=True)

    class Meta:
        """Extends model with extra attributes"""
        table_name = "services"


__all__ = ['database', 'BaseModel', 'Rides', 'Bikes']
