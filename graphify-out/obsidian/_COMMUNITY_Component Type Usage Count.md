---
type: community
members: 2
---

# Component Type Usage Count

**Members:** 2 nodes

## Members
- [[dot-count_component_types_in_use()]] - code - backend/database_manager.py
- [[Method to count how many components that references a given component type]] - rationale - backend/database_manager.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Component_Type_Usage_Count
SORT file.name ASC
```

## Connections to other communities
- 1 edge to [[_COMMUNITY_Database Manager Core]]

## Top bridge nodes
- [[dot-count_component_types_in_use()]] - degree 2, connects to 1 community