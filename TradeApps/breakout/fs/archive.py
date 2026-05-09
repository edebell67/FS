import json
import time
from datetime import datetime
from pathlib import Path

from common import _perform_archiving

CONFIG_PATH = Path(__file__).resolve().parent / "config.json"
POLL_SECONDS = 5


def _load_config():
    try:
        with CONFIG_PATH.open("r") as f:
            return json.load(f)
    except Exception:
        return {}


def _save_config(cfg):
    try:
        with CONFIG_PATH.open("w") as f:
            json.dump(cfg, f, indent=4)
    except Exception as e:
        print(f"[{datetime.now()}] [ARCHIVE] Failed to write config: {e}")


def main(run_once: bool = False):
    print(f"[{datetime.now()}] [ARCHIVE] Standalone archive watcher started.")
    while True:
        cfg = _load_config()
        if cfg.get("archive", False):
            try:
                print(f"[{datetime.now()}] [ARCHIVE] Flag detected. Archiving...")
                run_mode = str(cfg.get("run_mode", "live")).lower()
                date_str = datetime.now().strftime("%Y-%m-%d")
                base = Path(__file__).resolve().parent / "json" / run_mode
                source = base / date_str
                target = source / "archive" / datetime.now().strftime("%H%M%S")
                print(f"[{datetime.now()}] [ARCHIVE-CONTEXT] mode={run_mode} date={date_str} source={source} target={target}")
                archived_ok = _perform_archiving(cfg)
                if archived_ok:
                    cfg["archive"] = False
                    _save_config(cfg)
                    print(f"[{datetime.now()}] [ARCHIVE] Completed. Resetting flag.")
                else:
                    print(f"[{datetime.now()}] [ARCHIVE] Incomplete/Skipped. archive flag remains true.")
            except Exception as e:
                print(f"[{datetime.now()}] [ARCHIVE] Error during archiving: {e}")
        if run_once:
            break
        time.sleep(POLL_SECONDS)


if __name__ == "__main__":
    import sys
    run_once = len(sys.argv) > 1 and sys.argv[1].lower() in ("--once", "once", "-1")
    main(run_once=run_once)
