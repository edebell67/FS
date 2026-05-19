# Pick Now Effectiveness Analysis

Source: User request / Analysis session

Task Summary: Comprehensive analysis of pick_now strategy selection effectiveness across multiple trading days.

Context:
- Project: TradeApps/breakout
- Data Source: `_summary_net.json` backfilled to `_top10_history_backfilled.json`
- Dates Analyzed: 2026-03-16 to 2026-03-24 (6 trading days)
- Tool Created: `backfill_top10_history.py`

Priority: 1

---

## 1. Backfill Script Overview

Created `backfill_top10_history.py` to reconstruct historical top10 snapshots with pick_now evaluation.

### Usage
```bash
# Backfill with analysis
python backfill_top10_history.py --date 2026-03-24 --analyze

# Test different thresholds
python backfill_top10_history.py --date 2026-03-24 --min-appearances 10 --min-net-trend 50 --dry-run
```

### Current Thresholds (from config.json)
- `min_appearances`: 20
- `min_net_trend`: 100
- `min_snapshots`: 60

---

## 2. Single Day Analysis (2026-03-24)

### Position Tracking Results

Of the 21 strategies that received pick_now=True:

| Metric | Count | % |
|--------|-------|---|
| Still in top 10 at end | 6 | 29% |
| Stayed in top 10 ALWAYS (never left) | 4 | 19% |
| **Stayed above pick net ALWAYS** | **16** | **76%** |
| **Above pick net at last observation** | **19** | **90%** |

### Outcome Breakdown

| Outcome | Count | Description |
|---------|-------|-------------|
| WIN | 6 | Still in top 10, net increased |
| LOSS | 0 | Still in top 10, net decreased |
| DROPPED_UP | 5 | Left top 10 but net was higher than pick |
| DROPPED_DOWN | 2 | Left top 10 and net was lower than pick |
| DROPPED_FLAT | 8 | Left top 10 but net unchanged |

**Key insight:** 19 of 21 (90%) were at or above their pick net when last observed. Only 2 strategies actually went negative after being picked.

### The 2 That Went Negative
- `breakout_R_3_tp10.0_sl5.0 GBPEUR_C`: -90 (750→660)
- `breakout_R_2_tp10.0_sl5.0 GBPEUR_C`: -60 (600→540)

### First Pick Time
- **First pick_now: 06:44 AM** (snapshot #60)
- With thresholds of `min_appearances=20, min_snapshots=60`, the earliest possible pick is snapshot #60

---

## 3. Hourly Breakdown (2026-03-24)

| Hour | Picks | Total Change | Avg Per Pick |
|------|-------|--------------|--------------|
| 06:00 | 5 | -150 | **-30 pp** |
| 07:00 | 2 | +10 | +5 pp |
| 08:00 | 1 | +170 | +170 pp |
| 10:00 | 5 | +130 | +26 pp |
| 14:00 | 1 | +360 | **+360 pp** |
| 17:00 | 6 | +1,745 | **+291 pp** |
| 20:00 | 1 | +190 | +190 pp |
| **TOTAL** | **21** | **+2,455** | **+117 pp** |

**Key insight:** Early picks (06:00-07:00) performed worst. The 5 strategies picked at 06:00 (right when min_snapshots=60 threshold hit) averaged **-30 pp**. Later picks performed much better, with 17:00 being the sweet spot at **+291 pp** average.

---

## 4. Multi-Day Analysis (6 Trading Days)

### Summary by Date

| Date | Picks | Total Net | Avg PP | Best Hour | Worst Hour |
|------|-------|-----------|--------|-----------|------------|
| 2026-03-24 | 21 | +2,455 | +117 | 17:00 (+291pp) | 06:00 (-30pp) |
| 2026-03-23 | 11 | +1,013 | +92 | 16:00 (+190pp) | 12:00 (-20pp) |
| 2026-03-20 | 11 | +268 | +24 | 08:00 (+90pp) | 11:00 (-18pp) |
| 2026-03-19 | 19 | +2,470 | +130 | 08:00 (+328pp) | 17:00 (-60pp) |
| 2026-03-18 | 12 | +755 | +63 | 17:00 (+184pp) | 16:00 (+8pp) |
| 2026-03-16 | 19 | +1,485 | +78 | 08:00 (+343pp) | 13:00 (-181pp) |

### Hourly Breakdown by Date

#### 2026-03-24
```
06:00    5p    -150.0    -30.0 pp
07:00    2p     +10.0     +5.0 pp
08:00    1p    +170.0   +170.0 pp
10:00    5p    +130.0    +26.0 pp
14:00    1p    +360.0   +360.0 pp
17:00    6p   +1745.0   +290.8 pp
20:00    1p    +190.0   +190.0 pp
TOTAL   21p   +2455.0   +116.9 pp
```

#### 2026-03-23
```
07:00    4p    +460.0   +115.0 pp
12:00    1p     -20.0    -20.0 pp
13:00    2p    +320.0   +160.0 pp
16:00    1p    +190.0   +190.0 pp
19:00    1p     +62.5    +62.5 pp
20:00    1p      +0.0     +0.0 pp
23:00    1p      +0.0     +0.0 pp
TOTAL   11p   +1012.5    +92.0 pp
```

#### 2026-03-20
```
07:00    2p      +0.0     +0.0 pp
08:00    3p    +270.0    +90.0 pp
10:00    5p     +15.0     +3.0 pp
11:00    1p     -17.5    -17.5 pp
TOTAL   11p    +267.5    +24.3 pp
```

#### 2026-03-19
```
07:00    6p    +960.0   +160.0 pp
08:00    4p   +1310.0   +327.5 pp
09:00    1p      +0.0     +0.0 pp
11:00    1p      +0.0     +0.0 pp
13:00    1p      +0.0     +0.0 pp
16:00    1p     -60.0    -60.0 pp
17:00    1p     -60.0    -60.0 pp
18:00    3p    +130.0    +43.3 pp
23:00    1p    +190.0   +190.0 pp
TOTAL   19p   +2470.0   +130.0 pp
```

#### 2026-03-18
```
16:00    5p     +40.0     +8.0 pp
17:00    3p    +552.5   +184.2 pp
19:00    1p    +162.5   +162.5 pp
20:00    1p      +0.0     +0.0 pp
22:00    2p      +0.0     +0.0 pp
TOTAL   12p    +755.0    +62.9 pp
```

#### 2026-03-16
```
08:00    4p   +1372.5   +343.1 pp
09:00    2p    +275.0   +137.5 pp
10:00    3p      +0.0     +0.0 pp
11:00    3p     -50.0    -16.7 pp
12:00    1p    -130.0   -130.0 pp
13:00    2p    -362.5   -181.2 pp
16:00    2p      +0.0     +0.0 pp
18:00    1p    +190.0   +190.0 pp
19:00    1p    +190.0   +190.0 pp
TOTAL   19p   +1485.0    +78.2 pp
```

### Key Patterns

1. **Early picks (06:00-07:00) are inconsistent** - Sometimes good (03-23: +115pp), sometimes bad (03-24: -30pp)
2. **08:00 picks tend to be strong** - Best hour on 03-16 (+343pp), 03-19 (+328pp), 03-20 (+90pp)
3. **Afternoon picks (16:00-17:00) are mixed** - Great on 03-24 (+291pp), 03-18 (+184pp), but poor on 03-19 (-60pp)
4. **Later in day = higher confidence** - Total net is always positive across all dates

### Overall (6 Days)
- Total picks: 93
- Total net change: +8,445
- Average per pick: **+91 pp**

---

## 5. Strategy Type Breakdown (scalper/rev_scalper/other)

### Classification
- **scalper**: `breakout_R_` prefix (without Rev)
- **rev_scalper**: Contains `_Rev_` or `Rev_` after breakout_
- **other**: Standard breakout strategies

### Overall Summary (6 Days)

| Type | Picks | Total Net | Avg PP | W/L/Flat | Win% |
|------|-------|-----------|--------|----------|------|
| **other** | 40 | +5,205 | **+130** | 21/6/13 | 52.5% |
| scalper | 17 | +1,135 | +67 | 8/4/5 | 47.1% |
| rev_scalper | 36 | +2,105 | +59 | 13/6/17 | 36.1% |
| **TOTAL** | **93** | **+8,445** | **+91** | | |

### Daily Performance by Type

| Date | other | scalper | rev_scalper |
|------|-------|---------|-------------|
| 03-24 | 11p **+231pp** | 5p +6pp | 5p -24pp |
| 03-23 | 8p +79pp | -- | 3p +128pp |
| 03-20 | -- | 1p +0pp | 10p +27pp |
| 03-19 | 15p **+164pp** | 2p -60pp | 2p +65pp |
| 03-18 | 2p +20pp | 4p **+149pp** | 6p +20pp |
| 03-16 | 4p -118pp | 5p +126pp | 10p **+133pp** |

### Key Finding

"Other" strategies (non-scalper, non-rev_scalper) significantly outperform:
- **+130 pp** average vs +67 (scalper) and +59 (rev_scalper)
- Highest win rate at **52.5%**
- Contributes **62%** of total gains (+5,205 of +8,445)

---

## 6. Base Strategy Breakdown

### Classification
- **breakout**: Standard (e.g., `breakout_2_tp20.0_sl5.0`)
- **breakout_R**: R prefix (e.g., `breakout_R_2_tp20.0_sl5.0`)
- **breakout_Rev**: Rev prefix (e.g., `breakout_Rev_2_tp20.0_sl5.0`)
- **breakout_R_Rev**: R_Rev prefix (e.g., `breakout_R_Rev_2_tp20.0_sl5.0`)

### Overall Summary (6 Days)

| Strategy | Picks | Total Net | Avg PP | W/L/Flat | Win% |
|----------|-------|-----------|--------|----------|------|
| **breakout** | 40 | +5,205 | **+130** | 21/6/13 | **52.5%** |
| breakout_R_Rev | 20 | +1,605 | +80 | 8/4/8 | 40.0% |
| breakout_R | 17 | +1,135 | +67 | 8/4/5 | 47.1% |
| breakout_Rev | 16 | +500 | +31 | 5/2/9 | 31.2% |
| **TOTAL** | **93** | **+8,445** | **+91** | | |

### Daily Performance

| Date | breakout | breakout_R | breakout_Rev | breakout_R_Rev |
|------|----------|------------|--------------|----------------|
| 03-24 | 11p **+231pp** | 5p +6pp | -- | 5p -24pp |
| 03-23 | 8p +79pp | -- | 1p +62pp | 2p +160pp |
| 03-20 | -- | 1p +0pp | 9p +30pp | 1p +0pp |
| 03-19 | 15p **+164pp** | 2p -60pp | 1p +190pp | 1p -60pp |
| 03-18 | 2p +20pp | 4p **+149pp** | 5p -4pp | 1p +140pp |
| 03-16 | 4p -118pp | 5p +126pp | -- | 10p **+132pp** |

### Key Findings

1. **breakout (base)** is the clear winner:
   - Highest avg return: **+130 pp**
   - Highest win rate: **52.5%**
   - 43% of picks, but **62% of total gains**

2. **breakout_R_Rev** is second best (+80 pp avg)

3. **breakout_Rev** underperforms (+31 pp avg, 31% win rate)

4. **Consistency varies by day** - no single strategy wins every day

---

## 7. Appearance Frequency Analysis

### Initial Question
Did best performers generally have the higher frequency of appearance?

### Analysis 1: Appearances AT TIME OF PICK

| Appearances | Picks | Total | Avg PP | Win% |
|-------------|-------|-------|--------|------|
| **20-24** | 75 | +8,470 | **+113** | **49.3%** |
| 25-29 | 3 | -45 | -15 | 33.3% |
| 30-39 | 6 | +50 | +8 | 16.7% |
| 40-49 | 8 | -70 | -9 | 25.0% |
| 50+ | 1 | +40 | +40 | 100% |

**Correlation (Appearances at Pick vs Change): -0.220** (negative)

Initial finding suggested strategies picked RIGHT at 20 appearances perform best. However, this is misleading...

### Analysis 2: TOTAL Appearances (Full Day)

The user correctly pointed out:
> "If those picked at 20-24 make up most of the points gained, that suggests they will end up with significantly more appearances... however if picked near the peak of appearance the profit opportunity may have dried up..."

Reanalysis with TOTAL appearances:

| Total App | Picks | Total | Avg PP | Win% |
|-----------|-------|-------|--------|------|
| 20-29 | 41 | +1,263 | +31 | 19.5% |
| **30-39** | **19** | **+3,903** | **+205** | **89.5%** |
| 40-49 | 15 | +1,893 | +126 | 60.0% |
| 50-59 | 9 | +158 | +18 | 44.4% |
| 60-79 | 9 | +1,230 | +137 | 44.4% |

### Correlations

| Metric | Correlation | Interpretation |
|--------|-------------|----------------|
| Appearances at Pick vs Change | -0.220 | More appearances at pick = worse (misleading) |
| **Total Appearances vs Change** | **+0.088** | Weak positive |
| **Appearances AFTER Pick vs Change** | **+0.228** | Stronger positive |

### Top 10 Best Performers (with Total Appearances)

| Strategy | Product | Total App | App After | Change |
|----------|---------|-----------|-----------|--------|
| breakout_3_tp20.0_sl50.0 | GBPEUR_C | 61 | 39 | +760.0 |
| breakout_4_tp20.0_sl30.0 | GBPEUR_C | 72 | 52 | +760.0 |
| breakout_R_Rev_4_tp10.0_sl30.0 | GBPAUD_C | 45 | 24 | +465.0 |
| breakout_2_tp20.0_sl30.0 | GBPEUR_C | 30 | 10 | +380.0 |
| breakout_2_tp20.0_sl50.0 | GBPEUR_C | 30 | 10 | +380.0 |
| breakout_2_tp20.0_sl5.0 | NZDAUD_C | 26 | 6 | +380.0 |
| breakout_3_tp20.0_sl30.0 | GBPEUR_C | 30 | 10 | +362.5 |
| breakout_3_tp20.0_sl50.0 | GBPEUR_C | 28 | 8 | +362.5 |
| breakout_2_tp10.0_sl50.0 | GBPAUD_C | 37 | 17 | +360.0 |
| breakout_3_tp20.0_sl20.0 | GBPNZD_C | 31 | 11 | +360.0 |

### Top 10 Worst Performers (with Total Appearances)

| Strategy | Product | Total App | App After | Change |
|----------|---------|-----------|-----------|--------|
| breakout_3_tp20.0_sl5.0 | GBPNZD_C | 21 | 1 | -60.0 |
| breakout_R_Rev_2_tp20.0_sl5.0 | GBPAUD_C | 25 | 5 | -60.0 |
| breakout_R_2_tp20.0_sl5.0 | GBPNZD_C | 31 | 4 | -60.0 |
| breakout_3_tp20.0_sl20.0 | GBPEUR_C | 73 | 53 | -60.0 |
| breakout_R_3_tp10.0_sl5.0 | GBPEUR_C | 67 | 23 | -90.0 |
| breakout_R_Rev_3_tp20.0_sl5.0 | EURAUD_C | 27 | 7 | -120.0 |
| breakout_4_tp20.0_sl50.0 | GBPEUR_C | 52 | 17 | -130.0 |
| breakout_3_tp20.0_sl50.0 | GBPEUR_C | 76 | 56 | -130.0 |
| breakout_3_tp20.0_sl30.0 | GBPEUR_C | 75 | 55 | -240.0 |
| breakout_R_Rev_2_tp10.0_sl5.0 | GBPEUR_C | 57 | 37 | -322.5 |

### Key Insights

1. **Sweet spot is 30-39 total appearances** - 89.5% win rate, +205 pp avg

2. **20-29 total = likely dropped out early** - only 19.5% win rate, these got picked but didn't persist

3. **Top performers had 26-72 total appearances** - they kept appearing after being picked

4. **Worst performers split into two groups:**
   - Low total (21-31): Dropped out quickly after pick
   - High total (52-76): Stayed in top 10 but net declined (picked near peak)

5. **Note on "appearances after pick" correlation (+0.228):** This is essentially tautological - strategies that stay profitable stay in top 10, which means more appearances. This correlation doesn't predict success; it just restates it.

---

## 8. Actual Predictive Factors (AT TIME OF PICK)

The real question: What factors AT THE MOMENT OF PICK predict future success?

### Net Value at Pick

| Net at Pick | Picks | Avg Change | Win% |
|-------------|-------|------------|------|
| <600 | 10 | +47 | **10%** |
| **600-799** | **29** | **+138** | **69%** |
| 800-999 | 38 | +106 | 39% |
| 1000+ | 16 | -2 | 38% |

**Finding:** Sweet spot is **net 600-799** at pick = 69% win rate. Too low (<600) or too high (1000+) performs worse.

### Net Trend at Pick

| Net Trend | Picks | Avg Change | Win% |
|-----------|-------|------------|------|
| 100-149 | 5 | +102 | 40% |
| 150-249 | 19 | +126 | 47% |
| 250-399 | 40 | +91 | 45% |
| 400+ | 29 | +65 | 45% |

**Finding:** Higher net trend at pick = slightly worse outcomes. The profit opportunity may have already materialized.

### Snapshot # (Time of Day Proxy)

| Snapshot | Picks | Avg Change | Win% |
|----------|-------|------------|------|
| 60-69 | 34 | +103 | 50% |
| 70-84 | 23 | +102 | 48% |
| 85-99 | 10 | +25 | **20%** |
| 100-129 | 22 | +89 | 45% |
| 130+ | 4 | +95 | 50% |

**Finding:** Snapshots 85-99 are a "dead zone" with only 20% win rate.

### Correlations (AT TIME OF PICK)

| Factor | Correlation | Interpretation |
|--------|-------------|----------------|
| Net at pick | -0.130 | Higher net = slightly worse |
| Net trend at pick | -0.183 | Higher trend = slightly worse |
| Snapshot # | -0.048 | Negligible |

**All correlations are NEGATIVE:** This suggests picking strategies that are already "too successful" (high net, high trend) may mean the opportunity has passed.

### Trade Count at Pick

| Trades | Picks | Avg PP | Win% |
|--------|-------|--------|------|
| 0-4 | 12 | **+135** | 33% |
| 5-9 | 44 | +95 | 45% |
| **10-14** | **19** | **+117** | **53%** |
| 15-19 | 9 | +79 | **67%** |
| 20-29 | 6 | +4 | 33% |
| 30-49 | 2 | +0 | 0% |
| 50+ | 1 | **-323** | 0% |

**Correlations:**

| Factor | Correlation |
|--------|-------------|
| Trade count vs Change | **-0.269** |
| Buy count vs Change | **-0.290** |
| Sell count vs Change | **-0.226** |

**Finding:** Fewer trades at pick = better outcomes
- **Sweet spot: 10-14 trades** = +117 avg with 53% win rate
- **Top 10 winners:** All had 4-10 trades at pick
- **Worst performer:** 58 trades at pick → -322.5 change

This makes sense - high trade count means:
1. Strategy has been active longer → opportunity may be exhausted
2. More exposure to changing market conditions
3. Edge already captured in existing trades

### Top 10 Performers - Trade Counts

| Strategy | Product | Trades | B/S | Change |
|----------|---------|--------|-----|--------|
| breakout_3_tp20.0_sl50.0 | GBPEUR_C | 4 | 2/2 | +760.0 |
| breakout_4_tp20.0_sl30.0 | GBPEUR_C | 5 | 2/3 | +760.0 |
| breakout_R_Rev_4_tp10.0_sl30.0 | GBPAUD_C | 10 | 5/5 | +465.0 |
| breakout_2_tp20.0_sl30.0 | GBPEUR_C | 5 | 2/3 | +380.0 |
| breakout_2_tp20.0_sl50.0 | GBPEUR_C | 5 | 2/3 | +380.0 |

### Bottom 5 Performers - Trade Counts

| Strategy | Product | Trades | B/S | Change |
|----------|---------|--------|-----|--------|
| breakout_R_Rev_3_tp20.0_sl5.0 | EURAUD_C | 21 | 12/9 | -120.0 |
| breakout_4_tp20.0_sl50.0 | GBPEUR_C | 5 | 2/3 | -130.0 |
| breakout_3_tp20.0_sl50.0 | GBPEUR_C | 6 | 4/2 | -130.0 |
| breakout_3_tp20.0_sl30.0 | GBPEUR_C | 6 | 4/2 | -240.0 |
| breakout_R_Rev_2_tp10.0_sl5.0 | GBPEUR_C | 58 | 30/28 | -322.5 |

---

## 9. Conclusions & Recommendations

### What Works
1. **Standard breakout strategies** outperform scalper/rev_scalper variants
2. **Net at pick in 600-799 range** = 69% win rate (vs 10-39% outside this range)
3. **90% of picked strategies** stay at or above their pick net
4. **Total net across 6 days: +8,445** with 93 picks = +91 pp average

### What Doesn't Work
1. **Picking strategies with net < 600** - only 10% win rate
2. **Picking strategies with net > 1000** - opportunity already passed, -2 avg return
3. **Picking at the first eligible moment** (06:00, right at threshold) - worst avg returns
4. **breakout_Rev strategies** - lowest win rate (31.2%)
5. **High net_trend at pick** - negative correlation with future returns

### Executed Optimizations
*(Update 2026-03-24 23:33)* The following 4 data-driven "Golden Filters" derived from this analysis were formally implemented via `20260324_233200_breakout_golden_pick_now_filter.md`:
1. **Net Range Bound**: Pick only if net is between `600` and `799`.
2. **Max Trade Count**: Pick only if strategy has executed `< 20` trades.
3. **Strategy Exclusions**: Omit the `breakout_Rev_` variants due to low win rates.
4. **Time Dead Zone**: Skip evaluating picks inside the `85-99` snapshot window (08:30-10:00 AM).

### Original Potential Optimizations (Pre-Implementation)

1. **Add net_at_pick filter** - Only pick if net is in 600-800 range (69% win rate vs 38% for 1000+)
2. **Favor base breakout strategies** - 52.5% win rate vs 31-47% for variants
3. **Avoid snapshot 85-99 window** - 20% win rate dead zone
4. **Don't chase high net_trend** - Higher trend at pick correlates with worse outcomes
5. **Consider adjusting thresholds:**
   - Current: min_appearances=20, min_net_trend=100, min_snapshots=60
   - Add: max_net_at_pick=900, min_net_at_pick=550

---

## Evidence
Objective-Delivery-Coverage: 100%
- Evidence-Type: data_analysis
  - Status: complete
  - Artifacts:
    - `backfill_top10_history.py`
    - `_top10_history_backfilled.json` files for each analyzed date

## Implementation Log
- 2026-03-24 20:50: Created backfill_top10_history.py
- 2026-03-24 21:00: Analyzed 2026-03-24 data
- 2026-03-24 21:10: Extended to 6-day analysis
- 2026-03-24 21:30: Added strategy type breakdowns
- 2026-03-24 21:45: Added appearance frequency analysis
- 2026-03-24 22:06: Documented full analysis
- 2026-03-24 23:33: Implemented derived Golden Filters directly into `strategy_predictor.py` (Referenced via `20260324_233200_breakout_golden_pick_now_filter.md`).

Completion Status: Complete
