-- Insert sample data into strategy_side_current
INSERT INTO dbo.strategy_side_current (product, model, side)
SELECT DISTINCT pf.product, pf.model, 'BUY'
FROM dbo.product_forex pf
WHERE pf.trade_freq = 99
  AND pf.product = 'gbp'