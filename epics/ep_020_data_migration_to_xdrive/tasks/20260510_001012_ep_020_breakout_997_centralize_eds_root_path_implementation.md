## Task

- Implement a shared path-definition module for `TradeApps/breakout/fs`
- Replace live hardcoded `C:\Users\edebe\eds` references with shared imports
- Preserve source/config/script reads on `C:\Users\edebe\eds`
- Allow generated data paths to move to `X:\eds` via a separate generated-data root

## Task Type

- implementation

## Project

- breakout

## Destination Folder

- `workstream/200_inprogress/general`

## Dependency

- Prior analysis: `20260509_193742_breakout_999_centralize_eds_root_path_references.md`
- Target subtree: `C:\Users\edebe\eds\TradeApps\breakout\fs`

## Plan

1. Define a shared `paths.py` API with separate source-root and generated-data-root definitions.
2. Refactor live Python and batch entrypoints to consume the shared paths.
3. Leave backups, docs, session files, and historical artifacts untouched.
4. Validate with search reduction and targeted syntax checks.

## Evidence

- Implementation task opened after completing the analysis pass.
- Added [paths.py](<C:/Users/edebe/eds/TradeApps/breakout/fs/paths.py>) with:
- `EDS_ROOT` for source/repo paths
- `DATA_EDS_ROOT` for generated-data paths
- `BREAKOUT_FS_ROOT` for source `fs`
- `BREAKOUT_DATA_FS_ROOT` and `BREAKOUT_JSON_ROOT` for writable generated artifacts
- `TRADES_RT3_*` derived from the generated-data root
- Refactored live top-level scripts, nested tools, and batch launchers to remove hardcoded `C:\Users\edebe\eds` references from the active scope.
- Generated-data outputs now route through `DATA_EDS_ROOT`, while config and script paths remain on the source tree.
- Remaining hardcoded hits are scoped to intentionally historical files:
- `trade_viewer_api_backup.py`
- `trade_viewer_api.py.20251229_2150`

## Validation

- `rg -n --fixed-strings "C:\Users\edebe\eds" -g '!backup/**' -g '!docs/**' -g '!twitter_session/**' -g '!data_analysis/**' -g '!grid_live_history/**' -g '!json/**' -g '!*.txt' -g '!*.md' .`
- Result: only `trade_viewer_api_backup.py` and `trade_viewer_api.py.20251229_2150` remain, both historical backup files outside the active refactor scope.
- `python -m py_compile ...` on all modified Python files
- Result: passed

## Completion Status

- Complete
