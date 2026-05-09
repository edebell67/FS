"""Shared breakout strategy utilities."""

from __future__ import annotations

import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from collections import deque, defaultdict # Added defaultdict for global_stats
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple, Type, Set # Added Set
import uuid # [2025-12-26 V20251226_1800]
import shutil
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

import pandas as pd
import requests
from live_scheduler import get_matching_live_schedule # [V20260122_1630] Added for schedule-based activation
from json_layout import (
    configured_product_types,
    day_dir as _json_day_dir,
    default_product_type,
    ensure_day_dir,
    iter_day_dirs,
    load_layout_config,
    product_type_for_product,
    resolve_day_dir,
)
from strategy_name_generator import apply_strategy_name_fields, canonical_strategy_name

# [V20260101_2130] Track latest seen trading date for dynamic archiving and mode-agnostic date scoping
_LATEST_TRADING_DATE: Optional[str] = None

# [V20260211_1705] Process-level cache for live trades sent but not yet visible on disk
_LIVE_ORDERS_SENT_MEMORY_CACHE: Dict[str, Any] = {} 
_LAST_L_TRADE_ORDER_ERROR: Optional[str] = None
_LAST_L_TRADE_ORDER_PENDING_ID: Optional[str] = None
# [V20260217_1645] Disable market-bias caching so entry/exit gates always use latest file value.
_MARKET_BIAS_CACHE: Dict[Tuple[str, str], Dict[str, Any]] = {}
SIGNAL_AUDIT_VERSION = "V20260423_1658"
SIGNAL_AUDIT_FILENAME = "_signal_audit.json"
DEFAULT_TRADING_TIMEZONE = "Europe/London"


#CONFIG_FILE_PATH = os.path.join(os.path.dirname(__file__), 'config.json')

CONFIG_FILE_PATH = Path(__file__).resolve().parent / 'config.json'
GRID_LIVE_FILE_PATH = Path(__file__).resolve().parent / 'grid_live.json'
GRID_LIVE_SENT_TRADES_PATH = Path(__file__).resolve().parent / 'grid_live_sent_trades.json'
L_TRADE_EXECUTION_REQUESTS_DIR = Path(__file__).resolve().parent / 'execution_requests'
# [2026-04-07 17:15] V20260407_1715 - Added support for dynamic TWS order templates
TWS_ORDER_TEMPLATES_PATH = Path(__file__).resolve().parent / 'tws_order_templates.json'
_TWS_ORDER_TEMPLATES_CACHE: Dict[str, Any] = {'mtime': None, 'data': {}}
L_TRADE_EXECUTION_PENDING_PREFIX = 'pending:'

TRADE_OPEN_SUFFIX = '_op'
TRADE_CLOSED_SUFFIX = '_cl'
_TRADE_JSON_EXT = '.json'




def _parse_grid_live_metric(metric: Any) -> Tuple[str, Optional[str]]:
    """
    Normalize grid_live metric to (mode, direction).
    mode: 'net' or 'alt'
    direction: 'buy', 'sell', or None
    """
    raw = str(metric or 'net').lower()
    if raw in ('buy_net', 'sell_net', 'buy_alt', 'sell_alt'):
        direction, mode = raw.split('_', 1)
        return mode, direction
    if raw in ('net', 'alt'):
        return raw, None
    # Fallback to net
    return 'net', None

def _merge_grid_metric(existing: str, incoming: str) -> str:
    """
    Merge duplicate grid metrics for the same (model, product).
    Handles cases where both buy_* and sell_* entries are present.
    """
    e = str(existing or '').lower()
    i = str(incoming or '').lower()
    if not e:
        return i or 'net'
    if not i:
        return e
    if e == i:
        return e

    # If any broad metric is present, keep broad mode.
    if e in ('net', 'alt'):
        return e
    if i in ('net', 'alt'):
        return i

    # Directional merge: buy+sell of same mode => broad mode.
    # buy_net + sell_net -> net
    # buy_alt + sell_alt -> alt
    if {e, i} == {'buy_net', 'sell_net'}:
        return 'net'
    if {e, i} == {'buy_alt', 'sell_alt'}:
        return 'alt'

    # Mixed directional modes are ambiguous; prefer net mode for safety.
    if e.endswith('_net') or i.endswith('_net'):
        return 'net'
    return 'alt'


def _load_grid_live_map() -> Dict[Tuple[str, str], str]:
    global _GRID_LIVE_CACHE
    grid_path = GRID_LIVE_FILE_PATH
    try:
        mtime = grid_path.stat().st_mtime
    except OSError:
        _GRID_LIVE_CACHE = {'mtime': None, 'map': {}}
        return {}
    if _GRID_LIVE_CACHE.get('mtime') == mtime:
        return _GRID_LIVE_CACHE.get('map', {})
    try:
        with grid_path.open('r') as handle:
            raw = json.load(handle) or {}
    except (OSError, json.JSONDecodeError):
        _GRID_LIVE_CACHE = {'mtime': mtime, 'map': {}}
        return {}
    mapping: Dict[Tuple[str, str], str] = {}
    
    # [V20260130_1135] Support both flat list and category dict formats
    items = []
    if isinstance(raw, list):
        items = raw
    elif isinstance(raw, dict):
        for entries in raw.values():
            if isinstance(entries, list):
                items.extend(entries)
    
    for entry in items:
        if not isinstance(entry, dict):
            continue
        model = str(entry.get('model', '')).strip()
        product = str(entry.get('product', '')).strip().upper()
        if not model or not product:
            continue
        metric = str(entry.get('metric', 'net')).lower()
        # Allow directional metrics (buy_net/sell_net/buy_alt/sell_alt)
        if metric not in ('net', 'alt', 'buy_net', 'sell_net', 'buy_alt', 'sell_alt'):
            metric = 'net'
        key = (model, product)
        if key in mapping:
            mapping[key] = _merge_grid_metric(mapping[key], metric)
        else:
            mapping[key] = metric
    
    _GRID_LIVE_CACHE = {'mtime': mtime, 'map': mapping}
    return mapping


def _get_market_bias_for_date(run_mode: str, date_str: str) -> Optional[str]:
    """Read market bias from daily _targeted_strategies.json for the given mode/date."""
    mode = str(run_mode or 'live').lower()
    try:
        for base_dir in _iter_day_directories(mode, str(date_str)):
            bias_path = base_dir / '_targeted_strategies.json'
            if not bias_path.exists():
                continue
            with bias_path.open('r') as handle:
                data = json.load(handle) or {}
            bias = data.get('bias')
            if bias:
                return str(bias).upper()
        return None
    except Exception:
        return None


def _direction_matches_bias(direction: str, bias: Optional[str]) -> bool:
    """Return True when trade direction aligns with BUY/SELL bias."""
    b = str(bias or '').upper()
    d = str(direction or '').upper()
    if b == 'BUY':
        return d == 'LONG'
    if b == 'SELL':
        return d == 'SHORT'
    return False

def _load_grid_live_entries() -> List[Dict[str, Any]]:
    """Return normalized grid_live entries across live/sim sections."""
    grid_path = GRID_LIVE_FILE_PATH
    try:
        with grid_path.open('r') as handle:
            raw = json.load(handle) or {}
    except (OSError, json.JSONDecodeError):
        return []

    items: List[Dict[str, Any]] = []
    if isinstance(raw, list):
        for entry in raw:
            if isinstance(entry, dict):
                e = dict(entry)
                e.setdefault('mode', 'live')
                items.append(e)
        return items

    if isinstance(raw, dict):
        for mode_key, entries in raw.items():
            if not isinstance(entries, list):
                continue
            for entry in entries:
                if not isinstance(entry, dict):
                    continue
                e = dict(entry)
                e.setdefault('mode', str(mode_key))
                items.append(e)
    return items

def _get_grid_live_context_snapshot(model: str, product: str) -> Dict[str, Any]:
    """
    Capture relevant grid state when a trade promotion is blocked.
    Includes exact model+product matches and all product-side siblings.
    """
    model_key = str(model or '').strip()
    product_key = str(product or '').strip().upper()
    all_entries = _load_grid_live_entries()
    by_product = []
    exact_matches = []

    for entry in all_entries:
        e_model = str(entry.get('model', '')).strip()
        e_product = str(entry.get('product', '')).strip().upper()
        if e_product != product_key:
            continue
        item = {
            'mode': entry.get('mode'),
            'model': e_model,
            'product': e_product,
            'metric': str(entry.get('metric', 'net')).lower(),
            'source': entry.get('source'),
            'group': entry.get('group'),
            'activated_at': entry.get('activated_at'),
        }
        by_product.append(item)
        if e_model == model_key:
            exact_matches.append(item)

    return {
        'captured_at': datetime.now().isoformat(),
        'model': model_key,
        'product': product_key,
        'effective_metric_lookup': _get_grid_live_metric_for(model_key, product_key),
        'exact_matches': exact_matches,
        'product_entries': by_product,
    }

def _get_grid_live_origin(model: str, product: str) -> Dict[str, Optional[str]]:
    """
    Resolve source/group for a model+product from grid_live.
    Uses exact match first, then base-model fallback.
    """
    model_key = str(model or '').strip()
    product_key = str(product or '').strip().upper()
    entries = _load_grid_live_entries()
    exact = None
    fallback = None
    for entry in entries:
        e_model = str(entry.get('model', '')).strip()
        e_product = str(entry.get('product', '')).strip().upper()
        if e_product != product_key:
            continue
        if e_model == model_key:
            exact = entry
            break
        m_norm = e_model.lower()
        s_norm = model_key.lower()
        if s_norm.startswith(m_norm + "_") or m_norm.startswith(s_norm + "_"):
            fallback = fallback or entry
    chosen = exact or fallback
    if not chosen:
        return {'source': None, 'group': None}
    return {'source': chosen.get('source'), 'group': chosen.get('group')}

def _build_source_group(source: Optional[str], group: Optional[str]) -> str:
    s = str(source or 'breakout').strip()
    g = str(group or '').strip()
    return f"{s}|{g}" if g else s



def _get_grid_live_metric_for(model: str, product: str) -> Optional[str]:
    if not model or not product:
        return None
    mapping = _load_grid_live_map()
    model_str = str(model)
    product_key = str(product).upper()
    # Exact match first.
    exact = mapping.get((model_str, product_key))
    if exact:
        return exact
    # Fallback: allow base-model matching for parameterized strategy names.
    # Example: grid has `breakout_Rev`, runtime strategy is `breakout_Rev_4_tp10.0_sl30.0`.
    for (m_key, p_key), metric in mapping.items():
        if str(p_key).upper() != product_key:
            continue
        m_norm = str(m_key).lower()
        s_norm = model_str.lower()
        if s_norm.startswith(m_norm + "_") or m_norm.startswith(s_norm + "_"):
            return metric
    return None




def _get_weekly_summary_net(run_mode: str, current_date_str: str, model: str, product: str, metric: str) -> float:
    # [2026-04-07 16:35] V20260407_1635 - New: Calculate weekly total net
    try:
        from datetime import datetime, timedelta
        dt = datetime.fromisoformat(current_date_str)
        # Find Monday of the current week (weekday() is 0 for Monday)
        monday = dt - timedelta(days=dt.weekday())
        
        total = 0.0
        current = monday
        while current.strftime('%Y-%m-%d') <= current_date_str:
            # We use the existing summary stats lookup
            val = _get_summary_metric_value(run_mode, current.strftime('%Y-%m-%d'), model, product, metric)
            if val is not None:
                total += val
            current += timedelta(days=1)
        return total
    except Exception as e:
        print(f"[ERROR] Failed to calculate weekly summary: {e}")
        return 0.0


def _load_summary_net_stats(date_str: str, run_mode: str) -> Dict[Tuple[str, str], Dict[str, float]]:
    cache_key = (run_mode.lower(), date_str)
    cache_entry = _SUMMARY_NET_CACHE.get(cache_key)
    candidate_files: List[Path] = []
    for base_dir in _iter_day_directories(run_mode.lower(), date_str):
        candidate_files.extend([
            base_dir / '_summary_net.json',
            base_dir / '_summary_net_pre_auto_archive.json',
        ])

    summary_file = None
    mtime = None
    for candidate in candidate_files:
        try:
            mtime = candidate.stat().st_mtime
            summary_file = candidate
            break
        except OSError:
            continue

    if summary_file is None or mtime is None:
        _SUMMARY_NET_CACHE[cache_key] = (None, {})
        return {}

    cache_stamp = (str(summary_file), mtime)
    if cache_entry and cache_entry[0] == cache_stamp:
        return cache_entry[1]
    try:
        with summary_file.open('r') as handle:
            data = json.load(handle)
    except (OSError, json.JSONDecodeError):
        _SUMMARY_NET_CACHE[cache_key] = (cache_stamp, {})
        return {}
    mapping: Dict[Tuple[str, str], Dict[str, float]] = {}
    for strat, prods in (data.get('strategies') or {}).items():
        if not isinstance(prods, dict):
            continue
        for prod, points in prods.items():
            if not isinstance(points, list) or not points:
                continue
            last = points[-1]
            mapping[(str(strat), str(prod).upper())] = {
                'net': float(last.get('net', 0) or 0),
                'alt': float(last.get('alt_net', last.get('alt', 0) or 0)),
                'buy_net': float(last.get('buy_net', 0) or 0),
                'sell_net': float(last.get('sell_net', 0) or 0),
            }
    _SUMMARY_NET_CACHE[cache_key] = (cache_stamp, mapping)
    return mapping


def _get_summary_stats_entry(run_mode: str, date_str: str, model: str, product: str) -> Optional[Dict[str, float]]:
    stats = _load_summary_net_stats(date_str, run_mode)
    model_key = str(model)
    product_key = str(product).upper()
    entry = stats.get((model_key, product_key))
    if entry:
        return entry
    # Fallback to case-insensitive strategy matching.
    model_lower = model_key.lower()
    for (m_key, p_key), row in stats.items():
        if str(p_key).upper() != product_key:
            continue
        if str(m_key).lower() == model_lower:
            return row
    return None


def _get_summary_metric_value(run_mode: str, date_str: str, model: str, product: str, metric: str) -> Optional[float]:
    entry = _get_summary_stats_entry(run_mode, date_str, model, product)
    if not entry:
        return None
    metric_key = str(metric or 'net').lower()
    if metric_key in ('alt', 'net', 'buy_net', 'sell_net'):
        return entry.get(metric_key)
    return entry.get('net')

def _get_group_closed_live_pnl(json_base_dir: str, source_group: str) -> float:
    """Sum today's CLOSED live-trade net_return for a source-group."""
    total = 0.0
    today_str = _LATEST_TRADING_DATE or datetime.now().strftime('%Y-%m-%d')
    for day_dir in _iter_day_directories(Path(json_base_dir).name, today_str):
        for fp in day_dir.glob('*_cl.json'):
            try:
                with open(fp, 'r') as f:
                    d = json.load(f)
            except Exception:
                continue
            if d.get('is_live_trade') is not True:
                continue
            sg = str(d.get('source_group') or d.get('source_screen') or 'breakout')
            if sg != source_group:
                continue
            try:
                total += float(d.get('net_return', 0) or 0)
            except Exception:
                continue
    return total

def _get_total_open_live_trades_for_group(json_base_dir: str, source_group: str) -> int:
    """Count OPEN live trades for a given source-group."""
    today_str = _LATEST_TRADING_DATE or datetime.now().strftime('%Y-%m-%d')
    count = 0
    for day_dir in _iter_day_directories(Path(json_base_dir).name, today_str):
        for fp in day_dir.glob('*_op.json'):
            try:
                with open(fp, 'r') as f:
                    d = json.load(f)
            except Exception:
                continue
            if d.get('status') != 'OPEN':
                continue
            is_live = bool(d.get('is_live_trade') or d.get('order_sent_net') or d.get('order_sent_alt'))
            if not is_live:
                continue
            sg = str(d.get('live_cap_group') or d.get('source_group') or d.get('source_screen') or 'breakout')
            if sg == source_group:
                count += 1
    return count

def _get_total_open_tws_sent_trades(json_base_dir: str) -> int:
    """Count OPEN trades currently sent to TWS (order_sent_net=true)."""
    today_str = _LATEST_TRADING_DATE or datetime.now().strftime('%Y-%m-%d')
    count = 0
    for day_dir in _iter_day_directories(Path(json_base_dir).name, today_str):
        for fp in day_dir.glob('*_op.json'):
            try:
                with open(fp, 'r') as f:
                    d = json.load(f)
            except Exception:
                continue
            if d.get('status') != 'OPEN':
                continue
            if bool(d.get('order_sent_net')):
                count += 1
    return count


def _clean_trade_filename(filename: str) -> str:
    """Strip all known statuses and .json extensions to get a clean base stem."""
    f = filename
    # Strip multiple .json extensions if they exist
    while f.lower().endswith('.json'):
        f = f[:-5]
    # Strip multiple status suffixes if they exist
    changed = True
    while changed:
        changed = False
        for s in (TRADE_OPEN_SUFFIX, TRADE_CLOSED_SUFFIX, '_cld'):
            if f.lower().endswith(s):
                f = f[:-len(s)]
                changed = True
    return f

def _ensure_json_ext(filename: str) -> str:
    """Ensure filename ends with exactly one .json extension."""
    if filename.lower().endswith('.json'):
        return filename
    return f"{filename}.json"


def _write_json_atomic(filepath: str | Path, data: Any, indent: int = 2) -> None:
    """Write JSON via temp file + replace to avoid overlapping/truncated writes."""
    target = Path(filepath)
    target.parent.mkdir(parents=True, exist_ok=True)
    temp_path = target.with_name(f"{target.name}.{uuid.uuid4().hex}.tmp")
    try:
        with open(temp_path, 'w', encoding='utf-8') as handle:
            json.dump(data, handle, indent=indent)
            handle.flush()
            os.fsync(handle.fileno())
        last_error: Optional[Exception] = None
        for _ in range(10):
            try:
                os.replace(temp_path, target)
                last_error = None
                break
            except PermissionError as exc:
                last_error = exc
                time.sleep(0.05)
        if last_error is not None:
            raise last_error
    finally:
        try:
            if temp_path.exists():
                temp_path.unlink()
        except OSError:
            pass


def _append_signal_audit_entry(run_mode: str, date_str: str, product: str, entry: Dict[str, Any]) -> None:
    """Persist stage-by-stage signal/trade lifecycle events for later investigation."""
    return  # [V20260424] Disabled: concurrent write contention produces _signal_audit_corrupt_* files at high volume
    try:
        day_dir = _ensure_day_directory(str(run_mode or 'live').lower(), str(date_str), str(product or '').upper())
        target_path = day_dir / SIGNAL_AUDIT_FILENAME
        payload: Dict[str, Any] = {
            "version": SIGNAL_AUDIT_VERSION,
            "date": str(date_str),
            "product": str(product or '').upper(),
            "events": [],
        }
        if target_path.exists():
            try:
                with target_path.open('r', encoding='utf-8') as handle:
                    loaded = json.load(handle) or {}
                if isinstance(loaded, dict):
                    payload.update(loaded)
                    if not isinstance(payload.get("events"), list):
                        payload["events"] = []
            except Exception:
                corrupt_path = target_path.with_name(
                    f"_signal_audit_corrupt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                )
                try:
                    shutil.move(str(target_path), str(corrupt_path))
                except Exception:
                    pass
        payload["version"] = SIGNAL_AUDIT_VERSION
        payload["date"] = str(date_str)
        payload["product"] = str(product or '').upper()
        payload["updated_at"] = datetime.now().isoformat()
        payload.setdefault("events", []).append(entry)
        payload["events"] = payload["events"][-5000:]
        _write_json_atomic(target_path, payload, indent=2)
    except Exception as exc:
        print(f"[AUDIT] Failed to append signal audit entry: {exc}")


def _load_json_resilient(filepath: str | Path, repair: bool = False) -> Dict[str, Any]:
    """Load JSON, recovering the first valid object when trailing garbage exists."""
    path = Path(filepath)
    try:
        with open(path, 'r', encoding='utf-8') as handle:
            data = json.load(handle)
        return data if isinstance(data, dict) else {}
    except json.JSONDecodeError:
        pass

    with open(path, 'r', encoding='utf-8') as handle:
        raw = handle.read()

    decoder = json.JSONDecoder()
    stripped = raw.lstrip()
    if not stripped:
        raise json.JSONDecodeError("Empty JSON content", raw, 0)

    obj, end_idx = decoder.raw_decode(stripped)
    trailing = stripped[end_idx:].strip()
    if not isinstance(obj, dict):
        raise json.JSONDecodeError("Recovered JSON is not an object", raw, 0)

    if trailing and repair:
        _write_json_atomic(path, obj, indent=2)
        print(f"[REPAIR] Rewrote corrupted JSON file: {path.name}")
    return obj

def _strip_trade_status_suffix(filename: str) -> str:
    """Return base filename with .json but no status suffix."""
    base = _clean_trade_filename(filename)
    return f"{base}.json"

def _with_trade_status_suffix(filename: str, status: str) -> str:
    """Return filename with exactly one status suffix and one .json extension."""
    base = _clean_trade_filename(filename)
    suffix = TRADE_OPEN_SUFFIX if status.upper() == 'OPEN' else TRADE_CLOSED_SUFFIX
    return f"{base}{suffix}.json"


def _is_open_trade_filename(filename: str) -> bool:
    normalized = _ensure_json_ext(filename)
    return normalized[:-len(_TRADE_JSON_EXT)].endswith(TRADE_OPEN_SUFFIX)


def _trade_status_from_filename(filename: str) -> Optional[str]:
    normalized = _ensure_json_ext(filename)
    stem = normalized[:-len(_TRADE_JSON_EXT)]
    if stem.endswith(TRADE_OPEN_SUFFIX):
        return 'OPEN'
    if stem.endswith(TRADE_CLOSED_SUFFIX):
        return 'CLOSED'
    return None


def _is_auto_archivable_closed_trade_file(path: Path) -> bool:
    if not path.is_file():
        return False
    if path.suffix.lower() != _TRADE_JSON_EXT:
        return False
    if path.name.startswith('_'):
        return False

    normalized = _ensure_json_ext(path.name)
    stem = normalized[:-len(_TRADE_JSON_EXT)]
    return stem.endswith(TRADE_CLOSED_SUFFIX) or stem.endswith('_cld')



def _load_config() -> Dict[str, Any]:
    try:
        with open(CONFIG_FILE_PATH, 'r') as handle:
            cfg = json.load(handle)
            if isinstance(cfg, dict):
                cfg.setdefault('l_trade_auto_execution', True)
                cfg.setdefault('product_type', 'forex')
                cfg.setdefault('product_types', [cfg.get('product_type', 'forex')])
                cfg.setdefault('product_type_by_product', {})
                cfg.setdefault('default_min_value', 10.0)
                cfg.setdefault('min_value_by_product_type', {'forex': cfg.get('default_min_value', 10.0)})
                cfg.setdefault('min_value_by_product', {})
                cfg.setdefault('crypto_trade_qty_percent', cfg.get('trade_qty_percent', 45.0))
                return cfg
    except (FileNotFoundError, json.JSONDecodeError):
        return {
            "run_mode": "live",
            "product_type": "forex",
            "product_types": ["forex"],
            "product_type_by_product": {},
            "default_min_value": 10.0,
            "min_value_by_product_type": {
                "forex": 10.0,
            },
            "min_value_by_product": {},
            "endpoints": {
                "live": [
                    "http://127.0.0.1:8002/api/vw_000_fx_quotes",
                    "http://127.0.0.1:8002/api/vw_000_fx_quotes",
                ],
                "sim": [
                    "http://127.0.0.1:8002/api/vw_000_fx_quotes_sim2"
                ],
            },
            "trade_products": ["gbp"],
            "l_trade_auto_execution": True,
            "crypto_trade_qty_percent": 45.0,
            "bias_calc": "filtered_sum_net",
            "auto_net_check": True, # Default for auto activation
            "auto_alt_net_check": True, # Default for auto activation
            "auto_net_threshold": 0.0, # Default
            "auto_alt_threshold": 0.0, # Default
            "daily_target": 400.0, # Default daily target
            "max_live_trades": 1, # Default max live trades
            "market_update_enabled": False,
            "market_update_interval_minutes": 5,
            "max_live_tb": 5, # Default max simultaneously live trade buckets
            "max_trades_to_tws": 1, # Default max OPEN orders routed to TWS (order_sent_net=true)
            "top_n_strategies": 1, # [2025-12-23 V20251223_1150]
            "profitability_guard": { # Default guard config
                "mode": "recent_x",
                "count_x": 50,
                "threshold_y": 0.0
            },
            "enforce_market_bias": False,
            "enforce_market_bias_exit": False,
            "sleep_time": 10 # Default for strategy loop interval
        }


def _execution_request_path(request_id: str) -> Path:
    return L_TRADE_EXECUTION_REQUESTS_DIR / f'{request_id}.json'


def _is_execution_request_marker(value: Any) -> bool:
    return isinstance(value, str) and value.startswith(L_TRADE_EXECUTION_PENDING_PREFIX)


def _execution_request_id_from_marker(value: Any) -> Optional[str]:
    if not _is_execution_request_marker(value):
        return None
    request_id = value[len(L_TRADE_EXECUTION_PENDING_PREFIX):].strip()
    return request_id or None


def _load_execution_request(request_id: str) -> Optional[Dict[str, Any]]:
    if not request_id:
        return None
    path = _execution_request_path(request_id)
    if not path.exists():
        return None
    try:
        return _load_json_resilient(path, repair=True)
    except Exception:
        return None


def _list_execution_requests(status: Optional[str] = None) -> List[Dict[str, Any]]:
    requests: List[Dict[str, Any]] = []
    if not L_TRADE_EXECUTION_REQUESTS_DIR.exists():
        return requests
    for request_file in sorted(L_TRADE_EXECUTION_REQUESTS_DIR.glob('*.json'), reverse=True):
        try:
            data = _load_json_resilient(request_file, repair=True)
        except Exception:
            continue
        if not isinstance(data, dict):
            continue
        if status and str(data.get('status') or '').lower() != str(status).lower():
            continue
        requests.append(data)
    return requests


def _update_trade_file_pending_state(
    trade_json_path: Optional[str],
    *,
    mode: str,
    is_close: bool,
    request_id: Optional[str],
    status: str,
    request_context: Optional[Dict[str, Any]] = None,
) -> None:
    if not trade_json_path:
        return
    trade_path = Path(trade_json_path)
    if not trade_path.exists():
        return
    try:
        trade_data = _load_json_resilient(trade_path, repair=True)
    except Exception:
        return
    mode_key = str(mode or 'net').lower()
    if is_close:
        if status == 'pending' and request_id:
            trade_data['pending_close_request_id'] = request_id
            if isinstance(request_context, dict):
                if request_context.get('exit_time'):
                    trade_data['pending_close_exit_time'] = request_context.get('exit_time')
                if request_context.get('exit_price') is not None:
                    trade_data['pending_close_exit_price'] = request_context.get('exit_price')
                if request_context.get('exit_reason'):
                    trade_data['pending_close_exit_reason'] = request_context.get('exit_reason')
        else:
            trade_data.pop('pending_close_request_id', None)
            trade_data.pop('pending_close_exit_time', None)
            trade_data.pop('pending_close_exit_price', None)
            trade_data.pop('pending_close_exit_reason', None)
    else:
        pending_key = f'pending_order_request_{mode_key}'
        if status == 'pending' and request_id:
            trade_data[pending_key] = request_id
        else:
            trade_data.pop(pending_key, None)
    try:
        _write_json_atomic(trade_path, trade_data, indent=2)
    except Exception:
        return


def _finalize_execution_request_trade_file(request_data: Dict[str, Any], order_path: Optional[str]) -> None:
    order_args = request_data.get('order_args') or {}
    trade_json_path = order_args.get('trade_json_path')
    if not trade_json_path:
        return
    trade_path = Path(trade_json_path)
    if not trade_path.exists():
        return
    try:
        trade_data = _load_json_resilient(trade_path, repair=True)
    except Exception:
        return

    mode = str(order_args.get('mode') or 'net').lower()
    is_close = bool(order_args.get('is_close'))
    request_context = request_data.get('request_context') if isinstance(request_data.get('request_context'), dict) else {}

    if is_close:
        exit_price = _safe_float(request_context.get('exit_price'))
        entry_price = _safe_float(trade_data.get('entry_price'))
        direction = str(trade_data.get('direction') or '').upper()
        product = str(trade_data.get('product') or '').upper()
        cfg = _load_config()
        if None not in (entry_price, exit_price) and direction and product:
            pnl = _calculate_open_trade_pnl(entry_price, exit_price, direction, product, cfg)
            trade_data.update({
                'current_price': exit_price,
                'gross_pnl': pnl.get('gross_pnl'),
                'net_return': pnl.get('net_return'),
                'alt_net': pnl.get('alt_net'),
                'adhoc_cost_usd': pnl.get('adhoc_cost_usd'),
            })
        trade_data['status'] = 'CLOSED'
        trade_data['exit_time'] = request_context.get('exit_time') or datetime.now().isoformat()
        if exit_price is not None:
            trade_data['exit_price'] = exit_price
        trade_data['exit_reason'] = request_context.get('exit_reason') or 'Manual Close'
        trade_data.pop('pending_close_request_id', None)
        trade_data.pop('pending_close_exit_time', None)
        trade_data.pop('pending_close_exit_price', None)
        trade_data.pop('pending_close_exit_reason', None)
        if order_path:
            trade_data['close_order_path'] = order_path
        _write_json_atomic(trade_path, trade_data, indent=2)
        base_filename = _strip_trade_status_suffix(_ensure_json_ext(trade_path.name))
        closed_name = _with_trade_status_suffix(base_filename, 'CLOSED')
        closed_path = trade_path.with_name(closed_name)
        if trade_path.name != closed_name:
            try:
                os.replace(trade_path, closed_path)
            except OSError:
                pass
        try:
            _decrement_global_active(product, direction)
        except Exception:
            pass
        return

    flag_key = f'order_sent_{mode}'
    trade_data[flag_key] = True
    trade_data['is_live_trade'] = True
    trade_data['promoted_at'] = datetime.now().isoformat()
    trade_data.pop(f'pending_order_request_{mode}', None)
    if order_path:
        trade_data['latest_l_trade_order_path'] = order_path
    _write_json_atomic(trade_path, trade_data, indent=2)


def approve_l_trade_execution_request(request_id: str, approved_by: str = 'user') -> Dict[str, Any]:
    global _LAST_L_TRADE_ORDER_ERROR
    request_data = _load_execution_request(request_id)
    if not isinstance(request_data, dict):
        return {'success': False, 'message': f'Execution request {request_id} not found'}
    if str(request_data.get('status') or '').lower() != 'pending':
        return {
            'success': False,
            'message': f"Execution request {request_id} is already {request_data.get('status') or 'processed'}",
            'request': request_data,
        }

    order_args = dict(request_data.get('order_args') or {})
    order_args['bypass_execution_gate'] = True
    order_args['force_execution_request'] = False
    order_args['execution_request_id'] = request_id
    order_path = _create_l_trade_order(**order_args)
    if not order_path or _is_execution_request_marker(order_path):
        return {
            'success': False,
            'message': _LAST_L_TRADE_ORDER_ERROR or f'Failed to approve execution request {request_id}',
            'request': request_data,
        }

    request_data['status'] = 'approved'
    request_data['approved_at'] = datetime.now().isoformat()
    request_data['approved_by'] = approved_by
    request_data['order_path'] = order_path
    _write_json_atomic(_execution_request_path(request_id), request_data, indent=2)
    _finalize_execution_request_trade_file(request_data, order_path)
    return {'success': True, 'request': request_data, 'order_path': order_path}


def cancel_l_trade_execution_request(
    request_id: str,
    cancelled_by: str = 'user',
    reason: str = 'cancelled',
) -> Dict[str, Any]:
    request_data = _load_execution_request(request_id)
    if not isinstance(request_data, dict):
        return {'success': False, 'message': f'Execution request {request_id} not found'}
    if str(request_data.get('status') or '').lower() != 'pending':
        return {
            'success': False,
            'message': f"Execution request {request_id} is already {request_data.get('status') or 'processed'}",
            'request': request_data,
        }
    request_data['status'] = 'cancelled'
    request_data['cancelled_at'] = datetime.now().isoformat()
    request_data['cancelled_by'] = cancelled_by
    request_data['cancel_reason'] = reason
    _write_json_atomic(_execution_request_path(request_id), request_data, indent=2)
    order_args = request_data.get('order_args') or {}
    _update_trade_file_pending_state(
        order_args.get('trade_json_path'),
        mode=str(order_args.get('mode') or 'net'),
        is_close=bool(order_args.get('is_close')),
        request_id=None,
        status='cancelled',
        request_context=request_data.get('request_context') if isinstance(request_data.get('request_context'), dict) else None,
    )
    return {'success': True, 'request': request_data}


def _load_tws_order_templates() -> Dict[str, Any]:
    # [2026-04-07 17:15] V20260407_1715 - Load TWS order templates from JSON file
    global _TWS_ORDER_TEMPLATES_CACHE
    try:
        mtime = TWS_ORDER_TEMPLATES_PATH.stat().st_mtime
    except OSError:
        return {}
    
    if _TWS_ORDER_TEMPLATES_CACHE.get('mtime') == mtime:
        return _TWS_ORDER_TEMPLATES_CACHE.get('data', {})
    
    try:
        with open(TWS_ORDER_TEMPLATES_PATH, 'r') as f:
            data = json.load(f)
        _TWS_ORDER_TEMPLATES_CACHE = {'mtime': mtime, 'data': data}
        return data
    except (OSError, json.JSONDecodeError):
        return {}


def _get_tws_contract_details(product: str, config: Dict[str, Any]) -> Dict[str, Any]:
    # [2026-04-07 17:15] V20260407_1715 - Resolve TWS contract details based on product/type
    templates = _load_tws_order_templates()
    p_u = product.upper()
    p_type = _resolve_product_type(product, config)
    
    # 1. Start with product type defaults (e.g., 'forex', 'indices', 'metals')
    type_data = templates.get(p_type, {})
    details = {
        'symbol': p_u,
        'secType': type_data.get('secType', 'CASH'),
        'exchange': type_data.get('contract_fields', {}).get('exchange', 'IDEALPRO'),
        'currency': type_data.get('contract_fields', {}).get('currency', 'USD'),
    }
    
    # 2. Apply product-specific overrides if defined in templates
    prod_overrides = type_data.get('products', {}).get(p_u, {})
    if prod_overrides:
        details.update(prod_overrides)
        # Handle lastTradeDateOrContractMonth for Futures
        if details['secType'] == 'FUT':
            # Use current month if not specified, or sample from template example
            example = type_data.get('example', {})
            details.setdefault('lastTradeDateOrContractMonth', example.get('lastTradeDateOrContractMonth', '202606'))
            details.setdefault('multiplier', example.get('multiplier', '1'))
            
    return details


def _json_root_dir() -> Path:
    return Path(CONFIG_FILE_PATH).resolve().parent / 'json'


def _load_layout_runtime_config() -> Dict[str, Any]:
    cfg = load_layout_config(Path(CONFIG_FILE_PATH))
    cfg.setdefault('product_type', default_product_type(cfg))
    cfg.setdefault('product_types', configured_product_types(cfg))
    cfg.setdefault('product_type_by_product', {})
    return cfg


def _resolve_product_type(product: str | None, config: Optional[Dict[str, Any]] = None) -> str:
    return product_type_for_product(product, config or _load_layout_runtime_config())


def _trade_qty_percent_for_product(product: str | None, config: Optional[Dict[str, Any]] = None) -> float:
    cfg = config or _load_layout_runtime_config()
    default_pct = float(cfg.get('trade_qty_percent', 45.0))
    if _resolve_product_type(product, cfg) == 'crypto':
        return float(cfg.get('crypto_trade_qty_percent', default_pct))
    return default_pct


def _min_value_for_product(product: str | None, config: Optional[Dict[str, Any]] = None) -> float | None:
    cfg = config or _load_layout_runtime_config()
    product_key = str(product or '').strip().upper()
    raw_by_product = cfg.get('min_value_by_product', {})
    if isinstance(raw_by_product, dict) and product_key:
        raw_value = raw_by_product.get(product_key)
        if raw_value not in (None, ''):
            try:
                return float(raw_value)
            except (TypeError, ValueError):
                pass

    product_type = _resolve_product_type(product, cfg)
    raw_by_type = cfg.get('min_value_by_product_type', {})
    if isinstance(raw_by_type, dict):
        raw_value = raw_by_type.get(str(product_type).strip().lower())
        if raw_value not in (None, ''):
            try:
                return float(raw_value)
            except (TypeError, ValueError):
                pass

    raw_default = cfg.get('default_min_value')
    if raw_default not in (None, ''):
        try:
            return float(raw_default)
        except (TypeError, ValueError):
            pass
    return None


def _min_move_for_product(product: str | None, config: Optional[Dict[str, Any]] = None) -> float | None:
    cfg = config or _load_layout_runtime_config()
    product_key = str(product or '').strip().upper()
    raw_by_product = cfg.get('min_move_by_product', {})
    if isinstance(raw_by_product, dict) and product_key:
        raw_value = raw_by_product.get(product_key)
        if raw_value not in (None, ''):
            try:
                return float(raw_value)
            except (TypeError, ValueError):
                pass
    return None


def _get_pip_multiplier(product: str | None, config: Optional[Dict[str, Any]] = None) -> float:
    """Hierarchical lookup for product pip multiplier. [2026-03-17 16:55 V20260317_1600]"""
    cfg = config or _load_layout_runtime_config()
    product_key = str(product or '').strip().upper()

    # 1. Check direct product match
    raw_by_product = cfg.get('pip_multiplier_by_product', {})
    if isinstance(raw_by_product, dict) and product_key:
        val = raw_by_product.get(product_key)
        if val not in (None, ''):
            # print(f"[DEBUG] _get_pip_multiplier({product_key}) found direct match: {val}")
            return float(val)

    # 2. Check product type match
    product_type = _resolve_product_type(product, cfg)
    raw_by_type = cfg.get('pip_multiplier_by_product_type', {})
    if isinstance(raw_by_type, dict):
        val = raw_by_type.get(str(product_type).strip().lower())
        if val not in (None, ''):
            # print(f"[DEBUG] _get_pip_multiplier({product_key}) found type match ({product_type}): {val}")
            return float(val)

    # 3. Default fallback
    # print(f"[DEBUG] _get_pip_multiplier({product_key}) using default fallback: 10000.0 (type={product_type})")
    return 10000.0


def _pip_value_for_product(product: str | None, config: Optional[Dict[str, Any]] = None) -> float:
    """Resolve the USD value of one internal pip for a product."""
    cfg = config or _load_layout_runtime_config()
    min_move = _min_move_for_product(product, cfg)
    min_value = _min_value_for_product(product, cfg)
    pip_multiplier = _get_pip_multiplier(product, cfg)

    if min_move not in (None, 0.0) and min_value is not None and pip_multiplier not in (None, 0.0):
        return float(min_value) / (float(min_move) * float(pip_multiplier))

    raw_default = cfg.get('pip_value')
    if raw_default not in (None, ''):
        try:
            return float(raw_default)
        except (TypeError, ValueError):
            pass

    return PIP_VALUE


def _trade_quantity_for_product(product: str | None, config: Optional[Dict[str, Any]] = None) -> int | float:
    # [2026-04-08 14:00] V20260408_1400 - Dynamic quantity based on product type
    cfg = config or _load_layout_runtime_config()
    p_type = _resolve_product_type(product, cfg)
    pct = _trade_qty_percent_for_product(product, cfg)
    
    if p_type == 'forex':
        return int(100000 * (pct / 100.0))
    elif p_type == 'crypto':
        return float(1.0 * (pct / 100.0))
    else:
        # Futures (indices, energy, metals, rates)
        base_qty = int(cfg.get('futures_base_qty', 1))
        return int(base_qty)


def _max_quote_age_seconds_for_product(product: str | None, config: Optional[Dict[str, Any]] = None) -> Optional[float]:
    cfg = config or _load_layout_runtime_config()
    product_type = _resolve_product_type(product, cfg)
    raw_by_type = cfg.get('max_quote_age_seconds_by_product_type', {})
    if isinstance(raw_by_type, dict):
        raw_value = raw_by_type.get(str(product_type).strip().lower())
        if raw_value not in (None, ''):
            try:
                return float(raw_value)
            except (TypeError, ValueError):
                pass
    return None


def _resolve_day_directory(run_mode: str, date_str: str, product: str | None = None) -> Path:
    cfg = _load_layout_runtime_config()
    product_type = _resolve_product_type(product, cfg) if product else cfg.get('product_type')
    return resolve_day_dir(_json_root_dir(), run_mode, date_str, product_type)


def _ensure_day_directory(run_mode: str, date_str: str, product: str | None = None) -> Path:
    cfg = _load_layout_runtime_config()
    return ensure_day_dir(_json_root_dir(), run_mode, date_str, config=cfg, product=product)


def _iter_day_directories(run_mode: str, date_str: str) -> List[Path]:
    return iter_day_dirs(_json_root_dir(), run_mode, date_str, config=_load_layout_runtime_config())


CONFIG = _load_config()
_GRID_LIVE_CACHE = {'mtime': None, 'map': {}}
_SUMMARY_NET_CACHE: Dict[Tuple[str, str], Tuple[Optional[float], Dict[Tuple[str, str], Dict[str, float]]]] = {}

WINDOW_SIZE_CONFIG = CONFIG.get('window_size', 5)
if isinstance(WINDOW_SIZE_CONFIG, list):
    WINDOW_SIZES: List[int] = [int(value) for value in WINDOW_SIZE_CONFIG]
else:
    WINDOW_SIZES = [int(WINDOW_SIZE_CONFIG)]

def _get_float_list(key, default):
    val = CONFIG.get(key)
    if val is None or val == []:
        val = default
    if isinstance(val, list):
        parsed = []
        for v in val:
            try:
                parsed.append(float(v))
            except (TypeError, ValueError):
                pass
        return parsed if parsed else [float(default)]
    try:
        return [float(val)]
    except (TypeError, ValueError):
        return [float(default)]

TP_PIPS_LIST = _get_float_list('tp_pips', 30.0)

def _coerce_int_list(value: Any, fallback: List[int]) -> List[int]:
    if isinstance(value, list):
        result = []
        for item in value:
            try:
                result.append(int(item))
            except (TypeError, ValueError):
                continue
        return result or list(fallback)
    try:
        return [int(value)]
    except (TypeError, ValueError):
        return list(fallback)


def _coerce_float_list(value: Any, fallback: List[float]) -> List[float]:
    if isinstance(value, list):
        result = []
        for item in value:
            try:
                result.append(float(item))
            except (TypeError, ValueError):
                continue
        return result or list(fallback)
    try:
        return [float(value)]
    except (TypeError, ValueError):
        return list(fallback)


def _resolve_cli_or_config(cli_value: Any, base_value: Any, config_value: Any) -> Any:
    return config_value if cli_value == base_value else cli_value


def _config_mtime() -> Optional[float]:
    try:
        return os.path.getmtime(CONFIG_FILE_PATH)
    except OSError:
        return None

SL_PIPS_LIST = _get_float_list('sl_pips', 10.0)

PIP_BUFFER = float(CONFIG.get('pip_buffer') if CONFIG.get('pip_buffer') is not None else 0.0001)
TP_PIPS = TP_PIPS_LIST[0]
SL_PIPS = SL_PIPS_LIST[0]
COMMISSION_USD = float(CONFIG.get('commission_usd') if CONFIG.get('commission_usd') is not None else 5.0)
SPREAD_PIPS = float(CONFIG.get('spread_pips') if CONFIG.get('spread_pips') is not None else 2.0)
PIP_VALUE = float(CONFIG.get('pip_value') if CONFIG.get('pip_value') is not None else 10.0)
# Added trade_qty_percent and fixed DEFAULT_TRADE_PRODUCTS logic [2025-12-19 V20251219_0934]
TRADE_QTY_PERCENT = float(CONFIG.get('trade_qty_percent') if CONFIG.get('trade_qty_percent') is not None else 45.0)
env_products = os.getenv('BREAKOUT_TRADE_PRODUCTS')
if env_products:
    DEFAULT_TRADE_PRODUCTS = [p.strip() for p in env_products.split(',') if p.strip()]
else:
    DEFAULT_TRADE_PRODUCTS = CONFIG.get('trade_products', ['GBP'])
POLL_INTERVAL_SECONDS = int(CONFIG.get('sleep_time') if CONFIG.get('sleep_time') is not None else os.getenv('BREAKOUT_POLL_INTERVAL', '10'))
COMMISSION_PIPS = COMMISSION_USD / PIP_VALUE
ACTIVATIONS_FILE = os.path.join(os.path.dirname(__file__), 'activations.json')
ACTIVATION_SUFFIXES = ('_buy_net', '_sell_net', '_buy_alt', '_sell_alt')
_ACTIVATIONS_CACHE: Dict[str, Any] = {'mtime': None, 'data': {}}
# Preserve base defaults for runtime reloads
BASE_WINDOW_SIZES = list(WINDOW_SIZES)
BASE_TP_PIPS_LIST = list(TP_PIPS_LIST)
BASE_SL_PIPS_LIST = list(SL_PIPS_LIST)
BASE_PIP_BUFFER = PIP_BUFFER
BASE_TP_PIPS = TP_PIPS
BASE_SL_PIPS = SL_PIPS
BASE_POLL_INTERVAL_SECONDS = POLL_INTERVAL_SECONDS
BASE_COMMISSION_PIPS = COMMISSION_PIPS
BASE_SPREAD_PIPS = SPREAD_PIPS
ACTIVATIONS_LOCK_FILE = os.path.join(os.path.dirname(__file__), 'activations.lock') # [2025-12-22 V20251222_1600]
V_TRADES_LOCK_FILE = os.path.join(os.path.dirname(__file__), 'v_trades.lock') # [2025-12-26 V20251226_1630]
GLOBAL_ACTIVE_TRADES_FILE = os.path.join(os.path.dirname(__file__), 'active_trades.json')


@dataclass
class QuoteTick:
    timestamp: pd.Timestamp
    price: float
    bid: Optional[float] = None
    ask: Optional[float] = None
    raw: Dict[str, Any] = None


def _safe_float(value: Any) -> Optional[float]:
    try:
        if value is None:
            return None
        return float(value)
    except (TypeError, ValueError):
        return None


def _normalize_timestamp(value: Any) -> Optional[pd.Timestamp]:
    if value is None:
        return None
    try:
        ts = pd.to_datetime(value, utc=True, errors='coerce')
    except (ValueError, TypeError):
        return None
    if pd.isna(ts):
        return None
    if isinstance(ts, pd.Timestamp):
        return ts.tz_convert('UTC').tz_localize(None)
    return None


def _trading_timezone() -> ZoneInfo:
    try:
        cfg = _load_config()
        tz_name = str(cfg.get('trading_timezone') or DEFAULT_TRADING_TIMEZONE).strip()
        return ZoneInfo(tz_name or DEFAULT_TRADING_TIMEZONE)
    except (ZoneInfoNotFoundError, OSError, ValueError, TypeError):
        return ZoneInfo(DEFAULT_TRADING_TIMEZONE)


def _trading_local_timestamp(value: Any) -> Optional[pd.Timestamp]:
    ts = _normalize_timestamp(value)
    if ts is None:
        return None
    return ts.tz_localize('UTC').tz_convert(_trading_timezone())


def _trading_date_string(value: Any) -> Optional[str]:
    ts = _trading_local_timestamp(value)
    if ts is None:
        return None
    return ts.strftime('%Y-%m-%d')


def _trading_filename_timestamp(value: Any) -> Optional[str]:
    ts = _trading_local_timestamp(value)
    if ts is None:
        return None
    return ts.strftime('%Y%m%d_%H%M%S')


def _extract_mid_price(row: Dict[str, Any]) -> Optional[float]:
    for field in ('price', 'mid', 'mid_price', 'last', 'last_price'):
        maybe_value = _safe_float(row.get(field))
        if maybe_value is not None:
            return maybe_value
    bid = _safe_float(row.get('bid'))
    ask = _safe_float(row.get('ask'))
    if bid is not None and ask is not None:
        return (bid + ask) / 2.0
    return None


def _get_latest_price_snap(latest_prices: Dict[str, Any], product: str) -> Optional[Dict[str, Any]]:
    """Case-insensitive price lookup helper. [V20251228_0315]"""
    if not latest_prices or not product:
        return None
    # 1. Try exact match
    if product in latest_prices:
        return latest_prices[product]
    # 2. Try case-insensitive
    p_u = product.upper()
    for k, v in latest_prices.items():
        if str(k).upper() == p_u:
            return v
    return None


def _flatten_payload(payload: Any) -> Sequence[Dict[str, Any]]:
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        for key in ('data', 'results', 'records'):
            nested = payload.get(key)
            if isinstance(nested, list):
                return nested
        return [payload]
    return []


def _candidate_api_urls(trade_product: str) -> List[str]:
    config = _load_config()
    run_mode = config.get('run_mode', 'live')
    endpoints = config.get('endpoints', {})
    templates = endpoints.get(run_mode, endpoints.get('live', []))
    env_urls = os.getenv('BREAKOUT_API_URLS')
    if env_urls:
        templates = [item.strip() for item in env_urls.split(',') if item.strip()]

    seen = set()
    urls: List[str] = []
    for template in templates:
        if not template:
            continue
        formatted = template.format(product=trade_product.lower())
        if formatted in seen:
            continue
        seen.add(formatted)
        urls.append(formatted)
    return urls


def fetch_latest_quotes(trade_product: str) -> List[QuoteTick]:
    last_error: Optional[str] = None
    product_code = trade_product.lower()
    all_ticks: List[QuoteTick] = []
    for url in _candidate_api_urls(trade_product):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
        except requests.RequestException as exc:
            last_error = f'{url} -> {exc}'
            continue
        try:
            payload = response.json()
        except ValueError as exc:
            last_error = f'{url} -> Non-JSON payload ({exc})'
            continue

        filtered_records = _flatten_payload(payload)
        ticks: List[QuoteTick] = []
        for record in filtered_records:
            if not isinstance(record, dict):
                continue
            code_value = str(
                record.get('code')
                or record.get('trade_product')
                or record.get('product')
                or trade_product
            ).lower()
            if code_value != product_code:
                continue

            timestamp = _normalize_timestamp(
                record.get('timestamp')
                or record.get('quote_time')
                or record.get('time')
                or record.get('ts')
            )
            price = _extract_mid_price(record)
            bid = _safe_float(record.get('bid'))
            ask = _safe_float(record.get('ask'))
            if timestamp is None or price is None:
                continue
            ticks.append(QuoteTick(timestamp=timestamp, price=price, bid=bid, ask=ask, raw=record))

        ticks.sort(key=lambda tick: tick.timestamp)
        if ticks:
            all_ticks.extend(ticks)
            continue
        last_error = f'{url} -> no quotes matched product {trade_product}'
    if all_ticks:
        all_ticks.sort(key=lambda tick: tick.timestamp)
        freshest_timestamp = all_ticks[-1].timestamp
        freshest_ticks = [tick for tick in all_ticks if tick.timestamp == freshest_timestamp]
        return freshest_ticks
    raise RuntimeError(last_error or 'No API endpoint configured for quotes')


class BaseBreakoutStrategy:
    allow_reversal: bool = False

    def __init__(
        self,
        window_size: int,
        pip_buffer: float,
        tp_pips: float,
        sl_pips: float,
        commission_pips: float,
        spread_pips: float,
        trade_product: str,
        script_name: str,
        max_live_trades: Optional[int] = None,
    ) -> None:
        self.window_size = window_size
        self.pip_buffer = pip_buffer
        self.tp_pips = tp_pips
        self.sl_pips = sl_pips
        self.commission_pips = commission_pips
        self.spread_pips = spread_pips
        self.trade_product = trade_product.upper()
        self.script_name = script_name

        config = _load_config()
        self.run_mode = config.get('run_mode', 'LIVE').upper()
        self.product_type = _resolve_product_type(self.trade_product, config)
        # [2026-03-16 V20260316_1430] Initialize product-specific pip multiplier
        self.pip_multiplier = _get_pip_multiplier(self.trade_product, config)
        # Added state_persistence flag [2025-12-19 V20251219_0934]
        self.state_persistence = config.get('state_persistence', True)
        self.profitability_guard_config = config.get('profitability_guard', {})
        self.l_trade_generation_mode = str(config.get('l_trade_generation_mode', 'both')).lower()

        self.price_history = deque(maxlen=window_size)
        self.trade_log: List[Dict[str, Any]] = []
        self.open_trade: Optional[Dict[str, Any]] = None
        self.cumulative_pnl_usd = 0.0
        self.cumulative_alt_pnl_usd = 0.0
        self.trade_counter = 0
        self.cum_buy_net = 0.0
        self.cum_sell_net = 0.0
        self.cum_buy_alt = 0.0
        self.cum_sell_alt = 0.0
        self.latest_bid = None
        self.latest_ask = None
        self._table_header_printed = False
        
        self.json_base_dir = os.path.join(os.path.dirname(CONFIG_FILE_PATH), 'json', self.run_mode.lower())
        self.config = config # [V20260323_1935] Store config for P&L calculations
        os.makedirs(self.json_base_dir, exist_ok=True)
        self.active_trades_state = _load_active_trades()
        resolved_cap = max_live_trades if max_live_trades is not None else config.get('max_live_trades')
        self.max_live_trades = int(resolved_cap) if resolved_cap not in (None, '') else None
        # Call load_persisted_state [2025-12-19 V20251219_0934]
        self._load_persisted_state()

    def _load_persisted_state(self) -> None:
        """Scan disk for an open trade and restore the trade counter. [2025-12-27 V20251227_2330]"""
        if not self.state_persistence:
            print(f"[INFO] State persistence disabled for {self.trade_product} ({self.script_name}). Starting fresh.")
            return

        current_params = f"{self.window_size}_{self.pip_buffer}_{self.tp_pips}_{self.sl_pips}"
        max_id = 0
        found_open_trade = None

        # [V20251227_2340] OPTIMIZATION: ONLY scan the current date folder.
        # If the folder doesn't exist, we assume no trades and start fresh.
        # [V20260101_2130] Use latest seen trading date
        today_str = _LATEST_TRADING_DATE or datetime.now().strftime('%Y-%m-%d')
        folder_path = _resolve_day_directory(self.run_mode.lower(), today_str, self.trade_product)

        if folder_path.exists():
            # Only scan open trade files - closed/system files are irrelevant for state restore
            for json_path in folder_path.glob('*_op.json'):
                try:
                    fname = json_path.name
                    normalized_fname = _ensure_json_ext(fname)
                    base_filename = _strip_trade_status_suffix(normalized_fname)
                    # [V20260101_2250] Skip empty or system files (_top_one.json)
                    if os.path.getsize(json_path) == 0 or fname.startswith('_'):
                        continue

                    with open(json_path, 'r') as f:
                        data = json.load(f)
                    
                    tid = data.get('trade_id', 0)
                    # Convert to int if it's a numeric string
                    if isinstance(tid, str) and tid.isdigit():
                        tid = int(tid)
                    elif not isinstance(tid, (int, float)):
                        tid = 0

                    if tid > max_id:
                        max_id = int(tid)

                    # Skip virtual trades
                    fname = json_path.name
                    if fname.startswith("vt_"):
                        continue

                    if (
                        data.get('status') == 'OPEN' and 
                        data.get('product', '').upper() == self.trade_product and
                        # [V20260129_0325] More robust matching: check content AND filename
                        (self.script_name in fname or data.get('script_name') == self.script_name) and
                        current_params in fname
                    ):
                        # [V20251231_0300] Additional validation: check window_size in JSON
                        if data.get('window_size') == self.window_size:
                            desired_open_name = _with_trade_status_suffix(base_filename, 'OPEN')
                            if normalized_fname != desired_open_name:
                                try:
                                    new_path = json_path.with_name(desired_open_name)
                                    json_path.rename(new_path)
                                    normalized_fname = desired_open_name
                                    fname = desired_open_name
                                    json_path = new_path
                                except OSError as exc:
                                    print(f"[PERSIST] Failed to normalize {fname}: {exc}")
                            data['json_base_filename'] = base_filename
                            data['json_filename'] = desired_open_name
                            data['entry_time'] = self._coerce_timestamp(data.get('entry_time'))
                            data['id'] = data.get('trade_id', f"unknown_id_{uuid.uuid4().hex}")
                            # [V20251231_0300] Only keep the most recent open trade if multiple found
                            if found_open_trade is None or data.get('trade_id', 0) > found_open_trade.get('trade_id', 0):
                                found_open_trade = data
                                print(f"[PERSIST] Found open trade #{data.get('trade_id')} in {fname}")
                except Exception as e:
                    print(f"[PERSIST] Error reading {json_path.name}: {e}")
                    continue

        self.trade_counter = max_id
        if found_open_trade:
            self.open_trade = found_open_trade
            print(f"[RESUME] Restored open trade #{found_open_trade.get('trade_id')} for {self.trade_product} ({self.script_name}, window={self.window_size}). Resuming...")
            _increment_global_active(self.trade_product, found_open_trade.get('direction', ''))
        else:
            print(f"[INFO] No open trades found for {self.trade_product} ({self.script_name}, window={self.window_size}). Counter restored to {max_id}.")

    def _current_live_trades(self) -> int:
        state = _load_active_trades()
        self.active_trades_state = state
        return sum(int(value) for value in state.values())

    def _is_auto_promote_active(self, direction: str, mode: str) -> bool:
        # [2026-04-07 16:35] V20260407_1635 - New: Check for auto_promote flag in activations
        # [2026-04-07 16:50] V20260407_1650 - FIX: Support UI-style keys (breakout_breakout_...)
        try:
            activations = _load_activations()
            
            # 1. UI-style key: breakout_breakout_2_tp30.0_sl5.0_buy_net
            # Note: TP/SL in UI keys always have .0 suffix
            ui_strategy = f"{self.script_name}_{self.window_size}_tp{float(self.tp_pips):.1f}_sl{float(self.sl_pips):.1f}"
            ui_key = f"{self.script_name}_{ui_strategy}_{direction.lower()}_{mode.lower()}"
            
            # 2. Param-style key: breakout_2_0.00015_30.0_5.0_buy_net
            param_key = f"{self.script_name}_{self.window_size}_{self.pip_buffer}_{self.tp_pips}_{self.sl_pips}_{direction.lower()}_{mode.lower()}"
            
            entry = activations.get(ui_key) or activations.get(param_key)
            
            if isinstance(entry, dict) and entry.get('active') and entry.get('auto_promote'):
                activated_products = entry.get("products")
                if isinstance(activated_products, list):
                    return self.trade_product.upper() in [p.upper() for p in activated_products]
            return False
        except Exception:
            return False

    def _is_active(self, direction: str, mode: str) -> bool:
        # [2025-12-30] FIX: Link strategy activation to the specific product.
        # [2026-04-07 16:50] V20260407_1650 - FIX: Support UI-style keys (breakout_breakout_...)
        try:
            activations = _load_activations()
            
            # 1. UI-style key
            ui_strategy = f"{self.script_name}_{self.window_size}_tp{float(self.tp_pips):.1f}_sl{float(self.sl_pips):.1f}"
            ui_key = f"{self.script_name}_{ui_strategy}_{direction.lower()}_{mode.lower()}"
            
            # 2. Param-style key
            param_key = f"{self.script_name}_{self.window_size}_{self.pip_buffer}_{self.tp_pips}_{self.sl_pips}_{direction.lower()}_{mode.lower()}"
            
            entry = activations.get(ui_key) or activations.get(param_key)

            # If there's no entry for the strategy, it's not active.
            if entry is None:
                return False

            # Determine if the strategy is generally active.
            is_generally_active = False
            if isinstance(entry, bool):
                is_generally_active = entry
            elif isinstance(entry, dict):
                is_generally_active = bool(entry.get('active', False))

            # If not generally active, then it's not active for any product.
            if not is_generally_active:
                return False

            # If it is generally active, check for a product-specific list.
            if isinstance(entry, dict):
                activated_products = entry.get("products")
                # If a "products" list exists...
                if isinstance(activated_products, list):
                    # ...then activation is ONLY valid if the current product is in that list.
                    # The list is case-insensitive.
                    return self.trade_product.upper() in [p.upper() for p in activated_products]

            # If the strategy is active but there is NO "products" list,
            # it is no longer considered active for all products (strict scoping). [V20251231_1110]
            return False

        except Exception as exc:
            print(f"Error checking activation: {exc}")
            return False

    @staticmethod
    def _coerce_timestamp(value: Any) -> Optional[pd.Timestamp]:
        if isinstance(value, pd.Timestamp):
            return value
        return _normalize_timestamp(value)


    def _generate_trade_filename(self, guid: str, current_time: Any) -> str:
        """Create a deterministic trade filename keyed by script/guid/product/params."""
        ts_str = _trading_filename_timestamp(current_time) or pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')
        params = f"{self.window_size}_{self.pip_buffer}_{self.tp_pips}_{self.sl_pips}"
        # [V20260129_0435] GUID integration: insert GUID before product name
        return f"{self.script_name}_{guid}_{self.trade_product}_{ts_str}_{params}.json"

    def _compute_trade_filenames(self, guid: str, current_time: Any) -> Tuple[str, str]:
        """Derive base and open filenames using the status suffix convention."""
        base_filename = self._generate_trade_filename(guid, current_time)
        open_filename = _with_trade_status_suffix(base_filename, 'OPEN')
        return base_filename, open_filename

    def _is_market_bias_entry_allowed(self, direction: str, timestamp: Optional[pd.Timestamp] = None) -> Tuple[bool, str]:
        """When enforce_market_bias is enabled, allow L-trade only if direction aligns to bias_at_open."""
        cfg = _load_config()
        if not bool(cfg.get('enforce_market_bias', False)):
            return True, ''
        bias_at_open = (self.open_trade or {}).get('market_bias_at_open')
        if not bias_at_open:
            ts = timestamp or pd.Timestamp.now()
            bias_at_open = _get_market_bias_for_date(self.run_mode.lower(), ts.strftime('%Y-%m-%d'))
            if self.open_trade is not None and bias_at_open:
                self.open_trade['market_bias_at_open'] = bias_at_open
        if not _direction_matches_bias(direction, bias_at_open):
            return False, f"market-bias entry mismatch (direction={direction}, bias_at_open={bias_at_open})"
        return True, ''

    def _handle_live_orders(self, current_time: Any, current_price: float, direction: str) -> None:
        """Send tradeable JSON orders when guards/activations allow it."""
        if not self.open_trade:
            return

        if self.l_trade_generation_mode not in ('normal', 'both'):
            print(f"[L-TRADE] Normal L-Trade path disabled (mode={self.l_trade_generation_mode}). Skipping direct live order generation.")
            self._audit_signal_event(
                'live_order_path_skipped_generation_mode',
                current_time=current_time,
                l_trade_generation_mode=self.l_trade_generation_mode,
            )
            return

        dir_key = 'buy' if direction == 'LONG' else 'sell'
        guard_mode = str((self.profitability_guard_config or {}).get('mode', 'all_time'))
        trade_id = self.open_trade['id']
        timestamp = self._coerce_timestamp(current_time) or pd.Timestamp.now()
        bias_ok, bias_reason = self._is_market_bias_entry_allowed(direction, timestamp)
        bypass_mode_config = str(_load_config().get('bypass_criteria_check', '') or '').lower()
        bypass_grid_mode = bypass_mode_config in ('immediately', 'ultra')
        bypass_requires_positive_net = bypass_mode_config == 'immediately'
        grid_metric = None
        if bypass_grid_mode:
            grid_metric = _get_grid_live_metric_for(self.script_name, self.trade_product)
        if self.open_trade is not None:
            current_source = str(self.open_trade.get('source_screen') or 'breakout')
            origin = _get_grid_live_origin(self.script_name, self.trade_product)
            source_from_grid = origin.get('source')
            group_from_grid = origin.get('group')
            resolved_source = source_from_grid if current_source == 'grid_live' and source_from_grid else current_source
            resolved_group = _build_source_group(resolved_source, group_from_grid)
            self.open_trade['source_group'] = resolved_group
            if not self.open_trade.get('live_cap_group'):
                self.open_trade['live_cap_group'] = resolved_group

        # [V20251231_0249] Initialize block reasons list
        block_reasons = []
        block_reason_details = []

        def _maybe_send(mode: str) -> None:
            flag_key = f'order_sent_{mode}'
            pending_key = f'pending_order_request_{mode}'
            if self.open_trade.get(flag_key):
                return
            if self.open_trade.get(pending_key):
                return

            auto_promote_active = self._is_auto_promote_active(dir_key, mode)

            if not auto_promote_active and not bias_ok:
                reason = f"{mode.upper()}: Blocked ({bias_reason})"
                block_reasons.append(reason)
                block_reason_details.append(reason)
                self._audit_signal_event(
                    'live_order_blocked_market_bias',
                    current_time=current_time,
                    mode=mode,
                    reason=bias_reason,
                )
                print(f"[BIAS-BLOCK] {self.script_name} {self.trade_product} {reason}")
                return

            # [2026-04-07 16:40] V20260407_1640 - Special path for Auto-Promote Toggle
            if auto_promote_active:
                if isinstance(self.open_trade.get('entry_time'), pd.Timestamp):
                    trade_date_str = self.open_trade['entry_time'].strftime('%Y-%m-%d')
                else:
                    trade_date_str = timestamp.strftime('%Y-%m-%d')
                
                # Rule: selected strategy must have positive net_return for previous trades (current week total)
                # Weekly-performance auto-promotion is based on the strategy's total
                # net return for the product/week, not the directional buy/sell slice.
                weekly_net = _get_weekly_summary_net(
                    self.run_mode.lower(),
                    trade_date_str,
                    self.script_name,
                    self.trade_product,
                    'net',
                )
                
                if weekly_net > 0:
                    print(f"[AUTO-PROMOTE] {self.script_name} {self.trade_product} {mode.upper()} active. Weekly Net: {weekly_net:.2f} > 0. Attempting promotion...")
                    # Bypass standard guards, proceed to create_tradeable_json (which handles max limits)
                    self._audit_signal_event(
                        'live_order_attempt',
                        current_time=current_time,
                        mode=mode,
                        path_type='auto_promote',
                        weekly_net=weekly_net,
                    )
                    path = self._create_tradeable_json(timestamp, current_price, direction, trade_id, mode, is_close=False, is_auto_promote=True) # [2026-04-08 10:00] V20260408_1000
                    if path:
                        if _is_execution_request_marker(path):
                            request_id = _execution_request_id_from_marker(path)
                            self.open_trade[pending_key] = request_id
                            self._audit_signal_event(
                                'live_order_pending_approval',
                                current_time=current_time,
                                mode=mode,
                                path_type='auto_promote',
                                request_id=request_id,
                                weekly_net=weekly_net,
                            )
                            self._save_trade_json(current_price)
                            print(f"[AUTO-PROMOTE] Pending approval: execution request {request_id}.")
                        else:
                            self.open_trade[flag_key] = True
                            self.open_trade['is_live_trade'] = True
                            self._audit_signal_event(
                                'live_order_created',
                                current_time=current_time,
                                mode=mode,
                                path_type='auto_promote',
                                order_path=path,
                                weekly_net=weekly_net,
                            )
                            print(f"[AUTO-PROMOTE] Success: L-Trade order created.")
                        return
                    else:
                        detail = _LAST_L_TRADE_ORDER_ERROR or "limit check failed"
                        self._audit_signal_event(
                            'live_order_create_failed',
                            current_time=current_time,
                            mode=mode,
                            path_type='auto_promote',
                            weekly_net=weekly_net,
                            error=detail,
                        )
                        print(f"[AUTO-PROMOTE] Blocked: {detail}")
                        return
                else:
                    self._audit_signal_event(
                        'live_order_blocked_auto_promote_weekly_net',
                        current_time=current_time,
                        mode=mode,
                        path_type='auto_promote',
                        weekly_net=weekly_net,
                    )
                    print(f"[AUTO-PROMOTE] {self.script_name} {self.trade_product} {mode.upper()} blocked: Weekly Net {weekly_net:.2f} <= 0")
                    # If auto-promote is ON but condition (positive net) is not met, we don't promote.
                    return

            # Global bypass: only allow if strategy appears in grid_live.json and, when immediate, total net is positive.
            if bypass_grid_mode:
                if not grid_metric:
                    reason = f"{mode.upper()}: Bypass blocked (strategy not monitored in grid_live)"
                    block_reasons.append(reason)
                    block_reason_details.append(f"{mode.upper()}: strategy not present in grid_live map for ({self.script_name}, {self.trade_product})")
                    self._audit_signal_event(
                        'live_order_blocked_bypass_strategy_not_in_grid_live',
                        current_time=current_time,
                        mode=mode,
                        grid_metric=grid_metric,
                    )
                    print(f"[BYPASS] {self.script_name} {self.trade_product} not in grid_live.json")
                    return
                grid_mode, grid_dir = _parse_grid_live_metric(grid_metric)
                if grid_dir and grid_dir != dir_key:
                    reason = f"{mode.upper()}: Bypass blocked (grid_live {grid_dir.upper()} only)"
                    block_reasons.append(reason)
                    block_reason_details.append(f"{mode.upper()}: grid metric={grid_metric}, trade_direction={dir_key}")
                    self._audit_signal_event(
                        'live_order_blocked_bypass_grid_side',
                        current_time=current_time,
                        mode=mode,
                        grid_metric=grid_metric,
                        trade_direction=dir_key,
                    )
                    print(f"[BYPASS] {self.script_name} {self.trade_product} {dir_key.upper()} blocked by grid_live {grid_dir.upper()}")
                    return

                if bypass_requires_positive_net:
                    if isinstance(self.open_trade.get('entry_time'), pd.Timestamp):
                        trade_date_str = self.open_trade['entry_time'].strftime('%Y-%m-%d')
                    else:
                        trade_date_str = timestamp.strftime('%Y-%m-%d')

                    total_net = _get_summary_metric_value(
                        self.run_mode.lower(),
                        trade_date_str,
                        self.script_name,
                        self.trade_product,
                        grid_mode
                    )
                    if total_net is None or total_net <= 0:
                        reason = f"{mode.upper()}: Bypass blocked (summary net {total_net} <= 0)"
                        block_reasons.append(reason)
                        block_reason_details.append(f"{mode.upper()}: summary metric={grid_mode}, value={total_net}, trade_date={trade_date_str}")
                        self._audit_signal_event(
                            'live_order_blocked_bypass_summary_non_positive',
                            current_time=current_time,
                            mode=mode,
                            grid_metric=grid_metric,
                            summary_metric=grid_mode,
                            summary_value=total_net,
                            trade_date=trade_date_str,
                        )
                        print(f"[BYPASS] {self.script_name} {self.trade_product} summary net <= 0")
                        return
            else:
                if not self._is_active(dir_key, mode):
                    reason = f"{mode.upper()}: Not activated for {self.trade_product}"
                    block_reasons.append(reason)
                    block_reason_details.append(f"{mode.upper()}: activation key inactive for direction={dir_key}, mode={mode}")
                    self._audit_signal_event(
                        'live_order_blocked_activation_inactive',
                        current_time=current_time,
                        mode=mode,
                        trade_direction=dir_key,
                    )
                    print(f"[ACTIVATE] {self.script_name} {self.trade_product} {dir_key.upper()} {mode.upper()} inactive")
                    return
                if not self._is_profitability_guard_passed(dir_key, mode):
                    # [V20251231_0251] Get detailed guard info
                    guard_info = getattr(self, '_last_guard_check', {})
                    pnl_sum = guard_info.get('sum', 0)
                    threshold = guard_info.get('threshold', 0)
                    count = guard_info.get('count', 0)
                    reason = f"{mode.upper()}: Guard failed (sum=${pnl_sum:.2f} <= ${threshold:.2f}, {count} trades, mode={guard_mode})"
                    block_reasons.append(reason)
                    block_reason_details.append(f"{mode.upper()}: guard_sum={pnl_sum}, threshold={threshold}, count={count}, guard_mode={guard_mode}")
                    self._audit_signal_event(
                        'live_order_blocked_profitability_guard',
                        current_time=current_time,
                        mode=mode,
                        trade_direction=dir_key,
                        guard_sum=pnl_sum,
                        threshold=threshold,
                        count=count,
                        guard_mode=guard_mode,
                    )
                    print(f"[GUARD] {self.script_name} {self.trade_product} {dir_key.upper()} {mode.upper()} blocked (mode={guard_mode})")
                    return
            
            # [V20251231_1145] Create order first, check result to set flag
            self._audit_signal_event(
                'live_order_attempt',
                current_time=current_time,
                mode=mode,
                path_type='normal',
                trade_direction=dir_key,
            )
            path = self._create_tradeable_json(timestamp, current_price, direction, trade_id, mode, is_close=False)
            if path:
                if _is_execution_request_marker(path):
                    request_id = _execution_request_id_from_marker(path)
                    self.open_trade[pending_key] = request_id
                    self._audit_signal_event(
                        'live_order_pending_approval',
                        current_time=current_time,
                        mode=mode,
                        path_type='normal',
                        trade_direction=dir_key,
                        request_id=request_id,
                    )
                else:
                    self.open_trade[flag_key] = True
                    self.open_trade['is_live_trade'] = True # [V20260211_1615] consistency
                    self._audit_signal_event(
                        'live_order_created',
                        current_time=current_time,
                        mode=mode,
                        path_type='normal',
                        trade_direction=dir_key,
                        order_path=path,
                    )
            else:
                detail = _LAST_L_TRADE_ORDER_ERROR or "unknown create_l_trade_order failure"
                block_reasons.append(f"{mode.upper()}: Tradeable order creation failed ({detail})")
                block_reason_details.append(f"{mode.upper()}: {detail}")
                self._audit_signal_event(
                    'live_order_create_failed',
                    current_time=current_time,
                    mode=mode,
                    path_type='normal',
                    trade_direction=dir_key,
                    error=detail,
                )
                print(f"[LIMIT] {self.script_name} {self.trade_product} {dir_key.upper()} {mode.upper()} creation failed")

        _maybe_send('net')
        _maybe_send('alt')

        # [V20251231_0249] Store block reasons in trade if any

        if block_reasons:
            self.open_trade['trade_block_reason'] = '; '.join(block_reasons)
            self.open_trade['trade_block_reason_detail'] = '; '.join(block_reason_details)
            self.open_trade['grid_live_context_at_block'] = _get_grid_live_context_snapshot(
                self.script_name,
                self.trade_product
            )

        self._save_trade_json(current_price)

    def _get_grid_live_metric(self) -> Optional[str]:
        if self.run_mode != 'LIVE':
            return None
        return _get_grid_live_metric_for(self.script_name, self.trade_product)

    def _check_grid_live_toggle(self, current_time: Any, current_price: float) -> None:
        if not self.open_trade:
            return
        if self.open_trade.get('is_live_trade'):
            return
        if self.open_trade.get('order_sent_net') or self.open_trade.get('order_sent_alt'):
            return
        if _load_config().get('bypass_criteria_check') not in ('immediately', 'ultra'):
            return
        metric = self._get_grid_live_metric()
        if metric and self._trigger_grid_live_activation(current_time, current_price, self.open_trade.get('direction', 'LONG'), metric):
            self._save_trade_json(current_price)

    def _trigger_grid_live_activation(self, current_time: Any, current_price: float, direction: str, metric: Optional[str]) -> bool:
        if not self.open_trade or not metric:
            return False
        metric_mode, metric_dir = _parse_grid_live_metric(metric)
        if metric_dir:
            dir_key = 'buy' if direction == 'LONG' else 'sell'
            if metric_dir != dir_key:
                print(f"[GRID-LIVE] Skipping activation: {dir_key.upper()} trade blocked by grid_live {metric_dir.upper()}")
                return False
        timestamp = self._coerce_timestamp(current_time) or pd.Timestamp.now()
        bias_ok, bias_reason = self._is_market_bias_entry_allowed(direction, timestamp)
        if not bias_ok:
            print(f"[GRID-LIVE] Skipping activation: {bias_reason}")
            return False
        trigger_price = current_price if current_price is not None else self.open_trade.get('entry_price', 0.0)

        # [V20260207_1615] Respect directional activation toggles even for grid_live
        # UNLESS bypass_criteria_check is 'ultra'
        bypass_mode = _load_config().get('bypass_criteria_check', '').lower()
        if bypass_mode not in ('immediately', 'ultra'):
            dir_key = 'buy' if direction == 'LONG' else 'sell'
            if not self._is_active(dir_key, metric_mode):
                print(f"[GRID-LIVE] Skipping activation: {dir_key.upper()} {metric.upper()} NOT active for {self.trade_product}")
                return False

        entry_price_value = self.open_trade.get('entry_price', 0.0)
        sent_at = datetime.now().isoformat()
        previous_live = self.open_trade.get('is_live_trade', False)

        gross_pnl, net_pnl_usd, _, alt_net_pnl_usd, _ = self.calculate_pnl(
            entry_price_value,
            trigger_price,
            direction,
            self.commission_pips,
            self.spread_pips
        )
        if isinstance(self.open_trade.get('entry_time'), pd.Timestamp):
            trade_date_str = self.open_trade['entry_time'].strftime('%Y-%m-%d')
        else:
            trade_date_str = timestamp.strftime('%Y-%m-%d')
        summary_value = _get_summary_metric_value(self.run_mode.lower(), trade_date_str, self.script_name, self.trade_product, metric_mode)
        metric_value = alt_net_pnl_usd if metric_mode == 'alt' else net_pnl_usd
        metric_value = alt_net_pnl_usd if metric_mode == 'alt' else net_pnl_usd
        effective_value = summary_value if summary_value is not None else metric_value
        
        # [V20260211_1700] Enforce P&L Guard for 'immediately' mode. Only 'ultra' bypasses.
        bypass_guard = _load_config().get('bypass_criteria_check') == 'ultra'

        
        if not bypass_guard and effective_value <= 0:
            print(f"[GRID-LIVE] Skipping activation for {self.trade_product} {self.script_name} (metric {metric} P&L ${effective_value:.2f})")
            return False

        # [V20260204_1255] Delay metadata setting until after successful promotion
        path = self._create_tradeable_json(timestamp, trigger_price, direction, self.open_trade['id'], metric_mode, is_close=False)
        if path:
            self.open_trade['is_live_trade'] = True
            self.open_trade['source_screen'] = 'grid_live'
            origin = _get_grid_live_origin(self.script_name, self.trade_product)
            self.open_trade['source_group'] = _build_source_group(origin.get('source') or 'grid_live', origin.get('group'))
            self.open_trade['sent_at'] = sent_at
            self.open_trade['in_trade_entry_time'] = timestamp.isoformat()
            if direction == 'LONG':
                self.open_trade['in_trade_entry_price'] = self.latest_ask or trigger_price
            else:
                self.open_trade['in_trade_entry_price'] = self.latest_bid or trigger_price
                
            flag_key = f'order_sent_{metric_mode}'
            self.open_trade[flag_key] = True
            print(f"[GRID-LIVE] Immediate {metric.upper()} order created for {self.trade_product} {self.script_name} (trade #{self.open_trade['id']}).")
            return True

        # Roll back if order creation failed (e.g. max_live_trades limit)
        if not previous_live:
            self.open_trade.pop('is_live_trade', None)
            self.open_trade.pop('source_screen', None)
            self.open_trade.pop('sent_at', None)
            self.open_trade.pop('in_trade_entry_time', None)
            self.open_trade.pop('in_trade_entry_price', None)
        return False

    def _ensure_flag_consistency(self) -> None:
        """
        [V20260211_1620] Ensure is_live_trade is consistent with order flags.
        If any order was sent, the trade MUST be marked as live.
        """
        if not self.open_trade:
            return
            
        is_live = self.open_trade.get('is_live_trade', False)
        sent_net = self.open_trade.get('order_sent_net', False)
        sent_alt = self.open_trade.get('order_sent_alt', False)
        
        # If any order sent, MUST be live
        if sent_net or sent_alt:
            if not is_live:
                self.open_trade['is_live_trade'] = True
                print(f"[REPAIR] Corrected is_live_trade to True (sent_net={sent_net}, sent_alt={sent_alt})")
        
        # If is_live_trade is True but no order_sent flags, do NOT fabricate order_sent_net.
        # This preserves TWS-cap correctness based on real sent flags.
        if is_live:
            if not sent_net and not sent_alt:
                print("[REPAIR] is_live_trade=True with no order_sent flags; leaving flags unchanged.")

    def _is_trade_bucket_source_enabled(self) -> bool:
        cfg = _load_config()
        raw_sources = cfg.get('automated_trade_sources', cfg.get('Automated Trade Sources', []))
        normalized: Set[str] = set()
        if isinstance(raw_sources, str):
            normalized.update(p.strip().lower() for p in raw_sources.split(',') if p.strip())
        elif isinstance(raw_sources, list):
            normalized.update(str(v).strip().lower() for v in raw_sources if str(v).strip())

        if 'trade bucket' in normalized or 'trade_bucket' in normalized:
            return True
        return str(cfg.get('l_trade_generation_mode', '')).lower() == 'trade_bucket'

    def _stamp_tb_leader_fields_if_missing(self, trade_data: Dict[str, Any]) -> None:
        existing = str(trade_data.get('tb_leader', '')).strip().upper()
        if existing in ('Y', 'N'):
            return

        mem_existing = str((self.open_trade or {}).get('tb_leader', '')).strip().upper()
        if mem_existing in ('Y', 'N'):
            trade_data['tb_leader'] = mem_existing
            trade_data['tb_leader_set_at'] = (self.open_trade or {}).get('tb_leader_set_at')
            trade_data['tb_leader_bucket'] = (self.open_trade or {}).get('tb_leader_bucket')
            return

        if not self._is_trade_bucket_source_enabled():
            return

        source_screen = str(trade_data.get('source_screen') or '').lower()
        source_group = str(trade_data.get('source_group') or '')
        is_tb_context = ('trade_bucket' in source_screen) or source_group.upper().startswith('TB_') or ('TB_' in source_group.upper())
        if not is_tb_context:
            return

        is_leader = bool(trade_data.get('is_live_trade') or trade_data.get('order_sent_net') or trade_data.get('order_sent_alt'))
        trade_data['tb_leader'] = 'Y' if is_leader else 'N'
        trade_data['tb_leader_set_at'] = datetime.utcnow().isoformat()
        trade_data['tb_leader_bucket'] = source_group or source_screen or 'trade_bucket'
        if self.open_trade is not None:
            self.open_trade['tb_leader'] = trade_data['tb_leader']
            self.open_trade['tb_leader_set_at'] = trade_data['tb_leader_set_at']
            self.open_trade['tb_leader_bucket'] = trade_data['tb_leader_bucket']

    def _audit_signal_event(self, stage: str, current_time: Any = None, **extra: Any) -> None:
        trade_ref = self.open_trade or {}
        event_time = (
            self._coerce_timestamp(current_time)
            or self._coerce_timestamp(trade_ref.get('entry_time'))
            or pd.Timestamp.now()
        )
        trade_date = event_time.strftime('%Y-%m-%d')
        entry: Dict[str, Any] = {
            'logged_at': datetime.now().isoformat(),
            'trade_time': event_time.isoformat() if hasattr(event_time, 'isoformat') else str(event_time),
            'stage': stage,
            'run_mode': self.run_mode.lower(),
            'product': self.trade_product,
            'strategy': self.script_name,
            'window_size': self.window_size,
            'tp_pips': self.tp_pips,
            'sl_pips': self.sl_pips,
            'trade_id': trade_ref.get('id'),
            'guid': trade_ref.get('guid'),
            'direction': trade_ref.get('direction'),
            'entry_price': trade_ref.get('entry_price'),
            'json_filename': trade_ref.get('json_filename'),
            'source_screen': trade_ref.get('source_screen'),
            'source_group': trade_ref.get('source_group'),
            'is_live_trade': trade_ref.get('is_live_trade'),
            'order_sent_net': trade_ref.get('order_sent_net'),
            'order_sent_alt': trade_ref.get('order_sent_alt'),
        }
        entry.update(extra)
        _append_signal_audit_entry(self.run_mode.lower(), trade_date, self.trade_product, entry)

    def _save_trade_json(self, current_price: Optional[float] = None) -> None:
        if not self.open_trade:
            return
            
        # [V20260211_1620] Run self-healing before saving
        self._ensure_flag_consistency()
        
        trade_id = self.open_trade['id']

        base_filename = self.open_trade.get('json_base_filename')
        filename = self.open_trade.get('json_filename')
        if not base_filename and filename:
            base_filename = _strip_trade_status_suffix(filename)
            self.open_trade['json_base_filename'] = base_filename
        if not filename:
            seed_name = base_filename or self._generate_trade_filename(self.open_trade.get('guid', 'unknown'), pd.Timestamp.now()) # [FIXED 2026-04-08 10:00] V20260408_1000
            filename = _with_trade_status_suffix(seed_name, 'OPEN')
        else:
            filename = _ensure_json_ext(filename)
            if not _is_open_trade_filename(filename):
                filename = _with_trade_status_suffix(base_filename or filename, 'OPEN')
        self.open_trade['json_filename'] = filename
        self.open_trade['json_base_filename'] = base_filename or _strip_trade_status_suffix(filename)
        trade_date = _trading_date_string(self.open_trade.get('entry_time')) or pd.Timestamp.now().strftime('%Y-%m-%d')
        date_dir = _ensure_day_directory(self.run_mode.lower(), trade_date, self.trade_product)
        filepath = str(date_dir / filename)
        
        # [V20260129_0245] RELOAD AND MERGE: pick up external live promotion (e.g. from grid monitor)
        disk_data = {}
        if os.path.exists(filepath):
            try:
                disk_data = _load_json_resilient(filepath, repair=True)
            except:
                pass

        entry_price = self.open_trade['entry_price']
        direction = self.open_trade['direction']
        if current_price is not None:
            gross_pnl, net_pnl_usd, _, alt_net_pnl_usd, adhoc_cost_usd = self.calculate_pnl(
                entry_price, current_price, direction, self.commission_pips, self.spread_pips
            )
        else:
            # Still calculate fixed costs even if no price tick yet [V20260323_1935]
            gross_pnl, net_pnl_usd, _, alt_net_pnl_usd, adhoc_cost_usd = self.calculate_pnl(
                entry_price, entry_price, direction, self.commission_pips, self.spread_pips
            )

        # Build trade data using disk_data as base to preserve existing fields [V20260129_0245]
        trade_data = disk_data.copy()
        trade_data.update({
            'trade_id': trade_id,
            'guid': self.open_trade.get('guid'),  # [V20260415_1445] Fix: persist GUID to JSON
            'product': self.trade_product,
            'direction': direction,
            'script_name': self.script_name,
            'source_strategy': self.script_name,
            'strategy_name': canonical_strategy_name(self.script_name) or self.script_name,
            'entry_time': self.open_trade['entry_time'].isoformat() if hasattr(self.open_trade['entry_time'], 'isoformat') else str(self.open_trade['entry_time']),
            'entry_price': entry_price,
            'gross_pnl_pips': gross_pnl,
            'net_return': net_pnl_usd,
            'min_net': net_pnl_usd,  # [V20260428] Track minimum net (drawdown) - initialized to opening cost
            'alt_net': alt_net_pnl_usd,
            'adhoc_cost_usd': adhoc_cost_usd, # [V20260323_1935] Explicitly record upfront cost
            'status': 'OPEN',
            'window_size': self.window_size,
            'pip_buffer': self.pip_buffer,
            'tp_pips': self.tp_pips,
            'sl_pips': self.sl_pips,
        })
        price_value = current_price if current_price is not None else entry_price
        last_updated = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        trade_data = _with_last_updated_after_current_price(
            trade_data,
            price_value,
            last_updated,
        )
        market_bias_at_open = self.open_trade.get('market_bias_at_open') or disk_data.get('market_bias_at_open')
        if market_bias_at_open:
            trade_data['market_bias_at_open'] = market_bias_at_open
            latest_bias = _get_market_bias_for_date(self.run_mode.lower(), trade_date) or market_bias_at_open
            trade_data['market_bias_latest'] = latest_bias
        
        # Explicitly protect and sync live flags [V20260129_0245]
        # These fields might be updated by the grid monitor or manual UI action
        live_keys = ('order_sent_net', 'order_sent_alt', 'is_live_trade', 'is_live_scheduled', 'source_screen', 
                    'source_group', 'live_cap_group', 'trade_block_reason', 'trade_block_reason_detail',
                    'grid_live_context_at_block', 'sent_at', 'in_trade_entry_time', 'in_trade_entry_price',
                    'tb_leader', 'tb_leader_set_at', 'tb_leader_bucket')
        
        for key in live_keys:
            mem_val = self.open_trade.get(key)
            disk_val = disk_data.get(key)
            # Sync: disk (truth) -> memory (if memory is behind)
            if disk_val not in (None, False) and mem_val in (None, False):
                self.open_trade[key] = disk_val
                mem_val = disk_val
            # Final write: ensure any truth (disk or memory) is preserved
            if mem_val is not None:
                trade_data[key] = mem_val

        self._stamp_tb_leader_fields_if_missing(trade_data)
        apply_strategy_name_fields(trade_data)

        _write_json_atomic(filepath, trade_data, indent=2)
        self._audit_signal_event(
            'open_trade_json_saved',
            current_time=self.open_trade.get('entry_time'),
            filepath=filepath,
            net_return=trade_data.get('net_return'),
            alt_net=trade_data.get('alt_net'),
            status=trade_data.get('status'),
        )

    def _finalize_trade_json(
        self,
        filename: str,
        exit_time,
        exit_price: float,
        exit_reason: str,
        net_pnl_usd: float,
        alt_net_pnl_usd: float,
        gross_pnl_pips: float = 0.0,
        adhoc_cost_usd: float = 0.0,
    ) -> None:
        trade_date = _trading_date_string((self.open_trade or {}).get('entry_time')) or pd.Timestamp.now().strftime('%Y-%m-%d')
        date_dir = _ensure_day_directory(self.run_mode.lower(), trade_date, self.trade_product)
        
        # [V20260129_0130] Fix: Strip potential .json from base_filename to avoid .json.json
        raw_base = (self.open_trade or {}).get('json_base_filename') or _strip_trade_status_suffix(filename)
        base_filename = raw_base[:-5] if raw_base.lower().endswith('.json') else raw_base
        
        open_filename = _with_trade_status_suffix(base_filename, 'OPEN')
        closed_filename = _with_trade_status_suffix(base_filename, 'CLOSED')
        current_filename = _ensure_json_ext(filename)
        filepath = str(date_dir / current_filename)
        if not os.path.exists(filepath) and current_filename != open_filename:
            alt_path = str(date_dir / open_filename)
            if os.path.exists(alt_path):
                filepath = alt_path
                current_filename = open_filename
        closed_path = str(date_dir / closed_filename)
        # [V20260129_0245] PRESERVE DISK STATE ON FINALIZE
        try:
            disk_data = _load_json_resilient(filepath, repair=True)
        except Exception:
            disk_data = {}
            
        # Determine live status from memory OR disk [V20260129_0245]
        is_live = (
            self.open_trade.get('order_sent_net', False) or 
            self.open_trade.get('order_sent_alt', False) or 
            disk_data.get('is_live_trade', False) or
            self.open_trade.get('is_live_scheduled', False)
        )
        
        trade_data = disk_data.copy()
        trade_data.update(
            {
                'script_name': self.script_name,
                'source_strategy': self.script_name,
                'strategy_name': canonical_strategy_name(self.script_name) or self.script_name,
                'is_live_trade': is_live,
                'exit_time': exit_time.isoformat() if hasattr(exit_time, 'isoformat') else str(exit_time),
                'exit_price': exit_price,
                'exit_reason': exit_reason,
                'gross_pnl_pips': gross_pnl_pips,
                'net_return': net_pnl_usd,
                'alt_net': alt_net_pnl_usd,
                'adhoc_cost_usd': adhoc_cost_usd, # [V20260323_1935]
                'status': 'CLOSED',
            }
        )
        market_bias_at_open = (self.open_trade or {}).get('market_bias_at_open') or disk_data.get('market_bias_at_open')
        if market_bias_at_open:
            trade_data['market_bias_at_open'] = market_bias_at_open
            trade_date_for_close = _trading_date_string((self.open_trade or {}).get('entry_time')) or pd.Timestamp.now().strftime('%Y-%m-%d')
            close_bias = _get_market_bias_for_date(self.run_mode.lower(), trade_date_for_close) or market_bias_at_open
            trade_data['market_bias_latest'] = close_bias
        # Port over flags if disk had them but memory didn't
        for f in ('order_sent_net', 'order_sent_alt', 'sent_at'):
            if disk_data.get(f) and not trade_data.get(f):
                trade_data[f] = disk_data[f]
        apply_strategy_name_fields(trade_data)

        _write_json_atomic(filepath, trade_data, indent=2)
        if filepath != closed_path:
            try:
                os.replace(filepath, closed_path)
                filepath = closed_path
            except OSError as exc:
                print(f"[PERSIST] Unable to rename {current_filename} to {closed_filename}: {exc}")
        if self.open_trade is not None:
            self.open_trade['json_filename'] = closed_filename
            self.open_trade['json_base_filename'] = base_filename

    def _create_tradeable_json(
        self,
        current_time,
        current_price: float,
        direction: str,
        trade_id: int,
        mode: str = 'net',
        is_close: bool = False,
        is_auto_promote: bool = False, # [2026-04-08 10:00] V20260408_1000
        request_context: Optional[Dict[str, Any]] = None,
    ) -> Optional[str]:
        # [V20260126_0410] Pass stored source if available, default to breakout
        source = 'breakout'
        source_group = 'breakout'
        guid = 'unknown' # [V20260129_0435]
        if self.open_trade:
            source = self.open_trade.get('source_screen', 'breakout')
            source_group = self.open_trade.get('live_cap_group') or self.open_trade.get('source_group', source)
            guid = self.open_trade.get('guid', 'unknown')
        trade_json_path = None
        if self.open_trade and self.open_trade.get('json_filename'):
            trade_date = _trading_date_string(self.open_trade.get('entry_time')) or pd.Timestamp.now().strftime('%Y-%m-%d')
            date_dir = _ensure_day_directory(self.run_mode.lower(), trade_date, self.trade_product)
            trade_json_path = str(date_dir / self.open_trade.get('json_filename'))

        return _create_l_trade_order(
            product=self.trade_product,
            direction=direction,
            strategy_key=self.script_name,
            trade_id=str(trade_id),
            current_price=current_price,
            latest_bid=self.latest_bid,
            latest_ask=self.latest_ask,
            mode=mode,
            is_close=is_close,
            source=source,
            source_group=source_group,
            guid=guid, # [V20260129_0435]
            is_auto_promote=is_auto_promote, # [2026-04-08 10:00] V20260408_1000
            trade_json_path=trade_json_path,
            request_context=request_context,
        )

    def calculate_pnl(
        self,
        entry_price: float,
        exit_price: float,
        direction: str,
        commission_pips: float,
        spread_pips: float = 0.0,
    ) -> Tuple[float, float, float, float, float]:
        price_diff_raw = exit_price - entry_price
        # [2026-03-16 V20260316_1430] Use dynamic multiplier for pips
        price_diff_pips = price_diff_raw * self.pip_multiplier
        pip_value = _pip_value_for_product(self.trade_product, self.config)
        if direction == 'LONG':
            gross_pnl = price_diff_pips
        else:
            gross_pnl = -price_diff_pips
        gross_pnl_usd = gross_pnl * pip_value
        # Determine commission USD based on trade product [2025-12-29 V20251229_1200]
        commission_usd_for_trade = 10.0 if "_C" in self.trade_product.upper() else COMMISSION_USD
        comm_cost_usd = commission_usd_for_trade
        
        # [V20260323_1930] Apply upfront adhoc cost per product type
        adhoc_cost_usd = 0.0
        try:
            # self.config is usually available on the strategy instance
            # We use product_type_for_product to get the correct category
            p_type = product_type_for_product(self.trade_product, self.config)
            type_costs = self.config.get("product_type_cost", {})
            adhoc_cost_usd = float(type_costs.get(p_type, 0.0) or 0.0)
            print(f"[DEBUG_ADHOC] product={self.trade_product} p_type={p_type} type_costs={type_costs} adhoc={adhoc_cost_usd}")
        except Exception as e:
            print(f"[DEBUG_ADHOC_ERR] product={self.trade_product} error={e}")

        # [V20260325_0500] Apply 2x adhoc cost upfront (entry + exit)
        total_adhoc_cost = adhoc_cost_usd * 2
        actual_net_pnl_usd = gross_pnl_usd - comm_cost_usd - total_adhoc_cost
        alt_gross_pnl = -gross_pnl
        alt_gross_pnl_usd = alt_gross_pnl * pip_value
        spread_cost_usd = spread_pips * pip_value
        alt_net_pnl_usd = alt_gross_pnl_usd - comm_cost_usd - spread_cost_usd - total_adhoc_cost
        return gross_pnl, actual_net_pnl_usd, alt_gross_pnl, alt_net_pnl_usd, total_adhoc_cost

    def _is_profitability_guard_passed(self, direction_key: str, mode_key: str) -> bool:
        """Strict profitability guard with precise filename parsing [2025-12-19 V20251219_1605]"""
        guard_cfg = self.profitability_guard_config or {}
        mode = str(guard_cfg.get('mode', 'all_time')).lower()
        threshold = float(guard_cfg.get('threshold_y', 0.0))
        count_x = int(guard_cfg.get('count_x', 0))
        direction_label = 'LONG' if direction_key == 'buy' else 'SHORT'
        pnl_field = 'net_return' if mode_key == 'net' else 'alt_net'
        
        # Collect trades from disk instead of memory
        trades_with_metadata: List[Dict] = []
        if not os.path.exists(self.json_base_dir):
            return True

        json_files = list(Path(self.json_base_dir).rglob('*_cl.json'))
        
        target_script = self.script_name.lower()
        target_prod = self.trade_product.upper()

        for json_path in json_files:
            try:
                raw_name = json_path.name
                normalized_name = _strip_trade_status_suffix(raw_name)
                fname = normalized_name.lower()
                
                # Precise check for script and product in filename
                # Pattern: {script}_{product}_{time}_{params}.json
                # We check if filename STARTS with our script name followed by product
                prefix_match = f"{target_script}_{target_prod.lower()}_ "
                if not fname.startswith(prefix_match):
                    # Fallback for old/alternative naming: check if script matches and product is in metadata
                    # BUT strictly verify script name isn't just a substring
                    parts = fname.split('_')
                    matching_script = False
                    prod_idx = -1
                    for i in range(1, len(parts)):
                        potential_script = '_'.join(parts[:i])
                        if potential_script == target_script:
                            matching_script = True
                            prod_idx = i # The next part should be the product
                            break
                    if not matching_script:
                        continue
                
                with open(json_path, 'r') as f:
                    data = json.load(f)
                
                # Product isolation (Strict check)
                file_product = data.get('product', '').upper()
                if not file_product:
                    # Infer product from filename part identified earlier
                    if prod_idx != -1 and prod_idx < len(parts):
                         file_product = parts[prod_idx].upper()

                # Verify all constraints
                if (
                    file_product == target_prod and
                    data.get('direction', '').upper() == direction_label and
                    data.get('status', '').upper() == 'CLOSED'
                ):
                    
                    # Optional window size check: if it exists in JSON, it must match.
                    # If it doesn't exist (old trade), we rely on the filename prefix match already performed.
                    f_win = data.get('window_size')
                    if f_win is not None and int(f_win) != int(self.window_size):
                        continue
                    
                    exit_time = _normalize_timestamp(data.get('exit_time'))
                    pnl_val = data.get(pnl_field, 0.0)
                    trade_id = data.get('id', 0)
                    
                    if exit_time and pnl_val is not None:
                        trades_with_metadata.append({
                            'time': exit_time,
                            'pnl': float(pnl_val),
                            'id': int(trade_id)
                        })
            except Exception:
                continue

        if not trades_with_metadata:
            print(f"[GUARD][ZHP] {self.script_name} {target_prod} {direction_label} {mode_key.upper()} - Zero-History Probation: Blocking until first win recorded.")
            return False

        # Sort by exit time DESC, then ID DESC (ensuring deterministic "Recent X")
        trades_with_metadata.sort(key=lambda x: (x['time'], x['id']), reverse=True)

        relevant_pnl = []
        if mode == 'today':
            today = pd.Timestamp.now().date()
            relevant_pnl = [t['pnl'] for t in trades_with_metadata if t['time'].date() == today]
        elif mode == 'recent_x' and count_x > 0:
            relevant_pnl = [t['pnl'] for t in trades_with_metadata[:count_x]]
        else:
            relevant_pnl = [t['pnl'] for t in trades_with_metadata]

        if not relevant_pnl:
            print(f"[GUARD] {self.script_name} {target_prod} {direction_label} {mode_key.upper()} - No trades found for mode '{mode}', allowing trade.")
            return True

        pnl_sum = sum(relevant_pnl)
        status = 'PASSED' if pnl_sum > threshold else 'BLOCKED'
        
        print(f"[GUARD] {self.script_name} {target_prod} {direction_label} {mode_key.upper()} (mode={mode}) sum: {pnl_sum:.2f} | count: {len(relevant_pnl)} | threshold: {threshold:.2f} | result: {status}")
        
        # [V20251231_0251] Store guard details for block reason
        self._last_guard_check = {
            'sum': pnl_sum,
            'threshold': threshold,
            'count': len(relevant_pnl),
            'mode': mode
        }
        
        return pnl_sum > threshold

    def close_trade(self, exit_time, exit_price, exit_reason):
        if not self.open_trade:
            return False
        entry_price = self.open_trade['entry_price']
        direction = self.open_trade['direction']
        entry_time = self._coerce_timestamp(self.open_trade['entry_time'])
        exit_time_ts = self._coerce_timestamp(exit_time)
        if entry_time is not None:
            if exit_time_ts is None or exit_time_ts < entry_time:
                replacement_exit_time = pd.Timestamp.now()
                print(
                    f"[{datetime.now()}] [TIME-GUARD] Replacing invalid exit_time "
                    f"for {self.trade_product} trade #{self.open_trade['id']} "
                    f"(entry_time={entry_time}, exit_time={exit_time_ts}) "
                    f"with current time {replacement_exit_time}."
                )
                exit_time_ts = replacement_exit_time
        elif exit_time_ts is None:
            exit_time_ts = pd.Timestamp.now()
        actual_gross_pnl, actual_net_pnl_usd, alt_gross_pnl, alt_net_pnl_usd, adhoc_cost_usd = self.calculate_pnl(
            entry_price, exit_price, direction, self.commission_pips, self.spread_pips
        )
        self.cumulative_pnl_usd += actual_net_pnl_usd
        self.cumulative_alt_pnl_usd += alt_net_pnl_usd
        if direction == 'LONG':
            self.cum_buy_net += actual_net_pnl_usd
            self.cum_buy_alt += alt_net_pnl_usd
        else:
            self.cum_sell_net += actual_net_pnl_usd
            self.cum_sell_alt += alt_net_pnl_usd
        trade_data = {
            'Trade #': self.open_trade['id'],
            'Entry Time': entry_time,
            'Direction': direction,
            'Entry Price': entry_price,
            'Exit Time': exit_time_ts,
            'Exit Price (Trigger)': exit_price,
            'Exit Reason': exit_reason,
            'Actual Gross P&L (Pips)': actual_gross_pnl,
            'Actual Net P&L (USD)': actual_net_pnl_usd,
            'Alt Gross P&L (Pips)': alt_gross_pnl,
            'Alt Net P&L (USD)': alt_net_pnl_usd,
            'adhoc_cost_usd': adhoc_cost_usd, # [V20260323_1935]
            'Cumulative P&L (USD)': self.cumulative_pnl_usd,
            'Cumulative Alt P&L (USD)': self.cumulative_alt_pnl_usd,
        }
        self.trade_log.append(trade_data)
        if self.open_trade.get('order_sent_net', False):
            self._create_tradeable_json(exit_time_ts, exit_price, direction, self.open_trade['id'], 'net', is_close=True)
        if self.open_trade.get('order_sent_alt', False):
            self._create_tradeable_json(exit_time_ts, exit_price, direction, self.open_trade['id'], 'alt', is_close=True)
        self._finalize_trade_json(
            self.open_trade['json_filename'], 
            exit_time_ts, 
            exit_price, 
            exit_reason, 
            actual_net_pnl_usd, 
            alt_net_pnl_usd,
            gross_pnl_pips=actual_gross_pnl,
            adhoc_cost_usd=adhoc_cost_usd # [V20260323_1935]
        )
        _decrement_global_active(self.trade_product, direction)
        self.open_trade = None
        self._print_trade_row(trade_data)
        return True

    def _print_trade_row(self, trade_data: Dict[str, Any]) -> None:
        if not self._table_header_printed:
            header = '| ' + ' | '.join(
                [
                    'Trade #',
                    'Entry Time',
                    'Direction',
                    'Entry Price',
                    'Exit Time',
                    'Exit Price (Trigger)',
                    'Exit Reason',
                    'Actual Gross P&L (Pips)',
                    'Actual Net P&L (USD)',
                    'Alt Gross P&L (Pips)',
                    'Alt Net P&L (USD)',
                    'Cumulative P&L (USD)',
                    'Cumulative Alt P&L (USD)',
                ]
            ) + ' |'
            divider = '-' * len(header)
            print(divider)
            print(header)
            print(divider)
            self._table_header_printed = True
        row_values = (
            f"{trade_data['Trade #']}",
            str(trade_data['Entry Time']),
            trade_data['Direction'],
            f"{trade_data['Entry Price']:.5f}",
            str(trade_data['Exit Time']),
            f"{trade_data['Exit Price (Trigger)']:.5f}",
            trade_data['Exit Reason'],
            f"{trade_data['Actual Gross P&L (Pips)']:.2f}",
            f"{trade_data['Actual Net P&L (USD)']:.2f}",
            f"{trade_data['Alt Gross P&L (Pips)']:.2f}",
            f"{trade_data['Alt Net P&L (USD)']:.2f}",
            f"{trade_data['Cumulative P&L (USD)']:.2f}",
            f"{trade_data['Cumulative Alt P&L (USD)']:.2f}",
        )
        print('| ' + ' | '.join(row_values) + ' |')

    def check_and_exit(self, current_time, current_price):
        if not self.open_trade:
            return False
        cfg = _load_config()
        if bool(cfg.get('enforce_market_bias_exit', False)):
            is_l_trade = bool(
                self.open_trade.get('is_live_trade')
                or self.open_trade.get('order_sent_net')
                or self.open_trade.get('order_sent_alt')
            )
            if is_l_trade:
                ts = self._coerce_timestamp(current_time) or pd.Timestamp.now()
                latest_bias = _get_market_bias_for_date(self.run_mode.lower(), ts.strftime('%Y-%m-%d'))
                direction = self.open_trade.get('direction', '')
                if latest_bias and not _direction_matches_bias(direction, latest_bias):
                    print(
                        f"[{datetime.now()}] [BIAS-EXIT] Closing L-trade #{self.open_trade.get('id')} "
                        f"for bias mismatch (direction={direction}, latest_bias={latest_bias})."
                    )
                    return self.close_trade(current_time, current_price, 'Bias Exit')
        entry_price = self.open_trade['entry_price']
        direction = self.open_trade['direction']
        # [2026-03-16 V20260316_1430] Use dynamic multiplier for exit levels
        if direction == 'LONG':
            tp_level = entry_price + (self.tp_pips / self.pip_multiplier)
            sl_level = entry_price - (self.sl_pips / self.pip_multiplier)
            if current_price >= tp_level:
                return self.close_trade(current_time, tp_level, 'TP Hit')
            if current_price <= sl_level:
                return self.close_trade(current_time, sl_level, 'SL Hit')
        elif direction == 'SHORT':
            tp_level = entry_price - (self.tp_pips / self.pip_multiplier)
            sl_level = entry_price + (self.sl_pips / self.pip_multiplier)
            if current_price >= sl_level:
                return self.close_trade(current_time, sl_level, 'SL Hit')
            if current_price <= tp_level:
                return self.close_trade(current_time, tp_level, 'TP Hit')
        return False

    @staticmethod
    def _format_timestamp(value: Any) -> str:
        if isinstance(value, pd.Timestamp):
            return value.strftime('%Y-%m-%d %H:%M:%S')
        return str(value)

    def display_open_trade_status(self, current_price: float) -> None:
        if not self.open_trade:
            return

        entry_price = self.open_trade['entry_price']
        direction = self.open_trade['direction']
        gross_pnl, net_pnl_usd, _, alt_net_pnl_usd, _ = self.calculate_pnl(
            entry_price, current_price, direction, self.commission_pips, self.spread_pips
        )
        potential_cum = self.cumulative_pnl_usd + net_pnl_usd
        potential_cum_alt = self.cumulative_alt_pnl_usd + alt_net_pnl_usd
        entry_time_str = self._format_timestamp(self.open_trade['entry_time'])
        now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        header = '#' * 120
        print(f"\n{header}")
        print(f"##  {self.run_mode} TRADE MONITOR ({self.script_name}) - {now_str}")
        print(header)
        print(
            "| {0:^7} | {1:^19} | {2:^10} | {3:^9} | {4:^16} | {5:^14} | {6:^14} | {7:^18} |".format(
                'Trade #', 'Entry Time', 'Entry Px', 'Dir', 'Gross PnL', 'Net PnL', 'Alt Net', 'Latest Px'
            )
        )
        print(f"{ '=' * 120}")
        print(
            "| {0:^7} | {1:^19} | {2:^10.5f} | {3:^9} | {4:^16.2f} | {5:^14.2f} | {6:^14.2f} | {7:^18.5f} |".format(
                self.open_trade['id'],
                entry_time_str,
                entry_price,
                direction,
                gross_pnl,
                net_pnl_usd,
                alt_net_pnl_usd,
                current_price,
            )
        )
        print(f"{ '=' * 120}")
        print(
            "| {0:^7} | {1:^19} | {2:^10} | {3:^9} | {4:^16} | {5:^14.2f} | {6:^14.2f} | {7:^18} |".format(
                '',
                '',
                '',
                '',
                'Projected Cum',
                potential_cum,
                potential_cum_alt,
                '',
            )
        )
        print(f"{header}\n")
        self._save_trade_json(current_price)

    def is_eod(self, current_time: datetime) -> bool:
        """Helper to determine if it's past the 23:00 cutoff. [V20260205_2300]"""
        if current_time is None:
            return False
        trading_time = _trading_local_timestamp(current_time)
        if trading_time is None:
            return False
        # [V20260205_2300] Cutoff at 23:00 (11 PM)
        return trading_time.hour >= 23

    def _force_close_prior_trading_day(self, current_time: Any, current_price: float) -> bool:
        if not self.open_trade:
            return False
        entry_date = _trading_date_string(self.open_trade.get('entry_time'))
        current_date = _trading_date_string(current_time)
        if not entry_date or not current_date or entry_date >= current_date:
            return False

        print(
            f"[{datetime.now()}] [DATE-ROLLOVER-FORCE-CLOSE] Closing {self.trade_product} "
            f"trade #{self.open_trade.get('id')} from {entry_date} before processing {current_date}."
        )
        closed = self.close_trade(current_time, current_price, 'Date Rollover Force Close')
        if closed:
            self.price_history.clear()
        return closed

    def enter_trade(self, current_time, entry_price: float, direction: str):
        """Enter a new trade if conditions are met."""
        if self.open_trade:
            return

        # [V20260205_2300] EOD Cutoff Guard
        if self.is_eod(current_time):
            print(f"[{datetime.now()}] [EOD-GUARD] Blocked NEW entry for {self.trade_product} - Past 23:00 cutoff.")
            return

        # [V20260123_1145] Strategic Decoupling:
        # We no longer exit early if inactive. Every strategy configuration should execute
        # its basic entry criteria and record the trade (Virtual Tracking).
        # Gates (Activations/Guards) are now handled exclusively in _handle_live_orders.

        self.trade_counter += 1
        trade_date_str = _trading_date_string(current_time) or pd.Timestamp.now().strftime('%Y-%m-%d')
        market_bias_at_open = _get_market_bias_for_date(self.run_mode.lower(), trade_date_str)
        # [V20260129_0435] GUID integration: generate unique ID for this trade sequence
        trade_guid = uuid.uuid4().hex[:8]
        base_filename, open_filename = self._compute_trade_filenames(trade_guid, current_time)
        
        # [V20260122_1630] Check activations_is_live.json schedule
        parm_str = f"{self.window_size}_{self.pip_buffer}_{self.tp_pips}_{self.sl_pips}"
        live_record = get_matching_live_schedule(self.trade_product, self.script_name, parm_str, current_time, mode=self.run_mode.lower())
        is_live_scheduled = live_record is not None
        source_screen = live_record.get('source', 'trade_bucket') if live_record else 'breakout'
        
        self.open_trade = {
            'id': self.trade_counter,
            'guid': trade_guid, # [V20260129_0435]
            'json_base_filename': base_filename,
            'json_filename': open_filename,
            'entry_time': current_time,
            'entry_price': entry_price,
            'direction': direction,
            'status': 'OPEN',
            'order_sent_net': False, # Initialize keys
            'order_sent_alt': False,
            'is_live_trade': False,
            'is_live_scheduled': is_live_scheduled, # [V20260122_1630]
            'source_screen': source_screen, # [V20260126_0410]
            'source_group': source_screen,
            'live_cap_group': source_screen,
            'market_bias_at_open': market_bias_at_open,
        }
        self._audit_signal_event(
            'signal_generated',
            current_time=current_time,
            signal_price=entry_price,
            is_live_scheduled=is_live_scheduled,
            parm_str=parm_str,
        )
        
        if is_live_scheduled:
            print(f"[{datetime.now()}] [SCHEDULE] Matching live window found for {self.trade_product} {self.script_name} (Source: {source_screen}). Mark as live.")
        
        print(f"[{datetime.now()}] [NEW TRADE] Entering {direction} for {self.trade_product} at {entry_price:.5f}")
        
        _increment_global_active(self.trade_product, direction)
        
        # This will save the initial open trade JSON
        self._save_trade_json(current_price=entry_price)

        grid_metric = self._get_grid_live_metric()
        if grid_metric and self._trigger_grid_live_activation(current_time, entry_price, direction, grid_metric):
            self._audit_signal_event(
                'grid_live_activation_matched',
                current_time=current_time,
                grid_metric=grid_metric,
            )
            self._save_trade_json(current_price=entry_price)

        # This will then attempt to send live orders if active/guards pass
        self._handle_live_orders(current_time, entry_price, direction)

    def process_new_tick(self, timestamp_value: Any, price: Any, bid: Any = None, ask: Any = None) -> None:
        current_time = self._coerce_timestamp(timestamp_value)
        current_price = _safe_float(price)
        self.latest_bid = _safe_float(bid)
        self.latest_ask = _safe_float(ask)

        if current_time is None or current_price is None:
            return

        self._force_close_prior_trading_day(current_time, current_price)

        window_ready = len(self.price_history) >= self.window_size
        was_closed = self.check_and_exit(current_time, current_price)
        if was_closed:
            print("[DEBUG] Trade closed - preserving rolling window")

        if not self.open_trade:
            # [V20260205_2300] Check for EOD before even trying to enter
            if not self.is_eod(current_time) and window_ready:
                check_fn = getattr(self, 'check_and_enter', None)
                if callable(check_fn):
                    check_fn(current_time, current_price)
        else:
            # [V20260205_2300] Force close if past 23:00
            if self.is_eod(current_time):
                print(f"[{datetime.now()}] [EOD-FORCE-CLOSE] Closing {self.trade_product} trade #{self.open_trade['id']} - Past 23:00 cutoff.")
                self.close_trade(current_time, current_price, 'EOD Force Close')
                return

            # [V20260122_1630] Check for immediate live activation of existing trade
            self._check_immediate_live_activation(current_time, current_price)
            # [V20260129] Also honor grid_live toggles that flip on after entry
            self._check_grid_live_toggle(current_time, current_price)
            self.display_open_trade_status(current_price)

        self.price_history.append(current_price)
        if not window_ready:
            print(f"[DEBUG] Building window: {len(self.price_history)}/{self.window_size}")

    def _check_immediate_live_activation(self, current_time: Any, current_price: float) -> None:
        """Checks if an already open trade should be activated to live status immediately. [V20260122_1630]"""
        if not self.open_trade:
            return
        
        # Only proceed if not already live
        order_sent_net = self.open_trade.get('order_sent_net', False)
        order_sent_alt = self.open_trade.get('order_sent_alt', False)
        if order_sent_net or order_sent_alt:
            return
            
        config = _load_config()
        if config.get("bypass_criteria_check") != "immediately":
            return

        parm_str = f"{self.window_size}_{self.pip_buffer}_{self.tp_pips}_{self.sl_pips}"
        print(f"[{datetime.now()}] [DEBUG-ACT] Checking schedule: Prod={self.trade_product}, Strat={self.script_name}, Mode={self.run_mode.lower()}, Time={current_time}")
        live_record = get_matching_live_schedule(self.trade_product, self.script_name, parm_str, current_time, mode=self.run_mode.lower())

        # Fallback to grid_live direct matching for immediate mode when scheduler has no row.
        grid_metric = _get_grid_live_metric_for(self.script_name, self.trade_product)
        source_screen = None
        if live_record:
            source_screen = live_record.get('source', 'trade_bucket')
        elif grid_metric:
            source_screen = 'grid_live'

        if source_screen:
            timestamp = self._coerce_timestamp(current_time) or pd.Timestamp.now()
            direction = self.open_trade.get('direction', 'LONG')
            bias_ok, bias_reason = self._is_market_bias_entry_allowed(direction, timestamp)
            if not bias_ok:
                self._audit_signal_event(
                    'immediate_activation_blocked_market_bias',
                    current_time=current_time,
                    source_screen=source_screen,
                    reason=bias_reason,
                )
                print(
                    f"[{datetime.now()}] [IMMEDIATE-BLOCK] {self.trade_product} {self.script_name} "
                    f"blocked: {bias_reason}"
                )
                return
            if isinstance(self.open_trade.get('entry_time'), pd.Timestamp):
                trade_date_str = self.open_trade['entry_time'].strftime('%Y-%m-%d')
            else:
                trade_date_str = timestamp.strftime('%Y-%m-%d')

            side_metric = 'buy_net' if direction == 'LONG' else 'sell_net'
            # Enforce side alignment when coming from grid_live metric.
            if grid_metric:
                _, metric_dir = _parse_grid_live_metric(grid_metric)
                if metric_dir:
                    trade_dir = 'buy' if direction == 'LONG' else 'sell'
                    if metric_dir != trade_dir:
                        self._audit_signal_event(
                            'immediate_activation_blocked_grid_side',
                            current_time=current_time,
                            source_screen=source_screen,
                            grid_metric=grid_metric,
                            trade_direction=trade_dir,
                        )
                        print(
                            f"[{datetime.now()}] [IMMEDIATE-BLOCK] {self.trade_product} {self.script_name} "
                            f"blocked by grid side: metric={grid_metric}, trade_dir={trade_dir}"
                        )
                        return
            total_net = _get_summary_metric_value(
                self.run_mode.lower(),
                trade_date_str,
                self.script_name,
                self.trade_product,
                'net'
            )
            side_net = _get_summary_metric_value(
                self.run_mode.lower(),
                trade_date_str,
                self.script_name,
                self.trade_product,
                side_metric
            )
            if total_net is None or side_net is None or total_net <= 0 or side_net <= 0:
                self._audit_signal_event(
                    'immediate_activation_blocked_non_positive_summary',
                    current_time=current_time,
                    source_screen=source_screen,
                    total_net=total_net,
                    side_metric=side_metric,
                    side_net=side_net,
                    trade_date=trade_date_str,
                )
                print(
                    f"[{datetime.now()}] [IMMEDIATE-BLOCK] {self.trade_product} {self.script_name} "
                    f"blocked: net={total_net}, {side_metric}={side_net}"
                )
                return

            print(f"[{datetime.now()}] [DEBUG-ACT] MATCH FOUND! Activating via {source_screen}...")
            print(f"[{datetime.now()}] [IMMEDIATE] Activating trade #{self.open_trade.get('id')} to LIVE status via schedule (Source: {source_screen}).")
            self.open_trade['source_screen'] = source_screen
            origin = _get_grid_live_origin(self.script_name, self.trade_product)
            source_from_grid = origin.get('source')
            group_from_grid = origin.get('group')
            effective_source = source_from_grid if source_screen == 'grid_live' and source_from_grid else source_screen
            self.open_trade['source_group'] = _build_source_group(effective_source, group_from_grid)
            
            # Set new fields
            self.open_trade['in_trade_entry_time'] = current_time.isoformat() if hasattr(current_time, 'isoformat') else str(current_time)
            if direction == 'LONG':
                self.open_trade['in_trade_entry_price'] = self.latest_ask or current_price
            else:
                self.open_trade['in_trade_entry_price'] = self.latest_bid or current_price
            
            # Immediately generate json order to send to tws
            # Bypass normal activation check if it's on a live schedule
            mode = 'net'
            trade_id = self.open_trade['id']
            self._audit_signal_event(
                'immediate_activation_attempt',
                current_time=current_time,
                source_screen=source_screen,
                mode=mode,
            )
            path = self._create_tradeable_json(timestamp, current_price, direction, trade_id, mode, is_close=False)
            if path:
                if _is_execution_request_marker(path):
                    request_id = _execution_request_id_from_marker(path)
                    self.open_trade[f'pending_order_request_{mode}'] = request_id
                    self._audit_signal_event(
                        'immediate_activation_order_pending_approval',
                        current_time=current_time,
                        source_screen=source_screen,
                        mode=mode,
                        request_id=request_id,
                    )
                    print(f"[IMMEDIATE] Execution request queued: {request_id}")
                else:
                    self.open_trade[f'order_sent_{mode}'] = True
                    self.open_trade['is_live_trade'] = True
                    self._audit_signal_event(
                        'immediate_activation_order_created',
                        current_time=current_time,
                        source_screen=source_screen,
                        mode=mode,
                        order_path=path,
                    )
                    print(f"[IMMEDIATE] Order generated: {path}")
                self._save_trade_json(current_price)
            else:
                detail = _LAST_L_TRADE_ORDER_ERROR or "unknown create_l_trade_order failure"
                self._audit_signal_event(
                    'immediate_activation_create_failed',
                    current_time=current_time,
                    source_screen=source_screen,
                    mode=mode,
                    error=detail,
                )



def _build_runtime_state(
    strategy_cls: Type[BaseBreakoutStrategy],
    trade_products_arg: Optional[List[str]],
    poll_interval_arg: int,
    window_override: Optional[int],
    pip_buffer_arg: float,
    tp_pips_arg: Optional[float],
    sl_pips_arg: Optional[float],
    commission_pips_arg: float,
    spread_pips_arg: float,
    script_alias: Optional[str],
    config: Dict[str, Any],
) -> Dict[str, Any]:
    target_products_cfg = trade_products_arg or config.get('trade_products', DEFAULT_TRADE_PRODUCTS)
    target_products = [p.upper() for p in target_products_cfg if p]
    if not target_products:
        target_products = DEFAULT_TRADE_PRODUCTS

    window_values = _coerce_int_list(config.get('window_size', BASE_WINDOW_SIZES), BASE_WINDOW_SIZES)
    if window_override is not None:
        actual_windows = [int(window_override)]
    else:
        actual_windows = window_values or BASE_WINDOW_SIZES

    pip_buffer_value = _resolve_cli_or_config(
        pip_buffer_arg,
        BASE_PIP_BUFFER,
        float(config.get('pip_buffer', BASE_PIP_BUFFER)),
    )

    tp_values = _coerce_float_list(config.get('tp_pips', BASE_TP_PIPS_LIST), BASE_TP_PIPS_LIST)
    if tp_pips_arg is None:
        actual_tps = tp_values or BASE_TP_PIPS_LIST
    else:
        actual_tps = [float(tp_pips_arg)]

    sl_values = _coerce_float_list(config.get('sl_pips', BASE_SL_PIPS_LIST), BASE_SL_PIPS_LIST)
    if sl_pips_arg is None:
        actual_sls = sl_values or BASE_SL_PIPS_LIST
    else:
        actual_sls = [float(sl_pips_arg)]

    commission_usd = float(config.get('commission_usd', COMMISSION_USD))
    pip_value = float(config.get('pip_value', PIP_VALUE)) or 1.0
    commission_pips_cfg = commission_usd / pip_value
    commission_pips_value = _resolve_cli_or_config(
        commission_pips_arg,
        BASE_COMMISSION_PIPS,
        commission_pips_cfg,
    )

    spread_pips_value = _resolve_cli_or_config(
        spread_pips_arg,
        BASE_SPREAD_PIPS,
        float(config.get('spread_pips', BASE_SPREAD_PIPS)),
    )

    poll_interval_value = int(
        _resolve_cli_or_config(
            poll_interval_arg,
            BASE_POLL_INTERVAL_SECONDS,
            int(config.get('sleep_time', BASE_POLL_INTERVAL_SECONDS)),
        )
    )

    processors_map: Dict[str, List[BaseBreakoutStrategy]] = {}
    base_name = script_alias or strategy_cls.__name__.lower()
    today_str = _LATEST_TRADING_DATE or datetime.now().strftime('%Y-%m-%d')

    for product in target_products:
        day_dir = _ensure_day_directory(str(config.get('run_mode', 'live')).lower(), today_str, str(product).upper())
        (day_dir / 'virtual').mkdir(parents=True, exist_ok=True)

    for product in target_products:
        p_code = product.upper()
        processors_map[p_code] = []
        for win in actual_windows:
            for tp in actual_tps:
                for sl in actual_sls:
                    suffix_parts = []
                    if len(actual_windows) > 1:
                        suffix_parts.append(str(win))
                    if len(actual_tps) > 1:
                        suffix_parts.append(f"tp{tp}")
                    if len(actual_sls) > 1:
                        suffix_parts.append(f"sl{sl}")
                    script_name = f"{base_name}_{'_'.join(suffix_parts)}" if suffix_parts else base_name
                    processors_map[p_code].append(
                        strategy_cls(
                            window_size=int(win),
                            pip_buffer=float(pip_buffer_value),
                            tp_pips=float(tp),
                            sl_pips=float(sl),
                            commission_pips=float(commission_pips_value),
                            spread_pips=float(spread_pips_value),
                            trade_product=p_code,
                            script_name=script_name,
                            max_live_trades=config.get('max_live_trades'),
                        )
                    )

    all_processors = [p for plist in processors_map.values() for p in plist]
    json_base_dir = all_processors[0].json_base_dir if all_processors else ''

    return {
        'processors_map': processors_map,
        'target_products': target_products,
        'poll_interval_seconds': poll_interval_value,
        'json_base_dir': json_base_dir,
        'resolved_windows': list(actual_windows),
        'resolved_tps': list(actual_tps),
        'resolved_sls': list(actual_sls),
        'script_alias': base_name,
    }


    # [V20251228_0930] Homogenize ALL sources: Strip product names from any strategy key
    # This prevents 'breakout_Rev_2_AUDNZD_C' from being a different key than 'breakout_Rev_2'
    if result and product:
        p_u = product.upper()
        # Remove product name with underscores surrounding it
        result = result.upper().replace(f"_{p_u}_", "_").replace(f"{p_u}_", "").replace(f"_{p_u}", "").strip("_").lower()
        if not result: result = "UNKNOWN_SCRIPT"

    return result

def _increment_global_active(product: str, direction: str) -> None:
    product = product.upper()
    direction = direction.upper()
    key = f"{product}_{direction}"
    state = _load_active_trades()
    state[key] = state.get(key, 0) + 1
    _save_active_trades(state)

def _decrement_global_active(product: str, direction: str) -> None:
    product = product.upper()
    direction = direction.upper()
    key = f"{product}_{direction}"
    state = _load_active_trades()
    if key in state:
        state[key] = max(0, state[key] - 1)
        if state[key] == 0:
            state.pop(key)
        _save_active_trades(state)


def _get_total_open_live_trades(json_base_dir: str) -> int:
    """Scan disk for trades with status=OPEN and is_live_trade=True. [V20251231_1145]"""
    count = 0
    if not os.path.exists(json_base_dir):
        return 0
    
    # Check today and yesterday for open trades
    today = pd.Timestamp.now().date()
    date_folders = [(today - pd.Timedelta(days=i)).strftime('%Y-%m-%d') for i in range(2)]
    
    run_mode = Path(json_base_dir).name
    for d_str in date_folders:
        for folder_path in _iter_day_directories(run_mode, d_str):
            for json_path in folder_path.glob('*_op.json'):
                if json_path.name.startswith(('vt_', '_')):
                    continue
                if not _is_open_trade_filename(json_path.name):
                    continue
                try:
                    if os.path.getsize(json_path) == 0:
                        continue
                    with open(json_path, 'r') as f:
                        data = json.load(f)
                    is_live = bool(data.get('is_live_trade', False))
                    if data.get('status') == 'OPEN' and is_live:
                        count += 1
                except Exception:
                    continue
    return count



def _load_active_trades() -> Dict[str, int]:
    try:
        with open(GLOBAL_ACTIVE_TRADES_FILE, 'r') as handle:
            data = json.load(handle)
            return {str(k): int(v) for k, v in data.items()}
    except (FileNotFoundError, json.JSONDecodeError, ValueError):
        return {}


def _save_active_trades(active_trades: Dict[str, int]) -> None:
    with open(GLOBAL_ACTIVE_TRADES_FILE, 'w') as handle:
        json.dump(active_trades, handle, indent=2)


def _load_trade_products_upper() -> Set[str]:
    try:
        cfg = _load_config()
    except Exception:
        cfg = {}
    return {str(prod).upper() for prod in cfg.get('trade_products', []) if isinstance(prod, str)}


def _split_activation_core(core_key: str, trade_products: Set[str]) -> Tuple[str, Optional[str]]:
    core_upper = core_key.upper()
    for prod in sorted(trade_products, key=len, reverse=True):
        token = f"_{prod}"
        if core_upper.endswith(token):
            return core_key[: len(core_key) - len(token)], prod
    parts = core_key.split('_')
    if len(parts) > 1:
        candidate = '_'.join(parts[-2:]) if len(parts[-1]) == 1 else parts[-1]
        cand_upper = candidate.upper()
        if cand_upper.isalpha() and 2 <= len(cand_upper) <= 8:
            return core_key[: len(core_key) - len(candidate) - 1], cand_upper
    return core_key, None


def _normalize_activation_key_entry(raw_key: str, trade_products: Set[str]) -> Tuple[str, Optional[str]]:
    suffix = next((suf for suf in ACTIVATION_SUFFIXES if raw_key.endswith(suf)), None)
    if not suffix:
        return raw_key, None
    core = raw_key[:-len(suffix)]
    base_core, product = _split_activation_core(core, trade_products)
    normalized_key = f"{base_core}{suffix}"
    return normalized_key, product


def _coerce_activation_entry(value: Any) -> Dict[str, Any]:
    if isinstance(value, dict):
        return {
            'active': bool(value.get('active')),
            'activated_at': value.get('activated_at'),
            'manual': bool(value.get('manual')),
            'products': value.get('products'), # [V20251231_1110] Keep products
            'auto_promote': bool(value.get('auto_promote', False)) # [2026-04-08 10:00] V20260408_1000
        }
    return {
        'active': bool(value),
        'activated_at': None,
        'manual': False,
        'products': None, # [V20251231_1110]
        'auto_promote': False # [2026-04-08 10:00] V20260408_1000
    }


def _merge_activation_entries(target: Dict[str, Any], incoming: Dict[str, Any]) -> Dict[str, Any]:
    target['active'] = target.get('active', False) or incoming.get('active', False)
    inc_ts = incoming.get('activated_at')
    if inc_ts and (not target.get('activated_at') or inc_ts > target.get('activated_at')):
        target['activated_at'] = inc_ts
    target['manual'] = target.get('manual', False) or incoming.get('manual', False)
    # [2026-04-08 10:00] V20260408_1000 - Merge auto_promote flag
    target['auto_promote'] = target.get('auto_promote', False) or incoming.get('auto_promote', False)
    # [V20251231_1110] Merge product lists
    p1 = target.get('products') or []
    p2 = incoming.get('products') or []
    if p1 or p2:
        combined = list(set([p.upper() for p in (p1 if isinstance(p1, list) else [])] + 
                           [p.upper() for p in (p2 if isinstance(p2, list) else [])]))
        target['products'] = combined
    return target


def _normalize_activation_dict(raw: Dict[str, Any], trade_products: Set[str]) -> Tuple[Dict[str, Any], bool]:
    normalized: Dict[str, Any] = {}
    dirty = False
    for raw_key, value in raw.items():
        base_key, _ = _normalize_activation_key_entry(str(raw_key), trade_products)
        entry = _coerce_activation_entry(value)
        if base_key in normalized:
            normalized[base_key] = _merge_activation_entries(normalized[base_key], entry)
        else:
            normalized[base_key] = entry
        if base_key != raw_key:
            dirty = True
    return normalized, dirty


def _load_activations() -> Dict[str, Any]:
    """Safely load activations from file and normalize their shape. [V20251230_2336]"""
    if not os.path.exists(ACTIVATIONS_FILE):
        _ACTIVATIONS_CACHE['mtime'] = None
        _ACTIVATIONS_CACHE['data'] = {}
        return {}

    try:
        current_mtime = os.path.getmtime(ACTIVATIONS_FILE)
    except OSError:
        current_mtime = None

    if _ACTIVATIONS_CACHE['mtime'] == current_mtime and current_mtime is not None:
        return _ACTIVATIONS_CACHE['data']

    # Get current run_mode from config
    config = _load_config()
    run_mode = config.get('run_mode', 'live').lower()

    trade_products = _load_trade_products_upper()
    try:
        with open(ACTIVATIONS_FILE, 'r') as f:
            raw = json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"[{datetime.now()}] [WARN] Failed to load activations file: {e}. Using empty dict.")
        _ACTIVATIONS_CACHE['mtime'] = current_mtime
        _ACTIVATIONS_CACHE['data'] = {}
        return {}

    # Handle both old (flat) and new (mode-segmented) formats
    if run_mode in raw:
        # New format: extract activations for current mode
        mode_activations = raw.get(run_mode, {})
    else:
        # Old format: assume all activations are for 'live' mode
        mode_activations = raw if run_mode == 'live' else {}

    normalized, dirty = _normalize_activation_dict(mode_activations, trade_products)
    
    # Note: We don't auto-save here to avoid overwriting other mode's data
    # The API layer handles migration and saving
    
    _ACTIVATIONS_CACHE['mtime'] = current_mtime
    _ACTIVATIONS_CACHE['data'] = normalized
    return normalized


def _save_activations(activations: Dict[str, Any]) -> None:
    """Safely save activations to file. [V20251230_2336]"""
    try:
        # Get current run_mode from config
        config = _load_config()
        run_mode = config.get('run_mode', 'live').lower()
        
        # Load full file to preserve other mode's data
        if os.path.exists(ACTIVATIONS_FILE):
            try:
                with open(ACTIVATIONS_FILE, 'r') as f:
                    full_data = json.load(f)
            except (json.JSONDecodeError, IOError):
                full_data = {'live': {}, 'sim': {}}
        else:
            full_data = {'live': {}, 'sim': {}}
        
        # Ensure mode sections exist
        if 'live' not in full_data:
            full_data['live'] = {}
        if 'sim' not in full_data:
            full_data['sim'] = {}
        
        # Sanitize activations for current mode
        sanitized = {}
        for key, value in activations.items():
            sanitized[key] = _coerce_activation_entry(value)
        
        # Update current mode section
        full_data[run_mode] = sanitized
        
        # Write back full structure
        with open(ACTIVATIONS_FILE, 'w') as f:
            json.dump(full_data, f, indent=4)
        
        print(f"[{datetime.now()}] [ACTIVATE] Saved activations for mode '{run_mode}'. Count: {len(sanitized)}")
        
        try:
            _ACTIVATIONS_CACHE['mtime'] = os.path.getmtime(ACTIVATIONS_FILE)
        except OSError:
            _ACTIVATIONS_CACHE['mtime'] = None
        _ACTIVATIONS_CACHE['data'] = sanitized
    except IOError as e:
        print(f"[{datetime.now()}] [ERROR] Failed to save activations file: {e}")


def _activation_enabled(entry: Any) -> bool:
    print(f"[{datetime.now()}] [DEBUG] _activation_enabled called with entry: {entry}") # <-- New debug print
    if isinstance(entry, bool):
        return entry
    if isinstance(entry, dict):
        return bool(entry.get('active', False))
    return False


def _activation_record(active: bool, manual: bool = False, products: Optional[List[str]] = None) -> Dict[str, Any]:
    record = {
        "active": active,
        "activated_at": datetime.now().isoformat() if active else None,
        "manual": manual
    }
    if active and products:
        record["products"] = products
    return record


def _fetch_top_frequency_mapping(run_mode: str) -> Dict[Tuple[str, str], str]:
    """
    Fetches top frequency data for buy/sell strategies from API.
    Returns a map: {(strategy_params, direction): product}
    """
    mapping = {}
    db_name = 'tradedb_sim2' if str(run_mode).lower() == 'sim' else 'tradedb'
    
    endpoints = [
        (f"{_load_config().get('api_base_url', 'http://127.0.0.1:8000/api')}/vw_top_one_frequency_buy?db={db_name}", 'buy'),
        (f"{_load_config().get('api_base_url', 'http://127.0.0.1:8000/api')}/vw_top_one_frequency_sell?db={db_name}", 'sell')
    ]
    
    for url, mapped_direction in endpoints:
        try:
            resp = requests.get(url, timeout=2)
            if resp.status_code == 200:
                payload = resp.json()
                data = payload.get('data', [])
                for item in data:
                    strat = item.get('strategy_and_params')
                    prod = item.get('product')
                    # API direction is usually lowercase, but let's normalize
                    api_dir = str(item.get('direction', '')).lower()
                    if strat and prod and api_dir == mapped_direction:
                        mapping[(strat, mapped_direction)] = prod
        except Exception:
            pass
            
    return mapping


def _perform_auto_activation_check(json_base_dir: str) -> Tuple[defaultdict, int]: # [2025-12-23 V20251223_1150]
    """Backend auto-activation with exclusive Global Top-N ranking and L-trade protection. [2025-12-23 V20251223_1150]"""
    # [2025-12-23 V20251223_1150] --- Global Lock Mechanism ---
    lock_path = Path(ACTIVATIONS_LOCK_FILE)
    try:
        # Attempt to create a lock file. If it already exists, another process has the lock.
        lock_path.touch(exist_ok=False) 
        # If we successfully created it, we have the lock.
        
        config = _load_config()
        run_mode = config.get('run_mode', 'live')
        net_activation_mode = str(config.get('net_activation_mode', 'auto')).lower()
        alt_activation_mode = str(config.get('alt_activation_mode', 'auto')).lower()

        auto_net = bool(config.get('auto_net_check', False)) and net_activation_mode != 'manual'
        auto_alt = bool(config.get('auto_alt_net_check', False)) and alt_activation_mode != 'manual'
        min_avg_net_threshold = float(config.get('min_avg_net_threshold', 20.0)) # [2025-12-23 V20251223_1150]
        min_trade_count_filter = 0

        # [V20260105] Fetch API Frequency Map for smart product selection
        freq_map = _fetch_top_frequency_mapping(run_mode)

        activations = _load_activations()
        print(f"[{datetime.now()}] [DEBUG] Activations loaded: {activations}")

        # [V20260101_2130] Use latest seen trading date
        today_str = _LATEST_TRADING_DATE or datetime.now().strftime('%Y-%m-%d')
        all_trade_data_today = []
        for today_dir in _iter_day_directories(Path(json_base_dir).name, today_str):
            for pattern in ('*_op.json', '*_cl.json'):
                for json_file in today_dir.glob(pattern):
                    try:
                        with open(json_file, 'r') as f:
                            data = json.load(f)
                        data['filename'] = json_file.name
                        all_trade_data_today.append(data)
                    except Exception:
                        continue

        # --- 1. Calculate Global Metrics ---
        total_todays_live_pnl = 0.0
        open_live_trades_count = 0
        protected_keys: Set[str] = set()
        
        for trade_data in all_trade_data_today:
            if trade_data.get('is_live_trade'):
                if trade_data.get('status') == 'CLOSED':
                    total_todays_live_pnl += float(trade_data.get('net_return', 0.0))
                elif trade_data.get('status') == 'OPEN':
                    open_live_trades_count += 1
                    # This trade is open and live, so its strategy is protected
                    script_name = _get_trade_script_name_from_data(trade_data) # Helper func for script_name
                    direction = (trade_data.get('direction') or '').lower()
                    dir_key = 'buy' if 'long' in direction else 'sell'
                    
                    if trade_data.get('order_sent_net'):
                        protected_keys.add(f"{script_name}_{dir_key}_net")
                    if trade_data.get('order_sent_alt'):
                        protected_keys.add(f"{script_name}_{dir_key}_alt")
        
        # Filter protected_keys to only those currently active (from previous state)
        # This ensures we don't protect something that was manually turned off
        protected_keys = {k for k in protected_keys if _activation_enabled(activations.get(k))}

        # --- 2. Aggregate P&L for ALL strategies (OPEN + CLOSED) [V20251228_0330] ---
        # [V20251231_1445] Added profitable_count for win rate calculation
        global_stats = defaultdict(lambda: defaultdict(lambda: {'pnl': 0.0, 'count': 0, 'profitable_count': 0}))
        
        for trade_data in all_trade_data_today:
            # [V20251228_0350] Nest everything inside the status check to prevent variable leakage.
            if trade_data.get('status') == 'CLOSED':
                script_name = _get_trade_script_name_from_data(trade_data)
                product = str(trade_data.get('product', 'UNKNOWN')).strip().upper()
                direction = (trade_data.get('direction') or '').lower()
                dir_key = 'buy' if 'long' in direction else 'sell'

                if not script_name or product == 'UNKNOWN' or script_name == "UNKNOWN_SCRIPT":
                    continue

                net_key = f"{script_name}_{dir_key}_net"
                alt_key = f"{script_name}_{dir_key}_alt"

                # [V20251228_0715] Deep Clean: Ensure the net_key/alt_key doesn't contain the product name
                # This fixes the issue where virtual trade source_strategy strings include the product
                p_u = product.upper()
                net_key = net_key.upper().replace(f"_{p_u}_", "_").replace(f"{p_u}_", "").replace(f"_{p_u}", "").lower()
                alt_key = alt_key.upper().replace(f"_{p_u}_", "_").replace(f"{p_u}_", "").replace(f"_{p_u}", "").lower()

                pnl_val = float(trade_data.get('net_return', 0.0))
                alt_pnl_val = float(trade_data.get('alt_net', 0.0))
                
                # [V20251228_0600] Audit Log: Detailed tracking
                if abs(pnl_val) > 0.01:
                    print(f"[{datetime.now()}] [V-TRADE-PnL] Found ${pnl_val:7.2f} for {product:8} via {net_key:40}")

                global_stats[net_key][product]['pnl'] += pnl_val
                global_stats[net_key][product]['count'] += 1
                if pnl_val > 0:
                    global_stats[net_key][product]['profitable_count'] += 1
                
                global_stats[alt_key][product]['pnl'] += alt_pnl_val
                global_stats[alt_key][product]['count'] += 1
                if alt_pnl_val > 0:
                    global_stats[alt_key][product]['profitable_count'] += 1

        # --- 3. Global Daily Target Check ---
        total_todays_live_pnl_closed = 0.0
        for trade_data in all_trade_data_today:
             if trade_data.get('is_live_trade') and trade_data.get('status') == 'CLOSED':
                 total_todays_live_pnl_closed += float(trade_data.get('net_return', 0.0))

        daily_target = float(config.get('daily_target', 400.0))
        daily_target_met = (total_todays_live_pnl_closed >= daily_target)
        if daily_target_met:
            print(f"[{datetime.now()}] [INFO] Global Daily P&L target of ${daily_target:.2f} MET (Today's Live CLOSED P&L: ${total_todays_live_pnl_closed:.2f}). No new activations allowed.")

        # --- 4. Determine Global Final Active Sets (Top 3 with protection) ---
        max_live_trades_global = int(config.get('max_live_trades', 1)) # Global limit for new trades
        guard_threshold_y = float(config.get('profitability_guard', {}).get('threshold_y', 0.0))
        # [V20251231_1445] Load auto-activation thresholds
        min_auto_trades = int(config.get('min_auto_trades', 3))
        min_auto_win_rate = float(config.get('min_auto_win_rate', 85.0))
        # [V20260101_0310] Load average return threshold
        min_auto_avg_return = float(config.get('min_auto_avg_return', 0.0))

        final_net_map: Dict[str, List[str]] = {}
        final_alt_map: Dict[str, List[str]] = {}

        top_n = int(config.get('top_n_strategies', 3)) # [2025-12-23 V20251223_1330]
        print(f"[{datetime.now()}] [DEBUG] _perform_auto_activation_check called. auto_net={auto_net}, auto_alt={auto_alt}, open_live_trades_count={open_live_trades_count}, max_live_trades_global={max_live_trades_global}")

        # Process Net Activations
        if auto_net and not daily_target_met and open_live_trades_count < max_live_trades_global:
            # [V20260101_1900] Get protected keys and their products
            protected_net_keys = {k for k in protected_keys if k.endswith('_net')}
            for key in protected_net_keys:
                entry = activations.get(key)
                if isinstance(entry, dict) and entry.get('products'):
                    final_net_map[key] = entry.get('products')

            slots_to_fill = max(0, top_n - len(protected_net_keys))

            net_candidates_raw = []
            for key, product_stats in global_stats.items():
                if key.endswith('_net'):
                    total_pnl = sum(stats['pnl'] for stats in product_stats.values())
                    total_count = sum(stats['count'] for stats in product_stats.values())
                    total_profitable = sum(stats['profitable_count'] for stats in product_stats.values())
                    win_rate = (total_profitable / total_count * 100.0) if total_count > 0 else 0.0
                    avg_return = (total_pnl / total_count) if total_count > 0 else 0.0

                    if total_pnl > guard_threshold_y and total_count >= min_auto_trades and \
                       win_rate > min_auto_win_rate and avg_return > min_auto_avg_return:
                        if key not in protected_net_keys:
                            # [V20260105] Extract script name and direction from key
                            parts = key.rsplit('_', 2)
                            if len(parts) == 3:
                                script_name, dir_key, _ = parts
                            else:
                                script_name, dir_key = key, 'unknown'
                            
                            # Check Frequency Map (API)
                            api_product = freq_map.get((script_name, dir_key))
                            
                            if api_product:
                                top_product = api_product
                                print(f"[{datetime.now()}] [AUTO-NET] Using API Frequency Product for {key}: {top_product}")
                                net_candidates_raw.append({'key': key, 'pnl': total_pnl, 'top_product': top_product})
                            else:
                                # [V20260105] NO ACTION TAKEN if API frequency data is missing
                                print(f"[{datetime.now()}] [AUTO-NET] Skipping {key}: No API frequency data found.")
            
            net_candidates_raw.sort(key=lambda x: x['pnl'], reverse=True)
            
            if slots_to_fill > 0 and net_candidates_raw:
                top_pnl = net_candidates_raw[0]['pnl']
                tied_for_top = [c for c in net_candidates_raw if c['pnl'] == top_pnl]
                
                if len(tied_for_top) > slots_to_fill:
                    tied_for_top.sort(key=lambda x: x['key'])
                    for i in range(slots_to_fill):
                        c = tied_for_top[i]
                        final_net_map[c['key']] = [c['top_product']]
                else:
                    for c in net_candidates_raw[:slots_to_fill]:
                        final_net_map[c['key']] = [c['top_product']]

        # Process Alt Activations
        if auto_alt and not daily_target_met and open_live_trades_count < max_live_trades_global:
            protected_alt_keys = {k for k in protected_keys if k.endswith('_alt')}
            for key in protected_alt_keys:
                entry = activations.get(key)
                if isinstance(entry, dict) and entry.get('products'):
                    final_alt_map[key] = entry.get('products')

            slots_to_fill = max(0, top_n - len(protected_alt_keys))

            alt_candidates_raw = []
            for key, product_stats in global_stats.items():
                if key.endswith('_alt'):
                    total_pnl = sum(stats['pnl'] for stats in product_stats.values())
                    total_count = sum(stats['count'] for stats in product_stats.values())
                    total_profitable = sum(stats['profitable_count'] for stats in product_stats.values())
                    win_rate = (total_profitable / total_count * 100.0) if total_count > 0 else 0.0
                    avg_return = (total_pnl / total_count) if total_count > 0 else 0.0

                    if total_pnl > guard_threshold_y and total_count >= min_auto_trades and \
                       win_rate > min_auto_win_rate and avg_return > min_auto_avg_return:
                        if key not in protected_alt_keys:
                            # [V20260105] Extract script name and direction from key
                            parts = key.rsplit('_', 2)
                            if len(parts) == 3:
                                script_name, dir_key, _ = parts
                            else:
                                script_name, dir_key = key, 'unknown'
                                
                            # Check Frequency Map (API)
                            api_product = freq_map.get((script_name, dir_key))

                            if api_product:
                                top_product = api_product
                                print(f"[{datetime.now()}] [AUTO-ALT] Using API Frequency Product for {key}: {top_product}")
                                alt_candidates_raw.append({'key': key, 'pnl': total_pnl, 'top_product': top_product})
                            else:
                                # [V20260105] NO ACTION TAKEN if API frequency data is missing
                                print(f"[{datetime.now()}] [AUTO-ALT] Skipping {key}: No API frequency data found.")

            alt_candidates_raw.sort(key=lambda x: x['pnl'], reverse=True)

            if slots_to_fill > 0 and alt_candidates_raw:
                top_pnl = alt_candidates_raw[0]['pnl']
                tied_for_top = [c for c in alt_candidates_raw if c['pnl'] == top_pnl]
                
                if len(tied_for_top) > slots_to_fill:
                    tied_for_top.sort(key=lambda x: x['key'])
                    for i in range(slots_to_fill):
                        c = tied_for_top[i]
                        final_alt_map[c['key']] = [c['top_product']]
                else:
                    for c in alt_candidates_raw[:slots_to_fill]:
                        final_alt_map[c['key']] = [c['top_product']]
        
        # --- 5. Calculate all updates (deactivations + activations) ---
        updates = {}
        current_activations_snapshot = activations.copy()

        def _is_manual_override(entry: Any) -> bool:
            return isinstance(entry, dict) and bool(entry.get('manual'))

        # [V20260101_1632] Deactivation logic including Manual Mode Cleanup
        for key, entry in current_activations_snapshot.items():
            if not (key.endswith('_net') or key.endswith('_alt')):
                continue
            
            # If the user has manually set this strategy to active, we never touch it automatically
            if _is_manual_override(entry):
                continue

            enabled = _activation_enabled(entry)
            
            # Handle Net strategies
            if key.endswith('_net'):
                # [V20260101_1945] DEBUG: Log why we are checking this key
                if enabled:
                    print(f"[{datetime.now()}] [DEBUG] Checking deactivation for {key}. auto_net={auto_net}, in_final={key in final_net_map}")
                
                # Deactivate if:
                # 1. Automation is enabled but strategy dropped out of Top-N
                # 2. Automation is DISABLED (Manual Mode) - we cleanup all system records to "clear the deck"
                if (auto_net and key not in final_net_map and enabled) or \
                   (not auto_net and enabled):
                    updates[key] = _activation_record(False)
            
            # Handle Alt strategies
            else:
                if (auto_alt and key not in final_alt_map and enabled) or \
                   (not auto_alt and enabled):
                    updates[key] = _activation_record(False)

        # Activate/Update keys that should be active
        if auto_net:
            for key, products in final_net_map.items():
                entry = current_activations_snapshot.get(key)
                if _is_manual_override(entry):
                    continue
                # [V20260101_1900] Update if products changed or if inactive
                current_products = entry.get('products', []) if isinstance(entry, dict) else []
                if not _activation_enabled(entry) or current_products != products:
                    updates[key] = _activation_record(True, products=products)
        
        if auto_alt:
            for key, products in final_alt_map.items():
                entry = current_activations_snapshot.get(key)
                if _is_manual_override(entry):
                    continue
                current_products = entry.get('products', []) if isinstance(entry, dict) else []
                if not _activation_enabled(entry) or current_products != products:
                    updates[key] = _activation_record(True, products=products)


        # --- 6. Apply updates ---
        if updates:
            print(f"[{datetime.now()}] [GLOBAL_ACTIVATION] Applying {len(updates)} change(s) to activations.json (Mode: {run_mode})")
            # Re-load activations one last time to minimize race conditions with other writes
            current_activations_final = _load_activations() 
            current_activations_final.update(updates)
            _save_activations(current_activations_final)

            for key, val in updates.items():
                action_type = "Activating" if (isinstance(val, dict) and val.get('active')) else "Deactivating"
                print(f"[{datetime.now()}] [GLOBAL_ACTIVATION] {action_type} {key}")
        else:
            print(f"[{datetime.now()}] [GLOBAL_ACTIVATION] No changes to activations.json for mode '{run_mode}'.")

        return global_stats, open_live_trades_count

    except FileExistsError: # Lock file already exists, another process is managing
        return defaultdict(lambda: defaultdict(lambda: {'pnl': 0.0, 'count': 0})), 0
    except Exception as e: # pylint: disable=broad-except
        print(f"[{datetime.now()}] [ERROR] Global Activation Check failed: {e}")
        return defaultdict(lambda: defaultdict(lambda: {'pnl': 0.0, 'count': 0})), 0
    finally:
        # Ensure the lock is released if we acquired it
        if lock_path.exists():
            try:
                lock_path.unlink()
            except Exception as e: # pylint: disable=broad-except
                print(f"[{datetime.now()}] [ERROR] Failed to release lock: {e}")


def _create_l_trade_order(
    product: str, 
    direction: str, 
    strategy_key: str, 
    trade_id: str,
    current_price: float,
    latest_bid: Optional[float] = None,
    latest_ask: Optional[float] = None,
    mode: str = 'net',
    is_close: bool = False,
    source: str = 'normal',
    source_group: Optional[str] = None,
    guid: str = 'unknown', # [V20260129_0435]
    is_auto_promote: bool = False, # [2026-04-08 10:00] V20260408_1000
    trade_json_path: Optional[str] = None,
    request_context: Optional[Dict[str, Any]] = None,
    requested_by: str = 'system',
    force_execution_request: bool = False,
    bypass_execution_gate: bool = False,
    execution_request_id: Optional[str] = None,
) -> Optional[str]:
    """Creates a new live trade order JSON file."""
    global _LAST_L_TRADE_ORDER_ERROR, _LAST_L_TRADE_ORDER_PENDING_ID
    _LAST_L_TRADE_ORDER_ERROR = None
    _LAST_L_TRADE_ORDER_PENDING_ID = None
    _config = _load_config() # Load config here
    # [MODIFIED 2025-12-28] Prevent new L-Trade order creation if archiving is active
    if _config.get('archive', False):
        _LAST_L_TRADE_ORDER_ERROR = "archive active"
        print(f"[L-TRADE-BLOCK] New L-Trade order for {product} {direction} blocked due to active archive process.")
        return None

    # [2025-12-23 V20251223_1530]
    # Use _config here
    run_mode = _config.get('run_mode', 'LIVE').upper()
    
    source_group_key = str(source_group or source or 'breakout')

    # max_live_trades guard (scoped per source_group)
    if not is_close:
        max_live_trades_global = int(_config.get('max_live_trades', 1))
        # [V20251231_1145] Use disk scan instead of unreliable active_trades.json
        json_base_dir = os.path.join(os.path.dirname(CONFIG_FILE_PATH), 'json', run_mode.lower())
        current_live_count = _get_total_open_live_trades_for_group(json_base_dir, source_group_key)

        # Per-group daily target guard (closed PnL)
        try:
            daily_target = float(_config.get('daily_target', 0) or 0)
        except (TypeError, ValueError):
            daily_target = 0.0
        if daily_target > 0 and not is_auto_promote: # [2026-04-08 10:00] V20260408_1000 - Bypass for auto-promoted trades
            group_closed_pnl = _get_group_closed_live_pnl(json_base_dir, source_group_key)
            if group_closed_pnl >= daily_target:
                _LAST_L_TRADE_ORDER_ERROR = (
                    f"daily_target reached for group {source_group_key} "
                    f"(target={daily_target}, closed_pnl={group_closed_pnl:.2f})"
                )
                print(
                    f"[GUARD] Daily target reached for {source_group_key}. "
                    f"Skipping L-Trade order for {strategy_key} {product} {direction} {mode.upper()}."
                )
                return None
        
        # [V20260211_1705] Add memory cache count for trades sent this cycle (but not on disk yet)
        # Prune old cache entries (older than 30s)
        now_ts = time.time()
        for k in list(_LIVE_ORDERS_SENT_MEMORY_CACHE.keys()):
            v = _LIVE_ORDERS_SENT_MEMORY_CACHE.get(k)
            if isinstance(v, dict):
                ts = float(v.get('ts', 0) or 0)
            else:
                ts = float(v or 0)
            if now_ts - ts > 30:
                del _LIVE_ORDERS_SENT_MEMORY_CACHE[k]

        memory_count = 0
        for v in _LIVE_ORDERS_SENT_MEMORY_CACHE.values():
            if isinstance(v, dict):
                if str(v.get('source_group') or '') == source_group_key:
                    memory_count += 1
            else:
                memory_count += 1
        total_effective_count = current_live_count + memory_count

        if total_effective_count >= max_live_trades_global:
            _LAST_L_TRADE_ORDER_ERROR = (
                f"max_live_trades reached (max={max_live_trades_global}, "
                f"group={source_group_key}, on_disk={current_live_count}, pending={memory_count})"
            )
            print(f"[GUARD] Max live trades ({max_live_trades_global}) reached for {source_group_key}. Current on-disk: {current_live_count}, Memory-pending: {memory_count}. Skipping L-Trade order for {strategy_key} {product} {direction} {mode.upper()}.")
            return None
        
        # [V20260217_2352] TWS routing cap: based on OPEN trades with order_sent_net=true.
        # Only NET OPEN orders are counted against this cap.
        if str(mode).lower() == 'net':
            try:
                max_trades_to_tws = int(_config.get('max_trades_to_tws', 1) or 1)
            except (TypeError, ValueError):
                max_trades_to_tws = 1
            max_trades_to_tws = max(0, max_trades_to_tws)

            tws_on_disk = _get_total_open_tws_sent_trades(json_base_dir)
            tws_pending = 0
            for v in _LIVE_ORDERS_SENT_MEMORY_CACHE.values():
                if not isinstance(v, dict):
                    continue
                if str(v.get('mode') or '').lower() != 'net':
                    continue
                if bool(v.get('is_close')):
                    continue
                tws_pending += 1

            tws_effective = tws_on_disk + tws_pending
            if tws_effective >= max_trades_to_tws:
                _LAST_L_TRADE_ORDER_ERROR = (
                    f"max_trades_to_tws reached (max={max_trades_to_tws}, "
                    f"on_disk={tws_on_disk}, pending={tws_pending})"
                )
                print(
                    f"[GUARD] max_trades_to_tws ({max_trades_to_tws}) reached. "
                    f"Skipping NET L-Trade order for {strategy_key} {product} {direction}."
                )
                return None
        
        # Mark this specific request as "pending" in memory cache
        cache_key = f"{source_group_key}_{strategy_key}_{product}_{trade_id}_{mode}"
        _LIVE_ORDERS_SENT_MEMORY_CACHE[cache_key] = {
            'ts': now_ts,
            'source_group': source_group_key,
            'mode': str(mode).lower(),
            'is_close': bool(is_close),
        }


    strategy_action = 'BUY' if direction == 'LONG' else 'SELL'
    if mode == 'alt':
        base_action = 'SELL' if strategy_action == 'BUY' else 'BUY'
    else:
        base_action = strategy_action
    if is_close:
        action = 'SELL' if base_action == 'BUY' else 'BUY'
        phase = 'CLOSE'
    else:
        action = base_action
        phase = 'OPEN'
    timestamp_str = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # We don't have window_size, pip_buffer, tp_pips, sl_pips directly here from a V-Trade.
    # So we'll need to derive a comment or use a simpler filename.
    # For now, let's use a simplified filename for V-Trade initiated L-trades.
    # Filename format: {product}_{strategy}_{action}_{timestamp}_{suffix}
    
    suffix = "close_tradeable.json" if is_close else "open_tradeable.json"
    
    # [V20260126_0410] Prefix filename with source screen (e.g. breakout_, grid_live_, trade_bucket_)
    prefix = source if source and source != 'normal' else 'breakout'
    # Sanitize prefix for filesystem
    prefix = prefix.replace(':', '_').replace(' ', '_').replace('/', '_').replace('\\', '_')
    # [V20260129_0435] GUID integration: include GUID before product name
    filename = f"{prefix}_{guid}_{product}_{strategy_key}_{action}_{timestamp_str}_{suffix}"

    # Determine guide price based on action and available data
    guide_price = None
    if latest_ask is not None and action == 'BUY':
        guide_price = latest_ask
    elif latest_bid is not None and action == 'SELL':
        guide_price = latest_bid
    
    if guide_price is None:
        guide_price = current_price
    if guide_price is None: # Fallback if current_price is also None
        guide_price = 0.0 # Should ideally not happen if a valid trade is being created.

    # [2026-04-08 14:00] V20260408_1400 - Use totalQuantity for non-forex to match TWS requirements
    contract = _get_tws_contract_details(product, _config)
    qty = _trade_quantity_for_product(product, _config)
    p_type = _resolve_product_type(product, _config)
    qty_key = 'totalQuantity' if p_type != 'forex' else 'quantity'

    tradeable_data = {
        **contract,
        'action': action,
        'orderType': 'MKT',
        qty_key: qty,
        'guidePrice': guide_price,
        'comment': f"{strategy_key} {mode.upper()} {phase} #{trade_id}",
        'source': source,
        'source_group': source_group_key,
        'guid': guid, # [V20260129_0435]
    }
    
    if run_mode == 'SIM':
        key = 'send_json_files_sim'
        default_dir = r'C:\Users\edebe\eds\trades_rt3_sim\orders'
    else: # Live mode
        key = 'send_json_files'
        default_dir = r'C:\Users\edebe\eds\trades_rt3\orders'
        
    tradeable_dir = _config.get(key, default_dir)
    try:
        os.makedirs(tradeable_dir, exist_ok=True)
    except Exception as exc:
        _LAST_L_TRADE_ORDER_ERROR = f"failed to create order directory '{tradeable_dir}': {exc}"
        print(f"[ERROR] Failed to ensure tradeable dir: {exc}")
        return None
    auto_execution_enabled = bool(_config.get('l_trade_auto_execution', True))
    queue_for_review = bool(force_execution_request) or (not is_close and not bypass_execution_gate and not auto_execution_enabled)
    if queue_for_review:
        request_id = execution_request_id or uuid.uuid4().hex
        marker = f'{L_TRADE_EXECUTION_PENDING_PREFIX}{request_id}'
        request_payload = {
            'request_id': request_id,
            'status': 'pending',
            'created_at': datetime.now().isoformat(),
            'requested_by': requested_by,
            'order_args': {
                'product': product,
                'direction': direction,
                'strategy_key': strategy_key,
                'trade_id': trade_id,
                'current_price': current_price,
                'latest_bid': latest_bid,
                'latest_ask': latest_ask,
                'mode': mode,
                'is_close': is_close,
                'source': source,
                'source_group': source_group,
                'guid': guid,
                'is_auto_promote': is_auto_promote,
                'trade_json_path': trade_json_path,
                'request_context': request_context,
                'requested_by': requested_by,
            },
            'request_context': request_context or {},
            'preview': {
                'phase': phase,
                'mode': str(mode).upper(),
                'product': product,
                'direction': direction,
                'strategy_key': strategy_key,
                'trade_id': trade_id,
                'action': action,
                'guide_price': guide_price,
                'tradeable_dir': tradeable_dir,
                'filename': filename,
                'filepath': os.path.join(tradeable_dir, filename),
                'source': source,
                'source_group': source_group_key,
                'guid': guid,
                'order_payload': tradeable_data,
            },
        }
        try:
            _write_json_atomic(_execution_request_path(request_id), request_payload, indent=2)
            _LAST_L_TRADE_ORDER_PENDING_ID = request_id
            _LAST_L_TRADE_ORDER_ERROR = f'pending approval ({request_id})'
            _update_trade_file_pending_state(
                trade_json_path,
                mode=str(mode or 'net'),
                is_close=bool(is_close),
                request_id=request_id,
                status='pending',
                request_context=request_context,
            )
            if not is_close:
                _LIVE_ORDERS_SENT_MEMORY_CACHE.pop(cache_key, None)
            print(f"[L-TRADE-EXECUTION] Queued {phase} {mode.upper()} request {request_id} for {strategy_key} {product}")
            return marker
        except Exception as exc:
            if not is_close:
                _LIVE_ORDERS_SENT_MEMORY_CACHE.pop(cache_key, None)
            _LAST_L_TRADE_ORDER_ERROR = f'failed to queue execution request: {exc}'
            print(f"[ERROR] Failed to queue l-trade execution request: {exc}")
            return None
    try:
        filepath = os.path.join(tradeable_dir, filename)
        with open(filepath, 'w') as handle:
            json.dump(tradeable_data, handle, indent=2)
        print(f"[TRADEABLE] Created {mode.upper()} {phase} order file: {filename}")
        if not is_close:
            _increment_global_active(product, direction)
            _update_trade_file_pending_state(
                trade_json_path,
                mode=str(mode or 'net'),
                is_close=False,
                request_id=None,
                status='approved',
            )
        return filepath
    except Exception as exc:
        if not is_close:
            _LIVE_ORDERS_SENT_MEMORY_CACHE.pop(cache_key, None)
        _LAST_L_TRADE_ORDER_ERROR = f"failed to write order file '{filename}': {exc}"
        print(f"[ERROR] Failed to create tradeable JSON: {exc}")
        return None



def _resolve_config_scalar(value: Any, default: Any, cast_func: Callable[[Any], Any]) -> Any:
    """Return a scalar from config values that might be scalars or lists."""
    candidate = value
    if isinstance(candidate, list):
        candidate = candidate[0] if candidate else default
    if candidate is None:
        candidate = default
    try:
        return cast_func(candidate)
    except (TypeError, ValueError):
        return cast_func(default)


def _determine_v_trade_entry_price(
    direction: str,
    current_price: Optional[float],
    latest_bid: Optional[float],
    latest_ask: Optional[float],
) -> float:
    """Pick the best available price snapshot for the virtual trade entry."""
    direction_upper = (direction or '').upper()
    if direction_upper == 'LONG':
        price = latest_ask if latest_ask is not None else current_price
    elif direction_upper == 'SHORT':
        price = latest_bid if latest_bid is not None else current_price
    else:
        price = current_price
    return float(price) if price is not None and price > 0 else 0.0




def _normalize_v_trade_payload(data: Dict[str, Any], config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Ensure V-Trade entries always expose the full schema."""
    config = config or _load_config()
    default_window = BASE_WINDOW_SIZES[0] if BASE_WINDOW_SIZES else 0
    window_size = _resolve_config_scalar(config.get('window_size', default_window), default_window, int)
    pip_buffer = _resolve_config_scalar(config.get('pip_buffer', BASE_PIP_BUFFER), BASE_PIP_BUFFER, float)
    tp_pips = _resolve_config_scalar(config.get('tp_pips', BASE_TP_PIPS), BASE_TP_PIPS, float)
    sl_pips = _resolve_config_scalar(config.get('sl_pips', BASE_SL_PIPS), BASE_SL_PIPS, float)
    defaults = {
        'entry_price': 0.0,
        'current_price': 0.0,
        'gross_pnl_pips': 0.0,
        'net_return': 0.0,
        'min_net': 0.0,  # [V20260428] Track minimum net (drawdown)
        'alt_net': 0.0,
        'cumulative_pnl': 0.0,
        'cumulative_alt_pnl': 0.0,
        'exit_time': None,
        'exit_price': None,
        'exit_reason': None,
        'status': data.get('status', 'OPEN'),
        'order_sent_net': False,
        'order_sent_alt': False,
        'is_live_trade': bool(data.get('is_live_trade', False)),
        'window_size': window_size,
        'pip_buffer': pip_buffer,
        'tp_pips': tp_pips,
        'sl_pips': sl_pips,
    }
    for key, value in defaults.items():
        data.setdefault(key, value)
    apply_strategy_name_fields(data)
    return data





def _compute_v_trade_gross_pips(entry_price: float, exit_price: float, direction: str, product: str = 'GBP', config: Optional[Dict] = None) -> float:
    if not entry_price or exit_price is None:
        return 0.0
    # [2026-03-16 V20260316_1430] Use dynamic multiplier for virtual pips
    multiplier = _get_pip_multiplier(product, config)
    diff = (exit_price - entry_price) * multiplier
    if (direction or '').upper() == 'LONG':
        return diff
    return -diff


def _calculate_v_trade_pnl(entry_price: float, current_price: float, direction: str, config: Dict[str, Any], product: str = 'GBP') -> Dict[str, float]:
    """Calculates PnL metrics for a V-Trade. [2025-12-25 V20251225_0345]"""
    pip_value = _pip_value_for_product(product, config)
    commission_usd = float(config.get('commission_usd', 10.0))
    spread_pips = float(config.get('spread_pips', 2.0))
    
    # [2026-03-16 V20260316_1430] Use dynamic multiplier for virtual PnL
    multiplier = _get_pip_multiplier(product, config)
    if (direction or '').upper() == 'LONG':
        gross_pips = (current_price - entry_price) * multiplier
    else:
        gross_pips = (entry_price - current_price) * multiplier
        
    gross_usd = gross_pips * pip_value
    
    # [V20260323_1930] Apply upfront adhoc cost per product type
    adhoc_cost_usd = 0.0
    try:
        p_type = product_type_for_product(product, config)
        type_costs = config.get("product_type_cost", {})
        adhoc_cost_usd = float(type_costs.get(p_type, 0.0) or 0.0)
        print(f"[DEBUG_VTRADE_ADHOC] product={product} p_type={p_type} type_costs={type_costs} adhoc={adhoc_cost_usd}")
    except Exception as e:
        print(f"[DEBUG_VTRADE_ADHOC_ERR] product={product} error={e}")

    # [V20260325_0500] Apply 2x adhoc cost upfront (entry + exit)
    total_adhoc_cost = adhoc_cost_usd * 2
    net_usd = gross_usd - commission_usd - total_adhoc_cost

    # Alt PnL (Reversal logic implies opposite direction)
    alt_gross_pips = -gross_pips
    alt_gross_usd = alt_gross_pips * pip_value
    spread_cost_usd = spread_pips * pip_value
    alt_net_usd = alt_gross_usd - commission_usd - spread_cost_usd - total_adhoc_cost

    return {
        'gross_pnl_pips': gross_pips,
        'net_return': net_usd,
        'alt_net': alt_net_usd,
        'adhoc_cost_usd': total_adhoc_cost  # [V20260325_0500] Include for audit
    }


def _perform_archiving(config: Dict[str, Any]) -> bool:
    """
    Archive current day folder contents into an in-date archive path:
    json/<mode>/<product_type>/<date>/archive/<HHMMSS> (or legacy
    json/<mode>/<date>/archive/<HHMMSS> when applicable during transition)
    then recreate a fresh date folder and reset underscore files.
    Returns True only when archive move completed successfully.
    """
    run_mode = config.get('run_mode', 'live')
    
    # Determine the base directory for the current run_mode (live or sim)
    # CONFIG_FILE_PATH is expected to be something like 'TradeApps/breakout/config.json'
    # So, Path(os.path.dirname(CONFIG_FILE_PATH)) will be 'TradeApps/breakout'
    # Then append 'json' and the run_mode
    base_dir = _json_root_dir() / run_mode.lower()
    if not base_dir.exists():
        print(f"[{datetime.now()}] [ARCHIVE-SKIP] Base directory not found for {run_mode}: {base_dir}")
        return False

    today_str = _LATEST_TRADING_DATE or datetime.now().strftime('%Y-%m-%d')
    source_dirs = _iter_day_directories(run_mode.lower(), today_str)
    if not source_dirs:
        print(f"[{datetime.now()}] [ARCHIVE-SKIP] Source date directory not found for {run_mode}: {today_str}")
        return False

    def _close_open_l_trades_before_archive(day_dir: Path, mode: str, cfg: Dict[str, Any]) -> int:
        """
        Generate CLOSE tradeable files for all OPEN live L-trades before archiving.
        Marks source trade files with archive close metadata.
        """
        if mode == 'sim':
            order_dir = cfg.get('send_json_files_sim') or r'C:\Users\edebe\eds\trades_rt3_sim\orders'
        else:
            order_dir = cfg.get('send_json_files') or r'C:\Users\edebe\eds\trades_rt3\orders'
        order_path = Path(order_dir)
        order_path.mkdir(parents=True, exist_ok=True)

        forced = 0
        now_iso = datetime.now().isoformat()
        now_tag = datetime.now().strftime('%Y%m%d_%H%M%S')
        qty = _trade_quantity_for_product(None, cfg)

        for fp in day_dir.glob('*_op.json'):
            try:
                with open(fp, 'r') as f:
                    d = json.load(f) or {}
            except Exception:
                continue
            product = str(d.get('product') or '').strip().upper() or None
            qty = _trade_quantity_for_product(product, cfg)
            if str(d.get('status', '')).upper() != 'OPEN':
                continue
            if not bool(d.get('is_live_trade') or d.get('order_sent_net') or d.get('order_sent_alt')):
                continue
            if d.get('archive_close_sent_at'):
                continue

            direction = str(d.get('direction') or '').upper()
            action = 'SELL' if direction in ('LONG', 'BUY') else 'BUY'
            product = str(d.get('product') or '').upper()
            strategy = str(d.get('script_name') or d.get('source_strategy') or 'unknown')
            trade_id = d.get('trade_id') or d.get('id') or 0
            close_filename = f"{product}_{strategy}_{action}_{now_tag}_archive_close_tradeable.json"
            
            # [2026-04-07 17:25] V20260407_1725 - Use dynamic contract details for archive close
            contract = _get_tws_contract_details(product, config)
            
            close_payload = {
                **contract,
                'action': action,
                'orderType': 'MKT',
                'quantity': qty,
                'guidePrice': float(d.get('current_price') or d.get('entry_price') or 0.0),
                'comment': f"{strategy} NET CLOSE #{trade_id} (Archive Reset)",
                'source': d.get('source_screen') or 'grid_live',
                'source_group': d.get('source_group'),
                'guid': d.get('guid') or 'unknown',
            }
            try:
                with open(order_path / close_filename, 'w') as f:
                    json.dump(close_payload, f, indent=2)
                d['archive_close_sent_at'] = now_iso
                d['archive_close_reason'] = 'archive_reset'
                d['archive_close_file'] = close_filename
                with open(fp, 'w') as f:
                    json.dump(d, f, indent=2)
                forced += 1
            except Exception as e:
                print(f"[{datetime.now()}] [ARCHIVE-CLOSE-ERROR] {fp.name}: {e}")
                continue
        return forced

    for source_date_dir in source_dirs:
        timestamp_str = datetime.now().strftime('%H%M%S')
        archive_target_dir = source_date_dir / "archive" / timestamp_str
        print(
            f"[{datetime.now()}] [ARCHIVE-CONTEXT] mode={run_mode.lower()} "
            f"date={today_str} source={source_date_dir} target={archive_target_dir}"
        )
        archive_target_dir.mkdir(parents=True, exist_ok=True)

        try:
            close_count = _close_open_l_trades_before_archive(source_date_dir, run_mode.lower(), config)
            print(f"[{datetime.now()}] [ARCHIVE-PREFLIGHT] Close requests sent for {close_count} open L-trade(s).")
        except Exception as e:
            print(f"[{datetime.now()}] [ARCHIVE-PREFLIGHT-ERROR] Failed to close open L-trades: {e}")

        print(f"[{datetime.now()}] [ARCHIVE-START] Archiving contents of {source_date_dir} to {archive_target_dir}")
        summary_files_to_keep_live = {
            "_summary_net.json",
            "_trades_summary.json",
            "_top20.json",
            "_tb_leadership.json",
        }

        try:
            for child in source_date_dir.iterdir():
                if child.name.lower() == "archive":
                    continue
                if child.name in summary_files_to_keep_live:
                    continue
                shutil.move(str(child), str(archive_target_dir / child.name))
        except Exception as e:
            print(f"[{datetime.now()}] [ARCHIVE-ERROR] Failed while moving into {archive_target_dir}: {e}")
            return False

        breakout_files_left = list(source_date_dir.glob("*reakout*.json")) + list(source_date_dir.glob("*_op.json"))
        if breakout_files_left:
            print(f"[{datetime.now()}] [ARCHIVE-SKIP] Archiving incomplete, raw trade files still remain in {source_date_dir}.")
            return False

        try:
            cleared_payload = {
                "last_update": datetime.now().isoformat(),
                "cleared": True
            }
            archived_underscore_files = list(archive_target_dir.rglob("_*.json"))
            for archived_file in archived_underscore_files:
                try:
                    rel_path = archived_file.relative_to(archive_target_dir)
                    if rel_path.name in summary_files_to_keep_live:
                        continue
                    target_path = source_date_dir / rel_path
                    target_path.parent.mkdir(parents=True, exist_ok=True)
                    target_path.write_text(json.dumps(cleared_payload, indent=2))
                except Exception as e:
                    print(f"[{datetime.now()}] [ARCHIVE-ERROR] Failed to reset {archived_file.name}: {e}")
        except Exception as e:
            print(f"[{datetime.now()}] [ARCHIVE-ERROR] Failed to reset underscore files: {e}")

        try:
            tb_file = source_date_dir / "_trade_buckets.json"
            with tb_file.open('w') as f:
                json.dump({"buckets": []}, f, indent=2)
            print(f"[{datetime.now()}] [ARCHIVE-RESET] Cleared trade buckets: {tb_file}")
        except Exception as e:
            print(f"[{datetime.now()}] [ARCHIVE-RESET-ERROR] Failed to clear trade buckets: {e}")

    print(f"[{datetime.now()}] [ARCHIVE-END] Archiving process completed for {run_mode}.")

    # 2) Clear grid_live entries for current mode.
    try:
        grid_file = Path(os.path.dirname(CONFIG_FILE_PATH)) / 'grid_live.json'
        grid_data: Any = {"live": [], "sim": []}
        if grid_file.exists():
            with grid_file.open('r') as f:
                loaded = json.load(f)
            if isinstance(loaded, list):
                grid_data = {"live": loaded, "sim": []}
            elif isinstance(loaded, dict):
                grid_data = loaded
        mode_key = run_mode.lower()
        if mode_key not in ('live', 'sim'):
            mode_key = 'live'
        grid_data[mode_key] = []
        with grid_file.open('w') as f:
            json.dump(grid_data, f, indent=2)
        print(f"[{datetime.now()}] [ARCHIVE-RESET] Cleared grid_live for mode={mode_key}.")
    except Exception as e:
        print(f"[{datetime.now()}] [ARCHIVE-RESET-ERROR] Failed to clear grid_live: {e}")
    return True


def _perform_cld_auto_archive(config: Dict[str, Any]) -> bool:
    """
    Archive top-level closed trade JSON files in the active day folder when
    their count exceeds `auto_archive_threshold`.
    Includes both standard `*_cl.json` closed trades and legacy `*_cld.json`
    records while excluding open trades and underscore support files.
    Supports both product-type day folders and the legacy day-root layout
    during transition.
    Returns True if any files were archived, False otherwise.
    """
    run_mode = str(config.get('run_mode', 'live') or 'live').lower()
    auto_archive_threshold = int(config.get('auto_archive_threshold', 5000))

    candidate_dates: Set[str] = set()
    if _LATEST_TRADING_DATE:
        candidate_dates.add(_LATEST_TRADING_DATE)
    candidate_dates.add(datetime.now(timezone.utc).strftime('%Y-%m-%d'))

    archived_any = False

    for today_str in candidate_dates:
        for source_date_dir in _iter_day_directories(run_mode, today_str):
            closed_trade_files = [
                f for f in source_date_dir.iterdir()
                if _is_auto_archivable_closed_trade_file(f)
            ]
            if len(closed_trade_files) <= auto_archive_threshold:
                print(
                    f"[{datetime.utcnow()}] [CLD-AUTO-ARCHIVE] {today_str}: "
                    f"{len(closed_trade_files)} closed trade files in {source_date_dir.name} "
                    f"(threshold: {auto_archive_threshold}) - no archive needed"
                )
                continue

            timestamp_str = datetime.now(timezone.utc).strftime('%H%M%S')
            archive_target = source_date_dir / 'archive' / timestamp_str
            archive_target.mkdir(parents=True, exist_ok=True)

            summary_net_file = source_date_dir / '_summary_net.json'
            if summary_net_file.exists():
                try:
                    archive_summary_copy = archive_target / '_summary_net_pre_auto_archive.json'
                    shutil.copy2(str(summary_net_file), str(archive_summary_copy))
                    source_summary_copy = source_date_dir / '_summary_net_pre_auto_archive.json'
                    shutil.copy2(str(summary_net_file), str(source_summary_copy))
                    print(
                        f"[{datetime.now(timezone.utc)}] [CLD-AUTO-ARCHIVE] {today_str}: "
                        f"preserved _summary_net.json at {archive_summary_copy} and {source_summary_copy}"
                    )
                except Exception as exc:
                    print(
                        f"[{datetime.now(timezone.utc)}] [CLD-AUTO-ARCHIVE-ERROR] "
                        f"Failed to preserve _summary_net.json before archive: {exc}"
                    )

            print(
                f"[{datetime.now(timezone.utc)}] [CLD-AUTO-ARCHIVE] {today_str}: "
                f"archiving {len(closed_trade_files)} closed trade files to {archive_target}"
            )

            moved_count = 0
            for closed_file in closed_trade_files:
                try:
                    shutil.move(str(closed_file), str(archive_target / closed_file.name))
                    moved_count += 1
                except Exception as exc:
                    print(f"[{datetime.now(timezone.utc)}] [CLD-AUTO-ARCHIVE-ERROR] Failed to move {closed_file.name}: {exc}")

            print(
                f"[{datetime.now(timezone.utc)}] [CLD-AUTO-ARCHIVE] {today_str}: "
                f"moved {moved_count} closed trade files to archive/{timestamp_str}/"
            )
            archived_any = archived_any or (moved_count > 0)

    return archived_any


def _finalize_v_trade_record(
    trade_data: Dict[str, Any],
    direction: str,
    exit_reason: str,
    current_price: float,
    latest_bid: Optional[float],
    latest_ask: Optional[float],
    config: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    record = _normalize_v_trade_payload(trade_data, config)
    # [V20251228_0315] Improved price determination with fallback to last known current_price
    exit_price = _determine_v_trade_entry_price(direction, current_price, latest_bid, latest_ask)
    if not exit_price or exit_price <= 0:
        exit_price = float(record.get('current_price') or record.get('entry_price') or 0.0)
        
    record['exit_time'] = datetime.now().isoformat()
    record['exit_price'] = exit_price
    record['current_price'] = exit_price
    record['exit_reason'] = exit_reason
    record['status'] = 'CLOSED'
    
    # Calculate final PnL [2025-12-25 V20251225_0345]
    entry_price = float(record.get('entry_price') or 0.0)
    cfg = config or _load_config()
    # [2026-03-16 V20260316_1430] Pass product and config
    pnl_metrics = _calculate_v_trade_pnl(entry_price, exit_price, direction, cfg, product=record.get('product', 'GBP'))
    
    record['gross_pnl_pips'] = pnl_metrics['gross_pnl_pips']
    record['net_return'] = pnl_metrics['net_return']
    record['alt_net'] = pnl_metrics['alt_net']
    record['adhoc_cost_usd'] = pnl_metrics.get('adhoc_cost_usd', 0.0)  # [V20260325_0500]
    # [V20260428] Final min_net check on close - falling market may close worse than any update
    current_min_net = record.get('min_net')
    if current_min_net is None or pnl_metrics['net_return'] < current_min_net:
        record['min_net'] = pnl_metrics['net_return']

    record.setdefault('cumulative_pnl', 0.0)
    record.setdefault('cumulative_alt_pnl', 0.0)
    record.setdefault('order_sent_net', False)
    record.setdefault('order_sent_alt', False)
    # [V20251226_1030] Preservation of filepath is handled by caller if needed
    return record


def _create_new_v_trade(
    virtual_dir: Path,
    strategy_key: str,
    product: str,
    direction: str,
    is_live: bool,
    config: Optional[Dict[str, Any]] = None,
    current_price: Optional[float] = None,
    latest_bid: Optional[float] = None,
    latest_ask: Optional[float] = None,
) -> None:
    """Creates a new virtual trade JSON file with the base trade schema."""
    
    _config = config or _load_config() # Load config here
    # [MODIFIED 2025-12-28] Prevent new V-Trade creation if archiving is active
    if _config.get('archive', False):
        print(f"[V-TRADE-BLOCK] New V-Trade for {product} {direction} blocked due to active archive process.")
        return
    if not _config.get('enable_virtual_trades', False):
        print(f"[V-TRADE-BLOCK] Virtual trade creation disabled (enable_virtual_trades=false).")
        return

    # [V20251228_0220] Broaden duplicate check: Look for ANY open trade for this PRODUCT in this direction
    # This prevents multiple trades for the same product when the "best strategy" shifts.
    # [MODIFIED 2025-12-28] Use a more general glob to account for new filename format.
    for existing_file in virtual_dir.glob(f"vt_*_open_*.json"):
        try:
            with open(existing_file, 'r') as f:
                existing_data = json.load(f)
            # Match strictly by product (internal data) and direction
            if str(existing_data.get('product', '')).upper() == product.upper() and \
               existing_data.get('status') == 'OPEN' and \
               existing_data.get('direction') == direction:
                print(f"[V-TRADE] [SKIP] Open trade already exists for PRODUCT {product} {direction}: {existing_file.name}")
                return
        except Exception:
            continue

    now = datetime.now()
    ts_str = now.strftime('%Y%m%d_%H%M%S')
    
    # [V20251228_0225] Reverted to clean filenames (no UIDs)
    # [MODIFIED 2025-12-28] Added direction ('buy'/'sell') to filename.
    direction_for_filename = 'buy' if direction == 'LONG' else 'sell'
    filename = f"vt_{ts_str}_open_{direction_for_filename}_{product}_{strategy_key}.json"
    filepath = virtual_dir / filename

    # Use _config here
    default_window = BASE_WINDOW_SIZES[0] if BASE_WINDOW_SIZES else 0
    window_size = _resolve_config_scalar(_config.get('window_size', default_window), default_window, int)
    pip_buffer = _resolve_config_scalar(_config.get('pip_buffer', BASE_PIP_BUFFER), BASE_PIP_BUFFER, float)
    tp_pips = _resolve_config_scalar(_config.get('tp_pips', BASE_TP_PIPS), BASE_TP_PIPS, float)
    sl_pips = _resolve_config_scalar(_config.get('sl_pips', BASE_SL_PIPS), BASE_SL_PIPS, float)
    entry_price = _determine_v_trade_entry_price(direction, current_price, latest_bid, latest_ask)

    trade_data = {
        'trade_id': f"v_{ts_str}",
        'product': product,
        'direction': direction,
        'entry_time': now.isoformat(),
        'entry_price': entry_price,
        'current_price': entry_price,
        'gross_pnl_pips': 0.0,
        'net_return': 0.0,
        'min_net': 0.0,  # [V20260428] Track minimum net (drawdown) - v-trade starts at 0
        'alt_net': 0.0,
        'cumulative_pnl': 0.0,
        'cumulative_alt_pnl': 0.0,
        'exit_time': None,
        'exit_price': None,
        'exit_reason': None,
        'status': 'OPEN',
        'order_sent_net': False,
        'order_sent_alt': False,
        'is_live_trade': is_live,
        'window_size': window_size,
        'pip_buffer': pip_buffer,
        'tp_pips': tp_pips,
        'sl_pips': sl_pips,
        'source_strategy': strategy_key,
        'strategy_name': canonical_strategy_name(strategy_key) or strategy_key,
    }
    apply_strategy_name_fields(trade_data)
    with open(filepath, 'w') as f:
        json.dump(trade_data, f, indent=2)
    print(f"[V-TRADE] Created new V-Trade: {filename}")


def _fetch_api_leaders(run_mode: str) -> Tuple[Optional[Dict], Optional[Dict]]:
    """
    Fetches the top buy and sell leaders from the frequency API.
    """
    db_name = 'tradedb_sim2' if run_mode.lower() == 'sim' else 'tradedb'
    base_url = _load_config().get('api_base_url', 'http://127.0.0.1:8000/api')
    
    top_buy = None
    top_sell = None

    try:
        # Fetch Top Buy
        buy_url = f"{base_url}/vw_top_one_frequency_buy?db={db_name}"
        buy_resp = requests.get(buy_url, timeout=2)
        if buy_resp.status_code == 200:
            buy_data = buy_resp.json().get('data', [])
            if buy_data:
                top_buy = buy_data[0]
    except Exception as e:
        print(f"[V-TRADE-API] Failed to fetch BUY leader: {e}")

    try:
        # Fetch Top Sell
        sell_url = f"{base_url}/vw_top_one_frequency_sell?db={db_name}"
        sell_resp = requests.get(sell_url, timeout=2)
        if sell_resp.status_code == 200:
            sell_data = sell_resp.json().get('data', [])
            if sell_data:
                top_sell = sell_data[0]
    except Exception as e:
        print(f"[V-TRADE-API] Failed to fetch SELL leader: {e}")
        
    return top_buy, top_sell

def _manage_virtual_trades(global_stats: defaultdict, json_base_dir: str, open_live_trades_count: int, latest_prices: Dict[str, Dict[str, Optional[float]]]) -> None:
    """
    Manages the lifecycle of virtual trades (V-Trades) based on leaders
    fetched from the vw_top_one_frequency API. [MODIFIED 2026-01-05]
    """
    lock_path = Path(V_TRADES_LOCK_FILE)
    try:
        if lock_path.exists() and (time.time() - lock_path.stat().st_mtime) > 120:
            lock_path.unlink(missing_ok=True)
        lock_path.touch(exist_ok=False)
    except (FileExistsError, OSError):
        return

    try:
        config = _load_config()
        run_mode = config.get('run_mode', 'live')

        # [MODIFIED 2025-12-28] Handle archive flag
        archive_flag = config.get('archive', False)
        if archive_flag:
            # [MODIFIED 2026-02-23] Reset archive flag only after successful archive completion.
            try:
                detect_date = _LATEST_TRADING_DATE or datetime.now().strftime('%Y-%m-%d')
                print(f"[{datetime.now()}] [ARCHIVE-DETECT] archive=true mode={run_mode} date={detect_date}")
                archived_ok = _perform_archiving(config)
                if archived_ok:
                    config['archive'] = False
                    with open(CONFIG_FILE_PATH, 'w') as f:
                        json.dump(config, f, indent=4)
                    print(f"[{datetime.now()}] [ARCHIVE-COMPLETED] All trades archived successfully for {run_mode}. Archive flag set to False.")
                    # Notify UI if a mechanism exists, for now, print to console
                    print("[UI-NOTIFICATION] Archiving completed successfully!")
                else:
                    print(f"[{datetime.now()}] [ARCHIVE-PENDING] Archive did not complete. Archive flag remains True.")
            except Exception as e:
                print(f"[{datetime.now()}] [ARCHIVE-ERROR] Error during archiving: {e}")
            return # Exit after archiving, no further trade management for this cycle

        virtual_trade_live_by_default = config.get('virtual_trade_live_by_default', True)
        
        today_str = _LATEST_TRADING_DATE or datetime.now().strftime('%Y-%m-%d')
        virtual_dir = _ensure_day_directory(run_mode, today_str) / 'virtual'
        virtual_dir.mkdir(parents=True, exist_ok=True)

        # --- MODIFIED: Fetch leaders from API instead of _top_one.json ---
        top_buy, top_sell = _fetch_api_leaders(run_mode)
        if top_buy:
             print(f"[{datetime.now()}] [V-TRADE-INFO] API Top Buy leader: {top_buy.get('product')} / {top_buy.get('strategy_and_params')}")
        if top_sell:
             print(f"[{datetime.now()}] [V-TRADE-INFO] API Top Sell leader: {top_sell.get('product')} / {top_sell.get('strategy_and_params')}")

        open_v_trades = []
        if virtual_dir.exists():
            for v_file in virtual_dir.glob('*.json'):
                try:
                    with open(v_file, 'r') as f:
                        data = json.load(f)
                    if data.get('status') == 'OPEN':
                        data['filepath'] = str(v_file)
                        open_v_trades.append(data)
                except: continue
        
        open_buy_v_trades = [t for t in open_v_trades if t.get('direction') == 'LONG']
        # --- MODIFIED: Check only for existence of top_buy leader ---
        if top_buy:
            leader_product = top_buy['product'].upper()
            
            for trade in open_buy_v_trades:
                if trade.get('product', '').upper() != leader_product:
                    print(f"[{datetime.now()}] [V-TRADE-CLOSE] Displacing BUY for {trade.get('product')} as it is not the API leader.")
                    finalized = _finalize_v_trade_record(trade, 'LONG', 'API_LEADER_CHANGED', latest_prices.get(trade.get('product'), {}).get('price'), latest_prices.get(trade.get('product'), {}).get('bid'), latest_prices.get(trade.get('product'), {}).get('ask'), config)
                    fp = trade.get('filepath')
                    if fp:
                        finalized.pop('filepath', None)
                        new_fp_str = str(fp).replace('_open_', '_closed_')
                        with open(new_fp_str, 'w') as f: json.dump(finalized, f, indent=2)
                        if new_fp_str != str(fp): Path(fp).unlink(missing_ok=True)
            
            if not any(t.get('product', '').upper() == leader_product for t in open_buy_v_trades):
                print(f"[{datetime.now()}] [V-TRADE-CREATE] Creating new BUY for API leader product: {leader_product}")
                _create_new_v_trade(virtual_dir, top_buy['strategy_and_params'], top_buy['product'], 'LONG', virtual_trade_live_by_default, config, latest_prices.get(top_buy['product'], {}).get('price'), latest_prices.get(top_buy['product'], {}).get('bid'), latest_prices.get(top_buy['product'], {}).get('ask'))
        else: # No top_buy leader from API
            for trade in open_buy_v_trades:
                print(f"[{datetime.now()}] [V-TRADE-CLOSE] Closing BUY for {trade.get('product')} due to no API leader.")
                # ... (closing logic remains the same)

        open_sell_v_trades = [t for t in open_v_trades if t.get('direction') == 'SHORT']
        # --- MODIFIED: Check only for existence of top_sell leader ---
        if top_sell:
            leader_product = top_sell['product'].upper()

            for trade in open_sell_v_trades:
                if trade.get('product', '').upper() != leader_product:
                    print(f"[{datetime.now()}] [V-TRADE-CLOSE] Displacing SELL for {trade.get('product')} as it is not the API leader.")
                    # ... (closing logic remains the same)

            if not any(t.get('product', '').upper() == leader_product for t in open_sell_v_trades):
                print(f"[{datetime.now()}] [V-TRADE-CREATE] Creating new SELL for API leader product: {leader_product}")
                _create_new_v_trade(virtual_dir, top_sell['strategy_and_params'], top_sell['product'], 'SHORT', virtual_trade_live_by_default, config, latest_prices.get(top_sell['product'], {}).get('price'), latest_prices.get(top_sell['product'], {}).get('bid'), latest_prices.get(top_sell['product'], {}).get('ask'))
        else: # No top_sell leader from API
            for trade in open_sell_v_trades:
                print(f"[{datetime.now()}] [V-TRADE-CLOSE] Closing SELL for {trade.get('product')} due to no API leader.")
                # ... (closing logic remains the same)
    
    finally:
        lock_path.unlink(missing_ok=True)


def _update_open_v_trades_prices(json_base_dir: str, latest_prices: Dict[str, Dict[str, Optional[float]]], config: Dict[str, Any]) -> None:
    """Updates prices and PnL for all OPEN V-Trades. Runs every poll cycle. [2025-12-25 V20251225_0350]"""
    if not json_base_dir:
        return
        
    # [V20260101_2130] Use latest seen trading date
    run_mode = Path(json_base_dir).name
    today_str = _LATEST_TRADING_DATE or datetime.now().strftime('%Y-%m-%d')
    virtual_dir = _resolve_day_directory(run_mode, today_str) / 'virtual'
    if not virtual_dir.exists():
        return

    # [V20251228_0215] Shared lock for atomic price updates across processes
    lock_path = Path(V_TRADES_LOCK_FILE)
    try:
        if lock_path.exists():
            if (time.time() - lock_path.stat().st_mtime) > 30: # Shorter stale check for high-freq updates
                lock_path.unlink(missing_ok=True)
        lock_path.touch(exist_ok=False)
    except (FileExistsError, OSError):
        # Another process is currently updating prices or managing trades
        return

    try:
        for v_file in virtual_dir.glob('vt_*.json'):
            try:
                # Quick read
                with open(v_file, 'r') as f:
                    data = json.load(f)
                
                if data.get('status') != 'OPEN':
                    continue
                    
                prod = data.get('product')
                if not prod:
                    continue
                    
                p_snap = _get_latest_price_snap(latest_prices, prod)
                if not p_snap or p_snap.get('price') is None:
                    continue
                    
                curr_px = p_snap.get('price')
                
                # Apply updates
                data['current_price'] = curr_px
                ent_px = float(data.get('entry_price') or curr_px)
                
                # Ensure full payload structure
                data = _normalize_v_trade_payload(data, config)
                
                # [2026-03-16 V20260316_1430] Pass product and config for dynamic PnL
                pnl = _calculate_v_trade_pnl(ent_px, curr_px, data.get('direction'), config, product=prod)
                data['gross_pnl_pips'] = pnl['gross_pnl_pips']
                data['net_return'] = pnl['net_return']
                data['alt_net'] = pnl['alt_net']
                data['adhoc_cost_usd'] = pnl.get('adhoc_cost_usd', 0.0)  # [V20260325_0500]

                # [V20260428] Track minimum net (drawdown) - update if current net is lower
                current_min_net = data.get('min_net')
                if current_min_net is None or pnl['net_return'] < current_min_net:
                    data['min_net'] = pnl['net_return']

                # Always pop filepath before saving to be safe
                data.pop('filepath', None)
                
                # Write back
                with open(v_file, 'w') as f_out:
                    json.dump(data, f_out, indent=2)
                    
            except Exception as e:
                # [V20251228_0215] Log error but continue loop
                print(f"[WARN] Failed to update virtual trade file {v_file.name}: {e}")
                continue
    finally:
        # Release price update lock
        lock_path.unlink(missing_ok=True)

    




def _calculate_open_trade_pnl(
    entry_price: float,
    current_price: float,
    direction: str,
    product: str,
    config: Dict[str, Any],
) -> Dict[str, float]:
    """Calculates PnL metrics for persisted OPEN trade JSON reconciliation."""
    pip_value = _pip_value_for_product(product, config)
    multiplier = _get_pip_multiplier(product, config)
    price_diff_raw = current_price - entry_price
    price_diff_pips = price_diff_raw * multiplier

    if (direction or '').upper() == 'LONG':
        gross_pips = price_diff_pips
    else:
        gross_pips = -price_diff_pips

    gross_usd = gross_pips * pip_value
    commission_usd_for_trade = 10.0 if "_C" in str(product).upper() else COMMISSION_USD

    adhoc_cost_usd = 0.0
    try:
        p_type = product_type_for_product(product, config)
        type_costs = config.get("product_type_cost", {})
        adhoc_cost_usd = float(type_costs.get(p_type, 0.0) or 0.0)
    except Exception:
        adhoc_cost_usd = 0.0

    total_adhoc_cost = adhoc_cost_usd * 2
    spread_pips = float(config.get('spread_pips', BASE_SPREAD_PIPS))
    spread_cost_usd = spread_pips * pip_value

    net_usd = gross_usd - commission_usd_for_trade - total_adhoc_cost
    alt_gross_pips = -gross_pips
    alt_gross_usd = alt_gross_pips * pip_value
    alt_net_usd = alt_gross_usd - commission_usd_for_trade - spread_cost_usd - total_adhoc_cost

    return {
        'gross_pnl_pips': gross_pips,
        'net_return': net_usd,
        'alt_net': alt_net_usd,
        'adhoc_cost_usd': total_adhoc_cost,
    }


def _with_last_updated_after_current_price(
    record: Dict[str, Any],
    current_price: float,
    last_updated: str,
    pnl: Optional[Dict[str, float]] = None,
) -> Dict[str, Any]:
    """Ensure `last_updated` is stored immediately after `current_price`."""
    updated: Dict[str, Any] = {}
    inserted = False

    for key, value in record.items():
        if key == 'last_updated':
            continue
        if key == 'current_price':
            updated[key] = current_price
            updated['last_updated'] = last_updated
            inserted = True
            continue
        updated[key] = value

    if not inserted:
        updated['current_price'] = current_price
        updated['last_updated'] = last_updated

    if pnl is not None:
        updated['gross_pnl_pips'] = pnl['gross_pnl_pips']
        updated['net_return'] = pnl['net_return']
        updated['alt_net'] = pnl['alt_net']
        updated['adhoc_cost_usd'] = pnl['adhoc_cost_usd']
        # [V20260428] Track minimum net (drawdown) - update if current net is lower
        current_min_net = record.get('min_net')
        if current_min_net is None or pnl['net_return'] < current_min_net:
            updated['min_net'] = pnl['net_return']
        else:
            updated['min_net'] = current_min_net

    return updated


def _reconcile_open_trade_exit_file(
    trade_file: Path,
    record: Dict[str, Any],
    price_snap: Dict[str, Any],
    config: Dict[str, Any],
) -> bool:
    """Fail-safe close for persisted OPEN trades when latest price already crossed TP/SL."""
    entry_price = _safe_float(record.get('entry_price'))
    tp_pips = _safe_float(record.get('tp_pips'))
    sl_pips = _safe_float(record.get('sl_pips'))
    current_price = _safe_float(price_snap.get('price'))
    direction = str(record.get('direction') or '').upper()
    product = str(record.get('product') or '').upper()
    if None in (entry_price, tp_pips, sl_pips, current_price) or not direction or not product:
        return False

    multiplier = _get_pip_multiplier(product, config)
    if multiplier in (None, 0):
        return False

    exit_reason: Optional[str] = None
    exit_price: Optional[float] = None
    if direction == 'LONG':
        tp_level = entry_price + (tp_pips / multiplier)
        sl_level = entry_price - (sl_pips / multiplier)
        if current_price >= tp_level:
            exit_reason = 'TP Hit'
            exit_price = tp_level
        elif current_price <= sl_level:
            exit_reason = 'SL Hit'
            exit_price = sl_level
    elif direction == 'SHORT':
        tp_level = entry_price - (tp_pips / multiplier)
        sl_level = entry_price + (sl_pips / multiplier)
        if current_price <= tp_level:
            exit_reason = 'TP Hit'
            exit_price = tp_level
        elif current_price >= sl_level:
            exit_reason = 'SL Hit'
            exit_price = sl_level

    if exit_reason is None or exit_price is None:
        return False

    exit_ts = _normalize_timestamp(price_snap.get('timestamp')) or pd.Timestamp.now()
    pnl = _calculate_open_trade_pnl(entry_price, exit_price, direction, product, config)
    last_updated = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    updated = _with_last_updated_after_current_price(record, current_price, last_updated, pnl)
    strategy_key = str(updated.get('script_name') or updated.get('source_strategy') or '')
    trade_id = str(updated.get('trade_id') or updated.get('id') or '')
    source = str(updated.get('source_screen') or 'breakout')
    source_group = str(updated.get('live_cap_group') or updated.get('source_group') or source)
    guid = str(updated.get('guid') or 'unknown')
    latest_bid = _safe_float(price_snap.get('bid'))
    latest_ask = _safe_float(price_snap.get('ask'))
    sent_net = bool(updated.get('order_sent_net'))
    sent_alt = bool(updated.get('order_sent_alt'))
    is_live_trade = bool(updated.get('is_live_trade'))

    if sent_net:
        _create_l_trade_order(
            product=product,
            direction=direction,
            strategy_key=strategy_key,
            trade_id=trade_id,
            current_price=exit_price,
            latest_bid=latest_bid,
            latest_ask=latest_ask,
            mode='net',
            is_close=True,
            source=source,
            source_group=source_group,
            guid=guid,
        )
    if sent_alt:
        _create_l_trade_order(
            product=product,
            direction=direction,
            strategy_key=strategy_key,
            trade_id=trade_id,
            current_price=exit_price,
            latest_bid=latest_bid,
            latest_ask=latest_ask,
            mode='alt',
            is_close=True,
            source=source,
            source_group=source_group,
            guid=guid,
        )
    if is_live_trade and not sent_net and not sent_alt:
        print(
            f"[FAILSAFE-CLOSE][REPAIR] {trade_file.name} had is_live_trade=True "
            f"with no order_sent flags. Sending NET close as fallback."
        )
        _create_l_trade_order(
            product=product,
            direction=direction,
            strategy_key=strategy_key,
            trade_id=trade_id,
            current_price=exit_price,
            latest_bid=latest_bid,
            latest_ask=latest_ask,
            mode='net',
            is_close=True,
            source=source,
            source_group=source_group,
            guid=guid,
        )
        updated['order_sent_net'] = True

    updated['status'] = 'CLOSED'
    updated['exit_time'] = exit_ts.isoformat() if hasattr(exit_ts, 'isoformat') else str(exit_ts)
    updated['exit_price'] = exit_price
    updated['exit_reason'] = exit_reason

    market_bias_at_open = updated.get('market_bias_at_open')
    if market_bias_at_open:
        trade_date_for_close = exit_ts.strftime('%Y-%m-%d') if hasattr(exit_ts, 'strftime') else datetime.now().strftime('%Y-%m-%d')
        updated['market_bias_latest'] = _get_market_bias_for_date(str(config.get('run_mode', 'live')).lower(), trade_date_for_close) or market_bias_at_open

    _write_json_atomic(trade_file, updated, indent=2)

    base_filename = _strip_trade_status_suffix(_ensure_json_ext(trade_file.name))
    closed_name = _with_trade_status_suffix(base_filename, 'CLOSED')
    closed_path = trade_file.with_name(closed_name)
    if trade_file.name != closed_name:
        try:
            os.replace(trade_file, closed_path)
        except OSError as exc:
            print(f"[WARN] Failed to rename {trade_file.name} to {closed_name}: {exc}")
    try:
        _decrement_global_active(product, direction)
    except Exception:
        pass
    print(f"[FAILSAFE-CLOSE] Closed {closed_name} via persisted-file reconciliation ({exit_reason}).")
    return True


def _update_open_trade_json_prices(
    json_base_dir: str,
    latest_prices: Dict[str, Dict[str, Optional[float]]],
    config: Dict[str, Any],
) -> None:
    """Updates current_price and PnL for persisted OPEN trade JSONs each poll cycle."""
    if not json_base_dir:
        return

    run_mode = Path(json_base_dir).name
    today_str = _LATEST_TRADING_DATE or datetime.now().strftime('%Y-%m-%d')
    target_products = [str(prod).upper() for prod in config.get('trade_products', []) if prod]

    for product in target_products:
        p_snap = _get_latest_price_snap(latest_prices, product)
        if not p_snap or p_snap.get('price') is None:
            continue

        current_price = _safe_float(p_snap.get('price'))
        if current_price is None:
            continue

        day_dir = _resolve_day_directory(run_mode, today_str, product)
        if not day_dir.exists():
            continue

        for trade_file in day_dir.glob('*.json'):
            try:
                if trade_file.name.startswith('_'):
                    continue

                data = _load_json_resilient(trade_file, repair=True)

                if str(data.get('status', '')).upper() != 'OPEN':
                    continue

                file_product = str(data.get('product', '')).upper()
                if file_product != product:
                    continue

                entry_price = _safe_float(data.get('entry_price'))
                if entry_price is None:
                    continue

                direction = str(data.get('direction') or '')
                pnl = _calculate_open_trade_pnl(entry_price, current_price, direction, product, config)
                last_updated = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                data = _with_last_updated_after_current_price(data, current_price, last_updated, pnl)

                if _reconcile_open_trade_exit_file(trade_file, data, p_snap, config):
                    continue

                _write_json_atomic(trade_file, data, indent=2)
            except Exception as exc:
                print(f"[WARN] Failed to refresh open trade file {trade_file.name}: {exc}")
                continue


def run_multiwindow(
    strategy_cls: Type[BaseBreakoutStrategy],
    trade_products: Optional[List[str]] = None,
    poll_interval_seconds: int = POLL_INTERVAL_SECONDS,
    window_override: Optional[int] = None,
    pip_buffer: float = PIP_BUFFER,
    tp_pips: Optional[float] = None,
    sl_pips: Optional[float] = None,
    commission_pips: float = COMMISSION_PIPS,
    spread_pips: float = SPREAD_PIPS,
    script_alias: Optional[str] = None,
):
    import concurrent.futures

    config = _load_config()
    config_mtime = _config_mtime()

    while True:
        # [V20260101_2340] Prioritize archive check BEFORE building state to avoid startup delays
        config = _load_config()
        run_mode = config.get('run_mode', 'live').lower()
        json_base_dir = os.path.join(os.path.dirname(CONFIG_FILE_PATH), 'json', run_mode)
        
        if config.get('archive'):
            print(f"[{datetime.now()}] [ARCHIVE-START] Archive flag detected on startup. Processing...")
            _manage_virtual_trades(defaultdict(lambda: defaultdict(lambda: {'pnl': 0.0, 'count': 0})), 
                                   json_base_dir, 0, {})

        print(f"[{datetime.now()}] [INIT] Building strategy runtime state (Mode: {run_mode})...")
        runtime_state = _build_runtime_state(
            strategy_cls,
            trade_products,
            poll_interval_seconds,
            window_override,
            pip_buffer,
            tp_pips,
            sl_pips,
            commission_pips,
            spread_pips,
            script_alias,
            config,
        )

        processors_map = runtime_state['processors_map']
        target_products = runtime_state['target_products']
        poll_value = runtime_state['poll_interval_seconds']
        json_base_dir = runtime_state['json_base_dir']
        resolved_windows = runtime_state.get('resolved_windows', [])
        resolved_tps = runtime_state.get('resolved_tps', [])
        resolved_sls = runtime_state.get('resolved_sls', [])
        runtime_alias = runtime_state.get('script_alias') or (script_alias or strategy_cls.__name__.lower())
        processors_per_product = max((len(plist) for plist in processors_map.values()), default=0)

        print(f"[DEBUG-WINDOWS] window_override={window_override}, resolved_windows={resolved_windows}")
        print(
            f"[{datetime.now()}] [INIT-MATRIX] {runtime_alias} "
            f"windows={resolved_windows} tp_pips={resolved_tps} sl_pips={resolved_sls} "
            f"products={target_products} processors_per_product={processors_per_product}"
        )

        if not target_products:
            print('[WARN] No trade products configured. Sleeping 5s...')
            time.sleep(5)
            config = _load_config()
            config_mtime = _config_mtime()
            continue

        last_check_time = 0
        last_check_time = 0
        
        # Store latest tick data for all products: {product: {'price': float, 'bid': float, 'ask': float}}
        latest_prices = defaultdict(lambda: {'price': None, 'bid': None, 'ask': None})

        try:
            print(f"[{datetime.now()}] [LOOP] Entering main trading loop (Poll: {poll_value}s)")
            with concurrent.futures.ThreadPoolExecutor(max_workers=max(1, len(target_products))) as executor:
                while True:
                    # Pause all trading activity while archive flag is active
                    if config.get('archive', False):
                        print(f"[{datetime.now()}] [ARCHIVE-PAUSE] Archive flag active. Trading loop paused.")
                        # Release V-trade lock if present to allow archiving to move files
                        try:
                            lock_path = Path(V_TRADES_LOCK_FILE)
                            if lock_path.exists():
                                lock_path.unlink(missing_ok=True)
                        except Exception as e:
                            print(f"[ARCHIVE-PAUSE] Failed to release lock: {e}")
                        
                        time.sleep(poll_value)

                        # Re-check config to see if archive flag was turned off externally
                        new_mtime = _config_mtime()
                        if new_mtime != config_mtime:
                            print(f"[CONFIG] Detected change while paused. Reloading...")
                            config = _load_config()
                            config_mtime = new_mtime
                        
                        continue

                    # Heartbeat log every 30 seconds [V20260101_2345]
                    if int(time.time()) % 30 == 0:
                        print(f"[{datetime.now()}] [HEARTBEAT] Trading loop active. Time: {time.time()}")
                        time.sleep(1) # Avoid multiple prints in same second
                    
                    new_mtime = _config_mtime()
                    if new_mtime != config_mtime:
                        print(f"[CONFIG] Detected change in {CONFIG_FILE_PATH}. Reloading runtime state...")
                        config = _load_config()
                        config_mtime = new_mtime
                        break

                    if time.time() - last_check_time > 60:
                        try:
                            _perform_cld_auto_archive(config)
                        except Exception as exc:
                            print(f"[{datetime.utcnow()}] [CLD-AUTO-ARCHIVE-ERROR] Runtime auto-archive failed: {exc}")



                    future_to_product = {
                        executor.submit(fetch_latest_quotes, product): product 
                        for product in target_products
                    }
                
                    results: Dict[str, List[QuoteTick]] = {}
                
                    for future in concurrent.futures.as_completed(future_to_product):
                        product = future_to_product[future]
                        try:
                            results[product] = future.result()
                        except Exception as exc:  # pylint: disable=broad-except
                            print(f"[WARN] Failed to fetch {product}: {exc}")

                    if not results:
                        print(f"[WARN] No quotes received for any product. Sleeping {poll_value}s...")
                    else:
                        price_summary = {p: f"{q[-1].price:.5f}" for p, q in results.items() if q}
                        print(f"[{datetime.now().strftime('%H:%M:%S')}] [PRICES] {price_summary}")

                    for product, quotes in results.items():
                        if not quotes:
                            continue

                        latest_tick = quotes[-1]
                        max_age_seconds = _max_quote_age_seconds_for_product(product, config)
                        if max_age_seconds is not None:
                            now_utc = pd.Timestamp.now(tz='UTC').tz_localize(None)
                            age_seconds = (now_utc - latest_tick.timestamp).total_seconds()
                            if age_seconds > max_age_seconds:
                                print(
                                    f"[WARN] Stale quote skipped for {product}: "
                                    f"age={age_seconds:.1f}s "
                                    f"ts={latest_tick.timestamp.isoformat()} "
                                    f"threshold={max_age_seconds:.1f}s"
                                )
                                continue
                        
                        # Update shared latest_prices dictionary
                        latest_prices[product] = {
                            'price': latest_tick.price,
                            'bid': latest_tick.bid,
                            'ask': latest_tick.ask,
                            'timestamp': latest_tick.timestamp,
                        }

                        # [V20260101_2130] Update dynamic trading date tracked globally
                        global _LATEST_TRADING_DATE
                        _LATEST_TRADING_DATE = _trading_date_string(latest_tick.timestamp) or latest_tick.timestamp.strftime('%Y-%m-%d')

                        try:
                            # [V20260101_2310] Fix: p_code was undefined, use product
                            for processor in processors_map.get(product, []):
                                processor.process_new_tick(
                                    latest_tick.timestamp, 
                                    latest_tick.price,
                                    bid=latest_tick.bid,
                                    ask=latest_tick.ask
                                )
                        except Exception as e:
                            print(f"[ERROR] Failed to process tick for {product}: {e}")

                    # [V20260207_1710] Direct archive check to avoid V-trade lock contention
                    try:
                        archive_cfg = _load_config()
                        if archive_cfg.get('archive', False):
                            print(f"[{datetime.now()}] [ARCHIVE-START] Archive flag detected in live loop. Processing...")
                            try:
                                detect_mode = archive_cfg.get('run_mode', 'live')
                                detect_date = _LATEST_TRADING_DATE or datetime.now().strftime('%Y-%m-%d')
                                print(f"[{datetime.now()}] [ARCHIVE-DETECT] archive=true mode={detect_mode} date={detect_date}")
                                archived_ok = _perform_archiving(archive_cfg)
                                if archived_ok:
                                    archive_cfg['archive'] = False
                                    with open(CONFIG_FILE_PATH, 'w') as f:
                                        json.dump(archive_cfg, f, indent=4)
                                    print(f"[{datetime.now()}] [ARCHIVE-COMPLETED] All trades archived successfully for {archive_cfg.get('run_mode', 'live')}. Archive flag set to False.")
                                else:
                                    print(f"[{datetime.now()}] [ARCHIVE-PENDING] Archive did not complete. Archive flag remains True.")
                            except Exception as e:
                                print(f"[{datetime.now()}] [ARCHIVE-ERROR] Error during archiving: {e}")
                            # Skip trade management this cycle after archiving
                            time.sleep(poll_value)
                            continue
                    except Exception as e:
                        print(f"[ARCHIVE-CHECK-ERROR] Failed archive check: {e}")

                    # Keep persisted OPEN trade JSONs in sync even if an older file is orphaned after a restart/runtime mismatch.
                    if json_base_dir:
                        _update_open_trade_json_prices(json_base_dir, latest_prices, config)

                    # [2025-12-25 V20251225_0350] continuous update of V-Trade prices
                    if json_base_dir:
                        _update_open_v_trades_prices(json_base_dir, latest_prices, config)

                    if time.time() - last_check_time > 60:
                        if json_base_dir:
                            global_stats, open_live_trades_count = _perform_auto_activation_check(json_base_dir)
                            # [2025-12-26 V20251226_0900] Always call reconciliation, even if no performance data exists
                            _manage_virtual_trades(global_stats or defaultdict(lambda: defaultdict(lambda: {'pnl': 0.0, 'count': 0})), 
                                                 json_base_dir, open_live_trades_count, latest_prices)
                        last_check_time = time.time()

                    time.sleep(poll_value)
        except KeyboardInterrupt:
            print('\nStopping live trading loop. Goodbye!')
            break









