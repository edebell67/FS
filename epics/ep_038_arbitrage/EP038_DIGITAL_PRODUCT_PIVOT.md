# EP038 — Digital Product Pivot: Pricing Spread Intelligence

Created: 2026-06-27

## Pivot

Instead of making the main business model direct arbitrage of products, EP038 can turn the **finding of price spreads** into the digital product itself.

The product is not:

```text
"We buy and resell trainers/domains/software keys."
```

The product becomes:

```text
"We find and package live marketplace pricing-spread intelligence for people who want arbitrage opportunities."
```

## Why this is stronger

Direct arbitrage has operational risk:

- stockouts;
- fulfilment delays;
- returns;
- authenticity disputes;
- marketplace policy exposure;
- capital/cash-flow requirement;
- platform account risk.

A digital spread-intelligence product has a different risk profile:

- no need to hold stock;
- no need to fulfil buyer orders;
- no live transaction exposure;
- repeatable research process;
- can cover both physical and digital categories;
- can be sold as reports, alerts, dashboards, watchlists, or subscriptions.

## Core product concept

EP038 sells:

```text
pricing spread intelligence
```

Examples:

- weekly arbitrage opportunity report;
- live watchlist of high-spread products;
- domain-name opportunity watchlist;
- trainer/outlet spread watchlist;
- marketplace spike alerts;
- source database for lower-cost acquisition;
- historical sale-price movement summaries;
- category-specific arbitrage briefs.

## Target customer

Potential buyers:

- eBay resellers;
- sneaker/trainer resellers;
- domain investors;
- side-hustle operators;
- local small resellers;
- marketplace sellers;
- product researchers;
- people who do not want to manually search multiple sources.

## MVP product

Start with a simple digital information product:

```text
EP038 Weekly Spread Sheet
```

Format:

```text
Google Sheet / CSV / PDF briefing / Notion-style report
```

Initial offer:

```text
10 researched pricing-spread candidates per week
+ marketplace observed sell/list price
+ lower-cost source link
+ estimated spread after visible fees
+ risk score
+ confidence rating
+ notes on source reliability
```

## Critical positioning

Do **not** promise guaranteed profit.

Use language like:

```text
research leads
pricing-spread watchlist
candidate opportunities
marketplace intelligence
further verification required
```

Avoid:

```text
guaranteed profit
risk-free arbitrage
instant money
sure thing
```

## Product value

The customer is paying for:

- time saved;
- cross-market price discovery;
- source discovery;
- spread monitoring;
- historical price context;
- initial filtering;
- risk notes;
- early signal of price spikes.

## Data model

Each opportunity record should include:

- product/domain/item name;
- category;
- marketplace URL;
- marketplace observed price;
- sold-price evidence if available;
- cheaper source URL;
- source price;
- spread percentage;
- visible fees/shipping assumptions;
- estimated net margin range;
- stock/availability status;
- policy/legal/licence risk;
- confidence score;
- last checked date;
- notes.

## Scoring model

### Spread score

```text
5 = >=40% gross spread
4 = 30–39%
3 = 20–29%
2 = 10–19%
1 = <10%
```

### Demand score

```text
5 = multiple sold comps / high velocity
4 = clear sold comps
3 = active listings and category demand
2 = weak evidence
1 = speculative
```

### Risk score

```text
5 = low risk / clean transfer / clear product identity
4 = manageable risk
3 = moderate risk
2 = high risk
1 = avoid
```

### Confidence score

Combine:

```text
spread + demand + risk + source reliability
```

## Product tiers

### Free/sample

```text
3 example opportunities
weekly public teaser
no full source database
```

### Starter

```text
10 opportunities/week
basic spread and risk notes
CSV/Sheet access
```

### Pro

```text
25–50 opportunities/week
category filters
source database
price-spike alerts
historical context
```

### Niche reports

```text
Trainer spreads
Domain-name spreads
Digital-products spread watchlist
Local marketplace flips
```

## Compliance guardrails

- Present records as research leads, not instructions to buy/sell.
- Do not scrape or redistribute marketplace data in a way that breaches terms.
- Do not advise illegal, deceptive, counterfeit, or unauthorised resale.
- Flag licence/platform restrictions for digital goods.
- Do not publish personal seller data unnecessarily.
- No claims of guaranteed profit.
- Make users verify stock, price, delivery, and policy before acting.

## Initial build path

1. Build a manual first issue with 10 candidate records.
2. Use only public-source research.
3. Store data in `data/spread_intelligence_candidates.csv`.
4. Produce a sample report in markdown/PDF.
5. Test whether the report feels valuable enough to sell.
6. Only then automate collection/monitoring.

## Key insight

The defensible product is not the spread itself.

The defensible product is:

```text
repeatable discovery + filtering + scoring + source memory + timing alerts
```

EP038 should therefore build the intelligence engine first, not rush into live arbitrage.
