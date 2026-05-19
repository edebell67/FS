Source: Direct user request in this session.

Task Summary: Add a `T-split` checkbox to the FS Top X Multi-Chart Loader workflow so that Trade Bucket creation splits `metric=net` selections into `buy_net` and `sell_net` only when all of the following are true: `add_to_tb=true`, metric basis is `T`/`net`, and `T-split=true`.

Context:
- `C:\Users\edebe\eds\TradeApps\breakout\fs\workflow_automation.html`
- `C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py`
- `C:\Users\edebe\eds\TradeApps\breakout\fs\workflows.json`

Plan:
- [x] 1. Add a persisted `T-split` workflow config control for Top X Multi-Chart Loader in the FS workflow automation UI.
  - [x] Test: Source inspection confirms the checkbox is rendered and saved into workflow config.
  - Evidence: `workflow_automation.html` now renders `topx_tsplit_<id>` and saves `t_split_for_tb` into the workflow config payload; `workflows.json` now includes `"t_split_for_tb": false` in the Top X workflow defaults.
- [x] 2. Update Top X TB creation logic so `metric=net` splits into `buy_net` + `sell_net` only when `add_to_tb=true` and `T-split=true`.
  - [x] Test: Code path inspection and validation confirm net-based TB creation remains unsplit by default and splits only when the new flag is enabled.
  - Evidence: `trade_viewer_api.py` now reads `t_split_for_tb` and sets Top X TB `should_split` true for the guarded case `(selected_metric == "net" and t_split_for_tb)`, while preserving the existing `buy_sell` and single-row split behavior.
- [x] 3. Verify non-target cases remain unchanged.
  - [x] Test: Confirm `buy_net`, `sell_net`, and existing `buy_sell` behavior are unaffected by the new flag.
  - Evidence: The new condition only augments the `metric=net` branch; `buy_sell` continues to force split behavior, while directional metric modes remain unchanged.

Implementation Log:
- 2026-03-13 21:11 +00:00: Created this task from the user request to add a guarded `T-split` option for Top X Trade Bucket creation.
- 2026-03-13 21:18 +00:00: Updated the workflow automation UI and workflow defaults to persist a new `t_split_for_tb` flag for the Top X workflow.
- 2026-03-13 21:20 +00:00: Updated Top X TB creation logic so `metric=net` only splits into `buy_net` and `sell_net` when `t_split_for_tb` is enabled.

Changes Made:
- `C:\Users\edebe\eds\TradeApps\breakout\fs\workflow_automation.html`
  - added a `T-split for TB` checkbox for `top_x_multi_chart_workflow`
  - added save-path wiring for `t_split_for_tb`
- `C:\Users\edebe\eds\TradeApps\breakout\fs\workflows.json`
  - added `"t_split_for_tb": false` to the Top X workflow default config
- `C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py`
  - read `t_split_for_tb` from workflow config
  - updated Top X TB split logic so `metric=net` splits only when the new flag is true

Validation:
- `python -m py_compile C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py`
  - PASS
- `rg -n "t_split_for_tb|topx_tsplit_" C:\Users\edebe\eds\TradeApps\breakout\fs\workflow_automation.html C:\Users\edebe\eds\TradeApps\breakout\fs\workflows.json C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py`
  - PASS: UI, config, and backend references are present and connected.
- User verification:
  - PASS 2026-03-13: user confirmed
    - `1 - yes` checkbox appears in UI
    - `2 - yes` `metric=net` + `add_to_tb=true` remains unsplit when `T-split` is off
    - `3 - yes` `metric=net` + `add_to_tb=true` splits into `buy_net` and `sell_net` when `T-split` is on

Risks/Notes:
- The new flag affects Trade Bucket creation only; Multi-Chart payload behavior for `metric=net` remains unchanged.
- `buy_sell` still implies split behavior and is not controlled by this new flag.

Completion Status:
- Complete - 2026-03-13 21:24 +00:00
