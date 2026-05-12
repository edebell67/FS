"""
[V20260415_1500] Backfill GUID from filename to JSON content.

This script extracts the 8-character GUID embedded in trade filenames
and adds it to the JSON content if missing.

Filename pattern: {strategy}_{guid}_{product}_{timestamp}_{params}_{status}.json
Example: breakout_R_2_tp5.0_sl30.0_1ef997d4_GBPEUR_S_20260415_060945_2_0.00015_5.0_30.0_op.json
                                  ^^^^^^^^ GUID here
"""

import json
import re
import os
from pathlib import Path
from datetime import datetime
from paths import BREAKOUT_JSON_ROOT

# Base directory for forex trades
BASE_DIR = BREAKOUT_JSON_ROOT / "live" / "forex"

# Regex to find 8-character hex GUID in filename
GUID_PATTERN = re.compile(r'_([a-f0-9]{8})_')

def extract_guid_from_filename(filename: str) -> str | None:
    """Extract the 8-char hex GUID from a trade filename."""
    match = GUID_PATTERN.search(filename)
    if match:
        return match.group(1)
    return None

def backfill_directory(date_dir: Path, dry_run: bool = False) -> dict:
    """Backfill all JSON files in a date directory."""
    stats = {'scanned': 0, 'updated': 0, 'skipped': 0, 'errors': 0}

    for json_file in date_dir.glob("*.json"):
        # Skip metadata files
        if json_file.name.startswith("_"):
            continue

        stats['scanned'] += 1

        try:
            # Extract GUID from filename
            guid = extract_guid_from_filename(json_file.name)
            if not guid:
                stats['skipped'] += 1
                continue

            # Read JSON content
            with open(json_file, 'r') as f:
                data = json.load(f)

            # Check if GUID already exists
            if data.get('guid'):
                stats['skipped'] += 1
                continue

            # Add GUID to data
            data['guid'] = guid

            if dry_run:
                print(f"[DRY-RUN] Would update {json_file.name} with guid={guid}")
            else:
                # Write updated JSON
                with open(json_file, 'w') as f:
                    json.dump(data, f, indent=2)
                print(f"[UPDATED] {json_file.name} -> guid={guid}")

            stats['updated'] += 1

        except Exception as e:
            print(f"[ERROR] {json_file.name}: {e}")
            stats['errors'] += 1

    return stats

def main(dry_run: bool = False, date_filter: str = None):
    """Main backfill function."""
    print(f"[{datetime.now()}] Starting GUID backfill (dry_run={dry_run})")
    print(f"Base directory: {BASE_DIR}")

    total_stats = {'scanned': 0, 'updated': 0, 'skipped': 0, 'errors': 0}

    # Find all date directories
    for date_dir in sorted(BASE_DIR.iterdir()):
        if not date_dir.is_dir():
            continue
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', date_dir.name):
            continue
        if date_filter and not date_dir.name.startswith(date_filter):
            continue

        print(f"\n[PROCESSING] {date_dir.name}")
        stats = backfill_directory(date_dir, dry_run)

        for key in total_stats:
            total_stats[key] += stats[key]

        print(f"  Scanned: {stats['scanned']}, Updated: {stats['updated']}, Skipped: {stats['skipped']}, Errors: {stats['errors']}")

    print(f"\n[{datetime.now()}] Backfill complete")
    print(f"Total - Scanned: {total_stats['scanned']}, Updated: {total_stats['updated']}, Skipped: {total_stats['skipped']}, Errors: {total_stats['errors']}")

    return total_stats

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Backfill GUID from filename to JSON")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without writing")
    parser.add_argument("--date", type=str, help="Filter by date prefix (e.g., '2026-04')")
    args = parser.parse_args()

    main(dry_run=args.dry_run, date_filter=args.date)
