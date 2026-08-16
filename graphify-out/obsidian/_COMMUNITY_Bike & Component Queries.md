---
type: community
members: 30
---

# Bike & Component Queries

**Members:** 30 nodes

## Members
- [[dot-calculate_component_triggers()]] - code - backend/business_logic.py
- [[dot-get_bike_details()]] - code - backend/business_logic.py
- [[dot-get_bike_overview()]] - code - backend/business_logic.py
- [[dot-get_component_collection_mapping()]] - code - backend/business_logic.py
- [[dot-get_component_details()]] - code - backend/business_logic.py
- [[dot-get_component_overview()]] - code - backend/business_logic.py
- [[dot-get_incident_reports()]] - code - backend/business_logic.py
- [[dot-get_workplans()]] - code - backend/business_logic.py
- [[dot-process_incidents()]] - code - backend/business_logic.py
- [[dot-process_workplans()]] - code - backend/business_logic.py
- [[dot-read_all_components()]] - code - backend/database_manager.py
- [[Build standard workplan data tuple for display (14 fields)]] - rationale - backend/utils.py
- [[Calculate lifetime and service triggers for a component]] - rationale - backend/business_logic.py
- [[Function to display user friendly text for None values]] - rationale - backend/utils.py
- [[Function to display user friendly text for None values_1]] - rationale - backend/utils.py
- [[Function to get list of all bikes, with prefix for retired bikes]] - rationale - backend/utils.py
- [[Method to build dictionaries of bike and component ids referenced in received…]] - rationale - backend/business_logic.py
- [[Method to build dictionaries of bike and component ids referenced in received…_1]] - rationale - backend/business_logic.py
- [[Method to create component-to-collection mapping dictionaries]] - rationale - backend/business_logic.py
- [[Method to produce payload for page bike details]] - rationale - backend/business_logic.py
- [[Method to produce payload for page bike overview]] - rationale - backend/business_logic.py
- [[Method to produce payload for page component details]] - rationale - backend/business_logic.py
- [[Method to produce payload for page component overview]] - rationale - backend/business_logic.py
- [[Method to produce payload for page incident reports]] - rationale - backend/business_logic.py
- [[Method to produce payload for page of all workplans]] - rationale - backend/business_logic.py
- [[Method to read content of components table as formatted tuples]] - rationale - backend/database_manager.py
- [[format_component_status()]] - code - backend/utils.py
- [[format_cost()]] - code - backend/utils.py
- [[get_formatted_bikes_list()]] - code - backend/utils.py
- [[get_workplan_data_tuple()]] - code - backend/utils.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Bike__Component_Queries
SORT file.name ASC
```

## Connections to other communities
- 11 edges to [[_COMMUNITY_Business Logic Core]]
- 11 edges to [[_COMMUNITY_Workplan Business Logic]]
- 5 edges to [[_COMMUNITY_Backend Module Entry Points]]
- 5 edges to [[_COMMUNITY_Component Status Updates]]
- 3 edges to [[_COMMUNITY_Collection Status Logic]]
- 2 edges to [[_COMMUNITY_Creation & Validation Logic]]
- 1 edge to [[_COMMUNITY_Database Manager Core]]
- 1 edge to [[_COMMUNITY_Bike Data Access]]

## Top bridge nodes
- [[dot-get_component_details()]] - degree 15, connects to 4 communities
- [[dot-get_bike_details()]] - degree 14, connects to 4 communities
- [[get_workplan_data_tuple()]] - degree 13, connects to 3 communities
- [[dot-get_component_overview()]] - degree 12, connects to 2 communities
- [[get_formatted_bikes_list()]] - degree 8, connects to 2 communities