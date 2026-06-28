from pathlib import Path
from datetime import datetime
import csv
import json

ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = ROOT / 'data' / 'ebay_live_snapshot.json'
BOARD = ROOT / 'data' / 'live_spread_board.csv'
OBS = ROOT / 'data' / 'live_spread_observations.csv'
SITE_JSON = ROOT / 'site_launch' / 'data' / 'spreads.json'
FALLBACK = ROOT / 'site_launch' / 'assets' / 'spread-data.js'


def fnum(v):
    try:
        return float(v)
    except Exception:
        return 0.0


def write_csv(path, rows, headers):
    with path.open('w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=headers)
        w.writeheader()
        w.writerows(rows)


def update_record(record, snap):
    record.update({
        'state': 'LIVE' if fnum(snap.get('gross_spread_gbp')) > 0 else 'COOLING',
        'marketplace_price': f"{fnum(snap.get('sale_guide_total_gbp')):.2f}",
        'marketplace_price_type': snap.get('sale_guide_note', ''),
        'source_price': f"{fnum(snap.get('source_total_gbp')):.2f}",
        'gross_spread_amount': f"{fnum(snap.get('gross_spread_gbp')):.2f}",
        'gross_spread_pct': f"{fnum(snap.get('gross_spread_pct')):.1f}",
        'last_checked': snap.get('captured_at', datetime.now().isoformat(timespec='seconds')),
        'source_availability': f"active auction observed; {snap.get('bids_text','')}; {snap.get('time_left_text','')}",
        'marketplace_demand_signal': 'Comparable eBay sold listing plus active auction bids/time pressure',
        'public_card_summary': f"Qualified live spread: active eBay auction current cost £{fnum(snap.get('source_total_gbp')):.2f} versus comparable sold-guide total £{fnum(snap.get('sale_guide_total_gbp')):.2f}. Gross spread £{fnum(snap.get('gross_spread_gbp')):.2f} before fees/risk.",
        'risk_notes': 'Real-time refreshed. Current auction price can rise before close. Sold guide is comparable but not identical; verify condition, accessories, seller reputation, postage, returns and eBay final price before action.',
        'hours_to_expiry': f"{fnum(snap.get('hours_to_expiry')):.2f}",
        'urgency_level': 'critical' if fnum(snap.get('hours_to_expiry')) <= 12 else 'high',
        'expiry_value_status': 'active' if fnum(snap.get('gross_spread_gbp')) > 0 else 'cooling',
        'source_kind': 'live',
        'data_quality': 'live_browser_refreshed',
        'qualified_spread': 'yes' if fnum(snap.get('gross_spread_gbp')) > 0 else 'no',
        'display_section': 'qualified_live_spreads' if fnum(snap.get('gross_spread_gbp')) > 0 else 'auction_watch',
        'internal_notes': f"Latest refresh snapshot: {SNAPSHOT}. No bid/buy/list/contact action taken.",
    })
    return record


def recalc_site(data):
    spreads = data.get('spreads', [])
    qualified = [s for s in spreads if s.get('source_kind') == 'live' and s.get('qualified_spread') == 'yes']
    demo = [s for s in spreads if not (s.get('source_kind') == 'live' and s.get('qualified_spread') == 'yes')]
    expiring = [s for s in qualified if s.get('time_sensitive') == 'yes' and fnum(s.get('hours_to_expiry')) <= 24]
    data['metrics'] = {
        **data.get('metrics', {}),
        'generated_at': datetime.now().isoformat(timespec='seconds'),
        'total_count': len(spreads),
        'qualified_live_spread_count': len(qualified),
        'qualified_live_gross_spread_value': round(sum(fnum(s.get('gross_spread_amount')) for s in qualified), 2),
        'qualified_expiring_24h_count': len(expiring),
        'qualified_expiring_24h_value': round(sum(fnum(s.get('gross_spread_amount')) for s in expiring), 2),
        'demo_example_count': len(demo),
        'active_count': len(qualified),
        'active_gross_spread_value': round(sum(fnum(s.get('gross_spread_amount')) for s in qualified), 2),
        'expiring_24h_count': len(expiring),
        'expiring_24h_value': round(sum(fnum(s.get('gross_spread_amount')) for s in expiring), 2),
    }
    return data


def main():
    snap = json.loads(SNAPSHOT.read_text(encoding='utf-8'))
    if snap.get('source_total_gbp') is None:
        raise SystemExit('Snapshot missing source_total_gbp; not applying update')

    with BOARD.open(encoding='utf-8', newline='') as f:
        rows = list(csv.DictReader(f))
        headers = list(rows[0].keys())
    for h in ['source_kind', 'data_quality', 'qualified_spread', 'display_section']:
        if h not in headers:
            headers.append(h)
    found = False
    for row in rows:
        if row.get('spread_id') == snap['spread_id']:
            update_record(row, snap)
            found = True
    if not found:
        raise SystemExit(f"Spread {snap['spread_id']} not found in board CSV")
    write_csv(BOARD, rows, headers)

    data = json.loads(SITE_JSON.read_text(encoding='utf-8'))
    for row in data.get('spreads', []):
        if row.get('spread_id') == snap['spread_id']:
            update_record(row, snap)
            found = True
    data = recalc_site(data)
    SITE_JSON.write_text(json.dumps(data, indent=2), encoding='utf-8')
    FALLBACK.write_text('window.EP038_SPREAD_DATA = ' + json.dumps(data, ensure_ascii=False) + ';\n', encoding='utf-8')

    obs_headers = ['observation_id', 'observed_at', 'spread_id', 'item_name', 'source_total_gbp', 'sale_guide_total_gbp', 'gross_spread_gbp', 'gross_spread_pct', 'time_left_text', 'bids_text', 'snapshot_path']
    write_header = not OBS.exists()
    with OBS.open('a', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=obs_headers)
        if write_header:
            w.writeheader()
        w.writerow({
            'observation_id': 'OBS-EBAY-REFRESH-' + datetime.now().strftime('%Y%m%d%H%M%S'),
            'observed_at': datetime.now().isoformat(timespec='seconds'),
            'spread_id': snap['spread_id'],
            'item_name': snap['item_name'],
            'source_total_gbp': f"{fnum(snap.get('source_total_gbp')):.2f}",
            'sale_guide_total_gbp': f"{fnum(snap.get('sale_guide_total_gbp')):.2f}",
            'gross_spread_gbp': f"{fnum(snap.get('gross_spread_gbp')):.2f}",
            'gross_spread_pct': f"{fnum(snap.get('gross_spread_pct')):.1f}",
            'time_left_text': snap.get('time_left_text', ''),
            'bids_text': snap.get('bids_text', ''),
            'snapshot_path': str(SNAPSHOT),
        })

    print(json.dumps({
        'updated': snap['spread_id'],
        'source_total_gbp': fnum(snap.get('source_total_gbp')),
        'sale_guide_total_gbp': fnum(snap.get('sale_guide_total_gbp')),
        'gross_spread_gbp': fnum(snap.get('gross_spread_gbp')),
        'gross_spread_pct': fnum(snap.get('gross_spread_pct')),
        'qualified_live_spread_count': data['metrics']['qualified_live_spread_count'],
        'qualified_live_gross_spread_value': data['metrics']['qualified_live_gross_spread_value'],
    }, indent=2))


if __name__ == '__main__':
    main()
