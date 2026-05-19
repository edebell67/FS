---
Task Type: standard
Task Attributes:
  workflow_task: true
  workflow_name: adaptive_strategy_selection_engine
  workflow_stage: in_progress
  depends_on: [20260421_043236_ep012_rank1_first_trade_open_time_grid_search]
  feeds_into: []
---
**Epic:** adaptive_strategy_selection_engine

# Enforce Valid Rank-1 Switch Criteria

**Source:** User clarification on 2026-04-21: only `rank-1 + net>X`, `rank-1 + gap>X`, and explicit AND/OR combinations are valid switching criteria. No implicit missing-held-net fallback and no switching without a configured criterion.

**Task Summary:** Replace the ambiguous open-time grid-search implementation with strict rank-1 switch criteria and regenerate results using only valid rule families.

**Context:** Prior reruns mixed assumptions around missing held net. This task locks the analysis definition so results are reliable and interpretable.

**Destination Folder:** `epics/ep_012_adaptive_strategy_selection_engine/results/learned/`

**Dependency:** `epics/ep_012_adaptive_strategy_selection_engine/results/learned/rank1_open_time_grid_search.py`

## Valid Criteria

- `rank-1 + net>X`: switch when new rank-1 net is greater than previous held rank-1 net plus `X`.
- `rank-1 + gap>X`: switch when new rank-1 cumulative rank-1 count is greater than previous held rank-1 cumulative count plus `X`.
- Explicit `AND` / `OR` combinations may be tested only when both component criteria are present.

## Plan

- [x] 1. Update the analysis script to remove implicit missing-held-net switching and support strict valid rule families.
  - [x] Test: Manual review confirms switches only occur through `net`, `gap`, `and`, or `or` criteria.
  - Evidence: `rank1_open_time_grid_search.py` now exposes `--rule-family net|gap|and|or`; missing held comparison data does not trigger a switch.

- [x] 2. Re-run strict net-only open-time analysis for 00:00, 01:00, 02:00, and 03:00.
  - [x] Test: `python epics/ep_012_adaptive_strategy_selection_engine/results/learned/rank1_open_time_grid_search.py --product-type forex --open-hours 0,1,2,3 --rule-family net --output-stem rank1_open_time_strict_net`
  - Evidence: Generated `rank1_open_time_strict_net_forex.csv` and `rank1_open_time_strict_net_forex.md`.

- [x] 3. Validate script syntax and generated report.
  - [x] Test: `python -m py_compile epics/ep_012_adaptive_strategy_selection_engine/results/learned/rank1_open_time_grid_search.py`
  - Evidence: Compile passed; generated strict net Markdown report was read successfully.

## Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true

- Evidence-Type: diff
  - Artifact: `epics/ep_012_adaptive_strategy_selection_engine/results/learned/rank1_open_time_grid_search.py`
  - Objective-Proved: Script enforces only valid rank-1 switch criteria.
  - Status: captured

- Evidence-Type: test_output
  - Artifact: `python epics/ep_012_adaptive_strategy_selection_engine/results/learned/rank1_open_time_grid_search.py --product-type forex --open-hours 0,1,2,3 --rule-family net --output-stem rank1_open_time_strict_net`
  - Objective-Proved: Strict rerun completed successfully.
  - Status: captured

- Evidence-Type: file_output
  - Artifact: `epics/ep_012_adaptive_strategy_selection_engine/results/learned/rank1_open_time_strict_net_forex.md`
  - Objective-Proved: Strict result artifacts were generated.
  - Status: captured

## Implementation Log

- 2026-04-21 10:54:58 BST — Created task after user clarified valid switch criteria and rejected implicit fallback semantics.
- 2026-04-21 10:58 BST — Updated script to support strict `net`, `gap`, `and`, and `or` rule families and removed implicit missing-held-net switching.
- 2026-04-21 11:00 BST — Ran strict net-only analysis for 00:00, 01:00, 02:00, and 03:00 first-open cutoffs.

## Changes Made

- Updated `epics/ep_012_adaptive_strategy_selection_engine/results/learned/rank1_open_time_grid_search.py`.
- Generated `epics/ep_012_adaptive_strategy_selection_engine/results/learned/rank1_open_time_strict_net_forex.csv`.
- Generated `epics/ep_012_adaptive_strategy_selection_engine/results/learned/rank1_open_time_strict_net_forex.md`.

## Strict Net-Only Results Summary

| First open cutoff | Best strict net rule | Total net | Avg/day | Switches | Days |
|---|---:|---:|---:|---:|---:|
| 00:00 | rank-1 + net>25 | 7,485 | 288 | 18 | 26 |
| 01:00 | rank-1 + net>25 | 18,935 | 728 | 20 | 26 |
| 02:00 | rank-1 + net>25 | 19,140 | 736 | 16 | 26 |
| 03:00 | rank-1 + net>25 | 19,525 | 751 | 15 | 26 |

## Validation

- `python epics/ep_012_adaptive_strategy_selection_engine/results/learned/rank1_open_time_grid_search.py --product-type forex --open-hours 0,1,2,3 --rule-family net --output-stem rank1_open_time_strict_net`
  - Passed. Loaded `26` forex days and wrote strict net artifacts.
- `python -m py_compile epics/ep_012_adaptive_strategy_selection_engine/results/learned/rank1_open_time_grid_search.py`
  - Passed.
- `Get-Content -Raw epics/ep_012_adaptive_strategy_selection_engine/results/learned/rank1_open_time_strict_net_forex.md`
  - Passed. Report includes strict net-only results and states no implicit missing-held-net fallback is used.

## Risks/Notes

- Prior `rank1_open_time_grid_search_corrected_*` outputs are superseded for decision-making because they used an implicit missing-held-net fallback that is not a valid criterion.
- Strict results still depend on current snapshot availability for held comparison data. If held comparison data is missing, no switch occurs because neither valid criterion can be evaluated.

## Completion Status

COMPLETE -- 2026-04-21 11:00 BST
