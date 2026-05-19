# EP016: Significant Moves Analysis Script (V2 - Corrected)

**Task Type:** standard
**Task Summary:** Corrected script with proper threshold logic for measuring tradable pip moves after turning point detection
**Dependency:** 20260504_190635_ep016_significant_moves_analysis_script
**Data Mode:** Mixed - 88% LIVE, 16% SIM (1,046 total turns)

---

## Objective

Provide accurate statistics on what percentage of detected turning points led to **meaningful, tradable price movements** using correct comparison operators:
- **TOP success**: `outcome_10m_pips < -5` (price fell MORE than 5 pips, i.e., -6, -10, -50)
- **BOTTOM success**: `outcome_10m_pips > 5` (price rose MORE than 5 pips, i.e., +6, +10, +50)

---

## Background: The V1 Bug

The initial script (`check_significant_moves.py`) had incorrect threshold logic using dynamic string formatting that produced wrong comparisons. V2 uses explicit, hardcoded SQL to ensure correctness.

---

## Process Description

### Script Structure
1. **TOP Analysis Section**:
   - Query all TOPs with 10-minute outcomes
   - Count: fell any amount, fell >5 pips, fell >10 pips, fell >20 pips
   - Count failures: rose any amount, rose >5 pips
   - Calculate average 10m move

2. **BOTTOM Analysis Section**:
   - Query all BOTTOMs with 10-minute outcomes
   - Count: rose any amount, rose >5 pips, rose >10 pips, rose >20 pips
   - Count failures: fell any amount, fell >5 pips
   - Calculate average 10m move

3. **Combined Summary**:
   - Aggregate stats across both turn types

4. **Outcome Distribution**:
   - Bucket outcomes into ranges with SUCCESS/FAIL labels
   - E.g., "Fell >50 pips (SUCCESS)", "Rose 0-5 pips (FAIL)"

### Key SQL Queries
```sql
-- TOP section
SELECT
    COUNT(*) FILTER (WHERE outcome_10m_pips < 0) as fell_any,
    COUNT(*) FILTER (WHERE outcome_10m_pips < -5) as fell_gt5,
    COUNT(*) FILTER (WHERE outcome_10m_pips < -10) as fell_gt10,
    COUNT(*) FILTER (WHERE outcome_10m_pips < -20) as fell_gt20,
    COUNT(*) FILTER (WHERE outcome_10m_pips > 0) as rose_wrong,
    COUNT(*) FILTER (WHERE outcome_10m_pips > 5) as rose_gt5_wrong
FROM turning_points WHERE turn_type = 'TOP'

-- Distribution buckets
CASE
    WHEN outcome_10m_pips < -50 THEN 'Fell >50 pips (SUCCESS)'
    WHEN outcome_10m_pips < -20 THEN 'Fell 20-50 pips (SUCCESS)'
    ...
END as bucket
```

---

## Plan
- [x] Create `check_significant_moves_v2.py` in ep016 logic folder
- [x] Use explicit SQL with correct operators (< for TOP fell, > for BOTTOM rose)
- [x] Separate SUCCESS and FAILURE sections clearly
- [x] Add outcome distribution with labeled buckets
- [x] Run and verify output matches expected logic
- [x] Document results

---

## Evidence

**Script Location:** `epics/ep_016_turning_point_pattern_engine/logic/check_significant_moves_v2.py`

**Execution Method:**
```bash
cd epics/ep_016_turning_point_pattern_engine/logic
cmd.exe /c "python check_significant_moves_v2.py"
```

**Key Results (10-minute horizon):**

### TOP Detection - Price Should Fall
| Threshold | Count | Success Rate |
|-----------|-------|--------------|
| Fell ANY amount | 496/521 | 95.2% |
| Fell > 5 pips | 361/521 | **69.3%** |
| Fell >10 pips | 222/521 | 42.6% |
| Fell >20 pips | 156/521 | 29.9% |
| Rose (WRONG) | 0/521 | 0.0% |

### BOTTOM Detection - Price Should Rise
| Threshold | Count | Success Rate |
|-----------|-------|--------------|
| Rose ANY amount | 514/525 | 97.9% |
| Rose > 5 pips | 388/525 | **73.9%** |
| Rose >10 pips | 268/525 | 51.0% |
| Rose >20 pips | 187/525 | 35.6% |
| Fell (WRONG) | 0/525 | 0.0% |

### Combined (All 1,046 Turns)
| Threshold | Success Rate |
|-----------|--------------|
| Correct direction (any) | 96.6% |
| **Correct > 5 pips** | **71.6%** |
| Correct >10 pips | 46.8% |

### Outcome Distribution (10-min)
**TOP:**
- Fell >50 pips: 139
- Fell 20-50 pips: 17
- Fell 10-20 pips: 66
- Fell 5-10 pips: 139
- Fell 0-5 pips (marginal): 135
- No change: 25

**BOTTOM:**
- Rose >50 pips: 147
- Rose 20-50 pips: 40
- Rose 10-20 pips: 81
- Rose 5-10 pips: 120
- Rose 0-5 pips (marginal): 126
- No change: 11

**Key Insight:** 71.6% of all detected turns moved >5 pips in the expected direction within 10 minutes. Notably, **0% moved in the wrong direction** - failures were only marginal moves or no change.

**Objective-Delivery-Coverage:** 100%
