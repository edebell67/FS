-- Let's check if there are any NULL values in the DNA model data
SELECT 
    dna.product, 
    dna.model, 
    dna.tp_pips, 
    dna.sl_pips
FROM dbo.vw_product_forex_dna_expanded dna
WHERE dna.tp_pips IS NULL OR dna.sl_pips IS NULL