USE [tradedb];

SET NOCOUNT ON;
SET ANSI_PADDING ON;
SET ANSI_WARNINGS ON;
SET ARITHABORT ON;
SET CONCAT_NULL_YIELDS_NULL ON;
SET NUMERIC_ROUNDABORT OFF;
SET QUOTED_IDENTIFIER ON;
SET ANSI_NULLS ON;

DECLARE @trade_reason NVARCHAR(64) = N'test_json_export_recognizable';

DECLARE @test_payload TABLE (
    guid_label   NVARCHAR(50),
    guid_value   UNIQUEIDENTIFIER,
    product      NVARCHAR(50),
    signal_upper NVARCHAR(10),
    signal_lower NVARCHAR(10),
    model        NVARCHAR(64),
    trade_qty    INT,
    flip_flag    BIT
);

INSERT INTO @test_payload (guid_label, guid_value, product, signal_upper, signal_lower, model, trade_qty, flip_flag)
VALUES
    (N'54474250-4255-5930-3030-303030303031', CAST('54474250-4255-5930-3030-303030303031' AS UNIQUEIDENTIFIER),
        N'GBP',      N'BUY',  N'buy',  N'TEST_GBP',       100, 0),
    (N'54434846-5345-4C4C-3030-303030303031', CAST('54434846-5345-4C4C-3030-303030303031' AS UNIQUEIDENTIFIER),
        N'CHF',      N'SELL', N'sell', N'TEST_CHF',       100, 0),
    (N'54474250-4555-5253-3030-303030303031', CAST('54474250-4555-5253-3030-303030303031' AS UNIQUEIDENTIFIER),
        N'GBPEUR_S', N'SELL', N'sell', N'TEST_GBPEUR_S',  100, 0),
    (N'54474250-4555-5243-3030-303030303031', CAST('54474250-4555-5243-3030-303030303031' AS UNIQUEIDENTIFIER),
        N'GBPEUR_C', N'BUY',  N'buy',  N'TEST_GBPEUR_C',  100, 0),
    (N'54474250-4341-4453-4230-303030303031', CAST('54474250-4341-4453-4230-303030303031' AS UNIQUEIDENTIFIER),
        N'GBPCAD_S', N'BUY',  N'buy',  N'TEST_GBPCAD_S',  100, 0);

-- Cleanup prior test artefacts
DELETE FROM dbo.tbl_rt_trades
WHERE trade_guid IN (SELECT guid_value FROM @test_payload)
   OR TRY_CONVERT(NVARCHAR(64), trade_reason) = @trade_reason;

DELETE FROM dbo.combined_trades_closed
WHERE TRY_CONVERT(UNIQUEIDENTIFIER, guid) IN (SELECT guid_value FROM @test_payload);

DELETE FROM dbo.combined_trades_open
WHERE TRY_CONVERT(UNIQUEIDENTIFIER, guid) IN (SELECT guid_value FROM @test_payload);

-- Insert open trades (fires open trigger)
INSERT INTO dbo.combined_trades_open (
    guid, model, product, product_type, created, last_update,
    signal, entry_price, latest_price, commission,
    target_profit, target_loss, rl_signal, tradeable,
    net_return, alt_net_return, trade_quantity, flip_trade, trade_reason
)
SELECT
    guid_label,
    model,
    product,
    N'forex',
    GETDATE(),
    GETDATE(),
    signal_upper,
    1.2345,
    1.2345,
    0,
    10,
    -10,
    NULL,
    1,
    0,
    0,
    trade_qty,
    flip_flag,
    @trade_reason
FROM @test_payload;

-- Close trades via direct-close mode
DECLARE @product NVARCHAR(50);
DECLARE @signal_close NVARCHAR(10);

DECLARE trade_cursor CURSOR LOCAL FAST_FORWARD FOR
    SELECT product, signal_lower FROM @test_payload;

OPEN trade_cursor;
FETCH NEXT FROM trade_cursor INTO @product, @signal_close;

WHILE @@FETCH_STATUS = 0
BEGIN
    EXEC dbo.sp_003_CloseTradesTargetReached_refactored
        @product         = @product,
        @signal_to_close = @signal_close,
        @trade_reason    = @trade_reason,
        @close_count     = 1,
        @guid_to_close   = NULL;

    FETCH NEXT FROM trade_cursor INTO @product, @signal_close;
END;

CLOSE trade_cursor;
DEALLOCATE trade_cursor;

SELECT trade_guid, trade_status, execution_status, product, signal,
       TRY_CONVERT(NVARCHAR(64), trade_reason) AS trade_reason,
       trade_time
FROM dbo.tbl_rt_trades
WHERE TRY_CONVERT(NVARCHAR(64), trade_reason) = @trade_reason
ORDER BY trade_time DESC;

SELECT guid, tradeable
FROM dbo.combined_trades_closed
WHERE guid IN (SELECT guid_label FROM @test_payload);
