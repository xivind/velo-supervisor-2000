---
type: community
members: 6
---

# Details Page Endpoints

**Members:** 6 nodes

## Members
- [[Endpoint for bike details page]] - rationale - backend/main.py
- [[Endpoint for component details page]] - rationale - backend/main.py
- [[Function to get button order for a specific page with defaults]] - rationale - backend/utils.py
- [[bike_details()]] - code - backend/main.py
- [[component_details()]] - code - backend/main.py
- [[get_button_order()]] - code - backend/utils.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Details_Page_Endpoints
SORT file.name ASC
```

## Connections to other communities
- 4 edges to [[_COMMUNITY_Page Endpoint Handlers]]
- 2 edges to [[_COMMUNITY_Main API Routes]]
- 1 edge to [[_COMMUNITY_Backend Module Entry Points]]

## Top bridge nodes
- [[bike_details()]] - degree 5, connects to 2 communities
- [[component_details()]] - degree 5, connects to 2 communities
- [[get_button_order()]] - degree 4, connects to 1 community