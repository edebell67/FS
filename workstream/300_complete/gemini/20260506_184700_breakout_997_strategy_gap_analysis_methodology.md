# Strategy Gap Analysis Methodology

## Source
- Ad-hoc analysis session 2026-05-06

## Task Type
standard

## Task Attributes
- `recurring_task: false`
- `workflow_task: false`

## Task Summary
Document the methodology for analyzing strategy performance gaps over time, comparing leader separation at specific time cutoffs (e.g., 3am, 4am, 5am) versus end-of-day (EOD) values. This analysis identifies top-performing strategies by `buy_net`, `sell_net`, and `net` metrics, tracks gap progression between ranked strategies, and compares day-over-day patterns.

## Context
- **Data Source**: `TradeApps/breakout/fs/json/live/forex/{date}/_summary_net.json`
- **File Size**: ~31MB per day (large JSON files)
- **Structure**: Nested JSON with strategies, currency pairs, and time-series records

## Destination Folder
epics/ep_breakout_analysis/

## Dependency
None

---

## Data Structure

```json
{
  "last_update": "2026-05-06T00:14:11.144022",
  "session_max_net": 0.0,
  "strategies": {
    "<strategy_name>": {
      "<currency_pair>": [
        {
          "t": "<timestamp>",
          "net": <net_pnl>,
          "buy_net": <buy_pnl>,
          "sell_net": <sell_pnl>,
          "buy_alt": <alt_buy>,
          "sell_alt": <alt_sell>,
          "live_buy": <live_buy_value>,
          "live_sell": <live_sell_value>,
          "b_c": <buy_count>,
          "s_c": <sell_count>,
          "buyPercent": <pct>,
          "sellPercent": <pct>
        }
      ]
    }
  }
}
```

---

## Analysis 1: Top N Strategies by Metric at Time Cutoff vs EOD

### Purpose
Identify top N strategies by a specific metric (`buy_net`, `sell_net`, or `net`) at a given time cutoff, then compare to EOD values.

### Python Implementation

```python
import json
from datetime import datetime

# Load data
with open("/path/to/forex/{date}/_summary_net.json", "r") as f:
    data = json.load(f)

cutoff = datetime.fromisoformat("2026-05-05T05:00:00")  # Adjust time as needed
metric = "net"  # or "buy_net" or "sell_net"

results = []

for strategy, pairs in data.get("strategies", {}).items():
    for pair, records in pairs.items():
        best_rec = None
        for rec in records:
            t = datetime.fromisoformat(rec["t"])
            if t <= cutoff:
                if best_rec is None or rec[metric] > best_rec[metric]:
                    best_rec = rec

        if best_rec:
            results.append({
                "strategy": strategy,
                "pair": pair,
                f"{metric}_cutoff": best_rec[metric],
                "net_cutoff": best_rec["net"],
                "buy_net_cutoff": best_rec["buy_net"],
                "sell_net_cutoff": best_rec["sell_net"],
                "rec_cutoff": best_rec,
                "eod": records[-1] if records else None
            })

# Sort and get top N
top_n = sorted(results, key=lambda x: x[f"{metric}_cutoff"], reverse=True)[:5]

# Output
for r in top_n:
    eod = r["eod"]
    print(f"{r['strategy']} | {r['pair']}")
    print(f"  Cutoff: buy_net={r['buy_net_cutoff']:.1f}  sell_net={r['sell_net_cutoff']:.1f}  net={r['net_cutoff']:.1f}")
    print(f"  EOD:    buy_net={eod['buy_net']:.1f}  sell_net={eod['sell_net']:.1f}  net={eod['net']:.1f}")
    print(f"  Change: buy_net={eod['buy_net']-r['buy_net_cutoff']:+.1f}  sell_net={eod['sell_net']-r['sell_net_cutoff']:+.1f}  net={eod['net']-r['net_cutoff']:+.1f}")
    print()
```

### Output Table Format

```
| Strategy | Pair | {metric} cutoff | {metric} EOD | Change | net cutoff | net EOD |
|----------|------|----------------:|-------------:|-------:|-----------:|--------:|
| `strategy_name` | PAIR_C | 360.0 | **640.0** | +280.0 | 360.0 | 640.0 |
```

### Full Breakdown Format

```
| Strategy | Pair | | buy_net | sell_net | net |
|----------|------|---|--------:|---------:|----:|
| `strategy_name` | PAIR_C | cutoff | 0.0 | 360.0 | 360.0 |
| | | EOD | 540.0 | 100.0 | 640.0 |
| | | Chg | **+540.0** | -260.0 | +280.0 |
```

---

## Analysis 2: Gap Progression Between Top Strategies Over Time

### Purpose
Track the gap (difference in net) between #1 and #2 (and optionally #3) ranked strategies throughout the trading day to identify breakaway points.

### Python Implementation

```python
import json
from datetime import datetime

with open("/path/to/forex/{date}/_summary_net.json", "r") as f:
    data = json.load(f)

# Collect all records with timestamps
all_records = []
for strategy, pairs in data.get("strategies", {}).items():
    for pair, records in pairs.items():
        for rec in records:
            all_records.append({
                "strategy": strategy,
                "pair": pair,
                "t": datetime.fromisoformat(rec["t"]),
                "net": rec["net"],
                "buy_net": rec["buy_net"],
                "sell_net": rec["sell_net"]
            })

timestamps = sorted(set(r["t"] for r in all_records))

def get_top_n_at_time(cutoff, n=3):
    """Get best net record for each strategy/pair up to cutoff, return top n."""
    best_by_strat = {}
    for r in all_records:
        if r["t"] <= cutoff:
            key = (r["strategy"], r["pair"])
            if key not in best_by_strat or r["net"] > best_by_strat[key]["net"]:
                best_by_strat[key] = r

    sorted_strats = sorted(best_by_strat.values(), key=lambda x: x["net"], reverse=True)
    return sorted_strats[:n]

# Track gaps over time
gaps = []
for t in timestamps:
    top3 = get_top_n_at_time(t, 3)
    if len(top3) >= 2:
        gap_1_2 = top3[0]["net"] - top3[1]["net"]
        gap_1_3 = top3[0]["net"] - top3[2]["net"] if len(top3) >= 3 else None
        gaps.append({
            "t": t,
            "gap_1_2": gap_1_2,
            "gap_1_3": gap_1_3,
            "first": top3[0],
            "second": top3[1],
            "third": top3[2] if len(top3) >= 3 else None
        })

# Find largest gap before specific time (e.g., 10am)
early_gaps = [g for g in gaps if g["t"].hour < 10]
if early_gaps:
    max_gap = max(early_gaps, key=lambda x: x["gap_1_2"])
    print(f"Largest gap before 10am: {max_gap['gap_1_2']:.1f} at {max_gap['t']}")
    print(f"#1: {max_gap['first']['strategy']} | {max_gap['first']['pair']} | net: {max_gap['first']['net']:.1f}")
    print(f"#2: {max_gap['second']['strategy']} | {max_gap['second']['pair']} | net: {max_gap['second']['net']:.1f}")

# Hourly progression output
seen_hours = set()
for g in gaps:
    hour_key = (g["t"].date(), g["t"].hour)
    if hour_key not in seen_hours:
        seen_hours.add(hour_key)
        print(f"{g['t']} | Gap 1-2: {g['gap_1_2']:.1f} | Gap 1-3: {g['gap_1_3']:.1f} | #1 net: {g['first']['net']:.1f}")
```

### Output Table Format: Gap Progression

```
| Time | Gap 1-2 | Gap 1-3 | Leader | #1 net | #2 net | #3 net |
|------|--------:|--------:|--------|-------:|-------:|-------:|
| 03:00 | 35.0 | 35.0 | momentum_s_0 GBPEUR | 390.0 | 355.0 | 355.0 |
| 04:00 | **215.0** | **215.0** | momentum_s_0 AUD | 645.0 | 430.0 | 430.0 |
```

### Largest Gap Summary Format

```
| Time | Gap | #1 | net | #2 | net |
|------|----:|----|----|----|----|
| **03:52:46** | **215.0** | `strategy_name` PAIR | 645.0 | `strategy_name` PAIR | 430.0 |
```

---

## Analysis 3: Day-Over-Day Comparison

### Purpose
Compare gap patterns between different trading days to identify regime changes.

### Comparison Table Format

```
| Metric | Monday | Tuesday |
|--------|-------:|--------:|
| Max gap before 10am | **215.0** | 30.0 |
| EOD leader net | 155,230 | 1,492.5 |
| EOD gap #1 vs #2 | 102,990 | 0.0 |
| Gap pattern | Clear leader | Tied all day |
```

---

## Key Observations from 2026-05-04 vs 2026-05-05

### Monday 2026-05-04
- **Largest gap before 10am**: 215.0 at 03:52 (`momentum_s_0` AUD at 645.0)
- Gap held from 4am-8am at 215.0
- Breakaway accelerated from 17:00 onwards
- EOD: Gap exploded to 102,990 with leader at 155,230

### Tuesday 2026-05-05
- **Largest gap before 10am**: 30.0 at 00:26
- Gap was 0.0 (tied) almost entire day
- Not just #1/#2 tied - #3 also tied most of the day
- Largest gap over #3: 197.5 at 15:00-16:00
- EOD: Only 17.5 ahead of #3

### Interpretation
- Monday: Clear early leader that held and expanded - directional day
- Tuesday: No separation - mean-reverting/choppy day

---

## Plan

- [x] 1. Document data source and JSON structure
  - Test: Verify JSON structure matches documented schema
  - Evidence: Schema documented above matches actual file structure
- [x] 2. Document Analysis 1: Top N by metric at cutoff vs EOD
  - Test: Python code runs without error on sample data
  - Evidence: Code tested in session, output matches expected format
- [x] 3. Document Analysis 2: Gap progression methodology
  - Test: Python code produces hourly gap snapshots
  - Evidence: Code tested in session, gap progression table generated
- [x] 4. Document Analysis 3: Day-over-day comparison format
  - Test: Comparison table format is clear and reproducible
  - Evidence: Format documented with example values
- [x] 5. Capture key observations from 2026-05-04 vs 2026-05-05
  - Test: Observations are factual and derived from analysis
  - Evidence: Observations match analysis output

## Evidence
- Evidence-Type: file_output
  - Artifact: This task file documents methodology
  - Objective-Proved: Analysis methodology is reproducible
  - Status: captured

Objective-Delivery-Coverage: 100%
Auto-Acceptance: true

## Implementation Log
- 2026-05-06 18:47: Created methodology documentation from ad-hoc analysis session

## Changes Made
- Created: `workstream/100_backlog/20260506_184700_breakout_997_strategy_gap_analysis_methodology.md`

## Validation
- Python code snippets validated during analysis session
- Output formats match actual session outputs

## Risks/Notes
- Large JSON files (~31MB) require streaming or chunked processing for memory-constrained environments
- Timestamps in data are ISO format with microseconds
- Analysis assumes records are ordered chronologically within each strategy/pair array

## Completion Status
Complete - 2026-05-06
