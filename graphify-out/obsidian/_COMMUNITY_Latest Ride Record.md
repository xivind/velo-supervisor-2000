---
type: community
members: 2
---

# Latest Ride Record

**Members:** 2 nodes

## Members
- [[dot-read_latest_ride_record()]] - code - backend/database_manager.py
- [[Method to retrieve the most recent ride]] - rationale - backend/database_manager.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Latest_Ride_Record
SORT file.name ASC
```

## Connections to other communities
- 1 edge to [[_COMMUNITY_Database Manager Core]]

## Top bridge nodes
- [[dot-read_latest_ride_record()]] - degree 2, connects to 1 community