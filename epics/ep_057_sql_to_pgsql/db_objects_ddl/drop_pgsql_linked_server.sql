USE [master]
GO

-- Drop the linked server if it exists
IF EXISTS (SELECT server_id FROM sys.servers WHERE name = N'PGSQL_TRADEDB')
EXEC master.dbo.sp_dropserver @server=N'PGSQL_TRADEDB', @droplogins='droplogins'
GO
