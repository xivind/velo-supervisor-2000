---
type: community
members: 2
---

# Read All Incidents

**Members:** 2 nodes

## Members
- [[dot-read_all_incidents()]] - code - backend/database_manager.py
- [[Method to read all incident records]] - rationale - backend/database_manager.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Read_All_Incidents
SORT file.name ASC
```

## Connections to other communities
- 1 edge to [[_COMMUNITY_Database Manager Core]]

## Top bridge nodes
- [[dot-read_all_incidents()]] - degree 2, connects to 1 community