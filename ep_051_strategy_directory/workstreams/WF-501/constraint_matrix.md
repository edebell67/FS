# WF-501 Constraint Matrix

## Version history

- 1.0.0 (2026-08-23): Initial constraint and feasibility rules.

| Rule | Type | Denominator / basis | Feasibility test | User-facing failure |
|---|---|---|---|---|
| Capital > 0 | Hard | Portfolio currency cash amount | amount > 0 | Capital must be positive. |
| Strategy count | Hard | Count of eligible canonical DNA IDs | min ≤ count ≤ max | Only N eligible strategies remain; reduce the minimum or relax named eligibility rules. |
| Strategy weight | Hard | Allocated capital / total allocated capital | each weight ≤ cap | The requested count and weight cap cannot sum to 100%. |
| Cluster concentration | Hard | Cluster allocation / total allocated capital | cluster sum ≤ cap | Cluster cap is infeasible for the eligible cluster mix. |
| Market concentration | Hard | Market allocation / total allocated capital | market sum ≤ cap | Market cap is infeasible for the eligible market mix. |
| Margin | Hard | Stressed margin / net liquidation value | stressed fraction ≤ cap | Stressed margin exceeds the configured capital denominator. |
| Closed history | Hard | Canonical closed trades only | sample ≥ threshold | Insufficient closed-trade evidence. Open trades are not substituted. |
| Quality | Hard | Latest governed snapshot | state in allowed set | Strategy excluded by data-quality state. |
| Diversification | Objective | Aligned closed-return series and relationship version | minimise expected shortfall subject to constraints | No “highest return” shortcut is permitted. |

Every percentage must carry a numerator, denominator, unit, time/evidence basis and calculation version. Costs and commission are already included in `net_return` and must not be deducted again. `close_type='target reached'` is not an outcome label; profit/loss is derived from the sign of `net_return`.

## Feasibility response contract

An infeasible request returns `feasible=false`, a stable reason code, the violated rule, observed and required values with units/denominators, affected canonical strategy IDs, and the smallest safe relaxation. It never silently drops a hard constraint.

