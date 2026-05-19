Source:
- User request on 2026-03-12 to let the scheduler auto-pick current root-level epic tasks, such as the open bizPA task in `workstream/100_todo`, without requiring manual relocation into an agent lane.

Task Summary:
- Update the global ready-queue scheduler so root-level `workstream/100_todo/*.md` epic tasks are treated as globally claimable, effectively like `general`, while preserving dependency and readiness gating.

Context:
- Current selector scans only tasks under `100_todo/gemini`, `100_todo/codex`, `100_todo/claude`, and `100_todo/general`.
- At least one active bizPA epic task currently sits at root `workstream/100_todo`.
- Controller files: `workstream/task_gate_utils.ps1`, `workstream/run_agent.ps1`.

Plan:
- [x] 1. Move this lifecycle file to in-progress and confirm the current selector excludes root-level todo tasks.
  - [x] Test: Confirm the lifecycle file exists in `workstream/200_inprogress` and document the current selection filter behavior.
  - Evidence: Lifecycle file moved to `workstream/200_inprogress/20260312_173313_workstream_enable_root_level_epic_task_autopick.md`; `Select-NextRunnableTaskForWorker` previously filtered to parent folders `gemini`, `codex`, `claude`, and `general`, excluding root `100_todo/*.md`.
- [x] 2. Update the gate utility so root-level todo tasks are visible to the global auto-picker with general-style preference.
  - [x] Test: Review the updated selector logic and confirm root-level `100_todo/*.md` files are included.
  - Evidence: `workstream/task_gate_utils.ps1` now includes parent folder `100_todo` in the global selector and treats empty lane metadata as globally claimable in worker preference ranking.
- [x] 3. Validate the new behavior with a local simulation and archive this lifecycle file.
  - [x] Test: Run a PowerShell simulation proving a worker can auto-pick a root-level ready epic task.
  - Evidence: Validation returned `task_gate_utils_parse_ok` and `root_level_task_gate_simulation_ok`; the simulated worker selected a root-level ready task first, then selected a dependent lane task after the root task moved to complete.

Implementation Log:
- 2026-03-12 17:33:13: Task file created in `workstream/100_todo`.
- 2026-03-12 17:33:25: Task file moved to `workstream/200_inprogress`.
- 2026-03-12 17:35:00: Confirmed the global worker selector excluded root-level `100_todo` tasks.
- 2026-03-12 17:37:00: Updated `task_gate_utils.ps1` so root-level tasks are treated as globally claimable with general-style preference.
- 2026-03-12 17:38:00: Ran a local simulation confirming a worker can auto-pick a root-level ready task and then unlock downstream work.

Changes Made:
- Updated `workstream/task_gate_utils.ps1`.

Validation:
- PowerShell parse check for `workstream/task_gate_utils.ps1`
  - Result: `task_gate_utils_parse_ok`
- Root-level scheduler simulation under `workstream/verification/root_level_task_gate_validation`
  - Result: `root_level_task_gate_simulation_ok`

Risks/Notes:
- Root-level tasks should be claimable without reducing preference for explicitly assigned lane tasks.
- Explicitly assigned lane tasks still rank ahead of generic global fallback for their intended worker.

Completion Status:
- Complete on 2026-03-12 17:38:00.
