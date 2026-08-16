---
type: community
members: 2
---

# Component Lifetime Status Write

**Members:** 2 nodes

## Members
- [[dot-write_component_lifetime_status()]] - code - backend/database_manager.py
- [[Method to update component lifetime status in database]] - rationale - backend/database_manager.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Component_Lifetime_Status_Write
SORT file.name ASC
```

## Connections to other communities
- 1 edge to [[_COMMUNITY_Database Manager Core]]

## Top bridge nodes
- [[dot-write_component_lifetime_status()]] - degree 2, connects to 1 community