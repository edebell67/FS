
import os
import sys
import json
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict

# Add current dir to path
sys.path.append(str(Path(r"C:\Users\edebe\eds\TradeApps\breakout\fs")))

try:
    import summary_net_generator
    from summary_net_generator import SummaryGenerator, load_json_with_retry
    
    def regenerate_recent():
        gen = SummaryGenerator()
        mode = 'live'
        
        # Last 3 days (Today, Sun, Sat) should be enough for the current social refresh
        today = datetime.now()
        dates = [(today - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(3)]
        
        # Get configured product types
        from json_layout import configured_product_types, load_layout_config
        cfg = load_layout_config(gen.config_path)
        product_types = configured_product_types(cfg)
        
        for date_str in dates:
            for p_type in product_types:
                target_dir = gen.json_dir / mode / p_type / date_str
                
                if not target_dir.exists():
                    continue

                print(f"Regenerating {p_type} for {date_str}...")
                
                from summary_net_generator import TargetContext, TargetState
                context = gen._build_target_context(mode, date_str, target_dir)
                
                # Clear existing state
                key, state = gen._state_for_target(context)
                state.initialized = False
                state.trade_index = []
                state.closed_cache = defaultdict(lambda: defaultdict(list))
                state.totals = defaultdict(lambda: defaultdict(summary_net_generator._new_totals))
                
                # Use recursive scan
                json_paths = [str(p) for p in target_dir.rglob("*.json") if "snapshot" not in p.name]
                if not json_paths:
                    continue

                cld_paths = [p for p in json_paths if p.endswith("_cld.json") or p.endswith("_cl.json") or "_closed_" in p.lower()]
                
                print(f"  Found {len(cld_paths)} closed files. Loading...")
                cld_tuples = []
                for i, p in enumerate(cld_paths):
                    t = load_json_with_retry(p)
                    if t and gen._trade_matches_target_product_type(t, context.product_type):
                        time_v = t.get('exit_time') or t.get('entry_time') or "0"
                        cld_tuples.append((time_v, p, t))
                    if i > 0 and i % 1000 == 0:
                        print(f"    Loaded {i}...")

                print(f"  Processing {len(cld_tuples)} trades...")
                cld_tuples.sort(key=lambda x: x[0])
                for i, (_, p, t) in enumerate(cld_tuples):
                    gen.process_trade_dict(p, t, state, context)
                    gen.processed_files.add(p)
                    if i > 0 and i % 1000 == 0:
                        print(f"    Processed {i}...")

                state.initialized = True
                
                # Finalize
                gen.process_date(mode, date_str, target_dir)
                print(f"  Done {p_type} for {date_str}.")
                
        print("Recent regeneration complete.")

    if __name__ == "__main__":
        regenerate_recent()

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
