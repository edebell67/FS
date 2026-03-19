Source: User report that `http://localhost:8080/epic-review` cannot be reached from the Epic Review button.

Context:
- `C:\Users\edebe\eds\workstream\kanban_dashboard.py`
- `C:\Users\edebe\eds\workstream\start_task_review.bat`

Plan:
- [x] 1. Inspect the dashboard route and port binding for `/epic-review`.
  - [x] Test: Confirm `kanban_dashboard.py` exposes `/epic-review` on the expected port.
  - [x] Evidence: `kanban_dashboard.py` serves `/epic-review` via `KanbanHandler` and binds `ThreadedHTTPServer(('localhost', 8080), ...)`.
- [x] 2. Diagnose whether the service is currently reachable on `localhost:8080`.
  - [x] Test: Probe `http://localhost:8080/epic-review`.
  - [x] Evidence: `curl.exe -I --max-time 3 http://localhost:8080/epic-review` failed with `Could not connect to server`, confirming no active listener.
- [x] 3. Restore access and verify the page responds.
  - [x] Test: Start the dashboard server and confirm `/epic-review` returns HTTP 200.
  - [x] Evidence: Started `python -u workstream\kanban_dashboard.py`; startup log reported `Real-Time Kanban Dashboard starting on http://localhost:8080`, and `Invoke-WebRequest http://localhost:8080/epic-review` returned `status=200`.

Notes:
- `workstream/start_task_review.bat` launches the standalone FastAPI task review app, not the integrated dashboard route on port `8080`.
- `curl -I` against the route returns `501 Unsupported method ('HEAD')` because the dashboard server does not implement `HEAD`; this does not affect normal browser GET access.

Chronology:
- 2026-03-13 22:39 Europe/London: Confirmed the `/epic-review` route exists in `kanban_dashboard.py` and is served by the integrated dashboard on port `8080`.
- 2026-03-13 22:41 Europe/London: Confirmed `localhost:8080` was not accepting connections and that the Epic Review outage was operational rather than a route regression.
- 2026-03-13 23:03 Europe/London: Started the dashboard server and verified `GET /epic-review` returned HTTP `200`.
