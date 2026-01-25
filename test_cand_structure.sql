-- Test script to verify #cand table structure
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

-- Check the table structure
SELECT 
    COLUMN_NAME, 
    IS_NULLABLE, 
    DATA_TYPE, 
    CHARACTER_MAXIMUM_LENGTH, 
    NUMERIC_PRECISION, 
    NUMERIC_SCALE
FROM tempdb.INFORMATION_SCHEMA.COLUMNS 
WHERE TABLE_NAME LIKE '#cand_test%'
ORDER BY ORDINAL_POSITION;