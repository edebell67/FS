# Breakout Fix Quote Fetch To Prefer Freshest Source

- Status: In Progress
- Started: 2026-04-09 16:28:33
- Project: breakout
- Owner: Codex

## Request

Fix the quote fetch path so stale earlier endpoints do not override fresher later endpoints. The concrete issue observed was `fetch_latest_quotes('CHF')` returning an old `2026-04-08 16:56:10.557779` quote while `http://127.0.0.1:8002/api/vw_000_fx_quotes` was serving fresh `CHF` data.

## Plan

1. Update `fetch_latest_quotes()` in `common.py` to aggregate matching ticks across all candidate URLs.
2. Return the freshest available ticks instead of the first non-empty source.
3. Validate with a direct `CHF` quote fetch and confirm the timestamp moves to the current day/time.

## Progress Log

- 2026-04-09 16:28:33: Created lifecycle record after confirming stale `8001`-sourced `CHF` was masking fresher `8002` FX quotes.
- 2026-04-09 16:28:37: Updated `fetch_latest_quotes()` in `common.py` to aggregate matching ticks across all configured URLs and return the freshest timestamp instead of the first non-empty source.
- 2026-04-09 16:28:40: Ran the standalone refresher for `CHF` after the patch and confirmed the affected `.op.json` updated to the new live price.

## Validation

- 2026-04-09 16:28:35: `python -m py_compile C:\Users\edebe\eds\TradeApps\breakout\fs\common.py` -> passed.
- 2026-04-09 16:28:39: Direct fetch check returned fresh `CHF`: `price=0.79025`, `bid=0.7902`, `ask=0.7903`, `timestamp=2026-04-09 15:28:35.497934`.
- 2026-04-09 16:28:40: `python C:\Users\edebe\eds\TradeApps\breakout\fs\open_trade_price_refresher.py --once --products CHF` -> updated the open trade file.
- 2026-04-09 16:28:49: Verified affected file now shows `current_price=0.79025`, `last_updated=2026-04-09 16:28:40`, `net_return=55.000000000003396`.

## Outcome

The quote fetch path no longer stops at the first stale endpoint. Open trade refresh now uses the freshest `CHF` quote available across the configured sources, which fixes the stale `.op.json` price problem caused by the dead/stale `8001` path masking fresher `8002` FX data.
