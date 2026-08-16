---
type: community
members: 23
---

# Business Logic Core

**Members:** 23 nodes

## Members
- [[dot-__init__()_2]] - code - backend/business_logic.py
- [[dot-create_workplan()]] - code - backend/business_logic.py
- [[dot-determine_trigger()]] - code - backend/business_logic.py
- [[dot-get_component_types()]] - code - backend/business_logic.py
- [[dot-modify_component_type()]] - code - backend/business_logic.py
- [[dot-set_time_strava_last_pull()]] - code - backend/business_logic.py
- [[dot-update_components_distance_iterator()]] - code - backend/business_logic.py
- [[dot-update_incident_record()]] - code - backend/business_logic.py
- [[dot-update_rides_bulk()]] - code - backend/business_logic.py
- [[dot-update_workplan()]] - code - backend/business_logic.py
- [[dot-validate_threshold_configuration()]] - code - backend/business_logic.py
- [[BusinessLogic]] - code - backend/business_logic.py
- [[Class that contains business logic]] - rationale - backend/business_logic.py
- [[Function to set the date for last pull from Strava]] - rationale - backend/business_logic.py
- [[Method to add workplan and optionally link to source incident]] - rationale - backend/business_logic.py
- [[Method to create or update component types]] - rationale - backend/business_logic.py
- [[Method to create or update ride data in bulk to database]] - rationale - backend/business_logic.py
- [[Method to determine which factor triggered a warning status]] - rationale - backend/business_logic.py
- [[Method to determine which selection of components to update]] - rationale - backend/business_logic.py
- [[Method to produce payload for page component types]] - rationale - backend/business_logic.py
- [[Method to update incident record (supports full or partial updates)]] - rationale - backend/business_logic.py
- [[Method to update workplan (supports full or partial updates)]] - rationale - backend/business_logic.py
- [[Validate threshold configuration rules for component intervals]] - rationale - backend/business_logic.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Business_Logic_Core
SORT file.name ASC
```

## Connections to other communities
- 11 edges to [[_COMMUNITY_Bike & Component Queries]]
- 10 edges to [[_COMMUNITY_Record Update & Refresh Logic]]
- 9 edges to [[_COMMUNITY_Creation & Validation Logic]]
- 6 edges to [[_COMMUNITY_Component Status Updates]]
- 6 edges to [[_COMMUNITY_Service Record Validation]]
- 6 edges to [[_COMMUNITY_Collection Status Logic]]
- 3 edges to [[_COMMUNITY_Workplan Business Logic]]
- 2 edges to [[_COMMUNITY_APScheduler Jobs]]
- 1 edge to [[_COMMUNITY_Backend Module Entry Points]]

## Top bridge nodes
- [[BusinessLogic]] - degree 61, connects to 9 communities
- [[dot-validate_threshold_configuration()]] - degree 5, connects to 2 communities
- [[dot-create_workplan()]] - degree 4, connects to 1 community
- [[dot-update_components_distance_iterator()]] - degree 4, connects to 1 community
- [[dot-determine_trigger()]] - degree 3, connects to 1 community