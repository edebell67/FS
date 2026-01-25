-- Create fn_split_csv_with_index function
IF OBJECT_ID('dbo.fn_split_csv_with_index', 'FN') IS NOT NULL
    DROP FUNCTION dbo.fn_split_csv_with_index
GO

CREATE FUNCTION dbo.fn_split_csv_with_index (@s NVARCHAR(MAX))
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

-- Create fn_decode_dna_array function
IF OBJECT_ID('dbo.fn_decode_dna_array', 'FN') IS NOT NULL
    DROP FUNCTION dbo.fn_decode_dna_array
GO

CREATE FUNCTION dbo.fn_decode_dna_array (@dna_array NVARCHAR(200))
RETURNS TABLE
AS
RETURN
WITH bits AS (
  SELECT pos, TRY_CAST(value AS INT) AS v
  FROM dbo.fn_split_csv_with_index(@dna_array)
),
codes AS (
  SELECT
    MAX(CASE WHEN pos=1  THEN v END) AS signal_code,
    MAX(CASE WHEN pos=2  THEN v END) AS base_qty_code,
    MAX(CASE WHEN pos=3  THEN v END) AS max_legs_code,
    MAX(CASE WHEN pos=4  THEN v END) AS exec_mode_code,
    MAX(CASE WHEN pos=5  THEN v END) AS exec_value_code,
    MAX(CASE WHEN pos=6  THEN v END) AS stagger_type_code,
    MAX(CASE WHEN pos=7  THEN v END) AS stagger_value_code,
    MAX(CASE WHEN pos=8  THEN v END) AS tp_code,
    MAX(CASE WHEN pos=9  THEN v END) AS sl_code,
    MAX(CASE WHEN pos=10 THEN v END) AS trailing_mode_code,
    MAX(CASE WHEN pos=11 THEN v END) AS trailing_value_code,
    MAX(CASE WHEN pos=12 THEN v END) AS profit_protect_code,
    MAX(CASE WHEN pos=13 THEN v END) AS pp_trigger_code,
    MAX(CASE WHEN pos=14 THEN v END) AS pp_lock_code,
    MAX(CASE WHEN pos=15 THEN v END) AS exit_rule_code,
    MAX(CASE WHEN pos=16 THEN v END) AS exit_value_code
  FROM bits
)
SELECT
  -- core
  CASE signal_code WHEN 1 THEN 'BUY' WHEN 2 THEN 'SELL' ELSE 'BOTH' END AS side_pref,
  CASE base_qty_code
    WHEN 1 THEN 30000 WHEN 2 THEN 40000 WHEN 3 THEN 50000
    WHEN 4 THEN 60000 WHEN 5 THEN 75000 WHEN 6 THEN 100000 END AS leg_qty,
  CASE max_legs_code WHEN 1 THEN 1 WHEN 2 THEN 2 ELSE 3 END AS max_legs,

  -- execution
  CASE exec_mode_code
    WHEN 1 THEN 'every_minutes' WHEN 2 THEN 'price_move'
    WHEN 3 THEN 'clock_bucket' ELSE 'event_gate' END AS exec_mode,
  CASE WHEN exec_mode_code=1
    THEN CASE exec_value_code WHEN 1 THEN 1 WHEN 2 THEN 2 WHEN 3 THEN 3 WHEN 4 THEN 5 WHEN 5 THEN 10 END END AS every_minutes,
  CASE WHEN exec_mode_code=2
    THEN CASE exec_value_code WHEN 1 THEN 5 WHEN 2 THEN 8 WHEN 3 THEN 10 WHEN 4 THEN 15 WHEN 5 THEN 20 END END AS price_move_pips,

  -- stagger
  CASE stagger_type_code WHEN 0 THEN 'none' WHEN 1 THEN 'time' ELSE 'price' END AS stagger_type,
  CASE WHEN stagger_type_code=1
    THEN CASE stagger_value_code WHEN 1 THEN 30 WHEN 2 THEN 60 WHEN 3 THEN 120 WHEN 4 THEN 180 END END AS stagger_seconds,
  CASE WHEN stagger_type_code=2
    THEN CASE stagger_value_code WHEN 1 THEN 3 WHEN 2 THEN 5 WHEN 3 THEN 8 WHEN 4 THEN 10 END END AS stagger_pips,

  -- targets
  CASE tp_code WHEN 1 THEN 3 WHEN 2 THEN 5 WHEN 3 THEN 8 WHEN 4 THEN 10 WHEN 5 THEN 12 WHEN 6 THEN 15 END AS tp_pips,
  CASE sl_code WHEN 1 THEN 3 WHEN 2 THEN 5 WHEN 3 THEN 7 WHEN 4 THEN 8 WHEN 5 THEN 10 END AS sl_pips,

  -- trailing
  CASE trailing_mode_code WHEN 0 THEN 'off' WHEN 1 THEN 'percent' ELSE 'pips' END AS trailing_mode,
  CASE WHEN trailing_mode_code=1
    THEN CASE trailing_value_code WHEN 1 THEN 30 WHEN 2 THEN 40 WHEN 3 THEN 50 WHEN 4 THEN 60 WHEN 5 THEN 70 WHEN 6 THEN 80 END END AS trailing_percent,
  CASE WHEN trailing_mode_code=2
    THEN CASE trailing_value_code WHEN 1 THEN 3 WHEN 2 THEN 5 WHEN 3 THEN 8 WHEN 4 THEN 10 END END AS trailing_pips,

  -- profit protection
  CASE profit_protect_code WHEN 1 THEN CAST(1 AS BIT) ELSE CAST(0 AS BIT) END AS profit_protect_enabled,
  CASE WHEN profit_protect_code=1
    THEN CASE pp_trigger_code WHEN 1 THEN 5 WHEN 2 THEN 8 WHEN 3 THEN 10 WHEN 4 THEN 12 WHEN 5 THEN 15 END END AS pp_trigger_pips,
  CASE WHEN profit_protect_code=1
    THEN CASE pp_lock_code WHEN 1 THEN 30 WHEN 2 THEN 40 WHEN 3 THEN 50 WHEN 4 THEN 60 WHEN 5 THEN 70 END END AS pp_lock_percent,

  -- exit
  CASE exit_rule_code WHEN 0 THEN 'none' WHEN 1 THEN 'max_duration' WHEN 2 THEN 'flip' ELSE 'breakeven_then_tp_sl' END AS exit_rule,
  CASE WHEN exit_rule_code=1
    THEN CASE exit_value_code WHEN 1 THEN 30 WHEN 2 THEN 60 WHEN 3 THEN 90 END END AS max_duration_min,
  CASE WHEN exit_rule_code=3
    THEN CASE exit_value_code WHEN 1 THEN 3 WHEN 2 THEN 5 WHEN 3 THEN 8 END END AS breakeven_trigger_pips
FROM codes;
GO

-- Create fn_decode_dna_json function
IF OBJECT_ID('dbo.fn_decode_dna_json', 'FN') IS NOT NULL
    DROP FUNCTION dbo.fn_decode_dna_json
GO

CREATE FUNCTION dbo.fn_decode_dna_json(@dna_json NVARCHAR(MAX))
RETURNS TABLE
AS
RETURN
WITH j AS (
  SELECT
    JSON_VALUE(@dna_json,'$.signal') AS side_pref,
    TRY_CAST(JSON_VALUE(@dna_json,'$.leg_qty') AS INT) AS leg_qty,
    TRY_CAST(JSON_VALUE(@dna_json,'$.max_legs') AS INT) AS max_legs,

    JSON_VALUE(@dna_json,'$.execute.mode') AS exec_mode,
    TRY_CAST(JSON_VALUE(@dna_json,'$.execute.value_code') AS INT) AS exec_value_code,

    JSON_VALUE(@dna_json,'$.stagger.type') AS stagger_type,
    TRY_CAST(JSON_VALUE(@dna_json,'$.stagger.value_code') AS INT) AS stagger_value_code,

    TRY_CAST(JSON_VALUE(@dna_json,'$.targets.tp_code') AS INT) AS tp_code,
    TRY_CAST(JSON_VALUE(@dna_json,'$.targets.sl_code') AS INT) AS sl_code,

    JSON_VALUE(@dna_json,'$.trailing.mode') AS trailing_mode,
    TRY_CAST(JSON_VALUE(@dna_json,'$.trailing.value_code') AS INT) AS trailing_value_code,

    TRY_CAST(JSON_VALUE(@dna_json,'$.profit_protect.enabled') AS BIT) AS profit_protect_enabled,
    TRY_CAST(JSON_VALUE(@dna_json,'$.profit_protect.trigger_code') AS INT) AS pp_trigger_code,
    TRY_CAST(JSON_VALUE(@dna_json,'$.profit_protect.lock_code') AS INT) AS pp_lock_code,

    JSON_VALUE(@dna_json,'$.exit.rule') AS exit_rule,
    TRY_CAST(JSON_VALUE(@dna_json,'$.exit.value_code') AS INT) AS exit_value_code
)
SELECT
  -- core
  j.side_pref, j.leg_qty, j.max_legs,
  j.exec_mode, j.stagger_type, j.trailing_mode, j.profit_protect_enabled, j.exit_rule,

  -- resolved execution
  CASE WHEN j.exec_mode='every_minutes'
       THEN CASE j.exec_value_code WHEN 1 THEN 1 WHEN 2 THEN 2 WHEN 3 THEN 3 WHEN 4 THEN 5 WHEN 5 THEN 10 END END AS every_minutes,
  CASE WHEN j.exec_mode='price_move'
       THEN CASE j.exec_value_code WHEN 1 THEN 5 WHEN 2 THEN 8 WHEN 3 THEN 10 WHEN 4 THEN 15 WHEN 5 THEN 20 END END AS price_move_pips,

  -- resolved stagger
  CASE WHEN j.stagger_type='time'
       THEN CASE j.stagger_value_code WHEN 1 THEN 30 WHEN 2 THEN 60 WHEN 3 THEN 120 WHEN 4 THEN 180 END END AS stagger_seconds,
  CASE WHEN j.stagger_type='price'
       THEN CASE j.stagger_value_code WHEN 1 THEN 3 WHEN 2 THEN 5 WHEN 3 THEN 8 WHEN 4 THEN 10 END END AS stagger_pips,

  -- targets
  CASE j.tp_code WHEN 1 THEN 3 WHEN 2 THEN 5 WHEN 3 THEN 8 WHEN 4 THEN 10 WHEN 5 THEN 12 WHEN 6 THEN 15 END AS tp_pips,
  CASE j.sl_code WHEN 1 THEN 3 WHEN 2 THEN 5 WHEN 3 THEN 7 WHEN 4 THEN 8 WHEN 5 THEN 10 END AS sl_pips,

  -- trailing
  CASE WHEN j.trailing_mode='percent'
       THEN CASE j.trailing_value_code WHEN 1 THEN 30 WHEN 2 THEN 40 WHEN 3 THEN 50 WHEN 4 THEN 60 WHEN 5 THEN 70 WHEN 6 THEN 80 END END AS trailing_percent,
  CASE WHEN j.trailing_mode='pips'
       THEN CASE j.trailing_value_code WHEN 1 THEN 3 WHEN 2 THEN 5 WHEN 3 THEN 8 WHEN 4 THEN 10 END END AS trailing_pips,

  -- profit protection
  CASE WHEN j.profit_protect_enabled=1
       THEN CASE j.pp_trigger_code WHEN 1 THEN 5 WHEN 2 THEN 8 WHEN 3 THEN 10 WHEN 4 THEN 12 WHEN 5 THEN 15 END END AS pp_trigger_pips,
  CASE WHEN j.profit_protect_enabled=1
       THEN CASE j.pp_lock_code WHEN 1 THEN 30 WHEN 2 THEN 40 WHEN 3 THEN 50 WHEN 4 THEN 60 WHEN 5 THEN 70 END END AS pp_lock_percent,

  -- exit extras
  CASE WHEN j.exit_rule='max_duration'
       THEN CASE j.exit_value_code WHEN 1 THEN 30 WHEN 2 THEN 60 WHEN 3 THEN 90 END END AS max_duration_min,
  CASE WHEN j.exit_rule='breakeven_then_tp_sl'
       THEN CASE j.exit_value_code WHEN 1 THEN 3 WHEN 2 THEN 5 WHEN 3 THEN 8 END END AS breakeven_trigger_pips
FROM j;
GO

-- Create vw_product_forex_dna_expanded view
IF OBJECT_ID('dbo.vw_product_forex_dna_expanded', 'V') IS NOT NULL
    DROP VIEW dbo.vw_product_forex_dna_expanded
GO

CREATE VIEW dbo.vw_product_forex_dna_expanded
AS
SELECT
  pf.product, pf.model,

  COALESCE(j.side_pref, a.side_pref) AS side_pref,
  COALESCE(j.leg_qty, a.leg_qty) AS leg_qty,
  COALESCE(j.max_legs, a.max_legs) AS max_legs,

  COALESCE(j.exec_mode, a.exec_mode) AS exec_mode,
  COALESCE(j.every_minutes, a.every_minutes) AS every_minutes,
  COALESCE(j.price_move_pips, a.price_move_pips) AS price_move_pips,

  COALESCE(j.stagger_type, a.stagger_type) AS stagger_type,
  COALESCE(j.stagger_seconds, a.stagger_seconds) AS stagger_seconds,
  COALESCE(j.stagger_pips, a.stagger_pips) AS stagger_pips,

  COALESCE(j.tp_pips, a.tp_pips) AS tp_pips,
  COALESCE(j.sl_pips, a.sl_pips) AS sl_pips,

  COALESCE(j.trailing_mode, a.trailing_mode) AS trailing_mode,
  COALESCE(j.trailing_percent, a.trailing_percent) AS trailing_percent,
  COALESCE(j.trailing_pips, a.trailing_pips) AS trailing_pips,

  COALESCE(j.profit_protect_enabled, a.profit_protect_enabled) AS profit_protect_enabled,
  COALESCE(j.pp_trigger_pips, a.pp_trigger_pips) AS pp_trigger_pips,
  COALESCE(j.pp_lock_percent, a.pp_lock_percent) AS pp_lock_percent,

  COALESCE(j.exit_rule, a.exit_rule) AS exit_rule,
  COALESCE(j.max_duration_min, a.max_duration_min) AS max_duration_min,
  COALESCE(j.breakeven_trigger_pips, a.breakeven_trigger_pips) AS breakeven_trigger_pips
FROM dbo.product_forex pf
OUTER APPLY dbo.fn_decode_dna_json(pf.dna_json) AS j
OUTER APPLY dbo.fn_decode_dna_array(pf.dna_array) AS a;
GO