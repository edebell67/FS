# EP038 — Subscriber Preference Alerts

Created: 2026-06-27

## Core idea

Subscribers should be notified when preferred spread types become available.

The product is not just a board users manually check. It becomes a personalised spread-intelligence feed.

```text
User sets preferences
→ EP038 monitors spread board
→ matching spreads trigger notifications
```

## Subscriber preferences

Subscribers should be able to select:

- categories;
- marketplaces;
- source types;
- minimum gross spread percentage;
- minimum gross spread value;
- maximum risk level;
- minimum confidence score;
- expiry/time-pressure preference;
- geography/currency;
- physical vs digital;
- notification channel;
- notification frequency.

## Example preferences

```text
Category: trainers
Marketplaces: eBay UK, Vinted, StockX
Minimum gross spread: 25%
Minimum gross value: £20
Risk: medium or lower
Expiry: notify if within 24h
Channel: email/Telegram
Frequency: instant + daily digest
```

Domain investor example:

```text
Category: domains
Marketplaces: GoDaddy Auctions, Sedo, ExpiredDomains
Minimum estimated spread: £100
Exclude trademark risk
Notify if auction closes within 12h
```

## Alert triggers

Alerts should fire when:

- a new matching spread is discovered;
- a watched spread becomes LIVE;
- spread value crosses a subscriber threshold;
- source price drops;
- marketplace price spikes;
- auction/offer expires within subscriber window;
- expired spread reappears;
- confidence score improves;
- risk decreases after validation.

## Notification types

### Instant alert

For time-sensitive/high-value matches.

Example:

```text
New trainer spread: £31 gross spread, 25.8%, auction closes in 6h.
Verify stock/fees before acting.
```

### Daily digest

For lower-urgency matches.

Example:

```text
Today: 12 matching spread candidates, £640 gross spread value, £210 expiring within 24h.
```

### Weekly category summary

For product marketing / retention.

Example:

```text
This week in trainer spreads: 48 candidates identified, £2,840 gross spread value, 17 expired within 24h.
```

## Subscriber-facing wording

Use:

```text
Get notified when spreads matching your criteria appear.
```

```text
Choose your categories, spread threshold and urgency window.
```

```text
Receive candidate spread alerts with confidence and risk notes.
```

Avoid:

```text
We tell you exactly what to buy.
Guaranteed profitable alerts.
Instant profit signals.
```

## Required data model

Create later:

```text
data/subscriber_preferences.csv
data/alert_events.csv
```

### subscriber_preferences.csv fields

- subscriber_id;
- status;
- email_or_channel;
- category_filters;
- marketplace_filters;
- min_gross_spread_pct;
- min_gross_spread_value;
- min_confidence_score;
- max_risk_score;
- time_sensitive_only;
- expiry_window_hours;
- frequency;
- created_at;
- updated_at;
- notes.

### alert_events.csv fields

- alert_id;
- subscriber_id;
- spread_id;
- trigger_type;
- triggered_at;
- delivery_channel;
- delivery_status;
- message_summary;
- user_clicked;
- notes.

## MVP approach

Do not build full accounts first.

Start with:

```text
email/waitlist form
+ preference fields
+ manual/semi-automated matching
+ daily digest
```

Then add instant alerts if demand is proven.

## Product implication

Subscriber preferences turn EP038 from:

```text
static board
```

into:

```text
personalised spread availability alert service
```

The sales promise becomes:

```text
Tell us what spreads you care about. We notify you when matching opportunities appear or are about to expire.
```

## Guardrail

Every alert must include:

```text
Research information only. Verify price, stock, fees, delivery, authenticity, rights and platform rules before acting. No profit is guaranteed.
```
