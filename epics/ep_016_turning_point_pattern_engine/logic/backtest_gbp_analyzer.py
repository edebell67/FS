import json
import os
import sys
from datetime import datetime, timedelta
from collections import defaultdict
from pathlib import Path

# -----------------------------------
# Configuration Defaults
# -----------------------------------
GBP_SYMBOL = "GBPAUD_C"
BUCKET_MINUTES = 5

# -----------------------------------
# Core Logic Class
# -----------------------------------
class GBPBacktester:
    def __init__(self, data_path, symbol, params=None):
        self.data_path = Path(data_path)
        self.symbol = symbol.upper()
        self.pip_multiplier = 100 if "JPY" in self.symbol else 10000
        self.params = params or {
            "conf_high": 20, "conf_med": 10, "conf_low": 6, "mild_threshold": 5,
            "price_offset": 0.0, "fixed_tp": None, "fixed_sl": None,
            "bucket_minutes": 5, "round_turn_cost": -2.0, "accumulation": 1
        }
        self.cost = self.params.get("round_turn_cost", -2.0)
        self.bucket_minutes = self.params.get("bucket_minutes", 5)
        self.minute_data = defaultdict(list) 
        self.all_snapshots = []

    def load_data(self):
        last_valid_prices = {}
        max_pip_diff = 500 

        if not self.data_path.exists():
            return False

        with open(self.data_path, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    snap = json.loads(line)
                    if self.symbol in snap:
                        raw_bid = float(snap[self.symbol]["bid"])
                        raw_ask = float(snap[self.symbol]["ask"])
                        if raw_bid <= 0 or raw_ask <= 0: continue
                        
                        if self.symbol in last_valid_prices:
                            prev_bid = last_valid_prices[self.symbol]["bid"]
                            diff_pips = abs(raw_bid - prev_bid) * self.pip_multiplier
                            if diff_pips > max_pip_diff: continue
                        
                        last_valid_prices[self.symbol] = {"bid": raw_bid, "ask": raw_ask}
                        dt = datetime.fromisoformat(snap["ts"])
                        snap["dt"] = dt
                        self.all_snapshots.append(snap)
                        
                        min_key = dt.strftime("%Y-%m-%d %H:%M")
                        self.minute_data[min_key].append((raw_bid, raw_ask))
                except:
                    continue
        
        if not self.all_snapshots: return False
        self.all_snapshots.sort(key=lambda x: x["dt"])
        return True

    def get_bucket_metrics(self, bucket_history):
        if not bucket_history: return None, None, None
        
        # Open prices are the first seen in the bucket
        open_bid, open_ask = bucket_history[0]
        
        bid_above = 0
        bid_below = 0
        ask_above = 0
        ask_below = 0
        
        for b, a in bucket_history:
            if b > open_bid: bid_above += 1
            elif b < open_bid: bid_below += 1
            
            if a > open_ask: ask_above += 1
            elif a < open_ask: ask_below += 1
            
        bid_net = bid_above - bid_below
        ask_net = ask_above - ask_below
        
        return bid_net, ask_net, open_bid

    def run_simulation(self):
        trades = []
        active_trade = None
        pending_trade = None
        current_bucket_key = None
        bucket_history = [] # Stores (bid, ask) for the current bucket
        state = "FLAT"
        prior_open = None
        p = self.params
        
        prec = 2 if self.pip_multiplier == 100 else 4

        for snap in self.all_snapshots:
            dt = snap["dt"]
            bucket_mins = p["bucket_minutes"]
            m_start = (dt.minute // bucket_mins) * bucket_mins
            bucket_key = dt.replace(minute=m_start, second=0, microsecond=0).strftime("%H:%M")
            
            raw_bid = round(float(snap[self.symbol]["bid"]), prec)
            raw_ask = round(float(snap[self.symbol]["ask"]), prec)

            # SIGNAL LOCKING: Only re-evaluate at the start of a new bucket
            if bucket_key != current_bucket_key:
                # The signal for the NEXT bucket is based on the history of the bucket that just CLOSED
                if bucket_history:
                    # Metrics for the bucket that just finished
                    bid_net, ask_net, bucket_open = self.get_bucket_metrics(bucket_history)
                    
                    if bucket_open is not None:
                        open_move = "flat"
                        if prior_open:
                            if bucket_open > prior_open: open_move = "higher"
                            elif bucket_open < prior_open: open_move = "lower"
                        
                        new_state = "FLAT"
                        if bid_net is not None:
                            if bid_net > 0 and ask_net > 0:
                                if bid_net >= p["conf_high"] and ask_net >= p["conf_high"]: new_state = "LONG_HIGH"
                                elif bid_net >= p["conf_med"] and ask_net >= p["conf_med"]: new_state = "LONG_MED"
                                elif bid_net >= p["conf_low"] and ask_net >= p["conf_low"]: new_state = "LONG_LOW"
                            elif bid_net < 0 and ask_net < 0:
                                if bid_net <= -p["conf_high"] and ask_net <= -p["conf_high"]: new_state = "SHORT_HIGH"
                                elif bid_net <= -p["conf_med"] and ask_net <= -p["conf_med"]: new_state = "SHORT_MED"
                                elif bid_net <= -p["conf_low"] and ask_net <= -p["conf_low"]: new_state = "SHORT_LOW"

                            if open_move == "higher" and bid_net < 0 and ask_net < 0: new_state = "EXIT_LONG"
                            elif open_move == "lower" and bid_net > 0 and ask_net > 0: new_state = "EXIT_SHORT"
                        
                        state = new_state
                        prior_open = bucket_open # The open price for the bucket that just finished
                
                bucket_history = []
                current_bucket_key = bucket_key
            
            bucket_history.append((raw_bid, raw_ask))
            
            # (TP/SL remains high-frequency, but 'state' only changes at bucket boundaries)

            raw_bid = snap[self.symbol]["bid"]
            raw_ask = snap[self.symbol]["ask"]

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
                exit_reason = "signal"
                if active_trade["direction"] == "long":
                    current_pnl = (raw_bid - active_trade["entry_price"]) * self.pip_multiplier
                    if state.startswith("SHORT_") or state == "EXIT_LONG": should_close = True
                else:
                    current_pnl = (active_trade["entry_price"] - raw_ask) * self.pip_multiplier
                    if state.startswith("LONG_") or state == "EXIT_SHORT": should_close = True

                if not should_close:
                    if p["fixed_tp"] and current_pnl >= p["fixed_tp"]:
                        should_close = True
                        exit_reason = "tp"
                    elif p["fixed_sl"] and current_pnl <= -p["fixed_sl"]:
                        should_close = True
                        exit_reason = "sl"

                if should_close:
                    exit_price = raw_bid if active_trade["direction"] == "long" else raw_ask
                    pips = (exit_price - active_trade["entry_price"]) * self.pip_multiplier if active_trade["direction"] == "long" else (active_trade["entry_price"] - exit_price) * self.pip_multiplier
                    trades.append({
                        "entry_ts": active_trade["entry_dt"].isoformat(), "exit_ts": dt.isoformat(),
                        "direction": active_trade["direction"], "entry_price": active_trade["entry_price"],
                        "exit_price": exit_price, "exit_reason": exit_reason,
                        "pips": round(pips + self.cost, 2), "alt_pips": round(-pips + self.cost, 2)
                    })
                    active_trade = None

            if not active_trade and not pending_trade:
                if state.startswith("LONG_") and "EXIT" not in state:
                    target_price = raw_ask + (p["price_offset"] / self.pip_multiplier)
                    if p["price_offset"] >= 0:
                        active_trade = {"direction": "long", "entry_price": target_price, "entry_dt": dt}
                    else:
                        pending_trade = {"direction": "long", "target_price": target_price, "dt": dt}
                elif state.startswith("SHORT_") and "EXIT" not in state:
                    target_price = raw_bid - (p["price_offset"] / self.pip_multiplier)
                    if p["price_offset"] >= 0:
                        active_trade = {"direction": "short", "entry_price": target_price, "entry_dt": dt}
                    else:
                        pending_trade = {"direction": "short", "target_price": target_price, "dt": dt}

        total_net = sum(t["pips"] for t in trades)
        duration_hours = (self.all_snapshots[-1]["dt"] - self.all_snapshots[0]["dt"]).total_seconds() / 3600
        return {
            "total_net": round(total_net, 2), "trade_count": len(trades),
            "pips_per_hour": round(total_net / duration_hours, 2) if duration_hours > 0 else 0,
            "duration_hours": round(duration_hours, 2), "params": self.params, "symbol": self.symbol,
            "trades": trades
        }

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", required=True)
    parser.add_argument("--symbol", default="GBPAUD_C")
    parser.add_argument("--conf_high", type=int, default=20)
    parser.add_argument("--conf_med", type=int, default=10)
    parser.add_argument("--conf_low", type=int, default=6)
    parser.add_argument("--price_offset", type=float, default=0.0)
    parser.add_argument("--fixed_tp", type=float, default=None)
    parser.add_argument("--fixed_sl", type=float, default=None)
    parser.add_argument("--bucket_minutes", type=int, default=5)
    parser.add_argument("--round_turn_cost", type=float, default=-2.0)
    args = parser.parse_args()
    
    params = {
        "conf_high": args.conf_high, "conf_med": args.conf_med, "conf_low": args.conf_low,
        "mild_threshold": 5, "price_offset": args.price_offset, "fixed_tp": args.fixed_tp,
        "fixed_sl": args.fixed_sl, "bucket_minutes": args.bucket_minutes,
        "round_turn_cost": args.round_turn_cost, "accumulation": 1
    }
    
    bt = GBPBacktester(args.data, args.symbol, params)
    if bt.load_data():
        results = bt.run_simulation()
        print(json.dumps(results, indent=2))
    else:
        print(f"Failed to load data for {args.symbol}")
