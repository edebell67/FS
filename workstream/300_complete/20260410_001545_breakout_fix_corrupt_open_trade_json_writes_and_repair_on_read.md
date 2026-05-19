# Breakout Fix Corrupt Open Trade Json Writes And Repair On Read

- Status: In Progress
- Started: 2026-04-10 00:15:45
- Project: breakout
- Owner: Codex

## Request

Investigate and fix `Extra data` JSON parse failures while refreshing open trade files.

## Findings

- Affected `.op.json` files contain one valid JSON object followed by trailing duplicated fragments.
- Example corruption pattern:
  - valid object ends with `}`
  - trailing text continues with duplicated fragment such as `"product_entries": [] } }`
- This indicates overlapping or non-atomic writes to the same file rather than bad field generation.

## Plan

1. Add atomic JSON write helper for trade-file persistence paths.
2. Add resilient JSON loader that can recover the first valid JSON object from a corrupted file and rewrite it cleanly.
3. Update open-trade save/refresh paths to use the safe helpers.
4. Validate by reading affected files and confirming refresh no longer errors.

## Progress Log

- 2026-04-10 01:34:00: Confirmed affected `.op.json` files contained one valid object followed by trailing duplicated fragments, causing `json.JSONDecodeError: Extra data`.
- 2026-04-10 01:35:00: Added `_write_json_atomic()` and `_load_json_resilient()` to `common.py`.
- 2026-04-10 01:35:00: Updated `_save_trade_json()`, `_finalize_trade_json()`, and `_update_open_trade_json_prices()` to use the safe helpers.
- 2026-04-10 01:36:30: Ran one-shot refresher and automatically repaired multiple corrupted `.op.json` files in place.
- 2026-04-10 01:36:45: Added retry logic to atomic replace on Windows to reduce transient access-denied collisions during concurrent activity.

## Validation

- 2026-04-10 01:36:55: `python -m py_compile C:\Users\edebe\eds\TradeApps\breakout\fs\common.py` -> passed.
- 2026-04-10 01:36:30: `python C:\Users\edebe\eds\TradeApps\breakout\fs\open_trade_price_refresher.py --once --products NZDAUD_C GBPEUR_S GBPNZD_C CHF` -> repaired multiple corrupt files and refreshed prices.
- 2026-04-10 01:37:03: Direct resilient-load check confirmed `breakout_2_tp10.0_sl5.0_2a8a0485_NZDAUD_C_20260410_000012_2_0.00015_10.0_5.0_op.json` now ends cleanly with a single valid JSON object.

## Outcome

Root cause was non-atomic overlapping writes to open trade JSON files. The code now writes trade JSON atomically and can recover already-corrupted files by salvaging the first valid JSON object and rewriting it cleanly.

## Follow-up

- Restart the running breakout and refresher processes so they load the patched `common.py`. Any already-running process still holds the old writer in memory and can reintroduce corruption until restarted.
