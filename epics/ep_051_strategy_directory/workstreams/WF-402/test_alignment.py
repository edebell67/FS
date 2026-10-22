# workstreams/WF-402/test_alignment.py — Daily aggregation, zero/missing, overlap, and version-policy tests.
#
# VERSION HISTORY
# v1.0.0 · 2026-08-23 · Initial version: proves raw asynchronous rows are aggregated before alignment.

import unittest
from datetime import datetime,timezone,timedelta
from decimal import Decimal
from alignment import align,daily_series

T=datetime(2026,1,1,tzinfo=timezone.utc)
class Tests(unittest.TestCase):
 def test_asynchronous_rows_aggregate_daily(self):
  trades=[{"strategy_id":"A","exit_at":T,"net_return":1},{"strategy_id":"A","exit_at":T+timedelta(hours=1),"net_return":2}];self.assertEqual(Decimal(3),daily_series(trades,{T.date():"COMPLETE"})["A"][T.date()])
 def test_complete_no_trade_is_zero(self):self.assertEqual(Decimal(0),daily_series([{"strategy_id":"A","exit_at":T,"net_return":1}],{(T+timedelta(days=1)).date():"COMPLETE"})["A"][(T+timedelta(days=1)).date()])
 def test_incomplete_day_is_null(self):self.assertIsNone(daily_series([{"strategy_id":"A","exit_at":T,"net_return":1}],{T.date():"INCOMPLETE"})["A"][T.date()])
 def test_null_excluded_from_overlap(self):self.assertEqual(1,align({1:Decimal(1),2:None},{1:Decimal(2),2:Decimal(3)})["overlap_count"])
 def test_minimum_overlap(self):self.assertEqual("INSUFFICIENT",align({1:Decimal(1)},{1:Decimal(2)})["quality"])

if __name__=="__main__":unittest.main()
