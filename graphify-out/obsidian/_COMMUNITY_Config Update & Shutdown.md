---
type: community
members: 4
---

# Config Update & Shutdown

**Members:** 4 nodes

## Members
- [[Endpoint to update config file based on which form was submitted]] - rationale - backend/main.py
- [[Helper function to shutdown the server after a short delay]] - rationale - backend/utils.py
- [[shutdown_server()]] - code - backend/utils.py
- [[update_config()]] - code - backend/main.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Config_Update__Shutdown
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_Backend Module Entry Points]]
- 2 edges to [[_COMMUNITY_Main API Routes]]

## Top bridge nodes
- [[update_config()]] - degree 5, connects to 2 communities
- [[shutdown_server()]] - degree 3, connects to 1 community