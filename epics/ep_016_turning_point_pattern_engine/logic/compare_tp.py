from strategy_tester import run_replay_test

symbol = "GBPAUD_C"

results_no_tp, _ = run_replay_test(symbol, take_profit=None)
results_tp7, _ = run_replay_test(symbol, take_profit=7)

print("GBPAUD_C: No TP vs TP=7")
print("=" * 60)
print(f"{'Threshold':<12} {'No TP':<10} {'TP=7':<10} {'Better':<10}")
print("-" * 60)

for t in range(20, 31):
    label = f">{t} FLIP"
    no_tp = results_no_tp.get(label, {}).get("total_pips", 0)
    tp7 = results_tp7.get(label, {}).get("total_pips", 0)
    better = "No TP" if no_tp > tp7 else ("TP=7" if tp7 > no_tp else "Same")
    print(f"{label:<12} {no_tp:<10} {tp7:<10} {better:<10}")
