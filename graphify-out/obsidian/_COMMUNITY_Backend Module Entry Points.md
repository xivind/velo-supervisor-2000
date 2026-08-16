---
type: community
members: 16
---

# Backend Module Entry Points

**Members:** 16 nodes

## Members
- [[Function to calculate remaining service interval or remaining lifetime as…]] - rationale - backend/utils.py
- [[Function to get current program version]] - rationale - backend/utils.py
- [[Function to parse button sorting data from form submission]] - rationale - backend/utils.py
- [[Function to read configuration file]] - rationale - backend/utils.py
- [[Function to update configuration file based on which form was submitted]] - rationale - backend/utils.py
- [[Incidents]] - code - backend/database_model.py
- [[Model for table incidents]] - rationale - backend/database_model.py
- [[business_logic.py]] - code - backend/business_logic.py
- [[calculate_percentage_reached()]] - code - backend/utils.py
- [[database_manager.py]] - code - backend/database_manager.py
- [[database_model.py]] - code - backend/database_model.py
- [[get_current_version()]] - code - backend/utils.py
- [[parse_button_sorting()]] - code - backend/utils.py
- [[read_config()]] - code - backend/utils.py
- [[utils.py]] - code - backend/utils.py
- [[write_config()]] - code - backend/utils.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Backend_Module_Entry_Points
SORT file.name ASC
```

## Connections to other communities
- 7 edges to [[_COMMUNITY_Database Models Core Tables]]
- 7 edges to [[_COMMUNITY_Workplan Business Logic]]
- 5 edges to [[_COMMUNITY_Bike & Component Queries]]
- 3 edges to [[_COMMUNITY_Database Models Bikes & Services]]
- 2 edges to [[_COMMUNITY_Database Manager Core]]
- 2 edges to [[_COMMUNITY_Config Update & Shutdown]]
- 2 edges to [[_COMMUNITY_Component Status Updates]]
- 2 edges to [[_COMMUNITY_Main API Routes]]
- 1 edge to [[_COMMUNITY_Business Logic Core]]
- 1 edge to [[_COMMUNITY_Components Table Model]]
- 1 edge to [[_COMMUNITY_Creation & Validation Logic]]
- 1 edge to [[_COMMUNITY_Service Record Validation]]
- 1 edge to [[_COMMUNITY_Details Page Endpoints]]
- 1 edge to [[_COMMUNITY_Config Page Endpoint]]
- 1 edge to [[_COMMUNITY_Log Filtering]]
- 1 edge to [[_COMMUNITY_Strava API Integration]]
- 1 edge to [[_COMMUNITY_APScheduler Jobs]]

## Top bridge nodes
- [[utils.py]] - degree 28, connects to 10 communities
- [[business_logic.py]] - degree 6, connects to 4 communities
- [[database_model.py]] - degree 12, connects to 3 communities
- [[Incidents]] - degree 5, connects to 3 communities
- [[write_config()]] - degree 5, connects to 1 community