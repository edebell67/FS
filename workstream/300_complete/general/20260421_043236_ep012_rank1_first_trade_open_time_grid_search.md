---
Task Type: standard
Task Attributes:
  workflow_task: true
  workflow_name: adaptive_strategy_selection_engine
  workflow_stage: complete
  depends_on: [20260419_235000_ep012_rank1_filtered_grid_search]
  feeds_into: []
---
**Epic:** adaptive_strategy_selection_engine

# Rank-1 Filtered Switching Grid Search With First-Trade Open-Time Cutoffs

**Source:** User request on 2026-04-21 to rerun the completed rank-1 filtered grid search with alternative first-trade open-time options.

**Task Summary:** Re-run the rank-1 filtered switching analysis while changing the first eligible opening trade time. Compare the prior opening baseline against two requested scenarios: first trade open after 02:00am and first trade open after 03:00am.

**Context:** Builds on completed task `workstream/300_complete/claude/20260419_235000_ep012_rank1_filtered_grid_search.md`, which corrected the baseline switching rule to use rank-1 as the switch target with net-gap thresholds. Prior best result was `rank-1 + net>200`.

**Destination Folder:** `epics/ep_012_adaptive_strategy_selection_engine/results/learned/`

**Dependency:** Completed rank-1 filtered analysis and reusable grid-search implementation, expected around `epics/ep_012_adaptive_strategy_selection_engine/results/learned/grid_search.py`.

## Requirements

1. Add or parameterize first-trade-open cutoff time in the rank-1 filtered analysis.
2. Re-run the rank-1 filtered threshold grid using first eligible opening trade after 02:00am.
3. Re-run the same grid using first eligible opening trade after 03:00am.
4. Compare both requested scenarios against the existing completed baseline.
5. Report total net, average/day, and switch count for each threshold and cutoff.
6. Identify whether the best rule changes from `rank-1 + net>200` under either cutoff.

## Analysis Options

- First trade open after `02:00am`
- First trade open after `03:00am`

## Plan

- [x] 1. Locate the existing rank-1 filtered grid-search implementation and confirm current opening-trade cutoff behavior.
  - [x] Test: `rg -n "run_filtered_r1|opening|rank-1|threshold|grid" epics/ep_012_adaptive_strategy_selection_engine TradeApps/breakout/fs`
  - Evidence: Existing `results/learned/grid_search.py` found, but it still contains the older highest-candidate baseline implementation rather than the corrected `run_filtered_r1` described in `20260419_235000_ep012_rank1_filtered_grid_search.md`.

- [x] 2. Add a cutoff parameter for first eligible opening trade time without changing unrelated switching logic.
  - [x] Test: Code review confirms the parameter affects only initial trade selection and does not alter post-open switching rules.
  - Evidence: Added `rank1_open_time_grid_search.py`; `open_hour` only controls first eligible snapshot at/after cutoff, while later switch logic remains rank-1 change plus net-gap threshold.

- [x] 3. Run grid search for first trade open after 02:00am.
  - [x] Test: Execute the grid-search command and capture total net, avg/day, and switches per threshold.
  - Evidence: `python epics/ep_012_adaptive_strategy_selection_engine/results/learned/rank1_open_time_grid_search.py --product-type forex --open-hours 1,2,3` generated 02:00 results in CSV/Markdown; best 02:00 rule is `rank-1 + net>25`, total `19,140`, avg/day `736`, switches `16`.

- [x] 4. Run grid search for first trade open after 03:00am.
  - [x] Test: Execute the grid-search command and capture total net, avg/day, and switches per threshold.
  - Evidence: Same command generated 03:00 results; best 03:00 rule is `rank-1 + net>25`, total `19,525`, avg/day `751`, switches `15`.

- [x] 5. Produce a concise comparison table and recommendation.
  - [x] Test: Output artifact includes both cutoff scenarios, best threshold per scenario, and comparison to the prior `rank-1 + net>200` result.
  - Evidence: `rank1_open_time_grid_search_forex.md` includes best-by-cutoff and full threshold tables for 01:00, 02:00, and 03:00.

## Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true

- Evidence-Type: test_output
  - Artifact: `python epics/ep_012_adaptive_strategy_selection_engine/results/learned/rank1_open_time_grid_search.py --product-type forex --open-hours 1,2,3`
  - Objective-Proved: Grid search was executed for the 02:00am and 03:00am first-open cutoffs.
  - Status: captured

- Evidence-Type: file_output
  - Artifact: `epics/ep_012_adaptive_strategy_selection_engine/results/learned/rank1_open_time_grid_search_forex.csv`
  - Objective-Proved: Result table/report exists under the declared destination folder.
  - Status: captured

- Evidence-Type: manual_verification
  - Artifact: `epics/ep_012_adaptive_strategy_selection_engine/results/learned/rank1_open_time_grid_search_forex.md`
  - Objective-Proved: Results are readable and compare the requested cutoff options against the prior baseline.
  - Status: captured

## Implementation Log

- 2026-04-21 04:32:36 BST — Created backlog task from user request to rerun rank-1 filtered analysis with first-trade-open cutoffs after 02:00am and 03:00am.
- 2026-04-21 04:36 BST — Located task file under `workstream/300_complete/codex/` with `PENDING` status; moved the same lifecycle file back to `workstream/200_inprogress/general/` before implementation.
- 2026-04-21 04:43 BST — Added reproducible analysis script and ran the requested grid search for forex data across 26 days (`2026-03-21` to `2026-04-17`), including 01:00 comparison baseline plus requested 02:00 and 03:00 cutoffs.

## Changes Made

- Created `epics/ep_012_adaptive_strategy_selection_engine/results/learned/rank1_open_time_grid_search.py`.
- Generated `epics/ep_012_adaptive_strategy_selection_engine/results/learned/rank1_open_time_grid_search_forex.csv`.
- Generated `epics/ep_012_adaptive_strategy_selection_engine/results/learned/rank1_open_time_grid_search_forex.md`.
- Moved lifecycle file to `workstream/200_inprogress/general/20260421_043236_ep012_rank1_first_trade_open_time_grid_search.md` during implementation.

## Results Summary

| First open cutoff | Best rule | Total net | Avg/day | Switches | Days |
|---|---:|---:|---:|---:|---:|
| 01:00 | rank-1 + net>25 | 18,935 | 728 | 20 | 26 |
| 02:00 | rank-1 + net>25 | 19,140 | 736 | 16 | 26 |
| 03:00 | rank-1 + net>25 | 19,525 | 751 | 15 | 26 |

Requested scenario result:
- 02:00 improves over the 01:00 run in this dataset by `+205` total net and reduces switches by `4`.
- 03:00 is the best of the tested first-open cutoffs, improving over 01:00 by `+590` total net and reducing switches by `5`.
- The best threshold in these reruns is `net>25`, not `net>200`.

## Validation

- `python epics/ep_012_adaptive_strategy_selection_engine/results/learned/rank1_open_time_grid_search.py --product-type forex --open-hours 1,2,3`
  - Passed. Loaded `26` forex days and wrote CSV/Markdown artifacts.
- `python -m py_compile epics/ep_012_adaptive_strategy_selection_engine/results/learned/rank1_open_time_grid_search.py`
  - Passed. Script compiles successfully.
- `Get-Content -Raw epics/ep_012_adaptive_strategy_selection_engine/results/learned/rank1_open_time_grid_search_forex.md`
  - Passed. Markdown report is readable and includes requested 02:00/03:00 scenarios.

## Risks/Notes

- The previous analysis used 26 test days from 2026-03-21 to 2026-04-17; implementation should preserve the same test window unless explicitly changed.
- The cutoff should only control the first opening trade, not later switch eligibility, unless analysis shows the existing implementation couples those concepts.
- If no eligible positive rank-1 exists after a cutoff on a given day, the result should explicitly document skip/hold behavior.
- The existing `grid_search.py` does not match the completed Claude task description for corrected `run_filtered_r1`; a new focused script was added instead of rewriting that older file.
- Results are for `forex` only, matching the existing `grid_search.py` default scope and recent switch-signal context. Other product types can be run with `--product-type`.

## Completion Status

COMPLETE -- 2026-04-21 04:45 BST
