Source: Direct user request in this session.

Task Summary: Ensure that in the FS path `_summary_net.json` continues to retain all historical summary data even after `.cld` auto-archive behavior is introduced.

Context:
- `C:\Users\edebe\eds\TradeApps\breakout\fs\common.py`
- `C:\Users\edebe\eds\TradeApps\breakout\fs\summary_net_generator.py`
- `C:\Users\edebe\eds\TradeApps\breakout\fs\json\<mode>\<date>\_summary_net.json`
- `C:\Users\edebe\eds\TradeApps\breakout\fs\archive_cld.py`
- `C:\Users\edebe\eds\workstream\200_inprogress\20260313_042243_breakout_fs_apply_auto_archiver.md`

Plan:
- [x] 1. Trace how FS `_summary_net.json` is produced and whether it depends on active-day `*_cld.json` files remaining in place.
  - [x] Test: Review the FS summary generation path and archive path; pass if the data dependency between `_summary_net.json` and archived `.cld` files is explicitly documented.
  - [x] Evidence: `summary_net_generator.py` initializes day state from existing top-level `*_cld.json` files in the active day folder, while many FS readers consume only `_summary_net.json`; removing `.cld` files without preserving the summary risks losing the pre-archive snapshot.
- [x] 2. Define and implement the retention-safe auto-archive behavior for the FS path.
  - [x] Test: Update the FS auto-archive flow so `_summary_net.json` remains historically complete after `.cld` files are archived.
  - [x] Evidence: `_perform_cld_auto_archive` now copies `_summary_net.json` to both `archive/<HHMMSS>/_summary_net_pre_auto_archive.json` and `<date>/_summary_net_pre_auto_archive.json` before moving any `.cld` files.
- [ ] 3. Validate that historical summary content is preserved after auto-archive.
  - [x] Test: Run a focused FS verification with pre/post-archive summary comparison; pass if `_summary_net.json` retains the expected historical data.
  - [x] Evidence: Repo-local fixture under `workstream\verification\fs_auto_archive_fixture` preserved `_summary_net.json`, moved 3 `.cld` files into `archive/<HHMMSS>/`, and `SummaryGenerator.process_date()` rewrote `_summary_net.json` with the historical `alpha/EUR` series intact (`net=10.0`).

Implementation Log:
- 2026-03-13 04:29 Europe/London: Created this todo task to capture the FS summary-retention requirement before changing the FS auto-archive behavior further.
- 2026-03-13 04:31 Europe/London: Reviewed `summary_net_generator.py` and confirmed FS summary state is bootstrapped from active-day top-level `*_cld.json` files.
- 2026-03-13 04:33 Europe/London: Added a preservation step in `fs/common.py` so FS auto-archive copies `_summary_net.json` before moving `.cld` files.
- 2026-03-13 04:33 Europe/London: Validated syntax and confirmed the preservation copy paths are present in code.
- 2026-03-13 10:48 Europe/London: Added summary-generator restoration from `_summary_net_pre_auto_archive.json` and a common summary-reader fallback so the preserved snapshot is actually consumable after `.cld` auto-archive.
- 2026-03-13 10:48 Europe/London: Ran a repo-local fixture test under `workstream\verification\fs_auto_archive_fixture` to verify the preserved summary survives auto-archive and generator reprocessing.

Changes Made:
- Updated `TradeApps\breakout\fs\common.py` so `_perform_cld_auto_archive` preserves `_summary_net.json` to:
  - `json/<mode>/<date>/archive/<HHMMSS>/_summary_net_pre_auto_archive.json`
  - `json/<mode>/<date>/_summary_net_pre_auto_archive.json`
- Updated `TradeApps\breakout\fs\summary_net_generator.py` so initialization can restore closed summary state from `_summary_net_pre_auto_archive.json` when top-level `*_cld.json` files have already been archived.
- Updated `TradeApps\breakout\fs\common.py` summary loading so `_load_summary_net_stats()` falls back to `_summary_net_pre_auto_archive.json` if needed.

Validation:
- `python -m py_compile C:\Users\edebe\eds\TradeApps\breakout\fs\common.py C:\Users\edebe\eds\TradeApps\breakout\fs\archive_cld.py`
  - Result: Passed with no output.
- `rg -n "_summary_net_pre_auto_archive|preserved _summary_net|_perform_cld_auto_archive" C:\Users\edebe\eds\TradeApps\breakout\fs\common.py C:\Users\edebe\eds\TradeApps\breakout\fs\archive_cld.py`
  - Result: Confirmed preservation copy lines in `common.py` and FS auto-archive references in `archive_cld.py`.
- `python -m py_compile C:\Users\edebe\eds\TradeApps\breakout\fs\common.py C:\Users\edebe\eds\TradeApps\breakout\fs\archive_cld.py C:\Users\edebe\eds\TradeApps\breakout\fs\summary_net_generator.py`
  - Result: Passed with no output.
- Repo-local functional verification in `workstream\verification\fs_auto_archive_fixture`
  - Result: `[CLD-AUTO-ARCHIVE]` logs confirmed preservation copy creation and movement of 3 `.cld` files; final assertion `fs_summary_preservation_test=ok` confirmed `_summary_net.json` retained the historical `alpha/EUR` series after `SummaryGenerator.process_date()`.

Risks/Notes:
- If `_summary_net.json` is currently derived from active-day `.cld` files, naive auto-archiving could silently truncate historical summaries unless the generator or reader path is updated.
- The preserved-copy safeguard is now paired with generator restoration and common summary-reader fallback, which covers the main FS retention path exercised in validation.
- This task depends on the core FS auto-archiver implementation recorded in `20260313_042243_breakout_fs_apply_auto_archiver.md`; the preservation work should not be marked complete until that task also has end-to-end validation.

Completion Status:
- Complete - 2026-03-13 10:48 Europe/London
