# Gemini Coder - Plan for sp_001_buy_sell_count_entry Enhancement

This document outlines the plan to modify `sp_001_buy_sell_count_entry` to use `vw_900_dynamic_leadership_live` for signal generation, as requested on 2025-11-13.

## 1. Understanding of Requirements

The goal is to update the `sp_001_buy_sell_count_entry` stored procedure. Currently, it uses `dbo.vw_125_top5_netreturn_signal_counts` to determine if a product should generate a 'BUY' or 'SELL' signal based on whether all 5 top net-return trades have the same signal. This needs to be changed to use `dbo.vw_900_dynamic_leadership_live`. The new logic will check if all 5 rows returned by `vw_900_dynamic_leadership_live` for a given product have the same signal (either all 'BUY' or all 'SELL'). If they do, that signal will be used for trade generation.

## 2. Plan of Approach

The primary change will be within the "Signals-driven candidates" section of `sp_001_buy_sell_count_entry`.

1.  **Modify `#signals` CTE**:
    *   Replace the source view from `dbo.vw_125_top5_netreturn_signal_counts` to `dbo.vw_900_dynamic_leadership_live`.
    *   Adjust the logic to count 'BUY' and 'SELL' signals from `vw_900_dynamic_leadership_live` for each product.
    *   Implement the condition: if all 5 entries for a product in `vw_900_dynamic_leadership_live` have the same signal (either all 'BUY' or all 'SELL'), then that signal should be used.

## 3. List of Changes

*   **`db_scripts/dbo.sp_001_buy_sell_count_entry.StoredProcedure.sql`**:
    *   [x] **Update `#signals` CTE**:
        *   Change the `FROM` clause from `dbo.vw_125_top5_netreturn_signal_counts` to `dbo.vw_900_dynamic_leadership_live`.
        *   Modify the `SELECT` statement within `#signals` to:
            *   Group by `product`.
            *   Count the occurrences of 'BUY' and 'SELL' signals from `vw_900_dynamic_leadership_live` for each product.
            *   Determine the final `signal` ('buy' or 'sell') based on whether the count of 'BUY' signals is 5 (and total count is 5) or the count of 'SELL' signals is 5 (and total count is 5).
        *   Ensure the `total_in_top5` check is adapted to the new view's structure, which implicitly returns top 5.

```sql
-- Old #signals CTE (for reference)
-- IF OBJECT_ID('tempdb..#signals') IS NOT NULL DROP TABLE #signals;
-- SELECT LOWER(product) AS product,
--        CASE
--            WHEN buy_count = 5 THEN N'buy'
--            WHEN sell_count = 5 THEN N'sell'
--        END AS signal
-- INTO #signals
-- FROM dbo.vw_125_top5_netreturn_signal_counts
-- WHERE (buy_count = 5 OR sell_count = 5)
--   AND total_in_top5 = 5;
-- DELETE FROM #signals WHERE signal IS NULL;

-- New #signals CTE (to be implemented)
IF OBJECT_ID('tempdb..#signals') IS NOT NULL DROP TABLE #signals;
SELECT
    LOWER(v.product) AS product,
    CASE
        WHEN SUM(CASE WHEN v.signal = 'BUY' THEN 1 ELSE 0 END) = 5 THEN N'buy'
        WHEN SUM(CASE WHEN v.signal = 'SELL' THEN 1 ELSE 0 END) = 5 THEN N'sell'
        ELSE NULL
    END AS signal
INTO #signals
FROM dbo.vw_900_dynamic_leadership_live AS v
GROUP BY v.product
HAVING COUNT(v.model) = 5; -- Ensure all 5 top models are present for the product

DELETE FROM #signals WHERE signal IS NULL;
```
    *   [x] **Update logging messages**: Adjust the `RAISERROR` messages related to signal generation to reflect the change in the source view if necessary.
    *   [x] **Add comment**: Add a comment explaining the change and the date.
*   **`db_scripts/dbo.vw_900_dynamic_leadership_live.View.sql`**:
    *   [x] Added `v.product` to the `SELECT` list and `GROUP BY` clause.
*   **Deployment**:
    *   [x] Deployed modified `vw_900_dynamic_leadership_live` to `tradedb`.
    *   [x] Deployed modified `vw_900_dynamic_leadership_live` to `tradedb_sim2`.
    *   [x] Changed `CREATE PROCEDURE` to `ALTER PROCEDURE` in `sp_001_buy_sell_count_entry.StoredProcedure.sql`.
    *   [x] Deployed modified `sp_001_buy_sell_count_entry` to `tradedb`.
    *   [x] Deployed modified `sp_001_buy_sell_count_entry` to `tradedb_sim2`.
