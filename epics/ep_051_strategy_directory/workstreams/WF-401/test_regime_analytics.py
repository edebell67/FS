# workstreams/WF-401/test_regime_analytics.py — Fixed-fixture regime analytics tests.
#
# VERSION HISTORY
# v1.0.0 · 2026-08-23 · Initial version: validates reconciliation, lift, sparse-state suppression, and UNKNOWN honesty.

import unittest
from decimal import Decimal
from regime_analytics import calculate

class Tests(unittest.TestCase):
 def test_reconciles(self):
  rows=[{"regime":"UP","net_return":2},{"regime":"DOWN","net_return":-1}];out=calculate(rows);self.assertEqual(Decimal(1),sum((v["net_return"] for v in out.values()),Decimal(0)))
 def test_lift(self):self.assertEqual(Decimal("1.5"),calculate([{"regime":"UP","net_return":2},{"regime":"DOWN","net_return":-1}])["UP"]["lift"])
 def test_sparse_is_insufficient(self):self.assertEqual("INSUFFICIENT",calculate([{"regime":"UP","net_return":1}])["UP"]["sufficiency"])
 def test_unknown_preserved(self):self.assertIn("UNKNOWN",calculate([{"regime":"UNKNOWN","net_return":0}]))
 def test_sufficient_threshold(self):self.assertEqual("SUFFICIENT",calculate([{"regime":"UP","net_return":1} for _ in range(30)])["UP"]["sufficiency"])

if __name__=="__main__":unittest.main()
