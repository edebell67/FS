# EP038 — Live Auction Proof Requirement

Created: 2026-06-28T16:29:40

## Requirement

EP038 needs at least **one product running in a live scenario**.

That means:

```text
one real product/asset
+ currently active auction marketplace listing
+ real-time/near-real-time monitoring
+ spread sought against lower acquisition/reference sources
+ observations captured into EP038 data
+ displayed on the live board as a real live/research signal
```

## Purpose

The static launch package proves the product shell. The live-auction proof proves the product engine.

The goal is to demonstrate that EP038 can:

- identify an active auction listing;
- track current bid/price and closing time;
- compare against a lower acquisition/reference source;
- calculate observed gross spread;
- track hours to expiry;
- capture observations into history;
- update the board with real data;
- keep clear information-only guardrails.

## Preferred first scenario

Use one accessible auction market with visible closing time and price/bid data.

Candidate types:

```text
eBay UK auction item
GoDaddy domain auction / closeout
Catawiki auction item
John Pye / i-bidder auction item
```

## Minimum live proof outputs

Create:

```text
data/live_auction_watch.csv
data/live_auction_observations.csv
scripts/live_auction_watch_once.py
spikes/004-live-auction-proof/README.md
```

Update:

```text
data/live_spread_board.csv
site_launch/data/spreads.json
site_launch/live-spreads.html via renderer/export
```

## Guardrails

No bidding, buying, listing, contacting sellers/buyers, or transaction action without explicit approval.

This proof is research/information only.

## Success definition

The proof succeeds when one live auction product has at least one captured observation with:

- product/listing name;
- marketplace URL;
- current auction price/bid;
- auction close/expiry time or hours remaining;
- candidate source/reference price;
- observed gross spread amount/percent where calculable;
- risk/confidence notes;
- board entry updated as `LIVE` or `WATCHING`.
