CREATE OR ALTER VIEW [dbo].[vwCombined_trades_closed_output_top200]
AS
WITH DailyModelTotals AS (
    -- Pass 1: Get final daily P&L from the pre-calculated CACHE table (Fast SELECT)
    SELECT 
        model,
        trade_date,
        MAX(net_return_sum) as net_final,
        MAX(alt_net_return_sum) as alt_final
    FROM dbo.dna_pnl_stream_cache
    GROUP BY model, trade_date
),
DailyRanks AS (
    -- Pass 2: Rank the pre-calculated winners
    SELECT 
        model,
        trade_date,
        DENSE_RANK() OVER (
            PARTITION BY trade_date 
            ORDER BY (CASE WHEN net_final >= alt_final THEN net_final ELSE alt_final END) DESC
        ) AS daily_rank
    FROM DailyModelTotals
),
Winners AS (
    -- Pass 3: Narrow down to Top 200
    SELECT model, trade_date 
    FROM DailyRanks 
    WHERE daily_rank <= 200
)
-- FINAL RESULT: Zero math, just an indexed join on physical data
-- [V20260125_1835] Added net_return for signal-level accuracy
SELECT
    r.model,
    r.product,
    r.created,
    r.signal,
    r.net_return,
    r.net_return_sum,
    r.alt_net_return_sum,
    r.buy_net_return_sum,
    r.sell_net_return_sum,
    r.trade_count
FROM dbo.dna_pnl_stream_cache r
INNER JOIN Winners w ON r.model = w.model AND r.trade_date = w.trade_date;
GO
