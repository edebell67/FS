# workstreams/WF-401/regime_analytics.py — Regime statistics, lift, confidence, and sufficiency states.
#
# VERSION HISTORY
# v1.0.0 · 2026-08-23 · Initial version: computes evidence-aware regime slices from prejoined leakage-free observations.

from collections import defaultdict
from decimal import Decimal
from math import sqrt

MIN_TRADES=30

def calculate(rows):
 overall=sum((Decimal(str(r["net_return"])) for r in rows),Decimal(0))/Decimal(len(rows)) if rows else None
 groups=defaultdict(list)
 for row in rows: groups[row.get("regime","UNKNOWN")].append(Decimal(str(row["net_return"])))
 result={}
 for regime,values in groups.items():
  n=len(values); mean=sum(values,Decimal(0))/Decimal(n); variance=sum(((v-mean)**2 for v in values),Decimal(0))/Decimal(n-1) if n>1 else None
  result[regime]={"trades":n,"net_return":sum(values,Decimal(0)),"mean_return":mean,"win_rate":Decimal(sum(v>0 for v in values))/Decimal(n),"lift":mean-overall if overall is not None else None,"standard_error":Decimal(str(sqrt(float(variance)/n))) if variance is not None else None,"sufficiency":"SUFFICIENT" if n>=MIN_TRADES else "INSUFFICIENT"}
 return result

