# Breakout Commonization Plan

**Date:** 2025-12-18 13:00
**Owner:** Codex
**Scope:** Refactor TradeApps/breakout/breakout*.py to share a single common.py module.

## 1. Motivation & Goals
- Reduce redundant logic across breakout.py, breakout_R.py, breakout_Rev.py, and breakout_R_Rev.py.
- Centralize shared utilities (config parsing, REST fetching, JSON persistence, profitability guard, activations) in common.py.
- Keep strategy-specific behaviour (signal direction, reversal allowance) in thin subclasses so future fixes can be made once.

## 2. Shared Surfaces Identified
- Config & constants: _load_config, CONFIG, global parameters, handling multi-window settings.
- Data helpers: QuoteTick, _safe_float, _normalize_timestamp, _extract_mid_price, _flatten_payload, _candidate_api_urls, fetch_latest_quotes.
- Processor logic: constructor, _is_active, _coerce_timestamp, _save_trade_json, _finalize_trade_json, _create_tradeable_json, calculate_pnl, close_trade, display_open_trade_status, guard checks, JSON persistence, CLI wiring.
- Entry logic hooks: each script differs in how it detects a signal and whether reversals are allowed while a trade is open.

## 3. Proposed Architecture
1. common.py
   - Export shared helpers and a BaseBreakoutStrategy class encapsulating the current LiveTradingProcessor responsibilities.
   - Provide overridable hooks: determine_signal(...), allow_reversal flag, optional post_entry_hook.
   - Maintain profitability guard logic and multi-window handling centrally.
2. Strategy scripts
   - Import from common and define thin subclasses overriding the hook(s) above.
   - Keep CLI entrypoint but delegate to a helper that instantiates strategy subclasses per configured window.
3. Documentation/Test updates
   - Note new shared module structure in README and re-run compile/test commands.

## 4. Implementation Steps
1. Create TradeApps/breakout/common.py containing helper functions and BaseBreakoutStrategy.
2. Refactor breakout.py to use the base class and keep only unique breakout rules.
3. Refactor breakout_R.py to override determine_signal for reversal entries.
4. Refactor breakout_Rev.py to set allow_reversal = True for immediate flips.
5. Refactor breakout_R_Rev.py to combine reversal allowance with reversal entry logic.
6. Move the multi-window run_live_trading scaffolding into common.py (e.g., run_multiwindow(strategy_cls, ...)).
7. Update docs/tests (README note + python3 -m py_compile TradeApps/breakout/breakout*.py).

## 5. Risks & Mitigations
- Regression risk: moving logic into a base class could break edge cases. Mitigate via incremental refactor and runtime validation.
- Strategy-specific quirks: ensure hooks capture all custom behaviour (e.g., reversal window reset) before deleting old code.
- Deployment coordination: roll out during sim/off hours.

## 6. Approval Checklist
- [ ] Hook design reviewed for each strategy.
- [ ] common.py exposes same CLI/runtime surface area.
- [ ] Stakeholders approve before migration.
