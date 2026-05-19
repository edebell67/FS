# Breakout Investigate Summary Net Generator Not Updating Forex Summary

- Status: Complete
- Created: 2026-04-10 01:46:13
- Project: breakout
- Owner: Codex

## Request

Investigate why `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\forex\2026-04-10\_summary_net.json` is not being updated with current forex summary data.

## Current Evidence

- `_summary_net.json` exists but is stale and nearly empty:
  - `last_update` around `2026-04-10T01:00:10`
  - `strategies: {}`
- The forex day folder contains many closed trades after that time:
  - `*_cld.json`: 113
  - `*_cl.json`: 1
- Closed trade files in the same folder have `LastWriteTime` as late as about `01:39`.
- `summary_net_generator.py` only includes trades where `status == 'CLOSED'`, so the issue is not open-trade exclusion alone.
- `summary_gen_debug.log` has not advanced since `2026-04-08 16:15:31`.
- `summary_gen.lock` is not present at the time of inspection.

## Investigation Goals

1. Confirm whether `summary_net_generator.py` is currently running.
2. Identify why it stopped or failed to process today’s forex closed trades.
3. Determine whether the supervisor is failing to launch/relaunch it.
4. Capture the concrete root cause and required remediation.

## Acceptance Criteria

1. Root cause is identified with evidence.
2. The task records whether the failure is process, lock, config, path, or runtime related.
3. Recommended fix or next action is documented clearly.

## Progress Log

- 2026-04-10 01:48:07: Ran `summary_net_generator.py` directly and reproduced immediate startup failure after forex initialization.
- 2026-04-10 01:48:10: Direct run logged `[CRITICAL] '>=' not supported between instances of 'int' and 'NoneType'`.
- 2026-04-10 01:49:00: Verified today’s forex folder contains many closed trades (`*_cld.json`) after `01:00`, so the stale `_summary_net.json` is not due to lack of closed data.
- 2026-04-10 01:50:00: Traced crash into `summary_net_generator.py` Top 20 / `pick_now` evaluation path.
- 2026-04-10 01:51:00: Confirmed `config.json` contains `pick_now.min_appearances = null`, `pick_now.min_net_trend = null`, and `pick_now.min_snapshots = null`.

## Findings

- `_summary_net.json` itself is only built from `CLOSED` trades, which is expected.
- The real issue is that `summary_net_generator.py` is crashing before it can process today’s closed forex files.
- Crash path:
  - `summary_net_generator.py` imports `strategy_predictor.evaluate_pick_now_logic`
  - during Top 20 generation it calls `evaluate_pick_now_logic(features, total_snapshots)`
  - `strategy_predictor.load_pick_now_config()` overlays values from `config.json`
  - because `pick_now.min_appearances`, `pick_now.min_net_trend`, and `pick_now.min_snapshots` are explicitly `null`, those `None` values replace the defaults
  - later comparisons such as `features.get("appearances", 0) >= min_appearances` crash with `int >= NoneType`

## Root Cause

Configuration defect in [C:\Users\edebe\eds\TradeApps\breakout\fs\config.json](C:\Users\edebe\eds\TradeApps\breakout\fs\config.json):

- `pick_now.min_appearances = null`
- `pick_now.min_net_trend = null`
- `pick_now.min_snapshots = null`

Those `null` values break `summary_net_generator.py` through the imported `strategy_predictor.evaluate_pick_now_logic()` path.

## Recommended Remediation

1. Replace the `null` `pick_now` thresholds in `config.json` with numeric values, or remove those keys so defaults apply.
2. Harden `strategy_predictor.load_pick_now_config()` or `evaluate_pick_now_logic()` so `None` falls back to defaults instead of crashing.
3. Restart `summary_net_generator.py` after the config/code fix so `_summary_net.json` repopulates from today’s closed forex files.
