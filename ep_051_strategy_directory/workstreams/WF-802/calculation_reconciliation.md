# WF-802 Calculation Reconciliation

## Version history

- 1.0.0 (2026-08-23): Initial reconciliation.

One tick × one contract reconciles to USD 12.50 gross. Four contracts reconcile to USD 50.00. Commission and fees are subtracted exactly once to produce canonical monetary `net_return`; outcome derives from its sign. Off-tick prices reject. Roll records preserve old/new contracts, effective time, adjustment and version. Seven automated tests pass.

