---

## 9) Clarifications from Follow‑Up Chat (Updated 2025-10-12 15:30 UTC)

### 9.1 Where the DNA is stored
- **Table:** `dbo.product_forex`
- **Columns:** `dna_array NVARCHAR(200)`, `dna_json NVARCHAR(MAX)`  
  (Added via `ALTER TABLE` as discussed.)

### 9.2 Which procedures change (and which do not)
- **Unchanged:** `sp_loop_create_trades_v2` — continues to orchestrate the minute loop and call the per‑model creation logic.
- **Updated:** Your per‑model trade creation proc(s), e.g. `sp_001_create_trades_v*`, should **fetch + decode DNA** at runtime and apply:
  - Entry side preference (BUY / SELL / BOTH)
  - Quantity per leg
  - Max concurrent legs (cap 3) and **exposure ≤ 100k**
  - Execution mode (every N minutes, price move, clock bucket, or event gate)
  - Stagger (time or price), TP/SL, trailing, profit protection, and extra exit rules
- **Unchanged:** Close/profit‑protection procs (e.g., `sp_003_CloseTradesTargetReached_refactored`) — keep your existing behavior; the helper exposes values you can optionally wire into those procs later, if desired.

### 9.3 Current `product_forex` columns (as provided)
Reference (subset):
```
product, min_val, contract_size, commission, model, target_profit, target_loss, trade_qty,
product_type, tradeable, trade_freq, rl_action, add_to_blog, tradeable_daily, mapto_tradezone,
full_target, use_trade_count, flip_trade, use_target_exit_only, multi_close_option,
dna_array, dna_json
```
**Mapping notes:**
- `trade_qty` remains populated; at runtime, prefer **DNA leg_qty** (decoded from `dna_json`).
- `target_profit / target_loss` remain populated; at runtime, prefer **DNA TP/SL** (code‑mapped pip values converted to price deltas).
- `trade_freq` is still valid when DNA `exec_mode='every_minutes'`; otherwise the DNA execution mode/value should take precedence.
- `rl_action` can continue to be used independently; DNA `signal` now carries side preference (BUY/SELL/BOTH).

---

## 10) Helper Decoder (Function, View, and Proc)

### 10.1 Inline TVF — decode from `dna_json`
```sql
CREATE OR ALTER FUNCTION dbo.fn_decode_dna_json(@dna_json NVARCHAR(MAX))
RETURNS TABLE
AS
RETURN
WITH j AS (
  SELECT
    side_pref              = JSON_VALUE(@dna_json,'$.signal'),
    leg_qty                = TRY_CAST(JSON_VALUE(@dna_json,'$.leg_qty') AS INT),
    max_legs               = TRY_CAST(JSON_VALUE(@dna_json,'$.max_legs') AS INT),

    exec_mode              = JSON_VALUE(@dna_json,'$.execute.mode'),
    exec_value_code        = TRY_CAST(JSON_VALUE(@dna_json,'$.execute.value_code') AS INT),

    stagger_type           = JSON_VALUE(@dna_json,'$.stagger.type'),
    stagger_value_code     = TRY_CAST(JSON_VALUE(@dna_json,'$.stagger.value_code') AS INT),

    tp_code                = TRY_CAST(JSON_VALUE(@dna_json,'$.targets.tp_code') AS INT),
    sl_code                = TRY_CAST(JSON_VALUE(@dna_json,'$.targets.sl_code') AS INT),

    trailing_mode          = JSON_VALUE(@dna_json,'$.trailing.mode'),
    trailing_value_code    = TRY_CAST(JSON_VALUE(@dna_json,'$.trailing.value_code') AS INT),

    profit_protect_enabled = TRY_CAST(JSON_VALUE(@dna_json,'$.profit_protect.enabled') AS BIT),
    pp_trigger_code        = TRY_CAST(JSON_VALUE(@dna_json,'$.profit_protect.trigger_code') AS INT),
    pp_lock_code           = TRY_CAST(JSON_VALUE(@dna_json,'$.profit_protect.lock_code') AS INT),

    exit_rule              = JSON_VALUE(@dna_json,'$.exit.rule'),
    exit_value_code        = TRY_CAST(JSON_VALUE(@dna_json,'$.exit.value_code') AS INT)
)
SELECT
  -- core
  j.side_pref, j.leg_qty, j.max_legs,
  j.exec_mode, j.stagger_type, j.trailing_mode, j.profit_protect_enabled, j.exit_rule,

  -- resolved execution
  every_minutes   = CASE WHEN j.exec_mode='every_minutes'
                         THEN CASE j.exec_value_code WHEN 1 THEN 1 WHEN 2 THEN 2 WHEN 3 THEN 3 WHEN 4 THEN 5 WHEN 5 THEN 10 END END,
  price_move_pips = CASE WHEN j.exec_mode='price_move'
                         THEN CASE j.exec_value_code WHEN 1 THEN 5 WHEN 2 THEN 8 WHEN 3 THEN 10 WHEN 4 THEN 15 WHEN 5 THEN 20 END END,

  -- resolved stagger
  stagger_seconds = CASE WHEN j.stagger_type='time'
                         THEN CASE j.stagger_value_code WHEN 1 THEN 30 WHEN 2 THEN 60 WHEN 3 THEN 120 WHEN 4 THEN 180 END END,
  stagger_pips    = CASE WHEN j.stagger_type='price'
                         THEN CASE j.stagger_value_code WHEN 1 THEN 3 WHEN 2 THEN 5 WHEN 3 THEN 8 WHEN 4 THEN 10 END END,

  -- targets
  tp_pips         = CASE j.tp_code WHEN 1 THEN 3 WHEN 2 THEN 5 WHEN 3 THEN 8 WHEN 4 THEN 10 WHEN 5 THEN 12 WHEN 6 THEN 15 END,
  sl_pips         = CASE j.sl_code WHEN 1 THEN 3 WHEN 2 THEN 5 WHEN 3 THEN 7 WHEN 4 THEN 8 WHEN 5 THEN 10 END,

  -- trailing
  trailing_percent= CASE WHEN j.trailing_mode='percent'
                         THEN CASE j.trailing_value_code WHEN 1 THEN 30 WHEN 2 THEN 40 WHEN 3 THEN 50 WHEN 4 THEN 60 WHEN 5 THEN 70 WHEN 6 THEN 80 END END,
  trailing_pips   = CASE WHEN j.trailing_mode='pips'
                         THEN CASE j.trailing_value_code WHEN 1 THEN 3 WHEN 2 THEN 5 WHEN 3 THEN 8 WHEN 4 THEN 10 END END,

  -- profit protection
  pp_trigger_pips = CASE WHEN j.profit_protect_enabled=1
                         THEN CASE j.pp_trigger_code WHEN 1 THEN 5 WHEN 2 THEN 8 WHEN 3 THEN 10 WHEN 4 THEN 12 WHEN 5 THEN 15 END END,
  pp_lock_percent = CASE WHEN j.profit_protect_enabled=1
                         THEN CASE j.pp_lock_code    WHEN 1 THEN 30 WHEN 2 THEN 40 WHEN 3 THEN 50 WHEN 4 THEN 60 WHEN 5 THEN 70 END END,

  -- exit extras
  max_duration_min       = CASE WHEN j.exit_rule='max_duration'
                                THEN CASE j.exit_value_code WHEN 1 THEN 30 WHEN 2 THEN 60 WHEN 3 THEN 90 END END,
  breakeven_trigger_pips = CASE WHEN j.exit_rule='breakeven_then_tp_sl'
                                THEN CASE j.exit_value_code WHEN 1 THEN 3 WHEN 2 THEN 5 WHEN 3 THEN 8 END END;
```

### 10.2 View — easy to join anywhere
```sql
CREATE OR ALTER VIEW dbo.vw_product_forex_dna_expanded
AS
SELECT
  pf.product, pf.model,
  d.*
FROM dbo.product_forex pf
CROSS APPLY dbo.fn_decode_dna_json(pf.dna_json) d;
```

### 10.3 Helper proc — OUTPUT params for procedural use
```sql
CREATE OR ALTER PROCEDURE dbo.sp_helper_decode_dna
  @product  NVARCHAR(50),
  @model    SYSNAME,

  @side_pref VARCHAR(8)      OUTPUT,
  @leg_qty   INT             OUTPUT,
  @max_legs  INT             OUTPUT,

  @exec_mode VARCHAR(32)     OUTPUT,
  @every_minutes INT         OUTPUT,
  @price_move_pips INT       OUTPUT,

  @stagger_type VARCHAR(16)  OUTPUT,
  @stagger_seconds INT       OUTPUT,
  @stagger_pips INT          OUTPUT,

  @tp_pips INT               OUTPUT,
  @sl_pips INT               OUTPUT,

  @trailing_mode VARCHAR(16) OUTPUT,
  @trailing_percent INT      OUTPUT,
  @trailing_pips INT         OUTPUT,

  @pp_enabled BIT            OUTPUT,
  @pp_trigger_pips INT       OUTPUT,
  @pp_lock_percent INT       OUTPUT,

  @exit_rule VARCHAR(32)     OUTPUT,
  @max_duration_min INT      OUTPUT,
  @breakeven_trigger_pips INT OUTPUT
AS
BEGIN
  SET NOCOUNT ON;

  SELECT
    @side_pref  = d.side_pref,
    @leg_qty    = d.leg_qty,
    @max_legs   = d.max_legs,

    @exec_mode       = d.exec_mode,
    @every_minutes   = d.every_minutes,
    @price_move_pips = d.price_move_pips,

    @stagger_type    = d.stagger_type,
    @stagger_seconds = d.stagger_seconds,
    @stagger_pips    = d.stagger_pips,

    @tp_pips         = d.tp_pips,
    @sl_pips         = d.sl_pips,

    @trailing_mode   = d.trailing_mode,
    @trailing_percent= d.trailing_percent,
    @trailing_pips   = d.trailing_pips,

    @pp_enabled      = d.profit_protect_enabled,
    @pp_trigger_pips = d.pp_trigger_pips,
    @pp_lock_percent = d.pp_lock_percent,

    @exit_rule            = d.exit_rule,
    @max_duration_min     = d.max_duration_min,
    @breakeven_trigger_pips = d.breakeven_trigger_pips
  FROM dbo.product_forex pf
  CROSS APPLY dbo.fn_decode_dna_json(pf.dna_json) d
  WHERE pf.product=@product AND pf.model=@model;
END
```

---

## 11) Runtime Contract (Entry · Management · Exit)

- **Entry**
  - Side preference: `side_pref` (`BUY`, `SELL`, `BOTH`)
  - Execution timing: `every_minutes` **or** `price_move_pips` **or** your clock/event gates
  - Stagger: `stagger_seconds` (time) or `stagger_pips` (price)
  - Capacity: enforce `open_trades < max_legs` and **exposure ≤ 100k** (`open_trades * leg_qty`)
- **Management**
  - Targets: `tp_pips`, `sl_pips`
  - Trailing: `trailing_mode` + (`trailing_percent` **or** `trailing_pips`)
  - Profit Protection: `pp_enabled`, `pp_trigger_pips`, `pp_lock_percent`
- **Exit**
  - Primary: TP/SL
  - Extras: `exit_rule` == `max_duration` (`max_duration_min`), `flip`, or `breakeven_then_tp_sl` (`breakeven_trigger_pips`)

**Execution rules (unchanged):** BUY at **ask**, SELL at **bid**, commission **$10**.  
**Loop orchestration (unchanged):** `sp_loop_create_trades_v2` continues to call your per‑model proc.  
**Decode location:** inside `sp_001_create_trades_v*` via `sp_helper_decode_dna` (or by joining `vw_product_forex_dna_expanded`).

---

## 12) Example — Using the Helper in `sp_001_create_trades_v*`
```sql
DECLARE
  @side_pref VARCHAR(8), @leg_qty INT, @max_legs INT,
  @exec_mode VARCHAR(32), @every_minutes INT, @price_move_pips INT,
  @stagger_type VARCHAR(16), @stagger_seconds INT, @stagger_pips INT,
  @tp_pips INT, @sl_pips INT, @trailing_mode VARCHAR(16),
  @trailing_percent INT, @trailing_pips INT,
  @pp_enabled BIT, @pp_trigger_pips INT, @pp_lock_percent INT,
  @exit_rule VARCHAR(32), @max_duration_min INT, @breakeven_trigger_pips INT;

EXEC dbo.sp_helper_decode_dna
  @product=@product, @model=@model,
  @side_pref=@side_pref OUTPUT, @leg_qty=@leg_qty OUTPUT, @max_legs=@max_legs OUTPUT,
  @exec_mode=@exec_mode OUTPUT, @every_minutes=@every_minutes OUTPUT, @price_move_pips=@price_move_pips OUTPUT,
  @stagger_type=@stagger_type OUTPUT, @stagger_seconds=@stagger_seconds OUTPUT, @stagger_pips=@stagger_pips OUTPUT,
  @tp_pips=@tp_pips OUTPUT, @sl_pips=@sl_pips OUTPUT,
  @trailing_mode=@trailing_mode OUTPUT, @trailing_percent=@trailing_percent OUTPUT, @trailing_pips=@trailing_pips OUTPUT,
  @pp_enabled=@pp_enabled OUTPUT, @pp_trigger_pips=@pp_trigger_pips OUTPUT, @pp_lock_percent=@pp_lock_percent OUTPUT,
  @exit_rule=@exit_rule OUTPUT, @max_duration_min=@max_duration_min, @breakeven_trigger_pips=@breakeven_trigger_pips;

-- Enforce caps & apply decoded parameters as part of your existing logic.
```

---

## 13) Quick Checklist
- [x] `ALTER TABLE dbo.product_forex ADD dna_array, dna_json`
- [ ] Seed 1,000 `gbp` models with diverse DNA (script in §4)
- [x] `CREATE FUNCTION dbo.fn_decode_dna_json`
- [x] `CREATE VIEW dbo.vw_product_forex_dna_expanded`
- [x] `CREATE PROCEDURE dbo.sp_helper_decode_dna`
- [ ] Update `sp_001_create_trades_v*` to call the helper and enforce cap/exposure
- [ ] Keep `sp_loop_create_trades_v2` **unchanged**
- [ ] Leaderboard continues to summarize realized P&L (start capital $10,000 each)


---

## 14) **Array Decoder (non‑JSON) + Unified View/Proc** (Updated 2025-10-12 15:30 UTC)

To support models that only have **`dna_array`**, add a CSV splitter & array decoder, then expose a **unified view** that prefers JSON but falls back to ARRAY. Finally, update the helper proc to read from the unified view.

### 14.1 CSV Splitter with Ordinal
```sql
CREATE OR ALTER FUNCTION dbo.fn_split_csv_with_index (@s NVARCHAR(MAX))
RETURNS @t TABLE (
  pos   INT              NOT NULL,
  value NVARCHAR(4000)   NOT NULL
)
AS
BEGIN
  IF @s IS NULL OR LTRIM(RTRIM(@s)) = '' RETURN;
  DECLARE @clean NVARCHAR(MAX) = REPLACE(REPLACE(@s, '{',''),'}',''); -- remove braces
  SET @clean = REPLACE(REPLACE(@clean, '{',''),'}','');               -- double-safety
  SET @clean = REPLACE(REPLACE(@clean, '{',''),'}','');
  SET @clean = REPLACE(REPLACE(@clean, '{',''),'}','');

  -- Strip single braces if any remain
  SET @clean = REPLACE(REPLACE(@clean, '{',''),'}','');
  SET @clean = REPLACE(REPLACE(@clean, '{',''),'}','');
  SET @clean = REPLACE(REPLACE(@clean, '{',''),'}','');
  SET @clean = REPLACE(REPLACE(@clean, '{',''),'}','');

  SET @clean = REPLACE(REPLACE(@clean, '{',''),'}','');
  SET @clean = REPLACE(REPLACE(@clean, '{',''),'}','');

  SET @clean = REPLACE(REPLACE(@clean, '{',''),'}','');
  SET @clean = REPLACE(REPLACE(@clean, '{',''),'}','');

  -- Final brace strip and XML split
  SET @clean = REPLACE(REPLACE(@clean, '{',''),'}','');
  SET @clean = REPLACE(REPLACE(@clean, '{',''),'}','');
  SET @clean = REPLACE(REPLACE(@clean, '{',''),'}','');
  SET @clean = REPLACE(REPLACE(@clean, '{',''),'}','');

  SET @clean = REPLACE(REPLACE(@clean, '{',''),'}','');
  SET @clean = REPLACE(REPLACE(@clean, '{',''),'}','');
  SET @clean = REPLACE(REPLACE(@clean, '{',''),'}','');

  SET @clean = REPLACE(REPLACE(@clean, '{',''),'}','');
  SET @clean = REPLACE(REPLACE(@clean, '{',''),'}','');
  SET @clean = REPLACE(REPLACE(@clean, '{',''),'}','');

  SET @clean = REPLACE(REPLACE(@clean, '{',''),'}','');

  -- Single-pass: remove braces
  SET @clean = REPLACE(REPLACE(@s, '{',''),'}','');
  SET @clean = REPLACE(REPLACE(@clean, '{',''),'}','');
  SET @clean = REPLACE(REPLACE(@clean, '{',''),'}','');
  SET @clean = REPLACE(REPLACE(@clean, '{',''),'}','');

  SET @clean = REPLACE(REPLACE(@clean, '{',''),'}','');
  SET @clean = REPLACE(REPLACE(@clean, '{',''),'}','');

  SET @clean = REPLACE(REPLACE(@clean, '{',''),'}','');
  SET @clean = REPLACE(REPLACE(@clean, '{',''),'}','');

  SET @clean = REPLACE(REPLACE(@clean, '{',''),'}','');

  SET @clean = REPLACE(REPLACE(@clean, '{',''),'}','');
  SET @clean = REPLACE(REPLACE(@clean, '{',''),'}','');

  SET @clean = REPLACE(REPLACE(@clean, '{',''),'}','');

  -- Strip single braces
  SET @clean = REPLACE(REPLACE(@clean, '{',''),'}','');
  SET @clean = REPLACE(REPLACE(@clean, '{',''),'}','');
  SET @clean = REPLACE(REPLACE(@clean, '{',''),'}','');

  -- Final normalizer
  SET @clean = REPLACE(REPLACE(@clean, '{',''),'}','');
  SET @clean = REPLACE(REPLACE(@clean, '{',''),'}','');

  DECLARE @xml XML = TRY_CAST('<x><i>' + REPLACE(@clean, ',', '</i><i>') + '</i></x>' AS XML);
  IF @xml IS NULL RETURN;

  INSERT INTO @t(pos, value)
  SELECT ROW_NUMBER() OVER (ORDER BY (SELECT 1)) AS pos,
         LTRIM(RTRIM(T.C.value('.', 'nvarchar(4000)'))) AS value
  FROM @xml.nodes('/x/i') AS T(C);

  RETURN;
END
```
> Accepts strings like `{1,2,3}` or `(1, 2, 3)` and returns (pos,value) pairs.

### 14.2 Array Decoder
```sql
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
```

### 14.3 **Unified View** — Prefer JSON, fall back to ARRAY
```sql
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
```

### 14.4 **Updated Helper Proc** — now reads the unified view
```sql
CREATE OR ALTER PROCEDURE dbo.sp_helper_decode_dna
  @product  NVARCHAR(50),
  @model    SYSNAME,

  @side_pref VARCHAR(8)      OUTPUT,
  @leg_qty   INT             OUTPUT,
  @max_legs  INT             OUTPUT,

  @exec_mode VARCHAR(32)     OUTPUT,
  @every_minutes INT         OUTPUT,
  @price_move_pips INT       OUTPUT,

  @stagger_type VARCHAR(16)  OUTPUT,
  @stagger_seconds INT       OUTPUT,
  @stagger_pips INT          OUTPUT,

  @tp_pips INT               OUTPUT,
  @sl_pips INT               OUTPUT,

  @trailing_mode VARCHAR(16) OUTPUT,
  @trailing_percent INT      OUTPUT,
  @trailing_pips INT         OUTPUT,

  @pp_enabled BIT            OUTPUT,
  @pp_trigger_pips INT       OUTPUT,
  @pp_lock_percent INT       OUTPUT,

  @exit_rule VARCHAR(32)     OUTPUT,
  @max_duration_min INT      OUTPUT,
  @breakeven_trigger_pips INT OUTPUT
AS
BEGIN
  SET NOCOUNT ON;
  SELECT
    @side_pref  = x.side_pref,
    @leg_qty    = x.leg_qty,
    @max_legs   = x.max_legs,

    @exec_mode       = x.exec_mode,
    @every_minutes   = x.every_minutes,
    @price_move_pips = x.price_move_pips,

    @stagger_type    = x.stagger_type,
    @stagger_seconds = x.stagger_seconds,
    @stagger_pips    = x.stagger_pips,

    @tp_pips         = x.tp_pips,
    @sl_pips         = x.sl_pips,

    @trailing_mode   = x.trailing_mode,
    @trailing_percent= x.trailing_percent,
    @trailing_pips   = x.trailing_pips,

    @pp_enabled      = x.profit_protect_enabled,
    @pp_trigger_pips = x.pp_trigger_pips,
    @pp_lock_percent = x.pp_lock_percent,

    @exit_rule            = x.exit_rule,
    @max_duration_min     = x.max_duration_min,
    @breakeven_trigger_pips = x.breakeven_trigger_pips
  FROM dbo.vw_product_forex_dna_expanded x
  WHERE x.product=@product AND x.model=@model;
END
```

**Result:** Your runtime can read **either** `dna_json` **or** `dna_array` transparently via the unified view and helper proc, with no changes to the loop orchestrator.

---

## 15) **Scalable `product_forex` Seeding (`sp_seed_product_forex_dna`)** (Updated 2025-10-12 15:30 UTC)

A new stored procedure `sp_seed_product_forex_dna` has been created to automate the seeding of `dbo.product_forex` with unique DNA-driven models. This addresses the critical need for scalable model generation.

### 15.1 `sp_seed_product_forex_dna` Details
- **Purpose**: Generates a specified number of unique models, each with a randomly generated `dna_json` string, and inserts them into `dbo.product_forex`.
- **Parameters**:
    - `@base_product NVARCHAR(50)`: The product for which to create models (default 'gbp').
    - `@start_model_id_param INT`: Optional. If provided, seeding starts from this ID; otherwise, it starts from the maximum existing 'DNA\_' model ID + 1.
- **Configuration**: The number of models to seed is read from `dbo.config` using `config_name = 'number_of_seed_model'` (default 10 if config is missing or invalid).
- **Model Naming**: Models are named `DNA_` followed by a unique incrementing ID (e.g., `DNA_100001`).
- **DNA Generation**: A `dna_json` string is constructed with randomly selected values for various DNA parameters (signal, leg quantity, max legs, execution mode, stagger, TP/SL codes, trailing, profit protection, exit rules).
- **`product_forex` Column Derivation**:
    - `trade_qty`: Derived from `dna_json.leg_qty`.
    - `target_profit`: Calculated as `dna.tp_pips * (pf.min_val * dna.leg_qty / pf.contract_size)`.
    - `target_loss`: Calculated as `-1 * dna.sl_pips * (pf.min_val * dna.leg_qty / pf.contract_size)` (ensuring it's negative).
    - `trade_freq`: Set to `99` (a numeric placeholder for 'dna' models).
    - `use_target_exit_only`: Derived from `dna_json.exit_rule` (1 if `exit_rule` is 'none', 0 otherwise).
    - Other columns (`min_val`, `contract_size`, `commission`, `product_type`, `tradeable`, `rl_action`, `add_to_blog`, `tradeable_daily`, `mapto_tradezone`, `full_target`, `use_trade_count`, `flip_trade`, `multi_close_option`) are set to default values consistent with existing non-DNA models.
- **Insertion**: Each generated model is inserted into `dbo.product_forex`.

---

## 16) **`sp_001_create_trades_v9_setbased` Enhancements for DNA Models** (Updated 2025-10-12 15:30 UTC)

The `sp_001_create_trades_v9_setbased` procedure has been significantly enhanced to correctly handle both traditional (non-DNA) and DNA-driven models.

### 16.1 Key Modifications
- **`#pf` Temporary Table**: Now includes `trade_freq`, `dna_array`, and `dna_json` columns from `dbo.product_forex`.
- **Exclusion of `trade_freq = 0` Models**: Models with `trade_freq = 0` are now explicitly excluded from the `#pf` temporary table, ensuring they are ignored by the trade generation process.
- **`max_open_trade_qty` Configuration**: Reads `max_open_trade_qty` from `dbo.config` (default 100,000).
- **`#open_qty` Temporary Table**: A new temporary table `#open_qty` is created to sum `trade_quantity` for all currently open trades (`tradeable = 1`), grouped by model. This is used for exposure checks.
- **Conditional Trade Candidate Generation**:
    - **Non-DNA Models (`trade_freq <> 99`)**: Continue to generate BUY and SELL candidates as before.
    - **DNA Models (`trade_freq = 99`)**:
        - **`side_pref = 'BUY'` or `side_pref = 'SELL'`**: A single trade candidate is generated for the specified `side_pref`.
        - **`side_pref = 'BOTH'`**: The trade side is determined by the `side` column in the `dbo.strategy_side_current` table. If `ssc.side` is NULL, no trade is generated.
        - **DNA Parameter Application**: `leg_qty`, `tp_pips`, `sl_pips` from DNA are used.
        - **Caps and Exposure Checks**: DNA candidates are filtered based on:
            - `ISNULL(oq.open_qty, 0) + dna.leg_qty <= @max_open_trade_qty` (total exposure limit).
            - `(SELECT COUNT(*) FROM dbo.combined_trades_open WHERE model = pf.model) < dna.max_legs` (per-model trade count limit, counting all open trades regardless of `tradeable` status).
- **`tradeable` Flag**: All trades (both non-DNA and DNA-driven) are inserted with `tradeable = 0`. The process for setting them to `1` (i.e., making them active) will be handled by a separate, subsequent step.
- **`trade_reason`**: Set to `'sp_001:dna-trade'` for DNA models and `'sp_001:d-trade_no_gates'` for non-DNA models.

---

## 17) **Strategy-Side Interface (`dbo.strategy_side_current`)** (Updated 2025-10-12 15:30 UTC)

A new table `dbo.strategy_side_current` has been introduced to facilitate communication between the strategy engine and the SQL trade creation procedures, especially for DNA models with `side_pref = 'BOTH'`.

### 17.1 `dbo.strategy_side_current` Details
- **Purpose**: Stores the current trade decision ('BUY', 'SELL', or NULL) made by the strategy engine for each `product`/`model` combination.
- **Schema**:
    ```sql
    CREATE TABLE dbo.strategy_side_current(
      product NVARCHAR(50) NOT NULL,
      model   SYSNAME      NOT NULL,
      side    VARCHAR(8)   NULL,      -- 'BUY' | 'SELL' | NULL (no entry)
      decided_at DATETIME2(3) NOT NULL CONSTRAINT DF_strategy_side_current_decided_at DEFAULT (SYSUTCDATETIME()),
      CONSTRAINT PK_strategy_side_current PRIMARY KEY (product, model)
    );
    ```
- **Usage**:
    - The **strategy engine** (application layer) is responsible for writing its trade decisions into this table based on DNA rules (e.g., `exec_mode`, `stagger`, cooldowns, etc.).
    - `sp_001_create_trades_v9_setbased` **reads** from this table to determine the trade signal when a DNA model has `side_pref = 'BOTH'`.

---

## 18) **Database Synchronization Mandate** (Updated 2025-10-12 15:30 UTC)

- **Mandate**: All modifications to database objects (tables, views, stored procedures, functions) in `tradedb` must also be applied to `tradedb_sim2` to maintain consistency between the production and simulation environments.

---

## 19) **Quick Checklist** (Updated 2025-10-12 15:30 UTC)
- [x] `ALTER TABLE dbo.product_forex ADD dna_array, dna_json`
- [x] `CREATE FUNCTION dbo.fn_split_csv_with_index`
- [x] `CREATE FUNCTION dbo.fn_decode_dna_json`
- [x] `CREATE FUNCTION dbo.fn_decode_dna_array`
- [x] `CREATE VIEW dbo.vw_product_forex_dna_expanded`
- [x] `CREATE PROCEDURE dbo.sp_helper_decode_dna`
- [x] `CREATE PROCEDURE dbo.sp_seed_product_forex_dna` (for scalable seeding)
- [x] `CREATE TABLE dbo.strategy_side_current`
- [x] Update `sp_001_create_trades_v9_setbased` to handle DNA models, `trade_freq` logic, `side_pref` (including 'BOTH'), and caps.
- [ ] Keep `sp_loop_create_trades_v2` **unchanged**
- [ ] Leaderboard continues to summarize realized P&L (start capital $10,000 each)
- [x] Ensure all `tradedb` object modifications are also applied to `tradedb_sim2`.