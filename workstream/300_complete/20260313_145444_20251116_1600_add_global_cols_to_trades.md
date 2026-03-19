# Plan: Add Global Return Columns to Trade Tables

This document outlines the plan to add new columns to the `combined_trades_closed` and `combined_trades_open` tables in both the `tradedb` and `tradedb_sim2` databases.

## 1. Requirements

Add the following columns to `combined_trades_closed` and `combined_trades_open` in both `tradedb` and `tradedb_sim2`:
- `g_close_time` (DATETIME)
- `g_net_return` (FLOAT)
- `g_alt_net_return` (FLOAT)

## 2. Plan of Approach

1.  **Create SQL Script**: A SQL script will be created containing the necessary `ALTER TABLE` statements.
2.  **Execute SQL Script**: The script will be executed using `sqlcmd` to apply the schema changes to both databases.

## 3. List of Changes

*   [X] Create and save the plan document.
*   [ ] Create the `add_global_cols.sql` script.
*   [ ] Add `ALTER TABLE` for `tradedb.dbo.combined_trades_closed`.
*   [ ] Add `ALTER TABLE` for `tradedb.dbo.combined_trades_open`.
*   [ ] Add `ALTER TABLE` for `tradedb_sim2.dbo.combined_trades_closed`.
*   [ ] Add `ALTER TABLE` for `tradedb_sim2.dbo.combined_trades_open`.
*   [ ] Execute the SQL script.
*   [ ] Verify the columns exist in all four tables.
