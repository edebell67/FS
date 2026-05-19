# Count #1 Leadership Changes Per Hour from _summary_net

## Source
User request - 2026-04-30

## Task Type
standard

## Task Attributes
- recurring_task: false
- looping_task: false
- splittable_task: false
- workflow_task: false

## Task Summary
Analyze `_summary_net.json` history to count how many times the #1 ranked strategy changed throughout the day, grouped by hour since midnight.

### Logic
1. Parse all timestamped entries from `_summary_net.json`
2. At each timestamp, calculate total `net` per strategy (sum across all products)
3. Determine which strategy is #1 (highest total net) at each point
4. Detect when #1 changes from one strategy to another
5. Count leadership changes per hour (00:00-00:59, 01:00-01:59, etc.)

## Context
- Project: TradeApps/breakout
- Source file: `fs/json/live/forex/{date}/_summary_net.json`
- Structure: `strategies.{strategy_name}.{product}[].{t, net, ...}`
- Excludes: momentum strategies (per user request)

## Destination Folder
None (script output / console report)

## Dependency
None

## Plan
- [x] 1. Read and parse _summary_net.json structure
  - Test: Successfully load JSON and list all strategies
  - Evidence: 24351 timestamped entries extracted

- [x] 2. Extract all timestamps and build timeline
  - Test: List all unique timestamps sorted chronologically
  - Evidence: 1725 unique timestamps identified

- [x] 3. Calculate strategy totals at each timestamp
  - Test: At a sample timestamp, show total net per strategy
  - Evidence: Cumulative totals calculated correctly

- [x] 4. Track #1 leader at each point and detect changes
  - Test: Identify all leadership change events
  - Evidence: 10 leadership changes detected for 2026-04-28

- [x] 5. Group changes by hour and generate report
  - Test: Output hourly breakdown
  - Evidence: Report generated showing changes per hour

## Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true

- Evidence-Type: file_output
  - Artifact: `TradeApps/breakout/fs/leadership_change_analyzer.py`
  - Objective-Proved: Script correctly analyzes leadership changes
  - Status: captured

- Evidence-Type: test_output
  - Artifact: Test run against 2026-04-28 data
  - Objective-Proved: Report shows 10 changes, hourly breakdown accurate
  - Status: captured

## Implementation Log
- 2026-04-30 10:18: Task created
- 2026-04-30 10:20: Script implemented
- 2026-04-30 10:21: Added momentum strategy exclusion
- 2026-04-30 10:22: Tested successfully against 2026-04-28 data

## Changes Made
**New file: `TradeApps/breakout/fs/leadership_change_analyzer.py`**

| Function | Purpose |
|----------|---------|
| `load_summary_net()` | Load _summary_net.json for given date |
| `extract_timeline()` | Extract (timestamp, strategy, product, net) tuples, excludes momentum |
| `calculate_strategy_totals_at_timestamps()` | Build cumulative totals per strategy at each timestamp |
| `find_leader_at_each_timestamp()` | Determine #1 at each point |
| `detect_leadership_changes()` | Find when leadership flips |
| `group_changes_by_hour()` | Group changes into 24 hour buckets |
| `generate_report()` | Format hourly breakdown report |

## Validation
```
$ python3 leadership_change_analyzer.py 2026-04-28

Total snapshots analyzed: 1725
Total leadership changes: 10
First leader: breakout_R_Rev_2_tp10.0_sl3.0
Final leader: breakout_R_2_tp20.0_sl50.0

Hour   Changes    Transitions
00:00  3          R_Rev_2 -> R_2 -> breakout_2 -> R_4
01:00  1          R_4 -> R_2
02:00  2          R_2 -> R_2 -> Rev_3
12:00  1          Rev_3 -> Rev_3
21:00  3          Rev_3 -> R_4 -> Rev_3 -> R_2
(other hours stable)
```

## Risks/Notes
- Ties resolved alphabetically (consistent ordering)
- Momentum strategies excluded per user request
- Works with forex path structure

## Completion Status
**COMPLETE** - 2026-04-30 10:22
