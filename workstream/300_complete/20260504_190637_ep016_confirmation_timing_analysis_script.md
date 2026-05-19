# EP016: Confirmation Timing Analysis Script

**Task Type:** standard
**Task Summary:** Analyze the impact of confirmation delay on tradable outcomes - measuring how much runway remains after a turn is confirmed
**Dependency:** 20260504_190636_ep016_significant_moves_v2_analysis_script
**Data Mode:** Mixed - 88% LIVE, 16% SIM (1,046 total turns)

---

## Objective

Address a critical question for trading: **How much time remains to act after a turning point is confirmed?**

The turning point detection algorithm requires confirmation (5 pip move) before declaring a TOP or BOTTOM. This confirmation takes 5-15 minutes. If the outcome is measured at T+10 minutes from turn_time, but confirmation happened at T+10 minutes, there's **zero runway left to trade**.

This script quantifies:
1. How long confirmation typically takes (5, 10, or 15 minutes)
2. What success rates look like when measured from confirmation time
3. Whether T+15m outcomes are more realistic for trading than T+10m

---

## Background: The Confirmation Timing Problem

### Turn Detection Timeline
```
T-15m   T-10m   T-5m    T (turn)   T+5m    T+10m   T+15m
  |       |       |        |         |        |        |
  [----pre-window----]     ^    [--post-window--]
                           |
                    Turn Price Set
                           |
         Confirmation happens somewhere in post-window
         (when price moves 5 pips in expected direction)
```

### The Issue
- `outcome_10m_pips` = price at T+10m minus turn_price
- But you don't KNOW it's a turn until confirmation at T+5m, T+10m, or T+15m
- If confirmed at T+10m, the "10-minute outcome" has already occurred - no time to trade
- If confirmed at T+15m, the "10-minute outcome" is BEFORE confirmation - can't use it

### The Solution
Measure success rates at T+15m, which gives:
- Turns confirmed at T+5m: 10 minutes of runway
- Turns confirmed at T+10m: 5 minutes of runway
- Turns confirmed at T+15m: 0 minutes (just confirmed)

---

## Process Description

### Script Logic
1. Query `confirmation_delay_minutes` distribution by turn_type
2. Calculate remaining runway: `10 - confirmation_delay`
3. For each delay bucket, calculate:
   - Success rate at T+10m (may be before/during confirmation)
   - Success rate at T+15m (more realistic for trading)
4. Show average favourable move by delay bucket
5. Explain trading implications

### Key SQL Queries
```sql
-- Confirmation delay distribution
SELECT turn_type, confirmation_delay_minutes, COUNT(*)
FROM turning_points
GROUP BY turn_type, confirmation_delay_minutes

-- Success rates by confirmation delay
SELECT
    confirmation_delay_minutes,
    ROUND(100.0 * COUNT(*) FILTER (WHERE
        (turn_type = 'TOP' AND outcome_10m_pips < -5) OR
        (turn_type = 'BOTTOM' AND outcome_10m_pips > 5)
    ) / COUNT(*), 1) as success_gt5_10m,
    ROUND(100.0 * COUNT(*) FILTER (WHERE
        (turn_type = 'TOP' AND outcome_15m_pips < -5) OR
        (turn_type = 'BOTTOM' AND outcome_15m_pips > 5)
    ) / COUNT(*), 1) as success_gt5_15m
FROM turning_points
GROUP BY turn_type, confirmation_delay_minutes
```

---

## Plan
- [x] Create `check_confirmation_timing.py` in ep016 logic folder
- [x] Query confirmation_delay_minutes distribution
- [x] Calculate remaining runway after confirmation
- [x] Show success rates at T+10m and T+15m by delay bucket
- [x] Document trading implications in output
- [x] Run and verify output
- [x] Document results

---

## Evidence

**Script Location:** `epics/ep_016_turning_point_pattern_engine/logic/check_confirmation_timing.py`

**Execution Method:**
```bash
cd epics/ep_016_turning_point_pattern_engine/logic
cmd.exe /c "python check_confirmation_timing.py"
```

**Key Results:**

### Confirmation Delay Distribution
| Turn Type | Delay | Count | % of Type |
|-----------|-------|-------|-----------|
| BOTTOM | 5 min | 269 | 51% |
| BOTTOM | 10 min | 143 | 27% |
| BOTTOM | 15 min | 113 | 22% |
| TOP | 5 min | 257 | 49% |
| TOP | 10 min | 143 | 27% |
| TOP | 15 min | 126 | 24% |

### Success Rates by Confirmation Delay (>5 pip threshold)
| Confirmed At | Runway Left | @T+10m | @T+15m |
|--------------|-------------|--------|--------|
| T+5 min | 5 min | ~94% | ~99% |
| T+10 min | 0 min | ~90% | ~93% |
| T+15 min | -5 min (past) | 0% | ~85% |

### Trading Implications

1. **~50% of turns confirm quickly (T+5m)**: These have 5-10 minutes of runway remaining and show 94-99% success rates at the >5 pip threshold.

2. **~27% confirm at T+10m**: The 10-minute outcome is measured at the same time as confirmation - effectively zero runway, but 90% still show success.

3. **~23% confirm late (T+15m)**: The 10-minute outcome has already passed, making it useless for trading. Must use T+15m outcome (85% success).

4. **Recommendation**: For realistic trading metrics, use `outcome_15m_pips` which provides:
   - 10 min runway for fast confirmations
   - 5 min runway for medium confirmations
   - 0 min runway for slow confirmations (just-confirmed signal)

**Objective-Delivery-Coverage:** 100%
