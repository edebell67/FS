USE tradedb_sim2;
GO

PRINT '--- STARTING LOOP DEBUG SCRIPT ---';

-- Hardcode the product to bypass the main cursor logic
DECLARE @currentproduct nvarchar(50) = 'gbpcad_c';

-- Configurable G-levels
DECLARE @buy_g_level nvarchar(50) = 'g2';
DECLARE @sell_g_level nvarchar(50) = 'g2';

-- Declare necessary variables
DECLARE @log_message_temp nvarchar(max);
DECLARE @nowtxt varchar(23);
DECLARE @now datetime2(3) = GETDATE();

-- Internal logic for the hardcoded product
SET @nowtxt  = CONVERT(varchar(23), GETDATE(), 121);
SET @log_message_temp = FORMATMESSAGE(N'[%s] sp_001_zone_distribution_trade >> DEBUG: Processing product: %s', @nowtxt, @currentproduct);
PRINT @log_message_temp;

-- Get zone data for the product
IF OBJECT_ID('tempdb..#zone_data') IS NOT NULL DROP TABLE #zone_data;
CREATE TABLE #zone_data (
    snapshot_time datetime2(3), product nvarchar(50),
    s_G9 float, s_G5 float, s_G4 float, s_G3 float, s_G2 float, s_G1 float,
    latest_price float,
    b_G1 float, b_G2 float, b_G3 float, b_G4 float, b_G5 float, b_G9 float
);
INSERT INTO #zone_data
SELECT TOP 2 [snapshot_time],[product],[s_G9],[s_G5],[s_G4],[s_G3],[s_G2],[s_G1],[latest_price],[b_G1],[b_G2],[b_G3],[b_G4],[b_G5],[b_G9]
FROM [dbo].[vw_201_zone_distribution_snapshots]
WHERE product=@currentproduct
ORDER BY snapshot_time DESC;

DECLARE @zone_row_count int = (SELECT COUNT(*) FROM #zone_data);
IF @zone_row_count < 2
BEGIN
    SET @nowtxt  = CONVERT(varchar(23), GETDATE(), 121);
    SET @log_message_temp = FORMATMESSAGE(N'[%s] sp_001_zone_distribution_trade >> Signal Generation: Not enough zone data (found %d rows) for product %s. No signals generated.', @nowtxt, @zone_row_count, @currentproduct);
    PRINT @log_message_temp;
    RETURN;
END;

-- Evaluate signals
DECLARE @current_b_g_val float, @previous_b_g_val float;
DECLARE @current_s_g_val float, @previous_s_g_val float;
DECLARE @latest_price_val float;

DECLARE @sql_select_current nvarchar(max);
SET @sql_select_current = N'SELECT TOP 1 @current_s_g_val = s_' + @buy_g_level + N', @current_b_g_val = b_' + @sell_g_level + N', @latest_price_val = latest_price FROM #zone_data ORDER BY snapshot_time DESC;';
EXEC sp_executesql @sql_select_current, N'@current_s_g_val float OUTPUT, @current_b_g_val float OUTPUT, @latest_price_val float OUTPUT', @current_s_g_val OUTPUT, @current_b_g_val OUTPUT, @latest_price_val OUTPUT;

DECLARE @sql_select_previous nvarchar(max);
SET @sql_select_previous = N'SELECT @previous_b_g_val = b_' + @sell_g_level + N', @previous_s_g_val = s_' + @buy_g_level + N' FROM #zone_data ORDER BY snapshot_time DESC OFFSET 1 ROW FETCH NEXT 1 ROW ONLY;';
EXEC sp_executesql @sql_select_previous, N'@previous_b_g_val float OUTPUT, @previous_s_g_val float OUTPUT', @previous_b_g_val OUTPUT, @previous_s_g_val OUTPUT;

SET @nowtxt  = CONVERT(varchar(23), GETDATE(), 121);
SET @log_message_temp = FORMATMESSAGE(N'[%s] sp_001_zone_distribution_trade >> Signal Generation: Current G-level values: s_%s=%s, b_%s=%s, latest_price=%s', @nowtxt, @buy_g_level, ISNULL(CAST(@current_s_g_val AS VARCHAR(20)), 'NULL'), @sell_g_level, ISNULL(CAST(@current_b_g_val AS VARCHAR(20)), 'NULL'), ISNULL(CAST(@latest_price_val AS VARCHAR(20)), 'NULL'));
PRINT @log_message_temp;

SET @nowtxt  = CONVERT(varchar(23), GETDATE(), 121);
SET @log_message_temp = FORMATMESSAGE(N'[%s] sp_001_zone_distribution_trade >> Signal Generation: Previous G-level values: s_%s=%s, b_%s=%s', @nowtxt, @buy_g_level, ISNULL(CAST(@previous_s_g_val AS VARCHAR(20)), 'NULL'), @sell_g_level, ISNULL(CAST(@previous_b_g_val AS VARCHAR(20)), 'NULL'));
PRINT @log_message_temp;

PRINT '--- ENDING LOOP DEBUG SCRIPT ---';
GO
