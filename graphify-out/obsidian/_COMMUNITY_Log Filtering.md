---
type: community
members: 4
---

# Log Filtering

**Members:** 4 nodes

## Members
- [[Endpoint to read log and return only business events]] - rationale - backend/main.py
- [[Function to get filtered log records]] - rationale - backend/utils.py
- [[get_filtered_log()]] - code - backend/main.py
- [[read_filtered_logs()]] - code - backend/utils.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Log_Filtering
SORT file.name ASC
```

## Connections to other communities
- 1 edge to [[_COMMUNITY_Page Endpoint Handlers]]
- 1 edge to [[_COMMUNITY_Main API Routes]]
- 1 edge to [[_COMMUNITY_Backend Module Entry Points]]

## Top bridge nodes
- [[get_filtered_log()]] - degree 4, connects to 2 communities
- [[read_filtered_logs()]] - degree 3, connects to 1 community