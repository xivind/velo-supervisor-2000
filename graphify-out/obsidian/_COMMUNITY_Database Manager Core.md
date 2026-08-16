---
type: community
members: 19
---

# Database Manager Core

**Members:** 19 nodes

## Members
- [[dot-__init__()_3]] - code - backend/database_manager.py
- [[dot-read_date_oldest_ride()]] - code - backend/database_manager.py
- [[dot-read_oldest_service_record()]] - code - backend/database_manager.py
- [[dot-read_open_incidents()]] - code - backend/database_manager.py
- [[dot-read_subset_component_history()]] - code - backend/database_manager.py
- [[dot-read_subset_installed_components()]] - code - backend/database_manager.py
- [[dot-write_component_distance()]] - code - backend/database_manager.py
- [[dot-write_component_service_status()]] - code - backend/database_manager.py
- [[dot-write_update_rides_bulk()]] - code - backend/database_manager.py
- [[Class to interact with a SQLite database through Peewee]] - rationale - backend/database_manager.py
- [[DatabaseManager]] - code - backend/database_manager.py
- [[Method to create or update ride data in bulk in database]] - rationale - backend/database_manager.py
- [[Method to get the date for the oldest ride for a given bike]] - rationale - backend/database_manager.py
- [[Method to read a subset of records from the component history table]] - rationale - backend/database_manager.py
- [[Method to read incident records with status 'Open]] - rationale - backend/database_manager.py
- [[Method to read installed components for a specific bike]] - rationale - backend/database_manager.py
- [[Method to retrieve the oldest record from the service log of a given component]] - rationale - backend/database_manager.py
- [[Method to update component distance in database]] - rationale - backend/database_manager.py
- [[Method to update component service status in database]] - rationale - backend/database_manager.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Database_Manager_Core
SORT file.name ASC
```

## Connections to other communities
- 6 edges to [[_COMMUNITY_Single-Record Reads]]
- 5 edges to [[_COMMUNITY_Database Models Core Tables]]
- 3 edges to [[_COMMUNITY_Component Data Access]]
- 3 edges to [[_COMMUNITY_Bike Data Access]]
- 2 edges to [[_COMMUNITY_Backend Module Entry Points]]
- 2 edges to [[_COMMUNITY_Database Models Bikes & Services]]
- 2 edges to [[_COMMUNITY_Component Type Data Access]]
- 1 edge to [[_COMMUNITY_Components Table Model]]
- 1 edge to [[_COMMUNITY_Read All Component Types]]
- 1 edge to [[_COMMUNITY_Component Type Usage Count]]
- 1 edge to [[_COMMUNITY_Bike & Component Queries]]
- 1 edge to [[_COMMUNITY_Read All Components]]
- 1 edge to [[_COMMUNITY_Components By Bike]]
- 1 edge to [[_COMMUNITY_Latest History Record]]
- 1 edge to [[_COMMUNITY_Oldest History Record]]
- 1 edge to [[_COMMUNITY_Service History Subset]]
- 1 edge to [[_COMMUNITY_Read Bikes Table]]
- 1 edge to [[_COMMUNITY_Service Record Subset]]
- 1 edge to [[_COMMUNITY_Latest Service Record]]
- 1 edge to [[_COMMUNITY_Read All Collections]]
- 1 edge to [[_COMMUNITY_Collection By Component]]
- 1 edge to [[_COMMUNITY_Read All Incidents]]
- 1 edge to [[_COMMUNITY_Read All Workplans]]
- 1 edge to [[_COMMUNITY_Planned Workplans Query]]
- 1 edge to [[_COMMUNITY_Incidents By Workplan]]
- 1 edge to [[_COMMUNITY_Services By Workplan]]
- 1 edge to [[_COMMUNITY_Component Lifetime Status Write]]
- 1 edge to [[_COMMUNITY_Bike From History]]
- 1 edge to [[_COMMUNITY_Bike Service Status Write]]
- 1 edge to [[_COMMUNITY_Service Record Write]]
- 1 edge to [[_COMMUNITY_History Record Write]]
- 1 edge to [[_COMMUNITY_Collection Write]]
- 1 edge to [[_COMMUNITY_Incident Record Write]]
- 1 edge to [[_COMMUNITY_Unique Bike IDs]]
- 1 edge to [[_COMMUNITY_Workplan Write]]
- 1 edge to [[_COMMUNITY_Recent Rides Query]]
- 1 edge to [[_COMMUNITY_Matching Rides Query]]
- 1 edge to [[_COMMUNITY_Latest Ride Record]]
- 1 edge to [[_COMMUNITY_Ride Distance Sum]]

## Top bridge nodes
- [[DatabaseManager]] - degree 65, connects to 39 communities