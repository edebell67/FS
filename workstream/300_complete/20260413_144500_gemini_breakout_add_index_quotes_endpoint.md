# Task: Expand Market Prices API with Index Quotes Endpoint

## 1. Understanding of Requirements
Expand the `market_prices_api` to support a new category of quotes specifically for Index products (es, mes, nq, mnq, rty, m2k). These quotes should be served from a new endpoint `/api/vw_000_index_quotes` and should be hidden from the general `/api/vw_000_futures_quotes` endpoint to avoid redundancy, although they remain part of the system. The source for these index quotes is a local file `index_prices.json`.

## 2. Plan of Approach
1.  **Define Index Products**: Create a list of target index codes: `['es', 'mes', 'nq', 'mnq', 'rty', 'm2k']`.
2.  **Update Cache Layer (`price_cache.py`)**:
    *   Add a new quote type identifier `I` for Index quotes.
    *   Add a `get_indices()` method to the `PriceCache` class.
3.  **Create Index Fetcher (`fetchers/index_fetcher.py`)**:
    *   Implement `IndexFetcher` based on the `FileForexFetcher` pattern.
    *   Monitor `Z:\algo_forex\prices\index_prices.json` (same folder as `forex_prices.json`).
    *   Update the cache with type `I` when data changes.
4.  **Update API Routes (`api.py`)**:
    *   Initialize the `IndexFetcher` in the app startup.
    *   Add the new route `/api/vw_000_index_quotes` to return `cache.get_indices()`.
    *   **Modify `vw_000_futures_quotes`**: Update the logic to filter out any quotes that belong to the Index list (es, nq, etc.) to ensure they only appear in the new endpoint.
5.  **Validation**:
    *   Start the API and verify that `/api/vw_000_index_quotes` returns the content of `index_prices.json`.
    *   Verify that `/api/vw_000_futures_quotes` no longer contains the index symbols.

## 3. List of Changes
*   **`market_prices_api/price_cache.py`**:
    *   [ ] Add `I` type support and `get_indices()` method.
*   **`market_prices_api/fetchers/index_fetcher.py`**:
    *   [ ] New file: Implement file-based fetcher for `index_prices.json`.
*   **`market_prices_api/api.py`**:
    *   [ ] Register `IndexFetcher` in lifespan.
    *   [ ] Add `/api/vw_000_index_quotes` endpoint.
    *   [ ] Add filtering to `/api/vw_000_futures_quotes`.
*   **`TradeApps/breakout/fs/constants.py`**:
    *   [ ] Update version to `V20260413_1445`.
