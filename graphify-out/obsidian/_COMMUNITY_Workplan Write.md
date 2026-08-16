---
type: community
members: 2
---

# Workplan Write

**Members:** 2 nodes

## Members
- [[dot-write_workplan()]] - code - backend/database_manager.py
- [[Method to create or update workplan record in database]] - rationale - backend/database_manager.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Workplan_Write
SORT file.name ASC
```

## Connections to other communities
- 1 edge to [[_COMMUNITY_Database Manager Core]]

## Top bridge nodes
- [[dot-write_workplan()]] - degree 2, connects to 1 community