---
type: community
members: 16
---

# Component Status Updates

**Members:** 16 nodes

## Members
- [[dot-compute_component_status()]] - code - backend/business_logic.py
- [[dot-determine_worst_status()]] - code - backend/business_logic.py
- [[dot-update_component_lifetime_service_alternate()]] - code - backend/business_logic.py
- [[dot-update_component_lifetime_status()]] - code - backend/business_logic.py
- [[dot-update_component_service_status()]] - code - backend/business_logic.py
- [[dot-update_time_based_fields()]] - code - backend/business_logic.py
- [[Function to calculate the number of days between two dates]] - rationale - backend/utils.py
- [[Function to get current datetime formatted as YYYY-MM-DD HHMM]] - rationale - backend/utils.py
- [[Method to compute component status using threshold logic]] - rationale - backend/business_logic.py
- [[Method to determine worst-case status between distance and days-based…]] - rationale - backend/business_logic.py
- [[Method to update component lifetime and service status when no installation…]] - rationale - backend/business_logic.py
- [[Method to update component table with lifetime status]] - rationale - backend/business_logic.py
- [[Method to update component table with service status]] - rationale - backend/business_logic.py
- [[Method to update time-based status fields for all non-retired components]] - rationale - backend/business_logic.py
- [[calculate_elapsed_days()]] - code - backend/utils.py
- [[get_formatted_datetime_now()]] - code - backend/utils.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Component_Status_Updates
SORT file.name ASC
```

## Connections to other communities
- 8 edges to [[_COMMUNITY_Record Update & Refresh Logic]]
- 6 edges to [[_COMMUNITY_Business Logic Core]]
- 5 edges to [[_COMMUNITY_Bike & Component Queries]]
- 4 edges to [[_COMMUNITY_Workplan Business Logic]]
- 2 edges to [[_COMMUNITY_Backend Module Entry Points]]
- 1 edge to [[_COMMUNITY_Creation & Validation Logic]]

## Top bridge nodes
- [[get_formatted_datetime_now()]] - degree 10, connects to 4 communities
- [[calculate_elapsed_days()]] - degree 9, connects to 3 communities
- [[dot-update_component_lifetime_service_alternate()]] - degree 8, connects to 3 communities
- [[dot-update_component_service_status()]] - degree 10, connects to 2 communities
- [[dot-update_component_lifetime_status()]] - degree 9, connects to 2 communities