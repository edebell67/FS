USE [tradedb]
GO

SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE OR ALTER FUNCTION dbo.fn_decode_dna_json(@dna_json NVARCHAR(MAX))
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