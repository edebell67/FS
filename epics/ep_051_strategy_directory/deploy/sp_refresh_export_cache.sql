-- EP051 export pre-aggregation cache.
-- Version 1.0.0 (2026-08-27).
--
-- Problem: hosted_directory/app/repository.py's local_strategies() and
-- local_equity_curves() (used by sync/export_snapshot.py) run unfiltered
-- aggregations, including window functions, over dbo.combined_trades_closed
-- (1M+ rows per repository.py's own comments) on every export. That is the
-- likely cause of the export timeouts blocking the EP051 sync acceptance
-- test (see agent_board/board.jsonl thread ep051_render_deployment,
-- ~2026-08-27T17:00-17:04).
--
-- Fix: precompute both result sets into cache tables on a schedule (wire
-- dbo.usp_ep051_refresh_export_cache into a SQL Server Agent job — every
-- 10 minutes to match the existing local sync cadence, or whatever cadence
-- fits). export_snapshot.py can then read these tables directly instead of
-- re-running the live aggregation on every export call. That Python-side
-- change is a separate follow-up, not included here — this script only
-- creates the tables and the refresh procedure.
--
-- Column shapes mirror repository.py's AGGREGATE_SQL (local_strategies)
-- and the local_equity_curves() CTE exactly, so a future repository.py
-- change can swap the live query for a `SELECT * FROM
-- dbo.ep051_export_strategy_summary` / `dbo.ep051_export_equity_curve`
-- with no shape mismatch.

IF NOT EXISTS (SELECT 1 FROM sys.tables WHERE name = 'ep051_export_strategy_summary')
BEGIN
    CREATE TABLE dbo.ep051_export_strategy_summary (
        strategy_id          varchar(64)     NOT NULL PRIMARY KEY,
        descriptive_name     nvarchar(200)   NULL,
        product_name         nvarchar(400)   NULL,
        total_trades         bigint          NOT NULL,
        wins                 bigint          NOT NULL,
        losses               bigint          NOT NULL,
        breakevens           bigint          NOT NULL,
        total_net_return     decimal(28,8)   NOT NULL,
        win_rate             decimal(18,10)  NULL,
        profit_factor        decimal(18,10)  NULL,
        max_drawdown_money   decimal(28,8)   NULL,
        evidence_start       datetime2       NULL,
        evidence_end         datetime2       NULL,
        refreshed_at         datetime2       NOT NULL DEFAULT sysutcdatetime()
    );
END

IF NOT EXISTS (SELECT 1 FROM sys.tables WHERE name = 'ep051_export_equity_curve')
BEGIN
    CREATE TABLE dbo.ep051_export_equity_curve (
        strategy_id     varchar(64)     NOT NULL,
        trade_number    int             NOT NULL,
        opened_at       datetime2       NULL,
        closed_at       datetime2       NULL,
        net_return      float           NOT NULL,
        equity          float           NOT NULL,
        drawdown        float           NOT NULL,
        refreshed_at    datetime2       NOT NULL DEFAULT sysutcdatetime(),
        CONSTRAINT pk_ep051_export_equity_curve PRIMARY KEY (strategy_id, trade_number)
    );
END

IF NOT EXISTS (SELECT 1 FROM sys.tables WHERE name = 'ep051_export_cache_run_log')
BEGIN
    CREATE TABLE dbo.ep051_export_cache_run_log (
        run_id              bigint IDENTITY(1,1) PRIMARY KEY,
        started_at          datetime2   NOT NULL,
        completed_at        datetime2   NULL,
        strategy_rows       int         NULL,
        equity_curve_rows   int         NULL,
        status              varchar(20) NOT NULL DEFAULT 'running',
        error_message       nvarchar(4000) NULL
    );
END
GO

CREATE OR ALTER PROCEDURE dbo.usp_ep051_refresh_export_cache
AS
BEGIN
    SET NOCOUNT ON;
    SET XACT_ABORT ON;

    DECLARE @run_id bigint, @started datetime2 = sysutcdatetime();
    INSERT INTO dbo.ep051_export_cache_run_log(started_at, status) VALUES (@started, 'running');
    SET @run_id = SCOPE_IDENTITY();

    BEGIN TRY
        -- Mirrors repository.py AGGREGATE_SQL with no date filter (matches
        -- export_snapshot.py's unfiltered local_strategies(settings) call).
        WITH universe AS (
            SELECT CASE WHEN RIGHT(model,2) IN ('_B','_S') THEN LEFT(model,LEN(model)-2) ELSE model END strategy_id,
                   MAX(NULLIF(LTRIM(RTRIM(strategy_name)),'')) descriptive_name
            FROM dbo.product_forex
            WHERE model LIKE 'DNA[_]%'
            GROUP BY CASE WHEN RIGHT(model,2) IN ('_B','_S') THEN LEFT(model,LEN(model)-2) ELSE model END
        ), universe_products AS (
            SELECT strategy_id, STRING_AGG(product, ', ') product_name
            FROM (
                SELECT DISTINCT CASE WHEN RIGHT(model,2) IN ('_B','_S') THEN LEFT(model,LEN(model)-2) ELSE model END strategy_id, product
                FROM dbo.product_forex WHERE model LIKE 'DNA[_]%' AND product IS NOT NULL
            ) source_products
            GROUP BY strategy_id
        ), canonical AS (
            SELECT CASE WHEN RIGHT(model,2) IN ('_B','_S') THEN LEFT(model,LEN(model)-2) ELSE model END strategy_id,
                   CAST(net_return AS float) net_return, created, COALESCE(g_close_time,last_update,created) closed_at
            FROM dbo.combined_trades_closed WITH (NOLOCK)
            WHERE model_ix LIKE 'DNA[_]%' AND net_return IS NOT NULL
        ), evidence AS (
            SELECT strategy_id, COUNT_BIG(*) total_trades,
                SUM(CASE WHEN net_return>0 THEN 1 ELSE 0 END) wins,
                SUM(CASE WHEN net_return<0 THEN 1 ELSE 0 END) losses,
                SUM(CASE WHEN net_return=0 THEN 1 ELSE 0 END) breakevens,
                SUM(net_return) total_net_return,
                SUM(CASE WHEN net_return>0 THEN net_return ELSE 0 END) gross_profit,
                ABS(SUM(CASE WHEN net_return<0 THEN net_return ELSE 0 END)) gross_loss,
                MIN(created) evidence_start, MAX(closed_at) evidence_end
            FROM canonical GROUP BY strategy_id
        )
        SELECT
            universe.strategy_id, universe.descriptive_name, universe_products.product_name,
            COALESCE(evidence.total_trades,0) total_trades, COALESCE(evidence.wins,0) wins,
            COALESCE(evidence.losses,0) losses, COALESCE(evidence.breakevens,0) breakevens,
            CAST(COALESCE(evidence.total_net_return,0) AS decimal(28,8)) total_net_return,
            CAST(COALESCE(CAST(evidence.wins AS decimal(28,10))/NULLIF(evidence.total_trades,0),0) AS decimal(18,10)) win_rate,
            CAST(evidence.gross_profit/NULLIF(evidence.gross_loss,0) AS decimal(18,10)) profit_factor,
            CAST(NULL AS decimal(28,8)) max_drawdown_money,
            evidence.evidence_start, evidence.evidence_end,
            sysutcdatetime() refreshed_at
        INTO #strategy_staging
        FROM universe
        LEFT JOIN universe_products ON universe_products.strategy_id=universe.strategy_id
        LEFT JOIN evidence ON evidence.strategy_id=universe.strategy_id;

        -- Mirrors repository.py local_equity_curves() (MAX_PROFILE_POINTS=1000 per strategy).
        WITH ranked_trades AS (
            SELECT
                CASE WHEN RIGHT(model,2) IN ('_B','_S') THEN LEFT(model,LEN(model)-2) ELSE model END strategy_id,
                COALESCE(g_close_time,last_update,created) closed_at, created opened_at, created, guid,
                CAST(net_return AS float) net_return,
                ROW_NUMBER() OVER(
                    PARTITION BY CASE WHEN RIGHT(model,2) IN ('_B','_S') THEN LEFT(model,LEN(model)-2) ELSE model END
                    ORDER BY COALESCE(g_close_time,last_update,created) DESC, created DESC, guid DESC) reverse_number
            FROM dbo.combined_trades_closed WITH (NOLOCK)
            WHERE model_ix LIKE 'DNA[_]%' AND net_return IS NOT NULL
        ), trades AS (
            SELECT strategy_id, closed_at, opened_at, created, guid, net_return
            FROM ranked_trades WHERE reverse_number <= 1000
        ), equity AS (
            SELECT strategy_id, closed_at, opened_at, guid, net_return,
                SUM(net_return) OVER(PARTITION BY strategy_id ORDER BY closed_at, created, guid ROWS UNBOUNDED PRECEDING) equity
            FROM trades
        ), curve AS (
            SELECT strategy_id, closed_at, opened_at, guid, net_return, equity,
                equity - CASE WHEN MAX(equity) OVER(PARTITION BY strategy_id ORDER BY closed_at, guid ROWS UNBOUNDED PRECEDING) > 0
                              THEN MAX(equity) OVER(PARTITION BY strategy_id ORDER BY closed_at, guid ROWS UNBOUNDED PRECEDING) ELSE 0 END drawdown,
                ROW_NUMBER() OVER(PARTITION BY strategy_id ORDER BY closed_at, guid) trade_number
            FROM equity
        )
        SELECT strategy_id, trade_number, opened_at, closed_at, net_return, equity, drawdown,
               sysutcdatetime() refreshed_at
        INTO #equity_staging
        FROM curve;

        BEGIN TRANSACTION;
            TRUNCATE TABLE dbo.ep051_export_strategy_summary;
            INSERT INTO dbo.ep051_export_strategy_summary
                (strategy_id, descriptive_name, product_name, total_trades, wins, losses, breakevens,
                 total_net_return, win_rate, profit_factor, max_drawdown_money, evidence_start, evidence_end, refreshed_at)
            SELECT strategy_id, descriptive_name, product_name, total_trades, wins, losses, breakevens,
                   total_net_return, win_rate, profit_factor, max_drawdown_money, evidence_start, evidence_end, refreshed_at
            FROM #strategy_staging;

            TRUNCATE TABLE dbo.ep051_export_equity_curve;
            INSERT INTO dbo.ep051_export_equity_curve
                (strategy_id, trade_number, opened_at, closed_at, net_return, equity, drawdown, refreshed_at)
            SELECT strategy_id, trade_number, opened_at, closed_at, net_return, equity, drawdown, refreshed_at
            FROM #equity_staging;
        COMMIT TRANSACTION;

        UPDATE dbo.ep051_export_cache_run_log
        SET completed_at = sysutcdatetime(),
            strategy_rows = (SELECT COUNT(*) FROM dbo.ep051_export_strategy_summary),
            equity_curve_rows = (SELECT COUNT(*) FROM dbo.ep051_export_equity_curve),
            status = 'success'
        WHERE run_id = @run_id;
    END TRY
    BEGIN CATCH
        IF XACT_STATE() <> 0 ROLLBACK TRANSACTION;
        UPDATE dbo.ep051_export_cache_run_log
        SET completed_at = sysutcdatetime(), status = 'failed', error_message = ERROR_MESSAGE()
        WHERE run_id = @run_id;
        THROW;
    END CATCH
END
GO
