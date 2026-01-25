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

  DECLARE @now datetime2(3) = GETDATE();

  /* Section 3: PF universe */
  IF OBJECT_ID('tempdb..#pf') IS NOT NULL DROP TABLE #pf;
  SELECT ROW_NUMBER() OVER (ORDER BY product, model) AS pf_ord,
         product, model, commission, target_profit, target_loss, trade_qty, product_type, trade_freq, dna_array, dna_json
  INTO #pf
  FROM dbo.product_forex
  WHERE trade_freq <> 0; -- GEMINI: 2025-10-11 - Exclude models with trade_freq = 0

  /* Section 4: latest quotes per product */
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
         1  -- in_whitelist
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
         1  -- in_whitelist
  FROM #pf pf
  JOIN #q  q ON q.product = pf.product
  WHERE pf.trade_freq <> 99; -- GEMINI: 2025-10-11 - Exclude DNA models from continuous trade creation

  -- basic sanity
  DELETE FROM #cand
  WHERE entry_price IS NULL OR latest_price IS NULL OR entry_price=0 OR latest_price=0;

  /* Section 6: D-trade insert (no 700/701/703; always insert BUY & SELL as tradeable=0, flip_trade=0) */
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
  RAISERROR(N'D-trades inserted = %d', 0, 1, @ins) WITH NOWAIT;

  SET NOCOUNT OFF;
END
GO