USE [tradedb]
GO
/****** Object:  StoredProcedure [dbo].[sp_003_CloseTradesTargetReached_refactored]    Script Date: 15/11/2025 02:36:25 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE PROCEDURE [dbo].[sp_003_CloseTradesTargetReached_refactored]
    @product         NVARCHAR(50) = NULL,   -- optional: direct close mode
    @signal_to_close NVARCHAR(4)  = NULL,   -- 'buy' or 'sell'
    @trade_reason    NVARCHAR(64) = NULL,   -- e.g. 'sp_001_v6'
    @close_count     INT          = 1,      -- most-recent-first
    @guid_to_close UNIQUEIDENTIFIER = NULL  -- optional explicit guid
AS
BEGIN
    SET NOCOUNT ON;
    SET XACT_ABORT ON;

    DECLARE @sp_name    SYSNAME      = N'dbo.sp_003_CloseTradesTargetReached_refactored';
    DECLARE @run_id     BIGINT;
    DECLARE @updated_on NVARCHAR(19) = N'2025-09-15 16:30:00';

    DECLARE @is_sim_mode BIT;
    EXEC dbo.sp_helper_is_sim_db @is_sim_mode = @is_sim_mode OUTPUT;

    BEGIN TRY
        /* 0) Run start */
        INSERT INTO dbo.proc_run_log(sp_name) VALUES(@sp_name);
        SET @run_id = SCOPE_IDENTITY();

        /* ===========================================================
           === DIRECT CLOSE MODE (called from sp_001_v6)
           =========================================================== */
        IF @product IS NOT NULL AND @signal_to_close IS NOT NULL AND @trade_reason IS NOT NULL
        BEGIN
            -- normalize signal
            SET @signal_to_close = LOWER(@signal_to_close);
            IF @signal_to_close IN (N'b', N'buy')  SET @signal_to_close = N'buy';
            IF @signal_to_close IN (N's', N'sell') SET @signal_to_close = N'sell';            -- gather candidates (namespaced temp tables)
            DROP TABLE IF EXISTS #DC_ToClose;
            CREATE TABLE #DC_ToClose (
                guid UNIQUEIDENTIFIER PRIMARY KEY,
                close_type NVARCHAR(64) NOT NULL
            );

            IF @guid_to_close IS NOT NULL
            BEGIN
                INSERT INTO #DC_ToClose(guid, close_type)
                SELECT o.guid, N'direct_close_guid'
                FROM dbo.combined_trades_open AS o WITH (READPAST)
                WHERE o.guid = @guid_to_close;

                IF NOT EXISTS (SELECT 1 FROM #DC_ToClose)
                BEGIN
                    INSERT INTO dbo.trade_close_audit (sp_name, phase, flags)
                    VALUES (@sp_name, N'direct_mode', N'guid not found');

                    UPDATE dbo.proc_run_log
                    SET end_ts = GETDATE(),
                        rows_open = NULL,
                        rows_to_close = 0,
                        rows_closed = 0,
                        message = N'No open trade matching guid for direct close.'
                    WHERE run_id = @run_id;

                    RAISERROR(N'Direct-close: no matching open trade for guid.', 10, 1);
                    RETURN 1;
                END

                SET @close_count = 1;
            END
            ELSE
            BEGIN
                INSERT INTO #DC_ToClose(guid, close_type)
                SELECT TOP (@close_count)
                       o.guid, N'direct_close'
                FROM dbo.combined_trades_open AS o WITH (READPAST)
                WHERE o.product = @product
                  AND LOWER(o.signal) = @signal_to_close
                  AND o.trade_reason = @trade_reason
                  AND o.tradeable <> 0
                ORDER BY o.created DESC;

                IF NOT EXISTS (SELECT 1 FROM #DC_ToClose)
                BEGIN
                    INSERT INTO dbo.trade_close_audit (sp_name, phase, flags)
                    VALUES (@sp_name, N'direct_mode', N'no matches');

                    UPDATE dbo.proc_run_log
                    SET end_ts = GETDATE(),
                        rows_open = NULL,
                        rows_to_close = 0,
                        rows_closed = 0,
                        message = N'No matching open trades for direct close.'
                    WHERE run_id = @run_id;

                    RAISERROR(N'Direct-close: no matching open trades found.', 10, 1);
                    RETURN 1;
                END
            END

            -- dynamic column-intersection move (DC_* temp tables to avoid collisions)
            DECLARE @dc_has_close_type BIT = CASE WHEN EXISTS
                (SELECT 1 FROM sys.columns WHERE object_id = OBJECT_ID('dbo.combined_trades_closed') AND name = 'close_type') THEN 1 ELSE 0 END;

            DECLARE @dc_has_closed_ts BIT = CASE WHEN EXISTS
                (SELECT 1 FROM sys.columns WHERE object_id = OBJECT_ID('dbo.combined_trades_closed') AND name = 'closed_ts') THEN 1 ELSE 0 END;

            DROP TABLE IF EXISTS #DC_col_open;
            DROP TABLE IF EXISTS #DC_col_closed;
            SELECT name INTO #DC_col_open   FROM sys.columns WHERE object_id = OBJECT_ID('dbo.combined_trades_open');
            SELECT name INTO #DC_col_closed FROM sys.columns WHERE object_id = OBJECT_ID('dbo.combined_trades_closed');

            DROP TABLE IF EXISTS #DC_col_intersect;
            SELECT o.name AS col
            INTO #DC_col_intersect
            FROM #DC_col_open o
            INNER JOIN #DC_col_closed c ON c.name = o.name;

            DECLARE @dc_cols_csv NVARCHAR(MAX) =
                STUFF((
                    SELECT ',' + QUOTENAME(col)
                    FROM #DC_col_intersect
                    ORDER BY col
                    FOR XML PATH(''), TYPE).value('.', 'nvarchar(max)'), 1, 1, '');

            DECLARE @dc_select_cols_csv NVARCHAR(MAX) =
                STUFF((
                    SELECT ',' + CASE 
                                    WHEN col = 'tradeable' 
                                      THEN 'CASE WHEN o.[tradeable] = 2 THEN 3 ELSE o.[tradeable] END AS [tradeable]'
                                    ELSE 'o.' + QUOTENAME(col)
                                 END
                    FROM #DC_col_intersect
                    ORDER BY col
                    FOR XML PATH(''), TYPE).value('.', 'nvarchar(max)'), 1, 1, '');

            IF @dc_has_close_type = 1 SET @dc_cols_csv = @dc_cols_csv + N',[close_type]';
            IF @dc_has_closed_ts  = 1 SET @dc_cols_csv = @dc_cols_csv + N',[closed_ts]';

            DECLARE @dc_select_suffix NVARCHAR(MAX) = N'';
            IF @dc_has_close_type = 1 SET @dc_select_suffix = @dc_select_suffix + N', t.close_type';
            IF @dc_has_closed_ts  = 1 SET @dc_select_suffix = @dc_select_suffix + N', GETDATE()';

            BEGIN TRANSACTION;
                DECLARE @dc_sql_insert NVARCHAR(MAX) = N'
                    INSERT INTO dbo.combined_trades_closed (' + @dc_cols_csv + N')
                    SELECT ' + @dc_select_cols_csv + @dc_select_suffix + N'
                    FROM #DC_ToClose t
                    JOIN dbo.combined_trades_open o ON o.guid = t.guid;
                ';
                EXEC sp_executesql @dc_sql_insert;

                DECLARE @rows_closed_direct INT = @@ROWCOUNT;

                DELETE o
                FROM dbo.combined_trades_open o
                JOIN #DC_ToClose t ON t.guid = o.guid;
            COMMIT TRANSACTION;

            -- prepare debug + logging values to avoid inline conversions
            DECLARE @dc_rows_to_close INT = (SELECT COUNT(*) FROM #DC_ToClose);
            DECLARE @dbg_direct NVARCHAR(4000) =
                CONVERT(VARCHAR(23), GETDATE(), 121) +
                N' sp_003_close DIRECT: product=' + ISNULL(@product,N'NULL') +
                N'; signal=' + ISNULL(@signal_to_close,N'NULL') +
                N'; reason=' + ISNULL(@trade_reason,N'NULL') +
                N'; rows_to_close=' + ISNULL(CONVERT(NVARCHAR(20), @dc_rows_to_close), N'0') +
                N'; rows_closed=' + ISNULL(CONVERT(NVARCHAR(20), @rows_closed_direct), N'0');

            INSERT INTO dbo.trade_close_audit (sp_name, phase, flags)
            VALUES (@sp_name, N'direct_mode',
                    N'product=' + ISNULL(@product,N'NULL') +
                    N'; signal=' + ISNULL(@signal_to_close,N'NULL') +
                    N'; reason=' + ISNULL(@trade_reason,N'NULL') +
                    N'; closed=' + ISNULL(CONVERT(NVARCHAR(32),@rows_closed_direct),N'0'));

            UPDATE dbo.proc_run_log
            SET end_ts = GETDATE(),
                rows_open = NULL,
                rows_to_close = @dc_rows_to_close,
                rows_closed = @rows_closed_direct,
                message = N'Direct-close completed'
            WHERE run_id = @run_id;

            RAISERROR(@dbg_direct, 0, 1) WITH NOWAIT;

            DROP TABLE IF EXISTS #DC_ToClose, #DC_col_open, #DC_col_closed, #DC_col_intersect;
            RETURN 0;
        END

        /* ============================
           === NORMAL LOGIC (existing)
           ============================ */

        /* 1) Config */
        DECLARE @Expire_After        INT           = TRY_CAST((SELECT config_value FROM dbo.config WHERE config_name='EXPIRE') AS INT);
        DECLARE @CloseOnReverseBSI   INT           = TRY_CAST((SELECT config_value FROM dbo.config WHERE config_name='gbp_close_at_reverse_buysellindex') AS INT);
        DECLARE @ProfitScanEnabled   INT           = TRY_CAST((SELECT config_value FROM dbo.config WHERE config_name='profit_scan_enabled') AS INT);
        DECLARE @ProfitScanMinProfit DECIMAL(19,4) = TRY_CONVERT(DECIMAL(19,4), (SELECT config_value FROM dbo.config WHERE config_name='profit_scan_min_profit'));
        DECLARE @CloseAllTrades       INT           = TRY_CAST((SELECT config_value FROM dbo.config WHERE config_name='close_all_trades') AS INT);
        DECLARE @CloseAllTradeables   INT           = TRY_CAST((SELECT config_value FROM dbo.config WHERE config_name='close_all_tradeables') AS INT);
        IF @Expire_After        IS NULL SET @Expire_After        = 1800;  -- 30m
        IF @CloseOnReverseBSI   IS NULL SET @CloseOnReverseBSI   = 0;
        IF @ProfitScanEnabled   IS NULL SET @ProfitScanEnabled   = 0;
        IF @CloseAllTrades     IS NULL SET @CloseAllTrades     = 0;
        IF @CloseAllTradeables IS NULL SET @CloseAllTradeables = 0;
        IF @ProfitScanMinProfit IS NULL OR @ProfitScanMinProfit <= 0
        BEGIN
            SELECT @ProfitScanMinProfit = TRY_CONVERT(DECIMAL(19,4), config_value)
            FROM dbo.config
            WHERE config_name = 'scan_open_tradeable_profit_and_close';
        END
        IF @ProfitScanMinProfit IS NULL SET @ProfitScanMinProfit = 0.0;

        /* 1a) Daily hard close gate */
        DECLARE @trade_closed TIME(0) = TRY_CONVERT(TIME(0), (SELECT config_value FROM dbo.config WHERE config_name='trade_closed'));
        DECLARE @now_tod     TIME(0) = CONVERT(TIME(0), GETDATE());
        DECLARE @force_close_all BIT = CASE WHEN @is_sim_mode = 0 AND @trade_closed IS NOT NULL AND @now_tod >= @trade_closed THEN 1 ELSE 0 END;

        /* Log config */
        INSERT INTO dbo.trade_close_audit (sp_name, phase, flags)
        VALUES
        (
          @sp_name, N'config',
          N'EXPIRE=' + ISNULL(CONVERT(NVARCHAR(32),@Expire_After),N'NULL') + N';' +
          N'close_at_reverse_bsi=' + ISNULL(CONVERT(NVARCHAR(32),@CloseOnReverseBSI),N'NULL') + N';' +
          N'profit_scan_enabled=' + ISNULL(CONVERT(NVARCHAR(32),@ProfitScanEnabled),N'NULL') + N';' +
          N'profit_scan_min_profit=' + ISNULL(CONVERT(NVARCHAR(64),@ProfitScanMinProfit),N'NULL') + N';' +
          N'close_all_trades=' + ISNULL(CONVERT(NVARCHAR(1),@CloseAllTrades),N'0') + N';' +
          N'close_all_tradeables=' + ISNULL(CONVERT(NVARCHAR(1),@CloseAllTradeables),N'0') + N';' +
          N'trade_closed=' + ISNULL(CONVERT(VARCHAR(8),@trade_closed,108),N'NULL') + N';' +
          N'force_close_all=' + ISNULL(CONVERT(NVARCHAR(1),@force_close_all),N'0')
        );

        -- 2025-10-29: NEXT VERSION NUMBER - Profit protection is now handled after staging open trades.

        /* 2) Stage open trades (+ product flags) â€” DEDUPE LATEST PER GUID */
        DROP TABLE IF EXISTS #Open;

        ;WITH j AS (
            SELECT
                o.guid, o.model, o.product, o.product_type, o.created,
                o.last_update, o.signal,
                o.entry_price, o.latest_price, o.entry_price2, o.latest_price2,
                o.commission, o.target_profit, o.target_loss, o.rl_signal, o.tradeable,
                o.net_return, o.alt_net_return, o.pos_net_return_buy, o.pos_net_return_sell,
                o.trade_diff, o.RL_Check, o.percent_profit, o.percent_loss,
                o.buy_count, o.sell_count, o.linked, o.int_profit, o.int_profit_time,
                o.trade_quantity, o.min_net_return, o.min_net_return_time,
                o.max_net_return, o.max_net_return_time, o.trade_reason, o.flip_trade,
                actual_net = TRY_CONVERT(DECIMAL(19,4),
                             CASE WHEN o.flip_trade IS NULL THEN NULL
                                  WHEN o.flip_trade = 0     THEN o.net_return
                                  WHEN o.flip_trade = 1     THEN o.alt_net_return
                             END),
                pf.use_target_exit_only, pf.mapto_tradezone, pf.multi_close_option,
                ROW_NUMBER() OVER (
                    PARTITION BY o.guid
                    ORDER BY COALESCE(o.last_update, o.created) DESC, o.created DESC
                ) AS rn
            FROM dbo.combined_trades_open AS o
            INNER JOIN dbo.product_forex   AS pf ON pf.model = o.model
        )
        SELECT
            guid, model, product, product_type, created,
            last_update, signal,
            entry_price, latest_price, entry_price2, latest_price2,
            commission, target_profit, target_loss, rl_signal, tradeable,
            net_return, alt_net_return, pos_net_return_buy, pos_net_return_sell,
            trade_diff, RL_Check, percent_profit, percent_loss,
            buy_count, sell_count, linked, int_profit, int_profit_time,
            trade_quantity, min_net_return, min_net_return_time,
            max_net_return, max_net_return_time, trade_reason, flip_trade,
            actual_net,
            use_target_exit_only, mapto_tradezone, multi_close_option
        INTO #Open
        FROM j
        WHERE rn = 1;

        /* Safety: verify dedupe worked before unique index */
        IF EXISTS (SELECT 1 FROM #Open GROUP BY guid HAVING COUNT(*) > 1)
        BEGIN
            RAISERROR(N'Duplicate guid remained in #Open after de-dupe; investigate source joins.', 16, 1);
            RETURN;
        END

        CREATE UNIQUE CLUSTERED INDEX IX_Open_guid ON #Open(guid);

        -- 2025-10-31: Call sp_9004 for each model to apply profit protection
        DECLARE @model_cursor CURSOR;
        DECLARE @model_name NVARCHAR(128);
        SET @model_cursor = CURSOR FOR SELECT DISTINCT model FROM #Open;
        OPEN @model_cursor;
        FETCH NEXT FROM @model_cursor INTO @model_name;
        WHILE @@FETCH_STATUS = 0
        BEGIN
            EXEC dbo.sp_9004_SetTrailingStopLossOnProfit @Model = @model_name;
            FETCH NEXT FROM @model_cursor INTO @model_name;
        END
        CLOSE @model_cursor;
        DEALLOCATE @model_cursor;

        DECLARE @rows_open INT = (SELECT COUNT(*) FROM #Open);

        /* 3) Current & previous snapshot per product */
        DROP TABLE IF EXISTS #Snap;
        ;WITH S AS (
            SELECT
                v.Product,
                v.tradezone,
                v.BuySellIndex AS bsi,
                v.SnapshotTimestamp,
                v.SnapshotID,
                ROW_NUMBER() OVER (PARTITION BY v.Product ORDER BY v.SnapshotTimestamp DESC, v.SnapshotID DESC) AS rn
            FROM dbo.vw_002_pos_buy_sell_count_gbp_tradepoint_signal AS v
        )
        SELECT p.Product,
               c.tradezone     AS curr_tradezone,
               c.bsi           AS curr_bsi,
               pS.bsi          AS prev_bsi
        INTO #Snap
        FROM (SELECT DISTINCT Product FROM #Open) AS p
        LEFT JOIN S  AS c  ON c.Product  = p.Product AND c.rn  = 1
        LEFT JOIN S  AS pS ON pS.Product = p.Product AND pS.rn = 2;

        CREATE UNIQUE CLUSTERED INDEX IX_Snap_Product ON #Snap(Product);



        DROP TABLE IF EXISTS #SigClose;
        CREATE TABLE #SigClose (guid UNIQUEIDENTIFIER PRIMARY KEY);

        IF OBJECT_ID('dbo.sp_9002_CheckTradeSignalForClosure','P') IS NOT NULL
        BEGIN
            DECLARE @g UNIQUEIDENTIFIER, @m VARCHAR(50), @s VARCHAR(10), @Close BIT;

            DECLARE cur CURSOR LOCAL FAST_FORWARD FOR
                SELECT o.guid, o.model, o.signal
        FROM #Open AS o
                WHERE o.multi_close_option = 'close_on_signal_change'
                  AND ISNULL(o.use_target_exit_only,0) = 0;

            OPEN cur;
            FETCH NEXT FROM cur INTO @g, @m, @s;
            WHILE @@FETCH_STATUS = 0
            BEGIN
                SET @Close = 0;
                EXEC dbo.sp_9002_CheckTradeSignalForClosure
                    @OpenTradeGuid = @g,
                    @Model         = @m,
                    @IncomingSignal= @s,
                    @CloseTrade    = @Close OUTPUT;

                INSERT INTO dbo.trade_close_audit(sp_name, phase, guid, flags)
                VALUES(@sp_name, N'signal_check', @g, N'close_on_signal_change=' + ISNULL(CONVERT(NVARCHAR(1),@Close),N'0'));

                IF @Close = 1
                    INSERT INTO #SigClose(guid) VALUES(@g);

                FETCH NEXT FROM cur INTO @g, @m, @s;
            END
            CLOSE cur; DEALLOCATE cur;
        END
        ELSE
        BEGIN
            INSERT INTO dbo.trade_close_audit(sp_name, phase, flags)
            VALUES(@sp_name, N'signal_check', N'sp_9002 missing');
        END

        /* 5) Profit scan (global) */
        DROP TABLE IF EXISTS #ProfitScanClose;
        CREATE TABLE #ProfitScanClose (guid UNIQUEIDENTIFIER PRIMARY KEY);

        IF @ProfitScanEnabled = 1 AND @ProfitScanMinProfit > 0
        BEGIN
            DECLARE @ProfitScanTotal DECIMAL(19,4);

            SELECT @ProfitScanTotal = SUM(actual_net)
            FROM #Open
            WHERE tradeable > 0
              AND flip_trade IS NOT NULL
              AND actual_net IS NOT NULL
              AND UPPER(signal) IN ('B','BUY','S','SELL');

            SET @ProfitScanTotal = ISNULL(@ProfitScanTotal, 0);

            INSERT INTO dbo.trade_close_audit(sp_name, phase, flags)
            VALUES(@sp_name, N'profit_scan',
                   N'enabled=1; threshold=' + CONVERT(NVARCHAR(32), @ProfitScanMinProfit) +
                   N'; total=' + CONVERT(NVARCHAR(32), @ProfitScanTotal));

            IF @ProfitScanTotal >= @ProfitScanMinProfit
            BEGIN
                INSERT INTO #ProfitScanClose(guid)
                SELECT guid
                FROM #Open
                WHERE tradeable > 0
                  AND flip_trade IS NOT NULL
                  AND actual_net IS NOT NULL
                  AND UPPER(signal) IN ('B','BUY','S','SELL');
            END
        END
        ELSE
        BEGIN
            INSERT INTO dbo.trade_close_audit(sp_name, phase, flags)
            VALUES(@sp_name, N'profit_scan', N'enabled=' + CONVERT(NVARCHAR(1), ISNULL(@ProfitScanEnabled,0))
                   + N'; threshold=' + ISNULL(CONVERT(NVARCHAR(32), @ProfitScanMinProfit), N'0'));
        END

        /* 6) Decide which to close */
        DROP TABLE IF EXISTS #ToClose;
        CREATE TABLE #ToClose (
            guid UNIQUEIDENTIFIER PRIMARY KEY,
            close_type NVARCHAR(64) NOT NULL
        );

        IF ISNULL(@CloseAllTrades,0) = 1
        BEGIN
            INSERT INTO #ToClose (guid, close_type)
            SELECT o.guid, N'close_all_trades'
            FROM #Open AS o
            WHERE NOT EXISTS (SELECT 1 FROM #ToClose t WHERE t.guid = o.guid);
        END

        IF ISNULL(@CloseAllTradeables,0) = 1
        BEGIN
            INSERT INTO #ToClose (guid, close_type)
            SELECT o.guid, N'close_all_tradeables'
            FROM #Open AS o
            WHERE o.tradeable > 0
              AND NOT EXISTS (SELECT 1 FROM #ToClose t WHERE t.guid = o.guid);
        END

        INSERT INTO #ToClose (guid, close_type)
        SELECT
            o.guid,
            close_type =
                CASE
                    WHEN psc.guid IS NOT NULL THEN 'profit scan exceeded'
                    WHEN CAST(o.net_return AS FLOAT) > CAST(o.target_profit AS FLOAT)
                      OR CAST(o.net_return AS FLOAT) < CAST(o.target_loss  AS FLOAT)
                    THEN 'target reached'
                    WHEN o.tradeable = 0
                         AND DATEDIFF(SECOND, o.created, GETDATE()) > @Expire_After
                    THEN 'Expired'
                    WHEN o.mapto_tradezone = 1 AND o.tradeable <> 0 AND s.curr_tradezone IS NULL
                    THEN 'zone ended'
                    WHEN o.mapto_tradezone = 1 AND o.tradeable <> 0 AND s.curr_tradezone IS NOT NULL AND s.curr_tradezone <> o.signal
                    THEN 'zone flip'
                    WHEN @CloseOnReverseBSI = 1 AND s.curr_tradezone IS NULL
                         AND s.prev_bsi IS NOT NULL AND s.curr_bsi IS NOT NULL
                         AND ((s.prev_bsi > 0 AND s.curr_bsi < 0) OR (s.prev_bsi < 0 AND s.curr_bsi > 0))
                    THEN 'reverse BSI'
                    WHEN sc.guid IS NOT NULL
                    THEN 'signal change'
                    ELSE 'unknown'
                END
        FROM #Open AS o
        LEFT JOIN #Snap            AS s   ON s.Product = o.product
        LEFT JOIN #SigClose        AS sc  ON sc.guid   = o.guid
        LEFT JOIN #ProfitScanClose AS psc ON psc.guid  = o.guid
        WHERE (
              psc.guid IS NOT NULL
           OR (
                ISNULL(o.use_target_exit_only,0) = 1
                AND (CAST(o.net_return AS FLOAT) > CAST(o.target_profit AS FLOAT)
                     OR CAST(o.net_return AS FLOAT) < CAST(o.target_loss  AS FLOAT))
              )
           OR (
                ISNULL(o.use_target_exit_only,0) = 0
                AND (
                       CAST(o.net_return AS FLOAT) > CAST(o.target_profit AS FLOAT)
                    OR CAST(o.net_return AS FLOAT) < CAST(o.target_loss  AS FLOAT)
                    OR (o.tradeable = 0 AND DATEDIFF(SECOND, o.created, GETDATE()) > @Expire_After)
                    OR (o.mapto_tradezone = 1 AND o.tradeable <> 0 AND s.curr_tradezone IS NULL)
                    OR (o.mapto_tradezone = 1 AND o.tradeable <> 0 AND s.curr_tradezone IS NOT NULL AND s.curr_tradezone <> o.signal)
                    OR (@CloseOnReverseBSI = 1 AND s.curr_tradezone IS NULL
                        AND s.prev_bsi IS NOT NULL AND s.curr_bsi IS NOT NULL
                        AND ((s.prev_bsi > 0 AND s.curr_bsi < 0) OR (s.prev_bsi < 0 AND s.curr_bsi > 0)))
                    OR (sc.guid IS NOT NULL)
                   )
            )
)
          AND NOT EXISTS (SELECT 1 FROM #ToClose t WHERE t.guid = o.guid);

        /* 6a) Hard daily close */
        IF @force_close_all = 1
        BEGIN
            INSERT INTO #ToClose (guid, close_type)
            SELECT o.guid, N'trade window closed'
        FROM #Open AS o
            WHERE NOT EXISTS (SELECT 1 FROM #ToClose t WHERE t.guid = o.guid);
        END

        /* 6b) Persistent candidate logging */
        INSERT INTO dbo.trade_close_audit
        (
          sp_name, phase, guid, close_type, product, model, signal,
          tradeable, use_target_exit_only, mapto_tradezone, multi_close_option,
          net_return, target_profit, target_loss, created, last_update, age_seconds,
          curr_tradezone, curr_bsi, prev_bsi,
          flags
        )
        SELECT
          @sp_name, N'candidate', o.guid, t.close_type, o.product, o.model, o.signal,
          o.tradeable, o.use_target_exit_only, o.mapto_tradezone, o.multi_close_option,
          TRY_CONVERT(decimal(19,4),o.net_return),
          TRY_CONVERT(decimal(19,4),o.target_profit),
          TRY_CONVERT(decimal(19,4),o.target_loss),
          o.created, o.last_update, DATEDIFF(SECOND, o.created, GETDATE()),
          s.curr_tradezone, s.curr_bsi, s.prev_bsi,
          N'profit_scan=' + CASE WHEN psc.guid IS NOT NULL THEN N'1' ELSE N'0' END + N';' +
          N'sig_change='  + CASE WHEN sc.guid  IS NOT NULL THEN N'1' ELSE N'0' END + N';' +
          N'reverse_bsi=' + CASE WHEN (@CloseOnReverseBSI = 1 AND s.curr_tradezone IS NULL
                                        AND s.prev_bsi IS NOT NULL AND s.curr_bsi IS NOT NULL
                                        AND ((s.prev_bsi > 0 AND s.curr_bsi < 0) OR (s.prev_bsi < 0 AND s.curr_bsi > 0)))
                                  THEN N'1' ELSE N'0' END
        FROM #ToClose AS t
        JOIN #Open    AS o   ON o.guid   = t.guid
        LEFT JOIN #Snap AS s ON s.Product= o.product
        LEFT JOIN #SigClose AS sc ON sc.guid = o.guid
        LEFT JOIN #ProfitScanClose AS psc ON psc.guid = o.guid;

        /* 7) CLOSE TRADES â€” ATOMIC BLOCK */
        DECLARE @has_close_type_n BIT = CASE WHEN EXISTS
            (SELECT 1 FROM sys.columns WHERE object_id = OBJECT_ID('dbo.combined_trades_closed') AND name = 'close_type') THEN 1 ELSE 0 END;

        DECLARE @has_closed_ts_n BIT = CASE WHEN EXISTS
            (SELECT 1 FROM sys.columns WHERE object_id = OBJECT_ID('dbo.combined_trades_closed') AND name = 'closed_ts') THEN 1 ELSE 0 END;

        DROP TABLE IF EXISTS #col_open;
        DROP TABLE IF EXISTS #col_closed;
        SELECT name INTO #col_open   FROM sys.columns WHERE object_id = OBJECT_ID('dbo.combined_trades_open');
        SELECT name INTO #col_closed FROM sys.columns WHERE object_id = OBJECT_ID('dbo.combined_trades_closed');

        DROP TABLE IF EXISTS #col_intersect;
        SELECT o.name AS col
        INTO #col_intersect
        FROM #col_open o
        INNER JOIN #col_closed c ON c.name = o.name;

        DECLARE @cols_csv NVARCHAR(MAX) =
            STUFF((
                SELECT ',' + QUOTENAME(col)
                FROM #col_intersect
                ORDER BY col
                FOR XML PATH(''), TYPE).value('.', 'nvarchar(max)'), 1, 1, '');

        DECLARE @select_cols_csv NVARCHAR(MAX) =
            STUFF((
                SELECT ',' + CASE 
                                WHEN col = 'tradeable' 
                                  THEN 'CASE WHEN o.[tradeable] = 2 THEN 3 ELSE o.[tradeable] END AS [tradeable]'
                                ELSE 'o.' + QUOTENAME(col)
                             END
                FROM #col_intersect
                ORDER BY col
                FOR XML PATH(''), TYPE).value('.', 'nvarchar(max)'), 1, 1, '');

        IF @has_close_type_n = 1 SET @cols_csv = @cols_csv + N',[close_type]';
        IF @has_closed_ts_n  = 1 SET @cols_csv = @cols_csv + N',[closed_ts]';

        DECLARE @select_suffix NVARCHAR(MAX) = N'';
        IF @has_close_type_n = 1 SET @select_suffix = @select_suffix + N', t.close_type';
        IF @has_closed_ts_n  = 1 SET @select_suffix = @select_suffix + N', GETDATE()';

        BEGIN TRANSACTION;  -- atomic move open -> closed
            DECLARE @sql_insert NVARCHAR(MAX) = N'
                INSERT INTO dbo.combined_trades_closed (' + @cols_csv + N')
                SELECT ' + @select_cols_csv + @select_suffix + N'
                FROM #ToClose t
                JOIN dbo.combined_trades_open o ON o.guid = t.guid;
            ';
            EXEC sp_executesql @sql_insert;

            DECLARE @rows_closed INT = @@ROWCOUNT;

            DELETE o
            FROM dbo.combined_trades_open o
            JOIN #ToClose t ON t.guid = o.guid;
        COMMIT TRANSACTION;

        /* 8) Summary logging */
        DECLARE @rows_to_close INT = (SELECT COUNT(*) FROM #ToClose);
        DECLARE @dbgfinal NVARCHAR(4000) =
            CONVERT(VARCHAR(23), GETDATE(), 121) +
            N' sp_003_close rows_open=' + ISNULL(CONVERT(NVARCHAR(20),@rows_open),N'0') +
            N'; rows_to_close=' + ISNULL(CONVERT(NVARCHAR(20),@rows_to_close),N'0') +
            N'; rows_closed=' + ISNULL(CONVERT(NVARCHAR(20),@rows_closed),N'0') +
            N'; updated=' + @updated_on;

        INSERT INTO dbo.trade_close_audit(sp_name, phase, flags)
        VALUES(@sp_name, N'summary',
               N'rows_open=' + ISNULL(CONVERT(NVARCHAR(32),@rows_open),N'0') +
               N'; rows_to_close=' + ISNULL(CONVERT(NVARCHAR(32),@rows_to_close),N'0') +
               N'; rows_closed=' + ISNULL(CONVERT(NVARCHAR(32),@rows_closed),N'0'));

        UPDATE dbo.proc_run_log
        SET end_ts = GETDATE(),
            rows_open = @rows_open,
            rows_to_close = @rows_to_close,
            rows_closed = @rows_closed,
            message = NULL
        WHERE run_id = @run_id;

        RAISERROR(@dbgfinal, 0, 1) WITH NOWAIT;

        /* 9) Cleanup */
        DROP TABLE IF EXISTS #ToClose, #ProfitScanClose, #SigClose, #Snap, #Open, #col_open, #col_closed, #col_intersect;

        RETURN 0;

    END TRY
    BEGIN CATCH
        IF XACT_STATE() <> 0 ROLLBACK TRANSACTION;

        DECLARE @err_msg NVARCHAR(2048) = ERROR_MESSAGE();
        DECLARE @err_num INT = ERROR_NUMBER();
        DECLARE @err_line INT = ERROR_LINE();
        DECLARE @err_state INT = ERROR_STATE();

        BEGIN TRY
            INSERT INTO dbo.trade_close_audit(sp_name, phase, flags)
            VALUES(@sp_name, N'error',
                   N'msg=' + ISNULL(@err_msg,N'') +
                   N'; num=' + CONVERT(NVARCHAR(16),@err_num) +
                   N'; line=' + CONVERT(NVARCHAR(16),@err_line) +
                   N'; state=' + CONVERT(NVARCHAR(16),@err_state));
        END TRY
        BEGIN CATCH
            -- swallow logging failure
        END CATCH

        IF @run_id IS NOT NULL
        BEGIN TRY
            UPDATE dbo.proc_run_log
            SET end_ts = GETDATE(),
                message = N'ERROR: ' + ISNULL(@err_msg,N'')
            WHERE run_id = @run_id;
        END TRY
        BEGIN CATCH
            -- swallow logging failure
        END CATCH

        RAISERROR(@err_msg, 16, 1);
        RETURN 1;
    END CATCH
END

GO
