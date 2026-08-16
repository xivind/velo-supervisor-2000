---
type: community
members: 14
---

# Service Record Validation

**Members:** 14 nodes

## Members
- [[dot-bulk_create_service_records()]] - code - backend/business_logic.py
- [[dot-create_service_record()]] - code - backend/business_logic.py
- [[dot-update_history_record()]] - code - backend/business_logic.py
- [[dot-update_service_record()]] - code - backend/business_logic.py
- [[dot-validate_history_record()]] - code - backend/business_logic.py
- [[dot-validate_service_record()]] - code - backend/business_logic.py
- [[Function to validate that a date string matches the required format YYYY-MM-DD…]] - rationale - backend/utils.py
- [[Method to add service record]] - rationale - backend/business_logic.py
- [[Method to bulk create service records for multiple components linked to a…]] - rationale - backend/business_logic.py
- [[Method to update a component history record with validation]] - rationale - backend/business_logic.py
- [[Method to update a service record]] - rationale - backend/business_logic.py
- [[Method to validate history records before processing and storing in database]] - rationale - backend/business_logic.py
- [[Method to validate service records before processing and storing in database]] - rationale - backend/business_logic.py
- [[validate_date_format()]] - code - backend/utils.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Service_Record_Validation
SORT file.name ASC
```

## Connections to other communities
- 6 edges to [[_COMMUNITY_Business Logic Core]]
- 3 edges to [[_COMMUNITY_Record Update & Refresh Logic]]
- 2 edges to [[_COMMUNITY_Creation & Validation Logic]]
- 1 edge to [[_COMMUNITY_Backend Module Entry Points]]

## Top bridge nodes
- [[dot-create_service_record()]] - degree 6, connects to 3 communities
- [[dot-validate_history_record()]] - degree 5, connects to 2 communities
- [[dot-update_history_record()]] - degree 4, connects to 2 communities
- [[dot-update_service_record()]] - degree 4, connects to 2 communities
- [[dot-validate_service_record()]] - degree 5, connects to 1 community