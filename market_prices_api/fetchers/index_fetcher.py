import json
import time
import os
import threading
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class IndexFetcher:
    """
    Fetcher that monitors a local JSON file for index price updates.
    Watches Z:\\algo_forex\\prices\\index_prices.json
    """
    def __init__(self, cache, file_path=r"Z:\algo_forex\prices\index_prices.json", interval=0.5):
        self.cache = cache
        self.file_path = file_path
        self.interval = interval
        self._stop_event = threading.Event()
        self._thread = None
        self._last_mtime = 0

    def start(self):
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()
        logger.info("Index fetcher started")

    def stop(self):
        self._stop_event.set()
        if self._thread:
            self._thread.join()
        logger.info("Index fetcher stopped")

    def _run(self):
        logger.info(f"Starting IndexFetcher watching: {self.file_path}")
        while not self._stop_event.is_set():
            try:
                if os.path.exists(self.file_path):
                    mtime = os.path.getmtime(self.file_path)
                    if mtime > self._last_mtime:
                        self._process_file()
                        self._last_mtime = mtime
            except Exception as e:
                logger.error(f"Error checking index JSON file: {e}")

            time.sleep(self.interval)

    def _process_file(self):
        """Reads JSON and updates the central price cache."""
        try:
            with open(self.file_path, 'r') as f:
                data = json.load(f)

                if "futures" in data:
                    for code, prices in data["futures"].items():
                        self.cache.update(
                            code=code,
                            quote_type="I",
                            bid=float(prices.get("bid", 0)),
                            ask=float(prices.get("ask", 0)),
                            provider="FILE_INDEX"
                        )

            logger.debug(f"Updated cache from {self.file_path}")
        except Exception as e:
            logger.error(f"Error processing index JSON data: {e}")

    def get_status(self):
        return {
            "source": self.file_path,
            "last_mtime": datetime.fromtimestamp(self._last_mtime).isoformat() if self._last_mtime > 0 else "Never",
            "active": self._thread is not None and self._thread.is_alive(),
            "type": "file_watcher"
        }
