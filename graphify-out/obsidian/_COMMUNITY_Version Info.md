---
type: community
members: 3
---

# Version Info

**Members:** 3 nodes

## Members
- [[Function to get latest version number and commit hash]] - rationale - backend/version.py
- [[get_git_info()]] - code - backend/version.py
- [[version.py]] - code - backend/version.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Version_Info
SORT file.name ASC
```
