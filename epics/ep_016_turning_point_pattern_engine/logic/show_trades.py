from strategy_tester import run_replay_test

symbol = "GBPAUD_C"
results, info = run_replay_test(symbol, thresholds=[28], include_flip=True, take_profit=None)

print(f"Snapshots: {info['snapshots']}")
print()

for label, data in results.items():
    print(f"{label}: {data['total_trades']} trades, {data['wins']}W/{data['losses']}L, {data['win_rate']}%, {data['total_pips']} pips")
    for t in data.get("trades", []):
        print(f"  {t['side']} {t['entry']:.5f} -> {t['exit']:.5f} = {t['net_pips']} pips ({t.get('exit_reason', 'SIGNAL')})")
    print()
