USE [tradedb_sim2]
GO
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE OR ALTER PROCEDURE dbo.sp_snapshot_dna_model_summary_5min
    @force_run BIT = 0,
    @target_date DATE = NULL
AS
BEGIN
    SET NOCOUNT ON;
    SET XACT_ABORT ON;

    DECLARE @sp_name NVARCHAR(128) = N'dbo.sp_snapshot_dna_model_summary_5min';
    DECLARE @now DATETIME2(3) = GETDATE();
    DECLARE @date DATE = COALESCE(@target_date, CAST(@now AS DATE));
    DECLARE @rows_inserted INT = 0;

    -- 1. Cadence Gate (Every 5 minutes, unless forced)
    IF @force_run = 0
    BEGIN
        IF EXISTS (
            SELECT 1 
            FROM dbo.tbl_dna_model_summary_snapshots_5min
            WHERE snapshot_timestamp >= DATEADD(MINUTE, -5, @now)
        )
        BEGIN
            RETURN;
        END
    END

    -- 2. Aggregate Closed Trades (Today / Target Date)
    IF OBJECT_ID('tempdb..#closed_stats') IS NOT NULL DROP TABLE #closed_stats;
    SELECT 
        c.model,
        COUNT(*) AS closed_cnt,
        SUM(CASE WHEN LOWER(c.signal) IN ('b','buy') THEN 1 ELSE 0 END) AS buy_closed_cnt,
        SUM(CASE WHEN LOWER(c.signal) IN ('s','sell') THEN 1 ELSE 0 END) AS sell_closed_cnt,
        SUM(c.net_return) AS closed_net,
        SUM(c.alt_net_return) AS closed_alt_net,
        SUM(CASE WHEN LOWER(c.signal) IN ('b','buy') THEN c.net_return ELSE 0.0 END) AS closed_buy_net,
        SUM(CASE WHEN LOWER(c.signal) IN ('b','buy') THEN c.alt_net_return ELSE 0.0 END) AS closed_buy_alt_net,
        SUM(CASE WHEN LOWER(c.signal) IN ('s','sell') THEN c.net_return ELSE 0.0 END) AS closed_sell_net,
        SUM(CASE WHEN LOWER(c.signal) IN ('s','sell') THEN c.alt_net_return ELSE 0.0 END) AS closed_sell_alt_net
    INTO #closed_stats
    FROM dbo.combined_trades_closed c WITH (NOLOCK)
    WHERE c.model LIKE 'DNA[_]%' 
      AND CAST(c.created AS DATE) = @date
    GROUP BY c.model;

    CREATE UNIQUE CLUSTERED INDEX IX_cs_model ON #closed_stats(model);

    -- 3. Aggregate Open Trades (Current Live Positions)
    IF OBJECT_ID('tempdb..#open_stats') IS NOT NULL DROP TABLE #open_stats;
    SELECT 
        o.model,
        COUNT(*) AS open_cnt,
        SUM(o.net_return) AS open_net,
        SUM(o.alt_net_return) AS open_alt_net,
        SUM(CASE WHEN LOWER(o.signal) IN ('b','buy') THEN o.net_return ELSE 0.0 END) AS open_buy_net,
        SUM(CASE WHEN LOWER(o.signal) IN ('b','buy') THEN o.alt_net_return ELSE 0.0 END) AS open_buy_alt_net,
        SUM(CASE WHEN LOWER(o.signal) IN ('s','sell') THEN o.net_return ELSE 0.0 END) AS open_sell_net,
        SUM(CASE WHEN LOWER(o.signal) IN ('s','sell') THEN o.alt_net_return ELSE 0.0 END) AS open_sell_alt_net
    INTO #open_stats
    FROM dbo.combined_trades_open o WITH (NOLOCK)
    WHERE o.model LIKE 'DNA[_]%' 
      AND COALESCE(o.tradeable, 0) > 0
    GROUP BY o.model;

    CREATE UNIQUE CLUSTERED INDEX IX_os_model ON #open_stats(model);

    -- 4. Target Universe of DNA Models with Strategy Metadata
    IF OBJECT_ID('tempdb..#models') IS NOT NULL DROP TABLE #models;
    SELECT DISTINCT 
        pf.model,
        pf.product,
        pf.strategy_name,
        COALESCE(
            JSON_VALUE(pf.dna_json, '$.script_name'),
            CASE 
                WHEN pf.strategy_name LIKE 'breakout_R_Rev%' THEN 'breakout_R_Rev'
                WHEN pf.strategy_name LIKE 'breakout_Rev%'   THEN 'breakout_Rev'
                WHEN pf.strategy_name LIKE 'breakout_R%'     THEN 'breakout_R'
                WHEN pf.strategy_name LIKE 'breakout%'       THEN 'breakout'
                ELSE 'other'
            END
        ) AS strategy_family
    INTO #models
    FROM dbo.product_forex pf WITH (NOLOCK)
    WHERE pf.model LIKE 'DNA[_]%';

    CREATE CLUSTERED INDEX IX_m_model ON #models(model);

    -- 5. Insert Snapshot Records
    INSERT INTO dbo.tbl_dna_model_summary_snapshots_5min
    (
        snapshot_timestamp,
        model,
        product,
        strategy_name,
        strategy_family,
        cum_net,
        cum_alt_net,
        cum_buy_net,
        cum_buy_alt_net,
        cum_sell_net,
        cum_sell_alt_net,
        open_trade_count,
        closed_trade_count,
        buy_closed_count,
        sell_closed_count,
        created_at
    )
    SELECT 
        @now AS snapshot_timestamp,
        m.model,
        m.product,
        m.strategy_name,
        m.strategy_family,
        COALESCE(cs.closed_net, 0.0) + COALESCE(os.open_net, 0.0) AS cum_net,
        COALESCE(cs.closed_alt_net, 0.0) + COALESCE(os.open_alt_net, 0.0) AS cum_alt_net,
        COALESCE(cs.closed_buy_net, 0.0) + COALESCE(os.open_buy_net, 0.0) AS cum_buy_net,
        COALESCE(cs.closed_buy_alt_net, 0.0) + COALESCE(os.open_buy_alt_net, 0.0) AS cum_buy_alt_net,
        COALESCE(cs.closed_sell_net, 0.0) + COALESCE(os.open_sell_net, 0.0) AS cum_sell_net,
        COALESCE(cs.closed_sell_alt_net, 0.0) + COALESCE(os.open_sell_alt_net, 0.0) AS cum_sell_alt_net,
        COALESCE(os.open_cnt, 0) AS open_trade_count,
        COALESCE(cs.closed_cnt, 0) AS closed_trade_count,
        COALESCE(cs.buy_closed_cnt, 0) AS buy_closed_count,
        COALESCE(cs.sell_closed_cnt, 0) AS sell_closed_count,
        @now AS created_at
    FROM #models m
    LEFT JOIN #closed_stats cs ON cs.model = m.model
    LEFT JOIN #open_stats os ON os.model = m.model
    WHERE COALESCE(cs.closed_cnt, 0) > 0 OR COALESCE(os.open_cnt, 0) > 0;

    SET @rows_inserted = @@ROWCOUNT;

    -- Cleanup
    DROP TABLE IF EXISTS #closed_stats, #open_stats, #models;

    RAISERROR(N'sp_snapshot_dna_model_summary_5min completed. Snapshotted %d active DNA models.', 10, 1, @rows_inserted) WITH NOWAIT;
END
GO
