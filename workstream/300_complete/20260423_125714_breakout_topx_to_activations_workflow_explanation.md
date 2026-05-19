# Breakout TopX To Activations Workflow Explanation

Source: User request, 2026-04-23
Task Type: standard

## Task Attributes
recurring_task: false
looping_task: false
splittable_task: false
workflow_task: false
depends_on: []
feeds_into: []

## Task Summary
Document and explain the workflow process from the Top X Multi-Chart Loader in `fs/workflow_automation.html` through the backend/payload/live-monitoring path to what is displayed in `fs/activations_explorer.html`.

## Context
Primary files to inspect:
- `TradeApps/breakout/fs/workflow_automation.html`
- `TradeApps/breakout/fs/trade_viewer_api.py`
- `TradeApps/breakout/fs/multi_chart.js`
- `TradeApps/breakout/fs/live_monitoring_logic.js`
- `TradeApps/breakout/fs/activations_explorer.html`

Likely artifacts/data files:
- `TradeApps/breakout/fs/workflows.json`
- `TradeApps/breakout/fs/workflow_multi_chart_payload.json`
- `TradeApps/breakout/fs/json/{mode}/{product_type}/{date}/grid_live.json`
- activation/live-monitoring files consumed by `activations_explorer.html`

Requested output:
- Explain the workflow process from Top X Multi-Chart Loader to Activations Explorer.
- Identify what triggers each step.
- Identify what data files/API endpoints are read/written.
- Explain where chart payload generation ends and where activation/live-monitoring begins.
- Clarify what must happen for Top X results to appear in `activations_explorer.html`.

## Destination Folder
Destination Folder: `workstream/300_complete/`

## Dependency
Dependency: Existing workflow automation and activation explorer implementation.

## Plan
- [x] 1. Inspect Top X workflow UI and save/run controls.
  - Test: Identify the relevant controls and API endpoints used by `workflow_automation.html`.
  - Evidence: `workflow_automation.html` loads `/api/workflows`, saves Top X config through `/api/workflows/update`, and runs it through `/api/workflows/run`.

- [x] 2. Trace backend Top X workflow execution.
  - Test: Identify the backend function that creates the Top X multi-chart payload and any optional trade-bucket/live activation behavior.
  - Evidence: `/api/workflows/run` calls `_run_top_x_multi_chart_workflow(...)`; that writes `workflow_multi_chart_payload.json`; if `add_to_tb` creates a live trade bucket, `_sync_bucket_to_grid_live(...)` is called.

- [x] 3. Trace multi-chart payload import and live activation path.
  - Test: Identify how `multi_chart.js` imports Top X payloads and what user/auto actions write live monitoring state.
  - Evidence: `multi_chart.js` calls `/api/workflows/multi_chart_payload`, imports items into `activeOverlays`, and `LiveMonitor.activateGroup(...)` posts selected leaders to `/api/grid_live`.

- [x] 4. Trace Activations Explorer data source.
  - Test: Identify which files/endpoints `activations_explorer.html` reads and how activation rows are derived.
  - Evidence: `activations_explorer.html` reads `/api/activations?mode=...`; backend serves `activations.json`; `_sync_grid_to_activations(...)` derives activation keys from `grid_live.json` entries.

- [x] 5. Write concise workflow explanation in this lifecycle file.
  - Test: Explanation includes triggers, API/file handoffs, and the condition required for Top X items to show in Activations Explorer.
  - Evidence: Explanation captured below in `Workflow Explanation`.

## Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true

- Evidence-Type: file_output
  - Artifact: This lifecycle document after completion.
  - Objective-Proved: Workflow explanation is captured in the task document.
  - Status: captured

- Evidence-Type: manual_verification
  - Artifact: Static code trace references.
  - Objective-Proved: Explanation is grounded in the current code path.
  - Status: captured

## Implementation Log
- 2026-04-23 12:57: Created todo task from user request.
- 2026-04-23 12:59: Moved task to in-progress.
- 2026-04-23 13:11: Traced workflow UI, backend Top X runner, multi-chart import, live-monitoring, grid-live sync, and activations explorer data source.
- 2026-04-23 13:24: Clarified that Trade Bucket is a first-class branch of the Top X workflow when `add_to_tb=true`, not just an implied downstream activation route.

## Workflow Explanation

### 1. Top X Workflow Configuration

The user-facing control starts in `TradeApps/breakout/fs/workflow_automation.html`.

The page loads workflow definitions from:

```text
GET /api/workflows
```

For `top_x_multi_chart_workflow`, the UI renders controls such as:

- `top_x`
- `metric`
- `delta_type`
- `include_scalper`
- `include_rev_scalper`
- `add_to_tb`
- `trade_alt_net`
- `t_split_for_tb`
- `sort_by_most_trades`
- `require_positive_total_net`
- `add_same_parameter_strategies_metrics`
- `merge_charts`
- `product_type` / `product_types`

When the user clicks `Save`, `saveWorkflow(id)` sends the workflow config to:

```text
POST /api/workflows/update
```

That persists the workflow configuration in the backend workflow store, backed by:

```text
TradeApps/breakout/fs/workflows.json
```

When the user clicks `Run Now`, `runWorkflowNow(id)` sends:

```text
POST /api/workflows/run
```

with the selected `id`, `mode`, and `date`.

### 2. Backend Top X Selection And Payload Generation

`POST /api/workflows/run` is handled in `trade_viewer_api.py`.

For the Top X workflow, it calls:

```text
_run_top_x_multi_chart_workflow(mode, date_str, wf)
```

That function:

- Reads the workflow config.
- Loads Top 20 data for the selected date/product type.
- Filters by scalper/rev-scalper options.
- Filters positive net rules if configured.
- Sorts by selected metric or trade count.
- Selects the configured `top_x` rows.
- Optionally expands to same-parameter strategy/metric families.
- Builds a Multi Chart import payload.

The payload is written to:

```text
TradeApps/breakout/fs/workflow_multi_chart_payload.json
```

The payload has source:

```text
top_x_multi_chart_workflow
```

and includes fields such as:

```text
mode
date
preferred_metric
delta_type
group
preset_name
run_id
product_types
merge_charts
items
```

Important distinction:

Creating this payload does not by itself create an Activation Explorer entry. It only makes chart candidates available to `multi_chart`.

### 3. Multi Chart Import

`TradeApps/breakout/fs/multi_chart.js` polls/loads:

```text
GET /api/workflows/multi_chart_payload
```

The backend returns the contents of:

```text
workflow_multi_chart_payload.json
```

`multi_chart.js` stores the payload temporarily in:

```text
localStorage["multi_chart_import_payload"]
```

Then `consumeSummaryImportPayload()` imports payload items into:

```text
activeOverlays
```

Each imported overlay is a chart definition with:

```text
key = "strategy | product"
group = chart card/group name
metric = net / buy_net / sell_net / alt_net
```

If `merge_charts=true` on a Top X payload, all imported Top X items are assigned to the same `payload.group`, so they appear as one merged card in Multi Chart. If `merge_charts=false`, each item keeps its individual `item.group`, so they appear as separate cards.

At this point, the items are visible in Multi Chart, but they are not necessarily active in Activations Explorer.

### 4. Live Monitoring / Grid Live Activation

Activations Explorer is fed from `activations.json`, not directly from `workflow_multi_chart_payload.json`.

The bridge from Multi Chart to Activations Explorer is:

```text
multi_chart active group
-> LiveMonitor
-> POST /api/grid_live
-> grid_live.json
-> _sync_grid_to_activations(...)
-> activations.json
-> GET /api/activations
-> activations_explorer.html
```

In `multi_chart.js`, a group/card can become live monitored. `LiveMonitor.activateGroup(groupName, leader)` sends the current selected leader to:

```text
POST /api/grid_live
```

The payload contains:

```text
group
models: [{ model, product, metric, activated_at }]
source
mode
```

`trade_viewer_api.py` handles this in:

```text
update_grid_live()
```

That endpoint writes to:

```text
TradeApps/breakout/fs/grid_live.json
```

Then it calls:

```text
_sync_grid_to_activations(new_target_list, mode=mode)
```

### 5. Activation Key Generation

`_sync_grid_to_activations(...)` converts `grid_live.json` entries into keys in:

```text
TradeApps/breakout/fs/activations.json
```

Metric mapping matters:

- `metric = net` creates both:
  - `{model}_buy_net`
  - `{model}_sell_net`
- `metric = buy_net` creates:
  - `{model}_buy_net`
- `metric = sell_net` creates:
  - `{model}_sell_net`
- `metric = alt` creates:
  - `{model}_buy_alt`
  - `{model}_sell_alt`

The activation entry stores:

```text
active
manual
auto_promote
activated_at
source
products
```

Manual activation entries are preserved when grid-live entries are synced.

### 6. Activations Explorer Display

`TradeApps/breakout/fs/activations_explorer.html` loads activations from:

```text
GET /api/activations?mode={live|sim}
```

The backend loads:

```text
TradeApps/breakout/fs/activations.json
```

and returns the selected mode section.

The UI parses keys such as:

```text
breakout_2_tp10.0_sl20.0_buy_net
breakout_2_tp10.0_sl20.0_sell_net
```

into:

```text
strategy
direction
mode
products
source
activated_at
```

If both buy and sell net keys exist for the same strategy, the UI collapses them into a single displayed `BOTH • NET` card.

### 7. Key Clarification

Top X Multi-Chart Loader has two different outcomes:

1. Multi Chart visibility:

Running Top X creates `workflow_multi_chart_payload.json`. Multi Chart imports this payload and shows the selected strategies as chart cards.

2. Activation Explorer visibility:

Strategies only appear in Activations Explorer after something writes them to `grid_live.json` and `_sync_grid_to_activations(...)` has updated `activations.json`.

That can happen through:

- Turning on live monitoring for a Multi Chart card/group.
- A live Trade Bucket created by the Top X workflow when `add_to_tb=true`, because bucket activation calls `_sync_bucket_to_grid_live(...)`.
- Other existing grid-live activation paths, such as frequency switch rules or manual activation endpoints.

Therefore:

Running Top X without live monitoring or live TB activation should populate Multi Chart, but should not be expected to populate Activations Explorer.

Running Top X with `add_to_tb=true` can populate Activations Explorer if a valid bucket is created and synced to `grid_live.json`.

Activating a Top X Multi Chart card manually from Multi Chart can also populate Activations Explorer through `/api/grid_live`.

### 8. Explicit Trade Bucket Branch

Trade Bucket is a direct branch inside `_run_top_x_multi_chart_workflow(...)` when the workflow config has:

```text
add_to_tb = true
```

The Top X workflow always creates the Multi Chart payload first. After that, if `add_to_tb=true` and there are sliced Top X candidates, the backend also tries to create live Trade Buckets.

The Trade Bucket branch does this:

1. Loads existing Trade Buckets for the selected `mode`, `date`, and `product_type`.
2. Checks `max_live_tb` so it does not exceed the configured live bucket limit.
3. Deduplicates against existing strategy/product keys.
4. Builds a bucket per selected Top X candidate, subject to validation.
5. Requires at least 2 strategy/metric rows after processing and deduplication.
6. Writes the bucket with:

```text
created_by_workflow = top_x_multi_chart_workflow
live = true
```

7. Saves the bucket into the Trade Bucket storage via `_save_trade_buckets(...)`.
8. Sets the automated source to:

```text
Trade Bucket
```

9. Immediately calls:

```text
_sync_bucket_to_grid_live(new_bucket, mode, date_str, product_type=product_type)
```

That means the Trade Bucket path can populate `grid_live.json` and then `activations.json` without the user manually activating the card in Multi Chart.

So the full branching model is:

```text
Top X workflow run
-> always writes workflow_multi_chart_payload.json
-> Multi Chart can import/display the charts

If add_to_tb=false:
  Activations Explorer is only updated later if a Multi Chart group is activated through LiveMonitor -> /api/grid_live.

If add_to_tb=true:
  Backend also creates live Trade Bucket(s)
  -> _sync_bucket_to_grid_live(...)
  -> grid_live.json
  -> _sync_grid_to_activations(...)
  -> activations.json
  -> Activations Explorer
```

## Changes Made
- Added workflow explanation to this lifecycle file.

## Validation
- Static trace confirmed:
  - `workflow_automation.html` uses `/api/workflows`, `/api/workflows/update`, and `/api/workflows/run`.
  - `trade_viewer_api.py` handles `top_x_multi_chart_workflow` through `_run_top_x_multi_chart_workflow`.
  - Top X output is written to `workflow_multi_chart_payload.json`.
  - `multi_chart.js` imports from `/api/workflows/multi_chart_payload`.
  - `live_monitoring_logic.js` posts live selections to `/api/grid_live`.
  - `trade_viewer_api.py` syncs `grid_live.json` into `activations.json` through `_sync_grid_to_activations`.
  - `activations_explorer.html` reads `/api/activations?mode=...`.

## Risks/Notes
- This is a documentation/explanation task; no code changes are expected unless investigation finds a gap the user asks to fix.
- Need to distinguish Top X multi-chart export from actual live activation. Exporting to Multi Chart may not itself create activation records unless live/TB activation is triggered.
- The exact UI control for enabling live monitoring is in Multi Chart, not in Activations Explorer.
- `add_to_tb=true` is a separate path: if a live bucket is created, it can sync directly to `grid_live.json` and then `activations.json`.

## Completion Status
Status: Complete
Created: 2026-04-23 12:57
Completed: 2026-04-23 13:13
