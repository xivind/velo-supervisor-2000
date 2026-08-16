---
type: community
members: 2
---

# Service History Subset

**Members:** 2 nodes

## Members
- [[dot-read_subset_service_history()]] - code - backend/database_manager.py
- [[Method to read a subset of receords from the component history table]] - rationale - backend/database_manager.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Service_History_Subset
SORT file.name ASC
```

## Connections to other communities
- 1 edge to [[_COMMUNITY_Database Manager Core]]

## Top bridge nodes
- [[dot-read_subset_service_history()]] - degree 2, connects to 1 community