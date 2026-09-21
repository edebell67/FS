-- =============================================================================
-- sp_002_UpdateCombinedTradesOpen (PL/pgSQL)
-- =============================================================================

CREATE OR REPLACE PROCEDURE public.sp_002_updatecombinedtradesopen()
LANGUAGE plpgsql
AS $$
DECLARE
    r_prod record;
    v_bid numeric(18, 8);
    v_ask numeric(18, 8);
    v_now timestamp := CURRENT_TIMESTAMP;
BEGIN
    -- 1) Refresh latest quotes if loader exists
    BEGIN
        CALL public.sp_000_loadfxquotesfromjson_01();
    EXCEPTION WHEN OTHERS THEN
        -- Non-blocking if optional external JSON loader is absent
        NULL;
    END;

    -- 2) Loop over each distinct product with open trades
    FOR r_prod IN 
        SELECT DISTINCT product 
        FROM public.combined_trades_open 
        WHERE product IS NOT NULL
    LOOP
        v_bid := NULL;
        v_ask := NULL;

        -- 3a) Fetch latest bid and ask from fx_quotes
        SELECT bid, ask INTO v_bid, v_ask
        FROM public.fx_quotes
        WHERE code = r_prod.product
        ORDER BY timestamp DESC
        LIMIT 1;

        -- 3b) Non-positive price guard
        IF (v_bid IS NOT NULL AND v_bid <= 0) OR (v_ask IS NOT NULL AND v_ask <= 0) THEN
            RAISE EXCEPTION 'Non-positive price detected (product=%, bid=%, ask=%). Procedure terminated.',
                r_prod.product, v_bid, v_ask;
        END IF;

        -- 4) Atomically update all open trades for this product
        IF v_bid IS NOT NULL AND v_ask IS NOT NULL THEN
            UPDATE public.combined_trades_open c
            SET
                latest_price = CASE WHEN lower(c.signal) IN ('buy', 'b') THEN v_bid ELSE v_ask END,
                latest_price2 = CASE WHEN lower(c.signal) IN ('buy', 'b') THEN v_ask ELSE v_bid END,
                net_return = calc.computed_net,
                alt_net_return = calc.computed_alt_net,
                last_update = v_now,
                max_net_return = CASE 
                    WHEN c.max_net_return IS NULL OR calc.computed_net > c.max_net_return THEN calc.computed_net
                    ELSE c.max_net_return 
                END,
                max_net_return_time = CASE 
                    WHEN c.max_net_return IS NULL OR calc.computed_net > c.max_net_return THEN v_now
                    ELSE c.max_net_return_time 
                END,
                min_net_return = CASE 
                    WHEN c.min_net_return IS NULL OR calc.computed_net < c.min_net_return THEN calc.computed_net
                    ELSE c.min_net_return 
                END,
                min_net_return_time = CASE 
                    WHEN c.min_net_return IS NULL OR calc.computed_net < c.min_net_return THEN v_now
                    ELSE c.min_net_return_time 
                END
            FROM (
                SELECT 
                    guid,
                    CASE WHEN lower(signal) IN ('buy', 'b')
                         THEN (v_bid - entry_price) * trade_quantity - commission
                         ELSE (entry_price - v_ask) * trade_quantity - commission
                    END AS computed_net,
                    CASE WHEN lower(signal) IN ('buy', 'b')
                         THEN (entry_price2 - v_ask) * trade_quantity - commission
                         ELSE (v_bid - entry_price2) * trade_quantity - commission
                    END AS computed_alt_net
                FROM public.combined_trades_open
                WHERE product = r_prod.product
            ) calc
            WHERE c.guid = calc.guid;
        END IF;
    END LOOP;
END;
$$;
