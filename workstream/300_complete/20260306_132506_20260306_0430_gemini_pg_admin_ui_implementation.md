# Task: PostgreSQL Admin UI Implementation (V20260306_0430)

## Objective
Provide a dedicated PostgreSQL-based management suite for trading operations, covering product setup, DNA generation, configuration, and multi-level performance summaries.

## Status: TODO
- [x] 1. Backend: Implement `admin_api_pg.py` with endpoints for Products, Config, and DNA triggers.
- [x] 2. UI: Create `product_manager.html` for `product_forex` updates.
- [x] 3. UI: Create `dna_generator.html` to trigger and monitor DNA data creation. (Renamed to dna_lab.html)
- [x] 4. UI: Create `config_editor.html` for direct `config` table management.
- [x] 5. UI: Create `summary_dashboard.html` with hierarchical grouping (Product > Model > Strategy > Signal).
- [x] 6. Logic: Implement Grouped Analytics SQL query for Net Return, Alt Net, and Trade Count.
- [x] 7. Deployment: Ensure accessibility from both `\fs` and `\db` app paths.

## Requirements Traceability
- **Groupings**: Product, Model, Strategy, Signal, Trade Status.
- **Metrics**: Net Return, Alt Net Return, Trade Count.
- **Data Source**: PostgreSQL `tradedb`.

## Timeline
- **Start**: 2026-03-06 04:30
- **Version**: V20260306_0430
- **Author**: Gemini CLI
