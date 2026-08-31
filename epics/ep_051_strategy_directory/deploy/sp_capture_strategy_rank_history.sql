-- EP051 strategy rank-position capture, moved server-side.
-- Version 1.0.0 (2026-08-31).
--
-- Problem: scripts/capture_strategy_rank_history.py is a long-running
-- Python process (its own `while True: ... time.sleep(900)` loop) that
-- opens a connection and re-runs the full current-day rank aggregation
-- against dbo.combined_trades_closed every 15 minutes. That competes with
-- the live trading system's own stored procedures for memory grants on
-- the shared SQL Server instance - the same RESOURCE_SEMAPHORE contention
-- pattern already worked around once for exports (see
-- sp_refresh_export_cache.sql). A measured run of the Python script's
-- query just now took 153.81s under live contention (1,478 strategies).
--
-- Fix: same shape as usp_ep051_refresh_export_cache - move the query into
-- a stored procedure, wire it into a SQL Server Agent job on a 15-minute
-- schedule (matching the Python script's current --interval default), and
-- retire live_01_run_ep051_rank_history.bat / capture_strategy_rank_history.py
-- once the Agent job is confirmed running. Not done here - this script only
-- creates the procedure and a run log table, and is being timed standalone
-- first.
--
-- Query logic is copied verbatim from capture_strategy_rank_history.py's
-- RANK_QUERY (current-day entry-date cohort, same canonical-strategy-id
-- CASE expression used everywhere else in EP051).

IF NOT EXISTS (SELECT 1 FROM sys.tables WHERE name = 'ep051_rank_capture_run_log')
BEGIN
    CREATE TABLE dbo.ep051_rank_capture_run_log (
        run_id          bigint IDENTITY(1,1) PRIMARY KEY,
        started_at      datetime2       NOT NULL,
        completed_at    datetime2       NULL,
        strategy_rows   int             NULL,
        status          varchar(20)     NOT NULL DEFAULT 'running',
        error_message   nvarchar(4000)  NULL
    );
END
GO

CREATE OR ALTER PROCEDURE dbo.usp_ep051_capture_strategy_rank_history
AS
BEGIN
    SET NOCOUNT ON;
    SET XACT_ABORT ON;

    DECLARE @run_id bigint, @started datetime2 = sysutcdatetime();
    DECLARE @captured_at datetime2 = CAST(SYSUTCDATETIME() AS datetime2(0));
    DECLARE @today_start datetime2 = CAST(CAST(SYSUTCDATETIME() AS date) AS datetime2);
    DECLARE @today_end datetime2 = DATEADD(day, 1, @today_start);
    DECLARE @row_count int;

    INSERT INTO dbo.ep051_rank_capture_run_log(started_at, status) VALUES (@started, 'running');
    SET @run_id = SCOPE_IDENTITY();

    BEGIN TRY
        WITH agg AS (
            SELECT CASE WHEN RIGHT(model,2) IN ('_B','_S') THEN LEFT(model,LEN(model)-2) ELSE model END strategy_id,
                   SUM(CAST(net_return AS float)) total_net_return, COUNT(*) total_trades
            FROM dbo.combined_trades_closed WITH (NOLOCK)
            WHERE model_ix LIKE 'DNA[_]%' AND net_return IS NOT NULL AND created >= @today_start AND created < @today_end
            GROUP BY CASE WHEN RIGHT(model,2) IN ('_B','_S') THEN LEFT(model,LEN(model)-2) ELSE model END
        )
        INSERT INTO dbo.ep051_strategy_rank_history (captured_at, strategy_id, total_net_return, total_trades, rank_position)
        SELECT @captured_at, strategy_id, total_net_return, total_trades,
               RANK() OVER (ORDER BY total_net_return DESC)
        FROM agg
        OPTION (MAXDOP 1);

        SET @row_count = @@ROWCOUNT;

        UPDATE dbo.ep051_rank_capture_run_log
        SET completed_at = sysutcdatetime(), strategy_rows = @row_count, status = 'success'
        WHERE run_id = @run_id;
    END TRY
    BEGIN CATCH
        UPDATE dbo.ep051_rank_capture_run_log
        SET completed_at = sysutcdatetime(), status = 'failed', error_message = ERROR_MESSAGE()
        WHERE run_id = @run_id;
        THROW;
    END CATCH
END
GO
