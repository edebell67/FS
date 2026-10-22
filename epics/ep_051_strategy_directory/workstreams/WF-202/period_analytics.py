# workstreams/WF-202/period_analytics.py — UTC period bucketing, rolling results, consistency, and concentration.
#
# VERSION HISTORY
# v1.0.0 · 2026-08-23 · Initial version: calculates deterministic day/week/month and rolling evidence with completeness.

from __future__ import annotations
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from statistics import median


def bucket_start(value: datetime, period: str) -> datetime:
    utc=value.astimezone(timezone.utc)
    if period == "DAY": return utc.replace(hour=0,minute=0,second=0,microsecond=0)
    if period == "WEEK": return (utc-timedelta(days=utc.weekday())).replace(hour=0,minute=0,second=0,microsecond=0)
    if period == "MONTH": return utc.replace(day=1,hour=0,minute=0,second=0,microsecond=0)
    raise ValueError("unsupported period")


def aggregate(trades, period, *, as_of):
    groups=defaultdict(list)
    for row in trades: groups[bucket_start(row["exit_at"],period)].append(Decimal(str(row["net_return"])))
    results=[]
    for start, values in sorted(groups.items()):
        if period=="DAY": end=start+timedelta(days=1)
        elif period=="WEEK": end=start+timedelta(days=7)
        else: end=(start.replace(day=28)+timedelta(days=4)).replace(day=1)
        total=sum(values,Decimal(0)); count=len(values)
        results.append({"period_start":start,"period_end":end,"trades":count,"winners":sum(v>0 for v in values),"losers":sum(v<0 for v in values),"breakevens":sum(v==0 for v in values),"net_return":total,"mean_trade":total/Decimal(count),"median_trade":Decimal(str(median(values))),"completeness":"COMPLETE" if as_of>=end else "INCOMPLETE"})
    return results


def rolling(period_rows, window):
    return [{"period_start":period_rows[i]["period_start"],"window":window,"net_return":sum((r["net_return"] for r in period_rows[max(0,i-window+1):i+1]),Decimal(0)),"observations":min(i+1,window),"complete":i+1>=window} for i in range(len(period_rows))]


def consistency(period_rows):
    values=[r["net_return"] for r in period_rows if r["completeness"]=="COMPLETE"]
    if not values:return {"profitable_period_ratio":None,"top_period_concentration":None}
    total=sum(values,Decimal(0)); positive_total=sum((v for v in values if v>0),Decimal(0)); top=max(values)
    return {"profitable_period_ratio":Decimal(sum(v>0 for v in values))/Decimal(len(values)),"top_period_concentration":top/positive_total if positive_total else None}

