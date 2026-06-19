import json
import os
import sys
from datetime import datetime, timedelta
from collections import defaultdict
from pathlib import Path

# -----------------------------------
# Configuration Defaults
# -----------------------------------
MILD_THRESHOLD = 5

class GBPBacktester:
    def __init__(self, data_path, symbol, params):
        self.data_path = Path(data_path)
        self.symbol = symbol.upper()
        self.params = params
        self.minute_data = defaultdict(list) 
        self.all_snapshots = []
        self.pip_multiplier = 100 if "JPY" in self.symbol else 10000
        self.cost = params.get("round_turn_cost", -2.0)

    def load_data(self):
        if not self.data_path.exists(): return False
        with open(self.data_path, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    snap = json.loads(line)
                    if self.symbol in snap:
                        ts_str = snap["ts"]
                        try: dt = datetime.fromisoformat(ts_str).replace(tzinfo=None)
                        except: dt = datetime.strptime(ts_str, "%Y-%m-%d %H:%M:%S.%f")
                        bid = float(snap[self.symbol]["bid"])
                        ask = float(snap[self.symbol]["ask"])
                        if bid > 0 and ask > 0:
                            self.all_snapshots.append({"dt": dt, "bid": bid, "ask": ask})
                except: continue
        return len(self.all_snapshots) > 0

    def get_bucket_metrics(self, bucket_history):
        if not bucket_history: return None, None, None
        open_bid, open_ask = bucket_history[0]
        bid_above = sum(1 for b, a in bucket_history if b > open_bid)
        bid_below = sum(1 for b, a in bucket_history if b < open_bid)
        ask_above = sum(1 for b, a in bucket_history if a > open_ask)
        ask_below = sum(1 for b, a in bucket_history if a < open_ask)
        return bid_above - bid_below, ask_above - ask_below, (open_bid + open_ask) / 2

    def run_simulation(self):
        trades = []
        active_trade = None
        pending_trade = None
        current_bucket_key = None
        bucket_history = [] 
        state = "FLAT"
        prior_open = None
        p = self.params
        mult = self.pip_multiplier
        prec = 2 if mult == 100 else 4

        for snap in self.all_snapshots:
            dt = snap["dt"]
            bucket_mins = p["bucket_minutes"]
            m_start = (dt.minute // bucket_mins) * bucket_mins
            bucket_key = dt.replace(minute=m_start, second=0, microsecond=0).strftime("%H:%M")
            
            raw_bid = round(snap["bid"], prec)
            raw_ask = round(snap["ask"], prec)

            # Signal Locking
            if bucket_key != current_bucket_key:
                if bucket_history:
                    bid_net, ask_net, bucket_open = self.get_bucket_metrics(bucket_history)
                    if bucket_open is not None:
                        open_move = "flat"
                        if prior_open:
                            if bucket_open > prior_open: open_move = "higher"
                            elif bucket_open < prior_open: open_move = "lower"
                        new_state = "FLAT"
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
                        prior_open = bucket_open
                bucket_history = []
                current_bucket_key = bucket_key
            
            bucket_history.append((raw_bid, raw_ask))

            # Entry Logic
            if pending_trade:
                off = p["price_offset"]
                is_hit = False
                if pending_trade["direction"] == "long":
                    if not state.startswith("LONG_"): pending_trade = None
                    elif (off >= 0 and raw_ask >= pending_trade["target_p"]) or (off < 0 and raw_ask <= pending_trade["target_p"]):
                        is_hit = True; fill_p = raw_ask
                else:
                    if not state.startswith("SHORT_"): pending_trade = None
                    elif (off >= 0 and raw_bid <= pending_trade["target_p"]) or (off < 0 and raw_bid >= pending_trade["target_p"]):
                        is_hit = True; fill_p = raw_bid
                if is_hit:
                    active_trade = {"dir": pending_trade["direction"], "entry_p": fill_p, "dt": dt, "state": pending_trade["state"]}
                    pending_trade = None

            if not active_trade and not pending_trade:
                if state.startswith("LONG_") and "EXIT" not in state:
                    pending_trade = {"direction": "long", "target_p": raw_ask + (p["price_offset"] / mult), "state": state}
                elif state.startswith("SHORT_") and "EXIT" not in state:
                    pending_trade = {"direction": "short", "target_p": raw_bid - (p["price_offset"] / mult), "state": state}

            # Exit Logic
            if active_trade:
                should_close = False
                exit_reason = "signal"
                if active_trade["dir"] == "long":
                    pnl = (raw_bid - active_trade["entry_p"]) * mult
                    exit_p = raw_bid
                    if state.startswith("SHORT_") or state == "EXIT_LONG": should_close = True
                else:
                    pnl = (active_trade["entry_p"] - raw_ask) * mult
                    exit_p = raw_ask
                    if state.startswith("LONG_") or state == "EXIT_SHORT": should_close = True

                if not should_close:
                    if p["fixed_tp"] and pnl >= p["fixed_tp"]: should_close = True; exit_reason = "tp"
                    elif p["fixed_sl"] and pnl <= -p["fixed_sl"]: should_close = True; exit_reason = "sl"

                if should_close:
                    trades.append({
                        "entry_ts": active_trade["dt"].isoformat(), "exit_ts": dt.isoformat(),
                        "direction": active_trade["dir"], "state": active_trade["state"],
                        "entry_price": active_trade["entry_p"], "exit_price": exit_p,
                        "exit_reason": exit_reason, "pips": round(pnl + self.cost, 2),
                        "alt_pips": round(-pnl + self.cost, 2)
                    })
                    active_trade = None

        total_net = sum(t["pips"] for t in trades)
        duration_hours = (self.all_snapshots[-1]["dt"] - self.all_snapshots[0]["dt"]).total_seconds() / 3600
        return {"total_net": round(total_net, 2), "trade_count": len(trades), "duration_hours": round(duration_hours, 2), "trades": trades}

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", required=True)
    parser.add_argument("--symbol", default="GBP")
    parser.add_argument("--conf_high", type=int, default=20)
    parser.add_argument("--conf_med", type=int, default=10)
    parser.add_argument("--conf_low", type=int, default=6)
    parser.add_argument("--price_offset", type=float, default=0.0)
    parser.add_argument("--fixed_tp", type=float, default=None)
    parser.add_argument("--fixed_sl", type=float, default=None)
    parser.add_argument("--bucket_minutes", type=int, default=5)
    parser.add_argument("--round_turn_cost", type=float, default=-2.0)
    args = parser.parse_args()
    bt = GBPBacktester(args.data, args.symbol, vars(args))
    if bt.load_data(): print(json.dumps(bt.run_simulation(), indent=2))
