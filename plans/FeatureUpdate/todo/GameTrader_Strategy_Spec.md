# GameTrader Strategy Specification

This document describes the core behaviour of the GameTrader simulation so that another implementation (or an LLM) can reconstruct the system accurately.

## 1. Configuration Overview (`config.py`)

- **Simulation paths**
  - `DATA_DIR`: `simulation_data`
  - `MARKET_DATA_FILE`: `simulation_data/market_data.json`
  - `PARTICIPANTS_DIR`: `simulation_data/participants`
  - `MAIN_LOG_FILE`: `simulation_data/simulation_log.jsonl`
  - `EXPERT_DATA_FILE`: `simulation_data/expert_data.jsonl`
- **Market defaults**
  - Initial GBP/USD mid ≈ 1.2500, with `SPREAD = 0.0001` (1 pip).
  - Random walk volatility step for synthetic feed ≈ 1e-4.
  - Price updates every `PRICE_UPDATE_INTERVAL_SECONDS = 3` unless an external REST price feed is enabled.
- **Trading limits**
  - Commission: $5 per leg.
  - Margin requirement: 3% of notional.
  - Size bounds: 30k ≤ notional ≤ 100k, multiples of 10k.
  - Rule-based traders disqualify if equity < $3,000.
- **Participants**
  - ~200 rule-based (`person XXX`).
  - RL agents: e.g. `RL 01`, `RL 02`.
  - Default initial capital: $10,000.
- **Win conditions**
  - A single participant hits $100,000 equity.
  - OR top 3 each exceed $25,000 profit (equity ≥ $35,000).
- **RL properties**
  - Observation vector length 12: [bid, ask, tick_count, cash, net_equity, margin_used, margin_available, open_position_count, avg_buy_price, avg_sell_price, agent_rank, top_participant_equity].
  - Action space size 5: {HOLD, BUY, SELL, CLOSE oldest BUY, CLOSE oldest SELL}.
  - Standard RL trade size: 50,000.
- **External price feed**
  - Optional REST endpoint `PRICE_FEED_URL` returning bid/ask data for a symbol (e.g. GBP in `vw_000_fx_quotes`).

## 2. Participants and Rule Generation (`participant_manager.py`)

### Rule-based traders
A rule-based participant stores:
- `buy_threshold`: positive float; if mid-price change over the last tick exceeds this, open BUY.
- `sell_threshold`: usually negative; if mid-price change falls below this, open SELL.
- `trade_size_multiplier`: multiplies a base trade size (10k) but all trades floor to 30k minimum.
- `max_open_positions`: cap (default 3).
- `profit_target_per_unit`: when P/L ≥ size × target, close the position.
- `stop_loss_per_unit`: when P/L ≤ size × stop-loss, close the position.

These parameters are generated randomly at creation and saved into persistent JSON (`simulation_data/participants/<id>.json`). They are not refreshed across runs unless the file is deleted.

### RL agents
- Created without rule thresholds; flagged `is_rl_agent`. Different logic drives their trades via `rl_agent_logic.py`.

### State updates
- Each tick, `get_participant_state_with_mtm` recomputes open P/L, net equity, margin used/available, and disqualifies rule-based traders whose equity drops under $3,000.

## 3. Market Simulation (`market_simulator.py`)

- Maintains `simulation_state`: bid, ask, previous mid, tick count, participants, RL IDs, etc.
- On each tick:
  1. Increment `price_tick_count`.
  2. Fetch external price (if configured) or step a random walk.
  3. Save bid/ask to `market_data.json`, log the event.
  4. Update every participant state with the new prices.
  5. Build a leaderboard (sorted net equity) and compute reward for RL agents as `Δ net_equity`.
  6. Rule-based participants: call `get_rule_based_action` → maybe open/close trades using `execute_trade`/`close_position`.
  7. RL agents: use `get_rl_agent_action` (or action override) to decide trades.
  8. Log high-performing rule-based traders as “experts” (state/action pairs) for imitation learning (saved to `expert_data.jsonl`).
  9. Run `check_game_end_conditions` to see if the simulation should halt.
  10. If still running, schedule another tick via `threading.Timer`.

### Rule-based action logic
```python
price_change = current_mid - previous_mid
# if any open position hits profit target or stop loss, close it first
if len(open_positions) < max_open_positions:
    if price_change > buy_threshold:
        return ('BUY', trade_size)
    elif price_change < sell_threshold:
        return ('SELL', trade_size)
return ('HOLD', None)
```
- Profit target = `size × profit_target_per_unit`.
- Stop loss = `size × stop_loss_per_unit`.
- `trade_size` = `max(base_trade_size × multiplier, MIN_NOTIONAL_PER_TRADE)`.

## 4. Trading Engine (`trading_engine.py`)

- Checks trade size is positive, a multiple of 10,000, within min/max bounds.
- Ensures margin available ≥ `size × MARGIN_REQUIREMENT` prior to entering.
- Ensures open position count < `max_open_positions`.
- BUY fills at current ask; SELL fills at current bid.
- Records every trade with UUID, timestamp, and reduces cash by $5 commission per leg.
- `close_position` calculates realized P/L, adds it to cash and realized P/L, charges closing commission, and logs a `position_closed` event.

## 5. Data & Logging (`data_persistence.py`)

- `save_participant_state` writes the full participant dict (rules included) to disk after each update.
- `log_event` appends JSONL entries to `simulation_log.jsonl`.
- `log_expert_data` stores state-action pairs from top performers.
- `archive_simulation_data` copies current JSON files (market, log, expert data, participant snapshots) into a timestamped archive directory.

## 6. RL Pipeline (`rl_agent_logic.py`, `rl_agent_train.py`, `imitation_agent_train.py`)

- Loads RL models (PyTorch) if available; otherwise agents fall back to random actions.
- Observations are preprocessed into 12-feature vectors; action logits map to {HOLD, BUY, SELL, CLOSE oldest BUY, CLOSE oldest SELL}.
- RL training script connects to Flask API:
  - Verifies simulation running (`/admin/resume` if needed).
  - Closes any residual positions.
  - Loops for `total_steps`, sending actions and collecting rewards (`Δ net_equity`), storing transitions in a replay buffer.
  - Periodically optimizes a DQN (AdamW, Smooth L1 loss, target net soft update).
  - Saves model to `rl_agent_model.pth` on completion.
- Imitation training consumes `expert_data.jsonl` to fit a supervised policy.

## 7. Service & UI

- Flask endpoints in `trader_game.py` expose admin controls (`/admin/start`, `/admin/stop`, `/admin/resume`, etc.), participant APIs, market price, and a JSON leaderboard.
- `trading_activity_viewer_frontend.html` provides a browser-based visualization.
- Batch scripts (`run_training_session.bat`, `train_rl_agents.py`) orchestrate training sessions or evaluation runs.

## 8. SQL Breakout Integration (optional)

- `sp_001_breakout_entry` runs within the live SQL environment:
  - Reads product/model info and recent entries from SQL tables.
  - Logs skip reasons (`reason:no_history`, `reason:open_breakout`, `reason:whitelist`, etc.) to `breakout_debug_ctx`.
  - Declares breakout if current ask ≥ max(previous 5 entry prices) + tolerance (2×10⁻⁵) or bid ≤ min - tolerance.
  - Respects `tradeable_product_list` when setting `tradeable = 1` on insert.

## 9. Example Participant Rules

- `person 103` (`simulation_data/participants/person 103.json`):
  - `buy_threshold`: 0.000274 (≈ 2.74 pips up to buy)
  - `sell_threshold`: -0.000120
  - `trade_size_multiplier`: 1.44 → trades default to 30k
  - `profit_target_per_unit`: 0.001210
  - `stop_loss_per_unit`: -0.001819
- `person 128` (`person 128.json`):
  - `buy_threshold`: 0.000213
  - `sell_threshold`: -0.000157
  - `trade_size_multiplier`: 1.51 → 30k
  - `profit_target_per_unit`: 0.001277, `stop_loss_per_unit`: -0.001562
- `person 084` (`person 084.json`):
  - `buy_threshold`: 0.000414 (slow to go long)
  - `sell_threshold`: 0.000316 (positive → waits for upward move before shorting)
  - `trade_size_multiplier`: 0.93 → 30k
  - `profit_target_per_unit`: 0.001967, `stop_loss_per_unit`: -0.001503
- Entry prices always reflect the quoted ask (BUY) or bid (SELL) at execution; thresholds only determine whether to place the trade.

## 10. Rebuild Checklist

1. Create Flask app (`trader_game.py`) with endpoints: `/admin/*`, `/market/price`, `/leaderboard`, `/participant/<id>/state`, etc.
2. Implement persistent storage for market data, participants, logs, expert data under `simulation_data/`.
3. Implement `participant_manager`, `trading_engine`, `market_simulator` as described above.
4. Generate and persist participant rule sets (only regenerated when states missing).
5. Implement RL action logic and training scripts if required.
6. Optionally, connect SQL breakout proc to produce DB-managed trades.
7. Provide a front-end viewer for live monitoring.

Any implementation that reproduces these components will behave like the original GameTrader system.
