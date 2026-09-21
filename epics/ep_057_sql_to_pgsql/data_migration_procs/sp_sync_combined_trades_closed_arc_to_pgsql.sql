USE [tradedb]
GO

CREATE PROCEDURE [dbo].[sp_sync_combined_trades_closed_arc_to_pgsql]
AS
BEGIN
    SET NOCOUNT ON;

    DECLARE @max_last_update DATETIME;

    -- Get the max last_update from the PostgreSQL table
    BEGIN TRY
        SELECT @max_last_update = max_last_update
        FROM OPENQUERY(PGSQL_TRADEDB, 'SELECT MAX(last_update) AS max_last_update FROM combined_trades_closed_arc');
    END TRY
    BEGIN CATCH
        -- Handle case where the table is empty or another error occurs
        SET @max_last_update = NULL;
    END CATCH

    -- If the PostgreSQL table is empty, set a very old date
    IF @max_last_update IS NULL
    BEGIN
        SET @max_last_update = '1900-01-01';
    END

    -- Insert new records into the PostgreSQL table
    BEGIN TRY
        INSERT INTO OPENQUERY(PGSQL_TRADEDB, '
            SELECT
                guid, model, product, product_type, created, last_update, signal, entry_price, latest_price, entry_price2, latest_price2,
                trade_quantity, commission, target_profit, target_loss, rl_signal, tradeable, net_return, alt_net_return, pos_net_return_buy,
                pos_net_return_sell, trade_diff, RL_Check, percent_profit, percent_loss, buy_count, sell_count, linked, int_profit, int_profit_time,
                close_type, min_net_return, min_net_return_time, max_net_return, max_net_return_time, trade_reason, flip_trade
            FROM combined_trades_closed_arc')
        SELECT
            guid, model, product, product_type, created, last_update, signal, entry_price, latest_price, entry_price2, latest_price2,
            trade_quantity, commission, target_profit, target_loss, rl_signal, tradeable, net_return, alt_net_return, pos_net_return_buy,
            pos_net_return_sell, trade_diff, RL_Check, percent_profit, percent_loss, buy_count, sell_count, linked, int_profit, int_profit_time,
            close_type, min_net_return, min_net_return_time, max_net_return, max_net_return_time, trade_reason, flip_trade
        FROM dbo.combined_trades_closed_arc
        WHERE last_update > @max_last_update;

        PRINT 'Successfully synchronized combined_trades_closed_arc to PostgreSQL.';
    END TRY
    BEGIN CATCH
        PRINT 'Error synchronizing combined_trades_closed_arc to PostgreSQL.';
        -- You can add more detailed error logging here if needed
    END CATCH
END
GO
