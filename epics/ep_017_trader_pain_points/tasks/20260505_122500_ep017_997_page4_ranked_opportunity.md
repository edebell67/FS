# Task: EP017 - 997 - Build Landing Page 4: "Ranked Opportunity Feed"

**Source:** `000_epic/20260505_120000_ep_017_trader_pain_point_series_processed.md`
**Task Type:** standard
**Task Attributes:**
- `recurring_task: false`
- `looping_task: false`
- `splittable_task: false`
- `workflow_task: true`
- `workflow_name: "ep017_landing_pages"`
- `workflow_stage: todo`
- `depends_on: ["20260505_120500_ep017_997_lead_capture_infrastructure"]`
**Task Summary:** Build the fourth landing page (Bottom-Right in `landing_pages_trading.png`) focused on the pain point of "Information overload / not knowing what to trade now."
**Context:** `landing_pages_trading.png`, HTML/CSS/JS.
**Destination Folder:** C:\Users\edebe\eds\epics\ep_017_trader_pain_points\page_4_ranked_opportunity
**Dependency:** 20260505_120500_ep017_997_lead_capture_infrastructure

---

## Plan
- [x] **1. Visual Implementation**
  - Test: Open `index.html` in browser and compare with `landing_pages_trading.png` bottom-right quadrant.
  - Evidence: Screenshot of the rendered page.
  - Evidence: Verified via Playwright desktop screenshot (2026-05-05)
- [x] **2. Lead Capture Integration**
  - Test: Fill out the form and submit. Check the `leads_pain_points` table in DB for the new entry.
  - Evidence: Log output or DB query result showing the captured email and `page_id="ranked_opportunity"`.
  - Evidence: Verified via `Invoke-RestMethod` and direct SQL query (2026-05-05)
- [x] **3. Mobile Verification**
  - Test: Resize browser to 375px width and verify layout.
  - Evidence: Screenshot of mobile view.
  - Evidence: Verified via Playwright mobile viewport screenshot (2026-05-05)

---

## Evidence
**Objective-Delivery-Coverage:** 100%
**Auto-Acceptance:** true

- Evidence-Type: screenshot
  - Artifact: `.playwright-mcp\page-2026-05-05T16-44-38-490Z.png`
  - Objective-Proved: Page matches design and focus.
  - Status: captured
- Evidence-Type: demo
  - Artifact: `psql` output showing `test_page4@example.com` in DB.
  - Objective-Proved: Lead capture works end-to-end.
  - Status: captured
- Evidence-Type: screenshot
  - Artifact: `.playwright-mcp\page-2026-05-05T16-45-42-190Z.png`
  - Objective-Proved: Mobile responsiveness verified.
  - Status: captured

---

## Implementation Log
- 2026-05-05 12:55: Task initialized.
- 2026-05-05 17:42: Scaffolded Page 4 by copying Page 3 and updating content for "Ranked Opportunity Feed" focus.
- 2026-05-05 17:45: Verified visual implementation and lead capture functionality.
- 2026-05-05 17:46: Mobile verification completed.

---

## Changes Made
- Created `epics/ep_017_trader_pain_points/page_4_ranked_opportunity/` folder.
- Created `index.html`, `styles.css`, `app.js`, and `verify_page.bat` for Page 4.


---

## Validation
None yet.

---

## Risks/Notes
- Adhere to vanilla CSS as per project standards.

---

## Completion Status
**COMPLETE** - 2026-05-05 17:48
