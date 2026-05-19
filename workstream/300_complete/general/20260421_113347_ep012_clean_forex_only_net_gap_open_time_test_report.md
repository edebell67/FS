---
Task Type: standard
Task Attributes:
  workflow_task: true
  workflow_name: adaptive_strategy_selection_engine
  workflow_stage: complete
  depends_on: [20260421_111532_ep012_clean_forex_only_open_time_results, 20260421_113015_ep012_clean_forex_only_gap_open_time_results]
  feeds_into: []
---
**Epic:** adaptive_strategy_selection_engine

# Clean Forex-Only Net/Gap Open-Time Test Report

**Source:** User request on 2026-04-21: output both strict `rank-1 + net>X` and strict `rank-1 + gap>X` clean forex-only tables to a task document describing the test.

**Task Summary:** Consolidate the clean forex-only open-time switching test into one task report with the test definition, clean-date filter, exclusions, and both result tables.

**Destination Folder:** `epics/ep_012_adaptive_strategy_selection_engine/results/learned/`

**Dependency:** Clean forex-only net and gap analysis artifacts:
- `epics/ep_012_adaptive_strategy_selection_engine/results/learned/rank1_open_time_strict_net_clean_forex_only.md`
- `epics/ep_012_adaptive_strategy_selection_engine/results/learned/rank1_open_time_strict_gap_clean_forex_only.md`

## Test Definition

Input scope:
- Source folder: `TradeApps/breakout/fs/json/live/forex/<date>/_frequency.json`
- Test window: `2026-03-21` to `2026-04-17`
- Product scope: only source files whose leaders contain expected forex products only
- Clean source files used: `16`
- Contaminated source files excluded: `10`

Clean dates used:
`2026-03-24`, `2026-03-26`, `2026-03-27`, `2026-03-28`, `2026-03-29`, `2026-03-30`, `2026-03-31`, `2026-04-01`, `2026-04-02`, `2026-04-03`, `2026-04-05`, `2026-04-06`, `2026-04-07`, `2026-04-08`, `2026-04-09`, `2026-04-17`.

Excluded contaminated dates:
`2026-03-21`, `2026-03-22`, `2026-03-23`, `2026-03-25`, `2026-04-10`, `2026-04-12`, `2026-04-13`, `2026-04-14`, `2026-04-15`, `2026-04-16`.

Switching rules tested:
- `rank-1 + net>X`: switch only when the new rank-1 strategy net is greater than the held strategy net plus `X`.
- `rank-1 + gap>X`: switch only when the new rank-1 cumulative count is greater than the held strategy cumulative rank-1 count plus `X`.
- No implicit fallback switching.
- No switching without an explicit valid criterion.
- Switch cost: `$50` per switch.
- First open cutoff values: `00:00`, `01:00`, `02:00`, `03:00`.

## Best Results Summary

### Strict Net

| First open cutoff | Best rule | Total net | Avg/day | Switches | Days |
|---|---:|---:|---:|---:|---:|
| 00:00 | rank-1 + net>50 | 1,695 | 106 | 5 | 16 |
| 01:00 | rank-1 + net>50 | 2,395 | 150 | 5 | 16 |
| 02:00 | rank-1 + net>50 | 2,400 | 150 | 5 | 16 |
| 03:00 | rank-1 + net>50 | 2,400 | 150 | 5 | 16 |

### Strict Gap

| First open cutoff | Best rule | Total net | Avg/day | Switches | Days |
|---|---:|---:|---:|---:|---:|
| 00:00 | rank-1 + gap>5 | 1,440 | 90 | 6 | 16 |
| 01:00 | rank-1 + gap>5 | 2,140 | 134 | 6 | 16 |
| 02:00 | rank-1 + gap>0 | 2,140 | 134 | 6 | 16 |
| 03:00 | rank-1 + gap>0 | 2,190 | 137 | 5 | 16 |

## Full Strict Net Results

### First open at/after 00:00

| Rule | Total net | Avg/day | Switches |
|---|---:|---:|---:|
| rank-1 + net>0 | 1,035 | 65 | 17 |
| rank-1 + net>25 | 1,600 | 100 | 5 |
| rank-1 + net>50 | 1,695 | 106 | 5 |
| rank-1 + net>75 | 1,625 | 102 | 4 |
| rank-1 + net>100 | 1,385 | 87 | 1 |
| rank-1 + net>150 | 1,385 | 87 | 1 |
| rank-1 + net>200 | 1,265 | 79 | 0 |
| rank-1 + net>300 | 1,265 | 79 | 0 |
| rank-1 + net>500 | 1,265 | 79 | 0 |

### First open at/after 01:00

| Rule | Total net | Avg/day | Switches |
|---|---:|---:|---:|
| rank-1 + net>0 | 1,295 | 81 | 15 |
| rank-1 + net>25 | 1,880 | 118 | 7 |
| rank-1 + net>50 | 2,395 | 150 | 5 |
| rank-1 + net>75 | 2,325 | 145 | 4 |
| rank-1 + net>100 | 2,185 | 137 | 2 |
| rank-1 + net>150 | 2,115 | 132 | 1 |
| rank-1 + net>200 | 1,995 | 125 | 0 |
| rank-1 + net>300 | 1,995 | 125 | 0 |
| rank-1 + net>500 | 1,995 | 125 | 0 |

### First open at/after 02:00

| Rule | Total net | Avg/day | Switches |
|---|---:|---:|---:|
| rank-1 + net>0 | 1,445 | 90 | 12 |
| rank-1 + net>25 | 1,935 | 121 | 6 |
| rank-1 + net>50 | 2,400 | 150 | 5 |
| rank-1 + net>75 | 2,220 | 139 | 3 |
| rank-1 + net>100 | 2,080 | 130 | 1 |
| rank-1 + net>150 | 2,080 | 130 | 1 |
| rank-1 + net>200 | 1,960 | 122 | 0 |
| rank-1 + net>300 | 1,960 | 122 | 0 |
| rank-1 + net>500 | 1,960 | 122 | 0 |

### First open at/after 03:00

| Rule | Total net | Avg/day | Switches |
|---|---:|---:|---:|
| rank-1 + net>0 | 1,495 | 93 | 11 |
| rank-1 + net>25 | 1,935 | 121 | 6 |
| rank-1 + net>50 | 2,400 | 150 | 5 |
| rank-1 + net>75 | 2,330 | 146 | 4 |
| rank-1 + net>100 | 2,100 | 131 | 1 |
| rank-1 + net>150 | 2,100 | 131 | 1 |
| rank-1 + net>200 | 1,980 | 124 | 0 |
| rank-1 + net>300 | 1,980 | 124 | 0 |
| rank-1 + net>500 | 1,980 | 124 | 0 |

## Full Strict Gap Results

### First open at/after 00:00

| Rule | Total net | Avg/day | Switches |
|---|---:|---:|---:|
| rank-1 + gap>0 | 1,235 | 77 | 6 |
| rank-1 + gap>5 | 1,440 | 90 | 6 |
| rank-1 + gap>10 | 1,440 | 90 | 6 |
| rank-1 + gap>15 | 1,340 | 84 | 5 |
| rank-1 + gap>20 | 1,340 | 84 | 5 |
| rank-1 + gap>25 | 1,390 | 87 | 4 |
| rank-1 + gap>50 | 1,290 | 81 | 3 |
| rank-1 + gap>75 | 1,290 | 81 | 3 |
| rank-1 + gap>100 | 1,170 | 73 | 2 |
| rank-1 + gap>150 | 1,265 | 79 | 0 |
| rank-1 + gap>200 | 1,265 | 79 | 0 |

### First open at/after 01:00

| Rule | Total net | Avg/day | Switches |
|---|---:|---:|---:|
| rank-1 + gap>0 | 2,040 | 127 | 8 |
| rank-1 + gap>5 | 2,140 | 134 | 6 |
| rank-1 + gap>10 | 2,140 | 134 | 6 |
| rank-1 + gap>15 | 2,040 | 128 | 5 |
| rank-1 + gap>20 | 2,040 | 128 | 5 |
| rank-1 + gap>25 | 2,090 | 131 | 4 |
| rank-1 + gap>50 | 2,090 | 131 | 4 |
| rank-1 + gap>75 | 2,020 | 126 | 3 |
| rank-1 + gap>100 | 1,900 | 119 | 2 |
| rank-1 + gap>150 | 1,995 | 125 | 0 |
| rank-1 + gap>200 | 1,995 | 125 | 0 |

### First open at/after 02:00

| Rule | Total net | Avg/day | Switches |
|---|---:|---:|---:|
| rank-1 + gap>0 | 2,140 | 134 | 6 |
| rank-1 + gap>5 | 2,140 | 134 | 6 |
| rank-1 + gap>10 | 2,080 | 130 | 4 |
| rank-1 + gap>15 | 1,980 | 124 | 3 |
| rank-1 + gap>20 | 1,980 | 124 | 3 |
| rank-1 + gap>25 | 2,030 | 127 | 2 |
| rank-1 + gap>50 | 2,030 | 127 | 2 |
| rank-1 + gap>75 | 2,030 | 127 | 2 |
| rank-1 + gap>100 | 1,910 | 119 | 1 |
| rank-1 + gap>150 | 1,960 | 122 | 0 |
| rank-1 + gap>200 | 1,960 | 122 | 0 |

### First open at/after 03:00

| Rule | Total net | Avg/day | Switches |
|---|---:|---:|---:|
| rank-1 + gap>0 | 2,190 | 137 | 5 |
| rank-1 + gap>5 | 2,190 | 137 | 5 |
| rank-1 + gap>10 | 2,190 | 137 | 5 |
| rank-1 + gap>15 | 2,000 | 125 | 3 |
| rank-1 + gap>20 | 2,000 | 125 | 3 |
| rank-1 + gap>25 | 2,050 | 128 | 2 |
| rank-1 + gap>50 | 2,050 | 128 | 2 |
| rank-1 + gap>75 | 2,050 | 128 | 2 |
| rank-1 + gap>100 | 1,930 | 121 | 1 |
| rank-1 + gap>150 | 1,980 | 124 | 0 |
| rank-1 + gap>200 | 1,980 | 124 | 0 |

## Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true

- Evidence-Type: file_output
  - Artifact: `workstream/300_complete/general/20260421_113347_ep012_clean_forex_only_net_gap_open_time_test_report.md`
  - Objective-Proved: Consolidated task report contains the test definition and both result tables.
  - Status: captured

- Evidence-Type: file_output
  - Artifact: `epics/ep_012_adaptive_strategy_selection_engine/results/learned/rank1_open_time_strict_net_clean_forex_only.md`
  - Objective-Proved: Source strict net result artifact exists.
  - Status: captured

- Evidence-Type: file_output
  - Artifact: `epics/ep_012_adaptive_strategy_selection_engine/results/learned/rank1_open_time_strict_gap_clean_forex_only.md`
  - Objective-Proved: Source strict gap result artifact exists.
  - Status: captured

## Implementation Log

- 2026-04-21 11:33:47 BST — Created consolidated task report with clean-date test definition and both strict net/gap result tables.

## Changes Made

- Created `workstream/300_complete/general/20260421_113347_ep012_clean_forex_only_net_gap_open_time_test_report.md`.

## Validation

- Read source net and gap Markdown artifacts before creating this consolidated report.
- Confirmed report includes clean date count, excluded date list, strict switching definitions, best summaries, and full tables.

## Risks/Notes

- Results use only 16 clean forex-only dates. They should not be compared directly to 25/26-day totals without normalizing by `Avg/day`.
- Excluded contaminated dates materially reduce the test sample size.

## Completion Status

COMPLETE -- 2026-04-21 11:34 BST
