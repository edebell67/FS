ALTER VIEW [dbo].[vwCombined_trades_closed_output_top200]
AS
WITH base AS (
    SELECT
        guid,
        model,
        product,
        created,
        signal,
        CAST(created AS date) AS trade_date,
        net_return,
        alt_net_return,
        SUM(net_return) OVER (
            PARTITION BY model, CAST(created AS date)
            ORDER BY created, guid
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ) AS net_return_sum,
        SUM(alt_net_return) OVER (
            PARTITION BY model, CAST(created AS date)
            ORDER BY created, guid
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ) AS alt_net_return_sum,
        SUM(CASE WHEN signal = 'BUY' THEN net_return ELSE 0 END) OVER (
            PARTITION BY model, CAST(created AS date)
            ORDER BY created, guid
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ) AS buy_net_return_sum,
        SUM(CASE WHEN signal = 'SELL' THEN net_return ELSE 0 END) OVER (
            PARTITION BY model, CAST(created AS date)
            ORDER BY created, guid
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ) AS sell_net_return_sum,
        COUNT(1) OVER (
            PARTITION BY model, CAST(created AS date)
            ORDER BY created, guid
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ) AS trade_count
    FROM dbo.combined_trades_closed_arc
    WHERE model LIKE 'DNA%'
),
ranked AS (
    SELECT *,
        DENSE_RANK() OVER (
            PARTITION BY trade_date
            ORDER BY 
                CASE 
                    WHEN net_return_sum >= alt_net_return_sum 
                    THEN net_return_sum 
                    ELSE alt_net_return_sum 
                END DESC
        ) AS model_rank
    FROM base
)
SELECT
    guid,
    model,
    product,
    created,
    signal,
    net_return,
    alt_net_return,
    net_return_sum,
    alt_net_return_sum,
    buy_net_return_sum,
    sell_net_return_sum,
    trade_count
FROM ranked
WHERE model_rank <= 200
GO
