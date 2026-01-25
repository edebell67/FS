-- Test script to isolate the issue
IF OBJECT_ID('tempdb..#cand_test') IS NOT NULL DROP TABLE #cand_test;
CREATE TABLE #cand_test(
   guid uniqueidentifier NOT NULL,
   pf_ord int NOT NULL,
   product nvarchar(50) NOT NULL,
   model nvarchar(50) NOT NULL,
   product_type nvarchar(50) NOT NULL,
   created datetime2(3) NOT NULL,
   commission float NOT NULL,
   target_profit smallint NULL,  -- Allow NULL
   target_loss smallint NULL,    -- Allow NULL
   trade_qty bigint NOT NULL,
   signal nvarchar(4) NOT NULL,            -- 'buy' / 'sell'
   entry_price float NULL,
   latest_price float NULL,
   net_return float NULL,
   alt_net_return float NULL,
   in_whitelist bit NOT NULL
);

-- Insert a test row with NULL values
INSERT #cand_test
SELECT 
    NEWID(), 
    1, 
    'test_product', 
    'test_model', 
    'test_type', 
    GETDATE(), 
    1.0, 
    NULL,  -- target_profit
    NULL,  -- target_loss
    1000, 
    'buy', 
    1.0, 
    1.0, 
    1.0, 
    1.0, 
    1