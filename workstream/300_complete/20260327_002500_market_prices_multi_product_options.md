# Plan: Multi-Product Options Support
**Version:** V20260327_0110
**Date:** 2026-03-27

## 1. Understanding of Requirements
Expand the `market_prices_api` to support multiple options products simultaneously and allow on-demand addition of new symbols without restarting the server.

## 2. Checklist of Changes
- [x] Modify `fetchers/options_fetcher.py`:
  - [x] Changed `self.symbol` to `self.symbols` list.
  - [x] Updated `_fetch_all()` to iterate through all tracked symbols.
  - [x] Added thread-safe `add_symbol(symbol)` method.
  - [x] Improved caching key and provider identification: `yahoo-options-{symbol}`.
- [x] Modify `api.py`:
  - [x] Updated `/api/vw_000_options_quotes` to support `symbol` query parameter for filtering.
  - [x] Added `POST /api/options/add_symbol` to dynamically register new tickers.
- [x] Modify `TradeApps/breakout/fs/constants.py`: Bump version to `V20260327_0110`.

## 3. Implementation Log
- **2026-03-27 01:08**: Converted `OptionsFetcher` to multi-symbol list.
- **2026-03-27 01:10**: Added POST registration endpoint in `api.py`.
- **2026-03-27 01:11**: Updated Constants version.

## 4. Verification
- `GET /api/vw_000_options_quotes?symbol=QQQ` will now filter specifically for QQQ options if already tracked.
- `POST /api/options/add_symbol?symbol=TSLA` will add TSLA to the background polling loop instantly.
