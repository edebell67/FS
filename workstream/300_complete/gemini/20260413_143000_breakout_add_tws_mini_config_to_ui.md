# Task: Add Mini-Product Substitution Config to UI

## 1. Understanding of Requirements
Add a new configuration section to the Breakout Trade Viewer UI (`trade_viewer.html`) to manage "Mini" product substitution. This config will be used by the execution engine to swap full-sized contracts for mini/micro contracts (e.g., ES -> MES) at the point of sending orders to TWS.

The configuration structure should be:
```json
"trade_mini_config": {
    "enabled_products": ["ES", "NQ"],
    "symbol_map": {
        "ES": "MES",
        "NQ": "MNQ",
        "GC": "MGC"
    }
}
```

The UI must support:
- Toggling "Mini Mode" for specific products.
- Editing and extending the symbol mapping list.

## 2. Plan of Approach
1.  **Modify `trade_viewer.html`**:
    *   **Section 1 (Enabled Products)**: Add a new entry to the `multiSections` array for `trade_mini_config.enabled_products`. This will automatically provide checkboxes and an "Add Custom" input.
    *   **Section 2 (Symbol Map)**: Add a new `config-section` containing a `textarea` for editing the `trade_mini_config.symbol_map` as a JSON object. This follows the established pattern for product-specific mappings in the system.
    *   **Section 3 (Data Binding)**: Ensure `renderConfigForm` correctly initializes these new fields from the loaded `config.json`.
    *   **Section 4 (Data Collection)**: Update `collectConfig()` to correctly extract the list of enabled products and the parsed JSON mapping from the textarea before saving.
2.  **Validation**:
    *   Open the Config Modal in the UI.
    *   Add "ES" to the enabled list.
    *   Update the mapping to include `"ES": "MES"`.
    *   Save and verify that `config.json` on the server reflects the changes.

## 3. List of Changes
*   **`TradeApps/breakout/fs/trade_viewer.html`**:
    *   [x] Update `renderConfigForm` to include the `enabled_products` multi-select and `symbol_map` JSON editor.
    *   [x] Update `collectConfig` to handle the new `trade_mini_config` structure.
*   **`TradeApps/breakout/fs/constants.py`**:
    *   [x] Update version to `V20260413_1430`.

## Completion Status
**COMPLETE** - All changes implemented and verified.
**Completion Date**: 2026-04-13 14:45