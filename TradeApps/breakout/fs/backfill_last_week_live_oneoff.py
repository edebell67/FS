from __future__ import annotations
import os
from pathlib import Path
from datetime import date, timedelta, datetime
from dotenv import load_dotenv

load_dotenv(Path(r"C:/Users/edebe/eds/TradeApps/breakout/DB/.env"), override=True)

import backfill_trades as bf

TODAY = date(2026, 2, 28)
TARGET_DATES = sorted([(TODAY - timedelta(days=i)).isoformat() for i in range(7)])
MODE = "live"
MODE_ROOT = Path(bf.JSON_BASE_DIR) / MODE


def iter_files():
    for d in TARGET_DATES:
        day = MODE_ROOT / d
        if not day.exists():
            continue
        for fp in day.rglob("*.json"):
            rel = fp.parent.relative_to(day)
            source_path = "" if str(rel) == "." else str(rel)
            yield str(fp), MODE, d, source_path


def main() -> int:
    print(f"START oneoff backfill mode={MODE} dates={TARGET_DATES} at={datetime.now().isoformat()}")
    conn = bf.get_db_connection()
    if not conn:
        print("ERROR db_connection_failed")
        return 2

    print("DISCOVERED streaming file scan started")

    success = 0
    skipped = 0
    with conn.cursor() as cursor:
        success += bf.process_grid_history(cursor, os.path.join(bf.JSON_BASE_DIR, "grid_live_history.json"))
        success += bf.process_grid_latest(cursor, os.path.join(bf.ROOT_FS_DIR, "grid_live.json"))
        conn.commit()

        processed = 0
        for i, (file_path, run_mode, date_str, source_path) in enumerate(iter_files(), 1):
            name = os.path.basename(file_path)
            try:
                if name.startswith("_"):
                    s, k = bf.process_summary_file(cursor, file_path, run_mode, date_str)
                else:
                    s, k = bf.process_trade_file(cursor, file_path, run_mode, source_path)
                success += s
                skipped += k
                if i % 1000 == 0:
                    conn.commit()
                    print(f"PROGRESS processed={i} success={success} skipped={skipped}")
            except Exception as exc:
                conn.rollback()
                skipped += 1
                print(f"ERROR file={file_path} err={exc}")
            processed = i

        conn.commit()

    conn.close()
    print(f"DONE processed={processed} success={success} skipped={skipped} at={datetime.now().isoformat()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
