# Synthetic Frontier sFX Derivatives Market -- Technical Design Brief (v2)

## 1. Executive Summary

sFX is a crypto-settled synthetic macro derivatives venue referencing
African currency volatility indices.

It is NOT: - A spot FX exchange - A remittance platform - A fiat
conversion service - A currency custody provider

It IS: - A volatility-driven perpetual derivatives market - Stablecoin
margined and settled - Order-book based with DAO vault backstop -
Algorithmically governed with transparent parameter bands

The system is engineered for frontier macro instability and designed to
survive volatility shocks.

------------------------------------------------------------------------

## 2. Instrument Design

### 2.1 Contract Type

-   Perpetual contracts (initially)
-   Stablecoin collateral (e.g., USDC)
-   No redeemable synthetic tokens
-   Positions only, no currency balances

### 2.2 Index Methodology

Each instrument references a Macro Volatility Index constructed from: -
Official reference rates - Offshore pricing (if available) - Parallel
market proxies (where observable) - Volatility weighting and smoothing -
Medianisation across sources

The trading price is determined by order flow. The index is used for: -
Funding rate calculation - Liquidation reference - Circuit breaker
anchoring

Price is not mechanically pegged to the index.

------------------------------------------------------------------------

## 3. Liquidity Architecture

### 3.1 Core Order Book

-   Central limit order book (CLOB)
-   Professional MM participation
-   Transparent depth visibility

### 3.2 DAO Vault Backstop

Vault provides: - Imbalance absorption - Liquidation counterparty -
Funding participation

Vault earns: - Trading fees - Funding spreads - Liquidation penalties

Exposure caps apply.

------------------------------------------------------------------------

## 4. Risk Engine Framework

### 4.1 Leverage Model

Initial leverage: 1x--2x Dynamic band: up to predefined max (e.g., 5x)

Leverage adjusts automatically based on: - Realized volatility - Vault
imbalance - Order book depth - Stress velocity

### 4.2 Funding Formula (Conceptual)

Funding Rate = f(imbalance %, volatility, open interest velocity)

Characteristics: - Continuous scaling (no cliff thresholds) - Aggressive
amplification during imbalance - Transparent calculation

### 4.3 Spread Elasticity

Minimum spread widens dynamically based on: - Volatility acceleration
(dVol/dt) - Order flow velocity - Vault imbalance - Liquidity thinning

------------------------------------------------------------------------

## 5. Stress Management Logic

### 5.1 Stress Detection Metrics

-   Volatility acceleration
-   Imbalance slope change
-   Liquidation clustering density
-   Order book thinning rate

### 5.2 Automatic Responses

-   Leverage compression
-   Funding multiplier increase
-   Spread widening
-   Position size caps tightening
-   Open interest caps enforcement

### 5.3 Circuit Breakers

Triggered when: - Index divergence exceeds predefined band - Data source
instability detected - Order book depth collapses beyond threshold

Reopening is gradual and rule-based.

------------------------------------------------------------------------

## 6. Transparency Layer

Live system state exposed publicly:

-   Vault capital
-   Long/short imbalance
-   Open interest per instrument
-   Current leverage band
-   Funding rate
-   Volatility metric
-   Risk parameter bands

Rules are deterministic and documented. Code may remain proprietary, but
formulas are visible.

------------------------------------------------------------------------

## 7. Governance Model

Governance controls: - Parameter bands (within predefined limits) - New
instrument listings - Vault allocation caps - Oracle weighting
adjustments

Emergency override logic must be predefined. Discretionary manual market
intervention is avoided.

------------------------------------------------------------------------

## 8. Instrument Isolation

-   No cross-margin initially
-   Separate vault exposure per instrument
-   Contagion containment by design

------------------------------------------------------------------------

## 9. Launch Scope

Phase 1: - 3--4 instruments (e.g., NGN, KES, GHS, ZAR macro indices) -
Low leverage - Conservative exposure caps - Focus on liquidity quality,
not volume

Phase 2: - Leverage scaling - Additional instruments - Spread
compression as depth improves

------------------------------------------------------------------------

## 10. Success Definition

Success is defined as:

-   Surviving first 30--50% macro shock
-   Vault capital intact
-   Liquidity functional
-   Funding stabilizing imbalance
-   Transparent rule execution
-   No governance panic

Long-term moat = survival + disciplined execution.

------------------------------------------------------------------------

This document outlines the technical and structural framework for a
resilient synthetic frontier macro derivatives venue.
