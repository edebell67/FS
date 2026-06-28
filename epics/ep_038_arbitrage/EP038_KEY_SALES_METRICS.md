# EP038 — Key Sales Metrics: Spread Value and Count

Created: 2026-06-27

## Core sales item

When EP038 identifies pricing spreads, the website must continuously publish and update two headline metrics:

```text
Total value of spreads identified
Total count of spreads identified
```

These become the key proof/sales items for the information product.

## Why this matters

The customer is buying access to pricing-spread information. The clearest proof of value is:

```text
How many spreads are being found?
How much gross spread value is being observed?
How fresh is the board?
How many are currently live vs expired/avoid?
```

## Required public metrics

The live website should display:

- total active spread count;
- total active gross spread value;
- total all-time identified spread count;
- total all-time gross spread value identified;
- count by state: DISCOVERED / WATCHING / LIVE / COOLING / EXPIRED / AVOID;
- last updated timestamp;
- optional average spread percentage;
- optional estimated net margin range total, once fee modelling improves.

## Calculation rules

### Active spread count

Count spreads with state:

```text
DISCOVERED
WATCHING
LIVE
COOLING
```

Exclude from active count:

```text
EXPIRED
AVOID
```

### Active gross spread value

Sum `gross_spread_amount` for active spreads where numeric.

Formula:

```text
marketplace_price - source_price = gross_spread_amount
```

Only include records where both prices are numeric and current enough.

### All-time identified count

Count all spread records except optionally deleted/test records.

### All-time identified gross spread value

Sum numeric gross spread amounts across all discovered records, including expired spreads, but keep it labelled as historical/all-time identified value.

## Critical wording guardrail

Do not label spread value as profit.

Use:

```text
Gross spread value identified
Observed gross spread value
Potential spread value before fees/risk
```

Avoid:

```text
profit found
guaranteed value
money you can make
```

## Website positioning

Hero proof block should say something like:

```text
£X gross spread value identified across Y spread candidates.
```

Supporting note:

```text
Before fees, stock, delivery, rights, authenticity and platform checks.
```

## Product implication

The website should make the ongoing discovery engine visible:

```text
Today we identified X spread candidates worth £Y gross spread value.
This week we identified X spread candidates worth £Y gross spread value.
Currently live: X candidates worth £Y gross spread value.
```

This turns EP038 from a static board into a measurable information feed.
