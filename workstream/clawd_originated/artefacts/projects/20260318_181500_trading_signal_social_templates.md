# Trading Signal Social Templates

Source feed: `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\miniapp_feed_2026-03-06.json`
Generated from feed timestamp: `2026-03-08T18:13:40.484589+00:00`

## Feed Snapshot

- Strategies available: `163`
- Open trades available: `1`
- Signals available: `4`
- Top strategy label fallback: `unknown`
- Open trade side fallback-ready sample: `SHORT` at `2.038825`

## Placeholder Rules

- Use `{{generated_at_utc}}` for freshness.
- Use `{{strategies_count}}`, `{{open_trades_count}}`, and `{{signals_count}}` for headline stats.
- Use `{{top_strategy_name}}` and `{{top_strategy_pair}}`; if the feed value is `unknown`, replace with `Top ranked strategy` and `multi-pair setup`.
- Use `{{open_trade_side}}` and `{{open_trade_entry}}`; if missing, replace with `live position` and `feed price`.
- Use `{{signal_trigger_text}}` and `{{signal_risk_note}}`; if the feed is generic, keep the copy outcome-focused instead of overclaiming.
- Keep the CTA pointed at the miniapp feed or landing demo.

## X Template

Hook:
`163 strategies scanned. 1 live trade open. 4 fresh setups on deck.`

Data Slot:
`Latest feed at {{generated_at_utc}} has {{signals_count}} signal ideas and {{open_trades_count}} open trade to review. Spotlight: {{top_strategy_name}} on {{top_strategy_pair}}.`

Body:
`Today’s miniapp snapshot compresses the desk into one glance: ranked strategies, live trade context, and the next trigger to watch. Current live position bias is {{open_trade_side}} with entry around {{open_trade_entry}}. Risk stays first: {{signal_risk_note}}.`

CTA:
`Open the miniapp feed to review the live board before the next candle prints.`

## TikTok Template

Hook:
`POV: your trading recap takes 10 seconds instead of 10 tabs.`

Data Slot:
`On-screen counters: {{strategies_count}} strategies | {{open_trades_count}} open trade | {{signals_count}} new signals | updated {{generated_at_utc}}`

Script:
`Here’s the trading signal board for today. We scanned {{strategies_count}} strategies and narrowed it to {{signals_count}} active watch items. There’s {{open_trades_count}} live position in flight, with a {{open_trade_side}} entry near {{open_trade_entry}}. If the pair label is missing, the setup still shows the desk-wide signal load and timing. Tap through if you want the ranked board, trigger notes, and risk framing in one place.`

CTA:
`Tap into the miniapp and check the live feed before you place the next trade.`

## Daily Recap Template

Hook:
`Daily desk recap: {{strategies_count}} ranked, {{open_trades_count}} live, {{signals_count}} queued.`

Data Slot:
`Feed refresh {{generated_at_utc}} | Lead setup: {{top_strategy_name}} | Trigger note: {{signal_trigger_text}}`

Body:
`The trading miniapp closed the day with {{strategies_count}} ranked strategies in the stack, {{open_trades_count}} open trade still active, and {{signals_count}} setups ready for follow-up. The current feed still has placeholder pair labels in places, so this recap should emphasize system coverage, live exposure, and risk discipline over specific instrument claims. Close with {{signal_risk_note}} to keep the recap compliant and useful.`

CTA:
`Review the full feed and carry only the validated setups into the next session.`

## Usage Notes

- Pair or strategy values marked `unknown` should never be spoken as-is in public copy.
- If `signals_count` is `0`, swap urgency language for a watchlist/no-trade framing.
- If `open_trades_count` is `0`, replace live-position references with `flat heading into the next session`.
