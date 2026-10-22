# WF-103 Alert Contract Test

Blocking alert fixture:

```json
{
  "rule_id": "net_return_total",
  "severity": "blocking",
  "publish_allowed": false,
  "expected": "100.00000000",
  "observed": "99.99000000",
  "difference": "0.01000000",
  "run_id": "00000000-0000-4000-8000-000000000103",
  "remediation": "Inspect quarantine and source checksum; replay or backfill only after correction."
}
```

PASS — the alert identifies the rule, observed difference, run lineage and safe recovery path without exposing raw payloads.

