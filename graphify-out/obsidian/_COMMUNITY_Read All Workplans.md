---
type: community
members: 2
---

# Read All Workplans

**Members:** 2 nodes

## Members
- [[dot-read_all_workplans()]] - code - backend/database_manager.py
- [[Method to read all workplans]] - rationale - backend/database_manager.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Read_All_Workplans
SORT file.name ASC
```

## Connections to other communities
- 1 edge to [[_COMMUNITY_Database Manager Core]]

## Top bridge nodes
- [[dot-read_all_workplans()]] - degree 2, connects to 1 community