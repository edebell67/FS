# R_Rev Strategy Buy_Net vs Sell_Net Divergence Analysis

**Task Type:** Analysis / Research
**Task Summary:** Compare buy_net vs sell_net for R_Rev strategies to identify positive divergence patterns where the difference is increasing.
**Dependency:** 20260505_035810_breakout_summary_net_analysis.md (completed)
**Status:** Complete
**Date:** 2026-05-05

---

## Objective

Analyze R_Rev (Range-Reversal) breakout strategies to:
1. Compare buy_net vs sell_net performance over time
2. Identify strategies where BOTH buy_net AND sell_net are positive
3. Find patterns where the difference (buy_net - sell_net) is increasing
4. Determine if directional bias strength correlates with overall profitability

---

## Data Source

**Files:** `TradeApps/breakout/fs/json/live/forex/{date}/_summary_net.json`

**Strategy Filter:** `breakout_R_Rev_*` patterns only

**Key Fields:**
| Field | Description |
|-------|-------------|
| buy_net | Profit/loss from buy positions |
| sell_net | Profit/loss from sell positions |
| net | Total (buy_net + sell_net) |
| b_c | Buy trade count |
| s_c | Sell trade count |
| t | Timestamp |

**Dates to Analyze:**
- 2026-04-28
- 2026-04-29
- 2026-04-30
- 2026-05-01
- 2026-05-03
- 2026-05-04
- 2026-05-05 (current)

---

## Plan

- [x] **1. Extract R_Rev data** - Filter all R_Rev strategies from _summary_net.json files
- [x] **2. Baseline metrics** - Calculate buy_net vs sell_net distribution for all R_Rev entries
- [x] **3. Positive divergence scan** - Find strategies where both buy_net > 0 AND sell_net > 0
- [x] **4. Divergence growth analysis** - Track (buy_net - sell_net) over time for each strategy
- [x] **5. Identify increasing divergence** - Flag strategies where |buy_net - sell_net| is growing
- [x] **6. Correlation check** - Does increasing divergence predict higher net gains?
- [x] **7. Direction bias analysis** - Are buy-dominant or sell-dominant strategies more profitable?
- [x] **8. Cross-validate** - Check if patterns hold across multiple dates
- [x] **9. Document findings** - Summarize actionable insights

---

## Analysis Outputs

### Analysis 1: R_Rev Buy vs Sell Baseline Distribution

```
Total R_Rev strategy-pair combinations: 4,481
Buy-dominant (buy_net > sell_net):       1,878 (41.9%)
Sell-dominant (sell_net > buy_net):      2,566 (57.3%)
Both positive (buy_net > 0 AND sell_net > 0): 453 (10.1%)

Avg buy_net:    -224.0
Avg sell_net:   -120.4
Avg net:        -344.5
Avg divergence: -103.6 (buy_net - sell_net)
```

**Key Finding:** R_Rev strategies are sell-dominant overall. Sells outperform buys by an average of 103.6 points.

---

### Analysis 2: Strategies with Both Buy_Net > 0 AND Sell_Net > 0

Only **10.1%** of strategy-pair combinations have both sides profitable.

**Top 10 Both-Positive Performers:**

| Date | Strategy | Pair | Buy_Net | Sell_Net | Net | Divergence |
|------|----------|------|--------:|----------:|----:|-----------:|
| 2026-05-05 | breakout_R_Rev_4_tp20.0_sl20.0 | GBPNZD_C | +645 | +775 | +1,420 | -130 |
| 2026-05-05 | breakout_R_Rev_4_tp20.0_sl30.0 | GBPNZD_C | +642 | +595 | +1,238 | +48 |
| 2026-04-29 | breakout_R_Rev_2_tp20.0_sl5.0 | GBPEUR_C | +135 | +1,025 | +1,160 | -890 |
| 2026-04-29 | breakout_R_Rev_3_tp20.0_sl20.0 | GBPEUR_C | +55 | +975 | +1,030 | -920 |
| 2026-04-29 | breakout_R_Rev_2_tp10.0_sl5.0 | EURAUD_C | +465 | +505 | +970 | -40 |
| 2026-04-29 | breakout_R_Rev_3_tp20.0_sl30.0 | GBPEUR_C | +40 | +875 | +915 | -835 |
| 2026-04-29 | breakout_R_Rev_3_tp20.0_sl50.0 | GBPEUR_C | +40 | +860 | +900 | -820 |
| 2026-05-05 | breakout_R_Rev_4_tp20.0_sl50.0 | GBPNZD_C | +242 | +595 | +838 | -352 |
| 2026-04-29 | breakout_R_Rev_2_tp20.0_sl5.0 | EURAUD_C | +70 | +730 | +800 | -660 |
| 2026-04-30 | breakout_R_Rev_4_tp20.0_sl50.0 | GBP | +555 | +245 | +800 | +310 |

**Both-Positive by Pair:**

| Pair | Count | Total Net | Avg Net | Avg Buy | Avg Sell |
|------|------:|----------:|--------:|--------:|---------:|
| GBPEUR_C | 51 | +18,032 | +353.6 | +94.6 | +259.0 |
| GBPAUD_C | 38 | +12,305 | +323.8 | +121.6 | +202.2 |
| CAD | 50 | +10,702 | +214.1 | +136.4 | +77.6 |
| GBP | 37 | +9,905 | +267.7 | +129.9 | +137.8 |
| GBPNZD_C | 24 | +9,275 | +386.5 | +145.5 | +240.9 |
| EURAUD_C | 23 | +8,810 | +383.0 | +153.0 | +230.0 |

---

### Analysis 3: Divergence Growth Patterns

```
Total growth records: 4,336
Divergence increasing: 3,961 (91.4%)
Monotonically increasing: 2,617 (60.4%)
Increasing + Both Positive at end: 335
```

**Finding:** 91.4% of R_Rev strategies show increasing divergence over the trading day.

**Top Increasing Divergence + Both Positive:**

| Date | Strategy | Pair | Div Start | Div End | Div Change | Net |
|------|----------|------|----------:|--------:|-----------:|----:|
| 2026-05-05 | breakout_R_Rev_4_tp20.0_sl20.0 | GBPNZD_C | +45 | -130 | -175 | +1,420 |
| 2026-05-05 | breakout_R_Rev_4_tp20.0_sl30.0 | GBPNZD_C | +45 | +48 | +2 | +1,238 |
| 2026-04-29 | breakout_R_Rev_2_tp20.0_sl5.0 | GBPEUR_C | -45 | -890 | -845 | +1,160 |
| 2026-04-29 | breakout_R_Rev_3_tp20.0_sl20.0 | GBPEUR_C | -45 | -920 | -875 | +1,030 |
| 2026-04-30 | breakout_R_Rev_4_tp20.0_sl50.0 | GBP | -185 | +310 | +495 | +800 |

---

### Analysis 4: Correlation - Divergence Growth vs Net Performance

```
Increasing divergence: 3,961 records, avg net = -373.8
Decreasing divergence:   375 records, avg net = -172.5
Difference: -201.3
```

**CRITICAL FINDING:** Increasing divergence correlates with WORSE performance, not better.

**By Dominant Side (among increasing divergence):**

| Dominant Side | Count | Avg Net |
|---------------|------:|--------:|
| Buy-dominant | 1,680 | -291.8 |
| Sell-dominant | 2,281 | -434.2 |

**Finding:** Sell-dominant with increasing divergence has the worst average performance (-434.2).

---

### Analysis 5: Date-by-Date Breakdown

| Date | Total | Both Pos | Buy Dom | Sell Dom | Avg Buy | Avg Sell | Avg Net | Best Both-Pos |
|------|------:|:--------:|--------:|---------:|--------:|---------:|--------:|---------------|
| 2026-04-28 | 701 | 134 | 433 | 246 | +41.7 | -87.7 | -46.0 | EURAUD_C +560 |
| 2026-04-29 | 720 | 97 | 240 | 475 | -161.3 | +37.5 | -123.8 | GBPEUR_C +1,160 |
| 2026-04-30 | 720 | 56 | 455 | 261 | -63.5 | -213.1 | -276.6 | GBP +800 |
| 2026-05-01 | 780 | 17 | 175 | 604 | -433.2 | -138.2 | -571.4 | CHF +570 |
| 2026-05-04 | 780 | 43 | 232 | 546 | -462.8 | -166.2 | -629.0 | CAD +365 |
| 2026-05-05 | 780 | 106 | 343 | 434 | -221.1 | -146.5 | -367.6 | GBPNZD_C +1,420 |

**Pattern:** Market regime shifts daily. 2026-04-28 was buy-dominant day, while 2026-04-29 and 2026-05-01 were strongly sell-dominant.

---

## Conclusions

### Key Findings

1. **Sell Side Outperforms Buy Side**
   - 57.3% of R_Rev strategies are sell-dominant
   - Avg sell_net (-120.4) beats avg buy_net (-224.0) by 103.6 points

2. **Both-Positive is Rare but Valuable**
   - Only 10.1% have both sides profitable
   - Best pairs: GBPEUR_C, GBPNZD_C, EURAUD_C

3. **Increasing Divergence is BAD**
   - 91.4% show increasing divergence
   - But increasing divergence = worse net (-373.8 vs -172.5)
   - **Counter-intuitive:** Look for STABLE or CONVERGING divergence

4. **Top Performers Share Characteristics**
   - Variant 4 appears frequently in top both-positive
   - SL 20-50 range dominates top performers
   - GBP crosses (GBPNZD_C, GBPEUR_C) are most successful

5. **Daily Regime Matters**
   - 2026-04-28: Buy day (buys profitable)
   - 2026-04-29: Sell day (sells very profitable)
   - No consistent daily pattern

### Actionable Insight

**DO NOT use "increasing divergence" as an entry signal for R_Rev strategies.**

The hypothesis that increasing |buy_net - sell_net| correlates with better net is **REJECTED**.

Instead, look for:
- Both buy_net > 0 AND sell_net > 0 (balanced performance)
- Stable or converging divergence (not increasing)
- GBP cross pairs (GBPNZD_C, GBPEUR_C)
- Variant 4 with SL 20-50

---

## Evidence

- **Objective-Delivery-Coverage:** 100%
- Analysis script: `scripts/analyze_r_rev_buy_sell_divergence.py`
- Data: 4,481 R_Rev strategy-pair combinations across 6 trading days
- Finding: Increasing divergence correlates with WORSE performance

---
