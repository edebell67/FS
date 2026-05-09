import os
import json
import time
import requests
from datetime import datetime, timezone, timedelta
from pathlib import Path
import threading

BASE_PATH = Path(r"C:\Users\edebe\eds\TradeApps\breakout\fs\json")

def get_trades_from_api(mode, date_str):
    try:
        url = f"http://127.0.0.1:5000/api/trades?mode={mode}&date={date_str}"
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            return resp.json().get("trades", [])
    except Exception as e:
        print(f"[MarketUpdate] API fetch failed: {e}")
    return []

def safe_float(v):
    try:
        return float(v or 0)
    except:
        return 0.0

def parse_trade_timestamp(ts_str):
    if not ts_str:
        return 0
    try:
        dt = datetime.fromisoformat(ts_str.replace('Z', '+00:00'))
        return dt.timestamp() * 1000
    except:
        return 0

def get_product_from_app(app_name):
    parts = app_name.split("_")
    for part in reversed(parts):
        if len(part) in (3, 6): # E.g., EURUSD
            return part.upper()
    return "UNKNOWN"

def get_latest_date(mode="live"):
    try:
        url = f"http://127.0.0.1:5000/api/dates?mode={mode}"
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            dates = resp.json().get("dates", [])
            if dates:
                return dates[0]
    except Exception as e:
        print(f"[MarketUpdate] API fetch failed for dates: {e}")
    return datetime.now().strftime('%Y-%m-%d')

def compute_metrics(trades):
    now_ms = time.time() * 1000
    if trades and len(trades) > 0:
        # Use latest trade time instead of actual time if it's lagging (e.g., sim or historical playback)
        latest_trade_ms = max([parse_trade_timestamp(t.get("exit_time", t.get("entry_time"))) for t in trades])
        if latest_trade_ms > 0 and now_ms - latest_trade_ms > 24 * 3600 * 1000:
            now_ms = latest_trade_ms + 1000  # Shift "now" to slightly after the last known trade

    totals = {"buy_net": 0.0, "sell_net": 0.0, "imbalance": 0.0}
    last_30m = {"buy_net": 0.0, "sell_net": 0.0}
    prev_30m = {"buy_net": 0.0, "sell_net": 0.0}
    
    open_count = 0
    open_net = 0.0
    
    products = {}
    factions = {}
    
    for t in trades:
        net = safe_float(t.get("net_return", 0.0))
        direction = str(t.get("direction", "LONG")).upper()
        is_buy = "LONG" in direction or "BUY" in direction
        status = str(t.get("status", "")).upper()
        
        product = str(t.get("product", "")).upper()
        if not product:
            product = get_product_from_app(t.get("app_name", ""))
            
        app = str(t.get("app_name", t.get("script_name", "UNKNOWN")))
        faction = "BREAKOUT"
        if "breakout_r_rev" in app.lower(): faction = "BREAKOUT_R_REV"
        elif "breakout_rev" in app.lower(): faction = "BREAKOUT_REV"
        elif "breakout_r" in app.lower(): faction = "BREAKOUT_R"
        
        if status == "OPEN":
            open_count += 1
            open_net += net
        else:
            # Add to totals
            if is_buy:
                totals["buy_net"] += net
            else:
                totals["sell_net"] += net
                
            # Product/Faction tracking
            if product not in products:
                products[product] = 0.0
            products[product] += net
            
            if faction not in factions:
                factions[faction] = 0.0
            factions[faction] += net
                
            # Time blocks
            exit_time_str = t.get("exit_time")
            if exit_time_str:
                try:
                    exit_ms = parse_trade_timestamp(exit_time_str)
                    diff_ms = now_ms - exit_ms
                    
                    if diff_ms <= 30 * 60 * 1000 and diff_ms >= 0:
                        if is_buy: last_30m["buy_net"] += net
                        else: last_30m["sell_net"] += net
                    elif diff_ms <= 60 * 60 * 1000 and diff_ms >= 0:
                        if is_buy: prev_30m["buy_net"] += net
                        else: prev_30m["sell_net"] += net
                except:
                    pass

    totals["imbalance"] = totals["buy_net"] + totals["sell_net"]
    
    # Sort products and factions
    sorted_prods = sorted(products.items(), key=lambda x: x[1], reverse=True)
    top_prod = sorted_prods[0] if sorted_prods else ("NONE", 0.0)
    weak_prod = sorted_prods[-1] if sorted_prods else ("NONE", 0.0)
    
    sorted_factions = sorted(factions.items(), key=lambda x: x[1], reverse=True)
    top_faction = sorted_factions[0] if sorted_factions else ("NONE", 0.0)
    
    return {
        "totals": totals,
        "last_30m": last_30m,
        "prev_30m": prev_30m,
        "open_count": open_count,
        "open_net": open_net,
        "top_product": top_prod,
        "weakest_product": weak_prod,
        "top_faction": top_faction
    }

def generate_market_update(mode="live", date_str=None):
    if not date_str:
        date_str = get_latest_date(mode)
        
    trades = get_trades_from_api(mode, date_str)
    if not trades:
        print("[MarketUpdate] No trades returned, skipping generation.")
        return
        
    metrics = compute_metrics(trades)
    
    # Determine Winner / Bias
    totals = metrics["totals"]
    buy_tot = totals["buy_net"]
    sell_tot = totals["sell_net"]
    
    current_bias = "BUY" if buy_tot > sell_tot else "SELL"
    if abs(buy_tot - sell_tot) < 50:
        current_bias = "NEUTRAL"
        
    last30_buy = metrics["last_30m"]["buy_net"]
    last30_sell = metrics["last_30m"]["sell_net"]
    
    # Narrative Logic (Boxing Style)
    now_str = datetime.now().strftime("%H:%M:%S")
    headline = f"LIVE Battle Pulse | Bias {current_bias} | {now_str}"
    
    beats = []
    beats.append(f"1. Bell: BUY ${buy_tot:.2f} vs SELL ${sell_tot:.2f}.")
    
    # Momentum beat
    if last30_buy > last30_sell and current_bias == "BUY":
        beats.append(f"2. BUY presses. Imbalance ${totals['imbalance']:.2f}.")
    elif last30_sell > last30_buy and current_bias == "SELL":
        beats.append(f"2. SELL drives hard. Imbalance ${totals['imbalance']:.2f}.")
    elif last30_buy > last30_sell:
        beats.append(f"2. BUY fights back. Imbalance ${totals['imbalance']:.2f}.")
    else:
        beats.append(f"2. SELL counters. Imbalance ${totals['imbalance']:.2f}.")
        
    beats.append(f"3. 30m score: BUY ${last30_buy:.2f} | SELL ${last30_sell:.2f}.")
    
    top_faction, fac_val = metrics["top_faction"]
    beats.append(f"4. Faction lead: {top_faction} ${fac_val:.2f}.")
    
    # Likely winner
    likely_winner = "BUY" if last30_buy > last30_sell else "SELL"
    confidence = "HIGH" if abs(last30_buy - last30_sell) > 100 else "LOW"
    beats.append(f"5. Likely winner next round: {likely_winner} ({confidence}).")
    
    top_prod, tp_val = metrics["top_product"]
    weak_prod, wp_val = metrics["weakest_product"]
    beats.append(f"6. Product impact: {top_prod} +${tp_val:.2f}; weak {weak_prod} ${wp_val:.2f}.")
    
    forecast = f"{likely_winner} favored into next round ({confidence} confidence)."
    
    update_payload = {
        "headline": headline,
        "created_at": datetime.now().isoformat(),
        "bias": current_bias,
        "market_condition": "TRENDING" if confidence == "HIGH" else "CHOPPY",
        "totals": {
            "buy_net": buy_tot,
            "sell_net": sell_tot,
            "imbalance": totals["imbalance"]
        },
        "windows": {
            "last_30m": {"buy_net": last30_buy, "sell_net": last30_sell},
            "prev_30m": {"buy_net": metrics["prev_30m"]["buy_net"], "sell_net": metrics["prev_30m"]["sell_net"]}
        },
        "narrative": "\n".join(beats),
        "forecast": forecast
    }
    
    # Save the file
    out_dir = BASE_PATH / mode / date_str
    out_dir.mkdir(parents=True, exist_ok=True)
    
    out_file = out_dir / "_market_update.json"
    with open(out_file, "w") as f:
        json.dump(update_payload, f, indent=4)
        
    # Append to history
    hist_file = out_dir / "_market_update_history.json"
    history = []
    if hist_file.exists():
        try:
            with open(hist_file, "r") as f:
                history = json.load(f)
        except:
            pass
            
    history.append(update_payload)
    # Keep last 500
    if len(history) > 500:
        history = history[-500:]
        
    with open(hist_file, "w") as f:
        json.dump(history, f, indent=4)
        
    print(f"[MarketUpdate] Generated update. Bias: {current_bias}, Winner: {likely_winner}")

def run_loop():
    print("[MarketUpdate] Starting periodic update generator loop (every 5 mins)...")
    while True:
        try:
            generate_market_update("live")
        except Exception as e:
            print(f"[MarketUpdate] Loop Error: {e}")
        time.sleep(300)

if __name__ == "__main__":
    generate_market_update("live", "2026-02-23")
