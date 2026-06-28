# EP038 — Time-Sensitive Spread Metrics

Created: 2026-06-27

## Core idea

Some spreads are time-sensitive, especially where one side of the spread is an auction, closeout, flash sale, limited stock, or high-turnover listing.

EP038 should publish not only:

```text
Total gross spread value identified
Total spread count identified
```

but also:

```text
Gross spread value subject to expiry
Count of time-sensitive spreads
Next expiry / auction close time
```

## Why this matters

A spread may exist only until:

- an auction closes;
- a source sale ends;
- stock sells out;
- a marketplace ask/listing changes;
- a buyer-request is fulfilled;
- a domain auction/closeout window ends.

Showing the amount of spread value under time pressure makes the live board more compelling.

Example public metric:

```text
£1,240 gross spread value identified — £420 expires within 24h.
```

This creates urgency while staying honest.

## Required metrics

The site should calculate and display:

- active gross spread value;
- active spread count;
- time-sensitive gross spread value;
- time-sensitive spread count;
- expiring within 1h;
- expiring within 6h;
- expiring within 24h;
- next expiry timestamp;
- earliest auction close;
- expired spread value lost/closed today later.

## Required fields

Add these to the live spread board schema:

```text
time_sensitive
expiry_type
expiry_at
hours_to_expiry
expiry_value_status
urgency_level
```

### Field meanings

`time_sensitive`:

```text
yes/no
```

`expiry_type` examples:

```text
auction_close
source_sale_end
stock_limited
buyer_request_window
domain_closeout
listing_turnover_risk
unknown
```

`expiry_at`:

```text
ISO timestamp if known
```

`hours_to_expiry`:

```text
numeric if known
```

`expiry_value_status`:

```text
active
expiring_soon
expired
unknown
```

`urgency_level`:

```text
low
medium
high
critical
```

## Website wording

Use:

```text
£X spread value expiring within 24h
Auction closes in Xh
Source offer ends soon
Time-sensitive spread
```

Avoid:

```text
must buy now
guaranteed profit if you act fast
risk-free urgent trade
```

## Product implication

Time-sensitive spread value becomes a key conversion lever:

```text
Here is the value of spreads currently visible.
Here is the value that may disappear soon.
```

This supports urgency without misleading users.

## Guardrail

Urgency must always be paired with verification wording:

```text
Verify price, stock, fees, delivery, authenticity and platform rules before acting.
```
