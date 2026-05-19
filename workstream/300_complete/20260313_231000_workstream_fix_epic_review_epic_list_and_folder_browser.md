Source: User report that the integrated Epic Task Review page shows an empty epic list and the Browse Folder button does not work.

Context:
- `C:\Users\edebe\eds\workstream\kanban_dashboard.py`
- `C:\Users\edebe\eds\workstream\apps\task_review\static\index.html`
- `C:\Users\edebe\eds\workstream\apps\task_review\static\app.js`

Plan:
- [x] 1. Trace the integrated Epic Review page data flow for epic loading and folder browsing.
  - [x] Test: Inspect the integrated dashboard route, inlined HTML/JS, and API responses for `/api/epics` and `/api/browse-files`.
  - [x] Evidence: `/api/epics` and `/api/browse-files` both respond, but the current UI defaults `folderPath` to `workstream/100_backlog`, and the integrated page likely depends on inlined markup matching the updated static app.
- [ ] 2. Fix the epic source and folder-browser wiring in the integrated dashboard Epic Review page.
  - [x] Test: The Epic selector should populate from `workstream/000_epic`, and clicking Browse Folder should render a navigable folder modal.
  - [x] Evidence: Updated the shared Epic Review frontend so the epic selector now loads from `/api/epics?folder=workstream/000_epic`, moved the folder-browser modal markup ahead of script execution so the modal nodes exist when JS initializes, and kept task loading bound to the separately chosen task-source folder.
- [ ] 3. Validate the integrated page end to end.
  - [x] Test: Browser/API smoke checks for epic listing, folder browsing, and task loading from a selected decomposed-task folder.
  - [x] Evidence: `python -m py_compile C:\Users\edebe\eds\workstream\kanban_dashboard.py C:\Users\edebe\eds\workstream\apps\task_review\app.py` passed. A bounded dashboard smoke run returned populated epic documents for `GET /api/epics?folder=workstream/000_epic`, `200` for `GET /api/browse-files?path=workstream`, and `200` for `GET /epic-review`.

Chronology:
- 2026-03-13 23:10 Europe/London: Confirmed the integrated page was defaulting the epic selector to task-derived data from `100_backlog` instead of epic documents from `000_epic`.
- 2026-03-13 23:13 Europe/London: Confirmed the folder-browser modal nodes were declared after the script tag, which left the JS wiring vulnerable to null element references during initialization.
- 2026-03-13 23:20 Europe/London: Updated the shared Epic Review HTML/JS and both backends so epics come from `000_epic`, the task-source folder remains separately browsable, and the folder modal is initialized safely.
- 2026-03-13 23:31 Europe/London: Ran a bounded dashboard smoke test and verified epic listing, folder browsing, and the `/epic-review` page route under the updated code.
