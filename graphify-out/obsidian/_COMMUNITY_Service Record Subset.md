---
type: community
members: 2
---

# Service Record Subset

**Members:** 2 nodes

## Members
- [[dot-read_subset_service_record()]] - code - backend/database_manager.py
- [[Method to retrieve record for a specific entry in the service log]] - rationale - backend/database_manager.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Service_Record_Subset
SORT file.name ASC
```

## Connections to other communities
- 1 edge to [[_COMMUNITY_Database Manager Core]]

## Top bridge nodes
- [[dot-read_subset_service_record()]] - degree 2, connects to 1 community