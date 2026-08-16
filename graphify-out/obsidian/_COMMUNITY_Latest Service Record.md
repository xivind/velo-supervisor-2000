---
type: community
members: 2
---

# Latest Service Record

**Members:** 2 nodes

## Members
- [[dot-read_latest_service_record()]] - code - backend/database_manager.py
- [[Method to retrieve the most recent record from the service log of a given…]] - rationale - backend/database_manager.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Latest_Service_Record
SORT file.name ASC
```

## Connections to other communities
- 1 edge to [[_COMMUNITY_Database Manager Core]]

## Top bridge nodes
- [[dot-read_latest_service_record()]] - degree 2, connects to 1 community