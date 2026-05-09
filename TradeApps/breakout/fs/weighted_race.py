import json
import os
import re
import time
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict
from json_layout import iter_day_dirs, load_layout_config

CONFIG_PATH = Path(__file__).resolve().parent / 'config.json'
BASE_ROOT = Path(r"C:\Users\edebe\eds\TradeApps\breakout\fs\json")
FREQUENCY_MINUTES = 5
FORCED_DATE = os.environ.get('FREQUENCY_TARGET_DATE')


def detect_latest_date(base_dir: Path) -> str:
    if not base_dir.exists():
        raise SystemExit(f'No data directory: {base_dir}')
    candidates = []
    for child in base_dir.iterdir():
        if not child.is_dir():
            continue
        try:
            datetime.strptime(child.name, '%Y-%m-%d')
            candidates.append(child.name)
        except ValueError:
            continue
    if not candidates:
        raise SystemExit(f'No dated folders found under {base_dir}')
    return sorted(candidates)[-1]


def load_trades(base_dir: Path):
    trades = []
    for path in base_dir.glob('*.json'):
        if path.name == '_summary_net.json':
            continue
        try:
            with path.open('r') as f:
                data = json.load(f)
        except Exception:
            continue
        # [V20260305_2330] Skip non-dict payloads (e.g. array-based files)
        if not isinstance(data, dict):
            continue
        # [V20260203_0130] Fix: Only process closed trades (history stability)
        timestamp = data.get('exit_time')
        if not timestamp:
            continue
        try:
            ts = datetime.fromisoformat(timestamp)
        except ValueError:
            continue
        net = data.get('net_return')
        try:
            net = float(net)
        except (TypeError, ValueError):
            continue
        product = data.get('product')
        if not product:
            m = re.search(r'_[0-9a-f]{8}_(.+?)_\d{8}_', path.name)
            product = m.group(1) if m else 'UNKNOWN'
        strategy = data.get('script_name') or data.get('app_name') or data.get('source_strategy') or 'UNKNOWN'
        trades.append((ts, net, (product, strategy)))
    return trades


def _best_per_product(cumulative):
    """[V20260420] Return one (key, net) per product — highest net strategy wins.
    Prevents all 5 leaders being sl-variants of the same strategy on the same product."""
    best = {}
    for key, value in sorted(cumulative.items(), key=lambda kv: kv[1], reverse=True):
        product = key[0]
        if product not in best:
            best[product] = (key, value)
    return sorted(best.values(), key=lambda kv: kv[1], reverse=True)[:5]


def build_race(trades, interval_minutes):
    trades.sort(key=lambda x: x[0])
    if not trades:
        return [], []
    interval = timedelta(minutes=interval_minutes)
    start_time = trades[0][0]
    end_time = max(trades[-1][0], datetime.now())
    minute = (start_time.minute // interval_minutes) * interval_minutes
    start_floor = start_time.replace(minute=minute, second=0, microsecond=0)
    if start_floor > start_time:
        start_floor -= interval
    buckets = []
    current = start_floor
    while current <= end_time:
        buckets.append(current)
        current += interval
    cumulative = defaultdict(float)
    freq = defaultdict(int)
    rank1_freq = defaultdict(int)
    best_rank_map = {} # [V20260203_0200] Track best rank
    weighted = defaultdict(float)
    last_seen = {}
    snapshots = []
    trade_idx = 0
    for idx, bucket_time in enumerate(buckets):
        while trade_idx < len(trades) and trades[trade_idx][0] <= bucket_time:
            ts, net, key = trades[trade_idx]
            cumulative[key] += net
            trade_idx += 1
        if not cumulative:
            continue
        # [V20260420] Deduplicate: one best strategy per product to avoid all-same-product top-5
        top = _best_per_product(cumulative)
        weight = idx + 1
        # [V20260203_1200] Update weights FIRST to capture current state
        for rank, (key, value) in enumerate(top):
            current_rank = rank + 1
            freq[key] += 1
            if rank == 0:
                rank1_freq[key] += 1

            if key not in best_rank_map or current_rank < best_rank_map[key]:
                best_rank_map[key] = current_rank

            weighted[key] += weight
            last_seen[key] = bucket_time

        # [V20260203_1200] Calculate Score Ranks based on current weighted scores
        score_ladder = sorted(weighted.items(), key=lambda x: x[1], reverse=True)
        score_ranks = {k: i+1 for i, (k, v) in enumerate(score_ladder)}

        snapshots.append({
            'time': bucket_time.isoformat(),
            'leaders': [
                {
                    'rank': rank + 1,
                    'score_rank': score_ranks.get(key),
                    'score': weighted.get(key),
                    'product': key[0],
                    'strategy': key[1],
                    'net': value
                }
                for rank, (key, value) in enumerate(top)
            ]
        })
    summary = [
        {
            'product': key[0],
            'strategy': key[1],
            'final_net': cumulative[key],
            'appearances': freq.get(key, 0),
            'rank1_appearances': rank1_freq.get(key, 0),
            'best_rank': best_rank_map.get(key, 999), # [V20260203_0200]
            'weighted_score': weighted.get(key, 0),
            'last_seen': last_seen.get(key).isoformat() if key in last_seen else None
        }
        for key in freq.keys()
    ]
    summary.sort(key=lambda x: (x['weighted_score'], x['appearances'], x['final_net']), reverse=True)
    return snapshots, summary


def run_race(run_mode):
    # [V20260323_1700] Restrict frequency by product_type/directory
    mode_root = BASE_ROOT / run_mode
    if not mode_root.exists():
        return

    target_date = datetime.now().strftime('%Y-%m-%d')
    cfg = load_layout_config(CONFIG_PATH)
    day_dirs = iter_day_dirs(BASE_ROOT, run_mode, target_date, config=cfg)
    if not day_dirs:
        return

    # [V20260420] Snapshots older than this are sealed — never overwritten
    SEAL_MINUTES = 10
    seal_cutoff = datetime.now() - timedelta(minutes=SEAL_MINUTES)

    for base_dir in day_dirs:
        # Extract product_type from path (e.g., .../json/live/forex/2026-03-24)
        product_type = base_dir.parent.name

        trades = load_trades(base_dir)
        if not trades:
            continue

        dated_output = base_dir / '_frequency.json'

        # [V20260420] Load existing sealed snapshots (immutable historical record)
        sealed_snaps = []
        if dated_output.exists():
            try:
                with dated_output.open('r') as f:
                    existing = json.load(f)
                for s in existing.get('snapshots', []):
                    try:
                        snap_dt = datetime.fromisoformat(s['time'])
                        if snap_dt <= seal_cutoff:
                            sealed_snaps.append(s)
                    except (ValueError, KeyError):
                        pass
            except Exception:
                pass

        new_snapshots, summary = build_race(trades, FREQUENCY_MINUTES)

        # [V20260420] Merge: sealed snapshots are immutable; only update recent buckets
        sealed_times = {s['time'] for s in sealed_snaps}
        final_snapshots = list(sealed_snaps)  # start with immutable history
        for s in new_snapshots:
            if s['time'] not in sealed_times:
                final_snapshots.append(s)  # append new/recent buckets only
        final_snapshots.sort(key=lambda s: s['time'])

        output = {
            'date': target_date,
            'run_mode': run_mode,
            'product_type': product_type,
            'frequency_minutes': FREQUENCY_MINUTES,
            'snapshot_count': len(final_snapshots),
            'snapshots': final_snapshots,
            'leaders': summary
        }

        try:
            tmp = dated_output.with_suffix('.tmp')
            with tmp.open('w') as f:
                json.dump(output, f, indent=2)
            tmp.replace(dated_output)
            print(f'[{datetime.now().isoformat()}] {len(final_snapshots)} snaps ({len(sealed_snaps)} sealed + {len(final_snapshots)-len(sealed_snaps)} fresh) for {target_date} ({run_mode}/{product_type})')
        except Exception as e:
            print(f"Error saving frequency json to {dated_output}: {e}")



def main():
    print(f"[{datetime.now().isoformat()}] Starting Dual-Mode Weighted Race...")
    while True:
        try:
            for mode in ['live', 'sim']:
                run_race(mode)
        except Exception as e:
            print(f"Global Loop Error: {e}")
        
        time.sleep(60)  # [V20260420] 60s — sealed snapshots make frequent rewrites unnecessary


if __name__ == '__main__':
    main()
