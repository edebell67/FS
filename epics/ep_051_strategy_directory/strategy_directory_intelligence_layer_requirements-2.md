# Strategy Directory — Intelligence Layer Requirements

**Document purpose:** Implementation-ready specification for the Strategy Directory Intelligence Layer, including competitive intelligence requirements and intra-library strategy analysis.

**Status:** Working requirements  
**Scope:** Strategy discovery, evaluation, ranking, comparison, regime analysis, cross-strategy relationships, portfolio intelligence, and decision intelligence.

---

## 1. Product Objective

The Strategy Directory must not operate as a simple catalogue of strategies.

The Intelligence Layer should transform raw strategy and trade data into decision intelligence that allows users to:

- Discover strategies matching explicit performance/risk constraints.
- Ask natural-language questions about strategies.
- Compare strategies on a normalized basis.
- Determine which strategies are statistically credible rather than merely high-performing.
- Understand when and under what market conditions a strategy performs.
- Identify strategies that complement or hedge one another.
- Detect strategy deterioration or behavioural change.
- Discover relationships across the entire strategy library.
- Identify strategies whose behaviour may lead or lag other strategies.
- Identify strategies that behave inversely to others.
- Construct combinations of strategies for objectives such as steady returns, reduced drawdown, regime diversification, and portfolio robustness.

The core product progression is:

**Directory → Search → Compare → Understand → Discover → Combine → Recommend**

---

# 2. Intelligence Architecture

The platform should separate intelligence into three architectural layers.

## 2.1 Data Layer

Responsible for source data and calculated observations:

- Strategy definitions
- Strategy versions
- Closed trades
- Open trades
- Returns
- Net returns
- Backtests
- Live performance
- Market data
- Strategy parameters
- Commission/fees
- Market/regime observations

## 2.2 Intelligence Layer

Responsible for all calculations and interpretation:

- Metric engine
- Performance analysis
- Risk analysis
- Robustness analysis
- Strategy scoring
- Ranking
- Percentile analysis
- Regime analysis
- Strategy comparison
- Strategy similarity
- Correlation
- Lead/lag analysis
- Inverse relationship analysis
- Strategy clustering
- Drawdown propagation
- Strategy health/decay
- Confidence analysis
- Portfolio/combination intelligence
- Explanation generation

## 2.3 Discovery Layer

Responsible for exposing intelligence to users:

- Directory
- Search
- Natural-language finder
- Filters
- Categories
- Rankings
- Strategy detail pages
- Compare
- Watchlist
- Saved searches
- Portfolio builder
- Recommendations
- “What works now?” discovery

The UI should consume intelligence from the Intelligence Layer rather than calculating strategy analytics itself.

---

# 3. End-to-End Intelligence Workflow

## Node 1 — Strategy Ingestion

Sources can include:

- Existing strategy database
- Closed trades
- Open trades
- Backtest results
- Live strategy results
- Uploaded/imported strategies
- Future third-party strategies

## Node 2 — Strategy Normalisation

Convert every strategy into a common schema.

Required fields should include:

- Strategy ID
- Strategy name
- Strategy version
- Author/source
- Asset class
- Product/instrument
- Product type
- Strategy family/type
- Timeframe
- Long/short/both
- Total return
- CAGR/annualised return where applicable
- Sharpe
- Sortino
- Calmar
- Maximum drawdown
- Win rate
- Profit factor
- Expectancy
- Trade count
- Trade frequency
- Average holding period
- Volatility
- Exposure
- Commission/fees
- Backtest period
- Live period
- Strategy parameters
- Regime performance

## Node 3 — Metric / Feature Engine

Calculate derived intelligence such as:

- Risk-adjusted return
- Return consistency
- Drawdown recovery
- Trade expectancy
- Regime sensitivity
- Parameter robustness
- Backtest/live divergence
- Strategy correlations
- Rolling performance
- Performance stability

## Node 4 — Strategy Intelligence Profile

Every strategy becomes a first-class searchable **Strategy Intelligence Object** rather than merely a database row.

The profile should contain:

### Identity
- Name
- ID
- Author/source
- Version
- Description

### Classification
- Asset class
- Instrument
- Strategy family
- Timeframe
- Long/short behaviour

### Performance
- CAGR
- Total return
- Monthly returns
- Annual returns
- Rolling returns

### Risk
- Maximum drawdown
- Volatility
- Downside deviation
- VaR where appropriate
- Drawdown duration/recovery

### Risk-adjusted performance
- Sharpe
- Sortino
- Calmar

### Trading behaviour
- Win rate
- Profit factor
- Expectancy
- Average holding period
- Trade frequency
- TP/SL behaviour
- Long/short performance

### Robustness
- Parameter sensitivity
- Out-of-sample performance
- Walk-forward results
- Live/backtest divergence
- Statistical experience/sample size

### Regime intelligence
- Bull
- Bear
- Trending
- Sideways
- High volatility
- Low volatility
- Other future regime definitions

### Intelligence scores
- Quality Score
- Performance Score
- Risk Score
- Robustness Score
- Consistency Score
- Regime Fit Score
- Confidence Score
- Strategy Health Score

## Node 5 — Discovery

Two parallel discovery mechanisms should be supported.

### Structured filtering

Examples:

- Asset
- Product
- Strategy type
- Return
- Win rate
- Drawdown
- Sharpe
- Timeframe
- Regime
- Trade frequency
- Holding period
- Live/backtest
- Long/short

### Natural-language strategy finder

Example:

> Show me equity strategies returning more than 20%, with at least a 60% win rate and maximum drawdown below 10%.

Translate internally into structured constraints such as:

```text
asset_class = equity
AND annual_return > 20%
AND win_rate >= 60%
AND max_drawdown <= 10%
```

More advanced examples:

> Find momentum strategies for US equities with Sharpe above 1.5, drawdown below 12%, at least five years of history, and positive bear-market performance.

> Which strategies perform best when volatility is increasing?

> Find strategies that perform well when EUR/USD is sideways but do not collapse when volatility rises.

> What strategies appear best suited to the current market?

## Node 6 — Candidate Retrieval

Return strategies meeting explicit constraints before ranking.

## Node 7 — Intelligence Ranking Engine

Do not rank purely by return.

Potential ranking dimensions:

- Performance Score
- Risk Score
- Robustness Score
- Consistency Score
- Regime Fit Score
- Evidence Confidence
- Strategy Health

Produce an overall Strategy Quality Score while retaining the component scores.

## Node 8 — Directory / Marketplace Results

Each strategy should behave like a product.

Results should expose enough intelligence for rapid comparison, with actions such as:

- Open
- Compare
- Watch
- Analyse
- Add to portfolio builder

## Node 9 — Strategy Detail Intelligence

Potential sections:

- Overview
- Returns
- Equity / net returns curve
- Drawdowns
- Trade analysis
- Risk
- Regime analysis
- Parameter sensitivity
- Rolling performance
- Benchmark comparison
- Similar strategies
- Inversely related strategies
- Leading/lagging relationships
- Correlated strategies
- Intelligence summary

## Node 10 — Compare Engine

Compare strategies across:

- Return
- Risk
- Drawdown
- Consistency
- Regime behaviour
- Trade behaviour
- Correlation
- Robustness
- Statistical confidence
- Strategy health

## Node 11 — User Intelligence

Support:

- Watchlists
- Saved searches
- Strategy collections
- Compare history
- Preferred markets
- Preferred risk levels
- Portfolio holdings/selected strategies

## Node 12 — Recommendation Engine

Recommendations can use:

- User query
- Risk preference
- Market
- Current regime
- Watched strategies
- Compared strategies
- Existing portfolio
- Strategy correlation
- Inverse relationships
- Lead/lag relationships
- Robustness
- Strategy health

---

# 4. Competition Match

This section captures the competitive intelligence benchmark.

## 4.1 Collective2-type capabilities

Competitive capabilities worth matching or exceeding include:

- Strong performance metrics
- Strong risk metrics
- Advanced numeric filtering
- Strategy ranking
- Composite ranking/quality concepts
- Risk-of-ruin analysis
- Correlation analysis
- Strategy-as-product presentation
- Watch/simulate/action-oriented user journey

The important product observation is that strategies can be treated as marketplace products that users discover and evaluate rather than simply as rows of statistical results.

## 4.2 Darwinex-type capabilities

Important intelligence concepts include:

- Statistical experience
- Risk stability
- Risk adjustment
- Entry quality
- Exit quality
- Investment capacity
- Composite strategy quality scoring
- Detection of sustained performance and deterioration

This supports our proposed:

- Quality Score
- Robustness Score
- Consistency Score
- Confidence Score
- Strategy Health / Decay Detection

## 4.3 QuantConnect-type capabilities

Important concepts include:

- Continuous strategy evaluation
- Out-of-sample evidence
- Ranking incorporating performance and evidence quality
- Research/backtest/live progression

## 4.4 Competitive Gap / Opportunity

Competitors are generally strong at answering:

> What has this strategy returned and how risky has it been?

Our Intelligence Layer should additionally answer:

> Is this a good strategy for what I am trying to achieve?

Target questions include:

- What is working now?
- What works in this type of market?
- What complements the strategies I already run?
- What gives me steadier returns?
- What reduces portfolio drawdown?
- Which high-performing strategies are statistically credible rather than lucky?
- Which strategies have stopped behaving like they historically did?
- Which strategies may be early indicators of changes elsewhere in the library?

The differentiator is **decision intelligence**, not simply more metrics.

---

# 5. Category-Relative Intelligence

Metrics should be interpreted relative to appropriate peer groups.

Example:

```text
Strategy Sharpe:       1.56

All strategies:        Top 21%
Momentum strategies:   Top 14%
US equity momentum:    Top 9%
5+ year strategies:    Top 11%
```

This allows explanations such as:

> This strategy ranks in the top 9% of comparable US equity momentum strategies for risk-adjusted return.

Apply percentile/rank intelligence to:

- Return
- Sharpe
- Sortino
- Drawdown
- Win rate
- Profit factor
- Expectancy
- Consistency
- Robustness
- Strategy health

---

# 6. Regime Intelligence

The engine should evaluate strategy performance under different market environments.

Initial regime concepts:

- Bull
- Bear
- Sideways
- Trending
- Mean-reverting
- High volatility
- Low volatility
- Rising volatility
- Falling volatility

Future query:

> What works now?

Workflow:

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

---

# 7. Strategy-as-a-Product / Marketplace Intelligence

Every strategy should have:

- Profile
- Evidence
- Characteristics
- Rankings
- Comparisons
- Followers/watchers
- Historical behaviour
- Related strategies
- Similar strategies
- Complementary strategies
- Health status

Example presentation:

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

[Compare] [Watch] [Full Analysis]
```

---

# 8. Strategy Health / Strategy Decay Detection

Continuously determine whether a strategy's recent behaviour differs materially from its historical behaviour.

Analyse changes in:

- Return distribution
- Win rate
- Expectancy
- Drawdown
- Volatility
- Trade frequency
- Holding time
- TP/SL behaviour
- Sharpe/Sortino
- Regime response
- Correlations to other strategies

Possible outputs:

- Healthy
- Watch
- Deteriorating
- Significant behavioural change
- Insufficient evidence

The engine should distinguish temporary underperformance from statistically meaningful structural change where possible.

---

# 9. Intra-Library Intelligence Engine

This is a major Intelligence Layer capability.

The system must analyse the **strategy library as a system**, rather than evaluating each strategy only in isolation.

Core modules:

1. Correlation analysis
2. Inverse relationship analysis
3. Lead/lag analysis
4. Behavioural clustering
5. Leader/follower detection
6. Drawdown relationship analysis
7. Drawdown propagation
8. Regime relationship analysis
9. Diversification value
10. Relationship stability
11. Statistical confidence

---

# 10. Lead/Lag Strategy Intelligence

Ordinary correlation asks:

> Are Strategy A and Strategy B related at the same time?

Lead/lag intelligence asks:

> Does movement in Strategy A tend to precede movement in Strategy B?

Example:

| Relationship | Correlation |
|---|---:|
| A(t) → B(t) | +0.18 |
| A(t) → B(t+1) | +0.72 |
| A(t) → B(t+2) | +0.51 |
| A(t) → B(t+3) | +0.19 |

The Intelligence Layer could conclude:

> Strategy A historically leads Strategy B by approximately one period.

## 10.1 Lag search

Do not restrict analysis to `t+1`.

Systematically test relationships such as:

```text
T-10 ... T-3, T-2, T-1, T, T+1, T+2, T+3 ... T+10
```

The appropriate range should depend on strategy frequency and available data.

Potential resolutions:

- Trade
- Minute
- 5-minute
- 15-minute
- Hour
- Session
- Day

## 10.2 Required validation

Lead/lag relationships are especially vulnerable to false discoveries when testing large libraries.

Require:

- Minimum observations
- Statistical significance
- Multiple-testing controls
- Out-of-sample confirmation
- Rolling-window stability
- Regime stability analysis
- Relationship persistence score

Do not present a high historical correlation as evidence of causation.

---

# 11. Inverse Strategy Intelligence

Identify strategies that systematically behave oppositely.

Example:

```text
Strategy A
    ↑
    │
negative correlation
    │
    ↓
Strategy B
```

Example finding:

```text
DNA_102001
Return correlation with DNA_105417 = -0.81
```

Potential interpretation:

> When A has historically struggled, B has tended to perform well.

Use cases:

- Hedging
- Diversification
- Drawdown reduction
- Portfolio construction
- Complementary strategy recommendations

The objective is not simply to find the five highest-return strategies. It is to find combinations whose return and drawdown behaviour complement one another.

---

# 12. Strategy Behavioural Clusters

Analyse the complete strategy library to identify strategies that behave similarly even where their source logic differs.

Example:

```text
STRATEGY LIBRARY
       │
       ├──── Cluster A
       │      DNA_100021
       │      DNA_100387
       │      DNA_101927
       │
       ├──── Cluster B
       │      DNA_100098
       │      DNA_102114
       │
       └──── Cluster C
              DNA_103219
              DNA_105817
```

This is particularly important for large generated/DNA strategy libraries.

Observed behaviour can classify strategies even before their underlying logic is fully described.

Potential intelligence:

> Forty apparently different strategies display essentially the same performance behaviour.

This prevents false diversification.

Cluster analysis should consider:

- Return correlation
- Drawdown correlation
- Volatility behaviour
- Holding periods
- Trade frequency
- Long/short bias
- Regime performance
- Recovery behaviour
- Lead/lag relationships

---

# 13. Leader / Follower Strategy Clusters

Combine clustering with lead/lag intelligence.

Example:

```text
                 DNA_A
                   │
               LEADER
              ↙    ↓    ↘
           +1      +2      +1
           ↓       ↓       ↓
        DNA_B    DNA_C    DNA_D
```

Potential classification:

- Leading strategies
- Concurrent strategies
- Lagging strategies

## 13.1 Strategy Leadership Score

Potential strategy-level metric:

```text
DNA_100427

Leadership Score        87/100
Strategies led              23
Median lead              2 hrs
Relationship confidence     91%
Persistence                 84%
```

Leadership scoring should account for:

- Number of statistically credible follower relationships
- Strength
- Lag consistency
- Out-of-sample persistence
- Regime persistence
- False-discovery controls

---

# 14. Drawdown Relationship Intelligence

Analyse what happens elsewhere in the strategy library when a strategy enters drawdown.

Example:

```text
A enters drawdown
      ↓
B usually enters DD +3 hours
C usually improves
D is largely unaffected
E usually enters DD +1 day
```

Questions to answer:

- Which strategies enter drawdown together?
- Which strategies enter drawdown first?
- Which strategies tend to improve when another deteriorates?
- Which strategies remain independent?
- Which strategy drawdowns historically precede wider cluster drawdowns?
- Which strategies recover first?

This can expose **risk propagation** through the library.

Potential finding:

> Strategy A deterioration historically precedes deterioration across 37% of this strategy cluster.

---

# 15. Regime Relationships Across Strategies

Combine intra-library relationships with the market-regime engine.

Example:

```text
VOLATILITY RISING

Strategy Group A
starts improving
        ↓
+2 hours
        ↓
Strategy Group B
starts improving
        ↓
+6 hours
        ↓
Strategy Group C
starts deteriorating
```

This creates two complementary regime mechanisms:

1. **External regime detection** — infer market conditions from market data.
2. **Internal regime detection** — infer possible market changes from collective strategy behaviour.

The strategy library can therefore potentially act as a **sensor for market-state transition**.

This must initially be treated as an analytical hypothesis and validated out-of-sample before being used for actionable recommendations.

---

# 16. Diversification Intelligence

Use cross-strategy analysis to determine whether strategies provide genuine diversification.

Analyse:

- Return correlation
- Downside correlation
- Drawdown overlap
- Tail-event correlation
- Regime correlation
- Lead/lag
- Recovery timing
- Exposure overlap

Potential output:

```text
Strategy A + Strategy B

Return correlation:       +0.12
Drawdown overlap:            18%
Regime overlap:              Low
Diversification score:     91/100
```

This should feed directly into the Portfolio Builder.

---

# 17. Portfolio / Strategy Combination Intelligence

The engine should support objectives such as:

- Steady returns
- Reduced drawdown
- Lower volatility
- Higher risk-adjusted return
- Regime diversification
- Funded-account constraints
- Lower strategy correlation
- Drawdown protection
- Balanced long/short behaviour

Example user query:

> Find three strategies that together reduce drawdown without materially reducing expected return.

Workflow:

```text
User objective
      ↓
Candidate strategy universe
      ↓
Quality / confidence filtering
      ↓
Correlation analysis
      ↓
Inverse relationship analysis
      ↓
Drawdown overlap analysis
      ↓
Regime diversification
      ↓
Combination simulation
      ↓
Rank combinations
      ↓
Explain trade-offs
```

---

# 18. Relationship Stability

A relationship should not be treated as permanent.

For every important cross-strategy relationship, measure:

- Full-history relationship
- Rolling relationship
- Recent relationship
- Regime-specific relationship
- Out-of-sample relationship
- Stability/persistence

Possible relationship states:

- Stable
- Strengthening
- Weakening
- Regime-dependent
- Recently broken
- Insufficient evidence

---

# 19. Statistical Confidence and Data-Mining Protection

This is mandatory for intra-library analysis.

With hundreds or thousands of strategies, the number of possible pairwise and lagged relationships becomes extremely large.

The engine must protect against spurious discoveries.

Requirements include:

- Minimum sample sizes
- Confidence intervals
- Significance testing where appropriate
- Multiple-hypothesis testing controls
- Out-of-sample validation
- Rolling validation
- Regime validation
- Minimum persistence thresholds
- Data-quality checks
- Look-ahead bias prevention

Every relationship shown to users should carry a confidence measure.

The system should distinguish:

**Interesting pattern** from **statistically credible relationship**.

---

# 20. Decision Intelligence

The three major intelligence areas now become:

```text
                 STRATEGY INTELLIGENCE
                          │
          ┌───────────────┼────────────────┐
          │               │                │
          ▼               ▼                ▼
  COMPETITION MATCH   INDIVIDUAL       INTRA-LIBRARY
                      STRATEGY          INTELLIGENCE
                      INTELLIGENCE
          │               │                │
          │               │                ├─ Correlation
          │               │                ├─ Inverse
          │               │                ├─ Lead/Lag
          │               │                ├─ Clusters
          │               │                ├─ DD propagation
          │               │                ├─ Leadership
          │               │                ├─ Relationship health
          │               │                └─ Diversification
          │               │
          └───────────────┼────────────────┘
                          ↓
                  DECISION INTELLIGENCE
                          ↓
              Discover / Compare / Combine
```

The eventual goal is to translate a trading objective or market question into:

**Strategy discovery → evaluation → relationship analysis → combination → explanation**

---

# 21. Target User Questions

The Intelligence Layer should eventually answer questions including:

### Discovery
- Which strategies have the highest risk-adjusted returns?
- Show me strategies with >60% win rate and <10% drawdown.
- Which strategies are best for sideways markets?
- What appears to work under current conditions?

### Quality
- Is this strategy statistically credible?
- Is its performance consistent?
- Is it robust?
- Is recent performance deteriorating?

### Relative intelligence
- How does this strategy compare with similar strategies?
- What percentile does it rank in?
- Are there effectively duplicate strategies in the library?

### Intra-library
- Which strategies move together?
- Which strategies behave inversely?
- Which strategies tend to lead other strategies?
- Which strategies lag?
- Are there leader/follower groups?
- Which strategy drawdowns tend to precede others?
- Which strategies recover while others deteriorate?
- Are cross-strategy relationships changing?

### Portfolio intelligence
- Which strategies genuinely diversify each other?
- What complements my existing strategy?
- What combination reduces drawdown?
- Which strategies provide protection when my current strategies struggle?
- Am I holding multiple strategies that are actually the same behavioural exposure?

---

# 22. Implementation Phases

## Phase 1 — Foundation

Build:

- Normalized strategy schema
- Strategy Intelligence Object
- Core metrics
- Strategy directory
- Structured filters
- Strategy detail page
- Baseline return correlation matrix

## Phase 2 — Core Intelligence

Build:

- Composite scoring
- Rankings
- Category percentiles
- Strategy comparison
- Strategy health
- Rolling metrics
- Similar strategy detection

## Phase 3 — Intra-Library Intelligence

Build:

- Correlation engine
- Inverse correlation engine
- Lead/lag analysis
- Behavioural clustering
- Drawdown overlap
- Drawdown propagation
- Relationship stability
- Confidence framework
- Leadership Score

## Phase 4 — Natural-Language Intelligence

Build:

- Natural-language finder
- Query-to-filter translation
- Explanation engine
- Saved searches
- Watchlists

## Phase 5 — Regime & Portfolio Intelligence

Build:

- Market regime engine
- Strategy/regime matching
- Cross-strategy regime relationships
- “What works now?” capability
- Diversification scoring
- Portfolio builder
- Strategy combination ranking
- Objective-based recommendations

## Phase 6 — Continuous Intelligence

Build:

- Strategy decay monitoring
- Relationship decay monitoring
- Emerging leader/follower detection
- Cluster changes
- Regime-transition signals
- Personalized recommendations
- Alerts/watch conditions

---

# 23. Core Principle

The Intelligence Layer must not simply produce more statistics.

It should convert strategy data into answers.

The central design principle is:

> **Translate a trading objective or market question into strategy discovery, evaluation, relationship analysis, combination, and an evidence-based explanation.**

For intra-library intelligence specifically:

> **Treat the strategy library itself as a dataset whose internal relationships can reveal diversification, inverse behaviour, lead/lag structure, behavioural clusters, drawdown propagation, and potentially changes in market state.**

This is the key expansion from a **Strategy Directory** into a **Strategy Intelligence Platform**.
