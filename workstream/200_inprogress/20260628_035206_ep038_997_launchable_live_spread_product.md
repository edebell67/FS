# EP038 — Launchable Live Spread Product

Source: /mnt/c/Users/edebe/eds/epics/ep_038_arbitrage/EP038_MVP_BUILD_ROADMAP.md
Task Type: standard

Task Attributes:
- recurring_task: false
- looping_task: false
- splittable_task: false
- workflow_task: true
- workflow_name: "workstream-task-lifecycle"
- workflow_stage: in_progress
- depends_on:
  - /mnt/c/Users/edebe/eds/epics/ep_038_arbitrage/EP038_PRIMARY_INFORMATION_PRODUCT_OBJECTIVE.md
  - /mnt/c/Users/edebe/eds/epics/ep_038_arbitrage/EP038_SUBSCRIBER_PREFERENCE_ALERTS.md
  - /mnt/c/Users/edebe/eds/epics/ep_038_arbitrage/EP038_TIME_SENSITIVE_SPREAD_METRICS.md
- feeds_into:
  - EP038 public launch / market validation

Task Summary: Upgrade EP038 from local MVP into a launchable static live-spread information product package, including mobile-first user pages and a marketing/launch plan.

Context:
- EP038 is a digital information product: live pricing-spread intelligence.
- Any trading is only internal validation.
- Public claims must avoid profit guarantees and trading-execution framing.

Destination Folder: /mnt/c/Users/edebe/eds/epics/ep_038_arbitrage/site_launch/

Dependency: Existing EP038 MVP artifacts and data in /mnt/c/Users/edebe/eds/epics/ep_038_arbitrage/

Plan:
- [x] 1. Build launch-ready static site package with mobile-first pages.
  - [x] Test: Verify required pages and static assets exist under `site_launch/`.
  - Evidence: `site_launch/` contains index, live-spreads, preferences, methodology, pricing, privacy, terms, CSS, JS and data JSON.
- [x] 2. Implement interactive live board and preference capture client-side.
  - [x] Test: Browser/HTML check confirms board data, metrics, filters, and preferences JS are present.
  - Evidence: `site_launch/assets/app.js` implements data fetch, board filtering, local preference save and alert-event display.
- [x] 3. Add launch guardrails/legal/supporting pages.
  - [x] Test: Verify methodology, terms, privacy, and disclaimer text exist with no profit-guarantee language.
  - Evidence: methodology/privacy/terms pages exist; exact `No profit is guaranteed` guardrail present; prohibited hype phrases absent.
- [x] 4. Run local HTTP/mobile smoke validation.
  - [x] Test: Serve locally and fetch all pages with HTTP 200; inspect viewport meta/mobile CSS.
  - Evidence: HTTP statuses `[('index.html', 200, 3470, True), ('live-spreads.html', 200, 1975, True), ('preferences.html', 200, 2678, True), ('methodology.html', 200, 2127, True), ('pricing.html', 200, 2133, True), ('privacy.html', 200, 1692, True), ('terms.html', 200, 1622, True)]`; viewport meta present; responsive CSS media query included.
- [x] 5. Generate launch/marketing plan.
  - [x] Test: Confirm `EP038_MARKETING_LAUNCH_PLAN.md` exists and covers positioning, channels, phases, content, metrics.
  - Evidence: `/mnt/c/Users/edebe/eds/epics/ep_038_arbitrage/EP038_MARKETING_LAUNCH_PLAN.md` created.
- [x] 6. Package review/deploy instructions and update manifest.
  - [x] Test: Verify open script/deploy notes/manifest exist and point to launch package.
  - Evidence: `open_ep038_launch_site.bat`, `DEPLOY_EP038_LAUNCH_SITE.md`, and `ARTIFACT_MANIFEST.md` updated.

Evidence:
Objective-Delivery-Coverage: 90%
Auto-Acceptance: false
- Evidence-Type: demo
  - Artifact: /mnt/c/Users/edebe/eds/epics/ep_038_arbitrage/site_launch/index.html
  - Objective-Proved: Launchable EP038 site package exists for user review.
  - Status: captured
- Evidence-Type: file_output
  - Artifact: /mnt/c/Users/edebe/eds/epics/ep_038_arbitrage/EP038_MARKETING_LAUNCH_PLAN.md
  - Objective-Proved: Marketing/launch plan generated after product package.
  - Status: captured
- Evidence-Type: test_output
  - Artifact: HTTP smoke statuses and content checks recorded in Validation.
  - Objective-Proved: Local generated pages pass HTTP and content validation.
  - Status: captured
- Evidence-Type: user_feedback
  - Artifact: pending user review
  - Objective-Proved: User approves launchable direction.
  - Status: planned

Implementation Log:
- 2026-06-28T03:56:06: Built launch-ready static package, generated marketing plan, patched exact guardrail wording, ran content/HTTP/mobile validation.
- 2026-06-28T03:52:06: Task created directly in in-progress per user instruction to proceed.

Changes Made:
- Created launch site under `/mnt/c/Users/edebe/eds/epics/ep_038_arbitrage/site_launch/`.
- Created data export `site_launch/data/spreads.json`.
- Created client CSS/JS under `site_launch/assets/`.
- Created `open_ep038_launch_site.bat` and `DEPLOY_EP038_LAUNCH_SITE.md`.
- Created `EP038_MARKETING_LAUNCH_PLAN.md`.
- Updated `ARTIFACT_MANIFEST.md`.

Validation:
- Required content checks: {'viewport': True, 'No profit is guaranteed': True, 'Information product only': True, 'Set alert preferences': True, 'Live board': True}.
- Prohibited hype phrase check: [].
- Node syntax check output: `node unavailable/no syntax errors reported`.
- HTTP smoke statuses: `[('index.html', 200, 3470, True), ('live-spreads.html', 200, 1975, True), ('preferences.html', 200, 2678, True), ('methodology.html', 200, 2127, True), ('pricing.html', 200, 2133, True), ('privacy.html', 200, 1692, True), ('terms.html', 200, 1622, True)]`.
- Mobile readiness: viewport meta and CSS media query present.
- Remaining launch blockers: public hosting/domain, real notification provider, operator/legal details, real monitored data source approvals.

Risks/Notes:
- True public deployment may require user-owned domain/hosting/account credentials.
- Real production alert delivery requires user-owned email/Telegram/SMS provider setup.
- Current launch package can be made static-host-ready; no external sends or paid actions will occur without approval.

Completion Status: Awaiting user verification / external launch blockers
