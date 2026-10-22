"""Synthetic equity-index futures pilot calculations. Version 1.0.0 (2026-08-23)."""
from decimal import Decimal

SPEC={"market":"FUTURES","venue":"PILOT_CME_STYLE","instrument_id":"EQIDX-202612","currency":"USD","tick_size":Decimal("0.25"),"tick_value":Decimal("12.50"),"multiplier":Decimal("50"),"calendar":"PILOT_EQUITY_SESSION","illustrative":True}
def reconcile_trade(*,entry,exit,contracts,commission,fees):
 values=[Decimal(str(x)) for x in (entry,exit,contracts,commission,fees)]
 entry,exit,contracts,commission,fees=values
 if contracts<=0 or any(v<0 for v in (commission,fees)):raise ValueError("invalid size or costs")
 price_change=exit-entry;gross=price_change*SPEC["multiplier"]*contracts;net=gross-commission-fees
 ticks=price_change/SPEC["tick_size"]
 if ticks != ticks.to_integral_value():raise ValueError("off-tick price")
 return {"gross":gross,"commission":commission,"fees":fees,"net_return":net,"ticks":ticks,"costs_included":True,"currency":SPEC["currency"]}
def roll(old_contract,new_contract,*,effective_at,adjustment):return {"old":old_contract,"new":new_contract,"effective_at":effective_at,"back_adjustment":Decimal(str(adjustment)),"version":"1.0.0"}

