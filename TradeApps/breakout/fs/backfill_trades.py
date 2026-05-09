# backfill_trades.py

import os
import json
import hashlib
import psycopg2
from psycopg2.extras import Json
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime
import time

# Load database configuration from .env file
load_dotenv()

# --- CONFIGURATION ---
# Base directory where the 'live' and 'sim' folders are located
JSON_BASE_DIR = r"C:\Users\edebe\eds\TradeApps\breakout\fs\json"
ROOT_FS_DIR = r"C:\Users\edebe\eds\TradeApps\breakout\fs"
# Set to 'live', 'sim', or ['live', 'sim'] to control what gets processed
MODES_TO_PROCESS = ['live', 'sim']
# Optional comma-separated list of YYYY-MM-DD folders to limit processing
# [V20260120_0430] Removed hardcoded dates to allow auto-sync of today's trades
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
    cursor.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_fs_json_archive_group_date
        ON fs_json_archive (file_group, file_date);
        """
    )


def is_date_folder(folder_name):
    """Returns True when folder_name matches YYYY-MM-DD."""
    try:
        datetime.strptime(folder_name, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def classify_file(file_path):
    """Classifies a JSON file path for archive metadata."""
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
    """Collects daily live/sim files for existing structured ingestion."""
    files_to_process = []
    for mode in MODES_TO_PROCESS:
        mode_path = os.path.join(JSON_BASE_DIR, mode)
        if not os.path.isdir(mode_path):
            continue

        for date_folder in os.listdir(mode_path):
            if not is_date_folder(date_folder):
                continue
            if TARGET_DATES and date_folder not in TARGET_DATES:
                continue

            full_date_path = os.path.join(mode_path, date_folder)
            if not os.path.isdir(full_date_path):
                continue

            for root, _, filenames in os.walk(full_date_path):
                relative_path = os.path.relpath(root, full_date_path)
                relative_path = '' if relative_path == '.' else relative_path
                for filename in filenames:
                    if filename.endswith('.json'):
                        file_path = os.path.join(root, filename)
                        files_to_process.append((file_path, mode, date_folder, relative_path))
    return files_to_process


def discover_archive_files():
    """Collects all JSON files that should be archived."""
    candidates = set()

    for fp in Path(ROOT_FS_DIR).glob("*.json"):
        candidates.add(str(fp))

    for fp in Path(JSON_BASE_DIR).glob("*.json"):
        candidates.add(str(fp))

    for mode in MODES_TO_PROCESS:
        mode_path = Path(JSON_BASE_DIR) / mode
        if not mode_path.exists():
            continue

        for fp in mode_path.glob("*.json"):
            candidates.add(str(fp))

        for date_dir in mode_path.iterdir():
            if not date_dir.is_dir() or not is_date_folder(date_dir.name):
                continue
            if TARGET_DATES and date_dir.name not in TARGET_DATES:
                continue
            for fp in date_dir.rglob("*.json"):
                candidates.add(str(fp))

    strategy_profile_dir = Path(JSON_BASE_DIR) / "strategy_profile"
    if strategy_profile_dir.exists():
        for fp in strategy_profile_dir.rglob("*.json"):
            candidates.add(str(fp))

    return sorted(candidates)


def archive_json_file(cursor, file_path):
    """
    Archives a JSON file in fs_json_archive.
    Returns one of: inserted, unchanged, excluded, failed
    """
    file_name = os.path.basename(file_path)
    if file_name.lower() in ARCHIVE_EXCLUDE_FILES:
        return "excluded"

    file_group, run_mode, file_date = classify_file(file_path)

    try:
        text = Path(file_path).read_text(encoding="utf-8")
    except UnicodeDecodeError:
        text = Path(file_path).read_text(encoding="utf-8-sig")
    except Exception as e:
        cursor.execute(
            """
            INSERT INTO fs_json_archive (
                file_path, file_name, file_group, run_mode, file_date, content_hash, json_data, ingest_status, error
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, 'failed', %s)
            ON CONFLICT (file_path, content_hash) DO NOTHING;
            """,
            (str(file_path), file_name, file_group, run_mode, file_date, "READ_ERROR", Json(None), str(e)),
        )
        return "failed"

    content_hash = hashlib.sha256(text.encode("utf-8")).hexdigest()

    try:
        payload = json.loads(text)
        ingest_status = "ok"
        error = None
    except Exception as e:
        payload = None
        ingest_status = "failed"
        error = f"JSON parse error: {e}"

    cursor.execute(
        """
        INSERT INTO fs_json_archive (
            file_path, file_name, file_group, run_mode, file_date, content_hash, json_data, ingest_status, error
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (file_path, content_hash) DO NOTHING;
        """,
        (
            str(file_path),
            file_name,
            file_group,
            run_mode,
            file_date,
            content_hash,
            Json(payload),
            ingest_status,
            error,
        ),
    )
    if cursor.rowcount > 0:
        return "inserted"
    return "unchanged"

def process_trade_file(cursor, file_path, run_mode, source_path):
    """Processes a single individual trade JSON file."""
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)

        # Skip if essential data is missing
        if 'trade_id' not in data:
            return 0, 1 # (success, skipped)

        # SQL for UPSERT operation
        # It tries to insert a new trade. If a trade with the same (run_mode, trade_id)
        # already exists, it updates the existing record instead.
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
                product = EXCLUDED.product,
                direction = EXCLUDED.direction,
                status = EXCLUDED.status,
                entry_time = EXCLUDED.entry_time,
                entry_price = EXCLUDED.entry_price,
                exit_time = EXCLUDED.exit_time,
                exit_price = EXCLUDED.exit_price,
                exit_reason = EXCLUDED.exit_reason,
                net_return = EXCLUDED.net_return,
                alt_net = EXCLUDED.alt_net,
                script_name = EXCLUDED.script_name,
                strategy_key = EXCLUDED.strategy_key,
                is_live_trade = EXCLUDED.is_live_trade,
                order_sent_net = EXCLUDED.order_sent_net,
                order_sent_alt = EXCLUDED.order_sent_alt,
                raw_data = EXCLUDED.raw_data,
                source_path = EXCLUDED.source_path;
        """
        
        product = data.get('product') or 'UNKNOWN'
        direction = data.get('direction') or 'UNKNOWN'
        script_name = data.get('script_name') or data.get('script') or data.get('source_strategy') or 'unknown_script'

        # [V20260119_1730] Extract app_name and strategy from filename to match trade_viewer_api.py logic
        filename = Path(file_path).stem
        parts = filename.split('_')

        parsed_app_name = 'unknown'
        parsed_strategy = 'unknown'

        if filename.startswith('vt_'):
            parsed_app_name = 'virtual_trade'
            parsed_strategy = data.get('source_strategy') or 'unknown'
        else:
            timestamp_idx = None
            for i, part in enumerate(parts):
                if len(part) == 8 and part.isdigit():
                    timestamp_idx = i
                    break

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
                            else:
                                parsed_app_name = '_'.join(parts[:candidate_idx])
                        else:
                            parsed_app_name = '_'.join(parts[:candidate_idx])
                    else:
                        if len(val) >= 3 and val.isalpha() and val.isupper():
                            parsed_app_name = '_'.join(parts[:candidate_idx])
                        else:
                            parsed_app_name = '_'.join(parts[:timestamp_idx])
                else:
                    parsed_app_name = '_'.join(parts[:timestamp_idx])

                window = parts[timestamp_idx + 2] if timestamp_idx + 2 < len(parts) else '5'
                pb = parts[timestamp_idx + 3] if timestamp_idx + 3 < len(parts) else '0.0001'
                tp = parts[timestamp_idx + 4].replace('.json', '') if timestamp_idx + 4 < len(parts) else '10.0'
                sl = parts[timestamp_idx + 5].replace('.json', '') if timestamp_idx + 5 < len(parts) else '6.0'
                parsed_strategy = f"{window}_{pb}_{tp}_{sl}"
        # Inject into data object for frontend compatibility [V20260119_1730]
        if 'app_name' not in data:
            data['app_name'] = parsed_app_name
        if 'strategy' not in data:
            data['strategy'] = parsed_strategy
        if 'product' not in data:
            data['product'] = product

        params = {
            'trade_id': data.get('trade_id'),
            'run_mode': run_mode,
            'product': product,
            'direction': direction,
            'status': data.get('status'),
            'entry_time': data.get('entry_time'),
            'entry_price': data.get('entry_price'),
            'exit_time': data.get('exit_time'),
            'exit_price': data.get('exit_price'),
            'exit_reason': data.get('exit_reason'),
            'net_return': data.get('net_return'),
            'alt_net': data.get('alt_net'),
            'script_name': script_name,
            'strategy_key': parsed_strategy,
            'is_live_trade': data.get('is_live_trade'),
            'order_sent_net': data.get('order_sent_net'),
            'order_sent_alt': data.get('order_sent_alt'),
            'raw_data': Json(data), # Use psycopg2's Json helper
            'source_path': str(file_path)
        }

        cursor.execute(sql, params)
        return 1, 0 # (success, skipped)

    except (json.JSONDecodeError, KeyError, TypeError) as e:
        error_message = f"Skipping malformed trade file: {file_path} | Error: {e}"
        print(f"\n {error_message}")
        with open("backfill_errors.log", "a") as error_log:
            error_log.write(f"{datetime.now().isoformat()} - {error_message}\n")
        return 0, 1

def process_summary_file(cursor, file_path, run_mode, summary_date):
    """Processes a single summary JSON file."""
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)

        summary_type = os.path.basename(file_path).replace('.json', '')

        sql = """
            INSERT INTO daily_summary (run_mode, summary_date, summary_type, data)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (run_mode, summary_date, summary_type) DO UPDATE SET
                data = EXCLUDED.data;
        """
        cursor.execute(sql, (run_mode, summary_date, summary_type, Json(data)))
        return 1, 0

    except (json.JSONDecodeError, KeyError) as e:
        error_message = f"Skipping malformed summary file: {file_path} | Error: {e}"
        print(f"\n {error_message}")
        with open("backfill_errors.log", "a") as error_log:
            error_log.write(f"{datetime.now().isoformat()} - {error_message}\n")
        return 0, 1

def process_grid_history(cursor, file_path):
    """Processes the grid_live_history.json file."""
    try:
        if not os.path.exists(file_path):
            return 0
            
        with open(file_path, 'r') as f:
            history_data = json.load(f)
            
        if not isinstance(history_data, list):
            return 0
            
        # Create table if not exists (Lazy initialization)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS grid_snapshots (
                id SERIAL PRIMARY KEY,
                snapshot_timestamp TIMESTAMP NOT NULL,
                run_mode VARCHAR(10),
                activations JSONB,
                UNIQUE (snapshot_timestamp, run_mode)
            );
        """)
        
        count = 0
        for entry in history_data:
            ts = entry.get('timestamp')
            mode = entry.get('mode', 'live')
            snapshot = entry.get('snapshot', {})
            
            if not ts:
                continue
                
            sql = """
                INSERT INTO grid_snapshots (snapshot_timestamp, run_mode, activations)
                VALUES (%s, %s, %s)
                ON CONFLICT (snapshot_timestamp, run_mode) DO NOTHING;
            """
            cursor.execute(sql, (ts, mode, Json(snapshot)))
            if cursor.rowcount > 0:
                count += 1
                
        return count
    except Exception as e:
        print(f"Error processing grid history: {e}")
        return 0

def process_grid_latest(cursor, file_path):
    """Processes the grid_live.json file into daily_summary."""
    try:
        if not os.path.exists(file_path):
            return 0
            
        with open(file_path, 'r') as f:
            data = json.load(f)
            
        summary_date = datetime.now().strftime('%Y-%m-%d')
        summary_type = 'grid_live_latest'
        
        sql = """
            INSERT INTO daily_summary (run_mode, summary_date, summary_type, data)
            VALUES ('live', %s, %s, %s)
            ON CONFLICT (run_mode, summary_date, summary_type) DO UPDATE SET
                data = EXCLUDED.data;
        """
        cursor.execute(sql, (summary_date, summary_type, Json(data)))
        return 1
    except Exception as e:
        print(f"Error processing grid latest: {e}")
        return 0

def main():
    """Main function to run the backfill process in a loop."""
    print(f"Starting Continuous Backfill Sync (Loop: 60s) | Hardcoded Dates: {BACKFILL_DATES}")
    
    while True:
        try:
            conn = get_db_connection()
            if not conn:
                print("DB connection failed. Retrying in 60s...")
                time.sleep(60)
                continue

            files_to_process = discover_structured_files()
            archive_files = discover_archive_files()

            success_count = 0
            skipped_count = 0
            archive_inserted = 0
            archive_unchanged = 0
            archive_failed = 0
            archive_excluded = 0

            with conn.cursor() as cursor:
                ensure_archive_table(cursor)

                for archive_file in archive_files:
                    archive_result = archive_json_file(cursor, archive_file)
                    if archive_result == "inserted":
                        archive_inserted += 1
                    elif archive_result == "unchanged":
                        archive_unchanged += 1
                    elif archive_result == "excluded":
                        archive_excluded += 1
                    else:
                        archive_failed += 1

                conn.commit()

                # [V20260207_GRID] Process root-level grid files first
                success_count += process_grid_history(cursor, os.path.join(JSON_BASE_DIR, 'grid_live_history.json'))
                success_count += process_grid_latest(cursor, os.path.join(ROOT_FS_DIR, 'grid_live.json'))
                conn.commit()

                if files_to_process:
                    for file_path, run_mode, date_str, source_path in files_to_process:
                        filename = os.path.basename(file_path)
                        try:
                            if filename.startswith('_'):
                                s, k = process_summary_file(cursor, file_path, run_mode, date_str)
                            else:
                                s, k = process_trade_file(cursor, file_path, run_mode, source_path)

                            if s > 0:
                                conn.commit()  # Commit each successful file
                                success_count += s
                            skipped_count += k
                        except Exception as e:
                            print(f"Error processing {file_path}: {e}")
                            conn.rollback()
                            skipped_count += 1

            if success_count > 0:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Synced {success_count} files.")
            print(
                f"[{datetime.now().strftime('%H:%M:%S')}] 🧾 Archive scan={len(archive_files)} "
                f"inserted={archive_inserted} unchanged={archive_unchanged} "
                f"excluded={archive_excluded} failed={archive_failed} "
                f"structured_skipped={skipped_count}"
            )
            
            conn.close()
            
        except Exception as e:
            print(f"Loop Error: {e}")
            
        time.sleep(60)

if __name__ == "__main__":
    main()






