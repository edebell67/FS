from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any, Dict, Tuple

from strategy_name_generator import apply_strategy_name_fields


BASE_DIR = Path(__file__).resolve().parent / "json"
MODES = ("live", "sim")
PRODUCT_TYPE_DIRS = ("forex", "crypto", "indices", "metals", "energy")
TRADE_HINT_TOKENS = ('"trade_id"', '"entry_time"', '"status"')
STRATEGY_HINT_TOKENS = ('"strategy_name"', '"source_strategy"', '"script_name"', '"app_name"')


def _looks_like_trade_record(data: Any) -> bool:
    return (
        isinstance(data, dict)
        and bool(data.get("product"))
        and any(data.get(key) for key in ("strategy_name", "source_strategy", "script_name", "app_name"))
        and any(key in data for key in ("trade_id", "entry_time", "status"))
    )


def _process_payload(payload: Any) -> Tuple[bool, int, int]:
    changed = False
    updated = 0
    skipped = 0

    if isinstance(payload, dict) and isinstance(payload.get("trades"), list):
        for item in payload["trades"]:
            if _looks_like_trade_record(item):
                if apply_strategy_name_fields(item):
                    changed = True
                    updated += 1
                else:
                    skipped += 1
            else:
                skipped += 1
        return changed, updated, skipped

    if _looks_like_trade_record(payload):
        updated_flag = apply_strategy_name_fields(payload)
        return updated_flag, int(updated_flag), int(not updated_flag)

    return False, 0, 1


def _iter_json_files(root: Path, dates: set[str] | None, product_types: set[str] | None):
    if not dates:
        if not product_types:
            for dirpath, _, filenames in os.walk(root):
                for filename in filenames:
                    if filename.lower().endswith(".json"):
                        yield Path(dirpath) / filename
            return
        for product_name in product_types:
            product_dir = root / product_name
            if not product_dir.exists():
                continue
            for dirpath, _, filenames in os.walk(product_dir):
                for filename in filenames:
                    if filename.lower().endswith(".json"):
                        yield Path(dirpath) / filename
        return

    seen: set[Path] = set()
    for date in dates:
        direct = root / date
        if direct.exists() and not product_types:
            for path in direct.rglob("*.json"):
                if path not in seen:
                    seen.add(path)
                    yield path

        for product_name in (product_types or set(PRODUCT_TYPE_DIRS)):
            product_dir = root / product_name
            if not product_dir.exists():
                continue
            candidate = product_dir / date
            if not candidate.exists():
                continue
            for dirpath, _, filenames in os.walk(candidate):
                for filename in filenames:
                    if not filename.lower().endswith(".json"):
                        continue
                    path = Path(dirpath) / filename
                    if path not in seen:
                        seen.add(path)
                        yield path
        
        if direct.exists() and not product_types:
            continue


def backfill_mode(
    mode: str,
    dry_run: bool = False,
    dates: set[str] | None = None,
    product_types: set[str] | None = None,
) -> Dict[str, int]:
    root = BASE_DIR / mode
    stats = {
        "files_scanned": 0,
        "files_updated": 0,
        "records_updated": 0,
        "files_skipped": 0,
        "files_failed": 0,
        "records_skipped": 0,
    }
    if not root.exists():
        return stats

    for index, path in enumerate(_iter_json_files(root, dates, product_types), start=1):
        stats["files_scanned"] += 1
        try:
            raw_text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            try:
                raw_text = path.read_text(encoding="utf-8-sig")
            except Exception:
                stats["files_failed"] += 1
                continue
        except Exception:
            stats["files_failed"] += 1
            continue

        if index % 5000 == 0:
            print(
                f"[{mode}] progress scanned={stats['files_scanned']} "
                f"updated_files={stats['files_updated']} failed_files={stats['files_failed']}"
            )

        if not any(token in raw_text for token in TRADE_HINT_TOKENS):
            stats["files_skipped"] += 1
            continue
        if not any(token in raw_text for token in STRATEGY_HINT_TOKENS):
            stats["files_skipped"] += 1
            continue
        if '"gen_strategy_name"' in raw_text and '"strategy_name"' in raw_text:
            stats["files_skipped"] += 1
            continue

        try:
            payload = json.loads(raw_text)
        except Exception:
            stats["files_failed"] += 1
            continue

        changed, updated, skipped = _process_payload(payload)
        stats["records_updated"] += updated
        stats["records_skipped"] += skipped

        if changed:
            stats["files_updated"] += 1
            if not dry_run:
                path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        else:
            stats["files_skipped"] += 1

    return stats


def main() -> int:
    parser = argparse.ArgumentParser(description="Backfill strategy_name and gen_strategy_name into trade JSON files.")
    parser.add_argument("--mode", choices=("live", "sim", "all"), default="all")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--date", action="append", help="Limit processing to one or more YYYY-MM-DD folders.")
    parser.add_argument(
        "--product-type",
        action="append",
        choices=PRODUCT_TYPE_DIRS,
        help="Limit processing to one or more product-type folders.",
    )
    args = parser.parse_args()

    modes = MODES if args.mode == "all" else (args.mode,)
    target_dates = {item.strip() for item in (args.date or []) if item and item.strip()}
    target_product_types = {item.strip() for item in (args.product_type or []) if item and item.strip()}
    grand = {
        "files_scanned": 0,
        "files_updated": 0,
        "records_updated": 0,
        "files_skipped": 0,
        "files_failed": 0,
        "records_skipped": 0,
    }

    for mode in modes:
        stats = backfill_mode(
            mode,
            dry_run=args.dry_run,
            dates=target_dates or None,
            product_types=target_product_types or None,
        )
        for key, value in stats.items():
            grand[key] += value
        print(
            f"[{mode}] scanned={stats['files_scanned']} updated_files={stats['files_updated']} "
            f"updated_records={stats['records_updated']} skipped_files={stats['files_skipped']} "
            f"failed_files={stats['files_failed']} skipped_records={stats['records_skipped']}"
        )

    print(
        f"[total] scanned={grand['files_scanned']} updated_files={grand['files_updated']} "
        f"updated_records={grand['records_updated']} skipped_files={grand['files_skipped']} "
        f"failed_files={grand['files_failed']} skipped_records={grand['records_skipped']}"
    )
    return 0 if grand["files_failed"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
