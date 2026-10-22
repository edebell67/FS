# Data Classification - EP051 DNA Strategy Directory

## Classification Levels

### 1. PUBLIC (Level 1)
- **Description**: Data intended for broad public consumption on the marketing/dashboard pages.
- **Fields/Endpoints**: 
  - Aggregated performance metrics (`win_rate`, `total_net_return`, `profit_factor`).
  - Canonical Strategy IDs (e.g., `DNA_102001`).
  - High-level regime state (e.g., "Trending", "Volatile").
- **Controls**: Read-only via public API. Rate-limited.

### 2. INTERNAL RESTRICTED (Level 2)
- **Description**: Internal data used for reconciliation, research, and tracking lineage. Not for public exposure.
- **Fields/Endpoints**:
  - Individual trade records (`guid`, exact entry/exit timestamps).
  - Original strategy suffixes (`_S`, `_B`).
  - Non-DNA trade data.
- **Controls**: Access restricted to authorized internal analysts and the aggregation engine. Requires IAM role.

### 3. CONFIDENTIAL / PII (Level 3)
- **Description**: Highly sensitive data that must not enter the DNA Directory scope.
- **Fields/Endpoints**:
  - Broker account identifiers.
  - Client names or IDs.
  - API Keys / Broker Tokens.
- **Controls**: Stripped at source. Any discovery in the DNA pipeline triggers an immediate P1 incident. Broker credentials handled exclusively via encrypted vaults in Phase 6+.
