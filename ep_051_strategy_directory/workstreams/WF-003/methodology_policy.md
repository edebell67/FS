# Methodology Policy - EP051 DNA Strategy Directory

## Methodology Versioning
- **Current Version**: `v1.0.0`
- **Policy**: Any change to analytics formulas, regime boundary thresholds, or metric calculations requires a new methodology version. 
- **Traceability**: All calculated analytics (`dna_strategy_stats`, `dna_strategy_period_stats`, `dna_strategy_regime_stats`) must store the `methodology_version` used during generation.
- **Rollout**: New versions are calculated alongside old ones for reconciliation before the serving layer switches versions atomically.

## Sample Sufficiency
- **Minimum History**: A strategy must have at least 30 valid closed trades to display full analytics.
- **Regime Confidence**: For regime-specific stats, at least 15 trades must have occurred during the specified regime state for the confidence level to be considered "Sufficient".
- **Handling Insufficient Data**: The UI and APIs must explicitly flag the dataset as "Insufficient Data" rather than omitting it or presenting statistically insignificant values.

## Change Process
1. Propose change via a Pull Request containing new formula/tests.
2. Run comparative backtest generation using the golden dataset to document impact.
3. Approve new methodology version (e.g. `v1.1.0`).
4. Re-calculate the data warehouse and switch serving snapshot.
