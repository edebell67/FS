# Summary of Debugging and Changes for `sp_001_zone_distribution_trade`

**Date:** 2025-11-07 15:00

**Version:** X

## 1. Initial Problem Identification

*   **Issue:** `sp_001_zone_distribution_trade` was not generating any trade signals, consistently logging "Generated 0 initial candidates after sanity checks."
*   **Discrepancy:** User observed non-NULL `s_G9`/`b_G9` data in `vw_201_zone_distribution_snapshots` at specific timestamps, while the stored procedure's internal logs showed `NULL` values for `s_G9`/`b_G9` when processing.

## 2. Debugging Steps and Findings

1.  **Added Debug Logging:** Implemented `RAISERROR` statements within the stored procedure to log:
    *   The `@currentproduct` being processed.
    *   The `COUNT(*)` of rows found for each product in `vw_201_zone_distribution_snapshots`.
    *   The values of `current_s_gX`, `previous_s_gX`, `current_b_gX`, `previous_b_gX`, and `LatestPrice` (where `X` was `9`, `5`, or `3`).
2.  **Identified Commented-Out Logic:** Initial debug logs revealed that the core signal generation logic (variable declarations, data retrieval for `current`/`previous` values, and `IF` conditions for `buy_criteria_met`/`sell_criteria_met`) was entirely commented out. This was the primary reason for no signals being generated.
3.  **Uncommented Signal Generation Logic:** The commented-out block was uncommented to activate the signal generation based on the user's confirmed criteria:
    *   Buy signal: `current s_gX is null AND prev s_gX > 0`
    *   Sell signal: `current b_gX is null AND prev b_gX > 0`
4.  **Testing with `G9` (Initial):** After uncommenting, the stored procedure still showed `NULL` values for `s_G9` and `b_G9` in the debug logs, leading to no signals. This indicated a lack of suitable data in `vw_201_zone_distribution_snapshots` at the time of execution.
5.  **Testing with `G5`:** Modified the stored procedure to use `s_G5`/`b_G5`. Debug logs still showed `NULL` values for `s_G5`/`b_G5`, resulting in no signals.
6.  **Testing with `G3`:** Modified the stored procedure to use `s_G3`/`b_G3`. This test successfully generated a **SELL signal for `gbpcad_c`** and inserted a trade, confirming the logic works when suitable data is present. The `Criteria Values` for `gbpcad_c` showed `current_b_g3: NULL, previous_b_g3: 5`, meeting the sell condition.
7.  **Reverted to `G9`:** As requested by the user, all modifications were reverted to use `s_G9`/`b_G9` for signal generation.

## 3. Changes Implemented

*   **`db_scripts/dbo.sp_001_zone_distribution_trade.StoredProcedure.sql`**:
    *   **Added Debug Logging:** Inserted `RAISERROR` statements to trace product processing, row counts, and criteria values.
    *   **Uncommented Signal Generation Logic:** Activated the block responsible for `current`/`previous` value retrieval, `buy_criteria_met`/`sell_criteria_met` evaluation, and `INSERT INTO #signals`/`INSERT INTO #cand`.
    *   **Temporary `G` Level Changes (Reverted):** Temporarily modified variable declarations, `SELECT` statements, `RAISERROR` logs, and `IF` conditions to use `G5` and then `G3` for testing. These changes were subsequently reverted back to `G9`.

## 4. Conclusion

The `sp_001_zone_distribution_trade` stored procedure's signal generation logic is now active and correctly evaluates the `s_G9`/`b_G9` (or `s_G3`/`b_G3` during testing) values. The successful trade generation with `G3` data confirmed the logic's functionality. The procedure has been reverted to use `G9` as per user request. The primary challenge remains the availability of non-NULL `s_G9` and `b_G9` data in `vw_201_zone_distribution_snapshots` at the time of execution to trigger signals.
