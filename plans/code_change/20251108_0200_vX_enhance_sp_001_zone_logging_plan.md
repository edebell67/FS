# Plan: Enhance Logging in `sp_001_zone_distribution_trade`

**Date:** 2025-11-08 02:00

**Version:** X

## 1. Understanding of Requirements

The user wants more granular logging within `sp_001_zone_distribution_trade` to explicitly show the evaluation of buy and sell signal criteria, including the values being compared and the outcome of each comparison.

## 2. Plan of Approach

I will add `RAISERROR` statements at key points within the signal generation section of `sp_001_zone_distribution_trade`. This will provide visibility into:
1.  The values of the G-level variables (`@current_b_g_val`, `@previous_b_g_val`, etc.) immediately before the criteria are evaluated. (This is already partially covered by an existing log, but I'll ensure it's clear).
2.  When each individual buy or sell criterion is met.
3.  The final boolean state of `@buy_criteria_met` and `@sell_criteria_met` before the decision to insert a signal is made.

## 3. List of Changes

*   **`db_scripts/dbo.sp_001_zone_distribution_trade.StoredProcedure.sql`**:
    *   [ ] After `IF (@current_b_g_val IS NULL AND @previous_b_g_val > 0) SET @sell_criteria_met = 1;`, add a `RAISERROR` to log that the sell criterion was met.
    *   [ ] After `IF (@current_s_g_val IS NULL AND @previous_s_g_val > 0) SET @buy_criteria_met = 1;`, add a `RAISERROR` to log that the buy criterion was met.
    *   [ ] Before the `IF @buy_criteria_met = 1 AND @sell_criteria_met = 1` block, add a `RAISERROR` to log the final boolean values of `@buy_criteria_met` and `@sell_criteria_met`.
