import json

file_path = r"X:\EDS\TradeApps\breakout\fs\json\live\forex\2026-03-29\_summary_net.json"

with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

strategies = data.get("strategies", {})

sample_m = "breakout_R_Rev_2_tp3.0_sl20.0"
print(f"Details for top performer: {sample_m}")
for prod, pts in strategies[sample_m].items():
    if pts:
        print(f" Product: {prod}, Points count: {len(pts)}")
        for pt in pts:
            print(f"   t={pt.get('t')}, net={pt.get('net')}, buy_net={pt.get('buy_net')}, sell_net={pt.get('sell_net')}, live_buy={pt.get('live_buy')}, live_sell={pt.get('live_sell')}, open={pt.get('open')}, b_c={pt.get('b_c')}, s_c={pt.get('s_c')}")

