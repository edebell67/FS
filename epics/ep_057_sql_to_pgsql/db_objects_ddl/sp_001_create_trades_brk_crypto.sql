CREATE OR REPLACE PROCEDURE public.sp_001_create_trades_brk_crypto()
 LANGUAGE plpgsql
AS $procedure$
DECLARE
    v_now timestamp := CURRENT_TIMESTAMP;
    v_product_list text;
    v_max_open_trade_qty bigint := 100000;
    v_max_open_trades integer := 1;
    v_inserted integer := 0;
BEGIN
    INSERT INTO public.crypto_quotes_history
        (timestamp, code, type, bid, ask, volume, provider)
    SELECT q.timestamp, LOWER(q.code), q.type, q.bid, q.ask, q.volume, q.provider
    FROM public.crypto_quotes q
    WHERE q.bid > 0 AND q.ask > 0
    ON CONFLICT (code, timestamp) DO NOTHING;

    DELETE FROM public.crypto_quotes_history
    WHERE timestamp < CURRENT_TIMESTAMP - INTERVAL '1 hour';

    SELECT LOWER(REPLACE(REPLACE(COALESCE(config_value, ''), '''', ''), ' ', ''))
      INTO v_product_list
      FROM public.config
     WHERE config_name = 'trade_crypto_product_list';

    v_product_list := COALESCE(v_product_list, '');

    SELECT COALESCE(tsql_compat.try_convert_numeric(config_value), 100000)::bigint
      INTO v_max_open_trade_qty
      FROM public.config
     WHERE config_name = 'max_open_trade_qty';
    v_max_open_trade_qty := COALESCE(v_max_open_trade_qty, 100000);

    SELECT COALESCE(tsql_compat.try_convert_numeric(config_value), 1)::integer
      INTO v_max_open_trades
      FROM public.config
     WHERE config_name = 'max_open_trades';
    v_max_open_trades := GREATEST(COALESCE(v_max_open_trades, 1), 1);

    CREATE TEMP TABLE IF NOT EXISTS tt_crypto_pf (
        pf_ord integer,
        product varchar(50),
        model text,
        commission double precision,
        target_profit smallint,
        target_loss smallint,
        trade_qty bigint,
        product_type varchar(50),
        window_size integer,
        pip_buffer numeric(18,8),
        allow_reversal boolean,
        contrarian boolean
    ) ON COMMIT DROP;
    TRUNCATE tt_crypto_pf;

    INSERT INTO tt_crypto_pf
    SELECT
        ROW_NUMBER() OVER (ORDER BY product, model)::integer,
        product,
        model,
        commission::double precision,
        target_profit,
        target_loss,
        trade_qty,
        product_type,
        COALESCE(NULLIF(dna_json, '')::jsonb->>'window_size', '3')::integer,
        COALESCE(
            (NULLIF(dna_json, '')::jsonb->>'pip_buffer')::numeric,
            CASE product
                WHEN 'ada'  THEN 0.0001
                WHEN 'avax' THEN 0.001
                WHEN 'btc'  THEN 0.01
                WHEN 'doge' THEN 0.00001
                WHEN 'eth'  THEN 0.01
                WHEN 'sol'  THEN 0.01
                WHEN 'xrp'  THEN 0.0001
                ELSE 0
            END
        )::numeric(18,8),
        COALESCE((NULLIF(dna_json, '')::jsonb->>'allow_reversal')::boolean, false),
        COALESCE((NULLIF(dna_json, '')::jsonb->>'contrarian')::boolean, false)
    FROM public.product_forex
    WHERE product_type = 'crypto'
      AND model ILIKE 'dna\_3%' ESCAPE '\'
      AND trade_freq = 98;

    IF NOT EXISTS (SELECT 1 FROM tt_crypto_pf) THEN
        RAISE NOTICE 'sp_001_create_trades_brk_crypto: no enabled DNA_3 models (requires trade_freq=98).';
        RETURN;
    END IF;

    CREATE TEMP TABLE IF NOT EXISTS tt_crypto_q (
        product varchar(50) PRIMARY KEY,
        ask_price double precision,
        bid_price double precision
    ) ON COMMIT DROP;
    TRUNCATE tt_crypto_q;

    INSERT INTO tt_crypto_q
    SELECT DISTINCT ON (LOWER(q.code))
        LOWER(q.code), q.ask::double precision, q.bid::double precision
    FROM public.crypto_quotes q
    JOIN (SELECT DISTINCT product FROM tt_crypto_pf) p ON p.product = LOWER(q.code)
    WHERE q.ask > 0 AND q.bid > 0
    ORDER BY LOWER(q.code), q.timestamp DESC, q.id DESC;

    CREATE TEMP TABLE IF NOT EXISTS tt_crypto_bounds (
        product varchar(50),
        window_size integer,
        min_bid double precision,
        max_bid double precision,
        min_ask double precision,
        max_ask double precision,
        quote_count bigint,
        PRIMARY KEY (product, window_size)
    ) ON COMMIT DROP;
    TRUNCATE tt_crypto_bounds;

    INSERT INTO tt_crypto_bounds
    WITH required_windows AS (
        SELECT DISTINCT product, window_size FROM tt_crypto_pf
    ), ranked AS (
        SELECT LOWER(code) AS product, bid::double precision AS bid, ask::double precision AS ask,
               ROW_NUMBER() OVER (PARTITION BY LOWER(code) ORDER BY timestamp DESC, id DESC) AS rn
        FROM public.crypto_quotes_history
        WHERE bid > 0 AND ask > 0
    )
    SELECT r.product, w.window_size,
           MIN(r.bid), MAX(r.bid), MIN(r.ask), MAX(r.ask), COUNT(*)
    FROM required_windows w
    JOIN ranked r ON r.product = w.product
                 AND r.rn > 1
                 AND r.rn <= w.window_size + 1
    GROUP BY r.product, w.window_size;

    CREATE TEMP TABLE IF NOT EXISTS tt_crypto_cand (
        guid varchar(64) PRIMARY KEY,
        pf_ord integer,
        product varchar(50),
        model text,
        product_type varchar(50),
        created timestamp,
        commission double precision,
        target_profit smallint,
        target_loss smallint,
        trade_qty bigint,
        signal varchar(10),
        entry_price double precision,
        latest_price double precision,
        net_return double precision,
        alt_net_return double precision,
        allow_reversal boolean
    ) ON COMMIT DROP;
    TRUNCATE tt_crypto_cand;

    INSERT INTO tt_crypto_cand
    SELECT gen_random_uuid()::varchar, pf.pf_ord, pf.product, pf.model, pf.product_type,
           v_now, pf.commission, pf.target_profit, pf.target_loss, pf.trade_qty,
           'buy', q.ask_price, q.ask_price,
           ((q.bid_price-q.ask_price)*pf.trade_qty)-pf.commission,
           ((q.ask_price-q.bid_price)*pf.trade_qty)-pf.commission,
           pf.allow_reversal
    FROM tt_crypto_pf pf
    JOIN tt_crypto_q q ON q.product=pf.product
    JOIN tt_crypto_bounds b ON b.product=pf.product AND b.window_size=pf.window_size
    WHERE b.quote_count=pf.window_size
      AND (v_product_list='' OR POSITION(','||LOWER(pf.product)||',' IN ','||v_product_list||',')>0)
      AND ((NOT pf.contrarian AND q.ask_price>b.max_ask+pf.pip_buffer)
        OR (pf.contrarian AND q.ask_price<b.min_ask-pf.pip_buffer));

    INSERT INTO tt_crypto_cand
    SELECT gen_random_uuid()::varchar, pf.pf_ord, pf.product, pf.model, pf.product_type,
           v_now, pf.commission, pf.target_profit, pf.target_loss, pf.trade_qty,
           'sell', q.bid_price, q.bid_price,
           ((q.bid_price-q.ask_price)*pf.trade_qty)-pf.commission,
           ((q.ask_price-q.bid_price)*pf.trade_qty)-pf.commission,
           pf.allow_reversal
    FROM tt_crypto_pf pf
    JOIN tt_crypto_q q ON q.product=pf.product
    JOIN tt_crypto_bounds b ON b.product=pf.product AND b.window_size=pf.window_size
    WHERE b.quote_count=pf.window_size
      AND (v_product_list='' OR POSITION(','||LOWER(pf.product)||',' IN ','||v_product_list||',')>0)
      AND ((NOT pf.contrarian AND q.bid_price<b.min_bid-pf.pip_buffer)
        OR (pf.contrarian AND q.bid_price>b.max_bid+pf.pip_buffer));

    -- A reversal-capable candidate closes an active opposite-side trade first.
    WITH reversals AS (
        SELECT DISTINCT ON (o.guid)
               o.guid,
               CASE WHEN LOWER(o.signal)='buy' THEN q.bid_price ELSE q.ask_price END AS exit_price
        FROM tt_crypto_cand c
        JOIN public.combined_trades_open o
          ON o.model=c.model AND COALESCE(o.tradeable,0)>0 AND LOWER(o.signal)<>LOWER(c.signal)
        JOIN tt_crypto_q q ON q.product=o.product
        WHERE c.allow_reversal
    ), closed AS (
        INSERT INTO public.combined_trades_closed (
            guid,model,product,product_type,created,last_update,signal,
            entry_price,latest_price,entry_price2,latest_price2,commission,target_profit,target_loss,
            rl_signal,tradeable,net_return,alt_net_return,pos_net_return_buy,pos_net_return_sell,
            trade_diff,rl_check,percent_profit,percent_loss,buy_count,sell_count,linked,
            int_profit,int_profit_time,trade_quantity,min_net_return,min_net_return_time,
            max_net_return,max_net_return_time,flip_trade,trade_reason,g_close_time,
            g_net_return,g_alt_net_return,strategy_name,close_type)
        SELECT o.guid,o.model,o.product,o.product_type,o.created,CURRENT_TIMESTAMP,o.signal,
               o.entry_price,r.exit_price,o.entry_price2,r.exit_price,o.commission,o.target_profit,o.target_loss,
               o.rl_signal,CASE WHEN o.tradeable=2 THEN 3 ELSE o.tradeable END,
               CASE WHEN LOWER(o.signal)='buy' THEN ((r.exit_price-o.entry_price)*o.trade_quantity)-o.commission
                    ELSE ((o.entry_price-r.exit_price)*o.trade_quantity)-o.commission END,
               CASE WHEN LOWER(o.signal)='buy' THEN ((o.entry_price-r.exit_price)*o.trade_quantity)-o.commission
                    ELSE ((r.exit_price-o.entry_price)*o.trade_quantity)-o.commission END,
               o.pos_net_return_buy,o.pos_net_return_sell,o.trade_diff,o.rl_check::double precision,
               o.percent_profit,o.percent_loss,o.buy_count,o.sell_count,o.linked,
               o.int_profit,o.int_profit_time,o.trade_quantity,o.min_net_return,o.min_net_return_time,
               o.max_net_return,o.max_net_return_time,(COALESCE(o.flip_trade,0) <> 0),o.trade_reason,CURRENT_TIMESTAMP,
               o.g_net_return,o.g_alt_net_return,o.strategy_name,'Reversed'
        FROM reversals r JOIN public.combined_trades_open o ON o.guid=r.guid
        RETURNING guid
    )
    DELETE FROM public.combined_trades_open o USING closed c WHERE o.guid=c.guid;

    DELETE FROM tt_crypto_cand c
    WHERE EXISTS (
        SELECT 1 FROM public.combined_trades_open o
        WHERE o.model=c.model AND COALESCE(o.tradeable,0)>0
    );

    WITH open_stats AS (
        SELECT model,
               COALESCE(SUM(trade_quantity),0)::bigint AS open_qty,
               COUNT(*) FILTER (WHERE COALESCE(tradeable,0)>0)::integer AS open_count
        FROM public.combined_trades_open
        WHERE model ILIKE 'dna\_3%' ESCAPE '\'
        GROUP BY model
    ), ranked AS (
        SELECT c.*,q.bid_price,q.ask_price,
               COALESCE(s.open_qty,0) AS open_qty,
               COALESCE(s.open_count,0) AS open_count,
               ROW_NUMBER() OVER (PARTITION BY c.model ORDER BY c.pf_ord,c.guid) AS rn
        FROM tt_crypto_cand c
        JOIN tt_crypto_q q ON q.product=c.product
        LEFT JOIN open_stats s ON s.model=c.model
    )
    INSERT INTO public.combined_trades_open (
        guid,model,product,product_type,created,last_update,signal,
        entry_price,latest_price,entry_price2,latest_price2,commission,target_profit,target_loss,
        rl_signal,tradeable,net_return,alt_net_return,pos_net_return_buy,pos_net_return_sell,
        trade_diff,rl_check,percent_profit,percent_loss,buy_count,sell_count,linked,
        int_profit,int_profit_time,trade_quantity,flip_trade,trade_reason,strategy_name)
    SELECT r.guid,r.model,r.product,r.product_type,r.created,CURRENT_TIMESTAMP,r.signal,
           r.entry_price,r.latest_price,
           CASE WHEN r.signal='buy' THEN r.bid_price ELSE r.ask_price END,
           CASE WHEN r.signal='buy' THEN r.bid_price ELSE r.ask_price END,
           r.commission,r.target_profit,r.target_loss,'F',1,r.net_return,r.alt_net_return,
           0,0,0,'0',0,0,0,0,0,0,NULL,r.trade_qty,0,'sp_001:dna3-crypto-trade',
           (SELECT pf.strategy_name FROM public.product_forex pf WHERE pf.model=r.model LIMIT 1)
    FROM ranked r
    WHERE r.open_qty+r.trade_qty<=v_max_open_trade_qty
      AND r.open_count+r.rn<=v_max_open_trades;

    GET DIAGNOSTICS v_inserted = ROW_COUNT;
    RAISE NOTICE 'sp_001_create_trades_brk_crypto: inserted % DNA_3 crypto trades.', v_inserted;
END;
$procedure$
