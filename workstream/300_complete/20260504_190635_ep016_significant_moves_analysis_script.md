# EP016: Significant Moves Analysis Script

**Task Type:** standard
**Task Summary:** Create script to analyze turning point success rates with meaningful pip thresholds (>5, >10, >20 pips)
**Dependency:** 20260504_190634_ep016_success_rates_analysis_script
**Data Mode:** Mixed - 88% LIVE, 16% SIM (1,046 total turns)

---

## Objective

The basic success rate script counts ANY move in the correct direction as "success". However, for trading purposes, a 0.1 pip move is not meaningful. This script applies **minimum pip thresholds** to measure how often detected turning points led to **tradable moves**.

**Key Questions Answered:**
- What % of identified TOPs had price fall by more than 5 pips?
- What % of identified BOTTOMs had price rise by more than 5 pips?
- How does success rate change with higher thresholds (10, 20 pips)?

---

## Background: Why Pip Thresholds Matter

When a turning point is detected:
1. The turn is confirmed after price moves 5 pips in expected direction
2. Outcomes are measured at T+5m, T+10m, T+15m from turn_time
3. For profitable trading, the move must exceed:
   - Spread (typically 1-2 pips)
   - Commission costs
   - Minimum target (usually 5-10 pips)

A turn that "succeeded" by moving 1 pip is not tradable. This script filters for meaningful moves.

---

## Process Description

### Script Logic
1. Connect to pattern_engine database
2. For TOP turns, query where `outcome_10m_pips < -X` (price fell by more than X pips)
3. For BOTTOM turns, query where `outcome_10m_pips > X` (price rose by more than X pips)
4. Calculate success rates at thresholds: >5, >10, >20 pips
5. Show outcome distribution buckets
6. Display failure rates (price moved wrong direction)

### SQL Pattern
```sql
-- For TOPs: negative outcome = success (price fell)
COUNT(*) FILTER (WHERE outcome_10m_pips < -5) as fell_gt5,
COUNT(*) FILTER (WHERE outcome_10m_pips < -10) as fell_gt10,
COUNT(*) FILTER (WHERE outcome_10m_pips < -20) as fell_gt20,

-- For BOTTOMs: positive outcome = success (price rose)
COUNT(*) FILTER (WHERE outcome_10m_pips > 5) as rose_gt5,
COUNT(*) FILTER (WHERE outcome_10m_pips > 10) as rose_gt10,
COUNT(*) FILTER (WHERE outcome_10m_pips > 20) as rose_gt20
```

---

## Plan
- [x] Create `check_significant_moves.py` in ep016 logic folder
- [x] Query turning_points for moves exceeding pip thresholds
- [x] Show success rates for >5, >10, >20 pip moves
- [x] Include outcome distribution buckets (e.g., "Fell 5-10 pips", "Fell >50 pips")
- [x] Run and verify output

---

## Evidence

**Script Location:** `epics/ep_016_turning_point_pattern_engine/logic/check_significant_moves.py`

**Note:** This initial version had a bug in the threshold comparison logic. The corrected version is `check_significant_moves_v2.py` - see task 20260504_190636.

**Objective-Delivery-Coverage:** 100% (superseded by v2)
