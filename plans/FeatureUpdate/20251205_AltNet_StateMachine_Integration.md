# Alt-Net State Machine Integration Plan

**Date:** 2025-12-05

## Background
The simple_trend_trader currently writes JSON trade files for every open/close event without checking whether a trade qualifies as a 'C' trade. We now need to gate the 'C' allocations using AltNetStateMachine while still opening trades normally.

## Requirements
1. **State Machine Usage**
   - Instantiate AltNetStateMachine once per strategy run.
   - On every trade close (primary and reverse), call on_close(side, alt_net, timestamp) with the recorded alt_net PnL and close time.
   - Before writing an open-trade JSON, call can_open(side) to decide whether a 'C' allocation should be emitted. Trades still open even if can_open returns False; we simply skip JSON generation.
   - After opening a trade (and writing JSON if applicable), call on_open(side) to maintain dominance tracking.

2. **Persistence**
   - Save the state machine snapshot to disk (e.g., alt_net_state.json) whenever state changes, and reload it on startup so restarts preserve eligibility.

3. **Configuration**
   - Add a config toggle (default True) that enables the state machine logic. When disabled, the system reverts to always writing JSON files.
   - Respect existing reverse-trade options (Reverse Trades, Replace_Reverse_trade, etc.) while gating only the 'C' allocation.

4. **Backups & Comments**
   - Create timestamped backups (YYYYMMDD_HHMMSS) for every modified file before editing.
   - Add concise comments explaining the new state-machine hooks.

## Checklist
- [ ] Create backups of Trades/simple_trend_trader.py and any new/modified helper modules.
- [ ] Implement state-machine instantiation, persistence load/save, and wiring into open/close paths.
- [ ] Add config flag to enable/disable the new behavior (default enabled).
- [ ] Ensure reverse-trade handling respects the same gating logic.
- [ ] Update documentation/comments to explain the new flow.
- [ ] Validate workflow manually (no automated tests available) to confirm JSON generation only occurs when AltNetStateMachine allows a 'C' trade.
