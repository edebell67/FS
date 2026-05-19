Source: User provided traceback on 2026-04-01 showing `kanban_dashboard.py` raising `ConnectionAbortedError: [WinError 10053]` while serving a GET request.
Task Type: bugfix
Project: workstream

## Objective
- Stop `kanban_dashboard.py` from emitting traceback noise when the browser aborts an in-flight HTTP request.
- Preserve normal error handling for real server-side faults.

## Plan
- [x] 1. Inspect the failing request handler path around the reported lines.
- [x] 2. Patch the HTTP handler to swallow client disconnect socket errors cleanly.
- [x] 3. Validate syntax and summarize the impact.

## Implementation Log
- 2026-04-01 12:04 Europe/London: Confirmed the dashboard request handler already had some local write guards, but disconnects could still bubble up and trigger a second write during error handling.
- 2026-04-01 12:06 Europe/London: Added a `handle_one_request` guard in `KanbanHandler` to swallow `BrokenPipeError`, `ConnectionAbortedError`, `ConnectionResetError`, and Windows socket abort/reset `OSError` cases.

## Changes Made
- Updated `C:\Users\edebe\eds\workstream\kanban_dashboard.py`

## Validation
- `python -m py_compile C:\Users\edebe\eds\workstream\kanban_dashboard.py`
- Result: passed. Existing unrelated `SyntaxWarning: invalid escape sequence '\d'` in the embedded `HTML_PAGE` string remains, but it does not block execution.

## Risks/Notes
- This change is intentionally narrow: only browser/client disconnect socket failures are suppressed. Other `OSError` cases still raise normally.
- Restart the running `kanban_dashboard.py` process to load the patched handler.
