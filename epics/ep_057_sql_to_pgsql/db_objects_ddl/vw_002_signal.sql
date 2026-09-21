

CREATE VIEW [dbo].[vw_002_pos_buy_sell_count_gbp_tradepoint_signal]
AS
SELECT 
    SnapshotID,
    SnapshotTimestamp,
    Product,
    PositiveBuyOpen,
    PositiveSellOpen,
    PositiveSellOpen_val,
    PositiveBuyClosed,
    PositiveSellClosed,
    BlockLatestPrice,
	[TotalBuyClosed],[TotalSellClosed],
    PositiveBuyClosedSum,
    PositiveSellClosedSum,
    PositiveBuyOpenSum,
    PositiveSellOpenSum,
    /* new ratio columns: cast to int and handle division by zero */
    CAST(PositiveBuyOpenSum / NULLIF(PositiveSellOpenSum, 0) AS INT) AS PositiveSumBuyOverSell,
    CAST(PositiveSellOpenSum / NULLIF(PositiveBuyOpenSum, 0) AS INT) AS PositiveSumSellOverBuy,
    BuySellIndex,
    /* enhanced tradezone column with NoBuyTrade and NoSellTrade for intermediate BSI ranges */
    CASE 
        -- signal 'buy' when BSI exceeds dynamic max or strong buy imbalance
        WHEN BuySellIndex > (SELECT config_value FROM config WHERE config_name = 'gbp_BuySellIndex_max') 
             OR (PositiveBuyOpen > PositiveSellOpen 
                 AND PositiveSellOpen < (SELECT config_value FROM config WHERE config_name = 'gbp_tradezone_limit')) 
        THEN 'buy'
        -- signal 'NoBuyTrade' when BSI is positive but below buy threshold
        WHEN BuySellIndex > 0 
             AND BuySellIndex < (SELECT config_value FROM config WHERE config_name = 'gbp_BuySellIndex_max') 
        THEN 'NoBuyTrade'
        -- signal 'NoSellTrade' when BSI is negative but above sell threshold
        WHEN BuySellIndex < 0 
             AND BuySellIndex > (SELECT config_value FROM config WHERE config_name = 'gbp_BuySellIndex_min') 
        THEN 'NoSellTrade'
        -- signal 'sell' when BSI below dynamic min or strong sell imbalance
        WHEN BuySellIndex < (SELECT config_value FROM config WHERE config_name = 'gbp_BuySellIndex_min') 
             OR (PositiveSellOpen > PositiveBuyOpen 
                 AND PositiveBuyOpen < (SELECT config_value FROM config WHERE config_name = 'gbp_tradezone_limit')) 
        THEN 'sell'
        ELSE NULL 
    END AS tradezone,
    /* existing tradepoint logic */
    CASE 
        -- signal a “buy” when BSI just crossed above the dynamic max limit
        WHEN BuySellIndex > (SELECT config_value FROM config WHERE config_name = 'gbp_BuySellIndex_max') 
             AND LAG(BuySellIndex) OVER (PARTITION BY Product ORDER BY SnapshotTimestamp, SnapshotID) 
                 <= (SELECT config_value FROM config WHERE config_name = 'gbp_BuySellIndex_max') 
        THEN 'buy'
        -- signal a “sell” when BSI just crossed below the dynamic min limit
        WHEN BuySellIndex < (SELECT config_value FROM config WHERE config_name = 'gbp_BuySellIndex_min') 
             AND LAG(BuySellIndex) OVER (PARTITION BY Product ORDER BY SnapshotTimestamp, SnapshotID) 
                 >= (SELECT config_value FROM config WHERE config_name = 'gbp_BuySellIndex_min') 
        THEN 'sell'
        ELSE NULL 
    END AS tradepoint
FROM dbo.vw_002_pos_buy_sell_count_gbp_tradepoint;
