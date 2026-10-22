# WF-802 Futures Pilot Report

## Version history

- 1.0.0 (2026-08-23): Initial synthetic pilot.

Selected pilot: a synthetic, liquid CME-style equity-index future fixture. It is deliberately illustrative—not a claim about a current exchange listing—and validates the framework without external market-data dependencies. Reference data defines venue, contract, USD settlement, 0.25 tick, 12.50 tick value, 50 multiplier, session calendar, expiry/roll version and disclosures.

The feed contract requires unique trade/contract IDs, aware UTC exchange/receive timestamps, side, entry/exit, contracts, prices, commission/fees and source version. Quality gates cover duplicate/gap/out-of-session/off-tick/unknown contract/late correction. Regime analysis uses governed session returns and sufficient samples; position sizing uses capital/margin denominators and never treats notional as loss. Private beta follows WF-703 comprehension and security gates.

