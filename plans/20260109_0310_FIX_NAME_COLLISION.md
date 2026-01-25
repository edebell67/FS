# Fix Strategy Name Collision
**Date**: 2026-01-09 03:10
**Version**: V20260109_0310

## Issue
The user identified that the persistence logic (introduced in `V20260108_2330`) allowed strategy names that are prefixes of others (e.g., `breakout` vs `breakout_Rev`) to incorrectly match and claim each other's trade json files.

**Consequence**: `breakout.py` would load `breakout_Rev` trades, reach its live trade limit, and stop trading ("SKIPPING" or "GUARD").

## Fix
Updated `_load_persisted_state` in `common.py` to use a stricter filename check:
```python
fname.startswith(f"{self.script_name}_{self.trade_product}_")
```
This ensures `breakout_` only matches files starting with `breakout_PRODUCT_`, and not `breakout_Rev_PRODUCT_`.

## Verification
1.  **Restart** the trading environment (verify_algo or manual).
2.  `breakout.py` should no longer "resume" trades belonging to `breakout_Rev.py`.
3.  Each strategy should track its own trade count correctly.
