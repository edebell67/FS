# workstreams/WF-204/read_models.py — Evidence envelopes, stable pagination, filtering, sorting, and authorization.
#
# VERSION HISTORY
# v1.1.0 · 2026-08-23 · Owner-scoped, allowlisted open-state authorization.
# v1.0.0 · 2026-08-23 · Initial version: implements deterministic public read-model behavior without exposing restricted fields.

from datetime import datetime,timezone

PUBLIC_FIELDS={"strategy_id","descriptive_name","market","status","total_trades","total_net_return","win_rate","profit_factor","max_drawdown_money","quality_state"}
OPEN_FIELDS={"strategy_id","instrument_id","signal","created_at","last_update","unrealized_net_return","quality_state"}

def envelope(data,*,basis="GBP monetary P&L",methodology="1.0.0",quality="VALID"):
 return {"data":data,"as_of":datetime.now(timezone.utc).isoformat(),"basis":basis,"methodology_version":methodology,"quality_state":quality}

def list_strategies(rows,*,limit=20,cursor=None,sort="strategy_id",minimum_trades=0):
 if not 1<=limit<=100:raise ValueError("limit must be 1..100")
 public=[{k:v for k,v in row.items() if k in PUBLIC_FIELDS} for row in rows if row.get("visibility")=="public" and row.get("total_trades",0)>=minimum_trades]
 public.sort(key=lambda r:(r.get(sort) is None,r.get(sort),r["strategy_id"]))
 if cursor:public=[r for r in public if r["strategy_id"]>cursor]
 page=public[:limit];return envelope({"items":page,"next_cursor":page[-1]["strategy_id"] if len(public)>limit and page else None})

def open_trades(rows,principal):
 """Return owner-scoped, allowlisted current state for a trusted principal."""
 if not isinstance(principal,dict) or principal.get("role") not in {"user","operator","admin"}:raise PermissionError("authentication required")
 role=principal["role"];account_id=principal.get("account_id")
 if role=="user" and not account_id:raise PermissionError("account scope required")
 scoped=rows if role in {"operator","admin"} else [row for row in rows if row.get("account_id")==account_id]
 return envelope([{k:v for k,v in row.items() if k in OPEN_FIELDS} for row in scoped],quality="CURRENT_STATE")
