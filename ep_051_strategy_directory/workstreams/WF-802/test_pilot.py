"""Version history: 1.0.0 (2026-08-23) — pilot reconciliation tests."""
import unittest
from decimal import Decimal
from pilot import reconcile_trade,roll,SPEC
class Tests(unittest.TestCase):
 def test_tick_value_reconciles(self):
  r=reconcile_trade(entry=5000,exit=5000.25,contracts=1,commission=0,fees=0);self.assertEqual((Decimal("1"),Decimal("12.50")),(r["ticks"],r["gross"]))
 def test_costs_once(self):self.assertEqual(Decimal("9.50"),reconcile_trade(entry=5000,exit=5000.25,contracts=1,commission=2,fees=1)["net_return"])
 def test_multi_contract_sizing(self):self.assertEqual(Decimal("50.00"),reconcile_trade(entry=5000,exit=5000.25,contracts=4,commission=0,fees=0)["gross"])
 def test_losing_outcome_supported(self):self.assertLess(reconcile_trade(entry=5000,exit=4999.75,contracts=1,commission=1,fees=1)["net_return"],0)
 def test_off_tick_rejected(self):
  with self.assertRaises(ValueError):reconcile_trade(entry=5000,exit=5000.10,contracts=1,commission=0,fees=0)
 def test_roll_is_versioned(self):self.assertEqual("1.0.0",roll("U6","Z6",effective_at="2026-09-01Z",adjustment=4)["version"])
 def test_market_metadata(self):self.assertEqual(("FUTURES","USD",True),(SPEC["market"],SPEC["currency"],SPEC["illustrative"]))
if __name__=="__main__":unittest.main()

