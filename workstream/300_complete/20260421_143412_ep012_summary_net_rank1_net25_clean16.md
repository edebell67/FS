# EP012 Summary Net Rank-1 Net>25 Clean 16-Day Replay

Source: User request, 2026-04-21
Task Type: standard

## Task Attributes
recurring_task: false
looping_task: false
splittable_task: false
workflow_task: false
depends_on:
- `workstream/300_complete/20260421_140509_ep012_summary_net_replay_correction.md`
feeds_into: []

## Task Summary
Run the corrected `_summary_net` replay for the earlier 16 clean forex dates using rule `rank-1 + net>25`, scored as entry/exit cumulative net deltas:
- open current rank #1 at/after cutoff,
- switch only when current rank #1 is different and `rank1_net > held_net + 25`,
- switch cost is `$50`,
- segment return is `exit_net - entry_net - switch_cost` for switch exits and `exit_net - entry_net` for day-end close.

## Context
Use canonical base strategies only and forex-shaped products only. Generated/suffixed strategy keys must be excluded.

## Destination Folder
Destination Folder: `epics/ep_012_adaptive_strategy_selection_engine/results/learned/`

## Dependency
Dependency: `epics/ep_012_adaptive_strategy_selection_engine/results/learned/summary_net_top3_hold_replay.py`

## Plan
- [x] 1. Run the 16-date rank-1 net>25 replay.
  - [x] Test: Execute replay generation and produce summary/day/event files.
  - Evidence: Generated `summary_net_rank1_net25_clean16_delta.md`, `_summary.csv`, `_days.csv`, and `_events.csv`.

- [x] 2. Validate outputs.
  - [x] Test: Confirm generated strategy keys are excluded and `2026-03-28` absence is handled.
  - Evidence: Run reported `generated_excluded=191`; 16-date whitelist produced 15 usable days because `2026-03-28` has no `_summary_net` snapshots.

- [x] 3. Report aligned summary.
  - [x] Test: Display aligned aggregate table.
  - Evidence: Aligned command output captured in Validation section.

## Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true

- Evidence-Type: file_output
  - Artifact: `epics/ep_012_adaptive_strategy_selection_engine/results/learned/summary_net_rank1_net25_clean16_delta.md`
  - Objective-Proved: Clean 16-day rank-1 net>25 replay outputs generated.
  - Status: captured

- Evidence-Type: file_output
  - Artifact: `epics/ep_012_adaptive_strategy_selection_engine/results/learned/summary_net_rank1_net25_clean16_delta_events.csv`
  - Objective-Proved: Per-segment entry/exit breakdown captured for audit.
  - Status: captured

## Implementation Log
- 2026-04-21 14:34: Created in-progress task.
- 2026-04-21 14:35: Ran 16-date clean whitelist replay for `rank-1 + net>25` using cumulative entry/exit net delta scoring.
- 2026-04-21 14:36: Captured summary, day, and event CSV outputs.

## Changes Made
- Created:
  - `epics/ep_012_adaptive_strategy_selection_engine/results/learned/summary_net_rank1_net25_clean16_delta.md`
  - `epics/ep_012_adaptive_strategy_selection_engine/results/learned/summary_net_rank1_net25_clean16_delta_summary.csv`
  - `epics/ep_012_adaptive_strategy_selection_engine/results/learned/summary_net_rank1_net25_clean16_delta_days.csv`
  - `epics/ep_012_adaptive_strategy_selection_engine/results/learned/summary_net_rank1_net25_clean16_delta_events.csv`

## Validation
- Replay command output:
```text
files 54 snapshots 40 generated_excluded 191 nonfx AUD,CAD,CHF,EUR,GBP,GBPEUR_S,NZD
Cutoff   Total net_return   Avg/day   Opened days   Switches   Usable days
----------------------------------------------------------------------
00:00               -308       -20            15         13            15
01:00               -308       -20            15         13            15
02:00               -382       -26            15         13            15
03:00               -485       -32            15         13            15
```

## Risks/Notes
- Earlier 16-date whitelist includes `2026-03-28`, but no `_summary_net` files exist for that date.
- These results use the entry/exit delta method requested in the discussion, not the earlier final-held-net scoring.
- Switch cost is `$50` per switch exit.

## Completion Status
Status: Complete
Created: 2026-04-21 14:34
Completed: 2026-04-21 14:36
