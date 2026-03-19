Source: User request to update the decomposition skill so recently identified task-generation gaps are prevented.

Context:
- `C:\Users\edebe\eds\skills\epic-decomposition\SKILL.md`
- `C:\Users\edebe\eds\skills\document-to-task-decomposition\SKILL.md`

Plan:
- [x] 1. Inspect the current decomposition skills against the identified task-quality gaps.
  - [x] Test: Review skill instructions and compare them to recent review findings.
  - [x] Evidence: Confirmed the current skills do not explicitly guard against missing blocker metadata on foundational tasks, vague output artifacts, duplicate verification bullets after UI expansion, or mojibake in copied epic metadata.
- [ ] 2. Update the relevant skill instructions to harden future task generation quality.
  - [x] Test: Skill guidance should explicitly require dependency clarity, concrete deliverable artifacts, deduplicated verification bullets, and UTF-8-safe metadata preservation.
  - [x] Evidence: Updated `skills/epic-decomposition/SKILL.md` and `skills/document-to-task-decomposition/SKILL.md` with new rules covering downstream blocker metadata for foundational tasks, artifact-shaped outputs, verification deduplication, and UTF-8 fidelity.
- [ ] 3. Validate the updated skill text and summarize the effective new rules.
  - [x] Test: Read back the modified sections and confirm the new requirements are present.
  - [x] Evidence: `rg` confirmed the new rule anchors (`UTF-8`, `Foundation tasks`, `Deduplicate verification`, `concrete artifacts`, `mojibake`) in both skill files.

Chronology:
- 2026-03-14 00:30 Europe/London: Reviewed the current decomposition skills and mapped them to the previously identified task-quality defects.
- 2026-03-14 00:33 Europe/London: Updated `skills/epic-decomposition/SKILL.md` with stronger rules for downstream blocker metadata, concrete outputs, verification deduplication, and UTF-8-safe metadata preservation.
- 2026-03-14 00:35 Europe/London: Updated `skills/document-to-task-decomposition/SKILL.md` so broader decomposition guidance also enforces concrete outputs, explicit sequencing, deduplicated verification, and UTF-8-safe metadata copying.
- 2026-03-14 00:36 Europe/London: Validated the updated skill text with targeted `rg` checks against the new rule phrases.
