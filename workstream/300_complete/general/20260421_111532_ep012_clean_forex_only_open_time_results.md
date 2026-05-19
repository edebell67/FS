---
Task Type: standard
Task Attributes:
  workflow_task: true
  workflow_name: adaptive_strategy_selection_engine
  workflow_stage: in_progress
  depends_on: [20260421_105458_ep012_enforce_valid_rank1_switch_criteria]
  feeds_into: []
---
**Epic:** adaptive_strategy_selection_engine

# Clean Forex-Only Open-Time Results

**Source:** User request on 2026-04-21 to provide the open-time switching results again using only `_frequency.json` files that contain forex-only products.

**Task Summary:** Exclude contaminated forex source dates and recalculate strict `rank-1 + net>X` first-open cutoff results using only clean forex-only source files.

**Context:** Prior scan found 15 contaminated source files across all scanned forex dates and 10 contaminated files inside the 2026-03-21 to 2026-04-17 test window. Clean test-window dates count is 16.

**Destination Folder:** `epics/ep_012_adaptive_strategy_selection_engine/results/learned/`

**Dependency:** Strict criteria script and clean/contaminated source file classification.

## Plan

- [x] 1. Identify clean forex-only source dates in the test window.
  - [x] Test: Scan `TradeApps/breakout/fs/json/live/forex/*/_frequency.json` and exclude files with non-expected product symbols.
  - Evidence: Clean dates: `2026-03-24, 2026-03-26, 2026-03-27, 2026-03-28, 2026-03-29, 2026-03-30, 2026-03-31, 2026-04-01, 2026-04-02, 2026-04-03, 2026-04-05, 2026-04-06, 2026-04-07, 2026-04-08, 2026-04-09, 2026-04-17`.

- [x] 2. Run strict `rank-1 + net>X` analysis on clean dates only.
  - [x] Test: Generate total net, avg/day, and switches for 00:00, 01:00, 02:00, and 03:00 first-open cutoffs.
  - Evidence: Generated `rank1_open_time_strict_net_clean_forex_only.csv` and `.md`.

- [x] 3. Report clean-date results and note excluded dates.
  - [x] Test: Final response includes clean date count, excluded contamination count, and result table.
  - Evidence: Results summarized in lifecycle and final response.

## Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true

- Evidence-Type: test_output
  - Artifact: Inline Python clean-date scan and strict net rerun
  - Objective-Proved: Clean-date analysis was executed.
  - Status: captured

- Evidence-Type: manual_verification
  - Artifact: `epics/ep_012_adaptive_strategy_selection_engine/results/learned/rank1_open_time_strict_net_clean_forex_only.md`
  - Objective-Proved: Result table is included in the response.
  - Status: captured

## Implementation Log

- 2026-04-21 11:15:32 BST — Created task and identified 16 clean forex-only dates in the 2026-03-21 to 2026-04-17 window.
- 2026-04-21 11:18 BST — Ran strict net-only open-time analysis using only the 16 clean forex-only dates.

## Changes Made

- Generated `epics/ep_012_adaptive_strategy_selection_engine/results/learned/rank1_open_time_strict_net_clean_forex_only.csv`.
- Generated `epics/ep_012_adaptive_strategy_selection_engine/results/learned/rank1_open_time_strict_net_clean_forex_only.md`.

## Results Summary

| First open cutoff | Best strict net rule | Total net | Avg/day | Switches | Days |
|---|---:|---:|---:|---:|---:|
| 00:00 | rank-1 + net>50 | 1,695 | 106 | 5 | 16 |
| 01:00 | rank-1 + net>50 | 2,395 | 150 | 5 | 16 |
| 02:00 | rank-1 + net>50 | 2,400 | 150 | 5 | 16 |
| 03:00 | rank-1 + net>50 | 2,400 | 150 | 5 | 16 |

Excluded contaminated dates:
`2026-03-21, 2026-03-22, 2026-03-23, 2026-03-25, 2026-04-10, 2026-04-12, 2026-04-13, 2026-04-14, 2026-04-15, 2026-04-16`.

## Validation

- Clean-date scan passed: `16` clean dates, `10` excluded contaminated dates in the 2026-03-21 to 2026-04-17 test window.
- Strict net rerun passed and wrote CSV/Markdown artifacts.

## Risks/Notes

- Clean-only results use fewer days and should not be compared directly to 25/26-day contaminated-window totals without normalizing by average/day.

## Completion Status

COMPLETE -- 2026-04-21 11:19 BST
