# Plan - Incorporate auto_trade_count_mode into Config UI

This plan describes the changes needed to add the `auto_trade_count_mode` field to the Strategy Configuration modal in the Trade Viewer.

## 1. Understanding of Requirements
- Add a new field `auto_trade_count_mode` to the Config UI.
- Possible values: `"max_count"` or `"min_trades"` (default).
- "max_count": Selects only the single strategy with the highest number of trades.
- "min_trades": Selects all strategies that meet the `min_auto_trades` setting.
- The field is already present in `config.json`.

## 2. Plan of Approach
1.  **Modify `trade_viewer.html`**:
    *   Update the `renderConfigForm` function to include the `auto_trade_count_mode` field in the "🛡️ Guards & Safety" section as a select dropdown.
2.  **Modify `constants.py`**:
    *   Update the `VERSION` constant to `V20260107_0430`. (Done by User)
3.  **Update `live_trades.html`**:
    *   Update the version in the footer to `v2026.01.07.0430`.

## 3. List of Changes

### `TradeApps\breakout\trade_viewer.html`
- [x] Add `{ label: 'Auto Trade Mode', key: 'auto_trade_count_mode', type: 'select', options: ['min_trades', 'max_count'] }` to the `sections` array in `renderConfigForm`.

### `TradeApps\breakout\constants.py`
- [x] Update `VERSION` to `V20260107_0430`. (Done by User)

### `TradeApps\breakout\live_trades.html`
- [x] Update version in footer to `v2026.01.07.0430`.

## 4. Verification Plan
- [x] Open the Strategy Configuration modal and verify the "Auto Trade Mode" dropdown is present and populated.
- [x] Change the value, save, and verify it updates in `config.json`.
- [x] Verify the version numbers are updated.
