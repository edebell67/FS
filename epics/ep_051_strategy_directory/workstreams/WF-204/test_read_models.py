# workstreams/WF-204/test_read_models.py — Contract, authorization, pagination, and exposure tests.
#
# VERSION HISTORY
# v1.0.0 · 2026-08-23 · Initial version: validates evidence envelopes, stable pages, restricted fields, and open-state authorization.

import unittest
from read_models import list_strategies,open_trades

class Tests(unittest.TestCase):
 def rows(self):return [{"strategy_id":f"DNA_{i:06d}","visibility":"public","total_trades":i,"market":"FX","broker_account":"secret"} for i in range(1,151)]
 def test_envelope_metadata(self):
  result=list_strategies(self.rows());self.assertIn("as_of",result);self.assertIn("basis",result);self.assertIn("methodology_version",result)
 def test_limit_and_cursor(self):
  first=list_strategies(self.rows(),limit=10);second=list_strategies(self.rows(),limit=10,cursor=first["data"]["next_cursor"]);self.assertEqual(10,len(first["data"]["items"]));self.assertNotEqual(first["data"]["items"][0]["strategy_id"],second["data"]["items"][0]["strategy_id"])
 def test_restricted_field_removed(self):self.assertNotIn("broker_account",list_strategies(self.rows())["data"]["items"][0])
 def test_private_rows_removed(self):
  rows=self.rows();rows[0]["visibility"]="private";self.assertNotIn("DNA_000001",[r["strategy_id"] for r in list_strategies(rows,limit=100)["data"]["items"]])
 def test_filter(self):self.assertTrue(all(r["total_trades"]>=100 for r in list_strategies(self.rows(),limit=100,minimum_trades=100)["data"]["items"]))
 def test_invalid_limit(self):
  with self.assertRaises(ValueError):list_strategies(self.rows(),limit=101)
 def test_open_requires_authentication(self):
  with self.assertRaises(PermissionError):open_trades([],{"role":"public"})
 def test_open_authenticated(self):self.assertEqual("CURRENT_STATE",open_trades([],{"role":"user","account_id":"a1"})["quality_state"])
 def test_open_is_owner_scoped_and_redacted(self):
  rows=[{"account_id":"a1","strategy_id":"DNA_1","instrument_id":"EUR_GBP","broker_account":"secret"},{"account_id":"a2","strategy_id":"DNA_2","instrument_id":"USD_JPY"}]
  result=open_trades(rows,{"role":"user","account_id":"a1"})["data"]
  self.assertEqual(["DNA_1"],[row["strategy_id"] for row in result]);self.assertNotIn("broker_account",result[0]);self.assertNotIn("account_id",result[0])
 def test_open_user_requires_account_scope(self):
  with self.assertRaises(PermissionError):open_trades([],{"role":"user"})

if __name__=="__main__":unittest.main()
