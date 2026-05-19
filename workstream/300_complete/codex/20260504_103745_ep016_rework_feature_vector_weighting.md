# Task: Rework EP016 Feature Vector Weighting

**Task Type:** standard
**Created:** 2026-05-04 10:37
**Epic:** ep_016_turning_point_pattern_engine

---

## Task Summary

Rework the pattern engine's 306-dimensional feature vector to prioritize features that actually correlate with profitable outcomes. Current similarity matching produces ~25% hit rate regardless of confidence level, with similarity score negatively correlated (r = -0.13) to outcome.

---

## Problem Statement

### Investigation Findings (2026-05-04)

**Predictive Accuracy of Live Engine:**
| Confidence | UP bias | DOWN bias |
|------------|---------|-----------|
| HIGH | 30.6% | 21.2% |
| MEDIUM_HIGH | 22.6% | 25.3% |
| MEDIUM | 24.7% | 24.2% |

Confidence level provides no edge — all hover around 25%.

**Feature Correlation Analysis (n=165 LIVE turns):**

| Feature | Correlation with Profitable Outcome |
|---------|-------------------------------------|
| `reversal_strength` | **+0.84** |
| `pattern_quality` | **+0.84** |
| `cluster_width` | **+0.65** |
| `magnet_shift_post` | +0.44 |
| `cluster_skew` | +0.44 |
| `peak_relative_pips` | +0.41 |
| `peak_frequency` | **-0.41** |
| `failed_probe_pips` | +0.29 |

**Critical Finding:**
```
Similarity score vs profitable outcome: r = -0.13 (NEGATIVE)
```

Higher similarity to historical patterns correlates with WORSE outcomes.

### Root Cause

The 306-dimensional vector structure:
- 294 dimensions: normalized frequency matrix (21 pip levels × 7 time indices × 2 sides)
- 12 dimensions: engineered features

Cosine similarity is dominated by the frequency matrix. The features that actually predict outcomes (`reversal_strength`, `cluster_width`) are drowned out.

---

## Dependency

None

---

## Plan

- [ ] **1. Create new vector model version** (`V3_WEIGHTED_FEATURES`)
  - Test: New version string exists in code

- [ ] **2. Restructure vector composition** — Option A: Weighted hybrid
  - Reduce frequency matrix weight (scale by 0.1-0.3)
  - Amplify predictive features (scale by 2-5x):
    - `reversal_strength`
    - `pattern_quality`
    - `cluster_width`
    - `magnet_shift_post`
    - `cluster_skew`
  - Test: Vector still 306D but weights redistributed

- [ ] **3. Alternative: Feature-only vector** — Option B
  - Drop frequency matrix entirely
  - Use only 12-20 engineered features
  - Test: Smaller vector (~20D), faster similarity

- [ ] **4. Regenerate historical pattern vectors**
  - Reprocess all `turning_points` with new model
  - Test: All `pattern_vectors` rows have new version

- [ ] **5. Regenerate library profiles**
  - Rebuild `pattern_library_profiles` with new vectors
  - Test: Profiles exist for new model version

- [ ] **6. Update live similarity engine**
  - Use new vector model for live comparisons
  - Test: `live_pattern_vectors` created with new version

- [ ] **7. Validate predictive improvement**
  - Run for 24-48 hours on LIVE data
  - Measure: Correlation of similarity score to outcome
  - Target: r > +0.20 (currently -0.13)
  - Measure: HIGH confidence hit rate
  - Target: >40% (currently ~25%)

- [ ] **8. Update confidence classification**
  - Adjust thresholds in `classify_confidence()` based on new similarity distribution
  - Test: Confidence labels meaningfully stratify outcomes

---

## Evidence

**Baseline Metrics (pre-fix):**
- LIVE snapshots: 4,356
- LIVE turns: 380 (194 BOTTOM, 186 TOP)
- Similarity-outcome correlation: r = -0.13
- HIGH confidence hit rate: ~25%

**Files to Modify:**
- `epics/ep_016_turning_point_pattern_engine/logic/feature_processor.py`
- `epics/ep_016_turning_point_pattern_engine/logic/live_similarity_engine.py`

**Objective-Delivery-Coverage:** 0%

---

## Notes

- Consider A/B testing V2 vs V3 vectors in parallel before full cutover
- May need to retrain cross-product relationship engine after vector change
- Document feature importance findings in `docs/` for future reference
