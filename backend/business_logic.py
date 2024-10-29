#!/usr/bin/env python3
"""Module to handle business logic"""

import logging
from datetime import datetime
from utils import read_config, calculate_percentage_reached, generate_unique_id
from strava import Strava
from database_manager import DatabaseManager

# Load configuration
CONFIG = read_config()

# Create database manager object
database_manager = DatabaseManager()

# Initialize Strava API
strava = Strava(CONFIG['strava_tokens'])

class BusinessLogic():
    """Class that contains business logic""" 
    def __init__(self, app_state):
        self.app_state = app_state

    # Read methods here
    
    async def update_rides_bulk(self, mode):
        """Method to create or update ride data in bulk to database"""
        logging.info(f"Retrieving rides from Strava. Mode set to: {mode}.")
        await strava.get_rides(mode)
        logging.info(f'There are {len(strava.payload_rides)} rides in the list.')

        success, message = database_manager.write_update_rides_bulk(strava.payload_rides)

        if success:
            logging.info(f"Bulk update of database OK: {message}.")
        else:
            logging.error(f"Bulk update of database failed: {message}.")

        if mode == "all":
            logging.info("Refreshing all bikes from Strava")
            await strava.get_bikes(database_manager.read_unique_bikes())
            success, message = database_manager.write_update_bikes(strava.payload_bikes)

            if success:
                logging.info(f"Bike update OK: {message}.")
            else:
                logging.error(f"Bike update failed failed: {message}.")

            success, message = self.update_components_distance_iterator(database_manager.read_unique_bikes())

        if mode == "recent":
            if len(strava.bike_ids_recent_rides) > 0:
                logging.info("Refreshing bikes used in recent rides from Strava")
                await strava.get_bikes(strava.bike_ids_recent_rides)
                success, message = database_manager.write_update_bikes(strava.payload_bikes)
                
                if success:
                    logging.info(f"Bike update OK: {message}.")
                else:
                    logging.error(f"Bike update failed failed: {message}.")
                
                success, message = self.update_components_distance_iterator(strava.bike_ids_recent_rides)

            else:
                logging.warning("No bikes found in recent activities.")

        self.app_state.strava_last_pull = datetime.now()
        self.set_time_strava_last_pull()

        if success:
            logging.info(f"Update of rides, bikes and components successful: {message}.")
        else:
            logging.error(f"Update of rides, bikes and components failed: {message}.")

        return success, message

    def update_components_distance_iterator(self, bike_ids):
        """Method to determine which selection of components to update"""
        try:
            logging.info(f'Iterating over bikes to find components to update. Received {len(bike_ids)} bikes.')
            for bike_id in bike_ids:
                for component in database_manager.read_subset_installed_components(bike_id):
                    
                    latest_history_record = database_manager.read_latest_history_record(component.component_id)
                    current_component_distance = latest_history_record.distance_marker
                    matching_rides = database_manager.read_matching_rides(component.bike_id, latest_history_record.updated_date)
                    current_component_distance += sum(ride.ride_distance for ride in matching_rides)
                    self.update_component_distance(component.component_id, current_component_distance)

            return True, f"Processed components for {len(bike_ids)} bikes."

        except Exception as error:
            return False, {str(error)}
    
    def update_component_distance(self, component_id, current_distance):
        """Method to update component table with distance from ride table"""        
        component = database_manager.read_component(component_id)
        distance_offset = component.component_distance_offset
        total_distance = current_distance + distance_offset

        success, message = database_manager.write_component_distance(component, total_distance)

        logging.info(f"Updated distance for component {component.component_name}. New total distance: {total_distance}.")

        updated_component = database_manager.read_component(component_id)

        if updated_component.bike_id is None:
            bike_id = database_manager.read_bike_id_recent_component_history(component_id)
        else:
            bike_id = updated_component.bike_id
        
        self.update_component_lifetime_status(updated_component)
        self.update_component_service_status(updated_component)
        self.update_bike_status(bike_id)

        if success:
            logging.info(f"Component distance update successful: {message}.")
        else:
            logging.error(f"Component distance update failed: {message}.")

        return success, message

    def update_component_lifetime_status(self, component):
        """Method to update component table with lifetime status"""
        if component.lifetime_expected:
            logging.info(f"Updating lifetime status for component {component.component_name}.")

            lifetime_remaining = component.lifetime_expected - component.component_distance
            lifetime_status = self.compute_component_status("lifetime",
                                                            calculate_percentage_reached(component.lifetime_expected,
                                                                                        int(lifetime_remaining)))
            
            success, message = database_manager.write_component_lifetime_status(component,
                                                                lifetime_remaining, lifetime_status)

        else:
            logging.info(f"Component {component.component_name} has no expected lifetime, setting NULL values for lifetime.")

            lifetime_remaining = None
            lifetime_status = None

            success, message = database_manager.write_component_lifetime_status(component, lifetime_remaining, lifetime_status)
 
        if success:
            logging.info(f"Component lifetime status update successful: {message}.")
        else:
            logging.error(f"Component lifetime status update failed: {message}.")
    
        return success, message
    
    def update_component_service_status(self, component):
        """Method to update component table with service status"""
        if component.service_interval:
            logging.info(f"Updating service status for component {component.component_name}.")
            latest_service_record = database_manager.read_latest_service_record(component.component_id)
            latest_history_record = database_manager.read_latest_history_record(component.component_id)

            if component.installation_status == "Installed":
                if latest_service_record is None:
                    logging.info(f'No service record found for component {component.component_name}. Using distance from installation log and querying distance from installation date to today.')
                    distance_since_service = latest_history_record.distance_marker
                    matching_rides = database_manager.read_matching_rides(component.bike_id, latest_history_record.updated_date)
                    distance_since_service += sum(ride.ride_distance for ride in matching_rides)
                    
                elif latest_service_record:
                    logging.info(f'Service record found for for component {component.component_name}. Querying distance from previous service date to today.')
                    matching_rides = database_manager.read_matching_rides(component.bike_id, latest_service_record.service_date)
                    distance_since_service = sum(ride.ride_distance for ride in matching_rides)

            elif component.installation_status != "Installed":
                if latest_service_record is None:
                    logging.info(f'Component {component.component_name} has been uninstalled and there are no previous services. Setting distance since service to distance at the time of uninstallation.')
                    distance_since_service = latest_history_record.distance_marker
                
                elif latest_service_record:
                    if latest_service_record.service_date > component.updated_date:
                        logging.info(f'Component {component.component_name} has been serviced after uninstall. Setting distance since service to 0.')
                        distance_since_service = 0
                
                    elif latest_service_record.service_date < component.updated_date:
                        logging.info(f'Component {component.component_name} has no services after uninstall, but a previous service exist. Using already calculated distance to next service.')
                        distance_since_service = component.service_interval + component.service_next*-1
        
            service_next = component.service_interval - distance_since_service
            service_status = self.compute_component_status("service",
                                                            calculate_percentage_reached(component.service_interval,
                                                                                        int(service_next)))
            
            success, message = database_manager.write_component_service_status(component, service_next, service_status)

        else:
            logging.info(f"Component {component.component_name} has no service interval, setting NULL values for service.")
            
            service_next = None
            service_status = None
            
            success, message = database_manager.write_component_service_status(component, service_next, service_status)

        if success:
            logging.info(f"Component service status update successful: {message}.")
        else:
            logging.error(f"Component service status update failed: {message}.")
    
        return success, message

    def update_bike_status(self, bike_id):
        """Method to update status for a given bike based on component service and lifetime status"""
        bike = database_manager.read_single_bike(bike_id)
        components = database_manager.read_subset_components(bike_id)            
        
        logging.info(f"Updating bike status for bike {bike.bike_name} with id {bike.bike_id}.")
        
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
    
        logging.info(f"New status for bike {bike.bike_name}: {service_status}.")

        success, message = database_manager.write_bike_service_status(bike, service_status)

        if success:
            logging.info(f"Bike update successful: {message}.")
        else:
            logging.error(f"Bike update failed: {message}.")
    
        return success, message

    def create_service_record(self,
                    component_id,
                    service_date,
                    service_description):
        """Method to add service record"""
        component_data = database_manager.read_component(component_id)
        service_id = generate_unique_id()

        service_data = {"service_id": service_id,
                        "component_id": component_id,
                        "service_date": service_date,
                        "description": service_description,
                        "component_name": component_data.component_name,
                        "bike_id": component_data.bike_id}
        
        latest_service_record = database_manager.read_latest_service_record(component_id)
        latest_history_record = database_manager.read_latest_history_record(component_id)

        if latest_history_record and service_date < latest_history_record.updated_date:
            message = f"Service date {service_date} is before the latest history record for component {component_data.component_name}. Services must be entered chronologically."
            logging.warning(message)
            return False, message

        elif latest_service_record and service_date < latest_service_record.service_date:
            message = f"Service date {service_date} is before the latest service record for component {component_id}. Services must be entered chronologically."
            logging.warning(message)
            return False, message

        if component_data.installation_status == "Installed":
            if latest_service_record is None:
                logging.info(f'No service record found for component {component_data.component_name}. Using distance from installation log and querying distance from installation date to service date.')
                distance_since_service = latest_history_record.distance_marker
                distance_since_service += database_manager.read_sum_distanse_subset_rides(component_data.bike_id, latest_history_record.updated_date, service_date)

            elif latest_service_record:
                logging.info(f'Service record found for component {component_data.component_name}. Querying distance from previous service date to current service date.')
                distance_since_service = database_manager.read_sum_distanse_subset_rides(component_data.bike_id, latest_service_record.service_date, service_date)

        elif component_data.installation_status != "Installed":
            if latest_service_record is None:
                logging.info(f'Component {component_data.component_name} has been uninstalled and there are no previous services. Setting historic distance since service to distance at the time of uninstallation.')
                distance_since_service = latest_history_record.distance_marker

            elif latest_service_record:
                if latest_service_record.service_date > component_data.updated_date:
                    logging.info(f'Component {component_data.component_name} has been serviced after uninstall. Setting distance since service to 0.')
                    distance_since_service = 0

        service_data.update({"distance_marker": distance_since_service})

        success, message = database_manager.write_service_record(service_data)
        self.update_component_service_status(component_data)
        self.update_bike_status(component_data.bike_id)

        if success:
            logging.info(f"Creation of service record successful: {message}.")
        else:
            logging.error(f"Creation of service record failed: {message}.")

        return success, message

    def modify_component_details(self,
                                 component_id,
                                 component_installation_status,
                                 component_updated_date,
                                 component_name,
                                 component_type,
                                 component_bike_id,
                                 expected_lifetime,
                                 service_interval,
                                 cost,
                                 offset,
                                 component_notes):
        "Method to update component details"
        component_bike_id = None if len(component_bike_id) == 0 else component_bike_id
        expected_lifetime = int(expected_lifetime) if expected_lifetime and expected_lifetime.isdigit() else None
        service_interval = int(service_interval) if service_interval and service_interval.isdigit() else None
        cost = int(cost) if cost and cost.isdigit() else None

        new_component_data = {"installation_status": component_installation_status,
                              "updated_date": component_updated_date,
                              "component_name": component_name,
                              "component_type": component_type,
                              "bike_id": component_bike_id,
                              "lifetime_expected": expected_lifetime,
                              "service_interval": service_interval,
                              "cost": cost,
                              "component_distance_offset": offset,
                              "notes": component_notes}

        if component_id is None:
            component_id = generate_unique_id()
            success, message = database_manager.write_component_details(component_id, new_component_data)

            if success:
                logging.info(message)
            else:
                logging.error(message)
        
        current_history_id = f'{component_updated_date} {component_id}'
        old_component_data = database_manager.read_component(component_id)
        component_id = old_component_data.component_id
        updated_bike_id = component_bike_id
        previous_bike_id = old_component_data.bike_id if old_component_data else None
        old_component_name = old_component_data.component_name if old_component_data else None
        latest_service_record = database_manager.read_latest_service_record(component_id)
        latest_history_record = database_manager.read_latest_history_record(component_id)

        if latest_history_record is not None and latest_history_record.history_id == current_history_id:
            if latest_history_record.update_reason == component_installation_status:
                logging.info(f"Only updating select component record details and service and lifetime status. Historic record already exist for component {old_component_data.component_name}.")
                success, message = database_manager.write_component_details(component_id, new_component_data)
                updated_component_data = database_manager.read_component(component_id)
                self.update_component_distance(component_id, old_component_data.component_distance - old_component_data.component_distance_offset)
            else:
                logging.warning(f"Cannot change installation status when record date is the same as previous record. Component: {old_component_data.component_name}.")

        else:
            if latest_history_record and component_updated_date < latest_history_record.updated_date:
                message = f"Component update date {component_updated_date} is before the latest history record for component {old_component_data.component_name}. Component update dates must be entered chronologically."
                logging.warning(message)
                return False, message, component_id

            elif latest_service_record and component_updated_date < latest_service_record.service_date:
                message = f"Component update date {component_updated_date} is before the latest service record for component {old_component_data.component_name}. Component update dates must be entered chronologically."
                logging.warning(message)
                return False, message, component_id

            if latest_history_record is None:
                historic_distance = 0

            else:
                if component_installation_status != "Installed":
                    logging.info(f'Timespan for historic distance query: start date {latest_history_record.updated_date} stop date {component_updated_date}.')
                    historic_distance = database_manager.read_sum_distanse_subset_rides(old_component_data.bike_id, latest_history_record.updated_date, component_updated_date)
                    historic_distance += latest_history_record.distance_marker

                else:
                    historic_distance = latest_history_record.distance_marker

            history_record_creation = self.create_history_record(old_component_name, latest_history_record, current_history_id, component_id, previous_bike_id, updated_bike_id, component_installation_status, component_updated_date, historic_distance)

            if history_record_creation is False:
                if success:
                   return success, f"{message}. No history record added.", component_id
                else:
                    return success, message, component_id

            elif history_record_creation is True:
                success, message = database_manager.write_component_details(component_id, new_component_data)
                updated_component_data = database_manager.read_component(component_id)
                latest_history_record = database_manager.read_latest_history_record(component_id)

                if updated_component_data.installation_status == "Installed":
                    logging.info(f'Timespan for current distance query: start date {updated_component_data.updated_date} stop date {datetime.now().strftime("%Y-%m-%d %H:%M")}.')
                    current_distance = database_manager.read_sum_distanse_subset_rides(updated_component_data.bike_id, updated_component_data.updated_date, datetime.now().strftime("%Y-%m-%d %H:%M"))
                    current_distance += latest_history_record.distance_marker
                    self.update_component_distance(component_id, current_distance)

                else:
                    current_distance = latest_history_record.distance_marker
                    self.update_component_distance(component_id, current_distance)

            else:
                logging.warning(f"Modification of component {old_component_data.component_name} skipped due to exceptions when creating history record.")

        return success, message, component_id

    def create_history_record(self,
                              old_component_name,
                              latest_history_record,
                              current_history_id,
                              component_id,
                              previous_bike_id,
                              updated_bike_id,
                              updated_component_installation_status,
                              component_updated_date,
                              historic_distance):
        """Method to create installation history record"""
        if latest_history_record is None and updated_component_installation_status != "Installed":
            logging.warning(f"Cannot change a component that is not installed: {old_component_name}.")
            return False

        elif latest_history_record is None:
            if updated_bike_id is None:
                logging.warning(f"Cannot set status to installed without specifying bike: {old_component_name}.")
                return False
            else:
                bike_id = updated_bike_id

        else:
            if latest_history_record.history_id == current_history_id:
                logging.warning(f"History record dated {component_updated_date} already exists: {old_component_name}.")
                return False

            elif latest_history_record.update_reason == updated_component_installation_status:
                logging.warning(f"Component status for {old_component_name} is already set to: {latest_history_record.update_reason}.")
                return False

            else:
                if updated_component_installation_status == "Installed":
                    if updated_bike_id is None:
                        logging.warning(f"Cannot set status to installed without specifying bike, component id {old_component_name}.")
                        return False
                    else:
                        bike_id = updated_bike_id

                elif updated_component_installation_status == "Retired":
                    bike_id = updated_bike_id

                elif updated_component_installation_status == "Not installed":
                    bike_id = previous_bike_id

        success, message = (database_manager
                            .write_history_record
                                (current_history_id,
                                 component_id,
                                 bike_id,
                                 old_component_name,
                                 component_updated_date,
                                 updated_component_installation_status,
                                 historic_distance))

        if success:
            logging.info(f"Creation of history record successful: {message}.")
            return True
        else:
            logging.error(f"Creation of history record failed: {message}.")
            return False

    def compute_component_status(self, mode, reached_distance_percent):
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
    
    def modify_component_type(self,
                              component_type,
                              expected_lifetime,
                              service_interval):
        """Method to create or update component types"""
        expected_lifetime = int(expected_lifetime) if expected_lifetime and expected_lifetime.isdigit() else None
        service_interval = int(service_interval) if service_interval and service_interval.isdigit() else None

        component_type_data = {"component_type": component_type,
                            "service_interval": service_interval,
                            "expected_lifetime": expected_lifetime}

        success, message = database_manager.write_component_type(component_type_data)

        if success:
            logging.info(f"Component type update successful: {message}.")
        else:
            logging.error(f"Component type update failed: {message}.")

        return success, message

    def delete_record(self, table_selector, record_id):
        """Method to delete a given record and associated records"""
        logging.info(f"Attempting to delete record with id {record_id} from table {table_selector}")

        success, message = database_manager.write_delete_record(table_selector, record_id)

        if success:
            logging.info(f"Deletion successful: {message}.")
        else:
            logging.error(f"Deletion failed: {message}.")

        return success, message

    def set_time_strava_last_pull(self):
        """Function to set the date for last pull from Strava"""
        if self.app_state.strava_last_pull:
            days_since = (datetime.now() - self.app_state.strava_last_pull).days
            self.app_state.strava_last_pull = self.app_state.strava_last_pull.strftime("%Y-%m-%d %H:%M")
            self.app_state.strava_days_since_last_pull = days_since
        
        elif self.app_state.strava_last_pull is None and database_manager.read_latest_ride_record():
            self.app_state.strava_last_pull = datetime.strptime(database_manager.read_latest_ride_record().record_time, "%Y-%m-%d %H:%M")
            self.app_state.strava_days_since_last_pull = (datetime.now() - self.app_state.strava_last_pull).days

        else:
            self.app_state.strava_last_pull = "never"
            self.app_state.strava_days_since_last_pull = None
