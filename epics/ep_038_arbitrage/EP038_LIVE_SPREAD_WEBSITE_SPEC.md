# EP038 — Live Spread Website Spec

Created: 2026-06-27

## Product direction

EP038 will become a website that publishes **continuous pricing spreads** as live digital products.

The primary business objective is **information provision**. We provide live pricing-spread intelligence; we do not position the site as a trading execution service.

The website is not simply a blog or static report.

It is a live market-intelligence product:

```text
Find recurring product/asset price spreads
→ monitor them continuously
→ publish active spreads as live product cards
→ sell access to filtered intelligence, alerts, and historical context
```

## Core website promise

```text
See active marketplace pricing gaps before they disappear.
```

Alternative positioning:

```text
Live spread intelligence for marketplace resellers.
```

```text
A continuously updated watchlist of product pricing gaps.
```

```text
Find what is selling high — and where it may be sourced lower.
```

## What the website publishes

Each spread is shown as a live product entry.

### Example live spread card

```text
Product: Nike Air Max [model / size]
Category: Trainers
Marketplace observed price: £120
Lower-cost source: £89
Gross spread: 25.8%
Estimated net margin range: £10–£18
Demand signal: recent sold/listing activity
State: LIVE
Last checked: 14:35 today
Risk: size/stock/authenticity/returns
Confidence: Medium
```

### Digital/domain example

```text
Asset: [domain name]
Category: Domain
Marketplace ask/comps: £400–£700
Acquisition source: deleted/closeout/reg-fee candidate
Source cost: £8–£25 + renewal
State: WATCHING
Risk: trademark/liquidity
Confidence: Low/Medium until comps verified
```

## Live spread states

Use visible state badges:

```text
DISCOVERED — found, not yet verified
WATCHING — repeated spread under observation
LIVE — active spread with visible source + marketplace evidence
COOLING — spread narrowing or stock weakening
EXPIRED — source gone or marketplace price changed
AVOID — risk/policy/licence issue
```

## Website sections

### 1. Home page

Goal: explain the product quickly.

Sections:

- hero: live spread intelligence;
- sample spread cards;
- how it works;
- why spreads disappear;
- who it is for;
- risk/verification disclaimer;
- email waitlist / sample issue signup.

### 2. Live Spread Board

Main product page.

Features:

- searchable/filterable spread cards;
- filters by category, spread %, confidence, state, age;
- sort by gross spread, confidence, last checked, demand;
- clear timestamp on every item;
- source and marketplace links gated by access tier later.

### 3. Category pages

Initial categories:

- trainers / sneakers;
- electronics/accessories;
- domains;
- digital products with resale rights;
- local marketplace flips;
- clearance/outlet spreads.

### 4. Spread detail page

For each spread:

- current observed marketplace price;
- current observed source price;
- gross spread;
- estimated fees;
- estimated net range;
- demand evidence;
- price history snapshots;
- stock/source notes;
- risk notes;
- action disclaimer;
- update history.

### 5. Sample/free page

Public teaser:

- 3 delayed/sample spreads;
- limited source visibility;
- email capture;
- explanation of paid access.

### 6. Pricing/waitlist page

Initially waitlist only.

Potential tiers later:

```text
Free teaser — 3 delayed/sample spreads
Starter — active board + weekly digest
Pro — alerts, source links, history, category filters
Niche packs — trainers/domains/digital-specific feeds
```

## MVP data model

Primary file now:

```text
data/live_spread_board.csv
```

Core fields:

- spread ID;
- state;
- category;
- item name;
- variant/SKU;
- marketplace URL;
- marketplace price;
- source URL;
- source price;
- gross spread amount;
- gross spread %;
- estimated fees;
- estimated net margin;
- observation count;
- first seen;
- last checked;
- source availability;
- demand signal;
- confidence score;
- risk score;
- public card summary.

## MVP technical approach

Start simple:

```text
CSV/JSON data
+ static website
+ manual refresh workflow
+ public sample board
```

Recommended stack for first MVP:

```text
Static HTML/JS page
or GitHub Pages
or simple Flask app if dynamic filtering needed
```

Do not build a crawler first.

First build:

```text
1. Manually collect 10 spreads.
2. Put them into live_spread_board.csv.
3. Generate a static board from the CSV.
4. Publish a sample public page.
5. Drive traffic/waitlist.
6. If people respond, automate collection and alerts.
```

## Compliance and positioning

Every page should include:

```text
Research leads only. Prices, stock, fees, delivery, resale rights and platform rules must be verified before acting. No profit is guaranteed.
```

Avoid claims like:

```text
guaranteed profit
risk-free arbitrage
buy this and make money
```

Use:

```text
candidate spreads
marketplace intelligence
watchlist
research feed
price-gap signals
```

## Success criteria for MVP

The website is successful if:

- visitors understand the concept in under 10 seconds;
- at least 10 sample spread cards are visible;
- each card has timestamp/freshness/confidence/risk;
- users join a waitlist or ask for access;
- at least one target user says they would pay for a refreshed board.

## Immediate next build step

Create a static proof page:

```text
EP038 Live Spread Board — sample MVP
```

using dummy/manual candidate data first, then replace with real researched spreads.
