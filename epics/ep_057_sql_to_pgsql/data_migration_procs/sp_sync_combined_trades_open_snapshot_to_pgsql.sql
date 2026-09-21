USE [tradedb]
GO

CREATE PROCEDURE [dbo].[sp_sync_combined_trades_open_snapshot_to_pgsql]
AS
BEGIN
    SET NOCOUNT ON;

    -- Truncate the PostgreSQL table
    BEGIN TRY
        EXEC (N'TRUNCATE TABLE combined_trades_open_snapshot') AT PGSQL_TRADEDB;
    END TRY
    BEGIN CATCH
        PRINT 'Error truncating combined_trades_open_snapshot in PostgreSQL.';
        -- You can add more detailed error logging here if needed
        RETURN;
    END CATCH

    -- Insert new records into the PostgreSQL table
    BEGIN TRY
        INSERT INTO OPENQUERY(PGSQL_TRADEDB, '
            SELECT
                guid, model, product, product_type, created, last_update, signal, entry_price, latest_price, entry_price2, latest_price2,
                commission, target_profit, target_loss, rl_signal, tradeable, net_return, alt_net_return, pos_net_return_buy,
                pos_net_return_sell, trade_diff, RL_Check, percent_profit, percent_loss, buy_count, sell_count, linked, int_profit, int_profit_time,
                trade_quantity, min_net_return, min_net_return_time, max_net_return, max_net_return_time, trade_reason, flip_trade
            FROM combined_trades_open_snapshot')
        SELECT
            guid, model, product, product_type, created, last_update, signal, entry_price, latest_price, entry_price2, latest_price2,
            commission, target_profit, target_loss, rl_signal, tradeable, net_return, alt_net_return, pos_net_return_buy,
            pos_net_return_sell, trade_diff, RL_Check, percent_profit, percent_loss, buy_count, sell_count, linked, int_profit, int_profit_time,
            trade_quantity, min_net_return, min_net_return_time, max_net_return, max_net_return_time, trade_reason, flip_trade
        FROM dbo.vwCombined_trades_open;

        PRINT 'Successfully synchronized combined_trades_open_snapshot to PostgreSQL.';
    END TRY
    BEGIN CATCH
        PRINT 'Error synchronizing combined_trades_open_snapshot to PostgreSQL.';
        -- You can add more detailed error logging here if needed
    END CATCH
END
GO
