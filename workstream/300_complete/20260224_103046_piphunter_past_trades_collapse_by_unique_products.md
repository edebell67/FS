# Task: PipHunter Past Trades - Collapse by Unique Product

## Task Summary
Add functionality to the past trades view to collapse trade rows under separate unique products, so users can review historical activity grouped by product first, then expand to see underlying trades.

## Context
- Area: PipHunter past trades/history UI and its backing aggregation/query logic.
- Goal: improve scanability when many trades exist across multiple products.
- Expected behavior: one collapsible section per unique product.

## Implementation Log
- 2026-02-24 10:30:46: Task created from user request and added to `workstream/100_todo`.
- 2026-02-24 15:26: Moved task to `workstream/200_inprogress`.
- 2026-02-24 15:30: Located applicable view at `app/signal/[id].tsx` (signal history context).
- 2026-02-24 15:36: Implemented product-collapsed history rendering with expandable sections per product.

## Changes Made
- Updated `TradeApps/breakout/piphunter/app/services/api.ts`:
  - Added `getStrategyTrades(strategyName, limit=50)` endpoint wrapper.
- Updated `TradeApps/breakout/piphunter/app/app/signal/[id].tsx`:
  - Added strategy-trade fetch after signal detail load.
  - Added grouping logic for past trades by product (`trade.product` or `trade.pair`).
  - Added collapsible UI sections (expand/collapse per product).
  - Added product-level totals and per-trade rows under each product section.
  - Added empty state when no trade history is available.

## Validation
- Static validation:
  - Verified new API method exists and is used by signal detail screen.
  - Verified grouped/collapsible UI paths are present in `signal/[id].tsx`.
- Command: `npx tsc --noEmit`
  - Result: fails due to pre-existing repository baseline type errors in legacy `App.tsx` and `profile.tsx` files; no new errors attributable to the past-trades collapse implementation.
- Runtime verification guidance:
  - Open a signal detail screen and confirm past trades collapse under unique products and expand correctly.

## Risks/Notes
- Need clear definition of "product" key (e.g., symbol, instrument id, product code) to avoid incorrect grouping.
- Confirm sort order: by product name, trade time, or P&L totals.
- Confirm whether collapsed state should persist across refresh/navigation.

## Completion Status
Complete - implementation delivered; runtime verification recommended on device/simulator.

