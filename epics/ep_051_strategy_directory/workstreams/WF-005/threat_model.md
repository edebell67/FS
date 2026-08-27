# Threat Model - EP051 DNA Strategy Directory

## 1. High-Level Architecture & Boundaries
The DNA Strategy Directory aggregates trade history into public analytics.
- **Trust Boundaries**: (1) Database Ingestion (Internal), (2) Aggregation Layer (Internal), (3) Public API / Frontend (External).

## 2. Threat Actors
- **External Unauthenticated**: Attempting to scrape restricted data or DDoS.
- **Compromised Internal Node**: Attempting to manipulate historical trade returns to falsify a strategy's win rate.
- **Malicious Broker Integration (Deferred)**: Supplying fake trade data to alter DNA metrics.

## 3. Top Threats & Mitigations
- **T1: Data Leakage of Private Trades** 
  - *Mitigation*: The `data_classification` explicitly isolates Non-DNA (research) trades from the public directory. Queries must filter by `is_dna = true`.
- **T2: Metric Manipulation (Historical Revisionism)** 
  - *Mitigation*: DNA trade definitions are immutable. Updates post-settlement are prohibited and generate a compliance alert.
- **T3: PII Leakage**
  - *Mitigation*: Strategy directory operates on anonymized GUIDs and strategy IDs. Broker account numbers and PII are stripped at ingestion.
- **T4: Broker Credential Compromise**
  - *Mitigation*: Explicitly deferred to Phases 6-8. Broker activation requirements will demand secrets management (HashiCorp/AWS KMS) and IP whitelisting.

## 4. Incident Responsibilities
- **Data Team**: Investigating data anomalies or unauthorized revisions.
- **Security Team**: Handling suspected leakage or DDoS against public read endpoints.
