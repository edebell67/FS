# WF-201 Independent Reconciliation

- Source closed count equals calculated `total_trades` after excluding open records.
- Source `sum(net_return)` equals snapshot `total_net_return` at 8-decimal precision.
- Outcome counts equal sign partitions of `net_return` and sum to total trades.
- Commission fields do not participate in arithmetic because source `net_return` is already net.
- Maximum drawdown was independently walked over the ordered additive P&L curve.
- Percentage drawdown remains null without starting equity.
- Snapshot key includes strategy, methodology version and calculation timestamp.

Result: PASS; 8 focused tests, 0 failures.

