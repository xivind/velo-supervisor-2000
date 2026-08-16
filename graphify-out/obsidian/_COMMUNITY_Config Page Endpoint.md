---
type: community
members: 4
---

# Config Page Endpoint

**Members:** 4 nodes

## Members
- [[Endpoint for component types page]] - rationale - backend/main.py
- [[Function to get button sorting configuration for config page]] - rationale - backend/utils.py
- [[config_overview()]] - code - backend/main.py
- [[get_button_sorting_config()]] - code - backend/utils.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Config_Page_Endpoint
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_Page Endpoint Handlers]]
- 1 edge to [[_COMMUNITY_Main API Routes]]
- 1 edge to [[_COMMUNITY_Backend Module Entry Points]]

## Top bridge nodes
- [[config_overview()]] - degree 5, connects to 2 communities
- [[get_button_sorting_config()]] - degree 3, connects to 1 community