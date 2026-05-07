import pandas as pd

# Parameters
CSV_PATH = r"C:\Users\edebe\eds\epics\ep_013_simulation_test_trades\data\intraday_gbp_prices_2_days.csv"
WINDOW_SIZE = 5
PIP_VALUE = 0.0001
LOT_SIZE = 100000
COMMISSION_PIPS = 1.0
TP_PIPS = 30
SL_PIPS = 10
TP_VAL = TP_PIPS * PIP_VALUE
SL_VAL = SL_PIPS * PIP_VALUE

def run_simulation():
    df = pd.read_csv(CSV_PATH)
    df['price'] = pd.to_numeric(df['price'])
    
    distinct_prices = []
    trades = []
    alt_trades = []
    actual_trades = []
    
    # State tracking
    current_strategy = 'net' # 'net' or 'alt'
    consecutive_losses = 0
    
    cum_net = 0.0
    cum_alt_net = 0.0
    cum_actual_net = 0.0
    active_trade = None 
    
    print(f"{'Time':<20} | {'Type':<5} | {'Active':<4} | {'Net $':<8} | {'Alt $':<8} | {'Act $':<8} | {'Cum Net':<10} | {'Cum Alt':<10} | {'Cum Act':<10}")
    print("-" * 125)

    for i, row in df.iterrows():
        price = row['price']
        dt = row['datetime']
        
        if not distinct_prices or price != distinct_prices[-1]:
            distinct_prices.append(price)
            if len(distinct_prices) > WINDOW_SIZE + 1:
                distinct_prices.pop(0)
        
        if active_trade:
            entry = active_trade['entry']
            trade_type = active_trade['type']
            outcome = None # (net, alt)
            
            if trade_type == 'BUY':
                pips = (price - entry) / PIP_VALUE
                if pips >= TP_PIPS:
                    outcome = ((TP_PIPS - COMMISSION_PIPS) * 10, (-TP_PIPS - COMMISSION_PIPS) * 10)
                elif pips <= -SL_PIPS:
                    outcome = ((-SL_PIPS - COMMISSION_PIPS) * 10, (SL_PIPS - COMMISSION_PIPS) * 10)
            else: # SELL
                pips = (entry - price) / PIP_VALUE
                if pips >= TP_PIPS:
                    outcome = ((TP_PIPS - COMMISSION_PIPS) * 10, (-TP_PIPS - COMMISSION_PIPS) * 10)
                elif pips <= -SL_PIPS:
                    outcome = ((-SL_PIPS - COMMISSION_PIPS) * 10, (SL_PIPS - COMMISSION_PIPS) * 10)
            
            if outcome:
                net_usd, alt_usd = outcome
                
                # Allocate Actual based on state AT START of trade
                actual_usd = net_usd if current_strategy == 'net' else alt_usd
                
                cum_net += net_usd
                cum_alt_net += alt_usd
                cum_actual_net += actual_usd
                
                print(f"{dt:<20} | {trade_type:<5} | {current_strategy:<4} | ${net_usd:<8.2f} | ${alt_usd:<8.2f} | ${actual_usd:<8.2f} | ${cum_net:<10.2f} | ${cum_alt_net:<10.2f} | ${cum_actual_net:<10.2f}")
                
                trades.append(net_usd)
                alt_trades.append(alt_usd)
                actual_trades.append(actual_usd)
                
                # Update State for NEXT trade
                if actual_usd < 0:
                    consecutive_losses += 1
                else:
                    consecutive_losses = 0
                
                if consecutive_losses >= 3:
                    old_strategy = current_strategy
                    current_strategy = 'alt' if current_strategy == 'net' else 'net'
                    consecutive_losses = 0
                    # print(f"--- SWITCHED: {old_strategy.upper()} -> {current_strategy.upper()} after 3 losses ---")

                active_trade = None
            
            # For debugging/display, stop after 20 trades
            # if len(trades) >= 20:
            #    break
            continue

        if len(distinct_prices) > WINDOW_SIZE:
            window = distinct_prices[:-1]
            if price > max(window):
                active_trade = {'type': 'BUY', 'entry': price}
            elif price < min(window):
                active_trade = {'type': 'SELL', 'entry': price}

    if trades:
        print("-" * 125)
        print(f"Total Trades: {len(trades)}")
        print(f"Final Cum Net: ${cum_net:.2f}")
        print(f"Final Cum Alt: ${cum_alt_net:.2f}")
        print(f"Final Cum Act: ${cum_actual_net:.2f}")

if __name__ == "__main__":
    run_simulation()
