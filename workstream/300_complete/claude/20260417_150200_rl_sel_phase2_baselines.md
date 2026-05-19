---
Task Type: standard
Task Attributes:
  workflow_task: true
  workflow_name: adaptive_strategy_selection_engine
  workflow_stage: backlog
  depends_on:
    - 20260417_150100_rl_sel_phase1_data_engineering
  feeds_into:
    - 20260417_150300_rl_sel_phase3_learned_selector
---

# Phase 2: Baselines — Implement and Evaluate Baseline A and Baseline B

**Source:** `workstream/000_epic/selection_strategy_rl_prd.md` (→ `_processed.md`)
**Destination Folder:** `epics/ep_012_adaptive_strategy_selection_engine/results/baselines/`
**Dependency:** Phase 1 processed dataset must exist in `epics/ep_012_adaptive_strategy_selection_engine/data/processed/`

## Task Summary
Implement Baseline A (persistent positive leader) and Baseline B (conservative hold-with-threshold). Run both across all available days using walk-forward partitions. Generate per-day and aggregate performance reports. These results become the proof benchmark for Phase 3.

## Context
- Locked parameters: switching_cost=$50, safety_margin=10% → effective switch threshold = held_net + $55
- Eligibility gate: `current_net > 0` hard filter on all candidates
- Input: processed dataset from Phase 1

## Baseline A: Persistent Positive Leader
At each minute:
1. Filter to candidates with `current_net > 0`
2. Select candidate with highest `rank1_appearances` (most frequent #1 in today's snapshots so far)
3. Tie-break: highest `net`
4. If none eligible: FLAT

## Baseline B: Conservative Hold-with-Threshold
At each minute:
1. If holding strategy with `current_net > 0`: HOLD unless challenger meets threshold
2. Challenger must satisfy: `challenger_net > held_net + 55` AND `challenger_net > 0`
3. If current hold goes non-positive: seek best eligible challenger; if none, FLAT
4. From FLAT: enter best eligible candidate when one appears

## Plan
- [x] 1. Implement `baseline_a(day_df) -> action_series` using rank1_appearances ranking
  - Evidence: `baselines.py` line 43-64; per-snap rank1_counts dict built cumulatively; FLAT emitted when eligible empty
- [x] 2. Implement `baseline_b(day_df, switching_cost=50, safety_margin=5) -> action_series`
  - Evidence: `baselines.py` line 67-113; B switches (446) < A switches (481) confirmed in aggregate
- [x] 3. Implement simulation engine: given action series, compute cumulative net after switching cost
  - Evidence: `baselines.py` line 116-158; day_net = final_net - switch_count * 50
- [x] 4. Run both baselines across all days using walk-forward partitions from Phase 1
  - Evidence: 132 rows in CSV (5 product types x ~26 folds); no errors
- [x] 5. Generate `daily_results_baselines.csv`
  - Evidence: 132 rows, 0 nulls in net columns confirmed by script output
- [x] 6. Generate `aggregate_baselines.json`
  - Evidence: total_net_a=177400, total_net_b=181155, best_baseline=B
- [x] 7. Save both files to `epics/ep_012_adaptive_strategy_selection_engine/results/baselines/`
  - Evidence: files confirmed at declared destination

## Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true

- Evidence-Type: file_output
  - Artifact: epics/ep_012_adaptive_strategy_selection_engine/results/baselines/daily_results_baselines.csv
  - Objective-Proved: Per-day baseline performance recorded (132 rows, 0 nulls)
  - Status: delivered

- Evidence-Type: file_output
  - Artifact: epics/ep_012_adaptive_strategy_selection_engine/results/baselines/aggregate_baselines.json
  - Objective-Proved: Aggregate totals and best-baseline identified (best=B, B_net=181155 > A_net=177400)
  - Status: delivered

- Evidence-Type: log_output
  - Artifact: Console output — Baseline B switches (446) < A switches (481): true
  - Objective-Proved: Baseline B exhibits conservative hold behavior
  - Status: delivered

## Implementation Log
- 2026-04-17: Implemented baseline_a, baseline_b, simulate() in baselines.py
- 2026-04-17: Loaded 172276 rows from 157 parquet files across 5 product types
- 2026-04-17: Ran all 132 walk-forward folds without errors
- 2026-04-17: Output files written to results/baselines/

## Changes Made
- Created: epics/ep_012_adaptive_strategy_selection_engine/results/baselines/baselines.py
- Created: epics/ep_012_adaptive_strategy_selection_engine/results/baselines/daily_results_baselines.csv (132 rows)
- Created: epics/ep_012_adaptive_strategy_selection_engine/results/baselines/aggregate_baselines.json

## Validation
```
python baselines.py
Loaded 172276 rows, 33 dates, 5 product types
Saved daily CSV: ...daily_results_baselines.csv (132 rows)
Null check: {'baseline_a_net': 0, 'baseline_b_net': 0}
total_net_a: 177400, total_net_b: 181155, best_baseline: B
Baseline B switches (446) < A (481): True
Phase 2 COMPLETE
```

## Risks/Notes
- Baseline A restarts selection from scratch each minute — it does not carry forward a held position, unlike Baseline B
- positive_rate = % of selected strategies still net > 0 five minutes after selection
- If fewer than 5 minutes remain in the day, skip positive_rate for those tail entries

## Completion Status
COMPLETE — 2026-04-17
