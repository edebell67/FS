# TASK C3: Implement Signals History Endpoint

**Workstream:** C - API LAYER
**Epic:** Autonomous Trading Signal Platform
**Status:** [ ] Awaiting User Verification

## Source

- [Autonomous Trading Signal Platform](C:\Users\edebe\eds\workstream\epic\Autonomous Trading Signal Platform.md)
- Prior dependency: `C:\Users\edebe\eds\workstream\300_complete\20260309_120011_workstreamB_build_signal_sync_service.md`

## Task Summary

Implement `GET /signals/history` on the shared FastAPI server so clients can retrieve persisted publishable signal history from the online database using the same public payload contract as the latest-signals endpoint.

## Context

- The base API app lives in `api_server.py` and already exposes `GET /signals/latest`.
- The online persistence contract for signals is defined in `online_db_schema.sql`.
- Signal payload expectations are defined in `json/publishable_signal_schema.json`.
- API tests live in `tests/test_api_server.py` and already use repository injection to avoid live database dependencies.

## Plan

- [x] 1. Confirm the endpoint contract and update this lifecycle file before code edits.
  - [x] Test: Review `workstream/epic/Autonomous Trading Signal Platform.md`, `api_server.py`, `online_db_schema.sql`, and `json/publishable_signal_schema.json`; pass if this file records the endpoint path, payload shape, and test strategy.
  - Evidence: Reviewed the epic, current API server, online schema, and publishable signal contract; confirmed `GET /signals/history` should return persisted signal rows in the same public payload shape as `/signals/latest`, with repository-injected tests used to avoid a live database dependency.
- [x] 2. Implement `GET /signals/history` in `api_server.py` with repository-backed retrieval of persisted signal history.
  - [x] Test: `python -m pytest tests/test_api_server.py -q`; pass if the API suite covers the new endpoint successfully.
  - Evidence: Added repository-backed history retrieval in `api_server.py` and extended `tests/test_api_server.py` with a deterministic `/signals/history` test. Validation passed with `5 passed in 17.63s`.
- [x] 3. Run a route smoke validation and record the result in this task file.
  - [x] Test: `python -c "from api_server import app; print('signals_history=' + str(any(getattr(route, 'path', None) == '/signals/history' for route in app.routes)))"`; pass if the command prints `signals_history=True`.
  - Evidence: Smoke validation passed and printed `signals_history=True`.

## Implementation Log

- 2026-03-09 12:00:22+00:00 - Task file created in `workstream/200_inprogress/gemini`.
- 2026-03-09 18:18:00+00:00 - Read `skills/workstream-task-lifecycle/SKILL.md`, the assigned task stub, and prerequisite schema/sync/API artifacts.
- 2026-03-09 18:20:00+00:00 - Replaced the stub task record with the required lifecycle structure and ordered checklist before editing code.
- 2026-03-09 18:24:00+00:00 - Updated `api_server.py` to extend the signal repository contract with history retrieval, added paged PostgreSQL-backed history fetching, and registered `GET /signals/history`.
- 2026-03-09 18:26:00+00:00 - Extended `tests/test_api_server.py` with a fake-repository test covering `/signals/history` limit and offset handling without requiring a live database.
- 2026-03-09 18:28:00+00:00 - Ran `python -m pytest tests/test_api_server.py -q`; the focused API suite passed with `5 passed in 17.63s`.
- 2026-03-09 18:29:00+00:00 - Ran the route smoke check; it passed and confirmed `/signals/history` is registered on the FastAPI app.

## Changes Made

- Updated `C:\Users\edebe\eds\api_server.py`
  - Extended the `LatestSignalRepository` protocol with `fetch_signal_history(limit, offset)`.
  - Refactored `PostgresLatestSignalRepository` so latest-signal reads reuse a shared history query path.
  - Added paged PostgreSQL-backed signal history retrieval ordered by `published_at DESC, signal_timestamp DESC`.
  - Added `GET /signals/history` with `limit` and `offset` query parameters, returning the same `LatestSignalPayload` schema as `/signals/latest`.
- Updated `C:\Users\edebe\eds\tests\test_api_server.py`
  - Added a repository-injected endpoint test for `/signals/history`.
  - Verified the route forwards `limit` and `offset` and serializes the public signal payload shape correctly.

## Validation

- Executed:
  - `python -m pytest tests/test_api_server.py -q`
  - `python -c "from api_server import app; print('signals_history=' + str(any(getattr(route, 'path', None) == '/signals/history' for route in app.routes)))"`
- Result:
  - Pass. `pytest` output: `5 passed in 17.63s`
  - Pass. Smoke output: `signals_history=True`
- User verification request:
  - Please verify whether `GET /signals/history` returns the signal history rows you expect, including correct ordering and the publishable fields `signal_id`, `timestamp`, `asset`, `direction`, `entry`, `tp`, `sl`, `strategy`, and `confidence`.

## Risks/Notes

- User verification will be required before this task can move to `workstream/300_complete` because `/signals/history` is a user-visible API behavior.

## Completion Status

Awaiting user verification as of 2026-03-09 18:29:00+00:00. Implementation and technical validation are complete; final completion and move to `workstream/300_complete` require user pass/fail confirmation for `/signals/history`.


## Execution Evidence
- Agent lane: gemini
- Command: C:\Users\edebe\AppData\Roaming\npm\codex.CMD exec -C C:\Users\edebe\eds Execute this task file end-to-end. Read and follow C:\Users\edebe\eds\skills\workstream-task-lifecycle\SKILL.md first. Task file: C:\Users\edebe\eds\workstream\200_inprogress/gemini\20260309_120022_workstreamC_implement_signals_history_endpoint.md. Implement required changes in the workspace, run validations, and update checklist items.
- Return code: 0
- Stdout:
```text
Implemented `GET /signals/history` in [api_server.py](/C:/Users/edebe/eds/api_server.py). It now uses the same public payload shape as `/signals/latest`, adds paged history retrieval via `limit` and `offset`, and reads persisted signals ordered by `published_at DESC, signal_timestamp DESC`. I also added endpoint coverage in [tests/test_api_server.py](/C:/Users/edebe/eds/tests/test_api_server.py) and updated the lifecycle record in [20260309_120022_workstreamC_implement_signals_history_endpoint.md](/C:/Users/edebe/eds/workstream/200_inprogress/gemini/20260309_120022_workstreamC_implement_signals_history_endpoint.md).

Validation passed:
`python -m pytest tests/test_api_server.py -q` -> `5 passed in 17.63s`
`python -c "from api_server import app; ..."` -> `signals_history=True`

Per the lifecycle workflow, this task is now awaiting user verification. Please verify that `GET /signals/history` returns the expected signal history rows, with correct ordering and fields: `signal_id`, `timestamp`, `asset`, `direction`, `entry`, `tp`, `sl`, `strategy`, and `confidence`.
```
- Stderr:
```text
r, online schema, and publishable signal contract; confirmed `GET /signals/history` should return persisted signal rows in the same public payload shape as `/signals/latest`, with repository-injected tests used to avoid a live database dependency.
+- [x] 2. Implement `GET /signals/history` in `api_server.py` with repository-backed retrieval of persisted signal history.
+  - [x] Test: `python -m pytest tests/test_api_server.py -q`; pass if the API suite covers the new endpoint successfully.
+  - Evidence: Added repository-backed history retrieval in `api_server.py` and extended `tests/test_api_server.py` with a deterministic `/signals/history` test. Validation passed with `5 passed in 17.63s`.
+- [x] 3. Run a route smoke validation and record the result in this task file.
+  - [x] Test: `python -c "from api_server import app; print('signals_history=' + str(any(getattr(route, 'path', None) == '/signals/history' for route in app.routes)))"`; pass if the command prints `signals_history=True`.
+  - Evidence: Smoke validation passed and printed `signals_history=True`.
+
+## Implementation Log
+
+- 2026-03-09 12:00:22+00:00 - Task file created in `workstream/200_inprogress/gemini`.
+- 2026-03-09 18:18:00+00:00 - Read `skills/workstream-task-lifecycle/SKILL.md`, the assigned task stub, and prerequisite schema/sync/API artifacts.
+- 2026-03-09 18:20:00+00:00 - Replaced the stub task record with the required lifecycle structure and ordered checklist before editing code.
+- 2026-03-09 18:24:00+00:00 - Updated `api_server.py` to extend the signal repository contract with history retrieval, added paged PostgreSQL-backed history fetching, and registered `GET /signals/history`.
+- 2026-03-09 18:26:00+00:00 - Extended `tests/test_api_server.py` with a fake-repository test covering `/signals/history` limit and offset handling without requiring a live database.
+- 2026-03-09 18:28:00+00:00 - Ran `python -m pytest tests/test_api_server.py -q`; the focused API suite passed with `5 passed in 17.63s`.
+- 2026-03-09 18:29:00+00:00 - Ran the route smoke check; it passed and confirmed `/signals/history` is registered on the FastAPI app.
+
+## Changes Made
+
+- Updated `C:\Users\edebe\eds\api_server.py`
+  - Extended the `LatestSignalRepository` protocol with `fetch_signal_history(limit, offset)`.
+  - Refactored `PostgresLatestSignalRepository` so latest-signal reads reuse a shared history query path.
+  - Added paged PostgreSQL-backed signal history retrieval ordered by `published_at DESC, signal_timestamp DESC`.
+  - Added `GET /signals/history` with `limit` and `offset` query parameters, returning the same `LatestSignalPayload` schema as `/signals/latest`.
+- Updated `C:\Users\edebe\eds\tests\test_api_server.py`
+  - Added a repository-injected endpoint test for `/signals/history`.
+  - Verified the route forwards `limit` and `offset` and serializes the public signal payload shape correctly.
+
+## Validation
+
+- Executed:
+  - `python -m pytest tests/test_api_server.py -q`
+  - `python -c "from api_server import app; print('signals_history=' + str(any(getattr(route, 'path', None) == '/signals/history' for route in app.routes)))"`
+- Result:
+  - Pass. `pytest` output: `5 passed in 17.63s`
+  - Pass. Smoke output: `signals_history=True`
+- User verification request:
+  - Please verify whether `GET /signals/history` returns the signal history rows you expect, including correct ordering and the publishable fields `signal_id`, `timestamp`, `asset`, `direction`, `entry`, `tp`, `sl`, `strategy`, and `confidence`.
+
+## Risks/Notes
+
+- User verification will be required before this task can move to `workstream/300_complete` because `/signals/history` is a user-visible API behavior.
+
+## Completion Status
+
+Awaiting user verification as of 2026-03-09 18:29:00+00:00. Implementation and technical validation are complete; final completion and move to `workstream/300_complete` require user pass/fail confirmation for `/signals/history`.

tokens used
126,389
```

# User Feedback
User Verified: PASS
