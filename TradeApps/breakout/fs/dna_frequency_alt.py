import json
import os
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict
import pyodbc
from json_layout import ensure_day_dir, load_layout_config
from paths import BREAKOUT_JSON_ROOT

CONFIG_PATH = Path(__file__).resolve().parent / 'config.json'
BASE_ROOT = BREAKOUT_JSON_ROOT
FREQUENCY_MINUTES = 5
FORCED_DATE = os.environ.get('FREQUENCY_TARGET_DATE')
VALUE_FIELD = 'alt_net_return'
OUTPUT_BASENAME = '_dna_alt_frequency.json'

DB_SERVER = os.getenv('DB_SERVER', 'tcp:EDS,1433')
DB_NAME = os.getenv('DB_NAME', 'tradedb')
DB_USER = os.getenv('DB_USER', 'sqlaccessfromapi')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'apiaccess@4321')
DB_DRIVER = os.getenv('DB_DRIVER', 'ODBC Driver 17 for SQL Server')
CONN_STR = f"DRIVER={{{DB_DRIVER}}};SERVER={DB_SERVER};DATABASE={DB_NAME};UID={DB_USER};PWD={DB_PASSWORD}"


def read_run_mode():
    try:
        with CONFIG_PATH.open('r') as cfg:
            data = json.load(cfg)
        return str(data.get('run_mode', 'live')).lower()
    except Exception:
        return 'live'


def get_conn_str(mode):
    target_db = 'tradedb_sim2' if mode == 'sim' else DB_NAME
    return f"DRIVER={{{DB_DRIVER}}};SERVER={DB_SERVER};DATABASE={target_db};UID={DB_USER};PWD={DB_PASSWORD}"

def fetch_rows(target_date, mode):
    query = """
        SELECT model, product, net_return, alt_net_return, strategy_name, strategy_params,
               created, last_update
        FROM vw_113_Combined_trades_all WITH (NOLOCK)
        WHERE model LIKE 'DNA_%'
          AND CAST(COALESCE(last_update, created) AS DATE) = ?
    """
    connection_string = get_conn_str(mode)
    with pyodbc.connect(connection_string) as conn:
        cursor = conn.cursor()
        cursor.execute(query, target_date)
        columns = [col[0].lower() for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]


def normalize_timestamp(row):
    for key in ('last_update', 'created'):
        val = row.get(key)
        if not val:
            continue
        if isinstance(val, datetime):
            return val
        try:
            return datetime.fromisoformat(str(val))
        except ValueError:
            continue
    return None


def build_race(trades, interval_minutes):
    trades.sort(key=lambda x: x[0])
    if not trades:
        return [], []
    interval = timedelta(minutes=interval_minutes)
    start_time = trades[0][0]
    end_time = max(trades[-1][0], datetime.now()) + interval
    minute = (start_time.minute // interval_minutes) * interval_minutes
    start_floor = start_time.replace(minute=minute, second=0, microsecond=0)
    if start_floor > start_time:
        start_floor -= interval
    cumulative = defaultdict(float)
    freq = defaultdict(int)
    rank1_freq = defaultdict(int)
    weighted = defaultdict(float)
    last_seen = {}
    snapshots = []
    trade_idx = 0
    current = start_floor
    while current <= end_time:
        while trade_idx < len(trades) and trades[trade_idx][0] <= current:
            ts, net, key = trades[trade_idx]
            cumulative[key] += net
            trade_idx += 1
        if cumulative:
            top = sorted(cumulative.items(), key=lambda kv: kv[1], reverse=True)[:5]
            weight = len(snapshots) + 1
            snapshots.append({
                'time': current.isoformat(),
                'leaders': [
                    {
                        'rank': idx + 1,
                        'product': key[0],
                        'strategy': key[1],
                        'net': value
                    }
                    for idx, (key, value) in enumerate(top)
                ]
            })
            for rank, (key, value) in enumerate(top):
                freq[key] += 1
                if rank == 0:
                    rank1_freq[key] += 1
                weighted[key] += weight
                last_seen[key] = current
        current += interval
    leaders = [
        {
            'product': key[0],
            'strategy': key[1],
            'final_net': cumulative[key],
            'appearances': freq.get(key, 0),
            'rank1_appearances': rank1_freq.get(key, 0),
            'weighted_score': weighted.get(key, 0),
            'last_seen': last_seen.get(key).isoformat() if key in last_seen else None
        }
        for key in freq.keys()
    ]
    leaders.sort(key=lambda x: (x['weighted_score'], x['appearances'], x['final_net']), reverse=True)
    return snapshots, leaders


def main():
    target_date = FORCED_DATE or datetime.now().strftime('%Y-%m-%d')
    
    # [V20260131_0440] Process BOTH modes
    for run_mode in ['live', 'sim']:
        try:
            # print(f"Processing mode: {run_mode} for {target_date}")
            rows = fetch_rows(target_date, run_mode)
            trades = []
            for row in rows:
                ts = normalize_timestamp(row)
                if not ts:
                    continue
                try:
                    net_value = float(row.get(VALUE_FIELD) or 0)
                except (TypeError, ValueError):
                    continue
                raw_product = (row.get('product') or 'UNKNOWN').upper()
                model = row.get('model') or 'DNA'
                strategy_name = row.get('strategy_name') or model
                params = row.get('strategy_params') or ''

                # [V20260201] Product -> {Model}_{Product}; Strategy -> {StrategyName}_{Params}
                product = f"{model}_{raw_product}"
                strategy = f"{strategy_name}_{params}" if params else strategy_name

                trades.append((ts, net_value, (product, strategy)))
            
            if not trades:
                # print(f'No DNA trades found for {target_date} in {run_mode}')
                continue

            snapshots, leaders = build_race(trades, FREQUENCY_MINUTES)
            output = {
                'date': target_date,
                'run_mode': run_mode,
                'frequency_minutes': FREQUENCY_MINUTES,
                'snapshot_count': len(snapshots),
                'snapshots': snapshots,
                'leaders': leaders
            }

            cfg = load_layout_config(CONFIG_PATH)
            written_paths = set()
            for _, _, (product_key, _) in trades:
                raw_product = str(product_key).split('_')[-1]
                dated_root = ensure_day_dir(BASE_ROOT, run_mode, target_date, config=cfg, product=raw_product)
                dated_path = dated_root / OUTPUT_BASENAME
                path_key = str(dated_path)
                if path_key in written_paths:
                    continue
                written_paths.add(path_key)
                with dated_path.open('w') as f:
                    json.dump(output, f, indent=2)
                print(f"Wrote {len(snapshots)} snapshots for {target_date} ({run_mode}) to {dated_path}")
        except Exception as e:
           print(f"Error processing {run_mode}: {e}")


if __name__ == '__main__':
    main()
