# workstreams/WF-402/alignment.py — Versioned daily strategy-series alignment with explicit zero and missing policies.
#
# VERSION HISTORY
# v1.0.0 · 2026-08-23 · Initial version: aggregates asynchronous trades before pair alignment and reports overlap quality.

from collections import defaultdict
from decimal import Decimal

def daily_series(trades,calendar):
 totals=defaultdict(lambda:Decimal(0))
 for row in trades:totals[(row["strategy_id"],row["exit_at"].date())]+=Decimal(str(row["net_return"]))
 result={}
 for strategy in {r["strategy_id"] for r in trades}:
  result[strategy]={day:(totals[(strategy,day)] if state=="COMPLETE" else None) for day,state in calendar.items()}
 return result

def align(series_a,series_b,min_overlap=30):
 dates=sorted(set(series_a)&set(series_b));pairs=[(d,series_a[d],series_b[d]) for d in dates if series_a[d] is not None and series_b[d] is not None]
 return {"pairs":pairs,"overlap_count":len(pairs),"calendar_count":len(dates),"overlap_ratio":len(pairs)/len(dates) if dates else 0.0,"quality":"SUFFICIENT" if len(pairs)>=min_overlap else "INSUFFICIENT"}

