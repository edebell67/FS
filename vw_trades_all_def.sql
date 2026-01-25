 SELECT t.trade_id,
    t.run_mode,
    t.product,
    t.direction,
    t.status,
    t.entry_time,
    t.entry_price,
    t.exit_time,
    t.exit_price,
    t.exit_reason,
    t.net_return,
    t.alt_net,
    t.script_name,
    t.is_live_trade,
    t.order_sent_net,
    t.order_sent_alt,
    t.raw_data,
    t.source_path,
    t.strategy_key,
    t.max_net_return,
    t.target_profit,
    t.target_loss,
    t.tp_pips,
    t.sl_pips,
    t.commission_pips,
    t.spread_pips,
    t.window_size,
    t.pip_buffer,
    t.created_at,
    t.updated_at,
        CASE
            WHEN t.status::text = 'OPEN'::text AND q.product IS NOT NULL THEN
            CASE
                WHEN t.direction::text = 'LONG'::text THEN q.bid
                ELSE q.ask
            END
            ELSE t.exit_price
        END AS display_exit_price,
        CASE
            WHEN t.status::text = 'OPEN'::text AND q.product IS NOT NULL THEN
            CASE
                WHEN t.direction::text = 'LONG'::text THEN (q.bid - t.entry_price) * 100000::numeric - COALESCE(t.commission_pips, 0::numeric) - COALESCE(t.spread_pips, 0::numeric)
                ELSE (t.entry_price - q.ask) * 100000::numeric - COALESCE(t.commission_pips, 0::numeric) - COALESCE(t.spread_pips, 0::numeric)
            END
            ELSE t.net_return
        END AS display_net_return,
        CASE
            WHEN t.status::text = 'OPEN'::text AND q.product IS NOT NULL THEN
            CASE
                WHEN t.direction::text = 'LONG'::text THEN (q.bid - t.entry_price) * 100000::numeric
                ELSE (t.entry_price - q.ask) * 100000::numeric
            END
            ELSE t.alt_net
        END AS display_alt_net
   FROM trades t
     LEFT JOIN latest_quotes q ON t.product::text = q.product::text AND t.status::text = 'OPEN'::text
  WHERE t.entry_time >= CURRENT_DATE;
