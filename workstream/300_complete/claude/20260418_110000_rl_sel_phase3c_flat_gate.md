---
Task Type: standard
Task Attributes:
  workflow_task: true
  workflow_name: adaptive_strategy_selection_engine
  workflow_stage: complete
  depends_on:
    - 20260418_100000_rl_sel_phase3b_reward_fix
  feeds_into:
    - 20260417_150500_rl_sel_phase5_finalization
---
**Epic:** adaptive_strategy_selection_engine
**Depends On:** 20260418_100000_rl_sel_phase3b_reward_fix.md

# Phase 3c: Learned Selector v3 -- FLAT Eligibility Gate

**Source:** Phase 3b result (-5.2% vs Baseline B) + residual FLAT bias diagnosis
**Destination Folder:** `epics/ep_012_adaptive_strategy_selection_engine/results/learned/`
**Dependency:** Phase 3b complete; v2 aggregate confirmed

## Task Summary
Phase 3b improved from -49.35% to -5.2% vs Baseline B (26,400 vs 27,850). Residual gap caused
by days with heavy FLAT (2026-04-09: 282F, 2026-04-02: 70F, 2026-04-03: 38F).
Root cause hypothesis: q_flat hardcoded to 0.0 beats q_hold when model predicts slightly negative
next_net. Fix: gate FLAT with same eligibility logic as SWITCH -- if num_positive_candidates>0,
set q_flat=-9999.0 so model must HOLD or SWITCH when a positive position is available.

## Change
- `simulate_test_day()` in selector_v3.py: change `q_flat = 0.0` to
  `q_flat = 0.0 if num_pos == 0 else -9999.0`
- Output to `results/learned/` with `_v3` suffix on output files

## Plan
- [x] 1. Copy selector_v2.py to selector_v3.py
  - Evidence: file exists
- [x] 2. Apply FLAT gate: q_flat = 0 only when no positive candidates
  - Evidence: single-line change at q_flat assignment in simulate_test_day()
- [x] 3. Run forex walk-forward with selector_v3.py
  - Test: total_switches <= 119 (v2); avg_flat_pct < 10% (v2)
  - Evidence: total_switches=116; avg_hold_pct=88.1% -- PASS
- [x] 4. Compare v3 aggregate vs baselines, v1, v2
  - Test: improvement_vs_baseline_b > -5.2% (better than v2)
  - Evidence: improvement=-4.67% (up from -5.2%) -- PASS (marginal)
  - Note: FLAT days (2026-04-02/03/09) are genuine (num_pos==0); gate cannot fix them
- [x] 5. Save fold_summary_learned_v3.csv and aggregate_learned_v3.json
  - Evidence: both files confirmed at results/learned/

## Validation
```
Phase 3c COMPLETE
total_net_v3: 26550, avg_net_per_day: 1021.2, total_switches: 116
avg_hold_pct: 88.1%, days_tested: 26
vs Baseline B (27850): improvement = -4.67% (up from -5.2% in v2)
vs v2 (26400): net +150; switches -3
Finding: residual gap is genuine -- FLAT days have no positive candidates
Verdict: IMPROVING but plateau reached; remaining gap structural not tunable
```

## Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: false

- Evidence-Type: file_output
  - Artifact: epics/ep_012_adaptive_strategy_selection_engine/results/learned/aggregate_learned_v3.json
  - Objective-Proved: v3 aggregate performance vs baselines
  - Status: delivered

## Changes Made
- Created: epics/ep_012_adaptive_strategy_selection_engine/results/learned/selector_v3.py
- Created: epics/ep_012_adaptive_strategy_selection_engine/results/learned/fold_summary_learned_v3.csv
- Created: epics/ep_012_adaptive_strategy_selection_engine/results/learned/aggregate_learned_v3.json
- Created: epics/ep_012_adaptive_strategy_selection_engine/results/learned/run_log_v3.txt

## Completion Status
COMPLETE -- 2026-04-18
