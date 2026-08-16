---
type: community
members: 2
---

# Planned Workplans Query

**Members:** 2 nodes

## Members
- [[dot-read_planned_workplans()]] - code - backend/database_manager.py
- [[Method to read workplans with status 'Planned]] - rationale - backend/database_manager.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Planned_Workplans_Query
SORT file.name ASC
```

## Connections to other communities
- 1 edge to [[_COMMUNITY_Database Manager Core]]

## Top bridge nodes
- [[dot-read_planned_workplans()]] - degree 2, connects to 1 community