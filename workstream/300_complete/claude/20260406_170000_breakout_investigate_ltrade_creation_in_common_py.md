Source: User request on 2026-04-06 to investigate how l-trade is created in the breakout common.py file.

Task Type: standard

Task Attributes:
- priority: medium
- execution_owner: claude
- workflow_ready: false

**Suggested Agent:** claude

Task Summary: Investigate and document how l-trade (live trade) is created, populated, and used in the breakout trading system's common.py file.

Context:
- Workspace: `C:\Users\edebe\eds`
- Target File: `C:\Users\edebe\eds\TradeApps\breakout\fs\common.py`
- Related Area: TradeApps breakout trading system
- Investigation Focus: l-trade creation, data flow, and usage patterns

Dependency: None

Execution Workflow:
1. Read and analyze common.py
2. Identify l-trade related code (creation, population, usage)
3. Trace data flow and dependencies
4. Document findings

Scheduled For: 2026-04-06 17:00:00+01:00

## Objective
Understand and document how l-trade is created in the breakout trading system, including:
- What l-trade represents
- How it is initialized/created
- What data populates it
- Where it is used downstream

## Investigation Findings

### What L-Trade Represents
L-Trade = **Live Trade** - An order that gets sent to TWS (Interactive Brokers) for actual execution in the market. This is distinguished from V-Trade (Virtual Trade) which is a paper trade used for backtesting/simulation.

### L-Trade Creation Lifecycle

```
Price Feed (OANDA API)
        │
        ▼
process_new_tick() [Line 2111]
        │
        ▼
check_and_enter() [breakout.py:21]
  - LONG: current_price > max(price_history) + pip_buffer
  - SHORT: current_price < min(price_history) - pip_buffer
        │
        ▼
enter_trade() [Line 2046] → Creates V-Trade
        │
        ▼
_handle_live_orders() [Line 1170]
  ├─ Check l_trade_generation_mode [Line 1175]
  ├─ Check _is_active() [Line 1094] → activations.json
  ├─ Check _is_profitability_guard_passed()
  └─ Check _is_market_bias_entry_allowed()
        │
        ▼
_create_tradeable_json() [Line 1657]
        │
        ▼
_create_l_trade_order() [Line 2995] → Creates L-Trade JSON
```

### Key Function: `_create_l_trade_order()` [common.py:2995-3200]

**Parameters:**
- `product`: Currency pair (e.g., "GBP")
- `direction`: "LONG" or "SHORT"
- `strategy_key`: Strategy identifier
- `trade_id`: Unique trade ID
- `current_price`: Market price at order time
- `latest_bid/ask`: Current bid/ask prices
- `mode`: "net" or "alt" (alternative direction)
- `is_close`: Boolean for close orders
- `source`: Origin screen (e.g., "breakout", "grid_live", "trade_bucket")
- `source_group`: Group for cap tracking
- `guid`: Unique identifier

### Guards/Checks Before L-Trade Creation

1. **Archive Block** [Line 3014]:
   - Blocks new L-Trades when archive process is active

2. **Max Live Trades** [Line 3027]:
   - Config: `max_live_trades` (default: 1)
   - Counts both on-disk and memory-pending orders
   - Scoped per `source_group`

3. **Daily Target** [Line 3037]:
   - Config: `daily_target` (default: 400.0)
   - Blocks when closed P&L >= target for group

4. **TWS Routing Cap** [Line 3079-3109]:
   - Config: `max_trades_to_tws` (default: 1)
   - Only applies to NET mode orders
   - Prevents overwhelming TWS with orders

5. **Memory Cache** [Line 3050-3068]:
   - Tracks orders sent within last 30 seconds
   - Prevents duplicates during disk write latency

### L-Trade Output

**File Location:**
- Live: `C:\Users\edebe\eds\trades_rt3\orders\`
- Sim: `C:\Users\edebe\eds\trades_rt3_sim\orders\`

**Filename Format:**
```
{source}_{guid}_{product}_{strategy}_{action}_{timestamp}_{open|close}_tradeable.json
```

**JSON Structure:**
```json
{
  "symbol": "GBP",
  "secType": "CASH",
  "exchange": "IDEALPRO",
  "currency": "USD",
  "action": "BUY|SELL",
  "orderType": "MKT",
  "quantity": <from config>,
  "guidePrice": <bid or ask>,
  "comment": "{strategy} {mode} {phase} #{trade_id}",
  "source": "breakout|grid_live|trade_bucket",
  "source_group": "{source}_{group}",
  "guid": "{guid}"
}
```

### Activation Points for L-Trade

1. **Normal Path** [Line 1272]:
   - Direct activation via `_handle_live_orders()` after V-Trade entry
   - Requires activation in `activations.json`

2. **Grid Live Path** [Line 1369]:
   - Activation via `_trigger_grid_live_activation()`
   - Triggered by `grid_live.json` configuration
   - Can bypass some guards with `bypass_criteria_check: ultra`

3. **Scheduled/Immediate Path** [Line 2244]:
   - Activation via schedule matching in `_check_live_schedule_in_progress()`
   - Source screen set to "grid_live" or "trade_bucket"

4. **Trade Close Path** [Lines 1883-1885]:
   - Creates close orders when V-Trade exits
   - Only if `order_sent_net` or `order_sent_alt` was True

### Configuration Settings

| Setting | Default | Description |
|---------|---------|-------------|
| `l_trade_generation_mode` | "both" | Controls generation: "normal", "both", "trade_bucket" |
| `max_live_trades` | 1 | Max concurrent live trades per source_group |
| `max_trades_to_tws` | 1 | Max NET orders to TWS |
| `daily_target` | 400.0 | P&L target to stop trading |
| `bypass_criteria_check` | "" | "immediately" or "ultra" to bypass guards |
| `send_json_files` | `trades_rt3/orders` | Live order output path |
| `send_json_files_sim` | `trades_rt3_sim/orders` | Sim order output path |

### Data Flow Summary

```
[OANDA API] → Tick Data
     │
[BaseBreakoutStrategy] → V-Trade (JSON file in /json/live/{date}/)
     │
[Activation Checks] → activations.json, grid_live.json, profitability_guard
     │
[_create_l_trade_order()] → L-Trade (JSON file in /trades_rt3/orders/)
     │
[TWS Consumer] → Executes market order via IB API
```

## Plan Status
- [x] 1. Read common.py and identify l-trade references
  - Evidence: Main function `_create_l_trade_order()` at line 2995, called by `_create_tradeable_json()` wrapper

- [x] 2. Trace l-trade creation logic
  - Evidence: Complete flow traced from tick processing through breakout detection to L-Trade file creation

- [x] 3. Identify data sources that populate l-trade
  - Evidence: Price data from OANDA, strategy parameters from config, activation status from activations.json

- [x] 4. Map l-trade usage downstream
  - Evidence: L-Trade JSON files consumed by TWS connector for market order execution

- [x] 5. Document findings
  - Evidence: This document

## Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true

- Evidence-Type: file_output
  - Artifact: This documentation file
  - Objective-Proved: Complete investigation of l-trade lifecycle
  - Status: complete

## Validation Rules
- Do not modify any code ✓
- Document actual code behavior, not assumptions ✓
- Include line numbers for key references ✓

## Completion Status
- State: COMPLETE
- Timestamp: 2026-04-06T21:35:00+01:00
