import json
import os
from datetime import datetime
from pathlib import Path
import pandas as pd

# [V20260122_1630] New scheduler helper to check activations_is_live.json

SCHEDULER_FILE = Path(__file__).resolve().parent / 'activations_is_live.json'

def _load_schedule():
    """Load and parse the activations_is_live.json file."""
    if not SCHEDULER_FILE.exists():
        return {"live": [], "sim": []}
    
    try:
        with open(SCHEDULER_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"[SCHEDULER] Error loading {SCHEDULER_FILE}: {e}")
        return {"live": [], "sim": []}

def get_matching_live_schedule(product, strategy, parm, current_time=None, mode='live'):
    """
    Scans activations_is_live.json for a matching record.
    Matches: product, strategy, parm, and time window.
    Supports both 'live' and 'sim' modes via the mode parameter.
    Returns the matching record dict if is_live is True, else None.
    """
    schedule = _load_schedule()
    mode = str(mode).lower() if mode else 'live'
    records = schedule.get(mode, [])
    
    if not current_time:
        current_time = datetime.utcnow()
    elif isinstance(current_time, pd.Timestamp):
        current_time = current_time.to_pydatetime()
    elif isinstance(current_time, str):
        try:
            current_time = datetime.fromisoformat(current_time.replace('Z', ''))
        except ValueError:
            current_time = datetime.utcnow()

    # Normalize strategy name (remove .py if present and force lowercase)
    strategy_name = strategy.replace('.py', '').lower() if strategy else ""

    for record in records:
        # 1. Match Basic Fields
        if record.get('product') != product: continue
        
        # [V20260122_1645] Lenient strategy matching
        rec_strat = record.get('strategy', '').replace('.py', '').lower()
        # print(f"[DEBUG] Checking {rec_strat} vs {strategy_name}")
        if rec_strat not in strategy_name and strategy_name not in rec_strat:
            continue
            
        # 2. Match Parameters (String or Dict) [V20260122_1640]
        rec_parm = record.get('parm')
        # print(f"[DEBUG] Checking parm: {rec_parm} vs {parm}")
        if isinstance(rec_parm, dict):
            # Convert dict to wait_buffer_tp_sl format for comparison
            # Note: handle both 'tp' and 'tp_pips', 'sl' and 'sl_pips'
            w = rec_parm.get('window_size', rec_parm.get('window'))
            b = rec_parm.get('pip_buffer', rec_parm.get('buffer'))
            tp = rec_parm.get('tp', rec_parm.get('tp_pips'))
            sl = rec_parm.get('sl', rec_parm.get('sl_pips'))
            
            # Construct a comparison string. Ensure floats are formatted consistently.
            try:
                # Check individual components if possible
                curr_w, curr_b, curr_tp, curr_sl = parm.split('_')
                if str(w) != curr_w: continue
                if abs(float(b) - float(curr_b)) > 1e-7: continue
                if abs(float(tp) - float(curr_tp)) > 1e-7: continue
                if abs(float(sl) - float(curr_sl)) > 1e-7: continue
            except (ValueError, TypeError):
                continue
        elif rec_parm != parm:
            continue
        
        # 3. Match Time Window
        try:
            start_time = pd.to_datetime(record['start_time']).tz_localize(None)
            
            # Check Start Time (must be on or after)
            if current_time < start_time:
                continue
                
            # Check End Time (must be before, if exists)
            end_time_val = record.get('end_time')
            if end_time_val:
                end_time = pd.to_datetime(end_time_val).tz_localize(None)
                if current_time >= end_time:
                    continue
            
            # 4. Check is_live flag
            if record.get('is_live') is True:
                # print(f"[SCHEDULER] MATCH FOUND: {record}")
                return record
            else:
                # print(f"[SCHEDULER] Record found but is_live is False: {record}")
                pass
                
        except (ValueError, KeyError, TypeError) as e:
            # print(f"[SCHEDULER] Time parsing error in record: {e}")
            continue
            
    # print(f"[SCHEDULER] No match found for {product} {strategy_name} {parm} at {current_time}")
    return None

if __name__ == "__main__":
    # Test logic
    test_time = datetime(2026, 1, 22, 17, 0, 0)
    match = get_matching_live_schedule("AUD", "breakout_R_Rev_3_tp10.0_sl10.0", "3_0.00015_10.0_10.0", test_time)
    print(f"Match found: {match is not None}")
    if match:
        print(f"Matched Record: {match}")
