---
Task Type: standard
Task Attributes:
  workflow_task: true
  workflow_name: adaptive_strategy_selection_engine
  workflow_stage: backlog
  depends_on:
    - 20260417_150300_rl_sel_phase3_learned_selector
  feeds_into:
    - 20260417_150500_rl_sel_phase5_finalization
---
**Epic:** adaptive_strategy_selection_engine
**Depends On:** 20260417_150300_rl_sel_phase3_learned_selector.md


# Phase 4: Comparative Evaluation — Learned vs Baselines Full Report

**Source:** `workstream/000_epic/selection_strategy_rl_prd.md` (→ `_processed.md`)
**Destination Folder:** `epics/ep_012_adaptive_strategy_selection_engine/results/evaluation/`
**Dependency:** Phase 2 baseline results and Phase 3 learned predictions must both exist

## Task Summary
Produce the definitive day-by-day comparison between the learned selector and both baselines. Generate all 4 required reports (daily results, aggregate, behavior diagnostics, feature audit). Determine whether the ≥25% improvement threshold is met and emit explicit ACCEPTED/REJECTED verdict.

## Context
- Proof threshold: learned cumulative net ≥ 25% better than best baseline (configurable)
- No design changes to features, rewards, or model permitted after this phase starts
- All comparisons on out-of-sample test days only (walk-forward)

## Plan
- [x] 1. Load and align: 26 forex rows from baselines + 26 forex rows from learned; inner join on (product_type, date)
  - Evidence: "26 aligned day-rows across ['forex']"; 0 nulls in net columns
- [x] 2. Switching cost verified: learned day_net = final_net - switch_count * 50 (from Phase 3 simulate_test_day)
  - Evidence: fold_summary_learned.csv switch_count column; $50 cost applied per switch
- [x] 3. Per-day metrics: baseline_a/b_net, learned_net, switches, hold_avg, positive_rate, flat_pct -- all non-null
  - Evidence: null_check = {baseline_a_net:0, baseline_b_net:0, learned_net:0}
- [x] 4. daily_results.csv saved with 26 rows
  - Evidence: file exists at evaluation/daily_results.csv
- [x] 5. aggregate_results.json saved; accepted=false
  - Evidence: verdict=REJECTED, improvement=-49.35%, threshold=25%
- [x] 6. behavior_diagnostics.json: 343 SWITCH decisions; HOLD=72.4%, SWITCH=6.1%, FLAT=21.5%; root cause documented
  - Evidence: file exists; sample_switch_decisions present
- [x] 7. feature_audit.md: 19 features listed; all confirmed live-safe; 5 sample decisions included
  - Evidence: file exists at evaluation/feature_audit.md; leakage verdict=CLEAN
- [x] 8. Verdict printed: REJECTED, improvement=-49.35%, threshold=25%
  - Evidence: console output shows exact values

## Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: false

- Evidence-Type: file_output
  - Artifact: epics/ep_012_adaptive_strategy_selection_engine/results/evaluation/daily_results.csv (26 rows)
  - Objective-Proved: Per-day comparison across all three selectors
  - Status: delivered

- Evidence-Type: file_output
  - Artifact: epics/ep_012_adaptive_strategy_selection_engine/results/evaluation/aggregate_results.json
  - Objective-Proved: REJECTED -- learned $14,105 vs best baseline $27,850 (-49.35%)
  - Status: delivered

- Evidence-Type: file_output
  - Artifact: epics/ep_012_adaptive_strategy_selection_engine/results/evaluation/behavior_diagnostics.json
  - Objective-Proved: 343 switches annotated; FLAT bias diagnosed (root cause: delta_net reward)
  - Status: delivered

- Evidence-Type: file_output
  - Artifact: epics/ep_012_adaptive_strategy_selection_engine/results/evaluation/feature_audit.md
  - Objective-Proved: All 19 features confirmed live-safe; leakage verdict=CLEAN
  - Status: delivered

- Evidence-Type: log_output
  - Artifact: VERDICT: REJECTED | improvement=-49.35% | threshold=+25%
  - Objective-Proved: Clear fail outcome with root cause
  - Status: delivered

## Implementation Log
- 2026-04-18: evaluate.py written; 26 aligned forex rows; all 4 reports generated
- 2026-04-18: Verdict REJECTED: learned=$14,105 vs Baseline B=$27,850 (-49.35%)
- 2026-04-18: Root cause: delta_net reward => Q_hold often negative => FLAT preferred (17.1% avg)

## Changes Made
- Created: epics/ep_012_adaptive_strategy_selection_engine/results/evaluation/evaluate.py
- Created: epics/ep_012_adaptive_strategy_selection_engine/results/evaluation/daily_results.csv (26 rows)
- Created: epics/ep_012_adaptive_strategy_selection_engine/results/evaluation/aggregate_results.json
- Created: epics/ep_012_adaptive_strategy_selection_engine/results/evaluation/behavior_diagnostics.json
- Created: epics/ep_012_adaptive_strategy_selection_engine/results/evaluation/feature_audit.md

## Validation
```
VERDICT: REJECTED | improvement=-49.35% | threshold=+25%
Learned=$14,105 | Best baseline B=$27,850 | Days beats B=2/26
HOLD=72.4%, FLAT=17.1%, Switches L=343 vs B=90
Phase 4 COMPLETE
```

## Risks/Notes
- Per PRD: REJECTED requires new Phase 3 task before retraining
- Fix identified: replace delta_net reward with absolute next_net reward
- High switch count (343 vs 90) secondary symptom of Q_switch overestimation

## Completion Status
COMPLETE -- 2026-04-18
