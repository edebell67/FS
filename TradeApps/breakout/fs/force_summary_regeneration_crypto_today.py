
import os
import sys
import json
from pathlib import Path
from collections import defaultdict
from datetime import datetime

# Add current dir to path
sys.path.append(str(Path(r"C:\Users\edebe\eds\TradeApps\breakout\fs")))

try:
    import summary_net_generator
    from summary_net_generator import SummaryGenerator, log_debug, load_json_with_retry
    
    def force_regen_crypto_today():
        gen = SummaryGenerator()
        mode = 'live'
        date_str = datetime.now().strftime("%Y-%m-%d")
        
        target_dir = gen.json_dir / mode / "crypto" / date_str
        
        if not target_dir.exists():
            print(f"Target directory not found: {target_dir}")
            return

        print(f"Starting optimized forced regeneration for CRYPTO: {target_dir}")
        
        from summary_net_generator import TargetContext, TargetState
        context = gen._build_target_context(mode, date_str, target_dir)
        
        # Ensure we clear existing state to force a full rebuild
        key, state = gen._state_for_target(context)
        state.initialized = False
        state.trade_index = []
        state.closed_cache = defaultdict(lambda: defaultdict(list))
        state.totals = defaultdict(lambda: defaultdict(summary_net_generator._new_totals))
        
        print("Scanning for closed files...")
        # Use rglob to catch all subfolders
        cld_paths = list(target_dir.rglob("*_cld.json"))
        cl_paths = list(target_dir.rglob("*_cl.json"))
        
        all_closed = cld_paths + cl_paths
        print(f"Found {len(all_closed)} closed/closing files. Loading...")
        
        cld_tuples = []
        for i, p in enumerate(all_closed):
            t = load_json_with_retry(p)
            if t and gen._trade_matches_target_product_type(t, context.product_type):
                time_v = t.get('exit_time') or t.get('entry_time') or "0"
                cld_tuples.append((time_v, str(p), t))
            if i % 1000 == 0:
                print(f"Loaded {i} files...")

        print(f"Sorting {len(cld_tuples)} trades...")
        cld_tuples.sort(key=lambda x: x[0])
        
        print("Processing trades into state...")
        for i, ( _, p, t) in enumerate(cld_tuples):
            gen.process_trade_dict(p, t, state, context)
            gen.processed_files.add(p)
            if i % 1000 == 0:
                print(f"Processed {i} trades...")

        state.initialized = True
        
        print("Finalizing summary files...")
        gen.process_date(mode, date_str, target_dir)
        
        print(f"Forced regeneration for {date_str} complete.")

    if __name__ == "__main__":
        force_regen_crypto_today()

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
