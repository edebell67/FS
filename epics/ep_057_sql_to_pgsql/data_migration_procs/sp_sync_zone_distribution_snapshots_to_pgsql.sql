USE [tradedb]
GO

CREATE PROCEDURE [dbo].[sp_sync_zone_distribution_snapshots_to_pgsql]
AS
BEGIN
    SET NOCOUNT ON;

    DECLARE @max_snapshot_time DATETIME;

    -- Get the max snapshot_time from the PostgreSQL table
    BEGIN TRY
        SELECT @max_snapshot_time = max_snapshot_time
        FROM OPENQUERY(PGSQL_TRADEDB, 'SELECT MAX(snapshot_time) AS max_snapshot_time FROM zone_distribution_snapshots');
    END TRY
    BEGIN CATCH
        -- Handle case where the table is empty or another error occurs
        SET @max_snapshot_time = NULL;
    END CATCH

    -- If the PostgreSQL table is empty, set a very old date
    IF @max_snapshot_time IS NULL
    BEGIN
        SET @max_snapshot_time = '1900-01-01';
    END

    -- Insert new records into the PostgreSQL table
    BEGIN TRY
        INSERT INTO OPENQUERY(PGSQL_TRADEDB, '
            SELECT
                snapshot_time, product, s_R9, s_R5, s_R4, s_R3, s_R2, s_R1, s_G1, s_G2, s_G3, s_G4, s_G5, s_G9, latest_price,
                b_R9, b_R5, b_R4, b_R3, b_R2, b_R1, b_G1, b_G2, b_G3, b_G4, b_G5, b_G9
            FROM zone_distribution_snapshots')
        SELECT
            snapshot_time, product, s_R9, s_R5, s_R4, s_R3, s_R2, s_R1, s_G1, s_G2, s_G3, s_G4, s_G5, s_G9, latest_price,
            b_R9, b_R5, b_R4, b_R3, b_R2, b_R1, b_G1, b_G2, b_G3, b_G4, b_G5, b_G9
        FROM dbo.zone_distribution_snapshots
        WHERE snapshot_time > @max_snapshot_time;

        PRINT 'Successfully synchronized zone_distribution_snapshots to PostgreSQL.';
    END TRY
    BEGIN CATCH
        PRINT 'Error synchronizing zone_distribution_snapshots to PostgreSQL.';
        -- You can add more detailed error logging here if needed
    END CATCH
END
GO
