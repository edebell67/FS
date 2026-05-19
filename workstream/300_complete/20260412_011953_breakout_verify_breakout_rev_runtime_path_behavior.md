# Task: Verify breakout_rev Runtime Path Behavior

Source: User request on 2026-04-12 to test `fs/breakout_rev.py`.

Task Type: verification

Task Attributes:
- priority: high
- execution_owner: codex
- workflow_ready: true
- ui_task: false

## Task Summary
Inspect the breakout reverse strategy script, determine the correct launch path and flags, run a focused verification, and confirm whether it uses the corrected product-type-aware JSON day-folder layout instead of the legacy `fs\json\live\{date}` path.

## Validation Plan
- Identify the exact file and runtime entrypoint.
- Run the narrowest viable verification command.
- Inspect resulting logs or filesystem writes relevant to JSON day-folder generation.
- Record whether the script still creates or targets the legacy flat live-date folder.

## Execution Log

### 2026-04-12 01:19
- Identified the relevant runtime wrapper as:
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\breakout_Rev.py`
- Also noted related contrarian variant:
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\breakout_R_Rev.py`

### 2026-04-12 01:22
- Inspected `breakout_Rev.py` and confirmed it delegates to:
  - `run_multiwindow(...)` in `C:\Users\edebe\eds\TradeApps\breakout\fs\common.py`
- Confirmed path creation inside shared runtime flow:
  - `BaseBreakoutStrategy._save_trade_json(...)` uses `_ensure_day_directory(...)`
  - `_ensure_day_directory(...)` delegates to `ensure_day_dir(...)` in `json_layout.py`

### 2026-04-12 01:25
- Ran CLI help check on the strategy entrypoint.
- Ran a direct instantiated save test using `BreakoutStrategyWithReversal` on product `GBPAUD_C`.
- Forced one synthetic open-trade JSON save and checked both:
  - product-type-aware target path
  - legacy flat-date path
- Removed the synthetic JSON artifact immediately after the check.

## Validation Results

### Entry Point Check
- Command:
  - `python "C:\Users\edebe\eds\TradeApps\breakout\fs\breakout_Rev.py" --help`
- Result:
  - Passed
  - Script parses and exposes expected CLI options.

### Direct Path Save Check
- Command:
```powershell
@'
import json
from pathlib import Path
import pandas as pd
from breakout_Rev import BreakoutStrategyWithReversal
from common import COMMISSION_PIPS, SPREAD_PIPS, PIP_BUFFER

strategy = BreakoutStrategyWithReversal(
    window_size=2,
    pip_buffer=float(PIP_BUFFER),
    tp_pips=10.0,
    sl_pips=5.0,
    commission_pips=float(COMMISSION_PIPS),
    spread_pips=float(SPREAD_PIPS),
    trade_product='GBPAUD_C',
    script_name='breakout_Rev_test_path_check',
)
entry_time = pd.Timestamp('2026-04-12 01:00:00')
strategy.open_trade = {
    'id': 999001,
    'guid': 'pathtest',
    'json_base_filename': 'breakout_Rev_test_path_check_pathtest_GBPAUD_C_20260412_010000_2_0.00015_10.0_5.0',
    'json_filename': 'breakout_Rev_test_path_check_pathtest_GBPAUD_C_20260412_010000_2_0.00015_10.0_5.0_op.json',
    'entry_time': entry_time,
    'entry_price': 1.95000,
    'direction': 'LONG',
    'status': 'OPEN',
    'order_sent_net': False,
    'order_sent_alt': False,
    'is_live_trade': False,
    'is_live_scheduled': False,
    'source_screen': 'breakout',
    'source_group': 'breakout',
    'live_cap_group': 'breakout',
    'market_bias_at_open': 'BUY',
}
strategy._save_trade_json(current_price=1.95010)
created = Path(strategy.json_base_dir) / 'forex' / '2026-04-12' / strategy.open_trade['json_filename']
legacy = Path(strategy.json_base_dir) / '2026-04-12' / strategy.open_trade['json_filename']
print(json.dumps({
    'run_mode': strategy.run_mode,
    'product_type': strategy.product_type,
    'created_path': str(created),
    'created_exists': created.exists(),
    'legacy_path': str(legacy),
    'legacy_exists': legacy.exists(),
}))
if created.exists():
    created.unlink()
'@ | python -
```

- Result:
  - Passed
  - Observed output:
```json
{
  "run_mode": "LIVE",
  "product_type": "forex",
  "created_path": "C:\\Users\\edebe\\eds\\TradeApps\\breakout\\fs\\json\\live\\forex\\2026-04-12\\breakout_Rev_test_path_check_pathtest_GBPAUD_C_20260412_010000_2_0.00015_10.0_5.0_op.json",
  "created_exists": true,
  "legacy_path": "C:\\Users\\edebe\\eds\\TradeApps\\breakout\\fs\\json\\live\\2026-04-12\\breakout_Rev_test_path_check_pathtest_GBPAUD_C_20260412_010000_2_0.00015_10.0_5.0_op.json",
  "legacy_exists": false
}
```

## Conclusion

- `breakout_Rev.py` is using the corrected shared runtime path flow.
- It writes to:
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\forex\2026-04-12\...`
- It does not create the legacy flat-date path:
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\2026-04-12\...`
