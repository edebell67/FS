Source:
- User request on 2026-03-12 to let each available model automatically pick the next ready task after decomposition and continue picking the next ready task as work completes.

Task Summary:
- Change the controller from fixed per-agent lane pickup to a self-managing global ready queue, so available models can claim the next runnable task automatically while still respecting agent preferences and epic dependency gates.

Context:
- Current runtime gate enforces `Epic Sequence`, `Depends On`, and `Readiness`.
- Current workers in `workstream/run_agent.ps1` still poll only their own agent lane.
- Some task files include `**Suggested Agent:**` and existing folders imply lane preference.

Plan:
- [x] 1. Move this lifecycle file to in-progress and inspect how current worker selection is still lane-bound.
  - [x] Test: Confirm the lifecycle file exists in `workstream/200_inprogress` and identify the fixed-lane selection in controller code.
  - Evidence: Lifecycle file moved to `workstream/200_inprogress/20260312_165906_workstream_enable_global_ready_task_autopick.md`; `workstream/run_agent.ps1` was confirmed to bind each worker to its own folder before this change.
- [x] 2. Update the shared gate and controller so idle workers can pick the next runnable task from the global ready pool.
  - [x] Test: Review the updated code and confirm workers now search across `100_todo` agent folders, using agent assignment as a preference rather than a hard restriction.
  - Evidence: `workstream/task_gate_utils.ps1` now parses `**Suggested Agent:**`, derives lane preference, and exposes `Select-NextRunnableTaskForWorker`; `workstream/run_agent.ps1` now calls that global selector for each worker.
- [x] 3. Validate the new scheduler with a local scenario covering preferred assignment, global fallback, and epic dependency gating.
  - [x] Test: Run a PowerShell simulation proving an available worker can claim a ready task outside its lane when needed, while blocked dependencies are still skipped.
  - Evidence: Validation returned `run_agent_parse_ok`, `task_gate_utils_parse_ok`, and `global_task_gate_simulation_ok`; simulated Geminin first claimed a `general` task, then fell back to a ready `codex` task when no preferred work remained, while a blocked dependent task was skipped until its dependency was completed.

Implementation Log:
- 2026-03-12 16:59:06: Task file created in `workstream/100_todo`.
- 2026-03-12 16:59:20: Task file moved to `workstream/200_inprogress`.
- 2026-03-12 17:02:00: Reviewed scheduler flow and confirmed workers still polled only their own lane even after readiness gating was added.
- 2026-03-12 17:08:00: Extended `task_gate_utils.ps1` to parse suggested agent and lane preference, then added global worker selection over all `100_todo` agent folders.
- 2026-03-12 17:10:00: Updated `run_agent.ps1` so each worker claims the next runnable task from the shared ready pool instead of a fixed lane.
- 2026-03-12 17:13:00: Parsed both PowerShell files and ran a global queue simulation covering preferred assignment, cross-lane fallback, and dependency gating.

Changes Made:
- Updated `workstream/task_gate_utils.ps1`.
- Updated `workstream/run_agent.ps1`.

Validation:
- PowerShell parse check for `workstream/run_agent.ps1`
  - Result: `run_agent_parse_ok`
- PowerShell parse check for `workstream/task_gate_utils.ps1`
  - Result: `task_gate_utils_parse_ok`
- Global scheduler simulation under `workstream/verification/global_task_gate_validation`
  - Result: `global_task_gate_simulation_ok`

Risks/Notes:
- Global pickup must not bypass dependency or readiness gates.
- Agent assignment should remain a preference so specialized tasks still tend to land on the intended model first.
- Current design still allows two workers to race for the same highest-ranked global task; the losing worker will fail to move it and retry on the next loop.
- `general` tasks are intentionally treated as globally claimable ahead of cross-specialty fallback.

Completion Status:
- Complete on 2026-03-12 17:13:00.
