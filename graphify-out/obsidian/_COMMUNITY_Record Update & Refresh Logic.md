---
type: community
members: 16
---

# Record Update & Refresh Logic

**Members:** 16 nodes

## Members
- [[dot-delete_record()]] - code - backend/business_logic.py
- [[dot-modify_component_details()]] - code - backend/business_logic.py
- [[dot-process_history_records()]] - code - backend/business_logic.py
- [[dot-process_service_records()]] - code - backend/business_logic.py
- [[dot-refresh_all_bikes()]] - code - backend/business_logic.py
- [[dot-update_bike_status()]] - code - backend/business_logic.py
- [[dot-update_component_distance()]] - code - backend/business_logic.py
- [[dot-update_component_type_count()]] - code - backend/business_logic.py
- [[Method to calculate distance and bike id for history records]] - rationale - backend/business_logic.py
- [[Method to calculate distance and bike id for service records]] - rationale - backend/business_logic.py
- [[Method to delete a given record and associated records]] - rationale - backend/business_logic.py
- [[Method to refresh all bikes from Strava]] - rationale - backend/business_logic.py
- [[Method to update component details]] - rationale - backend/business_logic.py
- [[Method to update component table with distance from ride table]] - rationale - backend/business_logic.py
- [[Method to update only the count of components for a given component type]] - rationale - backend/business_logic.py
- [[Method to update status for a given bike based on component service and…]] - rationale - backend/business_logic.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Record_Update__Refresh_Logic
SORT file.name ASC
```

## Connections to other communities
- 10 edges to [[_COMMUNITY_Business Logic Core]]
- 8 edges to [[_COMMUNITY_Component Status Updates]]
- 3 edges to [[_COMMUNITY_Creation & Validation Logic]]
- 3 edges to [[_COMMUNITY_Service Record Validation]]

## Top bridge nodes
- [[dot-process_history_records()]] - degree 10, connects to 4 communities
- [[dot-process_service_records()]] - degree 8, connects to 3 communities
- [[dot-update_component_distance()]] - degree 10, connects to 2 communities
- [[dot-delete_record()]] - degree 9, connects to 2 communities
- [[dot-update_bike_status()]] - degree 8, connects to 2 communities