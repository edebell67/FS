-- Table: combined_trades_closed_arc
-- Author: Gemini
-- Create Date: 2025-11-02
-- Description: PostgreSQL table for archived closed trade data.

CREATE TABLE combined_trades_closed_arc (
    guid VARCHAR(50),
    model TEXT NOT NULL,
    product VARCHAR(50),
    product_type VARCHAR(50),
    created TIMESTAMP,
    last_update TIMESTAMP,
    signal VARCHAR(50),
    entry_price DOUBLE PRECISION,
    latest_price DOUBLE PRECISION,
    entry_price2 DOUBLE PRECISION,
    latest_price2 DOUBLE PRECISION,
    trade_quantity DOUBLE PRECISION,
    commission DOUBLE PRECISION,
    target_profit DOUBLE PRECISION,
    target_loss DOUBLE PRECISION,
    rl_signal VARCHAR(1),
    tradeable DOUBLE PRECISION,
    net_return DOUBLE PRECISION,
    alt_net_return DOUBLE PRECISION,
    pos_net_return_buy DOUBLE PRECISION,
    pos_net_return_sell DOUBLE PRECISION,
    trade_diff DOUBLE PRECISION,
    RL_Check DOUBLE PRECISION,
    percent_profit DOUBLE PRECISION,
    percent_loss DOUBLE PRECISION,
    buy_count DOUBLE PRECISION,
    sell_count DOUBLE PRECISION,
    linked SMALLINT,
    int_profit DOUBLE PRECISION,
    int_profit_time TIMESTAMP,
    close_type VARCHAR(50),
    min_net_return NUMERIC(18, 8),
    min_net_return_time TIMESTAMP,
    max_net_return NUMERIC(18, 8),
    max_net_return_time TIMESTAMP,
    trade_reason VARCHAR(200),
    flip_trade BOOLEAN
);
