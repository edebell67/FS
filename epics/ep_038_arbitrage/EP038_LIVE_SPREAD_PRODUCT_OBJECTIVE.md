# EP038 — Live Spread Product Objective

Created: 2026-06-27

## Core objective

EP038 is not just a one-off report and not primarily a direct arbitrage operation.

The objective is to find **continuous pricing spreads** and present those spreads as the **live digital product**.

In plain English:

```text
We identify products/assets with recurring marketplace price gaps.
We monitor those spreads over time.
We package the active spreads as live product entries customers can view, filter, and act on after their own verification.
```

## Product definition

The product is:

```text
Live Spread Intelligence
```

Each live spread is itself a product entry.

Example entry:

```text
Item: Nike Air Max [model/size]
Marketplace observed price: £X
Lower-cost source observed price: £Y
Gross spread: Z%
Last checked: timestamp
Availability: visible / low / unknown
Confidence: medium/high
Risk notes: fees, delivery, returns, authenticity
```

For digital/domain examples:

```text
Item: Domain / digital asset / licence-resellable product
Marketplace ask/sold evidence: £X
Acquisition source: £Y
Spread: Z%
Rights/transfer status: checked / unclear / avoid
Last checked: timestamp
```

## Continuous spread requirement

A candidate should become a live product only when the spread is not a single random anomaly.

Preferred evidence:

- repeated marketplace listings/sold prices;
- repeated lower-cost source availability;
- historical price range;
- spread observed more than once;
- demand/sell-through signal;
- availability refresh possible;
- source reliability known.

## Live product states

Each spread product should have a state:

```text
DISCOVERED       found but not verified
WATCHING         being monitored for repeated spread
LIVE             spread currently active and source visible
COOLING          spread narrowing or source availability weak
EXPIRED          source gone or marketplace price changed
AVOID            policy/licence/fraud/trademark/authenticity risk too high
```

## User-facing presentation

The customer sees a live catalogue/watchlist, not just a static PDF:

- live spread cards;
- category filters;
- spread percentage;
- confidence score;
- last checked time;
- source/marketplace links;
- risk notes;
- price history sparkline later;
- alert when spread reappears or spikes.

## MVP live product format

Start manually with a simple table:

```text
Live Spread Board
```

Columns:

- spread ID;
- item/product;
- category;
- marketplace price;
- lower source price;
- gross spread %;
- estimated net margin range;
- state;
- confidence;
- last checked;
- source links;
- risk notes.

## What we are selling

We sell access to:

```text
continuously refreshed spread intelligence
```

not guaranteed profit.

Better wording:

```text
Live marketplace spread watchlist
Active pricing-gap intelligence
Candidate arbitrage leads
Reseller research feed
```

Avoid:

```text
guaranteed profit
risk-free arbitrage
buy this and make money
```

## Automation direction

The automation should eventually:

1. collect marketplace observed prices;
2. collect acquisition/source prices;
3. match equivalent products/assets;
4. calculate spread after fees;
5. store historical snapshots;
6. detect recurring spreads;
7. promote candidates to LIVE when thresholds are met;
8. expire candidates when prices/source availability change;
9. alert subscribers when active spreads appear.

## Immediate build target

Create a proof-of-process live board with:

```text
10 spread candidates
```

Each candidate must have:

- marketplace evidence;
- acquisition/source evidence;
- calculated gross spread;
- preliminary net margin estimate;
- live state;
- last checked timestamp;
- risk notes;
- confidence score.

## Key success question

The question is not:

```text
Can we buy and resell this item ourselves?
```

The question is:

```text
Can we reliably identify, refresh, score, and present active spreads that someone else would pay to monitor?
```

That is the digital product.
