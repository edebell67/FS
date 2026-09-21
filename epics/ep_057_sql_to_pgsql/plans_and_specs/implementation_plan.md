# Implementation Plan - Bi-Directional Net Display Mode (Buy Net & Sell Net without Total Net)

Add a new directional split mode (`BI_SPLIT` / "Buy & Sell Net") to `top10_5min_equity_curves.html` that displays both **`cum_buy_net`** and **`cum_sell_net`** lines side-by-side on the chart without displaying `total_net`, with zero loss of any existing functionality.

## User Review Required

> [!IMPORTANT]
> - **Existing Functionality Preserved**: All existing modes (`Total Net (All 10)`, `Cum Buy Net`, `Cum Sell Net`, `Tri-Split (Single Model)`), Replay from Baseline, Replay controls, Min Win Rate filter, Delta line toggles, individual model curve toggles, and multi-date tabs remain 100% untouched and functional.
> - **New Feature**: Appends a new mode button **"Buy & Sell Net"** (`BI_SPLIT`) right alongside existing split modes. When selected:
>   - Renders **Buy Net** (`cum_buy_net`) in Sky Blue (`#38bdf8`) and **Sell Net** (`cum_sell_net`) in Amber (`#fbbf24`) for the selected model (or selected visible models) side-by-side on the chart.
>   - Completely hides `total_net` from the chart.
>   - Ribbon inspector, hover tooltips, and card deltas synchronize seamlessly to reflect Buy Net and Sell Net without Total Net.
>   - Version bumped from `V20260920_1650` to `V20260920_1735`.

---

## Proposed Changes

### Dashboard & UI Layer

#### [MODIFY] [top10_5min_equity_curves.html](file:///C:/Users/edebe/eds/epics/ep_057_sql_to_pgsql/dashboards_and_uis/top10_5min_equity_curves.html)
- Add new button `<button id="metricBiSplit">Buy & Sell Net</button>` to the Directional Split selector toolbar.
- Update `splitMode` handling:
  - Add `'BI_SPLIT'` to `splitMode` state options (`ALL_NET`, `BUY_NET`, `SELL_NET`, `TRI_SPLIT`, `BI_SPLIT`).
  - In `setSplitMode(mode)`: handle `BI_SPLIT` active styles and button states.
  - In `drawChart()`: when `splitMode === 'BI_SPLIT'`, calculate scaling across Buy Net and Sell Net lines only (excluding Total Net), and render both the Sky Blue (`#38bdf8`) Buy curve and Amber (`#fbbf24`) Sell curve. Exclude the Net line entirely.
  - In `updateRibbon()`: update strategy title and ribbon focus to "Mode: Buy & Sell Net (Directional Split without Total Net)".
  - In tooltip hover listener: when in `BI_SPLIT`, show Δ Buy Net and Δ Sell Net exclusively, omitting Total Net.
- Synchronize copy to root artifacts directory `C:\Users\edebe\.gemini\antigravity\brain\6aed791c-b3c5-4ab4-a571-c23206db4462\top10_5min_equity_curves.html`.

---

### Configuration & Versioning Layer

#### [MODIFY] [constants.py](file:///C:/Users/edebe/eds/TradeApps/breakout/fs/constants.py)
- Update version number to `V20260920_1735`.

---

### Workstream Lifecycle & Memory Layer

#### [NEW] [20260920_173500_breakout_997_bi_directional_net_mode.md](file:///C:/Users/edebe/eds/workstream/100_backlog/20260920_173500_breakout_997_bi_directional_net_mode.md)
- Follow standard lifecycle tracking (`100_backlog` -> `200_inprogress` -> `300_complete` and mirror to Obsidian).

---

## Verification Plan

### Automated / Syntax Tests
- Run Python syntax check on `constants.py`.
- Run validation check on HTML structure and JavaScript bindings.

### Manual Verification
- Open `top10_5min_equity_curves.html` in browser.
- Verify that clicking "Buy & Sell Net" renders both Cum Buy Net and Cum Sell Net simultaneously with NO Total Net line.
- Verify Replay playback runs smoothly from baseline in `BI_SPLIT` mode.
- Verify all previous buttons (`Total Net`, `Cum Buy Net`, `Cum Sell Net`, `Tri-Split`, Delta toggles, Win Rate slider) continue to function exactly as before.
