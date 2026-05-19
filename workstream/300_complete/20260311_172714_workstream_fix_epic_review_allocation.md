Source: User request to make Epic Review allocation work fully so tasks can be reliably allocated to models from the review screen.
Task Summary: Fix Epic Review allocation end-to-end so per-task model choices are respected, only valid tasks can be allocated/reallocated, and the screen gives clear allocation behavior for selected and accepted tasks.
Context: workstream/apps/task_review/static/app.js; workstream/apps/task_review/static/index.html; workstream/apps/task_review/static/styles.css; workstream/kanban_dashboard.py
Plan:
- [x] 1. Read the Epic Review UI and backend allocation paths and capture the failure modes.
  - [x] Test: Identify the exact frontend handlers and backend file-move logic responsible for allocation.
  - [x] Evidence: Reviewed task_review app.js and kanban_dashboard.py allocation/task parsing paths.
- [x] 2. Patch the Epic Review frontend so allocation uses per-task model choices consistently and blocks non-allocatable tasks in the UI.
  - [x] Test: Local script exercise shows selected/accepted allocation buckets tasks by assigned model and ignores locked states.
  - [x] Evidence: Updated task_review/static/app.js, index.html, and styles.css to use per-task assignments for selected allocation, disable locked cards, and show allocation-state messaging.
- [x] 3. Patch the backend allocation logic so only valid todo-state tasks can be allocated or reallocated to models.
  - [x] Test: Backend returns success for root/model todo tasks and rejects in-progress/complete/failed tasks.
  - [x] Evidence: Updated workstream/kanban_dashboard.py `allocate_tasks()` guardrails and validated with temporary todo/complete task files.
- [x] 4. Validate the end-to-end Epic Review allocation behavior and request user verification.
  - [x] Test: Local validation confirms allocation file moves and state refresh behavior; user is asked to verify in the browser.
  - [x] Evidence: `py_compile`, `node --check`, and backend allocation sanity test all passed; browser verification requested below.
Implementation Log:
- 2026-03-11 17:27:14 Created implementation task for Epic Review allocation fixes.
- 2026-03-11 17:30:00 Updated Epic Review task card markup and styling to show allocatable vs locked task state.
- 2026-03-11 17:32:00 Patched Epic Review frontend allocation logic so `Allocate Selected` buckets by per-task assigned model, selection targets only allocatable todo tasks, and allocation failures surface to the user.
- 2026-03-11 17:34:00 Added backend allocation guardrails to reject non-`100_todo` tasks and allow safe todo-lane reallocation only.
- 2026-03-11 17:36:00 Ran local syntax checks and backend allocation sanity tests with temporary task files.
Changes Made:
- Lifecycle task created for this implementation.
- Updated `C:\Users\edebe\eds\workstream\apps\task_review\static\app.js`
- Updated `C:\Users\edebe\eds\workstream\apps\task_review\static\index.html`
- Updated `C:\Users\edebe\eds\workstream\apps\task_review\static\styles.css`
- Updated `C:\Users\edebe\eds\workstream\kanban_dashboard.py`
Validation:
- [x] Read the target Epic Review files and previous review findings.
- [x] `python -m py_compile C:\Users\edebe\eds\workstream\kanban_dashboard.py`
  - Result: Backend module compiled successfully after allocation guardrail changes.
- [x] `node --check C:\Users\edebe\eds\workstream\apps\task_review\static\app.js`
  - Result: Epic Review frontend script passed syntax check.
- [x] Temporary backend allocation sanity test via `python -`
  - Result: a temporary `100_todo` task moved successfully into `100_backlog/gemini`; a temporary `300_complete` task was rejected with `Only 100_todo tasks can be allocated from Epic Review (got 300_complete)` and remained in place.
- [x] User verification requested
  - Result: Need browser confirmation that Epic Review now allocates tasks as intended.
Risks/Notes:
- User-visible flow change; final completion requires user verification in the browser.
- Epic Review now treats non-`100_todo` tasks as locked for allocation. They remain visible for epic context, but cannot be requeued from review.
Completion Status: In progress as of 2026-03-11 17:27:14

