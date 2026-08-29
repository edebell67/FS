# Strategy Finder AI --- Narrow Implementation Specification

**Status:** Immediate implementation scope\
**Product:** Strategy Directory / Strategy Finder AI\
**Primary objective:** Find suitable strategies, hand selected strategy
skill(s) to an agent, place the agent into the Agent Arena, and give the
owner access to the already-deployed Owner Screen.

------------------------------------------------------------------------

## 1. Purpose

This specification deliberately defines a **narrow first
implementation** of Strategy Finder AI.

Strategy Finder AI is not responsible for running the Agent Arena,
reproducing the Owner Screen, calculating the full Strategy Directory
intelligence layer, or building a complex agent-management product.

Its immediate job is:

> **Find → Select → Assign to Agent → Join Arena → Watch**

The user should be able to arrive with no existing agent, describe the
type of strategy they want, select a suitable result, create an agent if
necessary, hand the selected strategy to that agent as a skill, send the
agent into the Agent Arena to trade, and then access the existing Owner
Screen to watch what happens.

The same flow must also work for a user who already owns one or more
agents.

------------------------------------------------------------------------

## 2. Core User Journey

``` text
User enters Strategy Finder
        ↓
Describes strategy requirement
        ↓
Finder searches Strategy Directory
        ↓
Matching strategies returned
        ↓
User examines/selects strategy
        ↓
"Give to Agent"
        ↓
Does user want:
  Existing Agent
       OR
  New Agent?
        ↓
Existing → select agent
New → quick-create agent
        ↓
Selected strategy handed to agent as skill
        ↓
Agent joins Agent Arena
        ↓
Agent begins trading
        ↓
User opens existing Owner Screen
        ↓
User watches agent activity/performance
```

This is the complete MVP product loop.

------------------------------------------------------------------------

## 3. Scope Boundary

### Strategy Finder IS responsible for

1.  Capturing what kind of strategy the user wants.
2.  Searching the Strategy Directory.
3.  Returning suitable strategy candidates.
4.  Allowing a strategy to be selected.
5.  Providing a clear **Give to Agent** action.
6.  Asking whether the skill should go to:
    -   an existing agent; or
    -   a new agent.
7.  Allowing selection of an existing agent.
8.  Triggering a lightweight new-agent creation flow.
9.  Passing the selected strategy to the chosen/new agent as a skill.
10. Triggering the process that places the agent into the Agent Arena.
11. Providing a route to the existing Owner Screen.

### Strategy Finder is NOT responsible for

-   Rebuilding the Agent Arena.
-   Rebuilding the Owner Screen.
-   Providing full agent portfolio management.
-   Running trading execution itself.
-   Creating a second agent monitoring interface.
-   Implementing every future Strategy Directory intelligence capability
    in the MVP.
-   Building the final credentials/authentication architecture inside
    Finder.

These should be integrated through clean interfaces.

------------------------------------------------------------------------

## 4. Strategy Search

### 4.1 User input

The Finder should accept normal-language requirements.

Examples:

``` text
Find me a low-drawdown FX strategy.

Find strategies with a win rate above 60%.

I want something that performs well in sideways markets.

Find a strategy with steady returns.

Show me strategies with drawdown below 8%.

Find something defensive.

Find an intraday strategy for EUR/USD.
```

The user should not need to understand the Strategy Directory database
structure.

### 4.2 Requirement interpretation

The Finder converts the request into available Strategy Directory
criteria.

Example:

``` text
User:
"I want an FX strategy with drawdown below 8%
that performs well in sideways markets."

Finder interpretation:

product_type = forex
max_drawdown <= 8%
sideways_regime_fit = preferred
```

The implementation should distinguish between:

-   **hard requirements** --- must be satisfied;
-   **preferences** --- influence ranking;
-   **objective** --- what the user is trying to achieve.

### 4.3 Search execution

The Finder sends the interpreted query to the Strategy Directory
search/intelligence service.

The Finder should not independently duplicate Strategy Directory
calculations.

Conceptually:

``` text
Finder UI
   ↓
Finder Query Service
   ↓
Strategy Directory API / Intelligence Layer
   ↓
Matching Strategy Objects
```

### 4.4 Results

For MVP, each result needs enough information to make a decision without
overwhelming the user.

Recommended minimum:

-   strategy ID/model;
-   descriptive name, if available;
-   match/suitability indicator;
-   return/performance indicator;
-   win rate;
-   max drawdown;
-   trade count/evidence indicator;
-   product/product type;
-   relevant regime information;
-   concise reason it matched.

Example:

``` text
DNA_108742
Defensive Mean Reversion

Match: 94%

Max Drawdown: 5.8%
Win Rate: 64%
Trades: 3,821
Market: FX
Strongest Regime: Sideways

Why it matched:
Controlled drawdown and historically strong sideways behaviour.
```

------------------------------------------------------------------------

## 5. Strategy Selection

A user can open a strategy result for more information, but the primary
action is:

> **Give to Agent**

This action is the bridge between the Strategy Directory and the Agent
ecosystem.

For the initial implementation, avoid adding unnecessary intermediate
workflows.

The selected Strategy Directory strategy is the thing being handed to
the agent as a skill/capability to use.

------------------------------------------------------------------------

## 6. Give to Agent Decision

After the user chooses **Give to Agent**, ask one simple question:

> **Where do you want to use this strategy?**

Options:

``` text
[ Use Existing Agent ]

[ Create New Agent ]
```

This decision should occur only when required and should not interrupt
the original Finder context.

The selected strategy must remain attached to the flow.

------------------------------------------------------------------------

## 7. Existing Agent Flow

If the user selects **Use Existing Agent**, retrieve the agents
belonging to that owner.

Example:

``` text
Choose an Agent

Atlas 427
NAV: $1.0837
Arena Rank: #137

Nova 12
NAV: $1.0211
Arena Rank: #814

Quantum 8
NAV: $1.1402
Arena Rank: #41
```

The user selects the desired agent.

Then:

``` text
Selected Strategy
        ↓
Create/assign Strategy Skill
        ↓
Attach Skill to Existing Agent
        ↓
Confirm Arena status
        ↓
Agent uses skill in trading
```

If the selected agent is already participating in the Arena, the
implementation should hand the skill to that agent without creating a
duplicate agent.

The precise rules governing how an existing agent incorporates a new
skill can be handled by the Agent/Arena service. Finder only needs a
defined integration contract.

------------------------------------------------------------------------

## 8. New Agent Flow

If the user selects **Create New Agent**, the creation process should be
intentionally lightweight.

The user came to find a strategy, not to configure an artificial hedge
fund manually.

### Minimum creation objective

The system needs only enough information to create a valid Arena agent.

Possible MVP:

``` text
Agent Name:
[ Atlas ]

Selected Skill:
DNA_108742 — Defensive Mean Reversion

Starting Arena Capital:
$1.00

[ Create Agent & Join Arena ]
```

The Arena's constitutional rule remains:

> **Each individual Agent Hedge Fund starts with exactly \$1 total
> capital.**

Do not turn creation into a long configuration wizard.

Future advanced settings may include risk appetite, turnover limits,
cash constraints, strategy categories and other parameters, but they are
outside this narrow implementation unless required by the existing Arena
API.

------------------------------------------------------------------------

## 9. Strategy-to-Skill Handover

The selected Strategy Directory object must be represented in a form the
agent can consume.

For MVP, the concept can remain deliberately simple:

``` text
Strategy Directory Strategy
        ↓
Agent Skill Reference
        ↓
Agent
```

Minimum skill payload could include:

``` json
{
  "skill_type": "strategy_directory_strategy",
  "strategy_id": "DNA_108742",
  "strategy_version": "current",
  "source": "strategy_directory"
}
```

The exact schema should align with the Agent Arena implementation.

The important architectural principle is:

> The strategy remains a Strategy Directory object. The agent receives
> the capability/reference required to use it.

Do not unnecessarily copy or fork the underlying strategy
implementation.

------------------------------------------------------------------------

## 10. Join Agent Arena

After agent assignment, the flow must allow the agent to participate in
the Agent Arena.

For a new agent:

``` text
Create Agent
     ↓
Attach Skill
     ↓
Register/Join Arena
     ↓
Start Trading
```

For an existing agent:

``` text
Select Agent
     ↓
Attach Skill
     ↓
Confirm/activate Arena participation
     ↓
Continue/Start Trading
```

Finder should call the Arena integration endpoint rather than contain
Arena execution logic.

The Arena remains responsible for matters such as:

-   starting NAV;
-   allocation;
-   cash;
-   trading decisions;
-   transaction/allocation costs;
-   performance;
-   ranking;
-   events;
-   skill development;
-   live agent state.

------------------------------------------------------------------------

## 11. Completion State

The Finder flow should end with a very clear success state.

Example:

``` text
ATLAS IS IN THE ARENA

Skill:
DNA_108742 — Defensive Mean Reversion

Starting NAV:
$1.00

Status:
Trading

[ Watch Atlas in Owner Screen ]

[ Find Another Strategy ]
```

The primary CTA should be:

> **Watch Agent**

This opens/routes the user to the existing Owner Screen.

------------------------------------------------------------------------

## 12. Existing Owner Screen Integration

The Owner Screen has already been implemented and deployed.

Therefore:

**Do not create another owner dashboard inside Strategy Finder.**

Finder needs only a connection/deep link into the existing Owner Screen.

Ideally, the link opens the relevant agent directly.

Conceptual route:

``` text
/owner/agents/{agent_id}
```

or whatever routing contract the existing implementation uses.

The Owner Screen remains the place where the user sees:

-   their agent(s);
-   Arena participation;
-   NAV/performance;
-   strategy/skill activity;
-   decisions;
-   ranking;
-   trading activity;
-   relevant Arena events.

------------------------------------------------------------------------

## 13. Multiple-Agent Ownership

The platform already assumes an owner may have multiple agents.

Finder must therefore never assume:

``` text
User = one agent
```

Instead:

``` text
Owner
 ├── Agent A
 ├── Agent B
 ├── Agent C
 └── Agent N
```

Every **Give to Agent** operation must support:

-   use one of my existing agents; or
-   create another agent.

This also means repeated Finder sessions can naturally expand an owner's
agent stable.

------------------------------------------------------------------------

## 14. Authentication / Credentials

Credentials and identity architecture have not yet been finalized.

This is a platform dependency rather than a reason to complicate Finder.

The eventual system needs to know:

``` text
Who is this user?
        ↓
What owner account do they belong to?
        ↓
Which agents belong to that owner?
        ↓
Which agent can receive the skill?
```

Likely platform concepts:

-   `user_id`
-   `owner_id`
-   authenticated session/token
-   agent ownership mapping
-   authorization to assign a skill
-   authorization to join/control Arena participation

For prototype implementation, these can be represented using
mock/session identities where necessary.

However, interfaces should be designed so real authentication can
replace mock identity without redesigning the Finder.

------------------------------------------------------------------------

## 15. Minimum Service Interfaces

The implementation will likely require interfaces equivalent to the
following.

### Search strategies

``` text
POST /finder/search
```

Input:

``` json
{
  "query": "Find me low drawdown FX strategies that work in sideways markets"
}
```

Output:

``` json
{
  "interpreted_query": {},
  "strategies": []
}
```

### Get owner's agents

``` text
GET /owners/{owner_id}/agents
```

### Create agent

``` text
POST /owners/{owner_id}/agents
```

### Assign skill

``` text
POST /agents/{agent_id}/skills
```

### Join Arena

``` text
POST /arena/agents/{agent_id}/join
```

### Owner Screen deep link

``` text
GET /owner/agents/{agent_id}
```

These are conceptual contracts. Existing Arena/Owner APIs should be
reused wherever they already provide the required functionality.

------------------------------------------------------------------------

## 16. Suggested UI State Machine

``` text
FINDER_IDLE
    ↓
FINDER_SEARCHING
    ↓
RESULTS
    ↓
STRATEGY_SELECTED
    ↓
AGENT_DESTINATION
   ↙             ↘
EXISTING_AGENT   CREATE_AGENT
   ↓             ↓
AGENT_SELECTED   AGENT_CREATED
       ↘         ↙
       ASSIGN_SKILL
            ↓
        JOIN_ARENA
            ↓
       ARENA_ACTIVE
            ↓
       OWNER_SCREEN
```

Each state should have an explicit success/error condition.

------------------------------------------------------------------------

## 17. Error and Edge Cases

The MVP should gracefully handle at least:

### No strategies match

Tell the user why and allow relaxation of requirements.

Example:

``` text
No strategy meets all three requirements.

Closest matches:
- two meet the drawdown and regime requirements;
- none also meet the requested 70% win rate.

[ Show Closest Matches ]
[ Change Requirements ]
```

### User has no existing agents

If **Use Existing Agent** is selected but none exist:

``` text
You don't have an agent yet.

[ Create My First Agent ]
```

### Agent creation fails

Preserve the selected strategy and allow retry.

### Skill assignment fails

Do not send the agent into the Arena until assignment succeeds.

### Arena join fails

Do not lose the newly created agent or assigned skill. Present retry.

### Existing agent already in Arena

Do not create duplicate participation. Assign the skill according to the
Arena's existing rules.

### User exits midway

Where practical, retain the selected strategy so the user can resume.

------------------------------------------------------------------------

## 18. Analytics / Events

Even this narrow implementation should instrument the funnel.

Recommended events:

``` text
finder_opened
finder_query_submitted
finder_results_returned
finder_no_results
strategy_opened
strategy_selected
give_to_agent_clicked
existing_agent_selected
new_agent_creation_started
new_agent_created
skill_assignment_started
skill_assignment_completed
skill_assignment_failed
arena_join_started
arena_join_completed
arena_join_failed
owner_screen_opened
```

Important funnel:

``` text
Finder Search
   ↓
Strategy Selection
   ↓
Give to Agent
   ↓
Agent Selected/Created
   ↓
Skill Assigned
   ↓
Arena Joined
   ↓
Owner Screen Viewed
```

This tells us whether Finder is actually converting Strategy Directory
discovery into Arena participation.

------------------------------------------------------------------------

## 19. UX Principles

### Principle 1 --- Finder first

The user starts with a need:

> "Find me a strategy."

Do not expose unnecessary Arena complexity before they have found
something interesting.

### Principle 2 --- One obvious next step

After selection:

> **Give to Agent**

### Principle 3 --- Do not assume an agent exists

Ask:

> **Existing Agent or New Agent?**

### Principle 4 --- New agent creation must be trivial

The user should not need expertise in agent configuration.

### Principle 5 --- Do not rebuild existing products

Finder connects to:

-   Strategy Directory;
-   Agent service;
-   Agent Arena;
-   existing Owner Screen.

### Principle 6 --- Preserve context

The selected strategy must survive agent selection/creation and any
recoverable errors.

### Principle 7 --- Get the agent trading quickly

The success condition is not merely:

> "Strategy found."

It is:

> **"Strategy found, handed to an agent, and the agent is now
> participating in the Arena."**

------------------------------------------------------------------------

## 20. MVP Acceptance Criteria

The narrow Finder implementation is successful when all of the following
are possible end-to-end.

### Scenario A --- New owner / no agent

1.  User opens Finder.
2.  User describes desired strategy.
3.  Finder searches Strategy Directory.
4.  Finder returns relevant strategies.
5.  User selects a strategy.
6.  User clicks **Give to Agent**.
7.  User selects **Create New Agent**.
8.  Agent is created.
9.  Selected strategy is assigned as the agent's skill.
10. Agent joins Agent Arena.
11. Agent starts participating/trading.
12. User can open that agent in the existing Owner Screen.

### Scenario B --- Existing agent

1.  User searches Finder.
2.  User selects strategy.
3.  User clicks **Give to Agent**.
4.  User selects **Use Existing Agent**.
5.  Finder displays owner's agents.
6.  User chooses an agent.
7.  Strategy skill is assigned.
8.  Agent participates/continues in Arena according to Arena rules.
9.  User opens that agent in Owner Screen.

### Scenario C --- Multiple agents

1.  Owner has multiple agents.
2.  Finder lists them distinctly.
3.  Owner can choose which receives the strategy.
4.  Owner can alternatively create another agent.
5.  No one-agent-per-owner assumption exists anywhere in the flow.

------------------------------------------------------------------------

## 21. Recommended Implementation Order

### Workstream 1 --- Finder Search

Implement:

``` text
Natural-language requirement
→ interpreted query
→ Strategy Directory search
→ ranked results
```

### Workstream 2 --- Strategy Selection

Implement:

``` text
Result
→ strategy detail/summary
→ Give to Agent
```

### Workstream 3 --- Agent Resolution

Implement:

``` text
Give to Agent
→ Existing / New
```

Then:

``` text
Existing → retrieve/select agent
New → quick-create agent
```

### Workstream 4 --- Skill Handover

Implement:

``` text
Strategy ID
→ agent-consumable skill/reference
→ assign to agent
```

### Workstream 5 --- Arena Integration

Implement:

``` text
Agent + skill
→ Arena join/activation
→ trading state
```

### Workstream 6 --- Owner Screen Handoff

Implement:

``` text
Successful Arena participation
→ Watch Agent
→ existing Owner Screen
```

### Workstream 7 --- Credentials

Integrate the final authentication/ownership mechanism once defined.

The preceding services should already accept stable owner/user
identifiers so credentials can be added without redesign.

------------------------------------------------------------------------

## 22. What Comes Later --- Explicitly Not MVP

The architecture should allow these later, but they should not delay the
narrow flow:

-   Strategy DNA.
-   Complementary strategy discovery.
-   Opposite/inverse strategy discovery.
-   Portfolio Builder.
-   What's Working Now?
-   Strategy Radar.
-   advanced skill creation.
-   multiple-strategy skills.
-   agent skill evolution.
-   participant skill marketplace.
-   agent skill licensing.
-   complex agent configuration.
-   personalized recommendations.
-   automated portfolio construction.

The first implementation proves the smallest valuable connection:

> **Can Strategy Finder turn strategy discovery into an autonomous Arena
> participant with almost no friction?**

------------------------------------------------------------------------

## 23. Final Product Definition

### Strategy Finder AI MVP

**Input**

> "Find me a strategy that meets these requirements."

**Finder**

> "Here are the best Strategy Directory matches."

**User**

> "I want this one."

**Finder**

> "Give it to an existing agent or create a new agent?"

**User**

> "Create a new one."

**System**

> Agent created.\
> Strategy handed to agent as a skill.\
> Agent joins the Arena.\
> Agent begins trading.

**Finder**

> **Watch your agent →**

**Owner Screen**

> Shows what the agent is doing in the Agent Arena.

------------------------------------------------------------------------

# North Star

The complete experience should feel this simple:

``` text
FIND
 ↓
SELECT
 ↓
GIVE TO AGENT
 ↓
CREATE OR CHOOSE AGENT
 ↓
JOIN ARENA
 ↓
TRADE
 ↓
WATCH
```

Everything in the first implementation should support this path.

Anything that does not materially help this path should be deferred.
