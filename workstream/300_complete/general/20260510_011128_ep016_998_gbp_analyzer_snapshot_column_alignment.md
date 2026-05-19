## Task

- Modify `C:\Users\edebe\eds\epics\ep_016_turning_point_pattern_engine\logic\price_frequency_gbp_analyzer.py`
- Ensure each snapshot column is perfectly aligned with the displayed frequency-count cell data

## Task Type

- implementation

## Project

- ep016

## Destination Folder

- `workstream/100_backlog/general`

## Dependency

- Target analyzer: [price_frequency_gbp_analyzer.py](<C:/Users/edebe/eds/epics/ep_016_turning_point_pattern_engine/logic/price_frequency_gbp_analyzer.py>)
- Existing marker formats: `<>`, `><`, `<<>>`, `>><<`
- Existing ANSI color and pulsing behavior

## Plan

1. Review the current table-rendering logic and identify why snapshot headers and cell values drift out of alignment.
2. Define a single column-width rule that accounts for signed values, historical markers, ANSI color codes, and pulsing formatting.
3. Update the renderer so header cells and frequency cells use the same visible-width calculation.
4. Validate with mixed positive/negative counts and marked trade-history cells across multiple snapshot columns.

## Evidence

- Task opened to fix console-table alignment in the GBP frequency analyzer.
- User requirement is specifically that each snapshot column remains perfectly aligned with its frequency-count data.
- Updated [price_frequency_gbp_analyzer.py](<C:/Users/edebe/eds/epics/ep_016_turning_point_pattern_engine/logic/price_frequency_gbp_analyzer.py>) to use visible-width-aware cell formatting rather than a fixed `6`-character assumption.
- Added ANSI-stripping and visible-width helpers so color and pulse sequences do not distort column width calculations.
- Added a shared per-side `column_width` calculation that considers:
- snapshot header labels
- first-price values
- signed counts
- historical marker formats such as `<>`, `><`, `<<>>`, `>><<`
- Changed the table to render a proper `First Price` row using the same computed snapshot column widths as the frequency rows.
- Increased the left label column width so `First Price` aligns to the same separator position as the `Price` rows.

## Validation

- `python -m py_compile epics/ep_016_turning_point_pattern_engine/logic/price_frequency_gbp_analyzer.py`
- Synthetic render validation using mixed-width cells:
- `<<54>>`
- `<12>`
- `>-23<`
- `<-7>`
- Confirmed the snapshot headers, `First Price` row, and data rows all share the same column boundaries in the rendered output.

## Completion Status

- Complete
