# WF-503 Portfolio Validation Report

## Version history

- 1.0.0 (2026-08-23): Initial promotion-gate evidence.

Decision candidate: PROMOTE to portfolio-builder integration, not to live capital.

The reference run uses an expanding-window design: universe and relationships are frozen at each training cutoff, optimization occurs only on training observations, and the next non-overlapping period is holdout. Delisted, quarantined and inactive strategies remain in historical universes where they were known, preventing survivorship filtering. Regime results cover risk-on and risk-off states; sparse states retain sample warnings. Results are compared with equal-weight and simple-quality-selection baselines on identical snapshots and cost basis.

Risks remain: limited history, regime misclassification, correlated tail losses, parameter instability and model-selection bias. Sensitivities vary weight/cluster caps, training length and relationship method. Promotion is blocked automatically by temporal overlap, future-dated universes, missing regimes/baselines/risks/sensitivity evidence.

