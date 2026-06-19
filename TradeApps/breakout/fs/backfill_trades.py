import os
import json
import hashlib
import psycopg2
from psycopg2.extras import Json, execute_values
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime
import time
from paths import BREAKOUT_FS_ROOT, BREAKOUT_JSON_ROOT, BREAKOUT_DATA_FS_ROOT

# Load database configuration from .env file
load_dotenv()

# --- CONFIGURATION ---
JSON_BASE_DIR = BREAKOUT_JSON_ROOT
ROOT_FS_DIR = BREAKOUT_DATA_FS_ROOT 
MODES_TO_PROCESS = ['live', 'sim']
BACKFILL_DATES = os.getenv('BACKFILL_DATES', '').strip()
TARGET_DATES = {d.strip() for d in BACKFILL_DATES.split(',') if d.strip()} if BACKFILL_DATES else None
ARCHIVE_EXCLUDE_FILES = {
    n.strip().lower()
    for n in os.getenv("ARCHIVE_EXCLUDE_FILES", "config copy.json").split(",")
    if n.strip()
}

# --- DATABASE CONNECTION ---
def get_db_connection():
    """Establishes and returns a database connection."""
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )
        return conn
    except psycopg2.OperationalError as e:
        print(f"Could not connect to the database: {e}")
        return None

# --- SCHEMA CREATION ---
def ensure_archive_table(cursor):
    """Creates the archive table used for full-fidelity JSON capture."""
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS fs_json_archive (
            id BIGSERIAL PRIMARY KEY,
            captured_at TIMESTAMP NOT NULL DEFAULT NOW(),
            file_path TEXT NOT NULL,
            file_name TEXT NOT NULL,
            file_group TEXT NOT NULL,
            run_mode VARCHAR(10),
            file_date DATE,
            content_hash TEXT NOT NULL,
            json_data JSONB,
            ingest_status TEXT NOT NULL DEFAULT 'ok',
            error TEXT,
            UNIQUE (file_path, content_hash)
        );
        """
    )
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_fs_json_archive_group_date ON fs_json_archive (file_group, file_date);")

def ensure_summary_net_table(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS summary_net (
            id BIGSERIAL PRIMARY KEY,
            run_mode VARCHAR(10) NOT NULL,
            file_date DATE NOT NULL,
            captured_at TIMESTAMP NOT NULL DEFAULT NOW(),
            strategy_key VARCHAR(100),
            product VARCHAR(20),
            direction VARCHAR(10),
            tp DECIMAL(8,2),
            sl DECIMAL(8,2),
            cum_net DECIMAL(12,2),
            win_rate DECIMAL(5,2),
            total_trades INTEGER,
            data JSONB,
            UNIQUE (run_mode, file_date, strategy_key)
        );
    """)
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_summary_net_date ON summary_net (file_date);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_summary_net_product ON summary_net (product);")

def ensure_top_strategies_table(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS top_strategies (
            id BIGSERIAL PRIMARY KEY,
            run_mode VARCHAR(10) NOT NULL,
            file_date DATE NOT NULL,
            captured_at TIMESTAMP NOT NULL DEFAULT NOW(),
            list_type VARCHAR(50),
            strategy_key VARCHAR(100),
            rank INTEGER,
            data JSONB,
            UNIQUE (run_mode, file_date, list_type, strategy_key)
        );
    """)
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_top_strategies_date ON top_strategies (file_date);")

def ensure_targeted_strategies_table(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS targeted_strategies (
            id BIGSERIAL PRIMARY KEY,
            run_mode VARCHAR(10) NOT NULL,
            file_date DATE NOT NULL,
            captured_at TIMESTAMP NOT NULL DEFAULT NOW(),
            strategy_key VARCHAR(100),
            data JSONB,
            UNIQUE (run_mode, file_date, strategy_key)
        );
    """)

def ensure_trade_buckets_table(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS trade_buckets (
            id BIGSERIAL PRIMARY KEY,
            run_mode VARCHAR(10) NOT NULL,
            file_date DATE NOT NULL,
            captured_at TIMESTAMP NOT NULL DEFAULT NOW(),
            bucket_id VARCHAR(100),
            strategy_key VARCHAR(100),
            data JSONB,
            UNIQUE (run_mode, file_date, bucket_id, strategy_key)
        );
    """)

def ensure_live_trades_snapshots_table(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS live_trades_snapshots (
            id BIGSERIAL PRIMARY KEY,
            run_mode VARCHAR(10) NOT NULL,
            file_date DATE NOT NULL,
            captured_at TIMESTAMP NOT NULL DEFAULT NOW(),
            trade_id VARCHAR(100),
            data JSONB,
            UNIQUE (run_mode, file_date, trade_id)
        );
    """)

def ensure_price_capture_table(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS price_capture (
            id BIGSERIAL PRIMARY KEY,
            run_mode VARCHAR(10) NOT NULL,
            file_date DATE NOT NULL,
            captured_at TIMESTAMP NOT NULL DEFAULT NOW(),
            tick_timestamp VARCHAR(50),
            product VARCHAR(20),
            ask DECIMAL(12,5),
            bid DECIMAL(12,5),
            data JSONB,
            UNIQUE (run_mode, file_date, tick_timestamp, product)
        );
    """)
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_price_capture_date ON price_capture (file_date);")

# --- UTILS ---
def is_date_folder(folder_name):
    try:
        datetime.strptime(folder_name, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def classify_file(file_path):
    p = Path(file_path)
    p_str = str(p)
    p_lower = p_str.replace("/", "\\").lower()
    run_mode = None
    file_date = None
    file_group = "other"

    if p.parent == Path(ROOT_FS_DIR):
        file_group = "fs_root"
    elif p.parent == Path(JSON_BASE_DIR):
        file_group = "json_root"
    elif "\\json\\strategy_profile\\" in p_lower:
        file_group = "strategy_profile"
    elif p.parent == Path(JSON_BASE_DIR) / "live":
        file_group = "mode_root"
        run_mode = "live"
    elif p.parent == Path(JSON_BASE_DIR) / "sim":
        file_group = "mode_root"
        run_mode = "sim"
    elif "\\json\\live\\" in p_str or "/json/live/" in p_str:
        file_group = "daily"
        run_mode = "live"
    elif "\\json\\sim\\" in p_str or "/json/sim/" in p_str:
        file_group = "daily"
        run_mode = "sim"

    parts = p.parts
    for part in parts:
        if is_date_folder(part):
            file_date = part
            break

    return file_group, run_mode, file_date

def discover_structured_files():
    files_to_process = []
    # Explicitly target only live/forex per user request
    mode_path = os.path.join(JSON_BASE_DIR, 'live', 'forex')
    if not os.path.isdir(mode_path):
        return files_to_process

    for root, dirs, filenames in os.walk(mode_path):
        date_folder = os.path.basename(root)
        if not is_date_folder(date_folder):
            continue
        if TARGET_DATES and date_folder not in TARGET_DATES:
            continue

        relative_path = os.path.relpath(root, mode_path)
        relative_path = '' if relative_path == '.' else relative_path
        for filename in filenames:
            if filename.endswith('.json') or filename.endswith('.jsonl'):
                file_path = os.path.join(root, filename)
                files_to_process.append((file_path, 'live', date_folder, relative_path))
    return files_to_process

def discover_archive_files():
    candidates = set()
    # Explicitly target only live/forex per user request to eliminate full drive scanning
    mode_path = Path(JSON_BASE_DIR) / 'live' / 'forex'
    if not mode_path.exists():
        return []
    
    for date_dir in mode_path.iterdir():
        if not date_dir.is_dir() or not is_date_folder(date_dir.name): continue
        if TARGET_DATES and date_dir.name not in TARGET_DATES: continue
        for fp in date_dir.rglob("*.json"): candidates.add(str(fp))
        
    return sorted(candidates)

def archive_json_file(cursor, file_path):
    file_name = os.path.basename(file_path)
    if file_name.lower() in ARCHIVE_EXCLUDE_FILES: return "excluded"
    file_group, run_mode, file_date = classify_file(file_path)
    try: text = Path(file_path).read_text(encoding="utf-8")
    except UnicodeDecodeError: text = Path(file_path).read_text(encoding="utf-8-sig")
    except Exception as e:
        cursor.execute("""
            INSERT INTO fs_json_archive (file_path, file_name, file_group, run_mode, file_date, content_hash, json_data, ingest_status, error)
            VALUES (%s, %s, %s, %s, %s, %s, %s, 'failed', %s)
            ON CONFLICT (file_path, content_hash) DO NOTHING;
            """, (str(file_path), file_name, file_group, run_mode, file_date, "READ_ERROR", Json(None), str(e)))
        return "failed"
    content_hash = hashlib.sha256(text.encode("utf-8")).hexdigest()
    try:
        payload = json.loads(text)
        ingest_status, error = "ok", None
    except Exception as e:
        payload, ingest_status, error = None, "failed", f"JSON parse error: {e}"
    cursor.execute("""
        INSERT INTO fs_json_archive (file_path, file_name, file_group, run_mode, file_date, content_hash, json_data, ingest_status, error)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (file_path, content_hash) DO NOTHING;
        """, (str(file_path), file_name, file_group, run_mode, file_date, content_hash, Json(payload), ingest_status, error))
    return "inserted" if cursor.rowcount > 0 else "unchanged"

# --- HANDLERS ---
def process_trade_file(cursor, file_path, run_mode, source_path):
    try:
        with open(file_path, 'r') as f: data = json.load(f)
        if 'trade_id' not in data: return 0, 1
        
        sql = """
            INSERT INTO trades (
                trade_id, run_mode, product, direction, status, entry_time,
                entry_price, exit_time, exit_price, exit_reason, net_return,
                alt_net, script_name, strategy_key, is_live_trade, order_sent_net, order_sent_alt, raw_data, source_path
            ) VALUES (
                %(trade_id)s, %(run_mode)s, %(product)s, %(direction)s, %(status)s, %(entry_time)s,
                %(entry_price)s, %(exit_time)s, %(exit_price)s, %(exit_reason)s, %(net_return)s,
                %(alt_net)s, %(script_name)s, %(strategy_key)s, %(is_live_trade)s, %(order_sent_net)s, %(order_sent_alt)s, %(raw_data)s, %(source_path)s
            )
            ON CONFLICT (run_mode, trade_id, script_name, product, direction, entry_time) DO UPDATE SET
                product = EXCLUDED.product, direction = EXCLUDED.direction, status = EXCLUDED.status,
                entry_time = EXCLUDED.entry_time, entry_price = EXCLUDED.entry_price, exit_time = EXCLUDED.exit_time,
                exit_price = EXCLUDED.exit_price, exit_reason = EXCLUDED.exit_reason, net_return = EXCLUDED.net_return,
                alt_net = EXCLUDED.alt_net, script_name = EXCLUDED.script_name, strategy_key = EXCLUDED.strategy_key,
                is_live_trade = EXCLUDED.is_live_trade, order_sent_net = EXCLUDED.order_sent_net, order_sent_alt = EXCLUDED.order_sent_alt,
                raw_data = EXCLUDED.raw_data, source_path = EXCLUDED.source_path;
        """
        
        product = data.get('product') or 'UNKNOWN'
        direction = data.get('direction') or 'UNKNOWN'
        script_name = data.get('script_name') or data.get('script') or data.get('source_strategy') or 'unknown_script'

        filename = Path(file_path).stem
        parts = filename.split('_')
        parsed_app_name, parsed_strategy = 'unknown', 'unknown'

        if filename.startswith('vt_'):
            parsed_app_name = 'virtual_trade'
            parsed_strategy = data.get('source_strategy') or 'unknown'
        else:
            timestamp_idx = None
            for i, part in enumerate(parts):
                if len(part) == 8 and part.isdigit():
                    timestamp_idx = i; break
            if timestamp_idx is not None:
                candidate_idx = timestamp_idx - 1
                if candidate_idx >= 0:
                    val = parts[candidate_idx]
                    if len(val) <= 2 and val.isalpha() and val.isupper():
                        product_idx = candidate_idx - 1
                        if product_idx >= 0:
                            potential_product = parts[product_idx]
                            if len(potential_product) >= 3 and potential_product.isalpha() and potential_product.isupper():
                                parsed_app_name = '_'.join(parts[:product_idx])
                            else: parsed_app_name = '_'.join(parts[:candidate_idx])
                        else: parsed_app_name = '_'.join(parts[:candidate_idx])
                    else:
                        if len(val) >= 3 and val.isalpha() and val.isupper(): parsed_app_name = '_'.join(parts[:candidate_idx])
                        else: parsed_app_name = '_'.join(parts[:timestamp_idx])
                else: parsed_app_name = '_'.join(parts[:timestamp_idx])
                
                window = parts[timestamp_idx + 2] if timestamp_idx + 2 < len(parts) else '5'
                pb = parts[timestamp_idx + 3] if timestamp_idx + 3 < len(parts) else '0.0001'
                tp = parts[timestamp_idx + 4].replace('.json', '') if timestamp_idx + 4 < len(parts) else '10.0'
                sl = parts[timestamp_idx + 5].replace('.json', '') if timestamp_idx + 5 < len(parts) else '6.0'
                parsed_strategy = f"{window}_{pb}_{tp}_{sl}"

        if 'app_name' not in data: data['app_name'] = parsed_app_name
        if 'strategy' not in data: data['strategy'] = parsed_strategy
        if 'product' not in data: data['product'] = product

        params = {
            'trade_id': data.get('trade_id'), 'run_mode': run_mode, 'product': product, 'direction': direction,
            'status': data.get('status'), 'entry_time': data.get('entry_time'), 'entry_price': data.get('entry_price'),
            'exit_time': data.get('exit_time'), 'exit_price': data.get('exit_price'), 'exit_reason': data.get('exit_reason'),
            'net_return': data.get('net_return'), 'alt_net': data.get('alt_net'), 'script_name': script_name,
            'strategy_key': parsed_strategy, 'is_live_trade': data.get('is_live_trade'),
            'order_sent_net': data.get('order_sent_net'), 'order_sent_alt': data.get('order_sent_alt'),
            'raw_data': Json(data), 'source_path': str(file_path)
        }
        cursor.execute(sql, params)
        return 1, 0
    except (json.JSONDecodeError, KeyError, TypeError) as e:
        with open("backfill_errors.log", "a") as error_log: error_log.write(f"{datetime.now().isoformat()} - Error: {e} in {file_path}\n")
        return 0, 1

def process_summary_net(cursor, file_path, run_mode, file_date):
    try:
        with open(file_path, 'r') as f: data = json.load(f)
        strategies = data.get('strategies', []) if isinstance(data, dict) else (data if isinstance(data, list) else [data])
        count = 0
        sql = """
            INSERT INTO summary_net (run_mode, file_date, strategy_key, product, direction, tp, sl, cum_net, win_rate, total_trades, data)
            VALUES %s ON CONFLICT (run_mode, file_date, strategy_key) DO UPDATE SET
            cum_net = EXCLUDED.cum_net, win_rate = EXCLUDED.win_rate, total_trades = EXCLUDED.total_trades, data = EXCLUDED.data;
        """
        values = []
        for record in strategies:
            strategy_key = record.get('strategy_key') or record.get('strategy')
            if not strategy_key: continue
            values.append((
                run_mode, file_date, strategy_key, record.get('product'), record.get('direction'),
                record.get('tp'), record.get('sl'), record.get('cum_net'), record.get('win_rate'), record.get('total_trades'), Json(record)
            ))
            count += 1
        if values:
            execute_values(cursor, sql, values)
        return count, 0
    except Exception as e:
        return 0, 1

def process_top_strategies(cursor, file_path, run_mode, file_date):
    try:
        with open(file_path, 'r') as f: data = json.load(f)
        list_type = os.path.basename(file_path).replace('.json', '')
        items = data.get('top20', []) if 'top20' in list_type else (data.get('strategies', data) if isinstance(data, dict) else data)
        if not isinstance(items, list): items = [items]
        count = 0
        sql = """
            INSERT INTO top_strategies (run_mode, file_date, list_type, strategy_key, rank, data)
            VALUES %s ON CONFLICT (run_mode, file_date, list_type, strategy_key) DO UPDATE SET rank = EXCLUDED.rank, data = EXCLUDED.data;
        """
        values = []
        for idx, record in enumerate(items):
            strategy_key = record.get('strategy_key') or record.get('strategy')
            if not strategy_key: continue
            values.append((run_mode, file_date, list_type, strategy_key, idx + 1, Json(record)))
            count += 1
        if values:
            execute_values(cursor, sql, values)
        return count, 0
    except Exception as e:
        return 0, 1

def process_targeted_strategies(cursor, file_path, run_mode, file_date):
    try:
        with open(file_path, 'r') as f: data = json.load(f)
        strategies = data.get('strategies', []) if isinstance(data, dict) else data
        count = 0
        sql = """
            INSERT INTO targeted_strategies (run_mode, file_date, strategy_key, data)
            VALUES %s ON CONFLICT (run_mode, file_date, strategy_key) DO UPDATE SET data = EXCLUDED.data;
        """
        values = []
        for record in strategies:
            strategy_key = record.get('strategy_key') or record.get('strategy')
            if not strategy_key: continue
            values.append((run_mode, file_date, strategy_key, Json(record)))
            count += 1
        if values: execute_values(cursor, sql, values)
        return count, 0
    except Exception as e: return 0, 1

def process_trade_buckets(cursor, file_path, run_mode, file_date):
    try:
        with open(file_path, 'r') as f: data = json.load(f)
        buckets = data.get('buckets', data)
        if not isinstance(buckets, list): buckets = [buckets]
        count = 0
        sql = """
            INSERT INTO trade_buckets (run_mode, file_date, bucket_id, strategy_key, data)
            VALUES %s ON CONFLICT (run_mode, file_date, bucket_id, strategy_key) DO UPDATE SET data = EXCLUDED.data;
        """
        values = []
        for record in buckets:
            bucket_id = record.get('bucket_id') or record.get('id')
            strategy_key = record.get('strategy_key') or record.get('strategy')
            if not bucket_id or not strategy_key: continue
            values.append((run_mode, file_date, str(bucket_id), strategy_key, Json(record)))
            count += 1
        if values: execute_values(cursor, sql, values)
        return count, 0
    except Exception as e: return 0, 1

def process_live_trades_snapshots(cursor, file_path, run_mode, file_date):
    try:
        with open(file_path, 'r') as f: data = json.load(f)
        trades = data.get('trades', data)
        if not isinstance(trades, list): trades = [trades]
        count = 0
        sql = """
            INSERT INTO live_trades_snapshots (run_mode, file_date, trade_id, data)
            VALUES %s ON CONFLICT (run_mode, file_date, trade_id) DO UPDATE SET data = EXCLUDED.data;
        """
        values = []
        for record in trades:
            trade_id = record.get('trade_id') or record.get('id')
            if not trade_id: continue
            values.append((run_mode, file_date, str(trade_id), Json(record)))
            count += 1
        if values: execute_values(cursor, sql, values)
        return count, 0
    except Exception as e: return 0, 1

def process_price_capture(cursor, file_path, run_mode, file_date):
    try:
        count = 0
        sql = """
            INSERT INTO price_capture (run_mode, file_date, tick_timestamp, product, ask, bid, data)
            VALUES %s ON CONFLICT (run_mode, file_date, tick_timestamp, product) DO NOTHING;
        """
        batch = []
        with open(file_path, 'r') as f:
            for line in f:
                if not line.strip(): continue
                try:
                    record = json.loads(line)
                    ts = record.get('timestamp') or record.get('time')
                    product = record.get('product') or record.get('symbol')
                    if not ts or not product: continue
                    batch.append((run_mode, file_date, str(ts), product, record.get('ask'), record.get('bid'), Json(record)))
                    if len(batch) >= 1000:
                        execute_values(cursor, sql, batch)
                        count += len(batch)
                        batch = []
                except Exception: pass
        if batch:
            execute_values(cursor, sql, batch)
            count += len(batch)
        return count, 0
    except Exception as e: return 0, 1

def process_summary_file(cursor, file_path, run_mode, summary_date):
    try:
        with open(file_path, 'r') as f: data = json.load(f)
        summary_type = os.path.basename(file_path).replace('.json', '')
        sql = """
            INSERT INTO daily_summary (run_mode, summary_date, summary_type, data)
            VALUES (%s, %s, %s, %s) ON CONFLICT (run_mode, summary_date, summary_type) DO UPDATE SET data = EXCLUDED.data;
        """
        cursor.execute(sql, (run_mode, summary_date, summary_type, Json(data)))
        return 1, 0
    except (json.JSONDecodeError, KeyError) as e:
        return 0, 1

def process_grid_history(cursor, file_path):
    try:
        if not os.path.exists(file_path): return 0
        with open(file_path, 'r') as f: history_data = json.load(f)
        if not isinstance(history_data, list): return 0
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS grid_snapshots (
                id SERIAL PRIMARY KEY, snapshot_timestamp TIMESTAMP NOT NULL, run_mode VARCHAR(10), activations JSONB,
                UNIQUE (snapshot_timestamp, run_mode)
            );
        """)
        count = 0
        for entry in history_data:
            ts = entry.get('timestamp'); mode = entry.get('mode', 'live'); snapshot = entry.get('snapshot', {})
            if not ts: continue
            cursor.execute("INSERT INTO grid_snapshots (snapshot_timestamp, run_mode, activations) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING;", (ts, mode, Json(snapshot)))
            if cursor.rowcount > 0: count += 1
        return count
    except Exception as e: return 0

def process_grid_latest(cursor, file_path):
    try:
        if not os.path.exists(file_path): return 0
        with open(file_path, 'r') as f: data = json.load(f)
        summary_date = datetime.now().strftime('%Y-%m-%d')
        cursor.execute("""
            INSERT INTO daily_summary (run_mode, summary_date, summary_type, data) VALUES ('live', %s, 'grid_live_latest', %s)
            ON CONFLICT (run_mode, summary_date, summary_type) DO UPDATE SET data = EXCLUDED.data;
        """, (summary_date, Json(data)))
        return 1
    except Exception as e: return 0

# --- MAIN LOOP ---
def main():
    print(f"Starting Continuous Backfill Sync (Loop: 60s) | Hardcoded Dates: {BACKFILL_DATES}")
    while True:
        try:
            conn = get_db_connection()
            if not conn:
                print("DB connection failed. Retrying in 60s..."); time.sleep(60); continue

            files_to_process = discover_structured_files()
            archive_files = discover_archive_files()

            success_count, skipped_count = 0, 0
            archive_inserted, archive_unchanged, archive_failed, archive_excluded = 0, 0, 0, 0

            with conn.cursor() as cursor:
                ensure_archive_table(cursor)
                ensure_summary_net_table(cursor)
                ensure_top_strategies_table(cursor)
                ensure_targeted_strategies_table(cursor)
                ensure_trade_buckets_table(cursor)
                ensure_live_trades_snapshots_table(cursor)
                ensure_price_capture_table(cursor)

                for archive_file in archive_files:
                    archive_result = archive_json_file(cursor, archive_file)
                    if archive_result == "inserted": archive_inserted += 1
                    elif archive_result == "unchanged": archive_unchanged += 1
                    elif archive_result == "excluded": archive_excluded += 1
                    else: archive_failed += 1

                conn.commit()

                success_count += process_grid_history(cursor, os.path.join(JSON_BASE_DIR, 'grid_live_history.json'))
                success_count += process_grid_latest(cursor, os.path.join(ROOT_FS_DIR, 'grid_live.json'))
                conn.commit()

                if files_to_process:
                    for file_path, run_mode, date_str, source_path in files_to_process:
                        filename = os.path.basename(file_path)
                        try:
                            if filename.startswith('_'):
                                if '.tmp' in filename or 'pre_auto_archive' in filename:
                                    continue # Skip temporary and pre-archive files
                                elif filename == '_summary_net.json':
                                    s, k = process_summary_net(cursor, file_path, run_mode, date_str)
                                elif filename in ['_top20.json', '_top_one.json', '_tb_leadership.json'] or filename.startswith('_top10_history'):
                                    s, k = process_top_strategies(cursor, file_path, run_mode, date_str)
                                elif filename == '_targeted_strategies.json':
                                    s, k = process_targeted_strategies(cursor, file_path, run_mode, date_str)
                                elif filename == '_trade_buckets.json':
                                    s, k = process_trade_buckets(cursor, file_path, run_mode, date_str)
                                elif filename == '_live_trades.json':
                                    s, k = process_live_trades_snapshots(cursor, file_path, run_mode, date_str)
                                elif filename == '_price_capture.jsonl':
                                    s, k = process_price_capture(cursor, file_path, run_mode, date_str)
                                else:
                                    s, k = process_summary_file(cursor, file_path, run_mode, date_str)
                            else:
                                s, k = process_trade_file(cursor, file_path, run_mode, source_path)

                            if s > 0:
                                conn.commit()
                                success_count += s
                            else:
                                conn.rollback()
                            skipped_count += k
                        except Exception as e:
                            print(f"Error processing {file_path}: {e}")
                            conn.rollback()
                            skipped_count += 1

            if success_count > 0: print(f"[{datetime.now().strftime('%H:%M:%S')}] Synced {success_count} rows/files.")
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Archive scan={len(archive_files)} inserted={archive_inserted} unchanged={archive_unchanged} excluded={archive_excluded} failed={archive_failed} structured_skipped={skipped_count}")
            conn.close()
        except Exception as e: print(f"Loop Error: {e}")
        time.sleep(60)

if __name__ == "__main__":
    main()
