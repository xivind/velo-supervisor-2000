#!/usr/bin/env python3
"""Module to handle business logic"""

import logging
from datetime import datetime
import peewee
from database_model import database, Rides, Bikes, Components, Services, ComponentTypes, ComponentHistory #This will be removed afer refactoring
from utils import read_parameters, calculate_percentage_reached
from strava import Strava
from database_manager import DatabaseManager

# Load configuration
CONFIG = read_parameters()

# Create database manager object
database_manager = DatabaseManager()

# Initialize Strava API
strava = Strava(CONFIG['strava_tokens'])




class ModifyTables(): #rename to something else, internal logic or something, might split into separate classes
    """Class to interact with a SQL database through peewee""" #Modify this description
    def __init__(self):
        pass #Check out this one..


    def update_component_distance(self, component_id, current_distance):
        """Method to update component table with distance from ride table"""
        try:
            component = Components.get(Components.component_id == component_id) 
            distance_offset = component.component_distance_offset
            total_distance = current_distance + distance_offset
    
            with database.atomic():
                component.component_distance = total_distance
                component.save()

            logging.info(f"Updated distance for component {component.component_name} (id {component.component_id}). New total distance: {total_distance}")
            
            updated_component = Components.get(Components.component_id == component_id)
            
            if updated_component.bike_id is None: #Refactor with classmethod, this one should use existing method instead
                bike_id = ComponentHistory.select().where(ComponentHistory.component_id == component_id).order_by(ComponentHistory.updated_date.desc()).first().bike_id

            else:
                bike_id = updated_component.bike_id
            
            self.update_component_lifetime_status(updated_component)
            self.update_component_service_status(updated_component)
            self.update_bike_status(bike_id)

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
                    component.service_status = self.compute_component_status("service", calculate_percentage_reached(component.service_interval, int(service_next)))
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
                    component.lifetime_status = self.compute_component_status("lifetime", calculate_percentage_reached(component.lifetime_expected, int(component.lifetime_remaining)))
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

        try:
            bike = Bikes.get_or_none(Bikes.bike_id == bike_id)
            components = Components.select().where(Components.bike_id == bike_id)
            
            logging.info(f"Updating bike status for bike {bike.bike_name} with id {bike.bike_id}")
            
            component_status = {"breakdown_imminent": 0,
                        "maintenance_required": 0,
                        "maintenance_approaching": 0,
                        "ok": 0}
            
            count_installed = 0
            count_retired = 0

            if components.exists():
                for component in components:
                    if component.installation_status == "Installed":
                        count_installed += 1
                        if component.lifetime_status == "Lifetime exceeded" or component.service_status =="Service interval exceeded":
                            component_status["breakdown_imminent"] += 1
                        elif component.lifetime_status == "Due for replacement" or component.service_status =="Due for service":
                            component_status["maintenance_required"] += 1
                        elif component.lifetime_status == "End of life approaching" or component.service_status =="Service approaching":
                            component_status["maintenance_approaching"] += 1
                        elif component.lifetime_status == "OK" or component.service_status =="OK":
                            component_status["ok"] += 1
                    
                    if component.installation_status == "Retired":
                        count_retired += 1

                if component_status["breakdown_imminent"] > 0:
                    service_status = "Breakdown imminent"
                elif component_status["maintenance_required"] > 0:
                    service_status = "Maintenance required"
                elif component_status["maintenance_approaching"] > 0:
                    service_status = "Maintenance approaching"
                elif component_status["ok"] > 0:
                    service_status = "Pristine condition"
                elif all(value == 0 for value in component_status.values()) and count_installed > 0:
                    service_status = "Maintenance not defined"
                elif count_installed == 0 and count_retired > 0:
                    service_status = "No active components"
            
            else:
                service_status = "No components registered"
        
            logging.info(f"New status for bike {bike.bike_name}: {service_status}")

            with database.atomic():
                bike.service_status = service_status
                bike.save()
        
        except Exception as error:
            logging.error(f'An error occurred while updating bike status for {bike.bike_name} with id {bike.bike_id}): {error}')
    
    def compute_component_status(self, mode, reached_distance_percent): #This is business 
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

# REFACTORED METHODS Add class here BusinessLogic, takes app as argument)

    async def update_rides_bulk(self, mode):
        """Method to create or update ride data in bulk to database"""
        logging.info(f"Retrieving rides from Strava. Mode set to: {mode}")
        await strava.get_rides(mode)
        logging.info(f'There are {len(strava.payload_rides)} rides in the list')

        success, message = database_manager.update_rides_bulk(strava.payload_rides)

        if success:
            logging.info(f"Bulk update of database OK: {message}")
        else:
            logging.error(f"Bulk update of database failed: {message}")

        if mode == "all":
            logging.info("Refreshing all bikes from Strava")
            await strava.get_bikes(database_manager.get_unique_bikes())
            success, message = database_manager.update_bikes(strava.payload_bikes)
            
            if success:
                logging.info(f"Bike update OK: {message}")
            else:
                logging.error(f"Bike update failed failed: {message}")
            
            modify_tables.update_components_distance_iterator(database_manager.get_unique_bikes())

        if mode == "recent":
            if len(strava.bike_ids_recent_rides) > 0:
                logging.info("Refreshing bikes used in recent rides from Strava")
                await strava.get_bikes(strava.bike_ids_recent_rides)
                success, message = database_manager.update_bikes(strava.payload_bikes)
                
                if success:
                    logging.info(f"Bike update OK: {message}")
                else:
                    logging.error(f"Bike update failed failed: {message}")
                
                modify_tables.update_components_distance_iterator(strava.bike_ids_recent_rides)

            else:
                logging.warning("No bikes found in recent activities")
        
        # See method below for how logging should be done
        #app.state.strava_last_pull = datetime.now() Disable during refactoring, app must be made available somehow
        #set_time_strava_last_pull(app, read_records) Disable during refactoring

        # Include return statement to route handler, see below
        
    def update_components_distance_iterator(self, bike_ids): #This function only prints to console, no message to user
        """Method to determine which selection of components to update"""
        try:
            logging.info(f'Iterating over bikes to find components to update. Received {len(bike_ids)} bikes')
            for bike_id in bike_ids: #Replace for loop with function
                for component in Components.select().where(
                    (Components.installation_status == 'Installed') &
                    (Components.bike_id == bike_id)).execute():
                    
                    latest_history_record = database_manager.read_latest_history_record(component.component_id) #Is this correct?
                    current_component_distance = latest_history_record.distance_marker
                    matching_rides = Rides.select().where((Rides.bike_id == component.bike_id) & (Rides.record_time >= latest_history_record.updated_date)) #Replace with function
                    current_component_distance += sum(ride.ride_distance for ride in matching_rides)
                    self.update_component_distance(component.component_id, current_component_distance)

        except (peewee.OperationalError, ValueError) as error:
            logging.error(f'An error occurred while iterating over bikes to find components to update: {error}')
    
    #More functions below, following the sequence from functions above
    
    def delete_record(self, table_selector, record_id):
        """Method to delete a given record and associated records"""
        logging.info(f"Attempting to delete record with id {record_id} from table {table_selector}")
        
        success, message = database_manager.delete_record(table_selector, record_id)
        
        if success:
            logging.info(f"Deletion successful: {message}")
        else:
            logging.error(f"Deletion failed: {message}")

        return success, message
    
    def set_time_strava_last_pull(self, app, read_records): #Read records should be called from database manager
        """
        Function to set the date for last pull from Strava
        Args:
            app: FastAPI application instance
            read_records: ReadRecords instance for database access
        """
        if app.state.strava_last_pull:
            days_since = (datetime.now() - app.state.strava_last_pull).days
            app.state.strava_last_pull = app.state.strava_last_pull.strftime("%Y-%m-%d %H:%M")
            app.state.strava_days_since_last_pull = days_since
        
        elif app.state.strava_last_pull is None and read_records.read_latest_ride_record():
            app.state.strava_last_pull = datetime.strptime(read_records.read_latest_ride_record().record_time, "%Y-%m-%d %H:%M")
            app.state.strava_days_since_last_pull = (datetime.now() - app.state.strava_last_pull).days

        else:
            app.state.strava_last_pull = "never"
            app.state.strava_days_since_last_pull = None