# EP047 — News public-scope integration

**Task Type:** standard
**Task Attributes:** workflow_task: true; workflow_name: EP047 Hyperlocal News and Directory; workflow_stage: in_progress
**Destination Folder:** `epics/ep_047_newssite/` and `epics/ep_047_directory_app/`
**Dependency:** Directory public-scope release; DB-backed News conversion is now included in `EP047-2026.07.31.1`.

## Plan

- [x] 1. Add a read-only public scope endpoint to the directory app.
  - Test: `npm run verify` passed with `/api/public-scope` included in the build.
- [x] 2. Filter the static News prototype from current public scope.
  - Test: Static HTML contains `allowedTowns` filtering for place options, stories and ticker.
- [x] 3. Filter contextual directory links by public town/category scope.
  - Test: Static HTML filters directory categories with `allowedCategories`.
- [x] 4. Convert News display to database extraction and add a repeatable seed/import path.
  - Test: `npx tsx --env-file=.env.local scripts/seed-news-from-static.ts --dry-run` passed: 7 stories and 7 category mappings extracted.
- [x] 5. Run local typecheck/build and prepare hosted migration + seed deployment.
  - Test: `npm run typecheck` passed; `npm run build` passed. Local DB seed was blocked by PostgreSQL recovery mode; Render `preDeployCommand` runs migration then seed.
- [ ] 6. Deploy and verify hosted health, public News API, directory scope and live News page.

## Evidence

Objective-Delivery-Coverage: 90%
Auto-Acceptance: false

- Evidence-Type: file_output
  - Artifact: `workstream/600_workflow/ep047/EP047_admin_visibility_and_news_management_workflow.html`
  - Objective-Proved: Approved EP047 workflow reference.
  - Status: captured
- Evidence-Type: manual_verification
  - Artifact: `not_applicable`
  - Objective-Proved: Hosted News scope behavior.
  - Status: planned

## Implementation Log

- 2026-07-30 — Started after directory visibility persistence passed; current static News prototype does not consume directory scope.
- 2026-07-30 — Added `/api/public-scope` and wired the static News prototype to remove hidden towns/stories and filter directory links. Release identifier advanced to `EP047-2026.07.30.5`. `npm run verify` passed.
- 2026-07-31 — Added `/api/public-news`, DB-backed News mapping, repeatable static-to-DB seed script, and Render pre-deploy migration/seed. News page now starts empty and renders only records returned by the DB API; its embedded stories are retained solely as the deploy-time seed source. Version advanced to `EP047-2026.07.31.1`.

## Completion Status

**Awaiting hosted verification** — DB-backed conversion is locally compiled and extraction-validated; deploy is the remaining step.
