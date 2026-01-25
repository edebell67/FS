USE [tradedb]
GO

SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE OR ALTER FUNCTION dbo.fn_decode_dna_array (@dna_array NVARCHAR(200))
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