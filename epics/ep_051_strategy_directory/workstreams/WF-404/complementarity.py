# workstreams/WF-404/complementarity.py — Transparent complementarity scoring, deterministic clusters, and rank stability.
#
# VERSION HISTORY
# v1.0.0 · 2026-08-23 · Initial version: computes published components without imputing suppressed evidence.

WEIGHTS={"return":.25,"downside":.25,"loss":.20,"drawdown":.20,"activity":.10}

def components(relationship):
 required=("return_correlation","downside_correlation","joint_loss_ratio","drawdown_overlap_ratio","independent_activity")
 if relationship.get("quality_state")!="SUFFICIENT" or any(relationship.get(k) is None for k in required):return None
 return {"return":(1-relationship["return_correlation"])/2,"downside":(1-relationship["downside_correlation"])/2,"loss":1-relationship["joint_loss_ratio"],"drawdown":1-relationship["drawdown_overlap_ratio"],"activity":relationship["independent_activity"]}

def score(relationship):
 parts=components(relationship)
 return None if parts is None else {"score":sum(parts[k]*WEIGHTS[k] for k in WEIGHTS),"components":parts,"version":"1.0.0"}

def rank(base,relationships):
 values=[]
 for row in relationships:
  result=score(row)
  if result:values.append((result["score"],row["other_strategy_id"],result["components"]))
 return [{"strategy_id":sid,"score":value,"components":parts} for value,sid,parts in sorted(values,key=lambda x:(-x[0],x[1]))]

def clusters(distances,threshold=.25):
 parent={x:x for pair in distances for x in pair[:2]}
 def find(x):
  while parent[x]!=x:parent[x]=parent[parent[x]];x=parent[x]
  return x
 for a,b,d in sorted(distances):
  if d<=threshold:
   ra,rb=find(a),find(b)
   if ra!=rb:parent[max(ra,rb)]=min(ra,rb)
 groups={}
 for item in sorted(parent):groups.setdefault(find(item),[]).append(item)
 return list(groups.values())

def rank_stability(window_rankings,max_shift=1):
 ids=set.intersection(*(set(window) for window in window_rankings)) if window_rankings else set()
 shifts={sid:max(r.index(sid) for r in window_rankings)-min(r.index(sid) for r in window_rankings) for sid in ids}
 return {"stable":all(v<=max_shift for v in shifts.values()),"rank_shifts":shifts}

