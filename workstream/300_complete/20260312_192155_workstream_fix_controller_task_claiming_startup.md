Source:
- User report on 2026-03-12 that tasks moved into `todo/general` are not being claimed.

Task Summary:
- Fix the controller startup/config issue preventing task claiming, then verify whether the current queue contains a runnable task for the auto-picker.

Context:
- Controller file: `workstream/run_agent.ps1`
- Current log shows startup failure loading `skills/workstream-task-lifecycle/lifecycle.md`
- Correct skill file path exists at `skills/workstream-task-lifecycle/SKILL.md`

Plan:
- [ ] 1. Move this lifecycle file to in-progress and confirm the controller startup failure from logs.
  - [ ] Test: Confirm the lifecycle file exists in `workstream/200_inprogress` and capture the controller log evidence.
  - Evidence:
- [ ] 2. Fix the controller configuration so it loads the correct lifecycle skill file.
  - [ ] Test: Review `workstream/run_agent.ps1` and confirm it no longer references the missing `lifecycle.md` path.
  - Evidence:
- [ ] 3. Validate the current auto-picker against the live queue and archive this lifecycle file.
  - [ ] Test: Run a selector probe under execution-policy bypass and report whether a runnable task is currently available.
  - Evidence:

Implementation Log:
- 2026-03-12 19:21:55: Task file created in `workstream/100_todo`.

Changes Made:
- None yet.

Validation:
- Pending.

Risks/Notes:
- The currently running controller process will still need restart to pick up the corrected file path.

Completion Status:
- In progress.
