-- Check product_forex records with trade_freq = 99 and their DNA data
SELECT 
    product, 
    model, 
    trade_freq,
    dna_array,
    dna_json,
    CASE 
        WHEN dna_json IS NOT NULL THEN 'Has JSON'
        WHEN dna_array IS NOT NULL THEN 'Has Array'
        ELSE 'No DNA Data'
    END AS dna_data_type
FROM dbo.product_forex
WHERE trade_freq = 99