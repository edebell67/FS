# DNA Strategy Directory — Trader/User Value Workflow

**Purpose:** engineer the product backwards from valuable trader questions rather than forwards from available analytics.  
**Status:** `[NOT STARTED]`  
**Owner:** `[TBD]`  
**Last updated:** `[YYYY-MM-DD]`

## 1. Value model

```mermaid
flowchart LR
  Q[User question] --> I[Intent and constraints]
  I --> D[Required data]
  D --> X[Derived intelligence]
  X --> U[UI answer and action]
  U --> E[Evidence, trust and limitations]
  E --> O[User outcome]
  O --> M[Measure success and learn]
```

The core promise is not “here are 500 strategies.” It is: “state what you are trying to achieve, receive a grounded answer, inspect its evidence, compare alternatives, and take a safe next action.”

Global trust semantics:

- Directory population is DNA only; Non-DNA is research/validation/what-if evidence and must be labelled separately.
- DNA is randomly generated once, then fixed/perpetual.
- `DNA_102001_S` and `DNA_102001_B` are one directory identity, `DNA_102001`; `signal` supplies direction.
- Closed-trade history comes from `combined_trades_closed`; current state comes from `combined_trades_open`.
- `target reached` can be a gain or loss; `net_return` determines outcome.
- Costs are already in trade results and are not deducted again.
- All historical evidence is descriptive, not a guarantee.

## 2. User-value node template

Each `UV-*` node should render as a clickable card with: user, trigger, question, intent, inputs, intelligence, UI response, action, evidence/trust, capabilities, success criteria, failure/empty state, status and owner.

## 3. Discover and orient

### UV-001 — “What is this directory, and can I trust what I am seeing?”

- **Status/owner:** `[NOT STARTED]` / `[TBD]`
- **Intent:** understand the product, DNA semantics, evidence basis and limitations before making choices.
- **Required data/intelligence:** strategy population/count; definition immutability; source coverage/freshness; methodology and quality status.
- **UI response:** short orientation; DNA vs Non-DNA boundary; glossary; evidence badges; methodology/disclosure links; as-of date.
- **Evidence/trust:** explain fixed DNA creation, identity normalization, closed/open separation, cost treatment, outcome semantics, missing/insufficient states and version history.
- **Capabilities:** public overview, glossary, methodology pages, status/freshness service.
- **Success criteria:** user correctly distinguishes a DNA strategy, open position, historical result, score and research dataset; reduced early abandonment/confusion.
- **Failure state:** if freshness or quality fails, show the issue and limit claims instead of showing stale confidence.

### UV-002 — “Show me the available strategies without overwhelming me.”

- **Status/owner:** `[NOT STARTED]` / `[TBD]`
- **Intent:** scan a large initial population quickly.
- **Inputs:** market/product, evidence threshold, preferred columns/cards.
- **Required data/intelligence:** canonical master, headline stats, coverage, lifecycle/visibility, quality.
- **UI response:** fast list/cards with understandable default columns, transparent sort, filters, pagination and saved/shareable views.
- **Evidence/trust:** units, sample size, period, freshness and insufficient-data badge on every row.
- **Capabilities:** indexed/filterable list API, cache/search, responsive accessible directory.
- **Success criteria:** median time to first relevant detail view; filter completion; low confusion about sort and units.
- **Failure state:** show why no results match and which constraints are binding.

## 4. Find a strategy for a stated need

### UV-101 — “I have £5,000. What strategies are appropriate for me?”

- **Status/owner:** `[NOT STARTED]` / `[TBD]`
- **Intent:** find strategies/portfolios feasible for available capital, not merely high-returning.
- **Inputs:** capital/base currency, broker/market, maximum drawdown tolerance, number of strategies, sizing constraints.
- **Required data/intelligence:** valid capital/margin model, quantity/minimum size, currency conversion, drawdown/activity, eligibility and broker capability.
- **UI response:** feasible candidates or portfolio options; expected historical drawdown/range; allocation; excluded options with reasons; warning if capital model is unavailable.
- **Evidence/trust:** sizing and margin assumptions, basis/as-of, stress/sensitivity, costs/slippage disclosure (without double-counting source costs), historical-not-guaranteed notice.
- **Capabilities:** capital suitability service, broker/instrument metadata, constrained portfolio search, preview.
- **Success criteria:** no infeasible recommendation; user can explain allocation and binding constraints; preview completion.
- **Failure state:** “cannot determine” rather than inventing a capital band.

### UV-102 — “Show me consistent strategies rather than one-hit wonders.”

- **Status/owner:** `[NOT STARTED]` / `[TBD]`
- **Intent:** prefer return distribution across time over concentrated total P&L.
- **Inputs:** minimum history/trades, period granularity, drawdown limit.
- **Required data/intelligence:** period/rolling series, profitable-period ratio, top-period/trade concentration, dispersion, drawdown, consistency components.
- **UI response:** ranked/filtered candidates with sparklines, profitable months, concentration and consistency breakdown.
- **Evidence/trust:** raw periods and score formula/version; warn when a short sample creates unstable consistency.
- **Capabilities:** period analytics, score calibration, filters, explanation drawer.
- **Success criteria:** chosen strategy meets declared consistency thresholds in validation/holdout evidence; users inspect components rather than relying only on score.

### UV-103 — “Find lower-drawdown strategies.”

- **Status/owner:** `[NOT STARTED]` / `[TBD]`
- **Intent:** constrain path risk.
- **Inputs:** monetary or percentage drawdown limit, capital basis, evidence window.
- **Required data/intelligence:** equity curve, peak/trough/recovery, current and maximum drawdown, duration, sizing/capital basis.
- **UI response:** filtered results and drawdown paths; recovery history; trade-off versus return/activity.
- **Evidence/trust:** never show percentage without valid denominator; expose drawdown window, worst episode and unresolved drawdown.
- **Capabilities:** drawdown engine, charts, unit compatibility validation.
- **Success criteria:** zero unit/basis misunderstandings; users can compare severity and duration, not only a single number.

### UV-104 — “I need frequent opportunities” / “I prefer selective trading.”

- **Status/owner:** `[NOT STARTED]` / `[TBD]`
- **Intent:** align activity with attention, operational load and capital usage.
- **Inputs:** trades/day range, holding time, active session/product, concurrency preference.
- **Required data/intelligence:** trade counts per active/calendar day, holding distributions, open-trade concurrency, activity continuity.
- **UI response:** activity filter and calendar/distribution; show inactive/stale periods and estimated operational burden.
- **Evidence/trust:** denominator and observation window; historical activity is not a promise of future frequency.
- **Capabilities:** behaviour analytics, filter, open-state aggregation.
- **Success criteria:** selected candidates fit declared activity band; fewer surprises about inactivity/concurrency.

### UV-105 — “Does it rely on BUY or SELL trades?”

- **Status/owner:** `[NOT STARTED]` / `[TBD]`
- **Intent:** understand directional dependence and balance.
- **Inputs:** desired BUY/SELL/balanced behaviour.
- **Required data/intelligence:** `signal` split, return/win rate/trades by direction, direction-balance score.
- **UI response:** BUY vs SELL comparison and filter; explain canonical suffix normalization.
- **Evidence/trust:** direction comes from `signal`, not `_S`/`_B`; show sample counts and unequal-exposure warning.
- **Capabilities:** canonical normalization, directional analytics, compare UI.
- **Success criteria:** no duplicate identities or suffix-based misclassification; user can identify directional dependence.

## 5. Evaluate one strategy deeply

### UV-201 — “How has DNA_102001 actually performed?”

- **Status/owner:** `[NOT STARTED]` / `[TBD]`
- **Intent:** assess historical return, risk, consistency and trade behaviour.
- **Required data/intelligence:** headline/period stats, equity/drawdown, distribution, MFE/MAE, coverage and quality.
- **UI response:** overview followed by interactive performance, drawdown, period, distribution and behaviour sections.
- **Evidence/trust:** source/window/units/sample/freshness/methodology; explicit close-type/outcome and cost explanations.
- **Capabilities:** detail API/UI, charts, methodology links, data-quality state.
- **Success criteria:** all displayed metrics reconcile to API/golden data; users find both strengths and limitations.

### UV-202 — “Is the apparent performance robust or dependent on a few trades/periods?”

- **Status/owner:** `[NOT STARTED]` / `[TBD]`
- **Intent:** detect fragility and concentration.
- **Required data/intelligence:** top-N trade/period contribution, rolling/subperiod results, bootstrap/confidence, streaks and sample sufficiency.
- **UI response:** concentration warning, rolling chart, best/worst subperiods, results excluding top contributors as sensitivity—not as replacement history.
- **Evidence/trust:** preserve full history; disclose exploratory sensitivity; never cherry-pick a favourable window.
- **Capabilities:** robustness service, sensitivity UI.
- **Success criteria:** users can identify concentrated strategies; fragile evidence is not presented with high confidence.

### UV-203 — “What is it doing right now?”

- **Status/owner:** `[NOT STARTED]` / `[TBD]`
- **Intent:** inspect current activity without confusing unrealized and historical results.
- **Required data/intelligence:** `combined_trades_open`, latest prices/returns, timestamps, source health; historical context separately.
- **UI response:** clearly labelled open-trades panel, as-of time, unrealized state and stale indicator.
- **Evidence/trust:** open state never included in closed-trade headline; privacy/access rules; no execution guarantee.
- **Capabilities:** low-latency open-state endpoint/cache, freshness monitor.
- **Success criteria:** no open/closed reconciliation confusion; stale data visibly blocks real-time interpretation.

### UV-204 — “Why did this trade count as a win or loss?”

- **Status/owner:** `[NOT STARTED]` / `[TBD]`
- **Intent:** understand trade-level semantics.
- **Required data/intelligence:** net result, exit method, commission field, target boundaries, timestamps and excursions.
- **UI response:** trade detail: outcome from `net_return`; close reason separately; costs-treated statement; MFE/MAE timeline if allowed.
- **Evidence/trust:** `target reached` may be profit or loss; costs already included; source lineage visible to authorized users.
- **Capabilities:** trade explanation component, calculation glossary.
- **Success criteria:** zero UI copy equates `target reached` with profit; support queries on outcome semantics decline.

## 6. Understand market behaviour

### UV-301 — “Which strategies historically did well in rising, falling, or sideways markets?”

- **Status/owner:** `[NOT STARTED]` / `[TBD]`
- **Intent:** discover regime-sensitive behaviour.
- **Inputs:** market/instrument, regime, minimum evidence, window.
- **Required data/intelligence:** objective directional regime observations joined as-of to trades; regime performance/lift and confidence.
- **UI response:** regime filter and matrix with sample counts, comparative lift and `collecting data`/`insufficient evidence` states.
- **Evidence/trust:** exact regime definition/version/lookback; no hindsight threshold selection or future data; warn about instability.
- **Capabilities:** market data, regime engine, leakage tests, regime API/UI.
- **Success criteria:** all claims meet sufficiency/stability gates; users can inspect definitions and evidence.

### UV-302 — “Which strategies handled high or low volatility?”

- **Status/owner:** `[NOT STARTED]` / `[TBD]`
- **Intent:** match exposure to volatility conditions.
- **Required data/intelligence:** market-specific volatility regimes, strategy stats by regime, drawdown and tail/excursion behaviour.
- **UI response:** volatility-regime comparison with risk/return trade-off and confidence.
- **Evidence/trust:** instrument-specific thresholds and version; avoid universal high/low definitions across unlike markets.
- **Capabilities:** volatility features, regime service, market adapters.
- **Success criteria:** no cross-market threshold misuse; behaviour remains reasonably stable in validation subperiods.

### UV-303 — “What happens when the regime changes?”

- **Status/owner:** `[NOT STARTED]` / `[TBD]`
- **Intent:** assess transition risk rather than static averages.
- **Required data/intelligence:** regime sequence/transition labels, rolling strategy behaviour, lag and drawdown around transitions.
- **UI response:** transition timeline/scenarios and explicit uncertainty; initially `not enough evidence` if unavailable.
- **Evidence/trust:** no claim that regimes are known prospectively unless a live classifier genuinely provides it; disclose classification lag.
- **Capabilities:** versioned regime timeline, transition analysis, monitoring.
- **Success criteria:** users understand retrospective vs live classification; no false precision.

## 7. Combine strategies and build portfolios

### UV-401 — “I already trade DNA_102001. What can I add that behaves differently?”

- **Status/owner:** `[NOT STARTED]` / `[TBD]`
- **Intent:** find complements rather than another similar strategy.
- **Inputs:** existing strategy, eligible markets, capital/strategy count, constraints.
- **Required data/intelligence:** aligned series, correlation, downside correlation, joint losses, drawdown overlap, independent activity, regime complementarity.
- **UI response:** complementary candidates ranked with a component-by-component rationale; compare combined vs original path.
- **Evidence/trust:** alignment frequency/window, overlap sample, stability, confidence and limitations; do not rely solely on ordinary correlation.
- **Capabilities:** relationship engine/API, complementarity ranking, add-to-builder action.
- **Success criteria:** selected addition improves declared diversification/risk objective in holdout/baseline evidence; user understands why.

### UV-402 — “Which strategies are basically duplicates?”

- **Status/owner:** `[NOT STARTED]` / `[TBD]`
- **Intent:** avoid redundant exposure.
- **Required data/intelligence:** return/downside correlation, drawdown/loss overlap, behaviour clusters, common exposure.
- **UI response:** similarity cluster and redundant-exposure warning with alternatives.
- **Evidence/trust:** cluster/version/window and raw relationship components; similarity is behavioural, not proof of identical logic.
- **Capabilities:** clustering, relationship visual, portfolio concentration checker.
- **Success criteria:** portfolios reduce redundant members/effective concentration.

### UV-403 — “Build me a diversified portfolio of five strategies.”

- **Status/owner:** `[NOT STARTED]` / `[TBD]`
- **Intent:** obtain a feasible, understandable combination.
- **Inputs:** five-strategy limit, capital, market, risk/drawdown, activity, regime/objective and allocation bounds.
- **Required data/intelligence:** eligible universe, validated stats/relationships/regimes, sizing, optimizer and baselines.
- **UI response:** several candidate portfolios, allocations, combined curve/drawdown, contribution, regime/scenario table, exclusions and sensitivity; save/share/export.
- **Evidence/trust:** reproducible run ID/version/seed, train/holdout or walk-forward results, baseline comparison, assumptions and infeasibility explanations.
- **Capabilities:** constrained search/optimizer, portfolio stats, run manifest, builder UI/API.
- **Success criteria:** constraints always hold; diversification improvement is demonstrated against simple/high-return/equal-weight baselines; explanation comprehension.

### UV-404 — “I want rising-market participation plus neutral/offsetting strategies.”

- **Status/owner:** `[NOT STARTED]` / `[TBD]`
- **Intent:** combine different regime roles to seek a smoother outcome/alpha without pretending certainty.
- **Inputs:** desired core regime exposure, neutral/offset allocation, capital and risk constraints.
- **Required data/intelligence:** regime response vectors, relationships, contribution, scenario/transition performance.
- **UI response:** core + diversifier portfolio decomposition; explain role of every member and trade-offs.
- **Evidence/trust:** role is observed and versioned, not a marketing label; show sparse/unstable regimes and holdout behaviour.
- **Capabilities:** regime-aware portfolio construction and explanation.
- **Success criteria:** each member has measurable marginal role; combined risk/regime profile matches declared objective in validation.

### UV-405 — “What if one strategy stops working or is paused?”

- **Status/owner:** `[NOT STARTED]` / `[TBD]`
- **Intent:** understand concentration and replacement options.
- **Required data/intelligence:** contribution/concentration, lifecycle/health, remove-one sensitivity, eligible complements.
- **UI response:** portfolio impact, replacement candidates, rebalance preview and warnings—no automatic action without authorization.
- **Evidence/trust:** current lifecycle/freshness, reason for pause, recomputation version, taxes/costs/rebalance limitations where relevant.
- **Capabilities:** lifecycle monitor, portfolio sensitivity, rebalance preview.
- **Success criteria:** user can maintain constraints after removal; paused strategy triggers no new deployment.

## 8. Research, validation, and what-if questions

### UV-501 — “Can I test a new idea quickly against historical minute-by-minute opportunities?”

- **Status/owner:** `[NOT STARTED]` / `[TBD]`
- **Intent:** rapid exploratory what-if/backtest using the Non-DNA warehouse.
- **Inputs:** entry rule/time, BUY/SELL, horizon/exit, product, sizing and evaluation period.
- **Required data/intelligence:** isolated Non-DNA continuous trade warehouse, historical price/trade state, reproducible query and bias controls.
- **UI response:** explicitly labelled research result with assumptions, sample, distribution and comparison; never add the idea to DNA directory automatically.
- **Evidence/trust:** source lineage; research/not-live label; no look-ahead; multiple-testing and execution caveats; fixed query manifest.
- **Capabilities:** permissioned what-if engine, reusable run IDs, validation report/export.
- **Success criteria:** result is reproducible; DNA/Non-DNA never commingle; exploratory findings require independent validation before promotion.

### UV-502 — “Can Non-DNA evidence validate a DNA claim?”

- **Status/owner:** `[NOT STARTED]` / `[TBD]`
- **Intent:** seek an independent supporting or contradictory lens.
- **Required data/intelligence:** comparable event definition, isolated datasets, matching market/time context, predeclared validation rule.
- **UI response:** validation panel that states support/contradiction/inconclusive, never substitutes Non-DNA P&L into DNA history.
- **Evidence/trust:** dataset independence/overlap, matching criteria, power/sample, pre-registration/version.
- **Capabilities:** research validation service and governance gate.
- **Success criteria:** validation cannot change canonical DNA metrics; inconclusive evidence remains inconclusive.

## 9. Deploy, monitor, and manage

### UV-601 — “Can I deploy this portfolio to my broker/platform?”

- **Status/owner:** `[NOT STARTED]` / `[TBD]`
- **Intent:** turn a researched portfolio into controlled execution.
- **Inputs:** broker/account, capital, sizing, products, risk limits and consent.
- **Required data/intelligence:** broker capabilities, instrument mapping, margin, account permissions, allocation, health and risk checks.
- **UI response:** deployment preview, supported/unsupported items, exposure/margin/risk summary, explicit confirmation; activation status.
- **Evidence/trust:** historical vs executable distinction; broker/cost/slippage/latency assumptions; permissions; immutable audit.
- **Capabilities:** broker abstraction, secret vault, sandbox, risk gates, idempotent intents.
- **Success criteria:** no unauthorized activation; sandbox and risk checks pass; intended and broker state reconcile.

### UV-602 — “Is my deployed strategy healthy?”

- **Status/owner:** `[NOT STARTED]` / `[TBD]`
- **Intent:** see data, strategy and execution health in one place.
- **Required data/intelligence:** heartbeats, freshness, intended/broker positions, rejects/fills, lifecycle, behavioural drift and limits.
- **UI response:** health status, issues, impact, last good timestamp and safe actions (pause/disable/support).
- **Evidence/trust:** separate performance drift from system failure; show alert cause and audit trail.
- **Capabilities:** monitoring, reconciliation, drift rules, notifications/runbooks.
- **Success criteria:** critical faults detected within SLO; no silent stale execution; users/operators can safely pause.

### UV-603 — “Why was a strategy paused, retired, or excluded?”

- **Status/owner:** `[NOT STARTED]` / `[TBD]`
- **Intent:** understand lifecycle decisions and preserve trust/history.
- **Required data/intelligence:** lifecycle event, trigger, quality/health/drift evidence, approving actor and replacement impact.
- **UI response:** status banner, reason/timestamp, historical continuity, deployment consequence and permitted next action.
- **Evidence/trust:** immutable audit and policy version; never erase poor history; distinguish automatic flag from human decision.
- **Capabilities:** lifecycle state machine, audit API/UI, portfolio impact.
- **Success criteria:** every transition is traceable; retired records remain historically accessible; no new deployment while paused.

## 10. Expand across markets

### UV-701 — “Can I compare FX with futures or crypto strategies?”

- **Status/owner:** `[NOT STARTED]` / `[TBD]`
- **Intent:** broaden diversification across liquid electronic markets.
- **Inputs:** markets, base currency, capital, sessions and risk constraints.
- **Required data/intelligence:** canonical instruments/calendars/currencies/contracts, normalized capital/return basis, market-specific regimes and costs/execution semantics.
- **UI response:** compatible cross-market comparison and portfolio view; prevent invalid unit comparisons.
- **Evidence/trust:** conversion rates/timestamps, market-specific methodology, liquidity/session and broker availability disclosures.
- **Capabilities:** adapter framework, FX conversion, cross-market portfolio engine.
- **Success criteria:** calculations reconcile within each market and after normalization; no universal regime/cost assumptions.

## 11. Cross-cutting product capabilities generated by the questions

| Capability | Driven by nodes | Minimum acceptance |
|---|---|---|
| Canonical strategy registry | UV-001, 105, 201 | suffix normalization, immutable definition, lineage |
| Historical/open data separation | UV-001, 203, 204 | closed metrics never include open trades |
| Metric/period engine | UV-102–104, 201–202 | golden tests, units/windows/sufficiency |
| Regime engine | UV-301–303, 404 | objective frozen definitions, no leakage |
| Relationship engine | UV-401–402 | aligned series, downside/drawdown overlap, stability |
| Portfolio engine | UV-101, 403–405 | constraints, reproducible runs, baselines/holdouts |
| Non-DNA research service | UV-501–502 | isolated and visibly labelled |
| Explainability/evidence | all | source, window, sample, version, as-of, limitations |
| Broker operations | UV-601–603 | confirmation, risk gates, reconciliation, audit |
| Multi-market adapters | UV-701 | explicit units/calendars/contracts/currency |

## 12. End-to-end user journeys and gates

### Journey A — Explore to shortlist

`UV-001 -> UV-002 -> one or more of UV-102/103/104/105 -> UV-201/202 -> compare/save`

Gate: the user can state why each shortlisted strategy fits and what evidence is weak.

### Journey B — Existing strategy to complement

`UV-201 -> UV-401 -> UV-402 -> UV-403 -> save/export`

Gate: combined evidence improves the declared diversification objective versus the original/simple baseline.

### Journey C — Capital to feasible portfolio

`UV-101 -> UV-403/404 -> sensitivity UV-405 -> deployment preview UV-601`

Gate: capital/sizing/margin assumptions are valid, constraints hold, and activation requires explicit confirmation.

### Journey D — Research to validated candidate

`UV-501 -> UV-502 -> governed DNA generation/new immutable ID -> collect closed trades -> normal eligibility process`

Gate: exploratory Non-DNA result never bypasses independent evidence or becomes a directory strategy directly.

### Journey E — Live monitoring

`UV-203/602 -> issue -> UV-603 -> UV-405 -> safe pause/rebalance preview`

Gate: current state, historical evidence and system health remain separate and auditable.

## 13. Measurement framework

Measure outcomes, not just clicks:

- time to a qualifying shortlist/portfolio;
- search-to-detail, compare, save and builder completion;
- percentage of users who can correctly explain outcome, drawdown basis, regime evidence and complementarity rationale;
- zero unsupported claim, identity collision, cost-double-counting and DNA/Non-DNA commingling incidents;
- proportion of recommendations with sufficient/stable evidence;
- portfolio constraint validity and holdout/baseline diversification improvement;
- stale-data detection and execution reconciliation SLOs;
- user-reported trust, usefulness and surprise after live observation.

Guard against optimizing engagement at the expense of safe interpretation. Do not rank or recommend because it increases clicks.

## 14. Visual workflow requirements

Render user-intent lanes: **Orient**, **Discover**, **Evaluate**, **Regimes**, **Combine**, **Research**, **Deploy/Monitor**, **Expand**. Each `UV-*` node opens the full specification. Show edges for the journeys above and optionally a reverse dependency view from user question to capability/data source. Filters: persona, intent, market, maturity, evidence state, status and owner. Include a persistent trust legend distinguishing raw facts, derived metrics, classifications, recommendations and live state.

## 15. Instructions for the subsequent product/implementation model

1. Use these user questions as acceptance scenarios and requirements generators; link every screen, API and analytical job to at least one `UV-*` node.
2. Prototype the user answer first using honest empty/insufficient states, then implement the smallest data/intelligence path that can support it correctly.
3. Preserve all canonical semantics and keep Non-DNA isolated.
4. Implement evidence components once and reuse them everywhere: source, as-of/window, sample, sufficiency, methodology/version, limitations.
5. Test comprehension with representative traders, not only task completion. Record whether users can distinguish return from outcome method, historical from live, correlation from diversification, and research from directory evidence.
6. Generate the interactive visual workflow from the structured `UV-*` nodes and keep its status/evidence synchronized with the implementation workflow.
7. Reject any feature that produces a confident answer without sufficient data, valid units/denominators, independent regime definitions, or reproducible portfolio evidence.
8. Attach screenshots, API examples, golden analytical outputs, user-test results and approvals to completed nodes.

