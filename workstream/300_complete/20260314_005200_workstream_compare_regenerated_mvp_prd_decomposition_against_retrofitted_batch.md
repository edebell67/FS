Source: User request to proceed with a comparison between future decompositions and the retrofitted MVP PRD backlog batch after updating the decomposition skills.

Context:
- `C:\Users\edebe\eds\workstream\000_epic\20260305_185316_mvp_prd_quarterly_export_10min.md`
- `C:\Users\edebe\eds\skills\epic-decomposition\SKILL.md`
- `C:\Users\edebe\eds\skills\document-to-task-decomposition\SKILL.md`
- `C:\Users\edebe\eds\workstream\100_backlog\20260314_0340*_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_*.md`

Plan:
- [x] 1. Identify the decomposition entrypoint used by the current workstream flow.
  - [x] Test: Inspect the relevant decomposition command/code path before regenerating tasks.
  - [x] Evidence: Confirmed the active path is `workstream/epic_decompose_cli.py`, invoked by `kanban_dashboard.py` through `decompose_epic()`, and that the CLI inlines the updated skill bodies into its prompt.
- [ ] 2. Regenerate the MVP PRD decomposition into a temporary destination.
  - [x] Test: Produce a fresh decomposition batch without disturbing the live backlog files.
  - [x] Evidence: Ran `python workstream/epic_decompose_cli.py --input workstream/000_epic/20260305_185316_mvp_prd_quarterly_export_10min.md` with elevated permissions; the CLI produced a fresh JSON batch under `workstream/artefacts/epic_decomp_20260314_052225_355873`.
- [ ] 3. Compare the regenerated batch with the retrofitted backlog batch and summarize whether the generator now reflects the updated rules.
  - [x] Test: Check for title encoding, dependency clarity, and verification deduplication deltas.
  - [x] Evidence: The regenerated batch contains `23` tasks versus `22` in the retrofitted backlog batch, uses the correct UTF-8 epic title, produces a concrete A1 output artifact description, and assigns exactly `5` deduplicated verification bullets to each UI-visible task (`G1`-`G4`) instead of the older repeated boilerplate pattern.

Chronology:
- 2026-03-14 00:52 Europe/London: Traced the active decomposition path to `workstream/epic_decompose_cli.py` and confirmed it embeds the skill text directly into the prompt.
- 2026-03-14 05:22 Europe/London: Ran the real decomposition CLI against the MVP PRD source epic and captured the generated payload under `workstream/artefacts/epic_decomp_20260314_052225_355873`.
- 2026-03-14 05:25 Europe/London: Compared the regenerated payload with the retrofitted backlog batch and confirmed the generator now reflects the updated skill rules for UTF-8 fidelity, concrete foundation outputs, and deduplicated UI verification.
