-- =============================================================================
-- PostgreSQL DDL Replica for tradedb (Mirrored from SQL Server tradedb)
-- Version: V20260919_1518
-- Target Platform: PostgreSQL 14+
-- =============================================================================

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- =============================================================================
-- SECTION 1: USER TABLES (Total: 84)
-- =============================================================================

-- Table: dbo.PivotedGbpNetReturnTodaySummary
CREATE TABLE IF NOT EXISTS pivotedgbpnetreturntodaysummary (
    entry_price NUMERIC(18,8) NOT NULL,
    "00:00-00:30" NUMERIC(19,4),
    "00:30-01:00" NUMERIC(19,4),
    "01:00-01:30" NUMERIC(19,4),
    "01:30-02:00" NUMERIC(19,4),
    "02:00-02:30" NUMERIC(19,4),
    "02:30-03:00" NUMERIC(19,4),
    "03:00-03:30" NUMERIC(19,4),
    "03:30-04:00" NUMERIC(19,4),
    "04:00-04:30" NUMERIC(19,4),
    "04:30-05:00" NUMERIC(19,4),
    "05:00-05:30" NUMERIC(19,4),
    "05:30-06:00" NUMERIC(19,4),
    "06:00-06:30" NUMERIC(19,4),
    "06:30-07:00" NUMERIC(19,4),
    "07:00-07:30" NUMERIC(19,4),
    "07:30-08:00" NUMERIC(19,4),
    "08:00-08:30" NUMERIC(19,4),
    "08:30-09:00" NUMERIC(19,4),
    "09:00-09:30" NUMERIC(19,4),
    "09:30-10:00" NUMERIC(19,4),
    "10:00-10:30" NUMERIC(19,4),
    "10:30-11:00" NUMERIC(19,4),
    "11:00-11:30" NUMERIC(19,4),
    "11:30-12:00" NUMERIC(19,4),
    "12:00-12:30" NUMERIC(19,4),
    "12:30-13:00" NUMERIC(19,4),
    "13:00-13:30" NUMERIC(19,4),
    "13:30-14:00" NUMERIC(19,4),
    "14:00-14:30" NUMERIC(19,4),
    "14:30-15:00" NUMERIC(19,4),
    "15:00-15:30" NUMERIC(19,4),
    "15:30-16:00" NUMERIC(19,4),
    "16:00-16:30" NUMERIC(19,4),
    "16:30-17:00" NUMERIC(19,4),
    "17:00-17:30" NUMERIC(19,4),
    "17:30-18:00" NUMERIC(19,4),
    "18:00-18:30" NUMERIC(19,4),
    "18:30-19:00" NUMERIC(19,4),
    "19:00-19:30" NUMERIC(19,4),
    "19:30-20:00" NUMERIC(19,4),
    "20:00-20:30" NUMERIC(19,4),
    "20:30-21:00" NUMERIC(19,4),
    "21:00-21:30" NUMERIC(19,4),
    "21:30-22:00" NUMERIC(19,4),
    "22:00-22:30" NUMERIC(19,4),
    "22:30-23:00" NUMERIC(19,4),
    "23:00-23:30" NUMERIC(19,4),
    "23:30-00:00" NUMERIC(19,4),
    signal VARCHAR(10) NOT NULL,
    CONSTRAINT pk_pivotedgbpnetreturntodaysummary PRIMARY KEY (entry_price, signal)
);

-- Table: dbo.PivotedGbpNetReturnToday_10mins_Columnar
CREATE TABLE IF NOT EXISTS pivotedgbpnetreturntoday_10mins_columnar (
    entry_price NUMERIC(18,6) NOT NULL,
    signal VARCHAR(10) NOT NULL,
    time_band CHAR(11) NOT NULL,
    avg_net_return NUMERIC(18,9) NOT NULL,
    trade_date DATE,
    CONSTRAINT pk_pivotedgbpnetreturntoday_10mins_columnar PRIMARY KEY (entry_price, signal, time_band)
);

-- Table: dbo.PivotedGbpNetReturnToday_10mins_Columnar_arc
CREATE TABLE IF NOT EXISTS pivotedgbpnetreturntoday_10mins_columnar_arc (
    entry_price NUMERIC(18,6) NOT NULL,
    signal VARCHAR(10) NOT NULL,
    time_band CHAR(11) NOT NULL,
    avg_net_return NUMERIC(18,9) NOT NULL,
    trade_date DATE
);

-- Table: dbo.ProductTradeSummary
CREATE TABLE IF NOT EXISTS producttradesummary (
    current_datetime TIMESTAMP WITHOUT TIME ZONE,
    product VARCHAR(50),
    buy_count INTEGER,
    sell_count INTEGER,
    bid NUMERIC(18,4),
    ask NUMERIC(18,4)
);

-- Table: dbo.TradeSnapshotLog
CREATE TABLE IF NOT EXISTS tradesnapshotlog (
    log_id BIGINT GENERATED ALWAYS AS IDENTITY NOT NULL,
    snapshottimestamp TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    product VARCHAR(64) NOT NULL,
    positivebuyopen INTEGER,
    positivesellopen INTEGER,
    positivesellopen_val NUMERIC(18,4),
    blocklatestprice NUMERIC(18,4),
    buysellindex NUMERIC(18,4),
    tradezone VARCHAR(32),
    tradepoint VARCHAR(64),
    current_datetime TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    buy_count INTEGER,
    sell_count INTEGER,
    buy_sell_diff INTEGER,
    bid NUMERIC(18,4),
    ask NUMERIC(18,4),
    loggedat TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    blocktimestamp TIMESTAMP WITHOUT TIME ZONE,
    CONSTRAINT pk__tradesna__9e2397e04a815db3 PRIMARY KEY (log_id)
);

-- Table: dbo.TradeSnapshotLog_arc
CREATE TABLE IF NOT EXISTS tradesnapshotlog_arc (
    snapshottimestamp TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    product VARCHAR(64) NOT NULL,
    positivebuyopen INTEGER,
    positivesellopen INTEGER,
    positivesellopen_val NUMERIC(18,4),
    blocklatestprice NUMERIC(18,4),
    buysellindex NUMERIC(18,4),
    tradezone VARCHAR(64),
    tradepoint VARCHAR(64),
    current_datetime TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    buy_count INTEGER,
    sell_count INTEGER,
    buy_sell_diff INTEGER,
    bid NUMERIC(18,4),
    ask NUMERIC(18,4),
    loggedat TIMESTAMP WITHOUT TIME ZONE NOT NULL
);

-- Table: dbo.TradeSummaryLog
CREATE TABLE IF NOT EXISTS tradesummarylog (
    logid INTEGER GENERATED ALWAYS AS IDENTITY NOT NULL,
    currentdatetime TIMESTAMP WITHOUT TIME ZONE,
    signal VARCHAR(50),
    opened INTEGER,
    closed INTEGER,
    positive INTEGER,
    age_label VARCHAR(10),
    current_prices TEXT,
    positive_open INTEGER,
    product VARCHAR(50),
    CONSTRAINT pk__tradesum__5e5499a8e929922c PRIMARY KEY (logid)
);

-- Table: dbo.TradeSummaryLog_arc
CREATE TABLE IF NOT EXISTS tradesummarylog_arc (
    logid INTEGER GENERATED ALWAYS AS IDENTITY NOT NULL,
    currentdatetime TIMESTAMP WITHOUT TIME ZONE,
    signal VARCHAR(50),
    opened INTEGER,
    closed INTEGER,
    positive INTEGER,
    age_label VARCHAR(10),
    current_prices TEXT,
    positive_open INTEGER,
    product VARCHAR(50),
    CONSTRAINT pk__tradesum__5e5499a853ef563b PRIMARY KEY (logid)
);

-- Table: dbo._700_return_type
CREATE TABLE IF NOT EXISTS _700_return_type (
    guid UUID NOT NULL,
    return_type CHAR(3) NOT NULL,
    created_utc TIMESTAMP WITHOUT TIME ZONE DEFAULT TIMEZONE('utc', CURRENT_TIMESTAMP) NOT NULL,
    CONSTRAINT pk___700_ret__497f6cb436456e17 PRIMARY KEY (guid)
);

-- Table: dbo._auto_newtrade_on_close_state
CREATE TABLE IF NOT EXISTS _auto_newtrade_on_close_state (
    id INTEGER NOT NULL,
    last_processed_close TIMESTAMP WITHOUT TIME ZONE,
    prev_recent_signal VARCHAR(10),
    CONSTRAINT pk__auto_state PRIMARY KEY (id)
);

-- Table: dbo.alt_net_group
CREATE TABLE IF NOT EXISTS alt_net_group (
    alt_net_group_id INTEGER GENERATED ALWAYS AS IDENTITY NOT NULL,
    update_time TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    product VARCHAR(50) NOT NULL,
    model VARCHAR(50) NOT NULL,
    signal VARCHAR(10) NOT NULL,
    linked INTEGER NOT NULL,
    net_return NUMERIC(18,5),
    alt_net_return NUMERIC(18,5),
    target_profit NUMERIC(18,5),
    target_loss NUMERIC(18,5),
    pos_net_return INTEGER,
    pos_alt_net_return INTEGER,
    percent_profit_target NUMERIC(18,5),
    percent_loss_target NUMERIC(18,5),
    latest_price NUMERIC(18,5),
    buy_count INTEGER,
    sell_count INTEGER,
    diff_count INTEGER,
    CONSTRAINT pk__alt_net___a68fb0eb5de33fe7 PRIMARY KEY (alt_net_group_id)
);

-- Table: dbo.auto_deactivate_flat_children_run_log
CREATE TABLE IF NOT EXISTS auto_deactivate_flat_children_run_log (
    run_id BIGINT GENERATED ALWAYS AS IDENTITY NOT NULL,
    started_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    completed_at TIMESTAMP WITHOUT TIME ZONE,
    status VARCHAR(16) NOT NULL,
    models_deactivated INTEGER,
    error_message VARCHAR(4000),
    CONSTRAINT pk__auto_dea__7d3d901b0c743b34 PRIMARY KEY (run_id)
);

-- Table: dbo.bcp_export_log
CREATE TABLE IF NOT EXISTS bcp_export_log (
    log_id INTEGER GENERATED ALWAYS AS IDENTITY NOT NULL,
    log_time TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    guid UUID,
    bcp_command TEXT,
    output_line VARCHAR(4000),
    CONSTRAINT pk__bcp_expo__9e2397e013a4d21d PRIMARY KEY (log_id)
);

-- Table: dbo.breakout_debug_ctx
CREATE TABLE IF NOT EXISTS breakout_debug_ctx (
    snapshot_id INTEGER GENERATED ALWAYS AS IDENTITY NOT NULL,
    logged_at TIMESTAMP WITHOUT TIME ZONE DEFAULT TIMEZONE('utc', CURRENT_TIMESTAMP) NOT NULL,
    batch_id UUID NOT NULL,
    stage VARCHAR(32) NOT NULL,
    product VARCHAR(50),
    model VARCHAR(128),
    max_prev_entry DOUBLE PRECISION,
    min_prev_entry DOUBLE PRECISION,
    ask_price DOUBLE PRECISION,
    bid_price DOUBLE PRECISION,
    signal VARCHAR(4),
    entry_price DOUBLE PRECISION,
    CONSTRAINT pk__breakout__c27cfbf7a0b3ebd9 PRIMARY KEY (snapshot_id)
);

-- Table: dbo.combined_trades_closed
CREATE TABLE IF NOT EXISTS combined_trades_closed (
    guid VARCHAR(50) NOT NULL,
    model TEXT NOT NULL,
    product VARCHAR(50),
    product_type VARCHAR(50),
    created TIMESTAMP WITHOUT TIME ZONE,
    last_update TIMESTAMP WITHOUT TIME ZONE,
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
    rl_check DOUBLE PRECISION,
    percent_profit DOUBLE PRECISION,
    percent_loss DOUBLE PRECISION,
    buy_count DOUBLE PRECISION,
    sell_count DOUBLE PRECISION,
    linked SMALLINT,
    int_profit DOUBLE PRECISION,
    int_profit_time TIMESTAMP WITHOUT TIME ZONE,
    close_type VARCHAR(50),
    min_net_return NUMERIC(18,8),
    min_net_return_time TIMESTAMP WITHOUT TIME ZONE,
    max_net_return NUMERIC(18,8),
    max_net_return_time TIMESTAMP WITHOUT TIME ZONE,
    trade_reason VARCHAR(200),
    flip_trade BOOLEAN,
    model_ix VARCHAR(200),
    g_close_time TIMESTAMP WITHOUT TIME ZONE,
    g_net_return DOUBLE PRECISION,
    g_alt_net_return DOUBLE PRECISION,
    bc_op INTEGER,
    sc_op INTEGER,
    strategy_name VARCHAR(100),
    CONSTRAINT pk_combined_trades_closed_new PRIMARY KEY (guid)
);

-- Table: dbo.combined_trades_closed_arc
CREATE TABLE IF NOT EXISTS combined_trades_closed_arc (
    guid VARCHAR(50),
    model TEXT NOT NULL,
    product VARCHAR(50),
    product_type VARCHAR(50),
    created TIMESTAMP WITHOUT TIME ZONE,
    last_update TIMESTAMP WITHOUT TIME ZONE,
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
    rl_check DOUBLE PRECISION,
    percent_profit DOUBLE PRECISION,
    percent_loss DOUBLE PRECISION,
    buy_count DOUBLE PRECISION,
    sell_count DOUBLE PRECISION,
    linked SMALLINT,
    int_profit DOUBLE PRECISION,
    int_profit_time TIMESTAMP WITHOUT TIME ZONE,
    close_type VARCHAR(50),
    min_net_return NUMERIC(18,8),
    min_net_return_time TIMESTAMP WITHOUT TIME ZONE,
    max_net_return NUMERIC(18,8),
    max_net_return_time TIMESTAMP WITHOUT TIME ZONE,
    trade_reason VARCHAR(200),
    flip_trade BOOLEAN
);

-- Table: dbo.combined_trades_open
CREATE TABLE IF NOT EXISTS combined_trades_open (
    guid VARCHAR(50),
    model VARCHAR(64) NOT NULL,
    product VARCHAR(50),
    product_type VARCHAR(50),
    created TIMESTAMP WITHOUT TIME ZONE,
    last_update TIMESTAMP WITHOUT TIME ZONE,
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
    rl_check VARCHAR(50),
    percent_profit DOUBLE PRECISION,
    percent_loss DOUBLE PRECISION,
    buy_count DOUBLE PRECISION,
    sell_count DOUBLE PRECISION,
    linked SMALLINT,
    int_profit DOUBLE PRECISION,
    int_profit_time TIMESTAMP WITHOUT TIME ZONE,
    trade_quantity BIGINT,
    min_net_return NUMERIC(18,8),
    min_net_return_time TIMESTAMP WITHOUT TIME ZONE,
    max_net_return NUMERIC(18,8),
    max_net_return_time TIMESTAMP WITHOUT TIME ZONE,
    flip_trade SMALLINT,
    trade_reason VARCHAR(50),
    g_close_time TIMESTAMP WITHOUT TIME ZONE,
    g_net_return DOUBLE PRECISION,
    g_alt_net_return DOUBLE PRECISION,
    buy_closed_count INTEGER,
    sell_closed_count INTEGER,
    strategy_name VARCHAR(100)
);

-- Table: dbo.combined_trades_open_snapshot
CREATE TABLE IF NOT EXISTS combined_trades_open_snapshot (
    guid VARCHAR(50),
    model VARCHAR(64) NOT NULL,
    product VARCHAR(50),
    product_type VARCHAR(50),
    created TIMESTAMP WITHOUT TIME ZONE,
    last_update TIMESTAMP WITHOUT TIME ZONE,
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
    rl_check VARCHAR(50),
    percent_profit DOUBLE PRECISION,
    percent_loss DOUBLE PRECISION,
    buy_count DOUBLE PRECISION,
    sell_count DOUBLE PRECISION,
    linked SMALLINT,
    int_profit DOUBLE PRECISION,
    int_profit_time TIMESTAMP WITHOUT TIME ZONE,
    trade_quantity BIGINT,
    min_net_return NUMERIC(18,8),
    min_net_return_time TIMESTAMP WITHOUT TIME ZONE,
    max_net_return NUMERIC(18,8),
    max_net_return_time TIMESTAMP WITHOUT TIME ZONE,
    trade_reason VARCHAR(50),
    flip_trade SMALLINT,
    zone_name VARCHAR(50),
    snapshottime TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Table: dbo.config
CREATE TABLE IF NOT EXISTS config (
    config_name VARCHAR(100) NOT NULL,
    config_value TEXT NOT NULL,
    config_value_unit VARCHAR(50),
    CONSTRAINT pk_configure_config_name PRIMARY KEY (config_name)
);

-- Table: dbo.crypto_quotes
CREATE TABLE IF NOT EXISTS crypto_quotes (
    id INTEGER GENERATED ALWAYS AS IDENTITY NOT NULL,
    timestamp TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    code VARCHAR(10) NOT NULL,
    type CHAR(1) DEFAULT 'C' NOT NULL,
    bid NUMERIC(18,8) NOT NULL,
    ask NUMERIC(18,8) NOT NULL,
    volume NUMERIC(18,4),
    provider VARCHAR(20),
    CONSTRAINT pk__crypto_q__3213e83f09e25262 PRIMARY KEY (id)
);

-- Table: dbo.dna_pnl_stream_cache
CREATE TABLE IF NOT EXISTS dna_pnl_stream_cache (
    id INTEGER GENERATED ALWAYS AS IDENTITY NOT NULL,
    model VARCHAR(100) NOT NULL,
    product VARCHAR(50),
    trade_date DATE NOT NULL,
    created TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    signal VARCHAR(10),
    net_return_sum DOUBLE PRECISION,
    alt_net_return_sum DOUBLE PRECISION,
    buy_net_return_sum DOUBLE PRECISION,
    sell_net_return_sum DOUBLE PRECISION,
    trade_count INTEGER,
    net_return DOUBLE PRECISION,
    alt_net_return DOUBLE PRECISION,
    g_close_time TIMESTAMP WITHOUT TIME ZONE,
    CONSTRAINT pk__dna_pnl___3213e83f7fd04797 PRIMARY KEY (id)
);

-- Table: dbo.ep051_directory_daily_summary
CREATE TABLE IF NOT EXISTS ep051_directory_daily_summary (
    trade_date DATE NOT NULL,
    strategy_id VARCHAR(20) NOT NULL,
    signal_group VARCHAR(4) NOT NULL,
    descriptive_name VARCHAR(100),
    product VARCHAR(50),
    total_trades INTEGER DEFAULT 0 NOT NULL,
    wins INTEGER DEFAULT 0 NOT NULL,
    losses INTEGER DEFAULT 0 NOT NULL,
    breakevens INTEGER DEFAULT 0 NOT NULL,
    total_net_return DOUBLE PRECISION DEFAULT 0 NOT NULL,
    gross_profit DOUBLE PRECISION DEFAULT 0 NOT NULL,
    gross_loss DOUBLE PRECISION DEFAULT 0 NOT NULL,
    evidence_start TIMESTAMP WITHOUT TIME ZONE,
    evidence_end TIMESTAMP WITHOUT TIME ZONE,
    CONSTRAINT pk_ep051_directory_daily_summary PRIMARY KEY (trade_date, strategy_id, signal_group)
);

-- Table: dbo.ep051_export_cache_run_log
CREATE TABLE IF NOT EXISTS ep051_export_cache_run_log (
    run_id BIGINT GENERATED ALWAYS AS IDENTITY NOT NULL,
    started_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    completed_at TIMESTAMP WITHOUT TIME ZONE,
    strategy_rows INTEGER,
    equity_curve_rows INTEGER,
    status VARCHAR(20) DEFAULT 'running' NOT NULL,
    error_message VARCHAR(4000),
    CONSTRAINT pk__ep051_ex__7d3d901b28299eef PRIMARY KEY (run_id)
);

-- Table: dbo.ep051_export_equity_curve
CREATE TABLE IF NOT EXISTS ep051_export_equity_curve (
    strategy_id VARCHAR(64) NOT NULL,
    trade_number INTEGER NOT NULL,
    opened_at TIMESTAMP WITHOUT TIME ZONE,
    closed_at TIMESTAMP WITHOUT TIME ZONE,
    net_return DOUBLE PRECISION NOT NULL,
    equity DOUBLE PRECISION NOT NULL,
    drawdown DOUBLE PRECISION NOT NULL,
    refreshed_at TIMESTAMP WITHOUT TIME ZONE DEFAULT TIMEZONE('utc', CURRENT_TIMESTAMP) NOT NULL,
    CONSTRAINT pk_ep051_export_equity_curve PRIMARY KEY (strategy_id, trade_number)
);

-- Table: dbo.ep051_export_strategy_summary
CREATE TABLE IF NOT EXISTS ep051_export_strategy_summary (
    strategy_id VARCHAR(64) NOT NULL,
    descriptive_name VARCHAR(200),
    product_name VARCHAR(400),
    total_trades BIGINT NOT NULL,
    wins BIGINT NOT NULL,
    losses BIGINT NOT NULL,
    breakevens BIGINT NOT NULL,
    total_net_return NUMERIC(28,8) NOT NULL,
    win_rate NUMERIC(18,10),
    profit_factor NUMERIC(18,10),
    max_drawdown_money NUMERIC(28,8),
    evidence_start TIMESTAMP WITHOUT TIME ZONE,
    evidence_end TIMESTAMP WITHOUT TIME ZONE,
    refreshed_at TIMESTAMP WITHOUT TIME ZONE DEFAULT TIMEZONE('utc', CURRENT_TIMESTAMP) NOT NULL,
    CONSTRAINT pk__ep051_ex__d30e3807a5e7d632 PRIMARY KEY (strategy_id)
);

-- Table: dbo.ep051_rank_capture_run_log
CREATE TABLE IF NOT EXISTS ep051_rank_capture_run_log (
    run_id BIGINT GENERATED ALWAYS AS IDENTITY NOT NULL,
    started_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    completed_at TIMESTAMP WITHOUT TIME ZONE,
    strategy_rows INTEGER,
    status VARCHAR(20) DEFAULT 'running' NOT NULL,
    error_message VARCHAR(4000),
    CONSTRAINT pk__ep051_ra__7d3d901ba11b37bc PRIMARY KEY (run_id)
);

-- Table: dbo.ep051_rank_capture_watermark
CREATE TABLE IF NOT EXISTS ep051_rank_capture_watermark (
    id INTEGER NOT NULL,
    for_date DATE NOT NULL,
    last_closed_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    last_guid VARCHAR(64) NOT NULL,
    CONSTRAINT pk__ep051_ra__3213e83f8bfccb6e PRIMARY KEY (id)
);

-- Table: dbo.ep051_strategy_rank_history
CREATE TABLE IF NOT EXISTS ep051_strategy_rank_history (
    captured_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    strategy_id VARCHAR(64) NOT NULL,
    total_net_return DOUBLE PRECISION NOT NULL,
    total_trades INTEGER NOT NULL,
    rank_position INTEGER NOT NULL,
    basis VARCHAR(32),
    CONSTRAINT pk_ep051_strategy_rank_history PRIMARY KEY (captured_at, strategy_id)
);

-- Table: dbo.ep051_strategy_rank_running_totals
CREATE TABLE IF NOT EXISTS ep051_strategy_rank_running_totals (
    for_date DATE NOT NULL,
    strategy_id VARCHAR(64) NOT NULL,
    total_net_return DOUBLE PRECISION NOT NULL,
    total_trades INTEGER NOT NULL,
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT TIMEZONE('utc', CURRENT_TIMESTAMP) NOT NULL,
    CONSTRAINT pk_ep051_strategy_rank_running_totals PRIMARY KEY (for_date, strategy_id)
);

-- Table: dbo.ep052_dna_matrix_run_log
CREATE TABLE IF NOT EXISTS ep052_dna_matrix_run_log (
    run_id BIGINT GENERATED ALWAYS AS IDENTITY NOT NULL,
    started_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    completed_at TIMESTAMP WITHOUT TIME ZONE,
    status VARCHAR(16) NOT NULL,
    models_created INTEGER,
    models_reactivated INTEGER,
    models_deactivated INTEGER,
    error_message VARCHAR(4000),
    CONSTRAINT pk__ep052_dn__7d3d901baba4d440 PRIMARY KEY (run_id)
);

-- Table: dbo.forex_price
CREATE TABLE IF NOT EXISTS forex_price (
    current_datetime TIMESTAMP WITHOUT TIME ZONE,
    current_prices TEXT
);

-- Table: dbo.forex_price_history
CREATE TABLE IF NOT EXISTS forex_price_history (
    current_datetime TIMESTAMP WITHOUT TIME ZONE,
    current_prices TEXT
);

-- Table: dbo.forex_products
CREATE TABLE IF NOT EXISTS forex_products (
    id INTEGER GENERATED ALWAYS AS IDENTITY NOT NULL,
    symbol VARCHAR(10) NOT NULL,
    currency VARCHAR(10) NOT NULL,
    sectype VARCHAR(10) DEFAULT 'CASH' NOT NULL,
    exchange VARCHAR(20) DEFAULT 'IDEALPRO' NOT NULL,
    system_product VARCHAR(50),
    CONSTRAINT pk__forex_pr__3213e83f169ae371 PRIMARY KEY (id)
);

-- Table: dbo.futures_quotes
CREATE TABLE IF NOT EXISTS futures_quotes (
    id INTEGER GENERATED ALWAYS AS IDENTITY NOT NULL,
    timestamp TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    code VARCHAR(10) NOT NULL,
    type CHAR(1) DEFAULT 'X' NOT NULL,
    bid NUMERIC(18,4) NOT NULL,
    ask NUMERIC(18,4) NOT NULL,
    volume NUMERIC(18,4),
    provider VARCHAR(20),
    CONSTRAINT pk__futures___3213e83f13e2deb3 PRIMARY KEY (id)
);

-- Table: dbo.fx_quotes
CREATE TABLE IF NOT EXISTS fx_quotes (
    id INTEGER GENERATED ALWAYS AS IDENTITY NOT NULL,
    timestamp TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    code VARCHAR(8) NOT NULL,
    type CHAR(1) NOT NULL,
    bid NUMERIC(18,6) NOT NULL,
    ask NUMERIC(18,6) NOT NULL,
    CONSTRAINT pk__fx_quote__3213e83f49cec6a7 PRIMARY KEY (id)
);

-- Table: dbo.fx_quotes_history
CREATE TABLE IF NOT EXISTS fx_quotes_history (
    id INTEGER GENERATED ALWAYS AS IDENTITY NOT NULL,
    timestamp TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    code VARCHAR(8) NOT NULL,
    type CHAR(1) NOT NULL,
    bid NUMERIC(18,6) NOT NULL,
    ask NUMERIC(18,6) NOT NULL,
    CONSTRAINT pk__fx_quote__3213e83fe03fc35d PRIMARY KEY (id)
);

-- Table: dbo.hrly_signal_perf_snapshots
CREATE TABLE IF NOT EXISTS hrly_signal_perf_snapshots (
    product VARCHAR(50),
    hourbucket TIMESTAMP WITHOUT TIME ZONE,
    buy_alt_net_return DOUBLE PRECISION,
    sell_alt_net_return DOUBLE PRECISION,
    sell INTEGER,
    buy INTEGER,
    update_time TIMESTAMP WITHOUT TIME ZONE
);

-- Table: dbo.myNewCombinedTable
CREATE TABLE IF NOT EXISTS mynewcombinedtable (
    product VARCHAR(50),
    signal VARCHAR(50),
    trade_date VARCHAR(10),
    time_block VARCHAR(19),
    total_trades INTEGER,
    trades_in_profit INTEGER,
    latest_price DOUBLE PRECISION,
    trade_status VARCHAR(6) NOT NULL
);

-- Table: dbo.price_crypto
CREATE TABLE IF NOT EXISTS price_crypto (
    current_datetime TIMESTAMP WITHOUT TIME ZONE,
    current_prices TEXT
);

-- Table: dbo.proc_gate
CREATE TABLE IF NOT EXISTS proc_gate (
    proc_name VARCHAR(128) NOT NULL,
    last_run_bucket TIMESTAMP WITHOUT TIME ZONE,
    CONSTRAINT pk__proc_gat__2d3358c4484ce83e PRIMARY KEY (proc_name)
);

-- Table: dbo.proc_run_log
CREATE TABLE IF NOT EXISTS proc_run_log (
    run_id BIGINT GENERATED ALWAYS AS IDENTITY NOT NULL,
    sp_name VARCHAR(128) NOT NULL,
    start_ts TIMESTAMP WITHOUT TIME ZONE DEFAULT TIMEZONE('utc', CURRENT_TIMESTAMP) NOT NULL,
    end_ts TIMESTAMP WITHOUT TIME ZONE,
    rows_open INTEGER,
    rows_to_close INTEGER,
    rows_closed INTEGER,
    message VARCHAR(4000),
    CONSTRAINT pk__proc_run__7d3d901bbbde0a26 PRIMARY KEY (run_id)
);

-- Table: dbo.proc_time_log
CREATE TABLE IF NOT EXISTS proc_time_log (
    id BIGINT GENERATED ALWAYS AS IDENTITY NOT NULL,
    proc_name VARCHAR(128) NOT NULL,
    step VARCHAR(64) NOT NULL,
    product VARCHAR(50),
    ts TIMESTAMP WITHOUT TIME ZONE DEFAULT TIMEZONE('utc', CURRENT_TIMESTAMP) NOT NULL,
    CONSTRAINT pk__proc_tim__3213e83f9f51d657 PRIMARY KEY (id)
);

-- Table: dbo.product_forex
CREATE TABLE IF NOT EXISTS product_forex (
    product VARCHAR(50) NOT NULL,
    min_val SMALLINT NOT NULL,
    contract_size INTEGER NOT NULL,
    commission SMALLINT NOT NULL,
    model TEXT NOT NULL,
    target_profit SMALLINT NOT NULL,
    target_loss SMALLINT NOT NULL,
    trade_qty BIGINT NOT NULL,
    product_type VARCHAR(50) NOT NULL,
    tradeable SMALLINT NOT NULL,
    trade_freq SMALLINT NOT NULL,
    rl_action SMALLINT NOT NULL,
    add_to_blog BOOLEAN NOT NULL,
    tradeable_daily BOOLEAN,
    mapto_tradezone BOOLEAN,
    full_target SMALLINT,
    use_trade_count BOOLEAN DEFAULT FALSE NOT NULL,
    flip_trade BOOLEAN,
    use_target_exit_only BOOLEAN,
    multi_close_option VARCHAR(50) DEFAULT 'none' NOT NULL,
    dna_array VARCHAR(200),
    dna_json TEXT,
    strategy_name VARCHAR(100),
    strategy_params VARCHAR(100)
);

-- Table: dbo.product_signal_snapshot
CREATE TABLE IF NOT EXISTS product_signal_snapshot (
    snapshotid INTEGER GENERATED ALWAYS AS IDENTITY NOT NULL,
    snapshottimestamp TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    product VARCHAR(100) NOT NULL,
    blockstarttime TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    blockendtime TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    blocklatestprice NUMERIC(18,5),
    totalbuyopen INTEGER NOT NULL,
    positivebuyopen INTEGER NOT NULL,
    positivevaluebuyopen NUMERIC(19,6) NOT NULL,
    avgpricebuyopen NUMERIC(18,5),
    totalsellopen INTEGER NOT NULL,
    positivesellopen INTEGER NOT NULL,
    positivevaluesellopen NUMERIC(19,6) NOT NULL,
    avgpricesellopen NUMERIC(18,5),
    totalbuyclosed INTEGER NOT NULL,
    positivebuyclosed INTEGER NOT NULL,
    positivevaluebuyclosed NUMERIC(19,6) NOT NULL,
    avgpricebuyclosed NUMERIC(18,5),
    totalsellclosed INTEGER NOT NULL,
    positivesellclosed INTEGER NOT NULL,
    positivevaluesellclosed NUMERIC(19,6) NOT NULL,
    avgpricesellclosed NUMERIC(18,5),
    CONSTRAINT pk__product___664f570bbe28669b PRIMARY KEY (snapshotid)
);

-- Table: dbo.sp_001_last_processed_snapshot
CREATE TABLE IF NOT EXISTS sp_001_last_processed_snapshot (
    product VARCHAR(50) NOT NULL,
    last_processed_time TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    CONSTRAINT pk_sp_001_last_processed_snapshot PRIMARY KEY (product)
);

-- Table: dbo.stale_open_cleanup_run_log
CREATE TABLE IF NOT EXISTS stale_open_cleanup_run_log (
    run_id BIGINT GENERATED ALWAYS AS IDENTITY NOT NULL,
    started_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    completed_at TIMESTAMP WITHOUT TIME ZONE,
    status VARCHAR(16) NOT NULL,
    rows_deleted INTEGER,
    error_message VARCHAR(4000),
    CONSTRAINT pk__stale_op__7d3d901b2bce5dd9 PRIMARY KEY (run_id)
);

-- Table: dbo.stg_selection
CREATE TABLE IF NOT EXISTS stg_selection (
    batch_id UUID NOT NULL,
    status VARCHAR(20) NOT NULL,
    signal VARCHAR(10) NOT NULL,
    marker_ts TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    selected_guid UUID,
    selected_created TIMESTAMP WITHOUT TIME ZONE,
    selected_last_update TIMESTAMP WITHOUT TIME ZONE,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT pk__stg_sele__dbfc043150191593 PRIMARY KEY (batch_id)
);

-- Table: dbo.stg_to_close
CREATE TABLE IF NOT EXISTS stg_to_close (
    batch_id UUID NOT NULL,
    guid UUID NOT NULL,
    reason VARCHAR(50) DEFAULT 'OpposingWhileArmed' NOT NULL,
    CONSTRAINT pk__stg_to_c__8f6bf2face3cf55c PRIMARY KEY (batch_id, guid)
);

-- Table: dbo.strategy_side_current
CREATE TABLE IF NOT EXISTS strategy_side_current (
    product VARCHAR(50) NOT NULL,
    model VARCHAR(128) NOT NULL,
    side VARCHAR(8),
    decided_at TIMESTAMP WITHOUT TIME ZONE DEFAULT TIMEZONE('utc', CURRENT_TIMESTAMP) NOT NULL,
    CONSTRAINT pk_strategy_side_current PRIMARY KEY (product, model)
);

-- Table: dbo.sysdiagrams
CREATE TABLE IF NOT EXISTS sysdiagrams (
    name VARCHAR(128) NOT NULL,
    principal_id INTEGER NOT NULL,
    diagram_id INTEGER GENERATED ALWAYS AS IDENTITY NOT NULL,
    version INTEGER,
    definition BYTEA,
    CONSTRAINT pk__sysdiagr__c2b05b6179d67780 PRIMARY KEY (diagram_id),
    CONSTRAINT uk_principal_name UNIQUE (principal_id, name)
);

-- Table: dbo.tbl_105_trade_lifecycle_snapshots
CREATE TABLE IF NOT EXISTS tbl_105_trade_lifecycle_snapshots (
    id INTEGER GENERATED ALWAYS AS IDENTITY NOT NULL,
    session_id VARCHAR(36) NOT NULL,
    app_trade_id BIGINT NOT NULL,
    guid VARCHAR(36) NOT NULL,
    timestamp TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    event_type VARCHAR(10) NOT NULL,
    trade_type VARCHAR(4) NOT NULL,
    product VARCHAR(50) NOT NULL,
    entry_price NUMERIC(18,5) NOT NULL,
    quantity NUMERIC(18,5) NOT NULL,
    commission NUMERIC(18,5) NOT NULL,
    current_price NUMERIC(18,5),
    current_pnl NUMERIC(18,5),
    alt_pnl NUMERIC(18,5),
    is_active BOOLEAN NOT NULL,
    trailing_stop_active BOOLEAN NOT NULL,
    current_trailing_stop_level NUMERIC(18,5),
    peak_net_return_since_trailing_active NUMERIC(18,5),
    is_flipped CHAR(1) NOT NULL,
    close_reason VARCHAR(255),
    close_price NUMERIC(18,5),
    strategy_config TEXT,
    trade_signal VARCHAR(8),
    CONSTRAINT pk__tbl_105___3213e83f4c433a33 PRIMARY KEY (id)
);

-- Table: dbo.tbl_700_bucket_boundaries
CREATE TABLE IF NOT EXISTS tbl_700_bucket_boundaries (
    product VARCHAR(50) NOT NULL,
    bucket_index INTEGER NOT NULL,
    cut_value NUMERIC(18,10) NOT NULL,
    computed_at TIMESTAMP WITHOUT TIME ZONE NOT NULL
);

-- Table: dbo.tbl_700_etl_state
CREATE TABLE IF NOT EXISTS tbl_700_etl_state (
    source_name VARCHAR(128) NOT NULL,
    last_close_ts TIMESTAMP WITHOUT TIME ZONE,
    extra_dt TIMESTAMP WITHOUT TIME ZONE,
    CONSTRAINT pk__tbl_700___52379dc01015f6cd PRIMARY KEY (source_name)
);

-- Table: dbo.tbl_700_open_trades_log
CREATE TABLE IF NOT EXISTS tbl_700_open_trades_log (
    guid UUID NOT NULL,
    product VARCHAR(50) NOT NULL,
    signal VARCHAR(10) NOT NULL,
    created_ts TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    entry_price NUMERIC(18,10) NOT NULL,
    entry_bucket INTEGER NOT NULL,
    time_bin INTEGER NOT NULL,
    session SMALLINT,
    decision VARCHAR(32) NOT NULL,
    size NUMERIC(18,4),
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT TIMEZONE('utc', CURRENT_TIMESTAMP) NOT NULL,
    snapshot_prior_count INTEGER,
    snapshot_prior_hit_rate NUMERIC(9,6),
    snapshot_prior_alt_mean NUMERIC(19,4),
    CONSTRAINT pk__tbl_700___497f6cb4bd142b79 PRIMARY KEY (guid)
);

-- Table: dbo.tbl_700_priors
CREATE TABLE IF NOT EXISTS tbl_700_priors (
    product VARCHAR(50) NOT NULL,
    signal VARCHAR(10) NOT NULL,
    entry_bucket INTEGER NOT NULL,
    time_bin INTEGER NOT NULL,
    session SMALLINT,
    session_key SMALLINT NOT NULL,
    prior_count INTEGER DEFAULT 0 NOT NULL,
    prior_win_sum INTEGER DEFAULT 0 NOT NULL,
    prior_alt_sum NUMERIC(19,4) DEFAULT 0 NOT NULL,
    model VARCHAR(50) DEFAULT N'UNKNOWN' NOT NULL,
    return_type VARCHAR(20) DEFAULT N'alt_net_return' NOT NULL,
    CONSTRAINT pk_tbl_700_priors PRIMARY KEY (product, signal, entry_bucket, time_bin, session_key)
);

-- Table: dbo.tbl_700_priors_7d_nomodel
CREATE TABLE IF NOT EXISTS tbl_700_priors_7d_nomodel (
    product VARCHAR(50) NOT NULL,
    signal VARCHAR(50) NOT NULL,
    entry_bucket INTEGER NOT NULL,
    time_bin INTEGER NOT NULL,
    return_type VARCHAR(20) NOT NULL,
    trade_count INTEGER NOT NULL,
    win_count INTEGER NOT NULL,
    loss_count INTEGER NOT NULL,
    return_sum DOUBLE PRECISION NOT NULL,
    avg_return DOUBLE PRECISION NOT NULL,
    hit_rate DOUBLE PRECISION NOT NULL,
    last_updated TIMESTAMP WITHOUT TIME ZONE DEFAULT TIMEZONE('utc', CURRENT_TIMESTAMP) NOT NULL,
    CONSTRAINT pk_tbl_700_priors_7d_nomodel PRIMARY KEY (product, signal, entry_bucket, time_bin, return_type)
);

-- Table: dbo.tbl_700_priors_v2
CREATE TABLE IF NOT EXISTS tbl_700_priors_v2 (
    model VARCHAR(50) NOT NULL,
    product VARCHAR(50) NOT NULL,
    signal VARCHAR(10) NOT NULL,
    entry_bucket INTEGER NOT NULL,
    time_bin INTEGER NOT NULL,
    return_type VARCHAR(20) NOT NULL,
    trade_count INTEGER NOT NULL,
    win_count INTEGER NOT NULL,
    loss_count INTEGER NOT NULL,
    return_sum DOUBLE PRECISION NOT NULL,
    avg_return DOUBLE PRECISION,
    hit_rate DOUBLE PRECISION,
    last_updated TIMESTAMP WITHOUT TIME ZONE DEFAULT TIMEZONE('utc', CURRENT_TIMESTAMP) NOT NULL,
    CONSTRAINT pk_tbl_700_priors_v2 PRIMARY KEY (model, product, signal, entry_bucket, time_bin, return_type)
);

-- Table: dbo.tbl_700_risk_state
CREATE TABLE IF NOT EXISTS tbl_700_risk_state (
    trade_date DATE NOT NULL,
    open_positions INTEGER DEFAULT 0 NOT NULL,
    realized_pnl NUMERIC(19,4) DEFAULT 0 NOT NULL,
    CONSTRAINT pk__tbl_700___cbe177c0f7b2a087 PRIMARY KEY (trade_date)
);

-- Table: dbo.tbl_701_topN_current
CREATE TABLE IF NOT EXISTS tbl_701_topn_current (
    asof_utc TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    product VARCHAR(50) NOT NULL,
    signal VARCHAR(50) NOT NULL,
    side CHAR(3) NOT NULL,
    model VARCHAR(50) NOT NULL,
    val NUMERIC(38,8) NOT NULL,
    pos INTEGER NOT NULL,
    CONSTRAINT ix_tbl_701_topn_current UNIQUE (asof_utc, product, signal, side, pos)
);

-- Table: dbo.tbl_800_hybrid_log
CREATE TABLE IF NOT EXISTS tbl_800_hybrid_log (
    event_id BIGINT GENERATED ALWAYS AS IDENTITY NOT NULL,
    event_type VARCHAR(32) NOT NULL,
    product VARCHAR(50) NOT NULL,
    model VARCHAR(64) NOT NULL,
    regime_state VARCHAR(32),
    fast_side VARCHAR(4),
    slow_side VARCHAR(4),
    metrics_id BIGINT,
    detail_payload TEXT,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT TIMEZONE('utc', CURRENT_TIMESTAMP) NOT NULL,
    CONSTRAINT pk_tbl_800_hybrid_log PRIMARY KEY (event_id)
);

-- Table: dbo.tbl_800_regime_history
CREATE TABLE IF NOT EXISTS tbl_800_regime_history (
    history_id BIGINT GENERATED ALWAYS AS IDENTITY NOT NULL,
    product VARCHAR(50) NOT NULL,
    model VARCHAR(64) NOT NULL,
    last_regime_state VARCHAR(32) NOT NULL,
    fast_side VARCHAR(4) DEFAULT 'NONE' NOT NULL,
    slow_side VARCHAR(4) DEFAULT 'NONE' NOT NULL,
    last_metrics_id BIGINT,
    transition_confirmed BOOLEAN DEFAULT FALSE NOT NULL,
    transition_started_at TIMESTAMP WITHOUT TIME ZONE,
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT TIMEZONE('utc', CURRENT_TIMESTAMP) NOT NULL,
    CONSTRAINT pk_tbl_800_regime_history PRIMARY KEY (history_id),
    CONSTRAINT uq_tbl_800_regime_history UNIQUE (product, model)
);

-- Table: dbo.tbl_800_regime_state
CREATE TABLE IF NOT EXISTS tbl_800_regime_state (
    regime_id BIGINT GENERATED ALWAYS AS IDENTITY NOT NULL,
    metrics_id BIGINT NOT NULL,
    product VARCHAR(50) NOT NULL,
    product_type VARCHAR(50),
    model VARCHAR(64) NOT NULL,
    regime_state VARCHAR(32) NOT NULL,
    fast_side VARCHAR(4) DEFAULT 'NONE' NOT NULL,
    slow_side VARCHAR(4) DEFAULT 'NONE' NOT NULL,
    dur_ratio NUMERIC(18,6),
    count_ratio NUMERIC(18,6),
    fast_real_pnl NUMERIC(19,4),
    slow_real_pnl NUMERIC(19,4),
    prev_regime_state VARCHAR(32),
    is_transition_confirmed BOOLEAN DEFAULT FALSE NOT NULL,
    evaluated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT TIMEZONE('utc', CURRENT_TIMESTAMP) NOT NULL,
    CONSTRAINT pk_tbl_800_regime_state PRIMARY KEY (regime_id)
);

-- Table: dbo.tbl_800_trade_metrics
CREATE TABLE IF NOT EXISTS tbl_800_trade_metrics (
    metrics_id BIGINT GENERATED ALWAYS AS IDENTITY NOT NULL,
    product VARCHAR(50) NOT NULL,
    product_type VARCHAR(50),
    model VARCHAR(64) NOT NULL,
    metrics_window_minutes SMALLINT NOT NULL,
    window_start TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    window_end TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    buy_trade_count INTEGER DEFAULT 0 NOT NULL,
    sell_trade_count INTEGER DEFAULT 0 NOT NULL,
    buy_avg_duration_minutes NUMERIC(18,4),
    sell_avg_duration_minutes NUMERIC(18,4),
    buy_real_pnl NUMERIC(19,4),
    sell_real_pnl NUMERIC(19,4),
    buy_ghost_count INTEGER DEFAULT 0 NOT NULL,
    sell_ghost_count INTEGER DEFAULT 0 NOT NULL,
    buy_ghost_ratio NUMERIC(9,6),
    sell_ghost_ratio NUMERIC(9,6),
    dur_ratio NUMERIC(18,6),
    count_ratio NUMERIC(18,6),
    fast_breakdown_count INTEGER DEFAULT 0 NOT NULL,
    created_utc TIMESTAMP WITHOUT TIME ZONE DEFAULT TIMEZONE('utc', CURRENT_TIMESTAMP) NOT NULL,
    CONSTRAINT pk_tbl_800_trade_metrics PRIMARY KEY (metrics_id)
);

-- Table: dbo.tbl_900_leadership_snapshots
CREATE TABLE IF NOT EXISTS tbl_900_leadership_snapshots (
    snapshot_id INTEGER GENERATED ALWAYS AS IDENTITY NOT NULL,
    snapshot_time TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    model VARCHAR(100),
    signal VARCHAR(10),
    latest_price DOUBLE PRECISION,
    net_return DOUBLE PRECISION,
    CONSTRAINT pk__tbl_900___c27cfbf78175d935 PRIMARY KEY (snapshot_id)
);

-- Table: dbo.tbl_CumulativeTradeProfit
CREATE TABLE IF NOT EXISTS tbl_cumulativetradeprofit (
    product VARCHAR(50),
    trade_date DATE,
    time_block INTEGER,
    "trade_in_profit (buy)" NUMERIC(18,2),
    "trade_in_profit (sell)" NUMERIC(18,2),
    avg_latest_price NUMERIC(18,2),
    "trade_in_profit_diff (buy-sell)" NUMERIC(18,2),
    cumulative_trade_in_profit_diff NUMERIC(18,2),
    calc_signal VARCHAR(10)
);

-- Table: dbo.tbl_ModelPerformanceLog
CREATE TABLE IF NOT EXISTS tbl_modelperformancelog (
    model TEXT NOT NULL,
    signal VARCHAR(50),
    product VARCHAR(50),
    last_update TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    total_trade_count INTEGER,
    total_return DOUBLE PRECISION,
    profitable_percent NUMERIC(26,12),
    avg_profitable_entry_price DOUBLE PRECISION,
    avg_profitable_latest_price DOUBLE PRECISION,
    fx_midprice NUMERIC(23,9)
);

-- Table: dbo.tbl_ProductSummaryData
CREATE TABLE IF NOT EXISTS tbl_productsummarydata (
    product VARCHAR(50),
    signal VARCHAR(50),
    trade_date VARCHAR(10),
    time_block VARCHAR(19),
    total_trades INTEGER,
    trades_in_profit INTEGER,
    latest_price DOUBLE PRECISION,
    trade_status VARCHAR(6) NOT NULL
);

-- Table: dbo.tbl_archive_dynamic_leadership
CREATE TABLE IF NOT EXISTS tbl_archive_dynamic_leadership (
    snapshot_time TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    model TEXT NOT NULL,
    product VARCHAR(50),
    signal VARCHAR(16) NOT NULL,
    latest_price DOUBLE PRECISION,
    alt_net_return_sum DOUBLE PRECISION
);

-- Table: dbo.tbl_changes
CREATE TABLE IF NOT EXISTS tbl_changes (
    change_date DATE,
    change_details TEXT,
    change_objects TEXT
);

-- Table: dbo.tbl_model_signal_net
CREATE TABLE IF NOT EXISTS tbl_model_signal_net (
    update_time TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    product VARCHAR(50) NOT NULL,
    model VARCHAR(50) NOT NULL,
    signal VARCHAR(50) NOT NULL,
    net_return_sum NUMERIC(38,8) NOT NULL,
    alt_net_return_sum NUMERIC(38,8) NOT NULL,
    CONSTRAINT pk_tbl_model_signal_net PRIMARY KEY (update_time, model, signal)
);

-- Table: dbo.tbl_model_signal_net_Xhr
CREATE TABLE IF NOT EXISTS tbl_model_signal_net_xhr (
    update_time TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    product VARCHAR(50) NOT NULL,
    model VARCHAR(50) NOT NULL,
    signal VARCHAR(50) NOT NULL,
    net_return_sum NUMERIC(38,8) NOT NULL,
    alt_net_return_sum NUMERIC(38,8) NOT NULL,
    CONSTRAINT pk_tbl_model_signal_net_xhr PRIMARY KEY (update_time, model, signal)
);

-- Table: dbo.tbl_model_signal_net_Xhr_arc
CREATE TABLE IF NOT EXISTS tbl_model_signal_net_xhr_arc (
    update_time TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    product VARCHAR(50) NOT NULL,
    model VARCHAR(50) NOT NULL,
    signal VARCHAR(50) NOT NULL,
    net_return_sum NUMERIC(38,8) NOT NULL,
    alt_net_return_sum NUMERIC(38,8) NOT NULL,
    CONSTRAINT pk_tbl_model_signal_net_xhr_arc PRIMARY KEY (update_time, model, signal)
);

-- Table: dbo.tbl_model_signal_net_arc
CREATE TABLE IF NOT EXISTS tbl_model_signal_net_arc (
    update_time TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    product VARCHAR(50) NOT NULL,
    model VARCHAR(50) NOT NULL,
    signal VARCHAR(50) NOT NULL,
    net_return_sum NUMERIC(38,8) NOT NULL,
    alt_net_return_sum NUMERIC(38,8) NOT NULL
);

-- Table: dbo.tbl_rt_trades
CREATE TABLE IF NOT EXISTS tbl_rt_trades (
    trade_id INTEGER GENERATED ALWAYS AS IDENTITY NOT NULL,
    trade_time TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    trade_guid UUID NOT NULL,
    trade_details VARCHAR(1000) NOT NULL,
    trade_status VARCHAR(50) NOT NULL,
    execution_status VARCHAR(50) NOT NULL,
    product_type VARCHAR(255),
    signal VARCHAR(255),
    product VARCHAR(255),
    trade_reason TEXT,
    flip_trade BOOLEAN,
    CONSTRAINT pk__tbl_rt_t__aaff5bf7735f1b19 PRIMARY KEY (trade_id)
);

-- Table: dbo.tbl_top_one
CREATE TABLE IF NOT EXISTS tbl_top_one (
    id INTEGER GENERATED ALWAYS AS IDENTITY NOT NULL,
    product VARCHAR(50),
    strategy_and_params VARCHAR(255),
    direction VARCHAR(10),
    total_net_return DOUBLE PRECISION,
    last_update TIMESTAMP WITHOUT TIME ZONE,
    CONSTRAINT pk__tbl_top___3213e83ff82f94d0 PRIMARY KEY (id)
);

-- Table: dbo.tbl_top_one_archive
CREATE TABLE IF NOT EXISTS tbl_top_one_archive (
    id INTEGER NOT NULL,
    product VARCHAR(50),
    strategy_and_params VARCHAR(255),
    direction VARCHAR(10),
    total_net_return DOUBLE PRECISION,
    last_update TIMESTAMP WITHOUT TIME ZONE,
    archive_timestamp TIMESTAMP WITHOUT TIME ZONE NOT NULL
);

-- Table: dbo.tbl_trade_link
CREATE TABLE IF NOT EXISTS tbl_trade_link (
    session_id VARCHAR(128) NOT NULL,
    message_id VARCHAR(128) NOT NULL,
    product VARCHAR(64) NOT NULL,
    action VARCHAR(16) NOT NULL,
    trade_quantity INTEGER NOT NULL,
    executed BOOLEAN DEFAULT FALSE NOT NULL,
    created TIMESTAMP WITHOUT TIME ZONE DEFAULT TIMEZONE('utc', CURRENT_TIMESTAMP) NOT NULL,
    guid UUID DEFAULT gen_random_uuid() NOT NULL,
    send_order BOOLEAN DEFAULT FALSE NOT NULL,
    session_config TEXT,
    CONSTRAINT pk_tbl_trade_link PRIMARY KEY (guid),
    CONSTRAINT uq_tbl_trade_link_msg UNIQUE (session_id, message_id)
);

-- Table: dbo.trade_bcsc_open_capture
CREATE TABLE IF NOT EXISTS trade_bcsc_open_capture (
    guid VARCHAR(50) NOT NULL,
    product VARCHAR(50),
    model VARCHAR(64),
    signal VARCHAR(16),
    trade_created TIMESTAMP WITHOUT TIME ZONE,
    bc_op INTEGER,
    sc_op INTEGER,
    captured_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT pk__trade_bc__497f6cb48f55917a PRIMARY KEY (guid)
);

-- Table: dbo.trade_close_audit
CREATE TABLE IF NOT EXISTS trade_close_audit (
    log_id BIGINT GENERATED ALWAYS AS IDENTITY NOT NULL,
    log_ts TIMESTAMP WITHOUT TIME ZONE DEFAULT TIMEZONE('utc', CURRENT_TIMESTAMP) NOT NULL,
    sp_name VARCHAR(128) NOT NULL,
    phase VARCHAR(40) NOT NULL,
    guid UUID,
    close_type VARCHAR(64),
    product VARCHAR(50),
    model VARCHAR(50),
    signal VARCHAR(10),
    tradeable INTEGER,
    use_target_exit_only BOOLEAN,
    mapto_tradezone BOOLEAN,
    multi_close_option VARCHAR(64),
    net_return NUMERIC(19,4),
    target_profit NUMERIC(19,4),
    target_loss NUMERIC(19,4),
    created TIMESTAMP WITHOUT TIME ZONE,
    last_update TIMESTAMP WITHOUT TIME ZONE,
    age_seconds INTEGER,
    curr_tradezone VARCHAR(50),
    curr_bsi DOUBLE PRECISION,
    prev_bsi DOUBLE PRECISION,
    flags VARCHAR(400),
    CONSTRAINT pk__trade_cl__9e2397e0e7993275 PRIMARY KEY (log_id)
);

-- Table: dbo.trade_close_candidates_log
CREATE TABLE IF NOT EXISTS trade_close_candidates_log (
    run_id BIGINT,
    guid UUID,
    close_type VARCHAR(64),
    logged_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Table: dbo.trade_lifecycle_snapshots
CREATE TABLE IF NOT EXISTS trade_lifecycle_snapshots (
    id INTEGER GENERATED ALWAYS AS IDENTITY NOT NULL,
    session_id VARCHAR(36) NOT NULL,
    app_trade_id BIGINT NOT NULL,
    guid VARCHAR(36) NOT NULL,
    timestamp TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    event_type VARCHAR(10) NOT NULL,
    trade_type VARCHAR(4) NOT NULL,
    product VARCHAR(50) NOT NULL,
    entry_price NUMERIC(18,5) NOT NULL,
    quantity NUMERIC(18,5) NOT NULL,
    commission NUMERIC(18,5) NOT NULL,
    current_price NUMERIC(18,5),
    current_pnl NUMERIC(18,5),
    alt_pnl NUMERIC(18,5),
    is_active BOOLEAN NOT NULL,
    trailing_stop_active BOOLEAN NOT NULL,
    current_trailing_stop_level NUMERIC(18,5),
    peak_net_return_since_trailing_active NUMERIC(18,5),
    is_flipped CHAR(1) NOT NULL,
    close_reason VARCHAR(255),
    close_price NUMERIC(18,5),
    strategy_config TEXT,
    trade_signal VARCHAR(8),
    is_c_trade BOOLEAN DEFAULT FALSE NOT NULL,
    is_rt_member BOOLEAN DEFAULT FALSE NOT NULL,
    instance_name VARCHAR(100) DEFAULT '' NOT NULL,
    CONSTRAINT pk__trade_li__3213e83f85adb752 PRIMARY KEY (id)
);

-- Table: dbo.vw126_open_trades_counts_snapshots
CREATE TABLE IF NOT EXISTS vw126_open_trades_counts_snapshots (
    id INTEGER GENERATED ALWAYS AS IDENTITY NOT NULL,
    update_time TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    pos_alt_net_return INTEGER NOT NULL,
    product VARCHAR(50) NOT NULL,
    signal VARCHAR(10) NOT NULL,
    trade_count INTEGER NOT NULL,
    pos_alt_net_return_2 INTEGER NOT NULL,
    product_2 VARCHAR(50) NOT NULL,
    signal_2 VARCHAR(10) NOT NULL,
    trade_count_2 INTEGER NOT NULL,
    trade_count_ratio DOUBLE PRECISION NOT NULL,
    latest_price NUMERIC(18,6),
    CONSTRAINT pk__vw126_op__3213e83f44b3b0b5 PRIMARY KEY (id)
);

-- Table: dbo.zone_counts_minutely_log
CREATE TABLE IF NOT EXISTS zone_counts_minutely_log (
    last_update TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    beyondtarget_buy INTEGER NOT NULL,
    darkgreen_buy INTEGER NOT NULL,
    green_buy INTEGER NOT NULL,
    pink_buy INTEGER NOT NULL,
    yellow_buy INTEGER NOT NULL,
    red_buy INTEGER NOT NULL,
    beyondstop_buy INTEGER NOT NULL,
    beyondstop_sell INTEGER NOT NULL,
    red_sell INTEGER NOT NULL,
    pink_sell INTEGER NOT NULL,
    yellow_sell INTEGER NOT NULL,
    green_sell INTEGER NOT NULL,
    darkgreen_sell INTEGER NOT NULL,
    beyondtarget_sell INTEGER NOT NULL,
    captured_on TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    current_price NUMERIC(18,10),
    product VARCHAR(128) NOT NULL,
    CONSTRAINT pk_zone_counts_minutely_log PRIMARY KEY (product, last_update)
);

-- Table: dbo.zone_distribution_snapshots
CREATE TABLE IF NOT EXISTS zone_distribution_snapshots (
    snapshot_time TIMESTAMP WITHOUT TIME ZONE DEFAULT TIMEZONE('utc', CURRENT_TIMESTAMP) NOT NULL,
    product VARCHAR(50) NOT NULL,
    s_r9 INTEGER,
    s_r5 INTEGER,
    s_r4 INTEGER,
    s_r3 INTEGER,
    s_r2 INTEGER,
    s_r1 INTEGER,
    s_g1 INTEGER,
    s_g2 INTEGER,
    s_g3 INTEGER,
    s_g4 INTEGER,
    s_g5 INTEGER,
    s_g9 INTEGER,
    latest_price NUMERIC(18,9),
    b_r9 INTEGER,
    b_r5 INTEGER,
    b_r4 INTEGER,
    b_r3 INTEGER,
    b_r2 INTEGER,
    b_r1 INTEGER,
    b_g1 INTEGER,
    b_g2 INTEGER,
    b_g3 INTEGER,
    b_g4 INTEGER,
    b_g5 INTEGER,
    b_g9 INTEGER
);

-- =============================================================================
-- SECTION 2: INDEXES (Total: 38)
-- =============================================================================

CREATE INDEX IF NOT EXISTS ix_tradesnapshotlog_producttime ON tradesnapshotlog (product, snapshottimestamp);
CREATE INDEX IF NOT EXISTS ix__700_return_type__guid ON _700_return_type (guid) INCLUDE (return_type);
CREATE INDEX IF NOT EXISTS ix_alt_net_group_productlinked ON alt_net_group (product, linked);
CREATE INDEX IF NOT EXISTS ix_alt_net_group_productmodel ON alt_net_group (product, model);
CREATE INDEX IF NOT EXISTS ix_alt_net_group_updatetime ON alt_net_group (update_time);
CREATE INDEX IF NOT EXISTS ix_combined_trades_closed_bcsc_op ON combined_trades_closed (bc_op, sc_op) INCLUDE (product, signal, net_return);
CREATE INDEX IF NOT EXISTS ix_ctc_new_modelix_created ON combined_trades_closed (model_ix, created) INCLUDE (product, net_return, alt_net_return, tradeable);
CREATE INDEX IF NOT EXISTS ix_ctc_new_product_created ON combined_trades_closed (product, created) INCLUDE (model, net_return, alt_net_return, tradeable, last_update);
CREATE INDEX IF NOT EXISTS ix_ctc_new_tradeable_product_created ON combined_trades_closed (tradeable, product, created) INCLUDE (model, net_return, alt_net_return);
CREATE INDEX IF NOT EXISTS ix_combined_trades_open_active_model ON combined_trades_open (model) INCLUDE (trade_quantity) WHERE (tradeable>(0));
CREATE INDEX IF NOT EXISTS ix_combined_trades_open_product ON combined_trades_open (product) INCLUDE (signal, entry_price, entry_price2, trade_quantity, commission, latest_price, latest_price2, net_return, alt_net_return, max_net_return, max_net_return_time, min_net_return, min_net_return_time, last_update);
CREATE INDEX IF NOT EXISTS ix_cto_model_signal_lastupdate_guid ON combined_trades_open (model, signal, last_update, guid) INCLUDE (net_return, alt_net_return);
CREATE INDEX IF NOT EXISTS ix_combined_trades_open_snapshot_guid ON combined_trades_open_snapshot (guid, snapshottime) INCLUDE (buy_count, sell_count);
CREATE INDEX IF NOT EXISTS ix_combined_trades_open_snapshot_snapshottime ON combined_trades_open_snapshot (snapshottime);
CREATE INDEX IF NOT EXISTS ix_dna_pnl_cache_created ON dna_pnl_stream_cache (created);
CREATE INDEX IF NOT EXISTS ix_dna_pnl_cache_date_model ON dna_pnl_stream_cache (trade_date, model);
CREATE INDEX IF NOT EXISTS ix_ep051_directory_daily_summary_date ON ep051_directory_daily_summary (trade_date);
CREATE INDEX IF NOT EXISTS ix_ep051_strategy_rank_history_strategy ON ep051_strategy_rank_history (strategy_id, captured_at);
CREATE UNIQUE INDEX IF NOT EXISTS ix_fx_quotes_history_code_ts_type ON fx_quotes_history (code, timestamp, type);
CREATE INDEX IF NOT EXISTS cx_hrly_signal_perf_snapshots ON hrly_signal_perf_snapshots (update_time, product, hourbucket);
CREATE INDEX IF NOT EXISTS ix_product_forex_trade_freq_product ON product_forex (trade_freq, product);
CREATE INDEX IF NOT EXISTS ix_product_signal_snapshot_timeproduct ON product_signal_snapshot (snapshottimestamp, product);
CREATE UNIQUE INDEX IF NOT EXISTS ux_105_guid_ts_event ON tbl_105_trade_lifecycle_snapshots (guid, timestamp, event_type);
CREATE INDEX IF NOT EXISTS ix_tbl_700_bucket_boundaries_prod_cut ON tbl_700_bucket_boundaries (product, cut_value);
CREATE INDEX IF NOT EXISTS ix_tbl_700_bucket_boundaries_prod_idx ON tbl_700_bucket_boundaries (product, bucket_index);
CREATE INDEX IF NOT EXISTS ix_tbl_700_open_trades_log_created ON tbl_700_open_trades_log (created_ts);
CREATE INDEX IF NOT EXISTS ix_tbl_700_open_trades_log_prod_decision ON tbl_700_open_trades_log (product, decision);
CREATE INDEX IF NOT EXISTS ix_tbl_700_priors_7d_nomodel_lookup ON tbl_700_priors_7d_nomodel (product, signal, entry_bucket, time_bin, return_type);
CREATE INDEX IF NOT EXISTS ix_tbl_700_priors_v2_lookup ON tbl_700_priors_v2 (product, signal, model, return_type, entry_bucket, time_bin);
CREATE INDEX IF NOT EXISTS ix_tbl_800_hybrid_log_lookup ON tbl_800_hybrid_log (product, model, created_at) INCLUDE (event_type, regime_state, metrics_id);
CREATE INDEX IF NOT EXISTS ix_tbl_800_regime_state_lookup ON tbl_800_regime_state (product, model, evaluated_at) INCLUDE (regime_state, fast_side, slow_side, metrics_id);
CREATE INDEX IF NOT EXISTS ix_tbl_800_trade_metrics_lookup ON tbl_800_trade_metrics (product, model, window_end) INCLUDE (metrics_window_minutes, buy_trade_count, sell_trade_count, dur_ratio, count_ratio);
CREATE INDEX IF NOT EXISTS ix_tbl_model_signal_net_pms_time ON tbl_model_signal_net (product, model, signal, update_time) INCLUDE (net_return_sum, alt_net_return_sum);
CREATE INDEX IF NOT EXISTS ix_tbl_model_signal_net_prod_model_signal_time ON tbl_model_signal_net (product, model, signal, update_time) INCLUDE (net_return_sum, alt_net_return_sum);
CREATE INDEX IF NOT EXISTS ix_tbl_trade_link_executed ON tbl_trade_link (executed, send_order);
CREATE INDEX IF NOT EXISTS ix_tbl_trade_link_session_msg ON tbl_trade_link (session_id, message_id);
CREATE INDEX IF NOT EXISTS ix_vw126_snapshots_update_time ON vw126_open_trades_counts_snapshots (update_time);
CREATE INDEX IF NOT EXISTS ix_zone_snapshots_time_product ON zone_distribution_snapshots (snapshot_time, product);

-- =============================================================================
-- SECTION 3: FOREIGN KEYS (Total: 1)
-- =============================================================================

DO $$ BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_tbl_800_regime_state_metrics') THEN
        ALTER TABLE tbl_800_regime_state ADD CONSTRAINT fk_tbl_800_regime_state_metrics FOREIGN KEY (metrics_id) REFERENCES tbl_800_trade_metrics (metrics_id);
    END IF;
END $$;
