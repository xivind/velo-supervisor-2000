---
type: community
members: 38
---

# Main API Routes

**Members:** 38 nodes

## Members
- [[Endpoint to add new collection]] - rationale - backend/main.py
- [[Endpoint to add service]] - rationale - backend/main.py
- [[Endpoint to bulk add service records for workplan components]] - rationale - backend/main.py
- [[Endpoint to change the status of all components in a collection]] - rationale - backend/main.py
- [[Endpoint to create a workplan (optionally linked to an incident)]] - rationale - backend/main.py
- [[Endpoint to create an incident record]] - rationale - backend/main.py
- [[Endpoint to delete records]] - rationale - backend/main.py
- [[Endpoint to modify component types]] - rationale - backend/main.py
- [[Endpoint to modify component types_1]] - rationale - backend/main.py
- [[Endpoint to modify component types_2]] - rationale - backend/main.py
- [[Endpoint to swap one component with another]] - rationale - backend/main.py
- [[Endpoint to update a workplan (supports full or partial updates)]] - rationale - backend/main.py
- [[Endpoint to update an existing component history record]] - rationale - backend/main.py
- [[Endpoint to update an existing service record]] - rationale - backend/main.py
- [[Endpoint to update an incident record (supports full or partial updates)]] - rationale - backend/main.py
- [[Endpoint to update existing collection]] - rationale - backend/main.py
- [[FastAPI]] - code
- [[Manage application startup and shutdown]] - rationale - backend/main.py
- [[add_collection()]] - code - backend/main.py
- [[add_incident_record()]] - code - backend/main.py
- [[add_service()]] - code - backend/main.py
- [[add_workplan()]] - code - backend/main.py
- [[bulk_add_service_records()]] - code - backend/main.py
- [[change_collection_status()]] - code - backend/main.py
- [[component_modify()]] - code - backend/main.py
- [[component_types_modify()]] - code - backend/main.py
- [[create_component()]] - code - backend/main.py
- [[delete_record()]] - code - backend/main.py
- [[lifespan()]] - code - backend/main.py
- [[main.py]] - code - backend/main.py
- [[middleware.py]] - code - backend/middleware.py
- [[post]] - code
- [[quick_swap()]] - code - backend/main.py
- [[update_collection()]] - code - backend/main.py
- [[update_history_record()]] - code - backend/main.py
- [[update_incident_record()]] - code - backend/main.py
- [[update_service_record()]] - code - backend/main.py
- [[update_workplan()]] - code - backend/main.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Main_API_Routes
SORT file.name ASC
```

## Connections to other communities
- 12 edges to [[_COMMUNITY_Page Endpoint Handlers]]
- 3 edges to [[_COMMUNITY_APScheduler Jobs]]
- 2 edges to [[_COMMUNITY_Error Handling Middleware]]
- 2 edges to [[_COMMUNITY_Details Page Endpoints]]
- 2 edges to [[_COMMUNITY_Config Update & Shutdown]]
- 2 edges to [[_COMMUNITY_Backend Module Entry Points]]
- 1 edge to [[_COMMUNITY_Config Page Endpoint]]
- 1 edge to [[_COMMUNITY_Log Filtering]]

## Top bridge nodes
- [[main.py]] - degree 39, connects to 8 communities
- [[post]] - degree 18, connects to 2 communities
- [[lifespan()]] - degree 5, connects to 1 community
- [[middleware.py]] - degree 3, connects to 1 community