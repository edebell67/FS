# Bot Parity Checklist Lead Magnet

## Task Type
Documentation / marketing asset creation

## Destination
/mnt/c/Users/edebe/eds/products/backtest_live_parity_audit_kit

## Dependency
Kanban task t_b9018719; parent t_20b21c7c package v0.2 exists.

## Plan
- Review existing paid kit docs and marketing copy.
- Create a lightweight free checklist that captures interest without giving away scripts/templates.
- Add CTA copy pointing to paid audit kit and async review options.
- Validate file presence and content boundaries.

## Tests / Evidence Planned
- Confirm deliverable files exist.
- Check lead magnet avoids trading advice/profit claims and does not expose paid scripts/templates.

## Evidence
- Existing paid kit docs reviewed: docs/02_parity_checklist.md, docs/03_deployment_readiness_scorecard.md, marketing/landing_page_copy.md, marketing/outreach_pack.md.
- New checklist keeps the asset lightweight and points readers to the paid kit for templates, scripts, scorecard, and full audit workflow.

## Implementation Log
- 2026-05-18 21:09 Started task.
- 2026-05-18 21:12 Created free checklist and CTA copy in the product marketing folder.
- 2026-05-18 21:14 Validated files for presence, line/character counts, disclaimer terms, and obvious risky phrase hits.

## Changes
- Added `/mnt/c/Users/edebe/eds/products/backtest_live_parity_audit_kit/marketing/free_bot_parity_checklist.md`.
- Added `/mnt/c/Users/edebe/eds/products/backtest_live_parity_audit_kit/marketing/free_lead_magnet_cta_copy.md`.

## Validation
- Command: `python - <<'PY' ...` checked both files.
- Result: checklist 183 lines / 5802 chars; CTA copy 193 lines / 5394 chars.
- Result: required disclaimer boundary terms present in both files.
- Result: no hits for selected risky phrases (`guaranteed returns`, `guarantee returns`, `profitable strategy`, `trading signal:`).
- Manual review confirmed no paid scripts or CSV templates were included in the free asset.

## Risks
- Lead magnet still needs a hosted download/capture URL before public use.
- Stripe placeholders remain intentionally unfilled until Ed provides links.

## Completion Status
Complete.
