# Script to update top10_5min_equity_curves.html to default to 2026-09-18
# Datetime stamp: 2026-09-20 21:36 - [V20260920_2136]

import os

html_path = r"C:\Users\edebe\eds\epics\ep_057_sql_to_pgsql\dashboards_and_uis\top10_5min_equity_curves.html"
brain_path = r"C:\Users\edebe\.gemini\antigravity\brain\6aed791c-b3c5-4ab4-a571-c23206db4462\top10_5min_equity_curves.html"
builder_path = r"C:\Users\edebe\eds\epics\ep_057_sql_to_pgsql\scratch_and_tools\build_scenario_modal_dashboard.py"

with open(html_path, "r", encoding="utf-8") as f:
    text = f.read()

old_v = "* v1.7.0 · 2026-09-20 · [V20260920_2020]"
new_v = "* v1.8.0 · 2026-09-20 · [V20260920_2136] Defaults to most recent trading date (2026-09-18 / Fri 18) upon startup while preserving full week and daily navigation, universal replay, scenario selection modal, baseline re-centering, and directional split controls.\n * v1.7.0 · 2026-09-20 · [V20260920_2020]"

if old_v in text:
    text = text.replace(old_v, new_v, 1)

old_date_decl = "    let currentDate = 'WEEK_OVERALL';"
new_date_decl = "    // Default to most recent trading date (datetime stamp: 2026-09-20 21:36 - [V20260920_2136])\n    let currentDate = '2026-09-18';"

if old_date_decl in text:
    text = text.replace(old_date_decl, new_date_decl, 1)
    print("Replaced currentDate in HTML text successfully.")
else:
    print("Warning: old_date_decl not found!")

with open(html_path, "w", encoding="utf-8") as f:
    f.write(text)

with open(brain_path, "w", encoding="utf-8") as f:
    f.write(text)

# Also update builder script so consistency is kept
with open(builder_path, "r", encoding="utf-8") as f:
    b_text = f.read()

old_b_vars = "    let currentCriteria = 'top_net'; // Active Scenario ID ('top_net', 'top_win', 'strongest_three', etc.)\n    let currentDate = 'WEEK_OVERALL';"
new_b_vars = "    let currentCriteria = 'top_net'; // Active Scenario ID ('top_net', 'top_win', 'strongest_three', etc.)\n    // Default to most recent trading date (datetime stamp: 2026-09-20 21:36 - [V20260920_2136])\n    let currentDate = '2026-09-18';"

if old_b_vars in b_text:
    b_text = b_text.replace(old_b_vars, new_b_vars)
    with open(builder_path, "w", encoding="utf-8") as f:
        f.write(b_text)
    print("Updated builder script successfully.")

print("All updates completed successfully.")
