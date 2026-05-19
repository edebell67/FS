Source:
- User request on 2026-03-12 to update the agent task pickup flow so it actively checks `Epic Sequence` and `Readiness` before starting work.

Task Summary:
- Implement runtime gating in the workstream agent controller so workers select only runnable tasks, enforce epic sequencing, and respect dependency readiness instead of relying on skill instructions alone.

Context:
- Primary controller: `workstream/run_agent.ps1`.
- New epic metadata fields now exist in decomposition output: `Epic Sequence`, `Depends On`, `Blocks`, `Readiness`.
- Workers currently sort only by `Priority` and timestamp.

Plan:
- [x] 1. Create this lifecycle file in progress and inspect the current controller pickup flow.
  - [x] Test: Confirm the lifecycle file exists in `workstream/200_inprogress` and document the current selection behavior in code.
  - Evidence: Lifecycle file moved to `workstream/200_inprogress/20260312_162722_workstream_enforce_epic_sequence_and_readiness_gate.md`; existing `workstream/run_agent.ps1` worker blocks were confirmed to sort only by `Priority` and timestamp before this change.
- [x] 2. Add shared task-gating helpers and wire each worker to use epic sequence and readiness checks before task start.
  - [x] Test: Review controller code to confirm workers now call a readiness gate before moving a task from `100_todo` to `200_inprogress`.
  - Evidence: Added `workstream/task_gate_utils.ps1`; Gemini, Codex, and Claude worker jobs in `workstream/run_agent.ps1` now dot-source the utility and call `Select-NextRunnableTask` before `Move-Item`.
- [x] 3. Validate the gating logic with a local dry-run scenario and archive this lifecycle file.
  - [x] Test: Run a PowerShell validation that simulates dependent epic tasks and confirms the controller gate selects the correct next task.
  - Evidence: Validation returned `run_agent_parse_ok`, `task_gate_utils_parse_ok`, and `task_gate_simulation_ok`; the dry run confirmed `task_1.md` with `Epic Sequence: 1.1` was selected first, then `task_2.md` with `Depends On: 1.1` became runnable only after task 1 moved to complete.

Implementation Log:
- 2026-03-12 16:27:22: Task file created in `workstream/100_todo`.
- 2026-03-12 16:27:40: Task file moved to `workstream/200_inprogress`.
- 2026-03-12 16:31:00: Inspected `workstream/run_agent.ps1` and confirmed workers selected tasks by `Priority` and timestamp only.
- 2026-03-12 16:38:00: Added `workstream/task_gate_utils.ps1` with task metadata parsing, epic dependency checks, readiness updates, and next-task selection.
- 2026-03-12 16:40:00: Updated all three worker jobs in `workstream/run_agent.ps1` to use the shared gate before moving tasks into `200_inprogress`.
- 2026-03-12 16:43:00: Parsed both PowerShell files and executed a simulated epic queue validation; all checks passed.

Changes Made:
- Added `workstream/task_gate_utils.ps1`.
- Updated `workstream/run_agent.ps1`.

Validation:
- PowerShell parse check for `workstream/run_agent.ps1`
  - Result: `run_agent_parse_ok`
- PowerShell parse check for `workstream/task_gate_utils.ps1`
  - Result: `task_gate_utils_parse_ok`
- Simulated dependency gate validation under `workstream/verification/task_gate_validation`
  - Result: `task_gate_simulation_ok`

Risks/Notes:
- The gating logic must not break legacy tasks that lack epic metadata.
- Changes must preserve parallel execution within the same epic layer.
- Legacy tasks without `Epic:` metadata remain runnable and continue using priority plus timestamp ordering.
- Higher epic layers are blocked until lower major layers are complete; tasks within the same major layer can still run in parallel.

Completion Status:
- Complete on 2026-03-12 16:43:00.
