Source: User request in Codex thread on 2026-04-13 to investigate the impact of `Auto Archive Threshold` in breakout FS config.
Task Type: standard
Task Attributes:
  recurring_task: false
  looping_task: false
  splittable_task: false
  workflow_task: false
  depends_on: []
  feeds_into: []
Task Summary: Trace where `auto_archive_threshold` is consumed, determine what data it moves or suppresses, and assess the current runtime impact against today's file counts.
Context: `C:\Users\edebe\eds\TradeApps\breakout\fs\config.json`, `archive_cld.py`, `common.py`, `trade_viewer_api.py`, `summary_net_generator.py`.
Destination Folder: None
Dependency: None
Plan:
- [x] 1. Locate the config key and all runtime call sites.
  - [x] Test: Search the FS codebase for `auto_archive_threshold` and inspect the referenced files.
  - [x] Evidence: `rg` hits captured for `archive_cld.py`, `common.py`, `config.json`, `trade_viewer.html`, and SQL/UI references.
- [x] 2. Determine what the threshold changes in behavior and whether archived data remains accessible.
  - [x] Test: Read the archiving function and archive-aware API/summary code paths.
  - [x] Evidence: `common.py` and `trade_viewer_api.py` excerpts captured showing top-level `*_cld.json` moves and recursive archive reads for closed trades.
- [x] 3. Compare today's active file counts to the configured threshold to assess present impact.
  - [x] Test: Count top-level `*_cld.json` files in current live day directories and compare to configured threshold.
  - [x] Evidence: PowerShell count output captured for `2026-04-13` day dirs showing `forex=2804`, `energy=2079`, `indices=994`, `crypto=160`, `metals=486`.

## Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true
- Evidence-Type: test_output
  - Artifact: `rg -n "auto_archive_threshold|_perform_cld_auto_archive|archive_cld.py"` output captured in Codex tool history
  - Objective-Proved: The config key is live and wired into FS runtime code.
  - Status: captured
- Evidence-Type: test_output
  - Artifact: Numbered excerpts from `common.py`, `archive_cld.py`, `trade_viewer_api.py`, and `summary_net_generator.py`
  - Objective-Proved: The threshold archives top-level closed-trade files, preserves `_summary_net` snapshots, and keeps archive-aware retrieval paths.
  - Status: captured
- Evidence-Type: manual_verification
  - Artifact: Codex final response in this thread
  - Objective-Proved: The user receives a direct impact assessment grounded in current counts and code behavior.
  - Status: captured

## Implementation Log
- 2026-04-13 12:08:32: Created lifecycle file for auto-archive-threshold investigation.
- 2026-04-13 12:08:45: Confirmed config value in `fs/config.json` is `2000`.
- 2026-04-13 12:09:10: Read `archive_cld.py` and `_perform_cld_auto_archive` in `common.py`.
- 2026-04-13 12:09:40: Verified archive-aware retrieval in `trade_viewer_api.py` and preserved-summary restore in `summary_net_generator.py`.
- 2026-04-13 12:10:10: Counted current top-level `*_cld.json` files for active live day folders.

## Changes Made
- No code changes.
- Added this lifecycle file to document the investigation.

## Validation
- `Select-String -Path 'C:\Users\edebe\eds\TradeApps\breakout\fs\config.json' -Pattern 'auto_archive_threshold' -Context 2,2`
  - Result: Pass. Current configured value confirmed as `2000`.
- `rg -n "auto_archive_threshold|_perform_cld_auto_archive|archive_cld.py" 'C:\Users\edebe\eds\TradeApps\breakout\fs'`
  - Result: Pass. Located all relevant runtime references.
- PowerShell day-dir count script for `2026-04-13`
  - Result: Pass. Current counts captured and compared to threshold.

## Risks/Notes
- `archive_cld.py` exists as a standalone watcher, but the threshold also runs inline from `common.py`, so the setting can take effect even if the standalone watcher is not supervised.
- The threshold does not itself recalculate summaries; it preserves `_summary_net.json` and relies on summary restore logic where needed.

## Completion Status
- Complete as of 2026-04-13 12:10:10.
