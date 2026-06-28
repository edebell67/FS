# EP038 — MVP Build Roadmap

Created: 2026-06-27

## Goal

Build the smallest website that proves whether people want a live pricing-spread product.

The MVP should show:

```text
continuous spreads as live product cards
```

not a static theory page.

## MVP v0 — Static proof board

### Objective

Create a simple static page that displays 10 spread cards from `data/live_spread_board.csv`.

### Required pages

```text
/index.html              landing page
/live-spreads.html       sample live board
/methodology.html        how spreads are found/scored
```

### Required features

- 9:16/social-card-friendly spread cards;
- category labels;
- state badges: LIVE/WATCHING/EXPIRED/AVOID;
- gross spread %;
- last checked timestamp;
- confidence/risk score;
- public note;
- email/waitlist CTA.

### What can be manual

- data collection;
- candidate refresh;
- price checks;
- CSV updates;
- deployment.

### What should not be built yet

- full crawler;
- paid login;
- payment system;
- alerts;
- user accounts;
- complex backend.

## Data requirement before public sample

Need at least 10 records in:

```text
data/live_spread_board.csv
```

They can be marked honestly as:

```text
DISCOVERED
WATCHING
LIVE
EXPIRED
AVOID
```

It is acceptable to show rejected/expired examples because they build trust.

## Candidate collection sequence

1. Physical products with clear sold-price evidence.
2. Domain candidates with clear transfer model.
3. Digital products only where licence/platform status is explicit.

Reason:

```text
The website product can cover all spreads, but the first board must contain examples that are easy to understand and verify.
```

## Page copy direction

Hero:

```text
Live pricing spreads, refreshed continuously.
```

Subhead:

```text
A live board of marketplace pricing gaps — showing where products or assets appear to sell higher in one place than they can be sourced elsewhere.
```

CTA:

```text
Join early access
```

Trust note:

```text
Research leads only. Verify prices, stock, fees, delivery and platform rules before acting. No profit is guaranteed.
```

## Build order

### Step 1 — Seed board

Populate `data/live_spread_board.csv` with 10 sample spread records.

### Step 2 — Generate static board

Create a script:

```text
scripts/render_live_spread_site.py
```

that reads CSV and writes static HTML.

### Step 3 — Local preview

Open/serve locally and inspect visual layout.

### Step 4 — Publish sample

Deploy to GitHub Pages or another static host.

### Step 5 — Market test

Use `EP038_MARKET_STRATEGY.md` to drive first traffic and collect waitlist interest.

## Validation criteria

Proceed to automation only if the static board gets one or more of:

- users understand the product without explanation;
- waitlist signups;
- category requests;
- someone asks for access to source links;
- someone is willing to pay for early access.

## Automation roadmap after validation

### Automation 1 — Refresh helper

Script to re-check URLs and timestamps manually/semi-automatically.

### Automation 2 — Price history snapshots

Append each check to:

```text
data/price_history.csv
```

### Automation 3 — State engine

Promote/demote spreads:

```text
DISCOVERED → WATCHING → LIVE → COOLING → EXPIRED
```

### Automation 4 — Alerts

Email/Telegram alert when:

- spread crosses threshold;
- expired spread returns;
- price spike detected;
- source price drops.

### Automation 5 — Paid access

Only after demand validation:

- private board;
- source links behind login;
- Stripe/subscription;
- category-specific feeds.

## Immediate next task

Build the static website skeleton and render it from `data/live_spread_board.csv`.
