ALTER TABLE combined_trades_closed_arc
ADD COLUMN trade_reason VARCHAR(200),
ADD COLUMN flip_trade BOOLEAN;
