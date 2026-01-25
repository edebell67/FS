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

  side_pref             = COALESCE(j.side_pref, a.side_pref),
  leg_qty               = COALESCE(j.leg_qty, a.leg_qty),
  max_legs              = COALESCE(j.max_legs, a.max_legs),

  exec_mode             = COALESCE(j.exec_mode, a.exec_mode),
  every_minutes         = COALESCE(j.every_minutes, a.every_minutes),
  price_move_pips       = COALESCE(j.price_move_pips, a.price_move_pips),

  stagger_type          = COALESCE(j.stagger_type, a.stagger_type),
  stagger_seconds       = COALESCE(j.stagger_seconds, a.stagger_seconds),
  stagger_pips          = COALESCE(j.stagger_pips, a.stagger_pips),

  tp_pips               = COALESCE(j.tp_pips, a.tp_pips),
  sl_pips               = COALESCE(j.sl_pips, a.sl_pips),

  trailing_mode         = COALESCE(j.trailing_mode, a.trailing_mode),
  trailing_percent      = COALESCE(j.trailing_percent, a.trailing_percent),
  trailing_pips         = COALESCE(j.trailing_pips, a.trailing_pips),

  profit_protect_enabled= COALESCE(j.profit_protect_enabled, a.profit_protect_enabled),
  pp_trigger_pips       = COALESCE(j.pp_trigger_pips, a.pp_trigger_pips),
  pp_lock_percent       = COALESCE(j.pp_lock_percent, a.pp_lock_percent),

  exit_rule             = COALESCE(j.exit_rule, a.exit_rule),
  max_duration_min      = COALESCE(j.max_duration_min, a.max_duration_min),
  breakeven_trigger_pips= COALESCE(j.breakeven_trigger_pips, a.breakeven_trigger_pips)
FROM dbo.product_forex pf
OUTER APPLY dbo.fn_decode_dna_json(pf.dna_json)  AS j
OUTER APPLY dbo.fn_decode_dna_array(pf.dna_array) AS a;
GO