# Live Multi-Asset Market Data Ingestion System

## Master Build Prompt

------------------------------------------------------------------------

## Objective

Design and implement a **resilient live intraday market data ingestion
system** that captures real-time prices across multiple asset classes
and feeds them into an existing trading system.

The system must:

-   Pull live intraday prices
-   Support futures, metals, energy, crypto, and major stocks
-   Handle rate limits
-   Include failover between multiple providers
-   Validate and normalize data
-   Provide clean structured output suitable for ingestion into a
    trading engine
-   Be production-ready and 24/7 capable

------------------------------------------------------------------------

## Asset Classes to Cover

### 1️⃣ Financial Futures

Include:

-   T-Bills
-   US Treasury Bonds
-   Interest Rate Futures

Primary exchanges may include:

-   CME
-   CBOT
-   Other relevant US futures exchanges

The system should not hardcode a single exchange dependency.

------------------------------------------------------------------------

### 2️⃣ Metals (Futures)

Include:

-   Gold
-   Silver

Likely from:

-   CME
-   COMEX
-   NYMEX (if applicable)

Source does not matter as long as:

-   Data is reliable
-   Latency is reasonable
-   Pricing is accurate for trading use

------------------------------------------------------------------------

### 3️⃣ Energy (Futures)

Include:

-   Crude Oil (WTI)
-   Brent Crude
-   Other key oil benchmarks if available

Exchange flexibility allowed.

------------------------------------------------------------------------

### 4️⃣ Cryptocurrencies (Spot)

Include:

-   BTC
-   ETH
-   Major liquid altcoins

Use multiple exchanges for redundancy if possible.

------------------------------------------------------------------------

### 5️⃣ Major Stocks

Include:

-   Large-cap US stocks
-   Highly liquid global equities (if available)

Focus on:

-   High volume
-   Institutional-grade pricing

------------------------------------------------------------------------

## System Requirements

### A. Multi-Provider Architecture

The system must:

-   Support multiple API providers per asset class
-   Automatically fail over if:
    -   API error occurs
    -   Latency exceeds threshold
    -   Data validation fails
-   Allow easy addition of new providers

------------------------------------------------------------------------

### B. Rate Limit Handling

Include:

-   Automatic request throttling
-   Adaptive retry logic
-   Exponential backoff
-   Intelligent caching for short intervals
-   Provider-specific rate-limit tracking

------------------------------------------------------------------------

### C. Data Validation Layer

Each incoming price must be validated:

-   Reject zero prices
-   Reject negative prices
-   Detect price jumps beyond configurable threshold
-   Compare against secondary provider (if available)
-   Flag abnormal volatility spikes

Must support:

-   Configurable deviation thresholds
-   Logging of rejected data
-   Alerting hook for anomalies

------------------------------------------------------------------------

### D. Normalization Layer

All incoming data must be normalized into a unified schema.

Example structure:

{ "symbol": "GC", "asset_class": "futures", "exchange": "CME",
"timestamp": "UTC ISO format", "bid": 0.0, "ask": 0.0, "last": 0.0,
"volume": 0, "source": "provider_name", "latency_ms": 0 }

------------------------------------------------------------------------

### E. Storage Layer

The system must:

-   Support streaming to:
    -   Database (Postgres / SQL Server)
    -   Message queue (Kafka / Redis / RabbitMQ)
    -   Flat file / JSON stream
-   Be easily configurable
-   Support both live and simulated environments

------------------------------------------------------------------------

### F. Trading System Integration

Provide:

-   Clean API endpoint OR
-   Stream output format
-   OR database write integration

Must be suitable for:

-   Real-time algorithmic trading
-   Snapshot capture
-   Replay capability

------------------------------------------------------------------------

### G. Observability & Monitoring

Include:

-   Structured logging
-   Provider health monitoring
-   Latency tracking
-   Failure counters
-   Alert hook integration
-   Toggleable debug mode

------------------------------------------------------------------------

## Architecture Requirements

Design the solution using:

-   Modular architecture
-   Provider adapters (plug-in pattern)
-   Validation middleware
-   Central orchestrator
-   Async / event-driven design

Language preference:

-   Python (preferred)
-   Use async where possible
-   Clean separation of concerns

------------------------------------------------------------------------

## Resilience Requirements

The system must:

-   Run 24/7
-   Recover automatically from API failures
-   Reconnect after network interruptions
-   Not crash the process on provider failure
-   Support graceful shutdown
-   Support restart without data corruption

------------------------------------------------------------------------

## Configuration

Use:

-   External config file (YAML or JSON)
-   Configurable:
    -   Symbols
    -   Providers
    -   Validation thresholds
    -   Polling frequency
    -   Output mode

No hardcoded secrets.

------------------------------------------------------------------------

## Deliverables Required

Generate:

1.  Full system architecture explanation
2.  Folder structure
3.  Core Python implementation
4.  Example provider adapter
5.  Validation middleware
6.  Failover mechanism
7.  Config file example
8.  Logging setup
9.  Example database write
10. Instructions for deployment
11. Instructions for scaling

------------------------------------------------------------------------

## Important Constraints

-   Do NOT rely on a single provider
-   Do NOT assume unlimited API usage
-   Must support institutional reliability standards
-   Must be extensible
-   Must not introduce unnecessary complexity

------------------------------------------------------------------------

## Design Philosophy

This is a financial production system.

No experimental shortcuts.

Focus on:

-   Stability
-   Determinism
-   Observability
-   Clean engineering

------------------------------------------------------------------------

## Stretch Enhancements (Optional but Preferred)

-   WebSocket support for real-time feeds
-   Dynamic provider scoring (latency + reliability weighted)
-   Auto-switching primary feed
-   In-memory price cache
-   Backtesting replay capability

------------------------------------------------------------------------

## Final Instruction to LLM

Produce production-grade code and documentation suitable for immediate
integration into a live trading system. Prioritize reliability, failover
logic, and clean modular architecture over speed of implementation.

------------------------------------------------------------------------

## Derived Tasks

Tasks decomposed from this backlog (created 2026-02-25):

| Phase | # | Task | Status | Location |
|-------|---|------|--------|----------|
| 1 - Foundation | 01 | Project Setup & Folder Structure | TODO | `100_todo/20260225_150834_live_mkt_01_project_setup.md` |
| 1 - Foundation | 02 | Configuration System | TODO | `100_todo/20260225_150835_live_mkt_02_config_system.md` |
| 1 - Foundation | 03 | Core Data Models | TODO | `100_todo/20260225_150836_live_mkt_03_data_models.md` |
| 2 - Provider Infra | 04 | Provider Adapter Base Class | TODO | `100_todo/20260225_150837_live_mkt_04_provider_base.md` |
| 2 - Provider Infra | 05 | Rate Limit Handler | TODO | `100_todo/20260225_150838_live_mkt_05_rate_limiter.md` |
| 2 - Provider Infra | 06 | Failover Mechanism | TODO | `100_todo/20260225_150839_live_mkt_06_failover.md` |
| 3 - Data Quality | 07 | Validation Middleware | TODO | `100_todo/20260225_150840_live_mkt_07_validation.md` |
| 3 - Data Quality | 08 | Normalization Layer | TODO | `100_todo/20260225_150841_live_mkt_08_normalizer.md` |
| 4 - Providers | 09 | Crypto Provider Adapter | TODO | `100_todo/20260225_150842_live_mkt_09_crypto_provider.md` |
| 4 - Providers | 10 | Futures/Metals/Energy Provider | TODO | `100_todo/20260225_150843_live_mkt_10_futures_provider.md` |
| 4 - Providers | 11 | Stocks Provider Adapter | TODO | `100_todo/20260225_150844_live_mkt_11_stocks_provider.md` |
| 5 - Storage | 12 | Storage Layer | TODO | `100_todo/20260225_150845_live_mkt_12_storage_layer.md` |
| 5 - Integration | 13 | Central Orchestrator | TODO | `100_todo/20260225_150846_live_mkt_13_orchestrator.md` |
| 5 - Integration | 14 | Trading System API | TODO | `100_todo/20260225_150847_live_mkt_14_api_endpoint.md` |
| 6 - Operations | 15 | Logging & Observability | TODO | `100_todo/20260225_150848_live_mkt_15_logging.md` |
| 6 - Operations | 16 | Deployment & Documentation | TODO | `100_todo/20260225_150849_live_mkt_16_deployment.md` |

**Total Tasks**: 16
**Completed**: 0/16

------------------------------------------------------------------------

## Backlog Status

**STATUS**: ACTIVE
**Decomposition Date**: 2026-02-25
**Completion Criteria**: All 16 tasks must be in `300_complete` with verification passed
