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

# Correct Missing Held-Net Switch Fallback

**Source:** User clarification on 2026-04-21: if held net is missing, switch evaluation should behave as `rank-1 + net>0`, not skip the switch and not require `rank-1 + net>threshold`.

**Task Summary:** Update the rank-1 open-time grid-search rerun so missing held-net snapshots use positive rank-1 fallback switching. Re-run the midnight/01:00/02:00/03:00 comparison and regenerate result artifacts.

**Context:** The first rerun script skipped switch checks when the held strategy was absent from the current snapshot. That undercounted switches versus the intended rule and likely explains the discrepancy with older switch counts.

**Destination Folder:** `epics/ep_012_adaptive_strategy_selection_engine/results/learned/`

**Dependency:** `epics/ep_012_adaptive_strategy_selection_engine/results/learned/rank1_open_time_grid_search.py`

## Plan

- [x] 1. Patch missing held-net behavior in `rank1_open_time_grid_search.py`.
  - [x] Test: Manual code review confirms missing held net switches to any positive changed rank-1 candidate.
  - Evidence: Updated missing-held-net branch so it switches when `held_net is None` and changed rank-1 has positive net.

- [x] 2. Re-run analysis for `00:00`, `01:00`, `02:00`, and `03:00`.
  - [x] Test: `python epics/ep_012_adaptive_strategy_selection_engine/results/learned/rank1_open_time_grid_search.py --product-type forex --open-hours 0,1,2,3 --output-stem rank1_open_time_grid_search_corrected`
  - Evidence: Generated corrected CSV/Markdown results; switch counts now align with the intended fallback behavior.

- [x] 3. Validate script syntax and regenerated reports.
  - [x] Test: `python -m py_compile epics/ep_012_adaptive_strategy_selection_engine/results/learned/rank1_open_time_grid_search.py`
  - Evidence: Compile passed; Markdown report was read successfully.

## Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true

- Evidence-Type: diff
  - Artifact: `epics/ep_012_adaptive_strategy_selection_engine/results/learned/rank1_open_time_grid_search.py`
  - Objective-Proved: Missing held-net fallback is implemented.
  - Status: captured

- Evidence-Type: test_output
  - Artifact: `python epics/ep_012_adaptive_strategy_selection_engine/results/learned/rank1_open_time_grid_search.py --product-type forex --open-hours 0,1,2,3 --output-stem rank1_open_time_grid_search_corrected`
  - Objective-Proved: Corrected analysis was executed.
  - Status: captured

- Evidence-Type: file_output
  - Artifact: `epics/ep_012_adaptive_strategy_selection_engine/results/learned/rank1_open_time_grid_search_corrected_forex.md`
  - Objective-Proved: Corrected result artifacts were generated.
  - Status: captured

## Implementation Log

- 2026-04-21 10:03:27 BST — Created correction task after user clarified missing held-net switch behavior.
- 2026-04-21 10:06 BST — Patched script and reran corrected analysis for 00:00, 01:00, 02:00, and 03:00 first-open cutoffs.

## Changes Made

- Updated `epics/ep_012_adaptive_strategy_selection_engine/results/learned/rank1_open_time_grid_search.py` so missing `held_net` falls back to switching to the positive changed rank-1 candidate.
- Generated `epics/ep_012_adaptive_strategy_selection_engine/results/learned/rank1_open_time_grid_search_corrected_forex.csv`.
- Generated `epics/ep_012_adaptive_strategy_selection_engine/results/learned/rank1_open_time_grid_search_corrected_forex.md`.

## Corrected Results Summary

| First open cutoff | Best rule | Total net | Avg/day | Switches | Days |
|---|---:|---:|---:|---:|---:|
| 00:00 | rank-1 + net>500 | 28,425 | 1,093 | 76 | 26 |
| 01:00 | rank-1 + net>300 | 28,875 | 1,111 | 67 | 26 |
| 02:00 | rank-1 + net>300 | 28,925 | 1,112 | 66 | 26 |
| 03:00 | rank-1 + net>300 | 29,075 | 1,118 | 63 | 26 |

Key comparison:
- `02:00 rank-1 + net>300`: `28,925`, `1,112/day`, `66` switches.
- `01:00 rank-1 + net>300`: `28,875`, `1,111/day`, `67` switches.
- Delaying to 02:00 is only marginally better than 01:00 under corrected missing-held-net behavior.

## Validation

- `python epics/ep_012_adaptive_strategy_selection_engine/results/learned/rank1_open_time_grid_search.py --product-type forex --open-hours 0,1,2,3 --output-stem rank1_open_time_grid_search_corrected`
  - Passed. Loaded `26` forex days and wrote corrected CSV/Markdown artifacts.
- `python -m py_compile epics/ep_012_adaptive_strategy_selection_engine/results/learned/rank1_open_time_grid_search.py`
  - Passed.
- `Get-Content -Raw epics/ep_012_adaptive_strategy_selection_engine/results/learned/rank1_open_time_grid_search_corrected_forex.md`
  - Passed. Report includes corrected full results.

## Risks/Notes

- This changes prior rerun results materially and supersedes the earlier `rank1_open_time_grid_search_forex.*` outputs for decision-making.
- Corrected output files use the `rank1_open_time_grid_search_corrected_*` stem. Earlier non-corrected result files should be treated as superseded.

## Completion Status

COMPLETE -- 2026-04-21 10:07 BST
