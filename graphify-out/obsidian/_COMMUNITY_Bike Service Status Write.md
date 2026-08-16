---
type: community
members: 2
---

# Bike Service Status Write

**Members:** 2 nodes

## Members
- [[dot-write_bike_service_status()]] - code - backend/database_manager.py
- [[Method to update bike service status in database]] - rationale - backend/database_manager.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Bike_Service_Status_Write
SORT file.name ASC
```

## Connections to other communities
- 1 edge to [[_COMMUNITY_Database Manager Core]]

## Top bridge nodes
- [[dot-write_bike_service_status()]] - degree 2, connects to 1 community