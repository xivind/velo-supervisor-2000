from .loader import AppModules


def recalculate(app: AppModules) -> list[str]:
    """Run the full recalculation chain and return one sorted line per failed call.

    Failures are returned, not raised, so a failure on real data stays comparable.
    Lines read <step>:<id>: <message>; the distance iterator covers all bikes in one call.
    """
    logic = app.business_logic
    manager = app.database_manager
    failures = []

    def check(step, identifier, result):
        success, message = result
        if success is False:
            failures.append(f"{step}:{identifier}: {message}")

    check(
        "distance_iterator", "all_bikes", logic.update_components_distance_iterator(sorted(manager.read_unique_bikes()))
    )
    for component in manager.read_all_components_objects():
        check("process_history_records", component.component_id, logic.process_history_records(component.component_id))
    check("update_time_based_fields", "all_components", logic.update_time_based_fields())
    for component_type in manager.read_all_component_types():
        check("update_component_type_count", component_type[0], logic.update_component_type_count(component_type[0]))
    return sorted(failures)
