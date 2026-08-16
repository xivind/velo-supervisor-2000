---
type: community
members: 9
---

# APScheduler Jobs

**Members:** 9 nodes

## Members
- [[Gracefully shutdown the APScheduler instance]] - rationale - backend/scheduler.py
- [[Initialize and start the APScheduler instance]] - rationale - backend/scheduler.py
- [[Scheduled job to sync Strava activities]] - rationale - backend/scheduler.py
- [[Scheduled job to update time-based status fields for all non-retired components]] - rationale - backend/scheduler.py
- [[scheduler.py]] - code - backend/scheduler.py
- [[start_scheduler()]] - code - backend/scheduler.py
- [[stop_scheduler()]] - code - backend/scheduler.py
- [[strava_sync_job()]] - code - backend/scheduler.py
- [[update_time_based_fields_job()]] - code - backend/scheduler.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/APScheduler_Jobs
SORT file.name ASC
```

## Connections to other communities
- 3 edges to [[_COMMUNITY_Main API Routes]]
- 2 edges to [[_COMMUNITY_Business Logic Core]]
- 1 edge to [[_COMMUNITY_Backend Module Entry Points]]

## Top bridge nodes
- [[scheduler.py]] - degree 6, connects to 2 communities
- [[start_scheduler()]] - degree 5, connects to 1 community
- [[strava_sync_job()]] - degree 4, connects to 1 community
- [[update_time_based_fields_job()]] - degree 4, connects to 1 community
- [[stop_scheduler()]] - degree 3, connects to 1 community