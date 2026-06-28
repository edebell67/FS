# EP038 — Artifact Manifest

Generated: 2026-06-27T20:05:29

Root:

```text
/mnt/c/Users/edebe/eds/epics/ep_038_arbitrage
```

## Current artifacts

| File | Size | Modified | Purpose |
|---|---:|---|---|
| `EP038_DIGITAL_PRODUCT_PIVOT.md` | 5095 | 2026-06-27T19:48:40 | Pivot from direct arbitrage to selling pricing-spread intelligence. |
| `EP038_LIVE_SPREAD_PRODUCT_OBJECTIVE.md` | 4018 | 2026-06-27T19:49:54 | Live-product objective: continuous spreads as live digital product entries. |
| `EP038_LIVE_SPREAD_WEBSITE_SPEC.md` | 5514 | 2026-06-27T20:04:29 | Website/product specification for publishing continuous live spreads as information products. |
| `EP038_MARKET_STRATEGY.md` | 6740 | 2026-06-27T19:54:12 | Market strategy for launching and acquiring users for live spread website. |
| `EP038_MVP_BUILD_ROADMAP.md` | 3720 | 2026-06-27T19:54:38 | MVP build sequence for static live spread board and validation. |
| `EP038_OBJECTIVE.md` | 4941 | 2026-06-27T17:52:21 | Original EP038 objective and digital-first priority. |
| `EP038_PRIMARY_INFORMATION_PRODUCT_OBJECTIVE.md` | 2686 | 2026-06-27T20:03:33 | Current primary objective: information provision as the digital product; trading only for internal validation. |
| `EP038_PRODUCT_ONE_PAGER.md` | 1857 | 2026-06-27T20:04:42 | Concise one-pager for Live Spread Intelligence as an information product. |
| `README_EP038.md` | 821 | 2026-06-27T17:54:26 | Top-level project index and guardrail summary. |
| `data/acquisition_sources.csv` | 233 | 2026-06-27T17:54:26 | EP038 working artifact. |
| `data/digital_category_shortlist.csv` | 2186 | 2026-06-27T17:56:07 | EP038 working artifact. |
| `data/domain_candidates.csv` | 2396 | 2026-06-27T19:14:15 | EP038 working artifact. |
| `data/domain_comps.csv` | 1015 | 2026-06-27T19:14:15 | EP038 working artifact. |
| `data/domain_source_checks.csv` | 1195 | 2026-06-27T19:14:15 | EP038 working artifact. |
| `data/live_spread_board.csv` | 437 | 2026-06-27T19:50:14 | Primary MVP board: spread information entries with state, confidence, risk, freshness. |
| `data/price_history.csv` | 130 | 2026-06-27T17:54:26 | EP038 working artifact. |
| `data/product_candidates.csv` | 1809 | 2026-06-27T17:56:07 | EP038 working artifact. |
| `data/spread_intelligence_candidates.csv` | 394 | 2026-06-27T19:49:06 | EP038 working artifact. |
| `reports/EP038_WEEKLY_SPREAD_SHEET_TEMPLATE.md` | 1260 | 2026-06-27T19:49:06 | EP038 working artifact. |
| `spikes/001-digital-policy-gates/README.md` | 2939 | 2026-06-27T17:56:07 | EP038 working artifact. |
| `spikes/002-candidate-category-shortlist/README.md` | 893 | 2026-06-27T17:56:07 | EP038 working artifact. |
| `spikes/003-domain-name-arbitrage/README.md` | 3188 | 2026-06-27T19:14:15 | EP038 working artifact. |

## Current project state

- EP038 primary objective is information provision as a digital product.
- The website/live board publishes continuous pricing-spread intelligence.
- Any trading is secondary internal testing/validation only.
- Public positioning must not imply execution, managed trading, or guaranteed profit.
- Next build step: create static website skeleton rendered from `data/live_spread_board.csv`.

## Guardrail

No live purchases, listings, automated scraping at scale, or marketplace transactions without explicit approval.

## Website MVP artifacts

- `site_mvp/index.html` — landing page.
- `site_mvp/live-spreads.html` — live spread board.
- `site_mvp/methodology.html` — methodology/disclaimer page.
- `site_mvp/styles.css` — visual styling.
- `scripts/render_live_spread_site.py` — CSV-to-static-site renderer.
- `open_ep038_site_mvp.bat` — Windows review entrypoint.


## Marketplace monitoring selection artifacts — 2026-06-27T23:09:33

- `EP038_MARKETPLACE_MONITORING_SELECTION_CRITERIA.md` — selection rule: prioritise continuous auction markets, ready buyer-demand marketplaces, buyer-request venues, and high-turnover listing environments.
- `data/marketplace_monitoring_universe.csv` — initial scored monitoring universe with 15 marketplaces/sources and 8 Tier-1 candidates.


## Key sales metrics — 2026-06-27T23:11:56

- `EP038_KEY_SALES_METRICS.md` — defines total spread value/count as headline sales metrics.
- `data/live_spread_board.csv` — updated with numeric `gross_spread_amount` values where possible.
- `scripts/render_live_spread_site.py` — updated to show active gross spread value/count and all-time identified value/count.


## Time-sensitive spread metrics — 2026-06-27T23:25:21

- `EP038_TIME_SENSITIVE_SPREAD_METRICS.md` — defines expiring/time-sensitive spread value as urgency metric.
- `data/live_spread_board.csv` — extended with time-sensitive/expiry fields.
- `scripts/render_live_spread_site.py` — displays expiring-within-24h value/count and per-card time pressure.


## Subscriber preference alerts — 2026-06-28T00:03:11

- `EP038_SUBSCRIBER_PREFERENCE_ALERTS.md` — defines personalised preferred-spread availability alerts.
- `data/subscriber_preferences.csv` — preference schema for categories, thresholds, risk, expiry windows, channels.
- `data/alert_events.csv` — alert event tracking schema.
- `scripts/render_live_spread_site.py` — updated CTA/methodology copy for alert preferences.


## Subscriber preference MVP — 2026-06-28T00:46:58

- `site_mvp/preferences.html` — static subscriber alert preferences page.
- `scripts/match_subscriber_alerts.py` — local matcher that creates would-send alert events; no external notifications.
- `data/subscriber_preferences.csv` — seeded with 3 demo subscriber preferences.
- `data/alert_events.csv` — populated with matched alert events for review.


## Launchable site package

- `site_launch/` — mobile-first launchable static EP038 product package.
- `site_launch/index.html` — launch home page.
- `site_launch/live-spreads.html` — interactive live spread board.
- `site_launch/preferences.html` — subscriber preference capture page.
- `site_launch/methodology.html` — methodology and guardrails.
- `site_launch/pricing.html` — early-access pricing concept.
- `site_launch/privacy.html` / `terms.html` — launch placeholder legal pages.
- `site_launch/assets/app.js` — client-side board filtering/preferences.
- `site_launch/data/spreads.json` — launch data export.
- `open_ep038_launch_site.bat` — Windows review launcher.
- `DEPLOY_EP038_LAUNCH_SITE.md` — deployment notes and blockers.
- `EP038_MARKETING_LAUNCH_PLAN.md` — marketing/launch plan.


## Live auction product proof — 2026-06-28T17:03:53

- `EP038_LIVE_AUCTION_PROOF_REQUIREMENT.md` — requirement for one real live auction product monitored end-to-end.
- `spikes/004-live-auction-proof/README.md` — selected live auction product and observation notes.
- `data/live_auction_watch.csv` — current live auction watch record for `namedigital.com`.
- `data/live_auction_observations.csv` — captured observation with current bid, time left, reference check, and spread status.
- `scripts/live_auction_watch_once.py` — one-shot capture script, no bidding/buying/contacting.
- `data/live_spread_board.csv` and `site_launch/data/spreads.json` — updated with `SPRD-LIVE-001`.


## Spread inclusion correction — 2026-06-28T19:19:21

- `EP038_SPREAD_INCLUSION_RULES.md` — mandatory rule: sale/reference/guide price required before board inclusion.
- Removed `SPRD-LIVE-001` from `data/live_spread_board.csv` and `site_launch/data/spreads.json`.
- Preserved `namedigital.com` as auction-watch observation only in `data/live_auction_observations.csv`.


## Demo/live separation — 2026-06-28T21:35:45

- Updated `data/live_spread_board.csv` with `source_kind`, `data_quality`, `qualified_spread`, and `display_section`.
- Updated `site_launch/data/spreads.json` so public live metrics show 0 qualified live spreads, 1 auction watch candidate, and 10 demo examples.
- Updated `site_launch/assets/app.js` to render qualified live spreads separately from demo examples.
- Updated `site_launch/index.html` headline to avoid claiming live spread value from demo records.
