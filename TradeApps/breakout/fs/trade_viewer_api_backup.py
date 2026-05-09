"""
Breakout Trade Viewer API Server
Activation model v2:
- Activation keys are STRATEGY + DIRECTION + MODE ONLY
- Products are stored as metadata inside activation entries
- Legacy keys containing product suffixes are auto-migrated
"""

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import json
import os
import threading
from pathlib import Path
from datetime import datetime
import re
import urllib.request # Switched to urllib for better compatibility
from typing import Dict, Any, List, Set, Tuple, Optional
from constants import VERSION # V20260105_2220
# V20260105_0025: Added /api/activations/remove endpoint

# ─────────────────────────────────────────────
# Global Locks
# ─────────────────────────────────────────────
# [V20260128_1515] Lock for serializing access to grid_live.json
GRID_LIVE_LOCK = threading.Lock()

# ─────────────────────────────────────────────
# App setup
# ─────────────────────────────────────────────
app = Flask(__name__)
CORS(app)

BASE_PATH = Path(r"C:\Users\edebe\eds\TradeApps\breakout\fs\json")
ROOT_PATH = BASE_PATH.parent
CONFIG_FILE = ROOT_PATH / "config.json"
ACTIVATIONS_FILE = ROOT_PATH / "activations.json"
ACTIVATION_SUFFIXES = ("_buy_net", "_sell_net", "_buy_alt", "_sell_alt")


# ─────────────────────────────────────────────
# API Endpoints
# ─────────────────────────────────────────────
@app.route('/api/trade_file', methods=['GET'])
def get_trade_file():
    """Load raw content of a specific trade JSON file [V20251230_0010] [V20260122_FS]"""
    try:
        run_mode = request.args.get('mode', 'live')
        date = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))
        # Support both 'filename' and 'trade_id' parameters for compatibility
        filename = request.args.get('filename') or request.args.get('trade_id')

        if not filename:
            return jsonify({'success': False, 'message': 'Filename or trade_id is required'}), 400

        # Prevent directory traversal
        safe_name = os.path.basename(filename)
        candidate_names = [safe_name]
        normalized = _strip_trade_suffix(safe_name)
        base_stem = Path(normalized).stem
        for suffix in ('_op.json', '_cl.json', '_cld.json'):
            candidate_names.append(f"{base_stem}{suffix}")

        file_path = None
        for candidate in candidate_names:
            for p in (BASE_PATH / run_mode / date / candidate, BASE_PATH / run_mode / date / 'virtual' / candidate):
                if p.exists():
                    file_path = p
                    safe_name = candidate
                    break
            if file_path:
                break

        # [V20260122_FS] Robust search: If no path found and 'filename' looks like an ID, search directory
        if not file_path and (filename.isdigit() or len(filename) < 10):
            print(f"[TRADE_FILE] Explicit match failed for {filename}, searching directory {date}...")
            search_dirs = [BASE_PATH / run_mode / date, BASE_PATH / run_mode / date / 'virtual']
            for s_dir in search_dirs:
                if not s_dir.exists(): continue
                for json_file in s_dir.glob('*.json'):
                    if filename in json_file.name: # Simple string match for trade_id
                        # Verify it's the actual ID by checking file content
                        try:
                            with open(json_file, 'r') as f:
                                data = json.load(f)
                                if str(data.get('trade_id')) == str(filename):
                                    file_path = json_file
                                    break
                        except: continue
                if file_path: break

        if not file_path:
            return jsonify({'success': False, 'message': f'File not found: {filename}'}), 404

        with open(file_path, 'r') as f:
            content = json.load(f)

        return jsonify({
            'success': True,
            'filename': filename,
            'content': content
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

def _strip_trade_suffix(filename: str) -> str:
    name = os.path.basename(filename)
    if not name.endswith('.json'):
        name = f"{name}.json"
    for suffix in ('_cld.json', '_cl.json', '_op.json'):
        if name.endswith(suffix):
            return name[:-len(suffix)] + '.json'
    return name


def _load_trade_products() -> Set[str]:
    try:
        with open(CONFIG_FILE, "r") as f:
            cfg = json.load(f)
        return {p.upper() for p in cfg.get("trade_products", []) if isinstance(p, str)}
    except Exception:
        return set()


def _extract_product(core: str, products: Set[str]) -> Tuple[str, Optional[str]]:
    core_upper = core.upper()
    for p in sorted(products, key=len, reverse=True):
        if core_upper.endswith(f"_{p}"):
            return core[: -(len(p) + 1)], p
    return core, None


def _normalize_key(raw_key: str, products: Set[str]) -> Tuple[str, Optional[str]]:
    suffix = next((s for s in ACTIVATION_SUFFIXES if raw_key.endswith(s)), None)
    if not suffix:
        return raw_key, None
    core = raw_key[: -len(suffix)]
    base, product = _extract_product(core, products)
    return f"{base}{suffix}", product


def _coerce_entry(value: Any) -> Dict[str, Any]:
    if isinstance(value, dict):
        # [V20260127_1520] Handle None products safely
        raw_products = value.get("products") or []
        return {
            "active": bool(value.get("active")),
            "manual": bool(value.get("manual")),
            "activated_at": value.get("activated_at"),
            "products": sorted({p.upper() for p in raw_products if isinstance(p, str)})
        }
    return {
        "active": bool(value),
        "manual": False,
        "activated_at": None,
        "products": []
    }


def _merge_entries(a: Dict[str, Any], b: Dict[str, Any]) -> Dict[str, Any]:
    a["active"] = a["active"] or b["active"]
    a["manual"] = a["manual"] or b["manual"]
    if b.get("activated_at") and (
        not a.get("activated_at") or b["activated_at"] > a["activated_at"]
    ):
        a["activated_at"] = b["activated_at"]
    a["products"] = sorted(set(a.get("products", [])) | set(b.get("products", [])))
    return a


def _is_legacy_format(raw: Dict[str, Any]) -> bool:
    """Check if activations.json is in old (flat) format. [V20251230_2336]"""
    if not raw:
        return False
    # If top-level keys are 'live' or 'sim', it's new format
    if 'live' in raw or 'sim' in raw:
        return False
    # Otherwise, check if any key looks like an activation key
    for key in raw.keys():
        if any(key.endswith(suffix) for suffix in ACTIVATION_SUFFIXES):
            return True
    return False


def _migrate_to_mode_format(raw: Dict[str, Any]) -> Dict[str, Any]:
    """Migrate old flat format to mode-segmented format. [V20251230_2336]"""
    # Move all existing activations to 'live' by default
    return {
        'live': raw,
        'sim': {}
    }


def _normalize_activations(raw: Dict[str, Any]) -> Tuple[Dict[str, Any], bool]:
    products = _load_trade_products()
    out: Dict[str, Any] = {}
    dirty = False

    for raw_key, raw_val in raw.items():
        base_key, product = _normalize_key(str(raw_key), products)
        entry = _coerce_entry(raw_val)

        if product:
            entry["products"].append(product)

        entry["products"] = sorted(set(entry["products"]))

        if raw_key != base_key or product:
            dirty = True

        if base_key in out:
            out[base_key] = _merge_entries(out[base_key], entry)
        else:
            out[base_key] = entry

    return out, dirty


def _load_activations() -> Dict[str, Any]:
    """Load activations with mode segmentation support. [V20251230_2336]"""
    if not ACTIVATIONS_FILE.exists():
        # Create new format structure
        return {'live': {}, 'sim': {}}

    try:
        with open(ACTIVATIONS_FILE, "r") as f:
            raw = json.load(f)
    except json.JSONDecodeError as jde:
        print(f"[ERROR] Corrupted activations.json: {jde}")
        return {'live': {}, 'sim': {}}
    except Exception as e:
        print(f"[ERROR] Loading activations.json failed: {e}")
        return {'live': {}, 'sim': {}}

    # Check if migration is needed
    if _is_legacy_format(raw):
        print("[MIGRATION] Converting activations.json to mode-segmented format...")
        raw = _migrate_to_mode_format(raw)
        dirty = True
    else:
        dirty = False

    # Ensure both mode sections exist
    if 'live' not in raw:
        raw['live'] = {}
        dirty = True
    if 'sim' not in raw:
        raw['sim'] = {}
        dirty = True

    # Normalize each mode section
    for mode in ['live', 'sim']:
        if mode in raw and isinstance(raw[mode], dict):
            normalized, mode_dirty = _normalize_activations(raw[mode])
            raw[mode] = normalized
            dirty = dirty or mode_dirty

    # Save if any changes were made
    if dirty:
        with open(ACTIVATIONS_FILE, "w") as f:
            json.dump(raw, f, indent=4)

    return raw


# ─────────────────────────────────────────────
# API Endpoints
# ─────────────────────────────────────────────
@app.route("/api/activations", methods=["GET"])
def get_activations():
    """Get activations for specified mode. [V20251230_2336]"""
    mode = request.args.get('mode', 'live').lower()
    all_activations = _load_activations()
    
    # Return activations for requested mode only
    mode_activations = all_activations.get(mode, {})
    
    return jsonify({
        "success": True,
        "activations": mode_activations
    })


# [V20260127_1520] Get available dates for a given mode
@app.route("/api/dates", methods=["GET"])
def get_dates():
    """Get available trade dates for specified mode."""
    mode = request.args.get('mode', 'live').lower()
    json_dir = ROOT_PATH / "json" / mode
    
    dates = []
    if json_dir.exists():
        for item in json_dir.iterdir():
            if item.is_dir() and len(item.name) == 10:  # YYYY-MM-DD format
                dates.append(item.name)
    
    dates.sort(reverse=True)  # Most recent first
    
    return jsonify({
        "success": True,
        "dates": dates
    })

@app.route('/api/trades', methods=['GET'])
def get_trades():
    """
    [V20260128_1500] Load trade JSON files for a given mode and date.
    Optimized: Uses filename pattern matching to reduce file scanning when filters are provided.
    """
    try:
        run_mode = request.args.get('mode', 'live')
        date = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))
        strategy_filter = request.args.get('strategy', 'all')
        req_strategy = strategy_filter # Alias for loop logic
        req_product = request.args.get('product')
        req_params = request.args.get('params')
        live_only = request.args.get('live_only', 'false').lower() == 'true'
        
        trade_dir = BASE_PATH / run_mode / date
        
        if not trade_dir.exists():
            return jsonify({
                'success': False,
                'message': f'Directory not found: {trade_dir}',
                'trades': []
            })
        
        trades = []
        
        # [V20260128_1500] Optimization: Build specific glob pattern based on filters
        # Filename format: {strategy}_{product}_{direction}_{timestamp}_{...}.json
        # Example: breakout_R_Rev_2_tp10.0_sl10.0_AUD_B_20260128_...
        if strategy_filter and strategy_filter != 'all' and strategy_filter != 'undefined':
            # Use strategy as glob prefix
            glob_pattern = f"{strategy_filter}_*.json"
        else:
            glob_pattern = "*.json"
        
        file_count = 0
        for json_file in trade_dir.glob(glob_pattern):
            if json_file.name.startswith('_'): # Skip metadata files
                continue
            
            file_count += 1
            # Safety limit to prevent hanging
            if file_count > 5000:
                print(f"[API] /api/trades: Hit 5000 file limit, stopping scan")
                break

            try:
                # [V20260128_0415] Optimization: Parse filename first to pre-filter before reading file content
                raw_filename = json_file.name
                normalized_filename = _strip_trade_suffix(raw_filename)
                filename = Path(normalized_filename).stem
                parts = filename.split('_')
                
                # Check for product/app_name in filename
                f_app_name = None
                f_product_code = None
                f_strategy_params = None
                
                if len(parts) >= 6:
                    timestamp_idx = None
                    for i, part in enumerate(parts):
                        if len(part) == 8 and part.isdigit():
                            timestamp_idx = i
                            break
                    
                    if timestamp_idx is not None:
                        # Parsing logic mirrors that in get_stats_summary and previous get_trades
                        candidate_idx = timestamp_idx - 1
                        if candidate_idx >= 0:
                            val = parts[candidate_idx]
                            if len(val) <= 2 and val.isalpha() and val.isupper():
                                product_idx = candidate_idx - 1
                                if product_idx >= 0:
                                    potential_product = parts[product_idx]
                                    if len(potential_product) >= 3 and potential_product.isalpha() and potential_product.isupper():
                                        f_app_name = '_'.join(parts[:product_idx])
                                        f_product_code = potential_product
                                    else:
                                        f_app_name = '_'.join(parts[:candidate_idx])
                                else:
                                    f_app_name = '_'.join(parts[:candidate_idx])
                            else:
                                if len(val) >= 3 and val.isalpha() and val.isupper():
                                    f_app_name = '_'.join(parts[:candidate_idx])
                                    f_product_code = val
                                else:
                                    f_app_name = '_'.join(parts[:timestamp_idx])
                        else:
                            f_app_name = '_'.join(parts[:timestamp_idx])
                            
                        window = parts[timestamp_idx + 2] if timestamp_idx + 2 < len(parts) else '5'
                        buffer = parts[timestamp_idx + 3] if timestamp_idx + 3 < len(parts) else '0.0001'
                        tp = parts[timestamp_idx + 4].replace('.json', '') if timestamp_idx + 4 < len(parts) else '10.0'
                        sl = parts[timestamp_idx + 5].replace('.json', '') if timestamp_idx + 5 < len(parts) else '6.0'
                        
                        f_strategy_params = f"{window}_{buffer}_{tp}_{sl}"

                # Server-Side Filter Check (Optimization)
                # [V20260128_1555] Relaxed pre-filter: allow f_app_name to start with req_strategy
                # This handles cases where f_app_name includes product components (e.g. GBPAUD_C)
                if req_strategy and req_strategy != 'all' and req_strategy != 'undefined' and f_app_name:
                    if req_strategy != f_app_name and not f_app_name.startswith(req_strategy):
                        continue
                    
                if req_product and req_product != 'all' and req_product != 'undefined' and f_product_code and req_product != f_product_code.upper():
                    pass 

                with open(json_file, 'r') as f:
                    trade_data = json.load(f)
                    
                    status_suffix = None
                    if raw_filename.endswith('_op.json') or raw_filename.endswith('_op'):
                        status_suffix = 'OPEN'
                    elif raw_filename.endswith('_cl.json') or raw_filename.endswith('_cl') or raw_filename.endswith('_cld.json') or raw_filename.endswith('_cld'):
                        status_suffix = 'CLOSED'
                    
                    # [V20260128_1555] Normalize App Name from JSON content (matches summary_net_generator)
                    # This ensures the Drill-down matches the table row accurately.
                    internal_app_name = trade_data.get('source_strategy') or trade_data.get('script_name') or trade_data.get('app_name') or f_app_name or 'unknown'
                    
                    # Apply logic to standardize fields
                    trade_data['app_name'] = internal_app_name
                    trade_data['script_name'] = internal_app_name # Compatibility
                    
                    # Strategy (Params) resolution
                    # Try to get from JSON first
                    strategy_params = trade_data.get('strategy') or f_strategy_params or ''
                    trade_data['strategy'] = strategy_params
                    trade_data['strategy_key'] = strategy_params # Compatibility
                    
                    # Product resolution
                    if 'product' not in trade_data:
                        trade_data['product'] = f_product_code or 'UNKNOWN'
                    
                    trade_data['filename'] = raw_filename
                    if status_suffix:
                        trade_data['status'] = status_suffix
                        
                    # Final Filter Checks
                    if strategy_filter != 'all' and internal_app_name != strategy_filter:
                         continue

                    # Filter by Params if requested
                    if req_params and req_params != 'all' and req_params != 'undefined':
                        if trade_data['strategy'] != req_params:
                            continue
                            
                    # Filter by Product if requested
                    if req_product and req_product != 'all' and req_product != 'undefined':
                        if trade_data.get('product') != req_product:
                            continue

                    # [V20260122_FS] Apply live_only filter
                    if live_only:
                        is_live = trade_data.get('order_sent_net') in [True, 'true']
                        if not is_live:
                            continue

                    trades.append(trade_data)
                            
            except json.JSONDecodeError as e:
                print(f"Error parsing {json_file}: {e}")
                continue
            except Exception as e:
                print(f"Error loading {json_file}: {e}")
                continue
        
        return jsonify({
            'success': True,
            'count': len(trades),
            'trades': trades,
            'mode': run_mode,
            'date': date,
            'version': VERSION
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e),
            'trades': []
        }), 500


@app.route('/api/stats_summary', methods=['GET'])
def get_stats_summary():
    """
    [V20260128_1448] FAST Strategy Performance Stats.
    Reads from pre-generated _summary_net.json instead of iterating through thousands of trade files.
    """
    try:
        run_mode = request.args.get('mode', 'live')
        date = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))

        trade_dir = BASE_PATH / run_mode / date
        summary_file = trade_dir / "_summary_net.json"

        if not summary_file.exists():
            return jsonify({
                'success': False,
                'message': f'Summary file not found: {summary_file}. Run summary_net_generator.py.',
                'data': []
            })

        with open(summary_file, 'r') as f:
            summary_data = json.load(f)

        strategies = summary_data.get('strategies', {})
        
        # Build aggregated stats from summary_net structure
        # Structure: { "strategy_name": { "PRODUCT": [ {t, net, buy_net, sell_net, b_c, s_c, ...}, ... ] } }
        
        result = []
        for strategy_name, products in strategies.items():
            for product, data_points in products.items():
                if not data_points:
                    continue
                
                # Get the LAST data point (most recent aggregation)
                last = data_points[-1] if isinstance(data_points, list) else data_points
                
                result.append({
                    'product': product,
                    'strategy': strategy_name,
                    'params': '',  # Not available in summary_net
                    'trade_count': last.get('b_c', 0) + last.get('s_c', 0),
                    'total_net': round(last.get('net', 0), 2),
                    'buy_count': last.get('b_c', 0),
                    'buy_net': round(last.get('buy_net', 0), 2),
                    'sell_count': last.get('s_c', 0),
                    'sell_net': round(last.get('sell_net', 0), 2),
                    'buyPercent': last.get('buyPercent', 0),
                    'sellPercent': last.get('sellPercent', 0),
                    'live_buy_net': 0,  # Not tracked in summary_net
                    'live_sell_net': 0  # Not tracked in summary_net
                })

        return jsonify({
            'success': True,
            'data': result,
            'mode': run_mode,
            'date': date,
            'source': 'summary_net'
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'message': str(e),
            'data': []
        }), 500


@app.route('/api/virtual_trades', methods=['GET'])
def get_virtual_trades():
    """Load virtual trade JSON files for the given run mode/date."""
    try:
        run_mode = request.args.get('mode', 'live')
        date = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))
        virtual_dir = BASE_PATH / run_mode / date / 'virtual'
        trades = []
        if virtual_dir.exists():
            for json_file in virtual_dir.glob('vt_*.json'):
                try:
                    with open(json_file, 'r') as handle:
                        trade_data = json.load(handle)
                        trade_data['filename'] = json_file.name
                        trades.append(trade_data)
                except Exception as exc:  # pylint: disable=broad-except
                    print(f"[WARN] Failed to read {json_file}: {exc}")
                    continue
        trades.sort(key=lambda entry: entry.get('entry_time') or entry.get('exit_time') or '', reverse=True)
        return jsonify({
            'success': True,
            'trades': trades
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e),
            'trades': []
        }), 500



@app.route("/api/activations", methods=["POST"])
def update_activations():
    """Update activations for specified mode. [V20251230_2336]"""
    payload = request.json or {}
    mode = payload.get('mode', 'live').lower()  # Get mode from payload
    activations_data = payload.get('activations', payload)  # Support both formats
    
    # Remove 'mode' key if it exists in activations_data
    if 'mode' in activations_data:
        del activations_data['mode']
    
    now = datetime.utcnow().isoformat()
    trade_products = _load_trade_products()

    # Load all activations (mode-segmented)
    all_activations = _load_activations()
    
    # Get activations for current mode
    mode_activations = all_activations.get(mode, {})

    for raw_key, value in activations_data.items():
        base_key, derived_product = _normalize_key(str(raw_key), trade_products)
        entry = mode_activations.get(base_key, {
            "active": False,
            "manual": False,
            "activated_at": None,
            "products": []
        })

        if isinstance(value, dict):
            requested_active = bool(value.get("active"))
            manual = bool(value.get("manual"))
            products = value.get("products") or value.get("product") or []
        else:
            requested_active = bool(value)
            manual = False
            products = []

        if derived_product:
            products = list(products) + [derived_product]

        products = {p.upper() for p in products if isinstance(p, str)}

        if products:
            if requested_active:
                entry["products"] = sorted(set(entry["products"]) | products)
                entry["active"] = True
                entry["activated_at"] = entry["activated_at"] or now
            else:
                entry["products"] = sorted(set(entry["products"]) - products)
                entry["active"] = bool(entry["products"])
                if not entry["active"]:
                    entry["activated_at"] = None
        else:
            entry["active"] = requested_active
            entry["activated_at"] = now if requested_active else None

        entry["manual"] = manual
        
        # [V20251230_2351] Remove entry if it becomes inactive
        if entry["active"]:
            mode_activations[base_key] = entry
        elif base_key in mode_activations:
            # Remove the entry if it's being deactivated
            del mode_activations[base_key]

    # Update the mode section
    all_activations[mode] = mode_activations

    # Save all activations
    with open(ACTIVATIONS_FILE, "w") as f:
        json.dump(all_activations, f, indent=4)

    return jsonify({
        "success": True,
        "activations": mode_activations  # Return only current mode's activations
    })


@app.route("/api/activations/remove", methods=["POST"])
def remove_activation():
    """Remove a specific activation key entirely. [V20260105_0025]"""
    try:
        payload = request.json or {}
        mode = payload.get('mode', 'live').lower()
        key = payload.get('key')

        if not key:
            return jsonify({"success": False, "message": "Key is required"}), 400

        all_activations = _load_activations()
        
        if mode not in all_activations:
            return jsonify({"success": False, "message": f"Mode {mode} not found"}), 404
            
        if key not in all_activations[mode]:
             return jsonify({"success": False, "message": f"Key {key} not found in {mode}"}), 404

        # Remove the key
        del all_activations[mode][key]

        # Save the updated file
        with open(ACTIVATIONS_FILE, "w") as f:
            json.dump(all_activations, f, indent=4)
        return jsonify({
            "success": True,
            "message": f"Successfully removed {key} from {mode}"
        })
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


# ─────────────────────────────────────────────
# Trade Promotion Helpers [V20260127_1610]
# ─────────────────────────────────────────────

def _scan_open_trades(mode: str, date_str: str) -> List[Dict[str, Any]]:
    """Scan and load all open trade JSON files for a given mode/date.
    
    Returns:
        List of dicts with 'path' and 'data' keys
    """
    json_dir = ROOT_PATH / "json" / mode / date_str
    if not json_dir.exists():
        return []
    
    open_trades = []
    for file_path in json_dir.glob("*_op.json"):
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                open_trades.append({
                    'path': file_path,
                    'data': data
                })
        except Exception as e:
            print(f"[WARN] Failed to load {file_path}: {e}")
    
    return open_trades


def _match_trade(trade_data: Dict[str, Any], strategy: str, product: str, direction: str, parm: str) -> bool:
    """Check if a trade matches the given criteria.
    
    Args:
        trade_data: Trade JSON data
        strategy: Strategy name (e.g., 'breakout_2_tp20.0_sl10.0')
        product: Product name (e.g., 'GBPEUR_C')
        direction: 'buy' or 'sell'
        parm: Parameter string (e.g., '2_0.00015_20.0_10.0')
    
    Returns:
        True if trade matches all criteria
    """
    # Match strategy name
    trade_strategy = trade_data.get('script_name', trade_data.get('app_name', ''))
    if trade_strategy != strategy:
        return False
    
    # Match product
    trade_product = trade_data.get('product', '')
    if trade_product != product:
        return False
    
    # Match direction
    trade_direction = trade_data.get('direction', '').upper()
    if direction == 'buy' and trade_direction not in ('LONG', 'BUY'):
        return False
    if direction == 'sell' and trade_direction not in ('SHORT', 'SELL'):
        return False
    
    # Match parameters (optional - if parm is provided)
    if parm:
        trade_parm = trade_data.get('strategy', '')  # Parameters are stored in 'strategy' field
        if trade_parm != parm:
            return False
    
    return True


def _promote_trade_to_live(trade_path: Path, trade_data: Dict[str, Any], mode_type: str = 'net') -> bool:
    """Promote a single trade to live status by creating tradeable order and updating flags.
    
    Args:
        trade_path: Path to the open trade JSON file
        trade_data: Trade data dict
        mode_type: 'net' or 'alt'
    
    Returns:
        True if promotion succeeded
    """
    try:
        # Check if already promoted
        flag_key = f'order_sent_{mode_type}'
        if trade_data.get(flag_key):
            print(f"[PROMOTE] Trade {trade_path.name} already has {flag_key}=True")
            return False
        
        # Create tradeable order JSON
        tradeable_dir = trade_path.parent / "tradeable"
        tradeable_dir.mkdir(exist_ok=True)
        
        # Generate tradeable filename
        base_name = trade_path.stem.replace('_opn', '')
        tradeable_name = f"{base_name}_{mode_type}_opn.json"
        tradeable_path = tradeable_dir / tradeable_name
        
        # Create tradeable order content
        tradeable_order = {
            'trade_id': trade_data.get('id', trade_data.get('trade_id')),
            'product': trade_data.get('product'),
            'direction': trade_data.get('direction'),
            'entry_price': trade_data.get('entry_price'),
            'entry_time': trade_data.get('entry_time'),
            'tp_pips': trade_data.get('tp_pips'),
            'sl_pips': trade_data.get('sl_pips'),
            'mode': mode_type,
            'promoted_at': datetime.utcnow().isoformat(),
            'promoted_by': 'activation_toggle',
            'status': 'OPEN'
        }
        
        # Write tradeable order
        with open(tradeable_path, 'w') as f:
            json.dump(tradeable_order, f, indent=2)
        
        # Update open trade JSON with live flag
        trade_data[flag_key] = True
        trade_data['promoted_at'] = datetime.utcnow().isoformat()
        
        with open(trade_path, 'w') as f:
            json.dump(trade_data, f, indent=2)
        
        print(f"[PROMOTE] Successfully promoted {trade_path.name} to {mode_type.upper()} L-trade")
        return True
        
    except Exception as e:
        print(f"[ERROR] Failed to promote trade {trade_path}: {e}")
        return False


@app.route("/api/promote_trades", methods=["POST"])
def promote_trades():
    """Promote existing open trades to L-trades when activation is toggled.
    
    This endpoint scans for open trades matching the given criteria and promotes
    them to live status by creating tradeable orders.
    """
    try:
        payload = request.json or {}
        mode = payload.get('mode', 'live').lower()
        strategy = payload.get('strategy', '')
        product = payload.get('product', '')
        direction = payload.get('direction', '')  # 'buy' or 'sell'
        parm = payload.get('parm', '')
        date_str = payload.get('date', datetime.now().strftime('%Y-%m-%d'))
        
        if not all([strategy, product, direction]):
            return jsonify({
                "success": False,
                "message": "Missing required parameters: strategy, product, direction"
            }), 400
        
        # Scan for open trades
        open_trades = _scan_open_trades(mode, date_str)
        
        # Find matching trades
        matching_trades = []
        for trade_info in open_trades:
            if _match_trade(trade_info['data'], strategy, product, direction, parm):
                matching_trades.append(trade_info)
        
        # Promote matching trades
        promoted_count = 0
        failed_count = 0
        
        for trade_info in matching_trades:
            # Promote to 'net' mode (can be extended to support 'alt' as well)
            if _promote_trade_to_live(trade_info['path'], trade_info['data'], mode_type='net'):
                promoted_count += 1
            else:
                failed_count += 1
        
        return jsonify({
            "success": True,
            "promoted": promoted_count,
            "failed": failed_count,
            "total_matched": len(matching_trades),
            "message": f"Promoted {promoted_count} trade(s) to live status"
        })
        
    except Exception as e:
        print(f"[ERROR] Promotion failed: {e}")
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


@app.route("/api/config", methods=["GET"])
def get_config():
    try:
        with open(CONFIG_FILE, "r") as f:
            return jsonify({"success": True, "config": json.load(f)})
    except Exception:
        return jsonify({"success": True, "config": {}})


@app.route("/api/config", methods=["POST"])
def update_config():
    data = request.json
    if not isinstance(data, dict):
        return jsonify({"success": False, "message": "Invalid config"}), 400

    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=4)

    return jsonify({"success": True})


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "ts": datetime.utcnow().isoformat()})


@app.route("/multi_chart.html")
def serve_multi_chart():
    return send_from_directory(ROOT_PATH, "multi_chart.html")


@app.route("/multi_chart.js")
def serve_multi_chart_js():
    return send_from_directory(ROOT_PATH, "multi_chart.js")


@app.route('/', defaults={'path': 'trade_viewer.html'})
@app.route('/<path:path>')
def serve_static(path):
    """Serve any static file from ROOT_PATH, fallback to trade_viewer.html"""
    try:
        # Prevent accessing files outside of ROOT_PATH
        if Path(ROOT_PATH / path).exists() and Path(ROOT_PATH / path).is_file():
            return send_from_directory(ROOT_PATH, path)
        return send_from_directory(ROOT_PATH, "trade_viewer.html")
    except:
        return send_from_directory(ROOT_PATH, "trade_viewer.html")


@app.route("/api/top_one", methods=["GET"])
def get_top_one():
    """Load _top_one.json for a given mode and date [V20260105_1532]"""
    try:
        run_mode = request.args.get('mode', 'live')
        date = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))
        
        file_path = BASE_PATH / run_mode / date / "_top_one.json"
        
        if not file_path.exists():
            return jsonify({
                'success': False,
                'message': f'Summary file not found for {date} ({run_mode})',
                'content': None
            })
            
        with open(file_path, 'r') as f:
            content = json.load(f)
            
        return jsonify({
            'success': True,
            'content': content
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route("/api/frequency", methods=["GET"])
def get_frequency():
    """Proxy for the SQL frequency API [V20260105_2355]"""
    try:
        mode = request.args.get('mode', 'live')
        db = 'tradedb_sim2' if mode == 'sim' else 'tradedb'
        
        # Call the port 8000 API
        url = f"http://127.0.0.1:8000/api/vw_top_one_frequency?db={db}"
        print(f"[PROXY] Fetching: {url}")
        
        with urllib.request.urlopen(url, timeout=10) as response:
            if response.status == 200:
                raw_data = response.read().decode('utf-8')
                data = json.loads(raw_data)
                rows = data.get('data', [])
                return jsonify({
                    'success': True,
                    'data': rows
                })
            else:
                return jsonify({
                    'success': False,
                    'message': f"SQL API returned status {response.status}"
                }), response.status
                
    except Exception as e:
        print(f"[ERROR] Proxy failed: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route("/sidebar.css")
def serve_sidebar_css():
    return send_from_directory(ROOT_PATH, "sidebar.css")


@app.route("/pnl_graph.css")
def serve_pnl_graph_css():
    return send_from_directory(ROOT_PATH, "pnl_graph.css")


@app.route("/sidebar.html")
def serve_sidebar_html():
    return send_from_directory(ROOT_PATH, "sidebar.html")


# ─────────────────────────────────────────────
# Trade Buckets Activation Sync [V20260122_2230]
# ─────────────────────────────────────────────

def _parse_strategy_key(key: str) -> Optional[dict]:
    """Parse a strategy key like 'breakout_Rev_3_tp20.0_sl10.0 | GBPEUR_C'."""
    if not key or ' | ' not in key:
        return None
    try:
        strat_part, product = key.split(' | ')
        product = product.strip()
        
        # Defaults
        tp = 5.0
        sl = 6.0
        window = 3
        buffer = 0.00015
        
        # Extract TP/SL using regex
        tp_m = re.search(r'_tp(\d+\.?\d*)', strat_part)
        sl_m = re.search(r'_sl(\d+\.?\d*)', strat_part)
        
        if tp_m: tp = float(tp_m.group(1))
        if sl_m: sl = float(sl_m.group(1))
        
        # Extract base name (strip params)
        base = strat_part
        if tp_m: base = strat_part[:tp_m.start()]
        elif sl_m: base = strat_part[:sl_m.start()]
        base = base.strip('_')
        
        # Try to infer window size from name (e.g. Rev_3 -> 3)
        win_m = re.search(r'_([1-9])$', base)
        if not win_m:
            win_m = re.search(r'_([1-9])_', base)
        if win_m:
            window = int(win_m.group(1))
            
        return {
            'product': product,
            'strategy': base,
            'parm': {
                'window_size': window,
                'pip_buffer': buffer,
                'tp': tp,
                'sl': sl
            }
        }
    except Exception as e:
        print(f"[PARSER] Error parsing key {key}: {e}")
        return None


def _sync_bucket_to_activations(bucket: dict, mode: str, date_str: str):
    """Sync bucket strategies to activations_is_live.json if criteria is met."""
    try:
        bucket_name = bucket.get('name')
        bucket_live = bucket.get('live', False)
        min_diff = float(bucket.get('minimum_difference', 5.0))
        start_time_str = bucket.get('start_time')
        
        # 1. Load Summary to calculate current net differences
        summary_file = BASE_PATH / mode / date_str / "_summary_net.json"
        summary_net = {}
        if summary_file.exists():
            try:
                with open(summary_file, 'r') as f:
                    summary_data = json.load(f)
                    summary_net = summary_data.get('strategies', {})
            except: pass

        # 2. Load current activations
        act_file = ROOT_PATH / 'activations_is_live.json'
        # Default structure
        act_data = {"live": [], "sim": []}
        if act_file.exists():
            try:
                with open(act_file, 'r') as f:
                    content = json.load(f)
                    if isinstance(content, dict):
                        act_data = content
            except: pass

        # 3. Clean out existing entries for THIS specific bucket
        source_tag = f"trade_bucket:{bucket_name}"
        active_list = act_data.get('live', [])
        new_active_list = [a for a in active_list if a.get('source') != source_tag]

        # 4. If bucket is live, evaluate strategies and find the SINGLE top performer
        if bucket_live:
            print(f"[SYNC] Identifying top performer for bucket '{bucket_name}'...")
            
            top_strat_record = None
            max_perf_diff = -999999.0
            
            for strat in bucket.get('strategies', []):
                strat_key = strat.get('key', '')
                parsed = _parse_strategy_key(strat_key)
                if not parsed: 
                    continue

                # Calculate current net performance relative to start_time
                strat_name_only = strat_key.split(' | ')[0]
                product_only = strat_key.split(' | ')[1]
                series = summary_net.get(strat_name_only, {}).get(product_only, [])
                
                current_total = 0.0
                if series:
                    current_total = series[-1].get('net', 0.0)
                
                baseline = 0.0
                if start_time_str and series:
                    try:
                        # Handle varied ISO formats
                        clean_start = start_time_str.replace('Z', '').replace(' ', 'T')
                        start_dt = datetime.fromisoformat(clean_start)
                        for point in series:
                            p_time = point.get('t', '').replace('Z', '').replace(' ', 'T')
                            p_dt = datetime.fromisoformat(p_time)
                            if p_dt <= start_dt:
                                baseline = point.get('net', 0.0)
                            else:
                                break
                    except Exception as te:
                        print(f"[SYNC] Time err for {strat_key}: {te}")

                perf_diff = round(current_total - baseline, 2)
                
                # Evaluation: Pick the highest performer
                if perf_diff > max_perf_diff:
                    max_perf_diff = perf_diff
                    top_strat_record = {
                        "start_time": start_time_str or datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
                        "end_time": None,
                        "is_live": True,
                        "product": parsed['product'],
                        "strategy": parsed['strategy'],
                        "parm": parsed['parm'],
                        "signal": ["buy", "sell"],
                        "source": source_tag,
                        "actual_diff": perf_diff # Meta info
                    }

            # 5. Check if the winner meets the threshold
            if top_strat_record and max_perf_diff >= min_diff:
                print(f"[SYNC] Top performer found: {top_strat_record['product']} {top_strat_record['strategy']} ({max_perf_diff} >= {min_diff}). Activating.")
                new_active_list.append(top_strat_record)
            else:
                if top_strat_record:
                    print(f"[SYNC] Top performer ({max_perf_diff}) did not meet threshold ({min_diff}). Nothing activated.")
                else:
                    print(f"[SYNC] No valid performers found in bucket.")

        act_data['live'] = new_active_list
        
        # Atomic write
        tmp_path = act_file.with_suffix('.tmp')
        with open(tmp_path, 'w') as f:
            json.dump(act_data, f, indent=4)
        os.replace(tmp_path, act_file)
        
        # V20260123_0010: Logging sync result
        res_count = len([a for a in new_active_list if a.get('source') == source_tag])
        print(f"[SYNC] Bucket '{bucket_name}' sync complete. Live records: {res_count}")

    except Exception as e:
        print(f"[SYNC] Global error: {e}")


@app.route("/sidebar-loader.js")
def serve_sidebar_loader_js():
    return send_from_directory(ROOT_PATH, "sidebar-loader.js")


# ─────────────────────────────────────────────
# Trade Buckets API (File-Based) [V20260122_FS]
# ─────────────────────────────────────────────

def _get_trade_buckets_path(mode: str, date_str: str) -> Path:
    """Get path to trade buckets file."""
    return BASE_PATH / mode / date_str / "_trade_buckets.json"


def _load_trade_buckets(mode: str = 'live', date_str: str = None) -> dict:
    """Load trade buckets from JSON file."""
    if not date_str:
        date_str = datetime.now().strftime('%Y-%m-%d')

    bucket_file = _get_trade_buckets_path(mode, date_str)

    if bucket_file.exists():
        try:
            with open(bucket_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading trade buckets: {e}")

    return {"buckets": []}


def _save_trade_buckets(data: dict, mode: str = 'live', date_str: str = None):
    """Save trade buckets to JSON file."""
    if not date_str:
        date_str = datetime.now().strftime('%Y-%m-%d')

    bucket_file = _get_trade_buckets_path(mode, date_str)

    # Ensure directory exists
    bucket_file.parent.mkdir(parents=True, exist_ok=True)

    try:
        with open(bucket_file, 'w') as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"Error saving trade buckets: {e}")


@app.route('/api/trade_buckets', methods=['GET'])
def get_trade_buckets():
    """Get all trade buckets with stats."""
    mode = request.args.get('mode', 'live')
    date_str = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))

    data = _load_trade_buckets(mode=mode, date_str=date_str)
    buckets = data.get('buckets', [])

    # Load summary_net for calculating totals
    summary_file = BASE_PATH / mode / date_str / "_summary_net.json"
    summary_net = {}
    if summary_file.exists():
        try:
            with open(summary_file, 'r') as f:
                summary_data = json.load(f)
                summary_net = summary_data.get('strategies', {})
        except:
            pass

    # Update bucket stats from summary data
    for bucket in buckets:
        if 'open_trades' not in bucket:
            bucket['open_trades'] = False
        if 'open_trade_count' not in bucket:
            bucket['open_trade_count'] = 0
        if 'live' not in bucket:
            bucket['live'] = False

        start_dt = None
        start_time_str = bucket.get('start_time')
        if start_time_str:
            try:
                start_dt = datetime.fromisoformat(start_time_str.replace('Z', ''))
            except:
                pass

        for strat in bucket.get('strategies', []):
            strat_key = strat.get('key', '')
            parts = strat_key.split(' | ')
            if len(parts) == 2:
                strategy_name, product = parts
                series = summary_net.get(strategy_name, {}).get(product, [])

                current_total = 0.0
                if series:
                    current_total = series[-1].get('net', 0.0)

                baseline = 0.0
                if start_dt and series:
                    for point in series:
                        point_time_str = point.get('t', '')
                        try:
                            point_dt = datetime.fromisoformat(point_time_str.replace('Z', ''))
                            if point_dt <= start_dt:
                                baseline = point.get('net', 0.0)
                            else:
                                break
                        except:
                            pass

                strat['total_net'] = round(current_total - baseline, 2)

            if 'live_trade_net' not in strat:
                strat['live_trade_net'] = 0.0

    return jsonify({
        'success': True,
        'buckets': buckets,
        'max_strategies': 5
    })


@app.route('/api/trade_buckets', methods=['POST'])
def create_trade_bucket():
    """Create a new trade bucket."""
    try:
        import uuid
        payload = request.json
        name = payload.get('name')
        strategies = payload.get('strategies', [])
        mode = payload.get('mode', 'live')

        start_time_str = payload.get('start_time')
        current_date_str = datetime.now().strftime('%Y-%m-%d')

        if start_time_str:
            try:
                if start_time_str.endswith('Z'):
                    dt = datetime.fromisoformat(start_time_str[:-1])
                else:
                    dt = datetime.fromisoformat(start_time_str)
                current_date_str = dt.strftime('%Y-%m-%d')
            except:
                pass

        data = _load_trade_buckets(mode=mode, date_str=current_date_str)
        buckets = data.get('buckets', [])

        if not name:
            return jsonify({'success': False, 'message': 'Bucket name is required'}), 400

        if any(b['name'] == name for b in buckets):
            return jsonify({'success': False, 'message': 'Bucket with this name already exists'}), 400

        bucket_guid = str(uuid.uuid4())

        processed_strategies = []
        for strat in strategies:
            strategy_id = str(uuid.uuid4())
            if isinstance(strat, dict):
                strat['strategy_id'] = strategy_id
                processed_strategies.append(strat)
            else:
                processed_strategies.append({
                    'strategy_id': strategy_id,
                    'key': strat,
                    'total_net': 0.0,
                    'live_trade_net': 0.0
                })

        new_bucket = {
            'bucket_id': bucket_guid,
            'name': name,
            'start_time': payload.get('start_time') or datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'mode': mode,
            'strategies': processed_strategies,
            'live': False,
            'open_trades': False,
            'open_trade_count': 0,
            'minimum_difference': float(payload.get('minimum_difference', 5.0))
        }

        buckets.append(new_bucket)
        data['buckets'] = buckets

        _save_trade_buckets(data, mode=mode, date_str=current_date_str)

        return jsonify({'success': True, 'bucket': new_bucket})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/trade_buckets/update', methods=['POST'])
def update_trade_bucket():
    """Update bucket status (live/not live) or other fields."""
    try:
        payload = request.json
        name = payload.get('name')
        mode = payload.get('mode', 'live')
        date_str = payload.get('date', datetime.now().strftime('%Y-%m-%d'))

        if not name:
            return jsonify({'success': False, 'message': 'Bucket name is required'}), 400

        data = _load_trade_buckets(mode=mode, date_str=date_str)
        buckets = data.get('buckets', [])

        updated = False
        target_bucket = None

        for b in buckets:
            if b['name'] == name:
                target_bucket = b
                if 'live' in payload:
                    b['live'] = bool(payload['live'])
                    updated = True
                if 'minimum_difference' in payload:
                    b['minimum_difference'] = float(payload['minimum_difference'])
                    updated = True
                break

        if not target_bucket:
            return jsonify({'success': False, 'message': 'Bucket not found'}), 404

        if updated:
            _save_trade_buckets(data, mode=mode, date_str=date_str)
            # [V20260122_2230] Sync with activations_is_live.json
            _sync_bucket_to_activations(target_bucket, mode, date_str)

        return jsonify({'success': True, 'bucket': target_bucket})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/trade_buckets/<path:bucket_name>', methods=['DELETE'])
def delete_trade_bucket(bucket_name):
    """Delete a trade bucket."""
    try:
        mode = request.args.get('mode', 'live')
        date_str = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))

        data = _load_trade_buckets(mode=mode, date_str=date_str)
        buckets = data.get('buckets', [])

        initial_len = len(buckets)
        buckets = [b for b in buckets if b['name'] != bucket_name]

        if len(buckets) < initial_len:
            data['buckets'] = buckets
            _save_trade_buckets(data, mode=mode, date_str=date_str)
            # [V20260122_2230] Clear records from activations by syncing empty/dead state
            _sync_bucket_to_activations({'name': bucket_name, 'live': False}, mode, date_str)
            return jsonify({'success': True, 'message': 'Bucket deleted'})
        else:
            return jsonify({'success': False, 'message': 'Bucket not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


# Main
# -----------------------------------------------------------

@app.route('/api/grid_live', methods=['GET'])
def get_grid_live():
    """
    [V20260128_1428] Returns the current grid_live.json state for frontend restoration.
    """
    try:
        grid_live_file = ROOT_PATH / "grid_live.json"
        if grid_live_file.exists():
            with open(grid_live_file, "r") as f:
                data = json.load(f)
            return jsonify({'success': True, 'data': data})
        else:
            return jsonify({'success': True, 'data': {}})
    except Exception as e:
        print(f"[API-ERROR] GET /api/grid_live failed: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/grid_live', methods=['POST'])
def update_grid_live():
    """
    [V20260126_1430] Receives live monitoring state from the multi_chart UI
    and updates the grid_live.json file for the backend monitor to read.
    """
    try:
        payload = request.json
        group = payload.get('group')
        models = payload.get('models') # This will be the list of {model, product, metric}

        if not group:
            return jsonify({'success': False, 'message': 'Group name is required'}), 400

        # Define the path to grid_live.json relative to this script's location
        grid_live_file = ROOT_PATH / "grid_live.json"
        
        # [V20260128_1515] Use global thread lock to prevent race condition on file write
        with GRID_LIVE_LOCK:
            data = {}
            if grid_live_file.exists():
                try:
                    with open(grid_live_file, "r") as f:
                        data = json.load(f)
                    if not isinstance(data, dict):
                        data = {}
                except Exception:
                    data = {}
            
            # [V20260128_1615] Update data and inject/preserve activated_at timestamps
            if models:
                now_str = datetime.utcnow().isoformat()
                old_models = data.get(group, [])
                
                # Helper to find old timestamp for a model definition
                def get_old_ts(m):
                    for om in old_models:
                        if (om.get('model') == m.get('model') and 
                            om.get('product') == m.get('product') and 
                            om.get('metric') == m.get('metric')):
                            return om.get('activated_at')
                    return None

                for m in models:
                    ts = get_old_ts(m)
                    m['activated_at'] = ts if ts else now_str

                print(f"[API] Setting live models for group '{group}': {models}")
                data[group] = models
            elif group in data:
                print(f"[API] Deactivating live monitoring for group '{group}'.")
                del data[group]
            
            # Save data back to file
            with open(grid_live_file, "w") as f:
                json.dump(data, f, indent=4)
            
        # [V20260128_1155] Sync to activations.json for UI consistency
        _sync_grid_to_activations(data)
            
        return jsonify({'success': True, 'message': f'grid_live.json updated for group {group}.'})
        
    except Exception as e:
        print(f"[API-ERROR] /api/grid_live failed: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

def _sync_grid_to_activations(grid_data: dict):
    """
    Rebuilds the 'live' section of activations.json based on current grid_live.json state.
    Preserves manual flags where possible.
    """
    try:
        activations = _load_activations()
        old_live = activations.get('live', {})
        new_live = {}
        
        # 1. Flatten grid_data into a set of active (model, product, metric) tuples
        # grid_data: { "GroupName": [ {model, product, metric}, ... ] }
        
        active_definitions = {} # key -> { products: set(), metric_keys: set() }
        
        for group, models in grid_data.items():
            for m in models:
                model = m.get('model')
                product = m.get('product')
                metric = m.get('metric', 'net')
                
                # Determine activation key based on metric
                # Standard: just model name
                # Specific: model + suffix
                key = model
                if metric == 'buy_net': key += '_buy_net'
                elif metric == 'sell_net': key += '_sell_net'
                elif metric == 'alt': key += '_buy_alt' # Assuming alt maps generally to this, or just base key? 
                
                # Let's stick to base key if metric is net
                
                if key not in active_definitions:
                    active_definitions[key] = set()
                
                active_definitions[key].add(product)

        # 2. Construct new_live state
        now = datetime.utcnow().isoformat()
        
        for key, products in active_definitions.items():
            # Check if existed previously to preserve manual flag / original activation time
            old_entry = old_live.get(key, {})
            
            entry = {
                "active": True,
                "manual": old_entry.get('manual', False), # Preserve manual flag
                "activated_at": old_entry.get('activated_at') or now,
                "products": sorted(list(products))
            }
            new_live[key] = entry
            
        # 3. Save
        activations['live'] = new_live
        
        with open(ACTIVATIONS_FILE, "w") as f:
            json.dump(activations, f, indent=4)
            
        print(f"[SYNC] activations.json synced with grid_live.json. Active keys: {len(new_live)}")

    except Exception as e:
        print(f"[SYNC-ERROR] Failed to sync activations: {e}")


if __name__ == "__main__":
    print("Trade Viewer API (activation v2)")
    app.run(host="0.0.0.0", port=5000, debug=True)
