Source: User request to generate a test to validate the FS JSON layout change.

Context:
- `C:\Users\edebe\eds\TradeApps\breakout\fs`

Goal:
- Add a focused regression test that validates support for `json/{run_mode}/{product_type}/{date}` and protects against regressions while legacy `json/{run_mode}/{date}` data may still exist.

Plan:
- [ ] 1. Inspect the existing FS test setup and identify the best target function/path for validation.
  - [x] Test: Review current tests and path resolution code before editing.
  - [x] Evidence: Confirmed there was no existing FS JSON layout regression test; the best low-risk validation target is a standalone day-directory resolver contract rather than the full Flask runtime.
- [ ] 2. Add a targeted test covering product-type-aware JSON directory resolution with legacy fallback expectations.
  - [x] Test: New test file created and wired to an existing executable test runner.
  - [x] Evidence: Added `TradeApps/breakout/fs/json_layout.py` with `resolve_day_dir()` and `normalize_product_type()`, plus `tests/test_breakout_fs_json_layout.py` covering product-type preference, legacy fallback, and normalization behavior.
- [ ] 3. Run the targeted test and record the result.
  - [x] Test: Execute the new test successfully.
  - [x] Evidence: `pytest C:\Users\edebe\eds\tests\test_breakout_fs_json_layout.py` passed with `4 passed in 0.03s`.

Chronology:
- 2026-03-14 01:23 Europe/London: Reviewed current tests and FS path assumptions; selected a standalone JSON layout resolver as the lowest-risk validation seam.
- 2026-03-14 01:27 Europe/London: Added `json_layout.py` and a new targeted pytest file to validate product-type-aware path resolution with legacy fallback.
- 2026-03-14 01:29 Europe/London: Fixed import-path and temp-directory issues in the new test so it runs cleanly in this repository and environment.
- 2026-03-14 01:30 Europe/London: Ran the targeted pytest successfully.
