-- Table: zone_distribution_snapshots
-- Author: Gemini
-- Create Date: 2025-11-02
-- Description: PostgreSQL table for zone distribution snapshots.

CREATE TABLE zone_distribution_snapshots (
    snapshot_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    product VARCHAR(50) NOT NULL,
    s_R9 INTEGER,
    s_R5 INTEGER,
    s_R4 INTEGER,
    s_R3 INTEGER,
    s_R2 INTEGER,
    s_R1 INTEGER,
    s_G1 INTEGER,
    s_G2 INTEGER,
    s_G3 INTEGER,
    s_G4 INTEGER,
    s_G5 INTEGER,
    s_G9 INTEGER,
    latest_price NUMERIC(18, 9),
    b_R9 INTEGER,
    b_R5 INTEGER,
    b_R4 INTEGER,
    b_R3 INTEGER,
    b_R2 INTEGER,
    b_R1 INTEGER,
    b_G1 INTEGER,
    b_G2 INTEGER,
    b_G3 INTEGER,
    b_G4 INTEGER,
    b_G5 INTEGER,
    b_G9 INTEGER
);

CREATE INDEX ix_zone_snapshots_time_product ON zone_distribution_snapshots (snapshot_time ASC, product ASC);
