# Data Contract - EP051 DNA Strategy Directory

## 1. Identity Normalization
- **Rule**: Strip `_S` and `_B` suffixes from strategy IDs. 
- **Examples**: `DNA_102001_S` -> `DNA_102001`, `DNA_102001_B` -> `DNA_102001`.
- **Validation**: Must be deterministic, case-insensitive on input, uppercase output, whitespace-trimmed.
- **Regex**: `^DNA_\d+$` (after suffix stripping).
- **Collision Handling**: Invalid identifiers are quarantined. The original suffix is preserved for lineage/reconciliation but not as part of the directory key.

## 2. Trade Sources and Schemas
- **Closed Trades (`combined_trades_closed`)**: Source of truth for historical analytics. Uniquely identified by `guid`. Idempotent ingestion required.
- **Open Trades (`combined_trades_open`)**: Source for current/open state only. Not mixed into historical aggregates.

## 3. Exit-Time, Currencies, and Cost Semantics
- **Exit-Time Precedence**: Defined as `COALESCE(g_close_time, last_update)`.
- **Costs**: Commission/costs are already incorporated in `net_return`. Will not be double-counted.
- **Outcome**: Derived strictly from `net_return` (positive = winner, negative = loser, zero = breakeven). `close_type = 'target reached'` is descriptive, not an outcome classification.
- **Currencies**: All monetary values require explicit currency/basis. Aggregation of unlike currencies is forbidden without FX conversion timestamp.

## 4. Non-DNA Isolation
- Non-DNA records are strictly isolated. They are for research, validation, and benchmarking only.
- Never commingle Non-DNA records with public DNA metrics.
