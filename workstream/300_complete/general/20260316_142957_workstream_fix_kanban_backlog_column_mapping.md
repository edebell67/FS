# Task: Fix Kanban Backlog Column Mapping

## Source
- User report with screenshot from `localhost:8080` showing `100_backlog/general` tasks missing from the Backlog column.

## Task Summary
- Fix the kanban board so backlog tasks returned by the API render in the Backlog column instead of being misclassified into Epic.

## Context
- The dashboard API returns the expected task files from `workstream/100_backlog/general`.
- The browser UI shows `Backlog` counts as `0`, which indicates a frontend grouping bug.

## Plan
- [x] 1. Verify whether the issue is in API data or frontend grouping.
  - [x] Test: compare filesystem and API task output with the visible board state.
  - [x] Evidence: backlog files exist on disk and `/api/tasks` returns them while the UI still shows zero in Backlog.
- [x] 2. Patch the kanban folder-to-column mapping for backlog folders.
  - [x] Test: inspect `kanban_dashboard.py` and confirm `100_backlog/*` maps to `100_backlog` instead of `000_epic`.
  - [x] Evidence: updated mapping logic in `kanban_dashboard.py`.
- [x] 3. Validate the updated dashboard code.
  - [x] Test: `python -m py_compile workstream\\kanban_dashboard.py`
  - [x] Evidence: successful compile result recorded in this task file.

## Implementation Log
- 2026-03-16 14:29: Verified backlog task files exist under `workstream/100_backlog/general`.
- 2026-03-16 14:30: Confirmed `http://localhost:8080/api/tasks?startDate=2026-03-16&endDate=2026-03-16` returns the expected backlog tasks.
- 2026-03-16 14:31: Isolated the render bug in `kanban_dashboard.py`: any folder containing `backlog` is being remapped to `000_epic`.
- 2026-03-16 14:33: Patched the folder normalization logic in `getTaskStatusBucket()` and `renderBoard()` so `100_backlog/*` stays mapped to `100_backlog`.
- 2026-03-16 14:34: Ran `python -m py_compile workstream\\kanban_dashboard.py` successfully.
- 2026-03-16 14:39: Verified the live page at `http://localhost:8080` is still serving the old `renderBoard()` script despite the code patch.
- 2026-03-16 14:40: Identified two active Python listeners on `127.0.0.1:8080`, indicating a stale kanban process is still bound alongside the restarted one.
- 2026-03-16 14:42: Stopped the stale Python listener on `127.0.0.1:8080`.
- 2026-03-16 14:43: Re-checked `http://localhost:8080` and confirmed the served page source now contains the patched `100_backlog` mapping logic.

## Changes Made
- Updated `workstream/kanban_dashboard.py` so `000_epic/*`, `100_backlog/*`, `200_inprogress/*`, `300_complete/*`, and `400_failed/*` map explicitly by status family.
- Kept legacy `todo` name handling mapped to Backlog for compatibility.
- Removed the incorrect broad behavior that treated any folder containing `backlog` as Epic.

## Validation
- `python -m py_compile C:\\Users\\edebe\\eds\\workstream\\kanban_dashboard.py`
- Result: pass
- `netstat -ano | Select-String ':8080'`
- Result: initial check showed two listening PIDs (`29476` and `32256`); final check shows only `29476`
- `Invoke-WebRequest -UseBasicParsing 'http://localhost:8080'`
- Result: final check shows the served page source contains `if (col.includes("100_backlog") || col.includes("todo")) col = "100_backlog";`

## Evidence
- Objective-Delivery-Coverage: 95%
- Auto-Acceptance: false
- Evidence-Type: manual_verification
- Artifact: user-provided screenshot of the kanban board at `localhost:8080`
- Objective-Proved: reproduces the board state where Backlog shows `0` despite expected tasks
- Status: captured
- Evidence-Type: file_output
- Artifact: `workstream/100_backlog/general/20260316_135213_trading_strategy_warehouse_build_landing_page_and_subscribe_funnel.md` and peer files
- Objective-Proved: confirms the backlog tasks exist on disk
- Status: captured
- Evidence-Type: url
- Artifact: `http://localhost:8080/api/tasks?startDate=2026-03-16&endDate=2026-03-16`
- Objective-Proved: confirms the API returns the backlog tasks that are not being rendered in Backlog
- Status: captured
- Evidence-Type: diff
- Artifact: `workstream/kanban_dashboard.py`
- Objective-Proved: shows the folder-to-column mapping now routes `100_backlog/*` to Backlog instead of Epic
- Status: captured
- Evidence-Type: test_output
- Artifact: `python -m py_compile C:\\Users\\edebe\\eds\\workstream\\kanban_dashboard.py`
- Objective-Proved: confirms the patched dashboard script is syntactically valid
- Status: captured
- Evidence-Type: log_output
- Artifact: `netstat -ano | Select-String ':8080'`
- Objective-Proved: confirms two concurrent listeners are active on the kanban port, which explains stale code still being served
- Status: captured
- Evidence-Type: url
- Artifact: `http://localhost:8080`
- Objective-Proved: confirms the live page source now contains the patched backlog mapping logic after the stale listener was removed
- Status: captured

## Completion Status
- Awaiting user verification


# User Feedback
User Verified: PASS
