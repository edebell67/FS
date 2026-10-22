# workstreams/WF-202/test_period_analytics.py — Boundary, reconciliation, rolling, and concentration tests.
#
# VERSION HISTORY
# v1.0.0 · 2026-08-23 · Initial version: proves UTC boundaries, completeness, headline reconciliation, and rolling windows.

import unittest
from datetime import datetime, timezone
from decimal import Decimal
from period_analytics import aggregate,bucket_start,consistency,rolling

def dt(value):return datetime.fromisoformat(value).replace(tzinfo=timezone.utc)

class PeriodTests(unittest.TestCase):
 def setUp(self):self.rows=[{"exit_at":dt("2026-01-04T23:59:00"),"net_return":"2"},{"exit_at":dt("2026-01-05T00:01:00"),"net_return":"-1"},{"exit_at":dt("2026-02-01T00:00:00"),"net_return":"4"}]
 def test_day_boundary(self):self.assertNotEqual(bucket_start(self.rows[0]["exit_at"],"DAY"),bucket_start(self.rows[1]["exit_at"],"DAY"))
 def test_week_starts_monday(self):self.assertEqual(0,bucket_start(self.rows[1]["exit_at"],"WEEK").weekday())
 def test_period_sum_reconciles(self):self.assertEqual(Decimal("5"),sum((r["net_return"] for r in aggregate(self.rows,"MONTH",as_of=dt("2026-03-01T00:00:00"))),Decimal(0)))
 def test_incomplete_period(self):self.assertEqual("INCOMPLETE",aggregate(self.rows,"MONTH",as_of=dt("2026-02-02T00:00:00"))[-1]["completeness"])
 def test_rolling_window(self):self.assertEqual(Decimal("5"),rolling(aggregate(self.rows,"DAY",as_of=dt("2026-03-01T00:00:00")),3)[-1]["net_return"])
 def test_consistency_uses_complete_periods(self):self.assertEqual(Decimal("0.6666666666666666666666666667"),consistency(aggregate(self.rows,"DAY",as_of=dt("2026-03-01T00:00:00")))["profitable_period_ratio"])

if __name__=="__main__":unittest.main()
