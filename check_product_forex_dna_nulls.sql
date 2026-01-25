-- Check for NULL values in product_forex for DNA models
SELECT 
    product, 
    model, 
    target_profit, 
    target_loss
FROM dbo.product_forex
WHERE trade_freq = 99 
  AND (target_profit IS NULL OR target_loss IS NULL)