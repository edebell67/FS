# EP016: Data Mode Check Script

**Task Type:** standard
**Task Summary:** Create script to verify whether turning point data comes from LIVE or SIM market mode
**Dependency:** None

---

## Objective

Before interpreting turning point success rates, we need to know whether the underlying data is from:
- **LIVE**: Real-time market price data from trading API
- **SIM**: Simulated/historical data for testing

This script queries the database to determine the data mode distribution for both snapshots and turning points.

---

## Background: Market Mode Tracking

The `frequency_snapshots` table includes a `market_mode` column that tracks whether each snapshot came from live market data or simulation. This allows:
1. Filtering analysis to only LIVE data for production metrics
2. Separating SIM results for backtesting validation
3. Understanding the composition of the current dataset

---

## Process Description

### Script Logic
1. Connect to pattern_engine database
2. Query `frequency_snapshots` grouped by `market_mode`
3. Join `turning_points` to `frequency_snapshots` via `turning_point_windows` to get mode per turn
4. Show date range of turning points
5. Output summary

### Key SQL Queries
```sql
-- Snapshot mode distribution
SELECT market_mode, COUNT(*)
FROM frequency_snapshots
GROUP BY market_mode

-- Turning points by underlying snapshot mode
SELECT fs.market_mode, COUNT(DISTINCT tp.turn_id) as turns
FROM turning_points tp
JOIN turning_point_windows tpw ON tpw.turn_id = tp.turn_id
JOIN frequency_snapshots fs ON fs.snapshot_id = tpw.snapshot_id
GROUP BY fs.market_mode
```

---

## Plan
- [x] Create `check_data_mode.py` in ep016 logic folder
- [x] Query frequency_snapshots by market_mode
- [x] Join to turning_points to get mode distribution of detected turns
- [x] Show date range of data
- [x] Run and verify output
- [x] Document results

---

## Evidence

**Script Location:** `epics/ep_016_turning_point_pattern_engine/logic/check_data_mode.py`

**Execution Method:**
```bash
cd epics/ep_016_turning_point_pattern_engine/logic
cmd.exe /c "python check_data_mode.py"
```

**Key Results:**

### Frequency Snapshots by Mode
| Mode | Count |
|------|-------|
| LIVE | 8,153 |
| SIM | 13,322 |
| NULL | 4,150 |

### Turning Points by Snapshot Mode
| Mode | Count | % of Total |
|------|-------|------------|
| LIVE | 930 | **88%** |
| SIM | 174 | 16% |

### Data Date Range
- From: 2026-05-03 17:25:00
- To: 2026-05-04 19:00:00
- Total turns: 1,061

**Key Finding:** 88% of detected turning points are from **LIVE market data**, making the success rate statistics representative of real market conditions.

**Objective-Delivery-Coverage:** 100%
