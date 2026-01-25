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
    signal_code        = MAX(CASE WHEN pos=1  THEN v END),
    base_qty_code      = MAX(CASE WHEN pos=2  THEN v END),
    max_legs_code      = MAX(CASE WHEN pos=3  THEN v END),
    exec_mode_code     = MAX(CASE WHEN pos=4  THEN v END),
    exec_value_code    = MAX(CASE WHEN pos=5  THEN v END),
    stagger_type_code  = MAX(CASE WHEN pos=6  THEN v END),
    stagger_value_code = MAX(CASE WHEN pos=7  THEN v END),
    tp_code            = MAX(CASE WHEN pos=8  THEN v END),
    sl_code            = MAX(CASE WHEN pos=9  THEN v END),
    trailing_mode_code = MAX(CASE WHEN pos=10 THEN v END),
    trailing_value_code= MAX(CASE WHEN pos=11 THEN v END),
    profit_protect_code= MAX(CASE WHEN pos=12 THEN v END),
    pp_trigger_code    = MAX(CASE WHEN pos=13 THEN v END),
    pp_lock_code       = MAX(CASE WHEN pos=14 THEN v END),
    exit_rule_code     = MAX(CASE WHEN pos=15 THEN v END),
    exit_value_code    = MAX(CASE WHEN pos=16 THEN v END)
  FROM bits
)
SELECT
  -- core
  side_pref = CASE signal_code WHEN 1 THEN 'BUY' WHEN 2 THEN 'SELL' ELSE 'BOTH' END,
  leg_qty   = CASE base_qty_code
                WHEN 1 THEN 30000 WHEN 2 THEN 40000 WHEN 3 THEN 50000
                WHEN 4 THEN 60000 WHEN 5 THEN 75000 WHEN 6 THEN 100000 END,
  max_legs  = CASE max_legs_code WHEN 1 THEN 1 WHEN 2 THEN 2 ELSE 3 END,

  -- execution
  exec_mode = CASE exec_mode_code
                WHEN 1 THEN 'every_minutes' WHEN 2 THEN 'price_move'
                WHEN 3 THEN 'clock_bucket' ELSE 'event_gate' END,
  every_minutes   = CASE WHEN exec_mode_code=1
                         THEN CASE exec_value_code WHEN 1 THEN 1 WHEN 2 THEN 2 WHEN 3 THEN 3 WHEN 4 THEN 5 WHEN 5 THEN 10 END END,
  price_move_pips = CASE WHEN exec_mode_code=2
                         THEN CASE exec_value_code WHEN 1 THEN 5 WHEN 2 THEN 8 WHEN 3 THEN 10 WHEN 4 THEN 15 WHEN 5 THEN 20 END END,

  -- stagger
  stagger_type = CASE stagger_type_code WHEN 0 THEN 'none' WHEN 1 THEN 'time' ELSE 'price' END,
  stagger_seconds = CASE WHEN stagger_type_code=1
                         THEN CASE stagger_value_code WHEN 1 THEN 30 WHEN 2 THEN 60 WHEN 3 THEN 120 WHEN 4 THEN 180 END END,
  stagger_pips    = CASE WHEN stagger_type_code=2
                         THEN CASE stagger_value_code WHEN 1 THEN 3 WHEN 2 THEN 5 WHEN 3 THEN 8 WHEN 4 THEN 10 END END,

  -- targets
  tp_pips = CASE tp_code WHEN 1 THEN 3 WHEN 2 THEN 5 WHEN 3 THEN 8 WHEN 4 THEN 10 WHEN 5 THEN 12 WHEN 6 THEN 15 END,
  sl_pips = CASE sl_code WHEN 1 THEN 3 WHEN 2 THEN 5 WHEN 3 THEN 7 WHEN 4 THEN 8 WHEN 5 THEN 10 END,

  -- trailing
  trailing_mode = CASE trailing_mode_code WHEN 0 THEN 'off' WHEN 1 THEN 'percent' ELSE 'pips' END,
  trailing_percent = CASE WHEN trailing_mode_code=1
                          THEN CASE trailing_value_code WHEN 1 THEN 30 WHEN 2 THEN 40 WHEN 3 THEN 50 WHEN 4 THEN 60 WHEN 5 THEN 70 WHEN 6 THEN 80 END END,
  trailing_pips    = CASE WHEN trailing_mode_code=2
                          THEN CASE trailing_value_code WHEN 1 THEN 3 WHEN 2 THEN 5 WHEN 3 THEN 8 WHEN 4 THEN 10 END END,

  -- profit protection
  profit_protect_enabled = CASE profit_protect_code WHEN 1 THEN CAST(1 AS BIT) ELSE CAST(0 AS BIT) END,
  pp_trigger_pips = CASE WHEN profit_protect_code=1
                         THEN CASE pp_trigger_code WHEN 1 THEN 5 WHEN 2 THEN 8 WHEN 3 THEN 10 WHEN 4 THEN 12 WHEN 5 THEN 15 END END,
  pp_lock_percent = CASE WHEN profit_protect_code=1
                         THEN CASE pp_lock_code WHEN 1 THEN 30 WHEN 2 THEN 40 WHEN 3 THEN 50 WHEN 4 THEN 60 WHEN 5 THEN 70 END END,

  -- exit
  exit_rule = CASE exit_rule_code WHEN 0 THEN 'none' WHEN 1 THEN 'max_duration' WHEN 2 THEN 'flip' ELSE 'breakeven_then_tp_sl' END,
  max_duration_min       = CASE WHEN exit_rule_code=1
                                THEN CASE exit_value_code WHEN 1 THEN 30 WHEN 2 THEN 60 WHEN 3 THEN 90 END END,
  breakeven_trigger_pips = CASE WHEN exit_rule_code=3
                                THEN CASE exit_value_code WHEN 1 THEN 3 WHEN 2 THEN 5 WHEN 3 THEN 8 END END;
GO