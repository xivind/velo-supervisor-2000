#!/usr/bin/env python3
"""Module for interaction with a Sqlite database"""

import peewee
import json
from database_model import (database,
                            Bikes,
                            Rides,
                            ComponentTypes,
                            Components,
                            ComponentHistory,
                            Services,
                            Incidents,
                            Workplans,
                            Collections)
from utils import (format_component_status,
                   format_cost)

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

    def read_sum_distance_subset_rides(self, bike_id, start_date, stop_date):
        """Method to sum distance for a given set of rides"""
        matching_rides = (Rides.select()
                          .where((Rides.bike_id == bike_id) &
                                 (Rides.record_time >= start_date) &
                                 (Rides.record_time <= stop_date)))
        if matching_rides:
            return sum(ride.ride_distance for ride in matching_rides)

        return 0

    def read_all_component_types(self):
        """Method to read and sort content of component_types table"""
        component_types = ComponentTypes.select()

        component_types_data = [(component_type.component_type,
                                 component_type.expected_lifetime,
                                 component_type.service_interval,
                                 component_type.in_use,
                                 component_type.mandatory,
                                 component_type.max_quantity) for component_type in component_types]

        component_types_data.sort(key=lambda x: x[0].lower())

        return component_types_data

    def read_single_component_type(self, component_type):
        """Method to retrieve record for a single component type"""
        return (ComponentTypes
                .get_or_none(ComponentTypes.component_type == component_type))

    def read_component_names(self, component_ids_raw):
        """Method to get component names based on list of ids"""

        if component_ids_raw is None:
            return ["Not assigned"]

        component_ids = json.loads(component_ids_raw)

        component_names = []
        for component_id in component_ids:
            component = self.read_component(component_id)
            if component:
                component_names.append(component.component_name)
            else:
                component_names.append("Deleted component")

        return component_names if component_names else ["Not assigned"]

    def count_component_types_in_use(self, component_type):
        """Method to count how many components that references a given component type"""
        return (Components
                .select()
                .where(Components.component_type == component_type)
                .count())

    def read_all_components(self):
        """Method to read content of components table"""
        all_components = Components.select()

        all_components_data = [(component.component_id,
                                component.component_type,
                                component.component_name,
                                round(component.component_distance),
                                component.installation_status,
                                format_component_status(component.lifetime_status),
                                format_component_status(component.service_status),
                                self.read_bike_name(component.bike_id),
                                format_cost(component.cost)) for component in all_components]

        return all_components_data

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
        """Method to read a subset of records from the component history table"""
        return (ComponentHistory
                .select()
                .where(ComponentHistory.component_id == component_id)
                .order_by(ComponentHistory.updated_date.desc()))

    def read_single_history_record(self, history_id):
        """Method to retrieve record for a specific entry in the installation log"""
        return (ComponentHistory
                .get_or_none(ComponentHistory.history_id == history_id))

    def read_latest_history_record(self, component_id):
        """Method to retrieve the most recent record from the installation log of a given component"""
        return (ComponentHistory
                .select().where(ComponentHistory.component_id == component_id)
                .order_by(ComponentHistory.updated_date.desc())
                .first())

    def read_oldest_history_record(self, component_id):
        """Method to retrieve the oldest record from the installation log of a given component"""
        return (ComponentHistory
                .select().where(ComponentHistory.component_id == component_id)
                .order_by(ComponentHistory.updated_date.asc())
                .first())
    
    def read_single_service_record(self, service_id):
        """Method to retrieve a specific service record"""
        return (Services
                .get_or_none(Services.service_id == service_id))

    def read_subset_service_history(self, component_id):
        """Method to read a subset of receords from the component history table"""
        return (Services.
                select()
                .where(Services.component_id == component_id)
                .order_by(Services.service_date.desc()))

    def read_subset_service_record(self, service_id):
        """Method to retrieve record for a specific entry in the service log"""
        return (Services
                .get_or_none(Services.service_id == service_id))

    def read_latest_service_record(self, component_id):
        """Method to retrieve the most recent record from the service log of a given component"""
        return (Services
                .select()
                .where(Services.component_id == component_id)
                .order_by(Services.service_date.desc())
                .first())

    def read_oldest_service_record(self, component_id):
        """Method to retrieve the oldest record from the service log of a given component"""
        return (Services
                .select()
                .where(Services.component_id == component_id)
                .order_by(Services.service_date.asc())
                .first())

    def read_single_collection(self, collection_id):
        """Method to retrieve record for a specific collection"""
        return (Collections
                .get_or_none(Collections.collection_id == collection_id))

    def read_all_collections(self):
        """Method to read all collections"""
        return Collections.select()

    def read_collections_by_bike(self, bike_id):
        """Method to read collections for a specific bike"""
        return (Collections
                .select()
                .where(Collections.bike_id == bike_id))

    def read_collection_by_component(self, component_id):
        """Method to find collection containing a specific component"""
        all_collections = Collections.select()
        
        for collection in all_collections:
            if collection.components:
                component_ids = json.loads(collection.components)
                if component_id in component_ids:
                    return collection
        
        return None
    
    def read_single_incident_report(self, incident_id):
        """Method to retrieve record for a specific incident report"""
        return (Incidents
                .get_or_none(Incidents.incident_id == incident_id))

    def read_all_incidents(self):
        """Method to read all incident records"""
        return Incidents.select()

    def read_open_incidents(self):
        """Method to read incident records with status 'Open'"""
        return (Incidents
                .select()
                .where(Incidents.incident_status == "Open")
                .order_by(Incidents.incident_date.desc()))

    def read_single_workplan(self, workplan_id):
        """Method to retrieve record for a specific workplan"""
        return (Workplans
                .get_or_none(Workplans.workplan_id == workplan_id))

    def read_all_workplans(self):
        """Method to read all workplans"""
        return Workplans.select()

    def read_planned_workplans(self):
        """Method to read workplans with status 'Planned'"""
        return (Workplans
                .select()
                .where(Workplans.workplan_status == "Planned")
                .order_by(Workplans.due_date.desc()))

    def write_update_rides_bulk(self, ride_list):
        """Method to create or update ride data in bulk in database"""
        try:
            with database.atomic():
                batch_size = 50
                total_processed = 0

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
                        action='REPLACE').execute()

                    total_processed += len(batch)

                return True, f"Rides table updated successfully. Processed {total_processed} rides."

        except peewee.OperationalError as error:
            return False, f"An error occurred during bulk update of rides table: {str(error)}."

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

            return True, f'Records for {len(bike_list)} bikes updated.'

        except peewee.OperationalError as error:
            return False, f"Update of bike records failed: {str(error)}."

    def write_component_distance(self, component, total_distance):
        """Method to update component distance in database"""
        try:
            with database.atomic():
                component.component_distance = total_distance
                component.save()

            return True, component.component_name

        except peewee.OperationalError as error:
            return False, f"{component.component_name}: {str(error)}"

    def write_component_details(self, component_id, new_component_data):
        """Method to create or update component data to the database"""
        try:
            with database.atomic():
                component = self.read_component(component_id)
                
                if component:
                    Components.update(**new_component_data).where(Components.component_id == component_id).execute()
                    return True, f'Component {component.component_name} updated.'

                else:
                    new_component_data.update({"component_distance": 0,
                                               "component_id": component_id})

                    Components.create(**new_component_data)
                    return True, f'Component {new_component_data["component_name"]} created.'

        except peewee.OperationalError as error:
            return False, f"Component modification failed: {str(error)}"
    
    def write_component_lifetime_status(self, component, lifetime_remaining, lifetime_status):
        """Method to update component lifetime status in database"""
        try:
            with database.atomic():
                component.lifetime_remaining = lifetime_remaining
                component.lifetime_status = lifetime_status
                component.save()

            return True, f"{component.component_name}."
        
        except peewee.OperationalError as error:
            return False, f"{component.component_name}: {str(error)}."

    def write_component_service_status(self, component, service_next, service_status):
        """Method to update component service status in database"""
        try:
            with database.atomic():
                component.service_next = service_next
                component.service_status = service_status
                component.save()

            return True, f"{component.component_name}."

        except peewee.OperationalError as error:
            return False, f"{component.component_name}: {str(error)}."

    def write_bike_service_status(self, bike, service_status):
        """Method to update bike service status in database"""
        try:
            with database.atomic():
                bike.service_status = service_status
                bike.save()

            return True, f"{bike.bike_name}."

        except peewee.OperationalError as error:
            return False, f"{bike.bike_name}: {str(error)}."

    def write_service_record(self, service_data):
        """Method to write or update service record in database"""
        try:
            with self.database.atomic():
                existing_service = Services.get_or_none(Services.service_id == service_data['service_id'])
                
                if existing_service:
                    Services.update(**service_data).where(
                        Services.service_id == service_data['service_id']
                    ).execute()
                    return True, f"Updated service record for component {service_data['component_name']}."
                else:
                    Services.create(**service_data)
                    return True, f"Created service record for component {service_data['component_name']}."

        except peewee.OperationalError as error:
            return False, f"Service record database error for {service_data['component_name']}: {str(error)}"
    
    def write_history_record(self, history_data):
        "Method to write or update history record in database"
        try:
            with self.database.atomic():
                existing_history = ComponentHistory.get_or_none(ComponentHistory.history_id == history_data['history_id'])
                
                if existing_history:
                    ComponentHistory.update(**history_data).where(
                        ComponentHistory.history_id == history_data['history_id']
                    ).execute()
                    return True, f"Updated history record for component {history_data['component_name']}."
                else:
                    ComponentHistory.create(**history_data)
                    return True, f"Created history record for component {history_data['component_name']}."

        except peewee.OperationalError as error:
            return False, f"History record database error for {history_data['component_name']}: {str(error)}"

    def write_collection(self, collection_data):
        """Method to create or update collection record in database"""
        try:
            with self.database.atomic():
                existing_collection = Collections.get_or_none(Collections.collection_id == collection_data['collection_id'])
                
                if existing_collection:
                    Collections.update(**collection_data).where(
                        Collections.collection_id == collection_data['collection_id']
                    ).execute()
                    return True, f"Updated collection {collection_data['collection_name']}"
                else:
                    Collections.create(**collection_data)
                    return True, f"Created collection {collection_data['collection_name']}"

        except peewee.OperationalError as error:
            return False, f"Collection database error for {collection_data['collection_name']}: {str(error)}"
    
    def write_incident_record(self, incident_data):
        """Method to create or update incident record in database"""
        try:
            with self.database.atomic():
                existing_incident = Incidents.get_or_none(Incidents.incident_id == incident_data['incident_id'])
                
                if existing_incident:
                    Incidents.update(**incident_data).where(
                        Incidents.incident_id == incident_data['incident_id']
                    ).execute()
                    return True, f"Updated incident report with id {incident_data['incident_id']}"
                else:
                    Incidents.create(**incident_data)
                    return True, f"Created new incident report with id {incident_data['incident_id']}"

        except peewee.OperationalError as error:
            return False, f"Incident record database error for report with id {incident_data['incident_id']}: {str(error)}"
    
    def write_workplan(self, workplan_data):
        """Method to create or update workplan record in database"""
        try:
            with self.database.atomic():
                existing_workplan = Workplans.get_or_none(Workplans.workplan_id == workplan_data['workplan_id'])
                
                if existing_workplan:
                    Workplans.update(**workplan_data).where(
                        Workplans.workplan_id == workplan_data['workplan_id']
                    ).execute()
                    return True, f"Updated workplan with id {workplan_data['workplan_id']}"
                else:
                    Workplans.create(**workplan_data)
                    return True, f"Created new workplan with id {workplan_data['workplan_id']}"

        except peewee.OperationalError as error:
            return False, f"Workplan database error for report with id {workplan_data['workplan_id']}: {str(error)}"
    
    def write_component_type(self, component_type_data):
        """Method to write component type record in database"""
        try:
            with database.atomic():
                component_type = self.read_single_component_type(component_type_data["component_type"])

                if component_type:
                    (ComponentTypes
                     .update(**component_type_data)
                     .where(ComponentTypes.component_type == component_type_data["component_type"])
                     .execute())
                    return True, f"Updated component type {component_type_data['component_type']}"

                else:
                    ComponentTypes.create(**component_type_data)
                    return True, f"Created component type {component_type_data['component_type']}"
        
        except peewee.OperationalError as error:
            return False, f"{component_type_data['component_type']}: {str(error)}."

    def write_delete_record(self, table_selector, record_id):
        """Method to delete a given record and associated records"""
        try:
            with self.database.atomic():
                if table_selector == "ComponentTypes":
                    record = self.read_single_component_type(record_id)
                    if record:
                        record.delete_instance()
                        return True, f"Deleted component type: {record_id}"
                
                elif table_selector == "Incidents":
                    record = self.read_single_incident_report(record_id)
                    if record:
                        record.delete_instance()
                        return True, f"Deleted incident report with id {record_id}"
                
                elif table_selector == "Workplans":
                    record = self.read_single_workplan(record_id)
                    if record:
                        record.delete_instance()
                        return True, f"Deleted workplan with id {record_id}"
                
                elif table_selector == "Components":
                    record = self.read_component(record_id)
                    if record:
                        services_deleted = Services.delete().where(Services.component_id == record_id).execute()
                        history_deleted = ComponentHistory.delete().where(ComponentHistory.component_id == record_id).execute()
                        record.delete_instance()
                        return True, f"Deleted component: {record.component_name}, related records deleted: {services_deleted} service(s), {history_deleted} history record(s)"
                
                elif table_selector == "Collections":
                    record = self.read_single_collection(record_id)
                    if record:
                        record.delete_instance()
                        return True, f"Deleted collection with id {record_id}"

                elif table_selector == "Services":
                    record = self.read_single_service_record(record_id)
                    if record:
                        record.delete_instance()
                        return True, f"Deleted service record with id {record_id}"
                
                elif table_selector == "ComponentHistory":
                    record = self.read_single_history_record(record_id)
                    if record:
                        record.delete_instance()
                        return True, f"Deleted installation history record with id {record_id}"

                else:
                    return False, "Invalid table selector"

                if not record:
                    return False, f"Record not found: {record_id}"

        except peewee.OperationalError as error:
            return False, {str(error)}
