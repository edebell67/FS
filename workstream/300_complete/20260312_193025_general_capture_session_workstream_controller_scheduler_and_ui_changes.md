Source:
- User request on 2026-03-12 to capture all changes in a new task.

Task Summary:
- Consolidate, review, and verify the major workstream changes implemented in this session so there is a single follow-up task covering the updated workflow, controller behavior, epic task metadata, UI transition highlights, and runtime fixes.

Context:
- Change areas touched in this session:
  - Skill creation and updates for epic task ordering and decomposition
  - Controller task gating and global auto-pick behavior
  - Root-level and `general` queue pickup behavior
  - Open epic task metadata backfill
  - Kanban status transition highlight behavior
  - Windows-safe lock handling in `summary_net_generator.py`
  - Controller startup fixes in `run_agent.ps1`

Plan:
- [ ] 1. Inventory the files changed in this session and group them by behavior area.
  - [ ] Test: `git diff --name-only` or equivalent file listing produces the changed file set for review.
  - Evidence:
- [ ] 2. Verify the workstream scheduler/controller changes end to end.
  - [ ] Test: Confirm the controller loads the lifecycle skill correctly, clears stale locks, and can identify a runnable task from the current queue.
  - Evidence:
- [ ] 3. Verify epic metadata and auto-pick behavior for current open epic tasks.
  - [ ] Test: Confirm open epic tasks contain `Epic Sequence`, `Depends On`, `Blocks`, `Readiness`, and `Epic Output Folder`, and that the selector can claim ready tasks.
  - Evidence:
- [ ] 4. Verify the Kanban status highlight behavior in the UI.
  - [ ] Test: Move one task into a normal status, one into complete, and one into failed; confirm the 2-second flash, 3-second green flash, and persistent red failed perimeter.
  - Evidence:
- [ ] 5. Verify the `summary_net_generator.py` lock fix on Windows in the real runtime path.
  - [ ] Test: Start the generator with and without a stale lock file and confirm it no longer fails with `WinError 87`.
  - Evidence:

Implementation Log:
- 2026-03-12 19:30:25: Task file created in `workstream/100_todo/general`.

Changes Made:
- None yet.

Validation:
- Pending.

Risks/Notes:
- This task is intended as a consolidation and verification pass, not a new feature implementation by itself.
- If the scope expands into additional controller/runtime changes, split that work into separate follow-up tasks.

Completion Status:
- Todo.
