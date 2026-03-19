Source:
- User requirement on 2026-03-12: all three workers resolving the same first runnable task should not be possible.

Task Summary:
- Make task claiming atomic so only one worker can reserve and move a runnable task at a time.

Context:
- Current selector is global, but workers independently call select and then `Move-Item`.
- This creates a race where multiple workers can choose the same task before any one move completes.
- Primary files: `workstream/task_gate_utils.ps1`, `workstream/run_agent.ps1`

Plan:
- [x] 1. Move this lifecycle file to in-progress and confirm the race exists between selection and move.
  - [x] Test: Confirm the lifecycle file exists in `workstream/200_inprogress` and document the non-atomic select-then-move flow.
  - Evidence: Lifecycle file moved to `workstream/200_inprogress/20260312_213326_workstream_make_task_claim_atomic.md`; workers previously called `Select-NextRunnableTaskForWorker` and then `Move-Item` separately, allowing concurrent resolution of the same task.
- [x] 2. Add an atomic claim helper using a shared lock and update workers to use it.
  - [x] Test: Review the updated code and confirm workers no longer call `Select-NextRunnableTaskForWorker` and `Move-Item` separately.
  - Evidence: Added `Claim-NextRunnableTaskForWorker` in `workstream/task_gate_utils.ps1` using a named mutex and atomic move to the worker directory; all workers in `workstream/run_agent.ps1` now use the claim helper and log `claimed ... -> ...`.
- [x] 3. Validate the claim behavior with a local simulation and archive this lifecycle file.
  - [x] Test: Sequential claim attempts should return different tasks once the first task is claimed.
  - Evidence: Validation returned `task_gate_utils_parse_ok`, `run_agent_parse_ok`, and `atomic_claim_simulation_ok`; the first claim returned `task_a.md` and the second returned `task_b.md`.

Implementation Log:
- 2026-03-12 21:33:26: Task file created in `workstream/100_todo`.
- 2026-03-12 21:33:40: Task file moved to `workstream/200_inprogress`.
- 2026-03-12 21:36:00: Confirmed the worker race existed because selection and move were separate operations.
- 2026-03-12 21:40:00: Added mutex-based atomic task claim helper and updated all workers to claim tasks through the shared lock.
- 2026-03-12 21:42:00: Ran parser checks and local claim simulation successfully.

Changes Made:
- Updated `workstream/task_gate_utils.ps1`.
- Updated `workstream/run_agent.ps1`.

Validation:
- PowerShell parse check for `workstream/task_gate_utils.ps1`
  - Result: `task_gate_utils_parse_ok`
- PowerShell parse check for `workstream/run_agent.ps1`
  - Result: `run_agent_parse_ok`
- Atomic claim simulation under `workstream/verification/atomic_claim_validation`
  - Result: `claim1=task_a.md`, `claim2=task_b.md`, `atomic_claim_simulation_ok`

Risks/Notes:
- The atomic claim lock must not deadlock the worker loop.
- The claim mutex uses a 5-second wait to avoid indefinite hangs if a worker dies while inside the claim section.

Completion Status:
- Complete on 2026-03-12 21:42:00.
