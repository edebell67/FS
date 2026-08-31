-- Adds EP051 strategy rank-position capture as a gated step (every ~30
-- minutes) inside the live sp_loop_create_trades_v2 loop, replacing the
-- standalone Python process (scripts/capture_strategy_rank_history.py /
-- live_01_run_ep051_rank_history.bat). Follows the exact pattern already
-- in production for usp_ep051_refresh_export_cache: a skip_* config flag,
-- a run-log-based cadence gate, and the same TRY/CATCH + RAISERROR
-- logging shape used by every other step in this loop.
--
-- Requires sp_capture_strategy_rank_history.sql
-- (usp_ep051_capture_strategy_rank_history + dbo.ep051_rank_capture_run_log)
-- to already be deployed.
--
-- IMPORTANT: sp_loop_create_trades_v2 is a single long-running WHILE 1=1
-- execution, not re-invoked per iteration - this CREATE OR ALTER changes
-- the stored *definition* only. It does NOT affect the currently running
-- live instance of the loop; the new step only takes effect the next time
-- the loop process is restarted. Do not restart the live trading loop to
-- pick this up without explicit operator go-ahead - it is the core
-- trade-creation process for the live system.
--
-- Full body below is the live definition fetched via OBJECT_DEFINITION()
-- on 2026-08-31, with only the @skip_ep051_rank_capture flag (declaration
-- + config load) and the new capture block (inserted immediately before
-- the loop's WAITFOR DELAY) added - no other line changed.

CREATE OR ALTER     PROCEDURE [dbo].[sp_loop_create_trades_v2]
AS
BEGIN
    SET NOCOUNT ON;

    DECLARE 
        @tag      SYSNAME       = N'sp_loop_create_trades',
        @version  NVARCHAR(32)  = N'v2.11 B-first+v1..v704/v92+v9fup',
        @ts       NVARCHAR(23),
        @msg      NVARCHAR(4000),
        @iter     BIGINT        = 0,
        @LoopDelay VARCHAR(8)   = '00:01',

        @skip_001_v1   INT,
        @skip_001_v2   INT,
        @skip_001_v3   INT,
        @skip_001_v4   INT,
        @skip_001_v5   INT,
        @skip_001_v6   INT,
        @skip_001_v7   INT,
        @skip_001_v701 INT,
        @skip_001_v702 INT,
        @skip_001_v703 INT,
        @skip_001_v704 INT,
        @skip_001_v8   INT,
        @skip_001_v91  INT,
        @skip_001_v92  INT,
        @skip_001_v9_followup INT,
        @skip_breakout_entry INT,
		@skip_001_buy_sell INT,
        @skip_001_zone INT, -- Added 2025-10-29
        @skip_800_exec INT,
        @skip_001_brk INT,
        @skip_001_create_trades_v9_setbased INT,
        @skip_ep051_export_cache INT,
        @skip_ep051_rank_capture INT

    /* load config flags (treat NULL as 0 later) */
    SELECT @skip_001_v1   = TRY_CAST(config_value AS INT) FROM dbo.config WHERE config_name='skip_001_v1';
    SELECT @skip_001_v2   = TRY_CAST(config_value AS INT) FROM dbo.config WHERE config_name='skip_001_v2';
    SELECT @skip_001_v3   = TRY_CAST(config_value AS INT) FROM dbo.config WHERE config_name='skip_001_v3';
    SELECT @skip_001_v4   = TRY_CAST(config_value AS INT) FROM dbo.config WHERE config_name='skip_001_v4';
    SELECT @skip_001_v5   = TRY_CAST(config_value AS INT) FROM dbo.config WHERE config_name='skip_001_v5';
    SELECT @skip_001_v6   = TRY_CAST(config_value AS INT) FROM dbo.config WHERE config_name='skip_001_v6';
    SELECT @skip_001_v7   = TRY_CAST(config_value AS INT) FROM dbo.config WHERE config_name='skip_001_v7';
    SELECT @skip_001_v701 = TRY_CAST(config_value AS INT) FROM dbo.config WHERE config_name='skip_001_v701';
    SELECT @skip_001_v702 = TRY_CAST(config_value AS INT) FROM dbo.config WHERE config_name='skip_001_v702';
    SELECT @skip_001_v703 = TRY_CAST(config_value AS INT) FROM dbo.config WHERE config_name='skip_001_v703';
    SELECT @skip_001_v704 = TRY_CAST(config_value AS INT) FROM dbo.config WHERE config_name='skip_001_v704';
    SELECT @skip_001_v8   = TRY_CAST(config_value AS INT) FROM dbo.config WHERE config_name='skip_001_v8';
    SELECT @skip_001_v91  = TRY_CAST(config_value AS INT) FROM dbo.config WHERE config_name='skip_001_v91';
    SELECT @skip_001_v92  = TRY_CAST(config_value AS INT) FROM dbo.config WHERE config_name='skip_001_v92';
    SELECT @skip_001_v9_followup = TRY_CAST(config_value AS INT) FROM dbo.config WHERE config_name='skip_001_v9_followup';
    SELECT @skip_breakout_entry = TRY_CAST(config_value AS INT) FROM dbo.config WHERE config_name='skip_breakout_entry';
    SELECT @skip_001_buy_sell = TRY_CAST(config_value AS INT) FROM dbo.config WHERE config_name='skip_001_buy_sell';
    SELECT @skip_001_zone = TRY_CAST(config_value AS INT) FROM dbo.config WHERE config_name='skip_001_zone'; -- Added 2025-10-29
    SELECT @skip_800_exec = TRY_CAST(config_value AS INT) FROM dbo.config WHERE config_name='skip_800_exec';
    SELECT @skip_001_brk = TRY_CAST(config_value AS INT) FROM dbo.config WHERE config_name='skip_001_brk';
    SELECT @skip_001_create_trades_v9_setbased = TRY_CAST(config_value AS INT) FROM dbo.config WHERE config_name='skip_001_create_trades_v9_setbased';
    SELECT @skip_ep051_export_cache = TRY_CAST(config_value AS INT) FROM dbo.config WHERE config_name='skip_ep051_export_cache';
    SELECT @skip_ep051_rank_capture = TRY_CAST(config_value AS INT) FROM dbo.config WHERE config_name='skip_ep051_rank_capture';


    WHILE 1=1
    BEGIN
        /* iteration banner + version */
        SET @iter += 1;
        SET @ts  = CONVERT(NVARCHAR(23), GETDATE(), 121);
        SET @msg = @ts + N' ' + @tag + N' ' + @version + N' iteration=' + CONVERT(NVARCHAR(20), @iter);
        RAISERROR(@msg, 10, 1) WITH NOWAIT;

        /* ===================== B) UPDATE/CLOSE (RUN FIRST) ===================== */
        SET @ts  = CONVERT(NVARCHAR(23), GETDATE(), 121);
        SET @msg = @ts + N' ' + @tag + N' --- B-first (update+close) start ---';
        RAISERROR(@msg, 10, 1) WITH NOWAIT;

        BEGIN TRY
            EXEC dbo.sp_002_UpdateCombinedTradesOpen;
            SET @ts  = CONVERT(NVARCHAR(23), GETDATE(), 121);
            SET @msg = @ts + N' ' + @tag + N' sp_002_UpdateCombinedTradesOpen OK';
            RAISERROR(@msg, 10, 1) WITH NOWAIT;
        END TRY
        BEGIN CATCH
            SET @ts  = CONVERT(NVARCHAR(23), GETDATE(), 121);
            SET @msg = @ts + N' ' + @tag + N' sp_002_UpdateCombinedTradesOpen ERROR'
                     + N' num='   + CONVERT(NVARCHAR(20), ERROR_NUMBER())
                     + N' sev='   + CONVERT(NVARCHAR(20), ERROR_SEVERITY())
                     + N' state=' + CONVERT(NVARCHAR(20), ERROR_STATE())
                     + N' line='  + CONVERT(NVARCHAR(20), ERROR_LINE())
                     + N' proc='  + ISNULL(ERROR_PROCEDURE(), N'NULL')
                     + N' msg='   + ERROR_MESSAGE();
            RAISERROR(@msg, 16, 1) WITH NOWAIT;
        END CATCH;

        BEGIN TRY
            EXEC dbo.sp_003_CloseTradesTargetReached_refactored;
            SET @ts  = CONVERT(NVARCHAR(23), GETDATE(), 121);
            SET @msg = @ts + N' ' + @tag + N' sp_003_CloseTradesTargetReached_refactored OK';
            RAISERROR(@msg, 10, 1) WITH NOWAIT;
        END TRY
        BEGIN CATCH
            SET @ts  = CONVERT(NVARCHAR(23), GETDATE(), 121);
            SET @msg = @ts + N' ' + @tag + N' sp_003_CloseTradesTargetReached_refactored ERROR'
                     + N' num='   + CONVERT(NVARCHAR(20), ERROR_NUMBER())
                     + N' sev='   + CONVERT(NVARCHAR(20), ERROR_SEVERITY())
                     + N' state=' + CONVERT(NVARCHAR(20), ERROR_STATE())
                     + N' line='  + CONVERT(NVARCHAR(20), ERROR_LINE())
                     + N' proc='  + ISNULL(ERROR_PROCEDURE(), N'NULL')
                     + N' msg='   + ERROR_MESSAGE();
            RAISERROR(@msg, 16, 1) WITH NOWAIT;
        END CATCH;

        SET @ts  = CONVERT(NVARCHAR(23), GETDATE(), 121);
        SET @msg = @ts + N' ' + @tag + N' --- B-first end ---';
        RAISERROR(@msg, 10, 1) WITH NOWAIT;

        /* ===================== A) CREATORS (RUN AFTER) ===================== */
        IF ISNULL(@skip_001_create_trades_v9_setbased,0) = 0
        BEGIN TRY
            EXEC dbo.sp_001_create_trades_v9_setbased;
            SET @ts  = CONVERT(NVARCHAR(23), GETDATE(), 121);
            SET @msg = @ts + N' ' + @tag + N' sp_001_create_trades_v9_setbased OK';
            RAISERROR(@msg, 10, 1) WITH NOWAIT;
        END TRY
        BEGIN CATCH
            SET @ts  = CONVERT(NVARCHAR(23), GETDATE(), 121);
            SET @msg = @ts + N' ' + @tag + N' sp_001_create_trades_v9_setbased ERROR'
                     + N' num='   + CONVERT(NVARCHAR(20), ERROR_NUMBER())
                     + N' sev='   + CONVERT(NVARCHAR(20), ERROR_SEVERITY())
                     + N' state=' + CONVERT(NVARCHAR(20), ERROR_STATE())
                     + N' line='  + CONVERT(NVARCHAR(20), ERROR_LINE())
                     + N' proc='  + ISNULL(ERROR_PROCEDURE(), N'NULL')
                     + N' msg='   + ERROR_MESSAGE();
            RAISERROR(@msg, 16, 1) WITH NOWAIT;
        END CATCH;
        IF ISNULL(@skip_001_create_trades_v9_setbased,0) = 1
        BEGIN
            SET @ts  = CONVERT(NVARCHAR(23), GETDATE(), 121);
            SET @msg = @ts + N' ' + @tag + N' sp_001_create_trades_v9_setbased skipped by config (skip_001_create_trades_v9_setbased=1)';
            RAISERROR(@msg, 10, 1) WITH NOWAIT;
        END

        IF ISNULL(@skip_001_brk,0) = 0
        BEGIN TRY
            EXEC dbo.sp_001_create_trades_brk;
            SET @ts  = CONVERT(NVARCHAR(23), GETDATE(), 121);
            SET @msg = @ts + N' ' + @tag + N' sp_001_create_trades_brk OK';
            RAISERROR(@msg, 10, 1) WITH NOWAIT;
        END TRY
        BEGIN CATCH
            SET @ts  = CONVERT(NVARCHAR(23), GETDATE(), 121);
            SET @msg = @ts + N' ' + @tag + N' sp_001_create_trades_brk ERROR'
                     + N' num='   + CONVERT(NVARCHAR(20), ERROR_NUMBER())
                     + N' sev='   + CONVERT(NVARCHAR(20), ERROR_SEVERITY())
                     + N' state=' + CONVERT(NVARCHAR(20), ERROR_STATE())
                     + N' line='  + CONVERT(NVARCHAR(20), ERROR_LINE())
                     + N' proc='  + ISNULL(ERROR_PROCEDURE(), N'NULL')
                     + N' msg='   + ERROR_MESSAGE();
            RAISERROR(@msg, 16, 1) WITH NOWAIT;
        END CATCH;

        IF ISNULL(@skip_001_v9_followup,0) = 0
        BEGIN TRY
            EXEC dbo.sp_001_create_trades_v9_setbased_followup;
            SET @ts  = CONVERT(NVARCHAR(23), GETDATE(), 121);
            SET @msg = @ts + N' ' + @tag + N' sp_001_create_trades_v9_setbased_followup OK';
            RAISERROR(@msg, 10, 1) WITH NOWAIT;
        END TRY
        BEGIN CATCH
            SET @ts  = CONVERT(NVARCHAR(23), GETDATE(), 121);
            SET @msg = @ts + N' ' + @tag + N' sp_001_create_trades_v9_setbased_followup ERROR'
                     + N' num='   + CONVERT(NVARCHAR(20), ERROR_NUMBER())
                     + N' sev='   + CONVERT(NVARCHAR(20), ERROR_SEVERITY())
                     + N' state=' + CONVERT(NVARCHAR(20), ERROR_STATE())
                     + N' line='  + CONVERT(NVARCHAR(20), ERROR_LINE())
                     + N' proc='  + ISNULL(ERROR_PROCEDURE(), N'NULL')
                     + N' msg='   + ERROR_MESSAGE();
            RAISERROR(@msg, 16, 1) WITH NOWAIT;
        END CATCH;
        IF ISNULL(@skip_001_v9_followup,0) = 1
        BEGIN
            SET @ts  = CONVERT(NVARCHAR(23), GETDATE(), 121);
            SET @msg = @ts + N' ' + @tag + N' sp_001_create_trades_v9_setbased_followup skipped by config (skip_001_v9_followup=1)';
            RAISERROR(@msg, 10, 1) WITH NOWAIT;
        END

        /* ---- v2 ---- */
        IF ISNULL(@skip_001_v2,0) = 0
        BEGIN TRY
            EXEC dbo.sp_001_copy_trade_as_tradeable_v2;
            SET @ts  = CONVERT(NVARCHAR(23), GETDATE(), 121);
            SET @msg = @ts + N' ' + @tag + N' sp_001_copy_trade_as_tradeable_v2 OK';
            RAISERROR(@msg, 10, 1) WITH NOWAIT;
        END TRY
        BEGIN CATCH
            SET @ts  = CONVERT(NVARCHAR(23), GETDATE(), 121);
            SET @msg = @ts + N' ' + @tag + N' sp_001_copy_trade_as_tradeable_v2 ERROR'
                     + N' num='   + CONVERT(NVARCHAR(20), ERROR_NUMBER())
                     + N' sev='   + CONVERT(NVARCHAR(20), ERROR_SEVERITY())
                     + N' state=' + CONVERT(NVARCHAR(20), ERROR_STATE())
                     + N' line='  + CONVERT(NVARCHAR(20), ERROR_LINE())
                     + N' proc='  + ISNULL(ERROR_PROCEDURE(), N'NULL')
                     + N' msg='   + ERROR_MESSAGE();
            RAISERROR(@msg, 16, 1) WITH NOWAIT;
        END CATCH;
        IF ISNULL(@skip_001_v2,0) = 1
        BEGIN
            SET @ts  = CONVERT(NVARCHAR(23), GETDATE(), 121);
            SET @msg = @ts + N' ' + @tag + N' sp_001_copy_trade_as_tradeable_v2 skipped by config (skip_001_v2=1)';
            RAISERROR(@msg, 10, 1) WITH NOWAIT;
        END


        /* ---- v3 ---- */
        IF ISNULL(@skip_001_v3,0) = 0
        BEGIN TRY
            EXEC dbo.sp_001_copy_trade_as_tradeable_v3;
            SET @ts  = CONVERT(NVARCHAR(23), GETDATE(), 121);
            SET @msg = @ts + N' ' + @tag + N' sp_001_copy_trade_as_tradeable_v3 OK';
            RAISERROR(@msg, 10, 1) WITH NOWAIT;
        END TRY
        BEGIN CATCH
            SET @ts  = CONVERT(NVARCHAR(23), GETDATE(), 121);
            SET @msg = @ts + N' ' + @tag + N' sp_001_copy_trade_as_tradeable_v3 ERROR'
                     + N' num='   + CONVERT(NVARCHAR(20), ERROR_NUMBER())
                     + N' sev='   + CONVERT(NVARCHAR(20), ERROR_SEVERITY())
                     + N' state=' + CONVERT(NVARCHAR(20), ERROR_STATE())
                     + N' line='  + CONVERT(NVARCHAR(20), ERROR_LINE())
                     + N' proc='  + ISNULL(ERROR_PROCEDURE(), N'NULL')
                     + N' msg='   + ERROR_MESSAGE();
            RAISERROR(@msg, 16, 1) WITH NOWAIT;
        END CATCH;
        IF ISNULL(@skip_001_v3,0) = 1
        BEGIN
            SET @ts  = CONVERT(NVARCHAR(23), GETDATE(), 121);
            SET @msg = @ts + N' ' + @tag + N' sp_001_copy_trade_as_tradeable_v3 skipped by config (skip_001_v3=1)';
            RAISERROR(@msg, 10, 1) WITH NOWAIT;
        END


        /* ---- v4 ---- */
        IF ISNULL(@skip_001_v4,0) = 0
        BEGIN TRY
            EXEC dbo.sp_001_copy_trade_as_tradeable_v4;
            SET @ts  = CONVERT(NVARCHAR(23), GETDATE(), 121);
            SET @msg = @ts + N' ' + @tag + N' sp_001_copy_trade_as_tradeable_v4 OK';
            RAISERROR(@msg, 10, 1) WITH NOWAIT;
        END TRY
        BEGIN CATCH
            SET @ts  = CONVERT(NVARCHAR(23), GETDATE(), 121);
            SET @msg = @ts + N' ' + @tag + N' sp_001_copy_trade_as_tradeable_v4 ERROR'
                     + N' num='   + CONVERT(NVARCHAR(20), ERROR_NUMBER())
                     + N' sev='   + CONVERT(NVARCHAR(20), ERROR_SEVERITY())
                     + N' state=' + CONVERT(NVARCHAR(20), ERROR_STATE())
                     + N' line='  + CONVERT(NVARCHAR(20), ERROR_LINE())
                     + N' proc='  + ISNULL(ERROR_PROCEDURE(), N'NULL')
                     + N' msg='   + ERROR_MESSAGE();
            RAISERROR(@msg, 16, 1) WITH NOWAIT;
        END CATCH;
        IF ISNULL(@skip_001_v4,0) = 1
        BEGIN
            SET @ts  = CONVERT(NVARCHAR(23), GETDATE(), 121);
            SET @msg = @ts + N' ' + @tag + N' sp_001_copy_trade_as_tradeable_v4 skipped by config (skip_001_v4=1)';
            RAISERROR(@msg, 10, 1) WITH NOWAIT;
        END


        /* ---- v5 ---- */
        IF ISNULL(@skip_001_v5,0) = 0
        BEGIN TRY
            EXEC dbo.sp_001_copy_trade_as_tradeable_v5;
            SET @ts  = CONVERT(NVARCHAR(23), GETDATE(), 121);
            SET @msg = @ts + N' ' + @tag + N' sp_001_copy_trade_as_tradeable_v5 OK';
            RAISERROR(@msg, 10, 1) WITH NOWAIT;
        END TRY
        BEGIN CATCH
            SET @ts  = CONVERT(NVARCHAR(23), GETDATE(), 121);
            SET @msg = @ts + N' ' + @tag + N' sp_001_copy_trade_as_tradeable_v5 ERROR'
                     + N' num='   + CONVERT(NVARCHAR(20), ERROR_NUMBER())
                     + N' sev='   + CONVERT(NVARCHAR(20), ERROR_SEVERITY())
                     + N' state=' + CONVERT(NVARCHAR(20), ERROR_STATE())
                     + N' line='  + CONVERT(NVARCHAR(20), ERROR_LINE())
                     + N' proc='  + ISNULL(ERROR_PROCEDURE(), N'NULL')
                     + N' msg='   + ERROR_MESSAGE();
            RAISERROR(@msg, 16, 1) WITH NOWAIT;
        END CATCH;
        IF ISNULL(@skip_001_v5,0) = 1
        BEGIN
            SET @ts  = CONVERT(NVARCHAR(23), GETDATE(), 121);
            SET @msg = @ts + N' ' + @tag + N' sp_001_copy_trade_as_tradeable_v5 skipped by config (skip_001_v5=1)';
            RAISERROR(@msg, 10, 1) WITH NOWAIT;
        END


        /* ---- v6 ---- */
        IF ISNULL(@skip_001_v6,0) = 0
        BEGIN TRY
            EXEC dbo.sp_001_copy_trade_as_tradeable_v6;
            SET @ts  = CONVERT(NVARCHAR(23), GETDATE(), 121);
            SET @msg = @ts + N' ' + @tag + N' sp_001_copy_trade_as_tradeable_v6 OK';
            RAISERROR(@msg, 10, 1) WITH NOWAIT;
        END TRY
        BEGIN CATCH
            SET @ts  = CONVERT(NVARCHAR(23), GETDATE(), 121);
            SET @msg = @ts + N' ' + @tag + N' sp_001_copy_trade_as_tradeable_v6 ERROR'
                     + N' num='   + CONVERT(NVARCHAR(20), ERROR_NUMBER())
                     + N' sev='   + CONVERT(NVARCHAR(20), ERROR_SEVERITY())
                     + N' state=' + CONVERT(NVARCHAR(20), ERROR_STATE())
                     + N' line='  + CONVERT(NVARCHAR(20), ERROR_LINE())
                     + N' proc='  + ISNULL(ERROR_PROCEDURE(), N'NULL')
                     + N' msg='   + ERROR_MESSAGE();
            RAISERROR(@msg, 16, 1) WITH NOWAIT;
        END CATCH;
        IF ISNULL(@skip_001_v6,0) = 1
        BEGIN
            SET @ts  = CONVERT(NVARCHAR(23), GETDATE(), 121);
            SET @msg = @ts + N' ' + @tag + N' sp_001_copy_trade_as_tradeable_v6 skipped by config (skip_001_v6=1)';
            RAISERROR(@msg, 10, 1) WITH NOWAIT;
        END


        /* ---- v7 ---- */
        IF ISNULL(@skip_001_v7,0) = 0
        BEGIN TRY
            EXEC dbo.sp_001_copy_trade_as_tradeable_v7;
            SET @ts  = CONVERT(NVARCHAR(23), GETDATE(), 121);
            SET @msg = @ts + N' ' + @tag + N' sp_001_copy_trade_as_tradeable_v7 OK';
            RAISERROR(@msg, 10, 1) WITH NOWAIT;
        END TRY
        BEGIN CATCH
            SET @ts  = CONVERT(NVARCHAR(23), GETDATE(), 121);
            SET @msg = @ts + N' ' + @tag + N' sp_001_copy_trade_as_tradeable_v7 ERROR'
                     + N' num='   + CONVERT(NVARCHAR(20), ERROR_NUMBER())
                     + N' sev='   + CONVERT(NVARCHAR(20), ERROR_SEVERITY())
                     + N' state=' + CONVERT(NVARCHAR(20), ERROR_STATE())
                     + N' line='  + CONVERT(NVARCHAR(20), ERROR_LINE())
                     + N' proc='  + ISNULL(ERROR_PROCEDURE(), N'NULL')
                     + N' msg='   + ERROR_MESSAGE();
            RAISERROR(@msg, 16, 1) WITH NOWAIT;
        END CATCH;
        IF ISNULL(@skip_001_v7,0) = 1
        BEGIN
            SET @ts  = CONVERT(NVARCHAR(23), GETDATE(), 121);
            SET @msg = @ts + N' ' + @tag + N' sp_001_copy_trade_as_tradeable_v7 skipped by config (skip_001_v7=1)';
            RAISERROR(@msg, 10, 1) WITH NOWAIT;
        END


        /* ---- v701 ---- */
        IF ISNULL(@skip_001_v701,0) = 0
        BEGIN TRY
            EXEC dbo.sp_001_copy_trade_as_tradeable_v701;
            SET @ts  = CONVERT(NVARCHAR(23), GETDATE(), 121);
            SET @msg = @ts + N' ' + @tag + N' sp_001_copy_trade_as_tradeable_v701 OK';
            RAISERROR(@msg, 10, 1) WITH NOWAIT;
        END TRY
        BEGIN CATCH
            SET @ts  = CONVERT(NVARCHAR(23), GETDATE(), 121);
            SET @msg = @ts + N' ' + @tag + N' sp_001_copy_trade_as_tradeable_v701 ERROR'
                     + N' num='   + CONVERT(NVARCHAR(20), ERROR_NUMBER())
                     + N' sev='   + CONVERT(NVARCHAR(20), ERROR_SEVERITY())
                     + N' state=' + CONVERT(NVARCHAR(20), ERROR_STATE())
                     + N' line='  + CONVERT(NVARCHAR(20), ERROR_LINE())
                     + N' proc='  + ISNULL(ERROR_PROCEDURE(), N'NULL')
                     + N' msg='   + ERROR_MESSAGE();
            RAISERROR(@msg, 16, 1) WITH NOWAIT;
        END CATCH;
        IF ISNULL(@skip_001_v701,0) = 1
        BEGIN
            SET @ts  = CONVERT(NVARCHAR(23), GETDATE(), 121);
            SET @msg = @ts + N' ' + @tag + N' sp_001_copy_trade_as_tradeable_v701 skipped by config (skip_001_v701=1)';
            RAISERROR(@msg, 10, 1) WITH NOWAIT;
        END


        /* ---- v702 ---- */
        IF ISNULL(@skip_001_v702,0) = 0
        BEGIN TRY
            EXEC dbo.sp_001_copy_trade_as_tradeable_v702;
            SET @ts  = CONVERT(NVARCHAR(23), GETDATE(), 121);
            SET @msg = @ts + N' ' + @tag + N' sp_001_copy_trade_as_tradeable_v702 OK';
            RAISERROR(@msg, 10, 1) WITH NOWAIT;
        END TRY
        BEGIN CATCH
            SET @ts  = CONVERT(NVARCHAR(23), GETDATE(), 121);
            SET @msg = @ts + N' ' + @tag + N' sp_001_copy_trade_as_tradeable_v702 ERROR'
                     + N' num='   + CONVERT(NVARCHAR(20), ERROR_NUMBER())
                     + N' sev='   + CONVERT(NVARCHAR(20), ERROR_SEVERITY())
                     + N' state=' + CONVERT(NVARCHAR(20), ERROR_STATE())
                     + N' line='  + CONVERT(NVARCHAR(20), ERROR_LINE())
                     + N' proc='  + ISNULL(ERROR_PROCEDURE(), N'NULL')
                     + N' msg='   + ERROR_MESSAGE();
            RAISERROR(@msg, 16, 1) WITH NOWAIT;
        END CATCH;
        IF ISNULL(@skip_001_v702,0) = 1
        BEGIN
            SET @ts  = CONVERT(NVARCHAR(23), GETDATE(), 121);
            SET @msg = @ts + N' ' + @tag + N' sp_001_copy_trade_as_tradeable_v702 skipped by config (skip_001_v702=1)';
            RAISERROR(@msg, 10, 1) WITH NOWAIT;
        END


        /* ---- v703 ---- */
        IF ISNULL(@skip_001_v703,0) = 0
        BEGIN TRY
            EXEC dbo.sp_001_copy_trade_as_tradeable_v703;
            SET @ts  = CONVERT(NVARCHAR(23), GETDATE(), 121);
            SET @msg = @ts + N' ' + @tag + N' sp_001_copy_trade_as_tradeable_v703 OK';
            RAISERROR(@msg, 10, 1) WITH NOWAIT;
        END TRY
        BEGIN CATCH
            SET @ts  = CONVERT(NVARCHAR(23), GETDATE(), 121);
            SET @msg = @ts + N' ' + @tag + N' sp_001_copy_trade_as_tradeable_v703 ERROR'
                     + N' num='   + CONVERT(NVARCHAR(20), ERROR_NUMBER())
                     + N' sev='   + CONVERT(NVARCHAR(20), ERROR_SEVERITY())
                     + N' state=' + CONVERT(NVARCHAR(20), ERROR_STATE())
                     + N' line='  + CONVERT(NVARCHAR(20), ERROR_LINE())
                     + N' proc='  + ISNULL(ERROR_PROCEDURE(), N'NULL')
                     + N' msg='   + ERROR_MESSAGE();
            RAISERROR(@msg, 16, 1) WITH NOWAIT;
        END CATCH;
        IF ISNULL(@skip_001_v703,0) = 1
        BEGIN
            SET @ts  = CONVERT(NVARCHAR(23), GETDATE(), 121);
            SET @msg = @ts + N' ' + @tag + N' sp_001_copy_trade_as_tradeable_v703 skipped by config (skip_001_v703=1)';
            RAISERROR(@msg, 10, 1) WITH NOWAIT;
        END


        /* ---- v704 ---- */
        IF ISNULL(@skip_001_v704,0) = 0
        BEGIN TRY
            EXEC dbo.sp_001_copy_trade_as_tradeable_v704;
            SET @ts  = CONVERT(NVARCHAR(23), GETDATE(), 121);
            SET @msg = @ts + N' ' + @tag + N' sp_001_copy_trade_as_tradeable_v704 OK';
            RAISERROR(@msg, 10, 1) WITH NOWAIT;
        END TRY
        BEGIN CATCH
            SET @ts  = CONVERT(NVARCHAR(23), GETDATE(), 121);
            SET @msg = @ts + N' ' + @tag + N' sp_001_copy_trade_as_tradeable_v704 ERROR'
                     + N' num='   + CONVERT(NVARCHAR(20), ERROR_NUMBER())
                     + N' sev='   + CONVERT(NVARCHAR(20), ERROR_SEVERITY())
                     + N' state=' + CONVERT(NVARCHAR(20), ERROR_STATE())
                     + N' line='  + CONVERT(NVARCHAR(20), ERROR_LINE())
                     + N' proc='  + ISNULL(ERROR_PROCEDURE(), N'NULL')
                     + N' msg='   + ERROR_MESSAGE();
            RAISERROR(@msg, 16, 1) WITH NOWAIT;
        END CATCH;
        IF ISNULL(@skip_001_v704,0) = 1
        BEGIN
            SET @ts  = CONVERT(NVARCHAR(23), GETDATE(), 121);
            SET @msg = @ts + N' ' + @tag + N' sp_001_copy_trade_as_tradeable_v704 skipped by config (skip_001_v704=1)';
            RAISERROR(@msg, 10, 1) WITH NOWAIT;
        END


        /* ---- v8 ---- */
        IF ISNULL(@skip_001_v8,0) = 0
        BEGIN TRY
            EXEC dbo.sp_001_copy_trade_as_tradeable_v8;
            SET @ts  = CONVERT(NVARCHAR(23), GETDATE(), 121);
            SET @msg = @ts + N' ' + @tag + N' sp_001_copy_trade_as_tradeable_v8 OK';
            RAISERROR(@msg, 10, 1) WITH NOWAIT;
        END TRY
        BEGIN CATCH
            SET @ts  = CONVERT(NVARCHAR(23), GETDATE(), 121);
            SET @msg = @ts + N' ' + @tag + N' sp_001_copy_trade_as_tradeable_v8 ERROR'
                     + N' num='   + CONVERT(NVARCHAR(20), ERROR_NUMBER())
                     + N' sev='   + CONVERT(NVARCHAR(20), ERROR_SEVERITY())
                     + N' state=' + CONVERT(NVARCHAR(20), ERROR_STATE())
                     + N' line='  + CONVERT(NVARCHAR(20), ERROR_LINE())
                     + N' proc='  + ISNULL(ERROR_PROCEDURE(), N'NULL')
                     + N' msg='   + ERROR_MESSAGE();
            RAISERROR(@msg, 16, 1) WITH NOWAIT;
        END CATCH;
        IF ISNULL(@skip_001_v8,0) = 1
        BEGIN
            SET @ts  = CONVERT(NVARCHAR(23), GETDATE(), 121);
            SET @msg = @ts + N' ' + @tag + N' sp_001_copy_trade_as_tradeable_v8 skipped by config (skip_001_v8=1)';
            RAISERROR(@msg, 10, 1) WITH NOWAIT;
        END


        /* ---- v91 ---- */
        IF ISNULL(@skip_001_v91,0) = 0
        BEGIN TRY
            EXEC dbo.sp_001_copy_trade_as_tradeable_v91;
            SET @ts  = CONVERT(NVARCHAR(23), GETDATE(), 121);
            SET @msg = @ts + N' ' + @tag + N' sp_001_copy_trade_as_tradeable_v91 OK';
            RAISERROR(@msg, 10, 1) WITH NOWAIT;
        END TRY
        BEGIN CATCH
            SET @ts  = CONVERT(NVARCHAR(23), GETDATE(), 121);
            SET @msg = @ts + N' ' + @tag + N' sp_001_copy_trade_as_tradeable_v91 ERROR'
                     + N' num='   + CONVERT(NVARCHAR(20), ERROR_NUMBER())
                     + N' sev='   + CONVERT(NVARCHAR(20), ERROR_SEVERITY())
                     + N' state=' + CONVERT(NVARCHAR(20), ERROR_STATE())
                     + N' line='  + CONVERT(NVARCHAR(20), ERROR_LINE())
                     + N' proc='  + ISNULL(ERROR_PROCEDURE(), N'NULL')
                     + N' msg='   + ERROR_MESSAGE();
            RAISERROR(@msg, 16, 1) WITH NOWAIT;
        END CATCH;
        IF ISNULL(@skip_001_v91,0) = 1
        BEGIN
            SET @ts  = CONVERT(NVARCHAR(23), GETDATE(), 121);
            SET @msg = @ts + N' ' + @tag + N' sp_001_copy_trade_as_tradeable_v91 skipped by config (skip_001_v91=1)';
            RAISERROR(@msg, 10, 1) WITH NOWAIT;
        END


        /* ---- breakout entry (new) ---- */
        IF ISNULL(@skip_breakout_entry,0) = 0
        BEGIN TRY
            EXEC dbo.sp_001_breakout_entry;
            SET @ts  = CONVERT(NVARCHAR(23), GETDATE(), 121);
            SET @msg = @ts + N' ' + @tag + N' sp_001_breakout_entry OK';
            RAISERROR(@msg, 10, 1) WITH NOWAIT;
        END TRY
        BEGIN CATCH
            SET @ts  = CONVERT(NVARCHAR(23), GETDATE(), 121);
            SET @msg = @ts + N' ' + @tag + N' sp_001_breakout_entry ERROR'
                     + N' num='   + CONVERT(NVARCHAR(20), ERROR_NUMBER())
                     + N' sev='   + CONVERT(NVARCHAR(20), ERROR_SEVERITY())
                     + N' state=' + CONVERT(NVARCHAR(20), ERROR_STATE())
                     + N' line='  + CONVERT(NVARCHAR(20), ERROR_LINE())
                     + N' proc='  + ISNULL(ERROR_PROCEDURE(), N'NULL')
                     + N' msg='   + ERROR_MESSAGE();
            RAISERROR(@msg, 16, 1) WITH NOWAIT;
        END CATCH;
        IF ISNULL(@skip_breakout_entry,0) = 1
        BEGIN
            SET @ts  = CONVERT(NVARCHAR(23), GETDATE(), 121);
            SET @msg = @ts + N' ' + @tag + N' sp_001_breakout_entry skipped by config (skip_breakout_entry=1)';
            RAISERROR(@msg, 10, 1) WITH NOWAIT;
        END


        /* ---- v92 ---- */
        IF ISNULL(@skip_001_v92,0) = 0
        BEGIN TRY
            EXEC dbo.sp_001_copy_trade_as_tradeable_v92;
            SET @ts  = CONVERT(NVARCHAR(23), GETDATE(), 121);
            SET @msg = @ts + N' ' + @tag + N' sp_001_copy_trade_as_tradeable_v92 OK';
            RAISERROR(@msg, 10, 1) WITH NOWAIT;
        END TRY
        BEGIN CATCH
            SET @ts  = CONVERT(NVARCHAR(23), GETDATE(), 121);
            SET @msg = @ts + N' ' + @tag + N' sp_001_copy_trade_as_tradeable_v92 ERROR'
                     + N' num='   + CONVERT(NVARCHAR(20), ERROR_NUMBER())
                     + N' sev='   + CONVERT(NVARCHAR(20), ERROR_SEVERITY())
                     + N' state=' + CONVERT(NVARCHAR(20), ERROR_STATE())
                     + N' line='  + CONVERT(NVARCHAR(20), ERROR_LINE())
                     + N' proc='  + ISNULL(ERROR_PROCEDURE(), N'NULL')
                     + N' msg='   + ERROR_MESSAGE();
            RAISERROR(@msg, 16, 1) WITH NOWAIT;
        END CATCH;
        IF ISNULL(@skip_001_v92,0) = 1
        BEGIN
            SET @ts  = CONVERT(NVARCHAR(23), GETDATE(), 121);
            SET @msg = @ts + N' ' + @tag + N' sp_001_copy_trade_as_tradeable_v92 skipped by config (skip_001_v92=1)';
            RAISERROR(@msg, 10, 1) WITH NOWAIT;
        END



        /* ---- buy sell entry (new) ---- */
        IF ISNULL(@skip_001_buy_sell,0) = 0
        BEGIN TRY
            EXEC dbo.sp_001_buy_sell_count_entry;
            SET @ts  = CONVERT(NVARCHAR(23), GETDATE(), 121);
            SET @msg = @ts + N' ' + @tag + N' sp_001_buy_sell_count_entry OK';
            RAISERROR(@msg, 10, 1) WITH NOWAIT;
        END TRY
        BEGIN CATCH
            SET @ts  = CONVERT(NVARCHAR(23), GETDATE(), 121);
            SET @msg = @ts + N' ' + @tag + N' sp_001_buy_sell_count_entry ERROR'
                     + N' num='   + CONVERT(NVARCHAR(20), ERROR_NUMBER())
                     + N' sev='   + CONVERT(NVARCHAR(20), ERROR_SEVERITY())
                     + N' state=' + CONVERT(NVARCHAR(20), ERROR_STATE())
                     + N' line='  + CONVERT(NVARCHAR(20), ERROR_LINE())
                     + N' proc='  + ISNULL(ERROR_PROCEDURE(), N'NULL')
                     + N' msg='   + ERROR_MESSAGE();
            RAISERROR(@msg, 16, 1) WITH NOWAIT;
        END CATCH;
        IF ISNULL(@skip_001_buy_sell,0) = 1
        BEGIN
            SET @ts  = CONVERT(NVARCHAR(23), GETDATE(), 121);
            SET @msg = @ts + N' ' + @tag + N' sp_001_buy_sell_count_entry skipped by config (skip_001_buy_sell=1)';
            RAISERROR(@msg, 10, 1) WITH NOWAIT;
        END


        /* ---- zone distribution entry (new) -- 2025-10-29 ---- */
        IF ISNULL(@skip_001_zone,0) = 0
        BEGIN TRY
            EXEC dbo.sp_001_zone_distribution_trade;
            SET @ts  = CONVERT(NVARCHAR(23), GETDATE(), 121);
            SET @msg = @ts + N' ' + @tag + N' sp_001_zone_distribution_trade OK';
            RAISERROR(@msg, 10, 1) WITH NOWAIT;
        END TRY
        BEGIN CATCH
            SET @ts  = CONVERT(NVARCHAR(23), GETDATE(), 121);
            SET @msg = @ts + N' ' + @tag + N' sp_001_zone_distribution_trade ERROR'
                     + N' num='   + CONVERT(NVARCHAR(20), ERROR_NUMBER())
                     + N' sev='   + CONVERT(NVARCHAR(20), ERROR_SEVERITY())
                     + N' state=' + CONVERT(NVARCHAR(20), ERROR_STATE())
                     + N' line='  + CONVERT(NVARCHAR(20), ERROR_LINE())
                     + N' proc='  + ISNULL(ERROR_PROCEDURE(), N'NULL')
                     + N' msg='   + ERROR_MESSAGE();
            RAISERROR(@msg, 16, 1) WITH NOWAIT;
        END CATCH;
        IF ISNULL(@skip_001_zone,0) = 1
        BEGIN
            SET @ts  = CONVERT(NVARCHAR(23), GETDATE(), 121);
            SET @msg = @ts + N' ' + @tag + N' sp_001_zone_distribution_trade skipped by config (skip_001_zone=1)';
            RAISERROR(@msg, 10, 1) WITH NOWAIT;
        END


        IF ISNULL(@skip_800_exec,0) = 0
        BEGIN TRY
            EXEC dbo.sp_800_exec_all;
            SET @ts  = CONVERT(NVARCHAR(23), GETDATE(), 121);
            SET @msg = @ts + N' ' + @tag + N' sp_800_exec_all OK';
            RAISERROR(@msg, 10, 1) WITH NOWAIT;
        END TRY
        BEGIN CATCH
            SET @ts  = CONVERT(NVARCHAR(23), GETDATE(), 121);
            SET @msg = @ts + N' ' + @tag + N' sp_800_exec_all ERROR'
                     + N' num='   + CONVERT(NVARCHAR(20), ERROR_NUMBER())
                     + N' sev='   + CONVERT(NVARCHAR(20), ERROR_SEVERITY())
                     + N' state=' + CONVERT(NVARCHAR(20), ERROR_STATE())
                     + N' line='  + CONVERT(NVARCHAR(20), ERROR_LINE())
                     + N' proc='  + ISNULL(ERROR_PROCEDURE(), N'NULL')
                     + N' msg='   + ERROR_MESSAGE();
            RAISERROR(@msg, 16, 1) WITH NOWAIT;
        END CATCH;
        IF ISNULL(@skip_800_exec,0) = 1
        BEGIN
            SET @ts  = CONVERT(NVARCHAR(23), GETDATE(), 121);
            SET @msg = @ts + N' ' + @tag + N' sp_800_exec_all skipped by config (skip_800_exec=1)';
            RAISERROR(@msg, 10, 1) WITH NOWAIT;
        END
        /* ---- capture snapshot (new) ---- */
        BEGIN TRY
            EXEC dbo.sp_522_Capture_TradePanel_Snapshot;
            SET @ts  = CONVERT(NVARCHAR(23), GETDATE(), 121);
            SET @msg = @ts + N' ' + @tag + N' sp_522_Capture_TradePanel_Snapshot OK';
            RAISERROR(@msg, 10, 1) WITH NOWAIT;
        END TRY
        BEGIN CATCH
            SET @ts  = CONVERT(NVARCHAR(23), GETDATE(), 121);
            SET @msg = @ts + N' ' + @tag + N' sp_522_Capture_TradePanel_Snapshot ERROR'
                     + N' num='   + CONVERT(NVARCHAR(20), ERROR_NUMBER())
                     + N' sev='   + CONVERT(NVARCHAR(20), ERROR_SEVERITY())
                     + N' state=' + CONVERT(NVARCHAR(20), ERROR_STATE())
                     + N' line='  + CONVERT(NVARCHAR(20), ERROR_LINE())
                     + N' proc='  + ISNULL(ERROR_PROCEDURE(), N'NULL')
                     + N' msg='   + ERROR_MESSAGE();
            RAISERROR(@msg, 16, 1) WITH NOWAIT;
        END CATCH;

        /* ---- capture open trades snapshot (all products) ---- */
        /* BEGIN TRY
            EXEC dbo.sp_9100_CreateCombinedTradesOpenSnapshot;
            SET @ts  = CONVERT(NVARCHAR(23), GETDATE(), 121);
            SET @msg = @ts + N' ' + @tag + N' sp_9100_CreateCombinedTradesOpenSnapshot OK';
            RAISERROR(@msg, 10, 1) WITH NOWAIT;
        END TRY
        BEGIN CATCH
            SET @ts  = CONVERT(NVARCHAR(23), GETDATE(), 121);
            SET @msg = @ts + N' ' + @tag + N' sp_9100_CreateCombinedTradesOpenSnapshot ERROR'
                     + N' num='   + CONVERT(NVARCHAR(20), ERROR_NUMBER())
                     + N' sev='   + CONVERT(NVARCHAR(20), ERROR_SEVERITY())
                     + N' state=' + CONVERT(NVARCHAR(20), ERROR_STATE())
                     + N' line='  + CONVERT(NVARCHAR(20), ERROR_LINE())
                     + N' proc='  + ISNULL(ERROR_PROCEDURE(), N'NULL')
                     + N' msg='   + ERROR_MESSAGE();
            RAISERROR(@msg, 16, 1) WITH NOWAIT;
        END CATCH; */

        /* ---- refresh EP051 export cache (gated to ~every 10 minutes) ---- */
        IF ISNULL(@skip_ep051_export_cache,0) = 0
        BEGIN TRY
            IF NOT EXISTS (
                SELECT 1 FROM dbo.ep051_export_cache_run_log
                WHERE status = 'success' AND completed_at >= DATEADD(MINUTE, -10, SYSUTCDATETIME())
            )
            BEGIN
                EXEC dbo.usp_ep051_refresh_export_cache;
                SET @ts  = CONVERT(NVARCHAR(23), GETDATE(), 121);
                SET @msg = @ts + N' ' + @tag + N' usp_ep051_refresh_export_cache OK';
                RAISERROR(@msg, 10, 1) WITH NOWAIT;
            END
        END TRY
        BEGIN CATCH
            SET @ts  = CONVERT(NVARCHAR(23), GETDATE(), 121);
            SET @msg = @ts + N' ' + @tag + N' usp_ep051_refresh_export_cache ERROR'
                     + N' num='   + CONVERT(NVARCHAR(20), ERROR_NUMBER())
                     + N' sev='   + CONVERT(NVARCHAR(20), ERROR_SEVERITY())
                     + N' state=' + CONVERT(NVARCHAR(20), ERROR_STATE())
                     + N' line='  + CONVERT(NVARCHAR(20), ERROR_LINE())
                     + N' proc='  + ISNULL(ERROR_PROCEDURE(), N'NULL')
                     + N' msg='   + ERROR_MESSAGE();
            RAISERROR(@msg, 16, 1) WITH NOWAIT;
        END CATCH;
        IF ISNULL(@skip_ep051_export_cache,0) = 1
        BEGIN
            SET @ts  = CONVERT(NVARCHAR(23), GETDATE(), 121);
            SET @msg = @ts + N' ' + @tag + N' usp_ep051_refresh_export_cache skipped by config (skip_ep051_export_cache=1)';
            RAISERROR(@msg, 10, 1) WITH NOWAIT;
        END


        /* ---- capture EP051 strategy rank history (gated to ~every 30 minutes) ---- */
        IF ISNULL(@skip_ep051_rank_capture,0) = 0
        BEGIN TRY
            IF NOT EXISTS (
                SELECT 1 FROM dbo.ep051_rank_capture_run_log
                WHERE status = 'success' AND completed_at >= DATEADD(MINUTE, -30, SYSUTCDATETIME())
            )
            BEGIN
                EXEC dbo.usp_ep051_capture_strategy_rank_history;
                SET @ts  = CONVERT(NVARCHAR(23), GETDATE(), 121);
                SET @msg = @ts + N' ' + @tag + N' usp_ep051_capture_strategy_rank_history OK';
                RAISERROR(@msg, 10, 1) WITH NOWAIT;
            END
        END TRY
        BEGIN CATCH
            SET @ts  = CONVERT(NVARCHAR(23), GETDATE(), 121);
            SET @msg = @ts + N' ' + @tag + N' usp_ep051_capture_strategy_rank_history ERROR'
                     + N' num='   + CONVERT(NVARCHAR(20), ERROR_NUMBER())
                     + N' sev='   + CONVERT(NVARCHAR(20), ERROR_SEVERITY())
                     + N' state=' + CONVERT(NVARCHAR(20), ERROR_STATE())
                     + N' line='  + CONVERT(NVARCHAR(20), ERROR_LINE())
                     + N' proc='  + ISNULL(ERROR_PROCEDURE(), N'NULL')
                     + N' msg='   + ERROR_MESSAGE();
            RAISERROR(@msg, 16, 1) WITH NOWAIT;
        END CATCH;
        IF ISNULL(@skip_ep051_rank_capture,0) = 1
        BEGIN
            SET @ts  = CONVERT(NVARCHAR(23), GETDATE(), 121);
            SET @msg = @ts + N' ' + @tag + N' usp_ep051_capture_strategy_rank_history skipped by config (skip_ep051_rank_capture=1)';
            RAISERROR(@msg, 10, 1) WITH NOWAIT;
        END

        WAITFOR DELAY @LoopDelay;
    END
END
GO
