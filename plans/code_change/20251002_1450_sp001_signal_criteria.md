# sp_001 copy-trade Signal Criteria Matrix

## v2
- **Source**: `tbl_model_signal_net` (filters `net_return_sum > @MinReturn`). Keep latest row per product/model/signal, sort by update/net return, take `@TopX`.
- **Gate**: count current open trades per signal; available slots = `@MaxOpenTrades - open(signal)`. Only signals with slots > 0 remain.
- **Outcome**: inserts both BUY and SELL candidates that still have slots (pulling defaults from last closed trade, priced with live bid/ask).

## v3
- **Source**: `tbl_model_signal_net_Xhr` (same filter logic as v2).
- **Gate / Outcome**: identical to v2 (slot-based capacity check per signal, candidates inserted while capacity remains).

## v4
- **Source**: last closed trade per signal for defaults + live quotes.
- **Decision helper**: each BUY/SELL candidate is run through `sp_700_decide_open`; `@skip_700_2` toggles the helper.
- **Gate**: enforces `@MaxOpenPerTradeReason` and the helper’s `accept` flag.
- **Outcome**: inserts whichever signals `sp_700_decide_open` approves.

## v5
- **Source**: `vw_120_buy_sell_count_hrly_change` (fields `buy_change`, `sell_change`).
- **Criteria**: qualify BUY when `buy_change` in `[0, @max_range]`; qualify SELL when `sell_change` in the same range.
- **Conflict rule**: if both qualify, keep only the larger positive change (ties cancel both).
- **Outcome**: insert qualified sides that also pass the profitability helper.

## v6
- **Source**: `vw_122_zone_counts_by_update_pivoted2` (`signal_final`).
- **Criteria**: map `signal_final` directly—BUY when `signal_final='buy'`, SELL when `'sell'`, otherwise skip.

## v7
- **Source**: `vw_123_zone_counts_with_prev`.
- **BUY**: `prev_red_buy = 0`, `red_buy > 0`, `darkgreen_buy = 0`.
- **SELL**: `prev_red_sell = 0`, `red_sell > 0`, `darkgreen_sell = 0`.

## v701
- **Source**: `vw_123_zone_counts_with_prev`.
- **BUY**: `darkgreen_buy > 0` while `darkgreen_sell = 0`.
- **SELL**: `darkgreen_sell > 0` while `darkgreen_buy = 0`.

## v702
- **Source**: `vw_123_zone_counts_with_prev`.
- **BUY**: `darkgreen_sell = 0` and `darkgreen_buy > 0`.
- **SELL**: `darkgreen_buy = 0` and `darkgreen_sell > 0`.

## v703
- **Source**: `vw_123_zone_counts_with_prev`.
- **BUY**: `(red_sell > 0 AND red_buy = 0)` OR `(red_sell > red_buy * 2)`.
- **SELL**: `(red_buy > 0 AND red_sell = 0)` OR `(red_buy > red_sell * 2)`.

## v704
- **Source**: `vw_123_zone_counts_with_prev`.
- **BUY**: `darkgreen_buy >= 0`, `darkgreen_sell = 0`, and `red_sell > red_buy * 2`.
- **SELL**: `darkgreen_sell >= 0`, `darkgreen_buy = 0`, and `red_buy > red_sell * 2`.
- **Logging**: records `dg_buy`, `dg_sell`, `red_buy`, and `red_sell` with every decision.

## v8
- **Source**: `vw_122_zone_counts_by_update_pivoted2.signal_final` (latest row).
- **Criteria**: same as v6—direct mapping of `signal_final` to BUY/SELL.

## v91
- **Strategy**: hard-coded BUY (sets `@new_signal = 'buy'`) with profitability guard; opposite opens are skipped (no forced close).

## v92
- **Strategy**: hard-coded SELL (sets `@new_signal = 'sell'`) with profitability guard; opposite opens are skipped (no forced close).
