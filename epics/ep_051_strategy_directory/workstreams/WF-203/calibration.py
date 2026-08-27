# workstreams/WF-203/calibration.py — Cohort-scoped empirical score calibration with insufficiency suppression.
#
# VERSION HISTORY
# v1.0.0 · 2026-08-23 · Initial version: freezes quantile thresholds and exposes raw components without qualitative labels.

from __future__ import annotations
import hashlib,json

MIN_COHORT=30

def quantile(values,q):
 ordered=sorted(values); position=(len(ordered)-1)*q; lo=int(position); hi=min(lo+1,len(ordered)-1); fraction=position-lo
 return ordered[lo]*(1-fraction)+ordered[hi]*fraction

def calibrate(records,metric,cohort,version):
 eligible=[r for r in records if r["cohort"]==cohort and r.get("eligible") and r.get(metric) is not None]
 if len(eligible)<MIN_COHORT:return {"status":"INSUFFICIENT","sample_size":len(eligible),"raw_components":[r.get(metric) for r in eligible],"bands":None}
 values=[float(r[metric]) for r in eligible]; thresholds=[quantile(values,q) for q in (.2,.4,.6,.8)]
 checksum=hashlib.sha256(json.dumps(sorted(values)).encode()).hexdigest()
 return {"status":"FROZEN","sample_size":len(values),"metric":metric,"cohort":cohort,"bands":thresholds,"version":version,"population_checksum":checksum,"raw_components":values}

def score(value,calibration,higher_is_better=True):
 if calibration["status"]!="FROZEN":return None
 band=1+sum(value>threshold for threshold in calibration["bands"])
 return band if higher_is_better else 6-band

