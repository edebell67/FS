
-- Test script for dbo.sp_get_rt_group_metrics
-- 2025-12-03

SET NOCOUNT ON;

-- 1. Define a temporary table with the same structure
-- Note: is_c_trade is also a required column based on the V64.3.1 update
IF OBJECT_ID('tempdb..#test_snapshots') IS NOT NULL
    DROP TABLE #test_snapshots;

CREATE TABLE #test_snapshots (
    app_trade_id VARCHAR(100),
    product VARCHAR(50),
    quantity DECIMAL(18, 2),
    current_pnl DECIMAL(18, 8),
    alt_pnl DECIMAL(18, 8),
    is_active BIT,
    event_type VARCHAR(50),
    trade_type VARCHAR(10),
    is_rt_member BIT,
    is_c_trade BIT,
    instance_name VARCHAR(100),
    timestamp DATETIME
);

-- 2. Insert sample data to simulate various scenarios
INSERT INTO #test_snapshots (app_trade_id, product, quantity, current_pnl, alt_pnl, is_active, event_type, trade_type, is_rt_member, is_c_trade, instance_name, timestamp)
VALUES
-- Trade 1: Active 'C' BUY from RT member (instance A)
('trade_01', 'GBP', 100.00, 25.50, 25.50, 1, 'open', 'buy', 1, 1, 'instance_A', GETDATE()),
-- Trade 2: Active 'C' SELL from RT member (instance B)
('trade_02', 'GBP', 50.00, -10.25, -10.25, 1, 'open', 'sell', 1, 1, 'instance_B', GETDATE()),
-- Trade 3: Closed 'C' BUY from RT member (instance A)
('trade_03', 'GBP', 200.00, 150.00, 150.00, 0, 'close', 'buy', 1, 1, 'instance_A', GETDATE()),
-- Trade 4: Active 'C' BUY from a NON-RT member (should be ignored)
('trade_04', 'GBP', 1000.00, 50.0, 50.0, 1, 'open', 'buy', 0, 1, 'instance_C', GETDATE()),
-- Trade 5: Active NON-'C' BUY from an RT member (should be ignored)
('trade_05', 'GBP', 2000.00, 75.0, 75.0, 1, 'open', 'buy', 1, 0, 'instance_A', GETDATE()),
-- Trade 6: An older, superseded snapshot for trade_01 (should be ignored)
('trade_01', 'GBP', 100.00, 10.00, 10.00, 1, 'snapshot', 'buy', 1, 1, 'instance_A', GETDATE() - 1);


-- 3. Execute the logic of sp_get_rt_group_metrics against the temp table
PRINT 'Executing stored procedure logic against test data...';

WITH LatestSnapshots AS (
    SELECT 
        app_trade_id,
        product,
        quantity,
        current_pnl,
        alt_pnl,
        is_active,
        event_type,
        trade_type,
        ROW_NUMBER() OVER (
            PARTITION BY app_trade_id 
            ORDER BY timestamp DESC
        ) as rn
    FROM #test_snapshots
    WHERE is_rt_member = 1
      AND is_c_trade = 1
)
SELECT 
    'current_open_qty' as metric,
    ABS(ISNULL(SUM(CASE WHEN is_active = 1 AND trade_type = 'buy' THEN quantity WHEN is_active = 1 AND trade_type = 'sell' THEN -quantity ELSE 0 END), 0)) as value
FROM LatestSnapshots WHERE rn = 1
UNION ALL
SELECT 
    'total_closed_profits' as metric,
    ISNULL(SUM(CASE WHEN is_active = 0 AND event_type = 'close' THEN current_pnl ELSE 0 END), 0) as value
FROM LatestSnapshots WHERE rn = 1
UNION ALL
SELECT 
    'current_open_profits' as metric,
    ISNULL(SUM(CASE WHEN is_active = 1 THEN current_pnl ELSE 0 END), 0) as value
FROM LatestSnapshots WHERE rn = 1;


-- 4. Clean up
DROP TABLE #test_snapshots;
PRINT 'Test complete.';
