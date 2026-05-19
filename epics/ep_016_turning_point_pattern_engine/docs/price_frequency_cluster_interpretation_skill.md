# Skill: Price Frequency Cluster Interpretation

## Purpose

Interpret bid/ask price-frequency cluster history to determine short-term market state and likely directional bias.

This skill is designed for real-time trading dashboards, trading assistants, or automated market-state classifiers using repeated price-frequency snapshots.

The core idea is simple:

> Direction is not confirmed by a single price touch.  
> Direction is confirmed when the frequency centre migrates and then rebuilds at the new zone.

---

## Input Format

The input should contain bid and ask cluster history over multiple time snapshots.

Example structure:

```text
[GBP]

BID Cluster History:
  Price    | 03:35 | 03:40 | 03:45 | 03:50 | 03:55 | 04:00
  -------------------------------------------------------------
  1.3015 |  -  |  56 |  67 |  31 |  -  |  -  |
  1.3014 |  -  |  38 |  25 |  68 |   1 |  -  |
  1.3013 |  -  |   1 |  13 |  53 |  13 |  -  |
  1.3012 |  -  |  -  |  15 |  31 |  24 |   4 |
  1.3011 |  -  |  -  |   4 |  34 |  63 |  15 |
  1.3010 |  -  |  -  |   3 |  39 |  46 |  10 |
  1.3009 |  -  |  -  |   2 |  14 |  49 |  11 |

ASK Cluster History:
  Price    | 03:35 | 03:40 | 03:45 | 03:50 | 03:55 | 04:00
  -------------------------------------------------------------
  1.3016 |  -  |  56 |  67 |  31 |  -  |  -  |
  1.3015 |  -  |  38 |  25 |  67 |   1 |  -  |
  1.3014 |  -  |   1 |  13 |  54 |  13 |  -  |
  1.3013 |  -  |  -  |  15 |  31 |  24 |   4 |
  1.3012 |  -  |  -  |   4 |  34 |  63 |  15 |
  1.3011 |  -  |  -  |   3 |  39 |  46 |  10 |
  1.3010 |  -  |  -  |   2 |  14 |  49 |  11 |
```

---

## Core Concepts

### 1. Accepted Zone

The accepted zone is the price area where frequency is highest or most concentrated during a snapshot.

Use the bid cluster primarily for directional read. Use ask cluster as confirmation.

Example:

```text
Bid:
1.3015: 67
1.3016: 71
1.3017: 48
```

Accepted zone:

```text
1.3015–1.3017
```

---

### 2. Frequency Magnet

The frequency magnet is the highest-frequency price level within the current snapshot.

Example:

```text
1.3016: 71
```

Interpretation:

```text
Current magnet = 1.3016 bid / 1.3017 ask
```

---

### 3. Cluster Migration

Cluster migration occurs when the accepted zone shifts from one price area to another across snapshots.

Example:

```text
03:35: 1.3020–1.3022
03:40: 1.3015–1.3018
03:50: 1.3010–1.3014
03:55: 1.3006–1.3011
```

Interpretation:

```text
Sustained downward migration.
Likely direction = down.
```

---

### 4. Failed Probe

A failed probe occurs when price frequency appears briefly at new higher or lower levels but does not rebuild there in the next snapshot.

Example:

```text
03:30:
1.3026: 63
1.3027: 49
1.3028: 17

03:35:
1.3026: -
1.3027: -
1.3028: -
```

Interpretation:

```text
Upper probe failed.
Bullish continuation has weakened or failed.
Watch for pullback.
```

---

### 5. Lower Acceptance

Lower acceptance occurs when the frequency centre moves lower and then builds meaningful frequency at the lower zone.

Example:

```text
03:45:
1.3015: 67
1.3016: 71

03:50:
1.3010: 39
1.3011: 34
1.3013: 53
1.3014: 68
```

Interpretation:

```text
Market has repriced lower.
Bias remains bearish.
```

---

### 6. Upper Acceptance

Upper acceptance occurs when the frequency centre moves higher and then builds meaningful frequency at the higher zone.

Example:

```text
03:20:
1.3010–1.3012

03:25:
1.3019–1.3021

03:30:
1.3024–1.3027
```

Interpretation:

```text
Market is accepting higher prices.
Bias is bullish.
```

---

### 7. Stall / Pause

A stall occurs when a previous high-frequency zone collapses and no clear new high-frequency zone has formed.

Example:

```text
03:50:
1.3014: 68
1.3013: 53
1.3010: 39

03:55:
1.3013: 5
1.3012: 4
```

Interpretation:

```text
Bearish move has stalled.
Do not assume continuation until new lower frequency builds.
```

---

## Directional Logic

### Bullish Continuation

Classify as bullish continuation when:

```text
1. Prior accepted zone was lower.
2. New frequency appears above the prior zone.
3. Frequency then builds at the higher zone.
4. Lower prices disappear or lose relevance.
```

Example output:

```text
Direction: Up
State: bullish continuation / higher acceptance
Current magnet: [price]
Continuation trigger: frequency builds above [upper level]
Failure trigger: frequency drops back below [prior accepted zone]
```

---

### Bearish Continuation

Classify as bearish continuation when:

```text
1. Prior accepted zone was higher.
2. New frequency appears below the prior zone.
3. Frequency then builds at the lower zone.
4. Higher prices disappear or lose relevance.
```

Example output:

```text
Direction: Down
State: bearish continuation / lower acceptance
Current magnet: [price]
Continuation trigger: frequency builds below [lower level]
Recovery trigger: frequency rebuilds above [prior accepted zone]
```

---

### Pullback

Classify as pullback when:

```text
1. Price previously migrated strongly in one direction.
2. Frequency then shifts against that move.
3. The new opposing cluster is meaningful but has not invalidated the broader structure.
```

Example:

```text
03:30: 1.3024–1.3027
03:35: 1.3020–1.3022
```

Interpretation:

```text
Bearish pullback within larger rebound.
Not full bearish reversal unless lower zones continue building.
```

---

### Failed Breakout

Classify as failed breakout when:

```text
1. Frequency appears above the prior accepted zone.
2. It does not build further.
3. The next snapshot loses the upper levels.
4. Frequency rotates back into or below the prior zone.
```

Example output:

```text
State: failed upside probe
Bias: neutral to bearish
Watch: rebuild above failed level to restore bullish bias
```

---

### Failed Breakdown

Classify as failed breakdown when:

```text
1. Frequency appears below the prior accepted zone.
2. It does not build further.
3. The next snapshot loses the lower levels.
4. Frequency rotates back into or above the prior zone.
```

Example output:

```text
State: failed downside probe
Bias: neutral to bullish
Watch: rebuild below failed level to restore bearish bias
```

---

### Lower Consolidation

Classify as lower consolidation when:

```text
1. Market has already migrated lower.
2. Current frequency is broad across a lower band.
3. Peak frequency is not at the lowest price.
4. No fresh lower acceptance has formed yet.
```

Example:

```text
1.3014: 68
1.3013: 53
1.3012: 31
1.3011: 34
1.3010: 39
```

Output:

```text
State: lower consolidation / bearish range
Bias: down compared with prior zone
Continuation only confirmed below lower edge
Recovery only confirmed above upper edge
```

---

### Upper Consolidation

Classify as upper consolidation when:

```text
1. Market has already migrated higher.
2. Current frequency is broad across a higher band.
3. Peak frequency is not at the highest price.
4. No fresh higher acceptance has formed yet.
```

Output:

```text
State: upper consolidation / bullish range
Bias: up compared with prior zone
Continuation only confirmed above upper edge
Failure only confirmed below lower edge
```

---

## State Labels

Use one of the following state labels:

```text
UPWARD_ACCEPTANCE
DOWNWARD_ACCEPTANCE
BULLISH_CONTINUATION
BEARISH_CONTINUATION
PULLBACK
STALLING
FAILED_BREAKOUT
FAILED_BREAKDOWN
LOWER_CONSOLIDATION
UPPER_CONSOLIDATION
NEUTRAL_BALANCE
THIN_PROBE
```

---

## Output Template

Use this structure for every interpretation:

```text
Direction: [Up / Down / Neutral / Unclear]

State: [state label in plain English]

Current magnet:
Bid: [price or range]
Ask: [price or range]

What changed:
[Explain how the accepted zone moved from prior snapshot to current snapshot.]

Interpretation:
[Explain whether this is acceptance, continuation, pullback, stall, failed probe, or consolidation.]

Continuation trigger:
[Price level/range where frequency must build to confirm further movement.]

Failure/reversal trigger:
[Price level/range where frequency must rebuild to invalidate the current read.]

Bottom line:
[One direct conclusion in plain language.]
```

---

## Example Output

```text
Direction: Down

State: bearish continuation / lower acceptance

Current magnet:
Bid: 1.3013–1.3014
Ask: 1.3014–1.3015

What changed:
The market moved from prior acceptance around 1.3015–1.3017 into a broader lower zone around 1.3010–1.3014.

Interpretation:
The market has repriced lower, but the strongest frequency is not at the absolute low. That means bearish pressure remains active, but the latest snapshot is more lower consolidation than fresh acceleration.

Continuation trigger:
Frequency builds below 1.3010 / 1.3009.

Failure/reversal trigger:
Frequency rebuilds above 1.3015 / 1.3016.

Bottom line:
Bias remains down, but another leg lower needs fresh acceptance below 1.3010.
```

---

## Automation Rules

### Rule 1: Do Not Overweight Single Prints

Low-frequency isolated prints should be treated as probes, not direction.

Example:

```text
1.3009: 2
```

Do not classify this alone as bearish continuation.

---

### Rule 2: Confirm Direction With Rebuild

A directional move requires frequency to rebuild at the new zone.

```text
Touch = weak signal
Build = confirmation
Repeated build = strong confirmation
```

---

### Rule 3: Compare Current Magnet To Previous Magnet

If the current magnet is above the previous magnet:

```text
Bias = upward rotation
```

If the current magnet is below the previous magnet:

```text
Bias = downward rotation
```

If the current magnet is close to the previous magnet:

```text
Bias = consolidation / balance
```

---

### Rule 4: Watch Edge Acceptance

For any cluster, identify:

```text
Upper edge = highest meaningful frequency area
Lower edge = lowest meaningful frequency area
```

Continuation requires frequency to build beyond the relevant edge.

---

### Rule 5: Treat Vanishing Frequency As Information

If a previous high-frequency zone disappears, that zone has likely been rejected or abandoned.

Example:

```text
03:30:
1.3026: 63

03:35:
1.3026: -
```

Interpretation:

```text
Upper acceptance failed.
```

---

### Rule 6: Thin Snapshots Require Caution

If total frequency in the latest snapshot is very low compared with previous snapshots, classify the read as lower conviction.

Example wording:

```text
The direction is still down-biased, but the latest snapshot is thin, so watch for snapback.
```

---

## Confidence Scoring

Assign confidence as follows:

### High Confidence

```text
- Clear migration across at least 2 snapshots
- Frequency builds meaningfully at new zone
- Prior zone disappears
```

### Medium Confidence

```text
- Clear movement into new zone
- Some frequency build
- Prior zone partly remains
```

### Low Confidence

```text
- Thin frequency
- Isolated prints only
- No clear accepted zone
```

---

## Recommended Dashboard Fields

```json
{
  "product": "GBP",
  "latest_time": "04:00",
  "direction": "DOWN",
  "state": "LOWER_CONSOLIDATION",
  "current_bid_magnet": "1.3011",
  "current_ask_magnet": "1.3012",
  "accepted_zone_bid": "1.3008-1.3012",
  "accepted_zone_ask": "1.3009-1.3013",
  "continuation_trigger": "frequency builds below 1.3008",
  "recovery_trigger": "frequency rebuilds above 1.3013",
  "confidence": "MEDIUM",
  "summary": "GBP remains down-biased, but latest frequency shows slowing pressure at the lower zone."
}
```

---

## Key Principle

Always interpret the sequence, not the isolated row.

The useful pattern is:

```text
Higher cluster rejected
→ frequency shifts lower
→ lower zone accepts
→ next lower zone tested
```

or:

```text
Lower cluster rejected
→ frequency shifts higher
→ higher zone accepts
→ next higher zone tested
```

The model should prioritise:

```text
1. Cluster migration
2. Frequency rebuild
3. Failed probes
4. Vanishing prior zones
5. Edge acceptance
6. Thin-snapshot caution
```
