# epics/ep_057_sql_to_pgsql/scenario_engine_v2/runner/manager.py — runs many virtual races in parallel (default 5 at once, configurable at any time), queues the rest, keeps a registry.
#
# VERSION HISTORY
# v1.1.0 · 2026-10-18 · remove(race_id) and clear_finished(): delete finished races from memory.
# v1.0.0 · 2026-10-17 · Initial version: RaceManager(max_concurrent) with submit / get / list / cancel / set_max_concurrent / wait; one thread per running race, each on its own Engine and data client.
"""The cap is the number of races RUNNING at once. More submissions wait in a queue (first in, first out) and start as slots free up. The cap can be raised or lowered while races
are running; lowering it never interrupts a race, it only stops new ones from starting. The default comes from EP057_MAX_RACES (else 5)."""
from __future__ import annotations

import os
import threading
import time
from collections import OrderedDict, deque

from .race import Race, RaceConfig

DEFAULT_MAX_CONCURRENT = 5
HARD_LIMIT = 64  # a safety ceiling, not the default; "easily increased" means set_max_concurrent / EP057_MAX_RACES up to this


def default_max_concurrent() -> int:
    try:
        return max(1, min(HARD_LIMIT, int(os.environ.get("EP057_MAX_RACES", DEFAULT_MAX_CONCURRENT))))
    except ValueError:
        return DEFAULT_MAX_CONCURRENT


class RaceManager:
    def __init__(self, max_concurrent: int | None = None, client_factory=None, keep_finished: int = 200):
        self._max = default_max_concurrent() if max_concurrent is None else self._clamp(max_concurrent)
        self._client_factory = client_factory
        self._lock = threading.RLock()
        self._races: "OrderedDict[str, Race]" = OrderedDict()
        self._queue: deque = deque()
        self._running: dict = {}
        self._keep_finished = keep_finished

    @staticmethod
    def _clamp(n) -> int:
        n = int(n)
        if n < 1:
            raise ValueError("max_concurrent must be at least 1")
        return min(n, HARD_LIMIT)

    # ---- configuration ----
    @property
    def max_concurrent(self) -> int:
        return self._max

    def set_max_concurrent(self, n: int) -> int:
        with self._lock:
            self._max = self._clamp(n)
        self._pump()
        return self._max

    # ---- races ----
    def submit(self, config: RaceConfig) -> Race:
        config.validate()
        race = Race(config)
        with self._lock:
            self._races[race.race_id] = race
            self._queue.append(race)
            self._trim()
        self._pump()
        return race

    def get(self, race_id: str) -> Race | None:
        with self._lock:
            return self._races.get(race_id)

    def list(self) -> list:
        with self._lock:
            return [r.summary() for r in reversed(self._races.values())]

    def counts(self) -> dict:
        with self._lock:
            states = [r.progress.state for r in self._races.values()]
        return {"max_concurrent": self._max, "running": states.count("running"), "queued": states.count("queued"),
                "completed": states.count("completed"), "failed": states.count("failed"), "cancelled": states.count("cancelled")}

    def cancel(self, race_id: str) -> bool:
        with self._lock:
            race = self._races.get(race_id)
            if race is None or race.progress.state in ("completed", "failed", "cancelled"):
                return False
            race.cancel()
            if race in self._queue:  # never started
                self._queue.remove(race)
                race.progress.state, race.progress.finished_at = "cancelled", time.time()
            return True

    def remove(self, race_id: str) -> bool:
        """Delete a finished race (completed / failed / cancelled). Running or queued races are refused: cancel them first."""
        with self._lock:
            race = self._races.get(race_id)
            if race is None or race.progress.state not in ("completed", "failed", "cancelled"):
                return False
            del self._races[race_id]
            return True

    def clear_finished(self) -> int:
        with self._lock:
            ids = [rid for rid, r in self._races.items() if r.progress.state in ("completed", "failed", "cancelled")]
            for rid in ids:
                del self._races[rid]
            return len(ids)

    def wait(self, timeout: float = 60.0) -> bool:
        """Block until nothing is queued or running (used by tests and scripts)."""
        end = time.time() + timeout
        while time.time() < end:
            with self._lock:
                if not self._queue and not self._running:
                    return True
            time.sleep(0.02)
        return False

    # ---- scheduling ----
    def _pump(self) -> None:
        with self._lock:
            while self._queue and len(self._running) < self._max:
                race = self._queue.popleft()
                if race.progress.state == "cancelled":
                    continue
                t = threading.Thread(target=self._run, args=(race,), name=f"race-{race.race_id}", daemon=True)
                self._running[race.race_id] = t
                race.progress.state = "running"
                t.start()

    def _run(self, race: Race) -> None:
        try:
            race.run(self._client_factory)
        finally:
            with self._lock:
                self._running.pop(race.race_id, None)
            self._pump()

    def _trim(self) -> None:
        finished = [rid for rid, r in self._races.items() if r.progress.state in ("completed", "failed", "cancelled")]
        for rid in finished[:max(0, len(finished) - self._keep_finished)]:
            del self._races[rid]
