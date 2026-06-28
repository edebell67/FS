# EP038 — Marketplace Monitoring Selection Criteria

Created: 2026-06-27

## Purpose

EP038 should not monitor marketplaces randomly.

The live spread information product needs marketplaces where pricing and demand signals are strong enough to produce useful spread intelligence.

## Primary monitoring criteria

Prioritise marketplaces that have one or more of the following:

### 1. Continuous auction market

These markets show live bidding, closing prices, and changing demand.

Good because:

- prices are discovered continuously;
- sold/closing prices create stronger demand evidence;
- price spikes can be observed;
- arbitrage spread windows may appear and disappear quickly.

Examples:

```text
eBay auctions
GoDaddy Auctions
Dynadot expired domain auctions
NameJet / SnapNames / DropCatch
Catawiki
John Pye / i-bidder / Bidspotter
```

### 2. Ready supply of active buyers

These are marketplaces where buyers arrive intending to purchase.

Good because:

- listing prices have commercial meaning;
- sold/completed listings may be available;
- demand can be inferred from turnover, watch counts, sold counts, reviews, or listing velocity;
- spreads are more useful if there is evidence buyers are present.

Examples:

```text
eBay
Vinted
Depop
StockX
GOAT
Laced
Cardmarket
TCGplayer
BrickLink
Discogs
Reverb
Chrono24
Sedo
Afternic
Flippa
Etsy
```

### 3. Buyer-request / wanted-demand venues

These are places where buyers actively request products or state demand.

Good because:

- buyer intent is visible before sourcing;
- can reveal underserved products;
- can indicate demand even where sold-price data is weak.

Examples:

```text
Facebook groups with wanted posts
Reddit buy/sell/trade communities where allowed
NamePros domain wanted threads
specialist forum wanted sections
Discord/Telegram community wanted channels where allowed
local marketplace wanted posts
```

Guardrail:

```text
No contacting buyers, posting offers, scraping private groups, or joining restricted communities without explicit approval.
```

### 4. High-turnover listing environments

Marketplaces where listings appear and disappear frequently can signal sell-through.

Good because:

- delisted items may indicate sales, withdrawals, or price changes;
- repeated disappearance of similar items suggests demand;
- fast turnover helps identify categories worth monitoring.

Important caveat:

```text
Delisted does not always mean sold.
```

EP038 should record turnover as a signal, not proof, unless sold/completed evidence is available.

Examples:

```text
Vinted
Depop
Facebook Marketplace
eBay active listings
Gumtree
Shpock
specialist classifieds
```

## Monitoring score

Each marketplace/source should be scored before being added to the monitoring universe.

| Dimension | Score |
|---|---:|
| Auction/closing-price visibility | 0–5 |
| Buyer-demand visibility | 0–5 |
| Sold/completed data availability | 0–5 |
| Listing turnover signal | 0–5 |
| Category relevance | 0–5 |
| Access feasibility | 0–5 |
| Policy/compliance fit | 0–5 |
| Automation feasibility | 0–5 |
| Noise/fraud risk | inverse 0–5 |

Suggested threshold:

```text
Monitor actively if score >= 28/45
Watch manually if score 20–27
Reject/defer if score < 20
```

## Marketplace priority tiers

### Tier 1 — strongest first targets

Use when building the first real EP038 monitoring universe.

```text
eBay UK
Vinted
Depop
StockX / Laced
Sedo / GoDaddy Auctions
ExpiredDomains.net / domain auctions
```

Why:

- strong buyer activity;
- visible price/sold/listing signals;
- high turnover or auction dynamics;
- category fit for trainers/domains/collectibles/digital assets.

### Tier 2 — specialist expansion

```text
Cardmarket / TCGplayer
BrickLink
Discogs
Reverb
Chrono24
Catawiki
Flippa
Etsy digital/download categories
```

Use when a category proves promising.

### Tier 3 — manual/local/opportunistic

```text
Facebook Marketplace
Gumtree
Shpock
specialist forums
buyer-request communities
```

Use carefully because data may be weaker and contact/consent/community rules matter.

## Data EP038 should collect

For each monitored marketplace:

- source name;
- marketplace type: auction / fixed-price / classified / buyer-request / hybrid;
- category coverage;
- observed listing count;
- observed new listings per period;
- observed delistings per period;
- sold/completed evidence if available;
- average/median price;
- price spike observations;
- turnover ratio;
- access method;
- policy notes;
- automation feasibility;
- risk notes.

## Key operating principle

EP038 should prioritise markets where we can observe at least two of:

```text
price discovery
buyer demand
listing turnover
sold/closed evidence
```

A marketplace with only listings and no demand/turnover evidence should be low priority.

## Public-product implication

The website should eventually show not just the spread, but the demand signal behind it:

```text
Demand signal: auction closes daily
Demand signal: repeated sold comps
Demand signal: 8 similar listings disappeared in 48h
Demand signal: active buyer requests
Demand signal: source price dropped while marketplace ask held
```

This makes EP038 more credible than a simple price-comparison board.
