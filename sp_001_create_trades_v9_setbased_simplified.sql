USE [tradedb]
GO

SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

ALTER PROCEDURE [dbo].[sp_001_create_trades_v9_setbased]
AS
BEGIN
  SET NOCOUNT ON;
  SET XACT_ABORT ON;
  SET FORCEPLAN OFF;

  /* ==== timing helpers (declare BEFORE first use) ==== */
  DECLARE @t_start  datetime2(3) = GETDATE();
  DECLARE @t_prev   datetime2(3) = @t_start;
  DECLARE @nowtxt   varchar(23);
  DECLARE @delta_ms int;

  /* Section 1: start + load quotes */
  SET @nowtxt  = CONVERT(varchar(23), GETDATE(), 121);
  SET @delta_ms = DATEDIFF(ms, @t_prev, GETDATE());
  ;RAISERROR(N'[%s] Section 1: Start - Load FX Quotes (ms=%d)', 0, 1, @nowtxt, @delta_ms) WITH NOWAIT;
  SET @t_prev = GETDATE();

  IF OBJECT_ID('dbo.sp_000_LoadFxQuotesFromJson_01','P') IS NOT NULL
      EXEC dbo.sp_000_LoadFxQuotesFromJson_01;

  /* Section 2: config & trading window */
  SET @nowtxt  = CONVERT(varchar(23), GETDATE(), 121);
  SET @delta_ms = DATEDIFF(ms, @t_prev, GETDATE());
  ;RAISERROR(N'[%s] Section 2: Config & window (ms=%d)', 0, 1, @nowtxt, @delta_ms) WITH NOWAIT;
  SET @t_prev = GETDATE();

  DECLARE @now datetime2(3) = GETDATE();

  DECLARE @is_sim_mode bit;
  EXEC dbo.sp_helper_is_sim_db @is_sim_mode = @is_sim_mode OUTPUT;

  DECLARE @trade_product_list_raw nvarchar(max) =
      (SELECT config_value FROM dbo.config WHERE config_name='trade_product_list');
  IF @trade_product_list_raw IS NULL SET @trade_product_list_raw = N'';

  -- normalize whitelist: lower-case, strip quotes/spaces
  DECLARE @trade_product_list nvarchar(max) =
      LOWER(REPLACE(REPLACE(@trade_product_list_raw,'''',''), ' ', ''));

  DECLARE @trade_start time(0) =
      TRY_CONVERT(time(0),(SELECT config_value FROM dbo.config WHERE config_name='trade_start'));
  IF @trade_start IS NULL SET @trade_start = '00:00';

  DECLARE @trade_end   time(0) =
      TRY_CONVERT(time(0),(SELECT config_value FROM dbo.config WHERE config_name='trade_end'));
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
  SELECT ROW_NUMBER() OVER (ORDER BY product, model) AS pf_ord,
         product, model, commission, target_profit, target_loss, trade_qty, product_type, trade_freq, dna_array, dna_json
  INTO #pf
  FROM dbo.product_forex
  WHERE trade_freq <> 0; -- GEMINI: 2025-10-11 - Exclude models with trade_freq = 0

  DECLARE @max_open_trade_qty INT;
  SELECT @max_open_trade_qty = TRY_CAST(config_value AS INT) FROM dbo.config WHERE config_name = 'max_open_trade_qty';
  IF @max_open_trade_qty IS NULL SET @max_open_trade_qty = 100000;

  IF OBJECT_ID('tempdb..#open_qty') IS NOT NULL DROP TABLE #open_qty;
  SELECT model, SUM(trade_quantity) AS open_qty
  INTO #open_qty
  FROM dbo.combined_trades_open
  WHERE tradeable = 1
  GROUP BY model;

  /* Section 4: latest quotes per product */
  SET @nowtxt  = CONVERT(varchar(23), GETDATE(), 121);
  SET @delta_ms = DATEDIFF(ms, @t_prev, GETDATE());
  ;RAISERROR(N'[%s] Section 4: Latest quotes by product (ms=%d)', 0, 1, @nowtxt, @delta_ms) WITH NOWAIT;
  SET @t_prev = GETDATE();

  IF OBJECT_ID('tempdb..#q') IS NOT NULL DROP TABLE #q;
  SELECT p.product,
         q.ask AS askPrice,
         q.bid AS bidPrice
  INTO #q
  FROM (SELECT DISTINCT product FROM #pf) AS p
  OUTER APPLY (
     SELECT TOP 1 ask, bid
     FROM dbo.fx_quotes WITH (READPAST)
     WHERE code = p.product
     ORDER BY [timestamp] DESC
  ) q;

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
     target_profit smallint NULL,  -- Allow NULL
     target_loss smallint NULL,    -- Allow NULL
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

  -- BUY rows (entry=ask, latest=ask) - Only for non-DNA models
  INSERT #cand
  SELECT NEWID(), pf.pf_ord, pf.product, pf.model, pf.product_type,
         @now, pf.commission, 
         ISNULL(pf.target_profit, 0),  -- Handle NULL target_profit
         ISNULL(pf.target_loss, 0),    -- Handle NULL target_loss
         pf.trade_qty,
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
  WHERE pf.trade_freq <> 99; -- GEMINI: 2025-10-11 - Exclude DNA models from continuous trade creation

  -- SELL rows (entry=bid, latest=bid) - Only for non-DNA models
  INSERT #cand
  SELECT NEWID(), pf.pf_ord, pf.product, pf.model, pf.product_type,
         @now, pf.commission, 
         ISNULL(pf.target_profit, 0),  -- Handle NULL target_profit
         ISNULL(pf.target_loss, 0),    -- Handle NULL target_loss
         pf.trade_qty,
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
  WHERE pf.trade_freq <> 99; -- GEMINI: 2025-10-11 - Exclude DNA models from continuous trade creation

  /* Section 5.5: build candidates for DNA models */
  SET @nowtxt  = CONVERT(varchar(23), GETDATE(), 121);
  SET @delta_ms = DATEDIFF(ms, @t_prev, GETDATE());
  ;RAISERROR(N'[%s] Section 5.5: Build DNA candidates (ms=%d)', 0, 1, @nowtxt, @delta_ms) WITH NOWAIT;
  SET @t_prev = GETDATE();

  -- basic sanity
  DELETE FROM #cand
  WHERE entry_price IS NULL OR latest_price IS NULL OR entry_price=0 OR latest_price=0;

  /* Section 6: D-trade insert (no 700/701/703; always insert BUY & SELL as tradeable=0, flip_trade=0) */
  SET @nowtxt  = CONVERT(varchar(23), GETDATE(), 121);
  ;RAISERROR(N'[%s] Section 6: Insert d-trades (no 700/701/703)', 0, 1, @nowtxt) WITH NOWAIT;

  IF OBJECT_ID('dbo.combined_trades_open','U') IS NULL
  BEGIN
    RAISERROR('Target table dbo.combined_trades_open does not exist. Aborting.', 16, 1);
    RETURN;
  END;

  /* === REPLACE your current unconditional insert with this === */
	INSERT dbo.combined_trades_open (
		guid, model, product, product_type,           -- 1-4
		created, last_update, signal,                  -- 5-7
		entry_price, latest_price,                     -- 8-9
		entry_price2, latest_price2,                   -- 10-11
		commission, target_profit, target_loss,        -- 12-14
		rl_signal, tradeable,                          -- 15-16
		net_return, alt_net_return,                    -- 17-18
		pos_net_return_buy, pos_net_return_sell,       -- 19-20
		trade_diff, RL_Check,                          -- 21-22
		percent_profit, percent_loss,                  -- 23-24
		buy_count, sell_count, linked,                 -- 25-27
		int_profit, int_profit_time, trade_quantity,   -- 28-30
		flip_trade, trade_reason                       -- 31-32
	)
	SELECT
		c.guid,
		c.model,
		c.product,
		c.product_type,
		c.created,
		GETDATE(),
		CASE WHEN c.signal = N'buy' THEN N'BUY' ELSE N'SELL' END,
		c.entry_price,
		c.latest_price,
		CASE WHEN c.signal = N'buy'  THEN q.bidPrice ELSE q.askPrice END,
		CASE WHEN c.signal = N'buy'  THEN q.askPrice ELSE q.bidPrice END,
		c.commission,
		ISNULL(c.target_profit, 0),  -- Handle NULL target_profit
		ISNULL(c.target_loss, 0),    -- Handle NULL target_loss
		N'F',
		0, -- tradeable
		c.net_return,
		c.alt_net_return,
		0, 0,                           -- pos_net_return_buy/sell
		0, 0,                           -- trade_diff, RL_Check
		0, 0,                           -- percent_profit, percent_loss
		0, 0, 0,                        -- buy_count, sell_count, linked
		0, NULL,                        -- int_profit, int_profit_time
		c.trade_qty,                    -- trade_quantity
		0,                              -- flip_trade = 0
		CASE WHEN pf.trade_freq = 99 THEN N'sp_001:dna-trade' ELSE N'sp_001:d-trade_no_gates' END -- trade_reason
	FROM #cand AS c
	JOIN #q    AS q ON q.product = c.product
    JOIN #pf pf ON pf.product = c.product AND pf.model = c.model
	WHERE c.in_whitelist = 1;           -- drop this line if you want truly all


  DECLARE @ins int = @@ROWCOUNT;
  SET @nowtxt  = CONVERT(varchar(23), GETDATE(), 121);
  ;RAISERROR(N'[%s] Section 6: d-trades inserted = %d', 0, 1, @nowtxt, @ins) WITH NOWAIT;

  /* Summary */
  SET @nowtxt  = CONVERT(varchar(23), GETDATE(), 121);
  SET @delta_ms = DATEDIFF(ms, @t_start, GETDATE());
  ;RAISERROR(N'[%s] Finished (total_ms=%d)', 0, 1, @nowtxt, @delta_ms) WITH NOWAIT;

  SET NOCOUNT OFF;
END
GO