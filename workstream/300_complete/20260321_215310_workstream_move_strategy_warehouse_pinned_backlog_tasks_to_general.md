# Move Strategy Warehouse Pinned Backlog Tasks To General

## Metadata
- Project: workstream
- Task: move_strategy_warehouse_pinned_backlog_tasks_to_general
- Started: 2026-03-21 21:53:10
- Status: complete

## Source
- User request in Codex thread on 2026-03-21 to drop the currently pinned focused-epic backlog tasks back to `100_backlog/general`.

## Task Summary
Move the currently pinned Strategy Warehouse backlog tasks out of agent-specific backlog lanes and back into the general backlog.

## Context
- `C:\Users\edebe\eds\workstream\100_backlog\gemini`
- `C:\Users\edebe\eds\workstream\100_backlog\general`
- Focused epic family: `strategy_warehouse_marketing_engine`

## Dependency
Dependency: None

## Plan
- [x] 1. Verify the current set of pinned Strategy Warehouse backlog tasks.
  - [x] Test: Enumerate focused-epic markdown files in worker-specific backlog lanes.
  - [x] Evidence: Pre-move check found `14` focused-epic backlog files pinned in `100_backlog/gemini`, with `0` in `codex` and `claude`.
- [x] 2. Move the pinned backlog tasks into `workstream/100_backlog/general`.
  - [x] Test: Matching backlog files are moved successfully without touching review or in-progress copies.
  - [x] Evidence: Move command output reported `moved_count=14`.
- [x] 3. Validate the post-move lane counts.
  - [x] Test: Recount focused-epic backlog files in worker-specific lanes and in `general`.
  - [x] Evidence: Post-move recount confirmed `0` remaining in `100_backlog/gemini` and `14` present in `100_backlog/general`.

## Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: false
- Evidence-Type: test_output
  - Artifact: Pre-move lane scan showing `gemini=14`, `codex=0`, `claude=0` for focused-epic backlog tasks.
  - Objective-Proved: Verified the exact set of pinned backlog tasks before the move.
  - Status: captured
- Evidence-Type: log_output
  - Artifact: Move command output `moved_count=14`.
  - Objective-Proved: All currently pinned focused-epic backlog tasks were moved out of the Gemini backlog lane.
  - Status: captured
- Evidence-Type: log_output
  - Artifact: Post-move recount and path listing showing `100_backlog/gemini=0` and `100_backlog/general=14`.
  - Objective-Proved: Focused-epic backlog is restored to general backlog and no pinned Gemini backlog tasks remain.
  - Status: captured

## Lifecycle Log
### 2026-03-21 21:53:10
- Created lifecycle record for returning pinned Strategy Warehouse backlog tasks to `100_backlog/general`.

### 2026-03-21 21:53:25
- Enumerated the focused-epic worker-specific backlog lanes.
- Found `14` matching tasks pinned in `100_backlog/gemini`; no matching tasks were present in `100_backlog/codex` or `100_backlog/claude`.

### 2026-03-21 21:53:40
- Moved the 14 pinned Gemini-lane backlog tasks into `100_backlog/general`.

### 2026-03-21 21:54:00
- Recounted the live backlog after the move.
- Confirmed `100_backlog/gemini` now has `0` matching focused-epic tasks and `100_backlog/general` now has `14`.

## Validation
- [x] Enumerate focused-epic backlog files in pinned worker lanes.
- [x] Move matching files to `workstream/100_backlog/general`.
- [x] Recount focused-epic backlog files after the move.
