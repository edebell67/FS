USE [tradedb]
GO

SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE OR ALTER FUNCTION dbo.fn_split_csv_with_index (@s NVARCHAR(MAX))
RETURNS @t TABLE (
  pos   INT              NOT NULL,
  value NVARCHAR(4000)   NOT NULL
)
AS
BEGIN
  IF @s IS NULL OR LTRIM(RTRIM(@s)) = '' RETURN;
  DECLARE @clean NVARCHAR(MAX) = REPLACE(REPLACE(@s, '{',''),'}','');

  DECLARE @xml XML = TRY_CAST('<x><i>' + REPLACE(@clean, ',', '</i><i>') + '</i></x>' AS XML);
  IF @xml IS NULL RETURN;

  INSERT INTO @t(pos, value)
  SELECT ROW_NUMBER() OVER (ORDER BY (SELECT 1)) AS pos,
         LTRIM(RTRIM(T.C.value('.', 'nvarchar(4000)'))) AS value
  FROM @xml.nodes('/x/i') AS T(C);

  RETURN;
END
GO