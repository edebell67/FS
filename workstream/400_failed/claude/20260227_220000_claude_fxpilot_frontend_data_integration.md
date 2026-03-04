# FXPilot Frontend - Live Data Integration Tasks

**Created**: 2026-02-27 22:00:00
**Project**: PipHunter Landing Page / FXPilot Dashboard
**Data Source**: `breakout/fs/json/live/2026-02-27/`

---

## Overview

Replace mock data in `forex-dashboard_1.jsx` with real breakout system data from the live JSON files.

---

## Data Files Available

| File | Purpose | Key Fields |
|------|---------|------------|
| `_top20.json` | Strategy rankings | strategy, product, total_net, buy_net, sell_net, trade_count, buyPercent, sellPercent |
| `_summary_net.json` | Equity curves | timestamp series with net, buy_net, sell_net per strategy/product |
| `_targeted_strategies.json` | Market bias & recommendations | bias, day_bias, recent_bias, top_recommendation, strategies[] |
| `_live_trades.json` | Active positions | trade_id, product, direction, entry_price, current_price, net_return, status |
| `_trade_buckets.json` | Trade groups | bucket_id, name, mode, strategies[], market_bias_at_creation |
| `*_cld.json` | Closed trades | Individual trade details |
| `*_op.json` | Open trades | Individual trade details |

---

## Tasks

### 1. Data Layer Setup
**Priority**: HIGH
**Status**: TODO

- [ ] Create `src/api/dataService.js` to fetch JSON files
- [ ] Add date parameter support (default: today)
- [ ] Implement caching layer with refresh interval
- [ ] Handle file loading errors gracefully

```javascript
// Target API structure
fetchTop20(date) -> Promise<Top20Data>
fetchSummaryNet(date) -> Promise<SummaryNetData>
fetchMarketBias(date) -> Promise<MarketBiasData>
fetchLiveTrades(date) -> Promise<LiveTradesData>
fetchTradeBuckets(date) -> Promise<TradeBucketsData>
```

---

### 2. Strategy Leaderboard
**Priority**: HIGH
**Status**: TODO

Replace `STRATEGIES` mock data with `_top20.json`:

- [ ] Map `_top20.json` fields to component props
- [ ] Display: strategy name, product, total_net, trade_count
- [ ] Show buy/sell breakdown with percentages
- [ ] Color-code by P&L (green positive, red negative)
- [ ] Add rank badges (#1, #2, #3 gold/silver/bronze)

**Field Mapping**:
```
strategy -> name
product -> pairs[0]
total_net -> totalPnL
buy_net + sell_net -> breakdown
buyPercent, sellPercent -> win rates
trade_count -> closedCount
```

---

### 3. Market Bias Panel
**Priority**: HIGH
**Status**: TODO

Create new component from `_targeted_strategies.json`:

- [ ] Display overall bias (BUY/SELL/MIXED)
- [ ] Show day_bias vs recent_bias conflict indicator
- [ ] Display top_recommendation card
- [ ] List eligible strategies with scalper indicator
- [ ] Show total_buy_net vs total_sell_net comparison

**UI Elements**:
- Large bias indicator (arrow up/down)
- Confidence meter (based on net difference)
- Top pick highlight card
- Mini strategy list (scrollable)

---

### 4. Live Trades View
**Priority**: HIGH
**Status**: TODO

Create real-time trades panel from `_live_trades.json`:

- [ ] Show active positions with entry/current price
- [ ] Display gross_pnl_pips and net_return
- [ ] Color by profit/loss status
- [ ] Show market_bias_at_open vs market_bias_latest
- [ ] Add is_live_trade indicator
- [ ] Display source_screen (grid_live, etc.)

**Columns**:
- Product | Direction | Entry | Current | P&L (pips) | Net | Status

---

### 5. Equity Curve Charts
**Priority**: MEDIUM
**Status**: TODO

Build charts from `_summary_net.json`:

- [ ] Parse timestamp series per strategy/product
- [ ] Create sparkline for each strategy card
- [ ] Build full equity curve for drill-down view
- [ ] Support buy vs sell overlay comparison
- [ ] Add session_max_net indicator line

**Chart Requirements**:
- SVG sparklines for cards (existing Spark component)
- Full chart in drill-down modal
- Tooltip with timestamp and exact values

---

### 6. Trade Buckets View
**Priority**: MEDIUM
**Status**: TODO

New tab from `_trade_buckets.json`:

- [ ] List buckets with name and creation time
- [ ] Show strategies within each bucket
- [ ] Display net_delta_from_creation per strategy
- [ ] Color by performance (net positive/negative)
- [ ] Show market_bias_at_creation indicator

---

### 7. Strategy Drill-Down Enhancement
**Priority**: MEDIUM
**Status**: TODO

Enhance existing drill-down with real data:

- [ ] Load individual trade files for selected strategy
- [ ] Display trade history table (from `*_cld.json` files)
- [ ] Show entry/exit prices, P&L per trade
- [ ] Calculate win rate from actual trades
- [ ] Add equity curve chart

---

### 8. Real-Time Updates
**Priority**: LOW
**Status**: TODO

Implement auto-refresh:

- [ ] Poll `_live_trades.json` every 5 seconds
- [ ] Poll `_top20.json` every 30 seconds
- [ ] Poll `_targeted_strategies.json` every 30 seconds
- [ ] Show "Last updated: X" timestamp
- [ ] Add manual refresh button
- [ ] Visual indicator when data changes

---

### 9. API Endpoint Option
**Priority**: LOW
**Status**: TODO

Alternative: Create Flask API endpoints:

- [ ] `/api/top20?date=2026-02-27`
- [ ] `/api/bias?date=2026-02-27`
- [ ] `/api/live-trades?date=2026-02-27`
- [ ] `/api/equity-curve?strategy=X&product=Y&date=Z`
- [ ] Add CORS support for local development

---

### 10. Mobile Optimization
**Priority**: LOW
**Status**: DONE (basic responsive added)

- [x] Add CSS media queries
- [x] Stack layout on mobile
- [x] Scrollable nav tabs
- [ ] Touch-friendly tap targets (44px min)
- [ ] Swipe gestures for tabs

---

## File Structure Target

```
piphunter/landing_page/
├── index.html
├── main.jsx
├── vite.config.js
├── package.json
├── src/
│   ├── api/
│   │   └── dataService.js      # NEW: Data fetching
│   ├── components/
│   │   ├── StrategyCard.jsx    # Updated with real data
│   │   ├── BiasPanel.jsx       # NEW: Market bias
│   │   ├── LiveTrades.jsx      # NEW: Active positions
│   │   ├── EquityCurve.jsx     # NEW: Charts
│   │   └── TradeBuckets.jsx    # NEW: Bucket view
│   └── App.jsx                 # Main dashboard
└── forex-dashboard_1.jsx       # Current (to be refactored)
```

---

## Notes

- Data path: `breakout/fs/json/{run_mode}/{current_date}/`
  - `run_mode`: from config (e.g., `live`, `sim`)
  - `current_date`: today's date (YYYY-MM-DD format)
- For Vite dev server, may need proxy config to access local files
- Consider serving JSON via simple Flask server for CORS handling
- Production: Data should come from PipHunter API (Render deployment)
