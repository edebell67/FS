"""
Grid Live Trading Monitor
[V20260128_1630] - Strategy-level profitability guard for breakout trades
- Syncs strategy signals with IB/TWS via L-Trades
- Supports DNA (SQL) and Breakout (JSON) strategies
"""
import os
import sys
import json
import time
import pyodbc
import logging
import traceback
import subprocess
from pathlib import Path
from datetime import datetime
from json_layout import iter_day_dirs, load_layout_config, resolve_day_dir

# --- Configuration ---
POLL_INTERVAL = 5 # Seconds
BASE_DIR = Path(r"C:\Users\edebe\eds\TradeApps\breakout\fs")
CONFIG_FILE = BASE_DIR / "config.json"
GRID_LIVE_FILE = BASE_DIR / "grid_live.json"
SENT_TRADES_FILE = BASE_DIR / "grid_live_sent_trades.json"
JSON_TRADES_BASE = BASE_DIR / "json"
TWS_ORDER_DIR = Path(r"C:\Users\edebe\eds\trades_rt3\orders")
LOCK_FILE = BASE_DIR / "grid_live_monitor.lock"

# --- Logging ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] - %(message)s',
    handlers=[
        logging.FileHandler(BASE_DIR / "grid_live_monitor.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

def acquire_lock():
    if LOCK_FILE.exists():
        try:
            with open(LOCK_FILE, 'r') as f:
                old_pid = int(f.read().strip())
            # Check if old process is still running (Windows)
            result = subprocess.run(['tasklist', '/FI', f'PID eq {old_pid}', '/NH'], capture_output=True, text=True)
            if str(old_pid) in result.stdout:
                logging.warning(f"Process {old_pid} is still running. Exiting.")
                return False
            else:
                logging.info(f"Lock file belongs to dead process {old_pid}. Overwriting.")
        except Exception as e:
            logging.warning(f"Could not check lock file: {e}. Removing.")
            try: LOCK_FILE.unlink()
            except: pass
            
    try:
        with open(LOCK_FILE, 'w') as f:
            f.write(str(os.getpid()))
        logging.info(f"Acquired lock with PID {os.getpid()}")
        return True
    except Exception as e:
        logging.error(f"Failed to create lock file: {e}")
        return False

def connect_to_db(mode='live'):
    db_name = 'tradedb_sim2' if mode == 'sim' else 'tradedb'
    conn_str = (
        'DRIVER={SQL Server};'
        'SERVER=tcp:EDS,1433;'
        f'DATABASE={db_name};'
        'Trusted_Connection=yes;'
    )
    return pyodbc.connect(conn_str)

def load_json(path, default):
    if not path.exists():
        return default
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Failed to load {path.name}: {e}")
        return default

def save_json(path, data):
    try:
        with open(path, "w") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        logging.error(f"Failed to save {path.name}: {e}")

def get_breakout_pnl_stats(date_str, mode='live'):
    """
    [V20260128_1630] Load strategy-level P&L from _summary_net.json for profitability guard.
    """
    stats = {}
    for day_dir in iter_day_dirs(JSON_TRADES_BASE, mode, date_str, config=load_layout_config(CONFIG_FILE)):
        summary_file = day_dir / "_summary_net.json"
        if not summary_file.exists():
            continue
        try:
            with open(summary_file, 'r') as f:
                data = json.load(f)
            for strat, prods in data.get('strategies', {}).items():
                for prod, points in prods.items():
                    if points:
                        last = points[-1]
                        stats[(strat, prod.upper())] = {
                            'net': float(last.get('net', 0)),
                            'alt': float(last.get('alt_net', last.get('alt', 0))),
                            'buy_net': float(last.get('buy_net', 0)),
                            'sell_net': float(last.get('sell_net', 0))
                        }
        except Exception as e:
            logging.error(f"Failed to parse _summary_net.json for P&L stats: {e}")
    
    return stats

def is_dna_model(model_name):
    """[V20260128_0145] Check if model is DNA (SQL) or breakout (JSON)"""
    return model_name.lower().startswith('dna_')

def get_json_open_trades(model, product, date_str, mode='live'):
    """
    [V20260128_1530] Scan JSON files for open trades matching model/product.
    """
    trades = []
    candidates = {}
    for date_folder in iter_day_dirs(JSON_TRADES_BASE, mode, date_str, config=load_layout_config(CONFIG_FILE)):
        patterns = (
            f"{model}_{product}_*_op.json",
            f"{model}*_{product}_*_op.json",
        )
        for pattern in patterns:
            for p in date_folder.glob(pattern):
                candidates[str(p)] = p

    for op_file in candidates.values():
        op_name = op_file.name
        try:
            with open(op_file, 'r') as f:
                trade_data = json.load(f)

            # Use filename stem as ID if missing in content
            trade_id = str(trade_data.get('trade_id') or op_file.stem)

            trades.append({
                'trade_id': trade_id,
                'direction': trade_data.get('direction'),
                'entry_price': float(trade_data.get('entry_price', 0)),
                'cumulative_pnl': float(trade_data.get('cumulative_pnl', 0)),
                'cumulative_alt_pnl': float(trade_data.get('cumulative_alt_pnl', 0)),
                'is_live_trade': trade_data.get('is_live_trade') == True or trade_data.get('order_sent_net') == True or trade_data.get('order_sent_alt') == True,
                'sent_at': trade_data.get('sent_at'),
                'filename': op_name,
                'file_path': str(op_file)
            })
        except Exception as e:
            logging.error(f"Error loading {op_name}: {e}")
            
    return trades

def check_json_trade_closed(model, product, trade_id, orig_filename, date_str, mode='live'):
    """
    [V20260128_1530] Check if a breakout trade has closed by looking for _cl.json or _cld.json.
    """
    # Derive the base stem (without _op and extension)
    stem = Path(orig_filename or trade_id).stem.replace('_op', '')
    
    for date_folder in iter_day_dirs(JSON_TRADES_BASE, mode, date_str, config=load_layout_config(CONFIG_FILE)):
        for suffix in ('_cl.json', '_cld.json'):
            candidate = stem + suffix
            for cl_file in date_folder.glob(f"*{candidate}"):
                try:
                    with open(cl_file, 'r') as f:
                        data = json.load(f)
                    return True, float(data.get('exit_price', 0.0))
                except:
                    pass
        if orig_filename:
            op_path = date_folder / orig_filename
            if not op_path.exists():
                logging.info(f"Trade marked CLOSED because {orig_filename} is missing.")
                return True, 0.0
            
    return False, 0.0

def count_current_live_trades(date_str, mode='live'):
    """
    [V20260211_1610] Count all currently open trades marked as live.
    Strict check: only counts trades with is_live_trade=True to prevent zombie blocks.
    """
    count = 0
    for date_folder in iter_day_dirs(JSON_TRADES_BASE, mode, date_str, config=load_layout_config(CONFIG_FILE)):
        for op_file in date_folder.glob("*_op.json"):
            try:
                with open(op_file, 'r') as f:
                    data = json.load(f)
                if data.get('is_live_trade') == True:
                    count += 1
            except:
                pass
    return count


def mark_json_trade_as_live(file_path, entry_time, entry_price):
    """Update JSON file to mark it as live_trade_executed and is_live_trade."""
    try:
        path = Path(file_path)
        if not path.exists():
            return False
            
        with open(path, 'r') as f:
            data = json.load(f)
            
        data['live_trade_executed'] = True
        data['is_live_trade'] = True
        data['order_sent_net'] = True # [V20260211_1615] Keep flags consistent

        data['in_trade_entry_time'] = entry_time
        data['in_trade_entry_price'] = entry_price
        
        # Atomic write
        temp_path = path.with_suffix('.tmp')
        with open(temp_path, 'w') as f:
            json.dump(data, f, indent=4)
        
        os.replace(temp_path, path)
        logging.info(f"Marked trade as live: {path.name} (Price: {entry_price})")
        return True
    except Exception as e:
        logging.error(f"Failed to mark trade as live {file_path}: {e}")
        return False

def create_l_trade_json(product, direction, model_id, trade_guid, metric_mode, is_close, price, is_dna=True):
    """
    [V20260128_1630] Create an L-Trade order file for TWS injection.
    Excludes '_dna_' prefix for breakout trades.
    """
    timestamp_str = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Logic from common.py _create_l_trade_order
    strategy_action = 'BUY' if (direction or '').upper() in ('LONG', 'BUY') else 'SELL'
    
    source_prefix = "dna" if is_dna else "breakout"
    
    if metric_mode == 'alt':
        base_action = 'SELL' if strategy_action == 'BUY' else 'BUY'
    else:
        base_action = strategy_action
        
    if is_close:
        action = 'SELL' if base_action == 'BUY' else 'BUY'
        phase = 'CLOSE'
    else:
        action = base_action
        phase = 'OPEN'
        
    suffix = "close_tradeable.json" if is_close else "open_tradeable.json"
    # [V20260129_0435] GUID integration: include GUID before product name
    filename = f"grid_live_{trade_guid}_{product}_{source_prefix}_{model_id}_{action}_{timestamp_str}_{suffix}"
    
    # [V20260126_1000] Dynamic qty from config
    config = load_json(CONFIG_FILE, {})
    qty_percent = float(config.get('trade_qty_percent', 45.0))
    qty = int(100000 * (qty_percent / 100.0))
    
    tradeable_data = {
        'symbol': product,
        'secType': 'CASH',
        'exchange': 'IDEALPRO',
        'currency': 'USD',
        'action': action,
        'orderType': 'MKT',
        'quantity': qty,
        'guidePrice': price,
        'comment': f"GRID-LIVE {source_prefix}_{model_id} {metric_mode.upper()} {phase} #{trade_guid}",
        'source': 'grid_live',
        'guid': trade_guid
    }
    
    os.makedirs(TWS_ORDER_DIR, exist_ok=True)
    filepath = TWS_ORDER_DIR / filename
    
    try:
        with open(filepath, "w") as f:
            json.dump(tradeable_data, f, indent=2)
        logging.info(f"Successfully created L-Trade order: {filename}")
        return True
    except Exception as e:
        logging.error(f"Failed to create order file {filename}: {e}")
        return False

def monitor_loop():
    sent_trades = load_json(SENT_TRADES_FILE, {}) # { guid: {status: 'OPEN_SENT', ... } }
    cycle_count = 0

    while True:
        cycle_count += 1
        try:
            # [V20260129_1055] Simplified grid live logic (datetime: 2026-01-29 10:45)
            # [V20260131_0300] Support 'sim' section by extracting 'live' key if dict
            raw_param = load_json(GRID_LIVE_FILE, [])
            if isinstance(raw_param, dict):
                live_config = raw_param.get('live', [])
            else:
                live_config = raw_param # Legacy list
            
            if not live_config:
                if cycle_count % 12 == 1:
                    logging.info(f"[CYCLE {cycle_count}] No active live models in grid_live.json - waiting...")
                time.sleep(POLL_INTERVAL)
                continue

            # Flatten live models
            dna_models = {}      # (model, product) -> metric
            breakout_models = {} # (model, product) -> metric

            for m in live_config:
                if not isinstance(m, dict): continue
                model_name = str(m.get('model'))
                product = str(m.get('product', '')).upper()
                metric = m.get('metric', 'net')
                if not model_name or not product: continue
                
                if is_dna_model(model_name):
                    dna_models[(model_name, product)] = metric
                else:
                    breakout_models[(model_name, product)] = metric

            today_str = datetime.now().strftime('%Y-%m-%d')
            dirty = False
            matched_count = 0
            total_models = len(dna_models) + len(breakout_models)

            # [V20260211_1525] Load max_live_trades limit from config
            config = load_json(CONFIG_FILE, {})
            max_live = int(config.get('max_live_trades', 1))
            current_live_count = count_current_live_trades(today_str)
            
            if cycle_count % 12 == 1:
                logging.info(f"[MAX_LIVE_CHECK] Current Live Trades: {current_live_count}, Max Allowed: {max_live}")

            # [V20260211_1525] RE-ENABLED TRADING LOGIC with max_live_trades guard
            # --- DNA ---
            if dna_models:
                try:
                    conn = connect_to_db()
                    cursor = conn.cursor()
                    cursor.execute("SELECT model, product, signal, guid, entry_price FROM dbo.combined_trades_open WITH (NOLOCK)")
                    sql_open = cursor.fetchall()
                    
                    cursor.execute("SELECT product, model, net_return_sum, alt_net_return_sum FROM dbo.dna_pnl_stream_cache WITH (NOLOCK)")
                    pnl_stats = {}
                    for row in cursor.fetchall():
                        pnl_stats[(str(row[1]), str(row[0]).upper())] = {'net': float(row[2] or 0), 'alt': float(row[3] or 0)}

                    for row in sql_open:
                        m_str, p_str, sig, guid, ep = str(row[0]), str(row[1]).upper(), row[2], str(row[3]), float(row[4] or 0)
                        if (m_str, p_str) in dna_models:
                            matched_count += 1
                            metric = dna_models[(m_str, p_str)]
                            if guid not in sent_trades:
                                # [V20260211_1525] Check max_live_trades limit
                                if current_live_count >= max_live:
                                    logging.warning(f"[MAX_LIVE_LIMIT] Skipping DNA trade {guid}. Current: {current_live_count}, Max: {max_live}")
                                    continue
                                    
                                stats = pnl_stats.get((m_str, p_str), {'net': 0, 'alt': 0})
                                pnl = stats['alt'] if metric == 'alt' else stats['net']
                                if pnl > 0:
                                    if create_l_trade_json(p_str, sig, m_str, guid, metric, False, ep, is_dna=True):
                                        sent_trades[guid] = {'status': 'OPEN_SENT', 'model': m_str, 'product': p_str, 'metric': metric, 'source': 'dna', 'sent_at': datetime.now().isoformat()}
                                        dirty = True
                                        current_live_count += 1  # Increment counter
                    
                    # DNA Closes
                    cursor.execute("SELECT guid, latest_price FROM dbo.combined_trades_closed WITH (NOLOCK)")
                    sql_closed = {str(r[0]): float(r[1] or 0) for r in cursor.fetchall()}
                    for guid, d in list(sent_trades.items()):
                        if d['status'] == 'OPEN_SENT' and d.get('source') == 'dna' and guid in sql_closed:
                            if create_l_trade_json(d['product'], None, d['model'], guid, d['metric'], True, sql_closed[guid], is_dna=True):
                                sent_trades[guid]['status'] = 'CLOSED_SENT'
                                sent_trades[guid]['closed_at'] = datetime.utcnow().isoformat()
                                dirty = True
                    conn.close()
                except Exception as e:
                    logging.error(f"DNA processing error: {e}")

            # --- Breakout ---
            if breakout_models:
                breakout_stats = get_breakout_pnl_stats(today_str)
                for (m_name, p_name), metric in breakout_models.items():
                    # [V20260128_1630] Profitability guard based on TOTAL strategy performance
                    stats = breakout_stats.get((m_name, p_name), {'net': 0, 'alt': 0, 'buy_net': 0, 'sell_net': 0})
                    strat_pnl = stats.get(metric, 0)
                    if metric == 'alt': strat_pnl = stats.get('alt', 0)

                    for t in get_json_open_trades(m_name, p_name, today_str):
                        # Derive a stable key for monitor memory from trade payload/file.
                        guid = str(
                            t.get('guid')
                            or t.get('trade_id')
                            or Path(t.get('filename', '')).stem
                            or f"{m_name}|{p_name}|unknown"
                        )
                        # [V20260211_1655] Respect P&L Guard: Don't promote if strategy is currently losing
                        if strat_pnl <= 0:
                            # logging.debug(f"[GUARD] Skipping {guid}: Strategy P&L {strat_pnl} is not positive.")
                            continue

                        # [V20260129_0325] SECONDARY SAFETY CHECK: Check disk for promotion flag
                        if t.get('is_live_trade'):

                            if guid not in sent_trades:
                                logging.info(f"[SYNC] Trade {guid} already live on disk. Updating monitor memory.")
                                sent_trades[guid] = {
                                    'status': 'OPEN_SENT', 'model': m_name, 'product': p_name, 'metric': metric, 
                                    'source': 'breakout', 'trade_id': t['trade_id'], 'filename': t['filename'], 
                                    'sent_at': t.get('sent_at') or datetime.utcnow().isoformat()
                                }
                                dirty = True
                            continue

                        # Strategies now control live activation for breakout trades.
                        continue
                
                # Breakout Closes
                for guid, d in list(sent_trades.items()):
                    if d['status'] == 'OPEN_SENT' and d.get('source') == 'breakout':
                        is_cl, exit_p = check_json_trade_closed(d['model'], d['product'], d.get('trade_id',''), d.get('filename',''), today_str)
                        if is_cl:
                            if create_l_trade_json(d['product'], None, d['model'], guid, d['metric'], True, exit_p, is_dna=False):
                                sent_trades[guid]['status'] = 'CLOSED_SENT'
                                sent_trades[guid]['closed_at'] = datetime.utcnow().isoformat()
                                dirty = True
            
            # [V20260210_1355] GROUP EXCLUSIVITY LOGIC (First-to-Match)
            # If any strategy in a 'group' has an open LIVE trade, deactivate the other siblings.
            groups_active_with_live = set()
            for m in live_config:
                if not isinstance(m, dict): continue
                model_name = m.get('model')
                product = m.get('product', '').upper()
                group_id = m.get('group')
                
                if not group_id or group_id == product: continue # Ignore default/empty groups
                
                # Check for open live trades for this specific model/product
                open_trades = get_json_open_trades(model_name, product, today_str)
                
                # If any open trade is marked as LIVE, this group is 'Triggered'
                if any(t.get('is_live_trade') for t in open_trades):
                    logging.info(f"[GROUP-AUTO-ARCHIVE] Group '{group_id}' has active live trade via {model_name} on {product}. Archiving siblings.")
                    groups_active_with_live.add(group_id)

            if groups_active_with_live:
                # Filter grid_live to remove non-live members of triggered groups
                new_live_config = []
                grid_changed = False
                for m in live_config:
                    group_id = m.get('group')
                    if group_id in groups_active_with_live:
                        # Only keep if it's the one that currently has the live trade
                        model_name = m.get('model')
                        product = m.get('product', '').upper()
                        open_trades = get_json_open_trades(model_name, product, today_str)
                        if any(t.get('is_live_trade') for t in open_trades):
                            new_live_config.append(m)
                        else:
                            logging.info(f"[GROUP-AUTO-ARCHIVE] Removing sibling strategy: {model_name} on {product} (Group: {group_id})")
                            grid_changed = True
                    else:
                        new_live_config.append(m)
                
                if grid_changed:
                    raw_param['live'] = new_live_config
                    save_json(GRID_LIVE_FILE, raw_param)
                    logging.info(f"[GROUP-AUTO-ARCHIVE] Saved updated grid_live.json with archived siblings.")

            if dirty: save_json(SENT_TRADES_FILE, sent_trades)
            
            if cycle_count % 12 == 1:
                logging.info(f"[CYCLE {cycle_count}] Mon:{total_models} Match:{matched_count} Pending:{len([g for g,d in sent_trades.items() if d['status']=='OPEN_SENT'])}")

        except Exception as e:
            logging.error(f"Error: {e}\n{traceback.format_exc()}")
        time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    if not acquire_lock():
        sys.exit(1)
    logging.info("Starting Grid Live Monitor Service...")
    monitor_loop()
