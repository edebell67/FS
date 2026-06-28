# EP038 — Spread Inclusion Rules

Created: 2026-06-28T19:18:51

## Mandatory rule

A record can only be included in the live spread board when both sides of the spread are known or defensibly estimated:

```text
source / acquisition price
+ sale price, sold price, or credible guide sale price
= spread candidate
```

If the sale/reference/guide price is unknown, the item is **not a spread**.

It may be stored as:

```text
auction watch candidate
research observation
source-side lead
```

but it must not be counted in:

```text
active spread count
active gross spread value
expiring spread value
subscriber spread alerts
```

## Required fields for board inclusion

A spread-board record requires:

- item/product/asset name;
- source/acquisition price;
- marketplace sale price, sold price, or credible guide sale price;
- spread amount;
- spread percentage;
- freshness timestamp;
- risk/confidence notes.

## Auction-specific rule

For auction products, current bid alone is not enough.

A live auction candidate becomes a spread only when EP038 also has one of:

- observed comparable sale price;
- sold/completed listing comp;
- marketplace guide price;
- credible resale ask range clearly labelled as guide;
- buyer-request price/offer evidence.

Without that, status is:

```text
watch_only_not_spread
```

## Example correction

`namedigital.com` on Sav had auction-side cost observed, but no exact resale/reference price for `namedigital.com` was visible.

Correct treatment:

```text
Keep in live_auction_observations.csv
Remove from live_spread_board.csv
Do not count as spread value
```

## Product implication

EP038 sells spread information. To maintain trust, the board must only show spread candidates where a spread can actually be calculated or credibly guided.
