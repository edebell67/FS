-- Table: combined_trades_open_snapshot
-- Author: Gemini
-- Create Date: 2025-10-26
-- Description: PostgreSQL table for snapshots of combined_trades_open data.

CREATE TABLE combined_trades_open_snapshot (
    guid VARCHAR(50),
    model VARCHAR(64) NOT NULL,
    product VARCHAR(50),
    product_type VARCHAR(50),
    created TIMESTAMP,
    last_update TIMESTAMP,
    signal VARCHAR(16) NOT NULL,
    entry_price DOUBLE PRECISION,
    latest_price DOUBLE PRECISION,
    entry_price2 DOUBLE PRECISION,
    latest_price2 DOUBLE PRECISION,
    commission DOUBLE PRECISION,
    target_profit SMALLINT,
    target_loss SMALLINT,
    rl_signal VARCHAR(1),
    tradeable SMALLINT,
    net_return DOUBLE PRECISION,
    alt_net_return DOUBLE PRECISION,
    pos_net_return_buy SMALLINT,
    pos_net_return_sell SMALLINT,
    trade_diff SMALLINT,
    RL_Check VARCHAR(50),
    percent_profit DOUBLE PRECISION,
    percent_loss DOUBLE PRECISION,
    buy_count DOUBLE PRECISION,
    sell_count DOUBLE PRECISION,
    linked SMALLINT,
    int_profit DOUBLE PRECISION,
    int_profit_time TIMESTAMP,
    trade_quantity BIGINT,
    min_net_return NUMERIC(18, 8),
    min_net_return_time TIMESTAMP,
    max_net_return NUMERIC(18, 8),
    max_net_return_time TIMESTAMP,
    trade_reason VARCHAR(50),
    flip_trade SMALLINT,
    snapshotTime TIMESTAMP NOT NULL DEFAULT NOW(),
    update_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Add an index for better query performance on snapshotTime if needed
CREATE INDEX ix_combined_trades_open_snapshot_snapshottime ON combined_trades_open_snapshot (snapshotTime ASC);
-- Add an index for update_time if frequently queried or used in WHERE clauses
CREATE INDEX ix_combined_trades_open_snapshot_update_time ON combined_trades_open_snapshot (update_time ASC);