---
type: community
members: 6
---

# Component Data Access

**Members:** 6 nodes

## Members
- [[dot-read_component()]] - code - backend/database_manager.py
- [[dot-read_component_names()]] - code - backend/database_manager.py
- [[dot-write_component_details()]] - code - backend/database_manager.py
- [[Method to create or update component data to the database]] - rationale - backend/database_manager.py
- [[Method to get component names based on list of ids]] - rationale - backend/database_manager.py
- [[Method to retrieve record for a specific component]] - rationale - backend/database_manager.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Component_Data_Access
SORT file.name ASC
```

## Connections to other communities
- 3 edges to [[_COMMUNITY_Database Manager Core]]
- 1 edge to [[_COMMUNITY_Single-Record Reads]]

## Top bridge nodes
- [[dot-read_component()]] - degree 5, connects to 2 communities
- [[dot-read_component_names()]] - degree 3, connects to 1 community
- [[dot-write_component_details()]] - degree 3, connects to 1 community