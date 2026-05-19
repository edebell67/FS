# Task: Investigate GBPAUD_C breakout_R_2_tp20.0_sl5.0 Live-Trade Flag Mismatch on 2026-04-10

Source: User investigation request on 2026-04-11 for `GBPAUD_C | breakout_R_2_tp20.0_sl5.0` trades on `2026-04-10` appearing as live on `fs/weekly_performance.html` but not marked as live in the underlying trade files.

Task Type: investigation

Task Attributes:
- priority: high
- execution_owner: codex
- workflow_ready: true
- ui_task: true

## Findings

1. `weekly_performance.html` does not show actual live-trade execution status in the `Live Trade` column.
   - The column is rendered as a checkbox toggle sourced from `isStrategyActive(product, strategy)`, not from `is_live_trade` or `order_sent_net`.
   - References:
   - `C:\Users\edebe\eds\TradeApps\breakout\fs\weekly_performance.html:1286`
   - `C:\Users\edebe\eds\TradeApps\breakout\fs\weekly_performance.html:1345`
   - `C:\Users\edebe\eds\TradeApps\breakout\fs\weekly_performance.html:802`

2. `isStrategyActive(...)` checks activation state only.
   - It reads `activations['breakout_<strategy>_buy_net']` and `activations['breakout_<strategy>_sell_net']` and returns `true` if either activation is active for the product.
   - It does not inspect trade JSONs, `_live_trades.json`, `is_live_trade`, `order_sent_net`, or `live_trade_executed`.
   - Reference:
   - `C:\Users\edebe\eds\TradeApps\breakout\fs\weekly_performance.html:802`

3. The actual `2026-04-10` GBPAUD_C trade files for `breakout_R_2_tp20.0_sl5.0` were not live trades.
   - Checked files:
   - `breakout_R_2_tp20.0_sl5.0_0854c49d_GBPAUD_C_20260410_152058_2_0.00015_20.0_5.0_cld.json`
   - `breakout_R_2_tp20.0_sl5.0_3c6aa16c_GBPAUD_C_20260410_210104_2_0.00015_20.0_5.0_cl.json`
   - `breakout_R_2_tp20.0_sl5.0_c4daa0c7_GBPAUD_C_20260410_114446_2_0.00015_20.0_5.0_cld.json`
   - Observed values:
   - `is_live_trade: false`
   - `order_sent_net: false` or null
   - `order_sent_alt: false` or null

4. The day-level live-trade export for `2026-04-10` was empty.
   - `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\forex\2026-04-10\_live_trades.json`
   - Observed: `"trade_count": 0`

5. The weekly screen likely indicated “live” because the strategy was activated for auto-promotion, not because any 2026-04-10 trade was routed live.
   - Current activation state contains:
   - `breakout_breakout_R_2_tp20.0_sl5.0_buy_net`
   - `breakout_breakout_R_2_tp20.0_sl5.0_sell_net`
   - both active for `products: ['GBPAUD_C']`
   - This explains the checked toggle in `weekly_performance.html`.
   - Note: the current activation timestamp is `2026-04-11T02:04:23.122245`, so the weekly page reflects current activation state rather than historical 2026-04-10 execution state.

## Conclusion

The trades were not marked as live because they were not live trades on disk. The apparent contradiction comes from `weekly_performance.html` using the label `Live Trade` for what is actually an activation/auto-promotion toggle. The UI is therefore misleading: it can show a checked state even when no underlying trade JSON for that strategy/product/date has `is_live_trade=true`.

## Recommended Fix

- Rename the `Live Trade` column in `weekly_performance.html` to something accurate such as `Auto Promote` or `Activation`.
- If true live execution status is needed on that screen, add a separate column sourced from real trade flags (`is_live_trade`, `order_sent_net`, `order_sent_alt`) or from `_live_trades.json`.
