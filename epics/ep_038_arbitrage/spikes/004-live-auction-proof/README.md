# EP038 Spike 004 — Live Auction Product Proof

Created: 2026-06-28T17:02:55

## Selected live product

```text
namedigital.com
```

## Auction marketplace

```text
Sav domain auctions
https://v2.sav.com/domains/auctions
```

## Captured auction observation

| Field | Value |
|---|---:|
| Current bid | $355.00 |
| Auction fee | $9.65 |
| Total current cost | $364.65 |
| Bidders | 5 |
| Bids | 14 |
| Time left observed | 1h 33m |
| End date | 2026-06-28 |

## Reference/spread check

Sedo public search endpoint was queried for `namedigital`.

Returned related domains:

```text
namedigital.co.uk
namedigital.com.br
```

No exact public resale/reference price for `namedigital.com` was visible in the captured response.

Therefore status is:

```text
spread sought, not yet quantified
```

This is intentionally honest: the auction product is live and monitored, but EP038 should not invent a gross spread value when the reference side is not confirmed.

## Outputs

```text
data/live_auction_watch.csv
data/live_auction_observations.csv
scripts/live_auction_watch_once.py
```

## Guardrail

No bid, buy, listing, contact, or transaction occurred.

This is research/information capture only.
