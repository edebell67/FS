# sp_001_copy_trade_as_tradeable_v703 Plan

## Objectives
- Clone v702 strategy into v703 with enhanced red-cell signal rules.
- Raise default profit target to 500 and align loss floor at -200.
- Introduce configurable profit protection via new helper routine.
- Document config toggles and operational checks for rollout.

## Functional Changes
1. New stored procedure dbo.sp_001_copy_trade_as_tradeable_v703 reads ed_buy/ed_sell from w_123_zone_counts_with_prev, applying:
   - BUY when ed_buy > 0 and ed_sell = 0, or ed_buy >= 2 * red_sell.
   - SELL when ed_sell > 0 and ed_buy = 0, or ed_sell >= 2 * red_buy.
2. Default trade templates now use 	arget_profit = 500 and 	arget_loss = -200.
3. Procedure invokes dbo.sp_helper_apply_profit_protection prior to exit, keeping trailing stops updated even on HOLD cycles.
4. sp_loop_create_trades_v2 loads skip_001_v703 and executes the new strategy when enabled.

## Profit Protection Helper
- dbo.sp_helper_apply_profit_protection reads profit_protect_trigger and profit_protect_percent from dbo.config.
- When max_net_return > trigger, recalculates 	arget_loss to hold at least percent of the peak return (rounded to SMALLINT).
- Emits concise telemetry when updates occur; silently skips on missing/invalid config.

## Config & Rollout Checklist
- Ensure dbo.config contains:
  - skip_001_v703 (0 to enable).
  - profit_protect_trigger (net-return threshold, e.g. 100).
  - profit_protect_percent (either 0-1 or 0-100 scale).
- Verify w_123_zone_counts_with_prev exposes ed_buy/ed_sell for target products.
- After deployment:
  1. Enable skip_001_v703 in staging; monitor logs for new signal and profit-protect messages.
  2. Confirm 	arget_loss updates in combined_trades_open once a trade crosses the trigger.
  3. Validate sp_loop_create_trades_v2 iterates v703 without regressions to earlier versions.
