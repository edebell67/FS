# Non-DNA Research API Boundary

## Purpose

Non-DNA data is an isolated research and validation warehouse. It is never a directory strategy population and never contributes to public DNA metrics, ranks, relationships, portfolio candidates, or live results.

## Permitted private interfaces

- `POST /internal/research/v1/non-dna/what-if`: time-bounded hypothetical entry/horizon analysis.
- `POST /internal/research/v1/non-dna/benchmark`: independent comparison against a supplied DNA evidence snapshot.
- `GET /internal/research/v1/non-dna/market-state`: research-only market opportunity observations.

Every response must include `data_domain: "NON_DNA_RESEARCH"`, `research_only: true`, source window, methodology version, generated timestamp, and the warning “Not DNA strategy performance.”

## Prohibited interfaces

- No route below `/api/v1/strategies` or `/api/v1/portfolios` may read the Non-DNA schema.
- No public search/filter value may expose Non-DNA identifiers.
- No Non-DNA result may be represented with a canonical `DNA_[0-9]+` strategy ID.
- No research output may be cached in a public directory cache namespace.

## Isolation architecture

- Separate database schema and least-privilege research service identity.
- Public directory role has no `USAGE`, `SELECT`, or function execution rights on the research schema.
- Export requires an explicit research lineage envelope; raw records stay isolated.
- Logs contain request/run IDs and aggregate counts, not restricted trade payloads.

