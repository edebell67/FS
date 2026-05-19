# Plan: Complete Workstream 1 Database Migrations
**Date:** 2026-01-20 19:40
**Version:** V20260120_1940
**Description:** Finalize the migration of JSON data to PostgreSQL for all tables, fixing data type mismatches and ensuring comprehensive data capture.

## Mission
Ensure all JSON-based data for the breakout application is correctly and fully migrated to the PostgreSQL `tradedb2` database, resolving any schema/data type issues found during execution.

## Checklist
- [x] 1. Fix `migrate_trade_buckets.py`
    - [x] Cast `open_trades` boolean to integer.
    - [x] Add `total_net` and `live_trade_net` calculation per product per bucket.
    - [x] Update SQL statement to include new fields and fix column type errors.
- [x] 2. Execute Migration Scripts
    - [x] Run `migrate_activations.py`
    - [x] Run `migrate_active_trades.py`
    - [x] Run `migrate_virtual_trades.py`
    - [x] Run `migrate_trade_buckets.py`
    - [x] Run `migrate_top_performers.py`
    - [x] Run `migrate_closed_trades.py`
    - [x] Run `migrate_daily_summaries.py` (Captures `summary_net` and `summary_totals`)
- [x] 3. Verification
    - [x] Verify record counts in each table.
    - [x] Spot check data completeness.
    - [x] Verified recursive capture from `_g_archive`.
- [x] 4. Finalize
    - [x] Update `Constants.py` version to `V20260120_1940`.

## Notes
- `trade_buckets` migration was failing due to `open_trades` being a boolean in JSON but an integer in DB.
- `trades` table already contains historical data from Dec 2025.
- Today's migration focused on `2026-01-20`.
