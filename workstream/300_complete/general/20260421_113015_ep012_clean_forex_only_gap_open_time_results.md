---
Task Type: standard
Task Attributes:
  workflow_task: true
  workflow_name: adaptive_strategy_selection_engine
  workflow_stage: complete
  depends_on: [20260421_111532_ep012_clean_forex_only_open_time_results]
  feeds_into: []
---
**Epic:** adaptive_strategy_selection_engine

# Clean Forex-Only Gap Open-Time Results

**Source:** User request on 2026-04-21: provide the same clean forex-only open-time stats for `rank-1 + gap>X`.

**Task Summary:** Run strict `rank-1 + gap>X` analysis using only clean forex-only source files.

**Destination Folder:** `epics/ep_012_adaptive_strategy_selection_engine/results/learned/`

**Dependency:** Clean forex-only date set from `20260421_111532_ep012_clean_forex_only_open_time_results`.

## Plan

- [x] 1. Reuse clean forex-only date set.
  - [x] Test: Scan confirms `16` clean dates and `10` excluded contaminated dates in the 2026-03-21 to 2026-04-17 window.
  - Evidence: Clean dates logged in command output.

- [x] 2. Run strict `rank-1 + gap>X` analysis for 00:00, 01:00, 02:00, and 03:00.
  - [x] Test: Inline Python generated total net, avg/day, and switches per threshold.
  - Evidence: `rank1_open_time_strict_gap_clean_forex_only.csv` and `.md`.

## Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true

- Evidence-Type: file_output
  - Artifact: `epics/ep_012_adaptive_strategy_selection_engine/results/learned/rank1_open_time_strict_gap_clean_forex_only.md`
  - Objective-Proved: Clean forex-only gap results were generated.
  - Status: captured

## Implementation Log

- 2026-04-21 11:30:15 BST — Generated clean forex-only `rank-1 + gap>X` open-time result artifacts.

## Changes Made

- Generated `epics/ep_012_adaptive_strategy_selection_engine/results/learned/rank1_open_time_strict_gap_clean_forex_only.csv`.
- Generated `epics/ep_012_adaptive_strategy_selection_engine/results/learned/rank1_open_time_strict_gap_clean_forex_only.md`.

## Results Summary

| First open cutoff | Best strict gap rule | Total net | Avg/day | Switches | Days |
|---|---:|---:|---:|---:|---:|
| 00:00 | rank-1 + gap>5 | 1,440 | 90 | 6 | 16 |
| 01:00 | rank-1 + gap>5 | 2,140 | 134 | 6 | 16 |
| 02:00 | rank-1 + gap>0 | 2,140 | 134 | 6 | 16 |
| 03:00 | rank-1 + gap>0 | 2,190 | 137 | 5 | 16 |

## Validation

- Command completed and wrote CSV/Markdown artifacts.

## Risks/Notes

- Clean-only subset contains 16 days; compare primarily by avg/day.

## Completion Status

COMPLETE -- 2026-04-21 11:31 BST
