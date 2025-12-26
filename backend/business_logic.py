#!/usr/bin/env python3
"""Module to handle business logic"""

import logging
from datetime import datetime
import json
from utils import (read_config,
                   calculate_percentage_reached,
                   generate_unique_id,
                   format_component_status,
                   format_cost,
                   get_formatted_datetime_now,
                   validate_date_format,
                   calculate_elapsed_days,
                   get_formatted_bikes_list,
                   parse_json_string,
                   generate_incident_title,
                   generate_workplan_title,
                   parse_checkbox_progress)
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

            exceeded_max_count = sum(1 for component in components
                                     if component.installation_status == "Installed" and
                                     (component.lifetime_status == "Lifetime exceeded" or
                                      component.service_status == "Service interval exceeded"))

            due_past_threshold_count = sum(1 for component in components
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
                               exceeded_max_count,
                               due_past_threshold_count,
                               compliance_report))

        open_incidents = self.process_incidents(database_manager.read_open_incidents())

        planned_workplans = self.process_workplans(database_manager.read_planned_workplans())

        assigned_collections = [collection.bike_id for collection in database_manager.read_all_collections() if collection.bike_id]

        payload = {"bikes_data": bikes_data,
                   "open_incidents": open_incidents,
                   "planned_workplans": planned_workplans,
                   "assigned_collections": assigned_collections}

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

        all_components_data = database_manager.read_all_components()
        all_collections = self.get_all_collections()

        bike_components = database_manager.read_subset_components(bike_id)
        bike_component_data = []
        
        for component in bike_components:
            triggers = self.calculate_component_triggers(component)

            bike_component_data.append((component.component_id,
                                       "-" if component.lifetime_remaining is None else round(component.lifetime_remaining),
                                       "-" if component.service_next is None else round(component.service_next),
                                       component.installation_status,
                                       component.component_type,
                                       component.component_name,
                                       round(component.component_distance),
                                       format_component_status(component.lifetime_status),
                                       format_component_status(component.service_status),
                                       format_cost(component.cost),
                                       triggers["lifetime_trigger"],
                                       triggers["service_trigger"],
                                       "-" if component.lifetime_remaining_days is None else component.lifetime_remaining_days,
                                       "-" if component.service_next_days is None else component.service_next_days,
                                       component.updated_date))

        count_installed = sum(1 for component in bike_component_data if component[3] == "Installed")
        count_retired = sum(1 for component in bike_component_data if component[3] == "Retired")

        sum_cost = sum(component[9] for component in bike_component_data
                      if component[3] == "Installed"
                      and component[9] != "No estimate"
                      and isinstance(component[9], int)
                      and component[7] in ["Due for replacement", "Lifetime exceeded"])
        
        sum_cost = sum_cost if sum_cost > 0 else "No estimate"

        recent_rides = database_manager.read_recent_rides(bike_id)
        recent_rides_data = [(ride.ride_id,
                              ride.record_time,
                              ride.ride_name,
                              round(ride.ride_distance),
                              ride.commute
                              ) for ride in recent_rides]

        compliance_report = self.process_bike_compliance_report(bike_id)

        open_incidents = self.process_incidents(database_manager.read_open_incidents())

        incident_reports_data = [(incident.incident_id,
                                  incident.incident_date,
                                  incident.incident_status,
                                  incident.incident_severity,
                                  parse_json_string(incident.incident_affected_component_ids),
                                  database_manager.read_component_names(incident.incident_affected_component_ids),
                                  incident.incident_affected_bike_id,
                                  database_manager.read_bike_name(incident.incident_affected_bike_id),
                                  incident.incident_description,
                                  incident.resolution_date,
                                  incident.resolution_notes,
                                  calculate_elapsed_days(incident.incident_date,
                                                         incident.resolution_date if incident.resolution_date
                                                         else get_formatted_datetime_now())[1],
                                  generate_incident_title(database_manager.read_component_names(incident.incident_affected_component_ids),
                                                          database_manager.read_bike_name(incident.incident_affected_bike_id),
                                                          incident.incident_description)) for incident in database_manager.read_open_incidents()]

        planned_workplans = self.process_workplans(database_manager.read_planned_workplans())

        workplans_data = [(workplan.workplan_id,
                           workplan.due_date,
                           workplan.workplan_status,
                           workplan.workplan_size,
                           parse_json_string(workplan.workplan_affected_component_ids),
                           database_manager.read_component_names(workplan.workplan_affected_component_ids),
                           workplan.workplan_affected_bike_id,
                           database_manager.read_bike_name(workplan.workplan_affected_bike_id),
                           workplan.workplan_description,
                           workplan.completion_date,
                           workplan.completion_notes,
                           calculate_elapsed_days(workplan.due_date,
                                                  workplan.completion_date if workplan.completion_date
                                                  else get_formatted_datetime_now())[1],
                           generate_workplan_title(database_manager.read_component_names(workplan.workplan_affected_component_ids),
                                                   database_manager.read_bike_name(workplan.workplan_affected_bike_id),
                                                   workplan.workplan_description),
                           parse_checkbox_progress(workplan.workplan_description)) for workplan in database_manager.read_planned_workplans()]

        component_collection_names, component_collection_data = self.get_component_collection_mapping()
        
        payload = {"recent_rides": recent_rides_data,
                   "bikes_data": bikes_data,
                   "bike_data": bike_data,
                   "component_types_data": component_types_data,
                   "bike_component_data": bike_component_data,
                   "all_components_data": all_components_data,
                   "all_collections": all_collections,
                   "count_installed" : count_installed,
                   "count_retired" : count_retired,
                   "sum_cost" : sum_cost,
                   "compliance_report": compliance_report,
                   "open_incidents": open_incidents,
                   "incident_reports_data": incident_reports_data,
                   "planned_workplans": planned_workplans,
                   "workplans_data": workplans_data,
                   "component_collection_names": component_collection_names,
                   "component_collection_data": component_collection_data}

        return payload

    def get_component_overview(self):
        """Method to produce payload for page component overview"""
        all_components_data = database_manager.read_all_components()

        all_components = database_manager.read_all_components_objects()
        all_components_display_data = []
        for component in all_components:
            triggers = self.calculate_component_triggers(component)

            all_components_display_data.append((component.component_id,
                                                component.component_type,
                                                component.component_name,
                                                round(component.component_distance),
                                                component.installation_status,
                                                format_component_status(component.lifetime_status),
                                                format_component_status(component.service_status),
                                                database_manager.read_bike_name(component.bike_id),
                                                format_cost(component.cost),
                                                triggers["lifetime_trigger"],
                                                triggers["service_trigger"],
                                                component.bike_id,
                                                component.updated_date))

        count_installed = sum(1 for component in all_components_display_data if component[4] == "Installed")
        count_not_installed = sum(1 for component in all_components_display_data if component[4] == "Not installed")
        count_retired = sum(1 for component in all_components_display_data if component[4] == "Retired")

        bikes = database_manager.read_bikes()
        bikes_data = get_formatted_bikes_list(bikes)

        component_types_data = database_manager.read_all_component_types()

        open_incidents = self.process_incidents(database_manager.read_open_incidents())

        planned_workplans = self.process_workplans(database_manager.read_planned_workplans())

        all_collections = self.get_all_collections()
        component_collection_names, component_collection_data = self.get_component_collection_mapping()

        payload = {"all_components_data": all_components_data,
                   "all_components_display_data": all_components_display_data,
                   "bikes_data": bikes_data,
                   "component_types_data": component_types_data,
                   "count_installed": count_installed,
                   "count_not_installed": count_not_installed,
                   "count_retired": count_retired,
                   "open_incidents": open_incidents,
                   "planned_workplans": planned_workplans,
                   "all_collections": all_collections,
                   "component_collection_names": component_collection_names,
                   "component_collection_data": component_collection_data}

        return payload

    def get_component_details(self, component_id):
        """Method to produce payload for page component details"""
        bikes = database_manager.read_bikes()
        bikes_data = get_formatted_bikes_list(bikes)

        component_types_data = database_manager.read_all_component_types()

        all_components_data = database_manager.read_all_components()

        bike_component = database_manager.read_component(component_id)

        component_age_days = None
        oldest_history_record = database_manager.read_oldest_history_record(component_id)
        if oldest_history_record:
            if bike_component.installation_status == "Retired":
                end_date = bike_component.updated_date
            else:
                end_date = get_formatted_datetime_now()
            success, age_days = calculate_elapsed_days(oldest_history_record.updated_date, end_date)
            
            if success:
                component_age_days = age_days

        triggers = self.calculate_component_triggers(bike_component)

        lifetime_percentage = (calculate_percentage_reached(bike_component.lifetime_expected,
                                                            round(bike_component.lifetime_remaining))
                              if bike_component.lifetime_remaining is not None else None)
        lifetime_percentage_days = (calculate_percentage_reached(bike_component.lifetime_expected_days,
                                                                 bike_component.lifetime_remaining_days)
                                   if bike_component.lifetime_remaining_days is not None else None)

        service_percentage = (calculate_percentage_reached(bike_component.service_interval,
                                                           round(bike_component.service_next))
                             if bike_component.service_next is not None else None)
        service_percentage_days = (calculate_percentage_reached(bike_component.service_interval_days,
                                                                bike_component.service_next_days)
                                  if bike_component.service_next_days is not None else None)

        bike_component_data = {"bike_id": bike_component.bike_id,
                               "component_id": bike_component.component_id,
                               "updated_date": bike_component.updated_date,
                               "component_name": bike_component.component_name,
                               "component_type": bike_component.component_type,
                               "component_distance": (round(bike_component.component_distance)
                                                      if bike_component.component_distance is not None else None),
                                "installation_status": bike_component.installation_status,
                                "component_age_days": component_age_days,
                                "lifetime_expected": bike_component.lifetime_expected,
                                "lifetime_expected_days": bike_component.lifetime_expected_days,
                                "lifetime_remaining": (round(bike_component.lifetime_remaining)
                                                       if bike_component.lifetime_remaining is not None else None),
                                "lifetime_remaining_days": bike_component.lifetime_remaining_days,
                                "lifetime_status": format_component_status(bike_component.lifetime_status),
                                "lifetime_status_distance": format_component_status(triggers["lifetime_status_distance"]),
                                "lifetime_status_days": format_component_status(triggers["lifetime_status_days"]),
                                "lifetime_trigger": triggers["lifetime_trigger"],
                                "lifetime_percentage": lifetime_percentage,
                                "lifetime_percentage_days": lifetime_percentage_days,
                                "service_interval": bike_component.service_interval,
                                "service_interval_days": bike_component.service_interval_days,
                                "service_next": (int(bike_component.service_next)
                                                 if bike_component.service_next is not None else None),
                                "service_next_days": bike_component.service_next_days,
                                "service_status": format_component_status(bike_component.service_status),
                                "service_status_distance": format_component_status(triggers["service_status_distance"]),
                                "service_status_days": format_component_status(triggers["service_status_days"]),
                                "service_trigger": triggers["service_trigger"],
                                "service_percentage": service_percentage,
                                "service_percentage_days": service_percentage_days,
                                "threshold_km": bike_component.threshold_km,
                                "threshold_days": bike_component.threshold_days,
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

        latest_service_record = database_manager.read_latest_service_record(component_id)
        if latest_service_record:
            success, message = calculate_elapsed_days(latest_service_record.service_date, get_formatted_datetime_now())
            if success:
                days_since_service = f"{message} days ago"
            else:
                days_since_service = "Failed to calculate days since last service"
        else:
            days_since_service = "Component has never been serviced"

        open_incidents = self.process_incidents(database_manager.read_open_incidents())

        incident_reports_data = [(incident.incident_id,
                                  incident.incident_date,
                                  incident.incident_status,
                                  incident.incident_severity,
                                  parse_json_string(incident.incident_affected_component_ids),
                                  database_manager.read_component_names(incident.incident_affected_component_ids),
                                  incident.incident_affected_bike_id,
                                  database_manager.read_bike_name(incident.incident_affected_bike_id),
                                  incident.incident_description,
                                  incident.resolution_date,
                                  incident.resolution_notes,
                                  calculate_elapsed_days(incident.incident_date,
                                                         incident.resolution_date if incident.resolution_date
                                                         else get_formatted_datetime_now())[1],
                                  generate_incident_title(database_manager.read_component_names(incident.incident_affected_component_ids),
                                                          database_manager.read_bike_name(incident.incident_affected_bike_id),
                                                          incident.incident_description)) for incident in database_manager.read_open_incidents()]
        
        planned_workplans = self.process_workplans(database_manager.read_planned_workplans())

        workplans_data = [(workplan.workplan_id,
                           workplan.due_date,
                           workplan.workplan_status,
                           workplan.workplan_size,
                           parse_json_string(workplan.workplan_affected_component_ids),
                           database_manager.read_component_names(workplan.workplan_affected_component_ids),
                           workplan.workplan_affected_bike_id,
                           database_manager.read_bike_name(workplan.workplan_affected_bike_id),
                           workplan.workplan_description,
                           workplan.completion_date,
                           workplan.completion_notes,
                           calculate_elapsed_days(workplan.due_date,
                                                  workplan.completion_date if workplan.completion_date
                                                  else get_formatted_datetime_now())[1],
                           generate_workplan_title(database_manager.read_component_names(workplan.workplan_affected_component_ids),
                                                   database_manager.read_bike_name(workplan.workplan_affected_bike_id),
                                                   workplan.workplan_description),
                           parse_checkbox_progress(workplan.workplan_description)) for workplan in database_manager.read_planned_workplans()]
        
        component_collection_names, component_collection_data = self.get_component_collection_mapping()

        payload = {"bikes_data": bikes_data,
                   "component_types_data": component_types_data,
                   "bike_component_data": bike_component_data,
                   "all_components_data": all_components_data,
                   "bike_name": database_manager.read_bike_name(bike_component.bike_id),
                   "component_history_data": component_history_data,
                   "service_history_data": service_history_data,
                   "days_since_service": days_since_service,
                   "open_incidents": open_incidents,
                   "incident_reports_data": incident_reports_data,
                   "planned_workplans": planned_workplans,
                   "workplans_data": workplans_data,
                   "component_collection_names": component_collection_names,
                   "component_collection_data": component_collection_data}

        return payload

    def calculate_collection_status(self, component_ids, collection_bike_id=None):
        """Calculate status flags for a collection based on its components."""
        retired_count = 0
        installed_count = 0
        not_installed_count = 0
        bike_ids_of_installed = set()

        for component_id in component_ids:
            component = database_manager.read_component(component_id)
            if not component:
                continue

            if component.installation_status == "Retired":
                retired_count += 1
            elif component.installation_status == "Installed":
                installed_count += 1
                if component.bike_id:
                    bike_ids_of_installed.add(component.bike_id)
            elif component.installation_status == "Not installed":
                not_installed_count += 1

        is_empty = len(component_ids) == 0
        has_retired = retired_count > 0
        has_mixed_statuses = (installed_count > 0 and not_installed_count > 0)
        has_different_bikes = len(bike_ids_of_installed) > 1

        actual_component_bike_id = list(bike_ids_of_installed)[0] if len(bike_ids_of_installed) == 1 else None

        collection_bike_mismatch = False
        if collection_bike_id:
            if len(bike_ids_of_installed) > 0:
                collection_bike_mismatch = collection_bike_id not in bike_ids_of_installed
            else:
                collection_bike_mismatch = True
        elif len(bike_ids_of_installed) > 0:
            collection_bike_mismatch = True

        can_display_bike = (not is_empty and
                            not has_retired and
                            not has_mixed_statuses and
                            not has_different_bikes and
                            not collection_bike_mismatch)

        blocks_operations = (is_empty or
                             has_retired or
                             has_mixed_statuses or
                             has_different_bikes)

        if is_empty:
            status_string = 'no_components'
        elif blocks_operations:
            status_string = 'needs_attention'
        else:
            status_string = 'healthy'

        bike_names_list = []
        for bike_id in bike_ids_of_installed:
            bike_name = database_manager.read_bike_name(bike_id)
            if bike_name:
                bike_names_list.append(bike_name)

        actual_component_bike_name = None
        if actual_component_bike_id:
            actual_component_bike_name = database_manager.read_bike_name(actual_component_bike_id)

        return {'is_empty': is_empty,
                'has_retired': has_retired,
                'has_mixed_statuses': has_mixed_statuses,
                'has_different_bikes': has_different_bikes,
                'collection_bike_mismatch': collection_bike_mismatch,
                'blocks_operations': blocks_operations,
                'can_display_bike': can_display_bike,
                'retired_count': retired_count,
                'installed_count': installed_count,
                'not_installed_count': not_installed_count,
                'bike_count': len(bike_ids_of_installed),
                'bike_names_list': bike_names_list,
                'actual_component_bike_id': actual_component_bike_id,
                'actual_component_bike_name': actual_component_bike_name,
                'status': status_string}

    def get_component_collection_mapping(self):
        """Method to create component-to-collection mapping dictionaries"""
        component_collection_names = {}
        component_collection_data = {}
        collections = database_manager.read_all_collections()

        for collection in collections:
            component_ids = json.loads(collection.components) if collection.components else []
            for component_id in component_ids:
                component_collection_names[component_id] = collection.collection_name
                component_collection_data[component_id] = (collection.collection_id,
                                                           collection.collection_name,
                                                           collection.components,
                                                           collection.bike_id,
                                                           collection.comment,
                                                           collection.updated_date)

        return component_collection_names, component_collection_data

    def get_all_collections(self):
        """Method to produce payload for displaying table of all collections"""
        all_collections = []
        collections = database_manager.read_all_collections()

        for collection in collections:
            component_ids = json.loads(collection.components) if collection.components else []

            component_details = []
            for component_id in component_ids:
                component = database_manager.read_component(component_id)
                component_details.append({'id': component_id,
                                          'name': component.component_name})

            status_info = self.calculate_collection_status(component_ids, collection.bike_id)

            bike_name = None

            if collection.bike_id:
                bike = database_manager.read_single_bike(collection.bike_id)
                bike_name = bike.bike_name if bike else None

            collection_data = (collection.collection_id,
                               collection.collection_name,
                               bike_name,
                               collection.updated_date,
                               json.dumps(component_ids),
                               collection.bike_id,
                               collection.comment,
                               component_details,
                               status_info['status'],
                               status_info['collection_bike_mismatch'])

            all_collections.append(collection_data)

        return all_collections

    def get_collection_details(self, collection_id):
        """Method to produce payload for collection details page"""

        collection = database_manager.read_single_collection(collection_id)
        if not collection:
            logging.error(f"Collection not found: {collection_id}")
            return {"error": "Collection not found"}

        component_ids = json.loads(collection.components) if collection.components else []

        overview_payload = self.get_component_overview()

        filtered_components = [component for component in overview_payload['all_components_display_data']
                              if component[0] in component_ids]

        bike_name = database_manager.read_bike_name(collection.bike_id) if collection.bike_id else None

        collection_data = {'collection_id': collection.collection_id,
                           'collection_name': collection.collection_name,
                           'updated_date': collection.updated_date,
                           'bike_name': bike_name,
                           'bike_id': collection.bike_id,
                           'component_count': len(component_ids),
                           'comment': collection.comment,
                           'components': json.dumps(component_ids)}

        warnings = self.calculate_collection_status(component_ids, collection.bike_id)

        overview_payload['collection_data'] = collection_data
        overview_payload['all_components_display_data'] = filtered_components
        overview_payload['warnings'] = warnings

        return overview_payload

    def get_incident_reports(self):
        """Method to produce payload for page incident reports"""
        all_components_data = database_manager.read_all_components()

        bikes = database_manager.read_bikes()
        bikes_data = get_formatted_bikes_list(bikes)

        incident_reports_data = [(incident.incident_id,
                                  incident.incident_date,
                                  incident.incident_status,
                                  incident.incident_severity,
                                  parse_json_string(incident.incident_affected_component_ids),
                                  database_manager.read_component_names(incident.incident_affected_component_ids),
                                  incident.incident_affected_bike_id,
                                  database_manager.read_bike_name(incident.incident_affected_bike_id),
                                  incident.incident_description,
                                  incident.resolution_date,
                                  incident.resolution_notes,
                                  calculate_elapsed_days(incident.incident_date,
                                                         incident.resolution_date if incident.resolution_date
                                                         else get_formatted_datetime_now())[1]) for incident in database_manager.read_all_incidents()]

        payload = {"all_components_data": all_components_data,
                   "bikes_data": bikes_data,
                   "incident_reports_data": incident_reports_data}

        return payload
    
    def process_incidents(self, incidents):
        """Method to build dictionaries of bike and component ids referenced in received incidents"""

        bike_incidents = {}
        component_incidents = {}

        if incidents:
            for incident in incidents:
                incident_id = incident.incident_id

                if incident.incident_affected_bike_id:
                    bike_id = incident.incident_affected_bike_id

                    if bike_id not in bike_incidents:
                        bike_incidents[bike_id] = {
                            "incident_count": 0,
                            "incident_ids": []
                        }

                    if incident_id not in bike_incidents[bike_id]["incident_ids"]:
                        bike_incidents[bike_id]["incident_count"] += 1
                        bike_incidents[bike_id]["incident_ids"].append(incident_id)

                if incident.incident_affected_component_ids:
                    component_ids = json.loads(incident.incident_affected_component_ids)

                    for component_id in component_ids:
                        if component_id not in component_incidents:
                            component_incidents[component_id] = {"incident_count": 0}

                        component_incidents[component_id]["incident_count"] += 1

                        component = database_manager.read_component(component_id)
                        if component and component.installation_status != "Not installed" and component.bike_id:
                            bike_id = component.bike_id

                            if bike_id not in bike_incidents:
                                bike_incidents[bike_id] = {"incident_count": 0,
                                                           "incident_ids": []}
                            
                            if incident_id not in bike_incidents[bike_id]["incident_ids"]:
                                bike_incidents[bike_id]["incident_count"] += 1
                                bike_incidents[bike_id]["incident_ids"].append(incident_id)

        return {"bike_incidents": bike_incidents,
                "component_incidents": component_incidents}

    def get_workplans(self):
        """Method to produce payload for page workplans"""
        all_components_data = database_manager.read_all_components()

        bikes = database_manager.read_bikes()
        bikes_data = get_formatted_bikes_list(bikes)

        workplans_data = [(workplan.workplan_id,
                           workplan.due_date,
                           workplan.workplan_status,
                           workplan.workplan_size,
                           parse_json_string(workplan.workplan_affected_component_ids),
                           database_manager.read_component_names(workplan.workplan_affected_component_ids),
                           workplan.workplan_affected_bike_id,
                           database_manager.read_bike_name(workplan.workplan_affected_bike_id),
                           workplan.workplan_description,
                           workplan.completion_date,
                           workplan.completion_notes,
                           calculate_elapsed_days(workplan.due_date,
                                                  workplan.completion_date if workplan.completion_date
                                                  else get_formatted_datetime_now())[1],
                           parse_checkbox_progress(workplan.workplan_description)) for workplan in database_manager.read_all_workplans()]

        payload = {"all_components_data": all_components_data,
                   "bikes_data": bikes_data,
                   "workplans_data": workplans_data}

        return payload
    
    def process_workplans(self, workplans):
        """Method to build dictionaries of bike and component ids referenced in received workplans"""

        bike_workplans = {}
        component_workplans = {}

        if workplans:
            for workplan in workplans:
                workplan_id = workplan.workplan_id

                if workplan.workplan_affected_bike_id:
                    bike_id = workplan.workplan_affected_bike_id

                    if bike_id not in bike_workplans:
                        bike_workplans[bike_id] = {
                            "workplan_count": 0,
                            "workplan_ids": []
                        }

                    if workplan_id not in bike_workplans[bike_id]["workplan_ids"]:
                        bike_workplans[bike_id]["workplan_count"] += 1
                        bike_workplans[bike_id]["workplan_ids"].append(workplan_id)

                if workplan.workplan_affected_component_ids:
                    component_ids = json.loads(workplan.workplan_affected_component_ids)

                    for component_id in component_ids:
                        if component_id not in component_workplans:
                            component_workplans[component_id] = {"workplan_count": 0}

                        component_workplans[component_id]["workplan_count"] += 1

                        component = database_manager.read_component(component_id)
                        if component and component.installation_status != "Not installed" and component.bike_id:
                            bike_id = component.bike_id

                            if bike_id not in bike_workplans:
                                bike_workplans[bike_id] = {"workplan_count": 0,
                                                           "workplan_ids": []}
                            
                            if workplan_id not in bike_workplans[bike_id]["workplan_ids"]:
                                bike_workplans[bike_id]["workplan_count"] += 1
                                bike_workplans[bike_id]["workplan_ids"].append(workplan_id)

        return {"bike_workplans": bike_workplans,
                "component_workplans": component_workplans}

    def get_component_types(self):
        """Method to produce payload for page component types"""
        payload = {"component_types": database_manager.read_all_component_types()}

        return payload

    async def update_rides_bulk(self, mode):
        """Method to create or update ride data in bulk to database"""
        logging.info(f"Retrieving rides from Strava. Mode set to: {mode}.")
        await strava.get_rides(mode)
        logging.debug(f'There are {len(strava.payload_rides)} rides in the list.')

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
        logging.debug(f"Updated distance for component {component.component_name}. New total distance: {total_distance}.")

        if not history_records:
            logging.warning(f"Component {component.component_name} has no installation records. Using alternate method to set lifetime and service status")
            success, message = self.update_component_lifetime_service_alternate("update",
                                                                                component_id,
                                                                                component.lifetime_expected,
                                                                                component.service_interval,
                                                                                None)

            if success:
                logging.debug(message)
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
            logging.debug(f"Component distance update successful: {message}")
        else:
            logging.error(f"Component distance update failed: {message}")

        return success, message

    def update_component_lifetime_status(self, component):
        """Method to update component table with lifetime status"""
        logging.debug(f"Updating lifetime status for component {component.component_name}.")

        distance_status = "Not defined"
        days_status = "Not defined"
        lifetime_remaining = None
        lifetime_remaining_days = None

        if component.lifetime_expected:
            lifetime_remaining = component.lifetime_expected - component.component_distance
            distance_status = self.compute_component_status("lifetime",
                                                            lifetime_remaining,
                                                            component.threshold_km)

        if component.lifetime_expected_days:
            oldest_record = database_manager.read_oldest_history_record(component.component_id)
            if oldest_record:
                first_install_date = oldest_record.updated_date

                if component.installation_status == "Retired":
                    end_date = component.updated_date
                else:
                    end_date = get_formatted_datetime_now()

                success, age_days = calculate_elapsed_days(first_install_date, end_date)
                if success:
                    lifetime_remaining_days = component.lifetime_expected_days - age_days
                    days_status = self.compute_component_status("lifetime",
                                                                lifetime_remaining_days,
                                                                component.threshold_days)

        final_status = self.determine_worst_status(distance_status, days_status)

        success, message = database_manager.write_component_lifetime_status(component,
                                                                            lifetime_remaining,
                                                                            final_status,
                                                                            lifetime_remaining_days)

        if success:
            logging.debug(f"Component lifetime status update successful: {message}")
        else:
            logging.error(f"Component lifetime status update failed: {message}")

        return success, message

    def update_component_service_status(self, component):
        """Method to update component table with service status"""
        logging.debug(f"Updating service status for component {component.component_name}.")
        
        if component.service_interval:
            latest_service_record = database_manager.read_latest_service_record(component.component_id)
            latest_history_record = database_manager.read_latest_history_record(component.component_id)

            if component.installation_status == "Installed":
                if latest_service_record is None:
                    logging.debug(f'No service record found for component {component.component_name}. Using distance from installation log and querying distance from installation date to today.')
                    distance_since_service = latest_history_record.distance_marker
                    matching_rides = database_manager.read_matching_rides(component.bike_id, latest_history_record.updated_date)
                    distance_since_service += sum(ride.ride_distance for ride in matching_rides)

                elif latest_service_record:
                    logging.debug(f'Service record found for component {component.component_name}. Processing installation periods since service.')
                    
                    history_records = database_manager.read_subset_component_history(component.component_id)
                    sorted_history = sorted(history_records, key=lambda x: x.updated_date)
                    
                    distance_since_service = 0
                    
                    logging.debug(f"Finding installation status at time of service for component {component.component_name}.")
                    service_time_status = next((record for record in reversed(sorted_history) 
                                                if record.updated_date <= latest_service_record.service_date),
                                                None)

                    logging.debug(f"Finding relevant bikes since service date for component {component.component_name}.")
                    relevant_bikes = {record.bike_id for record in sorted_history 
                                    if record.updated_date >= latest_service_record.service_date
                                    and record.bike_id is not None}
                    
                    logging.debug(f"Building list of relevant bikes to calculate distance to next service")
                    if (component.installation_status == "Installed" and
                        (not sorted_history or
                        latest_service_record.service_date >= sorted_history[-1].updated_date)):
                        relevant_bikes.add(component.bike_id)
                    
                    logging.debug(f"Found {len(relevant_bikes)} bikes to check for rides to calculate distance to next service")
                    
                    logging.debug(f"Querying rides for all relevant bikes to calculate distance to next service")
                    all_rides = []
                    for bike_id in relevant_bikes:
                        matching_rides = database_manager.read_matching_rides(bike_id, latest_service_record.service_date)
                        all_rides.extend(matching_rides)

                    all_rides.sort(key=lambda x: x.record_time)

                    logging.debug(f"Filtering rides and installation status to only count rides when component was installed")
                    for ride in all_rides:
                        current_status = next(
                            (record for record in reversed(sorted_history)
                            if record.updated_date <= ride.record_time),
                            service_time_status)

                        if (current_status and 
                            current_status.update_reason == "Installed" and
                            current_status.bike_id == ride.bike_id):
                            distance_since_service += ride.ride_distance
                            logging.debug(f"Ride on {ride.record_time} of {ride.ride_distance} km from bike {ride.bike_id} is relevant for calculating distance to next service")    
                
            elif component.installation_status != "Installed":
                if latest_service_record is None:
                    logging.debug(f'Component {component.component_name} has been uninstalled and there are no previous services. Setting distance since service to distance at the time of uninstallation.')
                    distance_since_service = latest_history_record.distance_marker

                elif latest_service_record:
                    if latest_service_record.service_date >= component.updated_date:
                        logging.debug(f'Component {component.component_name} has been serviced after or at uninstall. Setting distance since service to 0.')
                        distance_since_service = 0

                    else:
                        logging.debug(f'Component {component.component_name} was serviced before uninstall. Processing installation periods from service to uninstall.')
                        
                        history_records = database_manager.read_subset_component_history(component.component_id)
                        sorted_history = sorted(history_records, key=lambda x: x.updated_date)
                        
                        distance_since_service = 0

                        logging.debug(f"Finding installation status at time of service for component {component.component_name}.")
                        service_time_status = next((record for record in reversed(sorted_history) 
                                                if record.updated_date <= latest_service_record.service_date),
                                                None)

                        logging.debug(f"Finding relevant bikes between service date and uninstall date for component {component.component_name}.")
                        relevant_bikes = {record.bike_id for record in sorted_history 
                                        if (record.updated_date >= latest_service_record.service_date and 
                                            record.updated_date <= component.updated_date and
                                            record.bike_id is not None)}
                        
                        logging.debug(f"Found {len(relevant_bikes)} bikes to check for rides to calculate distance to next service")
                        
                        logging.debug(f"Querying rides for all relevant bikes to calculate distance to next service")
                        all_rides = []
                        for bike_id in relevant_bikes:
                            matching_rides = database_manager.read_matching_rides(bike_id, latest_service_record.service_date)
                            all_rides.extend(matching_rides)
                        
                        all_rides.sort(key=lambda x: x.record_time)

                        logging.debug(f"Filtering rides and installation status to only count rides when component was installed and before uninstall date")
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
                                logging.debug(f"Ride on {ride.record_time} of {ride.ride_distance} km from bike {ride.bike_id} is relevant for calculating distance to next service")

            service_next = component.service_interval - distance_since_service
            distance_status = self.compute_component_status("service", service_next, component.threshold_km)
        else:
            service_next = None
            distance_status = "Not defined"

        days_status = "Not defined"
        service_next_days = None

        if component.service_interval_days:
            latest_service_record = database_manager.read_latest_service_record(component.component_id)

            if latest_service_record:
                last_service_date = latest_service_record.service_date
            else:
                oldest_record = database_manager.read_oldest_history_record(component.component_id)
                if oldest_record:
                    last_service_date = oldest_record.updated_date
                else:
                    last_service_date = None

            if last_service_date:
                if component.installation_status == "Retired":
                    end_date = component.updated_date
                else:
                    end_date = get_formatted_datetime_now()

                success, days_since_service = calculate_elapsed_days(last_service_date, end_date)
                if success:
                    service_next_days = component.service_interval_days - days_since_service
                    days_status = self.compute_component_status("service", service_next_days, component.threshold_days)

        final_status = self.determine_worst_status(distance_status, days_status)

        success, message = database_manager.write_component_service_status(component, service_next, final_status, service_next_days)

        if success:
            logging.debug(f"Component service status update successful: {message}")
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
                lifetime_status_distance = self.compute_component_status("lifetime",
                                                                         lifetime_remaining,
                                                                         component.threshold_km)
            else:
                lifetime_remaining = None
                lifetime_status_distance = "Not defined"

            if component.lifetime_expected_days:
                oldest_history = database_manager.read_oldest_history_record(component_id)
                if oldest_history:
                    success, elapsed_days = calculate_elapsed_days(oldest_history.updated_date, get_formatted_datetime_now())
                    if success:
                        lifetime_remaining_days = component.lifetime_expected_days - elapsed_days
                    else:
                        logging.error(f"Failed to calculate elapsed days for component {component.component_name}")
                        lifetime_remaining_days = None
                else:
                    success, elapsed_days = calculate_elapsed_days(component.updated_date, get_formatted_datetime_now())
                    if success:
                        lifetime_remaining_days = component.lifetime_expected_days - elapsed_days
                    else:
                        logging.error(f"Failed to calculate elapsed days for component {component.component_name}")
                        lifetime_remaining_days = None

                if lifetime_remaining_days is not None:
                    lifetime_status_days = self.compute_component_status("lifetime",
                                                                         lifetime_remaining_days,
                                                                         component.threshold_days)
                else:
                    lifetime_status_days = "Not defined"
            else:
                lifetime_remaining_days = None
                lifetime_status_days = "Not defined"

            lifetime_status = self.determine_worst_status(lifetime_status_distance, lifetime_status_days)

            database_manager.write_component_lifetime_status(component,
                                                            lifetime_remaining,
                                                            lifetime_status,
                                                            lifetime_remaining_days)

            if service_interval:
                service_next = service_interval
                service_status_distance = self.compute_component_status("service",
                                                                        service_next,
                                                                        component.threshold_km)
            else:
                service_next = None
                service_status_distance = "Not defined"

            if component.service_interval_days:
                service_next_days = component.service_interval_days
                service_status_days = self.compute_component_status("service",
                                                                    service_next_days,
                                                                    component.threshold_days)
            else:
                service_next_days = None
                service_status_days = "Not defined"

            service_status = self.determine_worst_status(service_status_distance, service_status_days)

            database_manager.write_component_service_status(component,
                                                            service_next,
                                                            service_status,
                                                            service_next_days)

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
        
        logging.debug(f"Updating bike status for bike {bike.bike_name} with id {bike.bike_id}.")
        
        component_status = {"exceeded_max": 0,
                            "due_past_threshold": 0,
                            "ok": 0}

        count_installed = 0
        count_retired = 0

        if components.exists():
            for component in components:
                if component.installation_status == "Installed":
                    count_installed += 1
                    if component.lifetime_status == "Lifetime exceeded" or component.service_status == "Service interval exceeded":
                        component_status["exceeded_max"] += 1
                    elif component.lifetime_status == "Due for replacement" or component.service_status == "Due for service":
                        component_status["due_past_threshold"] += 1
                    elif component.lifetime_status == "OK" or component.service_status == "OK":
                        component_status["ok"] += 1

                if component.installation_status == "Retired":
                    count_retired += 1

            if component_status["exceeded_max"] > 0:
                service_status = "Components need attention"
            elif component_status["ok"] > 0:
                service_status = "All components healthy"
            elif all(value == 0 for value in component_status.values()) and count_installed > 0:
                service_status = "Maintenance not defined"
            elif count_installed == 0 and count_retired > 0:
                service_status = "No active components"
        
        else:
            service_status = "No components registered"
    
        logging.debug(f"New status for bike {bike.bike_name}: {service_status}")

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
                         threshold_km,
                         lifetime_expected_days,
                         service_interval_days,
                         threshold_days,
                         cost,
                         offset,
                         component_notes):
        """Method to create component"""
        try:
            component_bike_id = None if component_bike_id == 'None' or component_bike_id == '' else component_bike_id
            expected_lifetime = int(expected_lifetime) if expected_lifetime and expected_lifetime.isdigit() else None
            service_interval = int(service_interval) if service_interval and service_interval.isdigit() else None
            threshold_km = int(threshold_km) if threshold_km and threshold_km.isdigit() else None
            lifetime_expected_days = int(lifetime_expected_days) if lifetime_expected_days and lifetime_expected_days.isdigit() else None
            service_interval_days = int(service_interval_days) if service_interval_days and service_interval_days.isdigit() else None
            threshold_days = int(threshold_days) if threshold_days and threshold_days.isdigit() else None
            cost = int(cost) if cost and cost.isdigit() else None

            validation_success, validation_message = self.validate_threshold_configuration(expected_lifetime,
                                                                                           service_interval,
                                                                                           lifetime_expected_days,
                                                                                           service_interval_days,
                                                                                           threshold_km,
                                                                                           threshold_days)

            if not validation_success:
                logging.warning(f"Component creation validation failed: {validation_message}")
                return False, validation_message, None

            new_component_data = {"installation_status": component_installation_status,
                                  "updated_date": component_updated_date,
                                  "component_name": component_name,
                                  "component_type": component_type,
                                  "bike_id": component_bike_id,
                                  "lifetime_expected": expected_lifetime,
                                  "service_interval": service_interval,
                                  "threshold_km": threshold_km,
                                  "lifetime_expected_days": lifetime_expected_days,
                                  "service_interval_days": service_interval_days,
                                  "threshold_days": threshold_days,
                                  "cost": cost,
                                  "component_distance_offset": offset,
                                  "notes": component_notes}

            component_id = generate_unique_id()
            success, message = database_manager.write_component_details(component_id, new_component_data)

            if success:
                logging.info(message)
                if component_installation_status == "Installed":
                    success, message = self.create_history_record(component_id, component_installation_status, component_bike_id, component_updated_date)
                    if success:
                        logging.debug(message)
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
                                 threshold_km,
                                 lifetime_expected_days,
                                 service_interval_days,
                                 threshold_days,
                                 cost,
                                 offset,
                                 component_notes):
        """Method to update component details"""
        try:
            component_bike_id = None if component_bike_id == 'None' or component_bike_id == '' else component_bike_id
            expected_lifetime = int(expected_lifetime) if expected_lifetime and expected_lifetime.isdigit() else None
            service_interval = int(service_interval) if service_interval and service_interval.isdigit() else None
            threshold_km = int(threshold_km) if threshold_km and threshold_km.isdigit() else None
            lifetime_expected_days = int(lifetime_expected_days) if lifetime_expected_days and lifetime_expected_days.isdigit() else None
            service_interval_days = int(service_interval_days) if service_interval_days and service_interval_days.isdigit() else None
            threshold_days = int(threshold_days) if threshold_days and threshold_days.isdigit() else None
            cost = int(cost) if cost and cost.isdigit() else None

            validation_success, validation_message = self.validate_threshold_configuration(expected_lifetime,
                                                                                           service_interval,
                                                                                           lifetime_expected_days,
                                                                                           service_interval_days,
                                                                                           threshold_km,
                                                                                           threshold_days)

            if not validation_success:
                logging.warning(f"Component modification validation failed for {component_id}: {validation_message}")
                return False, validation_message, component_id

            new_component_data = {"installation_status": component_installation_status,
                                  "updated_date": component_updated_date,
                                  "component_name": component_name,
                                  "component_type": component_type,
                                  "bike_id": component_bike_id,
                                  "lifetime_expected": expected_lifetime,
                                  "service_interval": service_interval,
                                  "threshold_km": threshold_km,
                                  "lifetime_expected_days": lifetime_expected_days,
                                  "service_interval_days": service_interval_days,
                                  "threshold_days": threshold_days,
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
                            "bike_id": component_bike_id if component_bike_id else None,
                            "component_name": component.component_name,
                            "updated_date": component_updated_date,
                            "update_reason": installation_status,
                            "distance_marker": 0}
            
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
    
        logging.debug(f"Running general validation rules for history records: {history_id}.")
        
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
            logging.debug(f"Running validation rules for creation of history records: {history_id}.")

            oldest_history_record = database_manager.read_oldest_history_record(component.component_id)
            if oldest_history_record:
                if updated_date <= oldest_history_record.updated_date:
                    logging.warning(f"Date for new status cannot be at or before component creation date: {oldest_history_record.updated_date}. Component: {component.component_name}")
                    return False, f"Date for new status cannot be at or before component creation date: {oldest_history_record.updated_date}. Component: {component.component_name}"
            
            latest_history_record = database_manager.read_latest_history_record(component_id)
            if latest_history_record:
                if latest_history_record.update_reason == "Retired":
                    logging.warning(f"Status cannot be changed on a retired component: {component.component_name}")
                    return False, f"Status cannot be changed on a retired component: {component.component_name}"

                if updated_date <= latest_history_record.updated_date:
                    logging.warning(f"Component status changes must be done chronologically. Date for new status cannot be at or before date for the last status: {latest_history_record.updated_date}. Component: {component.component_name}")
                    return False, f"Component status changes must be done chronologically. Date for new status cannot be at or before date for the last status: {latest_history_record.updated_date}. Component: {component.component_name}"

                if latest_history_record.update_reason == installation_status:
                    logging.warning(f"Component status for {component.component_name} is already set to: {installation_status}.")
                    return False, f"Component status for {component.component_name} is already set to: {installation_status}."

            if not latest_history_record and installation_status == "Not installed":
                logging.warning(f"Component {component.component_name} is not installed and can therefore not be set to 'Not installed'.")
                return False, f"Component {component.component_name} is not installed and can therefore not be set to 'Not installed'."
            
            if installation_status == "Installed" and (component_bike_id is None or component_bike_id == ""):
                logging.warning(f"Status cannot be set to Installed without specifying bike. {component.component_name} is currently not assigned to a bike.")
                return False, f"Status cannot be set to Installed without specifying bike. {component.component_name} is currently not assigned to a bike."
            
            lastest_service_record = database_manager.read_latest_service_record(component_id)
            if lastest_service_record:
                if updated_date <= lastest_service_record.service_date and installation_status == "Retired":
                    logging.warning(f"A retired component cannot be serviced. Set retire date after latest service date: {lastest_service_record.service_date}")
                    return False, f"A retired component cannot be serviced. Set retire date after latest service date: {lastest_service_record.service_date}"
       
        if mode == "edit history":
            logging.debug(f"Running validation rules for editing of history records: {history_id}.")

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
            
        logging.debug(f"Validation of history record for {component.component_name} passed")
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
                        logging.debug(f'Timespan for historic distance query: start date {previous_record.updated_date} stop date {record.updated_date}.')
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
                logging.debug(f'Calculating additional distance since last history record: start date {latest_history_record.updated_date} stop date {datetime.now().strftime("%Y-%m-%d %H:%M")}')
                additional_distance = database_manager.read_sum_distance_subset_rides(latest_history_record.bike_id,
                                                                                      latest_history_record.updated_date,
                                                                                      datetime.now().strftime("%Y-%m-%d %H:%M"))
                current_distance += additional_distance
                logging.debug(f'Total distance: {current_distance} (History: {latest_history_record.distance_marker}, Additional: {additional_distance})')
                
            self.update_component_distance(component_id, current_distance)

            if success:
                latest_history = database_manager.read_latest_history_record(component_id)
                
                component_data = {
                    "installation_status": latest_history.update_reason,
                    "updated_date": latest_history.updated_date,
                    "component_name": component.component_name,
                    "component_type": component.component_type,
                    "bike_id": None if latest_history.update_reason == "Not installed" else latest_history.bike_id,
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

            return True, f"Successfully processed history records and related services for {component.component_name}"

        except Exception as error:
            logging.error(f"An error occurred processing history records for component {component.component_name}: {str(error)}")
            return False, f"Error processing history records for {component.component_name}: {str(error)}"

    def quick_swap_orchestrator(self,
                                old_component_id,
                                fate,
                                swap_date,
                                new_component_id,
                                new_component_data):
        """Method to orchestrate swap of one component with another"""
        try:
            logging.info(f"Quick swap: Starting swap operation for component {old_component_id}")

            old_component = database_manager.read_component(old_component_id)
            if not old_component:
                logging.error(f"Quick swap failed: Old component not found: {old_component_id}")
                return False, f"Quick swap failed: The component to be swapped (ID: {old_component_id}) was not found."

            logging.debug(f"Quick swap: Old component validated: {old_component.component_name}")

            is_valid, validation_message = self.validate_quick_swap(old_component,
                                                                    fate,
                                                                    new_component_id,
                                                                    new_component_data)

            if not is_valid:
                logging.error(f"Quick swap validation failed for {old_component.component_name}: {validation_message}")
                return False, validation_message

            bike_id = old_component.bike_id
            bike = database_manager.read_single_bike(bike_id)
            logging.debug(f"Quick swap: Validation passed. Bike: {bike.bike_name}, Fate: {fate}")

            if new_component_data:
                logging.debug(f"Quick swap: Creating new component '{new_component_data['component_name']}' of type {new_component_data['component_type']}")

                success, message, new_component_id = self.create_component(component_id=None,
                                                                           component_installation_status="Not installed",
                                                                           component_updated_date=swap_date,
                                                                           component_name=new_component_data["component_name"],
                                                                           component_type=new_component_data["component_type"],
                                                                           component_bike_id=None,
                                                                           expected_lifetime=new_component_data["lifetime_expected"],
                                                                           service_interval=new_component_data["service_interval"],
                                                                           threshold_km=new_component_data.get("threshold_km"),
                                                                           lifetime_expected_days=new_component_data.get("lifetime_expected_days"),
                                                                           service_interval_days=new_component_data.get("service_interval_days"),
                                                                           threshold_days=new_component_data.get("threshold_days"),
                                                                           cost=new_component_data["cost"],
                                                                           offset=new_component_data["offset"],
                                                                           component_notes=new_component_data["notes"])

                if success == False:
                    logging.error(f"Quick swap failed: Failed to create new component '{new_component_data['component_name']}': {message}")
                    return False, f"Quick swap failed: Could not create new component. {message}"

                elif success == "warning":
                    logging.warning(f"Quick swap: New component created with warning: {message}")

                logging.debug(f"Quick swap: New component created successfully with ID {new_component_id}")
                new_component = database_manager.read_component(new_component_id)
            
            else:
                new_component = database_manager.read_component(new_component_id)
                logging.debug(f"Quick swap: Using existing component: {new_component.component_name}")

            logging.debug(f"Quick swap: Setting {old_component.component_name} to '{fate}'")

            success, message = self.create_history_record(component_id=old_component_id,
                                                          installation_status=fate,
                                                          component_bike_id=bike_id,
                                                          component_updated_date=swap_date)

            if not success:
                logging.error(f"Quick swap failed: Could not update old component status: {message}")
                if new_component_data:
                    logging.warning(f"Quick swap partial failure: New component '{new_component.component_name}' (ID: {new_component_id}) was created with status 'Not installed'. Old component '{old_component.component_name}' (ID: {old_component_id}) could not be updated to '{fate}'. Manual fix required: {message}")
                    return False, f"Quick swap partially failed: New component '{new_component.component_name}' was created but remains 'Not installed'. Old component '{old_component.component_name}' remains 'Installed' on {bike.bike_name}. Manual fix required: {message}"
                else:
                    return False, f"Quick swap failed: Could not update '{old_component.component_name}' to '{fate}'. Existing component '{new_component.component_name}' was not touched. {message}"

            logging.debug(f"Quick swap: Old component status updated successfully")
            logging.debug(f"Quick swap: Installing {new_component.component_name} on {bike.bike_name}")

            success, message = self.create_history_record(component_id=new_component_id,
                                                          installation_status="Installed",
                                                          component_bike_id=bike_id,
                                                          component_updated_date=swap_date)

            if not success:
                logging.error(f"Quick swap failed: Could not install new component: {message}")
                logging.warning(f"Quick swap partial failure: {old_component.component_name} is now '{fate}' but {new_component.component_name} could not be installed")
                return False, f"Quick swap partially failed: '{old_component.component_name}' is now '{fate}', but '{new_component.component_name}' could not be installed on {bike.bike_name}. Manual fix required: {message}"

            old_component_refreshed = database_manager.read_component(old_component_id)
            new_component_refreshed = database_manager.read_component(new_component_id)

            success_message = f"Component swapped successfully: {old_component_refreshed.component_name} set to {fate}. {new_component_refreshed.component_name} installed on {bike.bike_name}"
            logging.info(f"Quick swap completed successfully: {success_message}")

            return True, success_message

        except Exception as error:
            logging.error(f"Quick swap operation failed with unexpected error: {str(error)}")
            return False, f"Quick swap failed due to an unexpected error: {str(error)}. Components may be in an inconsistent state. Please check component statuses manually and review the application log for details."

    def validate_quick_swap(self, old_component, fate, new_component_id, new_component_data):
        """Method to validate quick swap operation"""
        if old_component.installation_status != "Installed":
            return False, "Component must be installed to be swapped"

        if fate not in ["Not installed", "Retired"]:
            return False, "Invalid fate selection"

        if not old_component.bike_id:
            return False, "Old component has no bike assignment"

        if new_component_id:
            new_component = database_manager.read_component(new_component_id)
            if not new_component:
                return False, "Selected component not found"

            if new_component.installation_status != "Not installed":
                return False, "Selected component is not available for installation"

            if old_component.component_type != new_component.component_type:
                return False, f"Components must be of the same type. Cannot swap {old_component.component_type} with {new_component.component_type}."

        elif new_component_data:
            if not new_component_data.get("component_name"):
                return False, "Component name is required"

            if new_component_data.get("component_type") != old_component.component_type:
                return False, f"New component type must match old component type: {old_component.component_type}"

        else:
            return False, "Must provide either new_component_id or new_component_data"

        return True, ""

    def create_collection(self, collection_name, components, comment):
        """Method to create collection"""
        try:
            collection_id = generate_unique_id()
            comment = comment if comment else None

            collection_status = self.calculate_collection_status(components if components else [])
            calculated_bike_id = collection_status.get('actual_component_bike_id')

            collection_data = {"collection_id": collection_id,
                             "collection_name": collection_name,
                             "components": json.dumps(components) if components else None,
                             "bike_id": calculated_bike_id,
                             "comment": comment,
                             "sub_collections": None,
                             "updated_date": None}

            success, message = database_manager.write_collection(collection_data)

            if success:
                logging.info(f"Creation of collection successful: {message}")
                logging.debug(f"Collection {collection_id} bike_id set to {calculated_bike_id} based on component states")
                return success, message, collection_id
            else:
                logging.error(f"Creation of collection failed: {message}")
                return success, message, None

        except Exception as error:
            logging.error(f"Error creating collection with id {collection_id}: {str(error)}")
            return False, f"Error creating collection with id {collection_id}: {str(error)}", None
        
    def update_collection(self, collection_id, collection_name, components, comment):
        """Method to update collection"""
        try:
            comment = comment if comment else None

            collection_status = self.calculate_collection_status(components if components else [])
            calculated_bike_id = collection_status.get('actual_component_bike_id')

            collection_data = {"collection_id": collection_id,
                             "collection_name": collection_name,
                             "components": json.dumps(components) if components else None,
                             "bike_id": calculated_bike_id,
                             "comment": comment}

            success, message = database_manager.write_collection(collection_data)

            if success:
                logging.info(f"Update of collection successful: {message}")
                logging.debug(f"Collection {collection_id} bike_id set to {calculated_bike_id} based on component states")
            else:
                logging.error(f"Update of collection failed: {message}")

            return success, message

        except Exception as error:
            logging.error(f"Error updating collection with id {collection_id}: {str(error)}")
            return False, f"Error updating collection with id {collection_id}: {str(error)}"

    def validate_collection(self, collection_id, component_ids, bike_id, new_status=None):
        """Method to validate collections before allowing bulk operations"""
        logging.debug(f"Running validation rules for collection: {collection_id}")
        
        current_collection = database_manager.read_single_collection(collection_id)
        if not current_collection:
            logging.warning(f"Collection not found: {collection_id}")
            return False, f"Collection not found: {collection_id}"
        
        if component_ids:
            installed_components = []
            not_installed_components = []
            retired_components = []
            component_bikes = set()

            for component_id in component_ids:
                component = database_manager.read_component(component_id)
                if not component:
                    logging.warning(f"Component not found: {component_id}")
                    return False, f"Operation cancelled: Component {component_id} not found. No changes have been made."

                existing_collection = database_manager.read_collection_by_component(component_id)
                if existing_collection and existing_collection.collection_id != collection_id:
                    logging.warning(f"Component {component.component_name} already belongs to collection {existing_collection.collection_name}")
                    return False, f"Operation cancelled: Component {component.component_name} already belongs to collection {existing_collection.collection_name}. Remove it from that collection first. No changes have been made."

                if component.installation_status == "Installed":
                    installed_components.append(component)
                    if component.bike_id:
                        component_bikes.add(component.bike_id)
                elif component.installation_status == "Not installed":
                    not_installed_components.append(component)
                elif component.installation_status == "Retired":
                    retired_components.append(component)

            if retired_components:
                retired_names = [comp.component_name for comp in retired_components]
                logging.warning(f"Bulk operations not allowed on collections with retired components: {', '.join(retired_names)}")
                return False, f"Operation cancelled: Bulk operations cannot be performed on collections containing retired components. Retired components: {', '.join(retired_names)}. Remove retired components from this collection first. No changes have been made."

            if installed_components and not_installed_components:
                logging.warning(f"Collection cannot contain both installed and not-installed components. No changes have been made.")
                return False, f"Operation cancelled: Collection cannot contain both installed and not-installed components. Select components with the same installation status. No changes have been made."
            
            if installed_components and len(component_bikes) > 1:
                bike_names = [database_manager.read_single_bike(bike_id).bike_name for bike_id in component_bikes if database_manager.read_single_bike(bike_id)]
                logging.warning(f"All installed components in a collection must be on the same bike. Found components on: {', '.join(bike_names)}")
                return False, f"Operation cancelled: All installed components in a collection must be on the same bike. Found components on bikes: {', '.join(bike_names)}. Select components from the same bike. No changes have been made."

            if new_status == "Installed" and not bike_id:
                logging.warning(f"Collections being changed to Installed status must be assigned to a bike")
                return False, f"Operation cancelled: Collections being changed to 'Installed' status must be assigned to a bike. Assign this collection to a bike. No changes have been made."
        
        if bike_id:
            bike = database_manager.read_single_bike(bike_id)
            if not bike:
                logging.warning(f"Bike not found: {bike_id}")
                return False, f"Bike not found: {bike_id}"
        
        logging.debug(f"Validation of collection {collection_id} passed")
        return True, f"Validation of collection {collection_id} passed"
    
    def change_collection_status(self, collection_id, new_status, updated_date, bike_id):
        """Method to change status of all components in a collection"""
        try:
            logging.info(f"Starting collection status change for collection {collection_id} to '{new_status}'")

            collection = database_manager.read_single_collection(collection_id)
            if not collection:
                return False, f"Collection {collection_id} not found"

            component_ids = json.loads(collection.components) if collection.components else []

            if not component_ids:
                return False, "No components found in collection"

            is_valid, validation_message = self.validate_collection(collection_id, component_ids, bike_id, new_status)
            if not is_valid:
                logging.warning(f"Collection validation failed: {validation_message}")
                return False, validation_message

            success_count = 0
            successful_components = []
            failed_components = []
            
            for component_id in component_ids:
                component = database_manager.read_component(component_id)
                component_name = component.component_name if component else f"Component {component_id}"

                success, message = self.create_history_record(
                    component_id=component_id,
                    installation_status=new_status,
                    component_bike_id=bike_id,
                    component_updated_date=updated_date)

                if success:
                    success_count += 1
                    successful_components.append(component_name)
                else:
                    failed_components.append({"name": component_name, "error": message})
                    logging.error(f"Failed to update component {component_id}: {message}")

            if success_count > 0:
                try:
                    collection_status = self.calculate_collection_status(component_ids)
                    calculated_bike_id = collection_status.get('actual_component_bike_id')

                    collection_update_data = {
                        "collection_id": collection_id,
                        "collection_name": collection.collection_name,
                        "components": collection.components,
                        "bike_id": calculated_bike_id,
                        "comment": collection.comment,
                        "updated_date": updated_date}

                    database_manager.write_collection(collection_update_data)

                    logging.debug(f"Collection {collection_id} bike_id set to {calculated_bike_id} based on component states")
                    logging.debug(f"Collection {collection_id} last updated date set to {updated_date}")

                except Exception as error:
                    logging.error(f"Collection update failed entirely. Last updated date not chaged. Error: {str(error)}")

            total_count = len(component_ids)

            if success_count == total_count:
                message = {"type": "success",
                           "summary": f"Successfully updated status for all {success_count} components",
                           "total_count": total_count,
                           "success_count": success_count,
                           "successful_components": successful_components,
                           "failed_components": []}
                
                logging.info(f"Collection status change: all {success_count} components succeeded")
                return True, message

            elif success_count > 0:
                message = {"type": "partial_failure",
                           "summary": f"Status update failed - only {success_count} of {total_count} components were updated",
                           "total_count": total_count,
                           "success_count": success_count,
                           "successful_components": successful_components,
                           "failed_components": failed_components}
                
                logging.warning(f"Collection status change failed: {success_count} / {total_count} components succeeded")
                return False, message

            else:
                message = {"type": "complete_failure",
                           "summary": "Failed to update any components in collection",
                           "total_count": total_count,
                           "success_count": 0,
                           "successful_components": [],
                           "failed_components": failed_components}
                
                logging.error("Collection status change: all components failed")
                return False, message

        except Exception as error:
            logging.error(f"Error changing collection status for {collection_id}: {str(error)}")
            return False, f"Error changing collection status for {collection_id}: {str(error)}"
    
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

        logging.debug(f"Running validation rules for service records: {service_id}.")
        
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
        
        logging.debug(f"Validation of service record for {component.component_name} passed")
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

        logging.debug(f"Consolidating and sorting all services for component {component.component_name}")
        all_services = [service for service in all_services if service.service_id != service_id]
        all_services.append(type('Service', (), current_service_data)())
        all_services.sort(key=lambda x: x.service_date)

        logging.debug(f"Iterating over all services for component {component.component_name} to update distance markers and bike ids")
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
                        logging.debug(f"Calculating distance for installation period for first service record: {current_installation.updated_date} to {record.updated_date}")
                        period_distance = database_manager.read_sum_distance_subset_rides(current_installation.bike_id,
                                                                                          current_installation.updated_date,
                                                                                          record.updated_date)
                        accumulated_distance += period_distance
                        logging.debug(f"Added {period_distance} km from bike {current_installation.bike_id}")
                        current_installation = None

                logging.debug(f"Processing final installation period for first service record")
                if current_installation:
                    period_distance = database_manager.read_sum_distance_subset_rides(current_installation.bike_id,
                                                                                      current_installation.updated_date,
                                                                                      service_date)
                    accumulated_distance += period_distance
                    logging.debug(f"Added final period of {period_distance} km from bike {current_installation.bike_id} for first service record")

                new_service_distance = accumulated_distance

            else:
                logging.debug(f"Processing subsequent service records, using service dates to calculate distance")
                previous_service_date = all_services[index-1].service_date
                current_service_date = service.service_date
                
                accumulated_distance = 0
                current_installation = None
                
                initial_status = next(record for record in reversed(sorted_history)
                                      if record.updated_date <= previous_service_date)
                
                if initial_status.update_reason == "Installed":
                    current_installation = initial_status
                
                logging.debug(f"Processing installation changes within window {previous_service_date} to {current_service_date}")
                for record in sorted_history:
                    if record.updated_date <= previous_service_date:
                        logging.debug(f"Record {record.history_id} dated {record.updated_date} outside window, skipping")
                        continue
                    if record.updated_date > current_service_date:
                        logging.debug(f"Record {record.history_id} dated {record.updated_date} inside window, processing")
                        break
                    
                    if record.update_reason == "Installed":
                        current_installation = record
                    elif record.update_reason == "Not installed" and current_installation:
                        logging.debug(f"Calculating distance for the installation period: {current_installation.updated_date} to {record.updated_date}")
                        period_distance = database_manager.read_sum_distance_subset_rides(
                            current_installation.bike_id,
                            max(current_installation.updated_date, previous_service_date),
                            record.updated_date)
                        accumulated_distance += period_distance
                        logging.debug(f"Added {period_distance} km from bike {current_installation.bike_id} ({current_installation.updated_date} to {record.updated_date})")
                        current_installation = None

                logging.debug("Processing final installation period at the end of window")
                if current_installation:
                    period_distance = database_manager.read_sum_distance_subset_rides(current_installation.bike_id,
                                                                                      max(current_installation.updated_date, previous_service_date),
                                                                                      current_service_date)
                    accumulated_distance += period_distance
                    logging.debug(f"Added final period of {period_distance} km from bike {current_installation.bike_id} ({current_installation.updated_date} to {current_service_date})")

                new_service_distance = accumulated_distance
                logging.debug(f"Total accumulated distance: {accumulated_distance} km")

            logging.debug(f"Setting bike_id based on component status at service time")
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

    def compute_component_status(self, mode, remaining_value, threshold_value):
        """Method to compute component status using threshold logic"""
        if threshold_value is None or remaining_value is None:
            return "Not defined"

        if remaining_value <= 0:
            if mode == "service":
                return "Service interval exceeded"
            elif mode == "lifetime":
                return "Lifetime exceeded"

        if 0 < remaining_value < threshold_value:
            if mode == "service":
                return "Due for service"
            elif mode == "lifetime":
                return "Due for replacement"

        if remaining_value >= threshold_value:
            return "OK"

        return "Not defined"

    def determine_trigger(self, distance_status, days_status):
        """Method to determine which factor triggered a warning status"""
        warning_statuses = ["Due for service",
                            "Service interval exceeded",
                            "Due for replacement",
                            "Lifetime exceeded"]

        distance_is_warning = distance_status in warning_statuses
        days_is_warning = days_status in warning_statuses

        if distance_is_warning and days_is_warning:
            return 'both'
        elif distance_is_warning:
            return 'distance'
        elif days_is_warning:
            return 'time'
        else:
            return None

    def calculate_component_triggers(self, component):
        """Calculate lifetime and service triggers for a component"""
        lifetime_status_distance = self.compute_component_status("lifetime",
                                                                 component.lifetime_remaining,
                                                                 component.threshold_km)
        service_status_distance = self.compute_component_status("service",
                                                                component.service_next,
                                                                component.threshold_km)

        lifetime_status_days = self.compute_component_status("lifetime",
                                                             component.lifetime_remaining_days,
                                                             component.threshold_days)
        service_status_days = self.compute_component_status("service",
                                                            component.service_next_days,
                                                            component.threshold_days)

        return {"lifetime_trigger": self.determine_trigger(lifetime_status_distance, lifetime_status_days),
                "service_trigger": self.determine_trigger(service_status_distance, service_status_days),
                "lifetime_status_distance": lifetime_status_distance,
                "lifetime_status_days": lifetime_status_days,
                "service_status_distance": service_status_distance,
                "service_status_days": service_status_days}

    def determine_worst_status(self, distance_status, days_status):
        """Method to determine worst-case status between distance and days-based calculations"""
        severity_ranking = {"Service interval exceeded": 4,
                            "Lifetime exceeded": 4,
                            "Due for service": 3,
                            "Due for replacement": 3,
                            "OK": 2,
                            "Not defined": 1}

        distance_severity = severity_ranking.get(distance_status, 0)
        days_severity = severity_ranking.get(days_status, 0)

        if days_severity > distance_severity:
            return days_status
        else:
            return distance_status

    def update_time_based_fields(self):
        """Method to update time-based status fields for all non-retired components"""
        components = database_manager.read_all_components_objects()
        active_components = [component for component in components if component.installation_status != "Retired"]

        component_count = len(active_components)
        updated_count = 0
        error_count = 0

        logging.info(f'Starting time-based fields update for {component_count} components that are installed or not assigned.')
        for component in active_components:
            try:
                if component.lifetime_expected_days or component.service_interval_days:
                    logging.debug(f'{component.component_name} tracks days for lifetime or service intervals. Updating time-based fields.')
                    self.update_component_lifetime_status(component)
                    self.update_component_service_status(component)

                    if component.installation_status == "Installed" and component.bike_id:
                        self.update_bike_status(component.bike_id)

                    updated_count += 1

            except Exception as exception:
                error_count += 1
                logging.error(f"Error updating time fields for component {component.component_id}: {exception}")

        if error_count > 0:
            logging.warning(f"{updated_count} components successfully updated. {error_count} components failed to update.")
            return False, f"{updated_count} components successfully updated. {error_count} components failed to update."
        elif updated_count > 0:
            logging.info(f"{updated_count} components successfully updated.")
            return True, f"{updated_count} components successfully updated"
        else:
            logging.warning("No components have been configured to track days for lifetime or service intervals")
            return True, "No components have been configured to track days for lifetime or service intervals"

    def validate_threshold_configuration(self,
                                         expected_lifetime,
                                         service_interval,
                                         lifetime_expected_days,
                                         service_interval_days,
                                         threshold_km,
                                         threshold_days):
        """Validate threshold configuration rules for component intervals"""
        if expected_lifetime or service_interval:
            if threshold_km is None:
                return False, "Threshold (km) is required when distance-based intervals are configured"

        if lifetime_expected_days or service_interval_days:
            if threshold_days is None:
                return False, "Threshold (days) is required when time-based intervals are configured"

        if threshold_km is not None:
            if threshold_km <= 0:
                return False, "Threshold (km) must be greater than 0"

            intervals = []
            if expected_lifetime:
                intervals.append(expected_lifetime)
            if service_interval:
                intervals.append(service_interval)

            if intervals and threshold_km > min(intervals):
                return False, f"Threshold (km) must be less than or equal to the smallest interval ({min(intervals)} km)"

        if threshold_days is not None:
            if threshold_days <= 0:
                return False, "Threshold (days) must be greater than 0"

            intervals = []
            if lifetime_expected_days:
                intervals.append(lifetime_expected_days)
            if service_interval_days:
                intervals.append(service_interval_days)

            if intervals and threshold_days > min(intervals):
                return False, f"Threshold (days) must be less than or equal to the smallest interval ({min(intervals)} days)"

        return True, "Validation passed"

    def process_bike_compliance_report(self, bike_id):
        """Method to check if a bike has all mandatory components and respects max quantities"""
        compliance_report = {"all_mandatory_present": True,
                             "no_max_quantity_exceeded": True,
                             "missing_mandatory": [],
                             "exceeding_max_quantity": {}}

        component_types_raw = database_manager.read_all_component_types()

        component_types = {component_type[0]:
                                {'expected_lifetime': component_type[1],
                                 'lifetime_expected_days': component_type[2],
                                 'service_interval': component_type[3],
                                 'service_interval_days': component_type[4],
                                 'threshold_km': component_type[5],
                                 'threshold_days': component_type[6],
                                 'in_use': component_type[7],
                                 'mandatory': component_type[8],
                                 'max_quantity': component_type[9]} for component_type in component_types_raw}

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
                               incident_affected_component_ids,
                               incident_affected_bike_id,
                               incident_description,
                               resolution_date,
                               resolution_notes):
        """Method to add incident record"""
        try:
            incident_id = generate_unique_id()

            incident_affected_bike_id = incident_affected_bike_id if incident_affected_bike_id else None
            incident_description = incident_description if incident_description else None
            resolution_date = resolution_date if resolution_date else None
            resolution_notes = resolution_notes if resolution_notes else None

            incident_data = {"incident_id": incident_id,
                             "incident_date": incident_date,
                             "incident_status": incident_status,
                             "incident_severity": incident_severity,
                             "incident_affected_component_ids": json.dumps(incident_affected_component_ids) if incident_affected_component_ids else None,
                             "incident_affected_bike_id": incident_affected_bike_id,
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
                               incident_affected_component_ids,
                               incident_affected_bike_id,
                               incident_description,
                               resolution_date,
                               resolution_notes):
        """Method to update incident record"""
        try:
            incident_affected_bike_id = incident_affected_bike_id if incident_affected_bike_id else None
            incident_description = incident_description if incident_description else None
            resolution_date = resolution_date if resolution_date else None
            resolution_notes = resolution_notes if resolution_notes else None

            incident_data = {"incident_id": incident_id,
                             "incident_date": incident_date,
                             "incident_status": incident_status,
                             "incident_severity": incident_severity,
                             "incident_affected_component_ids": json.dumps(incident_affected_component_ids) if incident_affected_component_ids else None,
                             "incident_affected_bike_id": incident_affected_bike_id,
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

    def create_workplan(self,
                        due_date,
                        workplan_status,
                        workplan_size,
                        workplan_affected_component_ids,
                        workplan_affected_bike_id,
                        workplan_description,
                        completion_date,
                        completion_notes):
        """Method to add workplan"""
        try:
            workplan_id = generate_unique_id()

            workplan_affected_bike_id = workplan_affected_bike_id if workplan_affected_bike_id else None
            workplan_description = workplan_description if workplan_description else None
            completion_date = completion_date if completion_date else None
            completion_notes = completion_notes if completion_notes else None

            workplan_data = {"workplan_id": workplan_id,
                             "due_date": due_date,
                             "workplan_status": workplan_status,
                             "workplan_size": workplan_size,
                             "workplan_affected_component_ids": json.dumps(workplan_affected_component_ids) if workplan_affected_component_ids else None,
                             "workplan_affected_bike_id": workplan_affected_bike_id,
                             "workplan_description": workplan_description,
                             "completion_date": completion_date,
                             "completion_notes": completion_notes}
            
            success, message = database_manager.write_workplan(workplan_data)

            if success:
                logging.info(f"Creation of workplan successful: {message}")
            else:
                logging.error(f"Creation of workplan failed: {message}")

            return success, message

        except Exception as error:
            logging.error(f"Error creating workplan with id {workplan_id}: {str(error)}")
            return False, f"Error creating workplan with id {workplan_id}: {str(error)}"
        
    def update_workplan(self,
                        workplan_id,
                        due_date,
                        workplan_status,
                        workplan_size,
                        workplan_affected_component_ids,
                        workplan_affected_bike_id,
                        workplan_description,
                        completion_date,
                        completion_notes):
        """Method to update workplan"""
        try:
            workplan_affected_bike_id = workplan_affected_bike_id if workplan_affected_bike_id else None
            workplan_description = workplan_description if workplan_description else None
            completion_date = completion_date if completion_date else None
            completion_notes = completion_notes if completion_notes else None

            workplan_data = {"workplan_id": workplan_id,
                             "due_date": due_date,
                             "workplan_status": workplan_status,
                             "workplan_size": workplan_size,
                             "workplan_affected_component_ids": json.dumps(workplan_affected_component_ids) if workplan_affected_component_ids else None,
                             "workplan_affected_bike_id": workplan_affected_bike_id,
                             "workplan_description": workplan_description,
                             "completion_date": completion_date,
                             "completion_notes": completion_notes}
            
            success, message = database_manager.write_workplan(workplan_data)

            if success:
                logging.info(f"Update of workplan successful: {message}")
            else:
                logging.error(f"Update of workplan failed: {message}")

            return success, message

        except Exception as error:
            logging.error(f"Error updating workplan with id {workplan_id}: {str(error)}")
            return False, f"Error updating workplan with id {workplan_id}: {str(error)}"
    
    def modify_component_type(self,
                            component_type,
                            expected_lifetime,
                            lifetime_expected_days,
                            service_interval,
                            service_interval_days,
                            threshold_km,
                            threshold_days,
                            mandatory,
                            max_quantity,
                            mode):
        """Method to create or update component types"""
        expected_lifetime = int(expected_lifetime) if expected_lifetime and expected_lifetime.isdigit() else None
        lifetime_expected_days = int(lifetime_expected_days) if lifetime_expected_days and lifetime_expected_days.isdigit() else None
        service_interval = int(service_interval) if service_interval and service_interval.isdigit() else None
        service_interval_days = int(service_interval_days) if service_interval_days and service_interval_days.isdigit() else None
        threshold_km = int(threshold_km) if threshold_km and threshold_km.isdigit() else None
        threshold_days = int(threshold_days) if threshold_days and threshold_days.isdigit() else None
        max_quantity = int(max_quantity) if max_quantity and max_quantity.isdigit() else None

        validation_success, validation_message = self.validate_threshold_configuration(expected_lifetime,
                                                                                       service_interval,
                                                                                       lifetime_expected_days,
                                                                                       service_interval_days,
                                                                                       threshold_km,
                                                                                       threshold_days)

        if not validation_success:
            logging.warning(f"Component type validation failed: {validation_message}")
            return False, validation_message

        in_use = database_manager.count_component_types_in_use(component_type)

        component_type_data = {"component_type": component_type,
                            "expected_lifetime": expected_lifetime,
                            "lifetime_expected_days": lifetime_expected_days,
                            "service_interval": service_interval,
                            "service_interval_days": service_interval_days,
                            "threshold_km": threshold_km,
                            "threshold_days": threshold_days,
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
                logging.debug(f"Component type count updated: {component_type} used by {in_use} components")
            else:
                logging.error(f"Component type count update failed: {message}")
            
            return success, message
        
        return False, f"Component type not found: {component_type}"
    
    def delete_record(self, table_selector, record_id):
        """Method to delete a given record and associated records"""
        logging.info(f"Attempting to delete record with id {record_id} from table {table_selector}")

        component_id = None
        bike_id = None
        collection_id = None
        if table_selector == "Services":
            component_id = database_manager.read_single_service_record(record_id).component_id
            component = database_manager.read_component(component_id)
            bike_id = component.bike_id
        
        elif table_selector == "ComponentHistory":
            component_id = database_manager.read_single_history_record(record_id).component_id
            component = database_manager.read_component(component_id)
            bike_id = component.bike_id
            service_history = database_manager.read_subset_service_history(component_id)
            history_records = database_manager.read_subset_component_history(component_id)

            if service_history and history_records.count() == 1:
                logging.warning(f"Cannot delete initial history record {record_id} for component {component.component_name} as service records exist")
                return False, f"Cannot delete initial history record {record_id} for component {component.component_name} as service records exist", component_id, bike_id, collection_id
        
        elif table_selector == "Components":
            component = database_manager.read_component(record_id)
            component_type = component.component_type
            bike_id = component.bike_id

            collection = database_manager.read_collection_by_component(record_id)
            if collection:
                collection_id = collection.collection_id
                logging.warning(f"Cannot delete component {component.component_name} as it is part of collection: {collection.collection_name}")
                return False, f"Cannot delete component {component.component_name} as it is part of collection: {collection.collection_name}. Remove it from the collection first.", component.component_id, bike_id, collection_id

        elif table_selector == "Collections":
            collection = database_manager.read_single_collection(record_id)
            collection_component_ids = json.loads(collection.components) if collection.components else None
            print(table_selector)
            if collection_component_ids:
                logging.warning(f"Cannot delete collection {collection.collection_name} as it still contains components.")
                return False, f"Cannot delete collection {collection.collection_name} as it still contains components. Remove all components from collection before deleting.", None, None, None
            

        elif table_selector == "ComponentTypes":
            component_type = database_manager.read_single_component_type(record_id)
            if component_type.in_use > 0:
                logging.warning(f"Component type {component_type.component_type} is in use by {component_type.in_use} components and cannot be deleted")
                return False, f"Component type {component_type.component_type} is in use by {component_type.in_use} components and cannot be deleted", component_id, bike_id, collection_id
        
        success, message = database_manager.write_delete_record(table_selector, record_id)

        if success:
            logging.info(f"Deletion successful: {message}")
            if table_selector == "Services":
                logging.debug(f"Recalculating service records for component {component.component_name} after deletion")

                service_records = database_manager.read_subset_service_history(component_id)
                if service_records:
                    first_service = service_records.first()
                    success, message = self.process_service_records(component_id,
                                                                    first_service.service_id,
                                                                    first_service.service_date,
                                                                    first_service.description)
                    if not success:
                        logging.error(f"An error occured triggering update of service records for {component.component_name} after deletion: {message}")
                        return False, f"An error occured triggering update of service records for {component.component_name} after deletion: {message}", component_id, bike_id, collection_id
                
                elif not service_records:
                    component = database_manager.read_component(component_id)
                    self.update_component_distance(component_id, component.component_distance - component.component_distance_offset)

            elif table_selector == "ComponentHistory":
                logging.debug(f"Recalculating installation history records for component {component.component_name} after deletion")
                
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
                                                                                   str(component.threshold_km),
                                                                                   str(component.lifetime_expected_days),
                                                                                   str(component.service_interval_days),
                                                                                   str(component.threshold_days),
                                                                                   str(component.cost),
                                                                                   component.component_distance_offset,
                                                                                   component.notes)
                
                else:
                    success, message = self.process_history_records(component_id)
                
                if not success:
                    logging.error(f"An error occured triggering update of history records for {component_id} after deletion: {message}")
                    return False, f"An error occured triggering update of history records for {component_id} after deletion: {message}", component_id, bike_id, collection_id
                
            elif table_selector == "Components":
                self.update_component_type_count(component_type)
                if bike_id:
                    self.update_bike_status(bike_id)
        
        else:
            logging.error(f"Deletion of {record_id} failed: {message}")
            return False, f"Deletion of {record_id} failed: {message}", component_id, bike_id, collection_id

        return success, message, component_id, bike_id, collection_id

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
