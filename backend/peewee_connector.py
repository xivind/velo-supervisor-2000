#!/usr/bin/env python3
"""Module to interact with a SQL database through Peewee"""

import logging
from datetime import datetime
import peewee
import traceback
import uuid
import time
from peewee_models import database, Rides, Bikes, Components, Services, ComponentTypes, ComponentHistory #Match with export from peewee_models, maybe base_model is not needed since it is inherited?


class ReadTables(): #rename to something else, internal logic or something, might split into separate classes
    """Class to interact with a SQL database through peewee""" #Modify this description
    def __init__(self):
        pass #Check out this one..

    def read_component_types(self):
        """Method to read content of component_types table"""
        component_types = ComponentTypes.select()
        return component_types
    
    def read_all_components(self):
        """Method to read content of components table"""
        components = Components.select()
        return components
    
    def read_subset_components(self, bike_id):
        """Method to read components for a specific bike"""
        components = Components.select().where(Components.bike_id == bike_id)
        return components

    def read_recent_rides(self, bike_id):
        """Method to read recent rides for a specific bike"""
        recent_rides = Rides.select().where(Rides.bike_id == bike_id)
        recent_rides = (Rides.select().where(Rides.bike_id == bike_id).order_by(Rides.record_time.desc()).limit(5)) #Is this a duplicate? Can be merged with statement above?
        return recent_rides
    
    def read_bikes(self):
        """Method to read content of bikes table"""
        bikes = Bikes.select()
        return bikes
    
    def read_subset_component_history(self, component_id):
        """Method to read a subset of receords from the component history table"""
        component_history = ComponentHistory.select().where(ComponentHistory.component_id == component_id).order_by(ComponentHistory.updated_date.desc())
        if component_history.exists():
            return component_history
        
        return None

    def read_subset_service_history(self, component_id):
        """Method to read a subset of receords from the component history table"""
        service_history = Services.select().where(Services.component_id == component_id).order_by(Services.service_date.desc())
        if service_history.exists():
            return service_history
        
        return None


class ModifyTables(): #rename to something else, internal logic or something, might split into separate classes
    """Class to interact with a SQL database through peewee""" #Modify this description
    def __init__(self):
        pass #Check out this one..

    def update_rides_bulk(self, ride_list):
        """Method to create or update ride data in bulk to database"""
        logging.info(f'There are {len(ride_list)} rides in the list')

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

                    logging.info("Rides table updated successfully")

        except peewee.OperationalError as error:
            logging.error(f"An error occurred while updating the rides table: {error}")

    def update_bikes(self, bike_list):
        """Method to create or update bike data to the database"""
        try:
            with database.atomic():
                for bike_data in bike_list:
                    existing_bike = Bikes.get_or_none(Bikes.bike_id == bike_data["bike_id"])

                    if existing_bike:
                        filtered_bike_data = {key: value for key, value in bike_data.items() if key != 'bike_id'}
                        query = Bikes.update(**filtered_bike_data).where(Bikes.bike_id == bike_data["bike_id"])
                        query.execute()
                        logging.info(f'Record for bike with id {bike_data["bike_id"]} updated')

                    else:
                        query = Bikes.insert(**bike_data)
                        query.execute()
                        logging.info(f'Record for bike with id {bike_data["bike_id"]} inserted')

        except peewee.OperationalError as error:
            logging.error(f'An error occurred while updating the bikes table: {error}')

    def update_components_distance_selector(self, delimiter):
        """Method to determine which selection of components to update"""
        try:
            try:
                if delimiter == "all":
                    logging.info("All installed components selected")
                    with database.atomic():
                        for component in Components.select().where(Components.installation_status == 'Installed'):
                            self.update_component_distance(component)

            except (peewee.OperationalError, ValueError) as error:
                logging.error(f'An error occurred while selecting all installed components : {error}')

            try:
                if isinstance(delimiter, set):
                    logging.info("Components on recently used bikes selected")
                    with database.atomic():
                        for bike_id in delimiter:
                            for component in Components.select().where((Components.installation_status == 'Installed') & (Components.bike_id == bike_id)):
                                self.update_component_distance(component)

            except (peewee.OperationalError, ValueError) as error:
                logging.error(f'An error occurred while selecting components on recently used bikes : {error}')

            try:
                if "b" in delimiter: #This works, but probably only because it evaluates after delimiter set. Consider how to make this more resilient
                    logging.info(f"Components on bike with id {delimiter} selected")
                    with database.atomic():
                        for component in Components.select().where((Components.installation_status == 'Installed') & (Components.bike_id == delimiter)):
                            self.update_component_distance(component)

            except (peewee.OperationalError, ValueError) as error:
                logging.error(f'An error occurred while selecting components on a single bike : {error}')

        except (peewee.OperationalError, ValueError) as error:
            logging.error(f'An error occurred while selecting which components to update: {error}')

    def update_component_distance(self, component_id, current_distance):
        """Method to update component table with distance from ride table"""
        try:
            component = Components.get(Components.component_id == component_id)
            distance_offset = component.component_distance_offset
            total_distance = current_distance + distance_offset
    
            with database.atomic():
                component.component_distance = total_distance
                component.save()

            logging.info(f"Updated distance for component {component.component_name} (id {component.component_id})")
            
            updated_component = Components.get(Components.component_id == component_id)
            self.update_component_service_status(updated_component)
            self.update_component_lifetime_status(updated_component)
            self.update_bike_status(updated_component.bike_id)

        except (peewee.OperationalError, ValueError) as error:
            logging.error(f'An error occurred while updating component distance for component {component.component_name} (id {component.component_id}): {error}')

    def update_component_service_status(self, component):
        """Method to update component table with service status"""
        
        if component.service_interval:
            try:
                logging.info(f"Updating service status for component {component.component_name} with component id {component.component_id}")
                latest_service_record = Services.select().where(Services.component_id == component.component_id).order_by(Services.service_date.desc()).first()
                latest_history_record = ComponentHistory.select().where(ComponentHistory.component_id == component.component_id).order_by(ComponentHistory.updated_date.desc()).first()

                if component.installation_status == "Installed":
                    if latest_service_record is None:
                        logging.info(f'No service record found for component with id {component.component_id}. Using distance from installation log and querying distance from installation date to today')
                        distance_since_service = latest_history_record.distance_marker
                        matching_rides = Rides.select().where((Rides.bike_id == component.bike_id) & (Rides.record_time >= latest_history_record.updated_date))
                        distance_since_service += sum(ride.ride_distance for ride in matching_rides)
                        
                    elif latest_service_record:
                        logging.info(f'Service record found for for component with id {component.component_id}. Querying distance from previous service date to today')
                        matching_rides = Rides.select().where((Rides.bike_id == component.bike_id) & (Rides.record_time >= latest_service_record.service_date))
                        distance_since_service = sum(ride.ride_distance for ride in matching_rides)

                elif component.installation_status != "Installed":
                    if latest_service_record is None:
                        logging.info(f'Component with id {component.component_id} has been uninstalled and there are no previous services. Setting distance since service to distance at the time of uninstallation')
                        distance_since_service = latest_history_record.distance_marker
                    
                    elif latest_service_record:
                        if latest_service_record.service_date > component.updated_date:
                            logging.info(f'Component with id {component.component_id} has been serviced after uninstall. Setting distance since service to 0')
                            distance_since_service = 0
                    
                        elif latest_service_record.service_date < component.updated_date:
                            logging.info(f'Component with id {component.component_id} has no services after uninstall, but a previous service exist. Using already calculated distance to next service')
                            distance_since_service = component.service_interval + component.service_next*-1
            
                service_next = component.service_interval - distance_since_service

                with database.atomic():
                    component.service_next = service_next
                    component.service_status = self.compute_component_status("service", self.calculate_percentage_reached(int(component.service_interval), int(service_next)))
                    component.save()

            except peewee.OperationalError as error:
                logging.error(f'An error occurred while updating service status for component {component.component_name} with component id {component.component_id}: {error}')

        else:
            try:
                logging.info(f"Component {component.component_name} with component id {component.component_id} has no service interval, setting NULL values for service")
                with database.atomic():
                    component.service_next = None
                    component.service_status = None
                    component.save()

            except peewee.OperationalError as error:
                logging.error(f'An error occurred while setting blank service status for component {component.component_name} with component id {component.component_id}: {error}')

    def update_component_lifetime_status(self, component):
        """Method to update component table with lifetime status"""
        if component.lifetime_expected:
            try:
                logging.info(f"Updating lifetime status for component {component.component_name} (id {component.component_id})")

                with database.atomic():
                    component.lifetime_remaining = component.lifetime_expected - component.component_distance
                    component.lifetime_status = self.compute_component_status("lifetime", self.calculate_percentage_reached(int(component.lifetime_expected), int(component.lifetime_remaining)))
                    component.save()

            except peewee.OperationalError as error:
                logging.error(f'An error occurred while updating lifetime status for component {component.component_name} (id {component.component_id}): {error}')

        else:
            try:
                logging.info(f"Component {component.component_name} (id {component.component_id}) has no expected lifetime, setting NULL values for lifetime")

                with database.atomic():
                    component.lifetime_remaining = None
                    component.lifetime_status = None
                    component.save()

            except peewee.OperationalError as error:
                logging.error(f'An error occurred while setting blank lifetime status for component {component.component_name} (id {component.component_id}): {error}')

    def update_bike_status(self, bike_id):
        """Method to update status for a given bike based on component service and lifetime status"""
        
        if bike_id is None:
            logging.warning(f"Bike context is missing. Skipping update of bike status...")
        
        else:
            try:
                bike = Bikes.get_or_none(Bikes.bike_id == bike_id)
                components = Components.select().where(Components.bike_id == bike_id)
                
                logging.info(f"Updating bike status for bike {bike.bike_name} with id {bike.bike_id}")
                
                bike_status = {"breakdown_imminent": 0,
                            "maintenance_required": 0,
                            "maintenance_approaching": 0,
                            "ok": 0}

                if components.exists():
                    for component in components:
                        if component.installation_status == "Installed":
                            if component.lifetime_status == "Lifetime exceeded" or component.service_status =="Service interval exceeded":
                                bike_status["breakdown_imminent"] += 1
                            elif component.lifetime_status == "Due for replacement" or component.service_status =="Due for service":
                                bike_status["maintenance_required"] += 1
                            elif component.lifetime_status == "End of life approaching" or component.service_status =="Service approaching":
                                bike_status["maintenance_approaching"] += 1
                            elif component.lifetime_status == "OK" or component.service_status =="OK":
                                bike_status["ok"] += 1

                    if bike_status["breakdown_imminent"] > 0:
                        service_status = "Breakdown imminent"
                    elif bike_status["maintenance_required"] > 0:
                        service_status = "Maintenance required"
                    elif bike_status["maintenance_approaching"] > 0:
                        service_status = "Maintenance approaching"
                    elif bike_status["ok"] > 0:
                        service_status = "Pristine condition"
                    else:
                        service_status = "Maintenance not defined"
                    
                else:
                    service_status = None
            
                logging.info(f"New status for bike {bike.bike_name}: {service_status}")

                with database.atomic():
                    bike.service_status = service_status
                    bike.save()
            
            except Exception as error:
                logging.error(f'An error occurred while updating bike status for {bike.bike_name} with id {bike.bike_id}): {error}')
    
    def compute_component_status(self, mode, reached_distance_percent): #move to misc? Can be others also. Could be possible by calling classes directly
        """Method to compute service status"""
        if mode == "service":
            if 0 <= reached_distance_percent <= 70:
                status = "OK"
            elif 70 < reached_distance_percent <= 90:
                status = "Service approaching"
            elif 90 < reached_distance_percent <= 100:
                status = "Due for service"
            elif reached_distance_percent > 100:
                status = "Service interval exceeded"

        if mode == "lifetime":
            if 0 <= reached_distance_percent <= 70:
                status = "OK"
            elif 70 < reached_distance_percent <= 90:
                status = "End of life approaching"
            elif 90 < reached_distance_percent <= 100:
                status = "Due for replacement"
            elif reached_distance_percent > 100:
                status = "Lifetime exceeded"

        return status

    def calculate_percentage_reached(self, total, remaining): #move to misc?  Can be others also. Could be possible by calling classes directly
        """Method to calculate remaining service interval or remaining lifetime as percentage"""
        if isinstance(total, int) and isinstance(remaining, int):
            return round(((total - remaining) / total) * 100, 2)
        
        return 1000

class ReadRecords():
    """Class to interact with a SQL database through peewee""" #Modify this description
    def __init__(self):
        pass #Check out this one.

    def read_bike(self, bike_id):
        """Method to retrieve record for a specific bike"""
        bike = Bikes.get_or_none(Bikes.bike_id == bike_id)
        return bike
    
    def read_component(self, component_id):
        """Method to retrieve record for a specific component"""
        component = Components.get_or_none(Components.component_id == component_id)
        return component
    
    def read_history_record(self, history_id):
        """Method to retrieve record for a specific entry in installation log"""
        history_record = ComponentHistory.get_or_none(ComponentHistory.history_id == history_id)
        return history_record
    
    def read_latest_history_record(self, component_id):
        """Method to retrieve the most recent record from the installation log of a given component"""
        latest_history_record = ComponentHistory.select().where(ComponentHistory.component_id == component_id).order_by(ComponentHistory.updated_date.desc()).first()
        return latest_history_record

    def read_latest_service_record(self, component_id):
        """Method to retrieve the most recent record from the service log of a given component"""
        latest_service_record = Services.select().where(Services.component_id == component_id).order_by(Services.service_date.desc()).first()
        return latest_service_record


class ModifyRecords(): #Consider merging with modify tables
    """Class to interact with a SQL database through peewee""" #Modify this description
    def __init__(self):
        pass #Check out this one.

    def update_component_type(self, component_type_data): #Improve this one, see update_component method for blueprint
        """Method to create or update component types"""
    
        try:
            logging.info(f"Creating or updating component type {component_type_data['component_type']}") #MOve this down to the appropriate section
            with database.atomic():
                component_type = ComponentTypes.get_or_none(ComponentTypes.component_type == component_type_data["component_type"])

                if component_type:
                    component_type.component_type = component_type_data["component_type"]
                    component_type.service_interval = component_type_data["service_interval"]
                    component_type.expected_lifetime = component_type_data["expected_lifetime"]
                    component_type.save()
                    # Missing log statement
            
                else:
                    ComponentTypes.create(
                        component_type = component_type_data["component_type"],
                        service_interval = component_type_data["service_interval"],
                        expected_lifetime = component_type_data["expected_lifetime"])
                    # Missing log statement
        
        except peewee.OperationalError as error:
                logging.error(f'An error occurred while creating or updating component type {component_type_data["component_type"]}: {error}')
    
    def update_component_details(self, component_id, new_component_data):
        """Method to create or update component data to the database"""
        try:
            with database.atomic():
                component = Components.get_or_none(Components.component_id == component_id)
                
                if component:
                    Components.update(**new_component_data).where(Components.component_id == component_id).execute()
                    logging.info(f'Record for component with id {component_id} updated')

                else:
                    new_component_data.update({"component_distance": 0,
                                               "component_id": component_id})

                    Components.create(**new_component_data)
                    logging.info(f'Record for component with id {component_id} created')

        except peewee.OperationalError as error:
            logging.error(f'An error occurred while creating og updating component: {error}')

    def update_service_history(self, service_data):
        try:
            Services.create(**service_data)
            logging.info(f'Added record to service history with id {service_data["service_id"]} for component with id {service_data["component_id"]}')

        except peewee.OperationalError as error:
            logging.error(f'An error occurred while adding service record for component with id {service_data["component_id"]}: {error}')

    
    def update_component_history_record(self, old_component_name, latest_history_record, current_history_id, component_id, previous_bike_id, updated_bike_id, updated_component_installation_status, component_updated_date, historic_distance):
        """Method to create or update component history and write to the database"""
        try:
            halt_update = False

            if latest_history_record is None and updated_component_installation_status != "Installed":
                logging.warning(f"Cannot change a component that is not installed, component id {component_id}. Skipping...") #Can use return on these statements instead?
                halt_update = True
            
            elif latest_history_record is None:
                if updated_bike_id is None:
                    logging.warning(f"Cannot set status to installed without specifying bike, component id {component_id}. Skipping...")
                    halt_update = True
                else:
                    bike_id = updated_bike_id
            
            else:
                if latest_history_record.history_id == current_history_id:
                    logging.warning(f"Historic record already exist for component id {component_id} and record id {current_history_id}. Skipping...")
                    halt_update = True
                
                elif latest_history_record.update_reason == updated_component_installation_status:
                    logging.warning(f"Component status is already set to: {latest_history_record.update_reason}. Skipping...")
                    halt_update = True
                            
                else:
                    if updated_component_installation_status == "Installed":
                        if updated_bike_id is None:
                            logging.warning(f"Cannot set status to installed without specifying bike, component id {component_id}. Skipping...")
                            halt_update = True
                        else:
                            bike_id = updated_bike_id
                    
                    elif updated_component_installation_status == "Retired":
                        bike_id = updated_bike_id

                    elif updated_component_installation_status == "Not installed":
                        bike_id = previous_bike_id
                    
            if halt_update is False:
                with database.atomic():
                    ComponentHistory.create(history_id = current_history_id,
                                        component_id = component_id,
                                        bike_id = bike_id,
                                        component_name = old_component_name,
                                        updated_date = component_updated_date,
                                        update_reason = updated_component_installation_status,
                                        distance_marker = historic_distance)
                        
                    logging.info(f'Added record to installation history with id {current_history_id} for component with id {component_id}')

            return halt_update
        
        except peewee.OperationalError as error:
            logging.error(f'An error occurred while adding installation history record for component with id {component_id}: {error}')
            return True

    def delete_record(self, table_selector, record_id):
        """Method to delete a given record and associated records"""

        try:
            logging.info(f"Deleting record with id {record_id} from table {table_selector}")
            table_found = True
            
            if table_selector == str("ComponentTypes"):
                query = ComponentTypes.get_or_none(ComponentTypes.component_type == record_id)
            elif table_selector == str("Components"):
                query = Components.get_or_none(Components.component_id == record_id)
            else:
                logging.error(f'Error looking up table for deletion of record, non-existing table: {table_selector}')
                table_found = False
        
            if table_found:
                with database.atomic():
                    record = query
                    if record:
                        if table_selector == str("Components"):
                            services_deleted = Services.delete().where(Services.component_id == record_id).execute()
                            history_deleted = ComponentHistory.delete().where(ComponentHistory.component_id == record_id).execute()
                            logging.info(f"Deleted {services_deleted} service records and {history_deleted} history records for component with id {record_id}")
                            
                        record.delete_instance()
                    else:
                        logging.warning(f"No record found with id {record_id} in table {table_selector}")

        except peewee.OperationalError as error:
            logging.error(f'An error occurred while deleting record with id {record_id} from table {table_selector}: {error}')
        
class MiscMethods():
    """Class to interact with a SQL database through peewee""" #Modify this description
    def __init__(self):
        pass #Check out this one.

    def sum_distanse_subset_rides(self, bike_id, start_date, stop_date):
        """Method to sum distance for a given set of rides"""

        matching_rides = Rides.select().where(
                                            (Rides.bike_id == bike_id) &
                                            (Rides.record_time >= start_date) &
                                            (Rides.record_time <= stop_date))
        if matching_rides:
          return sum(ride.ride_distance for ride in matching_rides)
                   
        return 0
    
    def list_unique_bikes(self):
        """Method to query database and create list of unique bike ids"""
        try:
            unique_bike_ids = Rides.select(Rides.bike_id).distinct()
            bike_id_set = {
                ride.bike_id
                for ride in unique_bike_ids
                if ride.bike_id != "None"}

            return bike_id_set

        except (peewee.OperationalError, ValueError) as error:
            logging.error(f"An error occurred while creating list of unique bike_ids: {error}")
            return {}
        
    def generate_unique_id(self):
        """Method to generates a random and unique ID"""
        unique_id_part1 = uuid.uuid4()
        unique_id_part2 = time.time()

        return f'{str(unique_id_part1)[:6]}{str(unique_id_part2)[-4:]}'
    
    def format_datetime(self, date_str):
        """Method to reformat a datetime string"""
        date_obj = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S')
        formatted_datetime = date_obj.strftime('%Y-%m-%d')
        
        return formatted_datetime
    
    def format_component_status(self, status):
        """Method to display user friendly text for None values"""
        if status is not None:
            return status

        return "Not defined"
    
    def format_cost(self, cost):
        """Method to display user friendly text for None values"""
        if cost is not None:
            return cost

        return "No estimate"
    
    def get_bike_name(self, bike_id):
        """Method to get the name of a bike based on bike id"""
        bike = Bikes.get_or_none(Bikes.bike_id == bike_id)
        if bike:
            if bike.bike_name is not None:
                return bike.bike_name
        
        return "Not assigned"
    
    def get_first_ride(self, bike_id):
        """Method to get the date for the first ride for a given bike"""
        oldest_ride_record = Rides.select(Rides.record_time).where(Rides.bike_id == bike_id).order_by(Rides.record_time.asc()).first()
        if oldest_ride_record:
            first_ride =  oldest_ride_record.record_time.split('T')[0]
            return first_ride
        
        return None
    
    def get_component_statistics(self, component_list):
        """Method to summarise key data for a set of components"""
        component_statistics = {"count_installed": 0,
                                "count_not_installed": 0,
                                "count_retired": 0,
                                "count_lifetime_status_green": 0,
                                "count_lifetime_status_yellow": 0,
                                "count_lifetime_status_red": 0,
                                "count_lifetime_status_purple": 0,
                                "count_service_status_green": 0,
                                "count_service_status_yellow": 0,
                                "count_service_status_red": 0,
                                "count_service_status_purple": 0,
                                "sum_cost": 0,
                                }
        
        for component in component_list:
            if component[0] == "Installed":
                component_statistics["count_installed"] += 1
            if component[0] == "Not installed":
                component_statistics["count_not_installed"] += 1
            if component[0] == "Retired":
                component_statistics["count_retired"] += 1
            if component[4] == "OK" and component[0] == "Installed":
                component_statistics["count_lifetime_status_green"] += 1
            if component[4] == "End of life approaching" and component[0] == "Installed":
                component_statistics["count_lifetime_status_yellow"] += 1
            if component[4] == "Due for replacement" and component[0] == "Installed":
                component_statistics["count_lifetime_status_red"] += 1
            if component[4] == "Lifetime exceeded" and component[0] == "Installed":
                component_statistics["count_lifetime_status_purple"] += 1
            if component[5] == "OK" and component[0] == "Installed":
                component_statistics["count_service_status_green"] += 1
            if component[5] == "Service approaching" and component[0] == "Installed":
                component_statistics["count_service_status_yellow"] += 1
            if component[5] == "Due for service" and component[0] == "Installed":
                component_statistics["count_service_status_red"] += 1
            if component[5] == "Service interval exceeded" and component[0] == "Installed":
                component_statistics["count_service_status_purple"] += 1
            if component[6] is not None and isinstance(component[6], int) and component[0] == "Installed":
                    if (component[4] != "OK" and component[4] is not None) or (component[5] != "OK" and component[5] is not None):
                        component_statistics["sum_cost"] += component[6]

        if component_statistics["sum_cost"] == 0:
            component_statistics["sum_cost"] = "No estimate"
            
        return component_statistics

        

    

