# 2026-03-20 12:50 Rename tb_leadership.json to _tb_leadership.json

## Status: COMPLETE

### Task Overview
The user requested to rename the leadership tracking file `tb_leadership.json` to `_tb_leadership.json` to follow the prefix convention.

### Achievements
- [x] **Generator**: Updated `tb_leadership_generator.py` (V20260320_1250) to output `_tb_leadership.json`.
- [x] **Backend**: Updated `trade_viewer_api.py`’s `_load_tb_leadership` function to use `_iter_day_dirs_for` and lookup `_tb_leadership.json`.
- [x] **Maintenance**: Manually renamed the existing `tb_leadership.json` to `_tb_leadership.json` for 2026-03-20.
- [x] **Automation**: Updated `summary_net_generator.py` version to `V20260320_1250`.
- [x] **Constants**: Updated `Constants.py` version to `V20260320_1250`.

### Files Modified:
- `TradeApps/breakout/fs/tb_leadership_generator.py`
- `TradeApps/breakout/fs/trade_viewer_api.py`
- `TradeApps/breakout/fs/summary_net_generator.py`
- `TradeApps/breakout/fs/Constants.py`
- `plans/20260320_1250_V20260320_1250_Rename_Leadership_Json.md`
