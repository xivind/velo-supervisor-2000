#!/usr/bin/env python3
"""Module to handle business logic"""

import logging
import asyncio
from datetime import datetime
import json
from utils import (read_config,
                   calculate_percentage_reached,
                   generate_unique_id,
                   format_component_status,
                   format_cost,
                   get_component_statistics,
                   get_formatted_datetime_now,
                   validate_date_format,
                   calculate_elapsed_days,
                   get_formatted_bikes_list)
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

    def get_bike_overview(self):
        """Method to produce payload for page bike overview"""
        bikes = database_manager.read_bikes()
        bikes_data = []

        for bike in bikes:
            bike_name = bike.bike_name
            bike_id = bike.bike_id
            bike_retired = bike.bike_retired
            service_status = bike.service_status
            total_distance = round(bike.total_distance)

            components = database_manager.read_subset_components(bike_id)
            count_installed = sum(1 for component in components 
                                if component.installation_status == "Installed")

            critical_count = sum(1 for component in components 
                            if component.installation_status == "Installed" and
                            (component.lifetime_status == "Lifetime exceeded" or
                            component.service_status == "Service interval exceeded"))

            warning_count = sum(1 for component in components
                            if component.installation_status == "Installed" and
                            (component.lifetime_status == "Due for replacement" or
                            component.service_status == "Due for service"))

            compliance_report = self.process_bike_compliance_report(bike_id)

            bikes_data.append((bike_name,
                               bike_id,
                               bike_retired,
                               service_status,
                               total_distance,
                               count_installed,
                               critical_count,
                               warning_count,
                               compliance_report))

        payload = {"bikes_data": bikes_data}

        return payload

    def get_bike_details(self, bike_id):
        """Method to produce payload for page bike details"""
        bikes = database_manager.read_bikes()
        bikes_data = get_formatted_bikes_list(bikes)

        bike = database_manager.read_single_bike(bike_id)
        bike_data = {"bike_name": bike.bike_name,
                    "bike_id": bike.bike_id,
                    "bike_retired": bike.bike_retired,
                    "bike_service_status": bike.service_status,
                    "bike_total_distance": round(bike.total_distance),
                    "bike_notes": bike.notes,
                    "oldest_ride": database_manager.read_date_oldest_ride(bike_id)}

        component_types_data = database_manager.read_all_component_types()

        bike_components = database_manager.read_subset_components(bike_id)
        bike_components_data = [(component.component_id,
                                 "-" if component.lifetime_remaining is None else round(component.lifetime_remaining),
                                 "-" if component.service_next is None else round(component.service_next),
                                 component.installation_status,
                                 component.component_type,
                                 component.component_name,
                                 round(component.component_distance),
                                 format_component_status(component.lifetime_status),
                                 format_component_status(component.service_status),
                                 format_cost(component.cost)
                                 ) for component in bike_components]

        component_statistics = get_component_statistics([tuple(component[3:])
                                                         for component in bike_components_data])

        recent_rides = database_manager.read_recent_rides(bike_id)
        recent_rides_data = [(ride.ride_id,
                              ride.record_time,
                              ride.ride_name,
                              round(ride.ride_distance),
                              ride.commute
                              ) for ride in recent_rides]

        compliance_report = self.process_bike_compliance_report(bike_id)

        payload = {"recent_rides": recent_rides_data,
                   "bikes_data": bikes_data,
                   "bike_data": bike_data,
                   "component_types_data": component_types_data,
                   "bike_components_data": bike_components_data,
                   "count_installed" : component_statistics["count_installed"],
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
                   "sum_cost" : component_statistics["sum_cost"],
                   "compliance_report": compliance_report}

        return payload

    def get_component_overview(self):
        """Method to produce payload for page component overview"""
        components = database_manager.read_all_components()
        component_data = [(component.component_id,
                           component.component_type,
                           component.component_name,
                           round(component.component_distance),
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
        bikes_data = get_formatted_bikes_list(bikes)

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
        """Method to produce payload for page component details"""
        bikes = database_manager.read_bikes()
        bikes_data = get_formatted_bikes_list(bikes)

        component_types_data = database_manager.read_all_component_types()

        bike_component = database_manager.read_component(component_id)
        bike_component_data = {"bike_id": bike_component.bike_id,
                               "component_id": bike_component.component_id,
                               "updated_date": bike_component.updated_date,
                               "component_name": bike_component.component_name,
                               "component_type": bike_component.component_type,
                               "component_distance": (round(bike_component.component_distance) 
                                                      if bike_component.component_distance is not None else None),
                                "installation_status": bike_component.installation_status,
                                "lifetime_expected": bike_component.lifetime_expected,
                                "lifetime_remaining": (round(bike_component.lifetime_remaining)
                                                       if bike_component.lifetime_remaining is not None else None),
                                "lifetime_status": format_component_status(bike_component.lifetime_status),
                                "lifetime_percentage": (calculate_percentage_reached(bike_component.lifetime_expected,
                                                                                     round(bike_component.lifetime_remaining))
                                                                                     if bike_component.lifetime_remaining is not None else None),
                                "service_interval": bike_component.service_interval,
                                "service_next": (int(bike_component.service_next)
                                                 if bike_component.service_next is not None else None),
                                "service_status": format_component_status(bike_component.service_status),
                                "service_percentage": calculate_percentage_reached(bike_component.service_interval,
                                                                                   round(bike_component.service_next))
                                                                                   if bike_component.service_next is not None else None,
                                "offset": bike_component.component_distance_offset,
                                "component_notes": bike_component.notes,
                                "cost": format_cost(bike_component.cost)}

        component_history = database_manager.read_subset_component_history(bike_component.component_id)
        if component_history is not None:
            component_history_data = []

            for installation_record in component_history:
                bike_total_distance = 0
                if installation_record.bike_id:
                    bike_total_distance = database_manager.read_sum_distance_subset_rides(installation_record.bike_id,
                                                                                          "2000-01-01 00:00",
                                                                                          installation_record.updated_date)

                component_history_data.append((installation_record.history_id,
                                               installation_record.updated_date,
                                               installation_record.update_reason,
                                               installation_record.bike_id,
                                               database_manager.read_bike_name(installation_record.bike_id),
                                               round(bike_total_distance),
                                               round(installation_record.distance_marker)))
        else:
            component_history_data = None

        service_history = database_manager.read_subset_service_history(component_id)
        if service_history is not None:
            total_component_distance = 0
            enhanced_service_data = []
            
            for service_record in reversed(service_history):
                total_component_distance += service_record.distance_marker
            
            running_total = total_component_distance
            
            for service_record in service_history:
                bike_total_distance = 0
                if service_record.bike_id:
                    bike_total_distance = database_manager.read_sum_distance_subset_rides(service_record.bike_id,
                                                                                          "2000-01-01 00:00", 
                                                                                          service_record.service_date)

                enhanced_service_data.append((service_record.service_id,
                                              service_record.service_date,
                                              service_record.description,
                                              database_manager.read_bike_name(service_record.bike_id),
                                              round(bike_total_distance),
                                              round(service_record.distance_marker),
                                              round(running_total)))
                
                running_total -= service_record.distance_marker
            
            service_history_data = enhanced_service_data
        
        else:
            service_history_data = None

        oldest_history_record = database_manager.read_oldest_history_record(component_id)
        if oldest_history_record:
            success, message = calculate_elapsed_days(oldest_history_record.updated_date, get_formatted_datetime_now())
            if success:
                days_since_install = f"{message} days since first installation"
            else:
                days_since_install = message
        else:
            days_since_install = "Component has never been installed"
        
        latest_service_record = database_manager.read_latest_service_record(component_id)
        if latest_service_record:
            success, message = calculate_elapsed_days(latest_service_record.service_date, get_formatted_datetime_now())
            if success:
                days_since_service = f"{message} days since last service"
            else:
                days_since_service = message
        else:
            days_since_service = "Component has never been serviced"

        elapsed_days = {"days_since_install": days_since_install,
                        "days_since_service": days_since_service}

        payload = {"bikes_data": bikes_data,
                   "component_types_data": component_types_data,
                   "bike_component_data": bike_component_data,
                   "bike_name": database_manager.read_bike_name(bike_component.bike_id),
                   "component_history_data": component_history_data,
                   "service_history_data": service_history_data,
                   "elapsed_days": elapsed_days}

        return payload

    def get_incident_reports(self):
        """Method to produce payload for page incident reports"""
        components = database_manager.read_all_components()
        component_data = [(component.component_id,
                           component.component_type,
                           component.component_name,
                           round(component.component_distance),
                           component.installation_status,
                           format_component_status(component.lifetime_status),
                           format_component_status(component.service_status),
                           database_manager.read_bike_name(component.bike_id),
                           format_cost(component.cost)
                           ) for component in components]

        bikes = database_manager.read_bikes()
        bikes_data = get_formatted_bikes_list(bikes)

        incident_reports = database_manager.read_all_incidents()


        incident_reports_data = [(incident.incident_id,
                                  incident.incident_date,
                                  incident.incident_status,
                                  incident.incident_severity,
                                  database_manager.read_component_names_id(incident.affected_component_ids),
                                  database_manager.read_bike_name_id(incident.affected_bike_id),
                                  incident.incident_description,
                                  incident.resolution_date,
                                  incident.resolution_notes,
                                  calculate_elapsed_days(incident.incident_date,
                                                         incident.resolution_date if incident.resolution_date
                                                         else get_formatted_datetime_now())[1]) for incident in incident_reports]

        payload = {"component_data": component_data,
                   "bikes_data": bikes_data,
                   "incident_reports_data": incident_reports_data}

        return payload

    def get_component_types(self):
        """Method to produce payload for page component types"""
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
        history_records = database_manager.read_subset_component_history(component_id)

        success, message = database_manager.write_component_distance(component, total_distance)
        logging.info(f"Updated distance for component {component.component_name}. New total distance: {total_distance}.")

        if not history_records:
            logging.warning(f"Component {component.component_name} has no installation records. Using alternate method to set lifetime and service status")
            success, message = self.update_component_lifetime_service_alternate("update",
                                                                                component_id,
                                                                                component.lifetime_expected,
                                                                                component.service_interval,
                                                                                None)

            if success:
                logging.info(message)
            else:
                logging.error(message)

            return success, message

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
                                                                                        round(lifetime_remaining)))

            success, message = database_manager.write_component_lifetime_status(component,
                                                                                lifetime_remaining,
                                                                                lifetime_status)

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
                    logging.info(f'Service record found for component {component.component_name}. Processing installation periods since service.')
                    
                    history_records = database_manager.read_subset_component_history(component.component_id)
                    sorted_history = sorted(history_records, key=lambda x: x.updated_date)
                    
                    distance_since_service = 0
                    
                    logging.info(f"Finding installation status at time of service for component {component.component_name}.")
                    service_time_status = next((record for record in reversed(sorted_history) 
                                                if record.updated_date <= latest_service_record.service_date),
                                                None)

                    logging.info(f"Finding relevant bikes since service date for component {component.component_name}.")
                    relevant_bikes = {record.bike_id for record in sorted_history 
                                    if record.updated_date >= latest_service_record.service_date
                                    and record.bike_id is not None}
                    
                    logging.info(f"Building list of relevant bikes to calculate distance to next service")
                    if (component.installation_status == "Installed" and
                        (not sorted_history or
                        latest_service_record.service_date >= sorted_history[-1].updated_date)):
                        relevant_bikes.add(component.bike_id)
                    
                    logging.info(f"Found {len(relevant_bikes)} bikes to check for rides to calculate distance to next service")
                    
                    logging.info(f"Querying rides for all relevant bikes to calculate distance to next service")
                    all_rides = []
                    for bike_id in relevant_bikes:
                        matching_rides = database_manager.read_matching_rides(bike_id, latest_service_record.service_date)
                        all_rides.extend(matching_rides)

                    all_rides.sort(key=lambda x: x.record_time)

                    logging.info(f"Filtering rides and installation status to only count rides when component was installed")
                    for ride in all_rides:
                        current_status = next(
                            (record for record in reversed(sorted_history)
                            if record.updated_date <= ride.record_time),
                            service_time_status)

                        if (current_status and 
                            current_status.update_reason == "Installed" and
                            current_status.bike_id == ride.bike_id):
                            distance_since_service += ride.ride_distance
                            logging.info(f"Ride on {ride.record_time} of {ride.ride_distance} km from bike {ride.bike_id} is relevant for calculating distance to next service")    
                
            elif component.installation_status != "Installed":
                if latest_service_record is None:
                    logging.info(f'Component {component.component_name} has been uninstalled and there are no previous services. Setting distance since service to distance at the time of uninstallation.')
                    distance_since_service = latest_history_record.distance_marker

                elif latest_service_record:
                    if latest_service_record.service_date >= component.updated_date:
                        logging.info(f'Component {component.component_name} has been serviced after or at uninstall. Setting distance since service to 0.')
                        distance_since_service = 0

                    else:
                        logging.info(f'Component {component.component_name} was serviced before uninstall. Processing installation periods from service to uninstall.')
                        
                        history_records = database_manager.read_subset_component_history(component.component_id)
                        sorted_history = sorted(history_records, key=lambda x: x.updated_date)
                        
                        distance_since_service = 0

                        logging.info(f"Finding installation status at time of service for component {component.component_name}.")
                        service_time_status = next((record for record in reversed(sorted_history) 
                                                if record.updated_date <= latest_service_record.service_date),
                                                None)

                        logging.info(f"Finding relevant bikes between service date and uninstall date for component {component.component_name}.")
                        relevant_bikes = {record.bike_id for record in sorted_history 
                                        if (record.updated_date >= latest_service_record.service_date and 
                                            record.updated_date <= component.updated_date and
                                            record.bike_id is not None)}
                        
                        logging.info(f"Found {len(relevant_bikes)} bikes to check for rides to calculate distance to next service")
                        
                        logging.info(f"Querying rides for all relevant bikes to calculate distance to next service")
                        all_rides = []
                        for bike_id in relevant_bikes:
                            matching_rides = database_manager.read_matching_rides(bike_id, latest_service_record.service_date)
                            all_rides.extend(matching_rides)
                        
                        all_rides.sort(key=lambda x: x.record_time)

                        logging.info(f"Filtering rides and installation status to only count rides when component was installed and before uninstall date")
                        for ride in all_rides:
                            if ride.record_time > component.updated_date:
                                break

                            current_status = next(
                                (record for record in reversed(sorted_history)
                                if record.updated_date <= ride.record_time),
                                service_time_status)

                            if (current_status and 
                                current_status.update_reason == "Installed" and
                                current_status.bike_id == ride.bike_id):
                                distance_since_service += ride.ride_distance
                                logging.info(f"Ride on {ride.record_time} of {ride.ride_distance} km from bike {ride.bike_id} is relevant for calculating distance to next service")

            service_next = component.service_interval - distance_since_service
            service_status = self.compute_component_status("service",
                                                            calculate_percentage_reached(component.service_interval,
                                                                                        round(service_next)))

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

    def update_component_lifetime_service_alternate(self, mode, component_id, lifetime_expected, service_interval, distance_offset):
        """Method to update component lifetime and service status when no installation records exist"""
        try:
            component = database_manager.read_component(component_id)
            total_distance = 0

            if mode == "create":
                total_distance = distance_offset
                database_manager.write_component_distance(component, total_distance)
         
            component = database_manager.read_component(component_id)

            if lifetime_expected:
                lifetime_remaining = lifetime_expected - component.component_distance
                lifetime_status = self.compute_component_status("lifetime",
                                                                calculate_percentage_reached(lifetime_expected,
                                                                                            round(lifetime_remaining)))
                database_manager.write_component_lifetime_status(component,
                                                                lifetime_remaining,
                                                                lifetime_status)
            else:
                database_manager.write_component_lifetime_status(component,
                                                                None,
                                                                None)
            if service_interval:
                service_next = service_interval
                service_status = self.compute_component_status("service",
                                                                calculate_percentage_reached(service_interval,
                                                                                            round(service_next)))

                database_manager.write_component_service_status(component,
                                                                service_next,
                                                                service_status)
            else:
                database_manager.write_component_service_status(component,
                                                                None,
                                                                None)

            return True, f"Component {component.component_name} updated with lifetime and service status (no installation records)"

        except Exception as error:
            logging.error(f"An error occurred updating lifetime and service status for {component.component_name} (no installation records): {error}")
            return False, f"An error occurred updating lifetime and service status for {component.component_name} (no installation records): {error}"

    def update_bike_status(self, bike_id):
        """Method to update status for a given bike based on component service and lifetime status"""
        if not bike_id:
            logging.warning(f"Component is not assigned to any bike. Skipping update of bike status")
            return False, "Component is not assigned to any bike. Skipping update of bike status"

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

            if component_status["breakdown_imminent"] > 0 or component_status["maintenance_required"] > 0:
                service_status = "Components need attention"
            elif component_status["ok"] > 0 or component_status["maintenance_approaching"] > 0:
                service_status = "All components healthy"
            elif all(value == 0 for value in component_status.values()) and count_installed > 0:
                service_status = "Maintenance not defined"
            elif count_installed == 0 and count_retired > 0:
                service_status = "No active components"
        
        else:
            service_status = "No components registered"
    
        logging.info(f"New status for bike {bike.bike_name}: {service_status}")

        success, message = database_manager.write_bike_service_status(bike, service_status)

        if success:
            logging.info(f"Bike update successful: {message}")
        else:
            logging.error(f"Bike update failed: {message}")

        return success, message

    def create_component(self,
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
        """Method to create component"""
        try:
            component_bike_id = None if component_bike_id == 'None' or component_bike_id == '' else component_bike_id
            expected_lifetime = int(expected_lifetime) if expected_lifetime and expected_lifetime.isdigit() else None
            service_interval = int(service_interval) if service_interval and service_interval.isdigit() else None
            cost = int(cost) if cost and cost.isdigit() else None

            new_component_data = {
                "installation_status": component_installation_status,
                "updated_date": component_updated_date,
                "component_name": component_name,
                "component_type": component_type,
                "bike_id": component_bike_id,
                "lifetime_expected": expected_lifetime,
                "service_interval": service_interval,
                "cost": cost,
                "component_distance_offset": offset,
                "notes": component_notes
            }

            component_id = generate_unique_id()
            success, message = database_manager.write_component_details(component_id, new_component_data)

            if success:
                logging.info(message)
                if component_installation_status == "Installed":
                    success, message = self.create_history_record(component_id, component_installation_status, component_bike_id, component_updated_date)
                    if success:
                        logging.info(message)
                    else:
                        logging.error(message)
                
                elif component_installation_status == "Not installed":
                    logging.warning(f"Component {component_name} is not installed, no history record created. Using alternate method to set lifetime and service status")
                    success, message = self.update_component_lifetime_service_alternate("create",
                                                                                        component_id,
                                                                                        new_component_data["lifetime_expected"],
                                                                                        new_component_data["service_interval"],
                                                                                        new_component_data["component_distance_offset"])

                self.update_component_type_count(component_type)

            else:
                logging.error(message)

            if success:
                if component_bike_id:
                    bike = database_manager.read_single_bike(component_bike_id)
                    if bike.bike_retired == "False":
                        compliance_report = self.process_bike_compliance_report(component_bike_id)
                        if not compliance_report["all_mandatory_present"] or not compliance_report["no_max_quantity_exceeded"]:
                            logging.warning(f"Component {component_name} successfully created. Use of component types on {bike.bike_name} are not compliant")
                            return "warning", f"Component {component_name} successfully created. Use of component types on {bike.bike_name} are not compliant. See bike details for more information", component_id
                
                return success, f"Component {component_name} successfully created", component_id

            else:
                return success, f"Creation of component {component_name} failed", component_id

        except Exception as error:
            logging.error(f"An error occurred creating component {component_name}: {str(error)}")
            return False, f"An error occurred creating component {component_name}: {str(error)}", component_id

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
        """Method to update component details"""
        try:
            component_bike_id = None if component_bike_id == 'None' or component_bike_id == '' else component_bike_id
            expected_lifetime = int(expected_lifetime) if expected_lifetime and expected_lifetime.isdigit() else None
            service_interval = int(service_interval) if service_interval and service_interval.isdigit() else None
            cost = int(cost) if cost and cost.isdigit() else None

            new_component_data = {
                "installation_status": component_installation_status,
                "updated_date": component_updated_date,
                "component_name": component_name,
                "component_type": component_type,
                "bike_id": component_bike_id,
                "lifetime_expected": expected_lifetime,
                "service_interval": service_interval,
                "cost": cost,
                "component_distance_offset": offset,
                "notes": component_notes}

            component = database_manager.read_component(component_id)
            if not component:
                message = f"{component_name} with id {component_id} not found."
                logging.error(message)
                return False, message, component_id

            success, message = database_manager.write_component_details(component_id, new_component_data)
            if success:
                logging.info(message)
                updated_component = database_manager.read_component(component_id)
                self.update_component_distance(component_id, updated_component.component_distance - component.component_distance_offset)

                if component.component_type != new_component_data["component_type"]:
                    self.update_component_type_count(component.component_type)
                    self.update_component_type_count(new_component_data["component_type"])
            else:
                logging.error(message)

            if success:
                if component_bike_id:
                    bike = database_manager.read_single_bike(component_bike_id)
                    if bike.bike_retired == "False":
                        compliance_report = self.process_bike_compliance_report(component_bike_id)
                        if not compliance_report["all_mandatory_present"] or not compliance_report["no_max_quantity_exceeded"]:
                            logging.warning(f"Component {component_name} successfully updated. Use of component types on {bike.bike_name} are not compliant")
                            return "warning", f"Component {component_name} successfully updated. Use of component types on {bike.bike_name} are not compliant. See bike details for more information", component_id
                
                return success, message, component_id

            else:
                return success, message, component_id

        except Exception as error:
            logging.error(f"An error occurred modifying component details {component_name}: {str(error)}")
            return False, f"An error occurred modifying component details {component_name}: {str(error)}", component_id

    def create_history_record(self,
                              component_id,
                              installation_status,
                              component_bike_id,
                              component_updated_date):
        """Method to create installation history record"""
        try:
            history_id = generate_unique_id()
            component = database_manager.read_component(component_id)

            success, message = self.validate_history_record("create history", component_id, history_id, component_updated_date, installation_status, component_bike_id)
            if not success:
                logging.error(f"Validation of history record failed: {message}")
                return success, message

            if installation_status == "Not installed":
                component_bike_id = component.bike_id
            
            history_data = {"history_id": history_id,
                            "component_id": component_id,
                            'bike_id': component_bike_id,
                            "component_name": component.component_name,
                            "updated_date": component_updated_date,
                            "update_reason": installation_status,
                            'distance_marker': 0}
            
            success, message = database_manager.write_history_record(history_data)
            if not success:
                logging.error(f"Error creating history record: {message}")
                return success, message
            
            success, message = self.process_history_records(component_id)
            if not success:
                logging.error(f"Error processing history record: {message}")
                return success, message
            
            if success:
                if component_bike_id and installation_status != "Not installed":
                    bike = database_manager.read_single_bike(component_bike_id)
                    if bike.bike_retired == "False":
                        compliance_report = self.process_bike_compliance_report(component_bike_id)
                        if not compliance_report["all_mandatory_present"] or not compliance_report["no_max_quantity_exceeded"]:
                            logging.warning(f"{message}. Use of component types on {bike.bike_name} are not compliant")
                            return "warning", f"{message}. Use of component types on {bike.bike_name} are not compliant. See bike details for more information"
                
                logging.info(f"Creation of history record successful: {message}")
            else:
                logging.error(f"Creation of history record failed: {message}")
                return success, message

            return success, message

        except Exception as error:
            logging.error(f"An error occured creating history record for component {component.component_name}: {str(error)}")
            return False, f"An error occured creating history record for {component.component_name}: {str(error)}"
        
    def update_history_record(self, history_id, updated_date):
        """Method to update a component history record with validation"""
        try:
            current_history = database_manager.read_single_history_record(history_id)
            component = database_manager.read_component(current_history.component_id)

            success, message = self.validate_history_record("edit history", current_history.component_id, history_id, updated_date, current_history.update_reason, current_history.bike_id)
            if not success:
                logging.error(f"Validation of history record failed: {message}")
                return success, message
            
            history_data = {"history_id": history_id,
                            "component_id": current_history.component_id,
                            'bike_id': current_history.bike_id,
                            "component_name": component.component_name,
                            "updated_date": updated_date,
                            "update_reason": current_history.update_reason,
                            'distance_marker': 0}
            
            success, message = database_manager.write_history_record(history_data)
            if not success:
                logging.error(f"Error updating history record: {message}")
                return success, message
            
            success, message = self.process_history_records(component.component_id)
            if not success:
                logging.error(f"Error processing history record: {message}")
                return success, message
            
            if success:
                logging.info(f"Update of history record successful: {message}")
            else:
                logging.error(f"Update of history record failed: {message}")
                return success, message

            return success, message 
        
        except Exception as error:
            logging.error(f"An error occured updating history record for component {component.component_name}: {str(error)}")
            return False, f"An error occured updating history record for {component.component_name}: {str(error)}"

    def validate_history_record(self, mode, component_id, history_id, updated_date, installation_status, component_bike_id):
        """Method to validate history records before processing and storing in database"""
    
        logging.info(f"Running general validation rules for history records: {history_id}.")
        
        component = database_manager.read_component(component_id)
        if not component:
            logging.warning(f"Associated component for history record not found for component {component.component_name}")
            return False, f"Associated component for history record not found for component {component.component_name}"
        
        success, message = validate_date_format(updated_date)
        if not success:
            logging.warning(message)
            return False, message
        
        if updated_date > datetime.now().strftime("%Y-%m-%d %H:%M"):
            logging.warning(f"Updated date cannot be in the future. Component: {component.component_name}")
            return False, f"Updated date cannot be in the future. Component: {component.component_name}"

        if mode == "create history":
            logging.info(f"Running validation rules for creation of history records: {history_id}.")

            oldest_history_record = database_manager.read_oldest_history_record(component.component_id)
            if oldest_history_record:
                if updated_date <= oldest_history_record.updated_date:
                    logging.warning(f"Date for new status cannot be at or before component creation date: {oldest_history_record.updated_date}. Component: {component.component_name}")
                    return False, f"Date for new status cannot be at or before component creation date: {oldest_history_record.updated_date}. Component: {component.component_name}"
            
            latest_history_record = database_manager.read_latest_history_record(component_id)
            if latest_history_record:
                if updated_date <= latest_history_record.updated_date:
                    logging.warning(f"Component status changes must be done chronologically. Date for new status cannot be at or before date for the last status: {latest_history_record.updated_date}. Component: {component.component_name}")
                    return False, f"Component status changes must be done chronologically. Date for new status cannot be at or before date for the last status: {latest_history_record.updated_date}. Component: {component.component_name}"
                
                if latest_history_record.update_reason == installation_status:
                    logging.warning(f"Component status for {component.component_name} is already set to: {installation_status}.")
                    return False, f"Component status for {component.component_name} is already set to: {installation_status}."

            if not latest_history_record and installation_status == "Not installed":
                logging.warning(f"Component {component.component_name} is not installed and can therefore not be set to 'Not installed'.")
                return False, f"Component {component.component_name} is not installed and can therefore not be set to 'Not installed'."
            
            if installation_status == "Installed" and component_bike_id is None:
                logging.warning(f"Status cannot be set to Installed without specifying bike. {component.component_name} is currently not assigned to a bike.")
                return False, f"Status cannot be set to Installed without specifying bike. {component.component_name} is currently not assigned to a bike."
            
            lastest_service_record = database_manager.read_latest_service_record(component_id)
            if lastest_service_record:
                if updated_date <= lastest_service_record.service_date and installation_status == "Retired":
                    logging.warning(f"A retired component cannot be serviced. Set retire date after latest service date: {lastest_service_record.service_date}")
                    return False, f"A retired component cannot be serviced. Set retire date after latest service date: {lastest_service_record.service_date}"
       
        if mode == "edit history":
            logging.info(f"Running validation rules for editing of history records: {history_id}.")

            current_history = database_manager.read_single_history_record(history_id)
            if not current_history:
                logging.warning(f"History record not found: {history_id}")
                return False, f"History record not found: {history_id}"
        
            history_records = database_manager.read_subset_component_history(component_id)
            sorted_records = sorted(history_records, key=lambda x: x.updated_date)
            current_index = next((i for i, record in enumerate(sorted_records) 
                                if record.history_id == history_id), None)
            
            if current_index is not None:
                if current_index > 0:
                    prev_record = sorted_records[current_index - 1]
                    if updated_date <= prev_record.updated_date:
                        logging.warning(f"Updated date must be after previous installation record date: {prev_record.updated_date}")
                        return False, f"Updated date must be after previous installation record date: {prev_record.updated_date}"
                
                if current_index < len(sorted_records) - 1:
                    next_record = sorted_records[current_index + 1]
                    if updated_date >= next_record.updated_date:
                        logging.warning(f"Updated date must be before next installation record date: {next_record.updated_date}")
                        return False, f"Updated date must be before next installation record date: {next_record.updated_date}"
                    
                if current_index == 0:
                    oldest_service_record = database_manager.read_oldest_service_record(component_id)
                    if oldest_service_record and updated_date >= oldest_service_record.service_date:
                        logging.warning(f"First installation date for component {component.component_name} cannot be at or after first service date: {oldest_service_record.service_date}")
                        return False, f"First installation date for component {component.component_name} cannot be at or after first service date: {oldest_service_record.service_date}"
            
        logging.info(f"Validation of history record for {component.component_name} passed")
        return True, f"Validation of service record for {component.component_name} passed"
        
    def process_history_records(self, component_id):
        """Method to calculate distance and bike id for history records"""
        try:
            component = database_manager.read_component(component_id)
            history_records = database_manager.read_subset_component_history(component_id)
            if not history_records:
                logging.warning(f"No history records found for component: {component.component_name}")
                return False, f"No history records found for component: {component.component_name}"

            sorted_records = sorted(history_records, key=lambda x: x.updated_date)
            previous_record = None

            for record in sorted_records:
                if previous_record is None:
                    distance_marker = 0
                else:
                    if previous_record.update_reason == "Installed":
                        logging.info(f'Timespan for historic distance query: start date {previous_record.updated_date} stop date {record.updated_date}.')
                        historic_distance = database_manager.read_sum_distance_subset_rides(previous_record.bike_id, previous_record.updated_date, record.updated_date)
                        distance_marker = previous_record.distance_marker + historic_distance

                    else:
                        distance_marker = previous_record.distance_marker

                history_data = {"history_id": record.history_id,
                                "component_id": record.component_id,
                                'bike_id': record.bike_id,
                                "component_name": record.component_name,
                                "updated_date": record.updated_date,
                                "update_reason": record.update_reason,
                                'distance_marker': distance_marker}
                
                success, message = database_manager.write_history_record(history_data)
                if not success:
                    logging.error(f"Failed to update distance for component {component.component_name} and history record {record.history_id}: {message}")
                    return False, f"Failed to update distance for component {component.component_name} and history record {record.history_id}: {message}"

                previous_record = database_manager.read_single_history_record(record.history_id)
            
            latest_history_record = database_manager.read_latest_history_record(component_id)
            current_distance = latest_history_record.distance_marker

            if latest_history_record.update_reason == "Installed":
                logging.info(f'Calculating additional distance since last history record: start date {latest_history_record.updated_date} stop date {datetime.now().strftime("%Y-%m-%d %H:%M")}')
                additional_distance = database_manager.read_sum_distance_subset_rides(latest_history_record.bike_id,
                                                                                      latest_history_record.updated_date,
                                                                                      datetime.now().strftime("%Y-%m-%d %H:%M"))
                current_distance += additional_distance
                logging.info(f'Total distance: {current_distance} (History: {latest_history_record.distance_marker}, Additional: {additional_distance})')
                
            self.update_component_distance(component_id, current_distance)

            if success:
                latest_history = database_manager.read_latest_history_record(component_id)
                
                component_data = {
                    "installation_status": latest_history.update_reason,
                    "updated_date": latest_history.updated_date,
                    "component_name": component.component_name,
                    "component_type": component.component_type,
                    "bike_id": None if latest_history_record.update_reason == "Not installed" else latest_history_record.bike_id,
                    "lifetime_expected": component.lifetime_expected,
                    "service_interval": component.service_interval,
                    "cost": component.cost,
                    "component_distance_offset": component.component_distance_offset,
                    "notes": component.notes}

                success, message = database_manager.write_component_details(component_id, component_data)
                if not success:
                    logging.error(f"An error occured updating component installation status for {component.component_name}: {message}")
                    return False, f"An error occured updating component installation status for {component.component_name}: {message}"
                
                updated_component = database_manager.read_component(component_id)

                service_records = database_manager.read_subset_service_history(component_id)
                if service_records:
                    first_service = service_records.first()
                    success, message = self.process_service_records(component_id,
                                                                    first_service.service_id,
                                                                    first_service.service_date,
                                                                    first_service.description)
                    if not success:
                        logging.error(f"An error occured triggering update of service records for {updated_component.component_name}: {message}")
                        return False, f"An error occured triggering update of service records for {updated_component.component_name}: {message}"

                self.update_component_lifetime_status(updated_component)
                self.update_component_service_status(updated_component)
                
                if updated_component.bike_id is None:
                    bike_id = database_manager.read_bike_id_recent_component_history(component_id)
                else:
                    bike_id = updated_component.bike_id
                
                self.update_bike_status(bike_id)

            return True, "Successfully processed history records and related services"

        except Exception as error:
            logging.error(f"An error occurred processing history records for component {component_id}: {str(error)}")
            return False, f"Error processing history records for component {component_id}: {str(error)}"
      
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
            logging.error(f"An error occured creating service record for component with id {component_id}: {str(error)}")
            return False, f"Error creating service record for {component_id}: {str(error)}"
    
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
            logging.error(f"An error occured updating service records for component with id {component_id}: {str(error)}")
            return False, f"Error updating service records for component with id {component_id}: {str(error)}"

    def validate_service_record(self, mode, component_id, service_id, service_date):
        """Method to validate service records before processing and storing in database"""

        logging.info(f"Running validation rules for service records: {service_id}.")
        
        current_service = database_manager.read_single_service_record(service_id)
        if mode == "edit service" and not current_service:
            logging.warning(f"Service record not found: {service_id}")
            return False, f"Service record not found: {service_id}"

        component = database_manager.read_component(component_id)
        if not component:
            logging.warning(f"Associated component for service record for component {component.component_name} not found")
            return False, f"Associated component for service record for component {component.component_name} not found"

        success, message = validate_date_format(service_date)
        if not success:
            logging.warning(message)
            return False, message
        
        history_records = database_manager.read_subset_component_history(component.component_id)
        if not history_records:
            logging.warning(f"Services cannot be registered to components that have never been installed. Component: {component.component_name}")
            return False, f"Services cannot be registered to components that have never been installed. Component: {component.component_name}"

        oldest_history_record_date = database_manager.read_oldest_history_record(component.component_id).updated_date
        
        if service_date <= oldest_history_record_date:
            logging.warning(f"Service date cannot be at or before component creation date: {oldest_history_record_date}. Component: {component.component_name}")
            return False, f"Service date cannot be at or before component creation date {oldest_history_record_date}. Component: {component.component_name}"

        if service_date > datetime.now().strftime("%Y-%m-%d %H:%M"):
            logging.warning(f"Service date cannot be in the future. Component: {component.component_name}")
            return False, f"Service date cannot be in the future. Component: {component.component_name}"
        
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
        sorted_history = sorted(history_records, key=lambda x: x.updated_date)

        logging.info(f"Consolidating and sorting all services for component {component.component_name}")
        all_services = [service for service in all_services if service.service_id != service_id]
        all_services.append(type('Service', (), current_service_data)())
        all_services.sort(key=lambda x: x.service_date)

        logging.info(f"Iterating over all services for component {component.component_name} to update distance markers and bike ids")
        for index, service in enumerate(all_services):
            if index == 0:
                accumulated_distance = 0
                current_installation = None
                service_date = service.service_date
                
                for record in sorted_history:
                    if record.updated_date > service_date:
                        break
                        
                    if record.update_reason == "Installed":
                        current_installation = record
                    elif record.update_reason == "Not installed" and current_installation:
                        logging.info(f"Calculating distance for installation period for first service record: {current_installation.updated_date} to {record.updated_date}")
                        period_distance = database_manager.read_sum_distance_subset_rides(current_installation.bike_id,
                                                                                          current_installation.updated_date,
                                                                                          record.updated_date)
                        accumulated_distance += period_distance
                        logging.info(f"Added {period_distance} km from bike {current_installation.bike_id}")
                        current_installation = None

                logging.info(f"Processing final installation period for first service record")
                if current_installation:
                    period_distance = database_manager.read_sum_distance_subset_rides(current_installation.bike_id,
                                                                                      current_installation.updated_date,
                                                                                      service_date)
                    accumulated_distance += period_distance
                    logging.info(f"Added final period of {period_distance} km from bike {current_installation.bike_id} for first service record")

                new_service_distance = accumulated_distance

            else:
                logging.info(f"Processing subsequent service records, using service dates to calculate distance")
                previous_service_date = all_services[index-1].service_date
                current_service_date = service.service_date
                
                accumulated_distance = 0
                current_installation = None
                
                initial_status = next(record for record in reversed(sorted_history)
                                      if record.updated_date <= previous_service_date)
                
                if initial_status.update_reason == "Installed":
                    current_installation = initial_status
                
                logging.info(f"Processing installation changes within window {previous_service_date} to {current_service_date}")
                for record in sorted_history:
                    if record.updated_date <= previous_service_date:
                        logging.info(f"Record {record.history_id} dated {record.updated_date} outside window, skipping")
                        continue
                    if record.updated_date > current_service_date:
                        logging.info(f"Record {record.history_id} dated {record.updated_date} inside window, processing")
                        break
                    
                    if record.update_reason == "Installed":
                        current_installation = record
                    elif record.update_reason == "Not installed" and current_installation:
                        logging.info(f"Calculating distance for the installation period: {current_installation.updated_date} to {record.updated_date}")
                        period_distance = database_manager.read_sum_distance_subset_rides(
                            current_installation.bike_id,
                            max(current_installation.updated_date, previous_service_date),
                            record.updated_date)
                        accumulated_distance += period_distance
                        logging.info(f"Added {period_distance} km from bike {current_installation.bike_id} ({current_installation.updated_date} to {record.updated_date})")
                        current_installation = None

                logging.info("Processing final installation period at the end of window")
                if current_installation:
                    period_distance = database_manager.read_sum_distance_subset_rides(current_installation.bike_id,
                                                                                      max(current_installation.updated_date, previous_service_date),
                                                                                      current_service_date)
                    accumulated_distance += period_distance
                    logging.info(f"Added final period of {period_distance} km from bike {current_installation.bike_id} ({current_installation.updated_date} to {current_service_date})")

                new_service_distance = accumulated_distance
                logging.info(f"Total accumulated distance: {accumulated_distance} km")

            logging.info(f"Setting bike_id based on component status at service time")
            relevant_history = next(record for record in reversed(sorted_history)
                                    if record.updated_date <= service.service_date)
                
            new_bike_id = relevant_history.bike_id if relevant_history.update_reason == "Installed" else None

            service_data = {
                'service_id': service.service_id,
                'component_id': component.component_id,
                'component_name': component.component_name,
                'service_date': service.service_date,
                'description': service.description,
                'bike_id': new_bike_id,
                'distance_marker': new_service_distance
            }
            
            success, message = database_manager.write_service_record(service_data)
            if not success:
                logging.error(f"Error updating service records for {component.component_name}: {message}")
                return success, f"Error updating service records: {message}"

        logging.info(f"Service records for component {component.component_name} successfully updated")
        
        updated_component = database_manager.read_component(component_id)
        self.update_component_service_status(updated_component)
        if component.installation_status == "Installed":
            self.update_bike_status(component.bike_id)

        return True, "All service records successfully processed"

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

    def process_bike_compliance_report(self, bike_id):
        """Method to check if a bike has all mandatory components and respects max quantities"""
        compliance_report = {"all_mandatory_present": True,
                             "no_max_quantity_exceeded": True,
                             "missing_mandatory": [],
                             "exceeding_max_quantity": {}}

        component_types_raw = database_manager.read_all_component_types()

        component_types = {component_type[0]:
                                {'expected_lifetime': component_type[1],
                                 'service_interval': component_type[2],
                                 'in_use': component_type[3],
                                 'mandatory': component_type[4],
                                 'max_quantity': component_type[5]} for component_type in component_types_raw}

        installed_components_raw = database_manager.read_subset_installed_components(bike_id)
        installed_components = list(installed_components_raw)

        component_counts = {}
        for component in installed_components:
            component_type = component.component_type
            if component_type in component_counts:
                component_counts[component_type] += 1
            else:
                component_counts[component_type] = 1
        
        for component_type, properties in component_types.items():
            if properties['mandatory'] == 'Yes':
                if component_type not in component_counts:
                    compliance_report["all_mandatory_present"] = False
                    compliance_report["missing_mandatory"].append(component_type)

            if properties['max_quantity'] is not None and properties['max_quantity'] > 0:
                if component_type in component_counts and component_counts[component_type] > properties['max_quantity']:
                    compliance_report["no_max_quantity_exceeded"] = False
                    compliance_report["exceeding_max_quantity"][component_type] = {"current": component_counts[component_type],
                                                                                   "max_allowed": properties['max_quantity']}
        
        compliance_report["missing_mandatory"] = ", ".join(compliance_report["missing_mandatory"]) if compliance_report["missing_mandatory"] else "None"
        
        if compliance_report["exceeding_max_quantity"]:
            exceeded_strings = []
            for comp_type, details in compliance_report["exceeding_max_quantity"].items():
                exceeded_strings.append(f"{comp_type} (has {details['current']} / max {details['max_allowed']})")
            compliance_report["exceeding_max_quantity"] = ", ".join(exceeded_strings)
        else:
            compliance_report["exceeding_max_quantity"] = "None"

        return compliance_report

    def create_incident_record(self,
                               incident_date,
                               incident_status,
                               incident_severity,
                               affected_component_ids,
                               affected_bike_id,
                               incident_description,
                               resolution_date,
                               resolution_notes):
        """Method to add incident record"""
        try:
            incident_id = generate_unique_id()

            affected_bike_id = affected_bike_id if affected_bike_id else None
            incident_description = incident_description if incident_description else None
            resolution_date = resolution_date if resolution_date else None
            resolution_notes = resolution_notes if resolution_notes else None

            incident_data = {"incident_id": incident_id,
                             "incident_date": incident_date,
                             "incident_status": incident_status,
                             "incident_severity": incident_severity,
                             "affected_component_ids": json.dumps(affected_component_ids) if affected_component_ids else None,
                             "affected_bike_id": affected_bike_id,
                             "incident_description": incident_description,
                             "resolution_date": resolution_date,
                             "resolution_notes": resolution_notes}
            
            success, message = database_manager.write_incident_record(incident_data)

            if success:
                logging.info(f"Creation of incident report successful: {message}")
            else:
                logging.error(f"Creation of incident report failed: {message}")

            return success, message

        except Exception as error:
            logging.error(f"Error creating incident report with id {incident_id}: {str(error)}")
            return False, f"Error creating incident report with id {incident_id}: {str(error)}"
        
    def update_incident_record(self,
                               incident_id,
                               incident_date,
                               incident_status,
                               incident_severity,
                               affected_component_ids,
                               affected_bike_id,
                               incident_description,
                               resolution_date,
                               resolution_notes):
        """Method to update incident record"""
        try:
            affected_bike_id = affected_bike_id if affected_bike_id else None
            incident_description = incident_description if incident_description else None
            resolution_date = resolution_date if resolution_date else None
            resolution_notes = resolution_notes if resolution_notes else None

            incident_data = {"incident_id": incident_id,
                             "incident_date": incident_date,
                             "incident_status": incident_status,
                             "incident_severity": incident_severity,
                             "affected_component_ids": json.dumps(affected_component_ids) if affected_component_ids else None,
                             "affected_bike_id": affected_bike_id,
                             "incident_description": incident_description,
                             "resolution_date": resolution_date,
                             "resolution_notes": resolution_notes}
            
            success, message = database_manager.write_incident_record(incident_data)

            if success:
                logging.info(f"Update of incident report successful: {message}")
            else:
                logging.error(f"Update of incident report failed: {message}")

            return success, message

        except Exception as error:
            logging.error(f"Error updating incident report with id {incident_id}: {str(error)}")
            return False, f"Error updating incident report with id {incident_id}: {str(error)}"
    
    def modify_component_type(self,
                            component_type,
                            expected_lifetime,
                            service_interval,
                            mandatory,
                            max_quantity,
                            mode):
        """Method to create or update component types"""
        expected_lifetime = int(expected_lifetime) if expected_lifetime and expected_lifetime.isdigit() else None
        service_interval = int(service_interval) if service_interval and service_interval.isdigit() else None
        max_quantity = int(max_quantity) if max_quantity and max_quantity.isdigit() else None

        in_use = database_manager.count_component_types_in_use(component_type)
        
        component_type_data = {"component_type": component_type,
                            "service_interval": service_interval,
                            "expected_lifetime": expected_lifetime,
                            "in_use": in_use,
                            "mandatory": mandatory,
                            "max_quantity": max_quantity}

        if mode == "create":
            all_component_types_raw = database_manager.read_all_component_types()
            lowercase_component_types = [item[0].lower() for item in all_component_types_raw]
            if component_type.lower() in lowercase_component_types:
                logging.warning(f"Component type '{component_type}' already exists. Duplicate component types are not allowed. New component type not created")
                return False, f"Component type '{component_type}' already exists. Duplicate component types are not allowed. New component type not created"

        success, message = database_manager.write_component_type(component_type_data)

        if success:
            logging.info(f"Component type update successful: {message}")
        else:
            logging.error(f"Component type update failed: {message}")

        return success, message

    def update_component_type_count(self, component_type):
        """Method to update only the count of components for a given component type"""
        existing_type = database_manager.read_single_component_type(component_type)
        
        if existing_type:
            in_use = database_manager.count_component_types_in_use(component_type)
            
            component_type_data = {"component_type": component_type,
                                   "service_interval": existing_type.service_interval,
                                   "expected_lifetime": existing_type.expected_lifetime,
                                   "in_use": in_use,
                                   "mandatory": existing_type.mandatory,
                                   "max_quantity": existing_type.max_quantity}
            
            success, message = database_manager.write_component_type(component_type_data)
            
            if success:
                logging.info(f"Component type count updated: {component_type} used by {in_use} components")
            else:
                logging.error(f"Component type count update failed: {message}")
            
            return success, message
        
        return False, f"Component type not found: {component_type}"
    
    def delete_record(self, table_selector, record_id):
        """Method to delete a given record and associated records"""
        logging.info(f"Attempting to delete record with id {record_id} from table {table_selector}")

        component_id = None
        if table_selector == "Services":
            component_id = database_manager.read_single_service_record(record_id).component_id
            component = database_manager.read_component(component_id)
        
        elif table_selector == "ComponentHistory":
            component_id = database_manager.read_single_history_record(record_id).component_id
            component = database_manager.read_component(component_id)
            service_history = database_manager.read_subset_service_history(component_id)
            history_records = database_manager.read_subset_component_history(component_id)

            if service_history and history_records.count() == 1:
                logging.warning(f"Cannot delete initial history record {record_id} for component {component.component_name} as service records exist")
                return False, f"Cannot delete initial history record {record_id} for component {component.component_name} as service records exist", component_id
        
        elif table_selector == "Components":
            component = database_manager.read_component(record_id)
            component_type = component.component_type
            bike_id = database_manager.read_component(record_id).bike_id
        
        elif table_selector == "ComponentTypes":
            component_type = database_manager.read_single_component_type(record_id)
            if component_type.in_use > 0:
                logging.warning(f"Component type {component_type.component_type} is in use by {component_type.in_use} components and cannot be deleted")
                return False, f"Component type {component_type.component_type} is in use by {component_type.in_use} components and cannot be deleted", component_id
        
        success, message = database_manager.write_delete_record(table_selector, record_id)

        if success:
            logging.info(f"Deletion successful: {message}")
            if table_selector == "Services":
                logging.info(f"Recalculating service records for component {component.component_name} after deletion")

                service_records = database_manager.read_subset_service_history(component_id)
                if service_records:
                    first_service = service_records.first()
                    success, message = self.process_service_records(component_id,
                                                                    first_service.service_id,
                                                                    first_service.service_date,
                                                                    first_service.description)
                    if not success:
                        logging.error(f"An error occured triggering update of service records for {component.component_name} after deletion: {message}")
                        return False, f"An error occured triggering update of service records for {component.component_name} after deletion: {message}", component_id
                
                elif not service_records:
                    component = database_manager.read_component(component_id)
                    self.update_component_distance(component_id, component.component_distance - component.component_distance_offset)

            elif table_selector == "ComponentHistory":
                logging.info(f"Recalculating installation history records for component {component.component_name} after deletion")
                
                if history_records.count() == 0:
                    database_manager.write_component_distance(component, component.component_distance_offset)
                    success, message, component_id = self.modify_component_details(component_id,
                                                                     "Not installed",
                                                                     get_formatted_datetime_now(),
                                                                     component.component_name,
                                                                     component.component_type,
                                                                     "None",
                                                                     str(component.lifetime_expected),
                                                                     str(component.service_interval),
                                                                     str(component.cost),
                                                                     component.component_distance_offset,
                                                                     component.notes)
                
                else:
                    success, message = self.process_history_records(component_id)
                
                if not success:
                    logging.error(f"An error occured triggering update of history records for {component_id} after deletion: {message}")
                    return False, f"An error occured triggering update of history records for {component_id} after deletion: {message}", component_id
                
            elif table_selector == "Components":
                self.update_component_type_count(component_type)
                if bike_id:
                    self.update_bike_status(bike_id)
        
        else:
            logging.error(f"Deletion of {record_id} failed: {message}")
            return False, f"Deletion of {record_id} failed: {message}", component_id

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
