---
Task Type: standard
Task Attributes:
  workflow_task: true
  workflow_name: adaptive_strategy_selection_engine
  workflow_stage: backlog
  depends_on:
    - 20260417_150400_rl_sel_phase4_evaluation
  feeds_into:
    - 20260417_150500_rl_sel_phase5_finalization
---
**Epic:** adaptive_strategy_selection_engine
**Depends On:** 20260417_150400_rl_sel_phase4_evaluation.md

# Phase 3b: Learned Selector v2 -- Absolute Reward Fix

**Source:** Phase 4 evaluation verdict (REJECTED) + root cause diagnosis
**Destination Folder:** `epics/ep_012_adaptive_strategy_selection_engine/results/learned/`
**Dependency:** Phase 4 REJECTED verdict; root cause confirmed

## Task Summary
Phase 3 was REJECTED (-49.35% vs Baseline B). Root cause: delta_net reward made Q_hold
negative when positions slightly declined, causing model to prefer FLAT (17.1% FLAT rate).
Fix: replace delta_net with absolute next_net as the reward signal so holding a profitable
position is always rewarded positively. Rerun forex walk-forward; check if FLAT rate drops
and improvement vs baseline improves.

## Change
- `reward_vec()` in selector_v2.py: replace `delta = next_net - current_net; reward = delta`
  with `reward = next_net.copy()` (absolute value, not change)
- Output to `results/learned/` with `_v2` suffix on output files

## Plan
- [x] 1. Copy selector.py to selector_v2.py
  - Evidence: file exists
- [x] 2. Apply reward fix: reward = next_net (absolute) instead of delta_net
  - Evidence: reward_vec() updated; verified Q_hold > 0 when next_net > 0
- [x] 3. Run forex walk-forward with selector_v2.py
  - Test: FLAT% lower than v1's 17.1%; total switches fewer than v1's 343
  - Evidence: avg_flat_pct~10% (down from 17.1%); total_switches=119 (down from 343) -- PASS
- [x] 4. Compare v2 aggregate vs baselines and v1
  - Test: improvement_vs_baseline_b > -49.35% (better than v1)
  - Evidence: improvement_vs_baseline_b=-5.2% (up from -49.35%) -- PASS; still below +25% threshold
- [x] 5. Save fold_summary_learned_v2.csv and aggregate_learned_v2.json
  - Evidence: files exist at destination

## Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: false

- Evidence-Type: file_output
  - Artifact: epics/ep_012_adaptive_strategy_selection_engine/results/learned/aggregate_learned_v2.json
  - Objective-Proved: v2 aggregate performance vs baselines
  - Status: delivered

## Validation
```
Phase 3b COMPLETE
total_net_v2: 26400, avg_net_per_day: 1015.4, total_switches: 119
avg_hold_pct: 87.9%, avg_flat_pct: ~10%, days_tested: 26
vs Baseline B (27850): improvement = -5.2% (up from -49.35% in v1)
vs v1 (14105): net improvement +87%; switches -65%; FLAT -7pp
Verdict: IMPROVING but below +25% acceptance threshold
```

## Implementation Log
- 2026-04-18: Copied selector.py to selector_v2.py
- 2026-04-18: Changed reward_vec to use absolute next_net
- 2026-04-18: Ran forex walk-forward; run_log_v2.txt confirms 26/26 folds complete

## Changes Made
- Created: epics/ep_012_adaptive_strategy_selection_engine/results/learned/selector_v2.py
- Created: epics/ep_012_adaptive_strategy_selection_engine/results/learned/fold_summary_learned_v2.csv
- Created: epics/ep_012_adaptive_strategy_selection_engine/results/learned/aggregate_learned_v2.json

## Completion Status
COMPLETE -- 2026-04-18
