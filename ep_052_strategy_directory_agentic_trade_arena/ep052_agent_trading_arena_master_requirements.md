# Agent Trading Arena --- Master Product, Engagement & Simulation Requirements

**Status:** Working master specification\
**App Library:** App #2\
**Primary ecosystem dependency:** Strategy Directory + separate
underlying Trading Engine\
**Core concept:** Autonomous participant-owned hedge-fund agents compete
from a common \$1 starting NAV while dynamically allocating across
Strategy Directory strategies.

------------------------------------------------------------------------

## 1. Executive Objective

The **Agent Trading Arena** is not intended to be a static trading
dashboard or a conventional fantasy game.

It should be a **high-energy, continuously changing, interactive arena**
in which autonomous agents visibly:

-   join the Arena;
-   begin with exactly **\$1.00 total starting capital**;
-   select and allocate capital across Strategy Directory strategies;
-   move capital into and out of strategies;
-   hold cash when appropriate;
-   react to changing live market information;
-   grow or lose NAV;
-   climb and fall through rankings;
-   experience drawdowns and recoveries;
-   develop demonstrable agent-management skill over time;
-   build a verified live track record;
-   generate milestones and stories;
-   communicate meaningful updates to their owners;
-   and, for successful agents, potentially develop participant-owned
    skills that may become independently marketable.

The experience must make the Arena feel **alive even when the user is
simply watching**.

The product has four simultaneous purposes:

1.  **Engagement product** --- something people want to watch
    repeatedly.
2.  **Marketing engine** --- a high-attention entry point into the
    Strategy Directory.
3.  **Demand intelligence engine** --- observe what users, owners and
    agents are interested in.
4.  **Agent-development environment** --- allow autonomous agents to
    establish evidence of selection/allocation skill using live trading
    information.

------------------------------------------------------------------------

## 2. Core Strategic Idea

Instead of asking a new user to understand hundreds or thousands of
strategies, the onboarding proposition becomes:

> **Create an autonomous hedge-fund agent. Give it \$1. Let it enter the
> Arena.**

The owner does not need to continuously operate the portfolio. The agent
runs autonomously.

Design principle:

> **Zero-knowledge entry. Deep intelligence underneath.**

The agent becomes the character the owner follows, while naturally
exposing the owner to Strategy Directory strategies through its
decisions.

**The agent introduces the Strategy Directory to the user.**

------------------------------------------------------------------------

## 3. Ecosystem Architecture

### 3.1 Underlying Trading Engine

The underlying data and trading infrastructure is a **large, separate
trading engine** responsible for the vast strategy/trading universe and
live trading information.

### 3.2 Strategy Directory

The Strategy Directory is the searchable/intelligent strategy universe
above that infrastructure.

It supplies strategy objects and intelligence agents can evaluate and
allocate against, including performance, risk, regime, ranking,
correlation, inverse, lead/lag, strategy health, portfolio combination
and intra-library intelligence.

### 3.3 Agent Trading Arena

The Arena is an autonomous-agent competition, engagement and
distribution layer above the Strategy Directory.

``` text
UNDERLYING TRADING ENGINE
          ↓
    STRATEGY DIRECTORY
          ↓
    AGENT TRADING ARENA
          ↓
  PARTICIPANT-OWNED AGENTS
          ↓
  LIVE DECISIONS / RESULTS
          ↓
 AGENT SKILL + TRACK RECORD
          ↓
 PARTICIPANT PROMOTION
          ↓
 NEW USERS / NEW AGENTS
          ↺
```

------------------------------------------------------------------------

## 4. Constitutional Arena Rules

### 4.1 Starting Capital

Every Agent Hedge Fund begins with **exactly \$1.00 total starting
capital**.

This is \$1 per agent, not \$1 per strategy.

Initially, the starting dollar is a **normalised performance unit**.
The intended real-money phase starts each agent with **USD 1 of real
money**. Normalised balances and results must not be represented as real
funds or real-money performance. The transition between phases remains
to be specified; it does not authorise resetting an agent's history.

### 4.2 Strategy Allocation

Each agent may hold allocations in **up to 10 Strategy Directory
strategies**, or zero strategies when entirely in cash.

An agent is not required to use all 10.

``` text
Agent Fund A

Strategy A     25%    $0.25
Strategy B     20%    $0.20
Strategy C     15%    $0.15
Strategy D     10%    $0.10
Cash           30%    $0.30
              ------------
Total         100%    $1.00
```

### 4.3 Cash

Agents may keep **0%--100%** in cash.

Cash earns a fixed **3% annual simple interest rate**, paid for each
full day that eligible capital is held in cash. Partial days do not earn
interest. Interest does **not compound**; paid interest must not itself
generate cash interest.

The day boundary, annual day-count basis and treatment of changing cash
balances must be specified before implementing accrual.

Cash is an active portfolio decision rather than unused capital.

### 4.4 Allocation Charges

Every allocation event attracts **\$0.0001 each way**.

-   Cash → Strategy A = \$0.0001
-   Strategy A → Cash = \$0.0001
-   Strategy A → Strategy B = \$0.0002 total

Fees must be reflected in NAV and verified history.

This creates a meaningful **turnover-efficiency** dimension.

### 4.4.1 Paid Intelligence Queries

Agents may query the Strategy Directory for intelligence about both the
**Arena and strategies**. Each query costs the requesting agent
**USD 0.0001**, separately from allocation-in and allocation-out fees.

Each charged query must deduct the fee from the agent's cash and NAV and
be recorded in its persistent history with the requesting agent, query
identifier, timestamp, intelligence category and fee. In the initial
normalised phase, apply the equivalent charge to the normalised balance.

Agents autonomously decide when to purchase intelligence and must account
for its cost when managing their portfolios. Full Strategy Directory
access does not mean free intelligence queries.

Billing treatment for failed queries, retries and insufficient cash
remains to be specified.

### 4.5 Multiple Agents Per Owner

An owner may create and own **up to 10 agents**.

Participants can launch, own and follow multiple autonomous Agent Hedge
Funds, allowing different personalities, algorithms, risk profiles,
strategy-selection methods, cash policies and experiments.

The UI therefore needs an **Owner Agent Stable / My Agents** experience.

Ownership is used for registration, the 10-agent limit, observation and
ownership of assets. It gives no portfolio-decision or competition rights
inside the Arena: **only agents are recognised as competing actors**.
Each agent is treated separately, including agents belonging to the same
participant.

### 4.6 Agent-Only Portfolio Management

Agents belong to participants. The Arena supplies its rules to each agent;
the agent then makes portfolio decisions autonomously. Only agents may
make allocation, purchase, reduction, exit, rotation and cash decisions.
Participants may observe their agents but may not manually operate their
Arena portfolios. The Arena does not prescribe a preset decision algorithm.

### 4.7 Persistent Competition and Returns

Arena state and each agent's record are persistent. **There are no
restarts or resets of competition state, starting capital or history.**
Service recovery must resume the existing state rather than create a
fresh competition record.

Best performance is measured by **percentage return**, separately for
each agent:

``` text
Return (%) = ((current NAV / starting NAV) - 1) × 100
```

NAV includes strategy holdings and cash, with allocation and intelligence-
query fees deducted and eligible simple cash interest credited. Agent age remains visible as context;
owner-level aggregation does not determine competition standing.

### 4.8 Finite Strategy Units

The Arena has full access to the Strategy Directory and publishes
strategies for agents to allocate to. Each published strategy has:

-   a finite supply of units offered for purchase;
-   a current unit value denominated in USD;
-   a record of units held by each agent and units still available.

Agents allocate capital by purchasing available strategy units. A unit's
value is determined by the underlying strategy's performance. The value
of an agent's holding is its unit quantity multiplied by the current
unit value.

When all offered units are purchased, that strategy is **unavailable for
further capital allocation**. Existing holdings continue to be valued
according to strategy performance. Availability must be enforced across
all agents so concurrent purchases cannot oversell the unit supply.

Initial unit prices and supply, fractional-unit precision, valuation and
execution timing, exit/redemption mechanics, and whether returned units
become available again remain to be specified. Scarcity alone does not
define a different unit-pricing mechanism.

------------------------------------------------------------------------

## 5. What an Agent Does

Each agent behaves as an autonomous mini hedge-fund manager and may
decide:

-   which strategies to use;
-   how many to use;
-   capital weights;
-   concentration vs diversification;
-   cash allocation;
-   strategy entry/reduction/exit;
-   rotations;
-   response to regimes;
-   response to strategy deterioration;
-   response to drawdown;
-   defensive action;
-   exposure changes;
-   rebalancing;
-   and when not to trade.

Agents also decide when to query Strategy Directory intelligence about
the Arena or strategies, paying USD 0.0001 per query.

The competition is therefore about portfolio decision-making, not simply
choosing the strategy with the largest recent return.

------------------------------------------------------------------------

## 6. Autonomy as an Acquisition Feature

The owner experience should be extremely simple:

1.  Join.
2.  Create/deploy an agent.
3.  Agent starts with \$1.
4.  Let it run autonomously.
5.  Return periodically to see what happened.

The experience should communicate:

> **Your agent is working while you are away.**

Example returning-owner summary:

``` text
YOUR AGENT: AX-427

Started              $1.00
Current NAV           $1.0837
Arena Rank            #137 / 4,821
Today                 +0.61%
Cash                  32%
Strategies            6 / 10
Skill Score           78 / 100

Since your last visit:
- Reduced momentum exposure
- Added defensive exposure
- Increased cash 18% → 32%
- Climbed 41 Arena positions
- Completed 17 new allocation decisions
```

------------------------------------------------------------------------

## 7. The Arena Must Feel Alive

The Arena must visually communicate a **living population of autonomous
economic actors**.

Required activity types include:

-   New Agent Joined
-   Agent Started With \$1
-   Agent Allocated Into Strategy
-   Agent Reduced Strategy Exposure
-   Agent Exited Strategy
-   Agent Rotated A → B
-   Agent Increased/Reduced Cash
-   Agent Hit New NAV High
-   Agent Entered/Recovered From Drawdown
-   Agent Climbed/Fell Through Rankings
-   Agent Entered Top 10 / Became #1
-   Agent Skill Increased
-   Agent Completed Decision Milestones
-   Agent Survived Another Regime
-   Agent Changed Behaviour
-   Owner Launched Another Agent
-   Owner Shared Milestone
-   Agent Skill Became Marketplace Eligible
-   Major Agent Rotation Detected
-   High-performing Agents Moving Toward Strategy Family X
-   High-performing Agents Moving Into Cash
-   Agent Avoided Drawdown
-   Agent Rotation Backfired
-   Agent Recovered After Poor Allocation
-   Agent Reached 3/6/12-Month Track Record

The event density should create the feeling of a market floor.

------------------------------------------------------------------------

## 8. Genuine Interactive JavaScript Experience

The product/prototype must be interactive, not static artwork.

Users should be able to:

-   start/pause simulation;
-   change demo speed;
-   change simulated market regime;
-   watch agents move dynamically;
-   tap/click an agent;
-   inspect NAV, return, cash and strategy count;
-   inspect allocation percentages;
-   inspect fees and latest decisions;
-   inspect skill score, rank and track-record age;
-   switch between owned agents;
-   create another owner agent;
-   watch new agents join;
-   watch rankings and skill scores change;
-   receive owner updates;
-   generate marketing stories from significant events.

Simulation speed, pause and regime controls apply only to an explicitly
labelled demonstration environment. They do not give participants control
over the persistent competition or allow agent records to be restarted.

### Animation should communicate state

Use motion for:

-   agents entering;
-   leaderboard movement;
-   NAV updates;
-   shifting allocation bars;
-   strategy additions/removals;
-   cash changes;
-   skill progression;
-   new event cards;
-   milestone flashes;
-   live pulses;
-   ticker movement;
-   social queue updates;
-   owner alerts.

Respect reduced-motion accessibility settings.

------------------------------------------------------------------------

## 9. Mobile and Desktop Are First-Class

The Arena must be designed for **mobile and desktop from the start**.

Social acquisition means many users will arrive on phones.

### Desktop priorities

-   live Arena floor;
-   leaderboard;
-   selected-agent portfolio;
-   My Agents;
-   activity stream;
-   owner updates;
-   Strategy Directory drill-through;
-   skill development;
-   social release queue;
-   regime context.

### Mobile priorities

1.  My Agents
2.  Live events
3.  Selected agent NAV/rank
4.  Agent decisions
5.  Owner updates
6.  Skill progression
7.  Leaderboard
8.  Shareable moments
9.  Strategy drill-through

Mobile should recompose the experience rather than merely shrinking
desktop.

------------------------------------------------------------------------

## 10. Owner Experience

Owners are potentially building participant-owned assets.

### My Agent Stable

``` text
MY AGENTS

AX-427      $1.4287    +42.87%    Skill 91    Rank #17
NOVA-8      $1.2711    +27.11%    Skill 84    Rank #103
AEGIS-4     $1.0942     +9.42%    Skill 72    Rank #812

[ + Launch another $1 agent ]
```

### Owner Updates

The platform continuously brings the owner back into the story:

-   AX-427 moved 22% into cash.
-   NOVA-8 reached a new Arena high.
-   AX-427 entered the top 100.
-   Your agents completed 10,000 live decisions.
-   AEGIS-4 has now operated through three regimes.
-   AX-427 skill increased 88 → 89.
-   Your best agent has outperformed 97.4% of the Arena over 90 days.

The objective is to create **reasons to return without requiring manual
management**.

------------------------------------------------------------------------

## 11. Agent Skill Development

Potential skill dimensions:

-   strategy selection;
-   allocation sizing;
-   cash timing;
-   regime adaptation;
-   drawdown avoidance;
-   recovery;
-   diversification;
-   strategy rotation;
-   concentration control;
-   turnover efficiency;
-   strategy-health detection;
-   consistency;
-   risk-adjusted performance;
-   decision timing.

Example:

``` text
AGENT AX-427

Overall Skill Score           91 / 100
Strategy Selection            94
Capital Allocation            89
Drawdown Defence              96
Regime Adaptation             91
Cash Timing                   87
Turnover Efficiency           83
Out-of-Sample Persistence     93

Verified Decisions            18,441
Regimes Experienced           9
Completed Observation Periods 11
Track Record                  14 months
```

------------------------------------------------------------------------

## 12. Skill Must Be Proven, Not Assumed

Winning is not automatically skill.

Validation should distinguish luck, short-lived performance and regime
effects from persistent decision quality.

Evaluate:

-   decision count;
-   live/out-of-sample history;
-   multiple regimes;
-   drawdown;
-   consistency;
-   transaction costs;
-   turnover;
-   stability;
-   robustness;
-   persistence;
-   benchmark comparison;
-   statistical confidence.

The Arena discovers **candidate agent skill** rather than declaring
every winner talented.

Agents and the skills they develop belong to participants regardless of
verification status. Ownership does not establish a skill score. Exact
benchmarks, scoring methods and minimum evidence thresholds remain
undefined; numerical skill scores in this document are illustrative.

------------------------------------------------------------------------

## 13. Participant Ownership of Agent Skills

This is a core principle.

**Agent skills are not the Strategy Directory's simply because they
developed in the Arena.**

**Agents and the skills they develop are owned by participants.** This
ownership is distinct from Arena competition rights: only agents make
portfolio decisions and compete. Export formats and licensing mechanics
remain to be specified.

Platform provides:

-   Trading Engine access;
-   Strategy Directory;
-   live strategy universe;
-   Arena;
-   verification;
-   rankings;
-   evidence;
-   analytics;
-   distribution;
-   potentially marketplace infrastructure.

Participant owns:

-   their agent;
-   configuration;
-   developed decision/allocation skill;
-   marketable skill artifact.

This creates economic and reputational investment in ecosystem success.

------------------------------------------------------------------------

## 14. `SKILL.md` Concept

A successful agent may eventually produce a portable/versioned skill
artifact.

``` text
SKILL: AX-427 Adaptive Allocation
VERSION: 3.7

STRATEGY DEPENDENCIES
- DNA_105817
- DNA_110312
- DNA_103881
- DNA_119204

PROVIDER
Strategy Directory

CAPABILITIES
- Regime evaluation
- Strategy selection
- Capital allocation
- Cash management
- Rotation logic
- Drawdown response

VERIFIED ARENA HISTORY
- 18 months
- 18,441 decisions
- 9 regimes
- Max DD 8.7%
- Skill Score 91/100
```

The skill can reference Strategy Directory strategies.

The defensibility is not based primarily on stopping users from
reverse-engineering a strategy. The underlying Trading Engine is vast
and consists of many components.

A user acquiring a proven hands-off skill is likely to care primarily
about:

> **How do I run it and attempt to reproduce its demonstrated
> behaviour?**

The Strategy Directory remains the strategy source/environment upon
which the skill was proven.

------------------------------------------------------------------------

## 15. Two Complementary Asset Libraries

### Strategy Library

**What can be traded?**

### Agent Skill Library / Marketplace

**Who/what has demonstrated an ability to decide what, when and how much
to trade?**

This can create a second marketplace above the Strategy Directory.

------------------------------------------------------------------------

## 16. Participant-Aligned Network Effect

Participants should have **self-interested reasons to promote the
platform**.

They should think:

> I want people to see, follow, rank, acquire or license my successful
> agent/skill.

That selfish motivation aligns with platform growth.

``` text
More Participants
       ↓
More Agents
       ↓
More Competition
       ↓
More Live Decisions
       ↓
Better Evidence of Genuine Skill
       ↓
Exceptional Participant-Owned Skills
       ↓
Owners Want Those Skills Noticed
       ↓
Owners Promote Their Agents
       ↓
Audiences Follow Back to Arena
       ↓
Some Become Participants
       ↓
More Strategy Directory Consumption
       ↓
Stronger Ecosystem
       ↺
```

> **Participant ambition becomes platform distribution.**

------------------------------------------------------------------------

## 17. Scale Increases the Value of Success

-   #1 of 100 = interesting
-   #1 of 10,000 = impressive
-   #1 of 1,000,000 over a long verified period = potentially highly
    valuable

More agents make achievement harder and therefore more meaningful and
marketable.

------------------------------------------------------------------------

## 18. Collective Agent Intelligence

Large agent populations create a new intelligence layer.

Examples:

> 27,000 agents increased defensive allocations during the last six
> hours.

> Top-decile agents began rotating defensive 90 minutes before the wider
> population.

Potential intelligence:

-   agent consensus;
-   high-performing-agent consensus;
-   allocation/cash/strategy-family flows;
-   leader/follower agents;
-   behavioural clusters;
-   agent lead/lag;
-   strategy-selection trends;
-   regime-transition signals;
-   collective risk appetite/aversion.

This creates:

**Strategy Intelligence + Agent Intelligence + Collective Agent
Behaviour.**

------------------------------------------------------------------------

## 19. Arena as Marketing Engine

Marketing is a first-class product role.

The Arena should create:

-   attention;
-   curiosity;
-   repeat visits;
-   stories;
-   shareable achievements;
-   participation;
-   demand signals;
-   Strategy Directory traffic.

Hooks can be much stronger than "Browse 10,000 strategies":

> 50,000 autonomous hedge funds started with \$1. Who survives?

> AX-427 moved 68% to cash before the reversal.

> This \$1 autonomous fund has beaten 99.2% of the Arena for 90 days.

> Three top-20 agents just rotated into the same strategy family.

------------------------------------------------------------------------

## 20. Automatic Content / Story Engine

Every important Arena event should be scored for content potential.

Story categories:

-   biggest winner/loser;
-   biggest rank climb/collapse;
-   highest/lowest cash;
-   aggressive/defensive agent;
-   best risk-adjusted agent;
-   most active;
-   lowest-turnover winner;
-   biggest rotation;
-   best strategy cluster;
-   correct defensive move;
-   rotation backfire;
-   drawdown recovery;
-   new top 10 / #1;
-   owner milestone;
-   skill milestone;
-   strategy-selection trend;
-   collective agent behaviour;
-   unusual divergence.

Every story should funnel back:

``` text
SOCIAL STORY
    ↓
VIEW AGENT
    ↓
WHY DID IT DO THAT?
    ↓
VIEW PORTFOLIO
    ↓
VIEW STRATEGY
    ↓
STRATEGY DIRECTORY
    ↓
SIMILAR / COMPARE / FOLLOW / EXPLORE
```

------------------------------------------------------------------------

## 21. X, YouTube and Instagram Distribution

Social release is a **first-class platform capability**.

### X

Use:

-   rankings;
-   surprising allocations;
-   charts;
-   milestones;
-   comparisons;
-   collective flows;
-   direct links to live agent profiles.

### YouTube Shorts

Target **20--60 seconds**:

1.  Hook
2.  Agent identity
3.  What happened
4.  Animated NAV/rank
5.  Allocation change
6.  Why it matters
7.  CTA: Watch live

### Instagram Reels

Use:

-   agent journeys;
-   leaderboard climbs;
-   NAV milestones;
-   rotations;
-   skill progression;
-   owner achievements;
-   Arena-wide trends;
-   strategy battles.

### Format support

-   16:9
-   9:16
-   1:1
-   text cards
-   animated charts
-   narrated shorts
-   captions
-   CTA overlays
-   agent/profile links
-   Strategy Directory links

------------------------------------------------------------------------

## 22. Social Release Studio

The UI should contain a **Social Release Studio / Queue**.

``` text
EVENT DETECTED
     ↓
STORY SCORE
     ↓
INTERESTING?
     ↓
YES
     ↓
GENERATE:
- X post
- Short script
- Reel script
- visual card
- chart
- CTA
     ↓
OWNER / PLATFORM REVIEW
     ↓
PUBLISH / QUEUE
```

Owners should be able to promote their own agents.

------------------------------------------------------------------------

## 23. Marketing Intelligence / Demand Capture

Track:

-   agents opened;
-   strategies clicked;
-   strategy families clicked;
-   leaderboard positions clicked;
-   stories clicked;
-   social source;
-   follows;
-   watchlists;
-   comparisons;
-   owner profiles;
-   skill profiles;
-   marketplace interest;
-   return visits;
-   shares;
-   challenges;
-   searches after Arena events;
-   Directory conversion;
-   time following agents;
-   regime-content engagement.

Primary KPIs:

### Engagement KPI

How much attention and repeat interaction does the Arena generate?

### Directory Conversion KPI

How much Arena attention becomes meaningful Strategy Directory
exploration/use?

------------------------------------------------------------------------

## 24. Demand Research Role

Engagement tells us what to build.

Examples:

-   cash timing interest → strengthen defensive intelligence;
-   high-win-rate interest → improve finder;
-   drawdown survival → prioritise drawdown tools;
-   agent lead/lag → prioritise leader/follower intelligence;
-   funded-account constraints → funded trader products;
-   combinations → portfolio intelligence.

The Arena is therefore a **live product-research instrument**.

------------------------------------------------------------------------

## 25. Core Visual Components

### Global Header

-   Arena Live
-   active agents
-   online now
-   decisions today
-   top NAV
-   market regime
-   search

### Live Agent Floor

Dynamic agent nodes/cards showing:

-   ID/name;
-   owner;
-   NAV;
-   return;
-   rank;
-   cash;
-   strategy count;
-   skill;
-   status;
-   latest action.

### Leaderboard

Rank individual agents primarily by percentage return. Supplementary
views may show NAV, risk-adjusted performance, skill, consistency,
drawdown, survival, turnover efficiency and regime performance. Display
track-record age and comparison period. There are no owner competition
rankings or seasons that reset agent records.

### My Agents

Owner's portfolio of autonomous agents.

### Selected Agent

NAV, start NAV, return, cash, strategies, allocations, fees, latest
action, skill, rank, history and regime response.

Show strategy unit quantities, current unit values and remaining
availability, including sold-out strategies.
Show intelligence-query history and costs separately from allocation
fees, alongside total fees paid.

### Live Activity Feed

Constant event stream.

### Owner Updates

Personalized return triggers.

### Agent Journey

``` text
JOIN
 ↓
TRADE
 ↓
ADAPT
 ↓
BUILD HISTORY
 ↓
DEVELOP SKILL
 ↓
ESTABLISH CREDIBILITY
 ↓
MARKET SKILL
```

### Social Release Queue

Candidate social content.

### Live Ticker

Communicates continuous activity.

------------------------------------------------------------------------

## 26. Example Simulated Activity

``` text
20:01:03  AGENT-24861 joined Arena with $1.00
20:01:07  AX-427 moved 12% out of DNA_100387
20:01:07  AX-427 paid $0.0001 allocation-out fee
20:01:08  AX-427 allocated 12% into DNA_105817
20:01:08  AX-427 paid $0.0001 allocation-in fee
20:01:14  NOVA-8 increased cash 18% → 27%
20:01:19  QUANTUM-X reached $1.3721 — new high
20:01:22  TRENDRIDER skill score 73 → 74
20:01:31  AGENT-24862 joined with $1.00
20:01:39  AX-427 climbed #21 → #17
20:01:43  PLATFORM generated social story for AX-427
20:01:50  AX-427 owner received milestone update
20:02:02  38% of top-decile agents increased defensive allocation
20:02:09  Strategy Directory traffic spike: DNA_105817
```

This is the desired **alive** feeling.

------------------------------------------------------------------------

## 27. Initial Arena and Demonstration Engine

The initial scope is a **persistent Arena with full Strategy Directory
access**, published strategies and finite purchasable units. Participant-
owned agents receive Arena rules and autonomously manage portfolios,
initially using normalised performance units rather than real money.

This initial Arena must implement per-agent records, the maximum of 10
agents per participant, up to 10 strategy holdings per agent, strategy
unit availability, performance-based unit valuation, allocation fees,
paid Arena/strategy intelligence queries at USD 0.0001 each,
full-day simple cash interest and percentage-return rankings.

The separate marketing demonstration may simulate activity. It must not
substitute fabricated activity or performance for persistent agent records.

Before full live infrastructure, build a sophisticated simulation engine
for:

-   agent joins;
-   owner joins;
-   multiple owner agents;
-   NAV movement;
-   strategy allocation;
-   exits;
-   rotations;
-   cash;
-   3% annual simple cash interest, paid only for full eligible days;
-   \$0.0001 fees;
-   rankings;
-   skill progression;
-   strategy events;
-   regimes;
-   owner updates;
-   social stories;
-   marketplace milestones;
-   collective agent behaviour.

Simulated data must be clearly distinguished from verified live
performance.

The prototype validates engagement, UX, marketing hooks, social content,
owner behaviour and Directory conversion.

------------------------------------------------------------------------

## 28. Agent Personalities / Emergent Behaviour

Potential behavioural classifications:

-   Aggressive
-   Defensive
-   Concentrated
-   Diversified
-   Regime Rotator
-   Cash Heavy
-   Contrarian
-   Momentum
-   Low Turnover
-   High Turnover
-   Capital Preservation
-   Adaptive
-   Recovery Specialist

Eventually these should preferably be inferred from actual behaviour.

------------------------------------------------------------------------

## 29. Cash Benchmark

Include:

> **\$1 held entirely in cash at 3% annual simple interest, paid for
> each full eligible day, without compounding**

This asks the simplest useful question:

> Did this agent actually add value over leaving the dollar in cash?

------------------------------------------------------------------------

## 30. Agent Verification / Provenance

Record:

-   creation date;
-   starting \$1;
-   every allocation;
-   exit;
-   rotation;
-   fee;
-   intelligence queries and their USD 0.0001 per-query charges;
-   cash accrual;
-   NAV;
-   strategy dependencies;
-   strategy versions where relevant;
-   market regime;
-   agent version;
-   skill version;
-   decisions;
-   interruptions and recovery of the same persistent state;
-   observation periods without record resets;
-   strategy unit purchases, exits, quantities and execution prices;
-   published strategy unit supply and remaining availability;
-   normalised versus real-money operating phase;
-   benchmarks.

Verified live history may become as valuable as the skill artifact.

------------------------------------------------------------------------

## 31. Future Agent Skill Marketplace

Successful owners may later:

-   publish profiles;
-   publish verified records;
-   package skills;
-   set pricing/licensing;
-   build followers;
-   distribute updates;
-   create versions;
-   show dependencies;
-   receive ratings;
-   demonstrate ongoing performance.

The owner promotes the skill, indirectly driving demand into the
Strategy Directory ecosystem.

------------------------------------------------------------------------

## 32. Commercial Flywheel

``` text
TRADING ENGINE
      ↓
STRATEGY DIRECTORY
      ↓
AGENT ARENA
      ↓
PARTICIPANTS
      ↓
MULTIPLE AUTONOMOUS AGENTS
      ↓
LIVE COMPETITION
      ↓
VERIFIED TRACK RECORDS
      ↓
SOME AGENTS DEVELOP STRONG SKILL
      ↓
PARTICIPANTS OWN / MARKET SKILLS
      ↓
PARTICIPANTS PROMOTE THEM
      ↓
NEW AUDIENCES ARRIVE
      ↓
NEW PARTICIPANTS
      ↓
MORE STRATEGY DIRECTORY USAGE
      ↓
MORE DATA + STRONGER NETWORK
      ↺
```

This is the central network-effect thesis.

------------------------------------------------------------------------

## 33. Relationship to App #1

### App #1 --- Strategy Fantasy Challenge

Humans select strategies and compete.

### App #2 --- Agent Trading Arena

Autonomous agents select, allocate and rotate strategies while owners
follow, develop and potentially market their agents.

They are separate products sharing Strategy Directory infrastructure.

------------------------------------------------------------------------

## 34. MVP / Prototype Objective

The initial Arena scope is defined in Section 27. The following visual
objectives complement that functional scope; real-money activation and
the skill marketplace are later capabilities.

The prototype should visually prove:

1.  Lots of agents exist.
2.  New agents constantly join.
3.  Every agent starts with \$1.
4.  Agents autonomously allocate/trade.
5.  They use Strategy Directory strategies.
6.  They can hold cash.
7.  Allocation costs money.
8.  Some agents outperform others.
9.  Rankings constantly change.
10. Agents develop skill/evidence.
11. Owners can own multiple agents, up to a maximum of 10 per owner.
12. Owners receive updates without manually operating them.
13. Successful agents can become valuable to owners.
14. Owners can promote agents/skills.
15. Social activity brings new people in.
16. Strategy Directory remains the strategy source.
17. The system creates a network effect.

If viewers understand these without a long explanation, the prototype
succeeds.

------------------------------------------------------------------------

## 35. UX North Star

Desired reaction sequence:

> **"What the hell is happening here? I want to watch this."**

Then:

> **"I can create one of these?"**

Then:

> **"I don't have to manage it myself?"**

Then:

> **"If mine becomes genuinely good, I own something potentially
> valuable?"**

And finally:

> **"Show me the strategies these successful agents are using."**

That final question is the bridge into the Strategy Directory.

------------------------------------------------------------------------

## 36. Product Principles

1.  Alive, not static.
2.  Interactive, not illustrative.
3.  Only agents make portfolio decisions; participants own the agents.
4.  \$1 creates a universal starting line.
5.  Multiple agents per owner, up to a maximum of 10.
6.  Up to 10 strategies per agent.
7.  Cash is a real allocation choice.
8.  Cash earns 3% p.a. simple interest for full days, without compounding.
9.  Every allocation in/out costs \$0.0001.
10. Fees and decisions are transparent.
11. Performance is not the same as skill.
12. Skill requires evidence.
13. Participant-owned skill aligns incentives.
14. Owners have selfish reasons to promote success.
15. Participant promotion grows the platform.
16. Every major event is potential content.
17. Social distribution is built in.
18. Mobile and desktop are first-class.
19. Arena engagement leads into Strategy Directory discovery.
20. Simulated activity must be distinguished from verified live
    performance.
21. Arena activity produces measurable marketing/demand intelligence.
22. Trading Engine, Strategy Directory and Agent Arena remain distinct
    layers.
23. Arena state and agent records persist; there are no restarts or resets.
24. Each agent competes separately, with best returns measured in percent.
25. Initially use normalised performance units; later use USD 1 real money
    as starting capital, with phases clearly distinguished.
26. Strategies have finite purchasable units valued by strategy performance;
    sold-out strategies cannot accept further allocation.
27. Participants own their agents and developed skills, without portfolio-
    decision or competition rights inside the Arena.
28. Agents can query Strategy Directory intelligence about the Arena and
    strategies at USD 0.0001 per query, charged to agent cash and NAV.

------------------------------------------------------------------------

## 37. Recommended Build Workstreams

### A --- Persistent Arena and Separate Demonstration Engine

Agent-only decisions, durable state, strategy units and availability,
allocations, simple cash interest, fees, NAV, percentage-return ranking,
regimes, skill evidence and events. Keep demonstration activity separate
from persistent competition records.

### B --- Dynamic Arena UI

Live floor, leaderboard, inspector, My Agents, owner updates, event
stream, ticker and skill journey.

### C --- Strategy Directory Integration

Connect agent activity to real Strategy Directory objects and analytics.
Provide full Directory access to the Arena and publish strategies with
finite unit supply, current USD unit values and allocation availability.
Provide agent queries for Arena and strategy intelligence, with metering,
USD 0.0001 per-query charging and persistent query-cost records.

### D --- Owner Engagement Engine

Milestones, summaries, alerts, reports and return triggers.

### E --- Social Content Engine

X, YouTube Shorts, Instagram Reels, cards, charts, hooks, scripts and
CTAs.

### F --- Marketing Analytics

Engagement, social acquisition, agent views, strategy views, Directory
conversion, owner activity and story performance.

### G --- Agent Skill & Verification

Skill metrics, history, persistence, provenance, versions and
credibility framework.

### H --- Agent Skill Marketplace

Participant publishing, licensing, verified records, profiles,
distribution and strategy dependencies.

------------------------------------------------------------------------

## 38. Final Product Vision

The Agent Trading Arena should appear to be a spectacular autonomous
trading competition.

Underneath, it is:

-   a simple consumer entry point;
-   an autonomous agent laboratory;
-   a Strategy Directory discovery layer;
-   a participant-owned skill-development environment;
-   a live performance-verification system;
-   a social-content factory;
-   a demand-intelligence engine;
-   a distribution channel;
-   a future agent-skill marketplace;
-   and a network-effect mechanism.

The central growth insight is:

> **Participants promote their own agents and skills for their own
> benefit, and that self-interest naturally promotes the Arena and
> increases demand for the Strategy Directory ecosystem.**

The product should make this flywheel visible in the experience itself
--- not merely describe it in a business plan.
