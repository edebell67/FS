-- Test script to run sp_seed_product_forex_dna with a specific bias and model count

-- Set seed_target_bias to 8
IF EXISTS (SELECT 1 FROM dbo.config WHERE config_name = 'seed_target_bias')
    UPDATE dbo.config SET config_value = '8' WHERE config_name = 'seed_target_bias';
ELSE
    INSERT INTO dbo.config (config_name, config_value) VALUES ('seed_target_bias', '8');

-- Set number_of_seed_model to 1
IF EXISTS (SELECT 1 FROM dbo.config WHERE config_name = 'number_of_seed_model')
    UPDATE dbo.config SET config_value = '1' WHERE config_name = 'number_of_seed_model';
ELSE
    INSERT INTO dbo.config (config_name, config_value) VALUES ('number_of_seed_model', '1');

-- Execute the stored procedure
EXEC dbo.sp_seed_product_forex_dna;
