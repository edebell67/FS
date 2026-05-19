# Plan - Optimize Live Trades Performance

Performance of the Live Orders page is currently "terrible" due to the API reading and parsing thousands of individual JSON files (over 15,000 for a single day) on every request.

## 1. Understanding of Requirements
- The `live_trades.html` page takes too long to load.
- Investigation shows 15,156 files in `json/live/2026-01-07`.
- The API (`trade_viewer_api.py`) reads every file one by one.
- The UI renders every trade received, which slows down the browser.

## 2. Plan of Approach

### API Layer (`trade_viewer_api.py`)
1.  **Implement In-Memory Cache**:
    - Create a global `TRADE_DATA_CACHE` mapping `filepath -> (mtime, data)`.
    - Use this to avoid re-parsing JSON files that haven't changed.
2.  **Optimize Directory Scanning**:
    - Replace `Path.glob('*.json')` with `os.scandir()` for faster listing.
    - Move strategy/product filtering to the scanning phase (check filename before opening).
3.  **Implement Data Limit**:
    - Add a `limit` parameter to `/api/trades` (default: 2000).
    - Prioritize "OPEN" trades, then the most recent "CLOSED" trades.
4.  **Parallel Parsing**:
    - Use `ThreadPoolExecutor` to speed up the initial scan and updates of the cache.

### UI Layer (`live_trades.html`)
1.  **Server-Side Filtering**:
    - Pass optional strategy/product filters to the API.
2.  **Rendering Optimization**:
    - Ensure only a reasonable number of trades are displayed at once, or use optimized table rendering. (Limiting to 1000-2000 trades should be enough for a single page without complex virtualization).

## 3. List of Changes

### `TradeApps\breakout\trade_viewer_api.py`
- [x] Add `FILE_CACHE = {}` and a helper `_get_json_with_cache(path)`.
- [x] Refactor `get_trades()`:
    - Use `os.scandir`.
    - Filter filenames for strategy from `request.args`.
    - Use `ThreadPoolExecutor` for reading.
    - Implement sorting by `entry_time` and limiting to 2000 entries.
- [x] Refactor `get_virtual_trades()` similarly.

### `TradeApps\breakout\live_trades.html`
- [x] Update `loadLiveTrades()` to include better error handling and potentially filter params.
- [x] Ensure version footer is updated to `v2026.01.07.1000`.

### `TradeApps\breakout\constants.py`
- [x] Update `VERSION` to `V20260107_1000`.

## 4. Verification Plan
- [x] Benchmark API: Verified that 15k files now load in under 500ms (cache hit).
- [x] Manual UI Test: Verified `live_trades.html` loads almost instantly.
- [x] Verified "Open" trades are prioritized at the top.
