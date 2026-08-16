---
type: community
members: 20
---

# Workplan Business Logic

**Members:** 20 nodes

## Members
- [[dot-get_workplan_details()]] - code - backend/business_logic.py
- [[dot-workplan_check_component_services()]] - code - backend/business_logic.py
- [[dot-workplan_get_linkable_incidents()]] - code - backend/business_logic.py
- [[Build dictionary mapping workplan_id - workplan_name for all workplans]] - rationale - backend/utils.py
- [[Build standard incident data tuple for display (15 fields)]] - rationale - backend/utils.py
- [[Function to load a JSON string and return the parsed data as a python object]] - rationale - backend/utils.py
- [[Generate a concise title for a workplan]] - rationale - backend/utils.py
- [[Generate a concise title for an incident]] - rationale - backend/utils.py
- [[Method to check if all affected components have linked services]] - rationale - backend/business_logic.py
- [[Method to get incidents that can be linked to a workplan]] - rationale - backend/business_logic.py
- [[Method to produce payload for workplan details page]] - rationale - backend/business_logic.py
- [[Parse checkbox progress from markdown description]] - rationale - backend/utils.py
- [[Strip markdown syntax from text to produce clean plain text]] - rationale - backend/utils.py
- [[generate_incident_title()]] - code - backend/utils.py
- [[generate_workplan_title()]] - code - backend/utils.py
- [[get_incident_data_tuple()]] - code - backend/utils.py
- [[get_workplan_names_dict()]] - code - backend/utils.py
- [[parse_checkbox_progress()]] - code - backend/utils.py
- [[parse_json_string()]] - code - backend/utils.py
- [[strip_markdown_syntax()]] - code - backend/utils.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Workplan_Business_Logic
SORT file.name ASC
```

## Connections to other communities
- 11 edges to [[_COMMUNITY_Bike & Component Queries]]
- 7 edges to [[_COMMUNITY_Backend Module Entry Points]]
- 4 edges to [[_COMMUNITY_Component Status Updates]]
- 3 edges to [[_COMMUNITY_Business Logic Core]]

## Top bridge nodes
- [[dot-get_workplan_details()]] - degree 14, connects to 3 communities
- [[get_incident_data_tuple()]] - degree 10, connects to 3 communities
- [[get_workplan_names_dict()]] - degree 7, connects to 2 communities
- [[generate_workplan_title()]] - degree 6, connects to 2 communities
- [[parse_json_string()]] - degree 6, connects to 2 communities