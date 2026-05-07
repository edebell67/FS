"""
Crypto price fetcher - Binance API.
Runs in background thread, updates cache every 5 seconds.
"""

import threading
import time
import json
import urllib.request
import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)

# Symbols to track (Binance format -> our code)
SYMBOLS = {
    "BTCUSDT": "btc",
    "ETHUSDT": "eth",
    "SOLUSDT": "sol",
    "AVAXUSDT": "avax",
    "XRPUSDT": "xrp",
    "ADAUSDT": "ada",
    "DOGEUSDT": "doge",
}

POLL_INTERVAL = 5  # seconds
SPREAD_PCT = 0.0001  # 0.01% simulated spread


class CryptoFetcher:
    """Fetches crypto prices from Binance and updates cache."""

    def __init__(self, cache):
        self.cache = cache
        self.running = False
        self._thread: Optional[threading.Thread] = None
        self.last_update: Optional[float] = None
        self.error_count = 0
        self.success_count = 0

    def start(self):
        """Start the fetcher in background thread."""
        if self.running:
            return
        self.running = True
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()
        logger.info("Crypto fetcher started")

    def stop(self):
        """Stop the fetcher."""
        self.running = False
        if self._thread:
            self._thread.join(timeout=5)
        logger.info("Crypto fetcher stopped")

    def _run(self):
        """Main fetcher loop."""
        while self.running:
            try:
                prices = self._fetch_binance()
                if prices:
                    self._update_cache(prices)
                    self.success_count += 1
                    self.last_update = time.time()
                else:
                    self.error_count += 1
            except Exception as e:
                logger.error(f"Crypto fetch error: {e}")
                self.error_count += 1

            time.sleep(POLL_INTERVAL)

    def _fetch_binance(self) -> Dict[str, float]:
        """Fetch all prices from Binance in one call."""
        url = "https://api.binance.com/api/v3/ticker/price"
        try:
            with urllib.request.urlopen(url, timeout=10) as resp:
                data = json.loads(resp.read().decode())
                return {item["symbol"]: float(item["price"]) for item in data}
        except Exception as e:
            logger.warning(f"Binance API error: {e}")
            return {}

    def _update_cache(self, prices: Dict[str, float]):
        """Update cache with fetched prices."""
        for binance_sym, code in SYMBOLS.items():
            if binance_sym in prices:
                price = prices[binance_sym]
                spread = price * SPREAD_PCT
                bid = price - spread / 2
                ask = price + spread / 2
                self.cache.update(code, "C", bid, ask, "binance")

    def get_status(self) -> Dict:
        """Get fetcher status."""
        return {
            "name": "crypto",
            "source": "binance",
            "running": self.running,
            "last_update": self.last_update,
            "success_count": self.success_count,
            "error_count": self.error_count,
            "symbols": list(SYMBOLS.values()),
            "interval_seconds": POLL_INTERVAL
        }
