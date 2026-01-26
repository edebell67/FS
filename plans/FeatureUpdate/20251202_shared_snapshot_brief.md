# Shared Lifecycle Snapshot Table

- All tradepanel instances write their trade lifecycle events to `tradedb.dbo.trade_lifecycle_snapshots`. The definition lives in `db_scripts/dbo.trade_lifecycle_snapshots.Table.sql`.
- The table captures open/close/snapshot data with session identifiers so any instance (or aggregation service) can reconstruct system-wide state.

## Requirements

- Instances run independently and already publish each trade lifecycle event to `tradedb.dbo.trade_lifecycle_snapshots`, but they are unaware of each other when enforcing limits (max quantity, max loss/profit, RT ownership).
- Goal: leverage the shared snapshot table so every instance can see aggregated state (e.g., total open quantity, cumulative PnL, RT member status) and enforce global limits when multiple strategies trade the same product.
- Specific constraints:
  * `max trade quantity`: sum of open quantities across RT group must not exceed configured cap.
  * `max loss` / `max daily profit`: combine results from all RT instances so no single instance overshoots.
  * `RT instance`: only designated RT group members should send broker-bound orders.
- Desired outcome: a shared-state service that consumes snapshot data, exposes aggregated stats, and informs each instance whether it can execute new trades.

## RT Group UI Requirements Checklist

For all instances that are members of the RT group, the following information must be visible within the trade section of the UI:

- [ ] **Max Open Trade Quantity**: Display the configured `max_open_trade_qty` limit for the RT group
- [ ] **Current Open Quantity**: Show the current total open quantity across all RT group instances
- [ ] **Available Quantity to Trade**: Calculate and display the remaining quantity available to trade (max allowed minus current open qty)
- [ ] **RT Group Total Profits**: Display the sum of all profits (closed trades) across all instances in the RT group
- [ ] **RT Group Open Profits**: Display the sum of current open profits across all instances in the RT group
- [ ] **RT Membership Status**: Clearly indicate whether the current instance is a member of the RT group

**RT Group Membership Definition:**
- An instance is a member of the RT group if the 'Test CSV' checkbox is **unchecked** on the UI
- Only RT group members should display the aggregated RT group metrics listed above
## Table Definition

```sql
USE [tradedb];
GO
CREATE TABLE [dbo].[trade_lifecycle_snapshots](
    [id] [int] IDENTITY(1,1) NOT NULL PRIMARY KEY,
    [session_id] [varchar](36) NOT NULL,
    [app_trade_id] [bigint] NOT NULL,
    [guid] [varchar](36) NOT NULL,
    [timestamp] [datetime2](7) NOT NULL,
    [event_type] [varchar](10) NOT NULL,
    [trade_type] [varchar](4) NOT NULL,
    [product] [varchar](50) NOT NULL,
    [entry_price] [decimal](18,5) NOT NULL,
    [quantity] [decimal](18,5) NOT NULL,
    [commission] [decimal](18,5) NOT NULL,
    [current_price] [decimal](18,5) NULL,
    [current_pnl] [decimal](18,5) NULL,
    [alt_pnl] [decimal](18,5) NULL,
    [is_active] [bit] NOT NULL,
    [trailing_stop_active] [bit] NOT NULL,
    [current_trailing_stop_level] [decimal](18,5) NULL,
    [peak_net_return_since_trailing_active] [decimal](18,5) NULL,
    [is_flipped] [char](1) NOT NULL,
    [close_reason] [varchar](255) NULL,
    [close_price] [decimal](18,5) NULL,
    [strategy_config] [nvarchar](max) NULL,
    [trade_signal] [varchar](8) NULL
);
```

## Current Usage

- `TradeManager._send_trade_lifecycle_event()` pushes each trade dict (open/close/snapshot) to the backend, which inserts one row per event.
- Columns such as `is_active`, `quantity`, `current_pnl`, `strategy_config`, and `trade_signal` enable dashboards and services to aggregate cross-instance metrics.
- Because every instance writes here, querying by `product` or `session_id` yields a consolidated picture—this is the seed for multi-instance coordination.

## Additional Metadata Requirement

- Current rows only identify session_id (per tradepanel instance). To distinguish RT vs non-RT and support group-level aggregation, add metadata columns (e.g., instance_id, is_rt_member, rt_group_id) or store a companion mapping keyed by session_id so lifecycle snapshots can be filtered accordingly.

## Implications for Multi-Instance Limits

- Summing `quantity` per product across this table lets us enforce global max quantity rather than per-instance caps.
- Aggregating `current_pnl` & `alt_pnl` per day delivers shared loss/profit totals for daily targets.
- Adding instance metadata (instance id, RT group membership) either to this table or a companion table would make it easy to distinguish RT vs non-RT writers when enforcing RT-specific limits.


