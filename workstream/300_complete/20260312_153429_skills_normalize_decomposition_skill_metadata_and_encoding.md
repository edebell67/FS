Source:
- User request on 2026-03-12 to normalize older decomposition skill metadata so the skills validate cleanly.

Task Summary:
- Fix decomposition skill metadata and file encoding issues preventing validator execution, then re-run validation.

Context:
- Targets: `skills/epic-decomposition/SKILL.md` and `skills/document-to-task-decomposition/SKILL.md`.
- Current validator failure is a decode error before metadata checks.
- The new ordering behavior added to `skills/epic-decomposition/SKILL.md` must be preserved.

Plan:
- [x] 1. Move this lifecycle file to in-progress and inspect the current validator blocker in both skill files.
  - [x] Test: Confirm the lifecycle file exists in `workstream/200_inprogress` and identify the encoding/metadata issues in both target files.
  - Evidence: Lifecycle file moved to `workstream/200_inprogress/20260312_153429_skills_normalize_decomposition_skill_metadata_and_encoding.md`; validator initially failed on both skills with `UnicodeDecodeError`; `skills/epic-decomposition/SKILL.md` also used invalid frontmatter name `Epic Decomposition`.
- [x] 2. Rewrite the target skill files with clean validator-compatible encoding and normalized frontmatter names/descriptions.
  - [x] Test: Re-open both files and confirm the intended content is preserved with lowercase hyphen-case `name` values.
  - Evidence: Rewrote both `SKILL.md` files in clean ASCII content; `skills/epic-decomposition/SKILL.md` now uses `name: epic-decomposition`; `skills/document-to-task-decomposition/SKILL.md` preserved behavior with normalized validator-safe content.
- [x] 3. Run `quick_validate.py` against both skills and archive the lifecycle record.
  - [x] Test: Execute validator for both skill folders and confirm successful output.
  - Evidence: `quick_validate.py` returned `Skill is valid!` for both target folders.

Implementation Log:
- 2026-03-12 15:34:29: Task file created in `workstream/100_todo`.
- 2026-03-12 15:34:40: Task file moved to `workstream/200_inprogress`.
- 2026-03-12 15:35:20: Ran validator on both decomposition skills and confirmed decode failures blocked validation.
- 2026-03-12 15:38:00: Rewrote both `SKILL.md` files with clean validator-compatible content and preserved the earlier epic ordering guidance.
- 2026-03-12 15:39:00: Re-ran validation; both skills passed.

Changes Made:
- Updated `skills/document-to-task-decomposition/SKILL.md`.
- Updated `skills/epic-decomposition/SKILL.md`.

Validation:
- `python C:\Users\edebe\.codex\skills\.system\skill-creator\scripts\quick_validate.py skills\epic-decomposition`
  - Result: `Skill is valid!`
- `python C:\Users\edebe\.codex\skills\.system\skill-creator\scripts\quick_validate.py skills\document-to-task-decomposition`
  - Result: `Skill is valid!`

Risks/Notes:
- Rewriting the files must avoid losing any ordering rules or decomposition guidance added earlier today.
- Rewrites were limited to skill documentation content; no runtime scripts or controller code changed.

Completion Status:
- Complete on 2026-03-12 15:39:00.
