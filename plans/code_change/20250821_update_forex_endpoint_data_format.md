**Resolution Plan: Update Forex Price Endpoint and Data Format**

## 1. Understanding of Requirements

The current forex price endpoint `vw_000_forex_prices` needs to be replaced with `vw_000_fx_quotes`. The new endpoint returns data in a different JSON format, where `bid`, `ask`, and `code` (currency) are nested within a `data` array. This change necessitates updates to the constant defining the endpoint and the code responsible for fetching and parsing this data.

**New Data Format:**
```json
{
  "metadata": [
    {"column_name": "id", "data_type": "int"},
    {"column_name": "timestamp", "data_type": "datetime2"},
    {"column_name": "code", "data_type": "varchar"},
    {"column_name": "type", "data_type": "char"},
    {"column_name": "bid", "data_type": "decimal"},
    {"column_name": "ask", "data_type": "decimal"}
  ],
  "data": [
    {"id": 1, "timestamp": "2025-08-21T21:59:56.100644", "code": "gbp", "type": "F", "bid": 1.26508, "ask": 1.26518}
  ]
}
```

## 2. Plan of Approach

The changes will primarily involve updating the `tradepanel/constants.py` file and modifying the `APIClient` in `tradepanel/api.py` to correctly fetch and parse the new data format. Any components that consume the forex price data (e.g., in `tradepanel/trade_engine.py`) will also need to be reviewed and adjusted to handle the new structure where the currency `code` is part of the individual price entry.

## 3. Granular Checklist of Changes

*   **`tradepanel/constants.py`**:
    *   [ ] Update `ENDPOINT_FOREX_PRICES_APP` to use `vw_000_fx_quotes`.
        *   `ENDPOINT_FOREX_PRICES_APP: Final[str] = f"{API_BASE_URL}/vw_000_fx_quotes"`
    *   [ ] Add a comment explaining the change and the new data format.

*   **`tradepanel/api.py`**:
    *   [ ] Locate the method responsible for fetching forex prices (likely `fetch_forex_prices` or similar).
    *   [ ] Modify this method to:
        *   [ ] Expect the new JSON structure with `metadata` and `data` keys.
        *   [ ] Extract the list of price entries from the `data` key.
        *   [ ] For each entry in the `data` list, extract `code`, `bid`, and `ask`.
        *   [ ] Adapt the return format of this method to be compatible with how `trade_engine.py` (or other consumers) expects forex prices. This might involve returning a dictionary mapping currency codes to `(bid, ask)` tuples, or a list of dictionaries.
    *   [ ] Add comments to the modified method explaining the new parsing logic.

*   **`tradepanel/trade_engine.py` (and other consumers)**:
    *   [ ] Review `TradeManager.refresh_data_core()` and any other methods that consume forex price data.
    *   [ ] Adjust how forex prices are accessed and used, considering that the currency `code` is now part of the price data itself, rather than being implicitly known by the endpoint.
    *   [ ] Ensure that the `current_prices` dictionary (or similar structure) in `TradeManager` is correctly populated with the new data.
    *   [ ] Add comments to explain any changes in data consumption.

## 4. Verification Plan

*   [ ] Run the application and ensure it starts without errors.
*   [ ] Monitor logs for any errors related to API calls or data parsing.
*   [ ] Verify that forex prices are correctly displayed in the UI (if applicable).
*   [ ] Confirm that any trading logic dependent on forex prices (e.g., price updates, trade execution) functions as expected with the new data.
