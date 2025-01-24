#!/usr/bin/env python3
"""Module to handle business logic"""

import logging
import asyncio
from datetime import datetime
from utils import (read_config,
                   calculate_percentage_reached,
                   generate_unique_id,
                   format_component_status,
                   format_cost,
                   get_component_statistics)
from strava import Strava
from database_manager import DatabaseManager
from icecream import ic #remove before prod
import traceback #remove before prod

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

    def get_bike_overview(self):
        """Method to get bike overview"""
        bikes = database_manager.read_bikes()
        bikes_data = [(bike.bike_name,
                    bike.bike_id,
                    bike.bike_retired,
                    bike.service_status,
                    int(bike.total_distance),
                    sum(1 for component in database_manager.read_subset_components(bike.bike_id)
                        if component.installation_status == "Installed"),
                    sum(1 for component in database_manager.read_subset_components(bike.bike_id)
                        if component.installation_status == "Retired")) for bike in bikes]

        payload = {"bikes_data": bikes_data}

        return payload
    
    def get_bike_details(self, bike_id):
        """Method to get bike details"""
        bike = database_manager.read_single_bike(bike_id)
        bike_data = {"bike_name": bike.bike_name,
                    "bike_id": bike.bike_id,
                    "bike_retired": bike.bike_retired,
                    "bike_service_status": bike.service_status,
                    "bike_total_distance": int(bike.total_distance),
                    "bike_notes": bike.notes,
                    "oldest_ride": database_manager.read_date_oldest_ride(bike_id)}

        bike_components = database_manager.read_subset_components(bike_id)
        bike_components_data = [(component.component_id,
                                 component.installation_status,
                                 component.component_type,
                                 component.component_name,
                                 int(component.component_distance),
                                 format_component_status(component.lifetime_status),
                                 format_component_status(component.service_status),
                                 format_cost(component.cost)
                                 ) for component in bike_components]

        component_statistics = get_component_statistics([tuple(component[1:])
                                                         for component in bike_components_data])

        recent_rides = database_manager.read_recent_rides(bike_id)
        recent_rides_data = [(ride.ride_id,
                              ride.record_time,
                              ride.ride_name,
                              int(ride.ride_distance),
                              ride.commute
                              ) for ride in recent_rides]

        payload = {"recent_rides": recent_rides_data,
                   "bike_data": bike_data,
                   "bike_components_data": bike_components_data,
                   "count_installed" : component_statistics["count_installed"],
                   "count_lifetime_status_green" : component_statistics["count_lifetime_status_green"],
                   "count_lifetime_status_yellow" : component_statistics["count_lifetime_status_yellow"],
                   "count_lifetime_status_red" : component_statistics["count_lifetime_status_red"],
                   "count_lifetime_status_purple" : component_statistics["count_lifetime_status_purple"],
                   "count_lifetime_status_grey" : component_statistics["count_lifetime_status_grey"],
                   "count_service_status_green" : component_statistics["count_service_status_green"],
                   "count_service_status_yellow" : component_statistics["count_service_status_yellow"],
                   "count_service_status_red" : component_statistics["count_service_status_red"],
                   "count_service_status_purple" : component_statistics["count_service_status_purple"],
                   "count_service_status_grey" : component_statistics["count_service_status_grey"],
                   "sum_cost" : component_statistics["sum_cost"]}
        
        return payload
    
    def get_component_overview(self):
        """Method to get component overview"""
        components = database_manager.read_all_components()
        component_data = [(component.component_id,
                           component.component_type,
                           component.component_name,
                           int(component.component_distance),
                           component.installation_status,
                           format_component_status(component.lifetime_status),
                           format_component_status(component.service_status),
                           database_manager.read_bike_name(component.bike_id),
                           format_cost(component.cost)
                           ) for component in components]

        rearranged_component_data = [(comp[4],
                                        None,
                                        None,
                                        None,
                                        comp[5],
                                        comp[6],
                                        comp[8],
                                        None,
                                        comp[7]) for comp in component_data]

        component_statistics = get_component_statistics(rearranged_component_data)

        bikes = database_manager.read_bikes()
        bikes_data = [(bike.bike_name,
                       bike.bike_id)
                       for bike in bikes if bike.bike_retired == "False"]

        component_types_data = database_manager.read_all_component_types()

        payload = {"component_data": component_data,
                   "bikes_data": bikes_data,
                   "component_types_data": component_types_data,
                   "count_installed" : component_statistics["count_installed"],
                   "count_not_installed" : component_statistics["count_not_installed"],
                   "count_retired" : component_statistics["count_retired"],
                   "count_lifetime_status_green" : component_statistics["count_lifetime_status_green"],
                   "count_lifetime_status_yellow" : component_statistics["count_lifetime_status_yellow"],
                   "count_lifetime_status_red" : component_statistics["count_lifetime_status_red"],
                   "count_lifetime_status_purple" : component_statistics["count_lifetime_status_purple"],
                   "count_lifetime_status_grey" : component_statistics["count_lifetime_status_grey"],
                   "count_service_status_green" : component_statistics["count_service_status_green"],
                   "count_service_status_yellow" : component_statistics["count_service_status_yellow"],
                   "count_service_status_red" : component_statistics["count_service_status_red"],
                   "count_service_status_purple" : component_statistics["count_service_status_purple"],
                   "count_service_status_grey" : component_statistics["count_service_status_grey"],
                   "sum_cost" : component_statistics["sum_cost"]}
        
        return payload
    
    def get_component_details(self, component_id):
        """Method to get component details"""
        bikes = database_manager.read_bikes()
        bikes_data = [(bike.bike_name,
                       bike.bike_id)
                       for bike in bikes if bike.bike_retired == "False"]
        
        component_types_data = database_manager.read_all_component_types()
        
        bike_component = database_manager.read_component(component_id)
        bike_component_data = {"bike_id": bike_component.bike_id,
                               "component_id": bike_component.component_id,
                               "updated_date": bike_component.updated_date,
                               "component_name": bike_component.component_name,
                               "component_type": bike_component.component_type,
                               "component_distance": (int(bike_component.component_distance) 
                                                      if bike_component.component_distance is not None else None),
                                "installation_status": bike_component.installation_status,
                                "lifetime_expected": bike_component.lifetime_expected,
                                "lifetime_remaining": (int(bike_component.lifetime_remaining)
                                                       if bike_component.lifetime_remaining is not None else None),
                                "lifetime_status": format_component_status(bike_component.lifetime_status),
                                "lifetime_percentage": (calculate_percentage_reached(bike_component.lifetime_expected,
                                                                                     int(bike_component.lifetime_remaining))
                                                                                     if bike_component.lifetime_remaining is not None else None),
                                "service_interval": bike_component.service_interval,
                                "service_next": (int(bike_component.service_next)
                                                 if bike_component.service_next is not None else None),
                                "service_status": format_component_status(bike_component.service_status),
                                "service_percentage": calculate_percentage_reached(bike_component.service_interval,
                                                                                   int(bike_component.service_next))
                                                                                   if bike_component.service_next is not None else None,
                                "offset": bike_component.component_distance_offset,
                                "component_notes": bike_component.notes,
                                "cost": format_cost(bike_component.cost)}

        component_history = database_manager.read_subset_component_history(bike_component.component_id)
        if component_history is not None:
            component_history_data = [(installation_record.history_id,
                                       installation_record.updated_date,
                                       installation_record.update_reason,
                                       database_manager.read_bike_name(installation_record.bike_id),
                                       int(installation_record.distance_marker)) for installation_record in component_history]
        else:
            component_history_data = None

        service_history = database_manager.read_subset_service_history(bike_component.component_id)
        if service_history is not None:
            service_history_data = [(service_record.service_id,
                                     service_record.service_date,
                                     service_record.description,
                                     database_manager.read_bike_name(service_record.bike_id),
                                     int(service_record.distance_marker)) for service_record in service_history]
        else:
            service_history_data = None

        payload = {"bikes_data": bikes_data,
                   "component_types_data": component_types_data,
                   "bike_component_data": bike_component_data,
                   "bike_name": database_manager.read_bike_name(bike_component.bike_id),
                   "component_history_data": component_history_data,
                   "service_history_data": service_history_data}
        
        return payload

    def get_component_types(self):
        """Method to get all component types"""
        payload = {"component_types": database_manager.read_all_component_types()}
        
        return payload
    
    async def pull_strava_background(self, mode):
        """Function to pull data from Strava in the background"""
        while True:
            try:
                logging.info(f"Retrieving rides from Strava as background task. Mode set to: {mode}")

                success, message = await self.update_rides_bulk(mode)

                if success:
                    logging.info(f"Background update successful: {message}")
                else:
                    logging.error(f"Background update failed: {message}")

            except Exception as error:
                logging.error(f"An error occurred during background update: {error}")

            logging.info("Next pull from Strava is in four hours")
            await asyncio.sleep(14400)

    async def update_rides_bulk(self, mode):
        """Method to create or update ride data in bulk to database"""
        logging.info(f"Retrieving rides from Strava. Mode set to: {mode}.")
        await strava.get_rides(mode)
        logging.info(f'There are {len(strava.payload_rides)} rides in the list.')

        success, message = database_manager.write_update_rides_bulk(strava.payload_rides)

        if success:
            logging.info(f"Bulk update of database OK: {message}")
        else:
            logging.error(f"Bulk update of database failed: {message}")

        if mode == "all":
            logging.info("Refreshing all bikes from Strava")
            await strava.get_bikes(database_manager.read_unique_bikes())
            success, message = database_manager.write_update_bikes(strava.payload_bikes)

            if success:
                logging.info(f"Bike update OK: {message}")
            else:
                logging.error(f"Bike update failed failed: {message}")

            success, message = self.update_components_distance_iterator(database_manager.read_unique_bikes())

        if mode == "recent":
            if len(strava.bike_ids_recent_rides) > 0:
                logging.info("Refreshing bikes used in recent rides from Strava")
                await strava.get_bikes(strava.bike_ids_recent_rides)
                success, message = database_manager.write_update_bikes(strava.payload_bikes)
                
                if success:
                    logging.info(f"Bike update OK: {message}")
                else:
                    logging.error(f"Bike update failed failed: {message}")
                
                success, message = self.update_components_distance_iterator(strava.bike_ids_recent_rides)

            else:
                logging.warning("No bikes found in recent activities.")

        self.app_state.strava_last_pull = datetime.now()
        self.set_time_strava_last_pull()

        if success:
            message = f"Update of rides, bikes and components successful: {message}"
            logging.info(message)
        else:
            message = f"Update of rides, bikes and components failed: {message}"
            logging.error(message)

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
            logging.info(f"Component distance update successful: {message}")
        else:
            logging.error(f"Component distance update failed: {message}")

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
            logging.info(f"Component lifetime status update successful: {message}")
        else:
            logging.error(f"Component lifetime status update failed: {message}")
    
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
                        ic(distance_since_service) #DEBUG, there is something wrong with this logic

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
            logging.info(f"Component service status update successful: {message}")
        else:
            logging.error(f"Component service status update failed: {message}")
    
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
            logging.info(f"Bike update successful: {message}")
        else:
            logging.error(f"Bike update failed: {message}")
    
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

    def create_service_record(self,
                    component_id,
                    service_date,
                    service_description):
        """Method to add service record"""
        try:
            service_id = generate_unique_id()

            success, message = self.validate_service_record("create service", component_id, service_id, service_date)
            if not success:
                logging.error(f"Validation of service record failed: {message}")
                return success, message

            service_data = {"service_id": service_id,
                            "component_id": component_id,
                            "component_name": "",
                            "service_date": service_date,
                            "description": service_description,
                            'bike_id': "",
                            'distance_marker': 0}
            
            success, message = database_manager.write_service_record(service_data)
            if not success:
                logging.error(f"Error creating service record: {message}")
                return success, message
            
            success, message = self.process_service_records(component_id, service_id, service_date, service_description)
            if not success:
                logging.error(f"Error processing service record: {message}")
                return success, message
            
            if success:
                logging.info(f"Creation of service record successful: {message}")
            else:
                logging.error(f"Creation of service record failed: {message}")
                return success, message

            return success, message

        except Exception as error:
            logging.error(f"An error occured creating services for component with id {component_id}: {str(error)}")
            return False, f"Error creating service records for {component_id}: {str(error)}"
    
    def update_service_record(self,
                              component_id,
                              service_id,
                              service_date,
                              service_description):
        """Method to update a service record"""
        try:
            success, message = self.validate_service_record("edit service", component_id, service_id, service_date)
            if not success:
                logging.error(f"Validation of service record failed: {message}")
                return success, message
            
            success, message = self.process_service_records(component_id, service_id, service_date, service_description)
            if not success:
                logging.error(f"Error processing service record: {message}")
                return success, message
            
            if success:
                logging.info(f"Update of service record successful: {message}")
            else:
                logging.error(f"Update of service record failed: {message}")
                return success, message

            return success, message

        except Exception as error:
            logging.error(f"An error occured updating services for component with id {component_id}: {str(error)}")
            return False, f"Error updating service records for {component_id}: {str(error)}"

    def validate_service_record(self, mode, component_id, service_id, service_date):
        """Method to validate service records before processing and storing in database"""

        current_service = database_manager.read_single_service_record(service_id)
        if mode == "edit service" and not current_service:
            logging.warning(f"Service record not found: {service_id}")
            return False, f"Service record not found: {service_id}"

        component = database_manager.read_component(component_id)
        if not component:
            logging.warning(f"Associated component not found: {component_id}")
            return False, f"Associated component not found: {component_id}"

        history_records = database_manager.read_subset_component_history(component.component_id)
        if not history_records:
            logging.warning(f"No installation records found for component: {component.component_id}")
            return False, f"No installation records found: {component_id}"

        oldest_history_record_date = database_manager.read_oldest_history_record(component.component_id).updated_date
        
        if service_date < oldest_history_record_date:
            logging.warning(f"Service date cannot be before before component creation date: {oldest_history_record_date}. Component: {component.component_id}")
            return False, f"Service date cannot be before before component creation date ({oldest_history_record_date} for {component.component_id})"

        if service_date > datetime.now().strftime("%Y-%m-%d %H:%M"):
            logging.warning(f"Service date cannot be in the future. Component: {component.component_id}")
            return False, f"Service date cannot be in the future. Component id: {component.component_id}"
        
        logging.info(f"Validation of service record for {component.component_name} passed")
        return True, f"Validation of service record for {component.component_name} passed"
    
    def process_service_records(self, component_id, service_id, service_date, service_description):
        """Method to calculate distance and bike id for service records"""

        component = database_manager.read_component(component_id)
        current_service_data = {'service_id': service_id,
                                'component_id': component_id,
                                'component_name': component.component_name,
                                'service_date': service_date,
                                'description': service_description} 
            
        all_services = list(database_manager.read_subset_service_history(component.component_id))
        history_records = database_manager.read_subset_component_history(component.component_id)

        logging.info(f"Consolodating and sorting all services for component {component.component_name}")
        all_services = [service for service in all_services if service.service_id != service_id]
        all_services.append(type('Service', (), current_service_data)())
        all_services.sort(key=lambda x: x.service_date)
        
        logging.info(f"Iterating over all services for component {component.component_name} to update distance markers and bike ids")
        for index, service in enumerate(all_services):
            for record in history_records:
                if record.updated_date <= service.service_date:
                    relevant_history_record = record
                    logging.info(f"Defining history record for service {service.service_id} dated {service.service_date} is history record {relevant_history_record.history_id} dated {relevant_history_record.updated_date}")
                    break
            
            if index == 0:
                logging.info(f"Processing first service record {service.service_id} dated {service.service_date}")
                if relevant_history_record.update_reason == "Installed":
                    new_service_distance = relevant_history_record.distance_marker
                    new_service_distance += database_manager.read_sum_distanse_subset_rides(
                        relevant_history_record.bike_id,
                        relevant_history_record.updated_date,
                        service.service_date)
                    logging.info(f"First service record distance mark is at {new_service_distance} km, based on installations status {relevant_history_record.update_reason}")
                else:
                    new_service_distance = relevant_history_record.distance_marker
                    logging.info(f"First service record distance mark is at {new_service_distance} km, based on installations status {relevant_history_record.update_reason}")
            else:
                logging.info(f"Processing subsequent service record {service.service_id} dated {service.service_date}")
                if relevant_history_record.update_reason == "Installed":
                    new_service_distance = database_manager.read_sum_distanse_subset_rides(
                        relevant_history_record.bike_id,
                        all_services[index-1].service_date,
                        service.service_date)
                    logging.info(f"Subsequent service record distance mark is at {new_service_distance} km, based on installations status {relevant_history_record.update_reason}")
                else:
                    new_service_distance = database_manager.read_sum_distanse_subset_rides(
                        relevant_history_record.bike_id,
                        all_services[index-1].service_date,
                        relevant_history_record.updated_date)
                    logging.info(f"Subsequent service record distance mark is at {new_service_distance} km, based on installations status {relevant_history_record.update_reason}")

            if relevant_history_record.update_reason == "Installed":
                new_bike_id = relevant_history_record.bike_id
                logging.info(f"Service record {service.service_id} is now associated with bike {database_manager.read_single_bike(new_bike_id)}")
            else:
                new_bike_id = None
                logging.info(f"Service record {service.service_id} is not associated with any bike")
            
            service_data = {
                'service_id': service.service_id,
                'component_id': component.component_id,
                'component_name': component.component_name,
                'service_date': service.service_date,
                'description': service.description,
                'bike_id': new_bike_id,
                'distance_marker': new_service_distance}
            
            success, message = database_manager.write_service_record(service_data)
            if not success:
                logging.error(f"Error updating service records for {component.component_name}: {message}")
                return success, f"Error updating service records: {message}"

        logging.info(f"Service records for component {component.component_name} successfully updated")
        self.update_component_service_status(component)
        if component.installation_status == "Installed":
            self.update_bike_status(component.bike_id)
            
        return True, "All service records successfully processed"
    
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
            logging.info(f"Creation of history record successful: {message}")
            return success
        else:
            logging.error(f"Creation of history record failed: {message}")
            return success

    def update_history_record(self, history_id, updated_date, update_reason): ##This must be rewritten
        """Method to update a component history record with validation"""
        
    
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
            logging.info(f"Component type update successful: {message}")
        else:
            logging.error(f"Component type update failed: {message}")

        return success, message

    def delete_record(self, table_selector, record_id):
        """Method to delete a given record and associated records"""
        logging.info(f"Attempting to delete record with id {record_id} from table {table_selector}")

        component_id = None
        if table_selector == "Services":
            component_id = database_manager.read_single_service_record(record_id).component_id
        
        elif table_selector == "ComponentHistory":
            component_id = database_manager.read_single_history_record(record_id).component_id

        success, message = database_manager.write_delete_record(table_selector, record_id)

        if success:
            logging.info(f"Deletion successful: {message}")
            if table_selector == "Services":
                logging.info(f"Recalculating service records for component {component_id}")
                # Method is missing - need to update service records, call also update component service status and update bike status

            elif table_selector == "ComponentHistory":
                logging.info(f"Recalculating installation history records for component {component_id}")
                # Method is missing - need to update history records, call also update component service status and update bike status
        else:
            logging.error(f"Deletion failed: {message}")

        return success, message, component_id

    async def refresh_all_bikes(self):
        """Method to refresh all bikes from Strava"""
        unique_bike_ids = database_manager.read_unique_bikes()
        
        await strava.get_bikes(unique_bike_ids)
        success_main, message_main = database_manager.write_update_bikes(strava.payload_bikes)

        if success_main:
            for bike_id in unique_bike_ids:
                success_sub, message_sub = self.update_bike_status(bike_id)
                if not success_sub:
                    logging.error(message_sub)
                    return success_sub, message_sub
        
        logging.info(message_main)
        return success_main, message_main

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
