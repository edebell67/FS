"""
Forex price fetcher - Passthrough from existing API.
Fetches from http://127.0.0.1:8001/api/vw_000_fx_quotes?db=tradedb
Runs in background thread, updates cache every 5 seconds.
"""

import threading
import time
import json
import urllib.request
import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

# Source API
SOURCE_URL = "http://127.0.0.1:8001/api/vw_000_fx_quotes?db=tradedb"
POLL_INTERVAL = 5  # seconds


class ForexFetcher:
    """Fetches forex prices from existing API and updates cache."""

    def __init__(self, cache, source_url: str = SOURCE_URL):
        self.cache = cache
        self.source_url = source_url
        self.running = False
        self._thread: Optional[threading.Thread] = None
        self.last_update: Optional[float] = None
        self.error_count = 0
        self.success_count = 0
        self.available = True  # Track if source is available

    def start(self):
        """Start the fetcher in background thread."""
        if self.running:
            return
        self.running = True
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()
        logger.info("Forex fetcher started")

    def stop(self):
        """Stop the fetcher."""
        self.running = False
        if self._thread:
            self._thread.join(timeout=5)
        logger.info("Forex fetcher stopped")

    def _run(self):
        """Main fetcher loop."""
        while self.running:
            try:
                quotes = self._fetch_source()
                if quotes:
                    self._update_cache(quotes)
                    self.success_count += 1
                    self.last_update = time.time()
                    self.available = True
                else:
                    self.error_count += 1
                    self.available = False
            except Exception as e:
                logger.warning(f"Forex fetch error: {e}")
                self.error_count += 1
                self.available = False

            time.sleep(POLL_INTERVAL)

    def _fetch_source(self) -> List[Dict]:
        """Fetch from existing API."""
        try:
            with urllib.request.urlopen(self.source_url, timeout=5) as resp:
                data = json.loads(resp.read().decode())
                # Handle both {"data": [...]} and direct [...] formats
                if isinstance(data, dict) and "data" in data:
                    return data["data"]
                elif isinstance(data, list):
                    return data
                return []
        except urllib.error.URLError as e:
            logger.debug(f"Forex source unavailable: {e}")
            return []
        except Exception as e:
            logger.warning(f"Forex API error: {e}")
            return []

    def _update_cache(self, quotes: List[Dict]):
        """Update cache with fetched quotes."""
        for q in quotes:
            code = q.get("code", "").lower()
            if not code:
                continue

            bid = float(q.get("bid", 0))
            ask = float(q.get("ask", 0))

            if bid > 0 and ask > 0:
                self.cache.update(code, "F", bid, ask, "passthrough")

    def get_status(self) -> Dict:
        """Get fetcher status."""
        return {
            "name": "forex",
            "source": "passthrough",
            "source_url": self.source_url,
            "running": self.running,
            "available": self.available,
            "last_update": self.last_update,
            "success_count": self.success_count,
            "error_count": self.error_count,
            "interval_seconds": POLL_INTERVAL
        }
