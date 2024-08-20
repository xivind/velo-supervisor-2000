#!/usr/bin/env python3
"""Module to interact with a SQL database through Peewee"""

import logging
from datetime import datetime
import peewee
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

    def update_component_distance(self, component): # BROKEN
        """Method to update component table with distance from ride table"""
        try:
            if component.updated_date and component.installation_status == "Installed":
                query_start_date = datetime.strptime(component.updated_date.split()[0], '%Y-%m-%d')
                print(f'This is the query start date: {query_start_date}')
            
                if history_record.update_reason == "Not installed" or history_record.update_reason == "Retired":
                    query_stop_date = datetime.strptime(history_record.updated_date.split()[0], '%Y-%m-%d')
                    print(f'This is the query stop date triggered by delimiter: {query_start_date}')
                else:
                    query_stop_date = datetime.today()
                    print(f'This is the query stop date when no delimiter set: {query_stop_date}')

                matching_rides = Rides.select().where(
                                                    (Rides.bike_id == component.bike_id) & 
                                                    (Rides.record_time >= query_start_date) &
                                                    (Rides.record_time <= query_stop_date))
            

                distance_offset = Components.get(Components.component_id == component.component_id).component_distance_offset
                total_distance_current = sum(ride.ride_distance for ride in matching_rides)
                total_distance = total_distance_current + distance_offset

        
                with database.atomic():
                    component.component_distance = total_distance
                    component.save()

                    logging.info(f"Updated distance for component {component.component_name} (id {component.component_id})")

            self.update_component_service_status(component)
            self.update_component_lifetime_status(component)

        except (peewee.OperationalError, ValueError) as error:
            logging.error(f'An error occurred while updating component distance for component {component.component_name} (id {component.component_id}): {error}')

    def update_component_service_status(self, component):
        """Method to update component table with service status"""
        if component.service_interval:
            try:
                logging.info(f"Updating service status for component {component.component_name} (id {component.component_id})")

                services = Services.select().where((Services.component_id == component.component_id))
                service_list = [
                    service.service_date
                    for service in services
                    if service.service_date != "None"]
                service_list = sorted(service_list, reverse=True)

                if len(service_list) > 0:
                    newest_service = service_list[0]
                    matching_rides = Rides.select().where((Rides.bike_id == component.bike_id) & (Rides.record_time >= newest_service))
                    distance_since_service = sum(ride.ride_distance for ride in matching_rides)

                elif len(service_list) == 0:
                    distance_since_service = component.component_distance

                service_next = component.service_interval- distance_since_service

                with database.atomic():
                    component.service_next = service_next
                    component.service_status = self.compute_component_status("service", self.calculate_percentage_reached(int(component.service_interval), int(service_next)))
                    component.save()

            except peewee.OperationalError as error:
                logging.error(f'An error occurred while updating service status for component {component.component_name} (id {component.component_id}): {error}')

        else:
            try:
                logging.info(f"Component {component.component_name} (id {component.component_id}) has no service interval, setting NULL values for service")
                with database.atomic():
                    component.service_next = None
                    component.service_status = "Not defined"
                    component.save()

            except peewee.OperationalError as error:
                logging.error(f'An error occurred while setting blank service status for component {component.component_name} (id {component.component_id}): {error}')

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
                    component.lifetime_status = "Not defined"
                    component.save()

            except peewee.OperationalError as error:
                logging.error(f'An error occurred while setting blank lifetime status for component {component.component_name} (id {component.component_id}): {error}')

    def compute_component_status(self, mode, reached_distance_percent): #move to misc? Can be others also. Could be possible by calling classes directly
        """Method to compute service status"""

        if mode == "service":
            if int(reached_distance_percent) in range(0, 76):
                status = "OK"
            elif int(reached_distance_percent) in range(76, 100):
                status = "Service approaching"
            elif int(reached_distance_percent) >= 100:
                status = "Due for service"

        if mode == "lifetime":
            if int(reached_distance_percent) in range(0, 76):
                status = "OK"
            elif int(reached_distance_percent) in range(76, 100):
                status = "Lifetime approaching"
            elif int(reached_distance_percent) >= 100:
                status = "Lifetime reached"

        return status

    def calculate_percentage_reached(self, total, remaining): #move to misc?  Can be others also. Could be possible by calling classes directly
        """Method to calculate remaining service interval or remaining lifetime as percentage"""
        if isinstance(total, int) and isinstance(remaining, int):
            return int(((total - remaining) / total) * 100)
        
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
        """Method to retrieve record for a specific entry in installation log"""
        latest_history_record = ComponentHistory.select().where(ComponentHistory.component_id == component_id).order_by(ComponentHistory.updated_date.desc()).first()
        return latest_history_record


class ModifyRecords(): #Consider merging with modify tables
    """Class to interact with a SQL database through peewee""" #Modify this description
    def __init__(self):
        pass #Check out this one.

    def update_component_type(self, component_type_data):
        """Method to create or update component types"""
    
        try:
            logging.info(f"Creating or updating component type {component_type_data['component_type']}")
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
                    if component.component_distance is None:
                        adjusted_component_distance = 0
                    else:
                        adjusted_component_distance = component.component_distance

                    component.installation_status = new_component_data["component_installation_status"]
                    component.updated_date = new_component_data["component_updated_date"]
                    component.component_name = new_component_data["component_name"]
                    component.component_type = new_component_data["component_type"]
                    component.bike_id = new_component_data["component_bike_id"]
                    component.component_distance = adjusted_component_distance
                    component.lifetime_expected = new_component_data["expected_lifetime"]
                    component.service_interval = new_component_data["service_interval"]
                    component.cost = new_component_data["cost"]
                    component.component_distance_offset = new_component_data["offset"]
                    component.notes = new_component_data["component_notes"]
                    component.save()
                    logging.info(f'Record for component with id {component_id} updated')

                else:
                    # Must create ID
                    #Components.create(
                    #    component_type = component_type_data["component_type"],
                    #    service_interval = component_type_data["service_interval"],
                    #    expected_lifetime = component_type_data["expected_lifetime"])

                    logging.info(f'Record for component with id {component_id} inserted - NOT IMPLEMENTED')

        except peewee.OperationalError as error:
            logging.error(f'An error occurred while creating og updating component: {error}')

    def update_component_history_record(self, old_component_data, latest_history_record, current_historic_record_id, component_id, updated_bike_name, updated_component_installation_status, component_updated_date, distance_marker):
        """Method to create or update component history and write to the database"""
        try:
        # Consider if check is required for existing historic record id or that a first record exist, maybe not needed
            if latest_history_record is None and updated_component_installation_status != "Installed":
                print("Warning. Cannot change a component that is not installed. Skipping.. ")
            
            elif latest_history_record.update_reason == updated_component_installation_status:
                print(f"Warning! Component status is already set to: {latest_history_record.update_reason}. Skipping...")
                        
            else:
                if updated_component_installation_status == "Installed":
                    print("")
                
                elif updated_component_installation_status == "Retired":
                    print("")

                elif updated_component_installation_status == "Not installed":
                    print("")
                    
                    

                    elif component.installation_status == "Not installed" or component.installation_status == "Retired":
                        print(f"Warning! Component status is already set to: {latest_historic_record.update_reason}. Skipping...")


                    
                    if latest_historic_record is not None and latest_historic_record.update_reason == "Installed":
                        print("Estimating distance before uninstall")
                        query_start_date = datetime.strptime(latest_historic_record.updated_date.split()[0], '%Y-%m-%d')
                        query_stop_date = datetime.strptime(query_stop_date.split()[0], '%Y-%m-%d') #This statements do not seem to have effect? Check this other places also, append .date() to remove trailing zeros
                        print(query_start_date, query_stop_date)

                        #Move this to separate function, requires bike_id from before update
                        
                        bike_name = latest_component_history_record.bike_name

                    else:
                        
                with database.atomic():           
                    ComponentHistory.create(history_id = current_historic_record_id,
                                        component_id = component_id,
                                        bike_name = bike_name,
                                        component_name = component.component_name,
                                        updated_date = component.updated_date,
                                        update_reason = component.installation_status,
                                        distance_marker = distance_marker)
                    
                        logging.info(f'Created record to installtion history with id {history_id} for component with id {component_id}')

            
        except peewee.OperationalError as error:
            logging.error(f'An error occurred while adding or updatering record for installation history for component with id {component_id}: {error}')
    
    def delete_record(self, table_selector, record_id):
        """Method to delete any record"""

        try:
            logging.info(f"Deleting record with id {record_id} from table {table_selector}")
            if table_selector == str("ComponentTypes"):
                query = ComponentTypes.get_or_none(ComponentTypes.component_type == record_id)
                table_found = True
            elif table_selector == str("Services"):
                query = Services.get_or_none(Services.service_id == record_id)
                table_found = True
            else:
                logging.error(f'Error looking up table for deletion of record, non-existing table: {table_selector}')
                table_found = False
        
            if table_found:
                with database.atomic():
                    record = query
                    if record:
                        record.delete_instance()

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
                                "count_service_status_green": 0,
                                "count_service_status_yellow": 0,
                                "count_service_status_red": 0,
                                "sum_cost": 0,
                                }
        
        for component in component_list:
            if component[0] == "Installed":
                component_statistics["count_installed"] += 1
            if component[0] == "Not installed":
                component_statistics["count_not_installed"] += 1
            if component[0] == "Retired":
                component_statistics["count_retired"] += 1
            if component[4] == "OK":
                component_statistics["count_lifetime_status_green"] += 1
            if component[4] == "Lifetime approaching":
                component_statistics["count_lifetime_status_yellow"] += 1
            if component[4] == "Lifetime reached":
                component_statistics["count_lifetime_status_red"] += 1
            if component[5] == "OK":
                component_statistics["count_service_status_green"] += 1
            if component[5] == "Service approaching":
                component_statistics["count_service_status_yellow"] += 1
            if component[5] == "Due for service":
                component_statistics["count_service_status_red"] += 1
            if component[6] is not None and isinstance(component[6], (int)):
                component_statistics["sum_cost"] += component[6]

        if component_statistics["sum_cost"] == 0:
            component_statistics["sum_cost"] = "No estimate"
            
        return component_statistics

        

    

