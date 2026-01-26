# Plan: Configurable G-Level for Signal Generation in `sp_001_zone_distribution_trade`

**Date:** 2025-11-07 15:30

**Version:** X

## 1. Understanding of Requirements

The goal is to introduce flexibility in the `sp_001_zone_distribution_trade` stored procedure, allowing users to dynamically select which `G` level (from `G1` to `G9`) should be used for buy and sell signal generation. This selection will be controlled by new configuration entries in `dbo.config`.

*   **Configurable `G` Level:** The columns `s_G[X]` and `b_G[X]` (where `X` is 1-9) should be selectable for signal evaluation.
*   **Configuration Parameters:** Two new entries in `dbo.config` will control this:
    *   `sp_001_zone_buy_var`: Specifies the `G` level for buy signals (e.g., 'G9', 'G5', 'G3').
    *   `sp_001_zone_sell_var`: Specifies the `G` level for sell signals (e.g., 'G9', 'G5', 'G3').
*   **Dynamic Switching:** The system should be able to switch between `G` levels at any time by updating the config values.

## 2. Plan of Approach

The primary challenge is dynamically referencing SQL column names based on configuration values. This will be achieved using dynamic SQL (`sp_executesql`).

1.  **Retrieve Config Values:** Load `sp_001_zone_buy_var` and `sp_001_zone_sell_var` from `dbo.config`. Default to 'G9' if not found.
2.  **Modify Variable Declarations:** Replace the hardcoded `_g9` suffixes in the signal evaluation variables with generic names (e.g., `@current_s_g_val`, `@previous_s_g_val`).
3.  **Dynamic SQL for Data Retrieval:** Construct and execute dynamic SQL queries to fetch the `current` and `previous` `s_G[X]` and `b_G[X]` values from the `#zone_data` temporary table, based on the retrieved config values.
4.  **Modify `RAISERROR` Logging:** Update the debug logging to dynamically display the `G` levels being used for clarity.
5.  **Modify Signal Generation Logic:** Ensure the `IF` conditions for `buy_criteria_met` and `sell_criteria_met` correctly use the dynamically retrieved `G` values.

## 3. List of Changes

*   **`db_scripts/dbo.sp_001_zone_distribution_trade.StoredProcedure.sql`**:
    *   [ ] **Retrieve new config values:**
        *   Declare `DECLARE @buy_g_level nvarchar(50);` and `DECLARE @sell_g_level nvarchar(50);`.
        *   Load `sp_001_zone_buy_var` and `sp_001_zone_sell_var` from `dbo.config`. Set default to 'G9' if NULL.
    *   [ ] **Modify Variable Declarations:**
        *   Change `DECLARE @current_b_g9 float, @previous_b_g9 float;` to `DECLARE @current_b_g_val float, @previous_b_g_val float;`.
        *   Change `DECLARE @current_s_g9 float, @previous_s_g9 float;` to `DECLARE @current_s_g_val float, @previous_s_g_val float;`.
    *   [ ] **Replace static `SELECT` statements with Dynamic SQL for `current` values:**
        *   Construct a dynamic SQL string to `SELECT TOP 1 @current_s_g_val = s_` + `@buy_g_level` + `, @current_b_g_val = b_` + `@sell_g_level` + `, @latest_price_val = latest_price FROM #zone_data ORDER BY snapshot_time DESC;`.
        *   Execute this dynamic SQL using `EXEC sp_executesql`, passing output parameters.
    *   [ ] **Replace static `SELECT` statements with Dynamic SQL for `previous` values:**
        *   Construct a dynamic SQL string to `SELECT @previous_b_g_val = b_` + `@sell_g_level` + `, @previous_s_g_val = s_` + `@buy_g_level` + ` FROM #zone_data ORDER BY snapshot_time DESC OFFSET 1 ROW FETCH NEXT 1 ROW ONLY;`.
        *   Execute this dynamic SQL using `EXEC sp_executesql`, passing output parameters.
    *   [ ] **Modify `RAISERROR` Logging:**
        *   Update the `RAISERROR` message for "Criteria Values" to dynamically include the `G` levels and the generic variable names.
        *   Example: `N'current_s_' + @buy_g_level + N': ' + COALESCE(CAST(@current_s_g_val AS VARCHAR(20)), 'NULL')`.
    *   [ ] **Modify Signal Generation `IF` Conditions:**
        *   Update the `IF` conditions to use `@current_s_g_val`, `@previous_s_g_val`, `@current_b_g_val`, `@previous_b_g_val`.
        *   Example: `IF (@current_b_g_val IS NULL AND @previous_b_g_val > 0)`.

## 4. Required Configuration in `dbo.config` (User Action)

The following entries must be added to the `dbo.config` table for the configurable G-level feature to function correctly:

*   **`sp_001_zone_buy_var`**: `NVARCHAR(50)` - The G-level column to use for buy signals (e.g., `'G9'`, `'G5'`, `'G3'`). Default: `'G9'`.
*   **`sp_001_zone_sell_var`**: `NVARCHAR(50)` - The G-level column to use for sell signals (e.g., `'G9'`, `'G5'`, `'G3'`). Default: `'G9'`.
