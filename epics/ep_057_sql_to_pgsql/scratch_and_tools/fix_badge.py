file_path = r"C:\Users\edebe\.gemini\antigravity\brain\6aed791c-b3c5-4ab4-a571-c23206db4462\top5_high_freq_directional_split.html"
with open(file_path, "r", encoding="utf-8") as f:
    text = f.read()

text = text.replace(
    'const hoursBadge = m.meta.hours_led.map(h => h.substring(0, 2) + "h").join(", ");',
    'const statsBadge = `${m.meta.closed_trades} trades (${m.meta.win_rate}% win)`;'
)
text = text.replace(
    'Led: <strong class="text-slate-200">${hoursBadge}</strong>',
    'Vol: <strong class="text-amber-300">${statsBadge}</strong>'
)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(text)

print("Replacement done!")
