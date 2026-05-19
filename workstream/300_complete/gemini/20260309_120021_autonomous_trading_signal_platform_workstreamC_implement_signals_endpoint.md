# TASK C2: Implement Signals Endpoint

**Workstream:** C - API LAYER
**Epic:** Autonomous Trading Signal Platform
**Status:** [ ] Awaiting User Verification

## Source

- [Autonomous Trading Signal Platform](C:\Users\edebe\eds\workstream\epic\Autonomous Trading Signal Platform.md)
- Prior dependency: `C:\Users\edebe\eds\workstream\200_inprogress\gemini\20260309_120020_workstreamC_create_api_server.md`
- Prior dependency: `C:\Users\edebe\eds\workstream\300_complete\20260309_120011_workstreamB_build_signal_sync_service.md`

## Task Summary

Implement `GET /signals/latest` on the shared FastAPI server so clients can retrieve the most recent publishable trading signals from the online `signals` store using the same schema established by Workstreams A and B.

## Context

- The base FastAPI app exists in `api_server.py` and currently exposes only `/` and `/health`.
- The online persistence contract for signals is defined in `online_db_schema.sql`.
- Signal normalization and field expectations already exist in `sync_engine/signal_sync_service.py` and `json/publishable_signal_schema.json`.
- This task needs a testable repository abstraction so API tests do not require a live PostgreSQL instance.

## Plan

- [x] 1. Confirm the endpoint contract and lifecycle record before code changes.
  - [x] Test: Review `workstream/epic/Autonomous Trading Signal Platform.md`, `api_server.py`, `online_db_schema.sql`, and `sync_engine/signal_sync_service.py`; pass if this file records the endpoint path, payload source, and test strategy.
  - Evidence: Reviewed the epic plus current API/sync/schema files and confirmed the endpoint contract as `GET /signals/latest`, backed by persisted online `signals` rows joined to `strategies`, with repository injection used so tests do not require PostgreSQL.
- [x] 2. Implement `GET /signals/latest` in `api_server.py` with a repository abstraction that returns latest persisted signals.
  - [x] Test: `python -m pytest tests/test_api_server.py -q`; pass if endpoint coverage succeeds alongside the existing health test.
  - Evidence: Added `LatestSignalPayload`, `LatestSignalRepository`, `PostgresLatestSignalRepository`, and the `/signals/latest` route in `api_server.py`; extended `tests/test_api_server.py` with a fake-repository endpoint test. Validation passed with `4 passed in 1.45s`.
- [x] 3. Run an import and route smoke validation for the new endpoint and record the output.
  - [x] Test: `python -c "from api_server import app; print('signals_latest=' + str(any(getattr(route, 'path', None) == '/signals/latest' for route in app.routes)))"`; pass if the command prints `signals_latest=True`.
  - Evidence: Smoke validation passed and printed `signals_latest=True`.

## Implementation Log

- 2026-03-09 18:00:00+00:00 - Read `skills/workstream-task-lifecycle/SKILL.md`, the assigned C2 task stub, the prerequisite C1/B2 lifecycle files, and the current API/sync artifacts.
- 2026-03-09 18:02:00+00:00 - Replaced the stub task file with the required lifecycle structure and ordered checklist before editing application code.
- 2026-03-09 18:08:00+00:00 - Reviewed the live `api_server.py` and found it had already been extended by another in-progress task, so the C2 endpoint was added without reverting or replacing that existing work.
- 2026-03-09 18:11:00+00:00 - Added repository-backed latest-signal retrieval in `api_server.py`, including a PostgreSQL implementation, request-time repository resolution, and response serialization for publishable signal payloads.
- 2026-03-09 18:13:00+00:00 - Extended `tests/test_api_server.py` with a deterministic `/signals/latest` test using an injected fake repository while preserving the existing monitoring and health tests.
- 2026-03-09 18:14:00+00:00 - Ran the focused API test suite and hit a failing pre-existing monitoring test fixture due to a schema path assumption inside the temporary sync config.
- 2026-03-09 18:16:00+00:00 - Corrected the temporary test fixture to use an absolute schema path, reran the test suite successfully, then removed a Pydantic deprecation warning by switching to a field serializer for Decimal JSON output.
- 2026-03-09 18:17:00+00:00 - Ran the final focused validations: pytest passed and the route smoke check confirmed `/signals/latest` is registered.

## Changes Made

- Updated `C:\Users\edebe\eds\api_server.py`
  - Added `LatestSignalPayload` for the public `/signals/latest` response contract.
  - Added a `LatestSignalRepository` protocol plus `PostgresLatestSignalRepository` that reads the newest persisted signals from `signals` joined to `strategies`, ordered by `published_at` and `signal_timestamp`.
  - Added `_get_signal_repository()` so tests and future integrations can inject a repository without modifying route code.
  - Added `GET /signals/latest` with an optional `limit` query parameter constrained to `1..100`, defaulting to `20`.
  - Added Decimal field serialization for JSON responses without using deprecated Pydantic configuration.
- Updated `C:\Users\edebe\eds\tests\test_api_server.py`
  - Added a repository-injected endpoint test covering `GET /signals/latest`.
  - Fixed the monitoring-summary temporary config fixture to use an absolute schema path so the full focused API suite remains stable.

## Validation

- Executed:
  - `python -m pytest tests/test_api_server.py -q`
  - `python -c "from api_server import app; print('signals_latest=' + str(any(getattr(route, 'path', None) == '/signals/latest' for route in app.routes)))"`
- Result:
  - Pass. `pytest` output: `4 passed in 1.45s`
  - Pass. Smoke output: `signals_latest=True`
- User verification request:
  - Please verify whether `GET /signals/latest` returns the latest signal rows you expect, including `signal_id`, `timestamp`, `asset`, `direction`, `entry`, `tp`, `sl`, `strategy`, and `confidence`.

## Risks/Notes

- User verification will be required before this task can move to `workstream/300_complete` because `GET /signals/latest` is a user-visible API behavior.
- The default repository reads directly from PostgreSQL via environment-configured connection values; if the database is unavailable at runtime, the endpoint will fail until connection details or service availability are corrected.
- This task assumes the online database has already been populated by the Workstream B signal sync flow; otherwise the endpoint will correctly return an empty list.

## Completion Status

Awaiting user verification as of 2026-03-09 18:17:00+00:00. Implementation and technical validation are complete; final completion and move to `workstream/300_complete` require user pass/fail confirmation for the `/signals/latest` behavior.


## Execution Evidence
- Agent lane: gemini
- Command: C:\Users\edebe\AppData\Roaming\npm\codex.CMD exec -C C:\Users\edebe\eds Execute this task file end-to-end. Read and follow C:\Users\edebe\eds\skills\workstream-task-lifecycle\SKILL.md first. Task file: C:\Users\edebe\eds\workstream\200_inprogress/gemini\20260309_120021_workstreamC_implement_signals_endpoint.md. Implement required changes in the workspace, run validations, and update checklist items.
- Return code: 0
- Stdout:
```text
Implemented `GET /signals/latest` in [api_server.py](C:/Users/edebe/eds/api_server.py) with a repository abstraction that reads the newest persisted signals from the online `signals` and `strategies` tables, plus a bounded `limit` query param. I also extended [tests/test_api_server.py](C:/Users/edebe/eds/tests/test_api_server.py) to cover the new endpoint with an injected fake repository and fixed the existing monitoring test fixture.

The lifecycle record is updated in [20260309_120021_workstreamC_implement_signals_endpoint.md](C:/Users/edebe/eds/workstream/200_inprogress/gemini/20260309_120021_workstreamC_implement_signals_endpoint.md) with completed checklist items, evidence, and validation results. Technical validation passed:
`python -m pytest tests/test_api_server.py -q` -> `4 passed in 1.45s`
`python -c "from api_server import app; ..."` -> `signals_latest=True`

This task is left in `Awaiting user verification` per the repo workflow. Please verify whether `GET /signals/latest` returns the latest signal rows you expect with `signal_id`, `timestamp`, `asset`, `direction`, `entry`, `tp`, `sl`, `strategy`, and `confidence`.
```
- Stderr:
```text
tation Log
+
+- 2026-03-09 18:00:00+00:00 - Read `skills/workstream-task-lifecycle/SKILL.md`, the assigned C2 task stub, the prerequisite C1/B2 lifecycle files, and the current API/sync artifacts.
+- 2026-03-09 18:02:00+00:00 - Replaced the stub task file with the required lifecycle structure and ordered checklist before editing application code.
+- 2026-03-09 18:08:00+00:00 - Reviewed the live `api_server.py` and found it had already been extended by another in-progress task, so the C2 endpoint was added without reverting or replacing that existing work.
+- 2026-03-09 18:11:00+00:00 - Added repository-backed latest-signal retrieval in `api_server.py`, including a PostgreSQL implementation, request-time repository resolution, and response serialization for publishable signal payloads.
+- 2026-03-09 18:13:00+00:00 - Extended `tests/test_api_server.py` with a deterministic `/signals/latest` test using an injected fake repository while preserving the existing monitoring and health tests.
+- 2026-03-09 18:14:00+00:00 - Ran the focused API test suite and hit a failing pre-existing monitoring test fixture due to a schema path assumption inside the temporary sync config.
+- 2026-03-09 18:16:00+00:00 - Corrected the temporary test fixture to use an absolute schema path, reran the test suite successfully, then removed a Pydantic deprecation warning by switching to a field serializer for Decimal JSON output.
+- 2026-03-09 18:17:00+00:00 - Ran the final focused validations: pytest passed and the route smoke check confirmed `/signals/latest` is registered.
+
+## Changes Made
+
+- Updated `C:\Users\edebe\eds\api_server.py`
+  - Added `LatestSignalPayload` for the public `/signals/latest` response contract.
+  - Added a `LatestSignalRepository` protocol plus `PostgresLatestSignalRepository` that reads the newest persisted signals from `signals` joined to `strategies`, ordered by `published_at` and `signal_timestamp`.
+  - Added `_get_signal_repository()` so tests and future integrations can inject a repository without modifying route code.
+  - Added `GET /signals/latest` with an optional `limit` query parameter constrained to `1..100`, defaulting to `20`.
+  - Added Decimal field serialization for JSON responses without using deprecated Pydantic configuration.
+- Updated `C:\Users\edebe\eds\tests\test_api_server.py`
+  - Added a repository-injected endpoint test covering `GET /signals/latest`.
+  - Fixed the monitoring-summary temporary config fixture to use an absolute schema path so the full focused API suite remains stable.
+
+## Validation
+
+- Executed:
+  - `python -m pytest tests/test_api_server.py -q`
+  - `python -c "from api_server import app; print('signals_latest=' + str(any(getattr(route, 'path', None) == '/signals/latest' for route in app.routes)))"`
+- Result:
+  - Pass. `pytest` output: `4 passed in 1.45s`
+  - Pass. Smoke output: `signals_latest=True`
+- User verification request:
+  - Please verify whether `GET /signals/latest` returns the latest signal rows you expect, including `signal_id`, `timestamp`, `asset`, `direction`, `entry`, `tp`, `sl`, `strategy`, and `confidence`.
+
+## Risks/Notes
+
+- User verification will be required before this task can move to `workstream/300_complete` because `GET /signals/latest` is a user-visible API behavior.
+- The default repository reads directly from PostgreSQL via environment-configured connection values; if the database is unavailable at runtime, the endpoint will fail until connection details or service availability are corrected.
+- This task assumes the online database has already been populated by the Workstream B signal sync flow; otherwise the endpoint will correctly return an empty list.
+
+## Completion Status
+
+Awaiting user verification as of 2026-03-09 18:17:00+00:00. Implementation and technical validation are complete; final completion and move to `workstream/300_complete` require user pass/fail confirmation for the `/signals/latest` behavior.

tokens used
73,002
```

# User Feedback
User Verified: PASS
