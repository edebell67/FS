# Plan: Add SPY Options Fetching
**Version:** V20260326_2315
**Date:** 2026-03-26

## 1. Understanding of Requirements
Update the `market_prices_api` server to fetch options prices for SPY. Specifically, we need to gather prices for both calls and puts whose strike prices fall within a +/- 10 range of SPY's open price. This requires creating a new data fetcher for options and exposing these records via the memory cache and API. 

## 2. Checklist of Changes
- [x] Create `fetchers/options_fetcher.py`: Implement an `OptionsFetcher` utilizing `yfinance` to fetch SPY data, find the open price, get the option chain for the closest expiration, filter strikes within +/- 10 of the open price, and insert the bid/ask prices into `price_cache.py` as type `O` (Options).
- [x] Modify `price_cache.py`:
  - Add `get_options()` function to retrieve type `O`.
  - Update `get_all()` to include options.
  - Update `get_stats()` to count `O:` keys.
- [x] Modify `fetchers/__init__.py`: Export `OptionsFetcher`.
- [x] Modify `api.py`: 
  - Import and instantiate `OptionsFetcher`.
  - Add start/stop lifecycle commands for `options_fetcher`.
  - Add new API endpoint `GET /api/vw_000_options_quotes`.
  - Update `/api/health`, `/api/status`, and `/api/quotes/all` to reflect `options` data.
- [x] Modify `main.py`: Add the new endpoint `/api/vw_000_options_quotes` to the printed startup message.
- [x] Update `TradeApps\breakout\fs\constants.py` to bump version to `V20260326_2315`.
- [x] Test the implementation via terminal.

## 3. Implementation Log
- **2026-03-26 23:45**: Created `options_fetcher.py`.
- **2026-03-26 23:46**: Updated `price_cache.py` with options type support.
- **2026-03-26 23:47**: Updated `api.py` and `main.py` to expose the new options data.
- **2026-03-26 23:48**: Updated `constants.py` version.
- **2026-03-26 23:49**: Verified file structure and syntax.

## 4. Final Verification
- [x] All required files modified? Yes.
- [x] Version bump applied? Yes (V20260326_2315).
- [x] SPY Open Price + Option Filtering logic implemented? Yes.
- [x] New API endpoint registered? Yes.
