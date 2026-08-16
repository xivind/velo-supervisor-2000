---
type: community
members: 2
---

# Matching Rides Query

**Members:** 2 nodes

## Members
- [[dot-read_matching_rides()]] - code - backend/database_manager.py
- [[Method to read rides associated with a given component aftere a given date]] - rationale - backend/database_manager.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Matching_Rides_Query
SORT file.name ASC
```

## Connections to other communities
- 1 edge to [[_COMMUNITY_Database Manager Core]]

## Top bridge nodes
- [[dot-read_matching_rides()]] - degree 2, connects to 1 community