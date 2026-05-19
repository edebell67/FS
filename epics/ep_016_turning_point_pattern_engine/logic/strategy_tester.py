"""
Strategy Tester - Test different net pressure thresholds on replay or live data.
"""
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from urllib.request import urlopen

# ---------------------------------------------------
# Configuration
# ---------------------------------------------------
COST_PIPS = 3
HTTP_SOURCE_URL = "http://127.0.0.1:8002/api/vw_000_fx_quotes"

BREAKOUT_CONFIG_PATH = Path(__file__).resolve().parents[3] / "TradeApps" / "breakout" / "fs" / "config.json"
try:
    with open(BREAKOUT_CONFIG_PATH, "r", encoding="utf-8") as f:
        _config = json.load(f)
        GENERATED_DATA_ROOT = Path(_config.get("path_settings", {}).get("generated_data_root", "X:\\eds"))
except (FileNotFoundError, json.JSONDecodeError):
    GENERATED_DATA_ROOT = Path("X:\\eds")


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def get_snapshot_dir(date_str=None):
    if date_str is None:
        date_str = datetime.now().strftime("%Y-%m-%d")
    return GENERATED_DATA_ROOT / "TradeApps" / "breakout" / "fs" / "json" / "live" / "forex" / date_str


def load_replay_data(date_str=None):
    """Load snapshots from _price_capture.jsonl"""
    snapshot_file = get_snapshot_dir(date_str) / "_price_capture.jsonl"
    if not snapshot_file.exists():
        return []
    snapshots = []
    with open(snapshot_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                snapshots.append(json.loads(line))
    return snapshots


def fetch_live_quote(symbol):
    """Fetch live quote for symbol"""
    try:
        with urlopen(HTTP_SOURCE_URL, timeout=5) as response:
            payload = json.load(response)
        for quote in payload.get("data", []):
            if (quote.get("code") or "").upper() == symbol.upper():
                return {
                    "bid": float(quote.get("bid", 0)),
                    "ask": float(quote.get("ask", 0)),
                    "ts": quote.get("timestamp", "")
                }
    except Exception:
        pass
    return None


def pip_value(symbol):
    """Return pip multiplier for symbol"""
    return 100 if "JPY" in symbol.upper() else 10000


def compute_net_pressure(prices, open_price):
    """
    Compute net pressure from price history.
    prices = list of {"bid": x, "ask": y}
    Returns (bid_net, ask_net)
    """
    bid_above = bid_below = ask_above = ask_below = 0
    for p in prices:
        if p["bid"] > open_price:
            bid_above += 1
        elif p["bid"] < open_price:
            bid_below += 1
        if p["ask"] > open_price:
            ask_above += 1
        elif p["ask"] < open_price:
            ask_below += 1
    return (bid_above - bid_below, ask_above - ask_below)


class StrategyTester:
    def __init__(self, symbol, threshold=0, flip=False, take_profit=None):
        self.symbol = symbol.upper()
        self.threshold = threshold
        self.flip = flip
        self.take_profit = take_profit  # pips
        self.trades = []
        self.position = None  # {"side": "BUY"/"SELL", "entry_price": x, "entry_ts": "..."}
        self.prices = []  # rolling window
        self.open_price = None
        self.bucket_start = None

    def reset(self):
        self.trades = []
        self.position = None
        self.prices = []
        self.open_price = None
        self.bucket_start = None

    def get_bucket(self, ts_str):
        """Get 5-min bucket from timestamp"""
        try:
            dt = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
            minute = (dt.minute // 5) * 5
            return dt.strftime(f"%H:{minute:02d}")
        except:
            return None

    def process_tick(self, ts, bid, ask):
        """Process a single price tick"""
        bucket = self.get_bucket(ts)

        # New bucket - reset
        if bucket != self.bucket_start:
            self.bucket_start = bucket
            self.open_price = bid
            self.prices = []

        self.prices.append({"bid": bid, "ask": ask})

        if self.open_price is None:
            return None

        bid_net, ask_net = compute_net_pressure(self.prices, self.open_price)

        # Determine signal
        signal = None
        if bid_net > self.threshold and ask_net > self.threshold:
            signal = "SELL" if self.flip else "BUY"
        elif bid_net < -self.threshold and ask_net < -self.threshold:
            signal = "BUY" if self.flip else "SELL"

        # Execute trades
        trade_result = None
        if signal and self.position is None:
            # Open position
            entry_price = ask if signal == "BUY" else bid
            self.position = {"side": signal, "entry_price": entry_price, "entry_ts": ts}
        elif self.position:
            # Check for exit: take profit or opposite signal
            exit_price = bid if self.position["side"] == "BUY" else ask
            multiplier = pip_value(self.symbol)
            if self.position["side"] == "BUY":
                current_pips = (exit_price - self.position["entry_price"]) * multiplier
            else:
                current_pips = (self.position["entry_price"] - exit_price) * multiplier

            should_exit = False
            exit_reason = None

            # Take profit check
            if self.take_profit and current_pips >= self.take_profit:
                should_exit = True
                exit_reason = "TP"

            # Opposite signal check
            if signal and signal != self.position["side"]:
                should_exit = True
                exit_reason = "SIGNAL"

            if should_exit:
                gross_pips = current_pips
                net_pips = gross_pips - COST_PIPS

                trade_result = {
                    "side": self.position["side"],
                    "entry": self.position["entry_price"],
                    "exit": exit_price,
                    "gross_pips": round(gross_pips, 1),
                    "net_pips": round(net_pips, 1),
                    "entry_ts": self.position["entry_ts"],
                    "exit_ts": ts,
                    "exit_reason": exit_reason
                }
                self.trades.append(trade_result)
                self.position = None

        return {
            "ts": ts,
            "bid": bid,
            "ask": ask,
            "bid_net": bid_net,
            "ask_net": ask_net,
            "signal": signal,
            "position": self.position,
            "trade": trade_result
        }

    def summary(self):
        """Return P&L summary"""
        if not self.trades:
            return {"total_trades": 0, "total_pips": 0, "wins": 0, "losses": 0, "win_rate": 0}
        total_pips = sum(t["net_pips"] for t in self.trades)
        wins = sum(1 for t in self.trades if t["net_pips"] > 0)
        losses = sum(1 for t in self.trades if t["net_pips"] <= 0)
        return {
            "total_trades": len(self.trades),
            "total_pips": round(total_pips, 1),
            "wins": wins,
            "losses": losses,
            "win_rate": round(wins / len(self.trades) * 100, 1)
        }


def run_replay_test(symbol, date_str=None, thresholds=list(range(1, 31)), include_flip=True, take_profit=7):
    """Run backtest on replay data with multiple thresholds"""
    snapshots = load_replay_data(date_str)
    if not snapshots:
        print(f"No replay data found for {date_str or 'today'}")
        return None, None

    results = {}
    max_bid_net = 0
    max_ask_net = 0

    for threshold in thresholds:
        for flip in ([False, True] if include_flip else [False]):
            label = f">{threshold}" + (" FLIP" if flip else "")
            tester = StrategyTester(symbol, threshold=threshold, flip=flip, take_profit=take_profit)

            for snap in snapshots:
                ts = snap.get("ts", "")
                product_data = snap.get(symbol, {})
                if product_data:
                    result = tester.process_tick(ts, product_data["bid"], product_data["ask"])
                    if result:
                        max_bid_net = max(max_bid_net, abs(result["bid_net"]))
                        max_ask_net = max(max_ask_net, abs(result["ask_net"]))

            results[label] = tester.summary()
            results[label]["trades"] = tester.trades

    debug_info = {"snapshots": len(snapshots), "max_bid_net": max_bid_net, "max_ask_net": max_ask_net}
    return results, debug_info


def display_results(symbol, results, debug_info=None, take_profit=None):
    """Display test results"""
    clear_screen()
    print(f"{'='*60}")
    print(f" STRATEGY TESTER: {symbol}")
    print(f" Cost: {COST_PIPS} pips | Take Profit: {take_profit or 'None'} pips")
    if debug_info:
        print(f" Snapshots: {debug_info.get('snapshots', 0)} | Max bid_net: {debug_info.get('max_bid_net', 0)} | Max ask_net: {debug_info.get('max_ask_net', 0)}")
    print(f"{'='*60}\n")

    print(f"{'Threshold':<15} {'Trades':<8} {'Wins':<6} {'Losses':<8} {'Win%':<8} {'Net Pips':<10}")
    print("-" * 60)

    for label, data in results.items():
        print(f"{label:<15} {data['total_trades']:<8} {data['wins']:<6} {data['losses']:<8} {data['win_rate']:<8} {data['total_pips']:<10}")

    print("\n" + "=" * 60)


def run_live_test(symbol, thresholds=list(range(1, 31)), include_flip=True):
    """Run live test with multiple thresholds"""
    testers = {}
    for threshold in thresholds:
        for flip in ([False, True] if include_flip else [False]):
            label = f">{threshold}" + (" FLIP" if flip else "")
            testers[label] = StrategyTester(symbol, threshold=threshold, flip=flip)

    print(f"Running live test on {symbol}... (Ctrl+C to stop)\n")

    try:
        while True:
            quote = fetch_live_quote(symbol)
            if quote:
                for label, tester in testers.items():
                    tester.process_tick(quote["ts"], quote["bid"], quote["ask"])

                # Display every 5 seconds
                results = {label: tester.summary() for label, tester in testers.items()}
                display_results(symbol, results)

            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\nStopped.")
        results = {label: tester.summary() for label, tester in testers.items()}
        display_results(symbol, results)


if __name__ == "__main__":
    symbol = "GBPAUD_C"
    take_profit = None

    print("Strategy Tester")
    print("1. Replay (from _price_capture.jsonl)")
    print("2. Live")
    choice = input("Select mode (1/2): ").strip()

    if choice == "1":
        date_str = input("Date (YYYY-MM-DD) or Enter for today: ").strip() or None
        results, debug_info = run_replay_test(symbol, date_str, take_profit=take_profit)
        if results:
            display_results(symbol, results, debug_info, take_profit=take_profit)
            input("\nPress Enter to exit...")
    else:
        run_live_test(symbol)
