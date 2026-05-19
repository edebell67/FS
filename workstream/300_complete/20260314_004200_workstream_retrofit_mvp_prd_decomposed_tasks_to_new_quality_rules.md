Source: User request to apply the updated decomposition-quality rules retroactively to the generated MVP PRD backlog task set.

Context:
- `C:\Users\edebe\eds\workstream\100_backlog\20260314_0340*_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_*.md`
- `C:\Users\edebe\eds\skills\epic-decomposition\SKILL.md`
- `C:\Users\edebe\eds\skills\document-to-task-decomposition\SKILL.md`

Plan:
- [x] 1. Audit the generated MVP PRD task batch for the known quality defects.
  - [x] Test: Scan the batch for mojibake, missing foundation-task clarity, and duplicated UI verification bullets.
  - [x] Evidence: Confirmed corrupted epic title metadata across the batch, duplicated UI verification bullets across the `E` tasks, and missing foundation-task dependency clarity in task `A1`.
- [x] 2. Apply focused retrofits to the affected task files.
  - [x] Test: Update the task batch to preserve UTF-8 epic titles, normalize duplicated UI verification bullets, and strengthen `A1` output/dependency metadata.
  - [x] Evidence: Updated all matching backlog tasks to use the correct epic title, normalized verification sections for `E1`-`E4`, corrected the quarter-screen headline punctuation, and added explicit foundation-task dependency metadata plus concrete output wording to `A1`.
- [x] 3. Validate the retrofitted batch.
  - [x] Test: Confirm the batch no longer contains mojibake and that the affected tasks reflect the intended normalization.
  - [x] Evidence: `rg -n "�"` returned clean for the batch, and readback checks confirmed the normalized `A1`, `E1`, and `E4` task content.

Chronology:
- 2026-03-14 00:42 Europe/London: Audited the generated MVP PRD task set and identified the same metadata and verification issues already seen in spot reviews.
- 2026-03-14 00:47 Europe/London: Applied a batch metadata correction for the epic title across the full task set.
- 2026-03-14 00:49 Europe/London: Strengthened `A1` with explicit foundation-task dependency guidance and more concrete output wording.
- 2026-03-14 00:52 Europe/London: Deduplicated the UI verification sections for `E1`-`E4` and corrected the remaining quarter-screen mojibake in the acceptance text.
- 2026-03-14 00:54 Europe/London: Validated the retrofitted task set with targeted scans and file readback.
