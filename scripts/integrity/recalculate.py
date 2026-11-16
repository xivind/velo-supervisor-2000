from .loader import AppModules


def recalculate(app: AppModules) -> None:
    """Run the full recalculation chain that derives stored values from rides and history"""
    logic = app.business_logic
    manager = app.database_manager
    logic.update_components_distance_iterator(manager.read_unique_bikes())
    for component in manager.read_all_components_objects():
        logic.process_history_records(component.component_id)
    logic.update_time_based_fields()
    for component_type in manager.read_all_component_types():
        logic.update_component_type_count(component_type[0])
