# workstreams/WF-201/test_analytics.py — Golden and edge-case tests for headline analytics.
#
# VERSION HISTORY
# v1.0.0 · 2026-08-23 · Initial version: validates formulas, closed-only scope, drawdown, excursion, null ratios, and cost semantics.

import unittest
from datetime import datetime, timedelta, timezone
from decimal import Decimal

from analytics import calculate_headline

T0 = datetime(2026, 1, 1, tzinfo=timezone.utc)


def trade(guid, value, minutes=60, role="closed", **extra):
    row = {"guid": guid, "record_role": role, "created_at": T0, "exit_at": T0 + timedelta(minutes=minutes), "net_return": value, "close_type": "target reached"}
    row.update(extra); return row


class AnalyticsTests(unittest.TestCase):
    def test_golden_metrics_and_outcome_semantics(self):
        result = calculate_headline([trade("a", "10"), trade("b", "-4", 120), trade("c", "0", 30)])
        self.assertEqual((3, 1, 1, 1), (result["total_trades"], result["wins"], result["losses"], result["breakevens"]))
        self.assertEqual(Decimal("6.00000000"), result["total_net_return"])
        self.assertEqual(Decimal("2.50000000"), result["profit_factor"])
        self.assertEqual(Decimal("-4.00000000"), result["max_drawdown_money"])

    def test_open_rows_are_excluded(self):
        result = calculate_headline([trade("a", "10"), trade("o", "999", role="open")])
        self.assertEqual(1, result["total_trades"])
        self.assertEqual(Decimal("10.00000000"), result["total_net_return"])

    def test_net_return_is_not_reduced_by_commission(self):
        result = calculate_headline([trade("a", "95", commission="5")])
        self.assertEqual(Decimal("95.00000000"), result["total_net_return"])

    def test_no_losses_returns_null_profit_factor(self):
        self.assertIsNone(calculate_headline([trade("a", "2")])["profit_factor"])

    def test_no_capital_returns_null_percentage_drawdown(self):
        self.assertIsNone(calculate_headline([trade("a", "-2")])["max_drawdown_percent"])

    def test_capital_enables_percentage_drawdown(self):
        self.assertEqual(Decimal("-0.02000000"), calculate_headline([trade("a", "-2")], starting_equity=Decimal("100"))["max_drawdown_percent"])

    def test_excursion_and_holding(self):
        result = calculate_headline([trade("a", "5", 90, max_net_return="8", min_net_return="-3")])
        self.assertEqual(Decimal("90.00000000"), result["mean_holding_minutes"])
        self.assertEqual(Decimal("8.00000000"), result["mean_mfe"])
        self.assertEqual(Decimal("-3.00000000"), result["mean_mae"])

    def test_empty_input_has_explicit_quality_and_nulls(self):
        result = calculate_headline([])
        self.assertEqual("NO_DATA", result["quality_state"])
        self.assertIsNone(result["win_rate"])


if __name__ == "__main__": unittest.main()
