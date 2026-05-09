import json
import re
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict
import argparse

BASE_ROOT = Path(r"C:\Users\edebe\eds\TradeApps\breakout\fs\json\live")

# Determine default date: prefer newest YYYY-MM-DD directory, fallback to today

def detect_default_date():
    candidates = []
    for child in BASE_ROOT.iterdir():
        if not child.is_dir():
            continue
        name = child.name
        try:
            datetime.strptime(name, '%Y-%m-%d')
            candidates.append(name)
        except ValueError:
            continue
    if candidates:
        return sorted(candidates)[-1]
    return datetime.now().strftime('%Y-%m-%d')

def load_trades(base_dir):
    trades = []
    for path in base_dir.glob('*.json'):
        if path.name == '_summary_net.json':
            continue
        try:
            with path.open('r') as f:
                data = json.load(f)
        except Exception:
            continue
        timestamp = data.get('exit_time') or data.get('entry_time')
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

def build_race(trades, interval_minutes):
    trades.sort(key=lambda x: x[0])
    if not trades:
        return [], []
    interval = timedelta(minutes=interval_minutes)
    start_time = trades[0][0]
    end_time = trades[-1][0]
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
        top = sorted(cumulative.items(), key=lambda kv: kv[1], reverse=True)[:5]
        weight = idx + 1
        snapshots.append({
            'time': bucket_time.isoformat(),
            'leaders': [
                {
                    'rank': rank + 1,
                    'product': key[0],
                    'strategy': key[1],
                    'net': value
                }
                for rank, (key, value) in enumerate(top)
            ]
        })
        for rank, (key, value) in enumerate(top):
            freq[key] += 1
            if rank == 0:
                rank1_freq[key] += 1
            weighted[key] += weight
            last_seen[key] = bucket_time
    summary = []
    for key, count in freq.items():
        summary.append({
            'product': key[0],
            'strategy': key[1],
            'final_net': cumulative[key],
            'appearances': count,
            'rank1_appearances': rank1_freq.get(key, 0),
            'weighted_score': weighted[key],
            'last_seen': last_seen[key].isoformat() if key in last_seen else None
        })
    summary.sort(key=lambda x: (x['weighted_score'], x['appearances'], x['final_net']), reverse=True)
    return snapshots, summary

def main():
    parser = argparse.ArgumentParser(description='Build weighted race snapshots for a trading day.')
    parser.add_argument('date', nargs='?', default=None, help='Trading date (YYYY-MM-DD); defaults to latest folder')
    parser.add_argument('--freq', type=int, default=5, help='Snapshot frequency in minutes (default 5)')
    args = parser.parse_args()

    date = args.date or detect_default_date()
    base_dir = BASE_ROOT / date
    if not base_dir.exists():
        raise SystemExit(f'Directory not found: {base_dir}')

    trades = load_trades(base_dir)
    if not trades:
        raise SystemExit(f'No trades found for {date}')

    snapshots, summary = build_race(trades, args.freq)

    output = {
        'date': date,
        'frequency_minutes': args.freq,
        'snapshot_count': len(snapshots),
        'snapshots': snapshots,
        'leaders': summary
    }

    out_path = Path(r"C:\Users\edebe\eds\TradeApps\breakout\fs") / '_frequency.json'
    with out_path.open('w') as f:
        json.dump(output, f, indent=2)

    print(f'Wrote {len(snapshots)} snapshots for {date} to {out_path}')

if __name__ == '__main__':
    main()
