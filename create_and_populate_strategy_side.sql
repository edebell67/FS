-- Create strategy_side_current table
IF OBJECT_ID('dbo.strategy_side_current','U') IS NULL
BEGIN
  CREATE TABLE dbo.strategy_side_current(
    product NVARCHAR(50) NOT NULL,
    model   SYSNAME      NOT NULL,
    side    VARCHAR(8)   NULL,      -- 'BUY' | 'SELL' | NULL (no entry)
    decided_at DATETIME2(3) NOT NULL CONSTRAINT DF_strategy_side_current_decided_at DEFAULT (SYSUTCDATETIME()),
    CONSTRAINT PK_strategy_side_current PRIMARY KEY (product, model)
  );
END
GO

-- Insert sample data into strategy_side_current
INSERT INTO dbo.strategy_side_current (product, model, side)
SELECT DISTINCT pf.product, pf.model, 'BUY'
FROM dbo.product_forex pf
WHERE pf.trade_freq = 99
  AND pf.product = 'gbp'