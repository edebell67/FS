-- Check #pf temporary table
SELECT 
    product, 
    model, 
    target_profit, 
    target_loss
FROM #pf
WHERE target_profit IS NULL OR target_loss IS NULL