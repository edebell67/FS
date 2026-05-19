---
Task Type: standard
Task Attributes:
  workflow_task: true
  workflow_name: adaptive_strategy_selection_engine
  workflow_stage: complete
  depends_on: []
  feeds_into: []
---
**Epic:** adaptive_strategy_selection_engine

# Rank-1 Filtered Switching Grid Search

**Source:** User request — rerun baseline grid search using rank-1 as the switch trigger, filtered by net gap threshold
**Destination:** `epics/ep_012_adaptive_strategy_selection_engine/results/learned/grid_search.py`

## Task Summary
Correct the baseline B switching rule to use rank-1 as the switch target (not highest-net candidate), with an optional net gap filter. Grid search across thresholds to find the optimal rule.

## Rule Definition
At each 5-min snapshot:
- Identify current rank-1 strategy
- If rank-1 has changed AND new rank-1's net > held strategy's net + threshold → switch
- Otherwise hold

This differs from "always follow rank-1" (which switches unconditionally) and from the previous incorrect "net threshold" rule (which used highest-net candidate, ignoring rank).

## Plan
- [x] 1. Implement `run_filtered_r1(threshold)` in grid_search.py
- [x] 2. Run grid search across thresholds: -9999 (always), 0, 25, 50, 75, 100, 150, 200, 300, 500
- [x] 3. Compare against always-follow-rank-1 and learned v3

## Results (26 test days, 2026-03-21 to 2026-04-17)

| Rule | Total Net | Avg/day | Switches |
|------|-----------|---------|----------|
| Always rank-1 (no filter) | 25,415 | 977 | 162 |
| rank-1 + net>0 | 25,565 | 983 | 139 |
| rank-1 + net>25 | 26,715 | 1,027 | 116 |
| rank-1 + net>50 | 27,615 | 1,062 | 98 |
| rank-1 + net>75 | 27,675 | 1,064 | 96 |
| rank-1 + net>100 | 27,925 | 1,074 | 91 |
| rank-1 + net>150 | 28,130 | 1,082 | 84 |
| **rank-1 + net>200** | **28,935** | **1,113** | **62** |
| rank-1 + net>300 | 28,455 | 1,094 | 48 |
| rank-1 + net>500 | 28,130 | 1,082 | 34 |
| Learned v3 (model) | 26,550 | 1,021 | 116 |

## Key Findings
- Best rule: **rank-1 + net>200** (28,935 total, 62 switches)
- Sweet spot before over-filtering: net>200 peaks then declines at net>300+
- Learned v3 model (26,550) is below the corrected best baseline (28,935)
- Previous "Baseline B" grid search was incorrect — used highest-net candidate, not rank-1

## Notes
- Previous session's Baseline B numbers (30,950, 31,595, 32,320) were computed with different/incorrect logic
- Correct always-follow-rank-1 benchmark: 25,415 (26 test days)
- Learned v3 beats always-rank-1 (+4.5%) but loses to rank-1+net>200 (-8.2%)
- Next step: retrain learned model using rank-1 as trigger signal rather than any-candidate

## Completion Status
COMPLETE -- 2026-04-19
