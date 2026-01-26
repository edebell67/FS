# Plan: Further Enhance Logging in `sp_001_zone_distribution_trade` for Criteria Values

**Date:** 2025-11-08 03:30

**Version:** X

## 1. Understanding of Requirements

The user wants to see the actual values of the G-level variables (`@current_b_g_val`, `@previous_b_g_val`, `@current_s_g_val`, `@previous_s_g_val`) and how they are evaluated against the signal generation criteria, even when there isn't enough zone data to generate a signal. The current logging is not triggered in such cases.

## 2. Plan of Approach

I will add `RAISERROR` statements at earlier points in the signal generation section of `sp_001_zone_distribution_trade` to capture the values of the G-level variables immediately after they are retrieved (or attempted to be retrieved) from `#zone_data`, and also to show the contents of `#zone_data` itself. This will provide the requested visibility regardless of whether enough rows are found for signal generation.

## 3. List of Changes

*   **`db_scripts/dbo.sp_001_zone_distribution_trade.StoredProcedure.sql`**:
    *   [ ] After the `INSERT INTO #zone_data` statement, add a `RAISERROR` to display the contents of `#zone_data` for the current product. This will show what raw data is available.
    *   [ ] After the `EXEC sp_executesql @sql_select_current ...` statement, add a `RAISERROR` to display the values of `@current_s_g_val`, `@current_b_g_val`, and `@latest_price_val` as they are populated.
    *   [ ] After the `EXEC sp_executesql @sql_select_previous ...` statement, add a `RAISERROR` to display the values of `@previous_b_g_val` and `@previous_s_g_val` as they are populated.
