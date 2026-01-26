# Feature Documentation: Daily Negative Alt_Net Trade Summary

**File:** `Trades/trade_monitor/trade_monitor.py`
**Date:** 2025-11-27

## 1. Feature Overview

The **Daily Negative Alt_Net Trade Summary** is a specialized analysis feature within the `trade_monitor.py` script. Its primary purpose is to provide a focused, real-time view of all closed trades from the current trading day that have resulted in a loss as measured by the `Alt Net ($)` value.

This functionality serves as a critical tool for daily risk management and performance analysis, allowing a trader to quickly identify and diagnose underperforming trades and strategies without the noise of profitable trades or historical data.

## 2. Core Functionality

The feature is implemented within the `TradeLogProcessor` class and revolves around three key methods that work together to provide a hierarchical analysis of losing trades.

### 2.1. `get_negative_alt_trades_today()`

This is the foundational method that isolates the trades of interest.

-   **Data Source**: It processes trades from the `closed_trades` log directory for the current date.
-   **Filtering Criteria**:
    1.  **Metric**: It exclusively looks for trades where the `Alt Net ($)` value is less than zero (`< 0`).
    2.  **Timeframe**: It filters trades to ensure their exit, last update, or entry timestamp falls on the current calendar date.
    3.  **Visibility**: It respects the `VIEW_STATUS` configuration, excluding any trades whose `Trade Title` has been marked as 'hidden'.
-   **Output**: It returns a sorted list of individual trade data for all trades that meet these criteria.

### 2.2. `summarize_negative_alt_by_position()`

This method provides a high-level, aggregated summary of the day's losing trades.

-   **Input**: It calls `get_negative_alt_trades_today()` to get its data.
-   **Grouping**: It groups the losing trades by their `Position` (e.g., 'BUY', 'SELL', 'UNKNOWN').
-   **Aggregation**: For each position, it calculates:
    -   `Count`: The total number of losing trades.
    -   `Total Net P&L ($)`: The sum of the standard P&L for these trades.
    -   `Total Alt Net ($)`: The sum of the alternative P&L for these trades.
-   **Output**: It returns a list of summary rows, sorted to show the worst-performing positions first (by `Total Alt Net ($)`). This gives the user an immediate "top-down" view of where the biggest losses are originating from.

### 2.3. `get_negative_alt_trades_for_position(position)`

This method provides a detailed, drill-down view for a specific losing position.

-   **Input**: A specific position (e.g., 'BUY').
-   **Functionality**: It filters the list of today's negative `alt_net` trades to return only those matching the specified position.
-   **Output**: It returns a complete list of all individual trades for the selected losing position, allowing for in-depth analysis of each one.

## 3. User Workflow & Purpose

The intended user workflow for this feature is a classic "drill-down" analysis pattern, designed for rapid problem identification:

1.  **High-Level Summary**: The user first accesses a screen (likely part of the "Closed Trades Summary") that displays the output of `summarize_negative_alt_by_position()`. Here, they can immediately see if 'BUY' or 'SELL' trades are causing the most significant losses for the day.
2.  **Identify Problem Area**: The user identifies the position with the highest negative `Total Alt Net ($)`. For example, they might see that 'SELL' trades have a cumulative loss of -$5,000.
3.  **Drill Down for Details**: The user then selects that 'SELL' position. The UI calls `get_negative_alt_trades_for_position('SELL')` and displays the full list of every individual 'SELL' trade from today that contributed to that loss.
4.  **Analyze and Act**: With the detailed list, the user can now examine each losing trade's entry/exit times, associated `Trade Title`, and other parameters to understand *why* it failed and decide on a course of action (e.g., adjust strategy parameters, manually intervene, or stop a specific automated strategy).

In essence, this feature acts as a daily "hotspot" detector for trading losses, guiding the user from a general overview of "what's going wrong today?" to the specific trades that are the root cause.

---
# Enhancement: Negative Alt_Net Triggered Trades Analysis (v2) - TO BE RE-IMPLEMENTED!!!!

**Date:** 2025-11-27

### **1. Understanding of Requirements (Updated)**

The goal is to enhance the "Negative Alt_Net Trades" analysis to track and display the performance of trades that are executed immediately *after* a losing trade with the same signal.

1.  **Identify the "Trigger"**: A trade that closes with a negative `alt_net` is a "loser."
2.  **Find the "Triggered" Trade**: The system must find the very next trade executed with the exact same `signal` (or `Trade Title`) as the "loser" trade.
3.  **Create "Triggered" Lists**: These subsequent trades are collected into a new list named `"negative alt_net triggered"`.
4.  **Purpose**: To analyze the outcome of trades placed immediately after a losing trade for a specific signal, to identify patterns like repeated losses or successful reversals.
5.  **UI Display**: The results will be presented in a new, multi-level summary and drill-down interface, precisely matching the user-provided output examples. This includes a top-level summary, summaries by position for both negative and triggered trades, and finally, a detailed side-by-side list of the individual trades.

* see example  here - C:\Users\edebe\eds\plans\FeatureUpdate\20251127_1633_negAltNet_expected_outputs.txt


### **2. Implementation Plan (Updated)**

The implementation will add new aggregation and UI methods to produce the required multi-part report.

#### **File to be Modified:**

*   `C:\Users\edebe\eds\algo_viewer\trade_monitor\trade_monitor.py`

#### **Checklist of Tasks:**

1.  **[✓] Documentation**:
    *   [✓] Rename the documentation file to `20251127_1700_NegativeAltNetTriggeredTrades.md`.
    *   [✓] Append and update the plan based on user feedback and expected outputs.

2.  **[ ] Data Processing (`TradeLogProcessor` Class)**:
    *   [ ] Add a new list: `self.negative_alt_net_triggered_trades = []`.
    *   [ ] Enhance trade loading to create a master list of all trades (open and closed), sorted chronologically by entry time. This is essential for reliably finding the "next" trade.
    *   [ ] Implement `_find_negative_alt_net_triggered_trades()` to iterate through today's negative `alt_net` trades and find the corresponding "triggered" trade from the master list. This will populate `self.negative_alt_net_triggered_trades`.
    *   [ ] Implement `get_negative_alt_net_triggered_trades(self, position: str)` to return a filtered list of triggered trades for the UI.
    *   [ ] **(New)** Implement `summarize_negative_alt_triggered_by_position()` to aggregate the triggered trades by position (BUY/SELL) for the summary view.
    *   [ ] **(New)** Implement `get_overall_summary_data()` to calculate the grand totals for the top-level summary table, creating the "negative Alt_nets" and "negative Alt_nets Triggered" summary rows.

3.  **[ ] UI and Navigation**:
    * ONLY pages that will change visibly (ADDITIONAL DATA)
        * Negative Alt Net Trades by Position
        * Negative Alt Net Trades - SELL
        * Negative Alt Net Trades - BUY

   the below may need reviewing!!!!!!!!

    *   [ ] **(New)** Create a new primary view function `view_negative_analysis_dashboard(processor)`. This function will:
        *   Display the top-level summary table.
        *   Display the two summary tables grouped by position (one for negative trades, one for triggered).
        *   Prompt the user to select a position ('BUY' or 'SELL') to drill down into, or to go back.
    *   [ ] **(New)** Create a new drill-down view function `view_negative_analysis_detail(processor, position)`. This function will be called by the dashboard and will:
        *   Display the detailed list of individual negative trades for the selected position.
        *   Display the detailed list of the corresponding "triggered" trades.
    *   [ ] Integrate the new `view_negative_analysis_dashboard` into the main application's navigation map.
