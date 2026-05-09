from __future__ import annotations

import hashlib
import re
from typing import Any, Dict, Optional


WORDS = [
    "alpha",
    "amber",
    "apex",
    "arc",
    "atlas",
    "aurora",
    "axiom",
    "basil",
    "blaze",
    "cinder",
    "cipher",
    "cobalt",
    "comet",
    "cosmos",
    "delta",
    "drift",
    "echo",
    "ember",
    "falcon",
    "flux",
    "frost",
    "gamma",
    "glint",
    "granite",
    "harbor",
    "helix",
    "ion",
    "jade",
    "juno",
    "kappa",
    "kepler",
    "lattice",
    "legend",
    "lotus",
    "lumen",
    "matrix",
    "meridian",
    "mirage",
    "monarch",
    "nebula",
    "nova",
    "onyx",
    "orion",
    "phoenix",
    "pilot",
    "prism",
    "quartz",
    "quill",
    "radar",
    "raven",
    "ridge",
    "rocket",
    "sable",
    "sierra",
    "sigma",
    "solstice",
    "spark",
    "spire",
    "summit",
    "talon",
    "tango",
    "theta",
    "topaz",
    "vector",
    "vertex",
    "vortex",
    "wave",
    "zen",
    "zenith",
]

_NAME_RE = re.compile(
    r"^(?P<strategy>[A-Za-z][A-Za-z0-9_]*?)_(?P<window>\d+)_tp(?P<tp>-?\d+(?:\.\d+)?)_sl(?P<sl>-?\d+(?:\.\d+)?)$"
)
_INSTANCE_SUFFIX_RE = re.compile(r"^(?P<base>.+)_(?P<suffix>[0-9a-f]{8})$", re.IGNORECASE)


def md5_hex(value: str) -> str:
    return hashlib.md5(value.encode("utf-8")).hexdigest()


def canonical_strategy_name(name: str | None) -> Optional[str]:
    raw = str(name or "").strip()
    if not raw:
        return None
    if _NAME_RE.fullmatch(raw):
        return raw
    suffix_match = _INSTANCE_SUFFIX_RE.fullmatch(raw)
    if suffix_match:
        base = suffix_match.group("base")
        if _NAME_RE.fullmatch(base):
            return base
    return None


def parse_strategy_name(name: str | None) -> Optional[Dict[str, str]]:
    canonical = canonical_strategy_name(name)
    if not canonical:
        return None
    match = _NAME_RE.fullmatch(canonical)
    if not match:
        return None
    return {
        "strategy_name": canonical,
        "strategy": match.group("strategy"),
        "window": match.group("window"),
        "tp": match.group("tp"),
        "sl": match.group("sl"),
    }


def _short_code(value: str, length: int = 3) -> str:
    return md5_hex(value)[:length]


def strategy_alias(strategy: str, product: str) -> str:
    digest = md5_hex(f"{str(product or '').upper()}_{strategy}")
    first_idx = int(digest[0:8], 16) % len(WORDS)
    second_idx = int(digest[8:16], 16) % len(WORDS)
    first = WORDS[first_idx]
    second = WORDS[second_idx]
    if second == first:
        second = WORDS[(second_idx + 1) % len(WORDS)]
    return f"{first}-{second}"


def gen_strategy_name(strategy_name: str | None, product: str | None) -> Optional[str]:
    parsed = parse_strategy_name(strategy_name)
    if not parsed or not product:
        return None
    product_key = str(product).strip().upper()
    alias = strategy_alias(parsed["strategy"], product_key)
    tp_code = _short_code(f"{product_key}_tp_{parsed['tp']}")
    sl_code = _short_code(f"{product_key}_sl_{parsed['sl']}")
    return f"{alias}_{parsed['window']}_z{tp_code}_d{sl_code}"


def apply_strategy_name_fields(record: Dict[str, Any]) -> bool:
    if not isinstance(record, dict):
        return False

    product = record.get("product")
    raw_strategy = (
        record.get("strategy_name")
        or record.get("source_strategy")
        or record.get("script_name")
        or record.get("app_name")
    )
    canonical = canonical_strategy_name(raw_strategy)
    if not canonical:
        return False

    changed = False
    if record.get("strategy_name") != canonical:
        record["strategy_name"] = canonical
        changed = True

    generated = gen_strategy_name(canonical, product)
    if not generated:
        return changed
    if record.get("gen_strategy_name") != generated:
        record["gen_strategy_name"] = generated
        changed = True

    return changed
