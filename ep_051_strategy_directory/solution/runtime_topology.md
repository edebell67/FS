# EP051 Runtime Topology

## Version history

- 1.0.0 (2026-08-23): Initial deterministic topology.

The research-directory deployment separates: static web UI; read-only API; ingestion/analytics worker; PostgreSQL canonical/derived stores; Redis-compatible cache; migration job; and observability collector. Public traffic reaches only the web/API boundary. Open-state routes require owner-scoped authentication. Workers read source tables and publish immutable versioned snapshots. The offline broker sandbox is a separate optional profile with no network credential surface and is absent from the initial public topology.

Local verification requires Python 3.11+ only and performs no network installation. Containerized topology is defined by INF-002. Determinism comes from pinned image/runtime versions, immutable migration ordering, explicit environment templates, versioned snapshots and artifact digests.

