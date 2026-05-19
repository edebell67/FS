# Task: Generate RT TWS Sample Orders For Tracked Non-Crypto Products

## Source
- User Directive: 2026-04-08
- Template Input: `C:\Users\edebe\eds\TradeApps\breakout\fs\tws_order_templates.json`
- Product Config Input: `C:\Users\edebe\eds\TradeApps\breakout\fs\config.json`

## Task Type
standard

## Task Attributes
recurring_task: false
looping_task: false
splittable_task: false
workflow_task: false

## Task Summary
Use `tws_order_templates.json` to generate one sample minimum TWS order for each tracked product declared in `config.json` under `product_type_by_product`, excluding all crypto products. Persist the generated samples to `tws_order_template_RT.json` and capture the resulting product coverage, alias handling, and output details in this lifecycle record.

## Context
- Source template file: `C:\Users\edebe\eds\TradeApps\breakout\fs\tws_order_templates.json`
- Product tracking config: `C:\Users\edebe\eds\TradeApps\breakout\fs\config.json`
- Output file to create: `C:\Users\edebe\eds\TradeApps\breakout\fs\tws_order_template_RT.json`
- Tracked non-crypto products from `product_type_by_product`:
  - `BZ` energy
  - `CL` energy
  - `ES` indices
  - `GC` metals
  - `GOLD` metals
  - `HG` metals
  - `MCL` energy
  - `MES` indices
  - `MNQ` indices
  - `NG` energy
  - `NQ` indices
  - `RTY` indices
  - `SI` metals
  - `SIL` metals
  - `YM` indices
  - `ZB` rates
  - `ZF` rates
  - `ZN` rates
  - `ZT` rates
- Alias handling required:
  - `GOLD` is tracked in config but is not present as a product key in `tws_order_templates.json`.
  - For this sample generation task, `GOLD` is mapped to the metals template for `GC` and recorded as an alias.

## Destination Folder
C:\Users\edebe\eds\TradeApps\breakout\fs\

## Dependency
Dependency: None

## Plan
- [x] 1. Inspect the source template and tracked product mapping to determine the non-crypto product set and any template gaps.
  - [x] Test: `Get-Content -Path C:\Users\edebe\eds\TradeApps\breakout\fs\tws_order_templates.json -TotalCount 400` and `Get-Content -Path C:\Users\edebe\eds\TradeApps\breakout\fs\config.json -TotalCount 400`
  - Evidence: Confirmed 19 tracked non-crypto products and identified `GOLD` as an alias case not directly present in the source template.
- [x] 2. Generate one sample minimum order per tracked non-crypto product from the source template rules and document any assumptions.
  - [x] Test: PowerShell derivation over `product_type_by_product` excluding `crypto` produces a complete sample-order set with no unmapped non-crypto products.
  - Evidence: Derived 19 sample orders; all direct template matches resolved and `GOLD` was mapped to template product `GC`.
- [x] 3. Persist the generated output to `tws_order_template_RT.json`.
  - [x] Test: Output file exists at `C:\Users\edebe\eds\TradeApps\breakout\fs\tws_order_template_RT.json` and parses as valid JSON.
  - Evidence: File created with `_meta` plus `orders` payload covering all tracked non-crypto products.
- [x] 4. Record product coverage, output location, and validation evidence in this lifecycle file.
  - [x] Test: Lifecycle file includes the tracked product list, alias note, output path, and validation summary.
  - Evidence: This task file now contains source, coverage, assumptions, output path, and validation details.

## Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true
- Evidence-Type: file_output
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\tws_order_template_RT.json`
  - Objective-Proved: Generated RT sample-order file exists in the requested destination folder.
  - Status: captured
- Evidence-Type: diff
  - Artifact: Added `C:\Users\edebe\eds\TradeApps\breakout\fs\tws_order_template_RT.json` and this lifecycle task file.
  - Objective-Proved: Repository changes are limited to the requested RT output and its lifecycle record.
  - Status: captured
- Evidence-Type: test_output
  - Artifact: PowerShell validation confirmed JSON parsing and 19 generated non-crypto orders.
  - Objective-Proved: The generated output is structurally valid and covers the tracked non-crypto product set.
  - Status: captured

## Implementation Log
- 2026-04-08 13:09:05: Created lifecycle task for RT TWS sample-order generation from source template and config mapping.
- 2026-04-08 13:12:00: Read `tws_order_templates.json` and `config.json`; identified 19 tracked non-crypto products in `product_type_by_product`.
- 2026-04-08 13:14:00: Confirmed `GOLD` is tracked in config but absent from the template products list; documented it as an alias to `GC` for this sample output.
- 2026-04-08 13:18:00: Generated sample minimum orders using product-type templates, excluding crypto entries.
- 2026-04-08 13:22:00: Wrote `tws_order_template_RT.json` with generation metadata and product order samples.
- 2026-04-08 13:24:00: Validated JSON output and recorded lifecycle evidence.
- 2026-04-08 13:26:00: Parsed the generated JSON and confirmed `orders=19`; then moved the lifecycle file through `200_inprogress` to `300_complete`.

## Changes Made
- Added `C:\Users\edebe\eds\TradeApps\breakout\fs\tws_order_template_RT.json`.
- Added this lifecycle record.
- Generated one minimum sample TWS market order for each tracked non-crypto product in `product_type_by_product`.
- Applied alias mapping `GOLD -> GC` because the tracked config key does not exist directly in the source template product catalog.
- Used `lastTradeDateOrContractMonth: "202606"` for futures sample orders as a forward sample contract month placeholder.

## Generated Coverage
| Product | Product Type | Template Product | Exchange | secType | Min Quantity | Notes |
|---|---|---|---|---|---:|---|
| BZ | energy | BZ | IPE | FUT | 1 | direct template match |
| CL | energy | CL | NYMEX | FUT | 1 | direct template match |
| ES | indices | ES | CME | FUT | 1 | direct template match |
| GC | metals | GC | COMEX | FUT | 1 | direct template match |
| GOLD | metals | GC | COMEX | FUT | 1 | alias of `GC` |
| HG | metals | HG | COMEX | FUT | 1 | direct template match |
| MCL | energy | MCL | NYMEX | FUT | 1 | direct template match |
| MES | indices | MES | CME | FUT | 1 | direct template match |
| MNQ | indices | MNQ | CME | FUT | 1 | direct template match |
| NG | energy | NG | NYMEX | FUT | 1 | direct template match |
| NQ | indices | NQ | CME | FUT | 1 | direct template match |
| RTY | indices | RTY | CME | FUT | 1 | direct template match |
| SI | metals | SI | COMEX | FUT | 1 | direct template match |
| SIL | metals | SIL | COMEX | FUT | 1 | direct template match |
| YM | indices | YM | CBOT | FUT | 1 | direct template match |
| ZB | rates | ZB | CBOT | FUT | 1 | direct template match |
| ZF | rates | ZF | CBOT | FUT | 1 | direct template match |
| ZN | rates | ZN | CBOT | FUT | 1 | direct template match |
| ZT | rates | ZT | CBOT | FUT | 1 | direct template match |

## Validation
- Ran direct file inspection on source template and config inputs to verify source data.
- Ran PowerShell derivation over `product_type_by_product` excluding `crypto` to build the product list and sample output.
- Validated that the generated non-crypto order set contains 19 products.
- Validated that `C:\Users\edebe\eds\TradeApps\breakout\fs\tws_order_template_RT.json` exists and parses as JSON.
- Validation output: `orders=19`

## Risks/Notes
- The source template is marked draft and requires validation; the generated RT file is a sample-order artifact, not a confirmed production-ready routing specification.
- `GOLD` required alias handling because the tracked config key differs from the metals template key.
- `lastTradeDateOrContractMonth: "202606"` is a placeholder forward contract month for samples and may need refreshing for live use.
- Forex products are not represented in `product_type_by_product`, so no forex RT samples were generated for this task.

## Completion Status
- State: COMPLETE
- Timestamp: 2026-04-08 13:24:00
