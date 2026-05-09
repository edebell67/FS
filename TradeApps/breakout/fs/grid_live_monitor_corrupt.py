
import os
import sys
import json
import time
import pyodbc
import logging
import traceback
from datetime import datetime
from pathlib import Path
from json_layout import iter_day_dirs, load_layout_config

# [V20260126_0900] Grid Live Trading Monitor
# [V20260128_0145] Added support for JSON-based breakout strategies
# [V20260128_1442] Added singleton lock to prevent duplicate instances
# [V20260128_1530] Resolved excessive trade generation (noise) for breakout trades
# Watches SQL Server for DNA models AND JSON files for breakout strategies
# and generates L-Trade JSON orders for TWS.

# --- Configuration ---
POLL_INTERVAL = 5 # Seconds
GRID_LIVE_FILE = Path(r"C:\Users\edebe\eds\TradeApps\breakout\fs\grid_live.json")
SENT_TRADES_FILE = Path(r"C:\Users\edebe\eds\TradeApps\breakout\fs\grid_live_sent_trades.json")
CONFIG_FILE = Path(r"C:\Users\edebe\eds\TradeApps\breakout\fs\config.json")
LOCK_FILE = Path(r"C:\Users\edebe\eds\TradeApps\breakout\fs\grid_live_monitor.lock")

# [V20260128_0145] JSON trades base path for breakout strategies
JSON_TRADES_BASE = Path(r"C:\Users\edebe\eds\TradeApps\breakout\fs\json\live")
JSON_ROOT = JSON_TRADES_BASE.parent

# SQL Server credentials (from api_server_sql/main.py)
SERVER = "tcp:EDS,1433"
DATABASE = "tradedb"
USERNAME = "sqlaccessfromapi"
PASSWORD = "apiaccess@4321"

# TWS Order Directory (from common.py)
TWS_ORDER_DIR = r"C:\Users\edebe\eds\trades_rt3\orders"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [GRID-MONITOR] - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(r"C:\Users\edebe\eds\TradeApps\breakout\fs\grid_live_monitor.log"),
        logging.StreamHandler()
    ]
)

# [V20260128_1442] Singleton lock mechanism
def acquire_lock():
    """Attempt to acquire exclusive lock. Returns True if successful."""
    if LOCK_FILE.exists():
        try:
            with open(LOCK_FILE, 'r') as f:
                old_pid = int(f.read().strip())
            # Check if old process is still running (Windows)
            import subprocess
            # Use tasklist.exe to avoid shell escaping issues
            result = subprocess.run(['tasklist.exe', '/FI', f'PID eq {old_pid}'], capture_output=True, text=True)
            if str(old_pid) in result.stdout:
                logging.error(f"Another instance is already running (PID {old_pid}). Exiting.")
                return False
            else:
                logging.warning(f"Stale lock file found (PID {old_pid} not running). Removing.")
                LOCK_FILE.unlink()
        except Exception as e:
            logging.warning(f"Could not check lock file: {e}. Removing and proceeding.")
            try: LOCK_FILE.unlink()
            except: pass
    
    # Write our PID
    try:
        with open(LOCK_FILE, 'w') as f:
            f.write(str(os.getpid()))
        logging.info(f"Acquired lock with PID {os.getpid()}")
        return True
    except Exception as e:
        logging.error(f"Failed to create lock file: {e}")
        return False

def release_lock():
    """Release the lock file on exit."""
    if LOCK_FILE.exists():
        try:
            with open(LOCK_FILE, 'r') as f:
                pid = int(f.read().strip())
            if pid == os.getpid():
                LOCK_FILE.unlink()
                logging.info("Released lock file.")
        except: pass

import atexit
atexit.register(release_lock)

def connect_to_db():
    conn_str = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={SERVER};DATABASE={DATABASE};"
        f"UID={USERNAME};PWD={PASSWORD}"
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

def get_breakout_pnl_stats(date_str):
    """
    [V20260128_1630] Load strategy-level P&L from _summary_net.json for profitability guard.
    """
    stats = {}
    for day_dir in iter_day_dirs(JSON_ROOT, "live", date_str, config=load_layout_config(CONFIG_FILE)):
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

def save_json(path, data):
    try:
        with open(path, "w") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        logging.error(f"Failed to save {path.name}: {e}")

def is_dna_model(model_name):
    """[V20260128_0145] Check if model is DNA (SQL) or breakout (JSON)"""
    return model_name.lower().startswith('dna_')

def get_json_open_trades(model, product, date_str):
    """
    [V20260128_1530] Scan JSON files for open trades matching model/product.
    Uses filename stem as ID if missing in content.
    """
    trades = []

    # Pattern: {model}_{product}_*_op.json
    pattern = f"{model}_{product}_*_op.json"
    for date_folder in iter_day_dirs(JSON_ROOT, "live", date_str, config=load_layout_config(CONFIG_FILE)):
        for op_file in date_folder.glob(pattern):
            try:
                with open(op_file, 'r') as f:
                    trade_data = json.load(f)

                trade_id = str(trade_data.get('trade_id') or op_file.stem)

                if trade_data.get('status') == 'OPEN':
                    trades.append({
                        'trade_id': trade_id,
                        'direction': trade_data.get('direction', 'LONG'),
                        'entry_price': float(trade_data.get('entry_price', 0)),
                        'cumulative_pnl': float(trade_data.get('cumulative_pnl', 0)),
                        'cumulative_alt_pnl': float(trade_data.get('cumulative_alt_pnl', 0)),
                        'file_path': str(op_file),
                        'filename': op_file.name
                    })
            except Exception as e:
                logging.warning(f"Failed to read {op_file.name}: {e}")

    return trades

def check_json_trade_closed(model, product, trade_id, filename, date_str):
    """
    [V20260128_1530] Check if a JSON trade has been closed.
    Uses the stored filename for direct lookup first.
    """
    for date_folder in iter_day_dirs(JSON_ROOT, "live", date_str, config=load_layout_config(CONFIG_FILE)):
        op_file = date_folder / filename
        if op_file.exists():
            try:
                with open(op_file, 'r') as f:
                    trade_data = json.load(f)
                if trade_data.get('status') == 'OPEN':
                    return False, 0.0
            except:
                pass

        stem = Path(filename).stem
        if stem.endswith('_op'):
            stem = stem[:-3]
        
        for suffix in ['_cl.json', '_cld.json']:
            f = date_folder / f"{stem}{suffix}"
            if f.exists():
                try:
                    with open(f, 'r') as json_f:
                        data = json.load(json_f)
                    return True, float(data.get('exit_price') or data.get('current_price') or 0.0)
                except:
                    pass

        pattern = f"{model}_{product}_*_cl.json"
        for f in date_folder.glob(pattern):
            if trade_id in f.name:
                try:
                    with open(f, 'r') as json_f:
                        data = json.load(json_f)
                    return True, float(data.get('exit_price') or data.get('current_price') or 0.0)
                except:
                    pass

    return True, 0.0

def mark_json_trade_as_live(file_path):
    """
    [V20260128_1015] Updates the original trade JSON file to mark it as live.
    Sets 'order_sent_net' and 'is_live_trade' to True.
    """
    try:
        path = Path(file_path)
        if not path.exists():
            return False
            
        with open(path, 'r') as f:
            data = json.load(f)
            
        data['order_sent_net'] = True
        data['is_live_trade'] = True
        
        # Atomic write
        temp_path = path.with_suffix('.tmp')
        with open(temp_path, 'w') as f:
            json.dump(data, f, indent=4)
        
        os.replace(temp_path, path)
        logging.info(f"Marked trade as live: {path.name}")
        return True
    except Exception as e:
        logging.error(f"Failed to mark trade as live {file_path}: {e}")
        return False

def create_l_trade_json(product, direction, model_id, trade_guid, metric_mode, is_close, price, is_dna=True):
    """
    [V20260128_1630] Create an L-Trade order file for TWS injection.
    Excludes '_dna_' prefix for breakout trades.
    """
    timestamp_str = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
    
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
    # [V20260128_1630] Dynamic source prefix (dna vs breakout)
    filename = f"grid_live_{product}_{source_prefix}_{model_id}_{action}_{timestamp_str}_{suffix}"
    
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
    filepath = os.path.join(TWS_ORDER_DIR, filename)
    
    try:
        with open(filepath, "w") as f:
            json.dump(tradeable_data, f, indent=2)
        logging.info(f"Successfully created L-Trade order: {filename}")
        return True
    except Exception as e:
        logging.error(f"Failed to create order file {filename}: {e}")
        return False

def monitor_loop():
    sent_trades = load_json(SENT_TRADES_FILE, {}) # { guid: {status: 'OPEN_SENT', model: '...', metric: '...' } }
    cycle_count = 0

    while True:
        cycle_count += 1
        try:
            live_config = load_json(GRID_LIVE_FILE, {}) # { group: [{model, product, metric}] }

            if not live_config:
                if cycle_count % 12 == 1:
                    logging.info(f"[CYCLE {cycle_count}] No active live models in grid_live.json - waiting...")
                time.sleep(POLL_INTERVAL)
                continue

            # Flatten live models
            dna_models = {}      # (model, product) -> metric
            breakout_models = {} # (model, product) -> metric

            for group, models in live_config.items():
                for m in models:
                    model_name = str(m['model'])
                    product = str(m['product']).upper()
                    metric = m.get('metric', 'net')
                    if is_dna_model(model_name):
                        dna_models[(model_name, product)] = metric
                    else:
                        breakout_models[(model_name, product)] = metric

            today_str = datetime.utcnow().strftime('%Y-%m-%d')
            dirty = False
            matched_count = 0
            total_models = len(dna_models) + len(breakout_models)

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
                                stats = pnl_stats.get((m_str, p_str), {'net': 0, 'alt': 0})
                                pnl = stats['alt'] if metric == 'alt' else stats['net']
                                if pnl > 0:
                                    if create_l_trade_json(p_str, sig, m_str, guid, metric, False, ep, is_dna=True):
                                        sent_trades[guid] = {'status': 'OPEN_SENT', 'model': m_str, 'product': p_str, 'metric': metric, 'source': 'dna', 'sent_at': datetime.utcnow().isoformat()}
                                        dirty = True
                    
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
                        guid = f"json_{m_name}_{p_name}_{t['trade_id']}"
                        if guid not in sent_trades:
                            matched_count += 1
                            if strat_pnl > 0:
                                if create_l_trade_json(p_name, t['direction'], m_name, guid, metric, False, t['entry_price'], is_dna=False):
                                    mark_json_trade_as_live(t['file_path'])
                                    sent_trades[guid] = {'status': 'OPEN_SENT', 'model': m_name, 'product': p_name, 'metric': metric, 'source': 'breakout', 'trade_id': t['trade_id'], 'filename': t['filename'], 'sent_at': datetime.utcnow().isoformat()}
                                    dirty = True
                
                # Breakout Closes
                for guid, d in list(sent_trades.items()):
                    if d['status'] == 'OPEN_SENT' and d.get('source') == 'breakout':
                        is_cl, exit_p = check_json_trade_closed(d['model'], d['product'], d.get('trade_id',''), d.get('filename',''), today_str)
                        if is_cl:
                            if create_l_trade_json(d['product'], None, d['model'], guid, d['metric'], True, exit_p, is_dna=False):
                                sent_trades[guid]['status'] = 'CLOSED_SENT'
                                sent_trades[guid]['closed_at'] = datetime.utcnow().isoformat()
                                dirty = True

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
