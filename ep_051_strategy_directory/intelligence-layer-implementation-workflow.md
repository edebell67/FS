# Intelligence Layer Implementation Workflow

## Handoff-ready implementation specification

### Purpose

This specification translates two Collective2-derived observations into an implementable Intelligence Layer for a trading-strategy directory:

1. **Natural-language strategy discovery** — users can ask questions such as: *“Show me stock strategies with >60% win rate, <10% drawdown and >20% annual return.”*
2. **Strategy-as-a-product intelligence** — every strategy becomes a structured entity that can be searched, compared, scored, ranked, watched and eventually acted upon.

The Intelligence Layer becomes the brain behind the directory. It sits between raw strategy and market data and the user-facing discovery experience.

---

## 1. End-to-end workflow

```text
┌───────────────────────────────────────────────┐
│  1. STRATEGY INGESTION                        │
│                                               │
│  Backtests / Live Results / Uploaded Strategy │
│  Existing Strategy Database                   │
└──────────────────────┬────────────────────────┘
                       ↓
┌───────────────────────────────────────────────┐
│  2. STRATEGY NORMALISATION                    │
│                                               │
│  Convert every strategy into common schema:   │
│                                               │
│  • Name                                       │
│  • Asset / Market                             │
│  • Strategy type                              │
│  • Timeframe                                  │
│  • Long / Short                               │
│  • Return / CAGR                              │
│  • Sharpe / Sortino                           │
│  • Max drawdown                               │
│  • Win rate                                   │
│  • Profit factor                              │
│  • Trade count                                │
│  • Volatility                                 │
│  • Exposure                                   │
│  • Backtest period                            │
│  • Live period                                │
│  • Parameters                                 │
│  • Regime performance                         │
└──────────────────────┬────────────────────────┘
                       ↓
┌───────────────────────────────────────────────┐
│  3. METRIC / FEATURE ENGINE                   │
│                                               │
│  Calculate derived intelligence               │
│                                               │
│  Risk-adjusted return                         │
│  Stability                                    │
│  Drawdown recovery                            │
│  Return consistency                           │
│  Trade expectancy                             │
│  Regime sensitivity                           │
│  Parameter robustness                         │
│  Backtest/live divergence                     │
│  Strategy correlation                         │
└──────────────────────┬────────────────────────┘
                       ↓
┌───────────────────────────────────────────────┐
│  4. STRATEGY INTELLIGENCE PROFILE             │
│                                               │
│  Every strategy becomes a searchable          │
│  "product"                                    │
│                                               │
│  Performance                                  │
│  Risk                                         │
│  Behaviour                                    │
│  Market suitability                           │
│  Regime suitability                           │
│  Reliability                                  │
│  Evidence quality                             │
└──────────────────────┬────────────────────────┘
                       ↓
             ┌─────────┴───────────┐
             ↓                     ↓
┌──────────────────────────┐ ┌──────────────────────────┐
│ 5A. STRUCTURED FILTERING │ │ 5B. INTELLIGENT SEARCH  │
│                          │ │                          │
│ Asset                    │ │ Natural language query   │
│ Strategy type            │ │                          │
│ Return                   │ │ "Show me stock           │
│ Win rate                 │ │ strategies with >60%    │
│ Drawdown                 │ │ win rate and >20%       │
│ Sharpe                   │ │ return"                  │
│ Timeframe                │ │                          │
│ Regime                   │ │          ↓               │
│ Trade frequency          │ │ Query interpretation     │
└─────────────┬────────────┘ │          ↓               │
              │              │ Structured filters       │
              │              └────────────┬─────────────┘
              └──────────────┬────────────┘
                             ↓
┌───────────────────────────────────────────────┐
│  6. CANDIDATE STRATEGY RETRIEVAL              │
│                                               │
│  Return every strategy meeting constraints    │
└──────────────────────┬────────────────────────┘
                       ↓
┌───────────────────────────────────────────────┐
│  7. INTELLIGENCE RANKING ENGINE               │
│                                               │
│  Don't simply rank by return.                 │
│                                               │
│  Calculate composite scores:                  │
│                                               │
│  Performance Score                            │
│  Risk Score                                   │
│  Robustness Score                             │
│  Consistency Score                            │
│  Regime Fit Score                             │
│  Evidence Confidence                          │
│                                               │
│              ↓                                │
│                                               │
│       Strategy Quality Score                  │
└──────────────────────┬────────────────────────┘
                       ↓
┌───────────────────────────────────────────────┐
│  8. RESULTS / MARKETPLACE VIEW                │
│                                               │
│ Strategy     Return  DD   WR  Sharpe  Score    │
│ Strategy A    26%    7%  62%   2.1    91      │
│ Strategy B    31%   14%  67%   1.7    83      │
│ Strategy C    22%    5%  59%   2.4    94      │
│                                               │
│ Compare | Watch | Analyse | Open Strategy     │
└──────────────────────┬────────────────────────┘
                       ↓
┌───────────────────────────────────────────────┐
│  9. STRATEGY DETAIL INTELLIGENCE              │
│                                               │
│ Overview                                      │
│ Returns                                       │
│ Equity / Net Returns Curve                    │
│ Drawdowns                                     │
│ Trade Analysis                                │
│ Risk                                          │
│ Regime Analysis                               │
│ Parameter Sensitivity                         │
│ Rolling Performance                           │
│ Benchmark Comparison                          │
│ Similar Strategies                            │
│ Correlated Strategies                         │
│ Intelligence Summary                          │
└──────────────────────┬────────────────────────┘
                       ↓
┌───────────────────────────────────────────────┐
│ 10. COMPARE ENGINE                            │
│                                               │
│ Strategy A vs B vs C                          │
│                                               │
│ Return                                        │
│ Risk                                          │
│ Drawdown                                      │
│ Consistency                                   │
│ Regime                                        │
│ Trade behaviour                               │
│ Correlation                                   │
│ Robustness                                    │
└──────────────────────┬────────────────────────┘
                       ↓
┌───────────────────────────────────────────────┐
│ 11. USER INTELLIGENCE                         │
│                                               │
│ Watchlist                                     │
│ Saved searches                                │
│ Strategy collections                         │
│ Search history                                │
│ Compare history                               │
│ Preferred markets                             │
│ Preferred risk level                         │
└──────────────────────┬────────────────────────┘
                       ↓
┌───────────────────────────────────────────────┐
│ 12. RECOMMENDATION ENGINE                     │
│                                               │
│ "Strategies you may want to investigate"     │
│                                               │
│ Based on:                                     │
│ • Query                                       │
│ • Risk preferences                            │
│ • Market                                      │
│ • Current regime                              │
│ • Strategies watched                         │
│ • Strategies compared                        │
└───────────────────────────────────────────────┘
```

---

## 2. Strategy Intelligence Object

Node 4 is the critical part. A strategy must not be treated merely as a database row; it must be a first-class **Strategy Intelligence Object**.

```text
STRATEGY
│
├── Identity
│   ├── Name
│   ├── Author/source
│   ├── Version
│   └── Description
│
├── Classification
│   ├── Asset class
│   ├── Instruments
│   ├── Strategy family
│   ├── Timeframe
│   └── Long/short
│
├── Performance
│   ├── CAGR
│   ├── Total return
│   ├── Monthly returns
│   └── Annual returns
│
├── Risk
│   ├── Max drawdown
│   ├── Volatility
│   ├── VaR
│   └── Downside deviation
│
├── Risk-adjusted Performance
│   ├── Sharpe
│   ├── Sortino
│   └── Calmar
│
├── Trading Behaviour
│   ├── Win rate
│   ├── Profit factor
│   ├── Expectancy
│   ├── Average holding period
│   └── Trades/year
│
├── Robustness
│   ├── Parameter sensitivity
│   ├── Out-of-sample
│   ├── Walk-forward
│   └── Live/backtest divergence
│
├── Regime Intelligence
│   ├── Bull
│   ├── Bear
│   ├── Trending
│   ├── Sideways
│   ├── High volatility
│   └── Low volatility
│
└── Intelligence
    ├── Quality score
    ├── Risk score
    ├── Robustness score
    ├── Regime-fit score
    └── Confidence score
```

---

## 3. Advanced natural-language finder

This must be its own service, not merely a more attractive search box.

### Example 1: direct constraint translation

User query:

> **Show me equity strategies returning more than 20%, with at least a 60% win rate and maximum drawdown below 10%.**

Internal translation:

```text
asset_class = equity

AND annual_return > 20%

AND win_rate >= 60%

AND max_drawdown <= 10%
```

### Example 2: multi-dimensional strategy search

> Find momentum strategies for US equities that have a Sharpe above 1.5, drawdown below 12%, at least five years of backtest history and performed positively during bear markets.

### Example 3: regime-sensitive search

> Which strategies perform best when volatility is increasing?

### Example 4: current-market suitability

> **What strategies appear best suited to the current market?**

The final query invokes a broader intelligence workflow:

```text
Current Market
      ↓
Market Regime Engine
      ↓
Current regime characteristics
      ↓
Strategy Regime Database
      ↓
Candidate strategies
      ↓
Risk constraints
      ↓
Robustness constraints
      ↓
Similarity to historical conditions
      ↓
Rank
      ↓
Explain WHY
```

The service is responsible for query interpretation, validated query-to-filter translation, retrieval, ranking and an explanation of why each result satisfies the request.

---

## 4. Strategy-as-a-product marketplace model

The second Collective2 observation is important beyond the UI. Adopt this mental model:

> **Every strategy is a product.**

A strategy has a profile, evidence, characteristics, rankings, comparisons, followers/watchers, history and related products.

The directory should behave conceptually like **Amazon, AutoTrader or Rightmove—but for quantitative strategies.**

### Example strategy card

```text
NASDAQ Mean Reversion v3
────────────────────────────────

Quality Score                     91/100

Annual Return                       24.7%
Maximum Drawdown                     6.8%
Sharpe                               2.12
Win Rate                              64%
Track Record                       8.4 yrs

BEST ENVIRONMENT

✓ Sideways markets
✓ High volatility
✓ Bear-market rebounds

WEAKER ENVIRONMENT

✕ Strong persistent trends


Why the Intelligence Engine likes it

• Strong risk-adjusted return
• Drawdown substantially below category median
• Consistent performance across 7/8 years
• Positive out-of-sample results
• Low parameter sensitivity


[Compare]    [Watch]    [Full Analysis]
```

---

## 5. Category-relative intelligence

A Sharpe ratio of 1.5 does not mean much by itself. The Intelligence Layer must calculate relative standing across relevant cohorts.

```text
Strategy Sharpe:       1.56

All strategies:        Top 21%
Momentum strategies:   Top 14%
US equity momentum:    Top 9%
5+ year strategies:    Top 11%
```

The same relative analysis must be available for drawdown, CAGR, win rate, profit factor and other material metrics.

This enables generated intelligence such as:

> **This strategy ranks in the top 9% of comparable US equity momentum strategies for risk-adjusted return.**

That is genuine directory intelligence rather than a simple display of statistics.

---

## 6. Three-layer architecture

The directory should be explicitly separated into three layers:

```text
                   USER
                     │
                     ▼
        ┌────────────────────────┐
        │   DISCOVERY LAYER      │
        │                        │
        │ Search                 │
        │ Natural language       │
        │ Filters                │
        │ Categories             │
        │ Rankings               │
        │ Recommendations        │
        └───────────┬────────────┘
                    │
                    ▼
        ┌────────────────────────┐
        │  INTELLIGENCE LAYER    │
        │                        │
        │ Metric engine          │
        │ Ranking                │
        │ Scoring                │
        │ Regime analysis        │
        │ Comparisons            │
        │ Similarity             │
        │ Explanations           │
        │ Confidence             │
        └───────────┬────────────┘
                    │
                    ▼
        ┌────────────────────────┐
        │     DATA LAYER         │
        │                        │
        │ Strategy definitions   │
        │ Backtests              │
        │ Trades                 │
        │ Returns                │
        │ Market data            │
        │ Parameters             │
        │ Live performance       │
        └────────────────────────┘
```

### Layer responsibilities

- **Discovery Layer:** accepts search, filters and natural-language requests; presents categories, rankings, recommendations, marketplace results, detail pages and comparisons.
- **Intelligence Layer:** normalises metrics; performs ranking, scoring, regime analysis, comparison, similarity analysis, explanation generation and confidence assessment.
- **Data Layer:** stores strategy definitions, backtests, trades, returns, market data, parameters and live performance.

The directory UI must never calculate intelligence itself. It requests computed intelligence from the Intelligence Layer and renders the response.

---

## 7. API interaction examples

### Structured strategy query

```http
GET /strategies?
asset=equity
&min_win_rate=.60
&min_return=.20
&max_drawdown=.10
&sort=quality_score
```

### Natural-language intelligence query

```http
POST /intelligence/query
Content-Type: application/json

{
  "query": "Find robust equity strategies with high win rates and less than 10% drawdown."
}
```

The Intelligence Layer handles interpretation, retrieval, scoring and ranking, then returns the answer to the Discovery Layer.

---

## 8. Phased implementation order

### Phase 1 — Directory foundation

**Strategy schema → metric normalisation → structured filters → strategy directory → detail page.**

Deliver the canonical Strategy Intelligence Object, ingest and normalise strategy data, expose deterministic filters, and render directory and detail views.

### Phase 2 — Comparative intelligence

**Composite intelligence scores → rankings → category percentiles → strategy comparison.**

Add quality, risk, robustness, consistency, regime-fit and confidence scores; cohort-relative rankings; and side-by-side comparison.

### Phase 3 — Intelligent discovery

**Natural-language finder → query-to-filter translation → explanation engine → saved searches/watchlists.**

Translate user intent into structured constraints, provide explainable results, and retain user discovery signals.

### Phase 4 — Regime-aware recommendations

**Market-regime engine → strategy/regime matching → “What works now?” queries → personalised recommendations.**

Classify current conditions, match those conditions against historical strategy behavior, apply risk and robustness constraints, rank candidates and explain each recommendation.

The product progression is:

> **Directory → Search → Compare → Understand → Discover → Recommend.**

This progression slots directly into the strategy-directory workflow rather than becoming a separate application. The **Intelligence Layer becomes the brain behind the directory.**

---

## 9. Implementation acceptance criteria

A conforming implementation should ensure that:

- Every strategy is represented by the common Strategy Intelligence Object.
- Raw and derived metrics are produced by the Intelligence Layer, not the UI.
- Structured filters and natural-language queries resolve to the same canonical query model.
- Search results are constraint-valid before ranking is applied.
- Ranking considers performance, risk, robustness, consistency, regime fit and evidence confidence—not return alone.
- Every composite score and recommendation can be explained in user-readable terms.
- Metrics support category-relative percentiles across multiple cohorts.
- Current-market recommendations pass through regime, risk, robustness and historical-similarity checks.
- Users can compare, watch, analyse and open every marketplace result.
- Saved searches, watchlists and interaction history can feed later personalisation.

