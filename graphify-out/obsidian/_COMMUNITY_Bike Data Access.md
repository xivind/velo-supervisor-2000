---
type: community
members: 6
---

# Bike Data Access

**Members:** 6 nodes

## Members
- [[dot-read_bike_name()]] - code - backend/database_manager.py
- [[dot-read_single_bike()]] - code - backend/database_manager.py
- [[dot-write_update_bikes()]] - code - backend/database_manager.py
- [[Method to create or update bike data to the database]] - rationale - backend/database_manager.py
- [[Method to get the name of a bike based on bike id]] - rationale - backend/database_manager.py
- [[Method to retrieve record for a specific bike]] - rationale - backend/database_manager.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Bike_Data_Access
SORT file.name ASC
```

## Connections to other communities
- 3 edges to [[_COMMUNITY_Database Manager Core]]
- 1 edge to [[_COMMUNITY_Bike & Component Queries]]

## Top bridge nodes
- [[dot-read_bike_name()]] - degree 4, connects to 2 communities
- [[dot-read_single_bike()]] - degree 4, connects to 1 community
- [[dot-write_update_bikes()]] - degree 3, connects to 1 community