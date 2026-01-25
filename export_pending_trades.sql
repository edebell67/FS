CREATE TRIGGER trg_ExportPendingTradeToCSV
ON tbl_rt_trades
AFTER INSERT
AS
BEGIN
    SET NOCOUNT ON;

    DECLARE 
        @product_type NVARCHAR(100),
        @signal NVARCHAR(100),
        @product NVARCHAR(100),
        @trade_guid NVARCHAR(100),
        @trade_status NVARCHAR(100),
        @trade_details NVARCHAR(MAX),
        @current_time NVARCHAR(20),
        @filename NVARCHAR(500),
        @csv_content NVARCHAR(MAX),
        @cmd NVARCHAR(2000);

    DECLARE pending_cursor CURSOR FOR
    SELECT product_type, signal, product, trade_guid, trade_status, trade_details
    FROM INSERTED
    WHERE execution_status = 'pending';

    OPEN pending_cursor;

    FETCH NEXT FROM pending_cursor INTO @product_type, @signal, @product, @trade_guid, @trade_status, @trade_details;

    WHILE @@FETCH_STATUS = 0
    BEGIN
        -- Get current timestamp formatted as YYYYMMDD_HHMMSS
        SET @current_time = FORMAT(GETDATE(), 'yyyyMMdd_HHmmss');

        -- Build filename
        SET @filename = 'C:\\users\\edebe\\eds\\trades_rt\\' + 
                        @product_type + '_' + 
                        @signal + '_' + 
                        @product + '_' + 
                        @current_time + '_' + 
                        @trade_guid + '_' + 
                        @trade_status + '.csv';

        -- Build CSV content line
        SET @csv_content = @current_time + ',' + @product + ',' + @signal + ',' + @trade_details;

        -- Escape double quotes in content (basic CSV escaping)
        SET @csv_content = REPLACE(@csv_content, '"', '""');

        -- Wrap content in double quotes if it contains commas or quotes
        IF CHARINDEX(',', @csv_content) > 0 OR CHARINDEX('"', @csv_content) > 0
            SET @csv_content = '"' + @csv_content + '"';

        -- Build command to echo content into file
        SET @cmd = 'echo ' + @csv_content + ' > "' + @filename + '"';

        -- Execute command
        EXEC xp_cmdshell @cmd;

        FETCH NEXT FROM pending_cursor INTO @product_type, @signal, @product, @trade_guid, @trade_status, @trade_details;
    END

    CLOSE pending_cursor;
    DEALLOCATE pending_cursor;
END;
