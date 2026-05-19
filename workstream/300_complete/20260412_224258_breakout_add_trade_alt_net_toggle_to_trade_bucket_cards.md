# Task: Add Trade Alt Net Toggle To Trade Bucket Cards

Source: User request on 2026-04-12 to add a new `trade alt_net` toggle on each Trade Bucket card and wire it into live execution and drilldown behavior.

Task Type: feature

Task Attributes:
- priority: high
- execution_owner: codex
- workflow_ready: true
- ui_task: true

## Task Summary
Add a new Trade Bucket card toggle named `trade alt_net`. When enabled, the bucket should live-trade the single most negative strategy in the bucket using `alt_net` execution semantics: the strategy is sent to `grid_live`, flagged for `alt_net`, and all routed trades are inverted so buys become sells and sells become buys. Drilldown/L-trade attribution for that negative strategy must also use the `alt_net` path.

## Scope Notes
- The `trade alt_net` target is the single most negative strategy in the bucket.
- Only the most negative strategy is valid for `alt_net` execution.
- The normal positive/leader strategy behavior remains in place alongside the negative `alt_net` strategy.
- `grid_live` must carry enough state so runtime execution and drilldown attribution can distinguish normal `net` routing from `alt_net` routing.

## Validation Plan
- Add the new toggle to the Trade Bucket card UI and persist its state.
- Update bucket sync logic to promote both the normal leader and, when enabled, the most negative strategy with `alt_net` semantics.
- Ensure runtime execution inverts the trade direction for `alt_net`-flagged TB entries.
- Ensure drilldown/L-trade attribution for the negative strategy is evaluated against `alt_net`.
- Add focused regression tests for bucket promotion and `alt_net`-flagged behavior.

## Execution Log
- 2026-04-12 22:43 Moved task to in-progress and reviewed Trade Bucket card rendering, bucket sync/reconcile logic, `grid_live` metric handling, and runtime alt execution support in `common.py`.
- 2026-04-12 22:54 Confirmed the runtime already executes inverted orders when `grid_live.metric = alt`, so the implementation was aligned to existing `alt` execution mode rather than introducing a second inversion path.
- 2026-04-12 23:05 Patched `trade_viewer_api.py` to persist `trade_alt_net` on buckets, identify the single most negative strategy, expose `alt_trade_key`/`is_alt_candidate` in bucket payloads, and promote an additional `TBALT_{bucket}` grid-live entry with `metric = alt`.
- 2026-04-12 23:12 Patched `trade_viewer_api.py` grid-to-activation sync so `alt`, `buy_alt`, and `sell_alt` entries map to `*_buy_alt` / `*_sell_alt` activation keys.
- 2026-04-12 23:21 Patched `trade_bucket.html` to add the `TRADE ALT` toggle, mark the current loser row as the alt candidate, use `alt_net` PnL for that row’s live sums and drilldown, and make drilldown L-trade identification respect leader windows plus `order_sent_alt`.
- 2026-04-12 23:26 Added regression coverage for alt loser promotion in `TradeApps/breakout/fs/tests/test_weekly_auto_promote_activation_api.py`.

## Validation Results
- Command: `python -m pytest C:\Users\edebe\eds\TradeApps\breakout\fs\tests\test_weekly_auto_promote_activation_api.py -q`
- Result: `4 passed`

## Outcome
- Each Trade Bucket card now supports a persisted `trade alt_net` toggle.
- When enabled, the bucket promotes the normal leader plus the single most negative strategy as an `alt` grid-live entry.
- Runtime execution uses the existing alt path, so that loser strategy trades inverted automatically.
- Drilldown and per-row live sums for the alt candidate now use `alt_net` rather than `net_return`.
- Validation covered the backend promotion path and activation mapping; browser click-through was not run in this task.
