
import sys
import os
import time
from collections import defaultdict
from pathlib import Path
import json

# Add current directory to sys.path to ensure we can import common
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from common import _manage_virtual_trades, CONFIG_FILE_PATH, _load_config
except ImportError:
    # Fallback if running from a different directory
    sys.path.append(r'c:\Users\edebe\eds\TradeApps\breakout\fs')
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
    
    # We need to compute json_base_dir correctly here too just for the call,
    # though _perform_archiving ignores this argument and recalculates it (now correctly).
    json_base_dir = os.path.join(os.path.dirname(CONFIG_FILE_PATH), 'json', run_mode)
    
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
