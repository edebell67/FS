Source: `workstream/200_inprogress/codex/20260328_201416_ep_006_website_rebuilds_se_london_legacy_hairdressers.md`
Task Summary: Use the current JSON output from the SE London legacy hairdresser/barber discovery task to create redesigned landing pages for each listed site, following the same `redesign-existing-projects` skill used for the Fun Cuts rebuild, and save the outputs under `ep_006_website_rebuilds/redesigns`.
Context:
- Input JSON: `ep_006_website_rebuilds/se_london_hairdressers_legacy.json`
- Reference rebuild pattern: Fun Cuts homepage redesign task from `2026-03-27`
- Required skill: `C:\Users\edebe\eds\.agents\skills\redesign-existing-projects\SKILL.md`
- Output root: `ep_006_website_rebuilds/redesigns`
- Expected input count at task creation: 10 qualified legacy sites from the JSON `sites` array
Dependency: None

Plan:
- [ ] 1. Read the legacy-site JSON and define the redesign batch scope for every listed business.
  - Test: Load `ep_006_website_rebuilds/se_london_hairdressers_legacy.json` and confirm the site list and output naming plan for all entries.
  - Evidence: JSON summary recorded in the task log with the count of sites and the planned output subpaths.
- [ ] 2. Reuse the `redesign-existing-projects` skill and the Fun Cuts redesign pattern to generate a redesigned landing page deliverable for each listed site.
  - Test: For each JSON entry, create a dedicated redesign artifact set in `ep_006_website_rebuilds/redesigns/<slug>/` containing at minimum a homepage HTML deliverable and its companion CSS/assets as needed.
  - Evidence: File list for each completed redesign folder and note of the source site URL used.
- [ ] 3. Validate the redesign batch output and produce an index file for review.
  - Test: Generate a review index in `ep_006_website_rebuilds/redesigns/` that links each business name to its redesign entry file and source URL.
  - Evidence: Review index path plus a validation summary confirming all expected redesigns are present.

Evidence:
Objective-Delivery-Coverage: 0%
Auto-Acceptance: true
- Evidence-Type: file_output
  - Artifact: `ep_006_website_rebuilds/redesigns`
  - Objective-Proved: Confirms the redesigned landing page outputs were generated in the required folder.
  - Status: planned
- Evidence-Type: diff
  - Artifact: redesign deliverables generated per business plus review index
  - Objective-Proved: Shows the concrete output of the redesign batch.
  - Status: planned
- Evidence-Type: manual_verification
  - Artifact: review index under `ep_006_website_rebuilds/redesigns`
  - Objective-Proved: Provides a single path for reviewing every redesign artifact against the source businesses.
  - Status: planned

Implementation Log:
- 2026-03-29 02:54:28 Europe/London: Created backlog task to redesign every site in `ep_006_website_rebuilds/se_london_hairdressers_legacy.json` using the same `redesign-existing-projects` skill used for the Fun Cuts rebuild.

Changes Made:
- Backlog task created only. No implementation work started.

Validation:
- `Get-Content ep_006_website_rebuilds\se_london_hairdressers_legacy.json | Select-Object -First 80`
  - Result: Confirmed the current source JSON exists and contains the expected `sites` array of legacy businesses beginning with `Fun Cuts`.

Risks/Notes:
- The redesign batch should preserve each business's contact/location details from the source site while modernizing presentation.
- If any site lacks enough usable content or imagery, the implementation task should create a documented placeholder strategy rather than blocking the batch.
- Output should stay grouped under `ep_006_website_rebuilds/redesigns` with one subfolder per business to keep review manageable.

Completion Status:
- Backlog - 2026-03-29 02:54:28 Europe/London
