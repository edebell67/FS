# Plan for Product-Scoped Auto-Activation (V20251230_1115)

## 1. Understanding of Requirements
The goal is to modify the auto-activation logic in the Trade Viewer so that every activation is explicitly scoped to a product. Currently, auto-activations (triggered when a strategy's P&L crosses a threshold) are being sent to the API as simple boolean flags, which the backend treats as "Global" (empty product list). The user wants these activations to capture and store the specific product that triggered the activation.

## 2. Plan of Approach
The change will be implemented in the frontend JavaScript logic where the auto-activation API call is constructed.

1.  **Identify Trigger Point**: Locate the auto-activation logic within the `renderSummary` function in `trade_viewer.html`.
2.  **Enhance API Payload**: Modify the `fetch` call to `/api/activations` to send a structured object instead of a boolean.
3.  **Include Product Data**: Ensure the payload includes `active: true`, `manual: false`, and `products: [productCode]`.
4.  **Version Update**: Increment the application version to track this change.

## 3. List of Changes
*   **`TradeApps/breakout/trade_viewer.html`**:
    *   [x] In `renderSummary()`, update the `fetch` call to send a full activation object including the triggering product.
*   **`TradeApps/breakout/constants.py`**:
    *   [x] Update `VERSION` to `V20251230_1115`.

## 4. Verification Plan
*   Load the dashboard with data that triggers an auto-activation (or simulates one).
*   Check the Network tab to confirm the payload sent to `/api/activations` contains the `products` array.
*   Check `activations.json` to verify the strategy entry now contains physical product codes (e.g., `["GBPAUD_C"]`) instead of an empty list.
