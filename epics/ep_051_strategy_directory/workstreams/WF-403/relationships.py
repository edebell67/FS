# workstreams/WF-403/relationships.py — Pairwise correlation, downside, loss and drawdown overlap.
# VERSION HISTORY
# v1.0.0 · 2026-08-23 · Initial version: calculates canonical aligned pair evidence with thin-sample suppression.
from math import sqrt

def corr(a,b):
 n=len(a)
 if n<2:return None
 ma=sum(a)/n;mb=sum(b)/n;va=sum((x-ma)**2 for x in a);vb=sum((x-mb)**2 for x in b)
 return sum((x-ma)*(y-mb) for x,y in zip(a,b))/sqrt(va*vb) if va and vb else None
def drawdowns(values):
 equity=0;peak=0;out=[]
 for value in values:equity+=value;peak=max(peak,equity);out.append(equity-peak)
 return out
def relationship(id_a,id_b,pairs,min_sample=30):
 if id_a==id_b:raise ValueError("distinct strategies required")
 id_a,id_b=sorted((id_a,id_b));a=[float(x[0]) for x in pairs];b=[float(x[1]) for x in pairs];downs=[(x,y) for x,y in zip(a,b) if x<0 or y<0];da,db=drawdowns(a),drawdowns(b);n=len(a)
 return {"strategy_id_a":id_a,"strategy_id_b":id_b,"sample_count":n,"quality_state":"SUFFICIENT" if n>=min_sample else "SUPPRESSED","return_correlation":corr(a,b) if n>=min_sample else None,"downside_correlation":corr([x for x,y in downs],[y for x,y in downs]) if n>=min_sample else None,"joint_loss_ratio":sum(x<0 and y<0 for x,y in zip(a,b))/n if n else None,"drawdown_overlap_ratio":sum(x<0 and y<0 for x,y in zip(da,db))/n if n else None,"joint_drawdown_severity":sum(min(x,y) for x,y in zip(da,db) if x<0 and y<0)}
