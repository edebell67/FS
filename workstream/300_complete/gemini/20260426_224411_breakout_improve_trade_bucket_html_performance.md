Source: User request in Codex session on 2026-04-26
Task Type: standard
Task Attributes:
  recurring_task: false
  looping_task: false
  splittable_task: false
  workflow_task: false
Task Summary: Improve the performance of `TradeApps/breakout/fs/trade_bucket.html`, which is currently very slow.
Context: `TradeApps/breakout/fs/trade_bucket.html`, bucket page load/render path, bucket stats aggregation, drilldown/trade filtering, and any related API or client-side hot paths causing noticeable slowness.
Destination Folder: TradeApps/breakout/fs/
Dependency: None

Plan:
- [ ] 1. Trace and identify the current hot paths in `trade_bucket.html`.
  - [ ] Test: Inspect the load/render flow and locate repeated expensive work or unnecessary API calls; pass when the primary bottlenecks are identified.
- [ ] 2. Implement performance improvements in the slowest paths.
  - [ ] Test: Review code diff and targeted profiling evidence; pass when the expensive work is reduced or deferred without changing intended behavior.
- [ ] 3. Validate the page still behaves correctly after the optimization.
  - [ ] Test: Load `trade_bucket.html` and verify bucket rendering, stats, and drilldowns still work while page responsiveness improves.

## Evidence
Objective-Delivery-Coverage: 0%
Auto-Acceptance: false

## Implementation Log
- 2026-04-26 22:44:11+01:00 Created backlog lifecycle task to improve `trade_bucket.html` performance.

## Changes Made
- None yet.

## Validation
- Pending.

## Risks/Notes
- Likely bottlenecks include per-bucket repeated trade filtering, repeated recalculation of live-net contexts, and sequential/duplicated network requests during page load.

## Completion Status
- Backlog.
