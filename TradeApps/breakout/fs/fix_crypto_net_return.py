"""
fix_crypto_net_return.py - Recalculate net_return for crypto .cld files

Fixes incorrect net_return and alt_net values caused by using wrong pip_multiplier
before V20260316_1430 fix.

Usage:
    python fix_crypto_net_return.py [--date YYYY-MM-DD] [--dry-run]

Arguments:
    --date      Target date folder (default: today)
    --dry-run   Preview changes without writing (default: False)
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional, Tuple

# Configuration
CONFIG_PATH = Path(__file__).parent / "config.json"
JSON_BASE_DIR = Path(__file__).parent / "json"

def load_config() -> Dict[str, Any]:
    """Load config.json"""
    with open(CONFIG_PATH, 'r') as f:
        return json.load(f)

def get_pip_multiplier(product: str, config: Dict[str, Any]) -> float:
    """Hierarchical lookup for product pip multiplier."""
    product_key = str(product or '').strip().upper()

    # 1. Check direct product match
    by_product = config.get('pip_multiplier_by_product', {})
    if isinstance(by_product, dict) and product_key:
        val = by_product.get(product_key)
        if val is not None:
            return float(val)

    # 2. Check product type match
    product_type_map = config.get('product_type_by_product', {})
    product_type = product_type_map.get(product_key, 'forex')
    by_type = config.get('pip_multiplier_by_product_type', {})
    if isinstance(by_type, dict):
        val = by_type.get(str(product_type).lower())
        if val is not None:
            return float(val)

    # 3. Default fallback
    return 10000.0

def calculate_pnl(entry_price: float, exit_price: float, direction: str,
                  multiplier: float, config: Dict[str, Any]) -> Dict[str, float]:
    """Calculate PnL metrics using correct multiplier."""
    pip_value = float(config.get('pip_value', 10.0))
    commission_usd = float(config.get('commission_usd', 10.0))
    spread_pips = float(config.get('spread_pips', 2.0))

    if (direction or '').upper() == 'LONG':
        gross_pips = (exit_price - entry_price) * multiplier
    else:
        gross_pips = (entry_price - exit_price) * multiplier

    gross_usd = gross_pips * pip_value
    net_usd = gross_usd - commission_usd

    # Alt PnL (reversal logic)
    alt_gross_pips = -gross_pips
    alt_gross_usd = alt_gross_pips * pip_value
    spread_cost_usd = spread_pips * pip_value
    alt_net_usd = alt_gross_usd - commission_usd - spread_cost_usd

    return {
        'gross_pnl_pips': gross_pips,
        'net_return': net_usd,
        'alt_net': alt_net_usd
    }

def process_cld_file(file_path: Path, config: Dict[str, Any], dry_run: bool = True) -> Tuple[bool, str]:
    """Process a single .cld file and fix net_return if needed."""
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)

        # Extract required fields
        product = data.get('product', '')
        entry_price = data.get('entry_price')
        exit_price = data.get('exit_price')
        direction = data.get('direction', '')
        status = data.get('status', '')

        # Skip if not closed or missing prices
        if status != 'CLOSED' or entry_price is None or exit_price is None:
            return False, "skipped (not closed or missing prices)"

        # Get correct multiplier
        multiplier = get_pip_multiplier(product, config)

        # Calculate correct values
        pnl = calculate_pnl(entry_price, exit_price, direction, multiplier, config)

        # Get current values
        old_gross = data.get('gross_pnl_pips', 0.0)
        old_net = data.get('net_return', 0.0)
        old_alt = data.get('alt_net', 0.0)

        # Check if values differ significantly (tolerance for float comparison)
        tolerance = 0.01
        gross_diff = abs(pnl['gross_pnl_pips'] - old_gross) > tolerance
        net_diff = abs(pnl['net_return'] - old_net) > tolerance
        alt_diff = abs(pnl['alt_net'] - old_alt) > tolerance

        if not (gross_diff or net_diff or alt_diff):
            return False, "no change needed"

        # Update values
        data['gross_pnl_pips'] = pnl['gross_pnl_pips']
        data['net_return'] = pnl['net_return']
        data['alt_net'] = pnl['alt_net']

        change_msg = (f"FIXED: {product} | multiplier={multiplier} | "
                      f"gross: {old_gross:.2f} -> {pnl['gross_pnl_pips']:.2f} | "
                      f"net: {old_net:.2f} -> {pnl['net_return']:.2f} | "
                      f"alt: {old_alt:.2f} -> {pnl['alt_net']:.2f}")

        if not dry_run:
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2)

        return True, change_msg

    except Exception as e:
        return False, f"ERROR: {str(e)}"

def find_crypto_cld_files(date_str: str) -> list:
    """Find all crypto .cld files for a given date."""
    files = []

    for mode in ['live', 'sim']:
        crypto_dir = JSON_BASE_DIR / mode / 'crypto' / date_str
        if crypto_dir.exists():
            # Main directory
            files.extend(crypto_dir.glob('*_cld.json'))
            # Archive subdirectories
            archive_dir = crypto_dir / 'archive'
            if archive_dir.exists():
                for subdir in archive_dir.iterdir():
                    if subdir.is_dir():
                        files.extend(subdir.glob('*_cld.json'))

    return files

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Fix crypto net_return values')
    parser.add_argument('--date', default=datetime.now().strftime('%Y-%m-%d'),
                        help='Target date (YYYY-MM-DD)')
    parser.add_argument('--dry-run', action='store_true', default=False,
                        help='Preview changes without writing')
    args = parser.parse_args()

    print(f"=== Crypto net_return Fix Script ===")
    print(f"Date: {args.date}")
    print(f"Mode: {'DRY-RUN' if args.dry_run else 'LIVE (will modify files)'}")
    print()

    # Load config
    config = load_config()
    print(f"Loaded config from: {CONFIG_PATH}")
    print(f"Multipliers: BTC={get_pip_multiplier('BTC', config)}, "
          f"ETH={get_pip_multiplier('ETH', config)}, "
          f"SOL={get_pip_multiplier('SOL', config)}, "
          f"XRP={get_pip_multiplier('XRP', config)}")
    print()

    # Find files
    files = find_crypto_cld_files(args.date)
    print(f"Found {len(files)} crypto .cld files for {args.date}")
    print()

    # Process files
    fixed_count = 0
    skipped_count = 0
    error_count = 0

    for file_path in files:
        changed, msg = process_cld_file(file_path, config, args.dry_run)
        if changed:
            fixed_count += 1
            print(f"  {file_path.name}: {msg}")
        elif "ERROR" in msg:
            error_count += 1
            print(f"  {file_path.name}: {msg}")
        else:
            skipped_count += 1

    print()
    print(f"=== Summary ===")
    print(f"Total files: {len(files)}")
    print(f"Fixed: {fixed_count}")
    print(f"Skipped (no change): {skipped_count}")
    print(f"Errors: {error_count}")

    if args.dry_run and fixed_count > 0:
        print()
        print("Run without --dry-run to apply changes.")

if __name__ == "__main__":
    main()
