"""Configuration and mapping of the SQL database"""

from peewee import SqliteDatabase, Model, CharField, FloatField, IntegerField

database = SqliteDatabase('/home/xivind/SQLiteStudio/Test')  #Move to config


class BaseModel(Model):
    """Base model class for inheritance"""
    class Meta:
        database = database


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


class Athletes(BaseModel):
    """Model for table: athletes"""
    ahlete_id = CharField(primary_key=True, unique=True)


class Bikes(BaseModel):
    """Model for table: bikes"""
    bike_id = CharField(primary_key=True, unique=True)
    athlete_id = CharField()
    total_distance = FloatField() 


class Rides(BaseModel):
    """Model for table: rides"""
    ride_id = CharField(primary_key=True, unique=True)
    bike_id = CharField()
    record_time = CharField()
    ride_name = CharField()
    ride_distance = FloatField()
    ride_moving_time = CharField()


class Services(BaseModel):
    """Model for table: services"""
    service_id = CharField(primary_key=True, unique=True)


__all__ = ['database', 'BaseModel', 'Rides', 'Bikes']
