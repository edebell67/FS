---
name: ep038-live-spread-information-product
description: Build repeatable EP038-style live pricing-spread intelligence products: data model, spread value metrics, time-sensitive expiry metrics, subscriber preference alerts, static/mobile launch package, validation, and launch plan.
---

# EP038 Live Spread Information Product

Use this skill when building or repeating an EP038-style product where the **information about pricing spreads** is the digital product.

The public product is:

```text
Live pricing-spread intelligence
```

not:

```text
trading execution
managed arbitrage
guaranteed profit
```

Internal test trading may be used only to validate signal quality and scoring.

## Trigger Conditions

Use this skill when the user asks to:

- create a live spread board / pricing-spread website;
- turn arbitrage research into a digital information product;
- publish total spread value and spread count;
- track auction/expiry pressure on spread value;
- notify subscribers when preferred spreads appear;
- build a mobile-first launch package for spread intelligence;
- generate a launch/marketing plan for a spread information product.

## Core Product Model

The product sells access to:

- spread candidates;
- marketplace/source price comparison;
- gross spread value;
- spread count;
- freshness timestamps;
- expiry/time pressure;
- confidence scoring;
- risk notes;
- subscriber preference alerts;
- history/alerts later.

Always use the wording:

```text
gross spread value
observed spread value
candidate spread information
research information
```

Avoid:

```text
profit
guaranteed profit
risk-free arbitrage
we trade for you
copy our trades
```

## Required Artefacts

Create all artefacts under the epic root, e.g.:

```text
epics/ep_038_arbitrage/
```

Minimum files:

```text
EP038_PRIMARY_INFORMATION_PRODUCT_OBJECTIVE.md
EP038_LIVE_SPREAD_WEBSITE_SPEC.md
EP038_KEY_SALES_METRICS.md
EP038_TIME_SENSITIVE_SPREAD_METRICS.md
EP038_SUBSCRIBER_PREFERENCE_ALERTS.md
EP038_MARKETING_LAUNCH_PLAN.md
DEPLOY_EP038_LAUNCH_SITE.md
ARTIFACT_MANIFEST.md
```

Data:

```text
data/live_spread_board.csv
data/marketplace_monitoring_universe.csv
data/subscriber_preferences.csv
data/alert_events.csv
```

Launch package:

```text
site_launch/index.html
site_launch/live-spreads.html
site_launch/preferences.html
site_launch/methodology.html
site_launch/pricing.html
site_launch/privacy.html
site_launch/terms.html
site_launch/assets/styles.css
site_launch/assets/app.js
site_launch/data/spreads.json
open_ep038_launch_site.bat
```

## Data Model

`live_spread_board.csv` should include at least:

- spread_id;
- state;
- category;
- item_name;
- variant / SKU / identifier;
- marketplace and marketplace URL;
- marketplace price;
- source and source URL;
- source price;
- currency;
- gross_spread_amount;
- gross_spread_pct;
- estimated fees;
- estimated net margin range;
- observation count;
- first_seen;
- last_checked;
- source availability;
- demand signal;
- confidence score;
- risk score;
- policy/rights status;
- risk notes;
- public card summary;
- internal notes.


## Spread Inclusion Gate

A product/asset can only appear on the live spread board when both sides of the spread are known or defensibly estimated:

```text
source/acquisition price + sale price/sold price/credible guide sale price
```

If sale/reference/guide price is unknown, keep the item as an `auction watch candidate` or `research observation`, not a spread. It must not count toward active spread count, active gross spread value, expiring spread value, or subscriber spread alerts.

Auction-side current bid alone is not a spread.

## Required Metrics

The website must publish these headline metrics:

```text
active gross spread value
active spread count
all-time identified gross spread value
total identified spread count
```

Use active states:

```text
DISCOVERED
WATCHING
LIVE
COOLING
```

Exclude from active metrics:

```text
EXPIRED
AVOID
```

### Time-sensitive metrics

Add expiry/time-pressure fields:

```text
time_sensitive
expiry_type
expiry_at
hours_to_expiry
expiry_value_status
urgency_level
```

Publish:

```text
gross spread value expiring within 24h
count of time-sensitive spreads
next expiry / auction close where available
```

Always include:

```text
Time pressure indicates expiry risk, not an instruction to trade.
```

## Marketplace Monitoring Selection

Prioritise marketplaces/sources where at least two of these are visible:

```text
price discovery
buyer demand
listing turnover
sold/closed evidence
```

Priority marketplace types:

1. Continuous auction markets.
2. Ready-buyer marketplaces.
3. Buyer-request / wanted-demand venues.
4. High-turnover listing environments.

Score each candidate market on:

- auction/closing-price visibility;
- buyer-demand visibility;
- sold/completed data availability;
- listing turnover signal;
- category relevance;
- access feasibility;
- policy fit;
- automation feasibility;
- inverse noise/fraud risk.

## Subscriber Preference Alerts

Create preference and alert schemas:

```text
data/subscriber_preferences.csv
data/alert_events.csv
```

Preference fields should cover:

- subscriber_id;
- status;
- email/channel;
- category filters;
- marketplace filters;
- minimum gross spread percentage;
- minimum gross spread value;
- minimum confidence;
- maximum risk;
- time-sensitive-only;
- expiry window;
- frequency.

Alert events should include:

- alert_id;
- subscriber_id;
- spread_id;
- trigger_type;
- triggered_at;
- delivery_channel;
- delivery_status;
- message_summary;
- notes.

In MVP, use:

```text
delivery_status=would_send_no_delivery
```

until a user-owned notification provider is configured.

## Static/Mobile Launch Package

Build a static host-ready package under:

```text
site_launch/
```

Pages:

- `index.html` — headline metrics and CTA;
- `live-spreads.html` — interactive board with search/filter/time-sensitive toggle;
- `preferences.html` — subscriber preference capture;
- `methodology.html` — scoring and guardrails;
- `pricing.html` — free preview / founder access / pro later;
- `privacy.html` and `terms.html` — explicit placeholders if operator details are unknown.

Mobile requirements:

- viewport meta;
- responsive CSS media query;
- hamburger/mobile navigation;
- cards stack on mobile;
- form fields are touch-friendly;
- no wide tables as the primary mobile UI.

## Validation Checklist

Run local checks before claiming launch-ready:

1. Required files exist under `site_launch/`.
2. `site_launch/data/spreads.json` contains metrics and spreads.
3. Site contains exact guardrail:

```text
No profit is guaranteed.
```

4. Prohibited phrases are absent:

```text
risk-free arbitrage
buy this and make money
we trade for you
```

5. Local HTTP smoke returns 200 for all pages:

```text
index.html
live-spreads.html
preferences.html
methodology.html
pricing.html
privacy.html
terms.html
```

6. Mobile readiness:

```text
viewport meta present
responsive CSS present
```

7. JavaScript syntax checked where Node is available:

```bash
node --check site_launch/assets/app.js
```

## Marketing / Launch Plan

Generate `EP038_MARKETING_LAUNCH_PLAN.md` after the launch package exists.

It must include:

- positioning statement;
- primary sales hook;
- audience segments;
- offer ladder;
- 14-day launch sequence;
- content templates;
- validation metrics;
- risks and guardrails.

Core hook:

```text
We found £X gross spread value across Y candidates — and £Z may expire within 24h.
```

Validation targets before automation/payment build:

- 50 landing-page visits;
- 10 preference submissions;
- 3 user conversations;
- 1 paid/founder interest;
- repeated category requests.

## Launch Blockers to Surface

Do not pretend public launch is complete until these are resolved:

- hosting/domain target;
- operator/legal/privacy details;
- notification provider;
- real monitored source approvals/access;
- payment provider if charging;
- live data refresh process.

## Git / Handoff

When committing:

- stage only the epic folder, the relevant lifecycle task(s), and this skill if requested;
- avoid staging unrelated repo changes;
- run path-scoped git status if full status is slow;
- record commit SHA and push result;
- if push fails, report exact blocker and leave local commit intact.
