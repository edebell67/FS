USE [tradedb]
GO
/****** Object:  StoredProcedure [dbo].[sp_9004_SetTrailingStopLossOnProfit]    Script Date: 15/11/2025 02:36:25 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE PROCEDURE [dbo].[sp_9004_SetTrailingStopLossOnProfit]
    @Model NVARCHAR(128)
AS
BEGIN
    SET NOCOUNT ON;

    DECLARE @RowsAffected INT = 0;
    DECLARE @sp_name SYSNAME = N'sp_9004_SetTrailingStopLossOnProfit';
    DECLARE @nowtxt VARCHAR(23) = CONVERT(VARCHAR(23), GETDATE(), 121);

    IF @Model IS NULL OR LTRIM(RTRIM(@Model)) = N''
    BEGIN
        RAISERROR(N'[%s] %s: Parameter @Model is required.', 10, 1, @nowtxt, @sp_name) WITH NOWAIT;
        RETURN;
    END;

    -- 2025-10-29: NEXT VERSION NUMBER - Load configuration values
    DECLARE @ProfitProtectPercent DECIMAL(18, 8);
    DECLARE @ProfitProtectTrigger DECIMAL(18, 8);
    DECLARE @ProfitProtectionListRaw NVARCHAR(MAX);

    SELECT @ProfitProtectPercent = TRY_CAST(config_value AS DECIMAL(18, 8)) FROM dbo.config WHERE config_name = 'profit_protect_percent';
    SELECT @ProfitProtectTrigger = TRY_CAST(config_value AS DECIMAL(18, 8)) FROM dbo.config WHERE config_name = 'profit_protect_trigger';
    SELECT @ProfitProtectionListRaw = config_value FROM dbo.config WHERE config_name = 'profit_protection_list';

    DECLARE @ProtectPercentText NVARCHAR(32) = CONVERT(NVARCHAR(32), @ProfitProtectPercent);
    DECLARE @ProtectTriggerText NVARCHAR(32) = CONVERT(NVARCHAR(32), @ProfitProtectTrigger);

    IF @ProfitProtectPercent IS NULL OR @ProfitProtectPercent <= 0
    BEGIN
        RAISERROR(N'[%s] %s: Configuration ''profit_protect_percent'' is missing or invalid. Aborting.', 10, 1, @nowtxt, @sp_name) WITH NOWAIT;
        RETURN;
    END;

    IF @ProfitProtectTrigger IS NULL OR @ProfitProtectTrigger <= 0
    BEGIN
        RAISERROR(N'[%s] %s: Configuration ''profit_protect_trigger'' is missing or invalid. Aborting.', 10, 1, @nowtxt, @sp_name) WITH NOWAIT;
        RETURN;
    END;

    IF @ProfitProtectionListRaw IS NULL OR LTRIM(RTRIM(@ProfitProtectionListRaw)) = N''
    BEGIN
        RAISERROR(N'[%s] %s: Configuration ''profit_protection_list'' is missing or empty. Aborting.', 10, 1, @nowtxt, @sp_name) WITH NOWAIT;
        RETURN;
    END;

    -- Parse profit_protection_list into a temporary table
    IF OBJECT_ID('tempdb..#ProfitProtectionTradeReasons') IS NOT NULL DROP TABLE #ProfitProtectionTradeReasons;
    CREATE TABLE #ProfitProtectionTradeReasons (trade_reason NVARCHAR(64) PRIMARY KEY);

    INSERT INTO #ProfitProtectionTradeReasons (trade_reason)
    SELECT TRIM(REPLACE(value, '''', '')) -- Trim whitespace and remove single quotes for robust matching
    FROM STRING_SPLIT(@ProfitProtectionListRaw, ',')
    WHERE LTRIM(RTRIM(value)) <> '';

    IF NOT EXISTS (SELECT 1 FROM #ProfitProtectionTradeReasons)
    BEGIN
        RAISERROR(N'[%s] %s: No valid trade reasons found in ''profit_protection_list''. Aborting.', 10, 1, @nowtxt, @sp_name) WITH NOWAIT;
        RETURN;
    END;

    RAISERROR(N'[%s] %s: Config loaded for model ''%s'': Percent=%s, Trigger=%s, List=''%s''.', 10, 1, @nowtxt, @sp_name, @Model, @ProtectPercentText, @ProtectTriggerText, @ProfitProtectionListRaw) WITH NOWAIT;

    -- Update target_loss for open trades that meet the criteria
    UPDATE cto
    SET
        cto.target_loss = (cto.max_net_return * @ProfitProtectPercent / 100) -- 2025-10-31: Corrected logic to set floor directly
    FROM

        dbo.combined_trades_open cto
    INNER JOIN
        #ProfitProtectionTradeReasons pptr ON cto.trade_reason = pptr.trade_reason
    WHERE

        cto.model = @Model

        AND cto.max_net_return >= @ProfitProtectTrigger -- 2025-10-31: Changed trigger to use max_net_return
        AND cto.max_net_return IS NOT NULL AND cto.max_net_return > 0 -- Ensure max_net_return is valid
        AND (
            cto.target_loss IS NULL
            OR
            -- Only trail up: new calculated target_loss must be HIGHER than current
            (cto.max_net_return * @ProfitProtectPercent / 100) > cto.target_loss -- 2025-10-31: Updated trailing check
        );

    SET @RowsAffected = @@ROWCOUNT;

    RAISERROR(N'[%s] %s: Adjusted trailing target_loss for %d open trade(s) for model ''%s''.', 10, 1, @nowtxt, @sp_name, @RowsAffected, @Model) WITH NOWAIT;



    IF OBJECT_ID('tempdb..#ProfitProtectionTradeReasons') IS NOT NULL DROP TABLE #ProfitProtectionTradeReasons;

END
GO
