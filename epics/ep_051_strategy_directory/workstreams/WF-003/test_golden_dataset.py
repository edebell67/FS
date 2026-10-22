import json
import sys

def verify_golden_dataset(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
        
    trades = data['trades']
    expected = data['expected_metrics']
    
    total_trades = len(trades)
    wins = len([t for t in trades if t['net_return'] > 0])
    losses = len([t for t in trades if t['net_return'] < 0])
    breakevens = len([t for t in trades if t['net_return'] == 0])
    
    win_rate = wins / total_trades if total_trades > 0 else 0
    total_net_return = sum(t['net_return'] for t in trades)
    
    gross_profit = sum(t['net_return'] for t in trades if t['net_return'] > 0)
    gross_loss = abs(sum(t['net_return'] for t in trades if t['net_return'] < 0))
    
    profit_factor = gross_profit / gross_loss if gross_loss != 0 else None
    
    average_trade = total_net_return / total_trades if total_trades > 0 else 0
    average_win = gross_profit / wins if wins > 0 else 0
    average_loss = sum(t['net_return'] for t in trades if t['net_return'] < 0) / losses if losses > 0 else 0
    
    payoff_ratio = average_win / abs(average_loss) if average_loss != 0 else None
    loss_rate = losses / total_trades if total_trades > 0 else 0
    expectancy = (win_rate * average_win) + (loss_rate * average_loss)

    assert total_trades == expected['total_trades']
    assert wins == expected['wins']
    assert losses == expected['losses']
    assert breakevens == expected['breakevens']
    assert abs(win_rate - expected['win_rate']) < 1e-6
    assert abs(total_net_return - expected['total_net_return']) < 1e-6
    assert abs(gross_profit - expected['gross_profit']) < 1e-6
    assert abs(gross_loss - expected['gross_loss']) < 1e-6
    assert abs(profit_factor - expected['profit_factor']) < 1e-6
    assert abs(average_trade - expected['average_trade']) < 1e-6
    assert abs(average_win - expected['average_win']) < 1e-6
    assert abs(average_loss - expected['average_loss']) < 1e-6
    assert abs(payoff_ratio - expected['payoff_ratio']) < 1e-6
    assert abs(expectancy - expected['expectancy']) < 1e-6
    
    print("All golden dataset metric tests passed.")

if __name__ == "__main__":
    verify_golden_dataset(sys.argv[1])
