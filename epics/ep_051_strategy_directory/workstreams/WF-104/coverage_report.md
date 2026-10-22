# WF-104 Coverage Report

Fixture coverage: 3 observations; 2 fully known; 1 explicitly `UNKNOWN`; known coverage 66.67%.

Quality interpretation:

- `UNKNOWN` is an honest state and is excluded from performance claims, not treated as zero or carried forward.
- Coverage is reported by instrument, interval and definition version.
- A production threshold is not asserted by this foundation node; WF401 must apply governed sufficiency thresholds before regime analytics are published.

No-look-ahead check: PASS — observations with `available_at` later than the event timestamp cannot join.

