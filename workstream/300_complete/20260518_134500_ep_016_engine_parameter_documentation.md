# Task: EP_016 Engine Parameter Documentation
# Date: 2026-05-18 13:45
# Version: V20260518_1345

## Task Type
Documentation

## Destination Folder
epics/ep_016_turning_point_pattern_engine/logic

## Dependency
None

## Objective
Provide a comprehensive explanation of every command-line parameter available in the Turning Point Pattern Engine (price_frequency_pattern_analyzer_v2.py).

## Parameter Reference Guide

### 1. Strategy Configuration (The "Brain")
- **`--h {int}` (High Confidence)**: The primary threshold for "Strong" signals. Pressure must exceed this number (on both Bid and Ask) to trigger a HIGH conviction trade.
- **`--m {int}` (Medium Confidence)**: Threshold for "Moderate" signals.
- **`--l {int}` (Low Confidence)**: Threshold for "Entry-Level" signals.
- **`--bucket {int}` (Minutes)**: The resolution of the pattern. Controls how often the "Open Price" is reset and how long the price clusters accumulate.
- **`--offset {float}` (Pips)**: Adjustment to the entry price. 
    - Negative value (e.g., -0.35) acts as a "Limit Order" (waits for a better price). 
    - Positive value acts as an "Aggressive" fill.

### 2. Risk & Execution (The "Hands")
- **`--tp {float}` (Take Profit)**: Fixed profit target in pips. The trade will automatically close if this gain is reached.
- **`--sl {float}` (Stop Loss)**: Fixed protection floor in pips. The trade will automatically close if this loss is reached.
- **`--cost {float}` (Pips)**: The estimated cost of every trade (Spread + Commission). Default is -2.0. This is subtracted from every completed trade's P&L.
- **`--quantity {int}`**: The unit size for live trades (e.g., 50000). This value is written directly into the JSON order file.

### 3. Synchronization & Persistence (The "Patience")
- **`--poll {float}` (Seconds)**: Controls the logic heartbeat. 
    - Set to **5.0** to match the Backtest data frequency (recommended).
    - Set to **0.5** for high-frequency tick tracking.
- **`--restart`**: A safety flag. If included, the script will ignore any previous saved state for the day and start with 0.0 pips and zero data clusters.
- **`--live`**: The "Master Switch." If this is NOT included, the script runs in "Paper Trading" mode (logs only). If included, it writes real tradeable JSON files to the Z: drive.

### 4. Capital Protection (The "Shield")
- **`--target_pips {float}`**: The daily goal. Once the **Live P&L** hits this number, the script will stop placing new live trades for the day.
- **`--live_floor {float}`**: The "Shadow Mode" trigger. If the **Total P&L** falls below this value (usually 0.0), the script enters "Shadow Mode" and stops sending real orders until it recovers on paper.

### 5. Identification & Routing
- **`--symbol {string}`**: The code to fetch from the Price API (e.g., GBP, GBPAUD_C).
- **`--trade_symbol {string}`**: The symbol written into the JSON order (e.g., AUD). Allows you to analyze a cross-pair but execute on a base currency.
- **`--comment {string}`**: The name of the strategy (e.g., "EP016_V6_UNIV"). This appears in the UI, the window title, and the JSON order files.

## Evidence Inventory
- Objective-Delivery-Coverage: 100%
- Auto-Acceptance: true

## Implementation Log
- 2026-05-18 13:45: Documentation task created and completed per user request.

## Completion Status
**COMPLETE**
