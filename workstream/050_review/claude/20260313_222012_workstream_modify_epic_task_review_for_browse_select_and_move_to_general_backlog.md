Source: Direct user request in this session.

Task Summary: Modify Epic Task Review so the operator can select an epic to review, browse to the folder containing decomposed files, use per-task selection plus select-all, and move selected tasks into `workstream/100_backlog/general` where they will be picked up automatically.

Context:
- `C:\Users\edebe\eds\workstream\kanban_dashboard.py`
- `C:\Users\edebe\eds\workstream\apps\task_review\static\index.html`
- `C:\Users\edebe\eds\workstream\apps\task_review\static\app.js`
- `C:\Users\edebe\eds\workstream\apps\task_review\app.py`

Plan:
- [x] 1. Inspect the current Epic Review flow and identify which parts already exist.
  - [x] Test: Review the existing Epic Review HTML/JS/backend to confirm epic selection and per-task selection behavior.
  - Evidence: The existing Epic Review page already had epic selection, per-task checkboxes, and a select-visible action, but no folder browser and no direct move-to-`100_backlog/general` action.
- [x] 2. Add folder browsing to Epic Review so tasks can be loaded from a chosen decomposed-files folder.
  - [x] Test: Source inspection confirms a browse-folder UI and folder-aware epic/task loading are present.
  - Evidence: Added `Source Folder` controls plus a folder browser modal in `index.html`, folder-aware loading in `app.js`, and folder-query support to `/api/epics` and `/api/epics/{slug}/tasks` in both `kanban_dashboard.py` and `apps/task_review/app.py`.
- [x] 3. Add a move-selected action to send chosen tasks to `100_backlog/general`.
  - [x] Test: Source inspection confirms a `Move Selected to General Backlog` action exists and calls a backend move endpoint.
  - Evidence: Added `moveToGeneralButton` in `index.html`, move logic in `app.js`, and `/api/tasks/move-to-general` endpoints in `kanban_dashboard.py` and `apps/task_review/app.py`.
- [x] 4. Preserve existing selection behavior while broadening selection to browsed tasks.
  - [x] Test: Code inspection confirms task checkboxes and select-all now work for selectable browsed tasks, while allocation controls remain limited to `100_backlog` tasks.
  - Evidence: `app.js` now uses `isSelectableTask()` and `isMoveToGeneralCandidate()` so browsed tasks can be selected for movement without becoming allocatable model-lane tasks.
- [ ] 5. Verify the end-to-end review workflow in live use.
  - [x] Test: Backend syntax checks pass for both modified Python backends.
  - Evidence: `python -m py_compile C:\Users\edebe\eds\workstream\kanban_dashboard.py C:\Users\edebe\eds\workstream\apps\task_review\app.py` passed.
  - [ ] Test: User verifies that browsing to a decomposed-files folder, selecting tasks, and moving them to `100_backlog/general` works as intended in the Epic Review screen.
  - Evidence: Pending user verification.

Implementation Log:
- 2026-03-13 22:25 Europe/London: Recreated this lifecycle record in `200_inprogress` after implementing the requested Epic Review browse-and-move flow.
- 2026-03-13 22:19 Europe/London: Updated the Epic Review static UI to add source-folder controls, a folder browser modal, and a `Move Selected to General Backlog` action.
- 2026-03-13 22:22 Europe/London: Updated the built-in `kanban_dashboard.py` Epic Review backend so epics/tasks can be loaded from a chosen folder and selected tasks can be moved into `100_backlog/general`.
- 2026-03-13 22:24 Europe/London: Mirrored the same folder-aware Epic Review support into the standalone `apps/task_review/app.py` backend for consistency with the shared static frontend.

Changes Made:
- `C:\Users\edebe\eds\workstream\apps\task_review\static\index.html`
  - added `Source Folder` display and folder-browse controls
  - added folder-browser modal
  - added `Move Selected to General Backlog` action button
- `C:\Users\edebe\eds\workstream\apps\task_review\static\app.js`
  - added folder-scoped epic/task loading
  - added folder browser logic using `/api/browse-files`
  - added move-to-general action
  - broadened selection logic so browsed tasks can be selected for movement while preserving allocatable-lane checks for model assignment
- `C:\Users\edebe\eds\workstream\kanban_dashboard.py`
  - added folder-aware epic/task scanning
  - added move-to-general backend helper and endpoint
  - updated `/api/epics` to accept folder queries
- `C:\Users\edebe\eds\workstream\apps\task_review\app.py`
  - added folder-aware epic/task scanning
  - added `/api/browse-files`
  - added `/api/tasks/move-to-general`

Validation:
- `python -m py_compile C:\Users\edebe\eds\workstream\kanban_dashboard.py C:\Users\edebe\eds\workstream\apps\task_review\app.py`
  - PASS
- `rg -n "folderPath|browseFolderButton|moveToGeneralButton|/api/tasks/move-to-general|/api/browse-files" C:\Users\edebe\eds\workstream\kanban_dashboard.py C:\Users\edebe\eds\workstream\apps\task_review\app.py C:\Users\edebe\eds\workstream\apps\task_review\static\index.html C:\Users\edebe\eds\workstream\apps\task_review\static\app.js`
  - PASS: Epic Review UI and both backends contain the new browse/move capabilities.
- User verification requested:
  - Please verify that in Epic Review you can choose an epic, browse to the folder containing decomposed files, select tasks, and move the selected tasks into `100_backlog/general`.

Risks/Notes:
- The Epic Review page now supports two modes implicitly: normal backlog review and folder-scoped decomposed-file review.
- Allocation to model lanes remains restricted to `100_backlog` tasks; folder-browsed tasks are intended to be moved to `100_backlog/general` first.
- This is a user-visible workflow change and remains pending verification.

Completion Status:
- Awaiting user verification - 2026-03-13 22:25 Europe/London


# User Feedback
User Verified: FAIL
Details: no data


## Retry History
Retry-Count: 1
- Retry scheduled at 2026-03-18 17:21:30


## Execution Evidence
- Agent lane: claude
- Command: C:\Users\edebe\AppData\Roaming\npm\claude.CMD -p Execute this task file end-to-end. Read and follow C:\Users\edebe\eds\skills\workstream-task-lifecycle\SKILL.md first. Task file: C:\Users\edebe\eds\workstream\200_inprogress/claude\20260313_222012_workstream_modify_epic_task_review_for_browse_select_and_move_to_general_backlog.md. Implement required changes in the workspace, run validations, and update checklist items. --permission-mode acceptEdits
- Return code: 0
- Stdout:
```text
I'm unable to access files outside the current working directory (`C:\Users\edebe\OneDrive\Desktop\batch files`) due to permission restrictions. Could you please either:

1. **Grant read permission** when prompted for the paths under `C:\Users\edebe\eds\`
2. **Copy the files** to the current working directory so I can access them
3. **Re-launch** with the working directory set to `C:\Users\edebe\eds\` or add it as an allowed directory

I need access to both the skill definition and the task file to proceed.
```
