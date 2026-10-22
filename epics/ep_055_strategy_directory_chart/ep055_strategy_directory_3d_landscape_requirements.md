# Strategy Directory --- 3D Strategy Landscape Requirements

## 1. Objective

Create an interactive visual representation of the complete Strategy
Directory as a **single 3D data landscape**.

The landscape must make it possible to see **all strategies at once**,
potentially **2,000+ strategies**, while immediately revealing:

-   Which strategies are positive or negative.
-   Relative net value/performance through pillar height.
-   Which strategy family each strategy belongs to.
-   Where groups of strategies are improving together.
-   The fastest-growing clusters.
-   How the landscape changes between time snapshots.

The objective is not to build a conventional bar chart or a set of
strategy cards. It should feel like looking across a **terrain or city
of strategies**, where patterns become visually obvious before the user
drills into individual strategies.

------------------------------------------------------------------------

## 2. Core Visual Concept

Each individual strategy is represented by a **very thin vertical 3D
cylinder/pillar** standing upright on a flat landscape.

At small strategy counts the objects may visibly resemble cylinders. At
2,000+ strategies they should become very thin vertical pillars so that
density remains readable.

### Strategy encoding

  Visual property                   Meaning
  --------------------------------- ---------------------------------------------
  One pillar                        One strategy
  Green                             Positive net value
  Red                               Negative net value
  Neutral/grey                      At or very close to zero
  Pillar height                     Magnitude of net value
  Position                          Strategy's location within its family/group
  Change in height over snapshots   Change in strategy performance
  Highlighted local area            Cluster of unusually fast growth

The visual should therefore communicate both **individual strategy
state** and **population-level patterns**.

------------------------------------------------------------------------

## 3. Scale

The architecture must support the **entire strategy population**, not a
sampled subset.

Initial visual target:

-   2,000+ strategies.
-   Prototype/reference scale: approximately 2,400 strategies.
-   Four primary family sections.
-   Approximately 500--600+ strategies per section if distributed
    evenly.
-   Must remain extensible as the directory grows beyond this level.

The implementation must not assume that strategy counts remain fixed or
evenly distributed between families.

------------------------------------------------------------------------

## 4. Landscape Layout

The primary view is a **flat landscape divided into four clearly
identifiable sections**.

Conceptually:

``` text
+---------------------------+---------------------------+
|                           |                           |
|       FAMILY 1            |        FAMILY 2           |
|                           |                           |
|   hundreds of pillars     |    hundreds of pillars    |
|                           |                           |
+---------------------------+---------------------------+
|                           |                           |
|       FAMILY 3            |        FAMILY 4           |
|                           |                           |
|   hundreds of pillars     |    hundreds of pillars    |
|                           |                           |
+---------------------------+---------------------------+
```

The four sections are part of one continuous visual landscape rather
than four independent charts or display cases.

Each section must:

-   Have a clear family label.
-   Show the number of strategies in that family.
-   Contain every strategy assigned to that family.
-   Preserve enough spatial consistency that clusters and changes can be
    compared over time.

The exact four family names must come from the real Strategy Directory
taxonomy rather than being hard-coded prototype labels.

------------------------------------------------------------------------

## 5. Strategy Family Grouping

Strategies must be grouped according to the **breakout family of
strategies** defined by the Strategy Directory.

The visualisation layer must consume the family/group assigned to each
strategy from the underlying data.

Required strategy fields should include at minimum:

``` text
strategy_id
strategy_name
strategy_family
product
product_type
net_value
snapshot_date
```

Additional analytics can be supplied without changing the fundamental
landscape model.

------------------------------------------------------------------------

## 6. Positive / Negative Representation

Colour is directional:

-   **Green pillar:** positive net value.
-   **Red pillar:** negative net value.
-   **Neutral/grey pillar:** effectively flat / near zero.

The zero threshold should be configurable so insignificant movement does
not create misleading red/green noise.

Example:

``` text
net_value > threshold       -> green
net_value < -threshold      -> red
otherwise                   -> neutral
```

Colour represents direction only. It should **not** independently imply
that the Arena or Directory is judging a strategy as "good", "bad",
"superior", etc.

The system should present numerical facts.

------------------------------------------------------------------------

## 7. Pillar Height

The height of every strategy pillar is driven by the magnitude of the
selected **net value/performance measure**.

Conceptually:

``` text
height = scale(abs(net_value))
```

A strategy with a larger absolute net value produces a taller pillar.

The visual scaling function must prevent a few extreme strategies from
flattening the rest of the landscape. Suitable approaches include:

-   capped linear scaling;
-   percentile scaling;
-   logarithmic/square-root scaling;
-   configurable visual ceiling.

The raw numerical value must remain available on selection/inspection
even if the visual height is normalized.

------------------------------------------------------------------------

## 8. Five Snapshot View

The landscape must support at least **five time snapshots**.

Example:

``` text
Snapshot 1
Snapshot 2
Snapshot 3
Snapshot 4
Snapshot 5
```

These may initially represent months, but the implementation should not
hard-code "month" as the only possible period.

A user must be able to select a snapshot and see the complete landscape
update.

The same strategy should retain a stable spatial location between
snapshots wherever possible. This is important because movement in
pillar height then becomes visually meaningful.

Snapshot comparison should reveal:

-   newly positive strategies;
-   newly negative strategies;
-   strategies accelerating;
-   strategies deteriorating;
-   emerging clusters;
-   clusters losing momentum;
-   family-level shifts.

------------------------------------------------------------------------

## 9. Growth Measurement

The visual must distinguish **current net value** from
**growth/acceleration**.

A tall green pillar is not automatically the fastest-growing strategy.

Growth should be calculated from the strategy's movement across the
snapshot history.

Possible measures include:

``` text
growth = current_net_value - previous_net_value
```

and, when enough observations exist:

``` text
acceleration = recent_growth - earlier_growth
```

The precise growth metric should be modular so the intelligence layer
can later substitute more sophisticated calculations.

Examples:

-   absolute change;
-   percentage change;
-   slope over N snapshots;
-   acceleration;
-   risk-adjusted improvement;
-   consistency-weighted growth.

------------------------------------------------------------------------

## 10. Cluster Detection

A central requirement is to identify **clusters of strategies that are
growing quickly together**.

The important signal is not simply:

> Which individual strategy grew fastest?

It is:

> Where in the strategy landscape are multiple related/nearby strategies
> showing unusually strong growth at the same time?

A growth cluster therefore requires:

1.  Multiple strategies in a local logical/spatial group.
2.  Positive growth above a defined threshold.
3.  Sufficient density of qualifying strategies.
4.  A cluster-level growth score.

Conceptually:

``` text
qualifying_strategy =
    growth_score >= growth_threshold

cluster =
    neighbouring qualifying strategies
    meeting minimum cluster size/density

cluster_score =
    aggregate growth of strategies in cluster
```

The eventual clustering method can evolve. The visual requirement is
independent of the precise algorithm.

------------------------------------------------------------------------

## 11. Fastest-Growth Areas

The strongest clusters must be immediately visible.

Examples of visual treatment:

-   translucent hotspot over the area;
-   outline around the cluster;
-   brighter pillars within the cluster;
-   cluster label;
-   cluster rank.

Example labels:

``` text
FASTEST GROWTH #1
FASTEST GROWTH #2
FASTEST GROWTH #3
```

A cluster may also expose factual statistics such as:

``` text
32 strategies
Average growth +8.4%
24/32 positive
Family: [family name]
```

Again, labels should report measured facts rather than qualitative
claims such as "best" or "superior".

------------------------------------------------------------------------

## 12. Growth Focus Mode

The interface should provide at least two viewing states.

### All Strategies

Displays the entire strategy landscape normally.

### Highlight Growth

Keeps every strategy visible but visually reduces non-cluster strategies
so the fastest-growth areas become immediately obvious.

Non-cluster strategies should not disappear completely because the user
needs the surrounding landscape for context.

------------------------------------------------------------------------

## 13. Interaction

At 2,000+ strategies, displaying permanent labels for individual
strategies would create visual noise.

Default view:

-   no individual strategy labels;
-   family labels remain visible;
-   cluster labels remain visible;
-   population statistics remain visible.

Individual strategy detail appears when a pillar is selected.

Potential strategy detail:

``` text
Strategy ID
Strategy name
Family
Product
Product type
Current net value
Previous net value
Growth
Snapshot history
Current cluster membership
```

This detail can later link into the full Strategy Directory strategy
page.

------------------------------------------------------------------------

## 14. Drill-Down Hierarchy

The landscape should support a natural hierarchy:

``` text
ALL STRATEGIES
      ↓
4 STRATEGY FAMILIES
      ↓
GROWTH CLUSTERS
      ↓
INDIVIDUAL STRATEGIES
      ↓
FULL STRATEGY ANALYTICS
```

This allows the same visual to serve both rapid discovery and detailed
investigation.

------------------------------------------------------------------------

## 15. Family-Level Intelligence

Each family section should be capable of displaying aggregate factual
information such as:

-   strategy count;
-   number positive;
-   number negative;
-   number neutral;
-   aggregate net value;
-   average net value;
-   average growth;
-   number of fast-growth clusters.

This creates a second level of intelligence above individual strategies.

------------------------------------------------------------------------

## 16. Filtering

The visual architecture should allow later filtering without rebuilding
the landscape component.

Potential filters include:

-   product;
-   product type;
-   market regime;
-   positive/negative;
-   net-value range;
-   growth rate;
-   strategy family;
-   time period;
-   trade frequency;
-   drawdown;
-   win rate;
-   holding period;
-   session/time of day.

Filtered-out strategies can either disappear or become subdued depending
on the analytical use case.

------------------------------------------------------------------------

## 17. Spatial Consistency

Strategy positioning should not be random on every render.

A deterministic position should be derived from strategy identity and
family.

This is important because users should learn the geography of the
landscape.

For example:

``` text
family determines quadrant
strategy_id determines stable cell/coordinate
```

Later, positioning could become more intelligent by placing
behaviourally similar strategies close together.

That would make geographic clustering itself meaningful.

------------------------------------------------------------------------

## 18. Future Behaviour-Based Geography

The initial implementation can place strategies deterministically inside
their assigned family.

A later intelligence layer could organize strategies spatially according
to similarity.

Potential dimensions:

-   trading behaviour;
-   market regime response;
-   return profile;
-   drawdown profile;
-   volatility;
-   trade duration;
-   time of day;
-   product;
-   correlation.

This would turn the landscape into a genuine **Strategy Map**, where
nearby pillars have meaningful similarities.

Growth hotspots would then reveal not merely adjacent IDs but
**behavioural pockets of market performance**.

This is an important future direction and should not be blocked by the
MVP implementation.

------------------------------------------------------------------------

## 19. Data Separation

The visualisation should not calculate every metric itself.

Keep responsibilities separated:

### Trading / Strategy Data Layer

Provides underlying strategy and performance data.

### Intelligence Layer

Calculates:

-   snapshot metrics;
-   growth;
-   acceleration;
-   family aggregates;
-   cluster membership;
-   cluster ranking.

### Visualisation Layer

Receives prepared data and renders:

-   landscape;
-   pillars;
-   colour;
-   height;
-   clusters;
-   interactions.

Conceptual payload:

``` json
{
  "snapshot": "2026-09",
  "strategies": [
    {
      "strategy_id": "DNA_102001",
      "family": "family_a",
      "net_value": 12.4,
      "growth": 4.7,
      "cluster_id": "cluster_17"
    }
  ],
  "clusters": [
    {
      "cluster_id": "cluster_17",
      "family": "family_a",
      "strategy_count": 34,
      "average_growth": 7.8,
      "rank": 1
    }
  ]
}
```

------------------------------------------------------------------------

## 20. Performance Requirements

Rendering 2,000+ interactive DOM elements can become expensive,
particularly on mobile.

The implementation should therefore be designed with scale in mind.

Possible rendering progression:

### MVP

CSS/HTML pillars if performance is acceptable.

### Scale-up

Canvas/WebGL rendering for thousands or tens of thousands of strategies.

Potential technology:

-   HTML/CSS for prototype;
-   Canvas for dense 2D/2.5D rendering;
-   Three.js/WebGL for a richer 3D landscape if justified.

Do **not** introduce heavyweight 3D infrastructure until the simple
implementation proves insufficient.

The requirement is the analytical experience, not a particular rendering
technology.

------------------------------------------------------------------------

## 21. Responsive Behaviour

Desktop should provide the primary landscape experience.

Mobile should preserve the same information but may:

-   allow horizontal navigation;
-   reduce pillar spacing;
-   simplify cluster labels;
-   open strategy details in a separate panel;
-   allow family-level focus.

The mobile implementation must not reduce the dataset to a misleading
sample merely to fit the screen.

------------------------------------------------------------------------

## 22. Visual Principles

The landscape should feel:

-   dense;
-   analytical;
-   immediately readable;
-   alive as data changes;
-   visually distinctive;
-   suitable for screen capture/video.

Avoid:

-   thousands of labels;
-   decorative 3D that obscures data;
-   excessive glow;
-   unnecessary animation;
-   chart furniture;
-   isolated cards for every strategy.

The primary visual object is the **strategy population itself**.

------------------------------------------------------------------------

## 23. Animation

When moving between snapshots, pillar heights may animate smoothly from
the old value to the new value.

This allows the viewer to see areas rising or falling.

Potential later capability:

``` text
PLAY
Snapshot 1 → Snapshot 2 → Snapshot 3 → Snapshot 4 → Snapshot 5
```

This could turn the Strategy Directory into a highly visual
market-intelligence and content-generation asset.

Animation must remain optional and respect reduced-motion preferences.

------------------------------------------------------------------------

## 24. Screen-Capture / Content Use

The landscape should be designed so that it can also generate compelling
visual content.

Examples:

-   "Where strategies are growing fastest this month"
-   "A new cluster is forming"
-   "2,400 live strategies --- here is what changed"
-   "Which strategy family is accelerating?"
-   "Watch this group turn from red to green"

This supports the wider Strategy Directory distribution/content engine
without requiring a separate visualization product.

------------------------------------------------------------------------

## 25. MVP Scope

Keep the first implementation deliberately lightweight.

### Required

-   One landscape.
-   Four family sections.
-   2,000+ real strategies.
-   One pillar per strategy.
-   Stable pillar positions.
-   Green / red / neutral direction.
-   Height from net value.
-   Five selectable snapshots.
-   Growth calculation.
-   Cluster identification.
-   Fastest-growth cluster highlighting.
-   All-strategies / growth-focus modes.
-   Click/tap individual strategy.
-   Basic family and landscape totals.

### Not required initially

-   Full free-camera 3D navigation.
-   Complex physics.
-   AI-generated terrain.
-   Advanced WebGL effects.
-   User-created custom maps.
-   Dozens of filters.
-   Predictive cluster modelling.

These can be added only where evidence shows they improve discovery or
understanding.

------------------------------------------------------------------------

## 26. Success Test

The visual is successful if a user can look at the landscape for a few
seconds and answer:

1.  Where are most strategies positive?
2.  Where are most strategies negative?
3.  Which families contain the strongest current activity?
4.  Where are strategies improving fastest together?
5.  Is a new growth pocket emerging?
6.  How has that picture changed over the five snapshots?
7.  Which individual strategies make up an interesting cluster?

The key outcome is:

> **Turn thousands of individual strategy records into a landscape where
> collective behaviour and emerging opportunities become visually
> obvious.**

------------------------------------------------------------------------

## 27. Longer-Term Direction

This should ultimately become more than a directory visual.

It can become the visual interface to the Strategy Directory
intelligence layer:

``` text
THOUSANDS OF LIVE STRATEGIES
          ↓
PERFORMANCE LANDSCAPE
          ↓
FAMILIES / BEHAVIOURAL REGIONS
          ↓
EMERGING CLUSTERS
          ↓
FASTEST CHANGE
          ↓
STRATEGY DISCOVERY
          ↓
PORTFOLIO / CHALLENGE / AGENT HANDOFF
```

The important architectural decision is therefore to build the landscape
as a **reusable visualization of strategy intelligence**, rather than
hard-coding it as a one-off 2,400-bar demonstration.
