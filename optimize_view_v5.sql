ALTER VIEW [dbo].[vwCombined_trades_closed_output_top200]
AS
WITH DailyModelTotals AS (
    -- Pass 1: Get final P&L for each model/day to determine Top 200 candidates efficiently
    SELECT 
        model,
        CAST(created AS date) AS trade_date,
        SUM(net_return) as net_final,
        SUM(alt_net_return) as alt_final
    FROM dbo.combined_trades_closed_arc
    WHERE model LIKE 'DNA%'
    GROUP BY model, CAST(created AS date)
),
DailyRanks AS (
    -- Pass 2: Rank models based on their final P&L totals
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
    -- Filter down to the Top 200 models of each day
    SELECT model, trade_date 
    FROM DailyRanks 
    WHERE daily_rank <= 200
)
SELECT
    r.guid,
    r.model,
    r.product,
    r.created,
    r.signal,
    r.net_return,
    r.alt_net_return,
    -- Pass 3: Perform "Heavy" window functions ONLY for the winning models
    SUM(r.net_return) OVER (PARTITION BY r.model, CAST(r.created AS date) ORDER BY r.created, r.guid ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) as net_return_sum,
    SUM(r.alt_net_return) OVER (PARTITION BY r.model, CAST(r.created AS date) ORDER BY r.created, r.guid ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) as alt_net_return_sum,
    SUM(CASE WHEN r.signal = 'BUY' THEN r.net_return ELSE 0 END) OVER (PARTITION BY r.model, CAST(r.created AS date) ORDER BY r.created, r.guid ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) as buy_net_return_sum,
    SUM(CASE WHEN r.signal = 'SELL' THEN r.net_return ELSE 0 END) OVER (PARTITION BY r.model, CAST(r.created AS date) ORDER BY r.created, r.guid ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) as sell_net_return_sum,
    COUNT(1) OVER (PARTITION BY r.model, CAST(r.created AS date) ORDER BY r.created, r.guid ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) as trade_count
FROM dbo.combined_trades_closed_arc r
INNER JOIN Winners w ON r.model = w.model AND CAST(r.created AS date) = w.trade_date
WHERE r.model LIKE 'DNA%'
GO
