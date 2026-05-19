# Task: Investigate Why Trade Bucket Took Short Position

## Created
- 2026-04-27 09:56:49

## Status
- Complete

## Reference
- 999

## Request
- Investigate why `/trade_bucket.html` shows trade bucket `AUTO_TB_0427_023046_809_GBPNZD_C_breakout_R_2_tp20_0_sl20_0` taking a short position.

## Scope
- Trace the bucket configuration and creation context for `AUTO_TB_0427_023046_809_GBPNZD_C_breakout_R_2_tp20_0_sl20_0`.
- Determine what strategy, direction, leader, workflow, or activation logic caused a short trade to be taken.
- Check whether the short position was expected from the bucket settings and runtime state.
- Capture the root cause from source data and code path evidence.

## Acceptance Criteria
- The exact reason the bucket took a short position is identified.
- The explanation is tied to concrete bucket data, trade records, and code behavior.
- Any mismatch between expected and actual direction is documented.

## Validation
- Inspect the bucket details in `/trade_bucket.html`.
- Trace the related trade records and bucket strategy/runtime metadata.
- Verify the direction decision path from source data through backend logic.

## Findings
- `AUTO_TB_0427_023046_809_GBPNZD_C_breakout_R_2_tp20_0_sl20_0` was created with:
  - `market_bias_at_creation: BUY`
  - leader metric `buy_net`
  - strategy pair entries for `breakout_R_2_tp20.0_sl20.0 | GBPNZD_C` under both `buy_net` and `sell_net`
- The exact matching trade shown by the bucket API was:
  - `breakout_R_2_tp20.0_sl20.0_967b9771_GBPNZD_C_20260427_024931_2_0.00015_20.0_20.0_cl.json`
  - `direction: SHORT`
  - `source_group: breakout|AUTO_TB_0427_023046_809_GBPNZD_C_breakout_R_2_tp20_0_sl20_0`
- That trade was **not** promoted as a valid buy-side live trade:
  - `trade_block_reason: NET: Bypass blocked (grid_live BUY only)`
  - `trade_block_reason_detail: NET: grid metric=buy_net, trade_direction=sell`
  - `tb_leader: N`
  - `order_sent_net: false`
  - `is_live_trade: false`

## Root Cause
- The bucket did not "choose sell" or "switch to short".
- The underlying strategy `breakout_R_2_tp20.0_sl20.0` generated a normal market `SHORT` signal at `2026-04-27T02:49:31.220119`.
- The bucket’s `buy_net` activation correctly blocked that short from becoming a buy-side L-trade.
- The misleading part is the bucket trade query:
  - `/api/trades?...bucket_name=...&l_only=true`
  - this uses `_is_trade_in_leader_window(...)` in `trade_viewer_api.py`
  - `_is_trade_in_leader_window(...)` matches by `strategy + product + entry_time in leader window`
  - it does **not** check trade direction against `buy_net/sell_net`
  - it does **not** require `tb_leader == Y`
  - it does **not** require `order_sent_net/order_sent_alt/is_live_trade`
- Result: a blocked `SHORT` trade from the leader strategy was still returned as an "L-trade" for the bucket because it occurred during that bucket’s active leader window.

## Evidence
- `_trade_buckets.json` for `2026-04-27` shows the bucket leader metric as `buy_net`.
- `grid_live.json` shows the bucket source `TB_AUTO_TB_0427_023046_809_GBPNZD_C_breakout_R_2_tp20_0_sl20_0` with metric `buy_net`.
- Direct API call to `/api/trades?...bucket_name=AUTO_TB_0427_023046_809_GBPNZD_C_breakout_R_2_tp20_0_sl20_0&l_only=true` returned the short trade `967b9771`.
- Trade file `breakout_R_2_tp20.0_sl20.0_967b9771_GBPNZD_C_20260427_024931_2_0.00015_20.0_20.0_cl.json` proves the short was blocked by `grid_live BUY only` and tagged `tb_leader: N`.
- `_tb_leadership.json` for the day shows the bucket window for `breakout_R_2_tp20.0_sl20.0:GBPNZD_C` with an open-ended start, which is why the API matched the short by time window.

## Completion Status
- Completed 2026-04-27: root cause captured. The issue is query semantics in leader-window matching, not a bucket-side sell decision.
