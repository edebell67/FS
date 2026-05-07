"""
Futures price fetcher - Yahoo Finance API.
Runs in background thread, updates cache every 30 seconds (rate limit safe).
"""

import threading
import time
import json
import urllib.request
import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)

# Symbols to track (Yahoo format -> our code)
SYMBOLS = {
    "ES=F": "es",     # E-mini S&P 500
    "NQ=F": "nq",     # E-mini Nasdaq
    "YM=F": "ym",     # E-mini Dow
    "RTY=F": "rty",   # E-mini Russell
    "GC=F": "gc",     # Gold
    "SI=F": "si",     # Silver
    "HG=F": "hg",     # Copper
    "CL=F": "cl",     # Crude Oil WTI
    "BZ=F": "bz",     # Brent Crude
    "NG=F": "ng",     # Natural Gas
    "ZB=F": "zb",     # U.S. Treasury Bond Future
    "ZN=F": "zn",     # U.S. Treasury Note Future  
    "ZF=F": "zf",     # 10-Year T-Note Futures,
    "ZT=F": "zt",     # 2-Year T-Note Futures
}

POLL_INTERVAL = 30  # seconds (Yahoo rate limit safe)
SPREAD_PCT = 0.0002  # 0.02% simulated spread
REQUEST_DELAY = 0.2  # delay between individual requests


class FuturesFetcher:
    """Fetches futures prices from Yahoo Finance and updates cache."""

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
        logger.info("Futures fetcher started")

    def stop(self):
        """Stop the fetcher."""
        self.running = False
        if self._thread:
            self._thread.join(timeout=5)
        logger.info("Futures fetcher stopped")

    def _run(self):
        """Main fetcher loop."""
        while self.running:
            try:
                count = self._fetch_all()
                if count > 0:
                    self.success_count += 1
                    self.last_update = time.time()
                else:
                    self.error_count += 1
            except Exception as e:
                logger.error(f"Futures fetch error: {e}")
                self.error_count += 1

            time.sleep(POLL_INTERVAL)

    def _fetch_yahoo(self, symbol: str) -> Optional[float]:
        """Fetch single price from Yahoo Finance."""
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?interval=1d&range=1d"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode())
                return float(data["chart"]["result"][0]["meta"]["regularMarketPrice"])
        except Exception as e:
            logger.warning(f"Yahoo error for {symbol}: {e}")
            return None

    def _fetch_all(self) -> int:
        """Fetch all futures prices."""
        count = 0
        for yahoo_sym, code in SYMBOLS.items():
            if not self.running:
                break

            price = self._fetch_yahoo(yahoo_sym)
            if price:
                spread = price * SPREAD_PCT
                bid = price - spread / 2
                ask = price + spread / 2
                self.cache.update(code, "X", bid, ask, "yahoo")
                count += 1

            time.sleep(REQUEST_DELAY)

        return count

    def get_status(self) -> Dict:
        """Get fetcher status."""
        return {
            "name": "futures",
            "source": "yahoo",
            "running": self.running,
            "last_update": self.last_update,
            "success_count": self.success_count,
            "error_count": self.error_count,
            "symbols": list(SYMBOLS.values()),
            "interval_seconds": POLL_INTERVAL
        }
