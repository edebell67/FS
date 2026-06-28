# EP038 — Marketplace Arbitrage Research

Created: 2026-06-27

## Objective

EP038 is a marketplace arbitrage research/workflow project.

The goal is to identify products currently selling on marketplaces such as eBay and similar platforms, then find reliable acquisition sources where the same or equivalent product can be bought for up to ~25% less than the active resale market price.

Example product categories:

```text
Priority 1: digital products / digital assets / software / templates / downloadable products / licences / online services
Priority 2: physical products such as trainers / sneakers and other high-demand marketplace goods
```

Digital products should be given **higher priority** than physical products because they may reduce or remove stock handling, postage, delivery delay, sizing/condition mismatch, and return-logistics risk. However, digital products introduce different risks around licensing, resale rights, platform rules, refunds, account access, fraud, and intellectual-property compliance.

## Intended workflow

The desired commercial loop is:

```text
1. Identify high-selling marketplace items.
2. Track current sale/listing prices and historical sale-price movement.
3. Build a database of products with strong resale demand.
4. Build and maintain a list of lower-cost acquisition sources for each product.
5. When marketplace price spikes or demand is strong, list/sell the item.
6. If sold, simultaneously buy from the lower-cost source for delivery/fulfilment.
```

## Key datasets to build

### 1. Product database

For each candidate product:

- product name;
- brand;
- model/SKU/style code;
- category;
- variants/sizes/colours;
- marketplace listing URLs;
- current observed resale price;
- sold-price history if available;
- sell-through indicators;
- demand indicators;
- digital/physical flag;
- licence/resale rights status for digital products;
- delivery/fulfilment method;
- refund/chargeback risk;
- shipping/fees/taxes assumptions;
- target acquisition price;
- estimated gross margin;
- estimated net margin after fees.

### 2. Acquisition source database

For each product/source pair:

- supplier/source name;
- source URL;
- availability;
- price;
- shipping cost/time;
- return policy;
- reliability/risk rating;
- stock status history;
- notes on authenticity/condition.

### 3. Price history database

Track:

- marketplace asking prices;
- sold prices where available;
- price spikes;
- price drops;
- spread between resale marketplace and acquisition source;
- volatility by product/category.

## Main opportunity signal

The target signal is:

```text
marketplace resale price >= acquisition price + required margin buffer
```

Initial margin target:

```text
acquisition source up to 25% cheaper than marketplace sell price
```

But final decision must account for:

- marketplace fees;
- payment fees;
- postage;
- returns/refunds;
- buyer disputes;
- stockouts;
- authenticity risk;
- delivery timing;
- cash-flow timing.

## Important risks / guardrails

This project must avoid assuming profit from headline spread alone.

Key risks:

- eBay/marketplace fees may erase the 25% spread;
- digital resale/licensing rights may not permit resale;
- account, licence-key, template, ebook, course, SaaS-credit, or downloadable-asset resale may breach platform/source terms;
- buyer refunds/chargebacks are especially risky for instantly delivered digital goods;
- fraud and duplicate-delivery disputes;
- intellectual-property/copyright/trademark issues;
- marketplace restrictions on digitally delivered goods;
- supplier/source access changing after sale;
- physical-product buyer returns/refunds;
- counterfeit/authenticity concerns, especially trainers;
- size/variant mismatch;
- delivery delays;
- marketplace policy violations;
- dropshipping restrictions;
- VAT/tax/accounting obligations;
- payment holds;
- competition repricing.

## Research stance

EP038 should initially be treated as a research/data workflow, not immediate live selling.

No live purchases, listings, or marketplace transactions should be made without explicit approval.

## Initial practical aim

Build a small proof-of-process with **digital products first**:

```text
5–10 digital candidate products
+ marketplace observed prices/sold-price indicators
+ 2–3 possible lower-cost acquisition sources each
+ resale/licence/platform-rights check
+ estimated net margin after fees
+ fraud/refund/compliance risk notes
```

Then optionally compare against a smaller physical-product sample such as trainers:

```text
3–5 physical candidate products
+ marketplace observed prices/sold-price indicators
+ 2–3 possible lower-cost acquisition sources each
+ shipping/returns/authenticity notes
+ estimated net margin after fees
```

Then decide whether the arbitrage spread remains attractive after real-world costs, fulfilment risk, licensing rights, and marketplace/platform restrictions.
