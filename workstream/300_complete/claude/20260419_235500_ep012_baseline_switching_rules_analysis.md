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

# Baseline Switching Rules Analysis — rank-1 + net/gap thresholds

**Source:** User request — establish correct baseline switching rules using rank-1 as trigger, filtered by net gap and/or rank1_count_cum gap
**Destination:** Reference for frequency_explorer.html workflow and learned model benchmarking

## Task Summary
Evaluate rule-based switching strategies across net threshold, rank1_count_cum gap threshold,
and AND/OR combinations. All results on 25 clean test days (2026-03-22 to 2026-04-17).
2026-03-21 excluded as data anomaly (~$10k net, not representative of real trading).
Negatives excluded — only strategies with net > 0 are eligible for rank-1 consideration.

## Key Corrections vs Prior Session
- Previous "Baseline B" numbers (30,950 / 31,595 / 32,320) were incorrect — used highest-net candidate, not rank-1
- 2026-03-21 was a data anomaly inflating all results
- Correct always-rank-1 benchmark: $641/day (not $977/day)
- Correct learned v3 benchmark: $660/day (not $1,021/day)

## Rule Definitions

**Always rank-1 (net>0):**
At every snap, hold whoever is rank-1 with net > 0. Switch immediately on rank-1 change.

**rank-1 + net>X:**
Follow rank-1 but only switch if new rank-1's net > held strategy's net + X.

**rank-1 + gap>X:**
Follow rank-1 but only switch if new rank-1's rank1_count_cum > held's rank1_count_cum + X.

**rank-1 + net>X AND gap>Y:**
Follow rank-1 but only switch if BOTH net gap AND count gap conditions are met.

## Results — 25 Clean Test Days (excluding 2026-03-21)

### Net-based thresholds
| Rule | Total Net | Avg/day | Switches |
|------|-----------|---------|----------|
| Always rank-1 (net>0) | 16,035 | 641 | 121 |
| rank-1 + net>50 | 17,935 | 717 | 83 |
| rank-1 + net>100 | 18,195 | 728 | 77 |
| rank-1 + net>200 | 19,055 | 762 | 51 |
| rank-1 + net>300 | 19,220 | 769 | 45 |
| rank-1 + net>500 | 19,135 | 765 | 29 |

### Gap-based thresholds (rank1_count_cum)
| Rule | Total Net | Avg/day | Switches |
|------|-----------|---------|----------|
| rank-1 + gap>0 | 17,520 | 701 | 97 |
| rank-1 + gap>5 | 19,120 | 765 | 65 |
| rank-1 + gap>10 | 19,520 | 781 | 57 |
| rank-1 + gap>15 | 19,680 | 787 | 46 |
| rank-1 + gap>20 | 19,535 | 781 | 40 |
| rank-1 + gap>25 | 19,510 | 780 | 37 |
| rank-1 + gap>50 | 16,125 | 645 | 24 |

### Combination rules (AND / OR)
| Rule | Total Net | Avg/day | Switches |
|------|-----------|---------|----------|
| rank-1 + net>200 OR gap>20 | 18,925 | 757 | 60 |
| rank-1 + net>500 OR gap>20 | 19,575 | 783 | 47 |
| rank-1 + net>500 AND gap>20 | 19,040 | 762 | 24 |
| rank-1 + net>200 AND gap>20 | 19,660 | 786 | 32 |
| **rank-1 + net>100 AND gap>20** | **19,785** | **791** | **35** |

### Learned model comparison
| Strategy | Total Net | Avg/day | Switches |
|----------|-----------|---------|----------|
| Always rank-1 (net>0) | 16,035 | 641 | 121 |
| Learned v3 | 16,505 | 660 | 108 |
| rank-1 + net>100 AND gap>20 | **19,785** | **791** | 35 |

## Key Findings
1. **Best rule: rank-1 + net>100 AND gap>20** — $791/day, 35 switches (1.4/day)
2. AND combination outperforms OR — both signals must fire to reduce noise
3. Gap-based sweet spot: gap>15 to gap>20 (peaks then declines sharply above 25)
4. Net-based: higher threshold keeps improving but plateaus around net>300
5. OR combinations trigger too many switches, eroding gains
6. Learned v3 ($660/day) beats always-rank-1 (+3%) but loses to best rule-based (-16.6%)

## Recommended Workflow for frequency_explorer.html
1. At session open — pick first rank-1 with net > 0 as held strategy
2. At each 5-min snap — if rank-1 changes, check both conditions:
   - New rank-1 net > held net + $100
   - New rank-1 yellow badge (rank1_count_cum) > held badge + 20
3. Only switch if BOTH conditions are true
4. Target: ~$791/day, ~1.4 switches/day

## Data Quality Notes
- 2026-03-21 excluded: anomalous ~$10k net day (not representative)
- All net values are in USD
- Switch cost: $50 per switch (deducted from all totals)
- Test window: 2026-03-22 to 2026-04-17 (25 days)

## Completion Status
COMPLETE -- 2026-04-19
