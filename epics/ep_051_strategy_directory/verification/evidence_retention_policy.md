# EP051 Evidence Retention Policy

Version 1.0.0 — 2026-08-23

- Retain unit, integration, browser, security, data-quality, migration and rollback evidence for every release candidate.
- Bind each evidence bundle to source revision, release/snapshot ID, UTC execution time, environment, command/tool version and result.
- Keep successful public-release evidence for 24 months and failed/rejected release evidence for 12 months; security and incident evidence follows the longer applicable legal or incident requirement.
- Store evidence immutably with integrity hashes and least-privilege read access. Never retain secrets, raw credentials, private account identifiers, or unrestricted trade payloads.
- Operators may append a superseding result but must not rewrite the original. Expiry is logged and legal/security holds override deletion.
- `verification/ci_quality_report.json` is the portable machine-readable gate result. Public promotion also requires the external beta, deployed SLO/load/data-quality and rollback evidence explicitly identified by WF-703/WF-704; CI success alone does not authorize launch.
