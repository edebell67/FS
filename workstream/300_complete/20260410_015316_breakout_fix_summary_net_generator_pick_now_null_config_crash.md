# Breakout Fix Summary Net Generator Pick Now Null Config Crash

- Status: In Progress
- Started: 2026-04-10 01:53:16
- Project: breakout
- Owner: Codex

## Request

Resolve the `summary_net_generator.py` crash that prevents forex `_summary_net.json` from updating.

## Root Cause

`config.json` contains `null` values under `pick_now` for:

- `min_appearances`
- `min_net_trend`
- `min_snapshots`

Those `null` values override defaults in `strategy_predictor.load_pick_now_config()`, and `summary_net_generator.py` then crashes in `evaluate_pick_now_logic()` when it compares integers against `None`.

## Plan

1. Restore numeric `pick_now` threshold values in `config.json`.
2. Harden `strategy_predictor.load_pick_now_config()` so `None` does not override defaults.
3. Validate that the generator runs and updates today’s forex `_summary_net.json`.

## Progress Log

- 2026-04-10 01:50:40: Updated `config.json` `pick_now` thresholds from `null` to numeric defaults (`20`, `100`, `60`).
- 2026-04-10 01:50:45: Hardened `strategy_predictor.load_pick_now_config()` so `None` values no longer override defaults.
- 2026-04-10 01:50:58: Ran a direct forex `process_date()` pass successfully after the fix; no crash.
- 2026-04-10 01:52:21: Confirmed today’s forex `_summary_net.json` repopulated with live strategy data.

## Validation

- 2026-04-10 01:50:50: `python -m py_compile C:\Users\edebe\eds\TradeApps\breakout\fs\strategy_predictor.py C:\Users\edebe\eds\TradeApps\breakout\fs\summary_net_generator.py` -> passed.
- 2026-04-10 01:50:58: Direct `SummaryGenerator().process_date('live', '2026-04-10', forex_day_dir)` completed successfully and logged `Updated: 0 new, 798 op read (0 skipped)`.
- 2026-04-10 01:52:21: [C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\forex\2026-04-10\_summary_net.json](C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\forex\2026-04-10\_summary_net.json) now contains `strategy_count = 103` and `last_update = 2026-04-10T01:52:21.871909`.
- 2026-04-10 01:52:46: Starting `summary_net_generator.py` no longer crashes; it now aborts only because another instance is already running, which is the expected singleton behavior.

## Outcome

The generator crash is resolved. `_summary_net.json` is being generated again because the `pick_now` thresholds are valid numbers and the loader now ignores `None` overrides safely.
