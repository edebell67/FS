# Strategy Fantasy Challenge --- Functional & Implementation Specification

**Status:** Immediate implementation candidate --- App #1\
**Ecosystem:** Strategy Directory\
**Primary mode:** Human-first strategy competition\
**Architecture principle:** Create once, reuse everywhere.

## 1. Product Objective

The Strategy Fantasy Challenge is a human-first game built on top of the
Strategy Directory.

A participant builds a fantasy portfolio/list of strategies and then
chooses where that portfolio should participate.

The product must support users who: - have never used the Agent Arena; -
do not own an agent; - already own one or more agents; - want to compete
globally; - want to challenge friends privately; - want to do both; -
later decide they want an autonomous agent to trade their fantasy
portfolio.

Core journey:

``` text
DISCOVER STRATEGIES
        ↓
BUILD FANTASY PORTFOLIO
        ↓
SAVE AS PERSISTENT PORTFOLIO OBJECT
        ↓
CHOOSE DESTINATION(S)
   ↙          ↓          ↘
GLOBAL     PRIVATE       AGENT
BOARD      CHALLENGE     ARENA
```

A portfolio is created once and referenced by multiple destinations
rather than copied and recreated.

## 2. Three Core Functions

### Function 1 --- Create a Fantasy Portfolio

The human chooses a collection of Strategy Directory strategies.

Strategies can be sourced through: - Strategy Finder AI; - direct
Strategy Directory browsing; - an existing agent's current/selected
strategy list.

The resulting collection becomes a persistent Portfolio Object.

### Function 2 --- Compete / Challenge

The Portfolio Object can be submitted to one or more competition
destinations: - global leaderboard; - public competition; - private
one-to-one challenge; - private group challenge; - friends league; -
future specialist competitions.

A challenge is a destination for a portfolio, not the portfolio itself.

### Function 3 --- Send Portfolio to an Agent

The same Portfolio Object can be handed to: - an existing agent; or - a
newly created agent.

The portfolio becomes the strategy set/skill available to that agent.
The agent can then join the Agent Arena and trade. The owner is routed
to the existing Owner Screen to monitor it.

## 3. Human-First Design

The Fantasy Challenge must not require an agent.

``` text
Enter Fantasy Challenge
        ↓
Find Strategies
        ↓
Build Portfolio
        ↓
Enter Global Competition
        ↓
Challenge Friends
        ↓
Watch Leaderboards
```

The Agent Arena is an optional continuation.

After the user has built something they care about, the application can
ask:

> Would you like an agent to trade this portfolio autonomously?

## 4. Strategy Discovery --- Reuse Finder AI

The Fantasy Challenge should not build another strategy search engine.

``` text
Build Fantasy Portfolio
        ↓
Add Strategy
        ↓
Open Strategy Finder
        ↓
Describe requirements
        ↓
Finder returns Strategy Directory matches
        ↓
Add selected strategy to Portfolio
```

## 5. Portfolio Creation

The UI should support: - add strategy; - remove strategy; - inspect
strategy; - replace strategy; - use Finder AI; - import strategy list
from an owned agent; - save portfolio; - duplicate and modify
portfolio; - rename portfolio; - archive portfolio.

The number of strategies permitted may depend on competition rules.

## 6. Portfolio as a First-Class Persistent Object

The fantasy list becomes a persistent object with its own identity.

``` text
Portfolio ID: PF_00018427
Owner: OWNER_274
Name: Defensive FX Five
Strategies:
- DNA_108742
- DNA_104921
- DNA_112087
- DNA_107311
- DNA_103882
```

Destinations reference the portfolio ID. They should not independently
recreate the strategy collection unless an immutable competition
snapshot is required.

## 7. Prevent Exact Duplicate Portfolios

Users can create genuinely different combinations, but the same owner
should not accidentally create multiple portfolios containing exactly
the same strategy membership.

Generate a deterministic composition fingerprint:

``` text
sorted(strategy_ids)
        ↓
canonical representation
        ↓
composition_hash
```

If the same composition already exists, offer: - Use Existing
Portfolio - Open Existing Portfolio - Modify This Combination

## 8. Portfolio Schema

### Identity

``` text
portfolio_id
owner_id
name
description
version
created_at
updated_at
status
composition_hash
```

### Strategy Membership

``` text
strategy_id
strategy_version
position/order
weight/allocation if applicable
added_at
```

### Provenance

``` text
creation_source
created_manually
finder_generated
finder_query_id
imported_from_agent
source_agent_id
cloned_from_portfolio_id
parent_portfolio_id
```

### Objective

``` text
portfolio_objective
target_return
target_drawdown
target_volatility
target_regime
risk_preference
holding_horizon
```

### Intelligence Metadata --- for later population

``` text
portfolio_quality_score
diversification_score
consistency_score
robustness_score
regime_fit_score
evidence_confidence
correlation_score
concentration_score
estimated_drawdown
intelligence_version
last_analysed_at
```

### Lifecycle

``` text
draft
validated
submitted
active
completed
archived
```

### Destination Relationship

``` text
portfolio_destination_id
portfolio_id
destination_type
destination_id
submitted_at
status
```

## 9. Create Once --- Submit Anywhere

``` text
PF_00018427
      │
      ├── Global Weekly Competition
      ├── Ed vs John Private Challenge
      ├── Friends League #82
      ├── Agent AX-427
      └── Future Destination
```

The same portfolio may participate in multiple destinations when their
rules permit.

## 10. Global Competition

A user should be able to submit a portfolio to a global competition
without creating a private challenge.

Possible windows: - daily; - weekly; - monthly; - seasonal; - special
event; - regime-specific.

The MVP needs at least one simple global competition format.

## 11. Private Challenges

A participant can challenge: - one friend; - multiple friends; - a
private group.

Each participant selects or creates their own Portfolio Object. The
challenge references those portfolios.

## 12. Invite a Friend --- Shared Platform Service

Friend invitations must not be built only for Fantasy Challenge.

Create a reusable platform-wide Invitation Service callable by: -
Fantasy Strategy Challenge; - Agent Arena; - Strategy Directory; -
future applications.

Conceptually:

``` text
invite(
    inviter,
    destination_type,
    destination_id,
    recipient,
    context,
    message
)
```

Potential delivery channels later: - email; - share link; - SMS; -
WhatsApp/deep share; - social platforms; - in-platform notification.

Invitation context must survive account creation/authentication.

## 13. Leaderboards

Required views can include: - global; - competition; - private
challenge; - friends; - user's own positions.

The leaderboard is the main competitive feedback loop.

## 14. Scoring

The competition must use deterministic scoring.

A simple MVP can use portfolio return over the competition window.

A richer later model could use:

``` text
Fantasy Points =
Return Score
- Drawdown Penalty
+ Consistency Bonus
+ Regime Fit Bonus
```

Scoring must: - be identical for participants in the same competition; -
use a defined start/end period; - lock rules once started; - include
relevant costs; - prevent look-ahead; - be reproducible.

## 15. Portfolio Locking / Competition Snapshots

The persistent Portfolio Object can remain editable outside
competitions, but an active competition entry must be immutable.

Create a competition entry snapshot containing:

``` text
entry_id
portfolio_id
competition_id
snapshot_time
strategy_ids
weights
rules_version
scoring_version
```

## 16. Destination Validation

Before submission, validate the portfolio against destination rules: -
minimum/maximum strategies; - eligible product types; - eligible
strategy categories; - allocation limits; - dates; - strategy
availability; - destination-specific restrictions.

## 17. Send Portfolio to Agent --- Core Function

This is an explicit core capability.

``` text
Portfolio
    ↓
Send to Agent
    ↓
Existing Agent OR New Agent?
   ↙                     ↘
Select Agent         Quick Create
   ↓                     ↓
        Assign Portfolio Skill
                 ↓
            Join Arena
                 ↓
              Trade
                 ↓
       Existing Owner Screen
```

This must reuse the same agent handoff architecture used by Strategy
Finder AI.

## 18. Existing Agent Path

Retrieve the owner's agents, allow selection, and hand the portfolio to
the selected agent as its strategy set/skill according to Arena rules.

Do not duplicate Arena execution logic.

## 19. New Agent Path

If no suitable agent exists, or the owner wants another:

``` text
Create Agent
Name: Atlas
Portfolio: Defensive FX Five
Starting Arena Capital: $1.00
[ Create & Join Arena ]
```

Every individual Agent Hedge Fund starts with exactly \$1 total capital.

## 20. Portfolio-to-Agent Skill Representation

Conceptually:

``` json
{
  "skill_type": "strategy_portfolio",
  "portfolio_id": "PF_00018427",
  "portfolio_version": 1,
  "source": "strategy_fantasy_challenge"
}
```

## 21. Agent Arena Discovery Loop

``` text
Human builds fantasy portfolio
        ↓
Competes
        ↓
Becomes invested in portfolio
        ↓
"Would you like an autonomous agent to trade this?"
        ↓
Create/choose Agent
        ↓
Agent Arena
```

This introduces the Arena naturally rather than making it a
prerequisite.

## 22. Import from Agent

The reverse path is also required:

``` text
Create Fantasy Portfolio
        ↓
Import from My Agent
        ↓
Choose Agent
        ↓
Read Agent Strategy Set
        ↓
Create/reuse Portfolio Object
        ↓
Submit to Competition
```

## 23. Portfolio Provenance

Track creation source:

``` text
MANUAL
FINDER_AI
AGENT_IMPORT
PORTFOLIO_CLONE
SYSTEM_GENERATED
```

This enables later analysis of which creation methods produce successful
portfolios and Arena conversions.

## 24. Portfolio Management

Provide a My Portfolios area supporting: - view; - rename; - duplicate
and modify; - archive; - inspect strategies; - add/remove while
editable; - view destinations; - enter another competition; - challenge
friend; - send to agent.

## 25. Reusable Platform Services

The application should consume shared capabilities:

1.  Strategy Finder Service
2.  Portfolio Service
3.  Invitation Service
4.  Agent Service
5.  Agent Skill Assignment Service
6.  Agent Arena Service
7.  Existing Owner Screen
8.  Competition Service
9.  Leaderboard/Scoring Service

Platform principle:

> Build a capability once and reuse it everywhere.

## 26. Conceptual Service Interfaces

``` text
POST /portfolios
GET /portfolios/{id}
GET /owners/{owner_id}/portfolios
POST /portfolios/{id}/clone
POST /portfolios/{id}/validate

POST /finder/search

POST /competitions
GET /competitions
GET /competitions/{id}
POST /competitions/{id}/entries
GET /competitions/{id}/leaderboard

POST /invitations
GET /invitations/{invite_id}
POST /invitations/{invite_id}/accept

GET /owners/{owner_id}/agents
POST /owners/{owner_id}/agents
POST /agents/{agent_id}/skills
POST /arena/agents/{agent_id}/join
```

## 27. Analytics

Capture:

``` text
fantasy_app_opened
portfolio_creation_started
finder_opened_from_fantasy
strategy_added
strategy_removed
portfolio_created
portfolio_duplicate_detected
portfolio_saved
portfolio_submitted
global_competition_joined
private_challenge_created
invitation_created
invitation_opened
invitation_accepted
challenge_joined
competition_started
leaderboard_viewed
portfolio_sent_to_agent
existing_agent_selected
new_agent_created
agent_arena_joined
owner_screen_opened
agent_portfolio_imported
```

Important funnels:

``` text
Fantasy Visitor → Portfolio Created → Competition Entry → Return Visit
```

``` text
Fantasy Portfolio → Send to Agent → Agent Created/Selected → Arena Joined → Owner Screen
```

``` text
Challenge Created → Invitation Sent → Friend Joined → Friend Creates Portfolio
```

## 28. MVP Acceptance Criteria

### A --- Build Portfolio

-   Find strategies through Finder AI.
-   Add strategies.
-   Persist portfolio.
-   Detect exact duplicate composition.
-   Reopen portfolio.

### B --- Global Competition

-   Submit valid portfolio.
-   Snapshot/lock entry.
-   Score performance.
-   Show leaderboard.

### C --- Private Challenge

-   Create challenge.
-   Invite one or more people.
-   Invitee joins.
-   Invitee creates/selects portfolio.
-   Score participants.

### D --- Multiple Destinations

-   Same Portfolio Object can enter global and private destinations
    without recreation.

### E --- Agent Handoff

-   Send portfolio to existing agent.
-   Create new agent if needed.
-   Assign portfolio skill.
-   Join Arena.
-   Open existing Owner Screen.

### F --- Agent Import

-   Import an owned agent's strategy list into a Portfolio Object.
-   Enter it into Fantasy competition.

## 29. Implementation Workstreams

### Workstream 1 --- Portfolio Object

Schema, strategy membership, fingerprint, duplicate prevention,
provenance, lifecycle, ownership and persistence.

### Workstream 2 --- Finder Integration

Reuse Strategy Finder AI to populate portfolios.

### Workstream 3 --- Portfolio UI

Create, inspect, edit, save, clone/modify, archive and My Portfolios.

### Workstream 4 --- Competition Engine

Global competition, private challenges, destination rules, validation,
snapshots, scoring and leaderboard.

### Workstream 5 --- Shared Invitation Service

Build once as a reusable platform service and integrate Fantasy
Challenge first.

### Workstream 6 --- Agent Handoff

Reuse existing/new agent selection, skill assignment, Arena join and
Owner Screen handoff.

### Workstream 7 --- Agent Import

Use an owned agent's strategy set to seed a Fantasy Portfolio.

### Workstream 8 --- Analytics

Instrument product, social and cross-product conversion.

## 30. Separate Revisit Item --- Automated Portfolio Intelligence

This is not required for the initial Fantasy Challenge. It is a separate
cross-platform intelligence engine identified during the design
discussion.

Its role:

``` text
Strategies
    ↓
Automated Portfolio Intelligence
    ↓
Analyse combinations
    ↓
Estimate behaviour
    ↓
Compare alternatives
    ↓
Generate/evaluate portfolios
    ↓
Provide evidence-based guidance
```

Potential questions: - What happens if I combine these strategies? - Is
this portfolio genuinely diversified? - How has this combination behaved
in sideways markets? - Which strategy increases drawdown? - What
combination best matches my objective? - How confident are we based on
the evidence?

The human can disregard the recommendation; the objective is to make the
decision evidence-informed.

This engine can later serve: - Fantasy Challenge; - Strategy Finder
AI; - Portfolio Builder; - Agent Trading Arena; - autonomous agents; -
Strategy Radar; - What's Working Now?; - future applications.

## 31. Multi-Asset and Scale Requirements

Do not hard-code the portfolio architecture to FX.

The underlying ecosystem is intended to expand to: - crypto; -
futures; - equities; - other product types.

Portfolios reference Strategy Directory strategies, each of which
declares its product/product type.

The design should also assume the Strategy Directory can grow from
thousands to tens of thousands and potentially 100,000+ strategies
without redesigning the Portfolio Object.

## 32. Product Principles

1.  Human first --- no agent required.
2.  Agent optional --- powerful continuation, not entry barrier.
3.  Create once --- portfolio is persistent.
4.  Submit anywhere --- destinations reference the portfolio.
5.  Do not duplicate identical portfolios unnecessarily.
6.  Reuse Strategy Finder.
7.  Reuse agent handoff.
8.  Reuse invitations as a shared platform service.
9.  Capture portfolio provenance.
10. Preserve competition evidence and reproducibility.
11. Design the schema for future Portfolio Intelligence.
12. Design for multiple asset classes.

## 33. Final Product Loop

``` text
FIND STRATEGIES
       ↓
CREATE PORTFOLIO
       ↓
SAVE ONCE
       ↓
CHOOSE DESTINATION
  ↙         ↓          ↘
GLOBAL    FRIENDS      AGENT
  ↓         ↓            ↓
COMPETE   CHALLENGE    ARENA
  ↓         ↓            ↓
LEADERBOARD             OWNER SCREEN
```

Because the Portfolio Object persists:

``` text
CREATE ONCE
     ↓
COMPETE
     ↓
CHALLENGE
     ↓
SHARE
     ↓
SEND TO AGENT
     ↓
REUSE AGAIN
```

## 34. North Star

A new user should understand the proposition immediately:

> **Pick strategies you think will win. Build your fantasy portfolio.
> Put it up against everyone, challenge your friends, or let an
> autonomous agent take it into the Arena.**

Underneath that simple experience:

``` text
STRATEGY DIRECTORY
        ↓
STRATEGY FINDER
        ↓
PORTFOLIO OBJECT
        ↓
DESTINATION LAYER
   ↙        ↓        ↘
GLOBAL    PRIVATE    AGENT
COMPETE   CHALLENGE  ARENA
```

The first implementation should preserve that simplicity while making
every underlying capability reusable across the wider ecosystem.
