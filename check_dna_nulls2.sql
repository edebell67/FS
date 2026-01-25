-- Check vw_product_forex_dna_expanded records with NULL values
SELECT 
    product, 
    model, 
    side_pref,
    leg_qty,
    tp_pips,
    sl_pips,
    max_legs
FROM dbo.vw_product_forex_dna_expanded
WHERE product IN (SELECT product FROM dbo.product_forex WHERE trade_freq = 99)
  AND (leg_qty IS NULL OR tp_pips IS NULL OR sl_pips IS NULL OR max_legs IS NULL)