# Traceability Matrix - EP051 DNA Strategy Directory

| Req ID | Description | Phase | Owner | Workflow Node | Implementation / Schema | Test / Validation |
|--------|-------------|-------|-------|---------------|-------------------------|-------------------|
| REQ-01 | Canonical Identity | Phase 0 | Gemini | WF-002 | `dna_strategy` schema | Identity normalization unit tests |
| REQ-02 | Metric Dictionary | Phase 0 | Gemini | WF-003 | Metric definitions | Formula validation tests |
| REQ-03 | Regime Definitions | Phase 0 | Gemini | WF-004 | Regime methodology | Classification rules tests |
| REQ-04 | Security & Compliance | Phase 0 | Gemini | WF-005 | Boundary controls | RBAC and boundary contract tests |
| REQ-05 | Strategy Registry | Phase 1 | Gemini | WF-101 | `dna_strategy` table | Immutable hash property tests |
| REQ-06 | Ingestion Pipeline | Phase 1 | Gemini | WF-102 | Ingestion scripts | Idempotency and reconciliation tests |
| REQ-07 | Data Quality | Phase 1 | Gemini | WF-103 | Quarantine table | Schema drift and null tests |
| REQ-08 | Market Data | Phase 1 | Gemini | WF-104 | `market_regime_observation` | Regime join tests |
| REQ-09 | Headline Analytics | Phase 2 | Gemini | WF-201 | `dna_strategy_stats` | Golden dataset reconciliation |
| REQ-10 | Period Analytics | Phase 2 | Gemini | WF-202 | `dna_strategy_period_stats` | Period bucketing tests |
| REQ-11 | APIs & Read Models | Phase 2 | Gemini | WF-204 | REST API endpoints | OpenAPI contract and caching tests |
| REQ-12 | Directory UI | Phase 3 | Claude | WF-301 | Listing components | End-to-end journey UI tests |
| REQ-13 | Strategy Detail UI | Phase 3 | Claude | WF-302 | Individual strategy screen | Accessibility and empty state tests |
| REQ-14 | Compare & Watchlist | Phase 3 | Claude | WF-303 | Comparison tables | E2E compare journey tests |
| REQ-15 | Regime Analytics | Phase 4 | Claude | WF-401 | `dna_strategy_regime_stats` | Regime exposure and logic tests |
| REQ-16 | Portfolio Analytics | Phase 5 | Claude | WF-501 | `dna_portfolio` | Reproducible optimizer tests |
| REQ-17 | Broker Sandbox | Phase 6 | Codex | WF-601 | Broker API abstraction | **DEFERRED** |
| REQ-18 | Public Launch | Phase 7 | Codex | WF-704 | Rollback and telemetry | Release gates checklist |
