Source: Direct user request in this session.

Task Summary: Limit the workstream system so no more than three tasks are in `200_inprogress` concurrently, matching the three model lanes.

Context:
- `C:\Users\edebe\eds\workstream\run_agent.ps1`
- `C:\Users\edebe\eds\workstream\task_gate_utils.ps1`
- `C:\Users\edebe\eds\workstream\kanban_dashboard.py`

Plan:
- [x] 1. Identify every code path that can move tasks from `100_todo` to `200_inprogress` and define a shared concurrency rule.
  - [x] Test: Inspect `workstream\run_agent.ps1`, `workstream\task_gate_utils.ps1`, and `workstream\kanban_dashboard.py`; pass if all automatic claim paths are accounted for.
  - [x] Evidence: Confirmed two automatic claim flows: `run_agent.ps1` claims through `Claim-NextRunnableTaskForWorker` in `task_gate_utils.ps1`, and `kanban_dashboard.py` claims directly inside `multi_model_lane_worker`.
- [x] 2. Implement a hard cap of three active in-progress tasks across all workstream lanes.
  - [x] Test: Update the claim logic so auto-claim returns no task whenever recursive `200_inprogress` count is `>= 3`.
  - [x] Evidence: Added `Get-InProgressTaskCount` plus `if ($inProgressCount -ge 3) { return $null }` in `workstream\task_gate_utils.ps1`; added `MAX_CONCURRENT_INPROGRESS_TASKS = 3` and a recursive `200_inprogress` count gate in `workstream\kanban_dashboard.py`.
- [x] 3. Validate syntax and confirm the guard is present in both controller paths.
  - [x] Test: Run targeted PowerShell and Python syntax checks; pass if no parse errors occur and the new cap is visible in code.
  - [x] Evidence: `task_gate_utils.ps1 parse=ok`, `run_agent.ps1 parse=ok`, `python -m py_compile workstream\kanban_dashboard.py` passed, and `rg` confirmed the new guard locations.

Implementation Log:
- 2026-03-13 04:05 Europe/London: Created lifecycle task from the user request to cap concurrent in-progress tasks at three.
- 2026-03-13 04:07 Europe/London: Read `run_agent.ps1`, `task_gate_utils.ps1`, and the dashboard lane worker to trace all automatic claim paths into `200_inprogress`.
- 2026-03-13 04:09 Europe/London: Added a shared recursive in-progress count helper to `task_gate_utils.ps1` and blocked new claims when the count is already three or more.
- 2026-03-13 04:10 Europe/London: Added the same global cap to `kanban_dashboard.py` so the dashboard lane worker cannot bypass the controller-side limit.
- 2026-03-13 04:11 Europe/London: Ran PowerShell parse checks and Python compile validation; all passed.

Changes Made:
- Updated `workstream\task_gate_utils.ps1`:
  - Added `Get-InProgressTaskCount`.
  - Added a global `200_inprogress` cap check inside `Claim-NextRunnableTaskForWorker`.
- Updated `workstream\kanban_dashboard.py`:
  - Added `MAX_CONCURRENT_INPROGRESS_TASKS = 3`.
  - Added a recursive `200_inprogress` count gate before lane workers claim any new to-do task.

Validation:
- `powershell` parser check for `workstream\task_gate_utils.ps1`
  - Result: `task_gate_utils.ps1 parse=ok`
- `powershell` parser check for `workstream\run_agent.ps1`
  - Result: `run_agent.ps1 parse=ok`
- `python -m py_compile workstream\kanban_dashboard.py`
  - Result: Passed with no output.
- `rg -n "Get-InProgressTaskCount|inProgressCount -ge 3|MAX_CONCURRENT_INPROGRESS_TASKS|current_inprogress >= MAX_CONCURRENT_INPROGRESS_TASKS" workstream\task_gate_utils.ps1 workstream\kanban_dashboard.py`
  - Result: Confirmed the new guard at `task_gate_utils.ps1:144`, `task_gate_utils.ps1:455-456`, `kanban_dashboard.py:7`, and `kanban_dashboard.py:3533`.

Risks/Notes:
- Existing stale tasks already sitting in `200_inprogress` will still count against the cap until they are cleared or moved.
- I did not restart the controller or dashboard process in this task, so already-running processes will need to reload these files before the new guard takes effect.

Completion Status:
- Complete - 2026-03-13 04:11 Europe/London
