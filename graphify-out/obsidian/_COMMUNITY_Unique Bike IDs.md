---
type: community
members: 2
---

# Unique Bike IDs

**Members:** 2 nodes

## Members
- [[dot-read_unique_bikes()]] - code - backend/database_manager.py
- [[Method to query database and create list of unique bike ids]] - rationale - backend/database_manager.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Unique_Bike_IDs
SORT file.name ASC
```

## Connections to other communities
- 1 edge to [[_COMMUNITY_Database Manager Core]]

## Top bridge nodes
- [[dot-read_unique_bikes()]] - degree 2, connects to 1 community