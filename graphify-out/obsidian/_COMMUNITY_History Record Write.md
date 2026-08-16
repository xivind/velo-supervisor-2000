---
type: community
members: 2
---

# History Record Write

**Members:** 2 nodes

## Members
- [[dot-write_history_record()]] - code - backend/database_manager.py
- [[Method to write or update history record in database]] - rationale - backend/database_manager.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/History_Record_Write
SORT file.name ASC
```

## Connections to other communities
- 1 edge to [[_COMMUNITY_Database Manager Core]]

## Top bridge nodes
- [[dot-write_history_record()]] - degree 2, connects to 1 community