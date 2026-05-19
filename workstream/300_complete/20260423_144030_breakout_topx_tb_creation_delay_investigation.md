# Breakout Topx Tb Creation Delay Investigation

Source: User request, 2026-04-23
Task Type: investigation

## Task Summary
Investigate why the Top X Multi-Chart Loader workflow was activated/transferred at 02:00 but the first Trade Bucket creation appears at 08:32.

## Plan
- [x] Inspect workflow config and scheduling for `top_x_multi_chart_workflow`.
- [x] Inspect generated payload and Trade Bucket artifacts for relevant product/date folders.
- [x] Check whether `add_to_tb`, product type, max live TB, min rows, or source gating delayed TB creation.
- [x] Summarize the actual reason with file evidence.

## Implementation Log
- 2026-04-23 14:40: Created investigation task.
- 2026-04-23 14:52: Confirmed current Top X config: enabled, start `02:00`, interval 300s, `add_to_tb=true`, `delta_type=delta2`, product type `forex`.
- 2026-04-23 14:53: Confirmed first recorded Top X history entry for forex/2026-04-23 is `2026-04-23T04:45:27.296086`, not 02:00.
- 2026-04-23 14:54: Confirmed current Trade Bucket records start at `2026-04-23T08:32:13`.
- 2026-04-23 14:56: Confirmed grid-live archive at `02:15:22` contained only `weekly_performance` and `freq_switch_rule`; no TB source existed before the 08:32 archive.

## Findings

The `02:00` setting is only the workflow active-window start. It is not a guarantee that a Trade Bucket is created at 02:00.

Current workflow config:

```text
id: top_x_multi_chart_workflow
enabled: true
start_time: 02:00
run_interval_sec: 300
add_to_tb: true
delta_type: delta2
product_type: forex
```

Actual artifacts:

```text
_top10_history first entry: 2026-04-23T04:45:27.296086
_trade_buckets first current TB: 2026-04-23T08:32:13.350894
```

The first two current TBs were:

```text
AUTO_TB_0423_083213_350_EUR_breakout_R_2_tp5_0_sl30_0
AUTO_TB_0423_083213_435_EUR_breakout_R_2_tp5_0_sl50_0
```

Both were created by:

```text
created_by_workflow: top_x_multi_chart_workflow
delta_type: delta2
live: true
```

`grid_live_history/grid_live_live_20260423_021522.json` proves the 02:15 grid state was still:

```text
weekly_performance
freq_switch_rule
```

No `TB_...` source existed there. The next relevant archive at `08:32:13` still shows the same pre-TB state, meaning the 08:32 run is the first visible TB sync point.

Between 04:45 and 08:06, Top X history shows the same top candidates dominated by:

```text
EURAUD_C breakout_2_tp20.0_sl3.0
EURNZD_C breakout_2_tp20.0_sl3.0
GBPEUR_C breakout_2_tp20.0_sl3.0
EURAUD_C breakout_2_tp20.0_sl5.0
EURNZD_C breakout_2_tp20.0_sl5.0
```

The EUR candidates that ultimately produced the first TBs first appear in the Top X history at:

```text
2026-04-23T08:11:28.150683
EUR breakout_R_2_tp5.0_sl30.0
EUR breakout_R_2_tp5.0_sl50.0
```

However, the code does not persist skip reasons for failed Top X-to-TB attempts. Therefore the exact reason why runs at 08:11, 08:16, 08:21, and 08:27 did not create TBs cannot be proven from current artifacts. The likely causes are one of:

```text
add_to_tb was not enabled at those run ticks
or the summary/family expansion did not yet produce >=2 valid positive rows
or the workflow config differed before the later saved version
```

What is proven:

```text
No TB was generated at 02:00.
The auto workflow did not record Top X history until 04:45.
The first persisted current TB creation is 08:32.
The active-window start time is not the TB creation trigger.
TB creation requires a valid Top X candidate plus a valid same-parameter family with >=2 strategy/metric rows.
```

## Validation
- Inspected `TradeApps/breakout/fs/workflows.json`.
- Inspected `TradeApps/breakout/fs/json/live/forex/2026-04-23/_trade_buckets.json`.
- Inspected `TradeApps/breakout/fs/json/live/forex/2026-04-23/_top10_history.json`.
- Inspected `TradeApps/breakout/fs/grid_live_history/grid_live_live_20260423_021522.json`.
- Inspected `TradeApps/breakout/fs/grid_live_history/grid_live_live_20260423_083213.json`.

