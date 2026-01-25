USE [tradedb]
GO

IF OBJECT_ID('dbo.sp_test_result_set', 'P') IS NOT NULL
    DROP PROCEDURE dbo.sp_test_result_set;
GO

CREATE PROCEDURE dbo.sp_test_result_set
AS
BEGIN
    SELECT 'Test Message' AS Message, GETDATE() AS CurrentTime;
END
GO