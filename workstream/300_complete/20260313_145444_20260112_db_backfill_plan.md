# Plan: Database Creation and Data Backfill

**Date:** 2026-01-12

This document outlines the complete plan to create a new PostgreSQL database named `tradedb2` and implement a continuous backfill process for all trade-related JSON data.

---

## Phase 1: Database and Table Creation

This phase involves setting up the necessary database and table structures.

### Step 1: Create the Database

Connect to your PostgreSQL instance and execute:
```sql
CREATE DATABASE tradedb2;
```

### Step 2: Define Table Schemas

Connect to the newly created `tradedb2` database and run the following script. This creates the `trades` and `daily_summary` tables with appropriate keys and indexes for performance and data integrity.

```sql
-- Creates the table for individual trade data from JSON files
CREATE TABLE trades (
    -- Core identifiers
    trade_id BIGINT NOT NULL,
    run_mode VARCHAR(4) NOT NULL, -- 'live' or 'sim'

    -- Trade details
    product VARCHAR(50),
    direction VARCHAR(10),
    status VARCHAR(10),
    entry_time TIMESTAMPTZ,
    entry_price DECIMAL(18, 8),
    exit_time TIMESTAMPTZ,
    exit_price DECIMAL(18, 8),
    exit_reason VARCHAR(100),

    -- Performance metrics
    net_return DECIMAL(18, 8),
    alt_net DECIMAL(18, 8),

    -- Strategy and execution details
    script_name VARCHAR(255),
    is_live_trade BOOLEAN,
    order_sent_net BOOLEAN,
    order_sent_alt BOOLEAN,

    -- Full JSON data for future-proofing and detailed analysis
    raw_data JSONB,

    -- A unique key combining run_mode and trade_id to prevent duplicates
    PRIMARY KEY (run_mode, trade_id)
);

-- Creates the table for summary files like _summary_net.json and _top_one.json
CREATE TABLE daily_summary (
    run_mode VARCHAR(4) NOT NULL,
    summary_date DATE NOT NULL,
    summary_type VARCHAR(50) NOT NULL,
    data JSONB,

    -- A unique key to prevent duplicate summary files for the same day/type/mode
    PRIMARY KEY (run_mode, summary_date, summary_type)
);

-- Add indexes to columns that will be frequently used for filtering
CREATE INDEX idx_trades_entry_time ON trades(entry_time);
CREATE INDEX idx_trades_product ON trades(product);
CREATE INDEX idx_trades_script_name ON trades(script_name);
```

---

## Phase 2: Create the Backfill Script

An idempotent Python script will read the JSON files and upsert them into the database.

### Step 1: Install Python Dependencies

```shell
pip install psycopg2-binary python-dotenv tqdm
```

### Step 2: Create `.env` for Credentials

Create a file named `.env` in the project root to store database credentials securely.

```
# .env file
DB_NAME="tradedb2"
DB_USER="your_postgres_user"
DB_PASSWORD="your_postgres_password"
DB_HOST="localhost"
DB_PORT="5432"
```

### Step 3: Create `backfill_trades.py`

Create the Python script `backfill_trades.py` with the logic to find, read, and upsert trade and summary data from the JSON files. The script uses an `ON CONFLICT DO UPDATE` clause to ensure it can be re-run safely.

*(The full Python code from the previous turn would be included here.)*

---

## Phase 3: Execution and Verification

### Step 1: Run the Script

Execute the backfill process from the terminal:
```shell
python backfill_trades.py
```

### Step 2: Verify the Data in PostgreSQL

After the script completes, run these SQL queries to validate the backfill:
```sql
-- Check total count of live trades
SELECT COUNT(*) FROM trades WHERE run_mode = 'live';

-- Check total count of live summaries
SELECT COUNT(*) FROM daily_summary WHERE run_mode = 'live';

-- View a sample of trade data
SELECT trade_id, run_mode, product, entry_time, net_return FROM trades WHERE run_mode = 'live' LIMIT 10;
```

---

## Phase 4: Continuous Backfill Strategy

The backfill script is designed for repeated execution. While the API is being updated to work with the database, this script can be run at any time to keep the `tradedb2` database synchronized with any new or updated JSON files from the file system. This provides a consistent and up-to-date data source for development and testing of the new API.
