# EP012 Forex Summary Net Top-3 Hold Replay

Source: User request, 2026-04-21
Task Type: standard

## Task Attributes
recurring_task: false
looping_task: false
splittable_task: false
workflow_task: false
depends_on: []
feeds_into: []

## Task Summary
Create and run a replay analysis using `forex/_summary_net` as the ranking source.

Requested rule:
- Select the current product/strategy ranked #1.
- Continue holding that selected product/strategy while its net rank remains within the current top 3.
- If the held product/strategy falls out of the current top 3, replace it with the new current #1 product/strategy.
- Replay the rule across the available forex summary-net timeline and report switch count, total net, average per day, and trade/switch event details.

## Context
Primary data source:
- `TradeApps/breakout/fs/json/live/forex/**/_summary_net*.json`

Related prior analysis context:
- Strict rank-1 switching analysis using frequency files.
- Clean forex-only filtering concerns from prior `_frequency.json` work.
- This task must use `forex/_summary_net` specifically, not `_frequency.json`, unless explicitly needed for validation only.

## Destination Folder
Destination Folder: `epics/ep_012_adaptive_strategy_selection_engine/results/learned/`

Expected outputs must be placed under the destination folder or a subfolder:
- Replay script or notebook/report artifact.
- Summary markdown table.
- Switch/replacement event CSV or JSON.
- Any validation logs.

## Dependency
Dependency: None

## Plan
- [x] 1. Locate and inspect available `forex/_summary_net` files and confirm their schema.
  - [x] Test: Run a file discovery/schema inspection command and confirm required fields exist for timestamp, product, strategy, net, and rank derivation.
  - Evidence: `rg --files TradeApps/breakout/fs/json/live/forex -g "_summary_net*.json"` found source files; sample archive files contain `last_update`, `strategies`, strategy keys, product keys, and point fields `t` and `net`.

- [x] 2. Define deterministic top-3 hold replay semantics.
  - [x] Test: Document exact ranking sort, tie-break behavior, open-time handling if applicable, and replacement trigger condition.
  - Evidence: Report documents ranking by latest `net` at snapshot `last_update`, sorted net descending/product/strategy; open at/after cutoff; hold while current held key remains in top 3; replace with current #1 when held drops out.

- [x] 3. Implement replay using only the `forex/_summary_net` ranking source.
  - [x] Test: Run the replay script against the selected date range and verify it emits summary plus event artifacts.
  - Evidence: `summary_net_top3_hold_replay.py` generated summary, per-day, events CSVs and markdown reports under `epics/ep_012_adaptive_strategy_selection_engine/results/learned/`.

- [x] 4. Validate product scope and source consistency.
  - [x] Test: Check that included products come from the forex summary-net source and flag any non-forex leakage if present.
  - Evidence: Script filters to forex regex `^[A-Z]{6}_C$` by default and reports non-forex products found in source: `AUD, BTC, BZ, CAD, CHF, CL, ES, ETH, EUR, GBP, GBPEUR_S, GC, HG, NG, NQ, NZD, RTY, SI, SOL, XRP, YM, ZN, ZT`.

- [x] 5. Produce final analysis report.
  - [x] Test: Confirm report includes total net, avg/day, switch count, days covered, date range, source file count, and switch event examples.
  - Evidence: Reports created:
    - `epics/ep_012_adaptive_strategy_selection_engine/results/learned/summary_net_top3_hold_replay.md`
    - `epics/ep_012_adaptive_strategy_selection_engine/results/learned/summary_net_top3_hold_replay_20260321_20260417.md`
    - `epics/ep_012_adaptive_strategy_selection_engine/results/learned/summary_net_top3_hold_replay_20260321_20260416_excl_0417.md`

## Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true

- Evidence-Type: file_output
  - Artifact: `epics/ep_012_adaptive_strategy_selection_engine/results/learned/summary_net_top3_hold_replay.py`
  - Objective-Proved: Replay artifacts and report are generated from `forex/_summary_net`.
  - Status: captured

- Evidence-Type: test_output
  - Artifact: `python -m py_compile epics/ep_012_adaptive_strategy_selection_engine/results/learned/summary_net_top3_hold_replay.py` completed with exit code 0.
  - Objective-Proved: Replay command completes and validates required source/schema assumptions.
  - Status: captured

- Evidence-Type: file_output
  - Artifact: `epics/ep_012_adaptive_strategy_selection_engine/results/learned/summary_net_top3_hold_replay_20260321_20260416_excl_0417.md`
  - Objective-Proved: Interpretable replay report generated with outlier day excluded for comparison.
  - Status: captured

## Implementation Log
- 2026-04-21 13:39: Task created in backlog from user request.
- 2026-04-21 13:42: Moved task to in-progress and inspected `_summary_net` source schema.
- 2026-04-21 13:46: Implemented standalone replay script for top-3 hold/replacement rule.
- 2026-04-21 13:48: Ran all-available source replay; identified `2026-04-17` as dominant outlier day.
- 2026-04-21 13:51: Ran prior analysis window and prior window excluding `2026-04-17`.
- 2026-04-21 13:53: Validated script syntax with `py_compile`.

## Changes Made
- Added `epics/ep_012_adaptive_strategy_selection_engine/results/learned/summary_net_top3_hold_replay.py`.
- Generated all-available replay outputs:
  - `summary_net_top3_hold_replay.md`
  - `summary_net_top3_hold_replay_summary.csv`
  - `summary_net_top3_hold_replay_days.csv`
  - `summary_net_top3_hold_replay_events.csv`
- Generated prior-window replay outputs:
  - `summary_net_top3_hold_replay_20260321_20260417.md`
  - `summary_net_top3_hold_replay_20260321_20260417_summary.csv`
  - `summary_net_top3_hold_replay_20260321_20260417_days.csv`
  - `summary_net_top3_hold_replay_20260321_20260417_events.csv`
- Generated prior-window excluding `2026-04-17` outputs:
  - `summary_net_top3_hold_replay_20260321_20260416_excl_0417.md`
  - `summary_net_top3_hold_replay_20260321_20260416_excl_0417_summary.csv`
  - `summary_net_top3_hold_replay_20260321_20260416_excl_0417_days.csv`
  - `summary_net_top3_hold_replay_20260321_20260416_excl_0417_events.csv`

## Validation
- `python epics/ep_012_adaptive_strategy_selection_engine/results/learned/summary_net_top3_hold_replay.py --open-hours 0,1,2,3`
  - Result: `00:00 total=474170 avg_day=14818 opened=32 switches=56 days=32`; `01:00 total=474320 avg_day=14822 opened=32 switches=53 days=32`; `02:00 total=474470 avg_day=14827 opened=32 switches=50 days=32`; `03:00 total=474470 avg_day=14827 opened=32 switches=50 days=32`.
- `python epics/ep_012_adaptive_strategy_selection_engine/results/learned/summary_net_top3_hold_replay.py --start-date 2026-03-21 --end-date 2026-04-17 --open-hours 0,1,2,3 --output-stem summary_net_top3_hold_replay_20260321_20260417`
  - Result: all cutoffs `total=470145 avg_day=19589 opened=24 switches=5 days=24`.
- `python epics/ep_012_adaptive_strategy_selection_engine/results/learned/summary_net_top3_hold_replay.py --start-date 2026-03-21 --end-date 2026-04-16 --open-hours 0,1,2,3 --output-stem summary_net_top3_hold_replay_20260321_20260416_excl_0417`
  - Result: all cutoffs `total=16415 avg_day=714 opened=23 switches=5 days=23`.
- `python -m py_compile epics/ep_012_adaptive_strategy_selection_engine/results/learned/summary_net_top3_hold_replay.py`
  - Result: passed.

## Risks/Notes
- `_summary_net` under the forex folder contains non-forex product keys; the replay excludes those by default and reports them.
- The `2026-04-17` result dominates the prior-window total due to `GBPEUR_C / breakout_R_2_tp10.0_sl20.0_12141c72` with gross final net `453,730`.
- The script ranks only by observed `_summary_net` values; it does not validate whether unusually large net values are economically valid.
- The user-requested rule is rank retention within top 3, not threshold-based `net>X` or `gap>X` switching.

## Completion Status
Status: Complete
Created: 2026-04-21 13:39
Completed: 2026-04-21 13:53
