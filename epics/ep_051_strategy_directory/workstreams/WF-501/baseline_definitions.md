# WF-501 Baseline Portfolio Definitions

## Version history

- 1.0.0 (2026-08-23): Initial reproducible baselines.

All baselines use the same eligible universe, as-of timestamp, governed closed-trade snapshot, portfolio currency, capital denominator, cost basis and constraint set as the candidate optimizer run.

| Baseline | Allocation | Purpose |
|---|---|---|
| Equal weight | `1 / eligible_count` after hard constraints | Transparent reference; fails if caps make equal weight infeasible. |
| Equal risk contribution | Iterative weights targeting equal ex-ante volatility contribution | Tests whether sophisticated selection adds value beyond risk balancing. |
| Cluster balanced | Equal capital per relationship cluster, then equal within cluster | Tests diversification across observed behavior groups. |
| Simple quality selection | Highest governed quality tier, then longest closed-trade history; equal weight | Transparent non-return-ranked selection reference. |

Each baseline output records canonical IDs, weights, capital amounts, sizing policy, denominator, currency conversion snapshot, relationship/method versions, random seed (even when unused), exclusions and feasibility result. Baselines do not use future observations, open-trade outcomes, descriptive names as identifiers, or Non-DNA production candidates.

