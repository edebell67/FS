# Task: PipHunter Signal Unique Product Collapse Fix

## Status
TODO

## Source
- Verification feedback: "signals not collapsing and showing under unique product - fail"
- Prior task: `20260224_103046_piphunter_past_trades_collapse_by_unique_products.md`

## Task Summary
Fix signal detail trade-history collapse behavior so trades reliably load and group under unique products.

## Context
- Screen: `TradeApps/breakout/piphunter/app/app/signal/[id].tsx`
- Suspected issue: trade fetch keyed by `strategy_hint` instead of canonical strategy identifier.

## Implementation Log
- 2026-02-25 11:55:15: Task created in `workstream/100_todo`.
- 2026-02-25 11:55:40: Moved task to `workstream/200_inprogress`.
- 2026-02-25 11:56: Added strategy identifier fallback chain in signal detail trade fetch:
  - `signal.strategy` -> `signal.strategy_name` -> `signal.strategy_hint`.
- 2026-02-25 11:57: Confirmed updated fetch path in `signal/[id].tsx`.
- 2026-02-25 12:00: Hardened strategy resolution to support multiple payload shapes (`strategy`, `strategy_name`, nested `strategy.name/code`, `source_strategy`, `strategy_hint`).
- 2026-02-25 12:01: Added one-time fallback trade fetch using `strategy_hint` when canonical lookup returns empty.
- 2026-02-25 12:02: Normalized product grouping keys (`product/pair/symbol/instrument/product_name`) with uppercase trim to enforce unique-product collapse consistency.
- 2026-02-25 12:07: Added visible UI marker `PAST TRADES BY PRODUCT (FIX 2026-02-25)` to confirm patched binary is installed on device.
- 2026-02-25 12:08: Bumped dynamic app config version to `2.0.2` and Android `versionCode` to `2` to force a new testable install artifact.
- 2026-02-25 21:02: Added dedicated backend signal-trades resolution path (`/signals/<id>/trades`) with strategy + product fallbacks in API service.
- 2026-02-25 21:05: Updated app signal detail screen to use `getSignalTrades(signalId)` as primary source.
- 2026-02-25 21:07: Added backward-compatible fallback in app: if new endpoint is unavailable/unpopulated, try multiple strategy candidates via `getStrategyTrades`.
- 2026-02-25 21:08: Normalized product keys in UI grouping using broader field set (`product/pair/symbol/instrument/product_name`) and consistent uppercasing.
- 2026-02-25 21:14: Tightened UI grouping to canonical pair normalization (`[^A-Z]` stripped; trailing `C/F` removed) and prioritized selected signal pair trades first.

## Changes Made
- Updated `TradeApps/breakout/piphunter/app/app/signal/[id].tsx`:
  - Extended `SignalDetail` with optional `strategy` and `strategy_name`.
  - Changed strategy trade lookup key from `strategy_hint`-only to canonical fallback chain:
    - `strategy` first,
    - then `strategy_name`,
    - then `strategy_hint`.
  - Preserved existing unique-product grouping and collapse behavior.
  - Added robust strategy key resolver for variant signal payload structures.
  - Added fallback strategy trade fetch path when primary key returns no trades.
  - Expanded product-key extraction and normalization to improve unique grouping reliability.
  - Added test marker label in past-trades section for on-device build verification.
- Updated `TradeApps/breakout/piphunter/app/app.config.js`:
  - Version `2.0.1` -> `2.0.2`
  - Android `versionCode` set to `2`
- Updated `TradeApps/breakout/piphunter/api/services/breakout_bridge.py`:
  - Added `get_signal_trades(signal_id, mode, limit)` with:
    - strategy candidate resolution
    - strategy-based Supabase lookup
    - product/pair fallback lookup
    - dedupe/cap logic
- Updated `TradeApps/breakout/piphunter/api/routes/signals.py`:
  - Added `GET /api/v1/signals/<signal_id>/trades`.
- Updated `TradeApps/breakout/piphunter/app/services/api.ts`:
  - Added `getSignalTrades(signalId, limit)`.
- Updated `TradeApps/breakout/piphunter/app/app/signal/[id].tsx`:
  - Primary fetch now uses `getSignalTrades`.
  - Added compatibility fallback using multi-candidate strategy lookup if backend endpoint not yet active.
  - Improved product-key normalization for collapse grouping.
  - Added signal-pair-first filtering so if pair-specific trades exist, only that pair group is shown (prevents many near-duplicate GB/NZD variants).

## Validation
- Static check:
  - `rg -n "strategy\\?|strategy_name\\?|strategyName =|getStrategyTrades" TradeApps/breakout/piphunter/app/app/signal/[id].tsx`
  - Verified fallback strategy key path and trade fetch call are present.
- **ON-DEVICE TEST (2026-02-25 14:50)**:
  - Installed v2.0.2 (Code 3).
  - Outcome: **FAIL**. Signal screen collapse still not working.
  - Action: Need to re-investigate grouping logic and API payload for `pastTrades`.
- Static verification (2026-02-25 21:08):
  - Verified route/method usage:
    - `api/routes/signals.py` contains `/<signal_id>/trades`.
    - `breakout_bridge.py` contains `get_signal_trades`.
    - `app/services/api.ts` contains `getSignalTrades`.
    - `app/signal/[id].tsx` uses `api.getSignalTrades(...)` with fallback.
- User verification requested:
  - Re-test signal detail on device after app+API update.
  - Confirm product sections appear and expand/collapse correctly.

## Completion Status
Awaiting user verification (post-fix retest).
