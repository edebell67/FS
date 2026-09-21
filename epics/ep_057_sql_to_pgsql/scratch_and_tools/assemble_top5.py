import json

orig_file = r"C:\Users\edebe\.gemini\antigravity\brain\6aed791c-b3c5-4ab4-a571-c23206db4462\associates_hourly_directional_split.html"
with open(orig_file, "r", encoding="utf-8") as f:
    html = f.read()

json_file = r"C:\Users\edebe\.gemini\antigravity\brain\6aed791c-b3c5-4ab4-a571-c23206db4462\scratch\exact_format_all_data.json"
with open(json_file, "r", encoding="utf-8") as f:
    new_data = f.read()

# Replace titles
html = html.replace("Associate Models Directional Split (Buy Net & Sell Net) - Sep 15-18", "Top 5 High Frequency Profitable Models (Directional Split)")
html = html.replace("Associate Models Matrix Split", "High-Volume Scalpers (Cum Net > 0)")
html = html.replace("Hourly #1 Associate Models: Buy Net vs Sell Net", "Top 5 High-Frequency Models: Buy Net vs Sell Net")
html = html.replace("Held #1 Associate during:", "Trade Volume & Win Rate:")
html = html.replace("Hourly #1 Associate Models for Selected Date", "Top 5 High-Frequency Models for Selected Window")
html = html.replace("Overall 4-Day Period", "Overall Week")

# Adjust dateLabels
old_labels = """    const dateLabels = [
      { id: '2026-09-15', label: 'Tue 15' },
      { id: '2026-09-16', label: 'Wed 16' },
      { id: '2026-09-17', label: 'Thu 17' },
      { id: '2026-09-18', label: 'Fri 18' }
    ];"""

new_labels = """    const dateLabels = [
      { id: 'WEEK_OVERALL', label: 'Overall Week' },
      { id: '2026-09-14', label: 'Mon 14' },
      { id: '2026-09-15', label: 'Tue 15' },
      { id: '2026-09-16', label: 'Wed 16' },
      { id: '2026-09-17', label: 'Thu 17' },
      { id: '2026-09-18', label: 'Fri 18' }
    ];"""
html = html.replace(old_labels, new_labels)

# Adjust initial date
html = html.replace("let currentDate = '2026-09-15';", "let currentDate = 'WEEK_OVERALL';")

# Adjust data injection
marker_start = "const allData = {"
marker_end = "let currentDate ="
start_idx = html.find(marker_start)
end_idx = html.find(marker_end)

if start_idx != -1 and end_idx != -1:
    html = html[:start_idx] + "const allData = " + new_data + ";\n\n    " + html[end_idx:]

out_file = r"C:\Users\edebe\.gemini\antigravity\brain\6aed791c-b3c5-4ab4-a571-c23206db4462\top5_high_freq_directional_split.html"
with open(out_file, "w", encoding="utf-8") as f:
    f.write(html)

print("Generated top5_high_freq_directional_split.html successfully!")
