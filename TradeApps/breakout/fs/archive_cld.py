"""
Auto-archive FS closed trade JSON files when count exceeds threshold.

Usage:
    python archive_cld.py          # Run continuously (polls every 60 seconds)
    python archive_cld.py --once   # Run once and exit
"""

import json
import time
from datetime import datetime
from pathlib import Path

from common import _perform_cld_auto_archive

CONFIG_PATH = Path(__file__).resolve().parent / "config.json"
POLL_SECONDS = 60


def _load_config():
    try:
        with CONFIG_PATH.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except Exception:
        return {}


def main(run_once: bool = False):
    print(f"[{datetime.now()}] [CLD-AUTO-ARCHIVE] FS watcher started.")
    print(f"[{datetime.now()}] [CLD-AUTO-ARCHIVE] Poll interval: {POLL_SECONDS}s")

    while True:
        cfg = _load_config()
        auto_archive_threshold = int(cfg.get("auto_archive_threshold", 5000))
        run_mode = cfg.get("run_mode", "live")

        print(
            f"[{datetime.now()}] [CLD-AUTO-ARCHIVE] "
            f"Checking {run_mode} mode (threshold: {auto_archive_threshold})"
        )

        try:
            archived = _perform_cld_auto_archive(cfg)
            if archived:
                print(f"[{datetime.now()}] [CLD-AUTO-ARCHIVE] Archive completed successfully.")
        except Exception as exc:
            print(f"[{datetime.now()}] [CLD-AUTO-ARCHIVE] Error: {exc}")

        if run_once:
            print(f"[{datetime.now()}] [CLD-AUTO-ARCHIVE] Single run complete. Exiting.")
            break

        time.sleep(POLL_SECONDS)


if __name__ == "__main__":
    import sys

    run_once = len(sys.argv) > 1 and sys.argv[1].lower() in ("--once", "once", "-1")
    main(run_once=run_once)
