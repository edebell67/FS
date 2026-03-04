Priority: 2

decompose below into atomic tasks


sFX Unified Mobile Platform
Version 1.0
1. Product Overview
1.1 Product Name

sFX Mobile Platform

1.2 Product Type

Mobile-first synthetic macro derivatives trading platform.

1.3 Core Purpose

To provide a transparent, volatility-driven, crypto-settled derivatives market referencing frontier macro currency indices, accessible via a unified mobile interface serving multiple actor types.

The system must:

Enable price discovery via order flow

Provide transparent risk mechanics

Adapt dynamically to volatility

Expose real-time system health

Prioritise system survival

2. Product Scope
2.1 In Scope

Mobile-first trading interface

Unified role-based experience

Perpetual contracts (stablecoin settled)

Real-time volatility metrics

Vault backstop dashboard

Dynamic leverage band display

Funding rate visibility

Stress-mode system feedback

Governance parameter transparency

2.2 Out of Scope (V1)

Fiat on/off ramps

Spot FX conversion

Redemption of synthetic instruments

Cross-margin between instruments

Complex derivatives (options, structured products)

3. Target Users (Actors)
3.1 Retail Traders

Directional volatility traders needing clear risk metrics and fast execution.

3.2 Active / High-Frequency Traders

Data-sensitive users requiring funding, depth, and volatility acceleration visibility.

3.3 Market Makers (Liquidity Providers)

Inventory managers needing exposure monitoring, imbalance tracking, and risk adjustment tools.

3.4 Vault / Stakers

Capital providers requiring yield transparency and stress survivability insights.

3.5 Governance Participants

Users monitoring and voting on parameter bands.

3.6 Observers / Analysts

Users reviewing system health and macro volatility behaviour.

4. Core Product Principles

Transparency is structural, not cosmetic.

Volatility is embraced but contained.

Risk adjustments are rule-based and automatic.

System survival > short-term volume.

Same engine, different role-based emphasis.

5. Functional Requirements
5.1 Global UI Structure
5.1.1 Persistent Top Bar

Must display:

Instrument name

Live price

Volatility state (Normal/Elevated/Stress)

System state indicator

Wallet balance

Tap system state → opens stress metrics panel.

5.1.2 Bottom Navigation (Adaptive by Role)

Base Tabs:

Market

Trade / Exposure

Vault

Analytics

Account

Role-based prioritisation:

Retail → Trade primary

MM → Exposure primary

Staker → Vault primary

Governance → Governance tab enabled

5.2 Trade Module (Retail Focus)

Must include:

Live chart

Volatility overlay

Funding rate display

Dynamic leverage band display

Estimated liquidation price

Position size input

Market & limit orders

Estimated funding impact

When stress triggers:

Display volatility banner

Show leverage compression visually

Show spread floor change

No manual override allowed.

5.3 Exposure Module (MM Focus)

Must include:

Net delta per instrument

Inventory skew %

Funding forecast

Imbalance slope

Spread vs system floor

Order book depth view

Risk proximity indicators

Quick actions:

Reduce delta

Adjust quoting spread

Reduce exposure %

5.4 Vault Module (Staker Focus)

Must include:

Total vault capital

Utilisation %

Instrument exposure breakdown

Net imbalance

Current APY

Yield breakdown (fees, funding, liquidations)

Personal vault share

Drawdown tracking

Must include stress simulation tool:

User selects shock magnitude → sees projected impact.

5.5 Analytics Module

Must include:

Volatility history

Funding history

Open interest growth

Long/short ratio

Liquidation heatmap

Divergence vs index

Role-based filtering allowed.

5.6 Governance Module

Must display:

Current parameter bands

Leverage limits

Funding multiplier range

Spread floor range

Open interest caps

Proposal history

Voting status

Parameter change logs

Must show stress trigger history.

6. Risk & Stress Management UX
6.1 Stress Mode

When triggered:

System state indicator updates

Leverage band compresses automatically

Funding multiplier increases

Spread floor widens

Banner displayed globally

No emotional language.

Structured explanation available.

6.2 Transparency Layer

Every parameter change must be:

Visible

Time-stamped

Linked to trigger threshold

“Why did this change?” button must be accessible.

7. Non-Functional Requirements
7.1 Performance

Price updates < 250ms refresh

Order execution latency optimised

Real-time vault metrics < 1s delay

7.2 Reliability

Must operate during volatility spikes

No manual trading halt without predefined trigger

Circuit breakers must be rule-based

7.3 Security

Wallet-based authentication

Non-custodial where possible

Multi-layer risk validation before liquidation

8. Design Requirements
8.1 Visual System

Color logic:

Blue = Neutral

Green = Balanced

Amber = Elevated

Red = Stress

No casino visuals.
No hype animations.

Dark mode default.

8.2 Mobile-First Layout

Vertical stacking

Expandable cards

Swipe between instruments

Sticky trade panel

Collapsible analytics

Desktop may extend horizontally but must preserve mobile logic.

9. Success Metrics (V1)

System-level metrics:

Survive first volatility shock >30% move

No vault wipe event

No uncontrolled liquidation cascade

Parameter adjustments execute automatically

Liquidity remains functional during stress

User-level metrics:

Clear visibility of stress changes

No confusion regarding leverage compression

Reduced support tickets during volatility spikes

10. Risks & Mitigations
Risk	Mitigation
Thin liquidity during shock	Dynamic spread widening
Vault imbalance escalation	Funding multiplier scaling
Trader confusion	Visible rule triggers
Governance panic	Predefined parameter bands
UI overload	Role-based view layering
11. Release Phases
Phase 1

3–4 instruments

Low leverage

Conservative OI caps

Transparent metrics

Phase 2

Leverage expansion within band

Additional instruments

Governance refinement

12. Core Product Definition

sFX Mobile is:

A unified, mobile-first synthetic macro derivatives platform designed to provide structured volatility exposure with transparent, rule-based risk adaptation.

It is not a currency exchange.

It is a volatility market.

If you’d like next, we can:

- `Completion Status`: Awaiting user verification
