USE [tradedb];
GO

-- Test script for sp_001_buy_sell_count_entry's #signals CTE logic
-- This script will not modify any data, only select from views and simulate the CTE.

PRINT '--- Content of dbo.vw_900_dynamic_leadership_live ---';
SELECT
    snapshot_time,
    model,
    product,
    signal,
    net_return
FROM dbo.vw_900_dynamic_leadership_live
ORDER BY product, model;
GO

PRINT '--- Simulated #signals CTE output ---';
SELECT
    LOWER(v.product) AS product,
    CASE
        WHEN SUM(CASE WHEN v.signal = 'BUY' THEN 1 ELSE 0 END) = 5 THEN N'buy'
        WHEN SUM(CASE WHEN v.signal = 'SELL' THEN 1 ELSE 0 END) = 5 THEN N'sell'
        ELSE NULL
    END AS signal
FROM dbo.vw_900_dynamic_leadership_live AS v
GROUP BY v.product
HAVING COUNT(v.model) = 5; -- Ensure all 5 top models are present for the product
GO
