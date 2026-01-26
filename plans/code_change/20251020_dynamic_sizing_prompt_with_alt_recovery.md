# LLM Prompt: Simulation and Modification of a Trading Game Workflow

### 1. System Overview
This document specifies a simplified workflow for a single rule-based trading agent within a larger trading game simulation. The agent makes decisions based on price changes and its own internal rules. Your task is to understand this workflow, modify it with a new requirement, and then run a simulation using the new rules.

### 2. Core Data Structures
The workflow operates on the following JSON-like data structures:

#### Configuration Object
These are global, static values that control the simulation's constraints.
```json
{
  "STANDARD_TRADE_SIZE": 50000,
  "MIN_NOTIONAL_PER_TRADE": 30000,
  "MAX_NOTIONAL_PER_TRADE": 100000,
  "PROFIT_TARGET_PER_UNIT": 0.0010,
  "STOP_LOSS_PER_UNIT": -0.0010,
  "BUY_THRESHOLD": 0.0001,
  "SELL_THRESHOLD": -0.0001
}
```

#### Participant State Object
This represents the full state of a single trading agent.
```json
{
  "id": "person_01",
  "initial_capital": 10000.0,
  "net_equity": 10000.0,
  "open_positions": []
}
```

#### Position Object
This represents a single open trade within the participant's `open_positions` list.
```json
{
  "type": "BUY",
  "size": 50000,
  "entry_price": 1.2500
}
```

### 3. Existing Workflow Algorithm (Single Tick)
For each tick of the simulation, the following logic is applied to the Participant State:

1.  **Receive Input:** The workflow receives the `price_change` for the current tick (a float, e.g., `+0.00015`).
2.  **Check for Exit:**
    a. If `open_positions` is NOT empty, calculate the current profit/loss (P/L) for the open position.
    b. Check if the P/L meets the exit criteria (`current_pl >= size * PROFIT_TARGET_PER_UNIT` or `current_pl <= size * STOP_LOSS_PER_UNIT`).
    c. If exit criteria are met, the position is considered closed (remove it from the `open_positions` list) and no further action is taken this tick.
3.  **Check for Entry:**
    a. If `open_positions` IS empty, check if the entry criteria are met.
    b. **BUY criterion:** `price_change` > `BUY_THRESHOLD`.
    c. **SELL criterion:** `price_change` < `SELL_THRESHOLD`.
    d. If an entry criterion is met, calculate the `desired_trade_size`. **Currently, this is always equal to `STANDARD_TRADE_SIZE`.**
    e. A new Position Object is created and added to the `open_positions` list.

---

### 4. The Task

#### Part A: Modification Requirement
You must modify the **"Check for Entry"** step (Step 3.d) of the existing workflow. The method for calculating `desired_trade_size` must be replaced with a new dynamic logic.

**New Logic:**
Before creating a new position, you must first calculate a `trade_size_multiplier` based on the participant's current performance. This logic must be governed by new configuration parameters.

**New Configuration:**
```json
{
  "ENABLE_DYNAMIC_TRADE_SIZING": true,
  "PROFITABLE_SCENARIO_MULTIPLIER": 1.5,
  "LOSING_SCENARIO_MULTIPLIER": 0.5
}
```

**Algorithm for calculating `desired_trade_size`:**
1.  If `ENABLE_DYNAMIC_TRADE_SIZING` is `false`, `desired_trade_size` is `STANDARD_TRADE_SIZE`.
2.  If `ENABLE_DYNAMIC_TRADE_SIZING` is `true`:
    a.  **Determine Performance State:**
        - If `net_equity` > `initial_capital`, the state is "Winning".
        - If `net_equity` < `initial_capital`, the state is "Losing".
        - Otherwise, the state is "Neutral".
    b.  **Select Multiplier:**
        - If "Winning", `trade_size_multiplier` = `PROFITABLE_SCENARIO_MULTIPLIER`.
        - If "Losing", `trade_size_multiplier` = `LOSING_SCENARIO_MULTIPLIER`.
        - If "Neutral", `trade_size_multiplier` = 1.0.
    c.  **Calculate Size:** `desired_trade_size` = `STANDARD_TRADE_SIZE` * `trade_size_multiplier`.
3.  **Clamp the Size:** The final `desired_trade_size` must be clamped to be within the `MIN_NOTIONAL_PER_TRADE` and `MAX_NOTIONAL_PER_TRADE` limits.

#### Part B: Simulation Execution
Given the initial Participant State and scenario data below, simulate **3 ticks** of the **modified workflow**. For each tick, you must provide a **constant, descriptive output** that includes the following details in order:

1.  **Start of Tick:** Announce the tick number and the incoming `price_change`.
2.  **Workflow Status: Exit Check:**
    *   State that you are checking exit criteria.
    *   If a position is open, you must report its current unrealized P/L.
    *   If the exit criteria are met, state the reason (e.g., "Stop loss hit") and show the details of the closed trade.
    *   If not, state that the agent will hold the position.
3.  **Workflow Status: Entry Check:**
    *   If no exit occurred and no position is open, state that you are checking entry criteria.
    *   Describe the analysis: Compare the `price_change` to the `BUY_THRESHOLD` or `SELL_THRESHOLD`.
    *   If entry criteria are met:
        *   Announce the participant's performance state (e.g., "Participant is in a 'Winning' state").
        *   Show the calculation for the `desired_trade_size` using the correct multiplier.
        *   Announce the details of the trade **to be executed** (e.g., "Action: Execute BUY of size 75,000").
    *   If criteria are not met, state "No entry criteria met."
4.  **End of Tick Summary:**
    *   Show the final state of the `open_positions` list for that tick.

After all ticks are complete, you must output the final `Participant State` object.

---

### 5. Example Data for Simulation

**Scenario: Winning Participant**

**Initial Participant State:**
```json
{
  "id": "person_01",
  "initial_capital": 10000.0,
  "net_equity": 12000.0,
  "open_positions": []
}
```

**Tick Data (`price_change`):**
1.  `+0.00018`
2.  `-0.00005`
3.  `+0.00025`
---

### 6. Part C: Alt-Perspective Recovery (Less Invasive)

#### Goal
When a side enters a loss streak, keep the original signal **direction** (logical side) but **execute the opposite side**, and evaluate recovery using **`alt_net_return`**. This exploits persistence without changing the core entry/exit thresholds or the dynamic sizing framework.

#### New Configuration
```json
{
  "ENABLE_ALT_RECOVERY": true,
  "LOSS_STREAK_THRESHOLD": 3,
  "ALT_RECOVERY_LOOKBACK": 5,
  "ALT_RECOVERY_EXIT_RULE": "alt_cum_nonnegative_and_last_profitable",
  "ALT_RECOVERY_MAX_TRADES": 6,
  "ALT_RECOVERY_SIZE_MULTIPLIER": 1.0
}
```

#### Participant State Additions
- `loss_streak_count` (tracked per logical side)
- `alt_recovery_active` (bool, per logical side)
- `alt_recovery_trades` (count within the current recovery episode, per logical side)

#### Trigger
Activate when `loss_streak_count ≥ LOSS_STREAK_THRESHOLD` for a logical side **and** `ENABLE_ALT_RECOVERY = true`.

#### Behavior (while `alt_recovery_active`)
- **Signal intake remains unchanged.** If the strategy emits **BUY**, set `logical_side = BUY`.
- **Execution side flips:**
  - If `logical_side = BUY` ⇒ **execute SELL**
  - If `logical_side = SELL` ⇒ **execute BUY**
- **Tagging & accounting:**
  - Set `flip_trade = 1`, persist both `logical_side` (original) and `execution_side` (opposite).
  - Attribute realized P/L to **`alt_net_return` for the `logical_side`**.
- **Sizing:** Use existing dynamic sizing (Winning / Neutral / Losing) × `ALT_RECOVERY_SIZE_MULTIPLIER` (default 1.0), clamped to `MIN_NOTIONAL_PER_TRADE`…`MAX_NOTIONAL_PER_TRADE`.
- **TP/SL:** Unchanged; exits are evaluated on the *executed* side’s P/L.

#### Exit Conditions (end recovery)
Terminate `alt_recovery_active` when **any** of the following hold:
1. **Rule-based:** Over the last `ALT_RECOVERY_LOOKBACK` recovery trades (for that logical side), the cumulative **`alt_net_return ≥ 0`** **and** the **last trade was profitable** (`ALT_RECOVERY_EXIT_RULE`).
2. **Equity recovered:** `net_equity ≥ initial_capital`.
3. **Cap reached:** `alt_recovery_trades ≥ ALT_RECOVERY_MAX_TRADES` (fail-safe).

On exit: reset `loss_streak_count = 0`, `alt_recovery_trades = 0`, clear `alt_recovery_active`, and resume normal (non-flipped) execution with the standard dynamic sizing rules.

#### Worked Example
- Three consecutive **BUY** losses → trigger alt-recovery for `logical_side = BUY`.
- Subsequent **BUY** signals execute as **SELL**, `flip_trade = 1`; realized P/L accrues to **`alt_net_return` of BUY**.
- After two profitable flipped trades (making the last-`ALT_RECOVERY_LOOKBACK` cumulative `alt_net_return ≥ 0`), recovery ends and normal execution resumes.
