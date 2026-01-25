
import os
import json
import time
import pyodbc
import logging
from datetime import datetime
from pathlib import Path

# [V20260126_0900] Grid Live Trading Monitor
# Watches SQL Server for models marked "Live" in Multi-Chart Grid
# and generates L-Trade JSON orders for TWS.

# --- Configuration ---
POLL_INTERVAL = 5 # Seconds
GRID_LIVE_FILE = Path(r"C:\Users\edebe\eds\grid_live.json")
SENT_TRADES_FILE = Path(r"C:\Users\edebe\eds\grid_live_sent_trades.json")
CONFIG_FILE = Path(r"C:\Users\edebe\eds\TradeApps\breakout\fs\config.json")

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
        logging.FileHandler(r"C:\Users\edebe\eds\grid_live_monitor.log"),
        logging.StreamHandler()
    ]
)

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

def save_json(path, data):
    try:
        with open(path, "w") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        logging.error(f"Failed to save {path.name}: {e}")

def create_l_trade_json(product, direction, model_id, trade_guid, metric_mode, is_close, price=0.0):
    """
    Simulates the L-Trade process from common.py
    Creates a JSON file that a separate watcher (e.g. TWS relay) will pick up.
    """
    timestamp_str = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
    
    # Logic from common.py _create_l_trade_order
    strategy_action = 'BUY' if (direction or '').upper() in ('LONG', 'BUY') else 'SELL'
    
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
    # Format matches common.py: {product}_{strategy}_{action}_{timestamp}_{suffix}
    filename = f"{product}_dna_{model_id}_{action}_{timestamp_str}_{suffix}"
    
    # Default qty from config/common
    qty = 45000 # 100k * 45%
    
    tradeable_data = {
        'symbol': product,
        'secType': 'CASH',
        'exchange': 'IDEALPRO',
        'currency': 'USD',
        'action': action,
        'orderType': 'MKT',
        'quantity': qty,
        'guidePrice': price,
        'comment': f"GRID-LIVE dna_{model_id} {metric_mode.upper()} {phase} #{trade_guid}",
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
    
    while True:
        try:
            live_config = load_json(GRID_LIVE_FILE, {}) # { group: [{model, product, metric}] }
            if not live_config:
                time.sleep(POLL_INTERVAL)
                continue
                
            # Flatten live models for easier lookup
            live_models = {} # (model, product) -> metric
            for group, models in live_config.items():
                for m in models:
                    live_models[(str(m['model']), str(m['product']).upper())] = m.get('metric', 'net')
            
            conn = connect_to_db()
            cursor = conn.cursor()
            
            # 1. Check for OPEN Trades in SQL
            cursor.execute("SELECT model, product, signal, guid, entry_price FROM dbo.combined_trades_open")
            open_trades = cursor.fetchall()
            
            # Get current P&L sum per model to check "Positive Territory"
            cursor.execute("SELECT product, model, net_return_sum, alt_net_return_sum FROM dbo.dna_pnl_stream_cache")
            pnl_stats = {} # (model, product) -> {net, alt}
            for row in cursor.fetchall():
                # Indices: 0: product, 1: model, 2: net_return_sum, 3: alt_net_return_sum
                pnl_stats[(str(row[1]), str(row[0]).upper())] = {
                    'net': float(row[2] or 0),
                    'alt': float(row[3] or 0)
                }

            dirty = False
            for trade in open_trades:
                # Indices: 0: model, 1: product, 2: signal, 3: guid, 4: entry_price
                model_str = str(trade[0])
                prod_str = str(trade[1]).upper()
                guid = str(trade[3])
                
                if (model_str, prod_str) in live_models:
                    metric = live_models[(model_str, prod_str)]
                    
                    if guid not in sent_trades:
                        stats = pnl_stats.get((model_str, prod_str), {'net': 0, 'alt': 0})
                        pnl = stats['alt'] if metric == 'alt' else stats['net']
                        
                        if pnl > 0:
                            logging.info(f"Found NEW live trade for model {model_str} {prod_str} (P&L: ${pnl:.2f})")
                            if create_l_trade_json(prod_str, trade[2], model_str, guid, metric, is_close=False, price=float(trade[4] or 0)):
                                sent_trades[guid] = {
                                    'status': 'OPEN_SENT',
                                    'model': model_str,
                                    'product': prod_str,
                                    'metric': metric,
                                    'sent_at': datetime.utcnow().isoformat()
                                }
                                dirty = True
                        else:
                            logging.debug(f"Skipping trade {guid} for {model_str} - Negative Territory (${pnl:.2f})")

            # 2. Check for CLOSED Trades in SQL
            cursor.execute("SELECT guid, latest_price FROM dbo.combined_trades_closed")
            closed_guids = {str(row[0]): float(row[1] or 0) for row in cursor.fetchall()}
            
            for guid, data in list(sent_trades.items()):
                if data['status'] == 'OPEN_SENT' and guid in closed_guids:
                    logging.info(f"Trade {guid} for model {data['model']} detected as CLOSED in SQL.")
                    if create_l_trade_json(data['product'], None, data['model'], guid, data['metric'], is_close=True, price=closed_guids[guid]):
                        sent_trades[guid]['status'] = 'CLOSED_SENT'
                        sent_trades[guid]['closed_at'] = datetime.utcnow().isoformat()
                        dirty = True
            
            if dirty:
                save_json(SENT_TRADES_FILE, sent_trades)
                
            conn.close()
            
        except Exception as e:
            logging.error(f"Error in monitor loop: {e}")
            traceback_str = "".join(pyodbc.traceback.format_exc()) if hasattr(pyodbc, 'traceback') else ""
            logging.error(traceback_str)
            
        time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    logging.info("Starting Grid Live Monitor Service...")
    monitor_loop()
