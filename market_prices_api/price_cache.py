"""
Thread-safe in-memory price cache with TTL support.
No database dependency.
"""

import threading
from datetime import datetime, timezone
from typing import Any, Dict, List
from dataclasses import dataclass


@dataclass
class Quote:
    """Single price quote."""
    id: int
    timestamp: str
    code: str
    type: str  # C=crypto, X=futures, F=forex, FS=forex sim, I=index
    bid: float
    ask: float
    provider: str = ""
    stale: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "timestamp": self.timestamp,
            "code": self.code,
            "type": self.type,
            "bid": self.bid,
            "ask": self.ask,
            "stale": self.stale,
        }


class PriceCache:
    """
    Thread-safe in-memory cache for market prices.

    Stores latest quote per symbol, grouped by type.
    """

    def __init__(self, stale_threshold_seconds: int = 120):
        self._lock = threading.RLock()
        self._quotes: Dict[str, Quote] = {}  # key: "type:code" e.g. "C:btc"
        self._id_counter = 0
        self._stale_threshold = stale_threshold_seconds

    @staticmethod
    def _local_now() -> datetime:
        """Return an aware datetime in the host machine's local timezone."""
        return datetime.now().astimezone()

    def update(self, code: str, quote_type: str, bid: float, ask: float, provider: str = "") -> None:
        """Update or insert a quote."""
        with self._lock:
            key = f"{quote_type}:{code.lower()}"
            self._id_counter += 1

            if quote_type == "C":             # crypto
                bid_value = round(bid, 5)
                ask_value = round(ask, 5)
            elif quote_type == "X":           # futures
                bid_value = round(bid, 4)
                ask_value = round(ask, 4)
            elif quote_type in ("F", "FS"):   # forex + forex sim
                bid_value = round(bid, 5)
                ask_value = round(ask, 5)
            elif quote_type == "I":           # indices
                bid_value = round(bid, 4)
                ask_value = round(ask, 4)
            else:
                bid_value = round(bid, 5)
                ask_value = round(ask, 5)

            self._quotes[key] = Quote(
                id=self._id_counter,
                timestamp=self._local_now().isoformat(timespec="microseconds"),
                code=code.lower(),
                type=quote_type,
                bid=bid_value,
                ask=ask_value,
                provider=provider,
                stale=False,
            )

    def get_by_type(self, quote_type: str) -> List[Dict[str, Any]]:
        """Get all quotes of a specific type."""
        with self._lock:
            now = self._local_now()
            results: List[Dict[str, Any]] = []

            for quote in self._quotes.values():
                if quote.type == quote_type:
                    try:
                        ts = datetime.fromisoformat(quote.timestamp.replace("Z", "+00:00"))
                        if ts.tzinfo is None:
                            ts = ts.replace(tzinfo=timezone.utc)

                        age = (now - ts).total_seconds()
                        quote.stale = abs(age) > self._stale_threshold
                    except Exception:
                        quote.stale = True

                    results.append(quote.to_dict())

            return results

    def get_crypto(self) -> List[Dict[str, Any]]:
        """Get all crypto quotes."""
        return self.get_by_type("C")

    def get_futures(self) -> List[Dict[str, Any]]:
        """Get all futures quotes."""
        return self.get_by_type("X")

    def get_forex(self) -> List[Dict[str, Any]]:
        """Get all forex quotes."""
        return self.get_by_type("F")

    def get_forex_sim(self) -> List[Dict[str, Any]]:
        """Get all simulation forex quotes."""
        return self.get_by_type("FS")

    def get_indices(self) -> List[Dict[str, Any]]:
        """Get all index quotes."""
        return self.get_by_type("I")

    def get_all(self) -> Dict[str, List[Dict[str, Any]]]:
        """Get all quotes grouped by type."""
        return {
            "crypto": self.get_crypto(),
            "futures": self.get_futures(),
            "forex": self.get_forex(),
            "forex_sim": self.get_forex_sim(),
            "indices": self.get_indices(),
        }

    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        with self._lock:
            crypto_count = sum(1 for k in self._quotes if k.startswith("C:"))
            futures_count = sum(1 for k in self._quotes if k.startswith("X:"))
            forex_count = sum(1 for k in self._quotes if k.startswith("F:"))
            sim_count = sum(1 for k in self._quotes if k.startswith("FS:"))
            index_count = sum(1 for k in self._quotes if k.startswith("I:"))

            return {
                "total_quotes": len(self._quotes),
                "crypto_count": crypto_count,
                "futures_count": futures_count,
                "forex_count": forex_count,
                "forex_sim_count": sim_count,
                "index_count": index_count,
                "id_counter": self._id_counter,
            }

    def clear(self) -> None:
        """Clear all cached quotes."""
        with self._lock:
            self._quotes.clear()


# Global cache instance
cache = PriceCache()