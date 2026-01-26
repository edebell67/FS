# Plan: Debug `sp_loop_create_trades_v2` Skip Logic

**Date:** 2025-11-08 01:45

**Version:** X

## 1. Understanding of Requirements

The `sp_loop_create_trades_v2` stored procedure is exhibiting contradictory behavior regarding its skip flags:
*   `sp_001_zone_distribution_trade` is being skipped despite `skip_001_zone` being `0` in `dbo.config`.
*   `sp_001_breakout_entry` is executing despite `skip_breakout_entry` being `1` in `dbo.config`.

The goal is to understand why these discrepancies are occurring.

## 2. Plan of Approach

The most direct way to diagnose this is to inspect the values of the skip variables *within* `sp_loop_create_trades_v2` immediately after they are loaded from `dbo.config`. This will confirm what values the stored procedure is actually using for its conditional logic.

## 3. List of Changes

*   **`db_scripts/dbo.sp_loop_create_trades_v2.StoredProcedure.sql`**:
    *   [ ] Add `RAISERROR` statement to log the value of `@skip_001_zone` after it is loaded from `dbo.config`.
    *   [ ] Add `RAISERROR` statement to log the value of `@skip_breakout_entry` after it is loaded from `dbo.config`.
