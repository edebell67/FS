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
