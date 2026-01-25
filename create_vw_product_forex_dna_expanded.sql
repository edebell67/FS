USE [tradedb]
GO

SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE OR ALTER VIEW dbo.vw_product_forex_dna_expanded
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