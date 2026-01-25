CREATE OR ALTER PROCEDURE dbo.sp_refresh_dna_pnl_cache
    @FullRefresh BIT = 0
AS
BEGIN
    SET NOCOUNT ON;
    
    -- If full refresh, clear the cache
    IF @FullRefresh = 1
    BEGIN
        TRUNCATE TABLE dbo.dna_pnl_stream_cache;
    END

    -- Get the last processed time to do incremental updates
    DECLARE @LastCreated DATETIME = ISNULL((SELECT MAX(created) FROM dbo.dna_pnl_stream_cache), '2000-01-01');

    -- Insert new trades with their calculated rolling P&L
    INSERT INTO dbo.dna_pnl_stream_cache (
        model, product, trade_date, created, signal, 
        net_return_sum, alt_net_return_sum, buy_net_return_sum, sell_net_return_sum, trade_count,
        net_return -- [V20260125_1830] Added individual net return
    )
    SELECT 
        model, product, trade_date, created, signal,
        net_return_sum, alt_net_return_sum, buy_net_return_sum, sell_net_return_sum, trade_count,
        net_return -- [V20260125_1830] Added individual net return
    FROM (
        SELECT 
            model, product, CAST(created AS DATE) as trade_date, created, signal,
            net_return, -- [V20260125_1830]
            SUM(net_return) OVER (PARTITION BY model, CAST(created AS date) ORDER BY created, guid ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) as net_return_sum,
            SUM(alt_net_return) OVER (PARTITION BY model, CAST(created AS date) ORDER BY created, guid ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) as alt_net_return_sum,
            SUM(CASE WHEN signal = 'BUY' THEN net_return ELSE 0 END) OVER (PARTITION BY model, CAST(created AS date) ORDER BY created, guid ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) as buy_net_return_sum,
            SUM(CASE WHEN signal = 'SELL' THEN net_return ELSE 0 END) OVER (PARTITION BY model, CAST(created AS date) ORDER BY created, guid ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) as sell_net_return_sum,
            COUNT(1) OVER (PARTITION BY model, CAST(created AS date) ORDER BY created, guid ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) as trade_count
        FROM dbo.combined_trades_closed_arc
        WHERE created > @LastCreated
        AND model LIKE 'DNA%'
    ) AS source;

    PRINT 'Cache refresh complete.';
END
GO

-- Refresh with new column
EXEC dbo.sp_refresh_dna_pnl_cache @FullRefresh = 1;
GO
