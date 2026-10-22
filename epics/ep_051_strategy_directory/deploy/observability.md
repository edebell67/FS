# EP051 Observability Baseline

Version 1.0.0 — 2026-08-23

## Signals

- `/healthz` proves the process can answer; it does not assert dependency health.
- `/readyz` verifies the manifest, directory artifact, and the approved broker-disabled posture. Failed readiness returns HTTP 503.
- Structured service events must include UTC timestamp, environment, release/snapshot, request ID, route, status and latency; secrets, account identifiers and trade payloads are prohibited.
- Minimum metrics: request count/error ratio, p50/p95/p99 latency, readiness state, cache age, ingestion lag, data-quality rejects and reconciliation mismatches.

## Alert and ownership contract

| Condition | Threshold | Response |
|---|---|---|
| Readiness failure | 2 consecutive probes | Page operator; remove instance from traffic |
| HTTP 5xx | >1% for 5 minutes | Page operator; inspect release and dependencies |
| Closed snapshot age | >24 hours | Block freshness badge and investigate pipeline |
| Open state age | >5 seconds | Mark stale; never present as current |
| DQ/reconciliation gate | any release-blocking failure | Stop promotion and preserve evidence |

Dashboards segment by environment and release. Evidence retention follows `verification/evidence_retention_policy.md` once INF-007 is installed. Public launch remains a separate, evidence-gated decision; this baseline does not deploy or authorize production.
