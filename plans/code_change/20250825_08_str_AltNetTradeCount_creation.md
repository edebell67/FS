# Plan: Creation of 08_str_AltNetTradeCount.py

**Version:** 1.6
**Date:** 2025-08-25

---

### Objective

To create a new strategy file, `08_str_AltNetTradeCount.py`, based on the existing `07_str_AvgPriceWithOffset_live.py`, with new buy/sell criteria based on the count of closed trades.

### Status

*   **[x] Created `08_str_AltNetTradeCount.py`** by copying the content of `07_str_AvgPriceWithOffset_live.py`.
*   **[x] Implemented new buy/sell criteria** based on the count of closed trades with positive `alt_net_return`.
*   **[x] Implemented trade management logic** to reverse open trades if the opposing criteria are met.
*   **[x] Implemented a dynamic `created_gt` filter** that updates after a trade is closed.
*   **[x] Updated docstring** to reflect the new logic.
*   **[x] Restricted the closed trades endpoint** to the default product 'gbp'.
*   **[x] Modified the script to use the latest `created` datetime** from the closed trades API for the `created_gt` filter.
*   **[x] Fixed an issue where the script was getting the earliest `created` datetime instead of the latest.**
*   **[x] Fixed an issue where the `created_gt` parameter was not in the correct ISO 8601 format.**
