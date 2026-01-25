# 20260116 Fix Auto Activation Key Mapping

## Context
Auto Buy/Sell buttons on `strategy_performance.html` were writing activation keys that embed the product *before* the parameter block. The backend (`/api/activations`) only stripped product codes when they appeared at the very end of the key, so manual toggles never matched the pattern consumed by the live strategies in `common.py`. As a result `_get_activation_details` returned `active=False` and no L-trade orders were emitted even with `bypass_criteria_check = "all criteria"`.

## Change
- Added smarter product stripping logic in `trade_viewer_api._extract_product`. It now removes a product token even when it is sandwiched between the base strategy name and the parameter segment (e.g., `..._GBPEUR_C_3_...`).
- The normalization keeps underscores balanced so the canonical key now matches the `{script_name}_{window}_{pip_buffer}_{tp}_{sl}_{direction}_{mode}` form expected by the live loop.

## Validation & Next Steps
- Restart `trade_viewer_api.py` so it reloads `activations.json` with the new key normalization.
- Toggle an Auto Buy/Sell button and confirm the key in `activations.json` loses the embedded product (e.g., `breakout_3_tp10.0_sl10.0_GBPEUR_C_3_...` → `breakout_3_tp10.0_sl10.0_3_...` with `products` array listing `GBPEUR_C`).
- Once normalized, `_get_activation_details` will find the activation and, with bypass mode set to `all`, `_attempt_bypass_entry` should create the L-trade immediately when the button is ON.
