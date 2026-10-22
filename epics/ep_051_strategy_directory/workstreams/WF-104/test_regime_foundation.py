# workstreams/WF-104/test_regime_foundation.py — Tests objective classification, temporal availability, UNKNOWN, and coverage.
#
# VERSION HISTORY
# v1.0.0 · 2026-08-23 · Initial version: proves frozen thresholds and deterministic no-look-ahead joins.

import unittest
from datetime import datetime, timedelta, timezone

from regime_foundation import Observation, classify, coverage, join_regime

T0 = datetime(2026, 8, 23, tzinfo=timezone.utc)


class RegimeFoundationTests(unittest.TestCase):
    def test_frozen_direction_thresholds(self):
        self.assertEqual("TREND_UP", classify(101, 100, 1, .5, 1.5)[0])
        self.assertEqual("TREND_DOWN", classify(99, 100, 1, .5, 1.5)[0])
        self.assertEqual("SIDEWAYS", classify(100.5, 100, 1, .5, 1.5)[0])

    def test_volatility_thresholds(self):
        self.assertEqual("HIGH_VOLATILITY", classify(100, 100, 2, .5, 1.5)[1])
        self.assertEqual("LOW_VOLATILITY", classify(100, 100, .25, .5, 1.5)[1])

    def test_missing_features_are_unknown(self):
        self.assertEqual(("UNKNOWN", "UNKNOWN"), classify(None, None, None, None, None))

    def test_future_observation_cannot_join(self):
        future = Observation("EURUSD", T0, T0 + timedelta(days=1), T0 + timedelta(days=1, minutes=1), "TREND_UP", "HIGH_VOLATILITY")
        joined = join_regime(T0 + timedelta(hours=12), "EURUSD", [future])
        self.assertEqual(("UNKNOWN", "UNKNOWN"), (joined.directional_state, joined.volatility_state))

    def test_latest_available_valid_observation_wins(self):
        older = Observation("EURUSD", T0 - timedelta(days=2), T0 - timedelta(days=1), T0 - timedelta(hours=23), "SIDEWAYS", "NORMAL_VOLATILITY")
        newer = Observation("EURUSD", T0 - timedelta(days=1), T0, T0 + timedelta(minutes=1), "TREND_UP", "HIGH_VOLATILITY")
        self.assertIs(newer, join_regime(T0 + timedelta(hours=1), "EURUSD", [newer, older]))

    def test_coverage_is_explicit(self):
        known = Observation("EURUSD", T0, T0, T0, "SIDEWAYS", "NORMAL_VOLATILITY")
        unknown = Observation("EURUSD", T0, T0, T0, "UNKNOWN", "UNKNOWN")
        self.assertEqual({"total": 2, "fully_known": 1, "coverage": .5}, coverage([known, unknown]))


if __name__ == "__main__": unittest.main()
