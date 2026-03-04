# Task: Core Engine - Formulation Gate Logic

## Status
COMPLETE

## Implementation Log
- 2026-02-22 22:17 - Started implementation
- 2026-02-22 22:19 - Added formulation endpoint to strategies routes
- 2026-02-22 22:20 - Added promotable endpoint
- 2026-02-22 22:21 - Implemented FORMULATION_MIN_TRADES threshold
- 2026-02-22 22:22 - Added is_formulated(), get_strategy_formulation()
- 2026-02-22 22:23 - Added get_promotable_strategies()
- 2026-02-22 22:25 - Verified endpoints working

## Source Document
`000_backlog/20260222_205900_pipHunter_signal_marketplace_mobile_functionality_v2 (3).md` - Section 1.4

## Description
Implement the Formulation Gate that requires strategies to meet a minimum daily trade count before becoming eligible for promotion.

## Sub-tasks
- [x] Define configurable minimum trade count threshold (FORMULATION_MIN_TRADES = 5)
- [ ] Create `strategy_formulation` table - Using computed status
- [x] Implement trade count tracking per strategy per day
- [x] Create formulation check function: `is_formulated(strategy_id)`
- [x] Add formulation status to strategy response
- [x] Implement `/api/v1/strategies/{id}/formulation` endpoint
- [x] Add `/api/v1/strategies/promotable` endpoint
- [x] Implement "Forming" status indicator (PENDING, FORMING, FORMULATED)
- [ ] Create formulation event logging - Future
- [ ] Implement daily formulation reset - Implicit via date filter

## Changes Made

### Files Modified
1. `piphunter/api/routes/strategies.py`:
   - Added `get_strategy_formulation()` route
   - Added `get_promotable_strategies()` route

2. `piphunter/api/services/breakout_bridge.py`:
   - Added `FORMULATION_MIN_TRADES = 5` constant
   - Added `is_formulated()` method
   - Added `get_strategy_formulation()` method
   - Added `get_promotable_strategies()` method

### Data Model
Formulation response includes:
- trade_count, min_required, is_formulated
- status (PENDING, FORMING, FORMULATED)
- trades_remaining, daily_pnl, can_be_promoted

## Verification Test Results
1. GET /api/v1/strategies/{name}/formulation - PASS
2. Strategy with 12 trades shows FORMULATED - PASS
3. GET /api/v1/strategies/promotable - PASS: Returns formulated + profitable strategies

## Completion Date
2026-02-22 22:26
