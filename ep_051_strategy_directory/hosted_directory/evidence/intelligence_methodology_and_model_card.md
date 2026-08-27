# EP051 Intelligence Methodology and Model Card

Version: 1.0.0  
Decision role: investigation and allocation support; not personalised financial advice or automated execution.

## Canonical evidence

Strategy identity is normalized from direction-specific model IDs such as `DNA_102001_B` and `DNA_102001_S` to `DNA_102001`. Closed-trade evidence is sourced from `combined_trades_closed`; current positions remain a separate `combined_trades_open` view. Profit/loss is derived exclusively from signed `net_return`. `close_type='target reached'` is an exit description, not an outcome. Costs and commission are already included in `net_return` and are never deducted again.

Every hosted snapshot is content-addressed, bounded, immutable by snapshot ID, and reconciles directory aggregates, intelligence profiles and return series. Local caches carry a complete-envelope SHA-256 digest, schema version, generation timestamp and full curve/profile reconciliation.

## Metrics and scoring

Metrics are calculated server-side under methodology version `1.0.0`. Each metric carries a unit, source, evidence state and methodology version. The quality score is bounded from 0–100, exposes its component contributions, caps weak-evidence strategies, and makes rank eligibility explicit. Hard discovery constraints are applied before ranking; ineligible strategies never outrank eligible strategies in either sort direction.

Correlation aligns daily return observations and reports overlap/confidence. Similarity is a separate explainable feature-distance measure and is never represented as correlation. Period-sensitive comparisons disclose mismatched evidence windows.

## Regime model

The initial supported market is FX. Versioned daily reference-rate observations are sourced from the European Central Bank EXR feed. Only observations available at or before the evaluation timestamp are used. Derived features cover trend, realized volatility, volatility z-score, drawdown and cross-rate breadth. The deterministic classifier returns a state, probabilities, confidence, feature timestamp, source version and freshness state. Confidence is calibrated as next-observation direction persistence using chronological 80/20 calibration/holdout partitions and version `ecb-next-day-direction-2026-08-v1`; it is not a probability of profit. Stale, missing or future evidence fails closed to `UNKNOWN` and produces no recommendations.

Recommendations are candidates to investigate, not allocation commands. They apply hard evidence/risk constraints before regime suitability ranking and disclose positive evidence, counterevidence, sample size, uncertainty and methodology version. Immediate broker execution is intentionally outside this release.

## User intelligence and privacy

Public strategy evidence is never altered by private preferences. Hosted private objects are owner-scoped behind a trusted identity edge and PostgreSQL forced row-level security. Search plans—not executable free text—are stored. Interaction history is opt-in, expires after 90 days, and can be exported, reset or deleted. Cross-owner retention uses a distinct least-privilege maintenance role.

## Limitations and monitoring

Short evidence windows can produce unstable annualized values and receive collecting/low-confidence treatment. Regime fit is historical association, not causal proof. The service monitors latency, server errors, cache/feed freshness and model drift. Promotion requires metric, discovery, regime, security, operations, restore and browser-acceptance gates; any missing or failed gate blocks release. Versions are staged through shadow and canary modes and retain an immediate rollback target.
