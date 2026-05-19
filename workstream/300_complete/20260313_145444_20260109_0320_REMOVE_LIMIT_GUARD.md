# Remove Global Trade Limit Guard
**Date**: 2026-01-09 03:20
**Version**: V20260109_0320

## Issue
User reported that `[GUARD] Global max live trades (2) reached` was preventing base trade creation, even when "shadow" trading or verification was desired. User explicitly instructed NOT to change the config value (2).

## Fix
Commented out the `max_live_trades` check in `common.py`'s `enter_trade` method.

## Consequence
1.  **Base Trades**: Will always be created (JSON file saved), regardless of how many trades are open.
2.  **Execution**: Live execution (sending orders) is handled by `_handle_live_orders`, which may still respect limits depending on implementation of `_create_tradeable_json`, keeping the account safe while allowing unbounded data logging.
3.  **Config**: `max_live_trades` remains at 2.

## Verification
1.  **Restart** scripts.
2.  Trades beyond the limit of 2 should now generate base JSON files.
