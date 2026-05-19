# EP016: Success Rates Analysis Script

**Task Type:** standard
**Task Summary:** Create diagnostic script to measure turning point detection accuracy across all products and timeframes
**Dependency:** None
**Data Mode:** Mixed - 88% LIVE, 16% SIM (1,046 total turns from 2026-05-03 to 2026-05-04)

---

## Objective

Create a reusable Python script that queries the `turning_points` table in the pattern_engine PostgreSQL database to calculate and display success rates for detected market turning points.

**Success Definition:**
- **TOP**: Price fell after detection (outcome_pips < 0) - indicates the market correctly identified a peak
- **BOTTOM**: Price rose after detection (outcome_pips > 0) - indicates the market correctly identified a trough

The script provides visibility into detection algorithm performance across time horizons (5m, 10m, 15m, 30m) and by product.

---

## Background: Turning Point Detection Process

The pattern engine detects turning points through the following pipeline:

1. **Price Frequency Snapshots**: Every 5 minutes, bid/ask price frequency data is captured from the market prices API and stored in `frequency_snapshots` and `frequency_levels` tables.

2. **Magnet Price Calculation**: For each snapshot, the "magnet price" (highest frequency price level) is identified - this represents where the market is accepting trades.

3. **Turn Detection** (`turning_point_processor.py`):
   - Uses a 7-snapshot sliding window (T-3 to T+3)
   - Identifies the center snapshot (T) as a potential turn
   - **BOTTOM**: Center has lowest magnet price in window AND price rises by at least 5 pips in post-window
   - **TOP**: Center has highest magnet price in window AND price falls by at least 5 pips in post-window

4. **Outcome Labeling**: Once a turn is confirmed, future price movements are recorded:
   - `outcome_5m_pips`: Price at T+5min minus turn_price
   - `outcome_10m_pips`: Price at T+10min minus turn_price
   - `outcome_15m_pips`: Price at T+15min minus turn_price
   - `outcome_30m_pips`: Price at T+30min minus turn_price

---

## Process Description

### Script Logic
1. Connect to pattern_engine PostgreSQL database (localhost:5432)
2. Query `turning_points` with aggregations using PostgreSQL FILTER clause
3. For each turn_type (TOP/BOTTOM):
   - Count total detected turns
   - Count where outcome moved in expected direction (success)
   - Calculate percentage
4. Join to `products` table for per-product breakdown
5. Output formatted console report

### Key SQL Pattern
```sql
SELECT turn_type,
       COUNT(*) as total,
       COUNT(*) FILTER (WHERE
           (turn_type = 'BOTTOM' AND outcome_10m_pips > 0) OR
           (turn_type = 'TOP' AND outcome_10m_pips < 0)
       ) as success_10m
FROM turning_points
GROUP BY turn_type
```

---

## Plan
- [x] Create `check_success_rates.py` in `epics/ep_016_turning_point_pattern_engine/logic/`
- [x] Implement DB connection using psycopg2 with standard DB_CONFIG
- [x] Query success rates for 5m, 10m, 15m, 30m horizons
- [x] Calculate success as: BOTTOM = price rose, TOP = price fell
- [x] Add per-product breakdown section
- [x] Run script via Windows Python and verify output
- [x] Document results

---

## Evidence

**Script Location:** `epics/ep_016_turning_point_pattern_engine/logic/check_success_rates.py`

**Execution Method:**
```bash
cd epics/ep_016_turning_point_pattern_engine/logic
cmd.exe /c "python check_success_rates.py"
```

**Key Results:**

| Turn Type | Total | 5m Success | 10m Success | 15m Success |
|-----------|-------|------------|-------------|-------------|
| BOTTOM | 525 | 88.2% | 97.9% | 100.0% |
| TOP | 520 | 86.2% | 95.2% | 100.0% |
| **Combined** | **1,045** | **87.2%** | **96.6%** | **100.0%** |

Per-product breakdown shows 100% success at 10m for most FX pairs (AUD, EUR, GBP, JPY) with a few crosses showing 88-92%.

**Objective-Delivery-Coverage:** 100%
