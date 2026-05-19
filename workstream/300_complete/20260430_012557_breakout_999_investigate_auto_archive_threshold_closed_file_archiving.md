# Investigate Auto Archive Threshold Closed File Archiving

Source: Direct user request on 2026-04-30 to investigate whether the function referencing Auto Archive Threshold still archives closed files when the specified quantity is exceeded.

Task Type: standard

Task Attributes:
- recurring_task: false
- looping_task: false
- splittable_task: false
- workflow_task: false

Task Summary: Investigate whether `auto_archive_threshold` still triggers auto-archiving of closed trade files when the closed-file count exceeds the configured threshold.

Context:
- `C:\Users\edebe\eds\TradeApps\breakout\fs\config.json`
- `C:\Users\edebe\eds\TradeApps\breakout\fs\archive_cld.py`
- `C:\Users\edebe\eds\TradeApps\breakout\fs\common.py`
- `C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer.html`
- `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\forex\<date>`

Initial Triage:
- `trade_viewer.html` exposes `Auto Archive Threshold` as config key `auto_archive_threshold`.
- `archive_cld.py` reads `auto_archive_threshold` and calls `_perform_cld_auto_archive(cfg)`.
- `common.py` defines `_perform_cld_auto_archive(config)` and runtime loop references it.
- Current `config.json` contains `auto_archive_threshold: 1000`.
- Prior related completed tasks exist for applying auto-archive, preserving `_summary_net`, product-type layout, and restoring summary after archive.

Destination Folder: `C:\Users\edebe\eds\workstream\verification\auto_archive_threshold_20260430`

Dependency: None

Plan:
- [x] 1. Map the exact auto-archive execution path.
  - Test: [x] Review `archive_cld.py`, `common.py`, and runtime loop calls; expected pass condition is a documented call chain from config threshold to file move.
  - Evidence: `trade_viewer.html` exposes `auto_archive_threshold`; `archive_cld.py` loads config and calls `_perform_cld_auto_archive(cfg)`; `common.run_multiwindow` also calls `_perform_cld_auto_archive(config)` during runtime.
- [x] 2. Verify the closed-file suffix/type being counted.
  - Test: [x] Inspect `_perform_cld_auto_archive` to confirm whether it archives `*_cl.json`, `*_cld.json`, or both; expected pass condition is documenting the actual suffix behavior against the user expectation of closed files.
  - Evidence: `_perform_cld_auto_archive` uses `source_date_dir.glob('*_cld.json')`; it does not count or move raw `*_cl.json`. `summary_net_generator.py` processes `*_cl.json` and renames them to `*_cld.json`.
- [x] 3. Run a safe isolated threshold simulation.
  - Test: [x] Execute `_perform_cld_auto_archive` against a temporary copied day folder or monkeypatched resolver with threshold below test file count; expected pass condition is files move only when count exceeds threshold and no live production files are modified.
  - Evidence: Synthetic folder with 3 `*_cld.json`, 2 `*_cl.json`, threshold 2 returned `archived_return: true`; moved 3 `*_cld.json`; left 2 `*_cl.json` in place; preserved `_summary_net_pre_auto_archive.json`.
- [x] 4. Validate production wiring without changing live data.
  - Test: [x] Confirm `archive_cld.py --once` or runtime loop can reach the function with current config; expected pass condition is log/output proving no code path breakage.
  - Evidence: Stubbed `archive_cld.main(run_once=True)` called `_perform_cld_auto_archive` exactly once with `{'run_mode': 'live', 'auto_archive_threshold': 123}`.
- [x] 5. Document findings and recommended fix if behavior is broken or mismatched.
  - Test: [x] Record whether the feature works as designed, partially works, or needs a `_998_` fix follow-up; expected pass condition is an explicit go/no-go conclusion.
  - Evidence: Conclusion recorded: auto-archive still works for processed closed `*_cld.json` files; it does not directly archive raw `*_cl.json` files. No fix is required if "closed files" means processed closed files. A `_998_` follow-up is required only if raw `*_cl.json` files should be included directly.

Evidence:
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true
- Evidence-Type: test_output
  - Artifact: Isolated Python harness using `C:\Users\edebe\eds\workstream\verification\auto_archive_threshold_20260430`
  - Objective-Proved: Auto-archive threshold moves processed closed `*_cld.json` files when count exceeds threshold.
  - Status: captured
- Evidence-Type: log_output
  - Artifact: Stubbed `archive_cld.main(run_once=True)` output
  - Objective-Proved: Watcher entrypoint invokes `_perform_cld_auto_archive` with loaded config.
  - Status: captured
- Evidence-Type: manual_verification
  - Artifact: Code inspection of `common.py`, `archive_cld.py`, and `summary_net_generator.py`
  - Objective-Proved: Exact suffix behavior and call chain.
  - Status: captured

Implementation Log:
- 2026-04-30 01:25: Created investigation task from user request.
- 2026-04-30 01:26: Moved task to in-progress and inspected `archive_cld.py`, `common._perform_cld_auto_archive`, runtime loop call, and `summary_net_generator.py` closure processing.
- 2026-04-30 01:28: Ran isolated monkeypatched test folder with 3 processed closed files and 2 raw closed files.
- 2026-04-30 01:28: Validated watcher entrypoint with `_perform_cld_auto_archive` stubbed to avoid production file moves.
- 2026-04-30 01:28: Checked today production live forex folder counts: `cld=0`, `cl=0`, threshold `1000`.

Changes Made:
- None. This is an investigation task only.

Validation:
- `rg -n "auto_archive_threshold|_perform_cld_auto_archive|archive_cld"`: PASS. Located config UI, watcher entrypoint, runtime call, and threshold function.
- Isolated Python harness: PASS. With threshold `2` and 3 `*_cld.json`, `_perform_cld_auto_archive` returned `true`, moved all 3 `*_cld.json` into `archive/<HHMMSS>/`, and preserved summary copies. It did not move 2 raw `*_cl.json`.
- Stubbed watcher test: PASS. `archive_cld.main(run_once=True)` called `_perform_cld_auto_archive` once using loaded config.
- Production non-mutating count check: PASS. `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\forex\2026-04-30` has `cld=0`, `cl=0`, threshold `1000`.

Risks/Notes:
- The implementation appears to target `*_cld.json` files, not necessarily raw `*_cl.json` files. The investigation must confirm whether that matches the intended meaning of "closed files".
- Validation must avoid moving production trade files unless explicitly approved.
- Confirmed behavior: raw `*_cl.json` files are not directly archived by the threshold function. They are expected to be consumed by `summary_net_generator.py`, renamed to `*_cld.json`, and then archived by the threshold function.
- No production files were moved during this investigation.

Completion Status: complete - 2026-04-30 01:29
