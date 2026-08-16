---
type: community
members: 2
---

# Incidents By Workplan

**Members:** 2 nodes

## Members
- [[dot-read_incidents_by_workplan()]] - code - backend/database_manager.py
- [[Method to read all incidents linked to a specific workplan]] - rationale - backend/database_manager.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Incidents_By_Workplan
SORT file.name ASC
```

## Connections to other communities
- 1 edge to [[_COMMUNITY_Database Manager Core]]

## Top bridge nodes
- [[dot-read_incidents_by_workplan()]] - degree 2, connects to 1 community