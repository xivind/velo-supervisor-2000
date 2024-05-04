# DOCSTRING
from peewee import *
#Replace with "from peewee import MySQLDatabase" in future version

#change this param to MariaDB in future release
database = SqliteDatabase('test.db')

class Athletes(Model):
    AthleteId = CharField(unique=True)
    AthleteName = CharField()

    class Meta:
        database = database