 SELECT run_mode,
    product,
    script_name AS app_name,
    strategy_key AS strategy_parm,
    date(entry_time) AS trade_date,
    count(*) AS total_trades,
    sum(display_net_return) AS total_net,
    sum(
        CASE
            WHEN direction::text = 'LONG'::text THEN 1
            ELSE 0
        END) AS buy_count,
    sum(
        CASE
            WHEN direction::text = 'LONG'::text THEN display_net_return
            ELSE 0::numeric
        END) AS buy_net,
    sum(
        CASE
            WHEN direction::text = 'SHORT'::text THEN 1
            ELSE 0
        END) AS sell_count,
    sum(
        CASE
            WHEN direction::text = 'SHORT'::text THEN display_net_return
            ELSE 0::numeric
        END) AS sell_net,
    sum(
        CASE
            WHEN direction::text = 'LONG'::text AND order_sent_net = true THEN display_net_return
            ELSE 0::numeric
        END) AS live_buy_net,
    sum(
        CASE
            WHEN direction::text = 'SHORT'::text AND order_sent_net = true THEN display_net_return
            ELSE 0::numeric
        END) AS live_sell_net,
    COALESCE(sum(
        CASE
            WHEN direction::text = 'LONG'::text AND display_net_return > 0::numeric THEN 1
            ELSE 0
        END)::numeric * 100.0 / NULLIF(sum(
        CASE
            WHEN direction::text = 'LONG'::text THEN 1
            ELSE 0
        END), 0)::numeric, 0::numeric) AS buy_percent,
    COALESCE(sum(
        CASE
            WHEN direction::text = 'SHORT'::text AND display_net_return > 0::numeric THEN 1
            ELSE 0
        END)::numeric * 100.0 / NULLIF(sum(
        CASE
            WHEN direction::text = 'SHORT'::text THEN 1
            ELSE 0
        END), 0)::numeric, 0::numeric) AS sell_percent,
    sum(
        CASE
            WHEN order_sent_net = true OR order_sent_alt = true THEN 1
            ELSE 0
        END) AS live_order_count
   FROM vw_trades_all
  GROUP BY run_mode, product, script_name, strategy_key, (date(entry_time));
