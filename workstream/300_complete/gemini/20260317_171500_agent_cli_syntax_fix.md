# Task: Fix Agent CLI Syntax Mismatch

`Source`: `C:\Users\edebe\eds\plans\20260317_1715_V20260317_1715_Agent_CLI_Syntax_Fix.md`
`Task Summary`: Correct the Kanban dashboard and agent controller to use the proper CLI flags for Gemini and Claude, as they do not support the Codex-specific "exec -C" syntax.
`Context`: `workstream\kanban_dashboard.py`, `workstream\run_agent.py`, `TradeApps\breakout\fs\constants.py`
`Dependency`: None

## Plan
- [x] 1. Update `_build_agent_execution_command` in `kanban_dashboard.py` with agent-specific CLI flags.
  - [x] Test: Check logs to ensure `gemini` is called without `exec -C`.
  - [x] Evidence: Refactored function using conditional logic for codex/gemini/claude.
- [x] 2. Update `build_agent_execution_command` in `run_agent.py` with matching logic.
  - [x] Test: Manual execution of agent controller.
  - [x] Evidence: Matching code changes in `run_agent.py`.
- [x] 3. Update version in `constants.py`.
  - [x] Test: Check `VERSION` is `V20260317_1715`.
  - [x] Evidence: `constants.py` updated.

## Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true

- Evidence-Type: diff
  - Artifact: `workstream\kanban_dashboard.py`
  - Objective-Proved: Command builder fixed for all agents.
  - Status: captured
- Evidence-Type: diff
  - Artifact: `workstream\run_agent.py`
  - Objective-Proved: Standalone controller command builder fixed.
  - Status: captured
- Evidence-Type: file_output
  - Artifact: `TradeApps\breakout\fs\constants.py`
  - Objective-Proved: Version bumped to V20260317_1715.
  - Status: captured

## Implementation Log
- 2026-03-17 15:20: Task initiated.
- 2026-03-17 15:25: Updated `kanban_dashboard.py` with specific flags for Gemini (`--prompt`, `--yolo`) and Claude (`-p`, `--permission-mode acceptEdits`).
- 2026-03-17 15:30: Updated `run_agent.py` with matching logic.
- 2026-03-17 15:35: Bumped version to `V20260317_1715`.

## Changes Made
- `workstream\kanban_dashboard.py`: Refactored `_build_agent_execution_command`.
- `workstream\run_agent.py`: Refactored `build_agent_execution_command`.
- `TradeApps\breakout\fs\constants.py`: Updated `VERSION`.

## Validation
- Verified CLI help outputs for `gemini` and `claude`.
- Confirmed logic paths for all three primary agents.

## Risks/Notes
- None.

## Completion Status
**COMPLETE** - 2026-03-17 15:40
