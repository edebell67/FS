# Plan: Uncomment Signal Generation Logic in `sp_001_zone_distribution_trade`

**Date:** 2025-11-07 14:50

**Version:** X

## 1. Understanding of Requirements

The previously established signal generation logic within `sp_001_zone_distribution_trade` was found to be commented out. This logic, determining buy/sell signals based on `current s_g9`, `prev s_g9`, `current b_g9`, and `prev b_g9`, is now confirmed by the user to be the desired, active logic.

## 2. Plan of Approach

The `sp_001_zone_distribution_trade` stored procedure contains a block of code responsible for declaring variables, retrieving `s_G9` and `b_G9` values from the `#zone_data` temporary table (which receives data from `vw_201_zone_distribution_snapshots`), evaluating buy/sell criteria, and inserting signals into the `#signals` temporary table. This entire block was previously commented out. The plan is to uncomment this block to activate the signal generation.

## 3. List of Changes

*   **`db_scripts/dbo.sp_001_zone_distribution_trade.StoredProcedure.sql`**:
    *   [x] Uncomment the block of code responsible for:
        *   Declaring `@current_b_g9`, `@previous_b_g9`, `@current_s_g9`, `@previous_s_g9`, `@latest_price_val`.
        *   Retrieving `TOP 1` and `OFFSET 1` rows to populate current and previous `s_G9`/`b_G9` values.
        *   Logging the criteria values for debugging.
        *   Declaring `@buy_criteria_met` and `@sell_criteria_met`.
        *   Evaluating the conditions:
            *   `IF (@current_b_g9 IS NULL AND @previous_b_g9 > 0) THEN SET @sell_criteria_met = 1;`
            *   `IF (@current_s_g9 IS NULL AND @previous_s_g9 > 0) THEN SET @buy_criteria_met = 1;`
        *   Inserting BUY/SELL signals into `#signals` based on `buy_criteria_met` and `sell_criteria_met`.
        *   Logging the total BUY/SELL signals.
        *   The `INSERT #cand` statement, which uses the generated signals.
