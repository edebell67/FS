"""Version history: 1.0.0 (2026-08-23) — adapter conformance suite."""
import unittest
from datetime import datetime
from decimal import Decimal
from adapter_sdk import FXAdapter,Instrument,canonical_trade

FX={"strategy_id":"DNA_102001","symbol":"EUR/GBP","opened_at":"2026-01-01T00:00:00Z","closed_at":"2026-01-01T01:00:00Z","net_return":"12.5"}
class FutureAdapter:
 def instrument(self,r):return Instrument("FUTURES","CME","ES-202612","ESZ6","USD","USD",Decimal("50"),Decimal("0.25"),"CME_EQUITY")
 def timestamp(self,v):return datetime.fromisoformat(v.replace("Z","+00:00"))
 def net_return(self,r,i):return Decimal(str(r["price_change"]))*i.contract_multiplier*Decimal(str(r["contracts"]))
class Tests(unittest.TestCase):
 def test_fx_unchanged(self):
  result=canonical_trade(FXAdapter(),FX);self.assertEqual(("FX","EUR_GBP",Decimal("12.5"),"GBP"),(result["market"],result["instrument"]["instrument_id"],result["net_return"],result["currency"]))
 def test_future_uses_same_canonical_shape(self):
  raw={"strategy_id":"DNA_202001","opened_at":"2026-01-01T00:00:00Z","closed_at":"2026-01-01T01:00:00Z","price_change":"2","contracts":1};result=canonical_trade(FutureAdapter(),raw);self.assertEqual(Decimal("100"),result["net_return"]);self.assertEqual(set(canonical_trade(FXAdapter(),FX)),set(result))
 def test_outcome_uses_net_return(self):self.assertEqual("winner",canonical_trade(FXAdapter(),FX)["outcome"])
 def test_invalid_time_rejected(self):
  raw=dict(FX,closed_at="2025-01-01T00:00:00Z")
  with self.assertRaises(ValueError):canonical_trade(FXAdapter(),raw)
 def test_contract_metadata_is_explicit(self):
  i=FutureAdapter().instrument({});self.assertEqual((Decimal("50"),Decimal("0.25"),"CME_EQUITY"),(i.contract_multiplier,i.tick_size,i.calendar_id))
if __name__=="__main__":unittest.main()

