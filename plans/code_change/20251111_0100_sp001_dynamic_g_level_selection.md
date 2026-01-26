# 20251111_0100_sp001_dynamic_g_level_selection.md

## Summary
`sp_001_zone_distribution_trade` now respects the configured buy/sell G-level lists instead of iterating a hard-coded set.

## Changes
1. Parse `sp_001_zone_buy_var` and `sp_001_zone_sell_var` config entries (comma-separated) and populate `#GLevelsToProcess` with the union of those levels, trimming whitespace and deduplicating.
2. If both config values are blank/NULL, fall back to the previous default list (`g9`, `g5`, `g4`, `g3`) so the procedure still operates.
3. The G-level cursor reuses this temp table, so runtime logging and signal processing now only touch the configured G-levels (e.g., `g5`, `g9`).

## Deployment
Run `sqlcmd -S eds\\sqlexpress01 -d tradedb -E -b -i db_scripts/dbo.sp_001_zone_distribution_trade.StoredProcedure.sql` and repeat for `tradedb_sim2` to update both environments.
