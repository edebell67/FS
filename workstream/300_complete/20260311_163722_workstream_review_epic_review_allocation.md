Source: User request to review the Epic Review task-allocation flow and explain how tasks are allocated to models.
Task Summary: Inspect the Epic Review UI and backend allocation path, identify any concrete review findings, and explain the current model-allocation behavior.
Context: workstream/kanban_dashboard.py Epic Review UI, task parsing, allocation endpoints, and file-move logic.
Plan:
- [x] 1. Read the relevant Epic Review route, task parsing, and allocation code paths.
  - [x] Test: Capture line-numbered references for the review UI, allocation endpoint, and file-move functions.
  - [x] Evidence: Targeted inspection of workstream/kanban_dashboard.py route and allocation references started.
- [x] 2. Identify concrete review findings and explain the allocation flow end-to-end.
  - [x] Test: Correlate UI actions to backend functions and verify how files move between folders/models.
  - [x] Evidence: Reviewed Epic Review frontend task-card allocation logic in workstream/apps/task_review/static/app.js and backend allocation functions in workstream/kanban_dashboard.py.
- [x] 3. Summarize findings, assumptions, and risks in the lifecycle file and final response.
  - [x] Test: Final response includes findings first, then a concise explanation of the current allocation behavior.
  - [x] Evidence: Findings and allocation explanation documented below.
Implementation Log:
- 2026-03-11 16:37:22 Created review task for Epic Review allocation flow.
- 2026-03-11 16:39:00 Traced Epic Review task discovery, task parsing, and allocation endpoints in workstream/kanban_dashboard.py.
- 2026-03-11 16:40:00 Inspected Epic Review frontend state and button handlers in workstream/apps/task_review/static/app.js.
Changes Made:
- Created lifecycle task file for this review.
- No source code changes made; review-only task.
Validation:
- [x] Read lifecycle instructions and identified target code regions.
- [x] `rg -n "epic-review|allocate_tasks|bulk_allocate_by_workstream|/api/tasks/allocate|/api/epics|/api/models/status|allocate" workstream/kanban_dashboard.py`
  - Result: Located the review routes, task APIs, and allocation functions.
- [x] Line-numbered inspection of `workstream/apps/task_review/static/app.js`
  - Result: Confirmed the UI supports both per-task acceptance with per-task assigned model state and direct selected-task allocation using the default model.
- [x] Line-numbered inspection of `workstream/kanban_dashboard.py`
  - Result: Confirmed Epic Review indexes tasks across `100_todo`, `200_inprogress`, `300_complete`, and `400_failed`, and allocation is implemented as a filesystem move into `100_todo/{model}`.
Risks/Notes:
- Review-only task; no code changes planned unless separately requested.
- Findings:
  - High: `Allocate Selected` ignores the per-task model dropdown entirely and sends every selected task to the global default model. The frontend stores per-task assignments on dropdown change, but the button handler posts `defaultModel.value` for all selected tasks. This makes the per-card model selector misleading unless the user uses `Accept` plus `Allocate All Accepted`. References: `workstream/apps/task_review/static/app.js` lines 138-150 and 270-272.
  - High: the backend allocation endpoint will move any provided task path into `100_todo/{model}`, regardless of whether the task is already `200_inprogress`, `300_complete`, or `400_failed`. Since Epic Review lists tasks from all four state folders, the UI can effectively resurrect completed/failed/in-progress tasks back into a model todo lane. References: `workstream/kanban_dashboard.py` lines 1766-1773, 1844-1856, and 1888-1905.
  - Medium: accepted/assigned allocation state is purely client-side memory. Reloading the page or changing the epic/task list drops `acceptedPaths` and unsaved `assignedModels`, so a user can believe they staged workstream/model assignments that are actually lost before allocation. References: `workstream/apps/task_review/static/app.js` lines 1-8, 191-208, and 278-290.
  - Medium: there is a backend `bulk_allocate_by_workstream()` helper, but the current Epic Review UI never uses it. Allocation is per task path, not per workstream mapping, so any expectation of “assign all workstream B to Claude” is not implemented in the current screen. References: `workstream/kanban_dashboard.py` lines 1939-1950 and `workstream/apps/task_review/static/app.js` lines 278-287.
Completion Status: Complete as of 2026-03-11 16:42:00
