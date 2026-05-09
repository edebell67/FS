import json
import os
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path
from json_layout import iter_day_dirs, load_layout_config

def get_tp_sl(name):
    tp_match = re.search(r'tp([\d\.]+)', name)
    sl_match = re.search(r'sl([\d\.]+)', name)
    if tp_match and sl_match:
        return float(tp_match.group(1)), float(sl_match.group(1))
    return None, None

def parse_time(ts):
    """Parse ISO timestamp and return timezone-aware datetime (UTC)"""
    try:
        dt = datetime.fromisoformat(ts.replace('Z', ''))
        # Make timezone-aware if naive
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except:
        return datetime.min.replace(tzinfo=timezone.utc)

CONFIG_PATH = Path(__file__).resolve().parent / 'config.json'
DEFAULT_JSON_ROOT = Path(r'C:\Users\edebe\eds\TradeApps\breakout\fs\json')

def _load_config():
    try:
        with CONFIG_PATH.open('r') as f:
            return json.load(f)
    except Exception:
        return {}

def _read_run_mode():
    return str(_load_config().get('run_mode', 'live')).lower()

def _calc_filtered_sum_net_bias_inputs(trades):
    """
    Compute BUY/SELL totals using only strategy-product groups where total net > 0.
    Group key: (app_name, product).
    """
    grouped = {}
    for t in trades or []:
        app = str(t.get('app_name') or t.get('script_name') or 'UNKNOWN')
        product = str(t.get('product') or 'UNKNOWN').upper()
        key = (app, product)
        row = grouped.setdefault(key, {'buy_net': 0.0, 'sell_net': 0.0, 'buy_count': 0, 'sell_count': 0})
        direction = str(t.get('direction') or 'LONG').lower()
        net = float(t.get('net_return', 0) or 0)
        if 'short' in direction:
            row['sell_net'] += net
            row['sell_count'] += 1
        else:
            row['buy_net'] += net
            row['buy_count'] += 1

    total_buy_net = 0.0
    total_sell_net = 0.0
    total_buy_count = 0
    total_sell_count = 0
    for row in grouped.values():
        total_net = float(row['buy_net']) + float(row['sell_net'])
        if total_net > 0:
            total_buy_net += float(row['buy_net'])
            total_sell_net += float(row['sell_net'])
            total_buy_count += int(row['buy_count'])
            total_sell_count += int(row['sell_count'])
    return total_buy_net, total_sell_net, total_buy_count, total_sell_count

def _write_no_data_targeted(day_folder: Path, date_str: str) -> None:
    """Initialize _targeted_strategies.json for a fresh/no-trade day."""
    payload = {
        "last_update": datetime.now(timezone.utc).isoformat(),
        "date": date_str,
        "status": "NO_DATA",
        "market_condition": "NO_DATA",
        "bias": None,
        "day_bias": None,
        "recent_bias": None,
        "ui_bias": None,
        "recent_buy_pnl": 0,
        "recent_sell_pnl": 0,
        "recent_buy_count": 0,
        "recent_sell_count": 0,
        "eligible_count": 0,
        "top_recommendation": None,
        "strategies": []
    }
    day_folder.mkdir(parents=True, exist_ok=True)
    with (day_folder / '_targeted_strategies.json').open('w') as f:
        json.dump(payload, f, indent=2)

def run_strategy_picker(date_str, base_path=None, start_time=None, end_time=None):
    run_mode = _read_run_mode()
    if base_path is None:
        base_root = DEFAULT_JSON_ROOT
        cfg = load_layout_config(CONFIG_PATH)
        day_folders = iter_day_dirs(base_root, run_mode, date_str, config=cfg)
        if not day_folders:
            day_folders = [base_root / run_mode / date_str]
    else:
        base_root = Path(base_path)
        day_folders = [base_root / date_str if date_str else base_root]
    day_folder = day_folders[0]
    summary_path = None
    top20_path = None
    for candidate_dir in day_folders:
        candidate_summary = candidate_dir / '_trades_summary.json'
        candidate_top20 = candidate_dir / '_top20.json'
        if candidate_summary.exists():
            day_folder = candidate_dir
            summary_path = candidate_summary
            top20_path = candidate_top20
            break
    if summary_path is None:
        summary_path = day_folder / '_trades_summary.json'
        top20_path = day_folder / '_top20.json'

    if not summary_path.exists():
        print(f"Summary file not found: {summary_path}")
        _write_no_data_targeted(day_folder, date_str)
        return

    with summary_path.open('r') as f:
        data = json.load(f)
    trades = data.get('trades', [])

    # [V20260210_0215] Load previous bias for flip detection
    previous_bias = None
    targeted_path = day_folder / '_targeted_strategies.json'
    if targeted_path.exists():
        try:
            with targeted_path.open('r') as f:
                prev_data = json.load(f)
                previous_bias = prev_data.get('bias')
        except: pass
    
    if start_time:
        start_dt = datetime.fromisoformat(f"{date_str}T{start_time}").replace(tzinfo=timezone.utc)
        trades = [t for t in trades if parse_time(t.get('entry_time', '')) >= start_dt]

    if end_time:
        end_dt = datetime.fromisoformat(f"{date_str}T{end_time}").replace(tzinfo=timezone.utc)
        trades = [t for t in trades if parse_time(t.get('entry_time', '')) <= end_dt]

    if not trades:
        print("No trades found.")
        _write_no_data_targeted(day_folder, date_str)
        return

    # 1. Determine Window & Bias
    scan_start_time = datetime.max.replace(tzinfo=timezone.utc)
    scan_latest_time = datetime.min.replace(tzinfo=timezone.utc)
    for t in trades:
        et = parse_time(t.get('entry_time'))
        if et == datetime.min.replace(tzinfo=timezone.utc): continue
        if et < scan_start_time: scan_start_time = et
        if et > scan_latest_time: scan_latest_time = et
    
    # [V20260206_2130] For current date scans, use system UTC time for 'now' to align with trade file timestamps
    today_str = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    if date_str == today_str and not end_time:
        scan_latest_time = datetime.now(timezone.utc)
    
    # --- A. Total Day Bias (Based on total net P&L for all trades) ---
    # [V20260209_1635] Changed to use total net P&L to match summary data display
    total_buy_trades = [
        t for t in trades
        if 'long' in (t.get('direction') or 'LONG').lower()
    ]
    total_sell_trades = [
        t for t in trades
        if 'short' in (t.get('direction') or 'SHORT').lower()
    ]
    
    total_buy_net = sum(t.get('net_return', 0) for t in total_buy_trades)
    total_sell_net = sum(t.get('net_return', 0) for t in total_sell_trades)
    
    total_buy_count = len(total_buy_trades)
    total_sell_count = len(total_sell_trades)
    
    # [V20260210_1320] AI Picker Bias now Average-Net based (Sync with UI screen)
    # Helper to safe-calculate average
    def get_avg_net(net_sum, count):
        return net_sum / max(1, count) if count > 0 else -999999
        
    day_avg_buy = get_avg_net(total_buy_net, total_buy_count)
    day_avg_sell = get_avg_net(total_sell_net, total_sell_count)
    
    # Load Config for jitter control
    config = _load_config()
    bias_calc_mode = str(config.get('bias_calc', 'filtered_sum_net')).lower()
    if bias_calc_mode == 'filtered_sum_net':
        f_buy_net, f_sell_net, f_buy_count, f_sell_count = _calc_filtered_sum_net_bias_inputs(trades)
        total_buy_net, total_sell_net = f_buy_net, f_sell_net
        total_buy_count, total_sell_count = f_buy_count, f_sell_count

    pnl_threshold = float(config.get('picker_pnl_spread_threshold', 2000)) # Margin for sum diff or average weighting
    
    # If we have a previous bias, only flip if the leader is compelling [V20260210_1320]
    if previous_bias:
        # Require margin: Spread between total P&L sums (using existing threshold logic)
        total_pnl_diff = abs(total_buy_net - total_sell_net)
        threshold_met = (total_pnl_diff >= pnl_threshold)
        
        if not threshold_met:
            # Not enough strength to flip, keep previous bias
            day_bias = previous_bias
            print(f"[DEBUG-BIAS] Jitter Detected. Total P&L Spread ${total_pnl_diff:,.2f} too small. Staying {day_bias}")
        else:
            # [V20260210_1705] Stability Fix: Use Total Net P&L for direction to match trigger
            day_bias = 'BUY' if total_buy_net >= total_sell_net else 'SELL'
            print(f"[DEBUG-BIAS] Flip Triggered! New Direction: {day_bias} (Total Net: Buy {total_buy_net:.0f} vs Sell {total_sell_net:.0f})")
    else:
        # Initial run - Use Total Net P&L
        day_bias = 'BUY' if total_buy_net >= total_sell_net else 'SELL'
    
    # --- B. Recent Momentum Bias (Last 60 mins) ---
    recent_window_start = scan_latest_time - timedelta(minutes=60)
    recent_trades_all = [t for t in trades if parse_time(t.get('entry_time', '')) >= recent_window_start]
    recent_buy_trades = [t for t in recent_trades_all if 'long' in (t.get('direction') or 'LONG').lower()]
    recent_sell_trades = [t for t in recent_trades_all if 'short' in (t.get('direction') or 'SHORT').lower()]
    
    recent_buy_count_all = len(recent_buy_trades)
    recent_sell_count_all = len(recent_sell_trades)

    recent_buy_pnl = sum(t.get('net_return', 0) for t in recent_buy_trades)
    recent_sell_pnl = sum(t.get('net_return', 0) for t in recent_sell_trades)
    
    # [V20260210_1320] Average Net Decision for Momentum (Matches Screen Highlighter bars)
    recent_avg_buy = get_avg_net(recent_buy_pnl, recent_buy_count_all)
    recent_avg_sell = get_avg_net(recent_sell_pnl, recent_sell_count_all)
    
    # Ensure NEUTRAL/None default if no data [V20260210_1450] - Sync with Day Bias if no momentum
    if recent_avg_buy == recent_avg_sell:
        ui_bias = day_bias 
    else:
        ui_bias = "BUY" if recent_avg_buy > recent_avg_sell else "SELL"
        
    pnl_bias = ui_bias 
    recent_bias = ui_bias

    # --- C. Final Decision Logic ---
    # Final bias is Day Bias (Average-Net based)
    bias = day_bias 
    
    print(f"[DEBUG-BIAS] Day Total Net ({bias_calc_mode}): BUY ${total_buy_net:,.2f}, SELL ${total_sell_net:,.2f} -> {day_bias}")
    print(f"[DEBUG-BIAS] Recent Avg Net: BUY ${recent_avg_buy:,.2f}, SELL ${recent_avg_sell:,.2f} -> {recent_bias}")
    
    bias = day_bias 
    
    # Determine status based on recent vs day alignment
    bias_status = "STABLE"
    if day_bias == recent_bias:
        bias_status = "STRONG"  # Recent momentum confirms day bias
    else:
        bias_status = "MIXED"
        
    # Load Config for dynamic thresholds [V20260208_1910]
    config = _load_config()
    pnl_threshold = float(config.get('picker_pnl_spread_threshold', 2000))
    count_threshold = float(config.get('picker_count_diff_threshold', 0.05))
    scalper_ratio = float(config.get('scalper_ratio', 5))

    pnl_spread = abs(recent_buy_pnl - recent_sell_pnl)
    total_recent = recent_buy_count_all + recent_sell_count_all
    count_diff_pct = abs(recent_buy_count_all - recent_sell_count_all) / max(1, total_recent)
    
    # [V20260206_2030] Detect Choppiness (Using configurable thresholds)
    is_choppy = (count_diff_pct <= count_threshold) or (pnl_spread < pnl_threshold)

    # Eligibility Side Net (Use Recent Bias for filtering)
    init_side_net = {}
    init_total_net = {} # [V20260208_1910] Dashboard equivalent
    for t in recent_trades_all:
        app = t.get('app_name')
        t_net = (t.get('net_return') or 0)
        init_total_net[app] = init_total_net.get(app, 0) + t_net
        
        is_correct_side = (bias == 'BUY' and 'long' in (t.get('direction') or '').lower()) or \
                          (bias == 'SELL' and 'short' in (t.get('direction') or '').lower())
        if is_correct_side:
            init_side_net[app] = init_side_net.get(app, 0) + t_net

    # Load Top 20
    top20_names = set()
    if top20_path.exists():
        with top20_path.open('r') as f:
            t20_data = json.load(f)
            for item in t20_data.get('top20', []):
                top20_names.add(item.get('strategy'))

    # 2. Filter Eligible Strategies (Strict Scalper Only)
    eligible_apps = []
    all_apps = set(t.get('app_name') for t in trades)
    for app in all_apps:
        tp, sl = get_tp_sl(app)
        if tp is None or sl is None or sl == 0: continue
        
        # [V20260208_1400] MANDATORY: Filter for Scalper trades only based on config ratio
        if sl < (tp * scalper_ratio): continue 
        
        in_top20 = app in top20_names
        pos_net = init_side_net.get(app, 0) > 0
        if in_top20 or pos_net:
            eligible_apps.append(app)

    # 3. Simulate Sequential Performance (Using bias side only)
    sim_start = recent_window_start if bias_status == "FLIPPED" else (scan_start_time + timedelta(minutes=30))
    trading_trades = [t for t in trades if parse_time(t.get('entry_time', '')) > sim_start]
    
    results = []
    for app in eligible_apps:
        tp, sl = get_tp_sl(app)
        # Scalper flag in output also follows the config ratio
        is_scalper = (tp > 0 and sl >= tp * scalper_ratio)
        
        selected = [t for t in trading_trades if t.get('app_name') == app]
        if bias == 'BUY':
            selected = [t for t in selected if 'long' in (t.get('direction') or 'LONG').lower()]
        else:
            selected = [t for t in selected if 'short' in (t.get('direction') or 'SHORT').lower()]
        
        selected.sort(key=lambda x: parse_time(x.get('entry_time')))
        executed = []
        last_exit = datetime.min.replace(tzinfo=timezone.utc)
        for t in selected:
            e_time = parse_time(t.get('entry_time'))
            x_time = parse_time(t.get('exit_time'))
            if e_time >= last_exit:
                executed.append(t)
                last_exit = x_time
        
        if executed:
            net = sum(t.get('net_return', 0) for t in executed)
            last_trade = executed[-1]

            # [V20260206_1930] If trade is OPEN, show the current scan time as "last_entry" to indicate it is active
            # This ensures "Last Entry" column for open trades shows the current state's time
            display_time = last_trade.get('entry_time', '').split('T')[-1].split('.')[0]
            if last_trade.get('status', 'CLOSED') == 'OPEN':
                display_time = scan_latest_time.strftime('%H:%M:%S')

            results.append({
                'strategy': app, 
                'product': last_trade.get('product', 'UNKNOWN'),
                'net': net, 
                'total_day_net': round(init_total_net.get(app, 0), 2), # [V20260208_1910] Match dashboard
                'trades': len(executed),
                'scalper': is_scalper,
                'last_entry': display_time,
                'last_status': last_trade.get('status', 'CLOSED')
            })

    results.sort(key=lambda x: x['net'], reverse=True)
    
    # --- D. Export to JSON for UI ---
    scan_time = scan_latest_time if scan_latest_time != datetime.min.replace(tzinfo=timezone.utc) else datetime.now(timezone.utc)
    picker_output = {
        "last_update": scan_time.isoformat(),
        "date": date_str,
        "bias_calc": bias_calc_mode,
        "total_buy_net": round(total_buy_net, 2),
        "total_sell_net": round(total_sell_net, 2),
        "status": bias_status,
        "market_condition": "CHOPPY" if is_choppy else "TRENDING",
        "bias": bias,
        "day_bias": day_bias,
        "recent_bias": recent_bias,
        "ui_bias": ui_bias,
        "recent_buy_pnl": round(recent_buy_pnl, 2),
        "recent_sell_pnl": round(recent_sell_pnl, 2),
        "recent_buy_count": recent_buy_count_all,
        "recent_sell_count": recent_sell_count_all,
        "eligible_count": len(eligible_apps),
        "top_recommendation": {**results[0], "bias": bias} if results else None, # [V20260208_1920] Smart Targeting
        "strategies": results[:20]
    }
    
    targeted_path = day_folder / '_targeted_strategies.json'
    
    # [V20260209_2218] ALWAYS update the file so the UI stats are live.
    # The frontend handles the 'Flip' logic by comparing the new bias to its previous state.
    try:
        day_folder.mkdir(parents=True, exist_ok=True)
        with targeted_path.open('w') as f:
            json.dump(picker_output, f, indent=2)
        
        if previous_bias and previous_bias != bias:
            print(f"\n[BIAS CHANGED] {previous_bias} -> {bias}. Updated _targeted_strategies.json")
        elif not previous_bias:
            print(f"\n[INITIAL RUN] Created _targeted_strategies.json with bias: {bias}")
        else:
            # bias is the same, but we updated stats
            pass 
    except Exception as e:
        print(f"Error saving targeted strategies: {e}")

    print(f"\n==========================================")
    print(f"REPORT FOR {date_str} (Now: {scan_latest_time.strftime('%H:%M:%S')})")
    print(f"Status: {bias_status} {'[CHOPPY MARKET]' if is_choppy else '[TRENDING]'}")
    print(f"Bias Direction: {bias} (UI/Count: {ui_bias} | P&L: {pnl_bias})")
    print(f" - Day Started: {day_bias} | Recent (1hr): {recent_bias}")
    print(f" - Recent P&L: BUY ${recent_buy_pnl:,.2f} vs SELL ${recent_sell_pnl:,.2f}")
    print(f" - Recent Count: BUY {recent_buy_count_all} vs SELL {recent_sell_count_all}")
    if is_choppy:
        print(f" !! PRIORITY: Scalping strategies (tp5/sl50, etc) recommended !!")
    print(f"Eligible strategies: {len(eligible_apps)}")
    print(f"Executed strategies: {len(results)}")
    print(f"===============================================================")
    head = f"{'Strategy Name':<45} | {'Trades':<8} | {'Net Return':<12} | {'Type'}"
    print(head)
    print("-" * len(head))
    for res in results[:20]:
        tag = "[SCALPER]" if res['scalper'] else ""
        line = f"{res['strategy']:<45} | {res['trades']:<8} | {res['net']:<12.2f} | {tag}"
        print(line)

if __name__ == "__main__":
    import sys
    import time
    
    # 1. Check if a specific date was passed
    target_date = sys.argv[1] if len(sys.argv) > 1 else datetime.now(timezone.utc).strftime('%Y-%m-%d')
    base_path = sys.argv[2] if (len(sys.argv) > 2 and sys.argv[2].lower() != 'none') else None
    start_t = sys.argv[3] if (len(sys.argv) > 3 and sys.argv[3].lower() != 'none') else None
    end_t = sys.argv[4] if (len(sys.argv) > 4 and sys.argv[4].lower() != 'none') else None
    
    # 2. Continuous Run Logic
    print(f"Starting Strategy Picker ({target_date})...")
    while True:
        run_strategy_picker(target_date, base_path=base_path, start_time=start_t, end_time=end_t)
        
        # If we passed a specific date, only run once
        if len(sys.argv) > 1:
            break
            
        print("\nWaiting 60 seconds for next refresh...")
        time.sleep(60)
        target_date = datetime.now(timezone.utc).strftime('%Y-%m-%d')
