# JSON vs PostgreSQL Database Usage Analysis
**Date:** 2026-01-20 12:34  
**Version:** Analysis of current state

## Executive Summary

This document analyzes which functions in the `breakout` application are still interacting with JSON files versus the PostgreSQL database. The application is in a **hybrid state** with some components migrated to PostgreSQL while others still rely on JSON files.

## Current Database Configuration

- **DATA_SOURCE**: Configured in `config.json` (values: `"file_system"` or `"database"`)
- **Database Connection**: PostgreSQL via `psycopg2`
- **Environment**: Connection details stored in `.env` file

## Functions Using PostgreSQL Database

### trade_viewer_api.py

#### ✅ Migrated to PostgreSQL:

1. **`_get_daily_summary(run_mode, date_str, summary_type)`** (Line 124-146)
   - Fetches summary data from SQL when `DATA_SOURCE == "database"`
   - Falls back to JSON file when `DATA_SOURCE == "file_system"`
   - SQL Query: `SELECT data FROM daily_summaries WHERE run_mode = ? AND summary_date = ? AND summary_type = ?`

2. **`_save_daily_summary(run_mode, date_str, summary_type, data)`** (Line 148-165)
   - Saves summary data to PostgreSQL when `DATA_SOURCE == "database"`
   - SQL Query: `INSERT INTO daily_summaries ... ON CONFLICT ... DO UPDATE`

3. **`_load_trade_buckets(mode, date_str)`** (Line 100-122)
   - Loads trade buckets from database when `DATA_SOURCE == "database"`
   - Falls back to JSON when using file system

4. **`get_strategy_performance()`** (Line ~854)
   - Uses database queries with parameterized SQL
   - Executes: `cursor.execute(sql, tuple(params))`

### backfill_trades.py

#### ✅ Migrated to PostgreSQL:

1. **Trade insertion logic** (Line 161)
   - Inserts trade data into PostgreSQL
   - SQL: `INSERT INTO trades ...`

2. **Summary data insertion** (Line 185)
   - Inserts summary data using `Json()` type
   - SQL: `INSERT INTO daily_summaries ...`

### top_one_generator.py

#### ✅ Migrated to PostgreSQL:

1. **Table creation** (Line 51)
   - Creates `top_one` table in PostgreSQL
   - Executes: `cursor.execute(create_table_query)`

2. **Data insertion** (Lines 77, 95)
   - Inserts top performer data into database

## Functions Still Using JSON Files

### common.py - Critical JSON Dependencies

#### 🔴 Still Using JSON Files:

1. **`_load_config()`** (Line 35-66)
   - **Purpose**: Loads main configuration from `config.json`
   - **File**: `config.json`
   - **Status**: ⚠️ Should remain JSON (application configuration)

2. **`_load_persisted_state()`** (Line 402-493)
   - **Purpose**: Scans disk for open trades and restores trade counter
   - **Files**: Individual trade JSON files in `json/{mode}/{date}/` directories
   - **Status**: 🔴 **NEEDS MIGRATION** - Should query database for open trades

3. **`_get_activation_details()`** (Line 501-529)
   - **Purpose**: Retrieves activation details for a strategy
   - **File**: `activations.json`
   - **Status**: 🔴 **NEEDS MIGRATION** - Should be in database

4. **`_is_profitability_guard_passed()`** (Line ~1004)
   - **Purpose**: Checks profitability guard by scanning historical trades
   - **Files**: Scans multiple JSON trade files
   - **Status**: 🔴 **NEEDS MIGRATION** - Should query database with WHERE clause

5. **`_load_active_trades()`** (Line ~1527)
   - **Purpose**: Loads currently active trades
   - **File**: `active_trades.json`
   - **Status**: 🔴 **NEEDS MIGRATION** - Should query database

6. **`_save_active_trades()`** (Line ~1547)
   - **Purpose**: Saves active trades to disk
   - **File**: `active_trades.json`
   - **Status**: 🔴 **NEEDS MIGRATION** - Should update database

7. **`_load_virtual_trades()`** (Line ~1691)
   - **Purpose**: Loads virtual trades
   - **File**: Virtual trade JSON files
   - **Status**: 🔴 **NEEDS MIGRATION** - Should query database

8. **`_save_virtual_trade()`** (Line ~1798)
   - **Purpose**: Saves virtual trade to disk
   - **Files**: Individual virtual trade JSON files
   - **Status**: 🔴 **NEEDS MIGRATION** - Should insert into database

9. **`_manage_virtual_trades()`** (Line ~1924)
   - **Purpose**: Manages virtual trade lifecycle
   - **Files**: Reads multiple JSON files
   - **Status**: 🔴 **NEEDS MIGRATION** - Should use database queries

10. **`_update_trade_buckets()`** (Line ~2570)
    - **Purpose**: Updates trade bucket statistics
    - **File**: `_trade_bucket.json`
    - **Status**: 🔴 **NEEDS MIGRATION** - Should update database

11. **`_load_summary_net()`** (Line ~2857)
    - **Purpose**: Loads summary net data
    - **File**: `_summary_net.json`
    - **Status**: 🔴 **NEEDS MIGRATION** - Should query database

12. **`_save_summary_net()`** (Line ~2891)
    - **Purpose**: Saves summary net data
    - **File**: `_summary_net.json`
    - **Status**: 🔴 **NEEDS MIGRATION** - Should update database

13. **`_get_all_trades_for_product()`** (Line ~3154)
    - **Purpose**: Retrieves all trades for a specific product
    - **Files**: Scans multiple JSON files
    - **Status**: 🔴 **NEEDS MIGRATION** - Should use SELECT query

14. **`_load_all_trades()`** (Line ~3304, 3314)
    - **Purpose**: Loads all trades from disk
    - **Files**: Scans all JSON trade files
    - **Status**: 🔴 **NEEDS MIGRATION** - Should use SELECT query

### trade_viewer_api.py - Partial Migration

#### 🟡 Hybrid Functions (Support Both):

1. **`_get_daily_summary()`** - ✅ Already supports both
2. **`_save_daily_summary()`** - ✅ Already supports database
3. **`_load_trade_buckets()`** - ✅ Already supports both

#### 🔴 Still JSON Only:

1. **`get_trade_file()`** (Line 348-386)
   - **Purpose**: Loads raw content of specific trade JSON file
   - **Status**: 🔴 **NEEDS MIGRATION** - Should query database

2. **`_find_open_trade_for_descriptor()`** (Line 449-477)
   - **Purpose**: Finds open trade matching descriptor
   - **Files**: Scans JSON files with glob patterns
   - **Status**: 🔴 **NEEDS MIGRATION** - Should use database query

3. **`_promote_trade_file_to_live()`** (Line 480-531)
   - **Purpose**: Promotes virtual trade to live
   - **Files**: Reads and writes JSON files
   - **Status**: 🔴 **NEEDS MIGRATION** - Should update database records

### Other Python Files Still Using JSON

1. **`backfill_trades.py`** (Lines 44, 175)
   - Reads JSON files to backfill into database
   - Status: ⚠️ **Transitional** - Used for migration purposes

2. **`calc_net_return.py`** (Line 25)
   - Calculates net return from JSON files
   - Status: 🔴 **NEEDS MIGRATION**

3. **`check_pnl.py`** (Line 13)
   - Checks P&L from JSON files
   - Status: 🔴 **NEEDS MIGRATION**

4. **`cleanup_l_trades.py`** (Lines 17, 30)
   - Cleans up L-trades from JSON
   - Status: 🔴 **NEEDS MIGRATION**

5. **`cleanup_vtrades.py`** (Line 31)
   - Cleans up virtual trades from JSON
   - Status: 🔴 **NEEDS MIGRATION**

6. **`count_live_trades.py`** (Line 21)
   - Counts live trades from JSON
   - Status: 🔴 **NEEDS MIGRATION**

## Migration Priority Recommendations

### High Priority (Core Trading Functions)

1. ✅ **`_load_persisted_state()`** - Critical for trade state recovery
2. ✅ **`_load_active_trades()` / `_save_active_trades()`** - Active trade management
3. ✅ **`_is_profitability_guard_passed()`** - Performance-critical, currently scans many files
4. ✅ **`_load_all_trades()`** - Performance bottleneck
5. ✅ **`_get_activation_details()`** - Core activation logic

### Medium Priority (Summary & Reporting)

6. ✅ **`_load_summary_net()` / `_save_summary_net()`** - Already partially migrated
7. ✅ **`_update_trade_buckets()`** - Trade bucket management
8. ✅ **`_manage_virtual_trades()`** - Virtual trade lifecycle

### Low Priority (Utilities)

9. ✅ **`calc_net_return.py`** - Utility script
10. ✅ **`check_pnl.py`** - Utility script
11. ✅ **`cleanup_*.py`** - Maintenance scripts

### Should Remain JSON

- ✅ **`config.json`** - Application configuration (appropriate for JSON)
- ⚠️ **`activations.json`** - Could be migrated but may be useful as file for manual editing

## Database Schema Requirements

To complete the migration, the following tables/columns are needed:

### Existing Tables
- ✅ `daily_summaries` (run_mode, summary_date, summary_type, data)
- ✅ `trades` (trade data storage)
- ✅ `top_one` (top performer data)

### Required New Tables/Columns

1. **`active_trades`** table
   - Columns: trade_id, product, strategy, direction, entry_time, entry_price, status, etc.

2. **`virtual_trades`** table
   - Similar structure to active_trades with virtual-specific fields

3. **`activations`** table
   - Columns: strategy, direction, mode, active (boolean), products (array/json), manual (boolean)

4. **`trade_buckets`** table
   - Columns: run_mode, date, bucket_name, strategy_stats (json), open_trades, open_trade_count

## Verification Checklist

- [ ] All `json.load()` calls in `common.py` reviewed
- [ ] All `json.dump()` calls in `common.py` reviewed
- [ ] Database schema includes all required tables
- [ ] Migration scripts created for historical data
- [ ] Backward compatibility maintained during transition
- [ ] Performance testing completed (database vs file system)
- [ ] Error handling for database connection failures
- [ ] Rollback plan documented

## Notes

- The application currently supports a `DATA_SOURCE` configuration that allows switching between file system and database
- Some functions have already been updated to support both modes
- A complete migration would require updating all JSON-dependent functions to query PostgreSQL
- Consider maintaining JSON export functionality for backup/debugging purposes

---

**Next Steps:**
1. Review this analysis with stakeholder
2. Create detailed migration plan for high-priority functions
3. Implement database schema changes
4. Update functions one by one with proper testing
5. Maintain backward compatibility during transition
