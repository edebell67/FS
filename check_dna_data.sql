-- Let's check the data in the vw_product_forex_dna_expanded view
SELECT TOP 10 
    product, 
    model, 
    tp_pips, 
    sl_pips,
    leg_qty,
    side_pref
FROM dbo.vw_product_forex_dna_expanded
WHERE tp_pips IS NULL OR sl_pips IS NULL