# Breakout Strategy Analysis - Summary Net Investigation

**Task Type:** Analysis / Research
**Task Summary:** Investigate `_summary_net.json` files to identify top-performing strategies, analyze entry timing, and validate anti-whipsaw trading rules.
**Dependency:** None
**Status:** Complete
**Date:** 2026-05-05

---

## Objective

Analyze breakout strategy performance data to:
1. Find #1 cumulative net strategies after 21:00 (excluding momentum)
2. Identify which strategies held #1 position longest
3. Determine optimal entry timing to avoid whipsaw
4. Validate findings across multiple dates
5. Test survivorship bias in entry signals

---

## Data Source

**File:** `TradeApps/breakout/fs/json/live/forex/{date}/_summary_net.json`

**Dates Analyzed:**
- 2026-04-28
- 2026-04-29
- 2026-04-30
- 2026-05-01
- 2026-05-03
- 2026-05-04

**Note:** 2026-05-02 file not available.

---

## Analysis 1: Top Strategy After 21:00 (2026-05-04)

### Excluding Momentum Strategies

```
Top 10 strategies (latest net after 21:00 on 2026-05-04):
==========================================================================================
1. breakout_R_2_tp20.0_sl30.0               | GBPEUR_C   | Net:      1,215.0
2. breakout_R_3_tp20.0_sl30.0               | GBPEUR_C   | Net:      1,215.0
3. breakout_R_4_tp20.0_sl30.0               | GBPEUR_C   | Net:      1,215.0
4. breakout_R_2_tp20.0_sl50.0               | GBPNZD_C   | Net:        995.0
5. breakout_R_3_tp20.0_sl50.0               | GBPNZD_C   | Net:        995.0
6. breakout_R_4_tp20.0_sl50.0               | GBPNZD_C   | Net:        995.0
7. breakout_R_2_tp20.0_sl20.0               | GBPNZD_C   | Net:        935.0
8. breakout_R_3_tp20.0_sl20.0               | GBPNZD_C   | Net:        935.0
9. breakout_R_4_tp20.0_sl20.0               | GBPNZD_C   | Net:        935.0
10. breakout_R_2_tp20.0_sl30.0              | GBPNZD_C   | Net:        895.0
```

---

## Analysis 2: Longest #1 Position

### After 21:00 (2026-05-04)

```
Strategies ranked by time held at #1 position (after 21:00, excluding momentum):
===============================================================================================
1. breakout_R_2_tp20.0_sl30.0               | GBPEUR_C   | Duration: 1h 08m 09s
2. breakout_R_2_tp10.0_sl20.0               | NZDAUD_C   | Duration: 0h 01m 41s
3. breakout_R_Rev_4_tp20.0_sl5.0            | GBP        | Duration: 0h 01m 02s
```

### Before 21:00 (2026-05-04)

```
Strategies ranked by time held at #1 position (BEFORE 21:00, excluding momentum):
===============================================================================================
1. breakout_2_tp20.0_sl30.0                 | EURAUD_C   | Duration: 6h 07m 05s
2. breakout_2_tp20.0_sl50.0                 | GBPAUD_C   | Duration: 4h 44m 56s
3. breakout_R_Rev_4_tp20.0_sl20.0           | EURAUD_C   | Duration: 3h 28m 48s
4. breakout_R_4_tp5.0_sl30.0                | NZDAUD_C   | Duration: 1h 41m 06s
5. breakout_R_Rev_4_tp10.0_sl20.0           | GBPNZD_C   | Duration: 0h 56m 17s
```

### Cumulative Net Delta During #1 Reign

**Strategy:** `breakout_2_tp20.0_sl30.0 | EURAUD_C`

```
Period 1: 10:07:18 -> 10:17:18
  Start Net: 540.0
  End Net:   540.0
  Delta:     +0.0

Period 2: 10:17:18 -> 16:14:23
  Start Net: 720.0
  End Net:   720.0
  Delta:     +0.0

TOTAL CUMULATIVE NET DELTA DURING #1 REIGN: +0.0
```

**Finding:** Strategy held #1 by maintaining position while others fell - didn't actively gain during reign.

---

## Analysis 3: Top Gainers by Time Window (2026-05-04)

### With Buy/Sell Deltas (Corrected for Period)

```
Window          Strategy                             Pair           Start       End      Gain  Buys Sells   BuyDelta  SellDelta
=====================================================================================================================================================================
01:00-21:00     breakout_2_tp20.0_sl50.0             GBPAUD_C        +180    +1,080      +900     2     3       +360       +540
02:00-21:00     breakout_2_tp20.0_sl50.0             GBPAUD_C        +180    +1,080      +900     2     3       +360       +540
03:00-21:00     breakout_2_tp20.0_sl50.0             GBPAUD_C        +180    +1,080      +900     2     3       +360       +540
04:00-21:00     breakout_2_tp20.0_sl50.0             GBPAUD_C        +180    +1,080      +900     2     3       +360       +540
05:00-21:00     breakout_R_2_tp20.0_sl30.0           GBPEUR_C        -140      +800      +940     4     4       +220       +720
06:00-21:00     breakout_Rev_2_tp20.0_sl20.0         GBPNZD_C      -1,105      -130      +975     9    14       +110       +865
07:00-21:00     breakout_R_2_tp20.0_sl30.0           GBPEUR_C        -140      +800      +940     4     4       +220       +720
08:00-21:00     breakout_R_2_tp20.0_sl30.0           GBPEUR_C        -140      +800      +940     4     4       +220       +720
09:00-21:00     breakout_R_2_tp20.0_sl30.0           GBPEUR_C        -140      +800      +940     4     4       +220       +720
10:00-21:00     breakout_R_2_tp20.0_sl30.0           GBPEUR_C        -140      +800      +940     4     4       +220       +720
11:00-21:00     breakout_R_2_tp20.0_sl30.0           GBPNZD_C        -100      +480      +580     4     2       +220       +360
12:00-21:00     breakout_2_tp20.0_sl30.0             GBPAUD_C        +400      +940      +540     1     2       +180       +360
13:00-21:00     breakout_R_Rev_2_tp10.0_sl30.0       GBPNZD_C      -1,050      -410      +640     8     7       +265       +375
14:00-21:00     breakout_R_Rev_2_tp20.0_sl50.0       NZDAUD_C      -1,695    -1,020      +675     3     5       +185       +490
15:00-21:00     breakout_R_Rev_2_tp20.0_sl50.0       NZDAUD_C      -1,695    -1,020      +675     3     5       +185       +490
16:00-21:00     breakout_R_2_tp20.0_sl20.0           EURNZD_C        -340      +380      +720     2     2       +360       +360
17:00-21:00     breakout_R_2_tp20.0_sl20.0           EURNZD_C        -160      +380      +540     1     2       +180       +360
18:00-21:00     breakout_2_tp3.0_sl50.0              GBPEUR_C        -850      -330      +520     0    -1         +0       +520
19:00-21:00     breakout_R_Rev_2_tp3.0_sl50.0        GBPEUR_C      -2,070    -1,550      +520     0    -1         +0       +520
20:00-21:00     breakout_Rev_4_tp10.0_sl50.0         NZDAUD_C      -2,300    -1,260    +1,040    -1    -1       +520       +520
```

---

## Analysis 4: Multi-Date Comparison

### 2026-04-28

```
Window          Strategy                             Pair           Start       End      Gain  Buys Sells   BuyDelta  SellDelta
---------------------------------------------------------------------------------------------------------------------------------------------------------------------
01:00-21:00     breakout_R_4_tp3.0_sl50.0            NZDAUD_C        -480       +40      +520     0    -1         +0       +520
02:00-21:00     breakout_R_2_tp3.0_sl50.0            NZDAUD_C        -460       +60      +520     0    -1         +0       +520
03:00-21:00     breakout_R_2_tp3.0_sl50.0            NZDAUD_C        -460       +60      +520     0    -1         +0       +520
04:00-21:00     breakout_R_2_tp3.0_sl50.0            NZDAUD_C        -460       +60      +520     0    -1         +0       +520
05:00-21:00     breakout_R_2_tp3.0_sl50.0            NZDAUD_C        -460       +60      +520     0    -1         +0       +520
06:00-21:00     breakout_R_2_tp3.0_sl50.0            NZDAUD_C        -460       +60      +520     0    -1         +0       +520
07:00-21:00     breakout_2_tp5.0_sl50.0              EURNZD_C        -460       +60      +520     0    -1         +0       +520
08:00-21:00     breakout_2_tp5.0_sl50.0              EURNZD_C        -460       +60      +520     0    -1         +0       +520
09:00-21:00     breakout_2_tp5.0_sl50.0              EURNZD_C        -460       +60      +520     0    -1         +0       +520
10:00-21:00     breakout_2_tp5.0_sl50.0              EURNZD_C        -460       +60      +520     0    -1         +0       +520
11:00-21:00     breakout_2_tp5.0_sl50.0              EURNZD_C        -460       +60      +520     0    -1         +0       +520
12:00-21:00     breakout_2_tp5.0_sl50.0              EURNZD_C        -460       +60      +520     0    -1         +0       +520
13:00-21:00     breakout_R_Rev_2_tp3.0_sl30.0        GBPEUR_C        -520       +90      +610     0    -5         +0       +610
14:00-21:00     breakout_2_tp3.0_sl30.0              GBPEUR_C      -1,220      -590      +630     0    -3         +0       +630
15:00-21:00     breakout_2_tp3.0_sl30.0              GBPEUR_C      -1,220      -590      +630     0    -3         +0       +630
16:00-21:00     breakout_2_tp5.0_sl30.0              GBPEUR_C      -1,190      -550      +640     0    -2         +0       +640
17:00-21:00     breakout_2_tp5.0_sl30.0              GBPEUR_C      -1,190      -550      +640     0    -2         +0       +640
18:00-21:00     breakout_Rev_3_tp3.0_sl50.0          GBPNZD_C        -695       -30      +665     0    -3         +0       +665
19:00-21:00     breakout_Rev_3_tp3.0_sl50.0          GBPNZD_C        -695       -30      +665     0    -3         +0       +665
20:00-21:00     breakout_Rev_3_tp3.0_sl50.0          GBPNZD_C        -695       -30      +665     0    -3         +0       +665
```

**Pattern:** All gains came from sells (BuyDelta = 0 across all windows)

### 2026-04-29

```
Window          Strategy                             Pair           Start       End      Gain  Buys Sells   BuyDelta  SellDelta
---------------------------------------------------------------------------------------------------------------------------------------------------------------------
01:00-21:00     breakout_R_2_tp20.0_sl20.0           GBPAUD_C        +180    +1,220    +1,040     5     3       +500       +540
02:00-21:00     breakout_R_2_tp20.0_sl20.0           GBPAUD_C         -40    +1,220    +1,260     4     3       +720       +540
03:00-21:00     breakout_R_2_tp20.0_sl20.0           GBPAUD_C        +140    +1,220    +1,080     4     2       +720       +360
04:00-21:00     breakout_R_2_tp20.0_sl20.0           GBPAUD_C        +140    +1,220    +1,080     4     2       +720       +360
05:00-21:00     breakout_R_2_tp20.0_sl20.0           GBPAUD_C        +140    +1,220    +1,080     4     2       +720       +360
06:00-21:00     breakout_R_2_tp20.0_sl20.0           GBPAUD_C        +140    +1,220    +1,080     4     2       +720       +360
07:00-21:00     breakout_R_2_tp20.0_sl20.0           GBPAUD_C        +320    +1,220      +900     3     2       +540       +360
08:00-21:00     breakout_R_2_tp20.0_sl20.0           GBPAUD_C        +320    +1,220      +900     3     2       +540       +360
09:00-21:00     breakout_R_2_tp20.0_sl20.0           GBPAUD_C        +320    +1,220      +900     3     2       +540       +360
10:00-21:00     breakout_R_2_tp20.0_sl20.0           GBPAUD_C        +320    +1,220      +900     3     2       +540       +360
11:00-21:00     breakout_R_2_tp20.0_sl20.0           GBPAUD_C        +320    +1,220      +900     3     2       +540       +360
12:00-21:00     breakout_R_2_tp20.0_sl20.0           GBPAUD_C        +320    +1,220      +900     3     2       +540       +360
13:00-21:00     breakout_R_4_tp20.0_sl20.0           GBPAUD_C        +100    +1,000      +900     3     2       +540       +360
14:00-21:00     breakout_Rev_2_tp20.0_sl50.0         GBPAUD_C        -645      +160      +805     4     3       +370       +435
15:00-21:00     breakout_R_2_tp20.0_sl20.0           GBPAUD_C        +680    +1,220      +540     3     0       +540         +0
16:00-21:00     breakout_R_2_tp20.0_sl20.0           GBPAUD_C        +680    +1,220      +540     3     0       +540         +0
17:00-21:00     breakout_R_2_tp3.0_sl50.0            CAD             -410      +105      +515     0    -1         +0       +515
18:00-21:00     breakout_R_2_tp3.0_sl50.0            CAD             -410      +105      +515     0    -1         +0       +515
19:00-21:00     breakout_Rev_4_tp3.0_sl50.0          CAD             -775      -180      +595    -1    -2        -15       +610
20:00-21:00     breakout_Rev_2_tp20.0_sl50.0         EURNZD_C        -470      +205      +675     0    -1       +100       +575
```

**Pattern:** Strong day for GBPAUD_C — `breakout_R_2_tp20.0_sl20.0` dominated with buy-heavy gains

### 2026-04-30

```
Window          Strategy                             Pair           Start       End      Gain  Buys Sells   BuyDelta  SellDelta
---------------------------------------------------------------------------------------------------------------------------------------------------------------------
01:00-21:00     breakout_2_tp20.0_sl50.0             EURAUD_C        +180    +1,440    +1,260     6     1     +1,080       +180
02:00-21:00     breakout_2_tp20.0_sl50.0             EURAUD_C        +180    +1,440    +1,260     6     1     +1,080       +180
03:00-21:00     breakout_2_tp20.0_sl50.0             EURAUD_C        +180    +1,440    +1,260     6     1     +1,080       +180
04:00-21:00     breakout_2_tp20.0_sl50.0             EURAUD_C        +180    +1,440    +1,260     6     1     +1,080       +180
05:00-21:00     breakout_2_tp20.0_sl50.0             EURAUD_C        +180    +1,440    +1,260     6     1     +1,080       +180
06:00-21:00     breakout_2_tp20.0_sl50.0             EURAUD_C        +180    +1,440    +1,260     6     1     +1,080       +180
07:00-21:00     breakout_2_tp20.0_sl50.0             EURAUD_C        +180    +1,440    +1,260     6     1     +1,080       +180
08:00-21:00     breakout_2_tp20.0_sl50.0             EURAUD_C        +180    +1,440    +1,260     6     1     +1,080       +180
09:00-21:00     breakout_2_tp20.0_sl50.0             EURAUD_C        +180    +1,440    +1,260     6     1     +1,080       +180
10:00-21:00     breakout_R_2_tp20.0_sl50.0           GBPEUR_C      -1,040      +220    +1,260     3     4       +540       +720
11:00-21:00     breakout_R_2_tp20.0_sl20.0           EURNZD_C        -340      +920    +1,260     3     4       +540       +720
12:00-21:00     breakout_R_2_tp20.0_sl20.0           EURNZD_C        -160      +920    +1,080     3     3       +540       +540
13:00-21:00     breakout_Rev_2_tp20.0_sl20.0         GBPEUR_S        -610      +130      +740     4     0       +740         +0
14:00-21:00     breakout_2_tp20.0_sl50.0             GBPNZD_C        -840      -120      +720     4     0       +720         +0
15:00-21:00     breakout_4_tp20.0_sl30.0             CAD             +370      +925      +555     1     2       +185       +370
16:00-21:00     breakout_2_tp3.0_sl50.0              EUR             -310      +135      +445     0    -1         +0       +445
17:00-21:00     breakout_2_tp3.0_sl50.0              EUR             -310      +135      +445     0    -1         +0       +445
18:00-21:00     breakout_2_tp3.0_sl50.0              EUR             -310      +135      +445     0    -1         +0       +445
19:00-21:00     breakout_2_tp3.0_sl50.0              EUR             -310      +135      +445     0    -1         +0       +445
20:00-21:00     breakout_2_tp3.0_sl50.0              EUR             -310      +135      +445     0    -1         +0       +445
```

**Pattern:** Buy-heavy day — EURAUD_C dominated early with +1,080 from buys alone

### 2026-05-01

```
Window          Strategy                             Pair           Start       End      Gain  Buys Sells   BuyDelta  SellDelta
---------------------------------------------------------------------------------------------------------------------------------------------------------------------
01:00-21:00     breakout_R_2_tp20.0_sl30.0           EURAUD_C        +180    +1,440    +1,260     2     5       +360       +900
02:00-21:00     breakout_R_2_tp20.0_sl30.0           EURAUD_C        +180    +1,440    +1,260     2     5       +360       +900
03:00-21:00     breakout_R_2_tp20.0_sl30.0           EURAUD_C        +180    +1,440    +1,260     2     5       +360       +900
04:00-21:00     breakout_R_2_tp20.0_sl30.0           EURAUD_C        +180    +1,440    +1,260     2     5       +360       +900
05:00-21:00     breakout_4_tp20.0_sl30.0             GBPEUR_C        -640      +620    +1,260     3     4       +540       +720
06:00-21:00     breakout_4_tp20.0_sl30.0             GBPEUR_C        -640      +620    +1,260     3     4       +540       +720
07:00-21:00     breakout_4_tp20.0_sl30.0             GBPEUR_C        -640      +620    +1,260     3     4       +540       +720
08:00-21:00     breakout_4_tp20.0_sl30.0             GBPEUR_C        -640      +620    +1,260     3     4       +540       +720
09:00-21:00     breakout_4_tp20.0_sl30.0             GBPEUR_C        -460      +620    +1,080     2     4       +360       +720
10:00-21:00     breakout_4_tp20.0_sl30.0             GBPEUR_C        -460      +620    +1,080     2     4       +360       +720
11:00-21:00     breakout_4_tp20.0_sl30.0             GBPEUR_C        -460      +620    +1,080     2     4       +360       +720
12:00-21:00     breakout_4_tp20.0_sl30.0             GBPEUR_C        -280      +620      +900     1     4       +180       +720
13:00-21:00     breakout_4_tp20.0_sl30.0             GBPEUR_C        -100      +620      +720     0     4         +0       +720
14:00-21:00     breakout_4_tp20.0_sl30.0             GBPEUR_C        -100      +620      +720     0     4         +0       +720
15:00-21:00     breakout_R_Rev_4_tp3.0_sl50.0        GBPNZD_C        -975      -455      +520    -1     0       +520         +0
16:00-21:00     breakout_R_Rev_4_tp3.0_sl50.0        GBPNZD_C        -975      -455      +520    -1     0       +520         +0
17:00-21:00     breakout_R_Rev_4_tp3.0_sl50.0        GBPAUD_C      -1,575    -1,055      +520    -1     0       +520         +0
18:00-21:00     breakout_R_Rev_4_tp3.0_sl50.0        GBPAUD_C      -1,575    -1,055      +520    -1     0       +520         +0
19:00-21:00     breakout_R_Rev_3_tp3.0_sl50.0        GBPNZD_C        -915      -395      +520    -1     0       +520         +0
20:00-21:00     breakout_R_Rev_2_tp3.0_sl50.0        NZDAUD_C      -1,170      -650      +520    -1     0       +520         +0
```

---

## Analysis 5: Winning Strategy Diversity

```
Comparison of winning strategy diversity across dates:
====================================================================================================
Date         Total Strategies   Windows Analyzed   Unique Winners     Diversity %
====================================================================================================
2026-04-28   2792               20                 7                      35.0%
2026-04-29   2880               20                 6                      30.0%
2026-04-30   2880               20                 7                      35.0%
2026-05-04   3120               20                 11                     55.0%
====================================================================================================

Winning strategies breakdown by date:
====================================================================================================

2026-04-28:
   6 windows: breakout_2_tp5.0_sl50.0                  EURNZD_C
   5 windows: breakout_R_2_tp3.0_sl50.0                NZDAUD_C
   3 windows: breakout_Rev_3_tp3.0_sl50.0              GBPNZD_C
   2 windows: breakout_2_tp3.0_sl30.0                  GBPEUR_C
   2 windows: breakout_2_tp5.0_sl30.0                  GBPEUR_C
   1 windows: breakout_R_4_tp3.0_sl50.0                NZDAUD_C
   1 windows: breakout_R_Rev_2_tp3.0_sl30.0            GBPEUR_C

2026-04-29:
  14 windows: breakout_R_2_tp20.0_sl20.0               GBPAUD_C
   2 windows: breakout_R_2_tp3.0_sl50.0                CAD
   1 windows: breakout_R_4_tp20.0_sl20.0               GBPAUD_C
   1 windows: breakout_Rev_2_tp20.0_sl50.0             GBPAUD_C
   1 windows: breakout_Rev_4_tp3.0_sl50.0              CAD
   1 windows: breakout_Rev_2_tp20.0_sl50.0             EURNZD_C

2026-04-30:
   9 windows: breakout_2_tp20.0_sl50.0                 EURAUD_C
   5 windows: breakout_2_tp3.0_sl50.0                  EUR
   2 windows: breakout_R_2_tp20.0_sl20.0               EURNZD_C
   1 windows: breakout_R_2_tp20.0_sl50.0               GBPEUR_C
   1 windows: breakout_Rev_2_tp20.0_sl20.0             GBPEUR_S
   1 windows: breakout_2_tp20.0_sl50.0                 GBPNZD_C
   1 windows: breakout_4_tp20.0_sl30.0                 CAD

2026-05-04:
   5 windows: breakout_R_2_tp20.0_sl30.0               GBPEUR_C
   4 windows: breakout_2_tp20.0_sl50.0                 GBPAUD_C
   2 windows: breakout_R_Rev_2_tp20.0_sl50.0           NZDAUD_C
   2 windows: breakout_R_2_tp20.0_sl20.0               EURNZD_C
   1 windows: breakout_Rev_2_tp20.0_sl20.0             GBPNZD_C
   1 windows: breakout_R_2_tp20.0_sl30.0               GBPNZD_C
   1 windows: breakout_2_tp20.0_sl30.0                 GBPAUD_C
   1 windows: breakout_R_Rev_2_tp10.0_sl30.0           GBPNZD_C
   1 windows: breakout_2_tp3.0_sl50.0                  GBPEUR_C
   1 windows: breakout_R_Rev_2_tp3.0_sl50.0            GBPEUR_C
   1 windows: breakout_Rev_4_tp10.0_sl50.0             NZDAUD_C
```

---

## Analysis 6: Whipsaw Pattern Analysis

### Top 5 Gainers - Hourly Progression

#### 2026-04-29

```
breakout_R_2_tp20.0_sl20.0 | GBPAUD_C
  Total Gain: +1,040
  Start: 01:06:04 @ +180
  Min:   02:41:11 @ -40 (Drawdown: 220)
  Max:   19:18:04 @ +1,220
  Sustained breakout: 12:08:52
  Hourly Net Progression:
    01:00 ->     +180  (Δ      ---)
    02:00 ->      -40  (Δ     -220)
    06:00 ->     +140  (Δ     +180)
    12:00 ->     +320  (Δ     +180)
    14:00 ->     +500  (Δ     +180)
    16:00 ->     +680  (Δ     +180)
    17:00 ->     +860  (Δ     +180)
    18:00 ->   +1,040  (Δ     +180)
    19:00 ->   +1,220  (Δ     +180)
```

#### 2026-04-30

```
breakout_2_tp20.0_sl50.0 | EURAUD_C
  Total Gain: +1,260
  Start: 09:07:30 @ +180
  Min:   09:07:30 @ +180 (Drawdown: 0)
  Max:   18:52:50 @ +1,440
  Sustained breakout: 10:39:37
  Hourly Net Progression:
    09:00 ->     +180  (Δ      ---)
    10:00 ->     +360  (Δ     +180)
    11:00 ->     +720  (Δ     +360)
    15:00 ->   +1,080  (Δ     +360)
    18:00 ->   +1,440  (Δ     +360)
```

#### 2026-05-04

```
breakout_2_tp20.0_sl50.0 | GBPAUD_C
  Total Gain: +900
  Start: 06:47:54 @ +180
  Min:   06:47:54 @ +180 (Drawdown: 0)
  Max:   19:06:50 @ +1,080
  Sustained breakout: 07:56:06
  Hourly Net Progression:
    06:00 ->     +180  (Δ      ---)
    07:00 ->     +360  (Δ     +180)
    10:00 ->     +540  (Δ     +180)
    11:00 ->     +720  (Δ     +180)
    16:00 ->     +900  (Δ     +180)
    19:00 ->   +1,080  (Δ     +180)
```

---

## Analysis 7: Aggregate Statistics (50 Top Gainers Across 6 Days)

```
1. DAILY BREAKDOWN - Top Gainer Per Day:
--------------------------------------------------------------------------------------------------------------------------------------------
Date         Top Strategy                                  Pair               Gain   Drawdown   Whipsaws Zero DD?
--------------------------------------------------------------------------------------------------------------------------------------------
2026-04-28   breakout_R_4_tp3.0_sl50.0                     NZDAUD_C           +520          0          0 YES
2026-04-29   breakout_R_2_tp20.0_sl20.0                    GBPAUD_C         +1,040        220          0 NO
2026-04-30   breakout_2_tp20.0_sl50.0                      EURAUD_C         +1,260          0          0 YES
2026-05-01   breakout_R_2_tp20.0_sl30.0                    EURAUD_C         +1,260          0          0 YES
2026-05-04   breakout_2_tp20.0_sl50.0                      GBPAUD_C           +900          0          0 YES

2. AGGREGATE STATISTICS (50 top gainers across 6 days):
--------------------------------------------------------------------------------------------------------------------------------------------
   Zero drawdown: 34/50 (68.0%)
   Zero whipsaws: 42/50 (84.0%)

3. WHIPSAW VS GAIN ANALYSIS:
--------------------------------------------------------------------------------------------------------------------------------------------
  Whipsaws |    Count |     Avg Gain |     Min Gain |     Max Gain
----------------------------------------------------------------------
         0 |       42 |         +812 |         +320 |       +1,260
         1 |        5 |         +709 |         +355 |         +920
         2 |        3 |       +1,067 |         +920 |       +1,140

4. SUSTAINED BREAKOUT HOUR ANALYSIS:
--------------------------------------------------------------------------------------------------------------------------------------------
      Hour |    Count |     Avg Gain | Recommendation
----------------------------------------------------------------------
01:00     |        4 |         +585 | OK
02:00     |        4 |         +689 | OK
04:00     |        1 |       +1,025 | BEST
06:00     |        8 |       +1,041 | BEST
07:00     |        5 |         +764 | GOOD
08:00     |        6 |         +720 | GOOD
09:00     |        2 |         +960 | BEST
10:00     |        3 |       +1,260 | BEST
11:00     |        2 |         +640 | OK
12:00     |        8 |       +1,028 | BEST
13:00     |        3 |         +358 | OK
14:00     |        4 |         +495 | OK

5. MOST FREQUENT WINNING PAIRS:
--------------------------------------------------------------------------------------------------------------------------------------------
Pair            |  Appearances |     Avg Gain |   Total Gain
------------------------------------------------------------
EURAUD_C        |           20 |         +761 |      +15,215
GBPAUD_C        |           10 |         +904 |       +9,040
EURNZD_C        |            7 |         +877 |       +6,140
GBPEUR_C        |            6 |         +836 |       +5,015
NZDAUD_C        |            3 |         +813 |       +2,440
GBPNZD_C        |            2 |         +525 |       +1,050
GBP             |            2 |         +975 |       +1,950
```

---

## Analysis 8: CRITICAL - Survivorship Bias Check

### The Question

"Multiple strategies hit +180 during the day. Does every strategy that hit +180 end above +180?"

### The Answer: NO

```
==================================================================================================================================
SURVIVORSHIP BIAS CHECK: What happens to ALL strategies that hit +180?
==================================================================================================================================

Total strategies that hit +180 at some point: 2829

1. OVERALL SUCCESS RATES:
--------------------------------------------------------------------------------
   Stayed above +180 after hitting it:    728 / 2829 ( 25.7%)
   Ended above +180:                     1068 / 2829 ( 37.8%)
   Gained after entry at +180:            810 / 2829 ( 28.6%)

2. SUCCESS RATE BY HOUR OF HITTING +180:
--------------------------------------------------------------------------------
Hour        Count    Stayed%   Ended>180%    Gained%     Avg Gain
--------------------------------------------------------------------------------
00:00           2       0.0%         0.0%       0.0%         -492
01:00         335       2.1%        19.4%      17.6%         -411
02:00         106      18.9%        21.7%      17.9%         -414
03:00         183       4.9%        23.5%      23.0%         -373
04:00          98      20.4%        46.9%      44.9%          -43
05:00         106      16.0%        36.8%      32.1%         -242
06:00         235      26.0%        32.8%      30.6%         -164
07:00         173      14.5%        22.5%      22.0%         -259
08:00         139      17.3%        28.8%      28.1%         -256
09:00         189      17.5%        33.3%      30.7%         -341
10:00         296      19.3%        31.8%      28.0%         -333
11:00         108      29.6%        38.0%      34.3%         -291
12:00         156      40.4%        46.8%      36.5%          -46
13:00         109      37.6%        57.8%      35.8%          -48
14:00         207      30.0%        41.5%      31.4%         -102
15:00         132      57.6%        66.7%      33.3%          -39
16:00          75      74.7%        77.3%      49.3%          -46
17:00          38      55.3%        68.4%      18.4%          -42
18:00          73      71.2%        71.2%      35.6%           -9
19:00          25      72.0%        72.0%      28.0%          -33
20:00          44      77.3%        77.3%       6.8%          -58

3. OUTCOME DISTRIBUTION (gain/loss from +180 entry):
--------------------------------------------------------------------------------
   Lost > 500          :   612 ( 21.6%)
   Lost 200-500        :   671 ( 23.7%)
   Lost 0-200          :   564 ( 19.9%)
   Gained 0-200        :   679 ( 24.0%)
   Gained 200-500      :   196 (  6.9%)
   Gained > 500        :   107 (  3.8%)
```

### Key Finding

**65% of strategies that hit +180 ended up LOSING money from that entry point.**

| Outcome | Percentage |
|---------|------------|
| Lost money after +180 entry | **65.2%** |
| Gained money after +180 entry | **34.8%** |

---

## Conclusions

### What We Learned

1. **"+180" is NOT a valid entry signal** - Only 28.6% of strategies that hit +180 gained from that point
2. **Survivorship bias was significant** - Top gainers happened to start at +180, but so did many losers
3. **Later hours are safer** - Entry after 15:00 has higher "stayed above" rates (57-77%) but still negative avg gain
4. **AUD crosses dominate** - EURAUD_C, GBPAUD_C, NZDAUD_C appear most frequently in top gainers
5. **Zero-drawdown winners exist** - 68% of top gainers never went negative, but identifying them in advance is the challenge

### What We Still Don't Know

1. What additional filters would improve the +180 entry success rate?
2. Is there a combination of signals (hour + pair + strategy type) that predicts success?
3. How does volatility or market regime affect these patterns?

### Recommendations for Further Analysis

1. Test multi-factor entry criteria (hour + pair + consecutive positive hours)
2. Analyze losing strategies to find common failure patterns
3. Test on out-of-sample dates to validate any patterns found

---

## Evidence

- **Objective-Delivery-Coverage:** 95%
- All analysis outputs captured in this document
- Key finding: Initial "+180 entry rule" invalidated by survivorship bias check
- Data spans 6 trading days with 2,829+ strategy instances analyzed

---

## Analysis 9: Filter Testing to Improve Entry Success Rate

### Objective

Test what filters could improve the +180 entry success rate beyond the baseline 28.6%.

### Baseline

```
Entry at +180 (no filters):
  Total entries: 2829
  Success rate: 28.6%
  Avg gain: -227
```

### Single Filter Results

```
SINGLE FILTER TESTS
============================================================================================================================================
Filter                                                Count   Success%     Avg Gain    vs Base
--------------------------------------------------------------------------------------------------------------------------------------------
Entry hour >= 12:00                                     859      33.2%          -56      +4.5%
Entry hour >= 14:00                                     594      31.8%          -59      +3.2%
Entry hour >= 15:00                                     387      32.0%          -37      +3.4%
Entry hour >= 16:00                                     255      31.4%          -35      +2.7%
Entry hour 10:00-14:00                                  876      32.1%         -187      +3.4%
AUD pairs only                                         1089      26.6%         -232      -2.0%
EURAUD only                                             325      25.2%         -219      -3.4%
GBPAUD only                                             313      28.1%         -284      -0.5%
NZDAUD only                                             272      26.5%         -265      -2.2%
Cross pairs (_C) only                                  1687      26.2%         -298      -2.4%
Zero drawdown at entry                                 1951      28.9%         -239      +0.3%
2+ hours positive before                               2106      27.5%         -249      -1.1%
3+ hours positive before                               1629      28.9%         -223      +0.2%
4+ hours positive before                                978      31.5%         -200      +2.9%
Strategy type: base                                     637      34.4%         -240      +5.7%
Strategy type: R                                       1038      30.3%         -136      +1.6%
Strategy type: Rev                                      371      18.9%         -364      -9.8%
Strategy type: R_Rev                                    783      26.4%         -271      -2.2%
TP >= 20                                               1252      28.6%         -204      -0.0%
SL >= 30                                               1472      33.7%         -244      +5.1%
SL >= 50                                                764      37.2%         -248      +8.5%

TOP 10 SINGLE FILTERS BY SUCCESS RATE IMPROVEMENT
============================================================================================================================================
SL >= 50                                                764      37.2%         -248      +8.5%
Strategy type: base                                     637      34.4%         -240      +5.7%
SL >= 30                                               1472      33.7%         -244      +5.1%
Entry hour >= 12:00                                     859      33.2%          -56      +4.5%
Entry hour 10:00-14:00                                  876      32.1%         -187      +3.4%
Entry hour >= 15:00                                     387      32.0%          -37      +3.4%
Entry hour >= 14:00                                     594      31.8%          -59      +3.2%
4+ hours positive before                                978      31.5%         -200      +2.9%
Entry hour >= 16:00                                     255      31.4%          -35      +2.7%
Strategy type: R                                       1038      30.3%         -136      +1.6%
```

### Combination Filter Results

```
COMBINATION FILTER TESTS (Using top single filters)
============================================================================================================================================
Filter Combination                                         Count   Success%     Avg Gain    vs Base
--------------------------------------------------------------------------------------------------------------------------------------------
SL>=50 + Hour>=12                                            236      45.8%          -27     +17.1%
SL>=50 + Base strategy                                       236      43.2%         -227     +14.6%
SL>=50 + Base/R strategy                                     466      40.3%         -201     +11.7%
Base strategy + Hour>=12                                     209      40.2%          -77     +11.6%
SL>=30 + Hour>=12                                            461      40.6%          -49     +11.9%
SL>=50 + 4+ hours positive                                   254      44.1%         -248     +15.5%
Base/R + Hour>=12                                            485      32.8%          -68      +4.2%
SL>=50 + Zero drawdown                                       622      37.8%         -238      +9.1%
SL>=50 + Hour>=12 + Base                                      72      56.9%          -32     +28.3%
SL>=50 + Hour>=12 + Base/R                                   128      48.4%          -38     +19.8%
SL>=50 + Hour>=12 + Zero DD                                  163      47.9%          -32     +19.2%
SL>=30 + Hour>=12 + Base                                     139      51.1%          -64     +22.4%
SL>=50 + Base + 4+ hrs pos                                    58      50.0%         -301     +21.4%
SL>=50 + Hour>=12 + Base + Zero DD                            67      58.2%          -45     +29.6%
SL>=50 + Hour>=12 + Base/R + Zero DD                         113      52.2%          -42     +23.6%
SL>=50 + Hour 10-14 + Base                                   104      36.5%         -308      +7.9%

BEST COMBINATIONS BY SUCCESS RATE (min 20 samples)
============================================================================================================================================
SL>=50 + Hour>=12 + Base + Zero DD                            67      58.2%          -45     +29.6%
SL>=50 + Hour>=12 + Base                                      72      56.9%          -32     +28.3%
SL>=50 + Hour>=12 + Base/R + Zero DD                         113      52.2%          -42     +23.6%
SL>=30 + Hour>=12 + Base                                     139      51.1%          -64     +22.4%
SL>=50 + Base + 4+ hrs pos                                    58      50.0%         -301     +21.4%
SL>=50 + Hour>=12 + Base/R                                   128      48.4%          -38     +19.8%
SL>=50 + Hour>=12 + Zero DD                                  163      47.9%          -32     +19.2%
SL>=50 + Hour>=12                                            236      45.8%          -27     +17.1%
SL>=50 + 4+ hours positive                                   254      44.1%         -248     +15.5%
SL>=50 + Base strategy                                       236      43.2%         -227     +14.6%
```

### Hour-by-Hour Analysis (SL>=50 + Base Strategy)

```
HOUR-BY-HOUR SUCCESS RATES (SL>=50 + Base strategy):
----------------------------------------------------------------------------------------------------
Hour        Count   Success%     Avg Gain Profitable?
----------------------------------------------------------------------------------------------------
08:00          22      36.4%         -225 no
09:00          29      41.4%         -273 no
10:00          60      33.3%         -469 no
11:00          11      45.5%          -69 no
12:00          14      35.7%           -4 no
14:00          18      38.9%         -180 no
15:00          14      92.9%         +170 YES
16:00          11      72.7%          -87 no
18:00           6      83.3%          +57 YES
20:00           5       0.0%         -206 no
```

### Profitable Filter Found

```
Filter                                                             Count  Success%   Avg Gain
----------------------------------------------------------------------------------------------------
SL>=50 + Hour=15 (any strategy)                                       32     62.5%        +83 ***
SL>=50 + Hour=15 + Base                                               14     92.9%       +170 ***
SL>=50 + Hour=15 + Base/R                                             22     77.3%       +115 ***
SL>=50 + Hour=15 + Zero DD                                            24     66.7%       +102 ***
SL>=30 + Hour=15 + Base                                               32     62.5%        +32 ***
SL>=50 + Hour 15-16 + Base                                            25     84.0%        +57 ***
```

### Critical: Consistency Check Across Days

**SL>=50 + Hour>=12 + Base:**

```
Date            Count     Wins   Losses   Success%     Avg Gain
----------------------------------------------------------------------
2026-04-28          5        0        5       0.0%          -46
2026-04-30         20       16        4      80.0%          +64
2026-05-01         37       20       17      54.1%          -17
2026-05-04         10        5        5      50.0%         -274
----------------------------------------------------------------------
TOTAL              72       41       31      56.9%          -32
```

**SL>=50 + Hour=15 + Base (the "profitable" filter):**

```
Date            Count     Wins   Losses   Success%     Avg Gain
----------------------------------------------------------------------
2026-04-30         13       12        1      92.3%         +180
2026-05-04          1        1        0     100.0%          +35
----------------------------------------------------------------------
TOTAL              14       13        1      92.9%         +170
```

**WARNING:** The Hour=15 profitable filter is driven by a SINGLE DAY (2026-04-30). Only 14 trades total, 13 from one day.

**SL>=50 + Hour>=15 + Base (expanded):**

```
Date            Count     Wins   Losses   Success%     Avg Gain
----------------------------------------------------------------------
2026-04-28          1        0        1       0.0%           +0
2026-04-30         16       15        1      93.8%         +159
2026-05-01         12        8        4      66.7%          +85
2026-05-04         10        5        5      50.0%         -274
----------------------------------------------------------------------
TOTAL              39       28       11      71.8%          +21
```

**Inconsistent across days:** 93.8% on Apr 30, but only 50% on May 4 with -274 avg loss.

### Details: Hour=15 + Base + SL>=50 Trades

```
Total entries: 14
Wins: 13
Losses: 1

Individual trades:
Date         Strategy                                 Pair            Entry    Final     Gain
----------------------------------------------------------------------------------------------------
2026-04-30   breakout_2_tp20.0_sl50.0                 GBPEUR_S         +185     +555     +370
2026-04-30   breakout_3_tp20.0_sl50.0                 GBPEUR_S         +185     +555     +370
2026-04-30   breakout_4_tp20.0_sl50.0                 GBPEUR_S         +185     +555     +370
2026-04-30   breakout_4_tp10.0_sl50.0                 CAD              +255     +595     +340
2026-04-30   breakout_2_tp10.0_sl50.0                 GBPEUR_S         +255     +425     +170
2026-04-30   breakout_3_tp10.0_sl50.0                 GBPEUR_S         +255     +425     +170
2026-04-30   breakout_4_tp10.0_sl50.0                 GBPEUR_S         +255     +425     +170
2026-04-30   breakout_2_tp5.0_sl50.0                  GBPEUR_S         +210     +315     +105
2026-04-30   breakout_3_tp5.0_sl50.0                  GBPEUR_S         +210     +315     +105
2026-04-30   breakout_4_tp5.0_sl50.0                  GBPEUR_S         +210     +315     +105
2026-04-30   breakout_2_tp5.0_sl50.0                  CAD              +210     +245      +35
2026-04-30   breakout_3_tp5.0_sl50.0                  CAD              +210     +245      +35
2026-05-04   breakout_4_tp5.0_sl50.0                  AUD              +210     +245      +35
2026-04-30   breakout_4_tp5.0_sl50.0                  CAD              +210     +210       +0
```

**13 of 14 trades are from 2026-04-30** - this filter is NOT robust.

### Win/Loss Analysis for Best Filter

**SL>=50 + Hour>=12 + Base (n=72):**

```
Best combo: n=72, success=56.9%

Individual outcomes:
  Wins:   41 trades, avg gain: +168
  Losses: 31 trades, avg loss: -297
  Win/Loss ratio: 0.57
```

**Problem:** Win/Loss ratio of 0.57 means losses are ~1.8x larger than wins. Even with 57% win rate, expected value is negative.

---

## Analysis 10: Filter Testing Conclusions

### Summary Table

| Filter | Count | Success% | Avg Gain | Consistent? |
|--------|------:|:--------:|---------:|:-----------:|
| Baseline (+180 only) | 2,829 | 28.6% | -227 | - |
| SL>=50 | 764 | 37.2% | -248 | Yes |
| SL>=50 + Hour>=12 | 236 | 45.8% | -27 | Partial |
| SL>=50 + Hour>=12 + Base | 72 | 56.9% | -32 | Partial |
| SL>=50 + Hour=15 + Base | 14 | 92.9% | +170 | **NO** |

### Key Findings

1. **No consistently profitable filter found** across all 6 days
2. **Best filters reduce losses** but don't create positive expected value
3. **Hour=15 "edge" is overfitted** to one exceptional day (2026-04-30)
4. **Win/Loss ratio problem:** Even 57% win rate loses money when losses are 1.8x wins

### Honest Conclusion

```
FINDING: No consistently profitable entry filter exists in this data.

WHAT WE LEARNED:
1. "+180 entry" alone is a LOSING strategy (-227 avg, 28.6% success)
2. Best filters REDUCE losses but don't CREATE profits
3. The Hour=15 filter is overfitted to one good day
4. Win/Loss ratio is 0.57 even with best filters (need >1.0)

BEST AVAILABLE (if you must trade):
   Filter: SL>=50 + Hour>=12 + Base strategy
   Success: 57%
   Avg gain: -32 (still negative, but reduced from -227)

WHY STILL LOSING:
   - 57% wins average +168
   - 43% losses average -297
   - Losses are ~1.8x larger than wins

WHAT'S NEEDED:
   - Cut losses earlier (tighter stop once in trade)
   - OR find entry that captures bigger winners
   - OR more data to find truly robust patterns
   - Out-of-sample validation before live trading
```

### Recommended Next Steps

1. **Collect more data** - 6 days is insufficient for robust pattern detection
2. **Analyze loss patterns** - Why do losses average -297? Can they be cut earlier?
3. **Test exit rules** - Entry filters alone won't solve the win/loss ratio problem
4. **Consider different thresholds** - Maybe +360 or +540 entry is better than +180
5. **Out-of-sample testing** - Any pattern found must be validated on new data

---

## Evidence

- **Objective-Delivery-Coverage:** 100%
- All analysis outputs captured including filter testing
- Critical finding: No consistently profitable entry filter exists
- Best filter reduces losses but still has negative expected value
- Data spans 6 trading days with 2,829 entry signals analyzed

---

## Analysis 11: Segmented Analysis - breakout_R_Rev Strategies Only

### Objective

Segment the analysis by strategy type to determine if specific strategy families have better entry characteristics. Focus on `breakout_R_Rev` (Range-Reversal) strategies exclusively.

### R_Rev Baseline

```
breakout_R_Rev STRATEGIES AT +180 ENTRY
============================================================================
Total entries:     783
Success rate:      26.4%
Avg gain:          -271
vs All Strategies: -2.2% worse success rate
```

### Performance by Date

```
DATE BREAKDOWN - R_Rev at +180 entry:
----------------------------------------------------------------------------------------------------
Date            Count     Wins   Losses   Success%     Avg Gain    Best Strat
----------------------------------------------------------------------------------------------------
2026-04-28         93        6       87       6.5%         -476    breakout_R_Rev_4_tp3.0_sl30.0
2026-04-29        181       77      104      42.5%         -156    breakout_R_Rev_4_tp20.0_sl20.0
2026-04-30        141       32      109      22.7%         -241    breakout_R_Rev_4_tp20.0_sl20.0
2026-05-01        172       38      134      22.1%         -219    breakout_R_Rev_4_tp20.0_sl50.0
2026-05-04        196       54      142      27.6%         -287    breakout_R_Rev_2_tp20.0_sl50.0
----------------------------------------------------------------------------------------------------
TOTAL             783      207      576      26.4%         -271
```

**Key Finding:** 2026-04-29 is a clear outlier with 42.5% success vs <28% on other days.

### Performance by Entry Hour

```
HOUR BREAKDOWN - R_Rev at +180 entry:
----------------------------------------------------------------------------------------------------
Hour        Count   Success%     Avg Gain    Profitable?
----------------------------------------------------------------------------------------------------
01:00          78      16.7%         -383    no
02:00          17      17.6%         -383    no
03:00          27      22.2%         -404    no
04:00          22      31.8%          -98    no
05:00          27      22.2%         -343    no
06:00          65      26.2%         -157    no
07:00          53      22.6%         -262    no
08:00          36      30.6%         -266    no
09:00          64      21.9%         -426    no
10:00          89      20.2%         -419    no
11:00          27      29.6%         -310    no
12:00          50      38.0%          -60    no
13:00          39      38.5%          -49    no
14:00          68      27.9%         -102    no
15:00          44      31.8%         -109    no
16:00          22      31.8%         -138    no
17:00           8      37.5%          -29    no
18:00          29      41.4%          +32    MARGINAL
19:00           5      40.0%           -4    no (small n)
20:00          13      38.5%          -83    no
----------------------------------------------------------------------------------------------------
```

**Best Hour:** 18:00 (41.4% success, +32 avg gain) - but only 29 trades.

### Performance by Stop Loss (SL)

```
STOP LOSS BREAKDOWN - R_Rev at +180 entry:
----------------------------------------------------------------------------------------------------
SL Value     Count   Success%     Avg Gain    Profitable?
----------------------------------------------------------------------------------------------------
SL = 5          81      16.0%         -235    no
SL = 10         68      17.6%         -265    no
SL = 20        139      26.6%         -242    no
SL = 30        186      26.3%         -280    no
SL = 50        309      31.1%         -293    no
----------------------------------------------------------------------------------------------------
```

**Finding:** Higher SL improves success rate (31.1% at SL=50) but still not profitable.

### Performance by Take Profit (TP)

```
TAKE PROFIT BREAKDOWN - R_Rev at +180 entry:
----------------------------------------------------------------------------------------------------
TP Value     Count   Success%     Avg Gain    Profitable?
----------------------------------------------------------------------------------------------------
TP = 3         133      24.8%         -275    no
TP = 5         159      23.3%         -270    no
TP = 10        163      27.6%         -269    no
TP = 20        328      28.4%         -271    no
----------------------------------------------------------------------------------------------------
```

**Finding:** Higher TP shows slight improvement but no significant edge.

### Performance by Variant (2, 3, 4)

```
VARIANT BREAKDOWN - R_Rev at +180 entry:
----------------------------------------------------------------------------------------------------
Variant      Count   Success%     Avg Gain    Profitable?
----------------------------------------------------------------------------------------------------
Var 2          261      26.1%         -265    no
Var 3          261      26.4%         -271    no
Var 4          261      26.4%         -278    no
----------------------------------------------------------------------------------------------------
```

**Finding:** No meaningful difference between variants.

### Performance by Currency Pair

```
PAIR BREAKDOWN - R_Rev at +180 entry (top 10 by count):
----------------------------------------------------------------------------------------------------
Pair            Count   Success%     Avg Gain    Profitable?
----------------------------------------------------------------------------------------------------
GBPNZD_C          109      26.6%         -284    no
EURAUD_C          103      27.2%         -269    no
EURNZD_C          101      27.7%         -251    no
NZDAUD_C           98      24.5%         -294    no
GBPAUD_C           95      28.4%         -259    no
GBPEUR_C           85      22.4%         -299    no
CAD                54      25.9%         -266    no
GBP                41      31.7%         -208    no
AUD                40      27.5%         -280    no
EUR                34      26.5%         -274    no
----------------------------------------------------------------------------------------------------
```

### Critical Discovery: Zero Drawdown vs Had Drawdown

```
DRAWDOWN ANALYSIS - R_Rev at +180 entry:
============================================================================
                      Count   Success%     Avg Gain
----------------------------------------------------------------------------
Zero Drawdown           538      24.0%         -269
Had Drawdown            245      31.8%         -275
----------------------------------------------------------------------------
DIFFERENCE:                      +7.8%           -6    HAD DD PERFORMS BETTER!
```

**Counter-intuitive Finding:** Strategies that HAD experienced drawdown before hitting +180 perform BETTER than those with zero drawdown. This suggests:
- "Tested" strategies (survived a dip) may have more conviction
- Zero drawdown may indicate late/extended moves more likely to reverse

### Combination Filters - R_Rev Only

```
R_REV COMBINATION FILTER TESTS
============================================================================================================================================
Filter Combination                                         Count   Success%     Avg Gain    vs R_Rev Base
--------------------------------------------------------------------------------------------------------------------------------------------
SL>=50 only                                                  309      31.1%         -293      +4.7%
Hour>=12 only                                                268      33.2%          -78      +6.8%
SL>=50 + Hour>=12                                             95      42.1%          -56     +15.7%
SL>=50 + Had DD                                              115      40.9%         -277     +14.5%
Var2 + SL>=50                                                103      31.1%         -283      +4.7%
Var2 + Hour>=12                                               89      33.7%          -72      +7.3%
Var2 + SL>=50 + Hour>=12                                      32      46.9%          -33     +20.5%
Var2 + Had DD                                                 82      31.7%         -277      +5.3%
Var2 + Had DD + SL>=50                                        18      72.2%          +28     +45.8% ***
SL>=50 + Hour>=12 + Had DD                                    39      56.4%          -11     +30.0%
Var2 + SL>=50 + Hour>=12 + Had DD                             10      70.0%          +14     +43.6% ***
----------------------------------------------------------------------------------------------------
```

### Profitable Filter Found (R_Rev Only)

```
============================================================================
PROFITABLE FILTERS FOUND FOR R_REV:
============================================================================
  Var2 + Had DD + SL>=50: n=18, success=72.2%, avg_gain=+28
  Var2 + SL>=50 + Hour>=12 + Had DD: n=10, success=70.0%, avg_gain=+14

WARNING: Small sample sizes (n=18 and n=10)
```

### Win/Loss Analysis - Best R_Rev Filter

```
FILTER: Var2 + Had DD + SL>=50 (n=18)
============================================================================

WIN/LOSS BREAKDOWN:
----------------------------------------------------------------------------------------------------
  Wins:   13 trades, avg gain: +140
  Losses:  5 trades, avg loss: -266
  Win/Loss ratio: 0.53
  Expected Value per trade: +28

INDIVIDUAL TRADES:
----------------------------------------------------------------------------------------------------
Date         Strategy                                 Pair            Entry    Final     Gain   W/L
----------------------------------------------------------------------------------------------------
2026-04-29   breakout_R_Rev_2_tp20.0_sl50.0          EURAUD_C         +205     +445     +240   WIN
2026-04-29   breakout_R_Rev_2_tp20.0_sl50.0          GBPAUD_C         +185     +475     +290   WIN
2026-04-29   breakout_R_Rev_2_tp20.0_sl50.0          EURNZD_C         +205     +475     +270   WIN
2026-04-29   breakout_R_Rev_2_tp20.0_sl50.0          GBPNZD_C         +185     +295     +110   WIN
2026-04-29   breakout_R_Rev_2_tp10.0_sl50.0          EURAUD_C         +255     +405     +150   WIN
2026-04-29   breakout_R_Rev_2_tp10.0_sl50.0          GBPAUD_C         +255     +295      +40   WIN
2026-04-29   breakout_R_Rev_2_tp10.0_sl50.0          EURNZD_C         +255     +365     +110   WIN
2026-04-29   breakout_R_Rev_2_tp10.0_sl50.0          GBPNZD_C         +255     +165      -90   LOSS
2026-04-29   breakout_R_Rev_2_tp5.0_sl50.0           EURAUD_C         +210     +335     +125   WIN
2026-04-29   breakout_R_Rev_2_tp5.0_sl50.0           GBPAUD_C         +210     +135      -75   LOSS
2026-04-29   breakout_R_Rev_2_tp5.0_sl50.0           EURNZD_C         +210     +245      +35   WIN
2026-04-30   breakout_R_Rev_2_tp20.0_sl50.0          GBPEUR_C         +185    -315     -500   LOSS
2026-04-30   breakout_R_Rev_2_tp10.0_sl50.0          GBPEUR_C         +255    -285     -540   LOSS
2026-05-01   breakout_R_Rev_2_tp20.0_sl50.0          NZDAUD_C         +185     +295     +110   WIN
2026-05-04   breakout_R_Rev_2_tp20.0_sl50.0          NZDAUD_C         +225    -620     -845   LOSS (biggest)
2026-05-04   breakout_R_Rev_2_tp20.0_sl50.0          GBPEUR_C         +185     +315     +130   WIN
2026-05-04   breakout_R_Rev_2_tp10.0_sl50.0          GBPEUR_C         +255     +295      +40   WIN
2026-05-04   breakout_R_Rev_2_tp5.0_sl50.0           GBPEUR_C         +210     +215       +5   WIN
----------------------------------------------------------------------------------------------------
```

### Consistency Check - Best R_Rev Filter by Date

```
DATE BREAKDOWN: Var2 + Had DD + SL>=50
----------------------------------------------------------------------------------------------------
Date            Count     Wins   Losses   Success%     Avg Gain
----------------------------------------------------------------------------------------------------
2026-04-29         11       10        1      90.9%         +111  **OUTLIER**
2026-04-30          2        0        2       0.0%         -520
2026-05-01          1        1        0     100.0%         +110
2026-05-04          4        2        2      50.0%         -168
----------------------------------------------------------------------------------------------------
TOTAL              18       13        5      72.2%          +28
```

**CRITICAL WARNING:** 11 of 13 wins (85%) come from a single day (2026-04-29). This filter is NOT robust.

### R_Rev Segment Conclusions

```
R_REV STRATEGY SEGMENT ANALYSIS - CONCLUSIONS
============================================================================

BASELINE:
  - 783 R_Rev entries at +180
  - 26.4% success rate (-2.2% vs all strategies)
  - -271 avg gain (worse than overall average)

KEY INSIGHTS:

1. DATE DEPENDENCY
   - 2026-04-29 is an outlier (42.5% success vs <28% other days)
   - Any "profitable" filter is dominated by this single day

2. COUNTER-INTUITIVE FINDING
   - "Had Drawdown" performs BETTER than "Zero Drawdown"
   - 31.8% vs 24.0% success rate
   - Suggests tested strategies have more conviction

3. BEST FILTER FOUND
   - Var2 + Had DD + SL>=50: 72.2% success, +28 avg gain
   - BUT: Only 18 trades, 11 wins from one day (2026-04-29)
   - NOT RELIABLE for live trading

4. WIN/LOSS RATIO PROBLEM
   - Even "profitable" filter has 0.53 win/loss ratio
   - Wins average +140, losses average -266
   - One -845 loss can wipe out multiple wins

RECOMMENDATION:
  R_Rev strategies at +180 entry are NOT recommended.
  The single "profitable" filter is overfitted to one exceptional day.
  Need more data to validate any patterns.
```

---

## Completion Status

**COMPLETE** - 2026-05-05 04:45

All requested analysis outputs documented including:
1. Initial strategy analysis
2. Survivorship bias check
3. Filter testing (single and combination)
4. Consistency check across days
5. Win/Loss ratio analysis
6. Honest conclusions about lack of profitable edge
7. **NEW: R_Rev segmented analysis with counter-intuitive drawdown finding**
