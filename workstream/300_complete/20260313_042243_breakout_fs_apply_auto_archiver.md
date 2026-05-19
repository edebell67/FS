Source: Direct user request in this session.

Task Summary: Apply the `.cld` auto-archiver functionality to the FS Breakout runtime so `auto_archive_threshold` is actually used by the FS code path.

Context:
- `C:\Users\edebe\eds\TradeApps\breakout\fs\config.json`
- `C:\Users\edebe\eds\TradeApps\breakout\fs\common.py`
- `C:\Users\edebe\eds\TradeApps\breakout\fs\run_archive_process.py`
- `C:\Users\edebe\eds\TradeApps\breakout\DB\archive_cld.py`
- `C:\Users\edebe\eds\TradeApps\breakout\DB\common.py`

Plan:
- [x] 1. Compare the existing DB auto-archiver implementation against the FS archive/runtime entry points and choose the FS integration point.
  - [x] Test: Review `DB/archive_cld.py`, `DB/common.py`, `fs/common.py`, and `fs/run_archive_process.py`; pass if the FS invocation path and required parity behavior are identified.
  - [x] Evidence: Confirmed the DB path uses `archive_cld.py -> _perform_cld_archive`, while the FS path lacked a `.cld` threshold consumer. Chosen FS integration points were `fs/common.py` for the reusable implementation and the normal `run_multiwindow` loop for continuous runtime invocation.
- [x] 2. Implement FS-side `.cld` auto-archive behavior using `auto_archive_threshold`.
  - [x] Test: Add FS runtime logic that counts `*_cld.json` files under `json/<run_mode>/<date>` and archives them when the count exceeds the threshold.
  - [x] Evidence: Added `_perform_cld_auto_archive(config)` to `fs/common.py`, wired it into the FS main runtime loop, and added a standalone FS watcher script `fs/archive_cld.py`.
- [ ] 3. Validate the FS implementation with targeted syntax/runtime checks.
  - [x] Test: Run Python syntax checks and at least one focused functional verification of the archive trigger path; pass if the FS path reads the threshold and performs/archive-skips correctly.
  - [x] Evidence: Repo-local fixture under `workstream\verification\fs_auto_archive_fixture` triggered `.cld` auto-archive at threshold `2`, created preservation copies, moved 3 `.cld` files into `archive/<HHMMSS>/`, and preserved summary history through `SummaryGenerator.process_date()`.

Implementation Log:
- 2026-03-13 04:22 Europe/London: Created this task to capture the requested FS auto-archiver change.
- 2026-03-13 04:23 Europe/London: Compared the DB `.cld` auto-archiver against the FS runtime and confirmed the FS path had the config key but no active runtime consumer.
- 2026-03-13 04:24 Europe/London: Reviewed the FS archive flow in `fs/common.py` and the existing helper script `fs/run_archive_process.py` to avoid colliding with manual `archive=true` behavior.
- 2026-03-13 04:25 Europe/London: Implemented `_perform_cld_auto_archive(config)` in `fs/common.py` to archive top-level `*_cld.json` files when their count exceeds `auto_archive_threshold`.
- 2026-03-13 04:25 Europe/London: Wired `_perform_cld_auto_archive(config)` into the FS `run_multiwindow` loop so the threshold is checked during normal FS runtime.
- 2026-03-13 04:26 Europe/London: Added `fs/archive_cld.py` as a standalone watcher script mirroring the DB-side tooling pattern.
- 2026-03-13 04:33 Europe/London: Added `_summary_net.json` preservation copies before `.cld` auto-archive moves; this follow-up requirement is also tracked separately in `20260313_042937_breakout_fs_preserve_summary_net_history_pre_autoarchive.md`.
- 2026-03-13 04:34 Europe/London: Ran syntax validation and attempted an isolated functional verification; syntax passed, but the first temp-fixture run failed due to a temporary-file permission error in the test harness.
- 2026-03-13 10:48 Europe/London: Added generator restoration from the preserved summary snapshot and common summary-reader fallback to support the preservation requirement.
- 2026-03-13 10:48 Europe/London: Re-ran functional verification using a repo-local fixture under `workstream\verification\fs_auto_archive_fixture`; the FS auto-archive path triggered successfully and retained historical summary data.

Changes Made:
- Updated `TradeApps\breakout\fs\common.py`:
  - Added `_perform_cld_auto_archive(config)`.
  - Reads `auto_archive_threshold` from FS config.
  - Counts top-level `*_cld.json` files in `json/<run_mode>/<date>`.
  - Moves those files into `archive/<HHMMSS>/` when the threshold is exceeded.
  - Preserves `_summary_net.json` before `.cld` moves.
  - Invokes the auto-archive function from the normal FS runtime loop.
- Updated `TradeApps\breakout\fs\summary_net_generator.py`:
  - Restores prior closed summary history from `_summary_net_pre_auto_archive.json` when no top-level `.cld` files remain after auto-archive.
- Updated `TradeApps\breakout\fs\common.py` summary loading:
  - Falls back to `_summary_net_pre_auto_archive.json` when `_summary_net.json` is unavailable.
- Added `TradeApps\breakout\fs\archive_cld.py`:
  - Standalone FS watcher that polls config and runs `_perform_cld_auto_archive`.

Validation:
- `python -m py_compile C:\Users\edebe\eds\TradeApps\breakout\fs\common.py C:\Users\edebe\eds\TradeApps\breakout\fs\archive_cld.py`
  - Result: Passed with no output.
- `rg -n "def _perform_cld_auto_archive|_summary_net_pre_auto_archive|_perform_cld_auto_archive\(config\)|archive_cld.py|auto_archive_threshold" C:\Users\edebe\eds\TradeApps\breakout\fs\common.py C:\Users\edebe\eds\TradeApps\breakout\fs\archive_cld.py C:\Users\edebe\eds\TradeApps\breakout\fs\config.json`
  - Result: Confirmed config, implementation, preservation-copy logic, runtime invocation, and standalone watcher references.
- Focused functional verification attempt:
  - Command/Check: Temporary isolated FS fixture using Python to load `fs/common.py`, create a synthetic `json/live/<date>` folder, and invoke `_perform_cld_auto_archive`.
  - Result: First attempt failed because the temporary config fixture write hit a `PermissionError`.
- Repo-local fixture verification:
  - Command/Check: Inline Python fixture under `workstream\verification\fs_auto_archive_fixture` importing `fs/common.py` and `fs/summary_net_generator.py`, triggering `_perform_cld_auto_archive`, then running `SummaryGenerator.process_date()`.
  - Result: Passed with `fs_summary_preservation_test=ok`.

Risks/Notes:
- The FS path now has an active runtime consumer for `auto_archive_threshold`; the DB path is no longer the only implementation.
- The existing manual FS day-folder archive flow (`archive=true`) still exists and is separate from the new `.cld` threshold archiver.
- `_summary_net.json` preservation is implemented as a safeguard, but reader behavior against the preserved copy still needs dedicated verification.
- Related follow-up task: `C:\Users\edebe\eds\workstream\200_inprogress\20260313_042937_breakout_fs_preserve_summary_net_history_pre_autoarchive.md`

Completion Status:
- Complete - 2026-03-13 10:48 Europe/London
