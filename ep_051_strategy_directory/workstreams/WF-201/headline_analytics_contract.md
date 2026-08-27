# WF-201 Headline Analytics Contract

- Input is closed canonical trades only; open/unrealized rows are prohibited.
- `net_return` is consumed as already net of costs and is never reduced by commission again.
- Outcome is derived from the sign of `net_return`, never `close_type`.
- Monetary P&L and drawdown retain currency/basis; percentage values remain null without a defined capital denominator.
- Zero denominators produce null ratios with an explanatory quality state, not infinity or zero.
- Every snapshot includes evidence window, sample size/sufficiency, source watermark, methodology version and calculation timestamp.
- Publishing is atomic by `(strategy_id, methodology_version, calculated_at)` after WF103 reconciliation passes.

Test plan: golden arithmetic, independent spot checks, no-open-trade contamination, no cost duplication, no-loss ratios, zero trades, breakevens, holding times, equity/drawdown path, MFE/MAE and deterministic snapshot versioning.

