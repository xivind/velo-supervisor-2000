---
type: community
members: 4
---

# Workplan Table Filtering JS

**Members:** 4 nodes

## Members
- [[initializeWorkplanTable()]] - code - frontend/static/js/main.js
- [[setupWorkplanSearch()]] - code - frontend/static/js/main.js
- [[setupWorkplanStatusFiltering()]] - code - frontend/static/js/main.js
- [[updateWorkplansVisibility()]] - code - frontend/static/js/main.js

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Workplan_Table_Filtering_JS
SORT file.name ASC
```

## Connections to other communities
- 4 edges to [[_COMMUNITY_Frontend JS Core]]
- 1 edge to [[_COMMUNITY_Table Sorting & Search JS]]

## Top bridge nodes
- [[initializeWorkplanTable()]] - degree 4, connects to 2 communities
- [[setupWorkplanSearch()]] - degree 3, connects to 1 community
- [[setupWorkplanStatusFiltering()]] - degree 3, connects to 1 community
- [[updateWorkplansVisibility()]] - degree 3, connects to 1 community