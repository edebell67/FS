# Enforce Max One Task Per Model Backlog Lane

## Metadata
- Project: workstream
- Task: enforce_max_one_task_per_model_backlog_lane
- Started: 2026-03-22 00:40:00
- Status: complete

## Source
- User request in Codex thread on 2026-03-22 to enforce the same `max 1` rule in each model-specific backlog lane.

## Task Summary
Update the active scheduler path so each model-specific backlog lane keeps at most one task, with overflow returned to `100_backlog/general`.

## Context
- `C:\Users\edebe\eds\workstream\run_agent.py`

## Dependency
Dependency: `C:\Users\edebe\eds\workstream\300_complete\20260322_001900_workstream_fix_single_slot_worker_refill_behavior.md`

## Plan
- [x] 1. Inspect the active controller backlog-path handling.
  - Test: Locate the claim/revert points and any existing model-lane backlog writes.
  - Evidence: Confirmed the relevant enforcement points are `rebalance_model_backlog_lanes()` before claims and `_revert_to_backlog()` for returning work.
- [x] 2. Add backlog-lane normalization so each model lane retains at most one queued task.
  - Test: Confirm overflow tasks are moved from model-specific backlog lanes back to `100_backlog/general`.
  - Evidence: Added backlog-lane normalization in `run_agent.py` so each model lane keeps only one queued task and spills excess into `100_backlog/general`.
- [x] 3. Ensure reverts respect the same max-one rule.
  - Test: Confirm `_revert_to_backlog()` sends tasks to general when the model-specific backlog lane is already occupied.
  - Evidence: Updated `_revert_to_backlog()` to use `_preferred_backlog_target()`, which routes to `general` whenever a model-specific backlog lane is already full.
- [x] 4. Validate the updated controller.
  - Test: `python -m py_compile C:\Users\edebe\eds\workstream\run_agent.py`
  - Evidence: Module compiles after backlog-lane enforcement, and direct workspace checks verified both rebalance and revert behavior.

## Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: false
- Evidence-Type: diff
  - Artifact: `C:\Users\edebe\eds\workstream\run_agent.py`
  - Objective-Proved: Active controller now enforces at most one queued task in each model-specific backlog lane.
  - Status: verified
- Evidence-Type: command
  - Artifact: `python -m py_compile C:\Users\edebe\eds\workstream\run_agent.py`
  - Objective-Proved: Updated controller compiles successfully.
  - Status: verified
- Evidence-Type: command
  - Artifact: Workspace backlog rebalance validation script
  - Objective-Proved: Three Gemini backlog tasks were reduced to one in `100_backlog/gemini`, with the two overflow tasks moved to `100_backlog/general`.
  - Status: verified
- Evidence-Type: command
  - Artifact: Workspace revert-path validation script
  - Objective-Proved: Reverted work returned to `100_backlog/general` when `100_backlog/gemini` already contained one task.
  - Status: verified

## Execution Notes
- 2026-03-22 00:44: Added `MAX_MODEL_BACKLOG_PER_LANE = 1` to `run_agent.py` and implemented helpers for backlog target selection and lane rebalance.
- 2026-03-22 00:46: Wired periodic `rebalance_model_backlog_lanes()` into the active controller loop before task claims.
- 2026-03-22 00:47: Updated `_revert_to_backlog()` to respect the same max-one rule and use `general` when the model lane is already occupied.
- 2026-03-22 00:49: Validated both overflow rebalance and revert behavior with workspace-backed direct checks.

## Validation
- [x] Confirm enforcement points are identified.
- [x] Confirm overflow moves to `100_backlog/general`.
- [x] Confirm revert path respects the limit.
- [x] Run `python -m py_compile C:\Users\\edebe\\eds\\workstream\\run_agent.py`.
