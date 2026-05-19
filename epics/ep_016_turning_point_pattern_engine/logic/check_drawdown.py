import json
from pathlib import Path
from backtest_gbp_analyzer import GBPBacktester

def analyze_drawdown(symbol, dates, params, label):
    cumulative_net = 0.0
    min_ever = 0.0
    trade_num = 0
    print(f"\n--- {label} (Bucket: {params['bucket_minutes']}m) ---")
    
    for date_str in dates:
        data_path = f"X:\\eds\\TradeApps\\breakout\\fs\\json\\live\\forex\\{date_str}\\_price_capture.jsonl"
        bt = GBPBacktester(data_path, symbol, params)
        if bt.load_data():
            # To get raw trades, we need to run the logic manually or use the return.
            # My 'replace' for run_simulation didn't return the raw trades in the summary dict.
            # I will modify the class temporarily in memory here or just look at the pips logic.
            # I'll re-run with a trick to get the trades.
            
            # Re-implementing the core loop briefly to capture trade results
            trades = []
            active_trade = None
            pending_trade = None
            current_bucket_key = None
            state = "FLAT"
            prior_open = None
            pip_mult = bt.pip_multiplier
            cost = bt.cost
            
            for snap in bt.all_snapshots:
                dt = snap["dt"]
                bucket_mins = params["bucket_minutes"]
                m_start = (dt.minute // bucket_mins) * bucket_mins
                bucket_key = dt.replace(minute=m_start, second=0, microsecond=0).strftime("%H:%M")
                if bucket_key != current_bucket_key:
                    bid_net, ask_net, current_open = bt.get_bucket_metrics(dt)
                    if current_open is not None:
                        open_move = "flat"
                        if prior_open:
                            if current_open > prior_open: open_move = "higher"
                            elif current_open < prior_open: open_move = "lower"
                        new_state = "FLAT"
                        if bid_net is not None:
                            if bid_net > 0 and ask_net > 0:
                                if bid_net >= params["conf_high"] and ask_net >= params["conf_high"]: new_state = "LONG_HIGH"
                                elif bid_net >= params["conf_med"] and ask_net >= params["conf_med"]: new_state = "LONG_MED"
                                elif bid_net >= params["conf_low"] and ask_net >= params["conf_low"]: new_state = "LONG_LOW"
                            elif bid_net < 0 and ask_net < 0:
                                if bid_net <= -params["conf_high"] and ask_net <= -params["conf_high"]: new_state = "SHORT_HIGH"
                                elif bid_net <= -params["conf_med"] and ask_net <= -params["conf_med"]: new_state = "SHORT_MED"
                                elif bid_net <= -params["conf_low"] and ask_net <= -params["conf_low"]: new_state = "SHORT_LOW"
                            if open_move == "higher" and bid_net < 0 and ask_net < 0: new_state = "EXIT_LONG"
                            elif open_move == "lower" and bid_net > 0 and ask_net > 0: new_state = "EXIT_SHORT"
                        state = new_state
                        prior_open = current_open
                    current_bucket_key = bucket_key
                raw_bid = snap[symbol]["bid"]
                raw_ask = snap[symbol]["ask"]
                if pending_trade:
                    if pending_trade["direction"] == "long":
                        if not state.startswith("LONG_"): pending_trade = None
                        elif raw_ask <= pending_trade["target_price"]:
                            active_trade = {"direction": "long", "entry_price": pending_trade["target_price"], "entry_dt": dt}
                            pending_trade = None
                    else: 
                        if not state.startswith("SHORT_"): pending_trade = None
                        elif raw_bid >= pending_trade["target_price"]:
                            active_trade = {"direction": "short", "entry_price": pending_trade["target_price"], "entry_dt": dt}
                            pending_trade = None
                if active_trade:
                    should_close = False
                    if active_trade["direction"] == "long":
                        current_pnl = (raw_bid - active_trade["entry_price"]) * pip_mult
                        if state.startswith("SHORT_") or state == "EXIT_LONG": should_close = True
                    else:
                        current_pnl = (active_trade["entry_price"] - raw_ask) * pip_mult
                        if state.startswith("LONG_") or state == "EXIT_SHORT": should_close = True
                    if not should_close:
                        if params["fixed_tp"] and current_pnl >= params["fixed_tp"]: should_close = True
                        elif params["fixed_sl"] and current_pnl <= -params["fixed_sl"]: should_close = True
                    if should_close:
                        exit_price = raw_bid if active_trade["direction"] == "long" else raw_ask
                        pips = (exit_price - active_trade["entry_price"]) * pip_mult if active_trade["direction"] == "long" else (active_trade["entry_price"] - exit_price) * pip_mult
                        pips_with_cost = round(pips + cost, 2)
                        cumulative_net += pips_with_cost
                        trade_num += 1
                        if cumulative_net < min_ever: min_ever = cumulative_net
                        # print(f"Trade {trade_num:02} ({date_str}): {pips_with_cost:>6} | Cum: {cumulative_net:>7.2f}")
                        active_trade = None
                if not active_trade and not pending_trade:
                    if state.startswith("LONG_") and "EXIT" not in state:
                        target_price = raw_ask + (params["price_offset"] / pip_mult)
                        if params["price_offset"] >= 0: active_trade = {"direction": "long", "entry_price": target_price, "entry_dt": dt}
                        else: pending_trade = {"direction": "long", "target_price": target_price, "dt": dt}
                    elif state.startswith("SHORT_") and "EXIT" not in state:
                        target_price = raw_bid - (params["price_offset"] / pip_mult)
                        if params["price_offset"] >= 0: active_trade = {"direction": "short", "entry_price": target_price, "entry_dt": dt}
                        else: pending_trade = {"direction": "short", "target_price": target_price, "dt": dt}

    print(f"Final Net: {cumulative_net:.2f}")
    print(f"Max Drawdown (Below Zero): {min_ever:.2f}")

dates = ["2026-05-13", "2026-05-14", "2026-05-15"]
symbol = "GBP"

# 30m Version
p30 = {"conf_high": 53, "conf_med": 20, "conf_low": 7, "bucket_minutes": 30, "price_offset": -0.35, "fixed_tp": 10.0, "fixed_sl": 20.0}
analyze_drawdown(symbol, dates, p30, "V6 Universal")

# 15m Version
p15 = {"conf_high": 53, "conf_med": 20, "conf_low": 7, "bucket_minutes": 15, "price_offset": -0.35, "fixed_tp": 10.0, "fixed_sl": 20.0}
analyze_drawdown(symbol, dates, p15, "V6 Fast (15m)")
