# 2026-03-20 16:25:13 Validate L-trade window matching

## Status: COMPLETE

### Task Overview
Validate how trades should be identified as L-trades using `TradeApps/breakout/fs/json/live/forex/2026-03-20/_tb_leadership.json`, review existing workstream tasks, and verify whether current code paths match the intended rule.

### Chronology
- 2026-03-20 16:25:13: Task file created in `workstream/100_todo`.
- 2026-03-20 16:25:20: Task moved to `workstream/200_inprogress`.
- 2026-03-20 16:25:20: Reviewed existing workstream tasks covering trade bucket leadership and L-trades.
- 2026-03-20 16:25:20: Loaded `TradeApps/breakout/fs/json/live/forex/2026-03-20/_tb_leadership.json` to validate the persisted leadership-window format.
- 2026-03-20 16:29:00: Validated that `_tb_leadership.json` uses the required source-of-truth structure: bucket name plus strategy leadership windows with inclusive start and exclusive end semantics.
- 2026-03-20 16:31:00: Confirmed current `trade_bucket.html` did not load `/api/tb_leadership` for card-level counts and did not honor backend `is_l_trade` tags in drilldowns.
- 2026-03-20 16:34:00: Updated `TradeApps/breakout/fs/trade_bucket.html` to load persistent leadership windows, normalize them by `strategy|product`, use them for bucket/strategy L-trade counts, and treat `is_l_trade` as a first-class signal.
- 2026-03-20 16:35:00: Reconciled the three NZDAUD screenshot buckets against `_trades_summary.json` to compute direct leadership-window matches.

### Validation
- `Get-Content workstream\\100_todo\\20260320_115815_breakout_tb_leadership_ltrades.md -TotalCount 220`
- `Get-Content workstream\\200_inprogress\\20260320_110503_breakout_tb_leader_definition.md -TotalCount 220`
- `Get-Content workstream\\300_complete\\20260320_124500_breakout_tb_leadership_tracking.md -TotalCount 240`
- `Get-Content TradeApps\\breakout\\fs\\json\\live\\forex\\2026-03-20\\_tb_leadership.json -TotalCount 250`
- `rg -n \"tb_leadership|is_l_trade|bucket_name|leadership|L-Trade|l-trade\" TradeApps\\breakout\\fs\\trade_viewer_api.py`
- `rg -n \"tb_leadership|buildLeaderWindowsMap\\(|leaderWindowsMap|/api/tb_leadership\" TradeApps\\breakout\\fs\\trade_bucket.html`
- Powershell reconciliation against `_tb_leadership.json` and `_trades_summary.json` for the three NZDAUD buckets:
  - `AUTO_TB_0320_025235_163_NZDAUD_C_breakout_R_Rev_3_tp20_0_sl5_0`: 31 relevant trades, 7 L-trades, sum net `330.00`
  - `AUTO_TB_0320_025235_541_NZDAUD_C_breakout_R_2_tp10_0_sl5_0`: 55 relevant trades, 14 L-trades, sum net `-127.50`
  - `AUTO_TB_0320_025235_692_NZDAUD_C_breakout_Rev_3_tp10_0_sl5_0`: 43 relevant trades, 13 L-trades, sum net `155.00`
