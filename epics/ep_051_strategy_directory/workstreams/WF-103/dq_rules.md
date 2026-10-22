# WF-103 Data-Quality and Reconciliation Rules

Publishing is fail-closed. A batch may publish only when every blocking rule passes.

| Rule | Gate | Acceptance |
|---|---|---|
| Source/canonical accepted count | Blocking | Exact equality after documented quarantine exclusions |
| Closed-trade net return | Blocking | Absolute difference ≤ `0.00000001` in the same currency/basis |
| Duplicate closed `guid` | Blocking | Zero |
| Required identity/signal/timestamps/result | Blocking | 100% present in canonical accepted rows |
| Exit ordering | Blocking | `exit_at >= created_at` for every closed row |
| Numeric validity | Blocking | All reported decimals finite |
| Currency/basis completeness | Blocking | 100% before monetary aggregation |
| Schema drift | Blocking | No missing/changed required columns; additive optional fields reviewed |
| Closed-source freshness | Warning then blocking | Warning after 15m, blocking after 60m unless scheduled maintenance |
| Open-source freshness | Warning then blocking | Warning after 2m, blocking after 10m unless market/session policy says closed |
| Backfill equivalence | Blocking | Same canonical count, totals, IDs and checksums as incremental processing |

Alerts include run ID, source, rule ID, expected/observed values, severity, and replay/backfill instructions. They never include credentials or unrestricted payloads.

