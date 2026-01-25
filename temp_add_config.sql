-- Upsert script for adding/updating max_rt_group_quantity in dbo.config (Corrected)

IF NOT EXISTS (SELECT 1 FROM dbo.config WHERE config_name = 'max_rt_group_quantity')
BEGIN
    INSERT INTO dbo.config (config_name, config_value)
    VALUES ('max_rt_group_quantity', '100000');
    PRINT 'SUCCESS: Inserted max_rt_group_quantity into dbo.config.';
END
ELSE
BEGIN
    UPDATE dbo.config
    SET config_value = '100000'
    WHERE config_name = 'max_rt_group_quantity';
    PRINT 'SUCCESS: Updated max_rt_group_quantity in dbo.config.';
END
GO