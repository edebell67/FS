## Gemini Coder - Plan for "Add to Profitable Trades" Feature (v2)

This document outlines the plan to create a new stored procedure that adds to existing profitable trades, with a new constraint to prevent runaway trade creation.

### 1. Understanding of Requirements

The goal is to create a new stored procedure, `dbo.sp_add_to_profitable_trades`, that automatically "adds to" winning positions.

*   **Trigger:** The procedure will be driven by a new configuration setting, `add_to_trade_list`.
*   **Scan Logic:** The procedure will scan the `dbo.combined_trades_open` table for trades whose `trade_reason` is in the `add_to_trade_list`.
*   **Condition:** For each of these trades, it will check if *either* its `net_return` or `alt_net_return` is positive and exceeds the configured `add_to_trade_scan_value`.
*   **New Constraint:** A new trade will only be created if the profitable source trade has **not already been used** to create an "add-on" trade. This prevents a single profitable trade from generating multiple copies.
*   **Tracking Mechanism:** The new constraint will be enforced by adding a new `source_trade_guid` column to the `dbo.combined_trades_open` table. This column will be `NULL` for original trades and will contain the `guid` of the parent trade for "add-on" trades.
*   **Action:** If all conditions are met, the procedure will create and insert a new trade that is an identical copy of the profitable open trade, populating the new `source_trade_guid` field.
*   **Integration:** The new stored procedure will be integrated into the main `dbo.sp_loop_create_trades_v2` loop.

### 2. Plan of Approach

1.  **Schema Change:** First, I will provide the `ALTER TABLE` script to add the new `source_trade_guid` column to the `dbo.combined_trades_open` table. This is a prerequisite for the rest of the logic.
2.  **Create New Stored Procedure:** I will create the `dbo.sp_add_to_profitable_trades` SP. Its logic will be updated to:
    *   Load its configuration.
    *   Select profitable trades from `combined_trades_open` that meet the criteria.
    *   Crucially, the selection query will include a condition to **exclude** trades that have already been copied (i.e., whose `guid` already appears in the `source_trade_guid` column of another trade).
    *   When inserting the new copy, it will populate the `source_trade_guid` column with the `guid` of the original trade.
3.  **Integrate into Main Loop:** I will modify `dbo.sp_loop_create_trades_v2` to execute the new SP on each loop iteration, controlled by a `skip` flag.

### 3. List of Changes

*   **Schema Change: `dbo.combined_trades_open`**
    *   The following SQL script must be run first to add the necessary column:
        ```sql
        ALTER TABLE dbo.combined_trades_open
        ADD source_trade_guid UNIQUEIDENTIFIER NULL;
        GO
        ```

*   **New File: `db_scripts/dbo.sp_add_to_profitable_trades.StoredProcedure.sql`**
    *   Create a new stored procedure. The logic will be updated to:
        *   Select profitable trades `o` from `combined_trades_open` where `o.trade_reason` is in the list, the profit condition is met, AND `NOT EXISTS (SELECT 1 FROM dbo.combined_trades_open WHERE source_trade_guid = o.guid)`.
        *   The `INSERT` statement will now include the `source_trade_guid` column, populating it with the `guid` of the original trade being copied.

*   **Modify: `db_scripts/dbo.sp_loop_create_trades_v2.StoredProcedure.sql`**
    *   Add a new local variable: `@skip_add_to_trade INT`.
    *   Add a `SELECT` statement to load the `skip_add_to_trade` value from `dbo.config`.
    *   Add a new `IF ISNULL(@skip_add_to_trade, 0) = 0 BEGIN TRY...END TRY...END CATCH` block to execute `dbo.sp_add_to_profitable_trades`.

*   **Configuration: `dbo.config` Table**
    *   The following rows will need to be added to `dbo.config`:
        *   `('skip_add_to_trade', '0')`
        *   `('add_to_trade_list', 'sp_001_v6,sp_001_v8')`
        *   `('add_to_trade_scan_value', '50')`

*   **Plan File Creation**
    *   Save this plan to `C:\Users\edebe\eds\plans\20250928_add_to_trade_feature_v2.md`.
