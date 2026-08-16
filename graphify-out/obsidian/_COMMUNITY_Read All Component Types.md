---
type: community
members: 2
---

# Read All Component Types

**Members:** 2 nodes

## Members
- [[dot-read_all_component_types()]] - code - backend/database_manager.py
- [[Method to read and sort content of component_types table]] - rationale - backend/database_manager.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Read_All_Component_Types
SORT file.name ASC
```

## Connections to other communities
- 1 edge to [[_COMMUNITY_Database Manager Core]]

## Top bridge nodes
- [[dot-read_all_component_types()]] - degree 2, connects to 1 community