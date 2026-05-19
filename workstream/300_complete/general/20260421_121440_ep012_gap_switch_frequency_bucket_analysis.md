---
Task Type: standard
Task Attributes:
  workflow_task: true
  workflow_name: adaptive_strategy_selection_engine
  workflow_stage: complete
  depends_on: [20260421_113347_ep012_clean_forex_only_net_gap_open_time_test_report]
  feeds_into: []
---
**Epic:** adaptive_strategy_selection_engine

# Gap Switch Frequency Bucket Analysis

**Source:** User request on 2026-04-21: for `rank-1 + gap>X`, provide the `freq_count` / `rank1_count_cum` bucket at which each switch occurs.

**Task Summary:** Bucket the new rank-1 cumulative count at the exact switch event for clean forex-only strict `rank-1 + gap>X` analysis.

**Destination Folder:** `epics/ep_012_adaptive_strategy_selection_engine/results/learned/`

**Dependency:** Clean forex-only gap analysis.

## Test Definition

- Clean forex-only dates: `16`
- First-open cutoffs: `00:00`, `01:00`, `02:00`, `03:00`
- Switch criterion: strict `rank-1 + gap>X`
- Bucketed value: new rank-1 `rank1_count_cum` at switch time
- Buckets: `0-5`, `5-10`, `10-15`, `15-20`, `20-25`, `25-30`, `30-35`, `35-40`, `40-45`, `45-50`, `50+`

## Output Artifacts

- `epics/ep_012_adaptive_strategy_selection_engine/results/learned/rank1_gap_switch_count_buckets_clean_forex_only.csv`
- `epics/ep_012_adaptive_strategy_selection_engine/results/learned/rank1_gap_switch_events_clean_forex_only.csv`
- `epics/ep_012_adaptive_strategy_selection_engine/results/learned/rank1_gap_switch_count_buckets_clean_forex_only.md`

## Key Rows

Best clean gap rules from prior report:

| Cutoff | Rule | Switches | Dominant switch count buckets |
|---|---:|---:|---|
| 01:00 | rank-1 + gap>5 | 6 | `5-10`: 2, `15-20`: 2, `40-45`: 1, `50+`: 1 |
| 02:00 | rank-1 + gap>0 | 6 | `5-10`: 2, `10-15`: 2, `35-40`: 1, `50+`: 1 |
| 03:00 | rank-1 + gap>0 | 5 | `5-10`: 1, `10-15`: 2, `35-40`: 1, `50+`: 1 |

## Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true

- Evidence-Type: file_output
  - Artifact: `epics/ep_012_adaptive_strategy_selection_engine/results/learned/rank1_gap_switch_count_buckets_clean_forex_only.md`
  - Objective-Proved: Switch frequency bucket summary was generated.
  - Status: captured

- Evidence-Type: file_output
  - Artifact: `epics/ep_012_adaptive_strategy_selection_engine/results/learned/rank1_gap_switch_events_clean_forex_only.csv`
  - Objective-Proved: Raw switch events with `rank1_count_cum`, held count, gap, and bucket were generated.
  - Status: captured

## Implementation Log

- 2026-04-21 12:14:40 BST — Computed switch-time `rank1_count_cum` buckets for strict gap rules on clean forex-only dates.

## Changes Made

- Generated bucket summary CSV/Markdown and raw switch-event CSV.

## Validation

- Command completed successfully and printed bucket distribution table.

## Risks/Notes

- Buckets count switch events, not all rank-1 observations.
- For `gap>X`, higher thresholds mechanically shift switch events into higher count buckets.

## Completion Status

COMPLETE -- 2026-04-21 12:15 BST
