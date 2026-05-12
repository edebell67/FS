import sys
import os
import time
from collections import defaultdict
from pathlib import Path
import json

# Add current directory to sys.path to ensure we can import common
from paths import BREAKOUT_FS_ROOT, BREAKOUT_JSON_ROOT # [V20260510_1955]
sys.path.append(str(BREAKOUT_FS_ROOT))

from common import _manage_virtual_trades, CONFIG_FILE_PATH, _load_config

def run_archive():
    config = _load_config()
    print(f"Current archive flag: {config.get('archive')}")

    # Check current run mode
    run_mode = config.get('run_mode', 'live').lower()
    print(f"Current run_mode: {run_mode}")

    # Call _manage_virtual_trades which triggers the archive logic
    # We pass empty defaults for stats and prices as they won't be used due to the archive flag check
    print("Triggering _manage_virtual_trades to run archive process...")

    # [V20260510_1955] Use centralized path resolution
    json_base_dir = str(BREAKOUT_JSON_ROOT / run_mode)

    _manage_virtual_trades(
        defaultdict(lambda: defaultdict(lambda: {'pnl': 0.0, 'count': 0})),
        json_base_dir,
        0,
        {}
    )

    # Verify flag is reset
    config_after = _load_config()
    print(f"Archive flag after run: {config_after.get('archive')}")

if __name__ == "__main__":
    run_archive()
