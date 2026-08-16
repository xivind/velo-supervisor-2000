---
type: community
members: 2
---

# Collection Write

**Members:** 2 nodes

## Members
- [[dot-write_collection()]] - code - backend/database_manager.py
- [[Method to create or update collection record in database]] - rationale - backend/database_manager.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Collection_Write
SORT file.name ASC
```

## Connections to other communities
- 1 edge to [[_COMMUNITY_Database Manager Core]]

## Top bridge nodes
- [[dot-write_collection()]] - degree 2, connects to 1 community