---
type: community
members: 4
---

# Component Type Data Access

**Members:** 4 nodes

## Members
- [[dot-read_single_component_type()]] - code - backend/database_manager.py
- [[dot-write_component_type()]] - code - backend/database_manager.py
- [[Method to retrieve record for a single component type]] - rationale - backend/database_manager.py
- [[Method to write component type record in database]] - rationale - backend/database_manager.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Component_Type_Data_Access
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_Database Manager Core]]
- 1 edge to [[_COMMUNITY_Single-Record Reads]]

## Top bridge nodes
- [[dot-read_single_component_type()]] - degree 4, connects to 2 communities
- [[dot-write_component_type()]] - degree 3, connects to 1 community