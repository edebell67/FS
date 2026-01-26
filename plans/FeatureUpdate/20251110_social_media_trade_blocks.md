# Gemini Coder - Plan for Social Media Trade Blocks

## 1. Understanding of Requirements

The goal was to define concise data blocks for social media updates (X, Instagram, Telegram) regarding trade generation and performance. These blocks needed to be based on the available trade data within the system, ensuring succinctness for social media platforms.

## 2. Plan of Approach

1.  **Identify Key Trade Data Points**:
    *   Reviewed `algo_viewer/tradepanel/models.py` to understand the Python data structures for `TradeData`, `TradeLifecycleEvent`, and `TradeHistoryLogEntry`.
    *   Analyzed the SQL view `dbo.vw_113_Combined_trades_all.View.sql` to identify all available fields for both open and closed trades, confirming that `tradeable <> 0` indicates actual trades.

2.  **Formulate Sample Social Media Messages**:
    *   Created sample messages for four scenarios: Trade Generation, Trade Performance Update (Open Trade), Trade Performance (Closure - Profitable Trade), and Trade Performance (Closure - Loss Trade).
    *   Ensured messages were concise and incorporated relevant data points such as `product`, `type`, `entry_price`, `trade_quantity`, `model`, `trade_reason`, `guid`, `net_return`, `alt_net_return`, `trade_duration`, and `close_type`.

3.  **Present Formulated Sample Social Media Blocks**:
    *   The samples were written to `social_media_trade_blocks_sample.md` for user review and future reference.

## 3. List of Changes

*   **`social_media_trade_blocks_sample.md`**:
    *   [x] Created and populated with sample social media messages for trade generation and performance updates, leveraging data points from `algo_viewer/tradepanel/models.py` and `dbo.vw_113_Combined_trades_all.View.sql`.
    *   The samples include:
        *   Trade Generation Alert
        *   Open Trade Performance Update
        *   Profitable Trade Closure Message
        *   Loss Trade Closure Message

---
**Date:** 2025-11-10
**Version:** 1.0.0
