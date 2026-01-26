# TradePanel — Strategy Spec & Run Log
_Date:_ 13 Oct 2025  
_Scope:_ Encapsulate our discussion, define the strategies, spell out rules/assumptions, and summarise the empirical runs you asked me to execute.

---

## 1) Common Assumptions
- **Lot size:** 100,000 (100k) notional.
- **Pip definition:** 1 pip = 0.0001 (for standard FX pairs as used in your files).
- **Pip value:** £10 per pip per 100k.
- **Commission:** as specified per run (default £20/round unless noted).
- **Prices:** Unless stated otherwise, exits are computed on the **same column** as entries (typically `entry_price` or `Current Price`).
- **Non-overlapping (blocking) mode:** While a position is open, **new signals are ignored** until exit (unless we explicitly switch to “no-block”).
- **Same‑exit flipped (alt) P/L:** For any executed trade, the **alt** result flips the side but keeps the **same entry & exit rows**.  
  _Gross_ = (±pips) × £10; _Net_ = _Gross_ – commission.  
  Column in CSVs: `alt_net_return`.

---

## 2) Strategy A — \"Red‑XOR‑Zero\" Extreme Reversal Rule
**Idea.** Use structural zeros in the red counts to anticipate local extremes.

**Trigger (transition):**
```
(red_buy == 0) XOR (red_sell == 0)
```
The state must **change** versus the previous row (i.e., an entering transition).

**Direction mapping:**
- `red_buy == 0` → anticipate a **peak** → **SELL** signal.
- `red_sell == 0` → anticipate a **trough** → **BUY** signal.

**(Optional) Visual/Directional filter used in plots**  
Show `rb = 0` only if **price < previous bar**, and `rs = 0` only if **price > previous bar**.  
We also produced a plot of **Dark Green (Buy/Sell) local peaks** coinciding with `rb = 0` / `rs = 0`.

**Example management variants we tested:**
- **2‑row validity:** enter on transition, close after max 2 rows or on opposite transition.
- **Trailing stop (demo):** trail activates after +5 pips of MFE, trails by 5. (In that run, trail never activated; exits were timed.)

**Snapshot outcomes (from your earlier GBP set):**
- 2‑row validity: 30 trades; win 50%; avg **+0.23** pips; total **+7.0** pips; gross £70; **net −£530** (comm drag).
- With 5‑pip trail activation: 20 trades; win 45%; avg **+1.15** pips; total **+23** pips; gross £230; **net −£170**.

> Takeaway: The signal often locates turning areas, but tight holding windows plus per‑trade commission turned gross gains into net losses.

---

## 3) Strategy B — 5‑Bar Breakout
**Idea.** Trade breakouts beyond the **previous 5 bars’** high/low on the working price series.

**Signals** (computed with strictly prior data):
- `BUY` if `price[t] > max(price[t-1..t-5])`
- `SELL` if `price[t] < min(price[t-1..t-5])`
- Else `HOLD`

**Default exits**
- **Take‑profit (TP):** as specified (e.g., 30 pips)
- **Stop‑loss (SL):** as specified (e.g., 10 pips)
- **Commission:** as specified (per round trip)
- **Non‑overlapping (default):** ignore new signals while in a trade

**Variants we used on request**
1. **Same‑exit flipped (alt)** — analytics column `alt_*`: for each executed original trade, compute the P/L of **the opposite side** but **keeping the same entry & exit rows**.
2. **Flipped signals (opposite regime)** — generate entries from the **opposite breakout condition** itself. (We used this once for comparison.)
3. **No‑block (reverse‑on‑opposite‑signal)** — when an opposite signal arrives, **close the current trade and open the opposite immediately** at the same bar.

**Implementation notes**
- Warm‑up: first signal possible only after 5 fully populated prior bars.
- All ranges are computed from the same column used for entry/exit unless otherwise stated.
- Commission treated as a flat £ per round trip — included in `net_cash_£`.

---

## 4) Run Log & Results (you can open the CSVs referenced below)
Below is a concise index of the runs we executed during our session. Each CSV includes **one row per trade** with the original and the `alt_` columns.

### 4.1 Base file: `trades_20251013.csv`
**(a) TP=5.5 pips, SL=10 pips (55 / −100)**
- Original: 25 trades; win 48%; total **−102.0** pips; **£−1,520 net**.
- Flipped signals (opposite regime): 28 trades; total **+5.0** pips; **£−510 net** (commission drag).

**(b) TP=50 pips, SL=10 pips (500 / −100)**
- Original: 3 trades; total **−44.5** pips; **£−505 net**.  
- **Same‑exit flipped (per your table):** 3 trades; original net **−£505** vs **alt +£385**.

**(c) TP=30 pips, SL=10 pips**
- Executed: **5 trades**; exits: TP 0 / SL 5.  
- Original total **−53.5** pips → **£−635 net**; **alt +53.5 pips → £+435**.

**(d) TP=5 pips, SL=30 pips**
- Executed: **11 trades**; exits: TP 10 / SL 1.  
- Original total **+26.0** pips → **£+40 net**; **alt −26.0 pips → £−480**.

### 4.2 `zone-counts-gbp-2025-10-13-17-52-56.csv` (TP=30, SL=10, £20)
- Executed **6 trades**; TP 0 / SL 6.  
- Original **−63.0** pips → **£−750 net**; **alt +63.0 pips → £+510**.  
- CSV: `zone_counts_breakout_TP30_SL10_same_row.csv`

### 4.3 `zone-counts-gbpeur_c-2025-10-13-18-00-29.csv` (TP=30, SL=10, **£40**)
- Executed **5 trades**; TP 0 / SL 5.  
- Original **−58.0** pips → **£−780 net**; **alt +58.0 pips → £+380**.  
- CSV: `gbpeur_breakout_TP30_SL10_comm40_same_row.csv`

### 4.4 `zone-counts-eur-2025-10-13-18-11-38.csv` (TP=30, SL=10, £20)
- Executed **5 trades**; TP 1 / SL 4.  
- Original **−13.0** pips → **£−230 net**; **alt +13.0 pips → £+30**.  
- CSV: `eur_breakout_TP30_SL10_comm20_same_row.csv`

### 4.5 `eur_20251013.csv` (TP=30, SL=10, £20)
- Executed **6 trades**; TP 0 / SL 6.  
- Original **−101.5** pips → **£−1,135 net**; **alt +101.5 pips → £+895**.  
- CSV: `eur_breakout_TP30_SL10_comm20_same_row.csv`

### 4.6 `chf_20250113.csv` (TP=30, SL=10, £20)
- Executed **2 trades**; TP 1 / SL 1.  
- Original **+20.5** pips → **£+165 net**; **alt −20.5 pips → £−245**.  
- CSV: `chf_breakout_TP30_SL10_comm20_same_row.csv`

### 4.7 `gbpeur_20251013.csv` (TP=30, SL=10, **£40**)
- Executed **22 trades**; TP 4 / SL 18.  
- Original **−140.0** pips → **£−2,280 net**; **alt +140.0 pips → £+520**.  
- CSV: `gbpeur_breakout_TP30_SL10_comm40_same_row.csv`

### 4.8 `cad_20251013.csv` (TP=30, SL=10, £20)
- **Blocking (default non‑overlap):** Executed **2 trades**; TP 1 / SL 1.  
  Original **+18.5** pips → **£+145 net**; **alt −18.5 pips → £−225**.  
- **No‑block (reverse on opposite signal):** Executed **205 trades**; exits all by **flip** (TP/SL never hit first).  
  Original **−194.0** pips → **£−6,040 net**; **alt +194.0 pips → £−2,160 net** (commission drag).  
  CSVs: `cad_breakout_TP30_SL10_comm20_NO_BLOCK.csv`, `cad_breakout_TP30_SL10_comm20_NO_BLOCK_with_alt.csv`

> Broadly, with TP=30/SL=10, the **original breakout** is trend‑following; on several datasets it struggled to reach TP before a pullback hit SL. The **same‑exit flipped** (counter‑trend at those same timestamps) often produced equal/opposite pips and better net when SLs dominated.

---

## 5) Pseudocode (for clarity & audit)
### 5.1 5‑Bar Breakout — Blocking (default)
```python
for each bar t:
    update roll_max = max(price[t-1..t-5])
    update roll_min = min(price[t-1..t-5])
    sig = BUY if price[t] > roll_max else SELL if price[t] < roll_min else HOLD

    if no_open_position and sig in {BUY, SELL}:
        open(sig, price[t])
        continue

    if open_position:
        pnl_pips = side_mult * (price[t] - entry_price) / 0.0001
        if pnl_pips >= TP: close(TP)
        elif pnl_pips <= SL: close(SL)
        # else: ignore new signals while in trade
```

### 5.2 5‑Bar Breakout — No‑block (reverse on signal)
```python
if open_position and sig is opposite:
    close("flip", price[t])
    open(opposite_sig, price[t])
else:
    apply TP/SL as usual
```

### 5.3 Same‑exit flipped P/L (alt)
```python
alt_side   = opposite(original_side)
alt_pnl    = - original_pnl
alt_gross  = alt_pnl * £10
alt_net    = alt_gross - commission
```

---

## 6) Practical Recommendations
1. **Time stop** (e.g., 150–300 bars): prevents single trades from monopolising the window & reduces blocked signals.
2. **Flip priority:** If using no‑block, check **TP/SL before flipping** to allow moves to realise targets.
3. **TP/SL tuning:** On these intraday series, TP **10–20** pips and SL **8–12** pips may fit realised volatility better than 30/10.
4. **Volatility‑aware exits:** If available, compute TP/SL off a more volatile stream (`latest_price` / bid/ask midpoint) or use ATR‑scaled targets.
5. **Signal gating:** Combine the breakout with the **Red‑XOR‑Zero** filter (e.g., require `rs=0` proximity for BUY breakouts, `rb=0` for SELL). This should improve precision around turns.
6. **Commission awareness:** At £20–£40/round, small‑edge regimes need either higher TP frequency or lower churn; otherwise the net curve lags gross pips.

---

## 7) Artifacts (created during the session)
Charts & CSVs produced:
- `price_with_rb0_rs0.png` — directional rb/rs zero markers on price.
- `red_zero_events.csv`, `red_zero_events_directional.csv` — timestamps & prices where rb/rs = 0.
- `price_with_dg_peaks_and_red_zero.png`, `dg_peaks_with_red_zero_events.csv` — Dark Green peaks coincident with red zero.
- Breakout tradebooks for each dataset, e.g.:  
  `breakout_TP30_SL10_same_row.csv`, `eur_breakout_TP30_SL10_comm20_same_row.csv`,  
  `gbpeur_breakout_TP30_SL10_comm40_same_row.csv`,  
  `cad_breakout_TP30_SL10_comm20_NO_BLOCK.csv`, `cad_breakout_TP30_SL10_comm20_NO_BLOCK_with_alt.csv`, etc.

> If you want this document exported to PDF or Word, say the word and I’ll generate it.

---

## 8) Appendix — Column Mapping Hints
Different files used different headers; the code detected among:
- **Datetime:** `Last Update`, `last_update`, `created`, fields containing `time`/`update`/`timestamp`/`captured`/`date`.
- **Price:** `Current Price`, `entry_price`, or any column containing `price`/`mid`/`close`.  
Where multiple candidates existed, we chose the first plausible match and ordered the series by the datetime column when present.

---

**End of document.**

