Source: User request on 2026-04-28 to make momentum_step_pips visible in the config UI.
Task Type: standard
Task Attributes:
  recurring_task: false
  recurrence_type: scheduled
  recurrence_rule: None
  looping_task: false
  loop_until: manual_stop
  splittable_task: false
  split_output_type: files
  split_spawn_task: false
  split_failure_mode: fail_fast
  workflow_task: false
  workflow_name: ""
  workflow_stage: complete
  depends_on: []
  feeds_into: []
Task Summary: Update the configuration UI so the momentum_step_pips setting is visible and editable alongside the existing config fields.
Context: C:\Users\edebe\eds\TradeApps\breakout\fs\config.json and the associated config UI source files.
Destination Folder: C:\Users\edebe\eds\TradeApps\breakout\fs\
Plan:
- [x] 1. Locate the current config UI implementation and how config fields are loaded/rendered.
- [x] 2. Add momentum_step_pips to the visible/editable config UI.
- [x] 3. Verify the field displays correctly and persists through the existing config save flow.
Evidence:
Objective-Delivery-Coverage: 100%
Execution Log:
- 2026-04-28 19:40:17: Task created in workstream/100_todo.
- 2026-04-28 19:4x:xx: Identified the main config UI in C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer.html, where the modal form is rendered from the `sections` schema and saved through the generic `/api/config` flow.
- 2026-04-28 19:4x:xx: Added `momentum_step_pips` to the `⏱️ Timeouts & Thresholds` section as a visible numeric config field.
- 2026-04-28 19:4x:xx: Verified the field definition exists in the config form schema and that the existing generic `getNestedValue` and `setNestedValue` save path will load and persist the value without extra code changes.
Validation:
- Confirmed `Momentum Step Pips` field exists in `trade_viewer.html`
- Confirmed the config renderer still uses `getNestedValue(cfg, field.key)` for display
- Confirmed the config saver still uses `setNestedValue(newConfig, key, val)` for persistence
Outcome:
- `momentum_step_pips` is now visible and editable in the main config UI modal, using the same existing load/save mechanism as the other config values.
