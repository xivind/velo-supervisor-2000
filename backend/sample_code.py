from fastapi import FastAPI
from peewee_models import database, Rides, Bikes
import peewee # decide on how to import peewee modules

database.connect()

def test_select():
    """Function to test database connectivity"""
    counter = 0
    try:
        with database.atomic():
            table_data = Rides.select().where(Rides.ride_distance > 200)
            for component in table_data:
                print(component.ride_name)
                counter = counter+1

            print(counter)
    except Exception as error:
        print(error)


def test_update_bikes_table(data):
    """Function to test database connectivity"""
    try:
        # Start a transaction
        with database.atomic():
            for bike_id, bike_data in data.items():
                # Try to find an existing bike with the given bike_id
                bike = Bikes.get_or_none(Bikes.bike_id == bike_id)

                # If the bike already exists, update its data
                if bike:
                    bike.athlete_id = bike_data.get('athlete_id')
                    bike.total_distance = bike_data.get('total_distance')
                    bike.save()
                # If the bike doesn't exist, create a new row
                else:
                    Bikes.create(
                        bike_id=bike_id,
                        athlete_id=bike_data.get('athlete_id'),
                        total_distance=bike_data.get('total_distance', 0)
                    )

        print("Bikes table updated successfully!")
    except peewee.OperationalError as error:
        print("An error occurred while updating the bikes table:", error)

# Your dictionary of dictionaries holding bike data
# Example format: {'bike_id1': {'athlete_id': '123', 'total_distance': 100.5}, 'bike_id2': {'athlete_id': '456', 'total_distance': 200.3}}
your_data = {
    'b23232': {'athlete_id': '123', 'total_distance': 100.5},
    'b34343': {'athlete_id': '456', 'total_distance': 200.3}
}    

def test_delete_bike(bike_id):
    try:
        # Start a transaction
        with database.atomic():
            # Try to find the bike with the given bike_id
            bike = Bikes.get_or_none(Bikes.bike_id == bike_id)

            # If the bike exists, delete it
            if bike:
                bike.delete_instance()
                print(f"Bike with bike_id '{bike_id}' deleted successfully!")
            else:
                print(f"No bike found with bike_id '{bike_id}'. No deletion performed.")

    except peewee.OperationalError as e:
        print("An error occurred while deleting the bike:", e)

# Call the function to delete a bike with a specific bike_id
test_delete_bike('b23232')

def read_latest_component_history_record(self, component_id): # This function is no longer used?
        """Method to read the most recent component history record"""
        component_history_record = ComponentHistory.select().where(ComponentHistory.component_id == component_id).order_by(ComponentHistory.updated_date.desc()).first()
        if component_history_record:
            return component_history_record
        
        return None

def update_component_distance(self, component):
        """Method to update component table with distance from ride table"""
        try:
            if component.updated_date and component.installation_status == "Installed":
                updated_date = datetime.strptime(component.updated_date.split()[0], '%Y-%m-%d')
            else:
                updated_date = None

            record_time_query = Rides.select(Rides.record_time).where(Rides.bike_id == component.bike_id)
            record_time_value = record_time_query.scalar()
            record_time = datetime.strptime(record_time_value, '%Y-%m-%dT%H:%M:%S') if record_time_value else None

            matching_rides = Rides.select().where(
                (Rides.bike_id == component.bike_id) & (Rides.record_time >= updated_date))

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


<p class="card-text">
                    <span class="fw-bold bg-secondary-subtle rounded px-2 d-inline-block">Lifetime statistics installed components</span>
               </p>