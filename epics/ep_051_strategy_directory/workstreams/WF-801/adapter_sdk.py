"""Canonical market adapter SDK. Version 1.0.0 (2026-08-23)."""
from dataclasses import dataclass,asdict
from datetime import datetime,timezone
from decimal import Decimal

@dataclass(frozen=True)
class Instrument:
 market:str;venue:str;instrument_id:str;symbol:str;base_currency:str;quote_currency:str;contract_multiplier:Decimal;tick_size:Decimal;calendar_id:str

def canonical_trade(adapter,raw):
 i=adapter.instrument(raw)
 opened=adapter.timestamp(raw["opened_at"]);closed=adapter.timestamp(raw["closed_at"])
 if opened.tzinfo is None or closed.tzinfo is None or closed<opened:raise ValueError("invalid timestamps")
 net=adapter.net_return(raw,i)
 return {"strategy_id":raw["strategy_id"],"market":i.market,"venue":i.venue,"instrument":asdict(i),"opened_at":opened.astimezone(timezone.utc),"closed_at":closed.astimezone(timezone.utc),"net_return":Decimal(str(net)),"currency":i.quote_currency,"outcome":"winner" if net>0 else "loser" if net<0 else "breakeven"}

class FXAdapter:
 def instrument(self,raw):
  base,quote=raw["symbol"].split("/");return Instrument("FX","OTC",raw["symbol"].replace("/","_"),raw["symbol"],base,quote,Decimal("1"),Decimal("0.00001"),"FX_24X5")
 def timestamp(self,value):return datetime.fromisoformat(value.replace("Z","+00:00"))
 def net_return(self,raw,instrument):return Decimal(str(raw["net_return"]))

