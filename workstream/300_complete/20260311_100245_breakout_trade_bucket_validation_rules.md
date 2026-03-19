# TASK: Enable Multi-Metric Single Strategy in Trade Buckets

**Workstream:** J - TRADE BUCKETS
**Epic:** Autonomous Trading Signal Platform
**Epic Sequence:** 9.1
**Depends On:** none
**Blocks:** none
**Readiness:** ready
**Epic Output Folder:** C:\Users\edebe\eds\ep_autonomous_trading_signal_platform
**Status:** [ ] To Do

## Source
- User Request: "Multi chart has multiple cards with buy/sell charts.. None of these transfered to TB... single strategy can be added to TB when there are multiple charts ie buy / sell because a comparison can then be run between both"

## Task Summary
Enable the "Save as Trade Bucket" functionality to correctly handle single-strategy cards that display multiple comparison metrics (e.g., Buy Net vs Sell Net). Currently, these are likely overwriting each other or being rejected because the underlying strategy key is identical, despite the metrics differing. The system needs to treat `[Strategy] + [Buy Metric]` and `[Strategy] + [Sell Metric]` as distinct, valid entries within a single Trade Bucket.

## Context
- View the `saveToBucket()` function in `TradeApps/breakout/fs/multi_chart.js`. Note how it pushes to the array and constructs the payload: `${o.key} | ${metricPart}`.
- View the backend handler `create_trade_bucket()` in `TradeApps/breakout/fs/trade_viewer_api.py`. Note how it parses `key_only` and `metric_raw`.
- View the Trade Bucket UI (`trade_bucket.html`) where these are rendered. If buckets map data by `key` omitting the metric during rendering or deduplication, collisions will occur, causing the transfer to silently fail or display incorrectly.

## Plan
- [x] 1. Identify where collision/deduplication occurs:
    - **Confirmed**: Underlying backend logic and UI payload generation already support multiple metrics.
    - **Bug Found**: `tradeMatchesBucketStrategy` in `trade_bucket.html` only checks `model` and `product`, causing all metrics for the same strategy to show the same Live Net and trades.
    - **Infrastructure Gap**: `tradeBucketButton` in `multi_chart.html` (Smart Actions) has no listener in `multi_chart.js`.
- [ ] 2. Update `trade_bucket.html`:
    - Modify `tradeMatchesBucketStrategy` to respect the `metric` if present.
    - Ensure `isTradeEligibleForMetric` is applied whenever matching trades to bucket strategies.
- [ ] 3. Update `multi_chart.js`:
    - Implement `tradeBucketButton` click handler to aggregate all active charts into a single Trade Bucket (or one per card).
    - Ensure the logic uses `saveToBucket` or similar for each group.
- [ ] 4. Validate and Verify:
    - Test saving a single strategy with Buy and Sell metrics on one card.
    - Test saving multiple cards via Smart Actions.
    - Verify individual rows in the resulting Trade Bucket show correct, distinct directional Live Net values.
- [ ] 5. Once validated and documented, request User Verification.

