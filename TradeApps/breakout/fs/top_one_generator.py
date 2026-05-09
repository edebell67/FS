#!/usr/bin/env python
import os
import json
import glob
import time
from pathlib import Path
from datetime import datetime
import pyodbc
from json_layout import iter_day_dirs, load_layout_config

# --- Database Configuration ---
DB_SERVER = "tcp:EDS,1433"
DB_USERNAME = "sqlaccessfromapi"
DB_PASSWORD = "apiaccess@4321"
DB_DRIVER = "{ODBC Driver 17 for SQL Server}"

# This variable is no longer used but kept for reference
MIN_PROFIT_INCREMENT = 0.01 

def get_db_connection(db_name):
    """Establishes and returns a database connection for a specific database."""
    try:
        conn_str = f"DRIVER={DB_DRIVER};SERVER={DB_SERVER};DATABASE={db_name};UID={DB_USERNAME};PWD={DB_PASSWORD}"
        conn = pyodbc.connect(conn_str)
        print(f"Successfully connected to database: {db_name}")
        return conn
    except pyodbc.Error as ex:
        sqlstate = ex.args[0]
        print(f"Database connection error for '{db_name}': {sqlstate} - {ex}")
        return None

def create_table_if_not_exists(conn):
    """Creates the tbl_top_one table if it doesn't already exist."""
    db_name = conn.getinfo(pyodbc.SQL_DATABASE_NAME)
    try:
        cursor = conn.cursor()
        table_name = "tbl_top_one"
        print(f"Checking for table '{table_name}' in database '{db_name}'...")
        if cursor.tables(table=table_name, tableType='TABLE').fetchone():
            print(f"Table '{table_name}' already exists in '{db_name}'.")
        else:
            print(f"Table '{table_name}' does not exist in '{db_name}'. Attempting to create it.")
            create_table_query = f"""
            CREATE TABLE {table_name} (
                id INT PRIMARY KEY IDENTITY(1,1),
                product NVARCHAR(50),
                strategy_and_params NVARCHAR(255),
                direction NVARCHAR(10),
                total_net_return FLOAT,
                last_update DATETIME2
            );
            """
            cursor.execute(create_table_query)
            conn.commit()
            print(f"Table '{table_name}' created successfully in '{db_name}'.")
        cursor.close()
    except pyodbc.Error as ex:
        print(f"Error creating or checking for table in '{db_name}': {ex}")

def insert_into_db(conn, data):
    """
    Inserts the top buy/sell records into tbl_top_one on every cycle.
    """
    db_name = conn.getinfo(pyodbc.SQL_DATABASE_NAME)
    try:
        cursor = conn.cursor()
        last_update_dt = datetime.fromisoformat(data['last_update'])

        # --- Process Top Buy ---
        if 'top_buy' in data and data['top_buy']:
            buy_data = data['top_buy']
            product = str(buy_data['product']).strip()
            new_return = buy_data['total_net_return']
            
            insert_query = """
            INSERT INTO tbl_top_one (product, strategy_and_params, direction, total_net_return, last_update)
            VALUES (?, ?, ?, ?, ?);
            """
            cursor.execute(insert_query, 
                           product, 
                           buy_data['strategy_and_params'], 
                           buy_data['direction'], 
                           new_return, 
                           last_update_dt)
            print(f"Inserted 'buy' record for {product} with return {new_return:.2f}")

        # --- Process Top Sell ---
        if 'top_sell' in data and data['top_sell']:
            sell_data = data['top_sell']
            product = str(sell_data['product']).strip()
            new_return = sell_data['total_net_return']

            insert_query = """
            INSERT INTO tbl_top_one (product, strategy_and_params, direction, total_net_return, last_update)
            VALUES (?, ?, ?, ?, ?);
            """
            cursor.execute(insert_query, 
                           product, 
                           sell_data['strategy_and_params'], 
                           sell_data['direction'], 
                           new_return, 
                           last_update_dt)
            print(f"Inserted 'sell' record for {product} with return {new_return:.2f}")

        conn.commit()
        cursor.close()
    except pyodbc.Error as ex:
        print(f"Database insert error in '{db_name}': {ex}")
    except Exception as e:
        print(f"An unexpected error occurred during DB insert in '{db_name}': {e}")


BASE_DIR = Path(__file__).resolve().parent
CONFIG_PATH = BASE_DIR / 'config.json'
VALID_RUN_MODES = {'live', 'sim'}




def load_main_config() -> dict:
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(f"Breakout config not found at {CONFIG_PATH}")
    with CONFIG_PATH.open('r') as fh:
        return json.load(fh)


def resolve_run_modes(config: dict) -> list[str]:
    modes = config.get('run_modes')
    if isinstance(modes, list):
        normalized = [str(m).lower() for m in modes]
        filtered = [m for m in normalized if m in VALID_RUN_MODES]
        if filtered:
            return filtered
    run_mode = str(config.get('run_mode', 'live')).lower()
    if run_mode == 'both':
        return ['live', 'sim']
    if run_mode in VALID_RUN_MODES:
        return [run_mode]
    print(f"Warning: Unknown run_mode '{run_mode}'. Defaulting to 'live'.")
    return ['live']


def resolve_db_name(run_mode: str, config: dict) -> str:
    override_key = f'top_one_db_{run_mode}'
    override_map = config.get('top_one_databases', {})
    if override_key in config:
        return str(config[override_key])
    if isinstance(override_map, dict) and override_map.get(run_mode):
        return str(override_map[run_mode])
    return 'tradedb_sim2' if run_mode == 'sim' else 'tradedb'

    """Loads the breakout config, raising a clear error if it is missing."""
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(f'Breakout config not found at {CONFIG_PATH}')
    with CONFIG_PATH.open('r') as fh:
        return json.load(fh)


def generate_top_one_summary():
    """
    This script calculates top strategies, writes them to a '.json' file,
    and saves them to a database determined by the run_mode in config.json.
    """
    initialized_dbs = set()
    try:
        while True:
            try:
                print(f"\n--- Starting new cycle at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---")
                
                # 1. Read config
                main_config = load_main_config()
                
                top_n = main_config.get('top_n_strategies', 1)
                
                run_modes = resolve_run_modes(main_config)
                for run_mode in run_modes:
                    try:
                        print(f"DEBUG: Starting collection for mode: {run_mode}")
                        db_name_to_use = resolve_db_name(run_mode, main_config)
                        
                        # Database connection setup
                        if db_name_to_use not in initialized_dbs:
                            db_conn_setup = get_db_connection(db_name_to_use)
                            if db_conn_setup:
                                create_table_if_not_exists(db_conn_setup)
                                initialized_dbs.add(db_name_to_use)
                                db_conn_setup.close()

                        # 2. Determine directory
                        today_str = datetime.now().strftime('%Y-%m-%d')
                        json_root = CONFIG_PATH.parent / 'json'
                        day_dirs = iter_day_dirs(json_root, run_mode, today_str, config=load_layout_config(CONFIG_PATH))

                        if not day_dirs:
                            print(f"DEBUG: Directory not found for {run_mode}: {today_str}")
                            continue
                        
                        # 3. Aggregate data
                        summary = {}
                        processed_files = 0
                        for directory in day_dirs:
                            file_paths = glob.glob(os.path.join(str(directory), '*_cl.json'))
                            for file_path in file_paths:
                                filename = os.path.basename(file_path)
                                try:
                                    with open(file_path, 'r') as f:
                                        trade = json.load(f)
                                    
                                    if isinstance(trade, dict) and trade.get('status') in ('CLOSED', 'OPEN'):
                                        product = trade.get('product')
                                        direction = trade.get('direction')
                                        net_return = trade.get('net_return')

                                        if product and direction and isinstance(net_return, (int, float)):
                                            processed_files += 1
                                            splitter = f'_{product.upper()}_'
                                            strategy_and_params = filename.split(splitter)[0] if splitter in filename else 'unknown_strategy'
                                            key = (product, direction, strategy_and_params)
                                            summary[key] = summary.get(key, 0) + net_return
                                except:
                                    continue

                        # 4. Find Top N
                        if summary:
                            update_dt = datetime.now().isoformat()
                            output_data = {
                                "last_update": update_dt,
                                "top_n": top_n,
                                "global": {"buy": [], "sell": []},
                                "by_product": {}
                            }
                            
                            items = sorted(summary.items(), key=lambda x: x[1], reverse=True)
                            
                            # Global
                            buys = [it for it in items if it[0][1] == 'LONG'][:top_n]
                            sells = [it for it in items if it[0][1] == 'SHORT'][:top_n]
                            
                            for b in buys:
                                output_data["global"]["buy"].append({"product": b[0][0], "strategy": b[0][2], "direction": "buy", "pnl": b[1]})
                            for s in sells:
                                output_data["global"]["sell"].append({"product": s[0][0], "strategy": s[0][2], "direction": "sell", "pnl": s[1]})
                            
                            # Legacy root keys
                            if buys:
                                b = buys[0]
                                output_data["top_buy"] = {"product": b[0][0], "strategy_and_params": b[0][2], "direction": "buy", "total_net_return": b[1]}
                            if sells:
                                s = sells[0]
                                output_data["top_sell"] = {"product": s[0][0], "strategy_and_params": s[0][2], "direction": "sell", "total_net_return": s[1]}

                            # By Product
                            prods = sorted(list(set(it[0][0] for it in items)))
                            for p in prods:
                                p_items = [it for it in items if it[0][0] == p]
                                p_buys = [it for it in p_items if it[0][1] == 'LONG'][:top_n]
                                p_sells = [it for it in p_items if it[0][1] == 'SHORT'][:top_n]
                                output_data["by_product"][p] = {
                                    "buy": [{"strategy": it[0][2], "pnl": it[1]} for it in p_buys],
                                    "sell": [{"strategy": it[0][2], "pnl": it[1]} for it in p_sells]
                                }

                            # 5. Write JSON
                            for directory in day_dirs:
                                output_filepath = str(directory / '_top_one.json')
                                temp_path = output_filepath + ".tmp"
                                try:
                                    with open(temp_path, 'w') as outf:
                                        json.dump(output_data, outf, indent=2)
                                    os.replace(temp_path, output_filepath)
                                    print(f"Successfully wrote {run_mode} summary ({processed_files} files) to {output_filepath}.")
                                except:
                                    pass

                            # 6. Database record
                            db_conn = get_db_connection(db_name_to_use)
                            if db_conn:
                                try: insert_into_db(db_conn, output_data)
                                finally: db_conn.close()
                    except Exception as e:
                        print(f"Error in mode {run_mode}: {e}")

            except Exception as e:
                print(f"An unexpected error occurred in cycle: {e}")

            # 6. Wait
            time.sleep(60)
    except Exception as e:
        print(f"A critical error occurred outside the main loop: {e}")
    finally:
        print("--- Script finished ---")

if __name__ == "__main__":
    generate_top_one_summary()
