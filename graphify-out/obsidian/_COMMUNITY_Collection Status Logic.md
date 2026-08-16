---
type: community
members: 12
---

# Collection Status Logic

**Members:** 12 nodes

## Members
- [[dot-calculate_collection_status()]] - code - backend/business_logic.py
- [[dot-change_collection_status()]] - code - backend/business_logic.py
- [[dot-get_all_collections()]] - code - backend/business_logic.py
- [[dot-get_collection_details()]] - code - backend/business_logic.py
- [[dot-update_collection()]] - code - backend/business_logic.py
- [[dot-validate_collection()]] - code - backend/business_logic.py
- [[Calculate status flags for a collection based on its components.]] - rationale - backend/business_logic.py
- [[Method to change status of all components in a collection]] - rationale - backend/business_logic.py
- [[Method to produce payload for collection details page]] - rationale - backend/business_logic.py
- [[Method to produce payload for displaying table of all collections]] - rationale - backend/business_logic.py
- [[Method to update collection]] - rationale - backend/business_logic.py
- [[Method to validate collections before allowing bulk operations]] - rationale - backend/business_logic.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Collection_Status_Logic
SORT file.name ASC
```

## Connections to other communities
- 6 edges to [[_COMMUNITY_Business Logic Core]]
- 3 edges to [[_COMMUNITY_Bike & Component Queries]]
- 2 edges to [[_COMMUNITY_Creation & Validation Logic]]

## Top bridge nodes
- [[dot-calculate_collection_status()]] - degree 7, connects to 2 communities
- [[dot-change_collection_status()]] - degree 5, connects to 2 communities
- [[dot-get_all_collections()]] - degree 5, connects to 2 communities
- [[dot-get_collection_details()]] - degree 4, connects to 2 communities
- [[dot-update_collection()]] - degree 3, connects to 1 community