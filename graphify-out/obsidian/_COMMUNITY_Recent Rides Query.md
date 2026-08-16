---
type: community
members: 2
---

# Recent Rides Query

**Members:** 2 nodes

## Members
- [[dot-read_recent_rides()]] - code - backend/database_manager.py
- [[Method to read recent rides for a specific bike]] - rationale - backend/database_manager.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Recent_Rides_Query
SORT file.name ASC
```

## Connections to other communities
- 1 edge to [[_COMMUNITY_Database Manager Core]]

## Top bridge nodes
- [[dot-read_recent_rides()]] - degree 2, connects to 1 community