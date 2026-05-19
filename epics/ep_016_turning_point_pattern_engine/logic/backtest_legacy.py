import json
import os
import sys
from datetime import datetime, timedelta
from collections import defaultdict
from pathlib import Path

class LegacyBacktester:
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
        self.price_data = defaultdict(lambda: {"bid": defaultdict(lambda: defaultdict(int)), "ask": defaultdict(lambda: defaultdict(int))})
        self.first_prices = defaultdict(lambda: {"bid": {}, "ask": {}})
        self.bucket_times = []
        self.all_snapshots = []

    def load_data(self):
        last_valid_prices = {}
        max_pip_diff = 500 
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
                        snap["dt"] = datetime.fromisoformat(snap["ts"])
                        self.all_snapshots.append(snap)
                except: continue
        if not self.all_snapshots: return False
        self.all_snapshots.sort(key=lambda x: x["dt"])
        for snap in self.all_snapshots:
            dt = snap["dt"]
            minute = (dt.minute // self.bucket_minutes) * self.bucket_minutes
            bucket_time = dt.replace(minute=minute, second=0, microsecond=0).strftime("%H:%M")
            if bucket_time not in self.bucket_times: self.bucket_times.append(bucket_time)
            for side in ["bid", "ask"]:
                price = snap[self.symbol][side]
                price_pip = round(float(price), 2 if self.pip_multiplier == 100 else 4)
                if bucket_time not in self.first_prices[self.symbol][side]:
                    self.first_prices[self.symbol][side][bucket_time] = price_pip
                self.price_data[self.symbol][side][price_pip][bucket_time] += 1
        self.bucket_times = sorted(self.bucket_times)
        return True

    def compute_metrics(self, side, bucket_time):
        open_price = self.first_prices[self.symbol][side].get(bucket_time)
        metrics = {"open": open_price, "above": 0, "at_open": 0, "below": 0, "net": 0}
        if open_price is None: return metrics
        for price, bucket_counts in self.price_data[self.symbol][side].items():
            count = bucket_counts.get(bucket_time, 0)
            if count <= 0: continue
            if price > open_price: metrics["above"] += count
            elif price == open_price: metrics["at_open"] += count
            else: metrics["below"] += count
        metrics["net"] = metrics["above"] - metrics["below"]
        return metrics

    def classify(self, bid_m, ask_m, current_open, prior_open):
        bid_net = bid_m["net"]
        ask_net = ask_m["net"]
        open_move = None
        if current_open and prior_open:
            if current_open > prior_open: open_move = "higher"
            elif current_open < prior_open: open_move = "lower"
            else: open_move = "flat"
        state = "FLAT"
        p = self.params
        if bid_net > 0 and ask_net > 0:
            if bid_net >= p["conf_high"] and ask_net >= p["conf_high"]: state = "LONG_HIGH"
            elif bid_net >= p["conf_med"] and ask_net >= p["conf_med"]: state = "LONG_MED"
            elif bid_net >= p["conf_low"] and ask_net >= p["conf_low"]: state = "LONG_LOW"
        elif bid_net < 0 and ask_net < 0:
            if bid_net <= -p["conf_high"] and ask_net <= -p["conf_high"]: state = "SHORT_HIGH"
            elif bid_net <= -p["conf_med"] and ask_net <= -p["conf_med"]: state = "SHORT_MED"
            elif bid_net <= -p["conf_low"] and ask_net <= -p["conf_low"]: state = "SHORT_LOW"
        if open_move == "higher" and bid_net < 0 and ask_net < 0: state = "EXIT_LONG"
        elif open_move == "lower" and bid_net > 0 and ask_net > 0: state = "EXIT_SHORT"
        return state

    def run_simulation(self):
        trades = []
        active_trade = None
        pending_trade = None
        current_bucket = None
        for snap in self.all_snapshots:
            dt = snap["dt"]
            minute = (dt.minute // self.bucket_minutes) * self.bucket_minutes
            bucket = dt.replace(minute=minute, second=0, microsecond=0).strftime("%H:%M")
            if bucket != current_bucket:
                current_bucket = bucket
                bid_m = self.compute_metrics("bid", bucket)
                ask_m = self.compute_metrics("ask", bucket)
                try:
                    idx = self.bucket_times.index(bucket)
                    prior_open = self.first_prices[self.symbol]["bid"].get(self.bucket_times[idx-1]) if idx > 0 else None
                except ValueError: prior_open = None
                state = self.classify(bid_m, ask_m, bid_m["open"], prior_open)
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
                    if self.params["fixed_tp"] and current_pnl >= self.params["fixed_tp"]:
                        should_close = True; exit_reason = "tp"
                    elif self.params["fixed_sl"] and current_pnl <= -self.params["fixed_sl"]:
                        should_close = True; exit_reason = "sl"
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
                    target_price = raw_ask + (self.params["price_offset"] / self.pip_multiplier)
                    if self.params["price_offset"] >= 0:
                        active_trade = {"direction": "long", "entry_price": target_price, "entry_dt": dt}
                    else:
                        pending_trade = {"direction": "long", "target_price": target_price, "dt": dt}
                elif state.startswith("SHORT_") and "EXIT" not in state:
                    target_price = raw_bid - (self.params["price_offset"] / self.pip_multiplier)
                    if self.params["price_offset"] >= 0:
                        active_trade = {"direction": "short", "entry_price": target_price, "entry_dt": dt}
                    else:
                        pending_trade = {"direction": "short", "target_price": target_price, "dt": dt}
        total_net = sum(t["pips"] for t in trades)
        duration_hours = (self.all_snapshots[-1]["dt"] - self.all_snapshots[0]["dt"]).total_seconds() / 3600
        return {
            "total_net": round(total_net, 2), "trade_count": len(trades),
            "pips_per_hour": round(total_net / duration_hours, 2) if duration_hours > 0 else 0,
            "duration_hours": round(duration_hours, 2), "params": self.params, "symbol": self.symbol
        }
