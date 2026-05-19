# Task: EP_016 Signal Locking Specification
# Date: 2026-05-18 17:20
# Version: V20260518_1720

## Task Type
Architectural Alignment

## Destination Folder
epics/ep_016_turning_point_pattern_engine/logic

## Dependency
20260517_012000_ep_016_logic_restoration_and_collision_prevention.md

## Objective
Specify the logic required to make the Live Engine's processing 1:1 identical to the Backtester while maintaining real-time risk management.

## Technical Requirement: "Signal Locking"

### 1. Data Capture (The Pulse)
- **Requirement**: The engine MUST continue to poll at **5.0-second intervals**.
- **Reason**: This is required to populate the internal `price_data` dictionary with the same resolution (96 snapshots per bucket) used by the backtester. 
- **Failure Mode**: Setting `--poll` to the bucket size (e.g., 480s) results in an empty cluster and zero signals.

### 2. Decision Gating (The Lock)
- **Requirement**: The variable `state` (e.g., LONG_HIGH, FLAT) must ONLY be updated at the transition of a bucket (e.g., at 12:00:00, 12:08:00, 12:16:00).
- **Behavior**: 
    - During the 8-minute accumulation period, the engine continues to record prices but ignores any new signals.
    - At the start of a new bucket, the engine evaluates the *completed* cluster of the prior bucket and locks in the new `state`.
- **Reason**: This matches the "Patient" execution of the backtester and eliminates "Mid-Bucket Noise."

### 3. Risk Management (The Exception)
- **Requirement**: **Take Profit (TP)** and **Stop Loss (SL)** checks MUST remain active on every 5.0-second pulse.
- **Reason**: Unlike the signal brain, capital protection cannot wait for an 8-minute boundary. This provides "Synchronized Signals + Real-time Safety."

## Evidence Inventory
- Objective-Delivery-Coverage: 100%
- Auto-Acceptance: true

## Implementation Log
- 2026-05-18 17:15: Identified that large `--poll` values break cluster formation.
- 2026-05-18 17:20: Drafted Signal Locking spec to achieve 1:1 backtest alignment.

## Completion Status
**SPECIFICATION COMPLETE**
