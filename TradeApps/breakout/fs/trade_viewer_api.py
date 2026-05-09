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
import time
from pathlib import Path
from datetime import datetime, timezone, timedelta
import re
import uuid
import shutil
import urllib.request # Switched to urllib for better compatibility
from typing import Dict, Any, List, Set, Tuple, Optional
from constants import VERSION # V20260105_2220
# V20260105_0025: Added /api/activations/remove endpoint
from market_update_generator import generate_market_update
from narrative_generator import add_narrative_routes
from social_publisher import add_social_routes
from subscriber_api import add_subscriber_routes
from json_layout import (
    configured_product_types,
    day_dir,
    default_product_type,
    ensure_day_dir,
    iter_day_dirs,
    load_layout_config,
    product_type_for_product,
    resolve_day_dir,
)
import common as breakout_common
from strategy_snapshot_15m_generator import OUTPUT_NAME as STRATEGY_SNAPSHOT_15M_OUTPUT
from strategy_snapshot_15m_generator import build_payload as build_strategy_snapshot_15m_payload
from strategy_snapshot_15m_generator import write_payload as write_strategy_snapshot_15m_payload

# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# Global Locks
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# [V20260128_1515] Lock for serializing access to grid_live.json
GRID_LIVE_LOCK = threading.Lock()
OPEN_TRADE_REFRESH_LOCK = threading.Lock()
_OPEN_TRADE_REFRESH_LAST_RUN: Dict[Tuple[str, str, str], float] = {}
REALTIME_STATS_CACHE_LOCK = threading.Lock()
REALTIME_TRADE_EXECUTION_LOCK = threading.Lock()
REALTIME_STATS_REFRESH_TRIGGER_LOCK = threading.Lock()
REALTIME_STATS_REFRESH_STATE: Dict[str, Any] = {
    "running": False,
    "last_started_at": None,
    "last_finished_at": None,
    "last_error": "",
}
REALTIME_STATS_CACHE_MEMORY: Dict[str, Any] = {}
REALTIME_STATS_CACHE_MEMORY_MTIME: Optional[float] = None
REALTIME_STATS_SNAPSHOT_INDEX_MEMORY: List[dict[str, Any]] = []
REALTIME_STATS_SNAPSHOT_INDEX_MEMORY_MTIME: Optional[float] = None

# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# App setup
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
app = Flask(__name__)
CORS(app)

# [V20260224] Add narrative generation routes for PipHunter
add_narrative_routes(app)

# [V20260224] Add social publishing routes for PipHunter
add_social_routes(app)

# [V20260224] Add subscriber management routes for PipHunter
add_subscriber_routes(app)

BASE_PATH = Path(r"C:\Users\edebe\eds\TradeApps\breakout\fs\json")
ROOT_PATH = BASE_PATH.parent
CONFIG_FILE = ROOT_PATH / "config.json"
ACTIVATIONS_FILE = ROOT_PATH / "activations.json"
WORKFLOWS_FILE = ROOT_PATH / "workflows.json"
WORKFLOW_MULTI_CHART_PAYLOAD_FILE = ROOT_PATH / "workflow_multi_chart_payload.json"
WEEKLY_PERFORMANCE_STATE_FILE = ROOT_PATH / "weekly_performance_state.json"
ACTIVATION_SUFFIXES = ("_buy_net", "_sell_net", "_buy_alt", "_sell_alt")
TOPX_AUDIT_VERSION = "V20260423_1529"
WORKFLOW_STRATEGY_GROUP_OPTIONS = ("breakout", "breakout_r", "breakout_rev", "breakout_r_rev")
REALTIME_STATS_CACHE_FILE = ROOT_PATH / "realtime_stats_cache.json"
REALTIME_STATS_SNAPSHOTS_FILE = ROOT_PATH / "realtime_stats_snapshots.json"
REALTIME_STATS_SNAPSHOT_INDEX_FILE = ROOT_PATH / "realtime_stats_snapshot_index.json"
REALTIME_STATS_SNAPSHOT_DIR = ROOT_PATH / "realtime_stats_snapshots"
REALTIME_STATS_CACHE_REFRESH_SECONDS = 60
REALTIME_STATS_SNAPSHOT_SECONDS = 300
REALTIME_STATS_MAX_SNAPSHOTS = 288
REALTIME_TRADE_EXECUTION_STORE_FILE = ROOT_PATH / "realtime_trade_execution_store.json"
REALTIME_TRADE_EXECUTION_DEFAULT_COST_PIPS = 3.0
REALTIME_TRADE_SIGNAL_MIN_COUNT = 10
REALTIME_TRADE_SIGNAL_STALE_SECONDS = 60
REALTIME_TRADE_CLOSE_AVAILABLE_POLICIES = ("opposite_signal", "net_pips_after_cost_threshold")
REALTIME_STATS_WINDOWS = [
    {"key": "m5", "label": "Last 5 Min", "minutes": 5, "accent": "#4ade80"},
    {"key": "m30", "label": "Last 30 Min", "minutes": 30, "accent": "#38bdf8"},
    {"key": "h1", "label": "Last 1 Hour", "minutes": 60, "accent": "#c084fc"},
    {"key": "h3", "label": "Last 3 Hours", "minutes": 180, "accent": "#f59e0b"},
]
REALTIME_STATS_GROUP_OPTIONS = [
    {"key": "all", "label": "All"},
    {"key": "momentum", "label": "Momentum"},
    {"key": "momentum_r", "label": "Momentum R"},
    {"key": "breakout", "label": "Breakout"},
    {"key": "breakout_r", "label": "Breakout R"},
    {"key": "breakout_rev", "label": "Breakout Rev"},
    {"key": "breakout_r_rev", "label": "Breakout R Rev"},
]
REALTIME_STATS_GROUP_MAP = {item["key"]: item for item in REALTIME_STATS_GROUP_OPTIONS}
REALTIME_STATS_ROW_DEFS = {
    "open_buy": {"title": "Open Buy Trades", "status": "OPEN", "direction": "LONG", "accent": "#4ade80", "icon": "arrow-up-right", "tag": "Buy"},
    "open_sell": {"title": "Open Sell Trades", "status": "OPEN", "direction": "SHORT", "accent": "#f87171", "icon": "arrow-down-right", "tag": "Sell"},
    "closed_buy": {"title": "Closed Buy Trades", "status": "CLOSED", "direction": "LONG", "accent": "#60a5fa", "icon": "circle-check", "tag": "Buy"},
    "closed_sell": {"title": "Closed Sell Trades", "status": "CLOSED", "direction": "SHORT", "accent": "#f59e0b", "icon": "badge-check", "tag": "Sell"},
}


def _load_layout_runtime_config() -> dict:
    cfg = load_layout_config(CONFIG_FILE)
    cfg.setdefault("product_type", default_product_type(cfg))
    cfg.setdefault("product_types", configured_product_types(cfg))
    cfg.setdefault("product_type_by_product", {})
    return cfg


def _strip_activation_suffix(key: str) -> str:
    raw_key = str(key or "")
    for suffix in ACTIVATION_SUFFIXES:
        if raw_key.endswith(suffix):
            return raw_key[: -len(suffix)]
    return raw_key


def _strategy_model_from_activation_key(key: str) -> str:
    base = _strip_activation_suffix(key)
    # UI keys can be duplicated like breakout_breakout_R_2_tp20.0_sl5.0_buy_net.
    for idx, ch in enumerate(base):
        if ch != "_":
            continue
        prefix = base[:idx]
        remainder = base[idx + 1 :]
        if prefix and remainder.startswith(prefix + "_"):
            return remainder
    return base


def _sync_weekly_activation_to_grid_live(
    *,
    mode: str,
    model: str,
    product: str,
    requested_active: bool,
    manual: bool,
) -> None:
    if not model or not product:
        return

    grid_live_file = ROOT_PATH / "grid_live.json"
    normalized_mode = str(mode or "live").lower()
    normalized_product = str(product).strip().upper()
    source = "weekly_performance"
    group = "weekly_performance"

    with GRID_LIVE_LOCK:
        full_data = {"live": [], "sim": []}
        if grid_live_file.exists():
            try:
                with open(grid_live_file, "r") as f:
                    loaded = json.load(f)
                if isinstance(loaded, list):
                    full_data["live"] = loaded
                elif isinstance(loaded, dict):
                    full_data = loaded
                    full_data.setdefault("live", [])
                    full_data.setdefault("sim", [])
            except Exception:
                pass

        target_list = list(full_data.get(normalized_mode, []))
        filtered = [
            item
            for item in target_list
            if not (
                str(item.get("source") or "") == source
                and str(item.get("model") or "") == model
                and str(item.get("product") or "").upper() == normalized_product
            )
        ]

        if requested_active:
            existing = next(
                (
                    item
                    for item in target_list
                    if str(item.get("source") or "") == source
                    and str(item.get("model") or "") == model
                    and str(item.get("product") or "").upper() == normalized_product
                ),
                {},
            )
            filtered.append(
                {
                    "model": model,
                    "product": normalized_product,
                    "metric": "net",
                    "group": group,
                    "source": source,
                    "manual": bool(manual),
                    "activated_at": existing.get("activated_at") or datetime.now().isoformat(),
                }
            )

        def _material_signature(items: List[Dict[str, Any]]) -> List[Tuple[str, str, str, str]]:
            return sorted(
                (
                    str(x.get("model", "")),
                    str(x.get("product", "")),
                    str(x.get("metric", "")),
                    str(x.get("source", "")),
                )
                for x in items
            )

        if _material_signature(target_list) == _material_signature(filtered):
            return

        # [V20260424_2310] Pass current state for conditional archiving
        _archive_grid_live(normalized_mode, new_data=full_data)
        full_data[normalized_mode] = filtered
        with open(grid_live_file, "w") as f:
            json.dump(full_data, f, indent=4)
        _sync_grid_to_activations(filtered, mode=normalized_mode)


def _infer_product_type(product: str | None = None) -> str:
    return product_type_for_product(product, _load_layout_runtime_config())


def _resolve_refresh_products(
    cfg: Dict[str, Any],
    product: Optional[str] = None,
    product_type: Optional[str] = None,
) -> List[str]:
    if product and product not in ('all', 'undefined', 'null'):
        return [str(product).upper()]

    products = [str(p).upper() for p in cfg.get('trade_products', []) if p]
    if product_type and product_type not in ('all', 'undefined', 'null'):
        wanted = str(product_type).strip().lower()
        products = [p for p in products if product_type_for_product(p, cfg) == wanted]
    return products


def _refresh_open_trade_files(
    mode: str,
    date_str: str,
    product: Optional[str] = None,
    product_type: Optional[str] = None,
    force: bool = False,
) -> None:
    """Refresh persisted OPEN trade files from live quotes as an API-side fallback."""
    run_mode = str(mode or 'live').lower()
    scope_key = str(product or product_type or 'all').upper()
    throttle_key = (run_mode, str(date_str), scope_key)
    now_monotonic = time.monotonic()

    if not force:
        last_run = _OPEN_TRADE_REFRESH_LAST_RUN.get(throttle_key)
        if last_run is not None and (now_monotonic - last_run) < 2.0:
            return

    if not OPEN_TRADE_REFRESH_LOCK.acquire(blocking=False):
        return

    try:
        cfg = breakout_common._load_config()
        refresh_products = _resolve_refresh_products(cfg, product=product, product_type=product_type)
        if not refresh_products:
            return

        latest_prices: Dict[str, Dict[str, Optional[float]]] = {}
        breakout_common._LATEST_TRADING_DATE = date_str

        for prod in refresh_products:
            try:
                quotes = breakout_common.fetch_latest_quotes(prod)
                if not quotes:
                    continue
                latest = quotes[-1]
                latest_prices[prod.upper()] = {
                    'price': latest.price,
                    'bid': latest.bid,
                    'ask': latest.ask,
                }
            except Exception as exc:
                print(f"[OPEN-REFRESH] Failed quote fetch for {prod}: {exc}")

        if not latest_prices:
            return

        breakout_common._update_open_trade_json_prices(str(BASE_PATH / run_mode), latest_prices, cfg)
        _OPEN_TRADE_REFRESH_LAST_RUN[throttle_key] = now_monotonic
    except Exception as exc:
        print(f"[OPEN-REFRESH] Refresh failed: {exc}")
    finally:
        OPEN_TRADE_REFRESH_LOCK.release()


def _open_trade_refresh_worker() -> None:
    """Continuously refresh OPEN trade files from the API process."""
    while True:
        sleep_seconds = 5
        try:
            cfg = breakout_common._load_config()
            run_mode = str(cfg.get('run_mode', 'live')).lower()
            sleep_seconds = max(1, int(cfg.get('sleep_time', 5)))
            _refresh_open_trade_files(run_mode, datetime.now().strftime('%Y-%m-%d'), force=True)
        except Exception as exc:
            print(f"[OPEN-REFRESH] Worker error: {exc}")
        time.sleep(sleep_seconds)


def _start_open_trade_refresh_worker() -> None:
    t = threading.Thread(target=_open_trade_refresh_worker, daemon=True, name="open-trade-refresh-worker")
    t.start()


def _trade_quantity_for_product(product: str | None = None, cfg: Optional[Dict[str, Any]] = None) -> int:
    cfg = cfg or _load_layout_runtime_config()
    raw_by_product = cfg.get('min_value_by_product', {})
    product_key = str(product or '').strip().upper()
    if isinstance(raw_by_product, dict) and product_key:
        raw_value = raw_by_product.get(product_key)
        if raw_value not in (None, ''):
            try:
                return max(1, int(round(float(raw_value) * 1000.0)))
            except (TypeError, ValueError):
                pass

    raw_by_type = cfg.get('min_value_by_product_type', {})
    product_type = _infer_product_type(product)
    if isinstance(raw_by_type, dict):
        raw_value = raw_by_type.get(str(product_type).strip().lower())
        if raw_value not in (None, ''):
            try:
                return max(1, int(round(float(raw_value) * 1000.0)))
            except (TypeError, ValueError):
                pass

    raw_default = cfg.get('default_min_value')
    if raw_default not in (None, ''):
        try:
            return max(1, int(round(float(raw_default) * 1000.0)))
        except (TypeError, ValueError):
            pass

    default_pct = float(cfg.get('trade_qty_percent', 45.0))
    pct = float(cfg.get('crypto_trade_qty_percent', default_pct)) if _infer_product_type(product) == 'crypto' else default_pct
    return int(100000 * (pct / 100.0))


def _resolve_day_dir(mode: str, date_str: str, product: str | None = None, product_type: str | None = None) -> Path:
    cfg = _load_layout_runtime_config()
    resolved_type = product_type or (product_type_for_product(product, cfg) if product else cfg.get("product_type"))
    return resolve_day_dir(BASE_PATH, mode, date_str, resolved_type)


def _ensure_day_dir(mode: str, date_str: str, product: str | None = None, product_type: str | None = None) -> Path:
    cfg = _load_layout_runtime_config()
    resolved_type = product_type or (product_type_for_product(product, cfg) if product else cfg.get("product_type"))
    return ensure_day_dir(BASE_PATH, mode, date_str, config=cfg, product=product, product_type=resolved_type)


def _iter_day_dirs_for(mode: str, date_str: str, product_type: str | None = None) -> list[Path]:
    if product_type:
        resolved = _resolve_day_dir(mode, date_str, product_type=product_type)
        return [resolved] if resolved.exists() else []
    return iter_day_dirs(BASE_PATH, mode, date_str, config=_load_layout_runtime_config())


def _iter_trade_json_files(day_dir: Path, include_archived_closed: bool = False, product_hint: str | None = None):
    """
    [V20260424_2155] Optimized trade file iterator using os.scandir.
    Avoids glob/rglob overhead and string parsing for non-relevant files.
    """
    if not day_dir.exists():
        return

    seen = set()
    product_hint_lower = product_hint.lower() if product_hint else None

    # Step 1: Scan top-level files
    try:
        with os.scandir(day_dir) as it:
            for entry in it:
                if entry.is_file() and entry.name.endswith(".json"):
                    if entry.name.startswith('_'): continue
                    if product_hint_lower and product_hint_lower not in entry.name.lower(): continue

                    seen.add(entry.path)
                    yield Path(entry.path)
    except:
        pass

    if not include_archived_closed:
        return

    # Step 2: Recursive scan for archived trades
    archive_dir = day_dir / 'archive'
    if not archive_dir.exists():
        return

    def _scan_recursive(target):
        try:
            with os.scandir(target) as it:
                for entry in it:
                    if entry.is_dir():
                        yield from _scan_recursive(entry.path)
                    elif entry.is_file() and entry.name.endswith(".json"):
                        if entry.name.startswith('_'): continue
                        if not entry.name.lower().endswith(('_cl.json', '_cld.json')): continue
                        if product_hint_lower and product_hint_lower not in entry.name.lower(): continue

                        if entry.path not in seen:
                            seen.add(entry.path)
                            yield Path(entry.path)
        except:
            pass

    yield from _scan_recursive(archive_dir)

# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# API Endpoints
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
@app.route('/api/trade_file', methods=['GET'])
def get_trade_file():
    """Load raw content of a specific trade JSON file [V20251230_0010] [V20260122_FS]"""
    try:
        run_mode = request.args.get('mode', 'live')
        date = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))
        product = request.args.get('product')
        product_type = request.args.get('product_type')
        _refresh_open_trade_files(run_mode, date, product=product, product_type=product_type)
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

        candidate_day_dirs = _iter_day_dirs_for(run_mode, date, product_type)
        preferred_day_dir = _resolve_day_dir(run_mode, date, product=product, product_type=product_type)
        if preferred_day_dir not in candidate_day_dirs:
            candidate_day_dirs.insert(0, preferred_day_dir)
        file_path = None
        for candidate in candidate_names:
            for day_dir in candidate_day_dirs:
                for p in (day_dir / candidate, day_dir / 'virtual' / candidate):
                    if p.exists():
                        file_path = p
                        safe_name = candidate
                        break
                if file_path:
                    break
            if file_path:
                break

            for day_dir in candidate_day_dirs:
                for archived_file in _iter_trade_json_files(day_dir, include_archived_closed=True):
                    if archived_file.name == candidate:
                        file_path = archived_file
                        safe_name = candidate
                        break
                if file_path:
                    break
            if file_path:
                break

        # [V20260122_FS] Robust search: If no path found and 'filename' looks like an ID, search directory
        if not file_path and (filename.isdigit() or len(filename) < 10):
            print(f"[TRADE_FILE] Explicit match failed for {filename}, searching directory {date}...")
            for day_dir in candidate_day_dirs:
                search_dirs = [day_dir, day_dir / 'virtual']
                for s_dir in search_dirs:
                    if not s_dir.exists():
                        continue
                    for json_file in s_dir.glob('*.json'):
                        if filename in json_file.name:
                            try:
                                with open(json_file, 'r') as f:
                                    data = json.load(f)
                                    if str(data.get('trade_id')) == str(filename):
                                        file_path = json_file
                                        break
                            except:
                                continue
                    if file_path:
                        break
                if file_path:
                    break

            if not file_path:
                for day_dir in candidate_day_dirs:
                    for json_file in _iter_trade_json_files(day_dir, include_archived_closed=True):
                        if filename not in json_file.name:
                            continue
                        try:
                            with open(json_file, 'r') as f:
                                data = json.load(f)
                                if str(data.get('trade_id')) == str(filename):
                                    file_path = json_file
                                    break
                        except:
                            continue
                    if file_path:
                        break

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


@app.route('/api/workflows', methods=['GET'])
def get_workflows():
    """Workflow automation definitions and runtime state."""
    try:
        data = _load_workflows()
        workflows = data.get("workflows", [])
        enriched = []
        for w in workflows:
            if not isinstance(w, dict):
                continue
            item = dict(w)
            item["active_now"] = _workflow_active_now(item)
            enriched.append(item)

        # Persist defaults if file missing/outdated
        if not WORKFLOWS_FILE.exists():
            save_payload = dict(data)
            save_payload["workflows"] = workflows
            _save_workflows(save_payload)

        return jsonify({"success": True, "workflows": enriched, "updated_at": data.get("updated_at")})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route('/api/workflows/update', methods=['POST'])
def update_workflow():
    """Update one workflow schedule/toggle settings."""
    try:
        payload = request.json or {}
        workflow_id = str(payload.get("id") or "").strip()
        if not workflow_id:
            return jsonify({"success": False, "message": "id is required"}), 400

        data = _load_workflows()
        workflows = data.get("workflows", [])
        target = None
        for w in workflows:
            if isinstance(w, dict) and str(w.get("id")) == workflow_id:
                target = w
                break
        if target is None:
            return jsonify({"success": False, "message": "Workflow not found"}), 404

        if "enabled" in payload:
            target["enabled"] = bool(payload.get("enabled"))

        if "start_time" in payload:
            st = str(payload.get("start_time") or "").strip()
            if _hhmm_to_minutes(st) is None:
                return jsonify({"success": False, "message": "start_time must be HH:MM"}), 400
            target["start_time"] = st

        if "end_time" in payload:
            et = str(payload.get("end_time") or "").strip()
            if _hhmm_to_minutes(et) is None:
                return jsonify({"success": False, "message": "end_time must be HH:MM"}), 400
            target["end_time"] = et

        if "config" in payload:
            cfg_in = payload.get("config")
            if not isinstance(cfg_in, dict):
                return jsonify({"success": False, "message": "config must be object"}), 400
            cfg_existing = target.get("config", {}) if isinstance(target.get("config"), dict) else {}
            cfg_merged = dict(cfg_existing)
            for k, v in cfg_in.items():
                cfg_merged[str(k)] = v
            target["config"] = cfg_merged

        target["updated_at"] = datetime.now().isoformat()
        data["workflows"] = workflows
        _save_workflows(data)

        out = dict(target)
        out["active_now"] = _workflow_active_now(out)
        return jsonify({"success": True, "workflow": out})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route('/api/workflows/run', methods=['POST'])
def run_workflow_now():
    """Run one workflow immediately (manual trigger)."""
    try:
        payload = request.json or {}
        workflow_id = str(payload.get("id") or "").strip()
        mode = str(payload.get("mode") or "").strip().lower()
        date_str = str(payload.get("date") or "").strip()
        if not workflow_id:
            return jsonify({"success": False, "message": "id is required"}), 400

        cfg_live = _load_config_safe()
        if mode not in ("live", "sim"):
            mode = str(cfg_live.get("run_mode", "live")).lower()
            if mode not in ("live", "sim"):
                mode = "live"
        if not date_str:
            date_str = datetime.now().strftime("%Y-%m-%d")

        workflows_data = _load_workflows()
        workflows = workflows_data.get("workflows", [])
        wf = next((w for w in workflows if isinstance(w, dict) and str(w.get("id")) == workflow_id), None)
        if wf is None:
            return jsonify({"success": False, "message": "Workflow not found"}), 404

        if workflow_id == "TB_workflow":
            result = _run_tb_workflow_once(mode, date_str, wf)
        elif workflow_id == "profile_match_workflow":
            result = _run_profile_match_workflow_once(mode, date_str, wf)
        elif workflow_id == "top_x_multi_chart_workflow":
            result = _run_top_x_multi_chart_workflow(mode, date_str, wf)
        elif workflow_id == "multi_chart_prune_negative_non_live":
            result = {
                "success": True,
                "message": "Client-side workflow. It runs inside multi_chart every minute when enabled."
            }
        elif workflow_id == "tb_prune_all_negative":
            result = _run_tb_prune_all_negative_once(mode, date_str, wf)
        else:
            return jsonify({"success": False, "message": f"Run-now not supported for workflow '{workflow_id}'"}), 400

        _WORKFLOW_LAST_RUN[workflow_id] = time.time()
        return jsonify({"success": bool(result.get("success")), "result": result})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

def _strip_trade_suffix(filename: str) -> str:
    name = os.path.basename(filename)
    # [V20260129_0130] Pre-clean double extensions like .json.json
    while name.lower().endswith('.json.json'):
        name = name[:-5]
        
    if not name.lower().endswith('.json'):
        name = f"{name}.json"
        
    for suffix in ('_cld.json', '_cl.json', '_op.json'):
        if name.lower().endswith(suffix):
            return name[:-len(suffix)] + '.json'
    return name



def _update_automated_source(source_name: str):
    """Update automated_trade_source in config.json. [V20260205_2100]"""
    try:
        if not CONFIG_FILE.exists():
            return
        with open(CONFIG_FILE, "r") as f:
            cfg = json.load(f)
        
        changed = False
        if cfg.get('automated_trade_source') != source_name:
            cfg['automated_trade_source'] = source_name
            changed = True
        current_multi = cfg.get('automated_trade_sources')
        if not isinstance(current_multi, list):
            current_multi = [cfg.get('automated_trade_source')] if cfg.get('automated_trade_source') else []
        normalized = []
        for s in current_multi:
            if isinstance(s, str) and s.strip():
                sv = s.strip()
                if sv not in normalized:
                    normalized.append(sv)
        if source_name not in normalized:
            normalized.append(source_name)
            changed = True
        cfg['automated_trade_sources'] = normalized
        if changed:
            with open(CONFIG_FILE, "w") as f:
                json.dump(cfg, f, indent=4)
            print(f"[CONFIG] automated_trade_source(s) updated: single={source_name}, multi={normalized}")
    except Exception as e:
        print(f"[ERROR] Failed to update automated_trade_source: {e}")

def _is_source_allowed(requested_source: str) -> bool:
    """Check if the requested automated source is allowed. [V20260205_2100]"""
    try:
        if not CONFIG_FILE.exists():
            return True # Default to allowed if no config
        with open(CONFIG_FILE, "r") as f:
            cfg = json.load(f)
        
        current_multi = cfg.get('automated_trade_sources')
        if isinstance(current_multi, list):
            allowed = [str(s).strip() for s in current_multi if isinstance(s, str) and str(s).strip()]
            if allowed:
                return requested_source in allowed
        current_source = cfg.get('automated_trade_source')
        if not current_source:
            return True
        return current_source == requested_source
    except Exception as e:
        print(f"[ERROR] Failed to check automated_trade_source: {e}")
        return True

def _load_trade_products() -> Set[str]:
    try:
        with open(CONFIG_FILE, "r") as f:
            cfg = json.load(f)
        return {p.upper() for p in cfg.get("trade_products", []) if isinstance(p, str)}
    except Exception:
        return set()


def _normalize_workflow_product_types(cfg: Optional[dict]) -> List[str]:
    config = cfg if isinstance(cfg, dict) else {}
    raw_types = config.get("product_types")
    normalized: List[str] = []
    if isinstance(raw_types, list):
        for item in raw_types:
            val = str(item or "").strip().lower()
            if val and val not in normalized:
                normalized.append(val)
    raw_single = str(config.get("product_type") or "").strip().lower()
    if raw_single and raw_single not in normalized:
        normalized.append(raw_single)
    if not normalized:
        normalized.append(default_product_type(_load_layout_runtime_config()))
    return normalized


def _normalize_workflow_strategy_groups(cfg: Optional[dict]) -> List[str]:
    config = cfg if isinstance(cfg, dict) else {}
    raw_groups = config.get("strategy_groups")
    normalized: List[str] = []
    if isinstance(raw_groups, list):
        for item in raw_groups:
            val = str(item or "").strip().lower()
            if val in WORKFLOW_STRATEGY_GROUP_OPTIONS and val not in normalized:
                normalized.append(val)
    return normalized


def _workflow_strategy_group_for_model(model_name: str) -> Optional[str]:
    name = str(model_name or "").strip().lower()
    if not name:
        return None
    if name.startswith("breakout_r_rev_") or name == "breakout_r_rev":
        return "breakout_r_rev"
    if name.startswith("breakout_rev_") or name == "breakout_rev":
        return "breakout_rev"
    if name.startswith("breakout_r_") or name == "breakout_r":
        return "breakout_r"
    if name.startswith("breakout_") or name == "breakout":
        return "breakout"
    return None


def _workflow_strategy_group_allowed(model_name: str, selected_groups: Optional[List[str]]) -> bool:
    groups = selected_groups or []
    if not groups:
        return True
    return _workflow_strategy_group_for_model(model_name) in groups


def _default_workflows_payload() -> dict:
    return {
        "version": "V20260216_0010",
        "updated_at": datetime.now().isoformat(),
        "workflows": [
            {
                "id": "TB_workflow",
                "name": "TB_workflow",
                "description": "Auto pipeline: pick top Summary row, expand same-parameter family, optimize start-from range, save+activate TB.",
                "enabled": False,
                "start_time": "00:00",
                "end_time": "23:59",
                "timezone": "local",
                "steps": [
                    "Select best Performance Summary Breakdown row by total net",
                    "Send selection to Multi Chart and add all same-parameter strategies/metrics",
                    "Adjust start-from so max net range is under configured threshold",
                    "Save as Trade Bucket and activate"
                ],
                "config": {
                    "metric": "net",
                    "delta_type": "delta2",
                    "product_type": "forex",
                    "product_types": ["forex"],
                    "strategy_groups": [],
                    "trade_alt_net": False,
                    "max_range_target": 150,
                    "minimum_difference": 5.0,
                    "run_interval_sec": 900,
                    "max_buckets_per_day": 3,
                    "min_profitability_pct": 80.0,
                    "min_trade_count": 10,
                    "max_strategies_per_card": 4
                }
            },
            {
                "id": "profile_match_workflow",
                "name": "profile_match_workflow",
                "description": "Find current strategy/product pairs above profitability threshold and push to Multi Charts feed.",
                "enabled": False,
                "start_time": "00:00",
                "end_time": "23:59",
                "timezone": "local",
                "steps": [
                    "Scan current Top20 strategies for profitability >= threshold",
                    "Filter by minimum trade count, min total net >= X, and min avg net >= X",
                    "Optionally expand to all same-parameter strategies/metrics when preparing Multi Chart payload",
                    "Optionally adjust start-time baseline so highest net range is under 150 before TB send",
                    "Send matching strategy/product pairs to Multi Charts import payload"
                ],
                "config": {
                    "min_profitability_pct": 85.0,
                    "min_trade_count": 1,
                    "min_total_net": 0.0,
                    "min_avg_net": 0.0,
                    "max_items": 20,
                    "metric": "net",
                    "delta_type": "delta2",
                    "product_type": "forex",
                    "product_types": ["forex"],
                    "strategy_groups": [],
                    "trade_alt_net": False,
                    "scalper_only": False,
                    "enforce_market_bias": False,
                    "bias_recent_profitable_count": 2,
                    "add_to_tb": False,
                    "add_same_parameter_strategies_metrics": False,
                    "adjust_start_time_under_150": False,
                    "run_interval_sec": 300
                }
            },
            {
                "id": "multi_chart_prune_negative_non_live",
                "name": "multi_chart_prune_negative_non_live",
                "description": "Scan multi-chart every minute and remove non-live cards only when all chart sums(net) in the card are negative.",
                "enabled": False,
                "start_time": "00:00",
                "end_time": "23:59",
                "timezone": "local",
                "steps": [
                    "Scan visible Multi Chart cards every minute",
                    "Skip cards currently LIVE",
                    "Remove cards where all sum(net) values are negative"
                ],
                "config": {
                    "run_interval_sec": 60,
                    "product_type": "forex",
                    "negative_threshold": 0
                }
            },
            {
                "id": "tb_prune_all_negative",
                "name": "tb_prune_all_negative",
                "description": "Every minute, remove trade buckets where all strategy net values are below threshold.",
                "enabled": False,
                "start_time": "00:00",
                "end_time": "23:59",
                "timezone": "local",
                "steps": [
                    "Scan trade buckets for current mode/date",
                    "Evaluate strategy nets inside each bucket",
                    "Delete bucket if all strategy nets are below threshold"
                ],
                "config": {
                    "run_interval_sec": 60,
                    "product_type": "forex",
                    "negative_threshold": -20
                }
            },
            {
                "id": "top_x_multi_chart_workflow",
                "name": "Top X Multi-Chart Loader",
                "description": "Extracts the Top X (by total net) strategies from the Top 20 list and forces them into the Multi-Chart view.",
                "enabled": False,
                "start_time": "00:00",
                "end_time": "23:59",
                "timezone": "local",
                "steps": [
                    "Fetch the current mode/date Top 20 strategies",
                    "Filter by Scalper and/or Rev Scalper type if selected",
                    "Sort the filtered list descending by Total Net",
                    "Select exactly Top X strategies from the sorted list",
                    "Optionally add the best matching strategy to TB and activate",
                    "Optionally include all same-parameter strategies/metrics in the Multi-Chart payload",
                    "Send the matching strategies to the Multi Charts import payload"
                ],
                "config": {
                    "top_x": 6,
                    "metric": "net",
                    "delta_type": "delta2",
                    "product_type": "forex",
                    "product_types": ["forex"],
                    "strategy_groups": [],
                    "trade_alt_net": False,
                    "include_scalper": True,
                    "include_rev_scalper": True,
                    "add_to_tb": False,
                    "add_same_parameter_strategies_metrics": False,
                    "merge_charts": False,
                    "run_interval_sec": 300
                }
            }
        ]
    }

def _load_workflows() -> dict:
    if WORKFLOWS_FILE.exists():
        try:
            with open(WORKFLOWS_FILE, "r") as f:
                data = json.load(f)
            if not isinstance(data, dict):
                data = {}
        except Exception:
            data = {}
    else:
        data = {}

    defaults = _default_workflows_payload()
    workflows = data.get("workflows")
    if not isinstance(workflows, list):
        workflows = []

    existing_ids = {str(w.get("id")) for w in workflows if isinstance(w, dict)}
    for d in defaults["workflows"]:
        if d["id"] not in existing_ids:
            workflows.append(d)

    out = {
        "version": data.get("version") or defaults["version"],
        "updated_at": data.get("updated_at") or datetime.now().isoformat(),
        "workflows": workflows
    }
    return out


def _save_workflows(payload: dict):
    payload = payload or {}
    payload["updated_at"] = datetime.now().isoformat()
    with open(WORKFLOWS_FILE, "w") as f:
        json.dump(payload, f, indent=4)


def _hhmm_to_minutes(hhmm: str) -> Optional[int]:
    s = str(hhmm or "").strip()
    m = re.fullmatch(r"([01]\d|2[0-3]):([0-5]\d)", s)
    if not m:
        return None
    return int(m.group(1)) * 60 + int(m.group(2))


def _workflow_active_now(workflow: dict) -> bool:
    if not bool(workflow.get("enabled")):
        return False
    start_m = _hhmm_to_minutes(workflow.get("start_time"))
    end_m = _hhmm_to_minutes(workflow.get("end_time"))
    if start_m is None or end_m is None:
        return False
    now = datetime.now()
    now_m = now.hour * 60 + now.minute
    if start_m <= end_m:
        return start_m <= now_m <= end_m
    # Overnight window (e.g. 22:00 -> 02:00)
    return now_m >= start_m or now_m <= end_m


def _parse_model_signature(model_name: str) -> Tuple[str, str]:
    """
    Split model into base + param-signature.
    Example: breakout_R_3_tp10.0_sl50.0 -> (breakout_R, 3_tp10.0_sl50.0)
    """
    s = str(model_name or "").strip()
    m = re.search(r"(_\d+)?_tp[\d\.]+_sl[\d\.]+$", s)
    if not m:
        return s, "default"
    suffix = s[m.start() + 1:]
    base = s[:m.start()]
    return base, suffix


def _series_value_at_or_before(series: List[dict], target_dt: datetime, field: str = "net") -> float:
    """[V20260311_1215] Get value for a specific field at or before target datetime."""
    v = 0.0
    for p in series:
        ts = p.get("t")
        if not ts:
            continue
        try:
            p_dt = datetime.fromisoformat(str(ts).replace("Z", ""))
        except Exception:
            continue
        if p_dt <= target_dt:
            try:
                # [V20260311_1345] Use the specified field (net, buy_net, sell_net, alt_net)
                v = float(p.get(field, p.get("net", 0.0)) or 0.0)
            except Exception:
                v = 0.0
        else:
            break
    return v


def _select_tb_workflow_candidate(mode: str, date_str: str, wf_cfg: Optional[dict] = None) -> Optional[dict]:
    """
    Step 1 + 2 selector:
    - Pick best model/product by latest total net
    - Expand to all model/product pairs with same params signature.
    """
    wf_cfg = wf_cfg or {}
    product_type = str(wf_cfg.get("product_type") or "").strip().lower() or None
    min_profitability = float(wf_cfg.get("min_profitability_pct", 80.0) or 80.0)
    min_trade_count = int(wf_cfg.get("min_trade_count", 10) or 10)
    max_card_strategies = int(wf_cfg.get("max_strategies_per_card", 4) or 4)

    # [V20260317_1105] Load all matching summary data
    strategies: Dict[str, dict] = {}
    for day_dir in _iter_day_dirs_for(mode, date_str, product_type):
        summary_file = day_dir / "_summary_net.json"
        if summary_file.exists():
            try:
                with open(summary_file, "r") as f:
                    s_data = json.load(f) or {}
                    s_strats = s_data.get("strategies", {})
                    if isinstance(s_strats, dict):
                        for m_name, products in s_strats.items():
                            if m_name not in strategies:
                                strategies[m_name] = {}
                            strategies[m_name].update(products)
            except Exception:
                pass

    if not strategies:
        return None

    # Choose one best "card" candidate from top20 with profitability/trade-count gating.
    # [V20260317_1105] Load all matching top20 entries
    best = None
    candidates = []
    for day_dir in _iter_day_dirs_for(mode, date_str, product_type):
        top20_file = day_dir / "_top20.json"
        if top20_file.exists():
            try:
                with open(top20_file, "r") as f:
                    top20 = (json.load(f) or {}).get("top20", [])
                for r in top20:
                    if not isinstance(r, dict):
                        continue
                    strategy = str(r.get("strategy") or "").strip()
                    product = str(r.get("product") or "").strip()
                    trade_count = int(r.get("trade_count", 0) or 0)
                    buy_count = int(r.get("buy_count", 0) or 0)
                    sell_count = int(r.get("sell_count", 0) or 0)
                    buy_pct = float(r.get("buyPercent", 0.0) or 0.0)
                    sell_pct = float(r.get("sellPercent", 0.0) or 0.0)
                    total_net = float(r.get("total_net", 0.0) or 0.0)
                    denom = max(1, buy_count + sell_count)
                    profitability = ((buy_pct * buy_count) + (sell_pct * sell_count)) / denom
                    if trade_count < min_trade_count:
                        continue
                    if profitability < min_profitability:
                        continue
                    candidates.append({
                        "model": strategy,
                        "product": product,
                        "net": total_net,
                        "trade_count": trade_count,
                        "profitability": profitability
                    })
            except Exception:
                pass

    # Fallback if top20 unavailable/empty: pick best latest-net from summary.
    if not candidates:
        for model, products in strategies.items():
            if not isinstance(products, dict):
                continue
            for product, series in products.items():
                if not isinstance(series, list) or not series:
                    continue
                try:
                    net = float(series[-1].get("net", 0.0) or 0.0)
                except Exception:
                    net = 0.0
                candidates.append({
                    "model": model,
                    "product": product,
                    "net": net,
                    "trade_count": 0,
                    "profitability": 0.0
                })

    if not candidates:
        return None

    candidates.sort(key=lambda x: (x["net"], x["profitability"], x["trade_count"]), reverse=True)
    best = candidates[0]

    _, sig = _parse_model_signature(best["model"])
    product_scope = str(best["product"]).upper()

    # 1-card scope: same params signature + same product only, capped to max_strategies_per_card.
    family_all = []
    for model, products in strategies.items():
        if not isinstance(products, dict):
            continue
        _, model_sig = _parse_model_signature(model)
        if model_sig != sig:
            continue
        for product, series in products.items():
            if str(product).upper() != product_scope:
                continue
            if not isinstance(series, list) or not series:
                continue
            try:
                latest_net = float(series[-1].get("net", 0.0) or 0.0)
            except Exception:
                latest_net = 0.0
            family_all.append({"model": model, "product": product, "series": series, "latest_net": latest_net})

    family_all.sort(key=lambda x: x.get("latest_net", 0.0), reverse=True)
    family = family_all[:max(1, max_card_strategies)]

    return {
        "best": best,
        "base": _parse_model_signature(best["model"])[0],
        "sig": sig,
        "family": family
    }


def _optimize_start_from_for_range(family: List[dict], target_max: float) -> Tuple[Optional[datetime], Optional[datetime]]:
    """
    Step 3 optimizer:
    choose earliest start_dt where max(current_net - start_net) across family <= target_max.
    Returns (start_dt, eval_dt).
    """
    timestamps = []
    for item in family:
        for p in item.get("series", []):
            ts = p.get("t")
            if not ts:
                continue
            try:
                timestamps.append(datetime.fromisoformat(str(ts).replace("Z", "")))
            except Exception:
                pass
    if not timestamps:
        return None, None

    timestamps = sorted(set(timestamps))
    eval_dt = timestamps[-1]

    def max_range_from(start_dt: datetime) -> float:
        max_delta = 0.0
        for item in family:
            series = item.get("series", [])
            start_net = _series_value_at_or_before(series, start_dt)
            end_net = _series_value_at_or_before(series, eval_dt)
            d = end_net - start_net
            if d > max_delta:
                max_delta = d
        return max_delta

    chosen = None
    for t in timestamps:
        if max_range_from(t) <= float(target_max):
            chosen = t
            break
    if chosen is None:
        # fallback to latest timestamp; yields smallest range.
        chosen = eval_dt
    return chosen, eval_dt


def _run_tb_workflow_once(mode: str, date_str: str, wf: dict) -> dict:
    """
    Execute TB_workflow:
    1) choose best summary row
    2) add all same-parameter strategies
    3) optimize start-from range <= target
    4) save+activate TB
    """
    cfg = wf.get("config", {}) if isinstance(wf, dict) else {}
    target_max = float(cfg.get("max_range_target", 150) or 150)
    min_diff = float(cfg.get("minimum_difference", 5.0) or 5.0)

    selected = _select_tb_workflow_candidate(mode, date_str, cfg)
    if not selected:
        return {"success": False, "message": "No summary candidate found"}
    bias_at_creation = _get_current_bias(mode, date_str) or "UNKNOWN"

    family = selected["family"]
    if not family:
        return {"success": False, "message": "No same-parameter family found"}

    start_from_dt, eval_dt = _optimize_start_from_for_range(family, target_max)
    if not start_from_dt or not eval_dt:
        return {"success": False, "message": "No usable timeline points"}

    now = datetime.now()
    mmdd = now.strftime("%m%d")
    hhmmss_mmm = now.strftime("%H%M%S") + f"_{int(now.microsecond/1000):03d}"
    base = selected.get("base") or "model"
    sig = selected.get("sig") or "default"
    product = str(selected.get("best", {}).get("product") or "MIX").upper()
    bucket_name = f"AUTO_TB_{mmdd}_{hhmmss_mmm}_{product}_{base}_{sig}".replace(" ", "")

    data = _load_trade_buckets(mode=mode, date_str=date_str)
    buckets = data.get("buckets", [])
    if any(str(b.get("name")) == bucket_name for b in buckets):
        return {"success": False, "message": "Bucket already exists"}

    processed_strategies = []
    # [V20260311_1215] If family has only 1 strategy, split into Buy and Sell to satisfy "no single row" rule.
    if len(family) == 1:
        item = family[0]
        model = str(item.get("model") or "").strip()
        product = str(item.get("product") or "").strip()
        series = item.get("series") or []
        
        for m_type, m_field in [("buy_net", "buy_net"), ("sell_net", "sell_net")]:
            creation_net = round(_series_value_at_or_before(series, eval_dt, field=m_field), 2)
            start_from_net = round(_series_value_at_or_before(series, start_from_dt, field=m_field), 2)
            processed_strategies.append({
                "strategy_id": str(uuid.uuid4()),
                "key": f"{model} | {product}",
                "metric": m_type,
                "bias_at_creation": bias_at_creation,
                "start_from_net": start_from_net,
                "net_at_creation": creation_net,
                "current_total_net": creation_net,
                "start_net_delta_from_chart": round(creation_net - start_from_net, 2),
                "current_net_from_chart": round(creation_net - start_from_net, 2),
                "net_delta_from_creation": 0.0,
                "total_net": 0.0,
                "live_trade_net": 0.0
            })
    else:
        for item in family:
            model = str(item.get("model") or "").strip()
            product = str(item.get("product") or "").strip()
            series = item.get("series") or []
            if not model or not product:
                continue
            creation_net = round(_series_value_at_or_before(series, eval_dt), 2)
            start_from_net = round(_series_value_at_or_before(series, start_from_dt), 2)
            processed_strategies.append({
                "strategy_id": str(uuid.uuid4()),
                "key": f"{model} | {product}",
                "metric": "net",
                "bias_at_creation": bias_at_creation,
                "start_from_net": start_from_net,
                "net_at_creation": creation_net,
                "current_total_net": creation_net,
                "start_net_delta_from_chart": round(creation_net - start_from_net, 2),
                "current_net_from_chart": round(creation_net - start_from_net, 2),
                "net_delta_from_creation": 0.0,
                "total_net": 0.0,
                "live_trade_net": 0.0
            })

    # [V20260311_1345] Deduplicate by strategy+product+metric to ensure real diversity
    seen_strategies = set()
    deduped_strategies = []
    for s in processed_strategies:
        d_key = f"{s.get('key')}|{s.get('metric')}"
        if d_key not in seen_strategies:
            seen_strategies.add(d_key)
            deduped_strategies.append(s)
    processed_strategies = deduped_strategies

    if len(processed_strategies) < 2:
        # If we still have only 1 after dedup, force a Buy/Sell split if it was 'net' [V20260311_1345]
        if len(processed_strategies) == 1 and processed_strategies[0]['metric'] == 'net':
            s = processed_strategies[0]
            processed_strategies = []
            model_key = s.get('key')
            parts = model_key.split(' | ')
            if len(parts) == 2:
                model_name, product_name = parts[0].strip(), parts[1].strip()
                series = summary_data.get("strategies", {}).get(model_name, {}).get(product_name, [])
                for m_type in ("buy_net", "sell_net"):
                    c_net = round(_series_value_at_or_before(series, eval_dt, field=m_type), 2)
                    s_net = round(_series_value_at_or_before(series, start_from_dt, field=m_type), 2)
                    processed_strategies.append({
                        "strategy_id": str(uuid.uuid4()),
                        "key": model_key,
                        "metric": m_type,
                        "bias_at_creation": bias_at_creation,
                        "start_from_net": s_net,
                        "net_at_creation": c_net,
                        "current_total_net": c_net,
                        "start_net_delta_from_chart": round(c_net - s_net, 2),
                        "current_net_from_chart": round(c_net - s_net, 2),
                        "net_delta_from_creation": 0.0,
                        "total_net": 0.0,
                        "live_trade_net": 0.0
                    })

    if len(processed_strategies) < 2:
        return {"success": False, "message": "Minimum 2 unique strategies/metrics required for a Trade Bucket [V20260311_1345]"}

    new_bucket = {
        "bucket_id": str(uuid.uuid4()),
        "name": bucket_name,
        "start_time": now.isoformat(),
        "chart_start_time": start_from_dt.isoformat(),
        "mode": mode,
        "market_bias_at_creation": bias_at_creation,
        "strategies": processed_strategies,
        "live": True,
        "open_trades": False,
        "open_trade_count": 0,
        "minimum_difference": float(min_diff),
        "created_by_workflow": "TB_workflow"
    }

    buckets.append(new_bucket)
    data["buckets"] = buckets
    _save_trade_buckets(data, mode=mode, date_str=date_str)

    # activate into grid
    _sync_bucket_to_grid_live(new_bucket, mode, date_str)
    _update_automated_source("Trade Bucket")

    return {
        "success": True,
        "bucket_name": bucket_name,
        "family_size": len(processed_strategies),
        "selected_model": selected.get("best", {}).get("model"),
        "selected_product": selected.get("best", {}).get("product"),
        "start_from_time": start_from_dt.isoformat(),
        "created_time": eval_dt.isoformat()
    }


def _run_profile_match_workflow_once(mode: str, date_str: str, wf: dict) -> dict:
    cfg = wf.get("config", {}) if isinstance(wf, dict) else {}
    product_types = _normalize_workflow_product_types(cfg)
    strategy_groups = _normalize_workflow_strategy_groups(cfg)
    if not bool(cfg.get("_single_product_type_run")) and len(product_types) > 1:
        aggregate_items: List[dict] = []
        aggregate_tb: List[dict] = []
        successes = 0
        for pt in product_types:
            wf_copy = json.loads(json.dumps(wf))
            wf_cfg = wf_copy.setdefault("config", {})
            wf_cfg["product_type"] = pt
            wf_cfg["product_types"] = [pt]
            wf_cfg["_single_product_type_run"] = True
            result = _run_profile_match_workflow_once(mode, date_str, wf_copy)
            payload = None
            if WORKFLOW_MULTI_CHART_PAYLOAD_FILE.exists():
                try:
                    with open(WORKFLOW_MULTI_CHART_PAYLOAD_FILE, "r") as f:
                        payload = json.load(f) or {}
                except Exception:
                    payload = None
            if payload and isinstance(payload.get("items"), list):
                aggregate_items.extend(payload.get("items", []))
            if isinstance(result.get("tb"), dict):
                aggregate_tb.append({"product_type": pt, **result.get("tb")})
            if bool(result.get("success")):
                successes += 1

        if aggregate_items:
            merged_payload = {
                "source": "profile_match_workflow",
                "mode": mode,
                "date": date_str,
                "preferred_metric": str(cfg.get("metric", "net") or "net").lower(),
                "delta_type": _normalize_delta_type(cfg.get("delta_type")),
                "group": f"WF_PROFILE_MULTI_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "preset_name": f"WF_PROFILE_MULTI_{'_'.join(product_types).upper()}",
                "created_at": datetime.now().isoformat(),
                "run_id": f"{mode}_{date_str}_{int(time.time())}_profile_multi",
                "product_types": product_types,
                "strategy_groups": strategy_groups,
                "items": aggregate_items
            }
            with open(WORKFLOW_MULTI_CHART_PAYLOAD_FILE, "w") as f:
                json.dump(merged_payload, f, indent=4)
        return {
            "success": successes > 0,
            "message": f"Processed profile_match_workflow for {len(product_types)} product types.",
            "product_types": product_types,
            "pushed": len(aggregate_items),
            "tb": {"details": aggregate_tb}
        }
    product_type = str(cfg.get("product_type") or "").strip().lower() or None
    delta_type = _normalize_delta_type(cfg.get("delta_type"))
    min_profitability = float(cfg.get("min_profitability_pct", 85.0) or 85.0)
    min_trade_count = int(cfg.get("min_trade_count", 10) or 10)
    min_total_net = float(cfg.get("min_total_net", 0.0) or 0.0)
    min_avg_net = float(cfg.get("min_avg_net", 0.0) or 0.0)
    max_items = int(cfg.get("max_items", 20) or 20)
    metric_cfg = str(cfg.get("metric", "net") or "net").lower()
    scalper_only = bool(cfg.get("scalper_only", False))
    rev_scalper_only = bool(cfg.get("rev_scalper_only", False))
    enforce_market_bias = bool(cfg.get("enforce_market_bias", False))
    try:
        bias_recent_profitable_count = int(cfg.get("bias_recent_profitable_count", 2) or 2)
    except Exception:
        bias_recent_profitable_count = 2
    bias_recent_profitable_count = max(1, bias_recent_profitable_count)
    add_to_tb = bool(cfg.get("add_to_tb", False))
    add_same_parameter = bool(cfg.get("add_same_parameter_strategies_metrics", False))
    adjust_start_time_under_150 = bool(cfg.get("adjust_start_time_under_150", False))
    current_bias = str(_get_current_bias(mode, date_str) or "").upper()

    trades_summary_rows: List[dict] = []
    # [V20260317_1105] Multi-dir support via product_type
    for day_dir in _iter_day_dirs_for(mode, date_str, product_type):
        summary_file = day_dir / "_trades_summary.json"
        if summary_file.exists():
            try:
                with open(summary_file, "r") as f:
                    d = json.load(f) or {}
                rows = d.get("trades", [])
                if isinstance(rows, list):
                    trades_summary_rows.extend([r for r in rows if isinstance(r, dict)])
            except Exception:
                pass

    def _passes_bias_recent_two_profitable(model_name: str, product_name: str) -> bool:
        if not enforce_market_bias:
            return True
        if current_bias not in ("BUY", "SELL"):
            return False
        side = "LONG" if current_bias == "BUY" else "SHORT"
        candidates_rows = []
        for t in trades_summary_rows:
            app = str(t.get("app_name") or t.get("script_name") or "").strip()
            prod = str(t.get("product") or "").strip().upper()
            if app != str(model_name).strip() or prod != str(product_name).strip().upper():
                continue
            if str(t.get("status") or "").upper() != "CLOSED":
                continue
            d = str(t.get("direction") or "").upper()
            if side == "LONG" and "LONG" not in d:
                continue
            if side == "SHORT" and "SHORT" not in d:
                continue
            candidates_rows.append(t)
        if len(candidates_rows) < bias_recent_profitable_count:
            return False
        candidates_rows.sort(key=lambda x: str(x.get("entry_time") or x.get("exit_time") or ""), reverse=True)
        last_n = candidates_rows[:bias_recent_profitable_count]
        return all(float(r.get("net_return", 0.0) or 0.0) > 0 for r in last_n)

    scalper_models: Set[str] = set()

    # [V20260317_1105] Load scalper status from targeted strategies (multi-dir)
    for day_dir in _iter_day_dirs_for(mode, date_str, product_type):
        targeted_file = day_dir / "_targeted_strategies.json"
        if targeted_file.exists():
            try:
                with open(targeted_file, "r") as f:
                    targeted = json.load(f) or {}
                for s in (targeted.get("strategies") or []):
                    if isinstance(s, dict) and bool(s.get("scalper")):
                        model = str(s.get("strategy") or "").strip()
                        if model:
                            scalper_models.add(model)
            except Exception:
                pass

    _sr = 5.0
    _rsr = 2.0
    _cfg_path = BASE_PATH / "config.json"
    if _cfg_path.exists():
        try:
            with open(_cfg_path, "r") as f:
                _c = json.load(f)
                _sr = float(_c.get("scalper_ratio", 5.0))
                _rsr = float(_c.get("rev_scalper_ratio", 2.0))
        except: pass

    def _looks_like_scalper(model_name: str) -> bool:
        s = str(model_name or "").lower()
        tp_match = re.search(r'tp([\d.]+)', s)
        sl_match = re.search(r'sl([\d.]+)', s)
        if tp_match and sl_match:
            try:
                tp_val = float(tp_match.group(1))
                sl_val = float(sl_match.group(1))
                if tp_val > 0 and sl_val >= tp_val * _sr:
                    return True
            except: pass
        return ("scalp" in s) or ("_s_" in s) or s.endswith("_s")

    def _looks_like_rev_scalper(model_name: str) -> bool:
        s = str(model_name or "").lower()
        tp_match = re.search(r'tp([\d.]+)', s)
        sl_match = re.search(r'sl([\d.]+)', s)
        if tp_match and sl_match:
            try:
                tp_val = float(tp_match.group(1))
                sl_val = float(sl_match.group(1))
                if sl_val > 0 and tp_val >= sl_val * _rsr:
                    return True
            except: pass
        return False

    # [V20260317_1105] Multi-dir top20 load
    top20_rows = []
    for day_dir in _iter_day_dirs_for(mode, date_str, product_type):
        top20_file = day_dir / "_top20.json"
        if top20_file.exists():
            try:
                with open(top20_file, "r") as f:
                    batch = (json.load(f) or {}).get("top20", [])
                    if isinstance(batch, list):
                        top20_rows.extend(batch)
            except Exception:
                pass

    if not top20_rows:
        return {"success": False, "message": f"top20 data not found for {product_type or 'all'}"}

    candidates = []
    seen = set()
    for r in top20_rows:
        if not isinstance(r, dict):
            continue
        model = str(r.get("strategy") or "").strip()
        product = str(r.get("product") or "").strip().upper()
        if not model or not product:
            continue
        if not _workflow_strategy_group_allowed(model, strategy_groups):
            continue
        if scalper_only and rev_scalper_only:
            is_scalper = (model in scalper_models) or _looks_like_scalper(model)
            is_rev = _looks_like_rev_scalper(model)
            if not is_scalper and not is_rev:
                continue
        elif scalper_only:
            is_scalper = (model in scalper_models) or _looks_like_scalper(model)
            if not is_scalper:
                continue
        elif rev_scalper_only:
            is_rev = _looks_like_rev_scalper(model)
            if not is_rev:
                continue
        key = (model, product)
        if key in seen:
            continue
        seen.add(key)

        buy_count = int(r.get("buy_count", 0) or 0)
        sell_count = int(r.get("sell_count", 0) or 0)
        trade_count = int(r.get("trade_count", buy_count + sell_count) or 0)
        if trade_count < min_trade_count:
            continue

        buy_pct = float(r.get("buyPercent", 0.0) or 0.0)
        sell_pct = float(r.get("sellPercent", 0.0) or 0.0)
        denom = max(1, buy_count + sell_count)
        profitability = ((buy_pct * buy_count) + (sell_pct * sell_count)) / denom
        if profitability < min_profitability:
            continue

        total_net = float(r.get("total_net", 0.0) or 0.0)
        if total_net <= 0:
            continue
        if total_net < min_total_net:
            continue
        avg_net = float(r.get("avg_net", 0.0) or 0.0)
        if avg_net == 0.0:
            avg_net = (total_net / trade_count) if trade_count > 0 else 0.0
        if avg_net < min_avg_net:
            continue
        if not _passes_bias_recent_two_profitable(model, product):
            continue
        candidates.append({
            "model": model,
            "product": product,
            "trade_count": trade_count,
            "profitability": profitability,
            "total_net": total_net,
            "avg_net": avg_net
        })

    if not candidates:
        return {"success": False, "message": "no strategies matched threshold"}

    candidates.sort(key=lambda x: (x["profitability"], x["total_net"], x["trade_count"]), reverse=True)
    picked = candidates[:max(1, max_items)]

    summary_strategies: Dict[str, Dict[str, List[dict]]] = {}
    summary_net_file = _resolve_day_dir(mode, date_str) / "_summary_net.json"
    if summary_net_file.exists():
        try:
            with open(summary_net_file, "r") as f:
                summary_strategies = (json.load(f) or {}).get("strategies", {}) or {}
        except Exception:
            summary_strategies = {}

    def _series_for(model_name: str, product_name: str) -> List[dict]:
        try:
            products = summary_strategies.get(str(model_name), {})
            if isinstance(products, dict):
                series = products.get(str(product_name))
                if isinstance(series, list):
                    return series
        except Exception:
            pass
        return []

    def _family_for_same_param(model_name: str, product_name: str) -> List[dict]:
        _, sig = _parse_model_signature(model_name)
        product_scope = str(product_name).upper()
        out = []
        for model, products in summary_strategies.items():
            if not isinstance(products, dict):
                continue
            _, model_sig = _parse_model_signature(str(model))
            if model_sig != sig:
                continue
            for product, series in products.items():
                if str(product).upper() != product_scope:
                    continue
                if not isinstance(series, list) or not series:
                    continue
                try:
                    latest_net = float(series[-1].get("net", 0.0) or 0.0)
                except Exception:
                    latest_net = 0.0
                out.append({
                    "model": str(model),
                    "product": str(product).upper(),
                    "series": series,
                    "latest_net": latest_net
                })
        out.sort(key=lambda x: x.get("latest_net", 0.0), reverse=True)
        return out

    if metric_cfg == "bias_side":
        bias = str(_get_current_bias(mode, date_str) or "").upper()
        metric = "buy_net" if bias == "BUY" else ("sell_net" if bias == "SELL" else "net")
    else:
        metric = metric_cfg if metric_cfg in ("net", "buy_net", "sell_net") else "net"

    now_dt = datetime.now()
    now_local = now_dt.isoformat().split(".")[0]
    hhmmss = now_dt.strftime("%H%M%S")
    group_name = f"WF_PROFILE_{(product_type or 'all').upper()}_{date_str}_{int(min_profitability)}_{hhmmss}"
    payload_items = []
    payload_seen: Set[str] = set()
    for item in picked:
        model = str(item["model"])
        product = str(item["product"]).upper()
        if add_same_parameter:
            expanded = _family_for_same_param(model, product)
            if not expanded:
                expanded = [{"model": model, "product": product, "series": _series_for(model, product)}]
        else:
            expanded = [{"model": model, "product": product, "series": _series_for(model, product)}]

        for m in expanded:
            m_model = str(m.get("model") or "").strip()
            m_product = str(m.get("product") or "").strip().upper()
            if not m_model or not m_product:
                continue
            if not _workflow_strategy_group_allowed(m_model, strategy_groups):
                continue
            # Enforce net filters for expanded family members too.
            # This prevents negative/low-net same-parameter members from being pushed to multi_chart.
            m_latest_net = None
            try:
                if isinstance(m.get("series"), list) and m.get("series"):
                    m_latest_net = float(m["series"][-1].get("net", 0.0) or 0.0)
                else:
                    m_latest_net = float(m.get("latest_net", 0.0) or 0.0)
            except Exception:
                m_latest_net = 0.0
            if m_latest_net <= 0:
                continue
            if m_latest_net < min_total_net:
                continue
            dedup_key = f"{m_model}|{m_product}".lower()
            if dedup_key in payload_seen:
                continue
            payload_seen.add(dedup_key)

            safe_model = re.sub(r'[^A-Za-z0-9_]+', '_', m_model).strip('_')
            safe_product = re.sub(r'[^A-Za-z0-9_]+', '_', m_product).strip('_')
            per_card_group = f"{group_name}_{safe_product}_{safe_model}"
            payload_items.append({
                "strategy": m_model,
                "product": m_product,
                "product_type": product_type,
                "group": per_card_group,
                "parm_raw": ""
            })

    payload = {
        "source": "profile_match_workflow",
        "mode": mode,
        "date": date_str,
        "preferred_metric": metric,
        "delta_type": delta_type,
        "group": group_name,
        "preset_name": group_name,
        "created_at": now_local,
        "run_id": f"{mode}_{date_str}_{int(time.time())}",
        "product_types": [product_type] if product_type else [],
        "strategy_groups": strategy_groups,
        "items": payload_items
    }
    try:
        with open(WORKFLOW_MULTI_CHART_PAYLOAD_FILE, "w") as f:
            json.dump(payload, f, indent=4)
    except Exception as e:
        return {"success": False, "message": f"failed to write multi-chart payload: {e}"}

    tb_result = {
        "requested": add_to_tb,
        "created": False,
        "activated": False,
        "reason": "not_requested"
    }
    if add_to_tb and picked:
        trade_alt_net = bool(cfg.get("trade_alt_net", False))
        max_live_tb = _get_max_live_tb()
        tb_data = _load_trade_buckets(mode=mode, date_str=date_str, product_type=product_type)
        tb_buckets = tb_data.get("buckets", [])
        def _norm_key(model_name: str, product_name: str) -> str:
            m = str(model_name or "").strip().lower()
            p = str(product_name or "").strip().upper()
            return f"{m}|{p}"

        existing_keys: Set[str] = set()
        for b in tb_buckets:
            if not isinstance(b, dict):
                continue
            for s in (b.get("strategies") or []):
                if not isinstance(s, dict):
                    continue
                key_raw = str(s.get("key") or "")
                parts = key_raw.split(" | ") if " | " in key_raw else key_raw.split("|")
                if len(parts) == 2:
                    existing_keys.add(_norm_key(parts[0], parts[1]))
        live_count = sum(1 for b in tb_buckets if isinstance(b, dict) and bool(b.get("live")))
        if live_count >= max_live_tb:
            tb_result = {
                "requested": True,
                "created": False,
                "activated": False,
                "reason": f"max_live_tb_reached ({live_count}/{max_live_tb})"
            }
        else:
            tb_results_list = []
            
            for candidate in picked:
                if live_count >= max_live_tb:
                    tb_results_list.append({"requested": True, "created": False, "reason": f"max_live_tb_reached ({live_count}/{max_live_tb})"})
                    break
                    
                c_model = str(candidate.get("model") or "")
                c_prod = str(candidate.get("product") or "").upper()
                if _norm_key(c_model, c_prod) in existing_keys:
                    tb_results_list.append({"requested": True, "created": False, "reason": "already_exists"})
                    continue
                    
                if add_same_parameter:
                    c_family = _family_for_same_param(c_model, c_prod)
                else:
                    c_family = [{
                        "model": c_model, 
                        "product": c_prod, 
                        "series": candidate.get("series", []),
                        "latest_net": float(candidate.get("latest_net", 0.0) or 0.0)
                    }]
                
                if len(c_family) >= 1:
                    pre_tb_family = c_family
                    best_model = c_model
                    best_product = c_prod

                    now_dt = datetime.now()
                    mmdd = now_dt.strftime("%m%d")
                    hhmmss_mmm = now_dt.strftime("%H%M%S") + f"_{int(now_dt.microsecond/1000):03d}"
                    safe_product = re.sub(r'[^A-Za-z0-9_]+', '_', best_product).strip('_').upper()
                    safe_model = re.sub(r'[^A-Za-z0-9_]+', '_', best_model).strip('_')
                    bucket_name = f"AUTO_TB_{mmdd}_{hhmmss_mmm}_{safe_product}_{safe_model}".replace(" ", "")
                    bias_at_creation = _get_current_bias(mode, date_str) or "UNKNOWN"
                    total_net = round(float(candidate.get("total_net", 0.0) or 0.0), 2)
                    min_diff = float(cfg.get("minimum_difference", 5.0) or 5.0)
                    requested_metric = str(cfg.get("metric", "net") or "net").strip()

                    start_from_dt = now_dt
                    eval_dt = now_dt
                    if adjust_start_time_under_150:
                        family_with_series = [f for f in pre_tb_family if isinstance(f.get("series"), list) and f.get("series")]
                        if family_with_series:
                            s_dt, e_dt = _optimize_start_from_for_range(family_with_series, 150.0)
                            if s_dt and e_dt:
                                start_from_dt = s_dt
                                eval_dt = e_dt

                    processed_strategies = []
                    # [V20260311_1215] Forced split for single-strategy family OR buy_sell metric
                    should_split = (len(pre_tb_family) == 1) or (requested_metric == "buy_sell")

                    for fam in pre_tb_family:
                        fm = str(fam.get("model") or "").strip()
                        fp = str(fam.get("product") or "").strip().upper()
                        if not fm or not fp:
                            continue

                        series = fam.get("series") if isinstance(fam.get("series"), list) else []
                        
                        # [V20260323_1510] Filter expansion members for positive net in TB
                        f_latest_net = float(fam.get("latest_net", 0.0) or 0.0)
                        if f_latest_net <= 0:
                            continue
                        if bool(cfg.get("require_positive_total_net", True)):
                            try:
                                f_total_net = float(series[-1].get("net", 0.0) or 0.0) if series else f_latest_net
                            except: f_total_net = f_latest_net
                            if f_total_net <= 0:
                                continue
                        
                        metrics_to_add = [("buy_net", "buy_net"), ("sell_net", "sell_net")] if should_split else [("net", "net")]
                        
                        for m_type, m_field in metrics_to_add:
                            if series and adjust_start_time_under_150:
                                creation_net = round(_series_value_at_or_before(series, eval_dt, field=m_field), 2)
                                start_from_net = round(_series_value_at_or_before(series, start_from_dt, field=m_field), 2)
                            else:
                                creation_net = round(float(fam.get("latest_net", total_net) or 0.0), 2)
                                start_from_net = creation_net

                            processed_strategies.append({
                                "strategy_id": str(uuid.uuid4()),
                                "key": f"{fm} | {fp}",
                                "metric": m_type,
                                "bias_at_creation": bias_at_creation,
                                "start_from_net": start_from_net,
                                "net_at_creation": creation_net,
                                "current_total_net": creation_net,
                                "start_net_delta_from_chart": round(creation_net - start_from_net, 2),
                                "current_net_from_chart": round(creation_net - start_from_net, 2),
                                "net_delta_from_creation": 0.0,
                                "total_net": 0.0,
                                "delta_type": delta_type,
                                "live_trade_net": 0.0
                            })
                    
                    if len(processed_strategies) < 2:
                        tb_results_list.append({"requested": True, "created": False, "reason": "min_rows_violation_len1_no_split"})
                        continue

                    new_bucket = {
                        "bucket_id": str(uuid.uuid4()),
                        "name": bucket_name,
                        "date": date_str,
                        "mode": mode,
                        "product_type": product_type,
                        "trade_alt_net": trade_alt_net,
                        "market_bias_at_creation": bias_at_creation,
                        "metric": cfg.get("metric", "net"),
                        "delta_type": delta_type,
                        "chart_start_time": start_from_dt.isoformat(),
                        "start_time": eval_dt.isoformat(),
                        "strategies": processed_strategies,
                        "live": True,
                        "open_trades": False,
                        "open_trade_count": 0,
                        "minimum_difference": float(min_diff),
                        "created_by_workflow": "profile_match_workflow"
                    }

                    tb_buckets.append(new_bucket)
                    existing_keys.add(_norm_key(best_model, best_product))
                    live_count += 1
                    
                    _sync_bucket_to_grid_live(new_bucket, mode, date_str, product_type=product_type)

                    tb_results_list.append({
                        "requested": True,
                        "created": True,
                        "activated": True,
                        "bucket_name": bucket_name,
                        "family_size": len(processed_strategies),
                        "reason": "success"
                    })
                else:
                    tb_results_list.append({"requested": True, "created": False, "reason": "no_candidate_found_for_tb"})

            if any(r.get("created") for r in tb_results_list):
                tb_data["buckets"] = tb_buckets
                _save_trade_buckets(tb_data, mode=mode, date_str=date_str, product_type=product_type)
                _update_automated_source("Trade Bucket")
                tb_result = {
                    "requested": True,
                    "created": True,
                    "activated": True,
                    "reason": "ok",
                    "bucket_name": bucket_name
                }

    return {
        "success": True,
        "matched": len(candidates),
        "pushed": len(payload_items),
        "metric": metric,
        "group": group_name,
        "scalper_only": scalper_only,
        "rev_scalper_only": rev_scalper_only,
        "enforce_market_bias": enforce_market_bias,
        "bias_recent_profitable_count": bias_recent_profitable_count,
        "min_total_net": min_total_net,
        "min_avg_net": min_avg_net,
        "strategy_groups": strategy_groups,
        "add_same_parameter_strategies_metrics": add_same_parameter,
        "adjust_start_time_under_150": adjust_start_time_under_150,
        "delta_type": delta_type,
        "target": "multi_chart_payload",
        "tb": tb_result
    }

def _run_top_x_multi_chart_workflow(mode: str, date_str: str, wf: dict) -> dict:
    cfg = wf.get("config", {}) if isinstance(wf, dict) else {}
    product_types = _normalize_workflow_product_types(cfg)
    strategy_groups = _normalize_workflow_strategy_groups(cfg)
    if not bool(cfg.get("_single_product_type_run")) and len(product_types) > 1:
        aggregate_items: List[dict] = []
        aggregate_tb: List[dict] = []
        successes = 0
        for pt in product_types:
            wf_copy = json.loads(json.dumps(wf))
            wf_cfg = wf_copy.setdefault("config", {})
            wf_cfg["product_type"] = pt
            wf_cfg["product_types"] = [pt]
            wf_cfg["_single_product_type_run"] = True
            result = _run_top_x_multi_chart_workflow(mode, date_str, wf_copy)
            payload = None
            if WORKFLOW_MULTI_CHART_PAYLOAD_FILE.exists():
                try:
                    with open(WORKFLOW_MULTI_CHART_PAYLOAD_FILE, "r") as f:
                        payload = json.load(f) or {}
                except Exception:
                    payload = None
            if payload and isinstance(payload.get("items"), list):
                aggregate_items.extend(payload.get("items", []))
            if isinstance(result.get("tb"), dict):
                aggregate_tb.append({"product_type": pt, **result.get("tb")})
            if bool(result.get("success")):
                successes += 1
        merged_payload = {
            "source": "top_x_multi_chart_workflow",
            "mode": mode,
            "date": date_str,
            "preferred_metric": str(cfg.get("metric", "net") or "net").lower(),
            "delta_type": _normalize_delta_type(cfg.get("delta_type")),
            "group": f"WF_TOPX_MULTI_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "preset_name": f"WF_TOPX_MULTI_{'_'.join(product_types).upper()}",
            "created_at": datetime.now().isoformat(),
            "run_id": f"{mode}_{date_str}_{int(time.time())}_topx_multi",
            "product_types": product_types,
            "strategy_groups": strategy_groups,
            "merge_charts": bool(cfg.get("merge_charts", False)),
            "items": aggregate_items
        }
        with open(WORKFLOW_MULTI_CHART_PAYLOAD_FILE, "w") as f:
            json.dump(merged_payload, f, indent=4)
        return {
            "success": successes > 0,
            "message": f"Processed top_x_multi_chart_workflow for {len(product_types)} product types.",
            "product_types": product_types,
            "payload_items": len(aggregate_items),
            "tb": {"details": aggregate_tb}
        }
    product_type = str(cfg.get("product_type") or "").strip().lower() or None
    delta_type = _normalize_delta_type(cfg.get("delta_type"))
    top_x = int(cfg.get("top_x", 6) or 6)
    include_scalper = bool(cfg.get("include_scalper", True))
    include_rev_scalper = bool(cfg.get("include_rev_scalper", True))
    add_to_tb = bool(cfg.get("add_to_tb", False))
    t_split_for_tb = bool(cfg.get("t_split_for_tb", False))
    add_same_parameter = bool(cfg.get("add_same_parameter_strategies_metrics", False))
    merge_charts = bool(cfg.get("merge_charts", False))
    require_pick_now = bool(cfg.get("require_pick_now", False))
    # [V20260306_1845] Metric type selector: net, buy_net, sell_net, buy_sell
    selected_metric = str(cfg.get("metric", "net") or "net").strip()
    # Map metric to the _top20.json field name used for sorting
    _METRIC_SORT_FIELD = {
        "net": "total_net",
        "buy_net": "buy_net",
        "sell_net": "sell_net",
        "buy_sell": "total_net"  # buy_sell sorts by total_net but displays both
    }
    sort_field = _METRIC_SORT_FIELD.get(selected_metric, "total_net")
    # Map metric to _summary_net.json series field name
    _METRIC_SERIES_FIELD = {
        "net": "net",
        "buy_net": "buy_net",
        "sell_net": "sell_net",
        "buy_sell": "net"
    }
    series_net_field = _METRIC_SERIES_FIELD.get(selected_metric, "net")
    audit_entry = {
        "timestamp": datetime.now().isoformat(),
        "workflow_id": "top_x_multi_chart_workflow",
        "mode": mode,
        "date": date_str,
        "product_type": product_type,
        "active_window": {
            "start_time": wf.get("start_time"),
            "end_time": wf.get("end_time"),
            "active_now": _workflow_active_now(wf)
        },
        "config": {
            "top_x": top_x,
            "include_scalper": include_scalper,
            "include_rev_scalper": include_rev_scalper,
            "add_to_tb": add_to_tb,
            "add_same_parameter_strategies_metrics": add_same_parameter,
            "run_interval_sec": cfg.get("run_interval_sec"),
            "metric": selected_metric,
            "delta_type": delta_type,
            "require_positive_total_net": bool(cfg.get("require_positive_total_net", True)),
            "require_pick_now": require_pick_now,
            "sort_by_most_trades": bool(cfg.get("sort_by_most_trades", False)),
            "merge_charts": merge_charts,
            "strategy_groups": strategy_groups
        },
        "top20_exists": False,
        "top20_count": 0,
        "filtered_count": 0,
        "sliced_count": 0,
        "payload_items": 0,
        "filter_reason_counts": {},
        "tb": {
            "requested": add_to_tb,
            "created_count": 0,
            "outcomes": []
        },
        "status": "started",
        "message": ""
    }

    summary_strategies: Dict[str, Dict[str, List[dict]]] = {}
    if add_same_parameter or add_to_tb:
        for summary_net_file in [day_dir / "_summary_net.json" for day_dir in _iter_day_dirs_for(mode, date_str, product_type)]:
            if not summary_net_file.exists():
                continue
            try:
                with open(summary_net_file, "r") as f:
                    loaded_strategies = (json.load(f) or {}).get("strategies", {}) or {}
                if not isinstance(loaded_strategies, dict):
                    continue
                for model_name, products in loaded_strategies.items():
                    if not isinstance(products, dict):
                        continue
                    model_bucket = summary_strategies.setdefault(str(model_name), {})
                    for product_name, series in products.items():
                        if isinstance(series, list):
                            model_bucket[str(product_name)] = series
            except Exception:
                continue

    def _series_for(model_name: str, product_name: str) -> List[dict]:
        try:
            products = summary_strategies.get(str(model_name), {})
            if isinstance(products, dict):
                series = products.get(str(product_name))
                if isinstance(series, list):
                    return series
        except Exception:
            pass
        return []

    def _family_for_same_param(model_name: str, product_name: str) -> List[dict]:
        _, sig = _parse_model_signature(model_name)
        product_scope = str(product_name).upper()
        out = []
        for model_k, products in summary_strategies.items():
            if not isinstance(products, dict):
                continue
            _, model_sig = _parse_model_signature(str(model_k))
            if model_sig != sig:
                continue
            for prod_k, series in products.items():
                if str(prod_k).upper() != product_scope:
                    continue
                if not isinstance(series, list) or not series:
                    continue
                try:
                    # [V20260306_1845] Use selected metric field for family net value
                    latest_net = float(series[-1].get(series_net_field, 0.0) or 0.0)
                except Exception:
                    latest_net = 0.0
                out.append({
                    "model": str(model_k),
                    "product": str(prod_k).upper(),
                    "series": series,
                    "latest_net": latest_net
                })
        out.sort(key=lambda x: x.get("latest_net", 0.0), reverse=True)
        return out

    try:
        top_20: List[dict] = []
        for top20_file in [day_dir / "_top20.json" for day_dir in _iter_day_dirs_for(mode, date_str, product_type)]:
            if not top20_file.exists():
                continue
            audit_entry["top20_exists"] = True
            with open(top20_file, "r") as f:
                top_20.extend((json.load(f) or {}).get("top20", []))
        audit_entry["top20_count"] = len(top_20)

        if not top_20:
            audit_entry["status"] = "skipped"
            audit_entry["message"] = "top20 file not found."
            _log_topx_workflow_audit(mode, date_str, product_type, audit_entry)
            return {"success": False, "message": "top20 file not found."}

        if not top_20 or not isinstance(top_20, list):
            audit_entry["status"] = "skipped"
            audit_entry["message"] = "Failed to retrieve top 20 or list empty."
            _log_topx_workflow_audit(mode, date_str, product_type, audit_entry)
            return {"success": False, "message": "Failed to retrieve top 20 or list empty."}

        _sr = 5.0
        _rsr = 2.0
        _cfg_path = CONFIG_FILE
        if _cfg_path.exists():
            try:
                with open(_cfg_path, "r") as f:
                    _c = json.load(f)
                    _sr = float(_c.get("scalper_ratio", 5.0))
                    _rsr = float(_c.get("rev_scalper_ratio", 2.0))
            except: pass

        filtered = []
        filter_reason_counts = {
            "missing_strategy": 0,
            "strategy_group_filtered": 0,
            "not_scalper_or_rev_scalper": 0,
            "metric_not_positive": 0,
            "total_net_not_positive": 0,
            "pick_now_false": 0
        }
        for entry in top_20:
            strat_name = entry.get("strategy", "")
            if not strat_name:
                filter_reason_counts["missing_strategy"] += 1
                continue
            if not _workflow_strategy_group_allowed(strat_name, strategy_groups):
                filter_reason_counts["strategy_group_filtered"] += 1
                continue
            
            m = re.search(r'tp([\d.]+)_sl([\d.]+)', strat_name, re.IGNORECASE)
            is_scalper = ("scalp" in strat_name.lower()) or ("_s_" in strat_name.lower()) or strat_name.lower().endswith("_s")
            is_rev_scalper = False
            
            if m:
                tp = float(m.group(1))
                sl = float(m.group(2))
                if tp > 0 and sl >= tp * _sr:
                    is_scalper = True
                if sl > 0 and tp >= sl * _rsr:
                    is_rev_scalper = True
            
            should_include = False
            if not include_scalper and not include_rev_scalper:
                should_include = True
            else:
                if include_scalper and is_scalper:
                    should_include = True
                if include_rev_scalper and is_rev_scalper:
                    should_include = True
                
            if should_include:
                # [V20260312_1410] Ensure positive net for the selected sort metric
                metric_value = float(entry.get(sort_field, 0.0) or 0.0)
                if metric_value > 0:
                    # [V20260323_1500] Enforce total_net > 0 if explicitly requested in config
                    if bool(cfg.get("require_positive_total_net", True)):
                        if float(entry.get("total_net", 0.0) or 0.0) <= 0:
                            filter_reason_counts["total_net_not_positive"] += 1
                            continue
                    
                    # `pick_now` is useful for stricter automation gating, but multi-chart
                    # payload generation should not silently depend on it unless explicitly enabled.
                    if require_pick_now and not entry.get("pick_now", False):
                        filter_reason_counts["pick_now_false"] += 1
                        continue

                    filtered.append(entry)
                else:
                    filter_reason_counts["metric_not_positive"] += 1
            else:
                filter_reason_counts["not_scalper_or_rev_scalper"] += 1
        audit_entry["filter_reason_counts"] = filter_reason_counts

        # [V20260414_1420] Support sorting by trade count
        if bool(cfg.get("sort_by_most_trades", False)):
            filtered.sort(key=lambda x: int(x.get("trade_count", 0) or 0), reverse=True)
        else:
            # [V20260306_1845] Sort by selected metric field instead of hardcoded total_net
            filtered.sort(key=lambda x: float(x.get(sort_field, 0.0) or 0.0), reverse=True)

        sliced = filtered[:top_x]        
        audit_entry["filtered_count"] = len(filtered)
        audit_entry["sliced_count"] = len(sliced)
        now_local = datetime.now().isoformat()
        payload_items = []
        payload_seen: Set[str] = set()
        group_name = f"WF_TOPX_{(product_type or 'all').upper()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        for entry in sliced:
            m_model = str(entry.get("strategy", "")).strip()
            m_product = str(entry.get("product", "")).strip().upper()
            
            m_latest_net_from_top20 = float(entry.get(sort_field, 0.0) or 0.0)
            if add_same_parameter:
                expanded = _family_for_same_param(m_model, m_product)
                if not expanded:
                    expanded = [{"model": m_model, "product": m_product, "series": _series_for(m_model, m_product), "latest_net": m_latest_net_from_top20}]
            else:
                expanded = [{"model": m_model, "product": m_product, "series": _series_for(m_model, m_product), "latest_net": m_latest_net_from_top20}]
            
            for m in expanded:
                ex_model = str(m.get("model") or "").strip()
                ex_product = str(m.get("product") or "").strip().upper()
                if not ex_model or not ex_product:
                    continue
                if not _workflow_strategy_group_allowed(ex_model, strategy_groups):
                    continue

                # [V20260323_1510] Filter expansion members for positive net
                m_latest_net = float(m.get("latest_net", 0.0) or 0.0)
                if m_latest_net <= 0:
                    continue
                # Also check total_net if configured
                if bool(cfg.get("require_positive_total_net", True)):
                    try:
                        m_series = m.get("series") or []
                        m_total_net = float(m_series[-1].get("net", 0.0) or 0.0) if m_series else m_latest_net
                    except: m_total_net = m_latest_net
                    if m_total_net <= 0:
                        continue
                        
                dedup_key = f"{ex_model}|{ex_product}".lower()
                if dedup_key in payload_seen:
                    continue
                payload_seen.add(dedup_key)

                safe_model = re.sub(r'[^A-Za-z0-9_]+', '_', ex_model).strip('_')
                safe_product = re.sub(r'[^A-Za-z0-9_]+', '_', ex_product).strip('_')
                per_card_group = group_name if merge_charts else f"{group_name}_{safe_product}_{safe_model}"
                
                # [V20260306_1845] For buy_sell, create two overlay entries (buy_net + sell_net)
                if selected_metric == "buy_sell":
                    payload_items.append({
                        "strategy": ex_model,
                        "product": ex_product,
                        "product_type": product_type,
                        "group": per_card_group,
                        "metric": "buy_net",
                        "parm_raw": ""
                    })
                    payload_items.append({
                        "strategy": ex_model,
                        "product": ex_product,
                        "product_type": product_type,
                        "group": per_card_group,
                        "metric": "sell_net",
                        "parm_raw": ""
                    })
                else:
                    payload_items.append({
                        "strategy": ex_model,
                        "product": ex_product,
                        "product_type": product_type,
                        "group": per_card_group,
                        "metric": selected_metric if selected_metric != "net" else None,
                        "parm_raw": ""
                    })

        payload = {
            "source": "top_x_multi_chart_workflow",
            "mode": mode,
            "date": date_str,
            "preferred_metric": selected_metric,  # [V20260306_1845] Use selected metric type
            "delta_type": delta_type,
            "group": group_name,
            "preset_name": group_name,
            "created_at": now_local,
            "run_id": f"{mode}_{date_str}_{int(time.time())}_top_x",
            "product_types": [product_type] if product_type else [],
            "strategy_groups": strategy_groups,
            "merge_charts": merge_charts,
            "items": payload_items
        }
        audit_entry["payload_items"] = len(payload_items)

        try:
            with open(WORKFLOW_MULTI_CHART_PAYLOAD_FILE, "w") as f:
                json.dump(payload, f, indent=4)
        except Exception as e:
            audit_entry["status"] = "failed"
            audit_entry["message"] = f"failed to write multi-chart payload: {e}"
            _log_topx_workflow_audit(mode, date_str, product_type, audit_entry)
            return {"success": False, "message": f"failed to write multi-chart payload: {e}"}

        tb_result = {
            "requested": add_to_tb,
            "created": False,
            "activated": False,
            "reason": "not_requested"
        }

        if add_to_tb and sliced:
            trade_alt_net = bool(cfg.get("trade_alt_net", False))
            max_live_tb = _get_max_live_tb()
            tb_data = _load_trade_buckets(mode=mode, date_str=date_str, product_type=product_type)
            tb_buckets = tb_data.get("buckets", [])
            def _norm_key(model_name: str, product_name: str) -> str:
                m_str = str(model_name or "").strip().lower()
                p_str = str(product_name or "").strip().upper()
                return f"{m_str}|{p_str}"

            existing_keys: Set[str] = set()
            for b in tb_buckets:
                if not isinstance(b, dict):
                    continue
                for s in (b.get("strategies") or []):
                    if not isinstance(s, dict):
                        continue
                    key_raw = str(s.get("key") or "")
                    parts = key_raw.split(" | ") if " | " in key_raw else key_raw.split("|")
                    if len(parts) == 2:
                        existing_keys.add(_norm_key(parts[0], parts[1]))

            live_count = sum(1 for b in tb_buckets if isinstance(b, dict) and bool(b.get("live")))
            if live_count >= max_live_tb:
                tb_result = {
                    "requested": True,
                    "created": False,
                    "activated": False,
                    "reason": f"max_live_tb_reached ({live_count}/{max_live_tb})"
                }
                audit_entry["tb"]["outcomes"].append(tb_result.copy())
            else:
                tb_results_list = []
                
                for candidate in sliced:
                    if live_count >= max_live_tb:
                        tb_results_list.append({"requested": True, "created": False, "reason": f"max_live_tb_reached ({live_count}/{max_live_tb})"})
                        break
                        
                    c_model = str(candidate.get("strategy") or "")
                    c_prod = str(candidate.get("product") or "").upper()
                    if _norm_key(c_model, c_prod) in existing_keys:
                        tb_results_list.append({"requested": True, "created": False, "reason": "already_exists"})
                        continue
                        
                    if add_same_parameter:
                        c_family = _family_for_same_param(c_model, c_prod)
                    else:
                        c_family = [{
                            "model": c_model, 
                            "product": c_prod, 
                            "series": _series_for(c_model, c_prod),
                            "latest_net": float(candidate.get(sort_field, 0.0) or 0.0)
                        }]
                    
                    if len(c_family) >= 1:
                        pre_tb_family = c_family
                        best_model = c_model
                        best_product = c_prod

                        now_dt = datetime.now()
                        mmdd = now_dt.strftime("%m%d")
                        hhmmss_mmm = now_dt.strftime("%H%M%S") + f"_{int(now_dt.microsecond/1000):03d}"
                        safe_product_tb = re.sub(r'[^A-Za-z0-9_]+', '_', best_product).strip('_').upper()
                        safe_model_tb = re.sub(r'[^A-Za-z0-9_]+', '_', best_model).strip('_')
                        bucket_name = f"AUTO_TB_{mmdd}_{hhmmss_mmm}_{safe_product_tb}_{safe_model_tb}".replace(" ", "")
                        bias_at_creation = _get_current_bias(mode, date_str) or "UNKNOWN"
                        total_net = round(float(candidate.get("total_net", 0.0) or 0.0), 2)
                        min_diff = float(cfg.get("minimum_difference", 5.0) or 5.0)

                        start_from_dt = now_dt
                        eval_dt = now_dt

                        processed_strategies = []
                        # [V20260413_1330] Modified: Remove (len(pre_tb_family) == 1) override.
                        # Splitting ONLY occurs if explicitly requested via buy_sell metric or t_split_for_tb.
                        should_split = (
                            (selected_metric == "buy_sell")
                            or (selected_metric == "net" and t_split_for_tb)
                        )

                        for fam in pre_tb_family:
                            fm = str(fam.get("model") or "").strip()
                            fp = str(fam.get("product") or "").strip().upper()
                            if not fm or not fp:
                                continue
                            series = fam.get("series") if isinstance(fam.get("series"), list) else []
                            
                            # [V20260323_1510] Filter expansion members for positive net in TB
                            f_latest_net = float(fam.get("latest_net", 0.0) or 0.0)
                            if f_latest_net <= 0:
                                continue
                            if bool(cfg.get("require_positive_total_net", True)):
                                try:
                                    f_total_net = float(series[-1].get("net", 0.0) or 0.0) if series else f_latest_net
                                except: f_total_net = f_latest_net
                                if f_total_net <= 0:
                                    continue
                            
                            metrics_to_add = [("buy_net", "buy_net"), ("sell_net", "sell_net")] if should_split else [("net", "net")]
                            
                            for m_type, m_field in metrics_to_add:
                                if series:
                                    creation_net = round(_series_value_at_or_before(series, eval_dt, field=m_field), 2)
                                    start_from_net = round(_series_value_at_or_before(series, start_from_dt, field=m_field), 2)
                                else:
                                    creation_net = round(float(fam.get("latest_net", total_net) or 0.0), 2)
                                    start_from_net = creation_net

                                processed_strategies.append({
                                    "strategy_id": str(uuid.uuid4()),
                                    "key": f"{fm} | {fp}",
                                    "metric": m_type,
                                    "bias_at_creation": bias_at_creation,
                                    "start_from_net": start_from_net,
                                    "net_at_creation": creation_net,
                                    "current_total_net": creation_net,
                                    "start_net_delta_from_chart": round(creation_net - start_from_net, 2),
                                    "current_net_from_chart": round(creation_net - start_from_net, 2),
                                    "net_delta_from_creation": 0.0,
                                    "total_net": 0.0,
                                    "delta_type": delta_type,
                                    "live_trade_net": 0.0
                                })
                        
                        # [V20260311_1345] Deduplicate by strategy+product+metric
                        seen_s = set()
                        final_strategies = []
                        for s in processed_strategies:
                            d_key = f"{s.get('key')}|{s.get('metric')}"
                            if d_key not in seen_s:
                                seen_s.add(d_key)
                                final_strategies.append(s)
                        processed_strategies = final_strategies

                        # [V20260413_1330] Removed: Emergency split for single-row net metrics.
                        # This ensures the min_rows_violation guard below handles single charts strictly.

                        if len(processed_strategies) < 2:
                            tb_results_list.append({"requested": True, "created": False, "reason": "min_rows_violation_after_dedup"})
                            continue
                        
                        new_bucket = {
                            "bucket_id": str(uuid.uuid4()),
                            "name": bucket_name,
                            "date": date_str,
                            "mode": mode,
                            "product_type": product_type,
                            "trade_alt_net": trade_alt_net,
                            "market_bias_at_creation": bias_at_creation,
                            "metric": cfg.get("metric", "net"),
                            "delta_type": delta_type,
                            "chart_start_time": start_from_dt.isoformat(),
                            "start_time": eval_dt.isoformat(),
                            "strategies": processed_strategies,
                            "live": True,
                            "open_trades": False,
                            "open_trade_count": 0,
                            "minimum_difference": float(min_diff),
                            "created_by_workflow": "top_x_multi_chart_workflow"
                        }

                        tb_buckets.append(new_bucket)
                        existing_keys.add(_norm_key(best_model, best_product))
                        live_count += 1
                        
                        _sync_bucket_to_grid_live(new_bucket, mode, date_str, product_type=product_type)

                        tb_results_list.append({
                            "requested": True,
                            "created": True,
                            "activated": True,
                            "bucket_name": bucket_name,
                            "family_size": len(processed_strategies),
                            "reason": "success"
                        })
                    else:
                        tb_results_list.append({"requested": True, "created": False, "reason": "no_candidate_found_for_tb"})

                if any(r.get("created") for r in tb_results_list):
                    tb_data["buckets"] = tb_buckets
                    _save_trade_buckets(tb_data, mode=mode, date_str=date_str, product_type=product_type)
                    _update_automated_source("Trade Bucket")

                created_count = sum(1 for r in tb_results_list if r.get("created"))
                audit_entry["tb"]["created_count"] = created_count
                audit_entry["tb"]["outcomes"] = tb_results_list
                if created_count > 0:
                    tb_result = {
                        "requested": True,
                        "created": True,
                        "activated": True,
                        "reason": f"success ({created_count} buckets)",
                        "details": tb_results_list
                    }
                else:
                    tb_result = {
                        "requested": True,
                        "created": False,
                        "activated": False,
                        "reason": "no_candidate_found_for_tb" if not tb_results_list else tb_results_list[0].get("reason", "unknown")
                    }


        # [V20260323_1645] Log historical Top 10 snapshot
        _log_top10_history_snapshot(mode, date_str, product_type, sliced)
        audit_entry["status"] = "success"
        audit_entry["message"] = f"Successfully created Top {len(sliced)} multi-chart payload."
        audit_entry["history_snapshot_requested"] = bool(sliced)
        _log_topx_workflow_audit(mode, date_str, product_type, audit_entry)

        return {
            "success": True,
            "message": f"Successfully created Top {len(sliced)} multi-chart payload.",
            "top_x_selected": len(sliced),
            "payload_items": len(payload_items),
            "tb": tb_result
        }
    except Exception as e:
        audit_entry["status"] = "failed"
        audit_entry["message"] = str(e)
        _log_topx_workflow_audit(mode, date_str, product_type, audit_entry)
        return {"success": False, "message": str(e)}

def _run_tb_prune_all_negative_once(mode: str, date_str: str, wf: dict) -> dict:
    """
    Remove trade buckets where all strategy net values are below threshold.
    """
    cfg = wf.get("config", {}) if isinstance(wf, dict) else {}
    threshold = float(cfg.get("negative_threshold", -20) or -20)
    product_type = str(cfg.get("product_type") or "").strip().lower() or None

    data = _load_trade_buckets(mode=mode, date_str=date_str, product_type=product_type)
    buckets = data.get("buckets", [])
    if not buckets:
        return {"success": True, "removed": 0, "message": f"no buckets for {product_type or 'all'}"}

    kept = []
    removed_names = []
    removed_buckets = []

    def _load_summary_strategies_from_file(fpath: Path) -> dict:
        if not fpath.exists():
            return {}
        try:
            with open(fpath, "r") as f:
                return (json.load(f) or {}).get("strategies", {}) or {}
        except Exception:
            return {}

    def _latest_mode_date(_mode: str) -> str:
        mode_dir = BASE_PATH / _mode
        if not mode_dir.exists():
            return date_str
        try:
            dates = [p.name for p in mode_dir.iterdir() if p.is_dir() and re.fullmatch(r"\d{4}-\d{2}-\d{2}", p.name)]
            return sorted(dates)[-1] if dates else date_str
        except Exception:
            return date_str

    latest_date = _latest_mode_date(mode)
    summary_current = {}
    for day_dir in _iter_day_dirs_for(mode, latest_date, product_type):
        summary_current.update(_load_summary_strategies_from_file(day_dir / "_summary_net.json"))
    
    if not summary_current:
        for day_dir in _iter_day_dirs_for(mode, date_str, product_type):
            summary_current.update(_load_summary_strategies_from_file(day_dir / "_summary_net.json"))

    def _strategy_net_live(bucket: dict, s: dict) -> float:
        """
        Use the same basis as TB UI current range net:
        current_net_from_chart = latest_summary_net - start_from_net.
        Fallback to persisted fields only when live series is unavailable.
        """
        strat_key = str(s.get("key", "") or "")
        parts = strat_key.split(" | ")
        if len(parts) != 2:
            parts = strat_key.split("|")
        if len(parts) == 2 and summary_current:
            strategy_name = parts[0].strip()
            product = parts[1].strip()
            series = summary_current.get(strategy_name, {}).get(product, [])
            if isinstance(series, list) and series:
                try:
                    latest_net = float(series[-1].get("net", 0.0) or 0.0)
                except Exception:
                    latest_net = 0.0
                try:
                    start_from = float(s.get("start_from_net", s.get("net_at_creation", 0.0)) or 0.0)
                except Exception:
                    start_from = 0.0
                return float(round(latest_net - start_from, 2))

        for k in ("current_net_from_chart", "net_delta_from_creation", "total_net", "current_total_net", "net_at_creation", "start_from_net"):
            if k in s:
                try:
                    return float(s.get(k, 0) or 0)
                except Exception:
                    continue
        return 0.0

    for b in buckets:
        strategies = b.get("strategies", []) if isinstance(b, dict) else []
        if not isinstance(strategies, list) or not strategies:
            kept.append(b)
            continue
        nets = [_strategy_net_live(b, s) for s in strategies if isinstance(s, dict)]
        if nets and all(n < threshold for n in nets):
            bucket_name = str(b.get("name") or "UNKNOWN_BUCKET")
            removed_names.append(bucket_name)

            # Step 1 (required): Deactivate bucket before removing.
            # Persist live=false and push grid sync-off for this bucket source.
            if isinstance(b, dict):
                b["live"] = False
            try:
                _sync_bucket_to_grid_live({**b, "live": False}, mode, date_str)
            except Exception:
                pass

            removed_buckets.append(dict(b) if isinstance(b, dict) else {"name": bucket_name, "live": False})
            continue
        kept.append(b)

    if removed_buckets:
        try:
            hist_file = _resolve_day_dir(mode, date_str) / "_trade_buckets_removed_history.json"
            history = []
            if hist_file.exists():
                with open(hist_file, "r") as hf:
                    history = json.load(hf) or []
            if not isinstance(history, list):
                history = []
            history.append({
                "timestamp": datetime.now().isoformat(),
                "workflow": "tb_prune_all_negative",
                "threshold": threshold,
                "removed_count": len(removed_buckets),
                "removed_buckets": removed_buckets
            })
            with open(hist_file, "w") as hf:
                json.dump(history, hf, indent=4)
        except Exception as e:
            print(f"[WORKFLOW] tb_prune_all_negative archive write failed: {e}")

    if len(kept) != len(buckets):
        data["buckets"] = kept
        _save_trade_buckets(data, mode=mode, date_str=date_str, product_type=product_type)

    return {
        "success": True,
        "removed": len(removed_names),
        "removed_names": removed_names,
        "threshold": threshold
    }


@app.route('/api/workflows/multi_chart_payload', methods=['GET'])
def get_workflow_multi_chart_payload():
    """Return latest workflow-generated payload for Multi Chart import."""
    try:
        if not WORKFLOW_MULTI_CHART_PAYLOAD_FILE.exists():
            return jsonify({"success": True, "payload": None})
        with open(WORKFLOW_MULTI_CHART_PAYLOAD_FILE, "r") as f:
            payload = json.load(f)
        return jsonify({"success": True, "payload": payload})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route('/api/market_update', methods=['GET'])
def get_market_update():
    """Return latest periodic market narrative for mode/date."""
    try:
        mode = str(request.args.get('mode', 'live')).lower()
        date_str = str(request.args.get('date') or datetime.now().strftime('%Y-%m-%d'))
        update_file = _resolve_day_dir(mode, date_str) / "_market_update.json"
        if not update_file.exists():
            return jsonify({"success": True, "exists": False, "message": "No market update generated yet."})
        with open(update_file, "r") as f:
            payload = json.load(f) or {}
        return jsonify({"success": True, "exists": True, "update": payload})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route('/api/market_update/history', methods=['GET'])
def get_market_update_history():
    """Return historical market narrative blurbs for mode/date."""
    try:
        mode = str(request.args.get('mode', 'live')).lower()
        date_str = str(request.args.get('date') or datetime.now().strftime('%Y-%m-%d'))
        limit_raw = request.args.get('limit')
        try:
            limit = int(limit_raw) if limit_raw is not None else 200
        except Exception:
            limit = 200
        limit = max(1, min(limit, 2000))

        history_file = _resolve_day_dir(mode, date_str) / "_market_update_history.json"
        if not history_file.exists():
            return jsonify({"success": True, "exists": False, "history": []})
        with open(history_file, "r") as f:
            history = json.load(f) or []
        if not isinstance(history, list):
            history = []
        history = history[-limit:]
        history.reverse()  # newest first
        return jsonify({"success": True, "exists": True, "count": len(history), "history": history})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


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
            "source": value.get("source") or "ui",
            "products": sorted({p.upper() for p in raw_products if isinstance(p, str)}),
            "auto_promote": bool(value.get("auto_promote", False)),
        }
    return {
        "active": bool(value),
        "manual": False,
        "activated_at": None,
        "source": "ui",
        "products": [],
        "auto_promote": False,
    }


def _merge_entries(a: Dict[str, Any], b: Dict[str, Any]) -> Dict[str, Any]:
    a["active"] = a["active"] or b["active"]
    a["manual"] = a["manual"] or b["manual"]
    a["auto_promote"] = a.get("auto_promote", False) or b.get("auto_promote", False)
    if b.get("activated_at") and (
        not a.get("activated_at") or b["activated_at"] > a["activated_at"]
    ):
        a["activated_at"] = b["activated_at"]
    
    # [V20260204_2057] Preserve source from the most recent or non-'ui' entry
    if b.get("source") and b["source"] != "ui":
        a["source"] = b["source"]
    elif not a.get("source"):
        a["source"] = b.get("source", "ui")

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


# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# API Endpoints
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
@app.route("/api/activations", methods=["GET"])
def get_activations():
    """Get activations from activations.json. [V20260407_1745]"""
    mode = request.args.get('mode', 'live').lower()

    try:
        all_activations = _load_activations()
        mode_activations = all_activations.get(mode, {})

        return jsonify({
            "success": True,
            "activations": mode_activations
        })
    except Exception as e:
        print(f"[ERROR] /api/activations GET failed: {e}")
        return jsonify({
            "success": False,
            "message": str(e),
            "activations": {}
        })


# [V20260127_1520] Get available dates for a given mode
@app.route("/api/dates", methods=["GET"])
def get_dates():
    """Get available trade dates for specified mode."""
    mode = request.args.get('mode', 'live').lower()
    product_type = request.args.get('product_type', 'all').lower()
    required_file = request.args.get('file') # [V20260318_1055]
    
    dates = set()
    
    # [V20260318_1015] Use a specific directory if product_type is provided
    if product_type and product_type != 'all':
        json_dir = ROOT_PATH / "json" / mode / product_type
        if json_dir.exists():
            for item in json_dir.iterdir():
                if item.is_dir() and re.match(r'^\d{4}-\d{2}-\d{2}$', item.name):
                    # [V20260318_1055] Only add if file exists
                    if not required_file or (item / required_file).exists():
                        dates.add(item.name)
    else:
        # Fallback recursive search for all dates
        json_root = ROOT_PATH / "json" / mode
        if json_root.exists():
            for item in json_root.iterdir():
                if not item.is_dir():
                    continue
                # Level 1: json/live/2026-01-01
                if re.match(r'^\d{4}-\d{2}-\d{2}$', item.name):
                    if not required_file or (item / required_file).exists():
                        dates.add(item.name)
                    continue
                # Level 2: json/live/indices/2026-01-01
                for child in item.iterdir():
                    if child.is_dir() and re.match(r'^\d{4}-\d{2}-\d{2}$', child.name):
                        if not required_file or (child / required_file).exists():
                            dates.add(child.name)
    
    sorted_dates = sorted(dates, reverse=True)
    
    return jsonify({
        "success": True,
        "dates": sorted_dates
    })

@app.route('/api/trades', methods=['GET'])
def get_trades():
    """
    [V20260128_1500] Load trade JSON files for a given mode and date.
    Optimized: Uses filename pattern matching to reduce file scanning when filters are provided.
    """
    try:
        run_mode = request.args.get('mode', 'live')
        date = request.args.get('date')
        if not date:
            date = datetime.now().strftime('%Y-%m-%d')
            
        strategy_filter = request.args.get('strategy', 'all')
        req_strategy = strategy_filter # Alias for loop logic
        req_product = request.args.get('product')
        req_product_type = request.args.get('product_type')
        req_params = request.args.get('params')
        live_only = request.args.get('live_only', 'false').lower() == 'true'
        l_only = request.args.get('l_only', 'false').lower() == 'true' # [V20260424_1930] Filter for bucket leaders only
        since_time = request.args.get('since_time') # [V20260205_1640] Filter by entry time
        bucket_context = request.args.get('bucket_name') # [V20260320_1230] Context for L-Trade identification
        _refresh_open_trade_files(run_mode, date, product=req_product, product_type=req_product_type)
        
        since_dt = None
        if since_time:
            try:
                # Handle potential space/T differences in ISO strings
                since_dt = datetime.fromisoformat(since_time.replace('Z', '').replace(' ', 'T'))
            except: pass
        
        day_dirs = _iter_day_dirs_for(run_mode, date, req_product_type)
        
        print(f"[API] get_trades: mode={run_mode}, date={date}, strategy={strategy_filter}, product={req_product}, params={req_params}, live={live_only}")
        
        if not day_dirs:
            return jsonify({
                'success': False,
                'message': f'Directory not found for mode={run_mode} date={date}',
                'trades': []
            })
        
        # [V20260130_1420] Capture Session Max Net from summary metadata
        session_max_net = 0.0
        for trade_dir in day_dirs:
            summary_path = trade_dir / "_summary_net.json"
            if not summary_path.exists():
                continue
            try:
                with open(summary_path, 'r') as f:
                    s_data = json.load(f)
                    session_max_net = max(session_max_net, float(s_data.get('session_max_net', 0.0)))
            except:
                pass

        # [V20260205_1710] HIGH PERFORMANCE PATH: Use central trades summary if available
        indexed_trades = []
        for trade_dir in day_dirs:
            trades_summary_path = trade_dir / "_trades_summary.json"
            if not trades_summary_path.exists():
                continue
            try:
                with open(trades_summary_path, 'r') as f:
                    index_data = json.load(f)
                    indexed_trades.extend(index_data.get('trades', []))
            except Exception as e:
                print(f"[API] Failed to use trades index from {trades_summary_path}: {e}")
        if indexed_trades:
            # [V20260320_1230] Load leadership data if bucket context is provided
            leadership_map = {}
            bucket_metric_map = {}
            if bucket_context:
                all_leadership = _load_tb_leadership(run_mode, date, req_product_type)
                # Map by bucket name for easier lookup
                leadership_map = {bl['bucket']: bl for bl in all_leadership}
                bucket_metric_map[bucket_context] = _get_bucket_live_metric(bucket_context, run_mode)

            filtered = []
            for t in indexed_trades:
                        # 1. Product Filter
                        if req_product and req_product != 'all' and req_product != 'undefined':
                            if t.get('product', '').upper() != req_product.upper():
                                continue
                                
                        # 2. Strategy Filter
                        # [V20260429_1330] Use exact canonical model keys.
                        # Prefix/substring matching caused breakout_R rows to include breakout_R_Rev trades.
                        t_app = str(t.get('app_name') or t.get('script_name') or '').strip()
                        t_params = str(t.get('strategy') or t.get('strategy_key') or '').strip()
                        t_app_has_params = bool(re.search(r"_\d+_tp[\d.]+_sl[\d.]+$", t_app.lower()))
                        t_full_key = t_app if t_app_has_params or not t_params or t_app.lower().endswith(f"_{t_params.lower()}") else f"{t_app}_{t_params}"

                        req_strategy_clean = str(req_strategy or '').strip()
                        req_params_clean = str(req_params or '').strip()
                        if req_strategy_clean and req_strategy_clean not in ('all', 'undefined', 'null'):
                            target_full_key = req_strategy_clean
                            if req_params_clean and req_params_clean not in ('all', 'undefined', 'null', ''):
                                if not target_full_key.lower().endswith(f"_{req_params_clean.lower()}"):
                                    target_full_key = f"{target_full_key}_{req_params_clean}"

                            target_norm = target_full_key.lower()
                            candidate_norms = {
                                t_app.lower(),
                                t_params.lower(),
                                t_full_key.lower(),
                            }
                            if target_norm not in candidate_norms:
                                continue

                        # 2b. Params Filter (Explicitly requested by some views)
                        if req_params_clean and req_params_clean not in ('all', 'undefined', 'null', ''):
                            if req_params_clean.lower() not in {t_params.lower(), t_full_key.lower().split('_', 1)[-1]} and not t_full_key.lower().endswith(f"_{req_params_clean.lower()}"):
                                continue
                        
                        # 3. Live Only Filter
                        # [V20260205_2215] Robust live match (checks summarized is_live OR raw flags if indexed)
                        if live_only:
                            is_l = (
                                t.get('is_live') == True or 
                                t.get('is_live_trade') == True or 
                                t.get('order_sent_net') in (True, 'true')
                            )
                            if not is_l:
                                continue
                            
                        # 4. Since Time Filter
                        if since_dt:
                            e_time = t.get('entry_time')
                            if e_time:
                                try:
                                    e_dt = datetime.fromisoformat(e_time.replace('Z', '').replace(' ', 'T'))
                                    if e_dt < since_dt:
                                        continue
                                except: pass
                        
                        # [V20260320_1230] Tag L-Trades
                        is_l = False
                        if bucket_context and bucket_context in leadership_map:
                            if _is_trade_in_leader_window(
                                t,
                                leadership_map[bucket_context],
                                bucket_metric_map.get(bucket_context),
                            ):
                                is_l = True
                                t['is_l_trade'] = True

                        # [V20260424_1930] Server-side L-only filter
                        if l_only and not is_l:
                            continue

                        filtered.append(t)
            return jsonify({
                'success': True,
                'count': len(filtered),
                'trades': filtered,
                'mode': run_mode,
                'date': date,
                'session_max_net': session_max_net,
                'indexed': True,
                'version': VERSION
            })

        trades = []
        file_count = 0
        product_hint = req_product if req_product and req_product not in ('all', 'undefined') else None

        # [V20260424_1930] Load leadership data for legacy path
        leadership_map = {}
        bucket_metric_map = {}
        if bucket_context:
            all_leadership = _load_tb_leadership(run_mode, date, req_product_type)
            leadership_map = {bl['bucket']: bl for bl in all_leadership}
            bucket_metric_map[bucket_context] = _get_bucket_live_metric(bucket_context, run_mode)

        for trade_dir in day_dirs:

            for json_file in _iter_trade_json_files(
                trade_dir,
                include_archived_closed=True,
                product_hint=product_hint,
            ):
                file_count += 1
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
                            
                            # Normalize params to match summary_net format (window_tpX_slY)
                            f_strategy_params = f"{window}_tp{tp}_sl{sl}"

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
                        raw_lower = raw_filename.lower()
                        if '_op' in raw_lower:
                            status_suffix = 'OPEN'
                        elif '_cl' in raw_lower or '_cld' in raw_lower:
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
                        if req_product and req_product not in ('all', 'undefined', 'null'):
                            if trade_data.get('product', '').upper() != req_product.upper():
                                continue

                        target_id = req_strategy
                        if target_id in ('all', 'undefined', 'null', None):
                            target_id = ''
                        
                        if req_params and req_params not in ('all', 'undefined', 'null', ''):
                            if not target_id:
                                target_id = req_params
                            elif req_params not in target_id:
                                sep = '' if target_id.endswith('_') else '_'
                                target_id = f"{target_id}{sep}{req_params}"
                        
                        if target_id and target_id != 'all':
                            match = False
                            target_norm = str(target_id or '').strip().lower()
                            internal_norm = str(internal_app_name or '').strip().lower()
                            trade_params = str(trade_data.get('strategy') or req_params or '').strip()
                            params_norm = trade_params.lower()
                            internal_has_params = bool(re.search(r"_\d+_tp[\d.]+_sl[\d.]+$", internal_norm))
                            derived_full_norm = internal_norm if internal_has_params or not params_norm or internal_norm.endswith(f"_{params_norm}") else f"{internal_norm}_{params_norm}"

                            # [V20260429_1330] Exact canonical key matching only.
                            # Prefix matching incorrectly mixed strategy families such as breakout_R and breakout_R_Rev.
                            if target_norm in (internal_norm, params_norm, derived_full_norm):
                                match = True

                            if not match:
                                continue
                                
                        if req_product and req_product != 'all' and req_product != 'undefined':
                            if trade_data.get('product') != req_product:
                                continue

                        if live_only:
                            is_l = (
                                trade_data.get('is_live_trade') == True or 
                                trade_data.get('live_trade_executed') == True or 
                                trade_data.get('order_sent_net') in [True, 'true']
                            )
                            if not is_l:
                                continue
                                
                        if since_dt:
                            entry_time_str = trade_data.get('entry_time')
                            if entry_time_str:
                                try:
                                    entry_dt = datetime.fromisoformat(entry_time_str.replace('Z', '').replace(' ', 'T'))
                                    if entry_dt < since_dt:
                                        continue
                                except:
                                    pass

                        # [V20260424_1930] Tag and Filter L-Trades in legacy path
                        is_l = False
                        if bucket_context and bucket_context in leadership_map:
                            if _is_trade_in_leader_window(
                                trade_data,
                                leadership_map[bucket_context],
                                bucket_metric_map.get(bucket_context),
                            ):
                                is_l = True
                                trade_data['is_l_trade'] = True
                        
                        if l_only and not is_l:
                            continue

                        trades.append(trade_data)
                            
                except json.JSONDecodeError as e:
                    print(f"Error parsing {json_file}: {e}")
                    continue
                except Exception as e:
                    print(f"Error loading {json_file}: {e}")
                    continue
            if file_count > 5000:
                break
        
        return jsonify({
            'success': True,
            'count': len(trades),
            'trades': trades,
            'mode': run_mode,
            'date': date,
            'session_max_net': session_max_net,
            'version': VERSION
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e),
            'trades': []
        }), 500


@app.route('/api/top20', methods=['GET'])
def get_top20():
    try:
        run_mode = request.args.get('mode', 'live')
        product_type = request.args.get('product_type')
        date = request.args.get('date')
        if not date:
            date = datetime.now().strftime('%Y-%m-%d')

        merged = []
        last_update = None
        for top20_path in [day_dir / "_top20.json" for day_dir in _iter_day_dirs_for(run_mode, date, product_type)]:
            if not top20_path.exists():
                continue
            with open(top20_path, 'r') as f:
                data = json.load(f)
            merged.extend(data.get('top20', []))
            candidate_last_update = data.get('last_update')
            if candidate_last_update and (last_update is None or str(candidate_last_update) > str(last_update)):
                last_update = candidate_last_update
        if merged:
            return jsonify({
                'success': True,
                'top20': merged,
                'last_update': last_update,
                'version': VERSION
            })
        return jsonify({
            'success': False,
            'message': 'Top 20 data not yet generated for today.'
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/push_to_grid_v2', methods=['POST'])
def push_to_grid_v2():
    """
    [V20260205_1900] Pushes a top-performing strategy to grid_live.json.
    Ensures that Top 20 source supersedes any other existing source for that strategy.
    [V20260205_2100] Enforces automated_trade_source: Top20
    [V20260215_0001] Enforces automated_trade_sources allowlist from config UI.
    """
    try:
        data = request.json
        mode = data.get('mode', 'live')
        strategy = data.get('strategy')
        product = data.get('product')
        metric = data.get('metric', 'net')
        group = data.get('group') # [V20260210_1355] Support set-based grouping
        source = data.get('source', 'PSB') # [V20260210_1603] Allow custom source from UI

        if not strategy or not product:
            return jsonify({'success': False, 'message': 'Strategy and Product required.'})

        source_str = str(source).strip()

        # Normalize runtime source labels to config allowlist keys.
        if source_str.startswith('PSB_Family'):
            requested_source = 'PSB_Family'
        elif source_str.startswith('PSB'):
            requested_source = 'PSB'
        elif source_str.startswith('Top20'):
            requested_source = 'Top20'
        elif source_str.startswith('Trade Bucket'):
            requested_source = 'Trade Bucket'
        elif source_str.startswith(('Frequency', 'frequency', 'rank_alert')):
            requested_source = 'Frequency'
        else:
            requested_source = source_str

        if not _is_source_allowed(requested_source):
            print(f"[GRID-LIVE] REJECTED: source='{source_str}' blocked by config allowlist (requested='{requested_source}').")
            return jsonify({'success': True, 'message': 'Skipped (Source Overrule)'})

        grid_file = ROOT_PATH / "grid_live.json"

        with GRID_LIVE_LOCK:
            full_data = {'live': [], 'sim': []}
            if grid_file.exists():
                try:
                    with open(grid_file, "r") as f:
                        full_data = json.load(f)
                    if isinstance(full_data, list): # Migrate legacy
                        full_data = {'live': full_data, 'sim': []}
                except: pass

            mode_list = full_data.get(mode, [])

            # Remove any existing entry for this strategy/product (Override Logic)
            new_mode_list = []
            for item in mode_list:
                if item.get('model') == strategy and item.get('product') == product:
                    continue
                new_mode_list.append(item)

            # Add new top20 entry
            new_mode_list.append({
                "model": strategy,
                "product": product,
                "metric": metric,
                "activated_at": datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
                "group": group if group else f"{strategy} | {product}",
                "source": source_str if source_str != 'PSB' else f"PSB_{strategy}" # [V20260210_1603] Use provided source or default
            })

            full_data[mode] = new_mode_list

            with open(grid_file, "w") as f:
                json.dump(full_data, f, indent=4)
            
            # [V20260210_1630] Sync with activations (Activation Explorer)
            _sync_grid_to_activations(new_mode_list, mode=mode)

        return jsonify({'success': True, 'message': f'Strategy {strategy} promoted to grid via Top 20'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})



@app.route('/api/stats_summary', methods=['GET'])
def get_stats_summary():
    """
    [V20260128_1448] FAST Strategy Performance Stats.
    Reads from pre-generated _summary_net.json instead of iterating through thousands of trade files.
    """
    try:
        run_mode = request.args.get('mode', 'live')
        product_type = request.args.get('product_type')
        if product_type == 'all':
            product_type = None

        date = request.args.get('date')
        if not date:
            date = datetime.now().strftime('%Y-%m-%d')

        summary_files = [day_dir / "_summary_net.json" for day_dir in _iter_day_dirs_for(run_mode, date, product_type)]
        print(f"[API] stats_summary for mode={run_mode}, date={date}, paths={summary_files}")

        if not summary_files:
            return jsonify({
                'success': False,
                'message': f'Summary file not found for {date} ({run_mode}). Run summary_net_generator.py.',
                'data': []
            })

        strategies = {}
        for summary_file in summary_files:
            if not summary_file.exists():
                continue
            with open(summary_file, 'r') as f:
                summary_data = json.load(f)
            for strategy_name, products in (summary_data.get('strategies', {}) or {}).items():
                existing = strategies.setdefault(strategy_name, {})
                if isinstance(products, dict):
                    existing.update(products)
        limit_arg = request.args.get('limit')
        view_mode = request.args.get('view', '').lower()
        sort_key = request.args.get('sort_key', '').lower()
        sort_dir = request.args.get('sort_dir', '').lower()
        apply_sorting = any([limit_arg, view_mode, sort_key, sort_dir])
        limit = None
        if limit_arg:
            try:
                limit = max(1, min(int(limit_arg), 1000))
            except ValueError:
                limit = None
        
        # [V20260424_2210] Optimization: skip heavy distribution calc unless requested
        include_dist = request.args.get('include_dist', 'false').lower() == 'true'

        result = []
        global_dist = {f"{h:02d}": 0 for h in range(24)} if include_dist else None

        for strategy_name, products in strategies.items():
            for product, data_points in products.items():
                if not data_points:
                    continue

                # Check if data_points is a list (historical snapshots)
                series = data_points if isinstance(data_points, list) else [data_points]

                # [V20260210_1415] Hourly distribution for timebar
                local_dist = None
                if include_dist:
                    local_dist = {f"{h:02d}": 0 for h in range(24)}
                    last_total_count = 0
                    for pt in series:
                        try:
                            ts = datetime.fromisoformat(pt['t'])
                            hr = ts.strftime('%H')
                            curr_total = pt.get('b_c', 0) + pt.get('s_c', 0)
                            delta = max(0, curr_total - last_total_count)
                            if delta > 0:
                                local_dist[hr] += delta
                                if global_dist is not None: global_dist[hr] += delta
                            last_total_count = curr_total
                        except: continue

                # Get the LAST data point (most recent aggregation)
                last = series[-1]
                # [V20260129_1603] Try to extract params from strategy name if empty
                params = last.get('params', '')
                display_strategy = strategy_name
                if not params:
                    if '_' in strategy_name:
                         for prefix in ['breakout_R_Rev_v2_', 'breakout_R_Rev_', 'breakout_Rev_', 'breakout_R_', 'breakout_']:
                             if strategy_name.startswith(prefix):
                                 display_strategy = prefix.rstrip('_')
                                 params = strategy_name[len(prefix):]
                                 break
                         
                result.append({
                    'product': product,
                    'strategy': display_strategy,
                    'params': params,
                    'trade_count': last.get('b_c', 0) + last.get('s_c', 0),
                    'total_net': round(last.get('net', 0), 2),
                    'buy_count': last.get('b_c', 0),
                    'buy_net': round(last.get('buy_net', 0), 2),
                    'sell_count': last.get('s_c', 0),
                    'sell_net': round(last.get('sell_net', 0), 2),
                    'buyPercent': last.get('buyPercent', 0),
                    'sellPercent': last.get('sellPercent', 0),
                    'buy_alt': round(last.get('buy_alt', 0), 2),
                    'sell_alt': round(last.get('sell_alt', 0), 2),
                    'live_buy_net': round(last.get('live_buy', 0), 2),
                    'live_sell_net': round(last.get('live_sell', 0), 2),
                    'time_dist': local_dist # [V20260210_1415]
                })

        # ... (Global dist added below)


        if apply_sorting:
            allowed_keys = {
                'product': 'product',
                'strategy': 'strategy',
                'parm': 'params',
                'params': 'params',
                'total_net': 'total_net',
                'trade_count': 'trade_count',
                'buy_count': 'buy_count',
                'buy_net': 'buy_net',
                'buy_alt': 'buy_alt',
                'sell_count': 'sell_count',
                'sell_net': 'sell_net',
                'sell_alt': 'sell_alt',
                'live_buy': 'live_buy_net',
                'live_sell': 'live_sell_net',
                'buypercent': 'buyPercent',
                'sellpercent': 'sellPercent',
                'buyPercent': 'buyPercent',
                'sellPercent': 'sellPercent'
            }
            key = allowed_keys.get(sort_key, 'total_net')
            numeric_keys = {
                'total_net', 'trade_count', 'buy_count', 'buy_net', 'buy_alt',
                'sell_count', 'sell_net', 'sell_alt', 'live_buy_net', 'live_sell_net',
                'buyPercent', 'sellPercent'
            }
            is_numeric = key in numeric_keys

            result_sorted = sorted(result, key=lambda item: float(item.get(key, 0) or 0) if is_numeric else str(item.get(key, '')).lower())

            if limit:
                view = view_mode if view_mode in ('top', 'bottom') else 'top'
                if view == 'bottom':
                    result_sorted = result_sorted[:limit]
                else:
                    result_sorted = result_sorted[-limit:]

            if sort_dir == 'desc':
                result_sorted.reverse()

            result = result_sorted

        return jsonify({
            'success': True,
            'data': result,
            'snapshot': strategies, # [V20260210_1537] Raw series for playback
            'global_time_dist': global_dist, # [V20260210_1415]
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


@app.route('/api/portfolio_stats', methods=['GET'])
def get_portfolio_stats():
    """
    [V20260323_1945] Hierarchical Performance Stats for Treemap.
    Optimized: Backend filtering by product_type + efficient parsing.
    Part of task: hierarchical_treemap_filters
    """
    try:
        run_mode = request.args.get('mode', 'live')
        date = request.args.get('date')
        product_type_filter = request.args.get('product_type')
        
        if not date:
            date = datetime.now().strftime('%Y-%m-%d')

        # Handle 'all' as None for _iter_day_dirs_for
        p_type_req = None if product_type_filter == 'all' else product_type_filter

        cfg = _load_layout_runtime_config()
        type_mapping = cfg.get("product_type_by_product", {})

        # Get relevant product types
        day_dirs = _iter_day_dirs_for(run_mode, date, p_type_req)
        
        all_items = []
        
        for d_dir in day_dirs:
            # Fallback product type from directory
            dir_product_type = d_dir.parent.name
            if dir_product_type.lower() in ('live', 'sim'):
                dir_product_type = "forex" 
                
            summary_file = d_dir / "_summary_net.json"
            if not summary_file.exists():
                continue
                
            try:
                with open(summary_file, "r") as f:
                    data = json.load(f)
            except:
                continue
                
            strategies = data.get("strategies", {})
            for strat_name, products in strategies.items():
                # [V20260323_1945] PARSE ONCE PER STRATEGY (Optimization)
                parts = strat_name.split('_')
                s_name = "breakout"
                s_window = "unknown"
                s_params = "none"
                window_idx = -1
                param_idx = -1
                for i, p in enumerate(parts):
                    if p in ('2', '3', '4'): window_idx = i
                    if p.lower().startswith('tp'):
                        param_idx = i
                        break
                if param_idx != -1:
                    s_params = "_".join(parts[param_idx:])
                    if window_idx != -1:
                        s_name = "_".join(parts[:window_idx])
                        s_window = parts[window_idx]
                    else:
                        s_name = "_".join(parts[:param_idx])
                else:
                    s_name = strat_name
                s_name = s_name.lower()

                for prod, entries in products.items():
                    if not entries: continue
                    
                    # [V20260323_1900] Definitive categorization
                    p_upper = str(prod).upper()
                    p_type = product_type_for_product(p_upper, cfg)
                    
                    mapping = cfg.get("product_type_by_product", {})
                    if p_upper not in mapping and p_upper.lower() not in mapping:
                        if dir_product_type != "forex":
                            p_type = dir_product_type

                    # Backend Filtering: Skip if it doesn't match requested type
                    if p_type_req and p_type != p_type_req:
                        continue

                    last = entries[-1]
                    net = round(float(last.get('net', 0.0) or 0.0), 2)
                    
                    all_items.append({
                        "product_type": p_type,
                        "product": p_upper,
                        "strategy_name": s_name,
                        "strategy_window": s_window,
                        "strategy_params": s_params,
                        "full_strategy": strat_name,
                        "net": net,
                        "trades": last.get('b_c', 0) + last.get('s_c', 0)
                    })
                    
        return jsonify({
            "success": True,
            "date": date,
            "mode": run_mode,
            "count": len(all_items),
            "items": all_items
        })
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route('/api/virtual_trades', methods=['GET'])
def get_virtual_trades():
    """Load virtual trade JSON files for the given run mode/date."""
    try:
        run_mode = request.args.get('mode', 'live')
        date = request.args.get('date')
        if not date:
            date = datetime.now().strftime('%Y-%m-%d')
        trades = []
        for day_dir in _iter_day_dirs_for(run_mode, date):
            virtual_dir = day_dir / 'virtual'
            if not virtual_dir.exists():
                continue
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
            'trades': trades,
            'session_max_net': session_max_net
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
    sync_grid_live = bool(payload.get("sync_grid_live", False))
    sync_source = str(payload.get("source", "") or "").strip().lower()
    weekly_grid_changes: Dict[Tuple[str, str], Dict[str, Any]] = {}

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
            "source": "ui",
            "products": []
        })

        if isinstance(value, dict):
            requested_active = bool(value.get("active"))
            manual = bool(value.get("manual"))
            source = value.get("source") or entry.get("source", "ui")
            products = value.get("products") or value.get("product") or []
            # [2026-04-07 16:20] V20260407_1620 - Capture auto_promote flag
            auto_promote = bool(value.get("auto_promote", False))
        else:
            requested_active = bool(value)
            manual = False
            source = "ui"
            products = []
            auto_promote = False

        if derived_product:
            products = list(products) + [derived_product]

        products = {p.upper() for p in products if isinstance(p, str)}

        if products:
            if requested_active:
                entry["products"] = sorted(set(entry["products"]) | products)
                entry["active"] = True
                entry["activated_at"] = entry["activated_at"] or now
                entry["auto_promote"] = auto_promote
            else:
                entry["products"] = sorted(set(entry["products"]) - products)
                entry["active"] = bool(entry["products"])
                if not entry["active"]:
                    entry["activated_at"] = None
                    entry["auto_promote"] = auto_promote
                else:
                    # Product-scoped toggles share one activation key.
                    # Keep auto-promote enabled while other products remain active.
                    entry["auto_promote"] = bool(entry.get("auto_promote", False))
        else:
            entry["active"] = requested_active
            entry["activated_at"] = now if requested_active else None
            entry["auto_promote"] = auto_promote

        entry["manual"] = manual
        entry["source"] = source
        # [V20251230_2351] Remove entry if it becomes inactive
        if entry["active"]:
            mode_activations[base_key] = entry
        elif base_key in mode_activations:
            # Remove the entry if it's being deactivated
            del mode_activations[base_key]

        if sync_grid_live and sync_source == "weekly_performance":
            model_name = _strategy_model_from_activation_key(base_key)
            target_products = entry.get("products", []) if isinstance(entry, dict) else []
            if products:
                target_products = sorted(products)
            for product in target_products:
                weekly_grid_changes[(model_name, str(product).upper())] = {
                    "requested_active": bool(requested_active),
                    "manual": bool(manual),
                }

    # Update the mode section
    all_activations[mode] = mode_activations

    # Save all activations
    with open(ACTIVATIONS_FILE, "w") as f:
        json.dump(all_activations, f, indent=4)

    for (model_name, product_name), change in weekly_grid_changes.items():
        _sync_weekly_activation_to_grid_live(
            mode=mode,
            model=model_name,
            product=product_name,
            requested_active=bool(change.get("requested_active")),
            manual=bool(change.get("manual")),
        )

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

@app.route("/api/activations/remove_all", methods=["POST"])
def remove_all_activations():
    """Removes all activation keys for the specified mode. [V20260205_2125]"""
    try:
        payload = request.json or {}
        mode = payload.get('mode', 'live').lower()

        # 1. Clear Activations
        all_activations = _load_activations()
        if mode in all_activations:
            all_activations[mode] = {}
            with open(ACTIVATIONS_FILE, "w") as f:
                json.dump(all_activations, f, indent=4)
        
        # 2. Clear Grid-Live for that mode (to prevent auto-resync)
        # [V20260205_2125] Added to ensure deletions stick
        grid_live_file = ROOT_PATH / "grid_live.json"
        if grid_live_file.exists():
            try:
                with open(grid_live_file, "r") as f:
                    grid_data = json.load(f)
                
                if isinstance(grid_data, dict) and mode in grid_data:
                    grid_data[mode] = []
                    _archive_grid_live(mode) # Archive before clearing
                    with open(grid_live_file, "w") as f:
                        json.dump(grid_data, f, indent=4)
                    print(f"[CLEANUP] grid_live.json ({mode}) cleared via Remove All.")
                elif isinstance(grid_data, list) and mode == 'live':
                    _archive_grid_live(mode, force=True) # [V20260424_2310] Force archive on bucket deletion
                    with open(grid_live_file, "w") as f:
                        json.dump([], f, indent=4)
            except Exception as ge:
                print(f"[ERROR] Failed to clear grid_live during remove_all: {ge}")

        return jsonify({
            "success": True,
            "message": f"Successfully cleared all activations and grid_live entries for {mode}"
        })
            
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# Trade Promotion Helpers [V20260127_1610]
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

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


def _serialize_execution_candidate(trade_path: Path, trade_data: Dict[str, Any]) -> Dict[str, Any]:
    return {
        'path': str(trade_path),
        'filename': trade_path.name,
        'product': str(trade_data.get('product') or '').upper(),
        'direction': str(trade_data.get('direction') or '').upper(),
        'strategy_key': str(trade_data.get('script_name') or trade_data.get('source_strategy') or trade_data.get('app_name') or ''),
        'strategy_params': str(trade_data.get('strategy') or ''),
        'trade_id': trade_data.get('trade_id') or trade_data.get('id'),
        'entry_time': trade_data.get('entry_time'),
        'entry_price': trade_data.get('entry_price'),
        'current_price': trade_data.get('current_price'),
        'status': str(trade_data.get('status') or 'OPEN').upper(),
        'is_live_trade': bool(trade_data.get('is_live_trade') or trade_data.get('order_sent_net') or trade_data.get('order_sent_alt')),
        'order_sent_net': bool(trade_data.get('order_sent_net')),
        'order_sent_alt': bool(trade_data.get('order_sent_alt')),
        'pending_order_request_net': trade_data.get('pending_order_request_net'),
        'pending_order_request_alt': trade_data.get('pending_order_request_alt'),
        'pending_close_request_id': trade_data.get('pending_close_request_id'),
        'source_screen': trade_data.get('source_screen'),
        'source_group': trade_data.get('live_cap_group') or trade_data.get('source_group') or trade_data.get('source_screen') or 'breakout',
        'guid': trade_data.get('guid') or 'unknown',
    }


def _normalize_trade_path(raw_path: Any) -> Optional[Path]:
    if not raw_path:
        return None
    try:
        path = Path(str(raw_path)).resolve()
    except Exception:
        return None
    if ROOT_PATH not in path.parents:
        return None
    if not path.exists() or not path.is_file():
        return None
    return path


def _read_json_file(path: Path) -> Dict[str, Any]:
    with open(path, 'r') as handle:
        data = json.load(handle) or {}
    return data if isinstance(data, dict) else {}


@app.route("/api/l_trade_execution_requests", methods=["GET"])
def get_l_trade_execution_requests():
    status = request.args.get('status')
    requests_data = breakout_common._list_execution_requests(status=status)
    return jsonify({
        'success': True,
        'requests': requests_data,
        'count': len(requests_data),
    })


@app.route("/api/l_trade_execution_requests/approve", methods=["POST"])
def approve_l_trade_execution_requests():
    payload = request.json or {}
    request_ids = payload.get('request_ids') or []
    approved_by = str(payload.get('approved_by') or 'user')
    if not isinstance(request_ids, list) or not request_ids:
        return jsonify({'success': False, 'message': 'request_ids is required'}), 400
    results = [breakout_common.approve_l_trade_execution_request(str(request_id), approved_by=approved_by) for request_id in request_ids]
    failures = [item for item in results if not item.get('success')]
    return jsonify({
        'success': not failures,
        'results': results,
        'approved': len(results) - len(failures),
        'failed': len(failures),
    }), 200 if not failures else 400


@app.route("/api/l_trade_execution_requests/cancel", methods=["POST"])
def cancel_l_trade_execution_requests():
    payload = request.json or {}
    request_ids = payload.get('request_ids') or []
    cancelled_by = str(payload.get('cancelled_by') or 'user')
    reason = str(payload.get('reason') or 'cancelled')
    if not isinstance(request_ids, list) or not request_ids:
        return jsonify({'success': False, 'message': 'request_ids is required'}), 400
    results = [
        breakout_common.cancel_l_trade_execution_request(str(request_id), cancelled_by=cancelled_by, reason=reason)
        for request_id in request_ids
    ]
    failures = [item for item in results if not item.get('success')]
    return jsonify({
        'success': not failures,
        'results': results,
        'cancelled': len(results) - len(failures),
        'failed': len(failures),
    }), 200 if not failures else 400


@app.route("/api/l_trade_open_candidates", methods=["GET"])
def get_l_trade_open_candidates():
    mode = str(request.args.get('mode') or 'live').lower()
    date_str = str(request.args.get('date') or datetime.now().strftime('%Y-%m-%d'))
    candidates = []
    for trade_info in _scan_open_trades(mode, date_str):
        trade_data = trade_info.get('data') or {}
        if str(trade_data.get('status') or 'OPEN').upper() != 'OPEN':
            continue
        if bool(trade_data.get('order_sent_net') or trade_data.get('order_sent_alt') or trade_data.get('is_live_trade')):
            continue
        candidates.append(_serialize_execution_candidate(trade_info['path'], trade_data))
    return jsonify({'success': True, 'candidates': candidates, 'count': len(candidates)})


@app.route("/api/l_trade_close_candidates", methods=["GET"])
def get_l_trade_close_candidates():
    mode = str(request.args.get('mode') or 'live').lower()
    date_str = str(request.args.get('date') or datetime.now().strftime('%Y-%m-%d'))
    candidates = []
    for trade_info in _scan_open_trades(mode, date_str):
        trade_data = trade_info.get('data') or {}
        if str(trade_data.get('status') or 'OPEN').upper() != 'OPEN':
            continue
        if not bool(trade_data.get('order_sent_net') or trade_data.get('order_sent_alt') or trade_data.get('is_live_trade')):
            continue
        candidates.append(_serialize_execution_candidate(trade_info['path'], trade_data))
    return jsonify({'success': True, 'candidates': candidates, 'count': len(candidates)})


@app.route("/api/l_trade_execution_requests/open", methods=["POST"])
def queue_l_trade_open_requests():
    payload = request.json or {}
    trade_paths = payload.get('trade_paths') or []
    requested_by = str(payload.get('requested_by') or 'manual_execution_center')
    if not isinstance(trade_paths, list) or not trade_paths:
        return jsonify({'success': False, 'message': 'trade_paths is required'}), 400

    results = []
    for raw_path in trade_paths:
        trade_path = _normalize_trade_path(raw_path)
        if trade_path is None:
            results.append({'success': False, 'message': f'Invalid trade path: {raw_path}'})
            continue
        try:
            trade_data = _read_json_file(trade_path)
        except Exception as exc:
            results.append({'success': False, 'message': f'Failed to load {trade_path.name}: {exc}'})
            continue
        direction = str(trade_data.get('direction') or '').upper()
        strategy_key = str(payload.get('strategy_key') or trade_data.get('script_name') or trade_data.get('source_strategy') or '')
        current_price = trade_data.get('current_price')
        if current_price is None:
            current_price = trade_data.get('entry_price')
        marker = breakout_common._create_l_trade_order(
            product=str(trade_data.get('product') or '').upper(),
            direction=direction,
            strategy_key=strategy_key,
            trade_id=str(trade_data.get('trade_id') or trade_data.get('id') or ''),
            current_price=float(current_price or 0.0),
            latest_bid=trade_data.get('current_price'),
            latest_ask=trade_data.get('current_price'),
            mode=str(payload.get('mode') or 'net').lower(),
            is_close=False,
            source=str(payload.get('source') or trade_data.get('source_screen') or 'execution_center'),
            source_group=str(trade_data.get('live_cap_group') or trade_data.get('source_group') or trade_data.get('source_screen') or 'execution_center'),
            guid=str(trade_data.get('guid') or 'unknown'),
            trade_json_path=str(trade_path),
            requested_by=requested_by,
            force_execution_request=True,
        )
        request_id = breakout_common._execution_request_id_from_marker(marker)
        if request_id:
            results.append({'success': True, 'request_id': request_id, 'path': str(trade_path)})
        else:
            results.append({'success': False, 'message': breakout_common._LAST_L_TRADE_ORDER_ERROR or 'Failed to queue request', 'path': str(trade_path)})

    failures = [item for item in results if not item.get('success')]
    return jsonify({
        'success': not failures,
        'results': results,
        'queued': len(results) - len(failures),
        'failed': len(failures),
    }), 200 if not failures else 400


@app.route("/api/l_trade_execution_requests/close", methods=["POST"])
def queue_l_trade_close_requests():
    payload = request.json or {}
    trade_paths = payload.get('trade_paths') or []
    requested_by = str(payload.get('requested_by') or 'manual_execution_center')
    exit_reason = str(payload.get('exit_reason') or 'Manual Close')
    if not isinstance(trade_paths, list) or not trade_paths:
        return jsonify({'success': False, 'message': 'trade_paths is required'}), 400

    results = []
    for raw_path in trade_paths:
        trade_path = _normalize_trade_path(raw_path)
        if trade_path is None:
            results.append({'success': False, 'message': f'Invalid trade path: {raw_path}'})
            continue
        try:
            trade_data = _read_json_file(trade_path)
        except Exception as exc:
            results.append({'success': False, 'message': f'Failed to load {trade_path.name}: {exc}'})
            continue
        current_price = trade_data.get('current_price')
        if current_price is None:
            current_price = trade_data.get('entry_price')
        exit_time = datetime.now().isoformat()
        marker = breakout_common._create_l_trade_order(
            product=str(trade_data.get('product') or '').upper(),
            direction=str(trade_data.get('direction') or '').upper(),
            strategy_key=str(trade_data.get('script_name') or trade_data.get('source_strategy') or ''),
            trade_id=str(trade_data.get('trade_id') or trade_data.get('id') or ''),
            current_price=float(current_price or 0.0),
            latest_bid=trade_data.get('current_price'),
            latest_ask=trade_data.get('current_price'),
            mode='net',
            is_close=True,
            source=str(trade_data.get('source_screen') or 'execution_center'),
            source_group=str(trade_data.get('live_cap_group') or trade_data.get('source_group') or trade_data.get('source_screen') or 'execution_center'),
            guid=str(trade_data.get('guid') or 'unknown'),
            trade_json_path=str(trade_path),
            request_context={
                'exit_time': exit_time,
                'exit_price': current_price,
                'exit_reason': exit_reason,
            },
            requested_by=requested_by,
            force_execution_request=True,
        )
        request_id = breakout_common._execution_request_id_from_marker(marker)
        if request_id:
            results.append({'success': True, 'request_id': request_id, 'path': str(trade_path)})
        else:
            results.append({'success': False, 'message': breakout_common._LAST_L_TRADE_ORDER_ERROR or 'Failed to queue close request', 'path': str(trade_path)})

    failures = [item for item in results if not item.get('success')]
    return jsonify({
        'success': not failures,
        'results': results,
        'queued': len(results) - len(failures),
        'failed': len(failures),
    }), 200 if not failures else 400


@app.route("/api/config", methods=["GET"])
def get_config():
    try:
        with open(CONFIG_FILE, "r") as f:
            cfg = json.load(f)
            if isinstance(cfg, dict):
                cfg.setdefault('l_trade_auto_execution', True)
            return jsonify({"success": True, "config": cfg})
    except Exception:
        return jsonify({"success": True, "config": {"l_trade_auto_execution": True}})


def _normalize_weekly_performance_state(raw_state: Any) -> dict:
    def _normalize_weekly_product_type(raw_value: Any) -> Optional[str]:
        normalized = str(raw_value or "").strip().lower()
        if normalized in {"forex", "indices", "metals", "crypto", "energy"}:
            return normalized
        return None

    normalized_state = {
        "auto_select_modes": {},
        "auto_select_permitted_types": [],
        "selected_product_type": "forex",
        "selected_target_date": None,
    }
    if not isinstance(raw_state, dict):
        return normalized_state

    raw_modes = raw_state.get("auto_select_modes", {})
    if isinstance(raw_modes, dict):
        for raw_key, raw_value in raw_modes.items():
            key = str(raw_key or "").strip().lower()
            value = str(raw_value or "").strip()
            if key and value:
                normalized_state["auto_select_modes"][key] = value

    raw_permitted = raw_state.get("auto_select_permitted_types", [])
    if isinstance(raw_permitted, list):
        for raw_type in raw_permitted:
            normalized_type = _normalize_weekly_product_type(raw_type)
            if normalized_type and normalized_type not in normalized_state["auto_select_permitted_types"]:
                normalized_state["auto_select_permitted_types"].append(normalized_type)

    selected_product_type = _normalize_weekly_product_type(raw_state.get("selected_product_type"))
    if selected_product_type:
        normalized_state["selected_product_type"] = selected_product_type

    raw_selected_target_date = str(raw_state.get("selected_target_date") or "").strip()
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", raw_selected_target_date):
        normalized_state["selected_target_date"] = raw_selected_target_date

    return normalized_state


def _load_weekly_performance_state() -> dict:
    try:
        with open(WEEKLY_PERFORMANCE_STATE_FILE, "r") as f:
            return _normalize_weekly_performance_state(json.load(f))
    except Exception:
        return _normalize_weekly_performance_state({})


def _save_weekly_performance_state(state: dict) -> dict:
    normalized_state = _normalize_weekly_performance_state(state)
    with open(WEEKLY_PERFORMANCE_STATE_FILE, "w") as f:
        json.dump(normalized_state, f, indent=4)
    return normalized_state


def _week_dates_between(week_start, week_end) -> List[str]:
    return [
        (week_start + timedelta(days=offset)).strftime("%Y-%m-%d")
        for offset in range((week_end - week_start).days + 1)
    ]


def _weekly_stats_artifact_is_stale(
    *,
    stats_file: Path,
    product_type: str,
    week_start,
    week_end,
    source_filename: str,
) -> bool:
    if not stats_file.exists():
        return True

    week_start_date = week_start.date() if hasattr(week_start, "date") else week_start
    week_end_date = week_end.date() if hasattr(week_end, "date") else week_end
    today = datetime.now().date()
    if week_start_date <= today <= week_end_date:
        return True

    try:
        stats_mtime = stats_file.stat().st_mtime
    except OSError:
        return True

    product_base = BASE_PATH / "live" / product_type
    for date_str in _week_dates_between(week_start_date, week_end_date):
        source_file = product_base / date_str / source_filename
        if not source_file.exists():
            continue
        try:
            if source_file.stat().st_mtime > stats_mtime:
                return True
        except OSError:
            return True

    return False


@app.route("/api/weekly_performance_state", methods=["GET"])
def get_weekly_performance_state():
    state = _load_weekly_performance_state()
    cfg = _load_layout_runtime_config()
    payload = {
        "auto_select_modes": state.get("auto_select_modes", {}),
        "auto_select_permitted_types": state.get("auto_select_permitted_types", []),
        "selected_product_type": state.get("selected_product_type", "forex"),
        "selected_target_date": state.get("selected_target_date"),
        "vtrade_persistence_seconds": cfg.get("vtrade_persistence_seconds", 60),
        "product_type_by_product": cfg.get("product_type_by_product", {}),
        "scalper_ratio": cfg.get("scalper_ratio"),
        "rev_scalper_ratio": cfg.get("rev_scalper_ratio"),
    }
    return jsonify({"success": True, "state": payload})


@app.route("/api/weekly_performance_state", methods=["POST"])
def update_weekly_performance_state():
    incoming = request.json
    if not isinstance(incoming, dict):
        return jsonify({"success": False, "message": "Invalid weekly performance state"}), 400

    current_state = _load_weekly_performance_state()
    current_state.update(incoming)
    saved_state = _save_weekly_performance_state(current_state)
    return jsonify({"success": True, "state": saved_state})


@app.route("/api/config", methods=["POST"])
def update_config():
    incoming = request.json
    if not isinstance(incoming, dict):
        return jsonify({"success": False, "message": "Invalid config"}), 400

    incoming = dict(incoming)
    incoming.pop("auto_select_modes", None)
    incoming.pop("auto_select_permitted_types", None)

    # [V20260204_1410] 2026-02-04 14:10: Catch re-enabling Frequency Notifier to deactivate buckets
    old_cfg = {}
    try:
        with open(CONFIG_FILE, "r") as f:
            old_cfg = json.load(f)
    except:
        pass

    data = dict(old_cfg)
    data.update(incoming)
    if 'l_trade_auto_execution' not in data:
        data['l_trade_auto_execution'] = True
    else:
        data['l_trade_auto_execution'] = bool(data.get('l_trade_auto_execution'))

    # If rank_alert_suspended was true and is now false (or missing/false)
    was_suspended = old_cfg.get('rank_alert_suspended', False)
    is_suspended = data.get('rank_alert_suspended', False)
    
    if was_suspended and not is_suspended:
        print("[CONFIG] Frequency Notifier re-enabled. Deactivating Trade Buckets (Mutual Exclusion).")
        _deactivate_all_trade_buckets('live')
        _deactivate_all_trade_buckets('sim')
        # [V20260205_2100] Set automated source to Frequency
        _update_automated_source('Frequency')
        # Trigger grid sync for clean state
        _sync_bucket_to_grid_live({'name': 'cleanup', 'live': False}, 'live', datetime.now().strftime('%Y-%m-%d'))

    # Normalize automated source fields (backward compatible single + new multi)
    src_multi = data.get('automated_trade_sources')
    if isinstance(src_multi, list):
        normalized = []
        for s in src_multi:
            if isinstance(s, str) and s.strip():
                sv = s.strip()
                if sv not in normalized:
                    normalized.append(sv)
        data['automated_trade_sources'] = normalized
        if normalized:
            data['automated_trade_source'] = normalized[0]
    elif isinstance(data.get('automated_trade_source'), str) and data.get('automated_trade_source').strip():
        data['automated_trade_source'] = data['automated_trade_source'].strip()
        data['automated_trade_sources'] = [data['automated_trade_source']]

    normalized_product_type = default_product_type(data)
    data['product_type'] = normalized_product_type
    data['product_types'] = configured_product_types(data)
    raw_trade_products = data.get('trade_products', [])
    if isinstance(raw_trade_products, list):
        normalized_trade_products = []
        for raw_product in raw_trade_products:
            product_value = str(raw_product or '').strip().upper()
            if product_value and product_value not in normalized_trade_products:
                normalized_trade_products.append(product_value)
        data['trade_products'] = normalized_trade_products
    raw_mapping = data.get('product_type_by_product', {})
    normalized_mapping = {}
    if isinstance(raw_mapping, dict):
        for raw_key, raw_value in raw_mapping.items():
            key = str(raw_key or '').strip().upper()
            if not key:
                continue
            normalized_mapping[key] = product_type_for_product(key, {
                'product_type': normalized_product_type,
                'product_type_by_product': raw_mapping,
            })
    data['product_type_by_product'] = normalized_mapping
    if data.get('default_min_value') is None:
        data['default_min_value'] = 10.0
    raw_min_by_type = data.get('min_value_by_product_type', {})
    normalized_min_by_type = {}
    if isinstance(raw_min_by_type, dict):
        for raw_key, raw_value in raw_min_by_type.items():
            key = str(raw_key or '').strip().lower()
            if not key:
                continue
            try:
                normalized_min_by_type[key] = float(raw_value)
            except (TypeError, ValueError):
                continue
    if not normalized_min_by_type and data.get('default_min_value') is not None:
        normalized_min_by_type[normalized_product_type] = float(data['default_min_value'])
    data['min_value_by_product_type'] = normalized_min_by_type
    raw_min_by_product = data.get('min_value_by_product', {})
    normalized_min_by_product = {}
    if isinstance(raw_min_by_product, dict):
        for raw_key, raw_value in raw_min_by_product.items():
            key = str(raw_key or '').strip().upper()
            if not key:
                continue
            try:
                normalized_min_by_product[key] = float(raw_value)
            except (TypeError, ValueError):
                continue
    data['min_value_by_product'] = normalized_min_by_product
    raw_move_by_product = data.get('min_move_by_product', {})
    normalized_move_by_product = {}
    if isinstance(raw_move_by_product, dict):
        for raw_key, raw_value in raw_move_by_product.items():
            key = str(raw_key or '').strip().upper()
            if not key:
                continue
            try:
                normalized_move_by_product[key] = float(raw_value)
            except (TypeError, ValueError):
                continue
    data['min_move_by_product'] = normalized_move_by_product
    if data.get('crypto_trade_qty_percent') is None:
        data['crypto_trade_qty_percent'] = data.get('trade_qty_percent', 45.0)

    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=4)

    return jsonify({"success": True})


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "ts": datetime.utcnow().isoformat()})


@app.route("/multi_chart.html")
def serve_multi_chart():
    return send_from_directory(ROOT_PATH, "multi_chart.html")


# [V20260225] Live Hub routes for IP-based hosting
LANDING_PATH = Path(__file__).parent.parent / "piphunter" / "landing"

@app.route("/live")
@app.route("/live/")
def serve_live_hub():
    """Serve the PipHunter Live Hub website"""
    return send_from_directory(LANDING_PATH, "breakout-live-hub.html")

@app.route("/live/<path:subpath>")
def serve_live_assets(subpath):
    """Serve Live Hub static assets (styles, images, etc.)"""
    return send_from_directory(LANDING_PATH, subpath)


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
        product_type = request.args.get('product_type')
        date = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))
        
        for file_path in [day_dir / "_top_one.json" for day_dir in _iter_day_dirs_for(run_mode, date, product_type)]:
            if not file_path.exists():
                continue
            with open(file_path, 'r') as f:
                content = json.load(f)
            return jsonify({
                'success': True,
                'content': content
            })
        return jsonify({
            'success': False,
            'message': f'Summary file not found for {date} ({run_mode})',
            'content': None
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


# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# Trade Buckets Activation Sync [V20260122_2230]
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

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


# [V20260424_2230] Global throttle for grid archiving
_last_grid_archive_time = 0

def _cleanup_grid_live_history(history_dir: Path, max_files: int = 1000):
    """
    [V20260424_2230] Prune old history files to prevent disk/inode bloat.
    Keeps only the most recent N files.
    """
    try:
        files = sorted(history_dir.glob("grid_live_*.json"), key=lambda x: x.stat().st_mtime)
        if len(files) > max_files:
            to_delete = files[:len(files) - max_files]
            for f in to_delete:
                try:
                    f.unlink()
                except: pass
            print(f"[ARCHIVE-CLEANUP] Deleted {len(to_delete)} old history files.")
    except Exception as e:
        print(f"[ARCHIVE-CLEANUP-ERROR] {e}")

def _archive_grid_live(mode, new_data=None, force=False):
    """
    [V20260205_2130] Archive grid_live.json to individual files in grid_live_history directory.
    [V20260424_2230] Added throttling (1 min) and automatic pruning (1000 files).
    [V20260424_2310] Conditional Archiving: only record if product/metric change or force=True.
    """
    global _last_grid_archive_time
    try:
        source_file = ROOT_PATH / "grid_live.json"
        if not source_file.exists():
            return

        # [V20260424_2310] Change Detection Logic
        should_archive = force
        if not should_archive and new_data is not None:
            try:
                with open(source_file, "r") as f:
                    old_data_full = json.load(f)

                old_list = old_data_full.get(mode, []) if isinstance(old_data_full, dict) else (old_data_full if mode == 'live' else [])
                new_list = new_data.get(mode, []) if isinstance(new_data, dict) else new_data

                # Compare critical fields for each model
                old_map = {m.get('model'): (m.get('product'), m.get('metric')) for m in old_list if m.get('model')}
                new_map = {m.get('model'): (m.get('product'), m.get('metric')) for m in new_list if m.get('model')}

                # 1. Check for changes in existing or new models
                for model, (prod, met) in new_map.items():
                    if model not in old_map:
                        should_archive = True # New model added to grid
                        break
                    if old_map[model] != (prod, met):
                        should_archive = True # Product or Metric changed
                        break

                # 2. Check for removals (pruning)
                if not should_archive:
                    for model in old_map:
                        if model not in new_map:
                            should_archive = True # Model removed (significant state change)
                            break
            except:
                should_archive = True # Fallback to archive on error

        if not should_archive:
            return

        now = time.time()
        if now - _last_grid_archive_time < 60 and not force: # Throttle unless forced
            return
        _last_grid_archive_time = now

        # [V20260205_2130] Dedicated history directory
        history_dir = ROOT_PATH / "grid_live_history"
        if not history_dir.exists():
            try:
                history_dir.mkdir(parents=True, exist_ok=True)
            except: pass

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        history_file = history_dir / f"grid_live_{mode}_{timestamp}.json"

        with open(source_file, "r") as f:
            current_data = json.load(f)

        with open(history_file, "w") as f:
            json.dump(current_data, f, indent=4)

        # [V20260424_2230] Run cleanup after new archive created
        _cleanup_grid_live_history(history_dir)

        print(f"[ARCHIVE] grid_live archived to {history_file} (force={force})")
    except Exception as e:
        print(f"[ARCHIVE-ERROR] Failed to archive grid_live: {e}")

def _prune_grid_live_siblings(model: str, product: str, mode: str, reason: str = '') -> Dict[str, Any]:
    """
    Remove sibling products for the same model after a live execution.
    Keeps only entries that match the executed product for the model.
    """
    try:
        if not model or not product:
            return {"success": False, "removed": 0, "message": "model/product required"}

        grid_live_file = ROOT_PATH / "grid_live.json"
        if not grid_live_file.exists():
            return {"success": True, "removed": 0, "message": "grid_live.json missing"}

        with GRID_LIVE_LOCK:
            full_data = {'live': [], 'sim': []}
            try:
                with open(grid_live_file, "r") as f:
                    loaded = json.load(f)
                if isinstance(loaded, list):
                    full_data['live'] = loaded
                elif isinstance(loaded, dict):
                    full_data = loaded
            except Exception as e:
                return {"success": False, "removed": 0, "message": f"load failed: {e}"}

            mode_list = full_data.get(mode, [])
            removed = []
            kept = []
            for item in mode_list:
                if item.get('model') == model and str(item.get('product', '')).upper() != str(product).upper():
                    removed.append(item)
                else:
                    kept.append(item)

            if not removed:
                return {"success": True, "removed": 0}

            _archive_grid_live(mode, force=True) # [V20260424_2310] Force archive on bucket deletion

            full_data[mode] = kept
            with open(grid_live_file, "w") as f:
                json.dump(full_data, f, indent=4)

            _sync_grid_to_activations(kept, mode=mode)

        if removed:
            print(f"[PRUNE] Removed {len(removed)} sibling entries for {model} on {mode} (reason={reason})")
        return {"success": True, "removed": len(removed)}
    except Exception as e:
        print(f"[PRUNE-ERROR] {e}")
        return {"success": False, "removed": 0, "message": str(e)}

def _load_config_safe() -> Dict[str, Any]:
    try:
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
    except Exception:
        pass
    return {}

def _default_realtime_trade_close_config() -> dict[str, Any]:
    return {
        "enabled": True,
        "enabled_policies": ["opposite_signal"],
        "evaluate_on_realtime_stats": True,
        "evaluate_on_trade_log": True,
        "policies": {
            "opposite_signal": {
                "enabled": True,
                "require_executable_signal": True,
                "ignore_no_trade": True,
                "ignore_stale_snapshot": True,
            },
            "net_pips_after_cost_threshold": {
                "enabled": False,
                "threshold_pips": 5,
                "threshold_options": [3, 5, 10, 20],
            }
        },
    }

def _merge_nested_dict(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    merged = dict(base)
    for key, value in (override or {}).items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = _merge_nested_dict(merged[key], value)
        else:
            merged[key] = value
    return merged

def _load_realtime_trade_close_config() -> dict[str, Any]:
    cfg = _load_config_safe()
    raw = cfg.get("realtime_trade_close_config")
    merged = _merge_nested_dict(_default_realtime_trade_close_config(), raw if isinstance(raw, dict) else {})
    enabled_policies = merged.get("enabled_policies")
    if not isinstance(enabled_policies, list):
        enabled_policies = ["opposite_signal"]
    normalized_enabled: list[str] = []
    for item in enabled_policies:
        policy = str(item or "").strip().lower()
        if policy and policy in REALTIME_TRADE_CLOSE_AVAILABLE_POLICIES and policy not in normalized_enabled:
            normalized_enabled.append(policy)
    if not normalized_enabled:
        normalized_enabled = ["opposite_signal"]
    merged["enabled_policies"] = normalized_enabled
    policies = merged.get("policies")
    merged["policies"] = policies if isinstance(policies, dict) else {}
    for policy_name in REALTIME_TRADE_CLOSE_AVAILABLE_POLICIES:
        policy_cfg = merged["policies"].get(policy_name)
        if not isinstance(policy_cfg, dict):
            merged["policies"][policy_name] = {}
    return merged

def _parse_summary_point_ts(value: Any) -> Optional[datetime]:
    """Parse summary point timestamp into a timezone-aware datetime (UTC)."""
    if not value:
        return None
    try:
        dt = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    except Exception:
        return None

def _derive_bias_from_summary(mode: str, date_str: str, recent_window_minutes: int = 60, product_type: str | None = None) -> Dict[str, Any]:
    """
    Canonical bias derivation from _summary_net.json only.

    Returned fields (for strategy_performance bias display):
    - timestamp: summary last_update
    - bias: day bias from signed totals (BUY if total_buy_net >= total_sell_net else SELL)
    - market_condition: CHOPPY/TRENDING from configured thresholds
    - status: STRONG when recent bias aligns with day bias, else MIXED
    - recent_buy_pnl / recent_sell_pnl: trailing-window deltas from cumulative buy/sell nets
    - recent_buy_count / recent_sell_count: trailing-window deltas from cumulative counts
    - total_buy_net / total_sell_net: full current signed totals at summary timestamp
    """
    summary_file = _resolve_day_dir(mode, date_str, product_type=product_type) / "_summary_net.json"
    if not summary_file.exists():
        return {
            "success": False,
            "error": f"missing summary file: {summary_file}"
        }

    try:
        with open(summary_file, "r") as f:
            summary = json.load(f) or {}
    except Exception as e:
        return {"success": False, "error": f"failed reading summary: {e}"}

    raw_last_update = summary.get("last_update")
    cut_dt = _parse_summary_point_ts(raw_last_update) or datetime.now(timezone.utc)
    window_start = cut_dt - timedelta(minutes=max(1, int(recent_window_minutes or 60)))

    strategies = summary.get("strategies", {})
    if not isinstance(strategies, dict):
        strategies = {}

    total_buy_net = 0.0
    total_sell_net = 0.0
    recent_buy_pnl = 0.0
    recent_sell_pnl = 0.0
    recent_buy_count = 0
    recent_sell_count = 0
    latest_point_dt: Optional[datetime] = None

    for _model, products in strategies.items():
        if not isinstance(products, dict):
            continue
        for _product, points in products.items():
            if not isinstance(points, list) or not points:
                continue

            # Keep points that can be timestamped and are <= cutoff
            typed_points: List[Tuple[datetime, Dict[str, Any]]] = []
            for p in points:
                if not isinstance(p, dict):
                    continue
                p_dt = _parse_summary_point_ts(p.get("t"))
                if p_dt is None or p_dt > cut_dt:
                    continue
                typed_points.append((p_dt, p))

            if not typed_points:
                continue

            typed_points.sort(key=lambda x: x[0])
            last_dt, last_pt = typed_points[-1]
            if latest_point_dt is None or last_dt > latest_point_dt:
                latest_point_dt = last_dt

            last_buy = float(last_pt.get("buy_net", 0.0) or 0.0)
            last_sell = float(last_pt.get("sell_net", 0.0) or 0.0)
            last_bc = int(last_pt.get("b_c", 0) or 0)
            last_sc = int(last_pt.get("s_c", 0) or 0)

            base_buy = 0.0
            base_sell = 0.0
            base_bc = 0
            base_sc = 0
            for p_dt, p in typed_points:
                if p_dt <= window_start:
                    base_buy = float(p.get("buy_net", 0.0) or 0.0)
                    base_sell = float(p.get("sell_net", 0.0) or 0.0)
                    base_bc = int(p.get("b_c", 0) or 0)
                    base_sc = int(p.get("s_c", 0) or 0)
                else:
                    break

            total_buy_net += last_buy
            total_sell_net += last_sell
            recent_buy_pnl += (last_buy - base_buy)
            recent_sell_pnl += (last_sell - base_sell)
            recent_buy_count += max(0, last_bc - base_bc)
            recent_sell_count += max(0, last_sc - base_sc)

    day_bias = "BUY" if total_buy_net >= total_sell_net else "SELL"
    if recent_buy_pnl == recent_sell_pnl:
        recent_bias = day_bias
    else:
        recent_bias = "BUY" if recent_buy_pnl > recent_sell_pnl else "SELL"
    status = "STRONG" if day_bias == recent_bias else "MIXED"

    cfg = _load_config_safe()
    pnl_threshold = float(cfg.get("picker_pnl_spread_threshold", 2000) or 2000)
    count_threshold = float(cfg.get("picker_count_diff_threshold", 0.05) or 0.05)
    pnl_spread = abs(recent_buy_pnl - recent_sell_pnl)
    total_recent = recent_buy_count + recent_sell_count
    count_diff_pct = abs(recent_buy_count - recent_sell_count) / max(1, total_recent)
    is_choppy = (count_diff_pct <= count_threshold) or (pnl_spread < pnl_threshold)
    market_condition = "CHOPPY" if is_choppy else "TRENDING"

    return {
        "success": True,
        "source": "_summary_net.json",
        "timestamp": cut_dt.isoformat(),
        "last_update": raw_last_update,
        "latest_series_point": latest_point_dt.isoformat() if latest_point_dt else None,
        "run_mode": mode,
        "date": date_str,
        "product_type": product_type or default_product_type(_load_layout_runtime_config()),
        "bias": day_bias,
        "day_bias": day_bias,
        "recent_bias": recent_bias,
        "status": status,
        "market_condition": market_condition,
        "total_buy_net": round(total_buy_net, 2),
        "total_sell_net": round(total_sell_net, 2),
        "recent_buy_pnl": round(recent_buy_pnl, 2),
        "recent_sell_pnl": round(recent_sell_pnl, 2),
        "recent_buy_count": int(recent_buy_count),
        "recent_sell_count": int(recent_sell_count),
        "recent_window_minutes": int(max(1, int(recent_window_minutes or 60))),
    }

@app.route('/api/bias_from_summary', methods=['GET'])
def api_bias_from_summary():
    """Return canonical bias fields derived only from _summary_net.json."""
    try:
        mode = str(request.args.get('mode', 'live')).lower()
        date_str = request.args.get('date') or datetime.now(timezone.utc).strftime('%Y-%m-%d')
        product_type = request.args.get('product_type')
        recent_window_minutes = int(request.args.get('window_minutes', 60) or 60)
        payload = _derive_bias_from_summary(mode, date_str, recent_window_minutes, product_type)
        if not payload.get("success"):
            return jsonify(payload), 404
        return jsonify(payload)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

def _get_current_bias(mode: str, date_str: str) -> Optional[str]:
    try:
        bias_file = _resolve_day_dir(mode, date_str) / "_targeted_strategies.json"
        if not bias_file.exists():
            return None
        with open(bias_file, "r") as f:
            data = json.load(f)
        bias = data.get("bias")
        if bias:
            return str(bias).upper()
    except Exception:
        return None
    return None

def _select_psb_siblings(mode: str, date_str: str, bias: str, max_items: int) -> List[Dict[str, Any]]:
    summary_file = _resolve_day_dir(mode, date_str) / "_summary_net.json"
    if not summary_file.exists():
        return []
    try:
        with open(summary_file, "r") as f:
            summary_data = json.load(f)
    except Exception:
        return []

    strategies = summary_data.get("strategies", {})
    if not isinstance(strategies, dict):
        return []

    metric_key = "buy_net" if bias == "BUY" else "sell_net"
    count_key = "b_c" if bias == "BUY" else "s_c"
    total_key = "net"

    best_model = None
    best_metric = -float("inf")
    best_count = -1

    for model_name, products in strategies.items():
        if not isinstance(products, dict):
            continue
        for product, points in products.items():
            if not isinstance(points, list) or not points:
                continue
            last = points[-1]
            metric_val = float(last.get(metric_key, 0) or 0)
            count_val = int(last.get(count_key, 0) or 0)
            total_val = float(last.get(total_key, 0) or 0)
            if metric_val > 0 and count_val > 0 and total_val > 0:
                if metric_val > best_metric or (metric_val == best_metric and count_val > best_count):
                    best_metric = metric_val
                    best_count = count_val
                    best_model = model_name

    if not best_model:
        return []

    siblings = []
    products = strategies.get(best_model, {})
    if not isinstance(products, dict):
        return []
    for product, points in products.items():
        if not isinstance(points, list) or not points:
            continue
        last = points[-1]
        metric_val = float(last.get(metric_key, 0) or 0)
        count_val = int(last.get(count_key, 0) or 0)
        total_val = float(last.get(total_key, 0) or 0)
        # Enforce bias-specific profitability per strategy/product, not just at model selection stage.
        if metric_val <= 0 or count_val <= 0 or total_val <= 0:
            continue
        siblings.append({
            "model": best_model,
            "product": product,
            "metric": "buy_net" if bias == "BUY" else "sell_net",
            "metric_val": metric_val,
            "count_val": count_val
        })

    siblings.sort(key=lambda x: (x["metric_val"], x["count_val"]), reverse=True)
    return siblings[:max_items]

def _select_psb_family_entries(mode: str, date_str: str, bias: str, max_items: int) -> List[Dict[str, Any]]:
    """
    Select strategy/product candidates from the highest-priority family
    that matches market bias.

    BUY  -> family side 'buy'
    SELL -> family side 'sell'
    """
    priority_file = ROOT_PATH / "json" / "strategy_profile" / "priority_strategy_list.json"
    members_file = ROOT_PATH / "json" / "strategy_profile" / "strategy_profile_equivalent_family_members.json"
    summary_file = _resolve_day_dir(mode, date_str) / "_summary_net.json"

    if not priority_file.exists() or not members_file.exists() or not summary_file.exists():
        return []

    try:
        with open(priority_file, "r") as f:
            priority_data = json.load(f)
        with open(members_file, "r") as f:
            family_members = json.load(f)
        with open(summary_file, "r") as f:
            summary_data = json.load(f)
    except Exception:
        return []

    priorities = []
    if isinstance(priority_data, list):
        priorities = priority_data
    elif isinstance(priority_data, dict):
        priorities = priority_data.get("priorities", [])

    if not isinstance(priorities, list) or not isinstance(family_members, list):
        return []

    target_side = "buy" if str(bias).upper() == "BUY" else "sell"
    selected_family = None
    for item in priorities:
        if str(item.get("side", "")).lower() == target_side:
            selected_family = str(item.get("family_id", "")).strip()
            if selected_family:
                break
    if not selected_family:
        return []

    strategies = {
        str(m.get("strategy", "")).strip()
        for m in family_members
        if str(m.get("family_id", "")).strip() == selected_family
        and str(m.get("side", "")).lower() == target_side
    }
    if not strategies:
        return []

    strategies_blob = summary_data.get("strategies", {})
    if not isinstance(strategies_blob, dict):
        return []

    metric_key = "buy_net" if target_side == "buy" else "sell_net"
    count_key = "b_c" if target_side == "buy" else "s_c"
    total_key = "net"

    entries = []
    for model_name in strategies:
        products = strategies_blob.get(model_name, {})
        if not isinstance(products, dict):
            continue
        for product, points in products.items():
            if not isinstance(points, list) or not points:
                continue
            last = points[-1]
            metric_val = float(last.get(metric_key, 0) or 0)
            count_val = int(last.get(count_key, 0) or 0)
            total_val = float(last.get(total_key, 0) or 0)
            # Enforce per-product positivity for execution candidates.
            if metric_val <= 0 or count_val <= 0 or total_val <= 0:
                continue
            entries.append({
                "family_id": selected_family,
                "model": model_name,
                "product": product,
                "metric": metric_key,
                "metric_val": metric_val,
                "count_val": count_val
            })

    entries.sort(key=lambda x: (x["metric_val"], x["count_val"]), reverse=True)
    return entries[:max_items]

def _grid_is_empty(mode: str) -> bool:
    grid_live_file = ROOT_PATH / "grid_live.json"
    if not grid_live_file.exists():
        return True
    try:
        with open(grid_live_file, "r") as f:
            data = json.load(f)
        if isinstance(data, list):
            return len(data) == 0
        if isinstance(data, dict):
            return len(data.get(mode, [])) == 0
    except Exception:
        return True
    return True


def _normalize_bucket_metric(metric: Any) -> str:
    raw = str(metric or "net").strip().lower()
    if raw in ("buy", "buy_net", "buy_net_return_sum"):
        return "buy_net"
    if raw in ("sell", "sell_net", "sell_net_return_sum"):
        return "sell_net"
    if raw in ("alt", "alt_net", "buy_alt", "sell_alt"):
        return "alt_net"
    return "net"


def _trade_direction_key(trade: dict) -> str:
    direction = str((trade or {}).get("direction") or "").strip().upper()
    if direction in ("LONG", "BUY"):
        return "buy"
    if direction in ("SHORT", "SELL"):
        return "sell"
    return ""


def _is_trade_direction_compatible_with_bucket_metric(trade: dict, bucket_metric: Any) -> bool:
    metric = _normalize_bucket_metric(bucket_metric)
    direction = _trade_direction_key(trade)
    if metric == "buy_net":
        return direction == "buy"
    if metric == "sell_net":
        return direction == "sell"
    return True


def _get_bucket_live_metric(bucket_name: str, mode: str = "live") -> Optional[str]:
    grid_live_file = ROOT_PATH / "grid_live.json"
    if not grid_live_file.exists():
        return None
    try:
        with open(grid_live_file, "r") as f:
            data = json.load(f) or {}
        rows = data.get(str(mode or "live").lower(), []) if isinstance(data, dict) else data
        if not isinstance(rows, list):
            return None
        source_tag = f"TB_{bucket_name}"
        for row in rows:
            if not isinstance(row, dict):
                continue
            source = str(row.get("source") or "").strip()
            group = str(row.get("group") or "").strip()
            if source == source_tag or group == bucket_name:
                return _normalize_bucket_metric(row.get("metric"))
    except Exception:
        return None
    return None

_GRID_AUTO_LAST_FILL = 0.0
_GRID_AUTO_COOLDOWN = 60.0
_WORKFLOW_LAST_RUN: Dict[str, float] = {}
_TOPX_STARTUP_AUDIT_RECORDED = False
_MARKET_UPDATE_LAST_RUN: Dict[str, float] = {}


def _load_live_trades_for_day(mode: str, date_str: str) -> List[dict]:
    rows: list[dict] = []
    for day_dir in _iter_day_dirs_for(mode, date_str):
        live_file = day_dir / "_live_trades.json"
        if not live_file.exists():
            continue
        try:
            with open(live_file, "r") as f:
                data = json.load(f) or {}
            live_rows = data.get("trades", [])
            if isinstance(live_rows, list):
                rows.extend(r for r in live_rows if isinstance(r, dict))
        except Exception:
            continue
    if rows:
        return rows
    return []


def _generate_market_update(mode: str, date_str: str) -> dict:
    now = datetime.now()
    now_ts = now.timestamp()
    trades = _load_live_trades_for_day(mode, date_str)
    targeted = {}
    targeted_file = _resolve_day_dir(mode, date_str) / "_targeted_strategies.json"
    if targeted_file.exists():
        try:
            with open(targeted_file, "r") as f:
                targeted = json.load(f) or {}
        except Exception:
            targeted = {}

    bias = str(targeted.get("bias") or "N/A").upper()
    total_buy = float(targeted.get("total_buy_net", 0.0) or 0.0)
    total_sell = float(targeted.get("total_sell_net", 0.0) or 0.0)
    status = str(targeted.get("status") or "UNKNOWN")
    market_condition = str(targeted.get("market_condition") or "UNKNOWN")

    closed = [t for t in trades if str(t.get("status", "")).upper() == "CLOSED"]
    open_trades = [t for t in trades if str(t.get("status", "")).upper() == "OPEN"]
    last_window_sec = 30 * 60
    prev_window_sec = 60 * 60

    def _trade_ts(t: dict) -> float:
        ts = t.get("exit_time") or t.get("entry_time")
        if not ts:
            return 0.0
        try:
            return datetime.fromisoformat(str(ts).replace("Z", "")).timestamp()
        except Exception:
            return 0.0

    recent = [t for t in closed if (now_ts - _trade_ts(t)) <= last_window_sec]
    previous = [t for t in closed if last_window_sec < (now_ts - _trade_ts(t)) <= prev_window_sec]

    def _side(t: dict) -> str:
        d = str(t.get("direction") or "LONG").upper()
        return "SELL" if "SHORT" in d else "BUY"

    def _side_net(rows: List[dict], side: str) -> float:
        return sum(float(r.get("net_return", 0.0) or 0.0) for r in rows if _side(r) == side)

    recent_buy = _side_net(recent, "BUY")
    recent_sell = _side_net(recent, "SELL")
    prev_buy = _side_net(previous, "BUY")
    prev_sell = _side_net(previous, "SELL")
    open_net = sum(float(t.get("net_return", 0.0) or 0.0) for t in open_trades)

    imbalance = total_buy - total_sell
    if bias in ("BUY", "SELL"):
        lead_side = bias
    else:
        lead_side = "BUY" if total_buy >= total_sell else "SELL"

    momentum_side = "BUY" if recent_buy >= recent_sell else "SELL"
    momentum_delta = abs(recent_buy - recent_sell)
    forecast = (
        f"Next period likely favors {lead_side} continuation."
        if momentum_side == lead_side
        else f"Next period risk of rotation toward {momentum_side}."
    )

    def _product_impacts(rows: List[dict]) -> Dict[str, float]:
        net_by_product: Dict[str, float] = {}
        for r in rows:
            product = str(r.get("product") or "").strip().upper()
            if not product:
                continue
            net_by_product[product] = net_by_product.get(product, 0.0) + float(r.get("net_return", 0.0) or 0.0)
        return net_by_product

    def _faction_impacts(rows: List[dict]) -> Dict[str, float]:
        net_by_faction: Dict[str, float] = {}
        for r in rows:
            model = str(r.get("model") or "").strip().lower()
            if not model:
                continue
            faction = model.split("_tp")[0].upper() if "_tp" in model else model.upper()
            net_by_faction[faction] = net_by_faction.get(faction, 0.0) + float(r.get("net_return", 0.0) or 0.0)
        return net_by_faction

    product_impacts = _product_impacts(recent if recent else closed)
    faction_impacts = _faction_impacts(recent if recent else closed)
    top_product = "N/A"
    top_product_net = 0.0
    weak_product = "N/A"
    weak_product_net = 0.0
    top_faction = "N/A"
    top_faction_net = 0.0
    if product_impacts:
        ranked = sorted(product_impacts.items(), key=lambda x: x[1], reverse=True)
        top_product, top_product_net = ranked[0]
        weak_product, weak_product_net = ranked[-1]
    if faction_impacts:
        faction_ranked = sorted(faction_impacts.items(), key=lambda x: x[1], reverse=True)
        top_faction, top_faction_net = faction_ranked[0]

    likely_winner = lead_side
    if momentum_side != lead_side and momentum_delta > 0:
        likely_winner = momentum_side

    winner_confidence = "HIGH" if momentum_side == lead_side else "MEDIUM"
    if abs(imbalance) < 1e-9 and momentum_delta < 1e-9:
        winner_confidence = "LOW"

    headline = f"{mode.upper()} Battle Pulse {now.strftime('%H:%M:%S')} | Bias {bias}"
    beats = [
        f"Bell: BUY {total_buy:,.2f} vs SELL {total_sell:,.2f}.",
        f"{lead_side} presses. Imbalance {imbalance:,.2f}.",
        f"30m score: BUY {recent_buy:,.2f} | SELL {recent_sell:,.2f}.",
        f"Faction lead: {top_faction} {top_faction_net:,.2f}.",
        f"Likely winner: {likely_winner} ({winner_confidence}).",
        f"Product impact: {top_product} {top_product_net:,.2f}; weak {weak_product} {weak_product_net:,.2f}.",
        f"Open heat: {len(open_trades)} trades, net {open_net:,.2f}.",
        forecast,
    ]
    narrative = " ".join(beats)

    return {
        "created_at": now.isoformat(),
        "mode": mode,
        "date": date_str,
        "bias": bias,
        "market_condition": market_condition,
        "status": status,
        "totals": {
            "buy_net": round(total_buy, 2),
            "sell_net": round(total_sell, 2),
            "imbalance": round(imbalance, 2)
        },
        "windows": {
            "last_30m": {"buy_net": round(recent_buy, 2), "sell_net": round(recent_sell, 2), "closed_count": len(recent)},
            "prev_30m": {"buy_net": round(prev_buy, 2), "sell_net": round(prev_sell, 2), "closed_count": len(previous)}
        },
        "open": {"count": len(open_trades), "net": round(open_net, 2)},
        "forecast": forecast,
        "likely_winner": likely_winner,
        "winner_confidence": winner_confidence,
        "narrative_style": "strategy-boxing-battle-pulse",
        "faction_impact": {
            "top_faction": top_faction,
            "top_faction_net": round(top_faction_net, 2)
        },
        "product_impact": {
            "top_product": top_product,
            "top_product_net": round(top_product_net, 2),
            "weakest_product": weak_product,
            "weakest_product_net": round(weak_product_net, 2)
        },
        "narrative_beats": beats,
        "headline": headline,
        "narrative": narrative
    }


def _maybe_generate_market_update(mode: str, date_str: str, cfg: dict) -> None:
    enabled = bool(cfg.get("market_update_enabled", False))
    if not enabled:
        return
    try:
        interval_min = int(cfg.get("market_update_interval_minutes", 5) or 5)
    except Exception:
        interval_min = 5
    interval_sec = max(60, interval_min * 60)
    now_ts = time.time()
    key = f"{mode}:{date_str}"
    last = _MARKET_UPDATE_LAST_RUN.get(key, 0.0)
    if now_ts - last < interval_sec:
        return

    payload = _generate_market_update(mode, date_str)
    day_dir = _ensure_day_dir(mode, date_str)
    latest_file = day_dir / "_market_update.json"
    history_file = day_dir / "_market_update_history.json"

    try:
        with open(latest_file, "w") as f:
            json.dump(payload, f, indent=2)
        history = []
        if history_file.exists():
            try:
                with open(history_file, "r") as f:
                    history = json.load(f) or []
                if not isinstance(history, list):
                    history = []
            except Exception:
                history = []
        history.append(payload)
        history = history[-500:]
        with open(history_file, "w") as f:
            json.dump(history, f, indent=2)
        _MARKET_UPDATE_LAST_RUN[key] = now_ts
    except Exception as e:
        print(f"[MARKET-UPDATE] Failed to write market update: {e}")

def _auto_fill_grid_if_empty() -> None:
    global _GRID_AUTO_LAST_FILL
    cfg = _load_config_safe()
    run_mode = str(cfg.get("run_mode", "live")).lower()
    # [V20260211_1415] Optional kill switch for automatic grid refill when empty.
    # Keep default behavior (enabled) if key is missing.
    grid_auto_refil = bool(cfg.get("grid_auto_refil", cfg.get("grid_auto_refill", True)))
    if not grid_auto_refil:
        return
    automated_sources = cfg.get("automated_trade_sources")
    if isinstance(automated_sources, list):
        sources = [str(s).strip() for s in automated_sources if isinstance(s, str) and str(s).strip()]
    else:
        sources = [str(cfg.get("automated_trade_source", "PSB")).strip()]
    eligible_sources = [s for s in sources if s in ("PSB", "PSB_Family")]
    if not eligible_sources:
        return

    now = time.time()
    if now - _GRID_AUTO_LAST_FILL < _GRID_AUTO_COOLDOWN:
        return

    if not _grid_is_empty(run_mode):
        return

    date_str = datetime.now().strftime("%Y-%m-%d")
    bias = _get_current_bias(run_mode, date_str)
    if not bias:
        return

    # Prefer family source when both enabled.
    chosen_source = "PSB_Family" if "PSB_Family" in eligible_sources else "PSB"
    if not _is_source_allowed(chosen_source):
        return

    if chosen_source == "PSB_Family":
        candidates = _select_psb_family_entries(run_mode, date_str, bias, max_items=10)
    else:
        candidates = _select_psb_siblings(run_mode, date_str, bias, max_items=10)

    if not candidates:
        return

    _archive_grid_live(run_mode)

    with GRID_LIVE_LOCK:
        full_data = {'live': [], 'sim': []}
        grid_live_file = ROOT_PATH / "grid_live.json"
        if grid_live_file.exists():
            try:
                with open(grid_live_file, "r") as f:
                    loaded = json.load(f)
                if isinstance(loaded, list):
                    full_data['live'] = loaded
                elif isinstance(loaded, dict):
                    full_data = loaded
            except Exception:
                pass

        entries = []
        for item in candidates:
            source_tag = (
                f"PSB_FAMILY_{item.get('family_id', 'NA')}_{item['model']}"
                if automated_source == "PSB_Family"
                else f"PSB_{item['model']}"
            )
            group_tag = (
                f"PSB_FAMILY_AUTO|GRID_EMPTY|{bias}|{item.get('family_id', 'NA')}"
                if automated_source == "PSB_Family"
                else f"PSB_AUTO|GRID_EMPTY|{bias}|{item['model']}"
            )
            entries.append({
                "model": item["model"],
                "product": item["product"],
                "metric": item["metric"],
                "group": group_tag,
                "source": source_tag,
                "activated_at": datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
            })

        full_data[run_mode] = entries
        with open(grid_live_file, "w") as f:
            json.dump(full_data, f, indent=4)

        _sync_grid_to_activations(entries, mode=run_mode)

    _GRID_AUTO_LAST_FILL = now
    print(f"[PSB-AUTO] Source={automated_source} Grid empty -> populated {len(entries)} entries for bias {bias}")

def _prune_from_live_trades(mode: str, date_str: str) -> int:
    trade_dir = _resolve_day_dir(mode, date_str)
    live_file = trade_dir / "_live_trades.json"
    if not live_file.exists():
        return 0
    try:
        with open(live_file, "r") as f:
            data = json.load(f)
    except Exception:
        return 0
    trades = data.get("trades", [])
    removed_total = 0
    seen = set()
    for t in trades:
        if t.get("is_live_trade") is not True:
            continue
        model = t.get("source_strategy") or t.get("script_name") or t.get("app_name")
        product = t.get("product")
        if not model or not product:
            continue
        key = (model, str(product).upper())
        if key in seen:
            continue
        seen.add(key)
        res = _prune_grid_live_siblings(model, product, mode, reason="PERIODIC_SWEEP")
        removed_total += int(res.get("removed", 0) or 0)
    return removed_total

def _grid_auto_worker() -> None:
    global _TOPX_STARTUP_AUDIT_RECORDED
    while True:
        try:
            cfg = _load_config_safe()
            run_mode = str(cfg.get("run_mode", "live")).lower()
            date_str = datetime.now().strftime("%Y-%m-%d")
            if not _TOPX_STARTUP_AUDIT_RECORDED:
                try:
                    workflows = _load_workflows().get("workflows", [])
                    topx_wf = next((w for w in workflows if isinstance(w, dict) and str(w.get("id")) == "top_x_multi_chart_workflow"), None)
                    if topx_wf:
                        topx_cfg = topx_wf.get("config", {}) if isinstance(topx_wf.get("config"), dict) else {}
                        for pt in _normalize_workflow_product_types(topx_cfg):
                            _log_topx_workflow_audit(run_mode, date_str, pt, {
                                "timestamp": datetime.now().isoformat(),
                                "workflow_id": "top_x_multi_chart_workflow",
                                "mode": run_mode,
                                "date": date_str,
                                "product_type": pt,
                                "event": "grid_auto_worker_startup",
                                "enabled": bool(topx_wf.get("enabled")),
                                "active_window": {
                                    "start_time": topx_wf.get("start_time"),
                                    "end_time": topx_wf.get("end_time"),
                                    "active_now": _workflow_active_now(topx_wf)
                                },
                                "status": "startup",
                                "message": "grid auto worker started"
                            })
                finally:
                    _TOPX_STARTUP_AUDIT_RECORDED = True
            _maybe_generate_market_update(run_mode, date_str, cfg)
            _auto_fill_grid_if_empty()
            _prune_from_live_trades(run_mode, date_str)
            _sync_open_trade_bias(run_mode, date_str)
            _force_close_wrong_bias_trades(run_mode, date_str)
            # [V20260214_1945] Ensure bucket leaders are promoted/synced
            _reconcile_active_buckets(mode=run_mode)
            _run_enabled_workflows(run_mode, date_str)
        except Exception as e:
            print(f"[GRID-AUTO] Error: {e}")
        time.sleep(15)


def _run_enabled_workflows(mode: str, date_str: str) -> None:
    data = _load_workflows()
    workflows = data.get("workflows", [])
    now_ts = time.time()

    for wf in workflows:
        if not isinstance(wf, dict):
            continue
        wf_id = str(wf.get("id") or "").strip()
        if not wf_id:
            continue
        if not _workflow_active_now(wf):
            continue

        cfg = wf.get("config", {}) if isinstance(wf.get("config"), dict) else {}
        run_interval = int(cfg.get("run_interval_sec", 900) or 900)

        last_ts = _WORKFLOW_LAST_RUN.get(wf_id, 0.0)
        if now_ts - last_ts < max(60, run_interval):
            continue

        if wf_id == "TB_workflow":
            max_buckets = int(cfg.get("max_buckets_per_day", 3) or 3)
            try:
                buckets_data = _load_trade_buckets(mode=mode, date_str=date_str)
                auto_count = len([
                    b for b in buckets_data.get("buckets", [])
                    if str(b.get("name", "")).startswith("AUTO_TB_")
                ])
            except Exception:
                auto_count = 0
            if auto_count >= max_buckets:
                continue
            result = _run_tb_workflow_once(mode, date_str, wf)
        elif wf_id == "profile_match_workflow":
            result = _run_profile_match_workflow_once(mode, date_str, wf)
        elif wf_id == "multi_chart_prune_negative_non_live":
            result = {"success": True, "message": "client-side workflow tick"}
        elif wf_id == "tb_prune_all_negative":
            result = _run_tb_prune_all_negative_once(mode, date_str, wf)
        elif wf_id == "top_x_multi_chart_workflow":
            result = _run_top_x_multi_chart_workflow(mode, date_str, wf)
        else:
            continue
        _WORKFLOW_LAST_RUN[wf_id] = now_ts
        if result.get("success"):
            print(f"[WORKFLOW] {wf_id} executed: {result}")
        else:
            print(f"[WORKFLOW] {wf_id} skipped/fail: {result.get('message')}")

def _sync_open_trade_bias(mode: str, date_str: str) -> int:
    """
    Force-sync market_bias_latest on open trade files to current targeted bias.
    This prevents stale bias values inside trade records.
    """
    bias = _get_current_bias(mode, date_str)
    if not bias:
        return 0
    changed = 0
    for day_dir in _iter_day_dirs_for(mode, date_str):
        for fp in day_dir.glob('*_op.json'):
            try:
                with open(fp, 'r') as f:
                    d = json.load(f) or {}
            except Exception:
                continue
            if str(d.get('status', '')).upper() != 'OPEN':
                continue
            if not bool(d.get('is_live_trade') or d.get('order_sent_net') or d.get('order_sent_alt')):
                continue
            if str(d.get('market_bias_latest') or '').upper() == bias:
                continue
            d['market_bias_latest'] = bias
            try:
                _atomic_write_json(fp, d, indent=2)
                changed += 1
            except Exception:
                continue
    return changed

def _force_close_wrong_bias_trades(mode: str, date_str: str) -> int:
    """
    Hard safety net: generate CLOSE tradeable orders for any open live trades
    that are misaligned with current market bias.
    """
    cfg = _load_config_safe()
    if not bool(cfg.get("enforce_market_bias_exit", False)):
        return 0

    bias = _get_current_bias(mode, date_str)
    if bias not in ("BUY", "SELL"):
        return 0
    order_dir = cfg.get("send_json_files_sim") if mode == "sim" else cfg.get("send_json_files")
    if not order_dir:
        order_dir = r"C:\Users\edebe\eds\trades_rt3_sim\orders" if mode == "sim" else r"C:\Users\edebe\eds\trades_rt3\orders"
    order_path = Path(order_dir)
    order_path.mkdir(parents=True, exist_ok=True)

    forced = 0
    now_iso = datetime.now().isoformat()
    now_tag = datetime.now().strftime("%Y%m%d_%H%M%S")
    for day_dir in _iter_day_dirs_for(mode, date_str):
        for fp in day_dir.glob('*_op.json'):
            try:
                with open(fp, 'r') as f:
                    d = json.load(f) or {}
            except Exception:
                continue
            if str(d.get('status', '')).upper() != 'OPEN':
                continue
            if not bool(d.get('is_live_trade') or d.get('order_sent_net') or d.get('order_sent_alt')):
                continue
            if d.get('bias_exit_close_sent_at'):
                continue

            direction = str(d.get('direction') or '').upper()
            aligned = ((bias == 'BUY' and direction in ('LONG', 'BUY')) or (bias == 'SELL' and direction in ('SHORT', 'SELL')))
            if aligned:
                continue

            action = 'SELL' if direction in ('LONG', 'BUY') else 'BUY'
            product = str(d.get('product') or '').upper()
            strategy = str(d.get('script_name') or d.get('source_strategy') or 'unknown')
            trade_id = d.get('trade_id') or d.get('id') or 0
            close_filename = f"{product}_{strategy}_{action}_{now_tag}_bias_exit_close_tradeable.json"
            close_file = order_path / close_filename
            order_payload = {
                "symbol": product,
                "secType": "CASH",
                "exchange": "IDEALPRO",
                "currency": "USD",
                "action": action,
                "orderType": "MKT",
                "quantity": _trade_quantity_for_product(product, cfg),
                "guidePrice": float(d.get("current_price") or d.get("entry_price") or 0.0),
                "comment": f"{strategy} NET CLOSE #{trade_id} (Bias Exit API)",
                "source": d.get("source_screen") or "grid_live",
                "source_group": d.get("source_group"),
                "guid": d.get("guid") or "unknown"
            }
            try:
                _atomic_write_json(close_file, order_payload, indent=2)
                d['market_bias_latest'] = bias
                d['bias_exit_close_sent_at'] = now_iso
                d['bias_exit_target_bias'] = bias
                d['bias_exit_close_file'] = close_filename
                _atomic_write_json(fp, d, indent=2)
                forced += 1
                print(f"[BIAS-FORCE-CLOSE] {fp.name} -> {close_filename} (bias={bias}, direction={direction})")
            except Exception as e:
                print(f"[BIAS-FORCE-CLOSE-ERROR] {fp.name}: {e}")
                continue
    return forced

def _start_grid_auto_worker() -> None:
    t = threading.Thread(target=_grid_auto_worker, daemon=True, name="grid-auto-worker")
    t.start()

def _any_trade_bucket_is_live(mode):
    """[V20260204_1410] Check if any bucket in the current run mode is Live."""
    try:
        data = _load_trade_buckets(mode=mode)
        buckets = data.get('buckets', [])
        return any(b.get('live') for b in buckets)
    except:
        return False

def _deactivate_all_trade_buckets(mode):
    """[V20260204_1410] For mutual exclusion: deactivate all buckets when Frequency is re-enabled."""
    try:
        data = _load_trade_buckets(mode=mode)
        buckets = data.get('buckets', [])
        changed = False
        for b in buckets:
            if b.get('live'):
                b['live'] = False
                changed = True
        if changed:
            _save_trade_buckets(data, mode=mode)
            print(f"[BUCKET] Deactivated all {mode} buckets due to Frequency overrule.")
    except Exception as e:
        print(f"[BUCKET-ERROR] Deactivation failed: {e}")

def _normalize_tb_metric(metric_raw: Any) -> str:
    raw = str(metric_raw or 'net').strip().lower()
    if raw in ('buy', 'buy_net', 'buy_net_return_sum'):
        return 'buy_net'
    if raw in ('sell', 'sell_net', 'sell_net_return_sum'):
        return 'sell_net'
    if raw in ('alt', 'alt_net', 'alt_net_return_sum'):
        return 'alt_net'
    return 'net'


def _tb_metric_value(point: dict, metric_raw: Any) -> float:
    metric_key = _normalize_tb_metric(metric_raw)
    try:
        return float(point.get(metric_key, point.get('net', 0.0)) or 0.0)
    except Exception:
        return 0.0


def _normalize_delta_type(delta_type_raw: Any) -> str:
    raw = str(delta_type_raw or "delta2").strip().lower()
    if raw == "delta1":
        return "delta1"
    if raw == "delta3":
        return "delta3"
    return "delta2"


def _parse_bucket_strat_key(strat_key: Any) -> Tuple[Optional[str], Optional[str]]:
    parts = str(strat_key or '').split(' | ')
    if len(parts) != 2:
        parts = str(strat_key or '').split('|')
    if len(parts) != 2:
        return None, None
    return parts[0].strip(), parts[1].strip()


def _metric_value_at_or_before(series: list, target_dt: Optional[datetime], metric_raw: Any) -> Optional[float]:
    if not series or not target_dt:
        return None
    val = None
    for point in series:
        ts = str(point.get('t', '') or '').replace('Z', '').replace(' ', 'T')
        if not ts:
            continue
        try:
            point_dt = datetime.fromisoformat(ts)
        except Exception:
            continue
        if point_dt <= target_dt:
            val = _tb_metric_value(point, metric_raw)
        else:
            break
    return val


def _capture_bucket_delta3_baseline(bucket: dict, mode: str, date_str: str, product_type: str | None = None, selected_at: Optional[datetime] = None) -> None:
    if not isinstance(bucket, dict):
        return
    effective_selected_at = selected_at or datetime.now()
    bucket['delta3_selected_at'] = effective_selected_at.isoformat()

    summary_file = _resolve_day_dir(mode, date_str, product_type=product_type) / "_summary_net.json"
    summary_net = {}
    if summary_file.exists():
        try:
            with open(summary_file, 'r') as f:
                summary_net = (json.load(f) or {}).get('strategies', {}) or {}
        except Exception as e:
            print(f"[TRADE-BUCKETS-WARN] delta3 snapshot load failed: {e}")

    for strat in bucket.get('strategies', []):
        if not isinstance(strat, dict):
            continue
        strategy_name, product = _parse_bucket_strat_key(strat.get('key'))
        metric_raw = strat.get('metric', 'net')
        normalized_baseline = 0.0
        if strategy_name and product:
            series = summary_net.get(strategy_name, {}).get(product, []) or []
            if series:
                day_baseline = _tb_metric_value(series[0], metric_raw)
                d3_val = _metric_value_at_or_before(series, effective_selected_at, metric_raw)
                if d3_val is None:
                    d3_val = _tb_metric_value(series[-1], metric_raw)
                normalized_baseline = round(float(d3_val) - float(day_baseline), 2)
        strat['delta3_net_at_selection'] = normalized_baseline
        strat['delta3_selected_at'] = bucket['delta3_selected_at']


def _calculate_bucket_strat_perf(strat_entry, baseline_time_str, summary_net, delta_type='delta2'):
    """[V20260320_1300] Respect delta_type for leadership calculation."""
    try:
        if isinstance(strat_entry, dict):
            strat_key = str(strat_entry.get('key') or '').strip()
            metric_raw = strat_entry.get('metric', 'net')
        else:
            strat_key = str(strat_entry or '').strip()
            metric_raw = 'net'
        if not strat_key:
            return -999999.0
        strat_name_only = strat_key.split(' | ')[0]
        product_only = strat_key.split(' | ')[1]
        series = summary_net.get(strat_name_only, {}).get(product_only, [])
        
        current_total = 0.0
        day_baseline = 0.0
        if series:
            current_total = _tb_metric_value(series[-1], metric_raw)
            day_baseline = _tb_metric_value(series[0], metric_raw)
        current_total_normalized = current_total - day_baseline
        
        # [V20260320_1300] Handle Delta 1 (Profit since Midnight)
        if delta_type == 'delta1':
            return round(current_total_normalized, 2)

        if delta_type == 'delta3':
            d3_baseline = 0.0
            if isinstance(strat_entry, dict):
                d3_baseline = float(strat_entry.get('delta3_net_at_selection', 0.0) or 0.0)
            return round(current_total_normalized - d3_baseline, 2)

        # Default: Delta 2 (Profit since creation/baseline)
        baseline = 0.0
        if baseline_time_str and series:
            try:
                clean_start = baseline_time_str.replace('Z', '').replace(' ', 'T')
                start_dt = datetime.fromisoformat(clean_start)
                for point in series:
                    p_time = point.get('t', '').replace('Z', '').replace(' ', 'T')
                    p_dt = datetime.fromisoformat(p_time)
                    if p_dt <= start_dt:
                        baseline = _tb_metric_value(point, metric_raw)
                    else: break
            except: pass
        return round(current_total - baseline, 2)
    except: return -999999.0

def _get_bucket_top2_stats(bucket: dict, summary_net: dict, start_time_str: str, delta_type='delta2'):
    """
    Return top-2 leaderboard stats for a bucket using net-diff since the        
    canonical chart baseline/start_from time.
    """
    scored = []
    locked_metric = str(bucket.get('locked_directional_metric') or '').strip().lower()
    for s in bucket.get('strategies', []):
        k = s.get('key')
        if not k:
            continue
        row_metric = str(s.get('metric') or '').strip().lower()
        if locked_metric in ('buy_net', 'sell_net') and row_metric and row_metric != locked_metric:
            continue
        # [V20260320_1300] Propagate delta_type to perf calc
        diff = _calculate_bucket_strat_perf(s, start_time_str, summary_net, delta_type=delta_type)     
        scored.append((k, diff, s))
    if not scored:
        return None, -999999.0, -999999.0, -999999.0, 0, None
    scored.sort(key=lambda x: x[1], reverse=True)
    top_key, top_diff, top_entry = scored[0]
    second_diff = scored[1][1] if len(scored) > 1 else None
    gap = (top_diff - second_diff) if second_diff is not None else None
    return top_key, top_diff, second_diff, gap, len(scored), top_entry

def _get_bucket_bottom_stats(bucket: dict, summary_net: dict, start_time_str: str, delta_type='delta2'):
    """Return the single most negative strategy in the bucket."""
    scored = []
    for s in bucket.get('strategies', []):
        k = s.get('key')
        if not k:
            continue
        diff = _calculate_bucket_strat_perf(s, start_time_str, summary_net, delta_type=delta_type)
        scored.append((k, diff, s))
    if not scored:
        return None, 999999.0, 0, None
    scored.sort(key=lambda x: x[1])
    bottom_key, bottom_diff, bottom_entry = scored[0]
    return bottom_key, bottom_diff, len(scored), bottom_entry

def _bucket_passes_threshold(top_diff: float, second_diff: float, gap_diff: float, min_diff: float) -> bool:
    """
    Threshold rule:
    - 2+ strategies: require gap(top-second) >= min_diff
    - 1 strategy only: require top_diff >= min_diff
    """
    if second_diff is None:
        return top_diff >= min_diff
    return (gap_diff is not None) and (gap_diff >= min_diff)


def _resolve_tb_metric(bucket: dict, leader_entry: Optional[dict] = None) -> str:
    """
    Resolve Trade Bucket metric for grid promotion.
    Rules:
    - If TB explicitly selected buy_net/sell_net, preserve it.
    - If TB selected total_net/net, preserve as net (both sides).
    - Fallback to net when unknown.
    """
    if not isinstance(bucket, dict):
        return "net"

    locked_metric = str(bucket.get("locked_directional_metric") or "").strip().lower()
    if locked_metric in ("buy_net", "sell_net"):
        return locked_metric

    def _norm_metric(val: Any) -> Optional[str]:
        raw = str(val or "").strip().lower()
        if raw in ("buy_net", "sell_net", "net", "total_net"):
            return "net" if raw == "total_net" else raw
        return None

    if isinstance(leader_entry, dict):
        m = _norm_metric(leader_entry.get("metric"))
        if m:
            return m

    for key in ("metric", "selected_metric", "selection_metric", "leader_metric"):
        m = _norm_metric(bucket.get(key))
        if m:
            return m

    return "net"

def _resolve_tb_alt_metric(bucket: dict, loser_entry: Optional[dict] = None) -> str:
    return "alt"

def _infer_split_net_bucket_lock(strategies: list, minimum_difference: float) -> Optional[str]:
    if not isinstance(strategies, list):
        return None

    buy_total = 0.0
    sell_total = 0.0
    has_buy = False
    has_sell = False

    for strat in strategies:
        if not isinstance(strat, dict):
            continue
        metric = str(strat.get('metric') or '').strip().lower()
        try:
            basis = float(
                strat.get('current_total_net', strat.get('net_at_creation', 0.0)) or 0.0
            )
        except Exception:
            basis = 0.0
        if metric == 'buy_net':
            buy_total += basis
            has_buy = True
        elif metric == 'sell_net':
            sell_total += basis
            has_sell = True

    if not (has_buy and has_sell):
        return None

    min_diff = float(minimum_difference or 0.0)
    if buy_total >= (sell_total + min_diff):
        return 'buy_net'
    if sell_total >= (buy_total + min_diff):
        return 'sell_net'
    return None

def _ensure_bucket_locked_directional_metric(bucket: dict) -> Optional[str]:
    if not isinstance(bucket, dict):
        return None
    existing = str(bucket.get('locked_directional_metric') or '').strip().lower()
    if existing in ('buy_net', 'sell_net'):
        return existing
    inferred = _infer_split_net_bucket_lock(
        bucket.get('strategies', []),
        float(bucket.get('minimum_difference', 5.0) or 5.0),
    )
    if inferred:
        bucket['locked_directional_metric'] = inferred
    return inferred

def _sync_bucket_to_grid_live(bucket: dict, mode: str, date_str: str, product_type: str | None = None):
    """[V20260204_1410] Replaces _sync_bucket_to_activations. Updates grid_live.json instead."""
    try:
        bucket_name = bucket.get('name')
        bucket_live = bucket.get('live', False)
        _ensure_bucket_locked_directional_metric(bucket)
        resolved_product_type = (
            product_type
            or bucket.get('product_type')
            or default_product_type(_load_layout_runtime_config())
        )
        
        # [V20260205_2100] Check if Trade Bucket source is allowed for automated sync
        if bucket_live and not _is_source_allowed('Trade Bucket'):
            print(f"[BUCKET] Sync skipped for '{bucket_name}': Trade Bucket is not the current automated source.")
            return

        # [V20260216_0001] Enforce same-day bucket rule:
        # only buckets from today's date can be promoted to grid_live.
        today_str = datetime.now().strftime('%Y-%m-%d')
        if bucket_live and str(date_str) != today_str:
            print(f"[BUCKET] Skip promotion for '{bucket_name}': bucket date={date_str} != today={today_str}.")
            bucket_live = False

        # 1. Archive current state (already done in update_trade_bucket but good to be safe)
        _archive_grid_live(mode, force=True)
        grid_live_file = ROOT_PATH / "grid_live.json"
        
        with GRID_LIVE_LOCK:
            full_data = {'live': [], 'sim': []}
            if grid_live_file.exists():
                try:
                    with open(grid_live_file, "r") as f:
                        full_data = json.load(f)
                    if isinstance(full_data, list): # Migrate legacy
                        full_data = {'live': full_data, 'sim': []}
                except: pass
            
            # 2. Remove previous items from THIS bucket AND ALL Frequency items (Mutual Exclusion)
            # [V20260204_2130] Prefix with TB_
            source_tag = f"TB_{bucket_name}"
            alt_source_tag = f"TBALT_{bucket_name}"
            target_list = full_data.get(mode, [])
            
            # Clean list: remove this bucket's items (handle both raw and TB_ prefixed for transition)
            new_target_list = [
                m for m in target_list
                if m.get('source') not in (source_tag, alt_source_tag, bucket_name)
            ]
            if bucket_live:
                 # If activating bucket, clear ALL frequency/rank_alert items
                 new_target_list = [m for m in new_target_list 
                                   if not str(m.get('source', '')).startswith(('rank_alert', 'frequency'))]
            
            # 3. If bucket live, find and add Leader
            if bucket_live:
                summary_file = _resolve_day_dir(mode, date_str, product_type=resolved_product_type) / "_summary_net.json"
                summary_net = {}
                if summary_file.exists():
                    try:
                        with open(summary_file, 'r') as f:
                            summary_net = json.load(f).get('strategies', {})
                    except: pass
                
                min_diff = float(bucket.get('minimum_difference', 5.0))
                start_time_str = bucket.get('chart_start_time') or bucket.get('start_time')
                # [V20260320_1300] Pass bucket-level delta_type to leader stats
                b_delta_type = _normalize_delta_type(bucket.get('delta_type'))
                top_strat_key, max_diff, second_diff, gap_diff, n_scored, top_entry = _get_bucket_top2_stats(
                    bucket, summary_net, start_time_str, delta_type=b_delta_type
                )

                if top_strat_key and _bucket_passes_threshold(max_diff, second_diff, gap_diff, min_diff):
                    parsed = _parse_strategy_key(top_strat_key)
                    if parsed:
                        tb_metric = _resolve_tb_metric(bucket, top_entry)
                        print(f"[BUCKET] Promoting Leader from '{bucket_name}': {top_strat_key} (Top={max_diff}, Second={second_diff}, Gap={gap_diff})")
                        now_local = datetime.now().isoformat().split('.')[0]
                        new_entry = {
                            "model": top_strat_key.split(' | ')[0],
                            "product": parsed['product'],
                            "metric": tb_metric,
                            "group": bucket_name,
                            "source": source_tag,
                            "activated_at": now_local
                        }
                        new_target_list.append(new_entry)
                else:
                    print(
                        f"[BUCKET] No candidate meets threshold in '{bucket_name}' "
                        f"(Top={max_diff}, Second={second_diff}, Gap={gap_diff}, MinGap={min_diff}, N={n_scored})"
                    )

                if bool(bucket.get('trade_alt_net')):
                    bottom_strat_key, bottom_diff, _, bottom_entry = _get_bucket_bottom_stats(
                        bucket, summary_net, start_time_str, delta_type=b_delta_type
                    )
                    if bottom_strat_key and float(bottom_diff) < 0:
                        parsed_bottom = _parse_strategy_key(bottom_strat_key)
                        if parsed_bottom:
                            now_local = datetime.now().isoformat().split('.')[0]
                            new_target_list.append({
                                "model": bottom_strat_key.split(' | ')[0],
                                "product": parsed_bottom['product'],
                                "metric": _resolve_tb_alt_metric(bucket, bottom_entry),
                                "group": bucket_name,
                                "source": alt_source_tag,
                                "activated_at": now_local,
                                "trade_alt_net": True,
                            })
                            print(
                                f"[BUCKET] Promoting ALT loser from '{bucket_name}': "
                                f"{bottom_strat_key} (Bottom={bottom_diff})"
                            )
                    else:
                        print(
                            f"[BUCKET] No valid ALT loser in '{bucket_name}' "
                            f"(Bottom={bottom_diff})."
                        )
            
            # 4. Save and Sync
            full_data[mode] = new_target_list
            with open(grid_live_file, "w") as f:
                json.dump(full_data, f, indent=4)
            
            _sync_grid_to_activations(new_target_list, mode=mode)
            
    except Exception as e:
        print(f"[BUCKET-SYNC-ERROR] {e}")

def _reconcile_active_buckets(mode: str = 'live'):
    """
    [V20260204_2120] Background/Periodic reconciler for Trade Buckets.
    Ensures that if buckets are live:
    1. Stale frequency/rank_alert items are purged from grid_live.json (Mutual Exclusion).
    2. Bucket leaders meeting threshold are automatically promoted to grid_live.json if missing.
    """
    try:
        def _bucket_is_same_day(bucket: dict, day_str: str) -> bool:
            # Primary: use bucket start_time date when parseable
            start_time = str(bucket.get('start_time') or '').strip()
            if start_time:
                try:
                    start_dt = datetime.fromisoformat(start_time.replace('Z', ''))
                    return start_dt.strftime('%Y-%m-%d') == day_str
                except Exception:
                    pass
            # Fallback: if unparseable, trust file scope date only.
            return True

        date_str = datetime.now().strftime('%Y-%m-%d')
        # [V20260205_2100] Check if Trade Bucket source is allowed for automated sync
        if not _is_source_allowed('Trade Bucket'):
            return

        cfg = _load_layout_runtime_config()
        product_types = configured_product_types(cfg)

        grid_live_file = ROOT_PATH / "grid_live.json"
        with GRID_LIVE_LOCK:
            full_data = {'live': [], 'sim': []}
            if grid_live_file.exists():
                try:
                    with open(grid_live_file, "r") as f:
                        full_data = json.load(f)
                    if isinstance(full_data, list):
                        full_data = {'live': full_data, 'sim': []}
                except: pass
            
            target_list = full_data.get(mode, [])
            changed = False
            
            all_live_buckets: List[dict] = []
            for product_type in product_types:
                buckets_data = _load_trade_buckets(mode=mode, date_str=date_str, product_type=product_type)
                buckets = buckets_data.get('buckets', [])
                auto_deactivated, cap = _enforce_max_live_tb_inplace(buckets)
                if auto_deactivated:
                    _save_trade_buckets(buckets_data, mode=mode, date_str=date_str, product_type=product_type)
                    for b in auto_deactivated:
                        _sync_bucket_to_grid_live(
                            {'name': b.get('name'), 'live': False, 'product_type': product_type},
                            mode,
                            date_str,
                            product_type=product_type,
                        )
                    print(
                        f"[RECONCILE] max_live_tb={cap} enforced for {product_type}; "
                        f"auto-deactivated {len(auto_deactivated)} bucket(s)."
                    )

                live_buckets_all = [b for b in buckets if b.get('live')]
                live_buckets = [b for b in live_buckets_all if _bucket_is_same_day(b, date_str)]
                for bucket in live_buckets:
                    bucket.setdefault('product_type', product_type)
                all_live_buckets.extend(live_buckets)

            if not all_live_buckets:
                return

            # 1. Mutual Exclusion: Clear ALL frequency/rank_alert AND manual UI items if buckets are live
            # [V20260204_2155] Added 'ui' to purge list to ensure bucket priority.
            original_len = len(target_list)
            target_list = [m for m in target_list 
                          if not str(m.get('source', '')).startswith(('rank_alert', 'frequency', 'ui'))]
            if len(target_list) != original_len:
                print(f"[RECONCILE] Purged {original_len - len(target_list)} stale frequency/UI items (Buckets active)")
                changed = True

            allowed_tb_sources = set()
            for b in all_live_buckets:
                bn = b.get('name')
                if bn:
                    allowed_tb_sources.add(f"TB_{bn}")
                    allowed_tb_sources.add(f"TBALT_{bn}")
                    allowed_tb_sources.add(str(bn))
            before_tb = len(target_list)
            target_list = [
                m for m in target_list
                if (not str(m.get('source', '')).startswith('TB_')) or (str(m.get('source', '')) in allowed_tb_sources)
            ]
            if len(target_list) != before_tb:
                print(f"[RECONCILE] Purged {before_tb - len(target_list)} stale TB entries (date mismatch/non-live).")
                changed = True

            live_buckets_by_type: Dict[str, List[dict]] = {}
            for bucket in all_live_buckets:
                live_buckets_by_type.setdefault(
                    str(bucket.get('product_type') or default_product_type(cfg)),
                    [],
                ).append(bucket)

            for product_type, live_buckets in live_buckets_by_type.items():
                summary_file = _resolve_day_dir(mode, date_str, product_type=product_type) / "_summary_net.json"
                summary_net = {}
                if summary_file.exists():
                    try:
                        with open(summary_file, 'r') as f:
                            summary_net = json.load(f).get('strategies', {})
                    except:
                        pass

                for bucket in live_buckets:
                    bucket_name = bucket.get('name')
                    source_tag = f"TB_{bucket_name}"
                    alt_source_tag = f"TBALT_{bucket_name}"
                    min_diff = float(bucket.get('minimum_difference', 5.0))
                    start_time_str = bucket.get('chart_start_time') or bucket.get('start_time')
                    b_delta_type = _normalize_delta_type(bucket.get('delta_type'))
                    top_strat_key, max_diff, second_diff, gap_diff, n_scored, top_entry = _get_bucket_top2_stats(
                        bucket, summary_net, start_time_str, delta_type=b_delta_type
                    )

                    existing_for_bucket = [m for m in target_list if m.get('source') in (source_tag, bucket_name)]
                    existing_alt_for_bucket = [m for m in target_list if m.get('source') == alt_source_tag]

                    if top_strat_key and _bucket_passes_threshold(max_diff, second_diff, gap_diff, min_diff):
                        parsed = _parse_strategy_key(top_strat_key)
                        if parsed:
                            tb_metric = _resolve_tb_metric(bucket, top_entry)
                            already_promoted = any(
                                m.get('model') == parsed['strategy'] and
                                m.get('product') == parsed['product']
                                for m in existing_for_bucket
                            )

                            if not already_promoted:
                                target_list = [m for m in target_list if m.get('source') not in (source_tag, bucket_name)]
                                now_local = datetime.now().isoformat().split('.')[0]
                                new_entry = {
                                    "model": top_strat_key.split(' | ')[0],
                                    "product": parsed['product'],
                                    "metric": tb_metric,
                                    "group": bucket_name,
                                    "source": source_tag,
                                    "activated_at": now_local
                                }
                                target_list.append(new_entry)
                                print(
                                    f"[RECONCILE] Promoting new leader from '{bucket_name}' ({product_type}): "
                                    f"{top_strat_key} (Top={max_diff}, Second={second_diff}, Gap={gap_diff})"
                                )
                                changed = True
                    else:
                        if existing_for_bucket:
                            target_list = [m for m in target_list if m.get('source') not in (source_tag, bucket_name)]
                            print(
                                f"[RECONCILE] Removing member for '{bucket_name}' ({product_type}) - no strategy meets threshold "
                                f"(Top={max_diff}, Second={second_diff}, Gap={gap_diff}, MinGap={min_diff}, N={n_scored})."
                            )
                            changed = True

                    if bool(bucket.get('trade_alt_net')):
                        bottom_strat_key, bottom_diff, _, bottom_entry = _get_bucket_bottom_stats(
                            bucket, summary_net, start_time_str, delta_type=b_delta_type
                        )
                        if bottom_strat_key and float(bottom_diff) < 0:
                            parsed_bottom = _parse_strategy_key(bottom_strat_key)
                            if parsed_bottom:
                                already_promoted_alt = any(
                                    m.get('model') == parsed_bottom['strategy'] and
                                    m.get('product') == parsed_bottom['product'] and
                                    str(m.get('metric') or '').lower() == 'alt'
                                    for m in existing_alt_for_bucket
                                )
                                if not already_promoted_alt:
                                    target_list = [m for m in target_list if m.get('source') != alt_source_tag]
                                    now_local = datetime.now().isoformat().split('.')[0]
                                    target_list.append({
                                        "model": bottom_strat_key.split(' | ')[0],
                                        "product": parsed_bottom['product'],
                                        "metric": _resolve_tb_alt_metric(bucket, bottom_entry),
                                        "group": bucket_name,
                                        "source": alt_source_tag,
                                        "activated_at": now_local,
                                        "trade_alt_net": True,
                                    })
                                    print(
                                        f"[RECONCILE] Promoting ALT loser from '{bucket_name}' ({product_type}): "
                                        f"{bottom_strat_key} (Bottom={bottom_diff})"
                                    )
                                    changed = True
                        elif existing_alt_for_bucket:
                            target_list = [m for m in target_list if m.get('source') != alt_source_tag]
                            print(
                                f"[RECONCILE] Removing ALT loser for '{bucket_name}' ({product_type}) - "
                                f"no negative strategy available (Bottom={bottom_diff})."
                            )
                            changed = True
                    elif existing_alt_for_bucket:
                        target_list = [m for m in target_list if m.get('source') != alt_source_tag]
                        changed = True

            # 3. Save if changed
            if changed:
                full_data[mode] = target_list
                with open(grid_live_file, "w") as f:
                    json.dump(full_data, f, indent=4)
                _sync_grid_to_activations(target_list, mode=mode)
                
    except Exception as e:
        print(f"[RECONCILE-ERROR] Failed to reconcile buckets: {e}")


def _bucket_sort_ts(bucket: dict) -> float:
    """Best-effort timestamp for deterministic live-bucket cap ordering."""
    for key in ('start_time', 'chart_start_time'):
        raw = str(bucket.get(key) or '').strip()
        if not raw:
            continue
        try:
            return datetime.fromisoformat(raw.replace('Z', '')).timestamp()
        except Exception:
            continue
    return 0.0


def _get_max_live_tb() -> int:
    """Read max live trade-bucket cap from config with safe default."""
    cfg = _load_config_safe()
    try:
        value = int(cfg.get('max_live_tb', 5) or 5)
    except Exception:
        value = 5
    return max(1, value)


def _enforce_max_live_tb_inplace(buckets: List[dict], preferred_live_name: Optional[str] = None) -> Tuple[List[dict], int]:
    """
    Enforce max live TB cap in-place on bucket list.
    Keeps preferred bucket live (if requested), then keeps newest by start_time.
    Returns (auto_deactivated_buckets, max_live_tb).
    """
    cap = _get_max_live_tb()
    live = [b for b in buckets if bool(b.get('live'))]
    if len(live) <= cap:
        return [], cap

    live_sorted = sorted(
        live,
        key=lambda b: (_bucket_sort_ts(b), str(b.get('name') or '')),
        reverse=True
    )
    keep_names: List[str] = []
    if preferred_live_name:
        pref = str(preferred_live_name)
        if any(str(b.get('name')) == pref for b in live_sorted):
            keep_names.append(pref)
    for b in live_sorted:
        name = str(b.get('name') or '')
        if not name or name in keep_names:
            continue
        if len(keep_names) >= cap:
            break
        keep_names.append(name)

    keep_set = set(keep_names)
    auto_deactivated: List[dict] = []
    for b in buckets:
        if bool(b.get('live')) and str(b.get('name') or '') not in keep_set:
            b['live'] = False
            auto_deactivated.append(b)
    return auto_deactivated, cap


@app.route("/sidebar-loader.js")
def serve_sidebar_loader_js():
    return send_from_directory(ROOT_PATH, "sidebar-loader.js")


# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# Trade Buckets API (File-Based) [V20260122_FS]
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

def _get_trade_buckets_path(mode: str, date_str: str, product_type: str | None = None) -> Path:
    """Get path to trade buckets file."""
    return _resolve_day_dir(mode, date_str, product_type=product_type) / "_trade_buckets.json"


def _load_trade_buckets(mode: str = 'live', date_str: str = None, product_type: str | None = None) -> dict:
    """Load trade buckets from JSON file."""
    if not date_str:
        date_str = datetime.now().strftime('%Y-%m-%d')

    bucket_file = _get_trade_buckets_path(mode, date_str, product_type=product_type)

    if bucket_file.exists():
        try:
            with open(bucket_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading trade buckets: {e}")

    return {"buckets": []}


def _log_topx_workflow_audit(mode: str, date_str: str, product_type: str | None, entry: dict) -> None:
    day_dirs = _iter_day_dirs_for(mode, date_str, product_type)
    if not day_dirs:
        try:
            day_dirs = [_ensure_day_dir(mode, date_str, product_type=product_type)]
        except Exception:
            return
    target_file = day_dirs[0] / "_topx_workflow_audit.json"
    audit_data = {"version": TOPX_AUDIT_VERSION, "date": date_str, "product_type": product_type, "runs": []}
    if target_file.exists():
        try:
            with open(target_file, "r", encoding="utf-8") as f:
                loaded = json.load(f) or {}
            if isinstance(loaded, dict):
                audit_data.update(loaded)
                if not isinstance(audit_data.get("runs"), list):
                    audit_data["runs"] = []
        except Exception:
            corrupt_name = target_file.with_name(
                f"_topx_workflow_audit_corrupt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            )
            try:
                shutil.move(str(target_file), str(corrupt_name))
            except Exception:
                pass

    audit_data["version"] = TOPX_AUDIT_VERSION
    audit_data["date"] = date_str
    audit_data["product_type"] = product_type
    audit_data["updated_at"] = datetime.now().isoformat()
    audit_data.setdefault("runs", []).append(entry)
    audit_data["runs"] = audit_data["runs"][-1000:]
    try:
        _atomic_write_json(target_file, audit_data, indent=2)
    except Exception as e:
        print(f"[ERROR] Failed to update Top X workflow audit: {e}")


def _log_top10_history_snapshot(mode: str, date_str: str, product_type: str | None, top_x_list: List[dict]):
    """
    [V20260323_1645] Append Top 10 snapshot to history every 5 minutes.
    Part of task: historical_top10_logging
    """
    if not top_x_list:
        return

    day_dirs = _iter_day_dirs_for(mode, date_str, product_type)
    if not day_dirs:
        return
    
    target_file = day_dirs[0] / "_top10_history.json"
    now_dt = datetime.now()
    
    # Load existing history
    history_data = {"version": "V20260323_1645", "history": []}
    if target_file.exists():
        try:
            with open(target_file, 'r', encoding='utf-8') as f:
                history_data = json.load(f)
        except Exception:
            corrupt_name = target_file.with_name(
                f"_top10_history_corrupt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            )
            try:
                shutil.move(str(target_file), str(corrupt_name))
            except Exception:
                pass
            history_data = {"version": "V20260323_1645", "history": []}

    # Ensure 5-minute interval
    if history_data.get("history"):
        last_entry = history_data["history"][-1]
        try:
            last_ts = datetime.fromisoformat(last_entry["timestamp"])
            if (now_dt - last_ts).total_seconds() < 290: # Slightly under 300s to allow for slight jitter
                return
        except: pass

    # Prepare Top 10 (ensure exactly 10 and only key fields)
    top10 = []
    for e in top_x_list[:10]:
        top10.append({
            "strategy": e.get("strategy"),
            "product": e.get("product"),
            "net": float(e.get("total_net", 0.0) or 0.0),
            "pick_now": bool(e.get("pick_now", False))
        })

    history_data["history"].append({
        "timestamp": now_dt.isoformat(),
        "top10": top10
    })
    history_data["updated_at"] = now_dt.isoformat()
    history_data["date"] = date_str

    try:
        _atomic_write_json(target_file, history_data, indent=2)
    except Exception as e:
        print(f"[ERROR] Failed to update Top 10 history: {e}")


@app.route('/api/workflows/topx_audit', methods=['GET'])
def get_topx_workflow_audit():
    """Return persisted Top X workflow audit runs for a mode/date/product_type."""
    try:
        mode = request.args.get('mode', 'live').lower()
        date_str = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))
        product_type = request.args.get('product_type')
        limit = int(request.args.get('limit', 200) or 200)
        limit = max(1, min(limit, 1000))

        day_dirs = _iter_day_dirs_for(mode, date_str, product_type)
        if not day_dirs:
            return jsonify({'success': False, 'message': 'No data directory found'}), 404
        target_file = day_dirs[0] / "_topx_workflow_audit.json"
        if not target_file.exists():
            return jsonify({'success': False, 'message': '_topx_workflow_audit.json not found'}), 404
        with open(target_file, 'r', encoding='utf-8') as f:
            data = json.load(f) or {}
        runs = data.get("runs", [])
        if isinstance(runs, list):
            data["runs"] = runs[-limit:]
        return jsonify({'success': True, 'audit': data})
    except Exception as e:
        print(f"[ERROR] get_topx_workflow_audit: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/top10_history', methods=['GET'])
def get_top10_history():
    """Returns the historical Top 10 snapshots for evaluation."""
    try:
        mode = request.args.get('mode', 'live').lower()
        date_str = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))
        product_type = request.args.get('product_type')
        
        day_dirs = _iter_day_dirs_for(mode, date_str, product_type)
        if not day_dirs:
            return jsonify({'success': False, 'message': 'No data directory found'}), 404
            
        target_file = day_dirs[0] / "_top10_history.json"
        if not target_file.exists():
            return jsonify({'success': False, 'message': '_top10_history.json not found'}), 404
            
        with open(target_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        return jsonify({
            'success': True,
            'history': data.get('history', [])
        })
    except Exception as e:
        print(f"[ERROR] get_top10_history: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500


def _save_trade_buckets(data: dict, mode: str = 'live', date_str: str = None, product_type: str | None = None):
    """Save trade buckets to JSON file."""
    if not date_str:
        date_str = datetime.now().strftime('%Y-%m-%d')

    bucket_file = _get_trade_buckets_path(mode, date_str, product_type=product_type)

    # Ensure directory exists
    bucket_file.parent.mkdir(parents=True, exist_ok=True)

    try:
        with open(bucket_file, 'w') as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"Error saving trade buckets: {e}")


@app.route('/api/trade_buckets', methods=['GET'])
def get_trade_buckets():
    """
    Get all trade buckets with stats.
    [V20260214_2000] Enhanced logging and robust parsing.
    """
    try:
        raw_mode = request.args.get('mode', 'live')
        mode = raw_mode.lower()
        date_str = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))
        product_type = request.args.get('product_type')

        # Log request parameters for debugging
        print(f"[TRADE-BUCKETS] Request: mode='{mode}' (raw='{raw_mode}'), date='{date_str}', product_type='{product_type}'")

        data = _load_trade_buckets(mode=mode, date_str=date_str, product_type=product_type)
        buckets = data.get('buckets', [])

        
        if not buckets:
            print(f"[TRADE-BUCKETS] No buckets found for {mode}/{date_str}")

        def _load_summary_strategies_for_date(_mode: str, _date: str, _product_type: str | None) -> dict:
            fpath = _resolve_day_dir(_mode, _date, product_type=_product_type) / "_summary_net.json"
            if not fpath.exists():
                return {}
            try:
                with open(fpath, 'r') as f:
                    return (json.load(f) or {}).get('strategies', {}) or {}
            except Exception as e:
                print(f"[TRADE-BUCKETS-ERROR] Failed to load summary_net from {fpath}: {e}")
                return {}

        def _latest_mode_date(_mode: str, _product_type: str | None) -> str:
            try:
                base = _resolve_day_dir(_mode, date_str, product_type=_product_type).parent
                if not base.exists():
                    return date_str
                dates = []
                for p in base.iterdir():
                    if p.is_dir():
                        n = p.name
                        if len(n) == 10 and n[4] == '-' and n[7] == '-':
                            dates.append(n)
                if not dates:
                    return date_str
                return sorted(dates)[-1]
            except Exception:
                return date_str

        # Baseline compatibility uses requested date; current net uses latest available date.
        summary_net_baseline = _load_summary_strategies_for_date(mode, date_str, product_type)
        latest_date = _latest_mode_date(mode, product_type)
        summary_net_current = _load_summary_strategies_for_date(mode, latest_date, product_type)
        if not summary_net_current:
            summary_net_current = summary_net_baseline

        def _normalize_bucket_metric(metric_raw: str) -> str:
            raw = str(metric_raw or 'net').strip().lower()
            if raw in ('buy', 'buy_net', 'buy_net_return_sum'):
                return 'buy_net'
            if raw in ('sell', 'sell_net', 'sell_net_return_sum'):
                return 'sell_net'
            if raw in ('alt', 'alt_net', 'alt_net_return_sum'):
                return 'alt_net'
            return 'net'

        def _metric_value(point: dict, metric_raw: str) -> float:
            key = _normalize_bucket_metric(metric_raw)
            try:
                return float(point.get(key, point.get('net', 0.0)) or 0.0)
            except Exception:
                return 0.0

        # Update bucket stats from summary data
        for bucket in buckets:
            if 'open_trades' not in bucket:
                bucket['open_trades'] = False
            if 'open_trade_count' not in bucket:
                bucket['open_trade_count'] = 0
            if 'live' not in bucket:
                bucket['live'] = False
            if 'trade_alt_net' not in bucket:
                bucket['trade_alt_net'] = False
            bucket_delta_type = _normalize_delta_type(bucket.get('delta_type'))

            start_dt = None
            chart_start_dt = None
            start_time_str = bucket.get('start_time')
            chart_start_time_str = bucket.get('chart_start_time')
            
            if start_time_str:
                try:
                    start_dt = datetime.fromisoformat(start_time_str.replace('Z', ''))
                except:
                    pass
            if chart_start_time_str:
                try:
                    chart_start_dt = datetime.fromisoformat(chart_start_time_str.replace('Z', ''))
                except:
                    pass

            for strat in bucket.get('strategies', []):
                strat_key = strat.get('key', '')
                metric_raw = str(strat.get('metric', 'net') or 'net')
                
                # Robust parsing: try ' | ' first, then '|'
                parts = strat_key.split(' | ')
                if len(parts) != 2:
                    parts = strat_key.split('|')
                
                if len(parts) == 2:
                    strategy_name = parts[0].strip()
                    product = parts[1].strip()
                    
                    # Current net should reflect latest available summary data for this mode.
                    series = summary_net_current.get(strategy_name, {}).get(product, [])
                    if not series and summary_net_current:
                        # Log missing strategy/product only if summary exists but key is missing
                        # print(f"[TRADE-BUCKETS-DEBUG] Missing series for {strategy_name} | {product}")
                        pass

                    current_total = 0.0
                    if series:
                        current_total = _metric_value(series[-1], metric_raw)

                    # [V20260319_2115] Determine day-start baseline to normalize display to '0.00' start
                    day_baseline = 0.0
                    baseline_series = summary_net_baseline.get(strategy_name, {}).get(product, [])
                    if baseline_series:
                        day_baseline = _metric_value(baseline_series[0], metric_raw)

                    # Prefer immutable baseline captured at bucket creation.
                    baseline_val = strat.get('net_at_creation', None)
                    if baseline_val is None:
                        # Backward compatibility for legacy buckets without snapshot baseline.
                        baseline_val = 0.0
                        if start_dt and baseline_series:
                            for point in baseline_series:
                                point_time_str = point.get('t', '')
                                try:
                                    point_dt = datetime.fromisoformat(point_time_str.replace('Z', ''))
                                    if point_dt <= start_dt:
                                        baseline_val = _metric_value(point, metric_raw)
                                    else:
                                        break
                                except:
                                    pass

                    # [V20260319_2115] Chart start baseline for 'Start' column normalization
                    chart_baseline_val = 0.0
                    if chart_start_dt and baseline_series:
                        for point in baseline_series:
                            point_dt_str = point.get('t', '')
                            try:
                                p_dt = datetime.fromisoformat(point_dt_str.replace('Z', ''))
                                if p_dt <= chart_start_dt:
                                    chart_baseline_val = _metric_value(point, metric_raw)
                                else: break
                            except: pass
                    else:
                        chart_baseline_val = day_baseline

                    d3_baseline_val = float(strat.get('delta3_net_at_selection', 0.0) or 0.0)

                    # [V20260319_2135] Map metrics to Delta1/2/3 for UI standardization
                    strat['start_from_net'] = 0.0
                    strat['net_at_creation'] = round(float(baseline_val) - day_baseline, 2)
                    strat['current_total_net'] = round(float(current_total) - day_baseline, 2)
                    strat['delta1'] = strat['current_total_net'] # Profit since Midnight
                    strat['delta2'] = round(strat['current_total_net'] - strat['net_at_creation'], 2) # Profit since Creation
                    strat['delta3'] = round(strat['current_total_net'] - d3_baseline_val, 2) # Profit since Delta3 selection
                    strat['delta_type'] = _normalize_delta_type(strat.get('delta_type') or bucket_delta_type)
                    if bucket_delta_type == 'delta1':
                        strat['total_net'] = strat['delta1']
                    elif bucket_delta_type == 'delta3':
                        strat['total_net'] = strat['delta3']
                    else:
                        strat['total_net'] = strat['delta2']

            strat_rows = [s for s in bucket.get('strategies', []) if isinstance(s, dict)]
            if strat_rows:
                loser = min(strat_rows, key=lambda s: float(s.get('total_net', 0.0) or 0.0))
                bucket['alt_trade_key'] = loser.get('key') if float(loser.get('total_net', 0.0) or 0.0) < 0 else None
            else:
                bucket['alt_trade_key'] = None

            alt_trade_key = str(bucket.get('alt_trade_key') or '')
            for strat in strat_rows:
                strat['is_alt_candidate'] = bool(alt_trade_key and str(strat.get('key') or '') == alt_trade_key)

        return jsonify({
            'success': True,
            'buckets': buckets,
            'max_strategies': 5
        })
    except Exception as e:
        print(f"[TRADE-BUCKETS-CRITICAL] Error in get_trade_buckets: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/trade_buckets', methods=['POST'])
def create_trade_bucket():
    """Create a new trade bucket."""
    try:
        import uuid
        payload = request.json
        name = payload.get('name')
        strategies = payload.get('strategies', [])
        mode = payload.get('mode', 'live')
        product_type = payload.get('product_type')
        delta_type = _normalize_delta_type(payload.get('delta_type'))
        trade_alt_net = bool(payload.get('trade_alt_net', False))

        start_time_str = payload.get('start_time')
        chart_start_time_str = payload.get('chart_start_time')
        payload_date = str(payload.get('date', '')).strip()
        current_date_str = datetime.now().strftime('%Y-%m-%d')

        # Prefer explicit UI-selected trade date when provided.
        if payload_date:
            try:
                datetime.strptime(payload_date, '%Y-%m-%d')
                current_date_str = payload_date
            except Exception:
                pass

        if start_time_str and not payload_date:
            try:
                if start_time_str.endswith('Z'):
                    dt = datetime.fromisoformat(start_time_str[:-1])
                else:
                    dt = datetime.fromisoformat(start_time_str)
                current_date_str = dt.strftime('%Y-%m-%d')
            except:
                pass
        bias_at_creation = _get_current_bias(mode, current_date_str) or "UNKNOWN"

        data = _load_trade_buckets(mode=mode, date_str=current_date_str, product_type=product_type)
        buckets = data.get('buckets', [])

        # Snapshot summary_net at bucket creation time so baseline is static.
        summary_file = _resolve_day_dir(mode, current_date_str, product_type=product_type) / "_summary_net.json"
        summary_net = {}
        if summary_file.exists():
            try:
                with open(summary_file, 'r') as f:
                    summary_data = json.load(f)
                    summary_net = summary_data.get('strategies', {})
            except Exception as e:
                print(f"[TRADE-BUCKETS-WARN] create snapshot load failed: {e}")

        chart_start_dt = None
        if chart_start_time_str:
            try:
                chart_start_dt = datetime.fromisoformat(str(chart_start_time_str).replace('Z', ''))
            except Exception:
                chart_start_dt = None

        creation_dt = None
        if start_time_str:
            try:
                creation_dt = datetime.fromisoformat(str(start_time_str).replace('Z', ''))
            except Exception:
                creation_dt = None

        def _normalize_bucket_metric(metric_raw: str) -> str:
            raw = str(metric_raw or 'net').strip().lower()
            if raw in ('buy', 'buy_net', 'buy_net_return_sum'):
                return 'buy_net'
            if raw in ('sell', 'sell_net', 'sell_net_return_sum'):
                return 'sell_net'
            if raw in ('alt', 'alt_net', 'alt_net_return_sum'):
                return 'alt_net'
            return 'net'

        def _metric_value(point: dict, metric_raw: str) -> float:
            key = _normalize_bucket_metric(metric_raw)
            try:
                return float(point.get(key, point.get('net', 0.0)) or 0.0)
            except Exception:
                return 0.0

        def _net_at_or_before(series: list, target_dt: datetime, metric_raw: str):
            if not series or not target_dt:
                return None
            val = None
            for p in series:
                ts = p.get('t')
                if not ts:
                    continue
                try:
                    p_dt = datetime.fromisoformat(str(ts).replace('Z', ''))
                except Exception:
                    continue
                if p_dt <= target_dt:
                    val = _metric_value(p, metric_raw)
                else:
                    break
            return val

        def _creation_net_for_key(strat_key: str, metric_raw: str) -> float:
            parts = str(strat_key or '').split(' | ')
            if len(parts) != 2:
                parts = str(strat_key or '').split('|')
            if len(parts) != 2:
                return 0.0
            strategy_name = parts[0].strip()
            product = parts[1].strip()
            series = summary_net.get(strategy_name, {}).get(product, [])
            if not series:
                return 0.0
            # [V20260319_2125] Use creation_dt (the Cyan Dot logic) to find the exact baseline net
            if creation_dt:
                v = _net_at_or_before(series, creation_dt, metric_raw)
                if v is not None:
                    return float(v)
            return _metric_value(series[-1], metric_raw)

        def _start_from_net_for_key(strat_key: str, fallback_creation: float, metric_raw: str) -> float:
            if not chart_start_dt:
                return float(fallback_creation)
            parts = str(strat_key or '').split(' | ')
            if len(parts) != 2:
                parts = str(strat_key or '').split('|')
            if len(parts) != 2:
                return float(fallback_creation)
            strategy_name = parts[0].strip()
            product = parts[1].strip()
            series = summary_net.get(strategy_name, {}).get(product, [])
            v = _net_at_or_before(series, chart_start_dt, metric_raw)
            if v is None:
                # [V20260319_1445] If no history before chart start, assume 0.0 baseline to allow delta calculation
                return 0.0
            return float(v)

        if not name:
            return jsonify({'success': False, 'message': 'Bucket name is required'}), 400

        if any(b['name'] == name for b in buckets):
            return jsonify({'success': False, 'message': 'Bucket with this name already exists'}), 400

        bucket_guid = str(uuid.uuid4())

        processed_strategies = []
        for strat in strategies:
            strategy_id = str(uuid.uuid4())
            if isinstance(strat, dict):
                strat_key = strat.get('key') or strat.get('strategy') or ''
                metric_raw = str(strat.get('metric', 'net') or 'net')
                creation_net = round(_creation_net_for_key(strat_key, metric_raw), 2)
                start_from_net = round(_start_from_net_for_key(strat_key, creation_net, metric_raw), 2)
                strat['strategy_id'] = strategy_id
                strat['bias_at_creation'] = bias_at_creation
                strat['start_from_net'] = start_from_net
                strat['net_at_creation'] = creation_net
                strat['current_total_net'] = creation_net
                strat['net_delta_from_creation'] = 0.0
                strat['total_net'] = 0.0
                strat['delta_type'] = delta_type
                strat['delta3_net_at_selection'] = creation_net
                strat['delta3_selected_at'] = start_time_str or chart_start_time_str or datetime.now().isoformat()
                processed_strategies.append(strat)
            else:
                raw_strat = str(strat or '')
                parts = raw_strat.split(' | ')
                if len(parts) < 3:
                    parts = [p.strip() for p in raw_strat.split('|')]
                metric_raw = parts[2] if len(parts) >= 3 else 'net'
                key_only = ' | '.join(parts[:2]) if len(parts) >= 2 else raw_strat
                creation_net = round(_creation_net_for_key(key_only, metric_raw), 2)
                start_from_net = round(_start_from_net_for_key(key_only, creation_net, metric_raw), 2)
                processed_strategies.append({
                    'strategy_id': strategy_id,
                    'key': key_only,
                    'metric': metric_raw,
                    'bias_at_creation': bias_at_creation,
                    'start_from_net': start_from_net,
                    'net_at_creation': creation_net,
                    'current_total_net': creation_net,
                    'net_delta_from_creation': 0.0,
                    'total_net': 0.0,  # backward-compatible alias for net delta
                    'delta_type': delta_type,
                    'delta3_net_at_selection': creation_net,
                    'delta3_selected_at': start_time_str or chart_start_time_str or datetime.now().isoformat(),
                    'live_trade_net': 0.0
                })

        if len(processed_strategies) < 2:
            return jsonify({'success': False, 'message': 'Minimum 2 strategies/metrics required for a Trade Bucket [V20260311_1215]'}), 400

        minimum_difference = float(payload.get('minimum_difference', 5.0))
        locked_directional_metric = _infer_split_net_bucket_lock(processed_strategies, minimum_difference)

        new_bucket = {
            'bucket_id': bucket_guid,
            'name': name,
            'start_time': payload.get('start_time') or datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'chart_start_time': chart_start_time_str,
            'mode': mode,
            'product_type': product_type or default_product_type(_load_layout_runtime_config()),
            'delta_type': delta_type,
            'delta3_selected_at': start_time_str or chart_start_time_str or datetime.now().isoformat(),
            'trade_alt_net': trade_alt_net,
            'market_bias_at_creation': bias_at_creation,
            'strategies': processed_strategies,
            'locked_directional_metric': locked_directional_metric,
            'live': False,
            'open_trades': False,
            'open_trade_count': 0,
            'minimum_difference': minimum_difference
        }

        buckets.append(new_bucket)
        data['buckets'] = buckets

        if delta_type == 'delta3':
            selected_dt = creation_dt or chart_start_dt or datetime.now()
            _capture_bucket_delta3_baseline(new_bucket, mode=mode, date_str=current_date_str, product_type=product_type, selected_at=selected_dt)

        _save_trade_buckets(data, mode=mode, date_str=current_date_str, product_type=product_type)

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
        product_type = payload.get('product_type')

        if not name:
            return jsonify({'success': False, 'message': 'Bucket name is required'}), 400

        data = _load_trade_buckets(mode=mode, date_str=date_str, product_type=product_type)
        buckets = data.get('buckets', [])

        updated = False
        target_bucket = None
        auto_deactivated: List[dict] = []
        max_live_tb = _get_max_live_tb()

        for b in buckets:
            if b['name'] == name:
                target_bucket = b
                _ensure_bucket_locked_directional_metric(b)
                if 'live' in payload:
                    b['live'] = bool(payload['live'])
                    updated = True
                if 'minimum_difference' in payload:
                    b['minimum_difference'] = float(payload['minimum_difference'])
                    updated = True
                if 'delta_type' in payload:
                    next_delta_type = _normalize_delta_type(payload['delta_type'])
                    prev_delta_type = _normalize_delta_type(b.get('delta_type'))
                    b['delta_type'] = next_delta_type
                    if next_delta_type == 'delta3' and prev_delta_type != 'delta3':
                        selected_at = datetime.now()
                        _capture_bucket_delta3_baseline(b, mode=mode, date_str=date_str, product_type=product_type, selected_at=selected_at)
                    updated = True
                if 'trade_alt_net' in payload:
                    b['trade_alt_net'] = bool(payload['trade_alt_net'])
                    updated = True
                break

        if not target_bucket:
            return jsonify({'success': False, 'message': 'Bucket not found'}), 404

        if updated:
            if target_bucket.get('live'):
                auto_deactivated, max_live_tb = _enforce_max_live_tb_inplace(
                    buckets, preferred_live_name=name
                )
            _save_trade_buckets(data, mode=mode, date_str=date_str, product_type=product_type)
            
            # [V20260204_1410] 2026-02-04 14:10: Workflow Refinement
            # If a bucket is toggled live, suspend Frequency Notifier and sync to Grid Live
            if target_bucket.get('live'):
                # [V20260205_2100] Set automated source to Trade Bucket
                _update_automated_source('Trade Bucket')
                
                # 1. Update Config to suspend alerts
                try:
                    with open(CONFIG_FILE, "r") as f:
                        cfg = json.load(f)
                    cfg['rank_alert_suspended'] = True
                    # [V20260205_2100] Also ensure config sync
                    cfg['automated_trade_source'] = 'Trade Bucket'
                    srcs = cfg.get('automated_trade_sources')
                    if not isinstance(srcs, list):
                        srcs = []
                    srcs = [str(s).strip() for s in srcs if isinstance(s, str) and str(s).strip()]
                    if 'Trade Bucket' not in srcs:
                        srcs.append('Trade Bucket')
                    cfg['automated_trade_sources'] = srcs
                    with open(CONFIG_FILE, "w") as f:
                        json.dump(cfg, f, indent=4)
                    print("[BUCKET] Frequency Notifier SUSPENDED (Config updated)")
                except: pass
                
                # 2. Sync Leader to Grid Live (includes archiving)
                _sync_bucket_to_grid_live(target_bucket, mode, date_str, product_type=product_type)
            else:
                # If bucket deactivated, just ensure grid_live state is updated
                _sync_bucket_to_grid_live(target_bucket, mode, date_str, product_type=product_type)

            # Ensure any bucket auto-deactivated by max_live_tb cap is removed from grid.
            for b in auto_deactivated:
                if str(b.get('name') or '') != str(target_bucket.get('name') or ''):
                    _sync_bucket_to_grid_live(
                        {'name': b.get('name'), 'live': False, 'product_type': product_type},
                        mode,
                        date_str,
                        product_type=product_type,
                    )
            
        return jsonify({
            'success': True,
            'bucket': target_bucket,
            'max_live_tb': max_live_tb,
            'auto_deactivated': [str(b.get('name') or '') for b in auto_deactivated if b.get('name')]
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/trade_buckets/<path:bucket_name>', methods=['DELETE'])
def delete_trade_bucket(bucket_name):
    """Delete a trade bucket."""
    try:
        mode = request.args.get('mode', 'live')
        date_str = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))
        product_type = request.args.get('product_type')

        data = _load_trade_buckets(mode=mode, date_str=date_str, product_type=product_type)
        buckets = data.get('buckets', [])

        initial_len = len(buckets)
        buckets = [b for b in buckets if b['name'] != bucket_name]

        if len(buckets) < initial_len:
            data['buckets'] = buckets
            _save_trade_buckets(data, mode=mode, date_str=date_str, product_type=product_type)
            # [V20260122_2230] Clear records from activations by syncing empty/dead state
            # [V20260204_1410] Replaced _sync_bucket_to_activations with _sync_bucket_to_grid_live
            _sync_bucket_to_grid_live(
                {'name': bucket_name, 'live': False, 'product_type': product_type},
                mode,
                date_str,
                product_type=product_type,
            )
            return jsonify({'success': True, 'message': 'Bucket deleted'})
        else:
            return jsonify({'success': False, 'message': 'Bucket not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/trade_buckets/remove_all', methods=['POST'])
def remove_all_trade_buckets():
    """Remove all trade buckets for a given mode and date. [V20260206_1145]"""
    try:
        payload = request.json or {}
        mode = payload.get('mode', 'live').lower()
        date_str = payload.get('date', datetime.now().strftime('%Y-%m-%d'))
        product_type = payload.get('product_type')

        # 1. Load data
        data = _load_trade_buckets(mode=mode, date_str=date_str, product_type=product_type)
        buckets = data.get('buckets', [])
        
        if not buckets:
            return jsonify({'success': True, 'message': 'No buckets to remove.'})

        # 2. Sync all live buckets to OFF state in grid before clearing
        for b in buckets:
            if b.get('live'):
                 _sync_bucket_to_grid_live(
                     {'name': b['name'], 'live': False, 'product_type': product_type},
                     mode,
                     date_str,
                     product_type=product_type,
                 )

        # 3. Clear and save
        data['buckets'] = []
        _save_trade_buckets(data, mode=mode, date_str=date_str, product_type=product_type)
        
        print(f"[BUCKET] Cleared {len(buckets)} buckets for {mode} on {date_str}.")
        return jsonify({
            'success': True, 
            'message': f'Successfully removed {len(buckets)} buckets.'
        })

    except Exception as e:
        print(f"[BUCKET-ERROR] Remove all failed: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500


def _get_health_status(mode: str) -> dict:
    """Internal helper to get health status for a specific mode."""
    # 1. Check Trade Files & Recency
    today_str = datetime.now().strftime('%Y-%m-%d')
    # [V20260316_0150] Use resolve_day_dir to account for product type subfolder (e.g. /forex/)
    trade_dir = _resolve_day_dir(mode, today_str)
    trade_files_exist = False
    trade_recency_ok = True
    latest_trade_age_min = -1
    
    # Load config
    trade_file_max_age = 30
    try:
        with open(CONFIG_FILE, "r") as f:
            cfg = json.load(f)
            trade_file_max_age = cfg.get("trade_file_min_age_minutes", 30)
    except: pass

    if trade_dir.exists():
        json_files = list(trade_dir.glob('*.json'))
        # Filter out metadata files starting with _
        actual_trades = [f for f in json_files if not f.name.startswith('_')]
        trade_files_exist = len(actual_trades) > 0
        
        if trade_files_exist:
            # Get latest file based on modification time
            # [V20260312_0222] Robustness: Handle WinError 2 (missing file) and long path issues
            try:
                latest_file = max(actual_trades, key=lambda f: f.stat().st_mtime if f.exists() else 0)
                latest_ts = latest_file.stat().st_mtime
                age_min = (datetime.now().timestamp() - latest_ts) / 60
                latest_trade_age_min = int(age_min)
                
                if age_min > trade_file_max_age:
                    trade_recency_ok = False
                    print(f"[HEALTH] Trade files stale! Oldest is {age_min:.1f} min old (Limit: {trade_file_max_age})")
            except Exception as ex:
                print(f"[HEALTH-ERROR] Failed to stat latest trade file: {ex}")
                trade_files_exist = False

    # 2. Check Price Feed
    price_feed_ok = False
    feed_latency_sec = -1
    try:
        import subprocess
        target_db = 'tradedb_sim2' if mode == 'sim' else 'tradedb'
        if mode == 'live':
            urls = [
                "http://127.0.0.1:8001/api/vw_000_fx_quotes",
                "http://127.0.0.1:8002/api/vw_000_fx_quotes",
                "http://127.0.0.1:8000/api/vw_000_fx_quotes?db=tradedb",
            ]
        else:
            urls = [f"http://127.0.0.1:8001/api/vw_000_fx_quotes?db={target_db}"]

        for url in urls:
            result = subprocess.run(['curl', '-s', url], capture_output=True, text=True, timeout=5)
            
            if result.returncode != 0:
                print(f"[HEALTH-DEBUG] Curl failed for {url} with code {result.returncode}. Stderr: {result.stderr}")
                continue

            try:
                data = json.loads(result.stdout)
            except Exception as parse_err:
                print(f"[HEALTH-DEBUG] Invalid JSON from {url}: {parse_err}")
                continue

            rows = data.get('data', [])
            if not rows:
                print(f"[HEALTH-DEBUG] No data rows in response from {url}")
                continue

            # [V20260202_0150] User overridden: If we get data, connection is Active.
            # Latency checks will just inform the second row.
            price_feed_ok = True

            ts_str = rows[0].get('timestamp', '')
            if ts_str:
                # [V20260130_1357] Robust timestamp parsing (handles 'T' or ' ' separator)
                clean_ts = ts_str.replace('T', ' ').split('.')[0] # Remove fractional seconds
                feed_dt = datetime.strptime(clean_ts, '%Y-%m-%d %H:%M:%S')
                
                # [V20260202_0145] Check against both Local and UTC time to handle timezone mismatches
                latency_local = (datetime.now() - feed_dt).total_seconds()
                latency_utc = (datetime.utcnow() - feed_dt).total_seconds()
                
                # Use the smaller positive latency (assuming feed can't be in future)
                # If local is negative (feed in future vs local), maybe UTC is better match
                candidates = []
                if latency_local > -300: candidates.append(latency_local)
                if latency_utc > -300: candidates.append(latency_utc)
                
                latency = min(candidates) if candidates else latency_local
                feed_latency_sec = int(latency)
                
                if latency < 900: # Increased to 15 mins to be more tolerant of drift/weekend gaps
                    price_feed_ok = True
                elif 3300 < latency < 3900: # ~1 hour offset detection (3600s)
                    price_feed_ok = True
                    feed_latency_sec = int(latency - 3600) # Adjust display
                elif 4600 < latency < 4900: # ~1h 20m offset (likely what we saw 4670s)
                    # This implies feed is legitimately 1h+ old OR serious timezone skew.
                    # If user says "fine", we might just trust the connectivity.
                    pass
            break
    except Exception as e:
        print(f"[HEALTH] Price feed unavailable/error: {e}")

    is_healthy = trade_files_exist and price_feed_ok and trade_recency_ok
    
    return {
        'healthy': is_healthy,
        'checks': {
            'trade_files': trade_files_exist,
            'trade_recency': trade_recency_ok,
            'latest_trade_age_min': latest_trade_age_min,
            'price_feed': price_feed_ok,
            'feed_latency_sec': feed_latency_sec
        }
    }


@app.route('/api/system_health', methods=['GET'])
def health_check():
    """
    [V20260130_1315] System health check:
    1. Check for trade files in today's folder.
    2. Check if price feed is responsive and < 5 mins old.
    [V20260201_2330] Updated to support mode='all' for dual status.
    """
    try:
        mode = request.args.get('mode', 'live').lower()
        
        if mode == 'all':
             return jsonify({
                'success': True,
                'live': _get_health_status('live'),
                'sim': _get_health_status('sim'),
                'timestamp': datetime.now().isoformat()
            })
            
        status = _get_health_status(mode)
        
        return jsonify({
            'success': True,
            'healthy': status['healthy'],
            'checks': status['checks'],
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        print(f"[HEALTH-ERROR] Global health check failed: {e}")
        return jsonify({'success': False, 'healthy': False, 'message': str(e)}), 500

@app.route('/api/promotion_blocks', methods=['GET'])
def promotion_blocks():
    """
    Return trades with block reasons for promotion to L-trade,
    plus current grid entries for context.
    """
    try:
        mode = request.args.get('mode', 'live').lower()
        date_str = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))
        include_closed = str(request.args.get('include_closed', 'true')).lower() in ('1', 'true', 'yes')
        q = str(request.args.get('q', '') or '').strip().lower()
        try:
            limit = int(request.args.get('limit', 50))
        except Exception:
            limit = 50
        if limit <= 0:
            limit = 50

        day_dirs = _iter_day_dirs_for(mode, date_str)
        if not day_dirs:
            return jsonify({
                'success': True,
                'mode': mode,
                'date': date_str,
                'count': 0,
                'blocks': [],
                'grid_live': []
            })

        patterns = ['*_op.json']
        if include_closed:
            patterns.extend(['*_cl.json', '*_cld.json'])

        files = []
        product_hint = q.upper() if q and q.isalpha() and len(q) <= 10 else None
        for day_dir in day_dirs:
            for fp in _iter_trade_json_files(
                day_dir,
                include_archived_closed=include_closed,
                product_hint=product_hint,
            ):
                if any(fp.name.endswith(pat.replace('*', '')) for pat in patterns):
                    files.append(fp)

        blocks = []
        for fp in files:
            try:
                with open(fp, 'r') as f:
                    d = json.load(f)
            except Exception:
                continue

            reason = d.get('trade_block_reason')
            if not reason:
                continue

            script_name = d.get('script_name') or d.get('source_strategy') or d.get('app_name')
            product = d.get('product')
            reason_text = f"{reason} {d.get('trade_block_reason_detail') or ''}".strip()
            if q:
                hay = f"{product or ''} {script_name or ''} {reason_text}".lower()
                if q not in hay:
                    continue

            blocks.append({
                'filename': fp.name,
                'status': d.get('status'),
                'trade_id': d.get('trade_id'),
                'product': product,
                'script_name': script_name,
                'source_strategy': d.get('source_strategy'),
                'direction': d.get('direction'),
                'entry_time': d.get('entry_time'),
                'exit_time': d.get('exit_time'),
                'entry_price': d.get('entry_price'),
                'current_price': d.get('current_price'),
                'exit_price': d.get('exit_price'),
                'net_return': d.get('net_return'),
                'alt_net': d.get('alt_net'),
                'is_live_trade': bool(d.get('is_live_trade', False)),
                'order_sent_net': bool(d.get('order_sent_net', False)),
                'order_sent_alt': bool(d.get('order_sent_alt', False)),
                'source_screen': d.get('source_screen'),
                'trade_block_reason': reason,
                'trade_block_reason_detail': d.get('trade_block_reason_detail'),
                'grid_live_context_at_block': d.get('grid_live_context_at_block'),
            })

        blocks.sort(key=lambda x: (str(x.get('entry_time') or ''), str(x.get('filename') or '')), reverse=True)
        blocks = blocks[:limit]

        grid_file = ROOT_PATH / 'grid_live.json'
        grid_live = []
        if grid_file.exists():
            try:
                with open(grid_file, 'r') as f:
                    g = json.load(f)
                if isinstance(g, dict):
                    grid_live = g.get(mode, [])
                elif isinstance(g, list):
                    grid_live = g
            except Exception:
                grid_live = []

        return jsonify({
            'success': True,
            'mode': mode,
            'date': date_str,
            'query': q,
            'limit': limit,
            'count': len(blocks),
            'blocks': blocks,
            'grid_live': grid_live
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


# Main
# -----------------------------------------------------------
@app.route('/api/grid_live', methods=['GET'])
def get_grid_live():
    """
    [V20260128_1428] Returns the current grid_live.json state for frontend restoration.
    [V20260131_0300] Supports 'mode' param (live/sim) and separated storage.
    [V20260204_2120] Added automatic bucket reconciliation.
    """
    try:
        mode = request.args.get('mode', 'live').lower()
        
        # [V20260204_2120] Periodically ensure buckets are promoted / frequency cleared
        _reconcile_active_buckets(mode=mode)
        
        grid_live_file = ROOT_PATH / "grid_live.json"
        
        if grid_live_file.exists():
            with open(grid_live_file, "r") as f:
                data = json.load(f)
            
            # [V20260131_0300] Handle legacy List format transparently
            if isinstance(data, list):
                # If legacy list, assume it's 'live' data
                if mode == 'live':
                    return jsonify({'success': True, 'data': data})
                else:
                    return jsonify({'success': True, 'data': []})
            elif isinstance(data, dict):
                # New Dict format
                return jsonify({'success': True, 'data': data.get(mode, [])})
            
            return jsonify({'success': True, 'data': []})
        else:
            return jsonify({'success': True, 'data': []})
    except Exception as e:
        print(f"[API-ERROR] GET /api/grid_live failed: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/grid_live', methods=['POST'])
def update_grid_live():
    """
    [V20260129_1055] Receives live monitoring state from the multi_chart UI.
    [V20260130_1720] Added replace_all flag for "Monitor Only" feature.
    [V20260131_0300] Support 'mode' (live/sim) separation and format migration.
    """
    try:
        payload = request.json
        group = payload.get('group') # Card name source
        models = payload.get('models') # List of {model, product, metric}
        replace_all = bool(payload.get('replace_all', False))
        mode = payload.get('mode', 'live').lower() # [V20260131_0300]
        source = payload.get('source', 'ui')
        source_str = str(source).strip()

        if not group:
            return jsonify({'success': False, 'message': 'Group name is required'}), 400

        grid_live_file = ROOT_PATH / "grid_live.json"
        
        # [V20260205_2100] Handle automated_trade_source for Frequency
        if source_str == 'rank_alert_ui' or source_str == 'frequency_ui':
            # Manual trigger from Frequency screen
            _update_automated_source('Frequency')
        
        if source_str.startswith(('rank_alert', 'frequency')):
            # [V20260205_2100] Check if Frequency is the current automated source
            if not _is_source_allowed('Frequency'):
                 print(f"[GRID-LIVE] REJECTED: source='{source_str}' blocked. Current source is not Frequency.")
                 return jsonify({'success': True, 'message': 'Skipped (Source Overrule)'})

        # [V20260215_0004] Gate breakout/grid UI source by config allowlist.
        # Live-trades groups like 'breakout|...' originate from this path.
        if source_str in ('ui', 'grid_live', 'breakout'):
            if not _is_source_allowed('Breakout'):
                print(f"[GRID-LIVE] REJECTED: source='{source_str}' blocked by config allowlist (requested='Breakout').")
                return jsonify({'success': True, 'message': 'Skipped (Source Overrule)'})

        # [V20260204_2200] Block Manual UI updates if a Trade Bucket is Live
        # Enforces absolute bucket priority: "NO MORE - SOURCE:UI"
        if source_str in ('ui',):
            if _any_trade_bucket_is_live(mode):
                print(f"[GRID-LIVE] REJECTED: source='{source_str}' update blocked because a Trade Bucket is LIVE.")
                return jsonify({'success': True, 'message': 'Skipped (Bucket Live Overrule)'})

        with GRID_LIVE_LOCK:
            full_data = {'live': [], 'sim': []}
            
            if grid_live_file.exists():
                try:
                    with open(grid_live_file, "r") as f:
                        loaded = json.load(f)
                    
                    if isinstance(loaded, list):
                        # [V20260131_0300] Migration: Move legacy list to 'live'
                        full_data['live'] = loaded
                        print("[API] Migrating grid_live.json from List to Dict format.")
                    elif isinstance(loaded, dict):
                        full_data = loaded
                        # Ensure keys exist
                        if 'live' not in full_data: full_data['live'] = []
                        if 'sim' not in full_data: full_data['sim'] = []
                except Exception:
                    pass
            
            # Target the specific list for this mode
            target_list = full_data.get(mode, [])
            
            # [V20260130_1640] Absolute Strategy Persistence Guard (Per Mode)
            master_timestamps = { (m.get('model'), m.get('product')): m.get('activated_at') 
                                 for m in target_list if m.get('activated_at') }
            
            def _srcgrp(entry: Dict[str, Any]) -> Tuple[str, str]:
                src = str(entry.get('source') or 'ui')
                grp = str(entry.get('group') or '')
                return (src, grp)

            # 1. Isolate existing entries within this mode
            if replace_all:
                other_groups = []
                print(f"[API] replace_all=True ({mode}). Clearing previous items.")
            else:
                incoming_srcgrp = (str(source_str or 'ui'), str(group or ''))
                # Append semantics across different source-groups:
                # only replace entries for the exact same (source, group)
                other_groups = [m for m in target_list if _srcgrp(m) != incoming_srcgrp]
            
            # 2. Build updated state
            new_target_list = list(other_groups)
            if models:
                now_local = datetime.now().isoformat().split('.')[0] 
                for m in models:
                    m_model = m.get('model')
                    m_product = m.get('product')
                    
                    # [V20260202_0220] Fix: Ensure group is persisted in the model object
                    m['group'] = group
                    # [V20260204_1410] Ensure source is persisted
                    if 'source' not in m:
                        m['source'] = source_str

                    # Restore original timestamp if exists
                    original_ts = master_timestamps.get((m_model, m_product))
                    if m.get('activated_at'):
                        pass # Keep what's sent
                    elif original_ts:
                         m['activated_at'] = original_ts # Restore
                    else:
                         m['activated_at'] = now_local # New
                         
                    new_target_list.append(m)
            
            # Update the full structure
            def _material_signature(items: List[Dict[str, Any]]) -> List[Tuple[str, str, str]]:
                # Material change criteria: strategy/model, product, metric only.
                return sorted(
                    (
                        str(x.get('model', '')),
                        str(x.get('product', '')),
                        str(x.get('metric', ''))
                    )
                    for x in items
                )

            if _material_signature(target_list) == _material_signature(new_target_list):
                print(f"[GRID-LIVE] source={source} no material change for {mode} group={group}; skipped archive/write.")
                return jsonify({'success': True, 'count': len(target_list), 'message': 'No material change'})

            # [V20260215_0003] Archive only when material state changes.
            _archive_grid_live(mode, force=True) # [V20260424_2310] Force archive on bucket deletion

            full_data[mode] = new_target_list
            
            with open(grid_live_file, "w") as f:
                json.dump(full_data, f, indent=4)
            if models:
                print(f"[GRID-LIVE] source={source_str} updated {mode} entries from group={group}: {[m.get('model') for m in models]}")
                
            # [V20260131_0305] Sync activations for this mode
            _sync_grid_to_activations(new_target_list, mode=mode)
                
        return jsonify({'success': True, 'count': len(full_data[mode])})

    except Exception as e:
        print(f"[API-ERROR] POST /api/grid_live failed: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/grid_live/prune_siblings', methods=['POST'])
def prune_grid_live_siblings():
    """Prune sibling products for a model after live execution."""
    try:
        payload = request.json or {}
        mode = str(payload.get('mode', 'live')).lower()
        model = payload.get('model')
        product = payload.get('product')
        reason = payload.get('reason', '')
        result = _prune_grid_live_siblings(model, product, mode, reason=reason)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/grid_live/prune_from_live_trades', methods=['POST'])
def prune_from_live_trades():
    """Periodic sweep: prune sibling products for any executed live trades."""
    try:
        payload = request.json or {}
        mode = str(payload.get('mode', 'live')).lower()
        date = payload.get('date') or datetime.now().strftime('%Y-%m-%d')
        trade_dir = BASE_PATH / mode / date
        live_file = trade_dir / "_live_trades.json"
        if not live_file.exists():
            return jsonify({'success': True, 'removed': 0, 'message': 'no live trades file'})

        with open(live_file, 'r') as f:
            data = json.load(f)
        trades = data.get('trades', [])

        removed_total = 0
        seen = set()
        for t in trades:
            if t.get('is_live_trade') is not True:
                continue
            model = t.get('source_strategy') or t.get('script_name') or t.get('app_name')
            product = t.get('product')
            if not model or not product:
                continue
            key = (model, str(product).upper())
            if key in seen:
                continue
            seen.add(key)
            res = _prune_grid_live_siblings(model, product, mode, reason='PERIODIC_SWEEP')
            removed_total += int(res.get('removed', 0) or 0)

        return jsonify({'success': True, 'removed': removed_total, 'checked': len(seen)})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/switch_rule/activate', methods=['POST'])
def switch_rule_activate():
    """
    [V20260420] Activates a strategy in grid_live.json from the Frequency Explorer switch rule.
    Accepts { product, strategy, mode } — replaces any existing switch_rule entry (one active at a time).
    """
    try:
        payload = request.json or {}
        product  = str(payload.get('product', '')).strip()
        strategy = str(payload.get('strategy', '')).strip()
        mode     = str(payload.get('mode', 'live')).lower()

        if not product or not strategy:
            return jsonify({'success': False, 'message': 'product and strategy are required'}), 400

        grid_live_file = ROOT_PATH / "grid_live.json"
        # Build group name: freq_{product}_{strategy} with dots replaced by underscores
        safe_strategy = strategy.replace('.', '_')
        group = f"freq_{product}_{safe_strategy}"
        entry = {
            'model': strategy,
            'product': product,
            'metric': 'net',
            'group': group,
            'source': 'freq_switch_rule',
            'activated_at': datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        }

        def _switch_rule_material_signature(item: Dict[str, Any]) -> Tuple[str, str, str, str, str]:
            return (
                str(item.get('model') or ''),
                str(item.get('product') or ''),
                str(item.get('metric') or ''),
                str(item.get('group') or ''),
                str(item.get('source') or ''),
            )

        with GRID_LIVE_LOCK:
            full_data = {'live': [], 'sim': []}
            if grid_live_file.exists():
                try:
                    with open(grid_live_file, 'r') as f:
                        full_data = json.load(f)
                    if isinstance(full_data, list):
                        full_data = {'live': full_data, 'sim': []}
                except Exception:
                    pass

            target = full_data.get(mode, [])
            existing_switch = [m for m in target if m.get('source') == 'freq_switch_rule']
            if len(existing_switch) == 1:
                if _switch_rule_material_signature(existing_switch[0]) == _switch_rule_material_signature(entry):
                    print(f"[SWITCH_RULE] No-op for {product} / {strategy} in grid_live ({mode}); skipped timestamp-only rewrite.")
                    return jsonify({
                        'success': True,
                        'product': product,
                        'strategy': strategy,
                        'mode': mode,
                        'message': 'No material change'
                    })
            if existing_switch:
                # Archive before replacing previous freq_switch_rule entry
                _archive_grid_live(mode, force=True) # [V20260424_2310] Force archive on bucket deletion
            # Remove previous freq_switch_rule entry — only one active at a time
            target = [m for m in target if m.get('source') != 'freq_switch_rule']
            target.append(entry)
            full_data[mode] = target

            with open(grid_live_file, 'w') as f:
                json.dump(full_data, f, indent=4)

            # Sync grid_live state directly to activations.json — bypasses reconciler gating
            _sync_grid_to_activations(full_data.get(mode, []), mode=mode)

        print(f"[SWITCH_RULE] Activated {product} / {strategy} in grid_live ({mode})")
        return jsonify({'success': True, 'product': product, 'strategy': strategy, 'mode': mode})
    except Exception as e:
        print(f"[SWITCH_RULE] Error: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500


def _sync_grid_to_activations(grid_data: list, mode: str = 'live'):
    """
    Synchronizes activations.json with grid_live.json state. [V20260407_1745]
    Merges automated grid entries while preserving manual toggles and auto_promote flags.
    """
    try:
        # 1. Load current activations
        full_activations = _load_activations()
        current_mode_section = full_activations.get(mode, {})

        # 2. Prepare for merge
        # We start by keeping all MANUAL entries from the current activations
        new_mode_section = {
            k: v for k, v in current_mode_section.items() 
            if v.get('manual') == True
        }

        # 3. Track product definitions from Grid
        active_definitions = {} # key -> { 'products': set(), 'source': str, 'manual': bool, 'auto_promote': bool }

        # 4. Iterate Grid Data to build definitions
        for m in grid_data:
            model = m.get('model')
            product = m.get('product')
            metric = m.get('metric', 'net')
            source = m.get('source', 'ui')
            manual = bool(m.get('manual', False))

            # Determine target activation keys based on metric
            target_keys = []
            if metric == 'net':
                target_keys = [f"{model}_buy_net", f"{model}_sell_net"]
            elif metric == 'alt':
                target_keys = [f"{model}_buy_alt", f"{model}_sell_alt"]
            elif metric == 'buy_net':
                target_keys = [f"{model}_buy_net"]
            elif metric == 'sell_net':
                target_keys = [f"{model}_sell_net"]
            elif metric == 'buy_alt':
                target_keys = [f"{model}_buy_alt"]
            elif metric == 'sell_alt':
                target_keys = [f"{model}_sell_alt"]
            else:
                target_keys = [model] # Fallback

            for key in target_keys:
                if key not in active_definitions:
                    # Try to preserve metadata from existing activation if available
                    existing = current_mode_section.get(key, {})
                    # [V20260420] freq_switch_rule entries are autonomous selections — always auto_promote
                auto_promote_default = True if source == 'freq_switch_rule' else bool(existing.get('auto_promote', False))
                active_definitions[key] = {
                        'products': set(),
                        'source': source if source != 'ui' else existing.get('source', 'ui'),
                        'manual': manual or existing.get('manual', False),
                        'auto_promote': auto_promote_default,
                        'activated_at': existing.get('activated_at')
                    }

                # Add product
                if product:
                    active_definitions[key]['products'].add(product)

                # Update metadata if this grid entry is more specific/newer
                if source != 'ui':
                    active_definitions[key]['source'] = source
                if manual:
                    active_definitions[key]['manual'] = True

        # 5. Finalize Grid Entries into the new section
        now = datetime.utcnow().isoformat()
        for key, defs in active_definitions.items():
            # If it's already in new_mode_section (manual), merge products
            if key in new_mode_section:
                existing_products = set(new_mode_section[key].get('products', []))
                merged_products = sorted(list(existing_products | defs['products']))
                new_mode_section[key]['products'] = merged_products
                # Preserve existing manual/auto_promote/activated_at
            else:
                # Add as new automated entry
                new_mode_section[key] = {
                    "active": True,
                    "manual": defs['manual'],
                    "auto_promote": defs['auto_promote'],
                    "activated_at": defs['activated_at'] or now,
                    "source": defs['source'],
                    "products": sorted(list(defs['products']))
                }

        # 6. Atomic Update
        full_activations[mode] = new_mode_section

        with open(ACTIVATIONS_FILE, "w") as f:
            json.dump(full_activations, f, indent=4)

        print(f"[SYNC] activations.json ({mode}) merged with grid_live.json. Active keys: {len(new_mode_section)}")

    except Exception as e:
        print(f"[SYNC-ERROR] Failed to sync activations: {e}")

# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# [V20260209_1010] Bias-Flip Notification System
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
NOTIFICATION_LOG_FILE = ROOT_PATH / "notification_log.json"

@app.route('/api/notification_action', methods=['POST'])
def log_notification_action():
    """Log a bias-flip notification action [V20260209_1010]"""
    try:
        data = request.json
        
        # Load existing log
        if NOTIFICATION_LOG_FILE.exists():
            with open(NOTIFICATION_LOG_FILE, 'r') as f:
                log_data = json.load(f)
        else:
            log_data = {"logs": []}
        
        # Create log entry
        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "bias_from": data.get('bias_from'),
            "bias_to": data.get('bias_to'),
            "recommended_strategy": data.get('recommended_strategy'),
            "recommended_product": data.get('recommended_product'),
            "action": data.get('action'),  # activated|dismissed|auto_activate|suspended
            "run_mode": data.get('run_mode', 'live')
        }
        
        # Append to logs
        log_data["logs"].insert(0, log_entry)  # Most recent first
        
        # Keep only last 100 entries
        log_data["logs"] = log_data["logs"][:100]
        
        # Save
        with open(NOTIFICATION_LOG_FILE, 'w') as f:
            json.dump(log_data, f, indent=2)
        
        # If action is to update config, do it
        if data.get('action') == 'auto_activate':
            # Set ai_picker_prompt to false
            if CONFIG_FILE.exists():
                with open(CONFIG_FILE, 'r') as f:
                    config = json.load(f)
                config['ai_picker_prompt'] = False
                with open(CONFIG_FILE, 'w') as f:
                    json.dump(config, f, indent=2)
        
        elif data.get('action') == 'suspended':
            # Set bias_notifications_suspended to true
            if CONFIG_FILE.exists():
                with open(CONFIG_FILE, 'r') as f:
                    config = json.load(f)
                config['bias_notifications_suspended'] = True
                with open(CONFIG_FILE, 'w') as f:
                    json.dump(config, f, indent=2)
        
        return jsonify({"success": True, "message": "Action logged successfully"})
    
    except Exception as e:
        print(f"[NOTIFICATION-LOG-ERROR] {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/notification_log', methods=['GET'])
def get_notification_log():
    """Retrieve notification log entries [V20260209_1010]"""
    try:
        if not NOTIFICATION_LOG_FILE.exists():
            return jsonify({"success": True, "logs": []})
        
        with open(NOTIFICATION_LOG_FILE, 'r') as f:
            log_data = json.load(f)
        
        # Optional filtering by run_mode
        mode = request.args.get('mode')
        logs = log_data.get("logs", [])
        
        if mode:
            logs = [log for log in logs if log.get('run_mode') == mode]
        
        return jsonify({"success": True, "logs": logs})
    
    except Exception as e:
        print(f"[NOTIFICATION-LOG-ERROR] {e}")
        return jsonify({"success": False, "error": str(e)}), 500


# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# [V20260209_1335] Bias History Tracking
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
BIAS_HISTORY_SESSION_FILE = ROOT_PATH / "bias_history_session.json"

def _get_bias_history_file(mode: str, date_str: str) -> Path:
    day_dir = _ensure_day_dir(str(mode or 'live').lower(), str(date_str or datetime.now().strftime('%Y-%m-%d')))
    return day_dir / "_bias_history.json"


def _load_tb_leadership(mode: str, date_str: str, product_type: str | None = None) -> list:
    """Load the persistent leadership report for a given date."""
    day_dirs = _iter_day_dirs_for(mode, date_str, product_type)
    
    all_leadership = []
    for day_dir in day_dirs:
        lb_file = day_dir / "_tb_leadership.json"
        if lb_file.exists():
            try:
                with open(lb_file, 'r') as f:
                    all_leadership.extend(json.load(f))
            except:
                pass
    return all_leadership


def _is_trade_in_leader_window(trade: dict, bucket_leadership: dict, bucket_metric: Any = None) -> bool:
    """Check if a trade was executed while its strategy was the leader in a specific bucket."""
    strategy = trade.get('app_name', '') or trade.get('script_name', '')
    product = trade.get('product', '')
    full_key = f"{strategy}:{product}"
    
    # Try alternate matching from trade metadata
    # (some trades store source_strategy instead of script_name)
    alt_keys = [full_key]
    if trade.get('source_strategy'):
        alt_keys.append(f"{trade['source_strategy']}:{product}")
    
    entry_time = trade.get('entry_time') or trade.get('time')
    if not entry_time:
        return False
        
    try:
        # Handle Z suffix if present
        entry_dt = datetime.fromisoformat(entry_time.replace('Z', '').replace(' ', 'T'))
    except:
        return False
        
    for window in bucket_leadership.get('windows', []):
        w_strat = window.get('strategy')
        if any(ak == w_strat or ak.startswith(w_strat + ":") for ak in alt_keys):
            start_dt = datetime.fromisoformat(window.get('start').replace(' ', 'T'))
            end_val = window.get('end')
            if end_val:
                end_dt = datetime.fromisoformat(end_val.replace(' ', 'T'))
                if start_dt <= entry_dt < end_dt:
                    if not _is_trade_direction_compatible_with_bucket_metric(trade, bucket_metric):
                        return False
                    return True
            else:
                # Active window
                if entry_dt >= start_dt:
                    if not _is_trade_direction_compatible_with_bucket_metric(trade, bucket_metric):
                        return False
                    return True
    return False


@app.route('/api/tb_leadership', methods=['GET'])
def get_tb_leadership_route():
    mode = request.args.get('mode', 'live')
    date = request.args.get('date') or datetime.now().strftime('%Y-%m-%d')
    product_type = request.args.get('product_type')
    return jsonify({
        "success": True,
        "leadership": _load_tb_leadership(mode, date, product_type)
    })

def _load_bias_history_safe(mode: str, date_str: str) -> dict:
    target_file = _get_bias_history_file(mode, date_str)
    if target_file.exists():
        try:
            with open(target_file, 'r') as f:
                data = json.load(f) or {}
            if not isinstance(data, dict):
                return {"history": []}
            if not isinstance(data.get("history"), list):
                data["history"] = []
            return data
        except Exception:
            try:
                stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup = target_file.with_name(f"_bias_history.corrupt_{stamp}.json")
                shutil.copy2(target_file, backup)
            except Exception:
                pass
            return {"history": []}

    return {"history": []}

def _load_bias_sessions_safe() -> dict:
    if not BIAS_HISTORY_SESSION_FILE.exists():
        return {}
    try:
        with open(BIAS_HISTORY_SESSION_FILE, 'r') as f:
            data = json.load(f) or {}
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}

def _save_bias_sessions(data: dict) -> None:
    with open(BIAS_HISTORY_SESSION_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def _atomic_write_json(path: Path, data: Any, indent: int = 2) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(f".{uuid.uuid4().hex}.tmp")
    with open(tmp, "w") as f:
        json.dump(data, f, indent=indent)
    os.replace(tmp, path)

def _parse_iso_ts(value: Any) -> Optional[datetime]:
    if not value:
        return None
    try:
        raw = str(value).strip()
        dt = datetime.fromisoformat(raw.replace('Z', '+00:00'))
        local_tz = datetime.now().astimezone().tzinfo
        if dt.tzinfo is None:
            # Trade files commonly persist naive UTC timestamps.
            # Convert them to local wall-clock time before window bucketing.
            dt = dt.replace(tzinfo=timezone.utc)
        if local_tz is not None:
            dt = dt.astimezone(local_tz)
        return dt.replace(tzinfo=None)
    except Exception:
        return None

def _parse_local_iso_ts(value: Any) -> Optional[datetime]:
    if not value:
        return None
    try:
        dt = datetime.fromisoformat(str(value).strip().replace('Z', '+00:00'))
        if dt.tzinfo is not None:
            dt = dt.astimezone().replace(tzinfo=None)
        return dt
    except Exception:
        return None

def _realtime_stats_cache_is_stale(payload: dict[str, Any] | None) -> bool:
    if not isinstance(payload, dict):
        return True
    generated_at = _parse_local_iso_ts(payload.get("generated_at"))
    if not generated_at:
        return True
    return (datetime.now() - generated_at).total_seconds() > REALTIME_STATS_CACHE_REFRESH_SECONDS

def _realtime_name_matches_group(name: str, group_key: str) -> bool:
    if group_key == "all":
        return True
    if group_key == "momentum_r":
        return name.startswith("momentum_r")
    if group_key == "momentum":
        return name.startswith("momentum") and not name.startswith("momentum_r")
    if group_key == "breakout_r_rev":
        return name.startswith("breakout_r_rev_")
    if group_key == "breakout_rev":
        return name.startswith("breakout_rev_")
    if group_key == "breakout_r":
        return name.startswith("breakout_r_") and not name.startswith("breakout_r_rev_")
    if group_key == "breakout":
        return (
            name.startswith("breakout_")
            and not name.startswith("breakout_r_")
            and not name.startswith("breakout_rev_")
            and not name.startswith("breakout_r_rev_")
        )
    return False

def _realtime_trade_names(trade: dict[str, Any]) -> list[str]:
    return [
        str(trade.get("script_name") or "").lower(),
        str(trade.get("source_strategy") or "").lower(),
        str(trade.get("strategy_name") or "").lower(),
        str(trade.get("app_name") or "").lower(),
    ]

def _classify_realtime_strategy_group(trade: dict[str, Any]) -> Optional[str]:
    for name in _realtime_trade_names(trade):
        for group in REALTIME_STATS_GROUP_OPTIONS:
            if group["key"] == "all":
                continue
            if _realtime_name_matches_group(name, group["key"]):
                return group["key"]
    return None

def _new_realtime_card_state() -> dict[str, Any]:
    return {
        "count": 0,
        "profit_count": 0,
        "profit_value": 0.0,
        "loss_count": 0,
        "loss_value": 0.0,
        "net_value": 0.0,
        "bucket_counts": [0] * 12,
    }

def _register_realtime_metric(state: dict[str, Any], metric_value: float, event_dt: datetime, window_mins: int, now_dt: datetime) -> None:
    state["count"] += 1
    state["net_value"] += metric_value
    if metric_value >= 0:
        state["profit_count"] += 1
        state["profit_value"] += metric_value
    else:
        state["loss_count"] += 1
        state["loss_value"] += metric_value
    age_sec = max(0.0, (now_dt - event_dt).total_seconds())
    bucket_span = max(1.0, (window_mins * 60.0) / 12.0)
    bucket_idx = min(11, int(age_sec // bucket_span))
    state["bucket_counts"][11 - bucket_idx] += 1

def _finalize_realtime_card(state: dict[str, Any]) -> dict[str, Any]:
    count = int(state.get("count", 0) or 0)
    loss_abs = abs(float(state.get("loss_value", 0.0) or 0.0))
    profit_value = float(state.get("profit_value", 0.0) or 0.0)
    if count:
        win_rate = round((int(state.get("profit_count", 0) or 0) / count) * 100.0)
    else:
        win_rate = 0
    if loss_abs > 0:
        delta_pct = round((profit_value / loss_abs) * 100.0 - 100.0, 1)
    elif profit_value > 0:
        delta_pct = 100.0
    else:
        delta_pct = 0.0
    return {
        "count": count,
        "profit_count": int(state.get("profit_count", 0) or 0),
        "profit_value": round(profit_value, 2),
        "loss_count": int(state.get("loss_count", 0) or 0),
        "loss_value": round(float(state.get("loss_value", 0.0) or 0.0), 2),
        "net_value": round(float(state.get("net_value", 0.0) or 0.0), 2),
        "win_rate": win_rate,
        "delta_pct": delta_pct,
        "spark": list(state.get("bucket_counts", [0] * 12)),
    }

def _merge_finalized_realtime_cards(cards: list[dict[str, Any]]) -> dict[str, Any]:
    aggregate = {
        "count": 0,
        "profit_count": 0,
        "profit_value": 0.0,
        "loss_count": 0,
        "loss_value": 0.0,
        "net_value": 0.0,
        "bucket_counts": [0] * 12,
    }
    for card in cards:
        if not isinstance(card, dict):
            continue
        aggregate["count"] += int(card.get("count", 0) or 0)
        aggregate["profit_count"] += int(card.get("profit_count", 0) or 0)
        aggregate["profit_value"] += float(card.get("profit_value", 0.0) or 0.0)
        aggregate["loss_count"] += int(card.get("loss_count", 0) or 0)
        aggregate["loss_value"] += float(card.get("loss_value", 0.0) or 0.0)
        aggregate["net_value"] += float(card.get("net_value", 0.0) or 0.0)
        spark = list(card.get("spark", []))
        for idx in range(min(12, len(spark))):
            aggregate["bucket_counts"][idx] += int(spark[idx] or 0)
    return _finalize_realtime_card(aggregate)

def _build_empty_realtime_payload(group_key: str, product_key: str) -> dict[str, Any]:
    return {
        "last_update": datetime.now().isoformat(),
        "selected_group": group_key,
        "selected_product": product_key,
        "products": [],
        "windows": REALTIME_STATS_WINDOWS,
        "rows": [],
        "summary": {},
        "proximity": 0.8,
    }

def _combine_realtime_group_payloads(cache_payload: dict[str, Any], selected_product: str) -> dict[str, Any]:
    product_key = str(selected_product or "").strip().upper()
    concrete_groups = [group["key"] for group in REALTIME_STATS_GROUP_OPTIONS if group["key"] != "all"]
    payloads_root = cache_payload.get("payloads") or {}
    group_payloads: list[dict[str, Any]] = []
    all_products: set[str] = set()

    for group_key in concrete_groups:
        per_group = payloads_root.get(group_key, {})
        candidate = per_group.get(product_key) if product_key else per_group.get("__all__")
        if candidate is None and product_key:
            candidate = per_group.get("__all__")
        if not isinstance(candidate, dict):
            continue
        group_payloads.append(candidate)
        all_products.update(candidate.get("products", []) or [])

    if not group_payloads:
        return _build_empty_realtime_payload("all", product_key)

    rows_payload = []
    for row_key, row_def in REALTIME_STATS_ROW_DEFS.items():
        cards = {}
        for window in REALTIME_STATS_WINDOWS:
            cards[window["key"]] = _merge_finalized_realtime_cards([
                ((payload.get("rows") or [])[idx].get("cards", {}).get(window["key"], {}))
                for payload in group_payloads
                for idx, row in enumerate(payload.get("rows") or [])
                if row.get("key") == row_key
            ])
        rows_payload.append({
            "key": row_key,
            "title": row_def["title"],
            "accent": row_def["accent"],
            "icon": row_def["icon"],
            "tag": row_def["tag"],
            "cards": cards,
        })

    summary_payload = {}
    for window in REALTIME_STATS_WINDOWS:
        summary_payload[window["key"]] = _merge_finalized_realtime_cards([
            (payload.get("summary", {}) or {}).get(window["key"], {})
            for payload in group_payloads
        ])

    last_update = max(
        [str(payload.get("last_update") or "") for payload in group_payloads],
        default=datetime.now().isoformat(),
    )
    return {
        "last_update": last_update,
        "selected_group": "all",
        "selected_product": product_key,
        "products": sorted(all_products),
        "windows": REALTIME_STATS_WINDOWS,
        "rows": rows_payload,
        "summary": summary_payload,
        "proximity": 0.8,
    }

def _build_realtime_stats_cache(now_dt: Optional[datetime] = None) -> dict[str, Any]:
    now_dt = now_dt or datetime.now()
    cfg = _load_config_safe()
    product_types = cfg.get("product_types", ["forex", "crypto", "energy", "indices", "metals"])
    today_str = now_dt.strftime("%Y-%m-%d")
    yesterday_str = (now_dt - timedelta(days=1)).strftime("%Y-%m-%d")
    all_product_key = "__all__"
    scanned_trade_keys: set[str] = set()

    raw_rows: dict[str, dict[str, dict[str, dict[str, Any]]]] = {}
    raw_summary: dict[str, dict[str, dict[str, Any]]] = {}
    products_seen: dict[str, set[str]] = {group["key"]: set() for group in REALTIME_STATS_GROUP_OPTIONS}

    def ensure_product_bucket(group_key: str, product_key: str) -> None:
        raw_rows.setdefault(group_key, {})
        raw_summary.setdefault(group_key, {})
        if product_key not in raw_rows[group_key]:
            raw_rows[group_key][product_key] = {
                row_key: {window["key"]: _new_realtime_card_state() for window in REALTIME_STATS_WINDOWS}
                for row_key in REALTIME_STATS_ROW_DEFS
            }
        if product_key not in raw_summary[group_key]:
            raw_summary[group_key][product_key] = {
                window["key"]: _new_realtime_card_state() for window in REALTIME_STATS_WINDOWS
            }

    for group in REALTIME_STATS_GROUP_OPTIONS:
        ensure_product_bucket(group["key"], all_product_key)

    for date_str in [yesterday_str, today_str]:
        for pt in product_types:
            for ddir in _iter_day_dirs_for("live", date_str, pt):
                trades_summary_file = ddir / "_trades_summary.json"
                if not trades_summary_file.exists():
                    continue
                try:
                    with open(trades_summary_file, "r", encoding="utf-8") as f:
                        trades_summary_data = json.load(f)
                    trades_iter = trades_summary_data.get("trades", []) or []
                except Exception:
                    continue

                for trade in trades_iter:
                    trade_key = "|".join([
                        str(trade.get("trade_id") or ""),
                        str(trade.get("filename") or ""),
                        str(trade.get("status") or ""),
                        str(trade.get("entry_time") or trade.get("exit_time") or ""),
                    ])
                    if trade_key in scanned_trade_keys:
                        continue
                    scanned_trade_keys.add(trade_key)

                    group_key = _classify_realtime_strategy_group(trade)
                    if not group_key:
                        continue

                    product = str(trade.get("product") or "").strip().upper()
                    if product:
                        products_seen[group_key].add(product)
                        ensure_product_bucket(group_key, product)

                    entry_dt = _parse_iso_ts(trade.get("entry_time") or trade.get("in_trade_entry_time"))
                    exit_dt = _parse_iso_ts(trade.get("exit_time"))
                    status = str(trade.get("status", "") or trade.get("trade_status", "")).upper()
                    direction = str(trade.get("direction", "")).upper()
                    metric_value = float(trade.get("net_return", 0.0) or 0.0)

                    for window in REALTIME_STATS_WINDOWS:
                        minutes = int(window["minutes"])
                        cutoff_seconds = minutes * 60
                        row_key = None
                        event_dt = None

                        if status == "OPEN" and direction == "LONG" and entry_dt:
                            age_sec = (now_dt - entry_dt).total_seconds()
                            if 0 <= age_sec <= cutoff_seconds:
                                row_key = "open_buy"
                                event_dt = entry_dt
                        elif status == "OPEN" and direction == "SHORT" and entry_dt:
                            age_sec = (now_dt - entry_dt).total_seconds()
                            if 0 <= age_sec <= cutoff_seconds:
                                row_key = "open_sell"
                                event_dt = entry_dt
                        elif status == "CLOSED" and direction == "LONG" and exit_dt:
                            age_sec = (now_dt - exit_dt).total_seconds()
                            if 0 <= age_sec <= cutoff_seconds:
                                row_key = "closed_buy"
                                event_dt = exit_dt
                        elif status == "CLOSED" and direction == "SHORT" and exit_dt:
                            age_sec = (now_dt - exit_dt).total_seconds()
                            if 0 <= age_sec <= cutoff_seconds:
                                row_key = "closed_sell"
                                event_dt = exit_dt

                        if not row_key or not event_dt:
                            continue

                        for product_key in [all_product_key] + ([product] if product else []):
                            ensure_product_bucket(group_key, product_key)
                            _register_realtime_metric(raw_rows[group_key][product_key][row_key][window["key"]], metric_value, event_dt, minutes, now_dt)
                            _register_realtime_metric(raw_summary[group_key][product_key][window["key"]], metric_value, event_dt, minutes, now_dt)

    payloads: dict[str, dict[str, Any]] = {}
    for group in REALTIME_STATS_GROUP_OPTIONS:
        group_key = group["key"]
        payloads[group_key] = {}
        available_products = sorted(products_seen.get(group_key, set()))
        for product_key in raw_rows.get(group_key, {}):
            rows_payload = []
            for row_key, row_def in REALTIME_STATS_ROW_DEFS.items():
                rows_payload.append({
                    "key": row_key,
                    "title": row_def["title"],
                    "accent": row_def["accent"],
                    "icon": row_def["icon"],
                    "tag": row_def["tag"],
                    "cards": {
                        window["key"]: _finalize_realtime_card(raw_rows[group_key][product_key][row_key][window["key"]])
                        for window in REALTIME_STATS_WINDOWS
                    },
                })
            summary_payload = {
                window["key"]: _finalize_realtime_card(raw_summary[group_key][product_key][window["key"]])
                for window in REALTIME_STATS_WINDOWS
            }
            payloads[group_key][product_key] = {
                "last_update": now_dt.isoformat(),
                "selected_group": group_key,
                "selected_product": "" if product_key == all_product_key else product_key,
                "products": available_products,
                "windows": REALTIME_STATS_WINDOWS,
                "rows": rows_payload,
                "summary": summary_payload,
                "proximity": 0.8,
            }

    return {
        "generated_at": now_dt.isoformat(),
        "strategy_groups": REALTIME_STATS_GROUP_OPTIONS,
        "payloads": payloads,
    }

def _load_realtime_stats_cache() -> dict[str, Any]:
    global REALTIME_STATS_CACHE_MEMORY, REALTIME_STATS_CACHE_MEMORY_MTIME
    if not REALTIME_STATS_CACHE_FILE.exists():
        return {}
    try:
        mtime = REALTIME_STATS_CACHE_FILE.stat().st_mtime
        if REALTIME_STATS_CACHE_MEMORY and REALTIME_STATS_CACHE_MEMORY_MTIME == mtime:
            return REALTIME_STATS_CACHE_MEMORY
        with open(REALTIME_STATS_CACHE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f) or {}
        if isinstance(data, dict):
            REALTIME_STATS_CACHE_MEMORY = data
            REALTIME_STATS_CACHE_MEMORY_MTIME = mtime
            return data
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}

def _realtime_snapshot_key(dt: Optional[datetime] = None) -> str:
    dt = dt or datetime.now()
    bucket_minute = (dt.minute // 5) * 5
    bucket = dt.replace(minute=bucket_minute, second=0, microsecond=0)
    return bucket.isoformat()

def _realtime_snapshot_file(snapshot_at: str) -> Path:
    safe_name = re.sub(r"[^0-9A-Za-z_.-]+", "_", str(snapshot_at or "latest"))
    return REALTIME_STATS_SNAPSHOT_DIR / f"{safe_name}.json"

def _load_realtime_snapshot_file(snapshot_at: str) -> Optional[dict[str, Any]]:
    path = _realtime_snapshot_file(snapshot_at)
    if not path.exists():
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f) or {}
        return data if isinstance(data, dict) else None
    except Exception:
        return None

def _load_realtime_stats_snapshots() -> dict[str, Any]:
    if not REALTIME_STATS_SNAPSHOTS_FILE.exists():
        return {"version": 1, "snapshots": []}
    try:
        with open(REALTIME_STATS_SNAPSHOTS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f) or {}
        if not isinstance(data, dict):
            return {"version": 1, "snapshots": []}
        snapshots = data.get("snapshots")
        if not isinstance(snapshots, list):
            data["snapshots"] = []
        data.setdefault("version", 1)
        return data
    except Exception:
        return {"version": 1, "snapshots": []}

def _snapshot_meta(snapshot: dict[str, Any]) -> dict[str, Any]:
    return {
        "snapshot_at": snapshot.get("snapshot_at"),
        "generated_at": snapshot.get("generated_at"),
        "path": snapshot.get("path"),
    }

def _load_realtime_snapshot_index_file() -> list[dict[str, Any]]:
    global REALTIME_STATS_SNAPSHOT_INDEX_MEMORY, REALTIME_STATS_SNAPSHOT_INDEX_MEMORY_MTIME
    if not REALTIME_STATS_SNAPSHOT_INDEX_FILE.exists():
        return []
    try:
        mtime = REALTIME_STATS_SNAPSHOT_INDEX_FILE.stat().st_mtime
        if REALTIME_STATS_SNAPSHOT_INDEX_MEMORY and REALTIME_STATS_SNAPSHOT_INDEX_MEMORY_MTIME == mtime:
            return REALTIME_STATS_SNAPSHOT_INDEX_MEMORY
        with open(REALTIME_STATS_SNAPSHOT_INDEX_FILE, "r", encoding="utf-8") as f:
            data = json.load(f) or {}
        snapshots = data.get("snapshots", []) if isinstance(data, dict) else []
        if not isinstance(snapshots, list):
            return []
        index = [
            _snapshot_meta(item)
            for item in snapshots
            if isinstance(item, dict) and item.get("snapshot_at")
        ]
        REALTIME_STATS_SNAPSHOT_INDEX_MEMORY = index
        REALTIME_STATS_SNAPSHOT_INDEX_MEMORY_MTIME = mtime
        return index
    except Exception:
        return []

def _write_realtime_snapshot_index_file(snapshots: list[dict[str, Any]]) -> None:
    global REALTIME_STATS_SNAPSHOT_INDEX_MEMORY, REALTIME_STATS_SNAPSHOT_INDEX_MEMORY_MTIME
    index_payload = {
        "version": 1,
        "updated_at": datetime.now().isoformat(),
        "snapshot_seconds": REALTIME_STATS_SNAPSHOT_SECONDS,
        "max_snapshots": REALTIME_STATS_MAX_SNAPSHOTS,
        "snapshots": [_snapshot_meta(item) for item in snapshots if isinstance(item, dict) and item.get("snapshot_at")],
    }
    _atomic_write_json(REALTIME_STATS_SNAPSHOT_INDEX_FILE, index_payload, indent=2)
    REALTIME_STATS_SNAPSHOT_INDEX_MEMORY = index_payload["snapshots"]
    try:
        REALTIME_STATS_SNAPSHOT_INDEX_MEMORY_MTIME = REALTIME_STATS_SNAPSHOT_INDEX_FILE.stat().st_mtime
    except Exception:
        REALTIME_STATS_SNAPSHOT_INDEX_MEMORY_MTIME = None

def _realtime_snapshot_index(store: Optional[dict[str, Any]] = None) -> list[dict[str, Any]]:
    if store is None:
        index = _load_realtime_snapshot_index_file()
        if index:
            index.sort(key=lambda item: str(item.get("snapshot_at") or ""))
            return index
    store = store or _load_realtime_stats_snapshots()
    snapshots = [
        item for item in (store.get("snapshots") or [])
        if isinstance(item, dict) and item.get("snapshot_at")
    ]
    snapshots.sort(key=lambda item: str(item.get("snapshot_at") or ""))
    return [_snapshot_meta(item) for item in snapshots]

def _record_realtime_stats_snapshot(cache_payload: dict[str, Any]) -> None:
    if not isinstance(cache_payload, dict) or not cache_payload.get("payloads"):
        return
    snapshot_at = _realtime_snapshot_key(_parse_local_iso_ts(cache_payload.get("generated_at")) or datetime.now())
    index = _realtime_snapshot_index()
    if index and str(index[-1].get("snapshot_at")) == snapshot_at and _load_realtime_snapshot_file(snapshot_at):
        return

    snapshot = {
        "snapshot_at": snapshot_at,
        "generated_at": cache_payload.get("generated_at") or datetime.now().isoformat(),
        "strategy_groups": cache_payload.get("strategy_groups", REALTIME_STATS_GROUP_OPTIONS),
        "payloads": cache_payload.get("payloads", {}),
    }
    snapshot_path = _realtime_snapshot_file(snapshot_at)
    _atomic_write_json(snapshot_path, snapshot, indent=2)

    snapshots = [
        item for item in index
        if isinstance(item, dict) and item.get("snapshot_at") and str(item.get("snapshot_at")) != snapshot_at
    ]
    snapshots.append({
        "snapshot_at": snapshot_at,
        "generated_at": snapshot["generated_at"],
        "path": str(snapshot_path),
    })
    snapshots.sort(key=lambda item: str(item.get("snapshot_at") or ""))
    if len(snapshots) > REALTIME_STATS_MAX_SNAPSHOTS:
        expired = snapshots[:-REALTIME_STATS_MAX_SNAPSHOTS]
        snapshots = snapshots[-REALTIME_STATS_MAX_SNAPSHOTS:]
        for item in expired:
            old_path = _realtime_snapshot_file(str(item.get("snapshot_at") or ""))
            try:
                old_path.unlink(missing_ok=True)
            except Exception:
                pass
    _write_realtime_snapshot_index_file(snapshots)

def _snapshot_cache_payload(snapshot: dict[str, Any]) -> dict[str, Any]:
    return {
        "generated_at": snapshot.get("generated_at") or snapshot.get("snapshot_at") or datetime.now().isoformat(),
        "strategy_groups": snapshot.get("strategy_groups", REALTIME_STATS_GROUP_OPTIONS),
        "payloads": snapshot.get("payloads", {}),
    }

def _find_realtime_stats_snapshot(snapshot_at: str) -> tuple[Optional[dict[str, Any]], list[dict[str, Any]]]:
    index = _realtime_snapshot_index()
    if index:
        target_meta = None
        if snapshot_at:
            target_meta = next((item for item in index if str(item.get("snapshot_at")) == str(snapshot_at)), None)
        if target_meta is None:
            target_meta = index[-1]
        snapshot = _load_realtime_snapshot_file(str(target_meta.get("snapshot_at") or ""))
        if snapshot:
            return snapshot, index

    # Backward compatibility for snapshots created before per-snapshot files.
    store = _load_realtime_stats_snapshots()
    snapshots = [
        item for item in (store.get("snapshots") or [])
        if isinstance(item, dict) and item.get("snapshot_at")
    ]
    snapshots.sort(key=lambda item: str(item.get("snapshot_at") or ""))
    if not snapshots:
        return None, []
    if not snapshot_at:
        return snapshots[-1], [_snapshot_meta(item) for item in snapshots]
    exact = next((item for item in snapshots if str(item.get("snapshot_at")) == str(snapshot_at)), None)
    if exact:
        return exact, [_snapshot_meta(item) for item in snapshots]
    return snapshots[-1], [_snapshot_meta(item) for item in snapshots]

def _payload_from_cache_payload(
    cache_payload: dict[str, Any],
    selected_group: str,
    selected_product: str,
) -> dict[str, Any]:
    group_key = selected_group if selected_group in REALTIME_STATS_GROUP_MAP else "momentum"
    product_key = str(selected_product or "").strip().upper()
    if group_key == "all":
        payload = _combine_realtime_group_payloads(cache_payload, product_key)
        payload = dict(payload)
        payload["selected_group"] = "all"
        payload["selected_product"] = product_key
        payload["strategy_groups"] = cache_payload.get("strategy_groups", REALTIME_STATS_GROUP_OPTIONS)
        return payload

    group_payloads = (cache_payload.get("payloads") or {}).get(group_key, {})
    payload = group_payloads.get(product_key) if product_key else group_payloads.get("__all__")
    if payload is None and product_key:
        payload = group_payloads.get("__all__")
    if payload is None:
        payload = _build_empty_realtime_payload(group_key, product_key)
    payload = dict(payload)
    payload["selected_group"] = group_key
    payload["selected_product"] = product_key
    payload["strategy_groups"] = cache_payload.get("strategy_groups", REALTIME_STATS_GROUP_OPTIONS)
    return payload

def _refresh_realtime_stats_cache(force: bool = False) -> dict[str, Any]:
    global REALTIME_STATS_CACHE_MEMORY, REALTIME_STATS_CACHE_MEMORY_MTIME
    with REALTIME_STATS_CACHE_LOCK:
        current = _load_realtime_stats_cache()
        if not force and not _realtime_stats_cache_is_stale(current):
            return current
        rebuilt = _build_realtime_stats_cache()
        _atomic_write_json(REALTIME_STATS_CACHE_FILE, rebuilt, indent=2)
        REALTIME_STATS_CACHE_MEMORY = rebuilt
        try:
            REALTIME_STATS_CACHE_MEMORY_MTIME = REALTIME_STATS_CACHE_FILE.stat().st_mtime
        except Exception:
            REALTIME_STATS_CACHE_MEMORY_MTIME = None
        _record_realtime_stats_snapshot(rebuilt)
        return rebuilt

def _trigger_realtime_stats_cache_refresh(force: bool = False) -> None:
    with REALTIME_STATS_REFRESH_TRIGGER_LOCK:
        if REALTIME_STATS_REFRESH_STATE.get("running"):
            return
        REALTIME_STATS_REFRESH_STATE["running"] = True
        REALTIME_STATS_REFRESH_STATE["last_started_at"] = datetime.now().isoformat()
        REALTIME_STATS_REFRESH_STATE["last_error"] = ""

    def worker() -> None:
        try:
            _refresh_realtime_stats_cache(force=force)
        except Exception as exc:
            with REALTIME_STATS_REFRESH_TRIGGER_LOCK:
                REALTIME_STATS_REFRESH_STATE["last_error"] = str(exc)
        finally:
            with REALTIME_STATS_REFRESH_TRIGGER_LOCK:
                REALTIME_STATS_REFRESH_STATE["running"] = False
                REALTIME_STATS_REFRESH_STATE["last_finished_at"] = datetime.now().isoformat()

    threading.Thread(target=worker, daemon=True).start()

def _realtime_cache_meta(cache_payload: dict[str, Any], status: str) -> dict[str, Any]:
    generated_at = _parse_local_iso_ts(cache_payload.get("generated_at")) if isinstance(cache_payload, dict) else None
    with REALTIME_STATS_REFRESH_TRIGGER_LOCK:
        refresh_running = bool(REALTIME_STATS_REFRESH_STATE.get("running"))
        refresh_last_error = str(REALTIME_STATS_REFRESH_STATE.get("last_error") or "")
    return {
        "cache_status": status,
        "cache_generated_at": cache_payload.get("generated_at") if isinstance(cache_payload, dict) else None,
        "cache_age_seconds": round((datetime.now() - generated_at).total_seconds(), 1) if generated_at else None,
        "cache_refresh_running": refresh_running,
        "cache_refresh_error": refresh_last_error,
    }

def _get_realtime_stats_payload(
    selected_group: str,
    selected_product: str,
    snapshot_at: str = "",
    force_refresh: bool = False,
) -> dict[str, Any]:
    if snapshot_at and snapshot_at != "latest":
        snapshot, snapshot_index = _find_realtime_stats_snapshot(snapshot_at)
        if snapshot:
            payload = _payload_from_cache_payload(_snapshot_cache_payload(snapshot), selected_group, selected_product)
            payload["snapshot_mode"] = "historical"
            payload["snapshot_at"] = snapshot.get("snapshot_at")
            payload["snapshots"] = snapshot_index
            return payload

    cache_payload = _load_realtime_stats_cache()
    cache_status = "fresh"
    if force_refresh:
        cache_payload = _refresh_realtime_stats_cache(force=True)
        cache_status = "forced_refresh"
    elif _realtime_stats_cache_is_stale(cache_payload):
        cache_status = "stale_refreshing"
        if isinstance(cache_payload, dict) and cache_payload.get("payloads"):
            _trigger_realtime_stats_cache_refresh(force=True)
        else:
            cache_status = "rebuilt"
            # No usable cache exists yet; block once so the dashboard has data.
            cache_payload = _refresh_realtime_stats_cache(force=True)
    if not isinstance(cache_payload, dict) or not cache_payload.get("payloads"):
        cache_payload = _refresh_realtime_stats_cache(force=True)
        cache_status = "rebuilt"

    payload = _payload_from_cache_payload(cache_payload, selected_group, selected_product)
    payload["snapshot_mode"] = "latest"
    payload["snapshot_at"] = _realtime_snapshot_key(_parse_local_iso_ts(cache_payload.get("generated_at")) or datetime.now())
    payload["snapshots"] = _realtime_snapshot_index()
    payload.update(_realtime_cache_meta(cache_payload, cache_status))
    return payload

def _normalize_execution_mode(value: Any, default: str = "semi_automatic") -> str:
    mode = str(value or default).strip().lower().replace("-", "_")
    return mode if mode in {"automatic", "semi_automatic", "manual"} else default

def _realtime_row_map(rows: list[dict[str, Any]] | None) -> dict[str, dict[str, Any]]:
    return {
        str(row.get("key")): row
        for row in (rows or [])
        if isinstance(row, dict) and row.get("key")
    }

def _realtime_window_preference(payload: dict[str, Any], row_map: dict[str, dict[str, Any]]) -> str:
    available = {str(window.get("key")) for window in (payload.get("windows") or []) if isinstance(window, dict)}
    candidates = [key for key in ["h3", "h1", "m30", "m5"] if key in available]
    buy_row = row_map.get("open_buy") or {}
    sell_row = row_map.get("open_sell") or {}
    for key in candidates:
        buy_count = int(((buy_row.get("cards") or {}).get(key, {}) or {}).get("count", 0) or 0)
        sell_count = int(((sell_row.get("cards") or {}).get(key, {}) or {}).get("count", 0) or 0)
        if buy_count >= REALTIME_TRADE_SIGNAL_MIN_COUNT and sell_count >= REALTIME_TRADE_SIGNAL_MIN_COUNT:
            return key
    for key in candidates:
        buy_count = int(((buy_row.get("cards") or {}).get(key, {}) or {}).get("count", 0) or 0)
        sell_count = int(((sell_row.get("cards") or {}).get(key, {}) or {}).get("count", 0) or 0)
        if buy_count > 0 or sell_count > 0:
            return key
    return candidates[0] if candidates else "m30"

def _realtime_window_label(payload: dict[str, Any], window_key: str) -> str:
    for window in (payload.get("windows") or []):
        if isinstance(window, dict) and str(window.get("key")) == window_key:
            return str(window.get("label") or window_key)
    return window_key

def _realtime_default_entry_price(product: str) -> float:
    upper = str(product or "").upper()
    if "JPY" in upper:
        return 156.42
    if "XAU" in upper:
        return 2325.4
    if "BTC" in upper:
        return 64250.0
    return 1.2345

def _realtime_pip_size(product: str) -> float:
    return 0.01 if "JPY" in str(product or "").upper() else 0.0001

def _realtime_price_digits(product: str) -> int:
    return 4 if _realtime_pip_size(product) < 0.001 else 2

def _safe_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except Exception:
        return default

def _derive_realtime_trade_action(payload: dict[str, Any]) -> dict[str, Any]:
    row_map = _realtime_row_map(payload.get("rows") or [])
    window_key = _realtime_window_preference(payload, row_map)
    open_buy = ((row_map.get("open_buy") or {}).get("cards") or {}).get(window_key, {}) or {}
    open_sell = ((row_map.get("open_sell") or {}).get("cards") or {}).get(window_key, {}) or {}
    now_iso = str(payload.get("last_update") or payload.get("snapshot_at") or datetime.now().isoformat())
    generated_at = _parse_local_iso_ts(now_iso)
    age_seconds = round(max(0.0, (datetime.now() - generated_at).total_seconds()), 0) if generated_at else None
    stale = age_seconds is not None and age_seconds > REALTIME_TRADE_SIGNAL_STALE_SECONDS
    has_single_product = bool(str(payload.get("selected_product") or "").strip())
    buy_count = int(open_buy.get("count", 0) or 0)
    sell_count = int(open_sell.get("count", 0) or 0)
    buy_profit_count = int(open_buy.get("profit_count", 0) or 0)
    buy_loss_count = int(open_buy.get("loss_count", 0) or 0)
    sell_profit_count = int(open_sell.get("profit_count", 0) or 0)
    sell_loss_count = int(open_sell.get("loss_count", 0) or 0)
    buy_profit_rate = (buy_profit_count / buy_count) if buy_count > 0 else 0.0
    buy_loss_rate = (buy_loss_count / buy_count) if buy_count > 0 else 0.0
    sell_profit_rate = (sell_profit_count / sell_count) if sell_count > 0 else 0.0
    sell_loss_rate = (sell_loss_count / sell_count) if sell_count > 0 else 0.0
    buy_bias_score = buy_profit_rate + sell_loss_rate
    sell_bias_score = sell_profit_rate + buy_loss_rate
    buy_signal = (
        buy_count > 0
        and sell_count > 0
        and buy_profit_rate >= 0.75
        and sell_loss_rate >= 0.75
    )
    sell_signal = (
        sell_count > 0
        and buy_count > 0
        and sell_profit_rate >= 0.75
        and buy_loss_rate >= 0.75
    )
    action = "NO TRADE"
    bias_score = max(buy_bias_score, sell_bias_score)
    if has_single_product and not stale and buy_count >= REALTIME_TRADE_SIGNAL_MIN_COUNT and sell_count >= REALTIME_TRADE_SIGNAL_MIN_COUNT:
        if buy_signal and not sell_signal and buy_bias_score >= 1.5:
            action = "BUY"
            bias_score = buy_bias_score
        elif sell_signal and not buy_signal and sell_bias_score >= 1.5:
            action = "SELL"
            bias_score = sell_bias_score
    bias_strength = "High" if bias_score >= 1.8 else "Medium" if bias_score >= 1.5 else "Low"
    direction_bias = "NEUTRAL" if buy_bias_score == sell_bias_score else ("BUY" if buy_bias_score > sell_bias_score else "SELL")
    product = str(payload.get("selected_product") or "").strip().upper() or "All Products"
    entry_price = round(_realtime_default_entry_price(product), _realtime_price_digits(product))
    pip_size = _realtime_pip_size(product)
    cost_pips = REALTIME_TRADE_EXECUTION_DEFAULT_COST_PIPS
    break_even_price = (
        entry_price - (cost_pips * pip_size)
        if action == "SELL"
        else entry_price + (cost_pips * pip_size)
    )
    executable = has_single_product and action != "NO TRADE"
    reasons = [
        f"Open Buy Win Rate: {buy_profit_rate * 100:.1f}% ({buy_profit_count} / {buy_count})",
        f"Open Sell Loss Rate: {sell_loss_rate * 100:.1f}% ({sell_loss_count} / {sell_count})",
        f"Buy Profit Value: ${_safe_float(open_buy.get('profit_value', 0.0), 0.0):,.2f}",
        f"Sell Loss Value: ${_safe_float(open_sell.get('loss_value', 0.0), 0.0):,.2f}",
        f"Direction Bias: {direction_bias}",
    ]
    if not has_single_product:
        reasons.append("Execution requires a single selected product.")
    if buy_count < REALTIME_TRADE_SIGNAL_MIN_COUNT or sell_count < REALTIME_TRADE_SIGNAL_MIN_COUNT:
        reasons.append(f"Minimum open trade threshold not met for {_realtime_window_label(payload, window_key)}.")
    if stale:
        reasons.append(f"Snapshot is stale ({int(age_seconds or 0)}s old).")
    if action == "NO TRADE" and has_single_product and not stale and buy_count >= REALTIME_TRADE_SIGNAL_MIN_COUNT and sell_count >= REALTIME_TRADE_SIGNAL_MIN_COUNT:
        reasons.append(f"Bias strength is {bias_strength.lower()} or directional signals are mixed.")

    ticket = None
    if executable:
        ticket = {
            "product": product,
            "direction": action,
            "entry_price": entry_price,
            "time": now_iso,
            "cost_pips": cost_pips,
            "break_even_price": round(break_even_price, _realtime_price_digits(product)),
            "price_digits": _realtime_price_digits(product),
            "note": "Realtime stats ticket uses snapshot-derived direction and app-local placeholder live pricing.",
        }

    return {
        "action": action,
        "product": product,
        "has_single_product": has_single_product,
        "executable": executable,
        "window_key": window_key,
        "window_label": _realtime_window_label(payload, window_key),
        "bias_strength": bias_strength,
        "bias_score": round(bias_score, 3),
        "direction_bias": direction_bias,
        "reasons": reasons,
        "entry_price": entry_price,
        "pip_size": pip_size,
        "price_digits": _realtime_price_digits(product),
        "cost_pips": cost_pips,
        "break_even_price": round(break_even_price, _realtime_price_digits(product)),
        "generated_at": now_iso,
        "snapshot_age_seconds": int(age_seconds) if age_seconds is not None else None,
        "snapshot_mode": payload.get("snapshot_mode") or "latest",
        "snapshot_at": payload.get("snapshot_at") or "",
        "minimum_count": REALTIME_TRADE_SIGNAL_MIN_COUNT,
        "stale": stale,
        "ticket": ticket,
    }

def _empty_realtime_trade_execution_store() -> dict[str, Any]:
    return {
        "version": 1,
        "updated_at": datetime.now().isoformat(),
        "trades": [],
        "decisions": [],
    }

def _load_realtime_trade_execution_store() -> dict[str, Any]:
    if not REALTIME_TRADE_EXECUTION_STORE_FILE.exists():
        return _empty_realtime_trade_execution_store()
    try:
        with open(REALTIME_TRADE_EXECUTION_STORE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f) or {}
        if not isinstance(data, dict):
            return _empty_realtime_trade_execution_store()
        if not isinstance(data.get("trades"), list):
            data["trades"] = []
        if not isinstance(data.get("decisions"), list):
            data["decisions"] = []
        data.setdefault("version", 1)
        data.setdefault("updated_at", datetime.now().isoformat())
        return data
    except Exception:
        return _empty_realtime_trade_execution_store()

def _save_realtime_trade_execution_store(store: dict[str, Any]) -> None:
    store["updated_at"] = datetime.now().isoformat()
    _atomic_write_json(REALTIME_TRADE_EXECUTION_STORE_FILE, store, indent=2)

def _compute_trade_net_pips(direction: str, entry_price: float, exit_price: float, pip_size: float, cost_pips: float) -> float:
    if pip_size <= 0:
        return 0.0
    raw_pips = ((exit_price - entry_price) / pip_size) if direction == "BUY" else ((entry_price - exit_price) / pip_size)
    return round(raw_pips - cost_pips, 1)

def _resolve_realtime_exit_quote(product: str, direction: str) -> Optional[dict[str, float]]:
    try:
        quotes = breakout_common.fetch_latest_quotes(str(product or "").upper())
        if not quotes:
            return None
        latest = quotes[-1]
        fallback_price = _safe_float(getattr(latest, "price", None), 0.0)
        bid = _safe_float(getattr(latest, "bid", None), fallback_price)
        ask = _safe_float(getattr(latest, "ask", None), fallback_price)
        close_direction = str(direction or "").upper()
        if close_direction == "BUY":
            exit_price = bid or fallback_price or ask
        else:
            exit_price = ask or fallback_price or bid
        if not exit_price:
            return None
        return {
            "exit_price": float(exit_price),
            "bid": float(bid or exit_price),
            "ask": float(ask or exit_price),
            "price": float(fallback_price or exit_price),
        }
    except Exception:
        return None

def _current_trade_net_pips_from_quote(trade: dict[str, Any], quote: dict[str, float]) -> float:
    product = str(trade.get("product") or "")
    return _compute_trade_net_pips(
        str(trade.get("direction") or "BUY").upper(),
        _safe_float(trade.get("entry_price"), 0.0),
        _safe_float(quote.get("exit_price"), 0.0),
        _safe_float(trade.get("pip_size"), _realtime_pip_size(product)),
        _safe_float(trade.get("cost_pips"), REALTIME_TRADE_EXECUTION_DEFAULT_COST_PIPS),
    )

def _policy_can_close_from_action(trade: dict[str, Any], action_model: dict[str, Any], policy_cfg: dict[str, Any]) -> tuple[bool, str]:
    action = str(action_model.get("action") or "NO TRADE").upper()
    direction = str(trade.get("direction") or "").upper()
    if not direction or direction not in {"BUY", "SELL"}:
        return False, "unsupported_direction"
    if bool(policy_cfg.get("ignore_stale_snapshot", True)) and bool(action_model.get("stale")):
        return False, "stale_snapshot"
    if bool(policy_cfg.get("require_executable_signal", True)) and not bool(action_model.get("executable")):
        return False, "signal_not_executable"
    if bool(policy_cfg.get("ignore_no_trade", True)) and action == "NO TRADE":
        return False, "no_trade_signal"
    if direction == "BUY" and action == "SELL":
        return True, "opposite_signal"
    if direction == "SELL" and action == "BUY":
        return True, "opposite_signal"
    if action == direction:
        return False, "same_direction"
    return False, "mixed_signal"

def _evaluate_trade_close_policy_matches(trade: dict[str, Any], action_model: dict[str, Any], close_cfg: dict[str, Any]) -> list[dict[str, Any]]:
    matches: list[dict[str, Any]] = []
    if not bool(close_cfg.get("enabled", True)):
        return matches
    enabled_policies = list(close_cfg.get("enabled_policies") or [])
    policy_map = close_cfg.get("policies") or {}
    resolved_quote: Optional[dict[str, float]] = None
    for policy_name in enabled_policies:
        if policy_name not in REALTIME_TRADE_CLOSE_AVAILABLE_POLICIES:
            continue
        policy_cfg = policy_map.get(policy_name) or {}
        if not bool(policy_cfg.get("enabled", True)):
            continue
        if policy_name == "opposite_signal":
            should_close, reason = _policy_can_close_from_action(trade, action_model, policy_cfg)
            if should_close:
                matches.append({
                    "policy": policy_name,
                    "reason": reason,
                    "signal_action": str(action_model.get("action") or "NO TRADE").upper(),
                    "signal_snapshot_at": action_model.get("snapshot_at") or "",
                    "signal_window_key": action_model.get("window_key") or "",
                    "signal_window_label": action_model.get("window_label") or "",
                })
        if policy_name == "net_pips_after_cost_threshold":
            if resolved_quote is None:
                resolved_quote = _resolve_realtime_exit_quote(str(trade.get("product") or ""), str(trade.get("direction") or "").upper())
            if not resolved_quote:
                continue
            threshold_pips = _safe_float(policy_cfg.get("threshold_pips"), 5.0)
            current_net_pips = _current_trade_net_pips_from_quote(trade, resolved_quote)
            if current_net_pips > threshold_pips:
                matches.append({
                    "policy": policy_name,
                    "reason": "net_pips_after_cost_threshold",
                    "threshold_pips": threshold_pips,
                    "current_net_pips": current_net_pips,
                    "signal_snapshot_at": action_model.get("snapshot_at") or "",
                })
    return matches

def _close_trade_record(
    trade: dict[str, Any],
    exit_price: float,
    exit_time: Optional[str] = None,
    close_reason: str = "manual",
    close_policy_matches: Optional[list[dict[str, Any]]] = None,
    close_note: str = "",
) -> None:
    resolved_exit_time = str(exit_time or datetime.now().isoformat())
    product = str(trade.get("product") or "")
    trade["exit_price"] = round(float(exit_price), _realtime_price_digits(product))
    trade["exit_time"] = resolved_exit_time
    trade["status"] = "CLOSED"
    trade["updated_at"] = datetime.now().isoformat()
    trade["close_reason"] = close_reason
    trade["close_policy_matches"] = list(close_policy_matches or [])
    if close_note:
        trade["close_note"] = close_note
    trade["net_pips"] = _compute_trade_net_pips(
        str(trade.get("direction") or "BUY").upper(),
        _safe_float(trade.get("entry_price"), 0.0),
        _safe_float(trade.get("exit_price"), 0.0),
        _safe_float(trade.get("pip_size"), _realtime_pip_size(product)),
        _safe_float(trade.get("cost_pips"), REALTIME_TRADE_EXECUTION_DEFAULT_COST_PIPS),
    )

def _evaluate_realtime_trade_closures(
    selected_group: str,
    selected_product: str,
    action_model: dict[str, Any],
    trigger: str = "realtime_stats",
) -> list[dict[str, Any]]:
    product = str(selected_product or "").strip().upper()
    if not product:
        return []
    close_cfg = _load_realtime_trade_close_config()
    if trigger == "realtime_stats" and not bool(close_cfg.get("evaluate_on_realtime_stats", True)):
        return []
    if trigger == "trade_log" and not bool(close_cfg.get("evaluate_on_trade_log", True)):
        return []
    if not bool(close_cfg.get("enabled", True)):
        return []

    closed_events: list[dict[str, Any]] = []
    with REALTIME_TRADE_EXECUTION_LOCK:
        store = _load_realtime_trade_execution_store()
        trades = store.get("trades") or []
        dirty = False
        for trade in trades:
            if not isinstance(trade, dict):
                continue
            if str(trade.get("status") or "").upper() != "OPEN":
                continue
            if str(trade.get("product") or "").strip().upper() != product:
                continue
            matches = _evaluate_trade_close_policy_matches(trade, action_model, close_cfg)
            if not matches:
                continue
            quote = _resolve_realtime_exit_quote(product, str(trade.get("direction") or "").upper())
            if not quote:
                continue
            matched_policies = [str(match.get("policy") or "") for match in matches if match.get("policy")]
            close_reason = matched_policies[0] if len(matched_policies) == 1 else "multi_policy_close"
            close_note = f"Closed by {', '.join(matched_policies)} on {trigger}."
            _close_trade_record(
                trade,
                exit_price=float(quote["exit_price"]),
                close_reason=close_reason,
                close_policy_matches=matches,
                close_note=close_note,
            )
            closed_events.append({
                "trade_id": trade.get("id"),
                "product": product,
                "direction": trade.get("direction"),
                "close_reason": trade.get("close_reason"),
                "close_policy_matches": matches,
                "exit_price": trade.get("exit_price"),
            })
            dirty = True
        if dirty:
            _save_realtime_trade_execution_store(store)
    return closed_events

def _sorted_realtime_trades(trades: list[dict[str, Any]]) -> list[dict[str, Any]]:
    def sort_key(trade: dict[str, Any]) -> datetime:
        return _parse_local_iso_ts(trade.get("entry_time")) or _parse_local_iso_ts(trade.get("created_at")) or datetime.min
    return sorted([trade for trade in trades if isinstance(trade, dict)], key=sort_key, reverse=True)

def _filter_realtime_trade_log(trades: list[dict[str, Any]], trade_filter: str) -> list[dict[str, Any]]:
    mode = str(trade_filter or "all").strip().lower()
    if mode == "open":
        return [trade for trade in trades if str(trade.get("status") or "").upper() == "OPEN"]
    if mode == "closed":
        return [trade for trade in trades if str(trade.get("status") or "").upper() == "CLOSED"]
    if mode in {"manual", "semi_automatic", "automatic"}:
        return [trade for trade in trades if str(trade.get("execution_mode") or "").lower() == mode]
    return trades

def _summarize_realtime_trade_log(trades: list[dict[str, Any]]) -> dict[str, Any]:
    closed = [trade for trade in trades if str(trade.get("status") or "").upper() == "CLOSED"]
    total_trades = len(closed)
    winning_trades = len([trade for trade in closed if _safe_float(trade.get("net_pips"), 0.0) > 0])
    total_net_pips = round(sum(_safe_float(trade.get("net_pips"), 0.0) for trade in closed), 1)
    total_cost_pips = round(sum(_safe_float(trade.get("cost_pips"), 0.0) for trade in closed), 1)
    return {
        "total_trades": total_trades,
        "win_rate": round((winning_trades / total_trades) * 100.0) if total_trades else 0,
        "total_net_pips": total_net_pips,
        "average_net_pips": round(total_net_pips / total_trades, 1) if total_trades else 0.0,
        "total_cost_pips": total_cost_pips,
        "open_trades": len([trade for trade in trades if str(trade.get("status") or "").upper() == "OPEN"]),
    }

def _build_realtime_trade_log_view(payload: dict[str, Any], trade_filter: str = "all") -> tuple[list[dict[str, Any]], dict[str, Any]]:
    store = _load_realtime_trade_execution_store()
    selected_product = str(payload.get("selected_product") or "").strip().upper()
    trades = _sorted_realtime_trades(store.get("trades") or [])
    if selected_product:
        trades = [trade for trade in trades if str(trade.get("product") or "").strip().upper() == selected_product]
    trades = _filter_realtime_trade_log(trades, trade_filter)
    return trades, _summarize_realtime_trade_log(trades)

def _attach_realtime_execution_payload(payload: dict[str, Any], trade_filter: str = "all", evaluate_close_trigger: str = "realtime_stats") -> dict[str, Any]:
    trade_action = _derive_realtime_trade_action(payload)
    closed_events = _evaluate_realtime_trade_closures(
        str(payload.get("selected_group") or "momentum").strip().lower(),
        str(payload.get("selected_product") or "").strip().upper(),
        trade_action,
        trigger=evaluate_close_trigger,
    )
    trade_log, trade_log_summary = _build_realtime_trade_log_view(payload, trade_filter=trade_filter)
    close_cfg = _load_realtime_trade_close_config()
    payload["trade_action"] = trade_action
    payload["trade_ticket"] = trade_action.get("ticket")
    payload["trade_log"] = trade_log
    payload["trade_log_summary"] = trade_log_summary
    payload["execution_state"] = {
        "default_mode": "semi_automatic",
        "available_modes": ["automatic", "semi_automatic", "manual"],
        "auto_trade_enabled": False,
        "auto_trade_status": "disabled",
        "auto_trade_note": "Full automatic execution remains disabled pending semi-automatic validation.",
        "trade_log_filter": str(trade_filter or "all").strip().lower() or "all",
        "trade_close_config": close_cfg,
        "trade_close_available_policies": list(REALTIME_TRADE_CLOSE_AVAILABLE_POLICIES),
        "trade_close_last_events": closed_events,
    }
    return payload

def _realtime_trade_payload_response(
    selected_group: str,
    selected_product: str,
    snapshot_at: str = "",
    evaluate_close_trigger: str = "realtime_stats",
) -> dict[str, Any]:
    payload = _get_realtime_stats_payload(selected_group, selected_product, snapshot_at=snapshot_at)
    return _attach_realtime_execution_payload(payload, evaluate_close_trigger=evaluate_close_trigger)

def _record_realtime_trade_decision(
    store: dict[str, Any],
    decision: str,
    selected_group: str,
    selected_product: str,
    action_model: dict[str, Any],
    note: str = "",
) -> None:
    store.setdefault("decisions", [])
    store["decisions"].insert(0, {
        "decision_id": f"decision_{uuid.uuid4().hex[:12]}",
        "decision": decision,
        "created_at": datetime.now().isoformat(),
        "strategy_group": selected_group,
        "product": selected_product or action_model.get("product") or "",
        "action": action_model.get("action") or "NO TRADE",
        "snapshot_at": action_model.get("snapshot_at") or "",
        "window_key": action_model.get("window_key") or "",
        "window_label": action_model.get("window_label") or "",
        "bias_strength": action_model.get("bias_strength") or "",
        "bias_score": action_model.get("bias_score") or 0,
        "note": note,
    })
    store["decisions"] = store["decisions"][:500]

@app.route("/api/trades/log")
def get_trade_log():
    try:
        selected_product = str(request.args.get("product", "") or "").strip().upper()
        selected_group = str(request.args.get("strategy_group", "momentum") or "momentum").strip().lower()
        snapshot_at = str(request.args.get("snapshot", "") or "").strip()
        trade_filter = str(request.args.get("filter", "all") or "all").strip().lower()
        payload = _realtime_trade_payload_response(
            selected_group,
            selected_product,
            snapshot_at=snapshot_at,
            evaluate_close_trigger="trade_log",
        )
        trades = _filter_realtime_trade_log(list(payload.get("trade_log") or []), trade_filter)
        return jsonify({
            "success": True,
            "strategy_group": selected_group,
            "product": selected_product,
            "filter": trade_filter,
            "trades": trades,
            "summary": _summarize_realtime_trade_log(trades),
            "trade_action": payload.get("trade_action") or {},
        })
    except Exception as e:
        return jsonify({"success": False, "message": str(e), "trades": [], "summary": {}}), 500

@app.route("/api/trades/evaluate_close_signals", methods=["POST"])
def evaluate_trade_close_signals():
    try:
        data = request.get_json(silent=True) or {}
        selected_product = str(data.get("product", "") or "").strip().upper()
        selected_group = str(data.get("strategy_group", "momentum") or "momentum").strip().lower()
        snapshot_at = str(data.get("snapshot", "") or "").strip()
        payload = _realtime_trade_payload_response(
            selected_group,
            selected_product,
            snapshot_at=snapshot_at,
            evaluate_close_trigger="manual_eval",
        )
        return jsonify({
            "success": True,
            "message": "Trade close signals evaluated.",
            "closed_events": ((payload.get("execution_state") or {}).get("trade_close_last_events") or []),
            "payload": payload,
        })
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route("/api/trades/accept", methods=["POST"])
def accept_trade_suggestion():
    try:
        data = request.get_json(silent=True) or {}
        selected_product = str(data.get("product", "") or "").strip().upper()
        selected_group = str(data.get("strategy_group", "momentum") or "momentum").strip().lower()
        snapshot_at = str(data.get("snapshot", "") or "").strip()
        payload = _realtime_trade_payload_response(selected_group, selected_product, snapshot_at=snapshot_at)
        action_model = payload.get("trade_action") or {}
        if not action_model.get("executable"):
            return jsonify({"success": False, "message": "No executable trade suggestion is available for the selected product."}), 400

        execution_mode = _normalize_execution_mode(data.get("execution_mode"), "semi_automatic")
        entry_price = round(_safe_float(data.get("entry_price"), _safe_float(action_model.get("entry_price"), 0.0)), int(action_model.get("price_digits") or 4))
        product = str(action_model.get("product") or selected_product).strip().upper()
        direction = str(action_model.get("action") or "").upper()
        note = str(data.get("note") or f"Accepted {direction} suggestion from realtime stats.").strip()

        with REALTIME_TRADE_EXECUTION_LOCK:
            store = _load_realtime_trade_execution_store()
            existing_open = next((
                trade for trade in (store.get("trades") or [])
                if str(trade.get("product") or "").strip().upper() == product
                and str(trade.get("direction") or "").upper() == direction
                and str(trade.get("status") or "").upper() == "OPEN"
            ), None)
            if existing_open:
                return jsonify({"success": False, "message": f"An open {direction} trade already exists for {product}.", "trade": existing_open}), 409

            trade = {
                "id": f"trade_{uuid.uuid4().hex[:12]}",
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "entry_time": datetime.now().isoformat(),
                "exit_time": "",
                "direction": direction,
                "product": product,
                "entry_price": entry_price,
                "exit_price": None,
                "pip_size": _safe_float(action_model.get("pip_size"), _realtime_pip_size(product)),
                "cost_pips": _safe_float(action_model.get("cost_pips"), REALTIME_TRADE_EXECUTION_DEFAULT_COST_PIPS),
                "net_pips": 0.0,
                "status": "OPEN",
                "execution_mode": execution_mode,
                "strategy_group": selected_group,
                "snapshot_at": action_model.get("snapshot_at") or payload.get("snapshot_at") or "",
                "window_key": action_model.get("window_key") or "",
                "window_label": action_model.get("window_label") or "",
                "bias_strength": action_model.get("bias_strength") or "",
                "bias_score": action_model.get("bias_score") or 0,
                "reasoning": list(action_model.get("reasons") or []),
                "note": note,
                "source": "realtime_stats_accept",
            }
            store.setdefault("trades", [])
            store["trades"].insert(0, trade)
            _record_realtime_trade_decision(store, "accept", selected_group, product, action_model, note=note)
            _save_realtime_trade_execution_store(store)

        return jsonify({"success": True, "message": f"{direction} trade accepted for {product}.", "trade": trade, "payload": _realtime_trade_payload_response(selected_group, product, snapshot_at=snapshot_at)})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route("/api/trades/manual", methods=["POST"])
def create_manual_trade():
    try:
        data = request.get_json(silent=True) or {}
        selected_product = str(data.get("product", "") or "").strip().upper()
        if not selected_product:
            return jsonify({"success": False, "message": "Manual trades require a single product."}), 400
        direction = str(data.get("direction", "") or "").strip().upper()
        if direction not in {"BUY", "SELL"}:
            return jsonify({"success": False, "message": "Manual trades require direction BUY or SELL."}), 400
        selected_group = str(data.get("strategy_group", "momentum") or "momentum").strip().lower()
        snapshot_at = str(data.get("snapshot", "") or "").strip()
        payload = _realtime_trade_payload_response(selected_group, selected_product, snapshot_at=snapshot_at)
        action_model = payload.get("trade_action") or {}
        pip_size = _realtime_pip_size(selected_product)
        entry_price = round(_safe_float(data.get("entry_price"), _realtime_default_entry_price(selected_product)), _realtime_price_digits(selected_product))
        note = str(data.get("note") or "Manual trade opened from realtime stats panel.").strip()

        with REALTIME_TRADE_EXECUTION_LOCK:
            store = _load_realtime_trade_execution_store()
            trade = {
                "id": f"trade_{uuid.uuid4().hex[:12]}",
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "entry_time": datetime.now().isoformat(),
                "exit_time": "",
                "direction": direction,
                "product": selected_product,
                "entry_price": entry_price,
                "exit_price": None,
                "pip_size": pip_size,
                "cost_pips": REALTIME_TRADE_EXECUTION_DEFAULT_COST_PIPS,
                "net_pips": 0.0,
                "status": "OPEN",
                "execution_mode": "manual",
                "strategy_group": selected_group,
                "snapshot_at": payload.get("snapshot_at") or "",
                "window_key": action_model.get("window_key") or "",
                "window_label": action_model.get("window_label") or "",
                "bias_strength": action_model.get("bias_strength") or "",
                "bias_score": action_model.get("bias_score") or 0,
                "reasoning": list(action_model.get("reasons") or []),
                "note": note,
                "source": "realtime_stats_manual",
            }
            store.setdefault("trades", [])
            store["trades"].insert(0, trade)
            _record_realtime_trade_decision(store, "manual", selected_group, selected_product, action_model, note=note)
            _save_realtime_trade_execution_store(store)

        return jsonify({"success": True, "message": f"Manual {direction} trade created for {selected_product}.", "trade": trade, "payload": _realtime_trade_payload_response(selected_group, selected_product, snapshot_at=snapshot_at)})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route("/api/trades/reject", methods=["POST"])
def reject_trade_suggestion():
    try:
        data = request.get_json(silent=True) or {}
        selected_product = str(data.get("product", "") or "").strip().upper()
        selected_group = str(data.get("strategy_group", "momentum") or "momentum").strip().lower()
        snapshot_at = str(data.get("snapshot", "") or "").strip()
        payload = _realtime_trade_payload_response(selected_group, selected_product, snapshot_at=snapshot_at)
        action_model = payload.get("trade_action") or {}
        note = str(data.get("note") or f"Rejected {action_model.get('action') or 'NO TRADE'} suggestion from realtime stats.").strip()
        with REALTIME_TRADE_EXECUTION_LOCK:
            store = _load_realtime_trade_execution_store()
            _record_realtime_trade_decision(store, "reject", selected_group, selected_product, action_model, note=note)
            _save_realtime_trade_execution_store(store)
        return jsonify({"success": True, "message": note, "payload": _realtime_trade_payload_response(selected_group, selected_product, snapshot_at=snapshot_at)})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route("/api/trades/close", methods=["POST"])
def close_trade():
    try:
        data = request.get_json(silent=True) or {}
        trade_id = str(data.get("trade_id", "") or "").strip()
        if not trade_id:
            return jsonify({"success": False, "message": "trade_id is required."}), 400
        exit_price = data.get("exit_price")
        if exit_price in (None, ""):
            return jsonify({"success": False, "message": "exit_price is required to close a trade."}), 400
        selected_group = str(data.get("strategy_group", "momentum") or "momentum").strip().lower()
        snapshot_at = str(data.get("snapshot", "") or "").strip()
        with REALTIME_TRADE_EXECUTION_LOCK:
            store = _load_realtime_trade_execution_store()
            trade = next((item for item in (store.get("trades") or []) if str(item.get("id") or "") == trade_id), None)
            if not trade:
                return jsonify({"success": False, "message": f"Trade {trade_id} was not found."}), 404
            if str(trade.get("status") or "").upper() == "CLOSED":
                return jsonify({"success": False, "message": f"Trade {trade_id} is already closed.", "trade": trade}), 409
            resolved_exit_price = round(_safe_float(exit_price, 0.0), _realtime_price_digits(str(trade.get("product") or "")))
            _close_trade_record(
                trade,
                exit_price=resolved_exit_price,
                exit_time=str(data.get("exit_time") or datetime.now().isoformat()),
                close_reason=str(data.get("close_reason") or "manual"),
                close_policy_matches=[],
                close_note=str(data.get("close_note") or "Trade closed via manual close endpoint.").strip(),
            )
            _save_realtime_trade_execution_store(store)

        product = str(trade.get("product") or "").strip().upper()
        return jsonify({"success": True, "message": f"Trade {trade_id} closed.", "trade": trade, "payload": _realtime_trade_payload_response(selected_group, product, snapshot_at=snapshot_at)})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/api/bias_history', methods=['POST'])
def log_bias_history():
    """Log bias history entry every 5 minutes [V20260209_1335]"""
    try:
        data = request.json or {}
        mode = str(data.get('run_mode', 'live')).lower()
        timestamp = data.get('timestamp') or datetime.now(timezone.utc).isoformat()
        ts_dt = _parse_iso_ts(timestamp) or datetime.now(timezone.utc)
        date_str = ts_dt.strftime('%Y-%m-%d')
        reset_session = bool(data.get('reset_session', False))
        session_start = data.get('session_start')

        history_data = _load_bias_history_safe(mode, date_str)
        sessions = _load_bias_sessions_safe()
        if mode not in sessions:
            sessions[mode] = {"session_start": timestamp}
        if session_start:
            sessions[mode]["session_start"] = session_start
        if reset_session:
            sessions[mode]["session_start"] = timestamp
            history_data["history"] = [
                h for h in history_data.get("history", [])
                if str(h.get("run_mode", "live")).lower() != mode
            ]

        # Create history entry
        history_entry = {
            "timestamp": timestamp,
            "bias": data.get('bias'),
            "market_condition": data.get('market_condition'),
            "status": data.get('status'),
            "recent_buy_pnl": data.get('recent_buy_pnl'),
            "recent_sell_pnl": data.get('recent_sell_pnl'),
            "recent_buy_count": data.get('recent_buy_count'),
            "recent_sell_count": data.get('recent_sell_count'),
            "run_mode": mode
        }
        
        # Append to history
        history_data["history"].insert(0, history_entry)  # Most recent first
        
        # Keep only last 500 entries (covers ~41 hours at 5min intervals)
        history_data["history"] = history_data["history"][:500]
        
        # Save
        _atomic_write_json(_get_bias_history_file(mode, date_str), history_data, indent=2)
        _save_bias_sessions(sessions)
        
        return jsonify({
            "success": True,
            "message": "Bias history logged",
            "session_start": sessions.get(mode, {}).get("session_start"),
            "run_mode": mode
        })
    
    except Exception as e:
        print(f"[BIAS-HISTORY-ERROR] {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/bias_history', methods=['GET'])
def get_bias_history():
    """Retrieve bias history [V20260209_1335]"""
    try:
        mode = request.args.get('mode', 'live')
        date_str = request.args.get('date') or datetime.now().strftime('%Y-%m-%d')
        history_data = _load_bias_history_safe(str(mode).lower(), date_str)
        sessions = _load_bias_sessions_safe()
        
        # Optional filtering
        limit = request.args.get('limit', type=int, default=100)
        since_session = request.args.get('since_session', 'false').lower() in ('1', 'true', 'yes', 'on')
        
        history = history_data.get("history", [])
        
        session_start = None
        start_dt = None

        if mode:
            mode_l = str(mode).lower()
            history = [h for h in history if str(h.get('run_mode', 'live')).lower() == mode_l]
            if since_session:
                session_start = (sessions.get(mode_l) or {}).get("session_start")
                start_dt = _parse_iso_ts(session_start)
                if start_dt:
                    history = [h for h in history if (_parse_iso_ts(h.get("timestamp")) or datetime.min.replace(tzinfo=timezone.utc)) >= start_dt]
        
        # Compute flip summary in chronological order.
        chrono = sorted(history, key=lambda h: _parse_iso_ts(h.get("timestamp")) or datetime.min.replace(tzinfo=timezone.utc))
        start_bias = chrono[0].get("bias") if chrono else None
        first_flip_at = None
        flip_count = 0
        if chrono:
            prev_bias = str(chrono[0].get("bias") or "").upper()
            for h in chrono[1:]:
                b = str(h.get("bias") or "").upper()
                if b and prev_bias and b != prev_bias:
                    flip_count += 1
                    if first_flip_at is None:
                        first_flip_at = h.get("timestamp")
                    prev_bias = b

        history = history[:limit]
        
        return jsonify({
            "success": True,
            "history": history,
            "session_start": session_start if mode else None,
            "since_session": since_session,
            "start_bias": start_bias,
            "first_flip_at": first_flip_at,
            "flip_count": flip_count
        })
    
    except Exception as e:
        print(f"[BIAS-HISTORY-ERROR] {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/bias_audit', methods=['GET'])
def bias_audit():
    """Audit current open trades against latest targeted bias."""
    try:
        mode = str(request.args.get('mode', 'live')).lower()
        date_str = request.args.get('date') or datetime.now().strftime('%Y-%m-%d')
        bias = _get_current_bias(mode, date_str)
        if not bias:
            return jsonify({"success": False, "message": "No current bias available", "mode": mode, "date": date_str}), 404
        day_dirs = _iter_day_dirs_for(mode, date_str)
        if not day_dirs:
            return jsonify({"success": True, "mode": mode, "date": date_str, "bias": bias, "open_count": 0, "mismatch_count": 0, "mismatches": []})
        mismatches = []
        open_count = 0
        for day_dir in day_dirs:
            for fp in day_dir.glob('*_op.json'):
                try:
                    with open(fp, 'r') as f:
                        d = json.load(f) or {}
                except Exception:
                    continue
                if str(d.get('status', '')).upper() != 'OPEN':
                    continue
                if not bool(d.get('is_live_trade') or d.get('order_sent_net') or d.get('order_sent_alt')):
                    continue
                open_count += 1
                direction = str(d.get('direction') or '').upper()
                aligned = ((bias == 'BUY' and direction == 'LONG') or (bias == 'SELL' and direction == 'SHORT'))
                if not aligned:
                    mismatches.append({
                        "file": fp.name,
                        "entry_time": d.get("entry_time"),
                        "strategy": d.get("script_name") or d.get("source_strategy"),
                        "product": d.get("product"),
                        "direction": direction,
                        "market_bias_latest": d.get("market_bias_latest"),
                        "market_bias_at_open": d.get("market_bias_at_open")
                    })
        return jsonify({
            "success": True,
            "mode": mode,
            "date": date_str,
            "bias": bias,
            "open_count": open_count,
            "mismatch_count": len(mismatches),
            "mismatches": mismatches
        })
    except Exception as e:
        print(f"[BIAS-AUDIT-ERROR] {e}")
        return jsonify({"success": False, "error": str(e)}), 500


# [V20260209_1900] Bias-Aligned Strategy Switching - Smart Target Activation
@app.route('/api/smart_target/activate', methods=['POST'])
def smart_target_activate():
    """Activate a strategy in grid_live.json with bias tagging"""
    try:
        data = request.json
        strategy = data.get('strategy')
        product = data.get('product')
        metric = data.get('metric', 'buy_net')  # 'buy_net' or 'sell_net'
        mode = data.get('mode', 'live')
        bias = data.get('bias')  # NEW: BUY or SELL
        
        if not strategy or not product:
            return jsonify({"success": False, "error": "Strategy and product required"}), 400

        # [V20260215_0002] Gate Smart Target automation by config allowlist.
        if not _is_source_allowed('AI Target'):
            print("[SMART-TARGET] REJECTED: 'AI Target' is not enabled in automated_trade_sources.")
            return jsonify({"success": True, "message": "Skipped (Source Overrule)"})
        
        # Load grid_live.json
        grid_file = Path('grid_live.json')
        if grid_file.exists():
            with open(grid_file, 'r') as f:
                grid_data = json.load(f)
        else:
            grid_data = {"live": [], "sim": []}
        
        # Determine which list to update
        target_list = grid_data.get(mode, [])
        
        # Check if already exists [V20260210_1223]
        # Fix: keys in grid_live are 'model' and 'product', not 'strategy'
        existing = next((item for item in target_list 
                        if item.get('model') == strategy and item.get('product') == product), None)
        
        if existing:
            # Update existing entry
            existing['metric'] = metric
            existing['activated_for_bias'] = bias  # [V20260209_1900] Tag with bias
            existing['activated_at'] = datetime.now().isoformat()
            existing['source'] = 'ai_target' # Ensure source is set
        else:
            # Add new entry [V20260210_1223] Correct structure
            target_list.append({
                "model": strategy,
                "product": product,
                "metric": metric,
                "source": "ai_target",
                "manual": False,
                "group": product, # Default group to product
                "activated_for_bias": bias, 
                "activated_at": datetime.now().isoformat()
            })
        
        grid_data[mode] = target_list
        
        # Save grid_live.json
        with open(grid_file, 'w') as f:
            json.dump(grid_data, f, indent=2)
            
        # [V20260210_1645] Sync with activations (Activation Explorer)
        _sync_grid_to_activations(target_list, mode=mode)
        
        print(f"[SMART-TARGET] Activated {strategy} on {product} ({metric}) for {bias} bias")
        return jsonify({"success": True, "message": f"Activated {strategy} on {product}"})
    
    except Exception as e:
        print(f"[SMART-TARGET-ERROR] {e}")
        return jsonify({"success": False, "error": str(e)}), 500


# [V20260209_1900] Deactivate strategies with opposite bias
@app.route('/api/deactivate_wrong_bias', methods=['POST'])
def deactivate_wrong_bias():
    """Deactivate all strategies that don't match the current bias"""
    try:
        data = request.json
        current_bias = data.get('current_bias')  # 'BUY' or 'SELL'
        mode = data.get('mode', 'live')
        
        if not current_bias:
            return jsonify({"success": False, "error": "current_bias required"}), 400
            
        # [V20260210_0400] 2026-02-10 04:20 - Archive existing state before deactivating
        _archive_grid_live(mode, force=True)
        opposite_bias = 'SELL' if current_bias == 'BUY' else 'BUY'
        
        # Load grid_live.json
        grid_file = Path('grid_live.json')
        if not grid_file.exists():
            return jsonify({"success": True, "deactivated": 0, "message": "No grid_live.json found"})
        
        with open(grid_file, 'r') as f:
            grid_data = json.load(f)
        
        target_list = grid_data.get(mode, [])
        deactivated_count = 0
        deactivated_strategies = []
        
        # [V20260210_0400] 2026-02-10 04:20 - Find and deactivate/remove opposite-bias strategies
        new_list = []
        for item in target_list:
            if item.get('activated_for_bias') == opposite_bias:
                if item.get('source') == 'ai_target':
                    # REMOVE AI-targeted strategies to enforce "Switching"
                    deactivated_count += 1
                    deactivated_strategies.append(f"REMOVED: {item.get('model', item.get('strategy'))} on {item.get('product')}") # [V20260210_1236] Fix: use 'model' key
                    continue 
                else:
                    # Deactivate regular activations
                    item['buy'] = False
                    item['sell'] = False
                    item['deactivated_at'] = datetime.now().isoformat()
                    item['deactivation_reason'] = f"Bias changed to {current_bias}"
                    deactivated_count += 1
                    deactivated_strategies.append(f"DISABLED: {item.get('model', item.get('strategy'))} on {item.get('product')}") # [V20260210_1236] Fix: use 'model' key
            
            new_list.append(item)
        
        grid_data[mode] = new_list
        
        # Save updated grid_live.json
        with open(grid_file, 'w') as f:
            json.dump(grid_data, f, indent=4)
            
        # [V20260210_1645] Sync with activations (Activation Explorer)
        _sync_grid_to_activations(new_list, mode=mode)
        
        print(f"[DEACTIVATE-WRONG-BIAS] Deactivated {deactivated_count} {opposite_bias}-bias strategies")
        for strat in deactivated_strategies:
            print(f"  - {strat}")
        
        return jsonify({
            "success": True,
            "deactivated": deactivated_count,
            "strategies": deactivated_strategies,
            "message": f"Deactivated {deactivated_count} {opposite_bias}-bias strategies"
        })
    
    except Exception as e:
        print(f"[DEACTIVATE-WRONG-BIAS-ERROR] {e}")
        return jsonify({"success": False, "error": str(e)}), 500


def _start_market_update_worker():
    def worker():
        time.sleep(10)  # wait for startup
        while True:
            try:
                # Always generate for live. The generator internally determines the latest date
                generate_market_update("live")
            except Exception as e:
                print(f"[MarketUpdateWorker] Error generating update: {e}")
            time.sleep(300)
    t = threading.Thread(target=worker, daemon=True)
    t.start()

def _start_realtime_stats_cache_worker() -> None:
    def worker():
        time.sleep(12)
        while True:
            try:
                _refresh_realtime_stats_cache(force=True)
            except Exception as e:
                print(f"[RealtimeStatsCacheWorker] Error refreshing cache: {e}")
            time.sleep(REALTIME_STATS_CACHE_REFRESH_SECONDS)
    t = threading.Thread(target=worker, daemon=True)
    t.start()


# [V20260325_1745] API for Weekly Performance Dashboard
@app.route("/api/weekly_performance")
def get_weekly_performance():
    product_type = request.args.get("product_type", "forex").lower()
    target_date = request.args.get("target_date")  # Expected YYYY-MM-DD
    force_refresh = str(request.args.get("force_refresh", "")).strip().lower() in {"1", "true", "yes"}

    if not target_date:
        target_date = datetime.now().strftime("%Y-%m-%d")

    try:
        requested_date = datetime.strptime(target_date, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"error": f"Invalid target_date '{target_date}'. Expected YYYY-MM-DD."}), 400

    from tools.aggregate_top_strategies import aggregate_for_product_type, get_week_bounds

    week_start, week_end = get_week_bounds(target_date)
    week_start_str = week_start.strftime("%Y-%m-%d")
    week_end_str = week_end.strftime("%Y-%m-%d")

    stats_dir = Path(r"C:\Users\edebe\eds\TradeApps\breakout\fs\json\live") / product_type / "stats" / "weekly"
    stats_dir.mkdir(parents=True, exist_ok=True)
    # Cache weekly aggregates by aligned week-start date so all requests
    # inside the same week resolve to the same artifact.
    stats_file = stats_dir / f"{week_start_str}.json"

    should_refresh = force_refresh or _weekly_stats_artifact_is_stale(
        stats_file=stats_file,
        product_type=product_type,
        week_start=week_start,
        week_end=week_end,
        source_filename="_trades_summary.json",
    )

    if should_refresh:
        try:
            aggregate_for_product_type(
                product_type,
                target_date=week_start_str,
                output_file=stats_file,
            )
        except Exception as e:
            print(f"Error generating weekly stats: {e}")

    if not stats_file.exists():
        return jsonify({"error": f"Stats file not found for aligned week {week_start_str} to {week_end_str}"}), 404

    try:
        with open(stats_file, "r") as f:
            data = json.load(f)
        data["requested_target_date"] = target_date
        data["week_start"] = data.get("week_start", week_start_str)
        data["week_end"] = data.get("week_end", week_end_str)
        data["date_range"] = [data["week_start"], data["week_end"]]
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/weekly_summary_net_30min")
def get_weekly_summary_net_30min():
    product_type = request.args.get("product_type", "forex").lower()
    target_date = request.args.get("target_date")
    force_refresh = str(request.args.get("force_refresh", "")).strip().lower() in {"1", "true", "yes"}

    if not target_date:
        target_date = datetime.now().strftime("%Y-%m-%d")

    try:
        requested_date = datetime.strptime(target_date, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"error": f"Invalid target_date '{target_date}'. Expected YYYY-MM-DD."}), 400

    from tools.aggregate_top_strategies import (
        aggregate_summary_net_30min_for_product_type,
        get_week_bounds,
    )

    week_start, week_end = get_week_bounds(target_date)
    week_start_str = week_start.strftime("%Y-%m-%d")
    week_end_str = week_end.strftime("%Y-%m-%d")

    stats_dir = Path(r"C:\Users\edebe\eds\TradeApps\breakout\fs\json\live") / product_type / "stats" / "weekly"
    stats_dir.mkdir(parents=True, exist_ok=True)
    stats_file = stats_dir / f"{week_start_str}_summary_net_30m.json"

    should_refresh = force_refresh or _weekly_stats_artifact_is_stale(
        stats_file=stats_file,
        product_type=product_type,
        week_start=week_start,
        week_end=week_end,
        source_filename="_summary_net.json",
    )

    if should_refresh:
        try:
            aggregate_summary_net_30min_for_product_type(
                product_type,
                target_date=week_start_str,
                output_file=stats_file,
            )
        except Exception as e:
            print(f"Error generating weekly summary net 30m stats: {e}")

    if not stats_file.exists():
        return jsonify({"error": f"Stats file not found for aligned week {week_start_str} to {week_end_str}"}), 404

    try:
        with open(stats_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        data["requested_target_date"] = target_date
        data["week_start"] = data.get("week_start", week_start_str)
        data["week_end"] = data.get("week_end", week_end_str)
        data["date_range"] = [data["week_start"], data["week_end"]]
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/realtime_stats")
def get_realtime_stats():
    # [V20260428_1735] Cached strategy-group dashboard payload for the Real-Time Stats mockup.
    try:
        selected_product = str(request.args.get("product", "") or "").strip().upper()
        selected_group = str(request.args.get("strategy_group", "momentum") or "momentum").strip().lower()
        snapshot_at = str(request.args.get("snapshot", "") or "").strip()
        force_refresh = str(request.args.get("force_refresh", "") or "").strip().lower() in ("1", "true", "yes")
        trade_filter = str(request.args.get("trade_filter", "all") or "all").strip().lower()
        payload = _get_realtime_stats_payload(
            selected_group,
            selected_product,
            snapshot_at=snapshot_at,
            force_refresh=force_refresh,
        )
        payload = _attach_realtime_execution_payload(payload, trade_filter=trade_filter)
        payload["success"] = True
        payload["filter"] = "strategy_group"
        return jsonify(payload)
    except Exception as e:
        return jsonify({"success": False, "message": str(e), "rows": [], "summary": {}}), 500

if __name__ == "__main__":
    print("Trade Viewer API V1315 (activation v2)")
    try:
        # Avoid double-start in Flask reloader
        if os.environ.get("WERKZEUG_RUN_MAIN") == "true" or not app.debug:
            _start_open_trade_refresh_worker()
            _start_grid_auto_worker()
            _start_market_update_worker()
            _start_realtime_stats_cache_worker()
            print("[GRID-AUTO] Background workers started")
    except Exception as e:
        print(f"[GRID-AUTO] Failed to start worker: {e}")
    app.run(host="0.0.0.0", port=5000, debug=False, threaded=True, use_reloader=False)
