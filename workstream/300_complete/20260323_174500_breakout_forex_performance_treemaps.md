# Task: Forex Strategy Performance Treemap Visualization

## Status: Completed (2026-03-23 17:45)

## 1. Summary
Create an interactive, high-impact visual representation of the current session's Forex strategy performance using treemaps to identify consensus winners and underperformers at a glance.

## 2. Objectives
- [x] **Data Aggregation:** Aggregate final net returns for all strategy/product pairs from `_summary_net.json`.
- [x] **Multi-Product Layout:** Generate separate treemaps for each active Forex product (CHF, CAD, EUR, etc.).
- [x] **Visual Encoding:** 
    - [x] **Size:** Map absolute magnitude of Net Return to block size.
    - [x] **Color:** Implement a Red-Yellow-Green (RdYlGn) colorscale representing P&L.
- [x] **Interactivity:** Ensure hover data shows full strategy name and precise Net Return.
- [x] **Standalone Delivery:** Output as a portable, dark-themed HTML file using Plotly.js.
- [x] **UI Integration:** Added "Treemaps" link to the global sidebar menu.

## 3. Implementation Details
- **Script:** Created a Python generator using `plotly.graph_objects`.
- **Styling:** Dark-themed background (`#111`) with card-like borders for each product section.
- **Color Logic:** Used `cmid=0` to ensure the neutral color (yellow) aligns exactly with the break-even point.
- **Scale:** Integrated a color bar for reference.
- **Menu:** Modified `TradeApps/breakout/fs/sidebar.html` to include the new page.

## 4. Files Created / Modified
- `TradeApps/breakout/fs/forex_performance_treemaps.html`: The final interactive dashboard.
- `TradeApps/breakout/fs/sidebar.html`: Integrated the new view into the application menu.

## 5. Usage
Open the following file in any modern web browser:
`C:\Users\edebe\eds\forex_performance_treemaps.html`

## 6. Evidence
- **Verification:** Successfully generated for 2026-03-24 data.
- **Accuracy:** Block sizes correctly reflect the scale of gains/losses (e.g., larger blocks for ±1000 than for ±10).
- **Consensus:** Visual confirms CHF and CAD as current product leaders.

Completion Status: 100%
