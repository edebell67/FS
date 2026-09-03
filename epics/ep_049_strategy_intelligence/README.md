# EP049 Strategy Intelligence

## Version history

- 1.0.0 (2026-09-03): Initial epic overview after the agent-queryable intelligence API, the real EP052 Arena intelligence provider, and the owner-instruction relay loop were built and live-verified.

Agent-facing intelligence layer for the DNA Strategy Directory (EP051), and its real integration into the EP052 Agentic Arena as the `strategy_trading` skill's intelligence access. `ep_049` was explicitly settled by the user as the strategy intelligence epic on 2026-09-03, superseding an earlier, unrelated EP046 plan to deploy `site_restructure` to `/ep049` (that plan needs a new epic number when it resumes).

The application code lives in `epics/ep_051_strategy_directory/hosted_directory/` (the query engine, `app/main.py`, `app/intelligence/`) and `epics/ep_052_strategy_directory_agentic_trade_arena/scripts/` (the real Arena provider integration point and the owner-instruction agent). This epic folder holds the workflow doc and evidence for that work, not the running application itself.

## What is implemented

**Agent-queryable intelligence API** (EP051 `/api/intelligence/query/*`, all backed by real SQL Server/Postgres/memory data, not fixtures):
- `POST /query/search` and `/query/chain` - `StrategyQuery` filters (win_rate, sharpe, sortino, calmar, VaR, profit_factor, quality_score, evidence_confidence, track_record, walk_forward positive-fold rate, live/backtest divergence, regime fit, `return_basis` for net vs. reversed-trade screening), chainable across up to 10 stages.
- `POST /query/timetravel` and `/query/timetravel/series` - point-in-time backtesting with no look-ahead: screen using only evidence available as of a past date/time, then measure real forward performance against a same-window baseline, with a day-by-day consistency score.
- `POST /query/top-performers` and `POST /query/time-window` - canned, one-call answers to the two most common recent-performance asks ("best in the last N hours with more than M trades", "100% win rate before a clock time"), with correct no-look-ahead trailing-window semantics and local-time (not UTC) labelling.
- `POST /regime/similar-days` - intraday price-shape (24 hourly open/high/low%) nearest-neighbour day search per instrument, built from raw tick captures, joined to a strategy's real performance on matched days.
- `GET /query/schema` - full machine-readable field/endpoint catalogue for agent self-discovery.

**Real EP052 Arena intelligence provider** (`app/arena_provider.py`), replacing the Arena's `simulated_intelligence.py` random-selection placeholder:
- Implements the Arena's own pre-existing `GET /v1/contracts/intelligence` contract exactly (`POST /v1/queries`, `GET /v1/deliveries/{id}`), gated by a shared service token plus the Arena's own `X-EP052-Agent-ID` header - no new agent-identity system, since the Arena's owner/agent/connection model already authenticates the agent before any query reaches this provider.
- `kind`-dispatched ranking (`top_performers`, `high_win_rate`, `low_drawdown`, `quality`, plus aliases) against the real query engine, scoped to the request's window and `strategy_ids`; an unrecognized `kind` falls back to `quality` with an explanatory notice rather than erroring.
- `GET /v1/observability/agents` - per-agent query activity (count, fallback rate, latency, cache hits) with a rolling-window anomaly warning.
- `GET /v1/kinds` - the recognized `kind` vocabulary published live, with a running fallback-rate signal for when agents ask for a kind that doesn't exist yet.
- Verified end-to-end through the live running Arena using a real registered agent credential: real ranked (non-random) result, real `$0.01` fee charged and visible in owner positions, receipt recovery confirmed.

**Owner-instruction relay** (`scripts/instructed_intelligence_agent.py`, EP052 side):
- Reads free-text guidance from the Arena's existing owner Feedback box (`GET /v1/me/feedback`), interprets it via a deterministic, rule-based keyword parser (no LLM dependency, by design - see Architecture notes) into query parameters, submits the real intelligence query, then acknowledges the feedback and relays a plain-English summary back into the same Feedback thread.
- Verified end-to-end against a freshly registered owner+agent pair: real instruction submitted, real interpretation, real query, real fee, real reply visible to the owner.

**Not yet done:** deployment to any hosted URL (everything above runs against local services only, `127.0.0.1`); every new code path takes its base URL as a CLI/env parameter specifically so this can move to a hosted deployment later without code changes. Per-agent auth/rate-limiting for potentially thousands of concurrent agents was designed but not built - the Arena's existing per-agent-connection identity plus this epic's `/v1/observability/agents` anomaly logging is the current real-identity anchor for that, should it be needed.

## Architecture notes (binding for future work in this epic)

- **Everything agent-facing routes through the Arena.** No side-channel between an agent and a backend service, and no direct agent-to-agent bypass, even for a future skill designed to feel peer-to-peer - it is always agent -> Arena -> agent/service, with the Arena remaining the validator of every transaction.
- **Access is skill/purpose-scoped** (`ConnectionRequest.purpose`, currently `strategy_trading`), with full isolation between skills. This epic's intelligence access is `strategy_trading`'s access specifically, not a generic Arena feature - an agent connecting for a different future purpose has no awareness the exchange or intelligence layer exists. The Arena itself is a generic, multi-use-case surface; this isolation is deliberate groundwork for other future skills, potentially including agent-to-agent ones (still always mediated by the Arena).
- **Keep additions lightweight.** Prefer the smallest change that makes the agent<->Arena communication loop work correctly over new infrastructure (tables, services, config surfaces) unless the loop itself needs it. Rule-based/deterministic logic over new heavy dependencies is the default here.

## Evidence and workflow

- `workflow/EP049_real_intelligence_provider_workflow.html` - the 11-gate implementation workflow for the real Arena provider (RIP-010 through RIP-110), all gates complete.
- `evidence/end_to_end_verification_20260903.json` - direct-provider and live-Arena verification of the intelligence provider.
- `evidence/owner_instruction_loop_verification_20260903.json` - live verification of the owner-instruction relay loop.
- Application-level tests: `epics/ep_051_strategy_directory/hosted_directory/tests/` (118 passing, incl. 18 for `arena_provider.py`) and `epics/ep_052_strategy_directory_agentic_trade_arena/scripts/test_instructed_intelligence_agent.py` (10 passing).
- Workstream task record: `workstream/300_complete/claude/20260903_170500_ep051_997_agent_queryable_intelligence_and_arena_provider.md` (not git-tracked; `workstream/` is gitignored in this repo by convention).

This is decision support and research evidence, not personalised financial advice or a forecast.
