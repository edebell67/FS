Source:
- Follow-up request on 2026-03-12 to make the workstream controller auto-start more robustly so task claiming does not depend on a manual foreground session.

Task Summary:
- Add a durable launcher/supervisor for `workstream/run_agent.ps1` that can run in the background and restart the controller if it exits unexpectedly.

Context:
- Current controller script: `workstream/run_agent.ps1`
- Current manual launch command: `powershell -ExecutionPolicy Bypass -File C:\Users\edebe\eds\workstream\run_agent.ps1`
- Existing simple launcher pattern exists in `workstream/start_task_review.bat`

Plan:
- [ ] 1. Move this lifecycle file to in-progress and inspect the current launch pattern.
  - [ ] Test: Confirm the lifecycle file exists in `workstream/200_inprogress` and identify the existing launcher assets.
  - Evidence:
- [ ] 2. Add a supervisor-style launcher for the controller with persistent logging and restart behavior.
  - [ ] Test: Review the new launcher files and confirm they start `run_agent.ps1`, record supervisor logs, and restart after exit.
  - Evidence:
- [ ] 3. Validate the launcher behavior locally and archive this lifecycle file.
  - [ ] Test: Run the launcher briefly, confirm it starts the controller, and verify the supervisor log and PID artifacts are created.
  - Evidence:

Implementation Log:
- 2026-03-12 19:29:50: Task file created in `workstream/100_todo`.

Changes Made:
- None yet.

Validation:
- Pending.

Risks/Notes:
- The supervisor should not start duplicate controller instances.

Completion Status:
- In progress.
