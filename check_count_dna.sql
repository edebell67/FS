-- Check if there are any records with trade_freq = 99
SELECT COUNT(*) as count_records
FROM dbo.product_forex
WHERE trade_freq = 99