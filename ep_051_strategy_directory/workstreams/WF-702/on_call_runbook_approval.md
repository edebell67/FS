# WF-702 On-call and Incident Runbook Approval

## Version history

- 1.0.0 (2026-08-23): Initial ownership and SLA approval.

| Severity | Example | Acknowledge | Owner | Immediate action |
|---|---|---:|---|---|
| P1 | credential/private-data exposure; integrity loss | 15 min | Security lead + platform on-call | Disable affected public route, preserve evidence, rotate/revoke where relevant, notify incident commander. |
| P2 | stale analytics, failed publish, restore required | 30 min | Data/platform on-call | Freeze publish, serve last known-good snapshot with warning, reconcile and restore. |
| P3 | degraded search/UI or delayed noncritical job | 4 hours | Product engineering | Triage, communicate status and schedule correction. |

Runbooks cover public/private leak, metric integrity, stale snapshot, cache/index failure, portfolio abuse, sandbox drift and kill control. Each incident records commander, timeline, scope, evidence links, user impact, containment, recovery, root cause and follow-up owner/date. Broker-specific paging is inactive because live integration is deferred; sandbox alerts remain local test evidence.

Approval: operationally ready for private beta after WF-703 entry review. Public launch still requires infrastructure monitoring/backup/rollback and WF-704.

