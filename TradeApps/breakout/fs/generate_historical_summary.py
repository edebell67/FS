
import os
import json
import glob
from pathlib import Path
from datetime import datetime
from summary_net_generator import SummaryGenerator

def generate_for_dir(target_path, mode='live', date_str=None):
    gen = SummaryGenerator()
    target_dir = Path(target_path)
    if not date_str:
        date_str = target_dir.name
    
    if not target_dir.exists():
        print(f"Directory not found: {target_dir}")
        return

    print(f"Generating summary for {target_dir}...")
    gen.process_date(mode, date_str, target_dir)
    print(f"Generated _summary_net.json, _trades_summary.json, and _top20.json in {target_dir}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and os.path.isdir(sys.argv[1]):
        target = sys.argv[1]
        mode = sys.argv[2] if len(sys.argv) > 2 else "live"
        date = sys.argv[3] if len(sys.argv) > 3 else Path(target).name
        generate_for_dir(target, mode, date)
    else:
        target_date = sys.argv[1] if len(sys.argv) > 1 else "2026-02-04"
        target_mode = sys.argv[2] if len(sys.argv) > 2 else "live"
        base_path = Path(r'C:\Users\edebe\eds\TradeApps\breakout\fs')
        json_root = base_path / "json"
        target_dir = json_root / target_mode / target_date
        generate_for_dir(target_dir, target_mode, target_date)
