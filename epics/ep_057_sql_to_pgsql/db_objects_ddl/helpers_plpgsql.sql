-- =============================================================================
-- LEAF HELPER PROCEDURES & FUNCTIONS (PL/pgSQL)
-- =============================================================================

-- 1. sp_helper_is_sim_db
CREATE OR REPLACE PROCEDURE public.sp_helper_is_sim_db(INOUT is_sim_mode boolean)
LANGUAGE plpgsql
AS $$
DECLARE
    v_db_name text := current_database();
BEGIN
    IF lower(v_db_name) LIKE '%sim%' THEN
        is_sim_mode := TRUE;
    ELSE
        is_sim_mode := FALSE;
    END IF;
END;
$$;

-- 2. sp_helper_check_alt_net_return
CREATE OR REPLACE PROCEDURE public.sp_helper_check_alt_net_return(
    IN p_product text,
    IN p_trade_reason text,
    IN p_signal text,
    INOUT is_profitable boolean
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_total_alt_net numeric(38, 8) := 0;
    v_scan_period_mins integer := 180;
    v_cfg text;
BEGIN
    SELECT config_value INTO v_cfg FROM public.config WHERE config_name = 'scan_analysis_period' LIMIT 1;
    IF v_cfg IS NOT NULL AND v_cfg ~ '^[0-9]+$' THEN
        v_scan_period_mins := v_cfg::integer;
    END IF;

    SELECT COALESCE(SUM(actual_net), 0) INTO v_total_alt_net
    FROM public.vwcombined_trades_closed
    WHERE product = p_product
      AND lower(signal) = lower(p_signal)
      AND trade_reason = p_trade_reason
      AND created >= CURRENT_TIMESTAMP - (v_scan_period_mins || ' minute')::interval;

    IF v_total_alt_net > 0 THEN
        is_profitable := TRUE;
    ELSE
        is_profitable := FALSE;
    END IF;
END;
$$;

-- 3. sp_9004_settrailingstoplossonprofit
CREATE OR REPLACE PROCEDURE public.sp_9004_settrailingstoplossonprofit(
    IN p_model text,
    INOUT p_rows_affected integer DEFAULT 0
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_profit_protect_percent numeric(18, 8);
    v_profit_protect_trigger numeric(18, 8);
    v_profit_protection_list text;
    v_pct_text text;
    v_trig_text text;
BEGIN
    p_rows_affected := 0;
    IF p_model IS NULL OR trim(p_model) = '' THEN
        RETURN;
    END IF;

    SELECT config_value INTO v_pct_text FROM public.config WHERE config_name = 'profit_protect_percent' LIMIT 1;
    SELECT config_value INTO v_trig_text FROM public.config WHERE config_name = 'profit_protect_trigger' LIMIT 1;
    SELECT config_value INTO v_profit_protection_list FROM public.config WHERE config_name = 'profit_protection_list' LIMIT 1;

    IF v_pct_text ~ '^[0-9]+(\.[0-9]+)?$' THEN
        v_profit_protect_percent := v_pct_text::numeric;
    END IF;
    IF v_trig_text ~ '^[0-9]+(\.[0-9]+)?$' THEN
        v_profit_protect_trigger := v_trig_text::numeric;
    END IF;

    IF v_profit_protect_percent IS NULL OR v_profit_protect_percent <= 0 OR
       v_profit_protect_trigger IS NULL OR v_profit_protect_trigger <= 0 OR
       v_profit_protection_list IS NULL OR trim(v_profit_protection_list) = '' THEN
        RETURN;
    END IF;

    CREATE TEMP TABLE IF NOT EXISTS _profit_protection_reasons (trade_reason text PRIMARY KEY) ON COMMIT DROP;
    TRUNCATE _profit_protection_reasons;

    INSERT INTO _profit_protection_reasons (trade_reason)
    SELECT trim(both '''' from trim(s))
    FROM unnest(string_to_array(v_profit_protection_list, ',')) s
    WHERE trim(s) <> ''
    ON CONFLICT DO NOTHING;

    UPDATE public.combined_trades_open cto
    SET target_loss = (cto.max_net_return * v_profit_protect_percent / 100)
    FROM _profit_protection_reasons pptr
    WHERE cto.trade_reason = pptr.trade_reason
      AND cto.model = p_model
      AND cto.max_net_return >= v_profit_protect_trigger
      AND cto.max_net_return IS NOT NULL 
      AND cto.max_net_return > 0
      AND (cto.target_loss IS NULL OR (cto.max_net_return * v_profit_protect_percent / 100) > cto.target_loss);

    GET DIAGNOSTICS p_rows_affected = ROW_COUNT;
END;
$$;

-- 4. sp_9002_checktradesignalforclosure
CREATE OR REPLACE PROCEDURE public.sp_9002_checktradesignalforclosure(
    IN p_open_trade_guid uuid,
    IN p_model text,
    IN p_incoming_signal text,
    INOUT p_close_trade boolean DEFAULT FALSE
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_is_tradeable integer;
    v_last_signal text;
    v_last_return numeric(18, 8);
BEGIN
    p_close_trade := FALSE;

    SELECT tradeable INTO v_is_tradeable
    FROM public.combined_trades_open
    WHERE guid = p_open_trade_guid
    LIMIT 1;

    IF v_is_tradeable IS NULL OR v_is_tradeable = 0 THEN
        p_close_trade := FALSE;
        RETURN;
    END IF;

    SELECT signal, alt_net_return INTO v_last_signal, v_last_return
    FROM public.combined_trades_closed
    WHERE model = p_model
    ORDER BY last_update DESC
    LIMIT 1;

    IF v_last_signal IS NULL THEN
        p_close_trade := FALSE;
        RETURN;
    END IF;

    IF lower(v_last_signal) = lower(p_incoming_signal) AND v_last_return < 0.0 THEN
        p_close_trade := TRUE;
    ELSIF lower(v_last_signal) <> lower(p_incoming_signal) AND v_last_return > 0.0 THEN
        p_close_trade := TRUE;
    ELSE
        p_close_trade := FALSE;
    END IF;
END;
$$;

-- 5. usp_cleanup_stale_open_trades
CREATE OR REPLACE PROCEDURE public.usp_cleanup_stale_open_trades()
LANGUAGE plpgsql
AS $$
DECLARE
    v_rows_deleted integer := 0;
    v_started timestamp := TIMEZONE('utc', CURRENT_TIMESTAMP);
    v_run_id bigint;
BEGIN
    INSERT INTO public.stale_open_cleanup_run_log (started_at, status)
    VALUES (v_started, 'running')
    RETURNING run_id INTO v_run_id;

    BEGIN
        DELETE FROM public.combined_trades_open o
        WHERE EXISTS (
            SELECT 1 FROM public.combined_trades_closed c 
            WHERE c.guid = o.guid
        );
        GET DIAGNOSTICS v_rows_deleted = ROW_COUNT;

        UPDATE public.stale_open_cleanup_run_log
        SET completed_at = TIMEZONE('utc', CURRENT_TIMESTAMP),
            status = 'success',
            rows_deleted = v_rows_deleted
        WHERE run_id = v_run_id;
    EXCEPTION WHEN OTHERS THEN
        UPDATE public.stale_open_cleanup_run_log
        SET completed_at = TIMEZONE('utc', CURRENT_TIMESTAMP),
            status = 'failed',
            error_message = SQLERRM
        WHERE run_id = v_run_id;
        RAISE;
    END;
END;
$$;
