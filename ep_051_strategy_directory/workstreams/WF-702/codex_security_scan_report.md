# Security Review: ep_051_strategy_directory

## Scope

Static audit of EP051 implementation artifacts.

- Scan mode: repository
- Target kind: git_worktree
- Target ID: target_sha256_5902216066ca177e9fab86541d643291178bfe2557eada039704cf76f65f9e8e
- Revision: 59dcffb3bf421e6905d1b5b5289d3251189bb853
- Snapshot digest: codex-security-snapshot/v1:sha256:3ca9fe9799bebd2333cfffe32a3ff60e355696bcf88e229c65b8ac1523b5a0d1
- Inventory strategy: repository
- Included paths: .
- Excluded paths: none
- Runtime or test status: not deployed
- Artifacts reviewed: Python source/tests, HTML prototypes, SQL/API/security contracts

Limitations and exclusions:
- Static/offline review; no deployed service or live broker exists.
- Generated binaries and caches were excluded.
- Excluded \*\*/\*.png: Binary screenshots
- Excluded \*\*/__pycache__/\*\*: Generated cache

### Scan Summary

| Field | Value |
| --- | --- |
| Reportable findings | 4 |
| Severity mix | high: 2, medium: 2 |
| Confidence mix | high: 4 |
| Coverage | partial |
| Validation mode | source-backed static review |

Canonical artifacts: `scan-manifest.json`, `findings.json`, and `coverage.json`. This report is a deterministic projection of those files.

## Threat Model

Public inputs may be attacker controlled; protect private trading data, credentials, analytics, evidence, and offline broker boundaries.

### Assets

- private trading data
- credentials
- governed analytics
- audit evidence

### Trust Boundaries

- browser to API
- warehouse to read model
- sandbox to future adapter

### Attacker Capabilities

- control public inputs
- ordinary authenticated role

### Security Objectives

- prevent disclosure
- bound computation
- fail closed
- preserve audit integrity

### Assumptions

- Broker adapter is offline-only.

## Findings

| Finding | Severity | Confidence | Detailed write-up |
| --- | --- | --- | --- |
| [Authenticated users can retrieve every open-trade row without ownership filtering](#finding-1) | high | high | inline below |
| [Unbounded combinatorial portfolio search permits computational denial of service](#finding-2) | high | high | inline below |
| [Survivorship gate compares timestamps lexicographically and can approve invalid runs](#finding-3) | medium | high | inline below |
| [Non-finite numeric values fail open across sandbox order and risk controls](#finding-4) | medium | high | inline below |

### Confidence Scale

| Label | Meaning |
| --- | --- |
| high | Direct evidence supports the finding with no material unresolved blocker. |
| medium | Evidence supports a plausible issue, but material runtime or reachability proof remains. |
| low | Evidence is incomplete and the item is retained only for explicit follow-up. |

<a id="finding-1"></a>

### [1] Authenticated users can retrieve every open-trade row without ownership filtering

| Field | Value |
| --- | --- |
| Severity | high |
| Confidence | high |
| Confidence rationale | Direct source-backed dataflow validated independently. |
| Category | broken-access-control |
| CWE | CWE-862 |
| Affected lines | workstreams/WF-204/read_models.py:20-22 |

#### Summary

Ordinary authenticated users can receive unrestricted open-trade rows without owner/tenant filtering or field allowlisting.

#### Root Cause

Ordinary authenticated users can receive unrestricted open-trade rows without owner/tenant filtering or field allowlisting.

#### Validation

Validated against referenced source and counterevidence.

#### Dataflow

Ordinary authenticated users can receive unrestricted open-trade rows without owner/tenant filtering or field allowlisting.

#### Reachability

Documented future API or safety contract makes this path relevant.

#### Severity

**High** — Ordinary authenticated users can receive unrestricted open-trade rows without owner/tenant filtering or field allowlisting.

Additional runtime or deployment evidence could raise or lower this severity.

#### Remediation

Use trusted principal, owner filters, field allowlist, scoped roles, and cross-tenant tests.

<a id="finding-2"></a>

### [2] Unbounded combinatorial portfolio search permits computational denial of service

| Field | Value |
| --- | --- |
| Severity | high |
| Confidence | high |
| Confidence rationale | Direct source-backed dataflow validated independently. |
| Category | denial-of-service |
| CWE | CWE-400 |
| Affected lines | workstreams/WF-502/engine.py:74-88 |

#### Summary

The optimizer enumerates and retains every eligible combination for caller-controlled portfolio sizes.

#### Root Cause

The optimizer enumerates and retains every eligible combination for caller-controlled portfolio sizes.

#### Validation

Validated against referenced source and counterevidence.

#### Dataflow

The optimizer enumerates and retains every eligible combination for caller-controlled portfolio sizes.

#### Reachability

Documented future API or safety contract makes this path relevant.

#### Severity

**High** — The optimizer enumerates and retains every eligible combination for caller-controlled portfolio sizes.

Additional runtime or deployment evidence could raise or lower this severity.

#### Remediation

Enforce search budgets, track only best result, and add timeouts/rate limits and adversarial tests.

<a id="finding-3"></a>

### [3] Survivorship gate compares timestamps lexicographically and can approve invalid runs

| Field | Value |
| --- | --- |
| Severity | medium |
| Confidence | high |
| Confidence rationale | Direct source-backed dataflow validated independently. |
| Category | input-validation |
| CWE | CWE-697 |
| Affected lines | workstreams/WF-503/validation.py:8-13 |

#### Summary

Mixed-offset universe and training timestamps are compared as strings, allowing chronological inversion.

#### Root Cause

Mixed-offset universe and training timestamps are compared as strings, allowing chronological inversion.

#### Validation

Validated against referenced source and counterevidence.

#### Dataflow

Mixed-offset universe and training timestamps are compared as strings, allowing chronological inversion.

#### Reachability

Documented future API or safety contract makes this path relevant.

#### Severity

**Medium** — Mixed-offset universe and training timestamps are compared as strings, allowing chronological inversion.

Additional runtime or deployment evidence could raise or lower this severity.

#### Remediation

Parse all timestamps as aware datetimes, normalize UTC, and test offsets.

<a id="finding-4"></a>

### [4] Non-finite numeric values fail open across sandbox order and risk controls

| Field | Value |
| --- | --- |
| Severity | medium |
| Confidence | high |
| Confidence rationale | Direct source-backed dataflow validated independently. |
| Category | input-validation |
| CWE | CWE-754 |
| Affected lines | workstreams/WF-602/risk_gates.py:24-36 |

#### Summary

NaN and infinity are not rejected before safety comparisons, allowing malformed sandbox audit state.

#### Root Cause

NaN and infinity are not rejected before safety comparisons, allowing malformed sandbox audit state.

#### Validation

Validated against referenced source and counterevidence.

#### Dataflow

NaN and infinity are not rejected before safety comparisons, allowing malformed sandbox audit state.

#### Reachability

Documented future API or safety contract makes this path relevant.

#### Severity

**Medium** — NaN and infinity are not rejected before safety comparisons, allowing malformed sandbox audit state.

Additional runtime or deployment evidence could raise or lower this severity.

#### Remediation

Require finite real numbers and valid ranges throughout adapter, gates, and reconciler.

## Reviewed Surfaces

| Surface | Risk Area | Outcome | Notes |
| --- | --- | --- | --- |
| Browser UI and DOM sinks | not recorded | No issue found | No additional canonical notes were recorded. |
| Read models and ingestion | not recorded | Reported | No additional canonical notes were recorded. |
| Portfolio optimizer and validation | not recorded | Reported | No additional canonical notes were recorded. |
| Offline adapter and risk controls | not recorded | Reported | No additional canonical notes were recorded. |
| SQL/API/governance contracts | not recorded | No issue found | No additional canonical notes were recorded. |

## Open Questions And Follow Up

- Define saved-run route ownership when implemented.
- They do not exist yet.
  - Follow-up prompt: Review deferred unit deferred-3283d925a78561e0 and close its stated proof gap.
