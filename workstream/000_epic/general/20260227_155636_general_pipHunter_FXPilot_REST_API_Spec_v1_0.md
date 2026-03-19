# FXPilot REST API Specification

**Auto Trading Intelligence Platform — Dashboard Data Integration Guide**
Version 1.0 | Confidential — Internal Use Only

---

## Table of Contents

1. [Overview](#1-overview)
2. [Endpoints](#2-endpoints)
3. [Webhook — Live Trade Push](#3-webhook--live-trade-push)
4. [Filtering & Query Reference](#4-filtering--query-reference)
5. [Dashboard Integration Map](#5-dashboard-integration-map)
6. [Health Check](#6-health-check)
7. [Rate Limits & Caching](#7-rate-limits--caching)
8. [Implementation Notes for Backend Team](#8-implementation-notes-for-backend-team)
9. [Document History](#9-document-history)

---

## 1. Overview

This document defines the REST API contract between the FXPilot dashboard frontend and the custom Forex trading platform backend. The dashboard displays performance data for thousands of auto-generated strategies with top-20 ranking by default, drill-down trade views, and AI-powered analysis.

### 1.1 Design Principles

- **Performance first** — With thousands of strategies, the API must return pre-aggregated stats — never raw trade lists at portfolio level.
- **Pagination everywhere** — All list endpoints are paginated. The dashboard requests page 1 (top 20) by default.
- **Lazy loading** — Trade-level data is only fetched when a user drills into a specific strategy.
- **Filter at source** — Strategy type and pair filters are applied server-side via query parameters, not client-side.
- **Stateless** — The API is stateless. All context is passed in request parameters.

### 1.2 Base URL

All endpoints are relative to the configured base URL. During development this is set in the dashboard's Webhook configuration panel.

```
Production:   https://api.your-platform.com/v1
Development:  http://localhost:8080/v1
Staging:      https://staging-api.your-platform.com/v1
```

### 1.3 Authentication

All requests require an API key passed as a request header. The key is configured by the user in the dashboard's Webhook settings panel.

```http
X-API-Key: <your-api-key>
```

**Example:**
```http
GET /v1/strategies?limit=20&sort=pnl_desc
X-API-Key: sk-live-abc123def456
Content-Type: application/json
```

> ⚠️ **Security:** API keys must be transmitted over HTTPS only. Never embed keys in URLs or query strings. The dashboard stores the key in memory only — it is never persisted to localStorage or cookies.

### 1.4 Response Format

All responses return JSON with a consistent envelope structure:

```json
{
  "success": true,
  "data": { ... },
  "meta": {
    "total": 1247,
    "page": 1,
    "limit": 20,
    "pages": 63,
    "generated_at": "2026-02-27T14:23:05Z"
  }
}
```

### 1.5 Error Responses

```json
{
  "success": false,
  "error": {
    "code": "STRATEGY_NOT_FOUND",
    "message": "Strategy s_0042 does not exist",
    "http_status": 404
  }
}
```

| HTTP Status | Error Code       | Meaning                        |
|-------------|------------------|--------------------------------|
| 200         | —                | Success                        |
| 400         | INVALID_PARAMS   | Bad query parameters           |
| 401         | UNAUTHORIZED     | Missing or invalid API key     |
| 404         | NOT_FOUND        | Resource does not exist        |
| 429         | RATE_LIMITED     | Too many requests              |
| 500         | SERVER_ERROR     | Internal server error          |

---

## 2. Endpoints

### 2.1 `GET /strategies` — Strategy Leaderboard

Returns a paginated, ranked list of strategies with pre-computed performance statistics. This is the primary data source for the dashboard's Leaderboard view. The default call returns the top 20 strategies by net P&L.

| | |
|---|---|
| **Method** | `GET` |
| **Path** | `/v1/strategies` |
| **Auth** | `X-API-Key` header required |

#### Query Parameters

| Parameter   | Type    | Default    | Description |
|-------------|---------|------------|-------------|
| `limit`     | integer | `20`       | Number of strategies to return (max 100) |
| `page`      | integer | `1`        | Page number for pagination |
| `sort`      | string  | `pnl_desc` | Sort order: `pnl_desc`, `pnl_asc`, `winrate_desc`, `pf_desc`, `trades_desc` |
| `type`      | string  | *(all)*    | Filter by strategy type: `trend`, `mean_reversion`, `scalping`, `carry`, `event_driven`, `grid` |
| `pair`      | string  | *(all)*    | Filter by currency pair e.g. `EURUSD`, `GBPUSD` |
| `min_trades`| integer | `0`        | Minimum closed trade count to include a strategy |
| `status`    | string  | `active`   | Filter by status: `active`, `paused`, `stopped`, `all` |

#### Example Request

```http
GET /v1/strategies?limit=20&sort=pnl_desc&type=trend&pair=EURUSD
X-API-Key: sk-live-abc123
```

#### Response — `data.strategies[]`

| Field                    | Type      | Description |
|--------------------------|-----------|-------------|
| `id`                     | string    | Unique strategy identifier e.g. `"s_0042"` |
| `name`                   | string    | Human-readable strategy name |
| `type`                   | string    | Strategy type: `trend`, `mean_reversion`, `scalping`, `carry`, `event_driven`, `grid` |
| `timeframe`              | string    | Primary timeframe: `M1`, `M5`, `M15`, `H1`, `H4`, `D1` |
| `pairs`                  | string[]  | Array of currency pairs this strategy trades |
| `status`                 | string    | `active` \| `paused` \| `stopped` |
| `stats.total_pnl`        | float     | Net P&L across all closed trades (USD) |
| `stats.win_rate`         | float     | Win rate as a percentage 0–100 |
| `stats.profit_factor`    | float     | Gross profit / gross loss ratio |
| `stats.avg_win`          | float     | Average winning trade value (USD) |
| `stats.avg_loss`         | float     | Average losing trade value (USD, negative) |
| `stats.max_drawdown`     | float     | Largest single losing trade (USD, negative) |
| `stats.closed_count`     | integer   | Number of closed trades |
| `stats.open_count`       | integer   | Number of currently open trades |
| `stats.total_trades`     | integer   | Total trades (closed + open) |
| `stats.best_streak`      | integer   | Longest consecutive winning streak |
| `stats.equity_curve`     | float[]   | Cumulative P&L array (one value per closed trade, sorted by close time) — used for sparkline rendering |
| `created_at`             | string    | ISO 8601 timestamp of strategy creation |
| `last_trade_at`          | string    | ISO 8601 timestamp of most recent trade |

#### Example Response

```json
{
  "success": true,
  "data": {
    "strategies": [
      {
        "id": "s_0042",
        "name": "EMA Breakout v3",
        "type": "trend",
        "timeframe": "H4",
        "pairs": ["EURUSD", "GBPUSD"],
        "status": "active",
        "stats": {
          "total_pnl": 4821.50,
          "win_rate": 63.4,
          "profit_factor": 2.18,
          "avg_win": 187.40,
          "avg_loss": -85.90,
          "max_drawdown": -210.00,
          "closed_count": 142,
          "open_count": 3,
          "total_trades": 145,
          "best_streak": 9,
          "equity_curve": [120.5, 285.0, 210.3, 398.7, "..."]
        },
        "created_at": "2025-11-01T09:00:00Z",
        "last_trade_at": "2026-02-27T11:42:00Z"
      }
    ]
  },
  "meta": { "total": 1247, "page": 1, "limit": 20, "pages": 63 }
}
```

---

### 2.2 `GET /strategies/:id` — Single Strategy Detail

Returns full detail for a single strategy. Used when the user selects a strategy to drill down. Trades are fetched separately via endpoint 2.3.

| | |
|---|---|
| **Method** | `GET` |
| **Path** | `/v1/strategies/:id` |
| **Auth** | `X-API-Key` header required |
| **URL param `:id`** | Strategy ID e.g. `s_0042` |

Response shape is identical to a single item in the `strategies` array from endpoint 2.1, plus an optional `description` string field.

---

### 2.3 `GET /strategies/:id/trades` — Trade Drill-Down

Returns the paginated list of trades for a specific strategy. **Only called when a user drills down into a strategy card — never called at portfolio load time.**

| | |
|---|---|
| **Method** | `GET` |
| **Path** | `/v1/strategies/:id/trades` |
| **Auth** | `X-API-Key` header required |

#### Query Parameters

| Parameter | Type    | Default          | Description |
|-----------|---------|------------------|-------------|
| `limit`   | integer | `50`             | Trades per page |
| `page`    | integer | `1`              | Page number |
| `status`  | string  | `all`            | Filter: `all` \| `open` \| `closed` |
| `sort`    | string  | `open_time_desc` | Sort: `open_time_desc`, `open_time_asc`, `pnl_desc`, `pnl_asc` |
| `pair`    | string  | *(all)*          | Filter by specific pair e.g. `EURUSD` |

#### Response — `data.trades[]`

| Field          | Type         | Description |
|----------------|--------------|-------------|
| `id`           | string       | Unique trade identifier |
| `strategy_id`  | string       | Parent strategy ID |
| `pair`         | string       | Currency pair e.g. `EURUSD` |
| `direction`    | string       | `BUY` or `SELL` |
| `status`       | string       | `OPEN` or `CLOSED` |
| `lot`          | float        | Lot size |
| `pnl`          | float\|null  | Realised P&L for closed trades; `null` for open trades |
| `pips`         | float\|null  | Pips gained/lost; `null` for open trades |
| `open_time`    | string       | ISO 8601 timestamp trade was opened |
| `close_time`   | string\|null | ISO 8601 timestamp trade was closed; `null` if open |
| `sl`           | float        | Stop loss in pips |
| `tp`           | float        | Take profit in pips |
| `open_price`   | float        | Entry price |
| `close_price`  | float\|null  | Exit price; `null` if open |

---

### 2.4 `GET /portfolio/summary` — Portfolio Overview

Returns aggregated statistics across all strategies. Used by the AI Portfolio tab.

| | |
|---|---|
| **Method** | `GET` |
| **Path** | `/v1/portfolio/summary` |
| **Auth** | `X-API-Key` header required |

#### Response — `data`

| Field                      | Type      | Description |
|----------------------------|-----------|-------------|
| `total_strategies`         | integer   | Total number of strategies in the system |
| `active_strategies`        | integer   | Strategies with status = `active` |
| `total_pnl`                | float     | Net P&L across entire portfolio |
| `total_trades`             | integer   | Total trades across all strategies |
| `total_open`               | integer   | Currently open positions across all strategies |
| `avg_win_rate`             | float     | Mean win rate across all strategies |
| `best_profit_factor`       | float     | Highest profit factor across all strategies |
| `portfolio_equity_curve`   | float[]   | Combined cumulative P&L over time for all strategies |
| `top_strategy_id`          | string    | ID of the highest performing strategy |
| `worst_strategy_id`        | string    | ID of the lowest performing strategy |

---

### 2.5 `GET /portfolio/alerts` — Alert Feed

Returns the list of system-generated alerts for underperforming or notable strategies. Used by the Alerts tab.

| | |
|---|---|
| **Method** | `GET` |
| **Path** | `/v1/portfolio/alerts` |
| **Auth** | `X-API-Key` header required |

#### Response — `data.alerts[]`

| Field            | Type   | Description |
|------------------|--------|-------------|
| `id`             | string | Unique alert ID |
| `level`          | string | `critical` \| `warning` \| `info` |
| `strategy_id`    | string | Affected strategy ID |
| `strategy_name`  | string | Affected strategy name |
| `message`        | string | Human-readable alert description |
| `metric`         | string | The metric that triggered the alert e.g. `win_rate`, `profit_factor` |
| `value`          | float  | Current value of the triggering metric |
| `threshold`      | float  | Threshold that was breached |
| `created_at`     | string | ISO 8601 timestamp alert was generated |

---

## 3. Webhook — Live Trade Push

In addition to polling the REST API, the dashboard can receive real-time trade events pushed from the platform. When a new trade opens or closes, the platform POSTs to the dashboard's configured receiver URL.

### 3.1 Inbound Webhook Payload

```http
POST <dashboard-receiver-url>
Content-Type: application/json
X-Webhook-Secret: <shared-secret>

{
  "event": "trade.closed",
  "timestamp": "2026-02-27T14:23:05Z",
  "trade": {
    "id": "t_9981",
    "strategy_id": "s_0042",
    "strategy_name": "EMA Breakout v3",
    "pair": "EURUSD",
    "direction": "BUY",
    "status": "CLOSED",
    "lot": 0.5,
    "pnl": 142.50,
    "pips": 14.3,
    "open_time": "2026-02-27T09:15:00Z",
    "close_time": "2026-02-27T14:22:58Z",
    "sl": 25.0,
    "tp": 50.0,
    "open_price": 1.08420,
    "close_price": 1.08563
  }
}
```

> ⚠️ **Security:** Always include the `X-Webhook-Secret` header with a pre-shared secret. The dashboard validates this header before processing any incoming event. Use HTTPS for all webhook traffic.

### 3.2 Event Types

| Event                      | Triggered When |
|----------------------------|----------------|
| `trade.opened`             | A new trade has been entered for any strategy |
| `trade.closed`             | An existing trade has been closed (hit TP, SL, or manual) |
| `trade.updated`            | An open trade's SL, TP, or lot size has been modified |
| `strategy.stats_updated`   | A strategy's aggregated stats have been recalculated (after each close) |

---

## 4. Filtering & Query Reference

### 4.1 Strategy Types

| API Value        | Display Name     | Description |
|------------------|------------------|-------------|
| `trend`          | Trend Following  | Momentum and breakout strategies using MA/EMA signals |
| `mean_reversion` | Mean Reversion   | RSI, Bollinger Band, and oscillator-based entries |
| `scalping`       | Scalping         | High-frequency short-duration entries, typically M1–M15 |
| `carry`          | Carry Trade      | Interest rate differential exploitation, typically D1 |
| `event_driven`   | Event Driven     | News and economic release reaction strategies |
| `grid`           | Grid             | Fixed-interval grid strategies with hedging |

### 4.2 Currency Pairs

Use standard 6-character FX pair codes (no slash):

```
Major pairs:  EURUSD, GBPUSD, USDJPY, USDCHF, AUDUSD, NZDUSD, USDCAD
Minor pairs:  EURGBP, EURJPY, GBPJPY, AUDNZD, CADJPY, ...
Exotic pairs: USDMXN, USDTRY, USDZAR, ...
```

### 4.3 Combined Filter Example

Fetch top 50 scalping strategies on GBP/USD, sorted by win rate:

```http
GET /v1/strategies?limit=50&sort=winrate_desc&type=scalping&pair=GBPUSD&min_trades=10
X-API-Key: sk-live-abc123
```

---

## 5. Dashboard Integration Map

This table maps each dashboard view to the API endpoints it depends on:

| Dashboard View   | On Load | On Filter Change | On User Action |
|------------------|---------|------------------|----------------|
| **Leaderboard**  | `GET /strategies?limit=20&sort=pnl_desc` | `GET /strategies?type=X&pair=Y` | Drill-down → `GET /strategies/:id/trades` |
| **AI Compare**   | Uses cached strategy data from Leaderboard | — | No additional API calls |
| **AI Portfolio** | `GET /portfolio/summary` | — | No additional API calls |
| **Alerts**       | `GET /portfolio/alerts` | — | VIEW button → triggers drill-down |
| **Webhook Config** | — | — | Test connection → `GET /v1/health` |
| **Floating Chat** | Uses all cached data already in memory | — | No API calls — data passed to Claude as context |

> 💡 **Performance note:** The dashboard never requests trade-level data at portfolio load time. Only pre-aggregated stats (including `equity_curve`) are fetched up front. Full trade lists are lazy-loaded on demand when a user drills into a strategy card. This keeps initial load fast even with 1000+ strategies.

---

## 6. Health Check

### `GET /health`

Used by the dashboard's Webhook configuration panel to test API connectivity.

| | |
|---|---|
| **Method** | `GET` |
| **Path** | `/v1/health` |
| **Auth** | `X-API-Key` header required |

#### Example Response

```json
{
  "success": true,
  "data": {
    "status": "healthy",
    "version": "1.0.0",
    "strategies_count": 1247,
    "uptime_seconds": 86432,
    "db_connected": true
  }
}
```

---

## 7. Rate Limits & Caching

| Endpoint                          | Rate Limit   | Recommended Cache TTL |
|-----------------------------------|--------------|-----------------------|
| `GET /strategies`                 | 60 req/min   | 30 seconds            |
| `GET /strategies/:id`             | 120 req/min  | 30 seconds            |
| `GET /strategies/:id/trades`      | 120 req/min  | 15 seconds            |
| `GET /portfolio/summary`          | 30 req/min   | 60 seconds            |
| `GET /portfolio/alerts`           | 30 req/min   | 30 seconds            |
| `GET /health`                     | 10 req/min   | No cache              |

Rate limit headers are returned on every response:

```http
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 47
X-RateLimit-Reset: 1740662400
```

---

## 8. Implementation Notes for Backend Team

### 8.1 `equity_curve` Field

The `equity_curve` array is critical for the sparkline charts displayed on each strategy card and in the drill-down panel. It must be:

- **Pre-computed on the server** — not calculated client-side from raw trades
- **Sorted chronologically** by `close_time` — oldest first, newest last
- **Cumulative** — each value is the running total P&L, not the individual trade P&L
- **Trimmed to a maximum of 200 data points** using equal-interval sampling if the strategy has more than 200 closed trades

**Example — correctly formatted:**
```json
"equity_curve": [45.20, 112.80, 89.40, 201.60, 318.90, ...]
//               ^trade1 cumul  ^trade2 cumul  ...
```

### 8.2 Alert Generation

The platform should pre-compute alerts server-side via `GET /portfolio/alerts`. The dashboard also runs a lightweight client-side alert engine as a fallback, but server-side alerts are the authoritative source.

**Recommended alert thresholds:**

| Metric | Threshold | Level |
|--------|-----------|-------|
| Win rate | < 40% | `critical` |
| Win rate | 40–50% | `warning` |
| Profit factor | < 1.0 | `critical` |
| Profit factor | 1.0–1.3 | `warning` |
| Max single loss | < −$300 | `critical` |
| Open positions (one strategy) | > 8 | `warning` |
| Net P&L | < −$200 | `critical` |
| Win rate > 70% AND profit factor > 2.5 | — | `info` (outperforming) |

### 8.3 Recommended Database Indices

To support the sorting and filtering patterns this API requires:

```sql
-- Default sort
CREATE INDEX idx_strategies_pnl ON strategies (stats_total_pnl DESC);

-- Type and pair filters
CREATE INDEX idx_strategies_type ON strategies (type);
CREATE INDEX idx_strategies_pairs ON strategies USING GIN (pairs);  -- if array column

-- Status filter
CREATE INDEX idx_strategies_status ON strategies (status);

-- Trade drill-down
CREATE INDEX idx_trades_strategy_status ON trades (strategy_id, status);
CREATE INDEX idx_trades_strategy_time ON trades (strategy_id, open_time DESC);
```

### 8.4 Pagination for Large Strategy Sets

With potentially thousands of strategies, use **keyset pagination** (cursor-based) rather than OFFSET for sort orders beyond page 5, as OFFSET becomes slow at scale:

```http
# First page
GET /v1/strategies?limit=20&sort=pnl_desc

# Next page using cursor (preferred over page=2 for large datasets)
GET /v1/strategies?limit=20&sort=pnl_desc&after=s_0042&after_value=4821.50
```

The response should include a `meta.next_cursor` field when keyset pagination is supported.

---

## 9. Document History

| Version | Date        | Author        | Change |
|---------|-------------|---------------|--------|
| 1.0     | 27 Feb 2026 | FXPilot Team  | Initial specification — dashboard v3.0 integration |

---

*FXPilot API Specification — Confidential — Internal Use Only*
