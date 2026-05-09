from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable


def normalize_product_type(product_type: str | None) -> str | None:
    value = str(product_type or "").strip().lower()
    if not value:
        return None
    return "".join(ch if ch.isalnum() or ch in {"_", "-"} else "_" for ch in value)


def default_product_type(config: dict[str, Any] | None = None) -> str:
    normalized = normalize_product_type((config or {}).get("product_type"))
    return normalized or "forex"


def configured_product_types(config: dict[str, Any] | None = None) -> list[str]:
    cfg = config or {}
    values: list[str] = []
    for raw in cfg.get("product_types", []) if isinstance(cfg.get("product_types"), list) else []:
        normalized = normalize_product_type(raw)
        if normalized and normalized not in values:
            values.append(normalized)
    fallback = default_product_type(cfg)
    if fallback not in values:
        values.insert(0, fallback)
    return values


def product_type_for_product(product: str | None, config: dict[str, Any] | None = None) -> str:
    cfg = config or {}
    mapping = cfg.get("product_type_by_product", {})
    if isinstance(mapping, dict):
        product_key = str(product or "").strip().upper()
        for key in (product_key, product_key.lower()):
            normalized = normalize_product_type(mapping.get(key))
            if normalized:
                return normalized
    return default_product_type(cfg)


def load_layout_config(config_file: Path) -> dict[str, Any]:
    try:
        with config_file.open("r", encoding="utf-8") as handle:
            raw = json.load(handle)
        if isinstance(raw, dict):
            return raw
    except Exception:
        pass
    return {}


def day_dir(
    base_path: Path,
    run_mode: str,
    date_str: str,
    product_type: str | None = None,
) -> Path:
    mode = str(run_mode or "live").strip().lower() or "live"
    normalized_product_type = normalize_product_type(product_type)
    # [2026-03-23] Always use product_type subdirectory - prevent legacy json/live/YYYY-MM-DD/ paths
    if not normalized_product_type:
        normalized_product_type = "forex"  # Default to forex if no product_type provided
    return base_path / mode / normalized_product_type / date_str


def resolve_day_dir(
    base_path: Path,
    run_mode: str,
    date_str: str,
    product_type: str | None = None,
) -> Path:
    normalized_product_type = normalize_product_type(product_type)
    if normalized_product_type:
        candidate = day_dir(base_path, run_mode, date_str, normalized_product_type)
        if candidate.exists():
            return candidate
    legacy = day_dir(base_path, run_mode, date_str)
    if legacy.exists():
        return legacy
    if normalized_product_type:
        return day_dir(base_path, run_mode, date_str, normalized_product_type)
    return legacy


def ensure_day_dir(
    base_path: Path,
    run_mode: str,
    date_str: str,
    *,
    config: dict[str, Any] | None = None,
    product: str | None = None,
    product_type: str | None = None,
) -> Path:
    resolved_type = normalize_product_type(product_type)
    if not resolved_type:
        resolved_type = product_type_for_product(product, config)
    target = day_dir(base_path, run_mode, date_str, resolved_type)
    target.mkdir(parents=True, exist_ok=True)
    return target


def iter_day_dirs(
    base_path: Path,
    run_mode: str,
    date_str: str,
    *,
    config: dict[str, Any] | None = None,
    include_legacy: bool = True,
) -> list[Path]:
    cfg = config or {}
    seen: set[str] = set()
    paths: list[Path] = []
    if include_legacy:
        legacy = day_dir(base_path, run_mode, date_str)
        if legacy.exists():
            key = str(legacy.resolve()) if legacy.exists() else str(legacy)
            seen.add(key)
            paths.append(legacy)
    for product_type in configured_product_types(cfg):
        candidate = day_dir(base_path, run_mode, date_str, product_type)
        if not candidate.exists():
            continue
        key = str(candidate.resolve())
        if key in seen:
            continue
        seen.add(key)
        paths.append(candidate)
    mode_root = base_path / str(run_mode or "live").strip().lower()
    if mode_root.exists():
        for child in mode_root.iterdir():
            if not child.is_dir():
                continue
            try:
                candidate = child / date_str
            except TypeError:
                continue
            if not candidate.exists():
                continue
            key = str(candidate.resolve())
            if key in seen:
                continue
            seen.add(key)
            paths.append(candidate)
    return paths
