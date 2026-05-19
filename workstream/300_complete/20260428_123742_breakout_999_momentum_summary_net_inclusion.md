Source: User request on 2026-04-28 to investigate whether `momentum` trades should be included in `_summary_net.json`.
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
  workflow_stage: backlog
  depends_on: []
  feeds_into: []
Task Summary: Investigate whether `momentum.py` trade JSON artifacts are currently expected to feed into `_summary_net.json`, whether they already do so implicitly through existing summary generation logic, and what changes would be required if inclusion is intended.
Context: `C:\Users\edebe\eds\TradeApps\breakout\fs\momentum.py`, `C:\Users\edebe\eds\TradeApps\breakout\fs\common.py`, `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\forex\*\_summary_net.json`
Destination Folder: None
Dependency: None
Plan:
- [x] 1. Trace how `_summary_net.json` is generated and which trade sources / `script_name` values are currently included or excluded.
  - [x] Test: Inspect the summary generation path in local code and identify inclusion filters.
  - Evidence: [summary_net_generator.py](/C:/Users/edebe/eds/TradeApps/breakout/fs/summary_net_generator.py) processes generic trade files using `source_strategy` / `script_name` / `app_name` and does not contain a hardcoded allowlist for `breakout`-only script names.
- [x] 2. Determine whether `momentum` trade files already match the expected schema and naming needed for summary inclusion.
  - [x] Test: Compare a representative `momentum` trade JSON structure with the fields consumed by the summary pipeline.
  - Evidence: The generator accepts files that either contain `product` plus `source_strategy` / `script_name`, or can be hydrated from filename pattern `^(strategy)_(guid)_(product)_..._(cl|op).json`; `momentum` filenames and JSON fields match that contract.
- [x] 3. Conclude whether `momentum` should be included, whether it already is, and what code changes would be needed if not.
  - [x] Test: Produce a documented conclusion with code references and any gaps or required follow-on implementation.
  - Evidence: Closed `momentum` trades would already be included automatically. Open `momentum` trades can appear in the floating/open portion of `_summary_net.json`, but they do not contribute to the persistent closed P&L totals until they close. No code change is required for inclusion itself.
Evidence:
Objective-Delivery-Coverage: 100%
- Inclusion logic is generic by strategy key, not hardcoded to `breakout`
- `momentum` naming and metadata are compatible with the summary parser
- Closed-trade requirement is the material condition for persistent summary contribution
Execution Log:
- 2026-04-28 12:37:42: Investigative backlog task created in `workstream/100_todo`.
- 2026-04-28 12:38:00: Task moved to `workstream/200_inprogress`.
- 2026-04-28 12:40:00: Confirmed `common.py` auto-activation logic aggregates strategy keys generically from trade JSON metadata.
- 2026-04-28 12:41:00: Confirmed `summary_net_generator.py` hydrates strategy/product from either trade JSON metadata or generic filename pattern, including `momentum_*` names.
- 2026-04-28 12:42:00: Confirmed `summary_net_generator.py` only persists closed trades into cumulative totals, while open trades are treated as floating/open snapshots.
