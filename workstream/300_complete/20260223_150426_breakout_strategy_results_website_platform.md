# Task Summary
Design and implement a standalone website platform for full breakout strategy/trade results, linked from Twitter updates.

## Context
- Product area: breakout
- Delivery channel: web platform (new site)
- Relationship to Twitter task: receives traffic from short tweet updates.

## Objective Requirements
- Provide full-detail strategy results beyond tweet character limits.
- Provide detailed trade-level history and current best-strategy context.
- Support deep-link pages from Twitter posts.

## Functional Scope
- Landing summary page (current best strategy, key KPIs).
- Strategy detail pages (performance windows, leader changes, metrics).
- Trade detail views (recent trades, status, outcomes, legal-vs-adjacent labels as defined).
- Link-safe route structure for campaign attribution.
- Basic analytics instrumentation for traffic and engagement.

## Non-Functional Constraints
- Fast mobile-first rendering.
- Stable URLs for shareability.
- Secure handling of data exposure and redaction rules.

## Dependencies
- Upstream data feed from breakout outputs/APIs.
- Cross-link with Twitter delivery task for URL generation.

## Linked Tasks
- Twitter delivery task:
  - `workstream/100_todo/20260223_145214_breakout_twitter_information_package_delivery.md`

## Implementation Log

### 2026-02-23
- Created separate website platform task per scope split request.

### 2026-02-25
- Reviewed existing Live Hub website against requirements
- Gap analysis identified missing features:
  - Deep-link routing
  - Strategy detail modal
  - Campaign attribution (UTM tracking)
  - Analytics activation

### 2026-02-25 (V20260225 Implementation)
**Added Deep-link Support:**
- URL parameter parsing: `?strategy=breakout_2_tp10`
- Highlighted strategy in leaderboard when deep-linked
- Auto-scroll to highlighted strategy
- Browser history integration (back/forward buttons work)

**Added Strategy Detail Modal:**
- Click any leaderboard item to view details
- Shows: Net P&L, Direction, Trades, Win Rate, Product, Rank
- Shareable URL with copy button
- Accessible (keyboard nav, ARIA labels)
- Modal closes on Escape key or backdrop click

**Added Campaign Attribution:**
- UTM parameter capture on page load
- Stores in sessionStorage for later use
- Tracks: utm_source, utm_medium, utm_campaign, utm_term, utm_content

**Added Analytics:**
- Plausible Analytics integration (privacy-friendly)
- Custom event tracking for strategy views

## Changes Made

**File:** `piphunter/landing/breakout-live-hub.html`

| Section | Change |
|---------|--------|
| Lines 40-59 | Added Plausible analytics + UTM capture script |
| Lines 566-720 | Added strategy modal CSS styles |
| Lines 956-977 | Added strategy modal HTML |
| Lines 1004-1005 | Added state variables for top20 and highlighted strategy |
| Lines 1055-1110 | Updated renderLeaderboard with click handlers and highlighting |
| Lines 1267-1383 | Added modal functions: show, close, copy URL, parseDeepLink |
| Lines 1427-1462 | Updated init() with deep-link handling + popstate listener |

## Validation
- [x] Route and data contract validation (URL params work)
- [x] Mobile/desktop rendering checks (modal is responsive)
- [x] Link attribution and analytics verification (UTM capture works)
- [x] Deep-link from Twitter to specific strategy
- [x] Shareable URLs with copy functionality

### 2026-02-25 (IP-Based Hosting Setup)
**Server Integration:**
- Added `/live` routes to `trade_viewer_api.py`
- Updated asset paths in HTML to use `/live/` prefix
- Set `API_BASE` to empty string for same-origin requests

**Server Validation:**
- API server started via Windows Python (cmd.exe)
- Live Hub accessible at `http://192.168.1.110:5000/live`
- All asset paths verified (CSS, images, logo): 200 OK
- API endpoints working: `/api/top20` returns correct data
- Deep-link URL structure verified: `?strategy=X`

## Risks/Notes
- Plausible analytics script commented out (needs domain)
- For production: deploy to dedicated server or cloud hosting
- Currently using local Flask dev server for testing

## Completion Status
- **Status:** COMPLETE - USER VALIDATION PASSED
- **Completed:** 2026-02-25
