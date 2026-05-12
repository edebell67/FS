import sys
from pathlib import Path

# Add breakout fs to sys.path
sys.path.append(r'C:\Users\edebe\eds\TradeApps\breakout\fs')

import paths

print(f"EDS_ROOT: {paths.EDS_ROOT}")
print(f"DATA_EDS_ROOT: {paths.DATA_EDS_ROOT}")
print(f"BREAKOUT_DATA_FS_ROOT: {paths.BREAKOUT_DATA_FS_ROOT}")
print(f"BREAKOUT_JSON_ROOT: {paths.BREAKOUT_JSON_ROOT}")
print(f"TRADES_RT3_LIVE_DIR: {paths.TRADES_RT3_LIVE_DIR}")
