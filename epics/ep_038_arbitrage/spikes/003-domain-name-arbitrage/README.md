# Spike 003 — Domain name arbitrage

## Question

Given EP038 is digital-first, can domain names provide a viable arbitrage workflow where acquisition cost is materially lower than observed marketplace resale value?

## Why domains first

Domains are prioritised because eBay UK explicitly lists domain names as an exception under its electronically delivered items policy, and domain ownership transfer is a more established digital transfer model than software keys, accounts, or unauthorised download products.

## Candidate requirements

A domain candidate must have:

```text
clear acquisition source
+ clear transfer path
+ no obvious trademark conflict
+ marketplace/listing/sold-price evidence
+ estimated net spread after renewal/transfer/marketplace fees
```

## Data files

- `data/domain_candidates.csv` — candidate opportunity tracker.
- `data/domain_source_checks.csv` — source-access and usefulness log.
- `data/domain_comps.csv` — observed listing/sold-price comps.

## First source targets

Marketplace/sale evidence:

- eBay domain-name listings/sold listings where accessible;
- GoDaddy Auctions / aftermarket;
- Sedo;
- Dan/Atom where accessible;
- NameBio for historical domain sale comps if accessible.

Acquisition sources:

- expired-domain lists;
- registrar closeouts;
- hand-registration availability via registrar search;
- direct owner/outreach only later, not in this spike.

## Rejection rules

Reject if:

- trademark brand term appears in the domain;
- no realistic buyer/use-case is obvious;
- domain is long, hyphen-heavy, or spammy;
- no comparable pricing evidence exists;
- acquisition cannot be verified;
- margin disappears after renewal/transfer/fees.

## Current status

Initial artefacts created. Public source checks and candidates to follow.


## Source check results — 2026-06-27

See `data/domain_source_checks.csv`.

Summary:

- eBay search: blocked/error in this browser session.
- Sedo search: accessible enough to show keyword-specific featured domains, but prices were not captured in the initial snapshot.
- NameBio: blocked by captcha, but likely valuable for historical sold comps if accessed manually.
- ExpiredDomains.net deleted `.com`: accessible partial list; keyword search/filtering requires free login.

## Initial process-test candidates

See `data/domain_candidates.csv`.

Seeded six deleted `.com` names from the visible ExpiredDomains table, marked `research_only`.

Important: these are not buy recommendations. They are workflow test records. Each still needs:

- availability verification at registrar;
- acquisition cost check;
- trademark check;
- comparable sale/listing evidence;
- margin calculation;
- liquidity assessment.

## Interim verdict: PARTIAL

The domain workflow is feasible as a research process, but live opportunity detection needs better source access:

1. ExpiredDomains free account for keyword filters and richer metrics.
2. NameBio or equivalent for sold-price comps.
3. A registrar availability/price check source.
4. Marketplace access for current ask prices.

Without those, we can build the database structure and process, but should not claim validated arbitrage opportunities.
