---
type: community
members: 16
---

# Creation & Validation Logic

**Members:** 16 nodes

## Members
- [[dot-create_collection()]] - code - backend/business_logic.py
- [[dot-create_component()]] - code - backend/business_logic.py
- [[dot-create_history_record()]] - code - backend/business_logic.py
- [[dot-create_incident_record()]] - code - backend/business_logic.py
- [[dot-process_bike_compliance_report()]] - code - backend/business_logic.py
- [[dot-quick_swap_orchestrator()]] - code - backend/business_logic.py
- [[dot-validate_quick_swap()]] - code - backend/business_logic.py
- [[Function to generates a random and unique ID]] - rationale - backend/utils.py
- [[Method to add incident record]] - rationale - backend/business_logic.py
- [[Method to check if a bike has all mandatory components and respects max…]] - rationale - backend/business_logic.py
- [[Method to create collection]] - rationale - backend/business_logic.py
- [[Method to create component]] - rationale - backend/business_logic.py
- [[Method to create installation history record]] - rationale - backend/business_logic.py
- [[Method to orchestrate swap of one component with another]] - rationale - backend/business_logic.py
- [[Method to validate quick swap operation]] - rationale - backend/business_logic.py
- [[generate_unique_id()]] - code - backend/utils.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Creation__Validation_Logic
SORT file.name ASC
```

## Connections to other communities
- 9 edges to [[_COMMUNITY_Business Logic Core]]
- 3 edges to [[_COMMUNITY_Record Update & Refresh Logic]]
- 2 edges to [[_COMMUNITY_Collection Status Logic]]
- 2 edges to [[_COMMUNITY_Service Record Validation]]
- 2 edges to [[_COMMUNITY_Bike & Component Queries]]
- 1 edge to [[_COMMUNITY_Component Status Updates]]
- 1 edge to [[_COMMUNITY_Backend Module Entry Points]]

## Top bridge nodes
- [[dot-create_history_record()]] - degree 9, connects to 4 communities
- [[dot-create_component()]] - degree 9, connects to 3 communities
- [[generate_unique_id()]] - degree 8, connects to 3 communities
- [[dot-process_bike_compliance_report()]] - degree 7, connects to 3 communities
- [[dot-create_collection()]] - degree 4, connects to 2 communities