---
type: community
members: 12
---

# Single-Record Reads

**Members:** 12 nodes

## Members
- [[dot-read_single_collection()]] - code - backend/database_manager.py
- [[dot-read_single_history_record()]] - code - backend/database_manager.py
- [[dot-read_single_incident_report()]] - code - backend/database_manager.py
- [[dot-read_single_service_record()]] - code - backend/database_manager.py
- [[dot-read_single_workplan()]] - code - backend/database_manager.py
- [[dot-write_delete_record()]] - code - backend/database_manager.py
- [[Method to delete a given record and associated records_1]] - rationale - backend/database_manager.py
- [[Method to retrieve a specific service record]] - rationale - backend/database_manager.py
- [[Method to retrieve record for a specific collection]] - rationale - backend/database_manager.py
- [[Method to retrieve record for a specific entry in the installation log]] - rationale - backend/database_manager.py
- [[Method to retrieve record for a specific incident report]] - rationale - backend/database_manager.py
- [[Method to retrieve record for a specific workplan]] - rationale - backend/database_manager.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Single-Record_Reads
SORT file.name ASC
```

## Connections to other communities
- 6 edges to [[_COMMUNITY_Database Manager Core]]
- 1 edge to [[_COMMUNITY_Component Type Data Access]]
- 1 edge to [[_COMMUNITY_Component Data Access]]

## Top bridge nodes
- [[dot-write_delete_record()]] - degree 9, connects to 3 communities
- [[dot-read_single_collection()]] - degree 3, connects to 1 community
- [[dot-read_single_history_record()]] - degree 3, connects to 1 community
- [[dot-read_single_incident_report()]] - degree 3, connects to 1 community
- [[dot-read_single_service_record()]] - degree 3, connects to 1 community