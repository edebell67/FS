-- Check product_forex records with trade_freq = 99
SELECT 
    product, 
    model, 
    trade_freq,
    dna_array,
    dna_json
FROM dbo.product_forex
WHERE trade_freq = 99