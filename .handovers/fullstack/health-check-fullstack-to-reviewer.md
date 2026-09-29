# Fullstack Developer -> Code Reviewer Handover

**Feature/Task:** Health check for the Docker daemon (#103)
**Date:** 2026-09-27
**Status:** Complete, not committed (human reviews first)

## Context
Docker needs a health status for the whole app, which Portainer and the dashboard read from the Docker API. The app catches almost every failure and still answers 200/303, so HTTP status codes say little. Health is therefore based on errors the app logs, kept in memory for 24 hours, plus a database read. Design decisions are recorded in #103 (comment of 2026-09-27). Implemented guided, not by the agent.

## Deliverables
- `backend/business_logic.py`: 15 `logging.error` calls changed to `logging.warning`. Only the logging call changed. Validation rejections at 1484, 1537, 1792, 2166, 2213, 2329, 2408, 2439, and callers repeating a child failure at 1348, 1819, 1841, 1858, 2079, 2133, 2289.
- `backend/utils.py:170-205`: `ErrorRecorder` logging handler, `ERROR_RECORDER` instance, `get_health_status(database_success, database_message)`.
- `backend/database_manager.py:24-33`: `check_database_connection()`, renamed from `read_database_connection` after review since it returns a `(success, message)` tuple rather than data.
- `backend/business_logic.py:3399-3401`: `check_database_connection()`, a pass-through so the route goes through business logic like every other route.
- `backend/main.py:30`: recorder added to the root logger. `main.py:808-814`: `GET /health`, returns 200 or 503 with a JSON body.
- `backend/healthcheck.py`: new file. Script run by Docker. Prints the `/health` body; exit code 0 means healthy, 1 means unhealthy or unreachable.
- `DOCKERFILE:31-32`: `HEALTHCHECK --interval=600s --timeout=5s --retries=3 CMD ["python", "healthcheck.py"]`.
- `tests/test_health.py`: new file, 7 tests.

## Decisions Made
1. **Log level rule:** ERROR means something failed and is logged once, where it fails. WARNING means the request was rejected on purpose, or a caller is repeating a failure already logged below it. Toasts and modals use return values, not log levels, so users see no change. The only visible change is the colour in the config page log viewer.
2. **In memory, not the log file:** the log rotates at 10 KB x 3, so it can't answer "any error in the last 24 hours". A container restart clears the state (accepted).
3. **The handler filters on `record.levelno` in `emit()`:** `lifespan` in `main.py` resets the level of every root handler to INFO or DEBUG, so a handler level would not hold.
4. **The database check reads the `bikes` table, not `SELECT 1`:** `SELECT 1` succeeds on a corrupt file and on a missing file (SQLite creates an empty one, e.g. on a wrong Docker mount). Verified with `sqlite3` against both cases.
5. **`get_health_status` is in `utils.py`, the database read in `database_manager.py`:** `utils` can't import `database_manager` (circular), so the database result is passed in as a parameter.
6. **A separate check script instead of `curl`:** `python:3.12-slim` has no curl. Printing the body on a 503 needs `try/except`, which doesn't fit in `python -c`.
7. **Exception type in messages:** for `logging.exception` records, the recorder appends the exception type and text. Otherwise the middleware's 500s would only show "An error occurred" in Portainer.

## Next Steps for Code Reviewer
1. Check that the 15 changed lines are exactly groups A and B from #103 (`git diff backend/business_logic.py`).
2. Review thread safety: `emit()` runs under the handler lock, and `read_recent_errors` takes the same lock.
3. Run `uv run pytest -q`; 32 tests should pass.

## Verification done
- `uv run pytest -q`: 32 passed (25 existing, 7 new).
- End-to-end with the production log config (`uvicorn_log_config.ini`, log path redirected) against a migrated copy of the production DB:
  - fresh start: healthy, exit 0
  - mistyped date: still healthy, logged as WARNING twice
  - `/bike_details/nope`: unhealthy with the `AttributeError`, exit 1
  - broken Strava token and manual sync: unhealthy with both Strava errors. The sync itself still returns 200, the known silent failure.
  - app stopped: "Health endpoint not reachable", exit 1
- With the ini log config, the `uvicorn`, `uvicorn.error` and `uvicorn.access` loggers propagate to root, so uvicorn's own errors reach the recorder too.
- Not verified: the Docker build itself, since Docker isn't installed on the dev machine. Run `./create-container-vs2000.sh` and check `docker inspect --format '{{json .State.Health}}' velo-supervisor-2000` after 10 minutes.

## Blockers / Open Questions
- Known limitations, accepted in #103: a stale ID gives a 500 and marks the container unhealthy for 24 hours (fix tracked in #356). Silent failures, e.g. a dead scheduler, are not detected.
- The container shows `starting` for the first 600s. `--start-period`/`--start-interval` would shorten this but need Docker Engine 25+. Left out.

## References
- Issue #103 (decisions comment), #356 (404 for stale IDs)
