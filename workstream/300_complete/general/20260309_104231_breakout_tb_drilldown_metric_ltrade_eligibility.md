# Workstream Task: TB Drilldown Metric L-Trade Eligibility

## Source
Created from user request on 2026-03-09 to ensure Trade Bucket drilldown respects metric-specific L-trade eligibility rules.
Related task: `C:\Users\edebe\eds\workstream\200_inprogress\general\20260308_213800_breakout_trade_bucket_metric_display.md`

## Task Summary
Update the `/fs` Trade Bucket drilldown and trade eligibility display so metric-tagged bucket rows enforce side-specific L-trade interpretation. If a Trade Bucket row is `[B]`, only long/buy trades should be considered eligible as L-trades for that strategy. If `[S]`, only short/sell trades should be eligible. If `[N]`, both sides remain eligible under the existing broader criteria.

## Context
- `C:\Users\edebe\eds\TradeApps\breakout\fs\trade_bucket.html`
- `C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py`
- `C:\Users\edebe\eds\TradeApps\breakout\fs\common.py`
- `C:\Users\edebe\eds\TradeApps\breakout\fs\multi_chart.js`

## Plan
- [x] 1. Trace the current `/fs` Trade Bucket drilldown path and identify where metric-tagged bucket strategies are matched to trades and where L-trade status is inferred.
  - [x] Test: Inspect `/fs` drilldown code paths and confirm the exact functions/fields currently used for `tb_leader`, `is_live_trade`, `order_sent_net`, `order_sent_alt`, and trade direction filtering.
  - Evidence: `trade_bucket.html` drilldown flow confirmed through `showDrilldown()`, `renderDrilldownRows()`, `isLTradeFromFlags()`, and strategy row click handler using `parseBucketStrategy()`.
- [x] 2. Implement metric-aware TB drilldown filtering/display rules so `[B]` rows only treat long trades as L-trade-eligible, `[S]` rows only treat short trades as L-trade-eligible, and `[N]` rows preserve both-side eligibility.
  - [ ] Test: Server/browser verification that a `[B]` TB row does not mark short trades as L-trades, and a `[S]` TB row does not mark long trades as L-trades.
  - Evidence: `trade_bucket.html` now carries the clicked row metric into drilldown state and gates L-trade labeling/filtering with direction-aware `buy_net` / `sell_net` rules.
- [x] 3. Align any backend helper logic used by TB drilldown or L-trade annotation with the same metric-direction rules to avoid UI/backend disagreement.
  - [x] Test: Review `/fs/common.py` and related helpers; pass if directional enforcement is consistent with grid metric parsing and TB metric semantics.
  - Evidence: Existing `/fs` backend enforcement already maps `buy_net` to buy-only and `sell_net` to sell-only in grid/live execution, so no backend code change was required for TB drilldown labeling.
- [ ] 4. Validate `[N]` regression safety so generic net buckets still allow both long and short trades to qualify under the existing overarching criteria.
  - [ ] Test: Manual verification on an `[N]` bucket row showing that both directions remain eligible where previously allowed.
  - Evidence: Pending user verification.

## Implementation Log
- **2026-03-09 10:42:31**: Created new task to isolate TB drilldown metric-specific L-trade eligibility from the earlier TB metric display/promotion work.
- **2026-03-09 11:05:00**: Patched `/fs/trade_bucket.html` so strategy drilldown carries the TB row metric into the modal and applies side-aware L-trade eligibility. `[B]` now requires buy/long direction, `[S]` requires sell/short direction, `[N]` keeps the existing broad flag-based behavior.

## Changes Made
- Updated `C:\Users\edebe\eds\TradeApps\breakout\fs\trade_bucket.html`:
  - Added `lastDrilldownMetric` state for the active strategy drilldown.
  - Added `getTradeDirectionKey()` and `isTradeEligibleForMetric()` helpers.
  - Updated `isTradeLTrade()` to require both existing L-trade flags and metric-compatible direction.
  - Updated `renderDrilldownRows()` so L-trade badges, counts, and the `only L-trades` toggle respect the clicked TB metric.
  - Updated the strategy row click handler to pass `parsedStrategy.metric` into `showDrilldown(...)`.
  - Reset drilldown metric state in `closeTradeModal()`.

## Validation
- Code inspection:
  - `rg -n "lastDrilldownMetric|isTradeEligibleForMetric|getTradeDirectionKey|showDrilldown\\(.*metricRaw|parsedStrategy.metric" C:\Users\edebe\eds\TradeApps\breakout\fs\trade_bucket.html`
- Pending user/browser verification after `/fs` restart:
  - `[B]` TB drilldown should mark only long/buy trades as `L-TRADE`.
  - `[S]` TB drilldown should mark only short/sell trades as `L-TRADE`.
  - `[N]` TB drilldown should continue to allow both sides when existing L-trade flags are present.

## Risks/Notes
- This task should stay scoped to `/fs` drilldown/L-trade interpretation unless the user explicitly asks to mirror the behavior into `/DB`.
- The key risk is mismatch between UI drilldown labeling and backend live-trade eligibility logic if only one side is updated.

## Completion Status
In progress. Awaiting user verification.


# User Feedback
User Verified: PASS
