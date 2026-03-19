# Trading Signal Mobile Landing IA

Source feed: `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\miniapp_feed_2026-03-06.json`
Generated from feed timestamp: `2026-03-08T18:13:40.484589+00:00`

## IA Goal

Define a mobile-first landing structure that turns the extracted miniapp feed into a clear, swipeable summary of desk state. The layout prioritizes fast scan value, graceful fallback for placeholder data, and a direct path into the ranked strategy board.

## Feed Snapshot

- Strategies available: `163`
- Open trades available: `1`
- Signals available: `4`
- Lead strategy fallback state: `unknown`
- Current open trade sample: `SHORT` at `2.038825`

## Placeholder Rules

- Replace strategy or pair value `unknown` with `Top ranked setup` and `multi-pair coverage`.
- Replace missing confidence, win rate, drawdown, or PnL with `Not available yet`.
- Replace generic trigger copy (`See strategy conditions`) with action framing such as `Open details to review live trigger logic`.
- Keep risk copy visible even when all commercial or performance fields are partial.
- Never present placeholder values as verified market claims.

## Section Map

### Hero

Purpose: establish what the product is, when the feed was last generated, and what the trader can do next.

Primary content:
- Product label: `Trading Signal Miniapp`
- Timestamp: `meta.generated_at_utc`
- Summary line: derived from `meta.counts`
- Primary CTA: `Open live board`
- Secondary CTA: `Review next actions`

Component spec:
- Compact headline block with one-line positioning statement.
- Freshness chip showing last feed generation time.
- Two-button CTA row pinned above the fold.

Bound fields:
- `meta.generated_at_utc`
- `meta.counts.strategies`
- `meta.counts.open_trades`
- `meta.counts.signals`

### KPIs

Purpose: show the desk state in three compressed metric cards immediately below the hero.

Cards:
- `Strategies Scanned`: `meta.counts.strategies`
- `Open Trades`: `meta.counts.open_trades`
- `Signals Ready`: `meta.counts.signals`

Component spec:
- 3-card horizontal or 2x2 wrap layout for narrow screens.
- Large number, short label, and optional micro-caption.
- Use neutral/fallback wording when counts are zero.

Bound fields:
- `meta.counts.strategies`
- `meta.counts.open_trades`
- `meta.counts.signals`

### Top Strategies

Purpose: rank the most relevant setups and give enough context to decide whether to drill in.

Card count:
- Default: top 3 cards on landing, with link to full board.

Card fields:
- Strategy name: `strategies[].strategy_name`
- Pair: `strategies[].pair`
- Net today: `strategies[].net_today`
- Win rate: `strategies[].win_rate`
- Drawdown: `strategies[].drawdown`
- Confidence: `strategies[].confidence`
- Source badge: `strategies[].source`

Component spec:
- Each card shows strategy title, pair/fallback pair, one primary metric (`net_today`), and two secondary metrics.
- Confidence and win rate become muted chips when null.
- A trailing chevron or `View setup` affordance signals navigation.

Fallback behavior:
- If all metrics except name are null, keep the card but collapse to `Desk-ranked strategy awaiting enriched metrics`.
- Deduplicate repeated strategy IDs before display if the UI layer supports it; otherwise cap repeated cards visually.

### Open Trades

Purpose: surface active exposure with direct awareness of side, entry, and missing risk controls.

Card fields:
- Trade id: `open_trades[].trade_id`
- Strategy id: `open_trades[].strategy_id`
- Pair: `open_trades[].pair`
- Side: `open_trades[].side`
- Entry: `open_trades[].entry`
- Stop loss: `open_trades[].sl`
- Take profit: `open_trades[].tp`
- Unrealized PnL: `open_trades[].unrealized_pnl`
- Status: `open_trades[].status`

Component spec:
- Single prominent trade card when there is one active position.
- Side rendered as the primary badge (`LONG`/`SHORT`).
- Entry shown in large type, with SL/TP/PnL grouped below.
- If SL/TP are null, show `Protection levels not supplied` to avoid implying risk controls exist.

Empty state:
- If `meta.counts.open_trades == 0`, replace the section with `No live trades in flight`.

### Next Actions

Purpose: convert signals into a short list of follow-up actions without overclaiming precision.

Card count:
- Default: top 2 signal cards plus a `See all signals` affordance.

Card fields:
- Strategy id: `signals[].strategy_id`
- Pair: `signals[].pair`
- Bias: `signals[].bias`
- Trigger text: `signals[].trigger_text`
- Invalidation text: `signals[].invalidation_text`
- Risk note: `signals[].risk_note`
- Confidence: `signals[].confidence`

Component spec:
- Action-oriented cards with `Watch`, `Validate`, or `Stand by` labels derived from bias/confidence.
- Trigger and invalidation copy stacked as short paragraphs.
- Risk note fixed at the bottom of each card.

Fallback behavior:
- Generic `unknown` and `n/a` signals should render as desk-wide monitoring actions rather than pair-specific setups.
- Null confidence should not block rendering; use `Analyst review required`.

### CTA

Purpose: close the landing page with a strong next step and product framing.

Primary CTA:
- `Open the live strategy board`

Secondary CTA:
- `Review risk notes before trading`

Component spec:
- Sticky bottom CTA bar or final full-width panel.
- Include one sentence reminding the user that the feed may contain partial instrument labels and should be validated before execution.

## Mobile Flow Order

1. Hero
2. KPIs
3. Top Strategies
4. Open Trades
5. Next Actions
6. CTA

## Card Design Rules

- Keep every card to one dominant data point and at most two secondary metrics.
- Use chips for status-like values (`SHORT`, `top20`, `Not available yet`).
- Prefer progressive disclosure over dense tables.
- Reserve warning styling for missing protection levels, stale timestamps, or invalidation/risk copy.
- Ensure all cards can collapse gracefully when fields are null or `unknown`.

## Data Binding Summary

| Section | Primary fields | Secondary fields | Fallback priority |
|---|---|---|---|
| Hero | `meta.generated_at_utc` | `meta.counts.*` | Count summary + freshness |
| KPIs | `meta.counts.*` | none | Zero-state labels |
| Top Strategies | `strategies[].strategy_name`, `net_today` | `pair`, `win_rate`, `drawdown`, `confidence`, `source` | Title + placeholder metric chips |
| Open Trades | `open_trades[].side`, `entry`, `status` | `strategy_id`, `pair`, `sl`, `tp`, `unrealized_pnl` | Side + entry + missing protection warning |
| Next Actions | `signals[].trigger_text`, `risk_note` | `bias`, `invalidation_text`, `confidence`, `pair` | Monitoring action copy |
| CTA | static copy | freshness/risk reminder | Validation reminder |

## Delivery Notes

- This IA intentionally privileges counts, exposure state, and risk framing because the current sample feed has repeated strategies and placeholder labels.
- The design should be implemented as a landing layer above the deeper strategy board rather than a full replacement for detailed analytics views.
