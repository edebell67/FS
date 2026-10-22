# DNA Strategy Directory — End-to-End Implementation Specification

**Document status:** implementation baseline  
**Version:** 1.0  
**Primary population:** initially 300–500 DNA strategies  
**Purpose:** a build-ready specification for the data, intelligence, product, operational, and launch layers of the DNA Strategy Directory.

## 1. Product mandate

Build a public-facing directory and intelligence platform that turns a population of fixed DNA trading strategies into evidence-backed answers for traders. The product is not merely a catalogue of strategy IDs. Its differentiator is the layer above the trades: observed behaviour, regime response, strategy relationships, portfolio construction, and transparent explanations.

The initial release must support approximately 300–500 DNA strategies and scale to thousands without changing the identity model or core architecture. FX is the first market. The design must permit later expansion to futures, crypto, and other liquid electronic markets.

The product must help users answer questions such as:

- Which strategies meet my return, drawdown, activity, market, and capital constraints?
- How has a strategy behaved across time and market regimes?
- What should I combine with a strategy I already use?
- Which group of strategies has historically produced a better risk/diversification profile than simply selecting the highest returns?
- What evidence supports each classification, score, and suggestion?
- What is each strategy doing now, and is its live behaviour consistent with its history?

This is decision support, not a promise of future performance. Every presentation and API must distinguish fact, derived measure, classification, and recommendation.

## 2. Canonical semantics and non-negotiable constraints

### 2.1 DNA population and lifecycle

- Generate an initial population of **300–500 DNA strategies**.
- A DNA strategy is randomly generated **once**. Its definition then becomes fixed and perpetual.
- Never silently mutate a strategy definition while retaining the same canonical ID. A material definition change requires a new ID/version and lineage metadata.
- Friendly/descriptive names will be supplied later. Analytics must attach to the canonical ID, never to the mutable display name.
- Do not assign marketing-style labels such as “conservative,” “aggressive,” “income,” or “best for rising markets” until empirical thresholds, evidence, and governance rules exist.

### 2.2 Identity normalization

Directory identity is the normalized DNA identifier:

```text
DNA_102001_S -> DNA_102001
DNA_102001_B -> DNA_102001
```

The terminal `_S` and `_B` suffixes are ignored for directory identity. Preserve the original source `model` value for lineage and reconciliation, but do not create separate directory strategies from those suffixes. Trade direction comes from `signal` (`BUY`/`SELL`), not from the suffix.

Normalization must be deterministic, case-insensitive on input, canonicalized to uppercase, whitespace-trimmed, and limited to a documented regex. Invalid/unrecognized identifiers go to quarantine, not silent aggregation.

### 2.3 Trade sources

- `combined_trades_closed` is the source of truth for completed full-round-turn historical analytics.
- `combined_trades_open` is the source for current/open trade state only; do not mix unrealized values into closed-trade headline performance.
- A closed trade is uniquely identified by `guid`; ingestion must be idempotent.
- `close_type = 'target reached'` can represent either a profit or a loss boundary. It describes how the trade ended, not whether it won.
- Outcome is derived from `net_return`: positive = winner, negative = loser, zero = breakeven.
- Commission/costs are already incorporated into trade results. Do not subtract them again or overlay a hypothetical cost model on reported results. Commission may be displayed analytically, but not double-counted.
- For exit time, use an explicitly validated precedence rule, provisionally `COALESCE(g_close_time, last_update)`. Confirm this against source behaviour before production metrics.
- `min_net_return` and `max_net_return` support adverse/favourable excursion analytics. Treat their meaning and units as source contracts and validate them.

### 2.4 Non-DNA boundary

Non-DNA is **not** part of the strategy-directory population. It is a continuous trade warehouse, potentially creating buy and sell observations every minute with predefined boundaries. Its permitted roles are:

- research and hypothesis generation;
- independent validation and benchmarking;
- rapid historical what-if/backtest analysis (for example, hypothetical entry at a historical minute and exit after a chosen horizon);
- market-state and opportunity analysis.

Non-DNA records must remain clearly labelled and separated from DNA performance. Never present Non-DNA observations as DNA live results or commingle them in public DNA metrics.

## 3. Scope

### 3.1 In scope

- canonical strategy registry and immutable-definition lifecycle;
- trade ingestion, normalization, validation, reconciliation, and aggregation;
- headline, period, regime, relationship, and portfolio analytics;
- directory list, discovery, comparison, individual strategy pages, open-trade state, and portfolio builder;
- objective regime classification established independently of strategy outcomes;
- explainability, evidence windows, sample sufficiency, freshness, and methodology versioning;
- broker/platform deployment abstraction, health monitoring, kill controls, and audit trail;
- authenticated/admin APIs and deliberately limited public APIs;
- caching, performance, security, testing, observability, phased rollout, and public launch;
- multi-market extensibility.

### 3.2 Out of scope for initial public release

- treating Non-DNA records as listed strategies;
- guaranteed outcomes or personalized regulated financial advice;
- unsupported qualitative labels or AI-written claims without traceable evidence;
- automatic live-capital deployment without explicit user confirmation, broker controls, and suitability/risk disclosures;
- regime claims before regime data and minimum sample thresholds are met.

## 4. Target architecture

```text
Trading sources
  ├─ combined_trades_closed ─┐
  ├─ combined_trades_open ───┼─> ingestion/validation -> canonical trade views
  ├─ DNA definition registry ┤                           |
  └─ market/regime data ─────┘                           v
                                                analytics compute
                                     ┌─────────────┬─────────────┐
                                     v             v             v
                                  strategy       regime      relationships
                                     └─────────────┴─────────────┘
                                                   v
                                         portfolio intelligence
                                                   v
                                      versioned APIs + cache/search
                                                   v
                              directory / strategy / portfolio / admin UI

Non-DNA warehouse -> isolated research/validation/what-if services only
```

Recommended separation: raw/source schemas; canonical/validated views; derived analytics tables; serving/read models; public application. Preserve raw records unchanged.

## 5. Data model

All monetary values require a currency or normalized reporting basis. Do not aggregate unlike currencies without an explicit FX conversion timestamp and methodology. Prefer fixed precision decimal types over floating point in derived financial tables.

### 5.1 `dna_strategy` — canonical master

One row per normalized strategy.

| Field | Requirement |
|---|---|
| `strategy_id` | PK, canonical value such as `DNA_102001` |
| `descriptive_name` | nullable, supplied later, not an analytics key |
| `definition_hash` | immutable definition fingerprint |
| `definition_version` | version/lineage control |
| `parent_strategy_id` | nullable lineage reference |
| `market` / `product_type` | initially FX; extensible |
| `products` | normalized association, preferably separate join table |
| `status` | `DRAFT`, `COLLECTING`, `ELIGIBLE`, `ACTIVE`, `PAUSED`, `RETIRED`, `QUARANTINED` |
| `generated_at` | creation time |
| `eligible_at` / `retired_at` | lifecycle timestamps |
| `methodology_version` | active analytics/classification version |
| `visibility` | private/internal/public |
| `created_at` / `updated_at` | audit timestamps |

Add `dna_strategy_source_alias(strategy_id, source_model, first_seen_at, last_seen_at)` so all suffixed source models reconcile to the canonical identity.

### 5.2 `dna_strategy_stats` — headline snapshot

One row per strategy per calculation version/as-of time (or current materialized row plus immutable history).

Required fields:

- coverage: first/last trade, active/trading days, observation days, data freshness, total/buy/sell/breakeven trades;
- return: total, mean, median, standard deviation, best/worst, gross profit, gross loss, profit factor;
- outcome: wins, losses, breakevens, win/loss rates, average win/loss, payoff ratio, expectancy;
- path risk: maximum drawdown, drawdown percentage where a valid capital/equity denominator exists, current drawdown, maximum drawdown duration, recovery duration;
- behaviour: mean/median holding minutes, trades per active day/calendar day, buy/sell returns and win rates, streaks;
- excursion: mean/median MFE and MAE, capture ratio where valid;
- risk-adjusted/consistency: return dispersion, downside deviation, Sortino-like value (only with defined periodic series/risk-free convention), profitable-period ratio, concentration, consistency score;
- quality metadata: sample size, sufficiency status, last source watermark, calculation/methodology version, calculated timestamp.

Never label a currency P&L aggregate as a percentage return. Percentage drawdown and Sharpe/Sortino require an explicitly defined capital/equity and periodic-return methodology.

### 5.3 `dna_strategy_period_stats`

Primary key: `(strategy_id, period_type, period_start, methodology_version)`.

Support `DAY`, `WEEK`, `MONTH` initially and rolling windows later. Store trades, winners, losers, breakevens, net return, mean/median trade, win rate, period peak/trough, maximum drawdown, active flag, and completeness. Use a documented timezone and calendar.

### 5.4 `market_regime_observation`

One objective market-state observation per instrument/time bucket:

- instrument, market, interval start/end;
- directional state: `TREND_UP`, `TREND_DOWN`, `SIDEWAYS`, optionally `TRANSITION`/`UNKNOWN`;
- volatility state: `HIGH_VOLATILITY`, `NORMAL_VOLATILITY`, `LOW_VOLATILITY`;
- feature values, thresholds, lookback, data source, definition version, confidence/quality.

Regime definitions must be locked before evaluating DNA outcomes for the relevant methodology version to reduce hindsight bias.

### 5.5 `dna_strategy_regime_stats`

Primary key: `(strategy_id, regime_dimension, regime_value, definition_version, methodology_version)`.

Store exposure time, trades, net/average/median return, win rate, profit factor, maximum drawdown, downside deviation, confidence interval, sample size, sufficiency status, and comparative lift versus the strategy’s overall baseline.

### 5.6 `dna_strategy_relationship`

Store only one canonical pair (`strategy_id_a < strategy_id_b`) per window/version:

- observation window and frequency/alignment method;
- return correlation;
- downside correlation;
- overlapping loss-period percentage;
- drawdown overlap/severity;
- common exposure/time overlap;
- complementarity and diversification scores;
- sample count, confidence/quality, calculated timestamp, methodology version.

Do not correlate raw asynchronous trade rows. Create aligned daily (or documented interval) strategy return/P&L series, including explicit zero/no-trade policy.

### 5.7 Portfolio schema

- `dna_portfolio`: ID, owner/visibility, name, objective, base currency, capital, constraints JSON, optimizer/methodology version, status, timestamps.
- `dna_portfolio_member`: portfolio ID, strategy ID, weight/allocation, enabled state, rationale/evidence snapshot.
- `dna_portfolio_stats`: as-of/window, combined return, drawdown, volatility/downside deviation, correlation concentration, effective strategy count, turnover/activity, capital/margin estimate, scenario/regime results, freshness/version.
- `dna_portfolio_run`: request, eligible universe, exclusions, objective, constraints, solver seed/version, candidate solutions, selected solution, warnings and evidence; required for reproducibility.

### 5.8 Supporting entities

- product/instrument master, trading calendar, currency/FX conversion table;
- strategy definition store and immutable hashes;
- score/classification definition and version tables;
- data-quality issue/quarantine table;
- deployment, broker account mapping, order/execution event, health/heartbeat, alert and audit tables;
- saved searches, watchlists, comparisons, user preferences and disclosure acknowledgements.

## 6. Analytics specification

Let closed trade returns be `r_i = net_return_i`, ordered by validated exit time.

### 6.1 Core formulas

```text
total_trades       = count(valid closed trades)
wins               = count(r_i > 0)
losses             = count(r_i < 0)
breakevens         = count(r_i = 0)
win_rate           = wins / total_trades
total_net_return   = sum(r_i)
average_trade      = mean(r_i)
median_trade       = median(r_i)
gross_profit       = sum(r_i where r_i > 0)
gross_loss         = abs(sum(r_i where r_i < 0))
profit_factor      = gross_profit / gross_loss
average_win        = mean(r_i where r_i > 0)
average_loss       = mean(r_i where r_i < 0)
payoff_ratio       = average_win / abs(average_loss)
expectancy         = win_rate*average_win + loss_rate*average_loss
holding_minutes    = exit_time - created
trades_per_day     = trades / documented active-day denominator
```

Edge cases: profit factor is null/not infinite-display when no losses; ratios are null when denominators are zero; insufficient samples are explicitly flagged; missing values are not silently converted to zero.

### 6.2 Equity curve and drawdown

For additive monetary P&L:

```text
E_t = starting_equity + cumulative_sum(r_i)
peak_t = max(E_0 ... E_t)
drawdown_t = E_t - peak_t
max_drawdown = min(drawdown_t)
```

If starting equity is not defined, publish monetary drawdown only. Publish percentage drawdown only when the denominator and position-sizing policy are explicit. Also calculate start, trough, recovery timestamps and duration.

### 6.3 Excursion

Validate whether `max_net_return` and `min_net_return` are already net of costs and share the same basis as `net_return`.

```text
MFE_i = max_net_return_i
MAE_i = min_net_return_i
capture_i = net_return_i / MFE_i  (only when valid and MFE_i > 0)
```

Use distributions, not only averages. Surface how often winners first suffered adverse excursion and how often losing trades had meaningful favourable excursion.

### 6.4 Period consistency and concentration

Calculate profitable day/week/month ratios, rolling returns, rolling drawdowns, rolling trade counts, and return concentration. A defensible initial consistency score can combine:

- profitable-period ratio;
- stability of rolling results;
- penalty for dependence on the top N periods/trades;
- penalty for large dispersion/drawdown;
- sample sufficiency.

Publish the components and methodology version. Calibrate high/medium/low thresholds only after observing the initial population; freeze thresholds per version.

### 6.5 Initial intelligence scores

Keep the first public score set small:

1. **Consistency:** evenness of returns across time.
2. **Risk:** drawdown and dispersion/downside behaviour.
3. **Activity:** trading frequency and continuity.
4. **Direction balance:** dependence on BUY versus SELL performance.
5. **Diversification:** difference/complementarity relative to the eligible DNA universe.

Scores must be population-normalized only within comparable cohorts (market, currency/basis, observation window) and accompanied by raw metrics, methodology, sample size, and as-of date.

### 6.6 Correlation, downside correlation, and overlap

- Build aligned periodic series per strategy using the same timezone, calendar, and frequency.
- Return correlation: Pearson initially; optionally Spearman as robustness evidence.
- Downside correlation: correlation on periods where one or both strategies are below the documented downside threshold; publish definition.
- Loss overlap: proportion of aligned periods in which both returns are negative, with conditional forms such as `P(B<0 | A<0)`.
- Drawdown overlap: proportion of time both are in drawdown plus joint severity/duration statistics.
- Diversification score: versioned composite rewarding low/negative correlation, low downside correlation, low joint-loss/drawdown overlap, adequate independent activity, and robustness across subperiods/regimes.

Do not imply causation. Suppress/rank cautiously for thin overlap or unstable correlations.

### 6.7 Portfolio construction

Portfolio selection must not default to the highest-returning strategies. Inputs include capital, eligible markets/products, maximum strategies, minimum history/trades, per-strategy allocation bounds, correlation/concentration ceiling, activity, drawdown tolerance, and optional regime preferences.

Support transparent methods in sequence:

1. constrained equal weight after diversification selection;
2. risk-balanced allocation;
3. constrained optimization (return/risk/drawdown/diversification), only after robust validation.

Outputs must include allocation, combined historical series, drawdown, concentration, contribution by strategy, regime/scenario behaviour, excluded candidates and reasons, sensitivity, and limitations. Apply temporal train/validation/holdout or walk-forward evaluation; prevent look-ahead and survivorship bias.

## 7. Data pipeline

1. **Ingest:** read source tables incrementally using durable watermarks; preserve raw rows and source timestamps.
2. **Validate:** uniqueness, required fields, allowed signal, time ordering, numeric ranges, nulls, schema drift, and source freshness.
3. **Normalize:** canonical strategy ID, products, case, timestamps/timezone, result precision, and outcome.
4. **Quarantine:** isolate invalid identifiers/records with reason and replay support.
5. **Reconcile:** counts and P&L totals from source to canonical layer by batch/day/model.
6. **Aggregate:** headline and period stats from closed trades; open-state snapshot separately.
7. **Enrich:** attach objective market regime observations without future information.
8. **Relate:** build aligned series and pairwise relationship metrics.
9. **Construct:** run reproducible portfolio candidates and validation.
10. **Publish:** atomically replace/version serving snapshots, invalidate caches, update search index.

Jobs must be idempotent, restartable, backfillable by time/strategy/methodology version, and lineage-aware. Store source watermark, code version, definition version, row counts, checksum/reconciliation results, duration, and failure reason for every run.

Suggested freshness: open trades near real time; closed-trade headline refresh shortly after closure or at a frequent micro-batch; relationship/regime/portfolio analytics scheduled daily unless product needs dictate otherwise.

## 8. Directory and discovery UX

### 8.1 Directory listing

Default columns/cards:

- strategy ID and optional descriptive name;
- product(s)/market;
- evidence window and last active;
- closed trades;
- net return with currency/basis;
- win rate;
- profit factor;
- maximum drawdown;
- average trade;
- trades per day/activity;
- quality/sufficiency/freshness indicator.

Support server-side sort, pagination/virtualization, column selection, shareable URLs, saved searches, compare selection, and mobile-accessible layouts.

Filters: minimum trades/history, return, win rate, profit factor, maximum drawdown, BUY/SELL/both behaviour, product/market, active period, frequency, holding period, risk/consistency/activity bands (when governed), regime evidence (when sufficient), and portfolio complementarity.

Never rank by an opaque “best” default. State the default sort and allow users to change it.

### 8.2 Individual strategy screen

1. **Identity and evidence:** canonical ID, descriptive name when available, status, markets/products, data window, sample size, freshness, methodology.
2. **Overview:** return, drawdown, win rate, profit factor, trades, average trade, warnings.
3. **Performance:** equity curve, drawdown chart, day/week/month results, rolling results, distribution, streaks.
4. **Trade behaviour:** BUY vs SELL, holding periods, winners/losers, best/worst, frequency, MFE/MAE, exits. Explain that `target reached` is not an outcome.
5. **Market behaviour:** regime results with definitions, sample counts, confidence and “collecting data/insufficient evidence” states.
6. **Portfolio:** closest/similar and complementary strategies, relationship components, suggested combinations, add-to-builder.
7. **Current/open trades:** isolated live state from `combined_trades_open`, timestamps and unrealized status, subject to access/disclosure policy.
8. **Methodology and audit:** calculation definitions, versions, known limitations and change log.

### 8.3 Compare and discovery

Allow side-by-side comparison of raw metrics, normalized scores, equity/drawdown paths, regime behaviour, correlations, loss/drawdown overlap, data coverage, and quality. Provide empty/loading/error/stale/insufficient-data states; never fabricate content.

## 9. User value and explainability

Every derived label or suggestion must answer:

- What was calculated?
- From which source and time window?
- How many observations support it?
- What methodology/version was used?
- How stable is it across subperiods/regimes?
- Why is this strategy included or excluded?
- What could make the conclusion unreliable?

Display concise explanations with expandable methodology. Portfolio explanations should identify marginal contribution, not merely repeat individual returns. AI-generated summaries, if added, must use structured facts, cite their evidence fields, avoid unsupported claims, and be reproducible/auditable.

## 10. Broker/platform deployment

Create a broker-agnostic deployment layer, separate from analytics:

- capability discovery (products, order types, minimum sizes, sessions, margin);
- canonical instrument-to-broker mapping;
- strategy/portfolio allocation to account and sizing policy;
- explicit preview and confirmation before activation;
- idempotent order intents and execution reconciliation;
- broker acknowledgement/fill/reject/cancel event log;
- risk gates: max exposure, position, daily loss, stale data, disconnect, duplicate order, price tolerance;
- pause/disable and emergency kill controls;
- drift detection between intended, broker, and directory state;
- complete user/admin audit trail and least-privilege secret management.

Public research views must not imply that displayed historical results equal executable broker performance. Account for broker availability, slippage/latency disclosures, margin, sizing, and market differences without double-counting costs already in source results.

## 11. Monitoring and lifecycle

Monitor data freshness, job success/duration, row-count/P&L reconciliation, quarantine volume, null/schema anomalies, API latency/error/cache rates, UI availability, open-trade staleness, broker heartbeats/rejections/drift, and model analytics drift.

Lifecycle rules:

- `COLLECTING`: visible internally; public metrics restricted.
- `ELIGIBLE`: minimum evidence passed.
- `ACTIVE`: available in public discovery/deployment subject to policy.
- `PAUSED`: no new deployment; history retained.
- `RETIRED`: immutable historical record retained and excluded by default.
- `QUARANTINED`: data/definition integrity issue.

Define automatic flags for stale/no recent activity, material drawdown beyond governance thresholds, definition-hash mismatch, data-quality failure, and behaviour drift. A human-authorized policy decides pause/retire; never rewrite history.

## 12. APIs

Version all external contracts. Minimum endpoints/read models:

```text
GET  /api/v1/strategies
GET  /api/v1/strategies/{strategy_id}
GET  /api/v1/strategies/{strategy_id}/periods
GET  /api/v1/strategies/{strategy_id}/regimes
GET  /api/v1/strategies/{strategy_id}/relationships
GET  /api/v1/strategies/{strategy_id}/open-trades
POST /api/v1/strategies/compare
POST /api/v1/portfolios/search
POST /api/v1/portfolios
GET  /api/v1/portfolios/{portfolio_id}
POST /api/v1/portfolios/{portfolio_id}/deployment-preview
```

Responses include `as_of`, evidence window, methodology version, currency/basis, quality/sufficiency, and stable pagination. Define OpenAPI schemas, validation, consistent error envelopes, rate limits, authorization, field-level exposure, ETags, and deprecation policy. Admin/backfill/deployment APIs must be private and strongly authorized.

## 13. Caching and performance

- Precompute headline, period, regime, relationship, and portfolio read models.
- Use server-side filtering/sorting; do not download all strategies.
- Cache public list/detail payloads by query + methodology + snapshot; invalidate on atomic publish.
- Keep open-trade caching short and visibly timestamped.
- Index canonical ID, visibility/status, product/market, last active, major sortable metrics, and relationship pair/window.
- Avoid full pairwise recomputation when only a small set changed; use windowed/incremental approaches while retaining reproducibility.
- Establish measured SLOs before launch; initial targets may be p95 <500 ms for cached directory/detail reads, <2 s for normal portfolio search, and published freshness appropriate to each dataset.

## 14. Data quality, security, and privacy

Data-quality gates include source/canonical count reconciliation, duplicate GUID detection, identifier mapping coverage, valid timestamps, no closed trade with impossible exit ordering, finite numeric values, expected outcome totals, currency completeness, regime join coverage, and freshness.

Security requirements:

- least-privilege service identities and role-based access;
- separate public, authenticated user, operator, and admin capabilities;
- encrypted transport and managed secret storage/rotation;
- parameterized queries and strict input/schema validation;
- CSRF/session protections where applicable, secure headers, dependency scanning, patching, and audit logs;
- rate limiting and abuse controls for expensive search/portfolio endpoints;
- privacy minimization and retention controls for users/accounts;
- no broker credentials, account identifiers, internal notes, or raw restricted trade fields in public APIs/logs;
- threat model and security review before broker activation and public launch.

## 15. Testing and validation

### 15.1 Unit/property tests

Normalization (`_S`/`_B`), outcome from `net_return`, cost non-duplication, timestamps, formulas, drawdown, zero denominators, missing values, period bucketing, aligned series, regime joins, scores and constraints.

### 15.2 Integration/contract tests

Source-to-derived reconciliation, idempotent ingestion, backfill equivalence, schema drift, API/OpenAPI contracts, cache invalidation, authorization, broker sandbox and execution reconciliation.

### 15.3 Analytical validation

Golden datasets with hand-calculated metrics; independent implementation spot checks; no look-ahead; temporal holdouts/walk-forward; sensitivity to windows/thresholds; bootstrap/confidence stability; survivorship/selection-bias tests; portfolio comparisons against equal-weight and simple baselines.

### 15.4 UI/accessibility/performance

End-to-end journeys, empty/stale/insufficient/error states, keyboard and screen-reader usability, contrast/responsiveness, cross-browser checks, load/concurrency tests and query-plan review.

### 15.5 Release gates

No public metric without definition, owner, evidence source, test, version, quality state, and disclosure. No broker deployment without sandbox evidence, idempotency, risk controls, reconciliation, audit, and explicit authorization.

## 16. Observability and operational evidence

Use structured logs with correlation/run IDs, metrics, traces, immutable run manifests, dashboards, alerts, and runbooks. Each production workflow node must produce evidence: migration/checksum, test report, reconciliation output, screenshot/API sample, performance result, approval, or monitored rollout signal. Avoid logging secrets or unnecessary trade/account payloads.

## 17. Multi-market scaling

Represent market, venue, instrument, currency, tick/contract value, trading calendar/session, quantity convention, and margin independently. Market adapters translate raw source data into the canonical trade contract. Analytics must compare like-for-like units or use explicit normalized returns/capital. Regime features and thresholds are market/instrument/version specific. Begin with FX, validate one futures or crypto pilot privately, then broaden only after data quality, cost/execution semantics, and disclosures are correct.

## 18. Phased rollout

### Phase 0 — contracts and governance

Lock identity/source semantics, definition registry, metric dictionary, regime methodology, public/private boundaries, quality gates, threat model, and success measures.

### Phase 1 — foundation

Build schemas, canonical views, ingestion, quarantine/reconciliation, empty directory shell and test fixtures.

### Phase 2 — population and baseline analytics

Register 300–500 fixed DNA strategies, ingest closed/open trades, publish evidence-aware headline and period analytics internally.

### Phase 3 — empirical calibration and private directory

Observe population distributions; set versioned score/band thresholds; deliver list/detail/compare to internal users. Do not force labels when evidence is insufficient.

### Phase 4 — relationships and regimes

Deliver objective regime joins, correlation/downside/drawdown overlap, complementarity and robustness evidence.

### Phase 5 — portfolio intelligence

Release constrained portfolio search/builder with reproducible rationale, backtests, holdouts and baseline comparisons.

### Phase 6 — platform/broker pilot

Add deployment preview, sandbox integration, risk gates, monitoring, reconciliation and tightly controlled private activation.

### Phase 7 — public beta and launch

Security/performance/accessibility review, disclosures, support/runbooks, staged traffic, telemetry, rollback, then public launch.

### Phase 8 — market expansion

Pilot futures/crypto/other liquid electronic markets through adapters and market-specific validation.

## 19. Product success measures

- users can find a qualifying strategy or portfolio and understand why it qualifies;
- search-to-detail, compare, save/watchlist and portfolio-builder completion;
- evidence/methodology engagement and low unsupported-claim incidents;
- analytical reconciliation and freshness SLO attainment;
- portfolio suggestions outperform simple baselines on explicitly chosen risk/diversification objectives in holdout tests (not necessarily raw return);
- deployment preview-to-activation reliability, reconciliation accuracy and safety-control performance;
- zero identity collisions, cost double-counting, or Non-DNA/DNA commingling.

## 20. Definition of done

The directory is complete for initial public launch when:

- canonical semantics above are enforced and tested;
- 300–500 immutable DNA strategies are registered with full lineage;
- closed/open data are correctly separated and reconciled;
- strategy, stats, period, regime, relationship and portfolio schemas are live/versioned;
- formulas and methodology are documented, tested and visible;
- directory, strategy, compare and portfolio journeys meet accessibility/performance targets;
- every score/recommendation has evidence, sufficiency, freshness and limitations;
- APIs, caching, security, data quality, observability and runbooks pass release gates;
- broker functionality, if launched, passes sandbox/risk/audit gates;
- public disclosures and rollback plans are approved;
- Non-DNA remains an isolated research/validation facility.

## 21. Instructions for the subsequent implementation model

1. Treat this document and the two companion workflow files as the baseline contract; do not reinterpret the canonical semantics.
2. Inspect the actual repository, database dialect, migrations, existing APIs/UI, infrastructure and tests before selecting technologies or editing code.
3. Produce a requirements-to-code traceability matrix and identify assumptions/gaps. Validate especially exit-time semantics, currencies/capital basis, source update behaviour, and market data availability.
4. Implement in vertical slices following the phase workflow. Preserve raw data and use migrations; do not alter the trading engine merely to fit the directory.
5. Start with deterministic identity normalization and golden analytical fixtures. Make every pipeline idempotent, versioned, observable and backfillable.
6. Build the visual implementation and user-value workflows from the companion Markdown files. Render phases as lanes and node cards; each node must expose dependencies, steps, acceptance criteria, evidence/output and status. Add dependency edges, filters, node detail panels, status legend, progress, deep links and export/print support. Match the spirit of The Tech Principle workflow without copying protected branding or code.
7. Maintain status placeholders in the workflow source or a linked machine-readable manifest so the visual remains auditable.
8. Do not publish regime/classification/portfolio claims until their evidence thresholds and validation gates pass. Render honest “collecting data” and “insufficient evidence” states.
9. Run unit, integration, analytical, security, accessibility and performance validation. Attach concrete evidence to each completed node.
10. Finish with deployment/runbooks, migrations, OpenAPI documentation, metric dictionary, methodology pages, test reports, screenshots, monitoring links, risk register, and a launch/rollback report.

## 22. Companion artifacts

- `dna_strategy_directory_implementation_workflow.md` — build phases, dependency graph, nodes and evidence gates.
- `dna_strategy_directory_user_value_workflow.md` — trader questions mapped backwards to data, intelligence, UI, trust, capabilities and success measures.

