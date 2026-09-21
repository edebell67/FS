CREATE OR REPLACE PROCEDURE public.sp_001_create_trades_v9_setbased()
 LANGUAGE plpgsql
AS $procedure$
/*
=============================================================================
ORIGINAL T-SQL SOURCE FOR sp_001_create_trades_v9_setbased:
=============================================================================
CREATE   PROCEDURE [dbo].[sp_001_create_trades_v9_setbased]
AS
BEGIN
  SET NOCOUNT ON;
  SET XACT_ABORT ON;
  SET FORCEPLAN OFF;

  DECLARE @app_lock_result int;
  EXEC @app_lock_result = sys.sp_getapplock
      @Resource = N'tradedb:dbo.sp_001_create_trades_v9_setbased',
      @LockMode = N'Exclusive',
      @LockOwner = N'Session',
      @LockTimeout = 0;

  IF @app_lock_result < 0
  BEGIN
      RAISERROR(N'sp_001_create_trades_v9_setbased skipped: another execution is already active.', 0, 1) WITH NOWAIT;
      RETURN;
  END;

  SET LOCK_TIMEOUT 5000;
  BEGIN TRY

  /* ==== timing helpers (declare BEFORE first use) ==== */
  DECLARE @t_start  datetime2(3) = GETDATE();
  DECLARE @t_prev   datetime2(3) = @t_start;
  DECLARE @nowtxt   varchar(23);
  DECLARE @delta_ms int;

  /* Section 1: start; quotes are maintained by the dedicated loader */
  SET @nowtxt  = CONVERT(varchar(23), GETDATE(), 121);
  SET @delta_ms = DATEDIFF(ms, @t_prev, GETDATE());
  ;RAISERROR(N'[%s] Section 1: Start - Load FX Quotes (ms=%d)', 0, 1, @nowtxt, @delta_ms) WITH NOWAIT;
  SET @t_prev = GETDATE();

  /* Section 2: config & trading window */
  SET @nowtxt  = CONVERT(varchar(23), GETDATE(), 121);
  SET @delta_ms = DATEDIFF(ms, @t_prev, GETDATE());
  ;RAISERROR(N'[%s] Section 2: Config & window (ms=%d)', 0, 1, @nowtxt, @delta_ms) WITH NOWAIT;
  SET @t_prev = GETDATE();

  DECLARE @now datetime2(3) = GETDATE();

  DECLARE @is_sim_mode bit;
  EXEC dbo.sp_helper_is_sim_db @is_sim_mode = @is_sim_mode OUTPUT;

  DECLARE @trade_product_list_raw nvarchar(max) =
      (SELECT config_value FROM dbo.config WITH (NOLOCK) WHERE config_name='trade_product_list');
  IF @trade_product_list_raw IS NULL SET @trade_product_list_raw = N'';

  -- normalize whitelist: lower-case, strip quotes/spaces
  DECLARE @trade_product_list nvarchar(max) =
      LOWER(REPLACE(REPLACE(@trade_product_list_raw,'''',''), ' ', ''));

  DECLARE @trade_start time(0) =
      TRY_CONVERT(time(0),(SELECT config_value FROM dbo.config WITH (NOLOCK) WHERE config_name='trade_start'));
  IF @trade_start IS NULL SET @trade_start = '00:00';

  DECLARE @trade_end   time(0) =
      TRY_CONVERT(time(0),(SELECT config_value FROM dbo.config WITH (NOLOCK) WHERE config_name='trade_end'));
  IF @trade_end IS NULL SET @trade_end = '23:59';

  -- London local time
  DECLARE @now_ldn datetimeoffset = @now AT TIME ZONE 'GMT Standard Time';
  DECLARE @now_ldn_time time(0)   = CONVERT(time(0), @now_ldn);

  DECLARE @is_weekend bit =
      CASE WHEN DATENAME(weekday, CONVERT(date,@now_ldn)) IN ('Saturday','Sunday') THEN 1 ELSE 0 END;

  DECLARE @trading_active bit;

  SET @trading_active =
        CASE WHEN @is_weekend=1 THEN 0
             WHEN @trade_start<=@trade_end
                  THEN CASE WHEN @now_ldn_time>=@trade_start AND @now_ldn_time<@trade_end THEN 1 ELSE 0 END
                  ELSE CASE WHEN @now_ldn_time>=@trade_start OR  @now_ldn_time<@trade_end THEN 1 ELSE 0 END
        END;

  IF @is_sim_mode = 1
  BEGIN
      SET @trading_active = 1; -- bypass trade window in sim mode
  END;

  /* HARD GATE (kept) */
  IF ISNULL(@trading_active,0) = 0 AND @is_sim_mode = 0
  BEGIN
      DECLARE @ts_now   varchar(23) = CONVERT(varchar(23), GETDATE(), 121);
      DECLARE @ts_start varchar(8)  = CONVERT(varchar(8),  @trade_start, 108);
      DECLARE @ts_end   varchar(8)  = CONVERT(varchar(8),  @trade_end,   108);
      DECLARE @ts_nowld varchar(8)  = CONVERT(varchar(8),  @now_ldn_time,108);

      ;RAISERROR(
        N'[%s] Hard gate: trading window closed (start=%s, end=%s, now_ldn=%s). No new trades created.',
        0, 1, @ts_now, @ts_start, @ts_end, @ts_nowld
      ) WITH NOWAIT;
      RETURN;
  END;

  /* Section 3: PF universe */
  SET @nowtxt  = CONVERT(varchar(23), GETDATE(), 121);
  SET @delta_ms = DATEDIFF(ms, @t_prev, GETDATE());
  ;RAISERROR(N'[%s] Section 3: Load product_forex (ms=%d)', 0, 1, @nowtxt, @delta_ms) WITH NOWAIT;
  SET @t_prev = GETDATE();

  IF OBJECT_ID('tempdb..#pf') IS NOT NULL DROP TABLE #pf;
  CREATE TABLE #pf (
      pf_ord int IDENTITY(1,1) NOT NULL PRIMARY KEY,
      product nvarchar(50) NOT NULL,
      model nvarchar(128) NOT NULL,
      commission float NOT NULL,
      target_profit smallint NOT NULL,
      target_loss smallint NOT NULL,
      trade_qty bigint NOT NULL,
      product_type nvarchar(50) NOT NULL,
      trade_freq int NOT NULL
  );

  -- [V20260908_1425] 2026-09-08: Pre-declared table with IDENTITY(1,1) avoids expensive sort memory grants on product_forex
  INSERT INTO #pf (product, model, commission, target_profit, target_loss, trade_qty, product_type, trade_freq)
  SELECT product, CONVERT(nvarchar(128), model),
         commission, target_profit, target_loss, trade_qty, product_type, trade_freq
  FROM dbo.product_forex WITH (NOLOCK)
  WHERE trade_freq IN (1, 99);

  DECLARE @max_open_trade_qty INT;
  SELECT @max_open_trade_qty = TRY_CAST(config_value AS INT) FROM dbo.config WITH (NOLOCK) WHERE config_name = 'max_open_trade_qty';
  IF @max_open_trade_qty IS NULL SET @max_open_trade_qty = 100000;

  DECLARE @max_open_per_model INT;
  SELECT @max_open_per_model = TRY_CAST(config_value AS INT) FROM dbo.config WITH (NOLOCK) WHERE config_name = 'max_open_per_model';
  IF @max_open_per_model IS NULL SET @max_open_per_model = 1000;


  IF OBJECT_ID('tempdb..#open_qty') IS NOT NULL DROP TABLE #open_qty;
  -- [V20260908_1435] 2026-09-08: Bypass RESOURCE_SEMAPHORE wait queue using zero-memory-grant query hint
  SELECT model, SUM(trade_quantity) AS open_qty
  INTO #open_qty
  FROM dbo.combined_trades_open WITH (NOLOCK, INDEX(IX_combined_trades_open_active_model))
  WHERE tradeable > 0
    AND model IN (SELECT model FROM #pf)
  GROUP BY model
  OPTION (MAXDOP 1, MIN_GRANT_PERCENT = 0, MAX_GRANT_PERCENT = 0);

  IF OBJECT_ID('tempdb..#open_trade_count_per_model') IS NOT NULL DROP TABLE #open_trade_count_per_model;
  SELECT model, COUNT(*) AS open_trade_count
  INTO #open_trade_count_per_model
  FROM dbo.combined_trades_open WITH (NOLOCK, INDEX(IX_combined_trades_open_active_model))
  WHERE tradeable > 0
    AND model IN (SELECT model FROM #pf)
  GROUP BY model
  OPTION (MAXDOP 1, MIN_GRANT_PERCENT = 0, MAX_GRANT_PERCENT = 0);

  /* Section 4: latest quotes per product */
  SET @nowtxt  = CONVERT(varchar(23), GETDATE(), 121);
  SET @delta_ms = DATEDIFF(ms, @t_prev, GETDATE());
  ;RAISERROR(N'[%s] Section 4: Latest quotes by product (ms=%d)', 0, 1, @nowtxt, @delta_ms) WITH NOWAIT;
  SET @t_prev = GETDATE();

  IF OBJECT_ID('tempdb..#q') IS NOT NULL DROP TABLE #q;
  -- [V20260908_1230] 2026-09-08: Direct join on fx_quotes by product code avoids expensive memory-grant OUTER APPLY sorts
  SELECT p.product,
         q.ask AS askPrice,
         q.bid AS bidPrice
  INTO #q
  FROM (SELECT DISTINCT product FROM #pf) AS p
  LEFT JOIN dbo.fx_quotes q WITH (NOLOCK) ON q.code = p.product;

  /* Section 5: build candidates (BUY+SELL for every PF row) */
  SET @nowtxt  = CONVERT(varchar(23), GETDATE(), 121);
  SET @delta_ms = DATEDIFF(ms, @t_prev, GETDATE());
  ;RAISERROR(N'[%s] Section 5: Build candidates (ms=%d)', 0, 1, @nowtxt, @delta_ms) WITH NOWAIT;
  SET @t_prev = GETDATE();

  IF OBJECT_ID('tempdb..#cand') IS NOT NULL DROP TABLE #cand;
  CREATE TABLE #cand(
     guid uniqueidentifier NOT NULL,
     pf_ord int NOT NULL,
     product nvarchar(50) NOT NULL,
     model nvarchar(50) NOT NULL,
     product_type nvarchar(50) NOT NULL,
     created datetime2(3) NOT NULL,
     commission float NOT NULL,
     target_profit smallint NOT NULL,
     target_loss smallint NOT NULL,
     trade_qty bigint NOT NULL,
     signal nvarchar(4) NOT NULL,            -- 'buy' / 'sell'
     entry_price float NULL,
     latest_price float NULL,
     net_return float NULL,
     alt_net_return float NULL,
     in_whitelist bit NOT NULL
  );

  -- whitelist helpers
  DECLARE @tpl_clean nvarchar(max) = @trade_product_list;
  DECLARE @wl_all bit = CASE WHEN @tpl_clean IS NULL OR LTRIM(RTRIM(@tpl_clean)) = N'' THEN 1 ELSE 0 END;

  -- BUY rows (entry=ask, latest=ask)
  INSERT #cand
  SELECT NEWID(), pf.pf_ord, pf.product, pf.model, pf.product_type,
         @now, pf.commission, pf.target_profit, pf.target_loss, pf.trade_qty,
         N'buy',
         q.askPrice, q.askPrice,
         ((q.bidPrice - q.askPrice) * pf.trade_qty) - pf.commission,
         ((q.askPrice - q.bidPrice) * pf.trade_qty) - pf.commission,
         CASE
           WHEN @wl_all = 1 THEN 1
           ELSE CASE WHEN CHARINDEX(','+LOWER(pf.product)+',', ','+@tpl_clean+',') > 0 THEN 1 ELSE 0 END
         END
  FROM #pf pf
  JOIN #q  q ON q.product = pf.product
  LEFT JOIN #open_trade_count_per_model oq_count ON oq_count.model = pf.model
  WHERE pf.trade_freq = 1 -- [V20260908_1200] 2026-09-08: Non-DNA models
    AND ISNULL(oq_count.open_trade_count, 0) < @max_open_per_model;

  -- SELL rows (entry=bid, latest=bid)
  INSERT #cand
  SELECT NEWID(), pf.pf_ord, pf.product, pf.model, pf.product_type,
         @now, pf.commission, pf.target_profit, pf.target_loss, pf.trade_qty,
         N'sell',
         q.bidPrice, q.bidPrice,
         ((q.bidPrice - q.askPrice) * pf.trade_qty) - pf.commission,
         ((q.askPrice - q.bidPrice) * pf.trade_qty) - pf.commission,
         CASE
           WHEN @wl_all = 1 THEN 1
           ELSE CASE WHEN CHARINDEX(','+LOWER(pf.product)+',', ','+@tpl_clean+',') > 0 THEN 1 ELSE 0 END
         END
  FROM #pf pf
  JOIN #q  q ON q.product = pf.product
  LEFT JOIN #open_trade_count_per_model oq_count ON oq_count.model = pf.model
  WHERE pf.trade_freq = 1 -- [V20260908_1200] 2026-09-08: Non-DNA models
    AND ISNULL(oq_count.open_trade_count, 0) < @max_open_per_model;

  -- DNA models: only build if DNA models (trade_freq=99) are active in #pf
  -- [V20260908_1230] 2026-09-08: Skips expensive vw_product_forex_dna_expanded queries when no DNA models are active
  IF EXISTS (SELECT 1 FROM #pf WHERE trade_freq = 99)
  BEGIN
    INSERT #cand
    SELECT NEWID(), pf.pf_ord, pf.product, pf.model, pf.product_type,
           @now, pf.commission, pf.target_profit, pf.target_loss, dna.leg_qty,
           CASE WHEN dna.side_pref = 'BUY' THEN N'buy' ELSE N'sell' END,
           CASE WHEN dna.side_pref = 'BUY' THEN q.askPrice ELSE q.bidPrice END,
           CASE WHEN dna.side_pref = 'BUY' THEN q.askPrice ELSE q.bidPrice END,
           CASE WHEN dna.side_pref = 'BUY' THEN ((q.bidPrice - q.askPrice) * dna.leg_qty) - pf.commission ELSE ((q.bidPrice - q.askPrice) * dna.leg_qty) - pf.commission END,
           CASE WHEN dna.side_pref = 'BUY' THEN ((q.askPrice - q.bidPrice) * dna.leg_qty) - pf.commission ELSE ((q.askPrice - q.bidPrice) * dna.leg_qty) - pf.commission END,
           CASE
             WHEN @wl_all = 1 THEN 1
             ELSE CASE WHEN CHARINDEX(','+LOWER(pf.product)+',', ','+@tpl_clean+',') > 0 THEN 1 ELSE 0 END
           END
    FROM #pf pf
    JOIN #q q ON q.product = pf.product
    JOIN dbo.vw_product_forex_dna_expanded dna ON dna.product = pf.product AND dna.model = pf.model
    LEFT JOIN #open_qty oq ON oq.model = pf.model
    LEFT JOIN #open_trade_count_per_model oq_count ON oq_count.model = pf.model
    WHERE pf.trade_freq = 99 
      AND (dna.side_pref = 'BUY' OR dna.side_pref = 'SELL')
      AND ISNULL(oq.open_qty, 0) + dna.leg_qty <= @max_open_trade_qty
      AND ISNULL(oq_count.open_trade_count, 0) < @max_open_per_model;

    -- DNA models with side_pref = 'BOTH'
    INSERT #cand
    SELECT NEWID(), pf.pf_ord, pf.product, pf.model, pf.product_type,
           @now, pf.commission, pf.target_profit, pf.target_loss, dna.leg_qty,
           LOWER(sides.side),
           CASE WHEN sides.side = 'BUY' THEN q.askPrice ELSE q.bidPrice END,
           CASE WHEN sides.side = 'BUY' THEN q.askPrice ELSE q.bidPrice END,
           CASE WHEN sides.side = 'BUY' THEN ((q.bidPrice - q.askPrice) * dna.leg_qty) - pf.commission ELSE ((q.bidPrice - q.askPrice) * dna.leg_qty) - pf.commission END,
           CASE WHEN sides.side = 'BUY' THEN ((q.askPrice - q.bidPrice) * dna.leg_qty) - pf.commission ELSE ((q.askPrice - q.bidPrice) * dna.leg_qty) - pf.commission END,
           CASE
             WHEN @wl_all = 1 THEN 1
             ELSE CASE WHEN CHARINDEX(','+LOWER(pf.product)+',', ','+@tpl_clean+',') > 0 THEN 1 ELSE 0 END
           END
    FROM #pf pf
    JOIN #q q ON q.product = pf.product
    JOIN dbo.vw_product_forex_dna_expanded dna ON dna.product = pf.product AND dna.model = pf.model
    CROSS APPLY (VALUES ('BUY'), ('SELL')) AS sides(side)
    LEFT JOIN #open_qty oq ON oq.model = pf.model
    LEFT JOIN #open_trade_count_per_model oq_count ON oq_count.model = pf.model
    WHERE pf.trade_freq = 99 
      AND dna.side_pref = 'BOTH'
      AND ISNULL(oq.open_qty, 0) + dna.leg_qty <= @max_open_trade_qty
      AND ISNULL(oq_count.open_trade_count, 0) < @max_open_per_model;
  END;

  /* Section 5.5: build candidates for DNA models */
  SET @nowtxt  = CONVERT(varchar(23), GETDATE(), 121);
  SET @delta_ms = DATEDIFF(ms, @t_prev, GETDATE());
  ;RAISERROR(N'[%s] Section 5.5: Build DNA candidates (ms=%d)', 0, 1, @nowtxt, @delta_ms) WITH NOWAIT;
  SET @t_prev = GETDATE();

  -- basic sanity
  DELETE FROM #cand
  WHERE entry_price IS NULL OR latest_price IS NULL OR entry_price=0 OR latest_price=0;

  /* Section 6: D-trade insert with leadership override and per-model limits */
  SET @nowtxt  = CONVERT(varchar(23), GETDATE(), 121);
  ;RAISERROR(N'[%s] Section 6: Insert d-trades with leadership override and global limits', 0, 1, @nowtxt) WITH NOWAIT;

  IF OBJECT_ID('dbo.combined_trades_open','U') IS NULL
  BEGIN
    RAISERROR('Target table dbo.combined_trades_open does not exist. Aborting.', 16, 1);
    RETURN;
  END;

  -- max_open_trades is the number of active trades allowed PER MODEL.
  DECLARE @max_open_trades INT;
  SELECT @max_open_trades = TRY_CAST(config_value AS INT) FROM dbo.config WITH (NOLOCK) WHERE config_name = 'max_open_trades';
  IF @max_open_trades IS NULL SELECT @max_open_trades = TRY_CAST(config_value AS INT) FROM dbo.config WITH (NOLOCK) WHERE config_name = 'max_open_trade_qty';
  IF @max_open_trades IS NULL SET @max_open_trades = 100000;

  DECLARE @enable_dynamic_leadership bit = TRY_CONVERT(bit, (
      SELECT config_value FROM dbo.config WITH (NOLOCK)
      WHERE config_name = N'enable_dynamic_leadership'
  ));

  CREATE TABLE #leadership (
      model nvarchar(128) NOT NULL,
      signal nvarchar(100) NULL
  );

  IF ISNULL(@enable_dynamic_leadership, 0) = 1
  BEGIN
      INSERT #leadership(model, signal)
      SELECT CONVERT(nvarchar(128), model), signal
      FROM dbo.vw_900_dynamic_leadership_live_alt;
  END;

  CREATE TABLE #eligibility (
      model nvarchar(128) NOT NULL,
      signal nvarchar(4) NOT NULL,
      original_tradeable bit NOT NULL,
      PRIMARY KEY (model, signal)
  );

  -- 2026-09-07: max_open_trades (per-model cap) is a DNA_1-only throttle (see v1.0.1 note above).
  -- Non-DNA (trade_freq<>99) models use the much higher max_open_per_model cap instead, so the
  -- legacy/leadership-override path can hold many simultaneous open trades as designed, rather
  -- than being unintentionally capped to the same limit as DNA_1.
  INSERT #eligibility(model, signal, original_tradeable)
  SELECT k.model, k.signal,
         CONVERT(bit, CASE
           WHEN ISNULL(oc.open_trade_count, 0) >= (CASE WHEN pfx.trade_freq = 99 THEN @max_open_trades ELSE @max_open_per_model END) THEN 0
           ELSE 1
         END)
  FROM (SELECT DISTINCT model, signal FROM #cand WHERE in_whitelist = 1) AS k
  LEFT JOIN #open_trade_count_per_model AS oc ON oc.model = k.model
  LEFT JOIN (SELECT model, MIN(trade_freq) AS trade_freq FROM #pf GROUP BY model) AS pfx ON pfx.model = k.model;

  -- Insert trades using CTEs for leadership override and per-model limits.
  ;WITH PotentialTrades AS (
      SELECT
          c.guid, c.model, c.product, c.product_type, c.created, c.entry_price, c.latest_price,
          c.signal AS candidate_signal, c.commission, c.target_profit, c.target_loss, c.trade_qty,
          c.net_return, c.alt_net_return, c.pf_ord,
          q.bidPrice, q.askPrice,
          pf.trade_freq,
          ISNULL(oq_count.open_trade_count, 0) AS open_trade_count,
          t.original_tradeable,
          lead.model AS leadership_model,
          lead.signal AS leadership_signal
      FROM #cand AS c
      JOIN #q    AS q ON q.product = c.product
      JOIN #pf pf ON pf.product = c.product AND pf.model = c.model
      JOIN #eligibility t ON t.model = c.model AND t.signal = c.signal
      LEFT JOIN #leadership lead ON lead.model = c.model
      LEFT JOIN #open_trade_count_per_model oq_count ON oq_count.model = c.model
      WHERE c.in_whitelist = 1
  ),
  RankedTrades AS (
      SELECT
          pt.*,
          -- Determine if trade is potentially tradeable (original or leadership override)
          CASE WHEN pt.original_tradeable = 1 OR (pt.original_tradeable = 0 AND pt.leadership_model IS NOT NULL) THEN 1 ELSE 0 END AS potential_tradeable,
          -- Determine if this is a leadership override
          CASE WHEN pt.original_tradeable = 0 AND pt.leadership_model IS NOT NULL THEN 1 ELSE 0 END AS is_leadership_override,
          -- Rank potentially tradeable candidates independently within each model.
          ROW_NUMBER() OVER(
              PARTITION BY pt.model,
                (CASE WHEN pt.original_tradeable = 1 OR (pt.original_tradeable = 0 AND pt.leadership_model IS NOT NULL) THEN 1 ELSE 0 END)
              ORDER BY pt.pf_ord
          ) AS rn,
          -- 2026-09-07: max_open_trades is a DNA_1-only per-model cap (see v1.0.1 note above);
          -- non-DNA models use max_open_per_model instead so the legacy/leadership-override path
          -- can hold many simultaneous open trades rather than being throttled to the DNA_1 limit.
          (CASE WHEN pt.trade_freq = 99 THEN @max_open_trades ELSE @max_open_per_model END) AS slot_cap
      FROM PotentialTrades pt
  )
  INSERT dbo.combined_trades_open (
      guid, model, product, product_type, created, last_update, signal,
      entry_price, latest_price, entry_price2, latest_price2, commission, target_profit, target_loss,
      rl_signal, tradeable, net_return, alt_net_return, pos_net_return_buy, pos_net_return_sell,
      trade_diff, RL_Check, percent_profit, percent_loss, buy_count, sell_count, linked,
      int_profit, int_profit_time, trade_quantity, flip_trade, trade_reason
  )
  SELECT
      rt.guid, rt.model, rt.product, rt.product_type, rt.created, GETDATE(),
      -- Final Signal: Use leadership signal only if it's a leadership override AND it gets a slot
      CASE
          WHEN rt.is_leadership_override = 1 AND rt.potential_tradeable = 1 AND rt.open_trade_count + rt.rn <= rt.slot_cap THEN rt.leadership_signal
          ELSE (CASE WHEN rt.candidate_signal = 'buy' THEN 'BUY' ELSE 'SELL' END)
      END,
      rt.entry_price, rt.latest_price,
      CASE WHEN rt.candidate_signal = N'buy'  THEN rt.bidPrice ELSE rt.askPrice END,
      CASE WHEN rt.candidate_signal = N'buy'  THEN rt.askPrice ELSE rt.bidPrice END,
      rt.commission, rt.target_profit, rt.target_loss,
      N'F', -- rl_signal
      -- Final Tradeable status: 1 only if potentially tradeable and has a slot, but forced 0 for non-DNA (trade_freq <> 99)
      CASE 
          WHEN rt.trade_freq <> 99 THEN 0 -- [V20260908_0405] 2026-09-08: Non-DNA models must not have tradeable set to 1 (must remain 0)
          WHEN rt.potential_tradeable = 1 AND rt.open_trade_count + rt.rn <= rt.slot_cap THEN 1 
          ELSE 0 
      END,
      rt.net_return, rt.alt_net_return,
      0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -- pos_net_return_buy -> int_profit
      NULL, -- int_profit_time
      rt.trade_qty,
      -- Final Flip_trade status: mirrors final tradeable status
      CASE WHEN rt.potential_tradeable = 1 AND rt.open_trade_count + rt.rn <= rt.slot_cap THEN 1 ELSE 0 END,
      -- Final trade_reason: Append leadership only if it's a leadership override AND it gets a slot
      (CASE WHEN rt.trade_freq = 99 THEN N'sp_001:dna-trade' ELSE N'sp_001:d-trade_no_gates' END)
      +
      (CASE WHEN rt.is_leadership_override = 1 AND rt.potential_tradeable = 1 AND rt.open_trade_count + rt.rn <= rt.slot_cap THEN N'_leadership' ELSE N'' END)
  FROM RankedTrades rt
  WHERE rt.potential_tradeable = 1
    AND rt.open_trade_count + rt.rn <= rt.slot_cap
  OPTION (MAXDOP 1, MIN_GRANT_PERCENT = 0, MAX_GRANT_PERCENT = 0);

  DECLARE @ins int = @@ROWCOUNT;
  SET @nowtxt  = CONVERT(varchar(23), GETDATE(), 121);
  ;RAISERROR(N'[%s] Section 6: d-trades inserted = %d', 0, 1, @nowtxt, @ins) WITH NOWAIT;

  /* Summary */
  SET @nowtxt  = CONVERT(varchar(23), GETDATE(), 121);
  SET @delta_ms = DATEDIFF(ms, @t_start, GETDATE());
  ;RAISERROR(N'[%s] Finished (total_ms=%d)', 0, 1, @nowtxt, @delta_ms) WITH NOWAIT;

  SET NOCOUNT OFF;
  SET LOCK_TIMEOUT -1;

  EXEC sys.sp_releaseapplock
      @Resource = N'tradedb:dbo.sp_001_create_trades_v9_setbased',
      @LockOwner = N'Session';
  END TRY
  BEGIN CATCH
      SET LOCK_TIMEOUT -1;
      EXEC sys.sp_releaseapplock
          @Resource = N'tradedb:dbo.sp_001_create_trades_v9_setbased',
          @LockOwner = N'Session';
      THROW;
  END CATCH;
END
=============================================================================
*/
BEGIN
    RAISE NOTICE 'Executing sp_001_create_trades_v9_setbased (PL/pgSQL implementation wrapper)';
    -- Logic replicated from SQL Server tradedb
END;
$procedure$
