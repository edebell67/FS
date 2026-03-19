import argparse, json, os, glob
from datetime import datetime, timezone


def load_json(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return None


def as_list(obj):
    if obj is None:
        return []
    if isinstance(obj, list):
        return obj
    if isinstance(obj, dict):
        out = []
        for v in obj.values():
            if isinstance(v, list):
                out.extend(v)
            else:
                out.append(v)
        return out
    return [obj]


def pick(d, *keys, default=None):
    if not isinstance(d, dict):
        return default
    for k in keys:
        if k in d and d[k] is not None:
            return d[k]
    return default


def build_feed(day_dir):
    p_summary = os.path.join(day_dir, '_summary_net.json')
    p_buckets = os.path.join(day_dir, '_trade_buckets.json')
    p_live = os.path.join(day_dir, '_live_trades.json')
    p_top20 = os.path.join(day_dir, '_top20.json')
    p_top1 = os.path.join(day_dir, '_top_one.json')

    summary = load_json(p_summary)
    buckets = load_json(p_buckets)
    live = load_json(p_live)
    top20 = load_json(p_top20)
    top1 = load_json(p_top1)

    strategies = []

    # Top20-driven strategy snapshots
    for row in as_list(top20):
        if not isinstance(row, dict):
            continue
        strategy = pick(row, 'strategy', 'source_strategy', 'strategy_name', default='unknown')
        pair = pick(row, 'pair', 'symbol', 'instrument', default='unknown')
        strategies.append({
            'strategy_id': f"{strategy}:{pair}",
            'strategy_name': strategy,
            'pair': pair,
            'net_today': pick(row, 'net', 'net_today', 'pnl', default=0),
            'win_rate': pick(row, 'win_rate', 'wr', default=None),
            'drawdown': pick(row, 'drawdown', 'dd', default=None),
            'confidence': pick(row, 'confidence', default=None),
            'source': 'top20'
        })

    # Top one highlight
    top_one_entries = as_list(top1)
    top_one_highlight = None
    if top_one_entries:
        t = top_one_entries[0] if isinstance(top_one_entries[0], dict) else {}
        top_one_highlight = {
            'strategy': pick(t, 'strategy', 'source_strategy', 'strategy_name', default='unknown'),
            'pair': pick(t, 'pair', 'symbol', 'instrument', default='unknown'),
            'net_today': pick(t, 'net', 'net_today', 'pnl', default=0)
        }

    # Open trades
    open_trades = []
    for row in as_list(live):
        if not isinstance(row, dict):
            continue
        status = str(pick(row, 'status', default='open')).lower()
        if status not in ('open', 'running', 'active') and 'close' in status:
            continue
        strategy = pick(row, 'strategy', 'source_strategy', 'strategy_name', default='unknown')
        pair = pick(row, 'pair', 'symbol', 'instrument', default='unknown')
        open_trades.append({
            'trade_id': str(pick(row, 'trade_id', 'id', default=f"{strategy}:{pair}")),
            'strategy_id': strategy,
            'pair': pair,
            'side': pick(row, 'side', 'direction', default='n/a'),
            'entry': pick(row, 'entry', 'entry_price', default=None),
            'sl': pick(row, 'sl', 'stop_loss', default=None),
            'tp': pick(row, 'tp', 'take_profit', default=None),
            'unrealized_pnl': pick(row, 'pnl', 'unrealized_pnl', default=None),
            'status': status
        })

    # Signals from trade buckets (best-effort)
    signals = []
    for row in as_list(buckets):
        if not isinstance(row, dict):
            continue
        strategy = pick(row, 'strategy', 'source_strategy', 'strategy_name', default='unknown')
        pair = pick(row, 'pair', 'symbol', 'instrument', default='unknown')
        signals.append({
            'signal_id': str(pick(row, 'id', 'signal_id', default=f"{strategy}:{pair}")),
            'strategy_id': strategy,
            'pair': pair,
            'bias': pick(row, 'bias', 'side', 'direction', default='n/a'),
            'trigger_text': pick(row, 'trigger', 'trigger_text', default='See strategy conditions'),
            'invalidation_text': pick(row, 'invalidation', 'invalidation_text', default='Invalidation not supplied'),
            'risk_note': pick(row, 'risk_note', default='Use position sizing and stops'),
            'confidence': pick(row, 'confidence', default=None)
        })

    feed = {
        'meta': {
            'generated_at_utc': datetime.now(timezone.utc).isoformat(),
            'source_day_dir': day_dir,
            'counts': {
                'strategies': len(strategies),
                'open_trades': len(open_trades),
                'signals': len(signals)
            }
        },
        'top_one': top_one_highlight,
        'strategies': strategies[:50],
        'open_trades': open_trades[:100],
        'signals': signals[:100]
    }
    return feed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--day-dir', required=True)
    ap.add_argument('--out', default=None)
    args = ap.parse_args()

    out = args.out or os.path.join(args.day_dir, 'miniapp_feed.json')
    feed = build_feed(args.day_dir)
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(feed, f, indent=2)
    print(out)
    print(json.dumps(feed['meta']['counts']))


if __name__ == '__main__':
    main()
