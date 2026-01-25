-- Create the physical cache table
IF OBJECT_ID('dbo.dna_pnl_stream_cache', 'U') IS NOT NULL
    DROP TABLE dbo.dna_pnl_stream_cache;

CREATE TABLE dbo.dna_pnl_stream_cache (
    id INT IDENTITY(1,1) PRIMARY KEY,
    model NVARCHAR(100) NOT NULL,
    product NVARCHAR(50),
    trade_date DATE NOT NULL,
    created DATETIME NOT NULL,
    signal NVARCHAR(10),
    net_return_sum FLOAT,
    alt_net_return_sum FLOAT,
    buy_net_return_sum FLOAT,
    sell_net_return_sum FLOAT,
    trade_count INT
);

-- Index for instant retrieval by date and model
CREATE INDEX IX_dna_pnl_cache_date_model ON dbo.dna_pnl_stream_cache(trade_date, model);
CREATE INDEX IX_dna_pnl_cache_created ON dbo.dna_pnl_stream_cache(created);
GO
