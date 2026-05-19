## Task

Investigate why `C:\Users\edebe\eds\TradeApps\breakout\fs\grid_live_history` is receiving so many archive snapshots today and determine whether `activations.json` and/or `grid_live.json` are being rewritten more frequently than the actual number of intended activation switches.

## Source

- User request in Codex thread on 2026-04-20 after reviewing suspicious `activated_at` timestamps in `activations.json`.
- Codex inspection showing many `grid_live_history\grid_live_live_20260420_*.json` snapshots and mismatches between `activations.json` activation times and first-seen entries in grid history.

## Task Type

standard

## Task Attributes

- recurring_task: false
- looping_task: false
- splittable_task: false
- workflow_task: false
- depends_on: []
- feeds_into: []

## Task Summary

Trace the code paths that archive `grid_live.json` and update `activations.json`, quantify how often they fired today, and identify whether redundant rewrites, reconciliation loops, or UI/API sync behavior are creating excessive `grid_live_history` entries that do not correspond to real activation changes.

## Context

- Relevant files:
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py`
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\common.py`
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\grid_live.json`
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\activations.json`
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\grid_live_history\grid_live_live_20260420_*.json`
- Current concern:
  - `grid_live_history` shows many snapshots today.
  - `activations.json` `activated_at` values do not align cleanly with first appearance in grid history.
  - The observed archive count appears larger than the number of genuine strategy/product switches expected today.
- Likely failure domains:
  - `_archive_grid_live(mode)` being called on no-op writes
  - reconciliation loops rewriting `grid_live.json` or `activations.json` even when material state did not change
  - duplicate updates from weekly performance, rank alert, freq switch, or sync paths
  - UI/API requests causing repeated save cycles without real content changes

## Destination Folder

None

## Dependency

None

## Plan

- [ ] 1. Identify every code path that archives `grid_live.json` or rewrites `activations.json`/`grid_live.json`.
  - [ ] Test: locate all references to `_archive_grid_live`, grid-live sync, and activation save/update logic.
  - Evidence: mapped write/archive call graph with file references.
- [ ] 2. Quantify today’s `grid_live_history` activity and compare it to actual material state changes.
  - [ ] Test: inspect `grid_live_live_20260420_*.json` snapshots and determine whether adjacent files differ materially.
  - Evidence: count of total snapshots vs count of unique state transitions.
- [ ] 3. Correlate suspicious activation timestamps with the write/archive flow.
  - [ ] Test: compare `activations.json` `activated_at` values against grid history first-seen times and source/update paths.
  - Evidence: documented examples showing where timestamps are preserved vs overwritten.
- [ ] 4. Determine root cause and propose or implement a fix if justified.
  - [ ] Test: show how the identified path can create excessive archive noise and define the guard needed to suppress no-op writes.
  - Evidence: explanation plus diff or concrete remediation proposal.

## Evidence

Objective-Delivery-Coverage: 85%
Auto-Acceptance: false

## Implementation Log

### 2026-04-20 14:12:11

- Created investigation task after observing that `grid_live_history` contained many archive files for today and that current `activations.json` timestamps did not line up cleanly with the expected number or timing of real activation switches.

### 2026-04-20 14:25:00

- Mapped the primary archive/write call sites in `trade_viewer_api.py`.
- Confirmed that `/api/switch_rule/activate` always archives when any existing `freq_switch_rule` entry is present, then removes all prior `freq_switch_rule` rows and writes the replacement entry.
- Confirmed that `/api/grid_live` has a material-change guard, but its signature only considers `(model, product, metric)` and ignores `source`, `group`, and `activated_at`.
- Confirmed that `_sync_grid_to_activations(...)` preserves `activated_at` only if the activation key is still present in the current activation set; if a key disappears and later reappears, a fresh timestamp is generated.

### 2026-04-20 14:31:00

- Quantified today’s live-grid history snapshots by computing an adjacent material signature over `model`, `product`, `metric`, `source`, `group`, and `manual`.
- Result: `49` archive files for `grid_live_live_20260420_*.json`, but only `10` adjacent material states.
- The largest churn run was `34` consecutive archive files with the same effective one-entry live grid state beginning at `20260420_034111`.
- This demonstrates that today’s archive volume is mostly repeated archive-on-write behavior, not a matching count of real state transitions.

### 2026-04-20 14:36:00

- Reconstructed the material transitions visible in archive history:
  - `20260420_032225`: legacy `switch_rule` single-entry state.
  - `20260420_034108`: `freq_switch_rule` moved to `breakout_2_tp10.0_sl20.0 / EURAUD_C`.
  - `20260420_034111`: `freq_switch_rule` moved again to `breakout_2_tp5.0_sl20.0 / EURAUD_C`.
  - `20260420_092109`: TB auto entry added while `freq_switch_rule` remained.
  - `20260420_104640`: TB auto entry removed.
  - `20260420_104751`: weekly-performance `breakout_R_2_tp20.0_sl3.0 / EURAUD_C` added.
  - `20260420_132947`: `rank_alert_ui` `breakout_2_tp10.0_sl50.0 / GBPNZD_C` added.
- The repeated archives between those points do not correspond to distinct material states.

### 2026-04-20 14:40:00

- Correlated current activation timestamps with grid-history evidence:
  - `breakout_2_tp10.0_sl20.0 / EURAUD_C` appears in today’s grid history long before the current `activations.json` timestamp of `2026-04-20T12:27:19.458595`.
  - `breakout_R_2_tp20.0_sl3.0 / EURAUD_C` first appears in grid history at `20260420_132947`, which is later than the current activation timestamp stored in `activations.json`.
- Conclusion: `activations.json["activated_at"]` is not a durable “first activation seen” field. It is a merge-time timestamp that can be preserved, dropped, and regenerated depending on whether the activation key survives reconciliation.

### 2026-04-20 14:45:00

- Inspected the long archive churn run more closely.
- Finding: the repeated `034111` through `080338` history files are not switching between different strategies; they are mostly the same single `freq_switch_rule` entry:
  - `model = breakout_2_tp5.0_sl20.0`
  - `product = EURAUD_C`
  - `source = freq_switch_rule`
  - `group = freq_EURAUD_C_breakout_2_tp5_0_sl20_0`
- What changes across most of those files is `activated_at`, which advances repeatedly:
  - `2026-04-20T03:41:08`
  - `2026-04-20T03:41:11`
  - `2026-04-20T03:41:21`
  - `2026-04-20T03:47:35`
  - `...`
  - `2026-04-20T07:56:55`
- This is consistent with repeated calls to `/api/switch_rule/activate` for the same currently selected strategy/product, because that endpoint always stamps a fresh `activated_at`, archives if any `freq_switch_rule` entry already exists, then rewrites the entry.
- Additional confirmation: a few archive files in that run are exact duplicates, which means some writes are occurring even without a metadata change large enough to alter the archived content.

### 2026-04-20 14:51:00

- Implemented a guard in `trade_viewer_api.py` inside `/api/switch_rule/activate`.
- New behavior:
  - if there is exactly one existing `freq_switch_rule` entry for the mode
  - and its material signature `(model, product, metric, group, source)` matches the incoming request
  - then the endpoint returns early with `message = "No material change"`
  - and skips archive, `grid_live.json` rewrite, and `activations.json` sync
- This specifically blocks timestamp-only rewrites where `activated_at` is the only differing field.

## Changes Made

- Production code updated:
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py`
- Investigation evidence collected from:
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py`
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\activations.json`
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\grid_live_history\grid_live_live_20260420_*.json`

## Validation

- Code-path validation:
  - `trade_viewer_api.py:7157-7168` archives and rewrites on `/api/switch_rule/activate` whenever any `freq_switch_rule` entry already exists.
  - `trade_viewer_api.py:7032-7048` shows the `/api/grid_live` material guard only keys on `(model, product, metric)`.
  - `trade_viewer_api.py:7227-7263` shows `_sync_grid_to_activations(...)` preserving `activated_at` only when the prior activation key still exists; otherwise it assigns `now`.
- Snapshot validation:
  - Computed `49` live-grid archive files for `2026-04-20`.
  - Computed `10` adjacent material states across those same files.
  - Observed one run of `34` consecutive archives with the same effective one-entry grid state.
- Fix validation:
  - Parsed `trade_viewer_api.py` with Python `ast.parse(...)` successfully after the edit.
  - Confirmed the new no-op guard is present at `trade_viewer_api.py:7168-7177`.
  - Expected runtime behavior: repeated activation requests for the same `freq_switch_rule` selection no longer create archive churn when the only change would have been `activated_at`.

## Risks/Notes

- This may reveal multiple independent writers to the same state, so preserve existing behavior carefully during investigation.
- If timestamps are being regenerated on merge/recreate instead of first activation, the issue may affect both observability and workflow correctness.
- Strong root-cause candidate:
  - `freq_switch_rule` writes appear to be generating repeated full-file archives, and history count cannot be treated as “number of true switches”.
- Stronger root-cause hypothesis after timestamp review:
  - repeated `/api/switch_rule/activate` calls for the same selected item are re-stamping `activated_at` and archiving the prior file each time, inflating `grid_live_history` without reflecting real switching.
- Data-model note:
  - `activations.json["activated_at"]` currently behaves more like “current activation record creation time” than a durable first-seen timestamp.

## Completion Status

Complete
