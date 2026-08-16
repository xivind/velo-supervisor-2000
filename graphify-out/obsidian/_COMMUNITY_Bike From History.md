---
type: community
members: 2
---

# Bike From History

**Members:** 2 nodes

## Members
- [[dot-read_bike_id_recent_component_history()]] - code - backend/database_manager.py
- [[Method to get bike id from most recent component history]] - rationale - backend/database_manager.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Bike_From_History
SORT file.name ASC
```

## Connections to other communities
- 1 edge to [[_COMMUNITY_Database Manager Core]]

## Top bridge nodes
- [[dot-read_bike_id_recent_component_history()]] - degree 2, connects to 1 community