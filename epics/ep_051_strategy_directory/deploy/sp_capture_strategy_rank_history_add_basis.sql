-- Adds an explicit `basis` column to dbo.ep051_strategy_rank_history and
-- stamps it on every row usp_ep051_capture_strategy_rank_history writes,
-- replacing the implicit "captured_at >= MIN(started_at) FROM
-- ep051_rank_capture_run_log" cutover previously used by
-- app/repository.py's local_rank_journey() to skip pre-cutover rows.
--
-- Version 1.0.0 (2026-08-31).
--
-- Problem: the table already holds rows from two incompatible ranking
-- definitions - the retired all-time-basis Python script
-- (scripts/capture_strategy_rank_history.py, before its 1.1.0 current-day
-- change) ranked against the entire ~8000+ strategy universe, while the
-- new stored procedure ranks against today's cohort only. A timestamp
-- cutover works today because there happens to be exactly one writer with
-- one consistent definition going forward, but nothing stops a future
-- edit to the ranking window from silently reintroducing the same
-- mixed-basis bug, with no record of which rows came from which
-- definition. An explicit, stamped basis column makes that structural
-- instead of implicit: local_rank_journey() (and any future caller) can
-- filter on the exact basis value it understands, rather than trusting a
-- date range to line up with a code change.
--
-- Existing rows are backfilled to NULL (unknown basis, both the legacy
-- all-time rows and the current-day rows already written by
-- usp_ep051_capture_strategy_rank_history before this migration) -
-- deliberately not backfilled to 'current_day_v1' by guessing from
-- captured_at, since that would just recreate the same implicit-cutover
-- assumption this migration exists to remove. NULL rows are excluded by
-- the same "unknown basis, don't use it" logic as the old all-time rows -
-- app/repository.py was updated in the same change to filter on
-- basis = 'current_day_v1' instead of the run-log cutover, so the small
-- number of already-captured current-day-basis-but-unstamped rows will
-- simply age out of the 30-minute-cadence journey lookups within the hour.

IF NOT EXISTS (
    SELECT 1 FROM sys.columns
    WHERE object_id = OBJECT_ID('dbo.ep051_strategy_rank_history') AND name = 'basis'
)
BEGIN
    ALTER TABLE dbo.ep051_strategy_rank_history ADD basis varchar(32) NULL;
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
    DECLARE @basis varchar(32) = 'current_day_v1';

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
        INSERT INTO dbo.ep051_strategy_rank_history (captured_at, strategy_id, total_net_return, total_trades, rank_position, basis)
        SELECT @captured_at, strategy_id, total_net_return, total_trades,
               RANK() OVER (ORDER BY total_net_return DESC), @basis
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
