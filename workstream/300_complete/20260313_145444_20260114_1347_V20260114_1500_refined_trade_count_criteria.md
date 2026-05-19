# Refined top_trade_count Selection Criteria

## Goal Description
The objective is to refine the `top_trade_count` virtual trade selection criteria. Instead of just using trade count as a tiebreaker for PnL, the system should prioritize the strategy with the **highest trade count** among all strategies that have a **positive net return (PnL > 0)**.

## User Review Required
> [!IMPORTANT]
> This change modifies how "Leaders" are identified globally. 
> - A strategy with 50 trades and $1 profit will now beat a strategy with 5 trades and $100 profit.
> - Strategies with negative PnL will be excluded from the global leaderboard candidates.

## Proposed Changes

### [top_one_generator.py](file:///C:/Users/edebe/eds/TradeApps/breakout/top_one_generator.py)
Modify the global aggregation logic to:
1. Filter out all strategy results where `pnl <= 0`.
2. Sort the remaining strategies by `count` (descending).
3. Populate the `global` section of `_top_one.json` with these trade-count leaders.

### [common.py](file:///C:/Users/edebe/eds/TradeApps/breakout/common.py)
Ensure `_fetch_top_local_targets` correctly handles the comparison between the top Buy and top Sell when `multi_vtrade` is false:
1. Compare `trade_count` of the top Buy vs top Sell.
2. Select the one with the highest `trade_count` as the single leader.

### [constants.py](file:///C:/Users/edebe/eds/TradeApps/breakout/constants.py)
Update version to `V20260114_1500`.

## Verification Plan

### Manual Verification
1. **Check `_top_one.json`**:
   - Verify that `global.buy` and `global.sell` contain the products with the highest `trade_count` for that direction, provided their `pnl` is > 0.
   - Example: If `GBPEUR_C` BUY has 20 trades and $0.10 PnL, and `CAD` BUY has 5 trades and $100 PnL, `GBPEUR_C` should be the global buy leader.

2. **Monitor Console Logs**:
   - Verify `_manage_virtual_trades` output correctly identifies the leader with the highest trade count.
   - Example: `[V-TRADE-INFO] Single leader (top_trade_count): GBPEUR_C / LONG / breakout_...`

3. **Verify Negative PnL Exclusion**:
   - Confirm that no strategy with a negative PnL appears in the `global` section of `_top_one.json`.
 