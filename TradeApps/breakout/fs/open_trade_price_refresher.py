from __future__ import annotations

import argparse
import json
import os
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set

import common


def _discover_open_products(run_mode: str, date_str: str, explicit_products: Optional[List[str]] = None) -> List[str]:
    if explicit_products:
        return sorted({str(product).upper() for product in explicit_products if product})

    products: Set[str] = set()
    for day_dir in common._iter_day_directories(run_mode, date_str):
        for file_path in day_dir.glob("*_op.json"):
            try:
                with open(file_path, "r") as handle:
                    data = json.load(handle) or {}
            except Exception:
                continue

            if str(data.get("status", "")).upper() != "OPEN":
                continue

            product = str(data.get("product") or "").upper()
            if product:
                products.add(product)

    return sorted(products)


def _build_latest_prices(products: List[str]) -> Dict[str, Dict[str, Optional[float]]]:
    latest_prices: Dict[str, Dict[str, Optional[float]]] = {}
    for product in products:
        try:
            quotes = common.fetch_latest_quotes(product)
            if not quotes:
                continue
            latest = quotes[-1]
            latest_prices[product] = {
                "price": latest.price,
                "bid": latest.bid,
                "ask": latest.ask,
                "timestamp": latest.timestamp,
            }
        except Exception as exc:
            print(f"[REFRESH] Quote fetch failed for {product}: {exc}")
    return latest_prices


def run_refresh_cycle(run_mode: str, date_str: str, explicit_products: Optional[List[str]] = None) -> int:
    config = common._load_config()
    products = _discover_open_products(run_mode, date_str, explicit_products=explicit_products)
    if not products:
        print(f"[REFRESH] No open trade files found for mode={run_mode} date={date_str}")
        return 0

    common._LATEST_TRADING_DATE = date_str
    latest_prices = _build_latest_prices(products)
    if not latest_prices:
        print(f"[REFRESH] No live quotes available for open products: {', '.join(products)}")
        return 0

    json_base_dir = os.path.join(Path(common.CONFIG_FILE_PATH).resolve().parent, "json", run_mode)
    common._update_open_trade_json_prices(json_base_dir, latest_prices, config)
    print(
        f"[REFRESH] Updated open trade files for {len(latest_prices)} products at "
        f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )
    return len(latest_prices)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Refresh OPEN trade JSON prices alongside the main breakout process.")
    parser.add_argument("--mode", default=None, help="Run mode, defaults to config run_mode")
    parser.add_argument("--date", default=None, help="Trading date in YYYY-MM-DD, defaults to today")
    parser.add_argument("--interval", type=int, default=5, help="Refresh interval in seconds")
    parser.add_argument("--products", nargs="*", default=None, help="Optional product filter list")
    parser.add_argument("--once", action="store_true", help="Run one refresh cycle and exit")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = common._load_config()
    run_mode = str(args.mode or config.get("run_mode", "live")).lower()
    date_str = str(args.date or datetime.now().strftime("%Y-%m-%d"))
    interval = max(1, int(args.interval))

    if args.once:
        run_refresh_cycle(run_mode, date_str, explicit_products=args.products)
        return

    print(
        f"[REFRESH] Starting standalone open trade refresher "
        f"(mode={run_mode}, date={date_str}, interval={interval}s)"
    )
    while True:
        try:
            run_refresh_cycle(run_mode, date_str, explicit_products=args.products)
        except KeyboardInterrupt:
            print("[REFRESH] Stopped")
            return
        except Exception as exc:
            print(f"[REFRESH] Cycle failed: {exc}")
        time.sleep(interval)


if __name__ == "__main__":
    main()
