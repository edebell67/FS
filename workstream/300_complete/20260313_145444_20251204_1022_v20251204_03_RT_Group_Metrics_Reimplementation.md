# RT Group Metrics Re-Implementation Plan
**Version:** v20251204_03  
**Date:** 2025-12-04 10:22  
**Objective:** Re-implement RT group metrics in trade_engine.py after file corruption restoration

## 1. Understanding of Requirements
After restoring trade_engine.py from backup (2025-12-03), the RT group metrics feature (V64.3.0/V64.3.1) needs to be re-implemented. This feature allows RT group instances to view aggregated metrics and enforce global limits.

## 2. Plan of Approach
Based on the original plan in `20251202_2300_v64.3.0_RT_Group_Coordination.md`:

1. **Add RT group metrics state variables to TradeManager.__init__()**
2. **Add _fetch_rt_group_metrics() method to TradeManager**
3. **Integrate RT metrics fetch into _periodic_trade_lifecycle_snapshot_loop()**
4. **Modify _send_trade_lifecycle_event() to include is_rt_member and instance_name**
5. **Update version to v20251204_03**

## 3. List of Changes

*   **`algo_viewer/tradepanel/trade_engine.py`**:
    *   [ ] Add `rt_group_metrics` attribute in `TradeManager.__init__()`
    *   [ ] Add `last_rt_metrics_fetch_time` attribute in `TradeManager.__init__()`
    *   [ ] Add `_rt_metrics_fetch_interval` constant (10 seconds)
    *   [ ] Add `_fetch_rt_group_metrics()` method to TradeManager
    *   [ ] Add RT metrics fetch call in `_periodic_trade_lifecycle_snapshot_loop()`
    *   [ ] Modify `_send_trade_lifecycle_event()` to include `is_rt_member` and `instance_name` fields
    *   [ ] Add `is_c_trade` field to lifecycle events

*   **`algo_viewer/tradepanel/Constants.py`**:
    *   [ ] Update version to `v20251204_03`

## 4. Implementation Notes
- RT Membership is determined by `send_csv_to_test_folder_var == False`
- Instance name format: `{app_name_prefix}_{session_guid[:8]}`
- Metrics refresh every 10 seconds
- Only fetch metrics if instance is RT member
