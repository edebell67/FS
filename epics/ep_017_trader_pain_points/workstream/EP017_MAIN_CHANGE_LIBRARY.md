# EP017 Main Change / Action Library

Purpose: central library of applied EP017 changes, launch checks, verification evidence, and open launch actions. This file is the main reference for what has changed and what has been validated before public launch/outreach.

Location: `epics/ep_017_trader_pain_points/workstream/EP017_MAIN_CHANGE_LIBRARY.md`

Last Updated: 2026-05-12 11:08 BST

---

## Current Launch Baseline

- GitHub local HEAD: `59508107c1024242fa3cf35ff40daf39d43f86f2`
- GitHub remote `master`: `59508107c1024242fa3cf35ff40daf39d43f86f2`
- Public portal: `https://edebell67.github.io/epics/`
- Public page aliases:
  - Strongest Models: `https://edebell67.github.io/epics/models/`
  - Early Momentum: `https://edebell67.github.io/epics/momentum/`
  - Verifiable Data: `https://edebell67.github.io/epics/verify/`
  - Ranked Opportunity Feed: `https://edebell67.github.io/epics/ranked/`
- Lead capture backend: `https://ep-017.onrender.com/api/capture_lead`
- Backend stats endpoint: `https://ep-017.onrender.com/api/stats`

---

## Applied Changes / Actions

### 2026-05-12 — GitHub deployment baseline verified

- Confirmed local and remote GitHub `master` are aligned.
- Verified latest commit on both local and remote:
  - `59508107c1024242fa3cf35ff40daf39d43f86f2`
  - Message: `ep_020: Complete X: drive migration & ep017: Landing page anchor/link fixes`

Evidence:

```text
remote master: 59508107c1024242fa3cf35ff40daf39d43f86f2
local head:    59508107c1024242fa3cf35ff40daf39d43f86f2
```

### 2026-05-12 — Project context and launch workflow loaded

- Read user/project context inventory:
  - `C:\Users\edebe\Downloads\ed_project_context_inventory.md`
- Read landing-page-management skill:
  - `C:\Users\edebe\eds\skills\landing-page-management\SKILL.md`
- Applied key workflow checks:
  - Page variants mapped to pain points.
  - Email capture remains the primary objective.
  - Backend URL points to Render, not localhost.
  - Short aliases are used for public posting.
  - Marketing copy uses final shortened URLs.

### 2026-05-12 — EP017 file and alias inventory checked

Found key EP017 launch files:

- `page_1_strongest_models/index.html`
- `page_2_early_momentum/index.html`
- `page_3_verifiable_data/index.html`
- `page_4_ranked_opportunity/index.html`
- `page_1_strongest_models/app.js`
- `page_2_early_momentum/app.js`
- `page_3_verifiable_data/app.js`
- `page_4_ranked_opportunity/app.js`
- `marketing/copy_matrix.md`
- `verify_email_capture_focus.py`
- `verify_backend_capture.py`
- `api/json_backend.py`
- `api/requirements.txt`
- `api/Procfile`

Alias folders observed under `C:\Users\edebe\eds`:

- `models/`
- `momentum/`
- `data/`
- `ranked/`
- `index.html`

Note: public marketing uses `/verify/`; local folder inventory showed `data/` as an alias folder. Public HTTP check for `/verify/` returned 200, so deployed state is valid, but local alias naming should be checked before future edits if needed.

### 2026-05-12 — Email-capture focus verified

Command:

```text
python verify_email_capture_focus.py
```

Result:

```text
EMAIL CAPTURE FOCUS CHECK PASSED
Checked 4 pages
```

What this proves:

- The four public page variants still contain the lead form.
- Email inputs and submit buttons exist.
- Forbidden non-email-capture distractions remain absent:
  - `href="#pricing"`
  - `id="pricing"`
  - `https://piphunter.io/login`
  - `https://piphunter.io/strategies`
  - `class="login-btn"`

### 2026-05-12 — Public URL checks completed

HTTP checks returned 200 for:

```text
https://edebell67.github.io/epics/          -> 200
https://edebell67.github.io/epics/models/   -> 200
https://edebell67.github.io/epics/momentum/ -> 200
https://edebell67.github.io/epics/verify/   -> 200
https://edebell67.github.io/epics/ranked/   -> 200
https://ep-017.onrender.com/api/stats       -> 200
```

### 2026-05-12 — Live backend payload issue found and fixed in verification helper

Issue found:

- `verify_backend_capture.py` was using stale payload shape:

```json
{
  "email": "...",
  "page": "verification_script",
  "metadata": {...}
}
```

Backend response:

```text
400 {"error":"Missing email or page_id"}
```

Correct live payload shape used by page `app.js` files:

```json
{
  "email": "...",
  "page_id": "strongest_models",
  "pain_point_key": "finding_right_models"
}
```

Applied change:

- Updated `verify_backend_capture.py` to send:
  - `email`
  - `page_id`
  - `pain_point_key`
- Updated stats validation to check the submitted `page_id` count rather than `total_leads`, because `/api/stats` returns a page-id keyed JSON object.

Post-fix verification:

```text
Direct POST Result: 201 {"message":"Lead captured in JSON storage"}
New Lead Count For verification_script: 1
✅ SUCCESS: Lead capture backend is functional and incrementing.
```

### 2026-05-12 — Live backend direct capture verified

Manual production-shaped POST test:

```json
{
  "email": "launch_probe_<timestamp>@example.com",
  "page_id": "launch_readiness_probe",
  "pain_point_key": "launch_readiness_probe"
}
```

Result:

```text
status 201
body {"message":"Lead captured in JSON storage"}
stats 200 {"launch_readiness_probe":1}
```

### 2026-05-12 — CORS verified for GitHub Pages origin

Origin tested:

```text
https://edebell67.github.io
```

Results:

```text
OPTIONS 200
access-control-allow-headers: content-type
access-control-allow-methods: DELETE, GET, HEAD, OPTIONS, PATCH, POST, PUT
access-control-allow-origin: https://edebell67.github.io

POST 201
access-control-allow-origin: https://edebell67.github.io
{"message":"Lead captured in JSON storage"}
```

What this proves:

- Browser-based form submission from GitHub Pages should be allowed by the Render backend.

### 2026-05-12 — Browser check of first public alias completed

URL opened:

```text
https://edebell67.github.io/epics/models/
```

Browser result:

```text
Final URL: https://edebell67.github.io/epics/ep_017_trader_pain_points/page_1_strongest_models/
Title: TradeEdge | The Strongest Live Trading Models
```

What this proves:

- The `/models/` short alias redirects/loads the intended landing page.

### 2026-05-12 — Lifecycle task file created

Created:

```text
workstream/200_inprogress/20260512_110751_ep017_999_launch_readiness_audit_and_action_log.md
```

Purpose:

- Captures all launch-readiness actions and evidence in the required lifecycle format.
- Filename includes `ep017` as requested.

---

### 2026-05-12 — Browser form-submit checks completed for all four public aliases

Submitted test emails through the live browser form on all four public aliases.

Results:

```text
/models/   -> toast: Success! Your trial is being activated.
/momentum/ -> toast: Success! Your edge is being prepared.
/verify/   -> toast: Success! Access granted to the data feed.
/ranked/   -> toast: Success! Access granted to the data feed.
```

Backend stats after tests:

```json
{
  "early_momentum": 1,
  "ranked_opportunity": 1,
  "strongest_models": 1,
  "verifiable_data": 1
}
```

What this proves:

- Public pages load from the short aliases.
- Browser form submits to the live Render backend.
- The expected page IDs are being recorded by `/api/stats`.

### 2026-05-12 — GitHub SSH authentication restored and launch audit pushed

Created and pushed commit:

```text
953df432fbcee15188ca80c48264574e44dfc6c3 docs(ep017): record launch readiness audit
```

Commit includes:

- `epics/ep_017_trader_pain_points/verify_backend_capture.py`
- `epics/ep_017_trader_pain_points/workstream/200_inprogress/20260512_110751_ep017_999_launch_readiness_audit_and_action_log.md`
- `epics/ep_017_trader_pain_points/workstream/EP017_MAIN_CHANGE_LIBRARY.md`

Auth/push verification:

```text
SSH auth: Hi edebell67! You've successfully authenticated, but GitHub does not provide shell access.
Push: 59508107..953df432 master -> master
Remote master: 953df432fbcee15188ca80c48264574e44dfc6c3
Local HEAD:    953df432fbcee15188ca80c48264574e44dfc6c3
```

---

## Current Open Launch Actions

1. Track conversions by page_id/pain_point_key after first traffic.
2. Plan Reddit outreach before posting; backlog task created: `workstream/100_backlog/20260512_192105_ep017_999_reddit_outreach_planning.md`.
3. Extract the completed X outreach into a reusable marketing runbook/template; backlog task created: `workstream/100_backlog/20260512_192105_ep017_999_reusable_marketing_outreach_runbook.md`.

### 2026-05-12 — Controlled outreach run task created

Created lifecycle task:

```text
workstream/200_inprogress/20260512_134923_ep017_997_controlled_outreach_run_001.md
```

Selected first launch slice:

- Channel: X/Twitter, pending posting tooling/auth
- Page: Strongest Models
- URL: `https://edebell67.github.io/epics/models/`
- Expected tracking keys: `page_id = strongest_models`, `pain_point_key = finding_right_models`

Draft post prepared at 268 characters:

```text
Stop guessing which trading model is working today. I’m testing a live leaderboard that tracks 100+ strategy models and surfaces the strongest performers in real time. Data, not hype.

See the leaders: https://edebell67.github.io/epics/models/ #FinTwit #TradingSignals
```

Posting capability check:

```text
xurl not installed
```

---

### 2026-05-12 — Remaining X controlled outreach completed

Completed lifecycle task:

```text
workstream/300_complete/20260512_172614_ep017_997_remaining_landing_page_outreach.md
```

Published X posts:

```text
Strongest Models:      https://x.com/i/status/2054220737007726827
Early Momentum:        https://x.com/i/status/2054237178658423239
Verifiable Data:       https://x.com/i/status/2054239840711872882
Ranked Opportunity:    https://x.com/i/status/2054242462319726943
```

Evidence artifact:

```text
ep017_remaining_posts_result.json
```

Follow-up process tasks created:

```text
workstream/100_backlog/20260512_192105_ep017_999_reddit_outreach_planning.md
workstream/100_backlog/20260512_192105_ep017_999_reusable_marketing_outreach_runbook.md
```

Important user feedback captured for future posts:

- Preserve preferred/user-provided `https://t.co/...` short URLs in X post text instead of replacing with expanded URLs unless explicitly instructed otherwise.
- Future message changes should be adaptive variants based on response data, changing one variable at a time.

---

## Known Live Backend Test Entries Created

The following probe keys may appear in `/api/stats` as test data:

- `launch_readiness_probe`
- `verification_script`
- `cors_probe`

These should be treated as internal verification entries, not real user demand.

---

## Related Lifecycle Files

- `workstream/300_complete/20260512_100428_ep017_998_remove_non_email_capture_links.md`
- `workstream/200_inprogress/20260512_110751_ep017_999_launch_readiness_audit_and_action_log.md`
