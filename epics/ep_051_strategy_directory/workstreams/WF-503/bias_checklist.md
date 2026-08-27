# WF-503 Bias Checklist

## Version history

- 1.0.0 (2026-08-23): Initial checklist.

- [x] Training and holdout timestamps do not overlap.
- [x] Eligibility and universe membership are reconstructed as-of each cutoff.
- [x] Quarantined/inactive historical strategies are not silently removed.
- [x] Costs are already represented in canonical net returns and are not double counted.
- [x] Open positions are excluded from closed-outcome validation.
- [x] Relationship/regime inputs are versioned and cutoff-safe.
- [x] Equal-weight and simple-selection baselines share identical inputs.
- [x] Sparse samples, multiple testing, parameter sensitivity and tail concentration are disclosed.

