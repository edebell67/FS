import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Tuple
from json_layout import configured_product_types, default_product_type, ensure_day_dir, load_layout_config
from paths import BREAKOUT_JSON_ROOT


CONFIG_PATH = Path(__file__).parent / "config.json"
JSON_ROOT = BREAKOUT_JSON_ROOT


def load_run_mode(config_path: Path) -> str:
    try:
        cfg = json.loads(config_path.read_text())
        return str(cfg.get("run_mode", "live")).lower()
    except Exception:
        return "live"


def collect_live_trades(directory: Path) -> Dict[str, Dict]:
    live_trades: Dict[str, Dict] = {}

    def canonical_stem(path: Path) -> str:
        stem = path.stem
        if stem.endswith("_op"):
            return stem[:-3]
        if stem.endswith("_cld"):
            return stem[:-4]
        return stem

    def process(path: Path, status: str) -> None:
        try:
            data = json.loads(path.read_text())
        except Exception:
            return
        if not data.get("is_live_trade"):
            return
        trade_id = str(data.get("trade_id") or path.stem)
        script_name = data.get("script_name", "unknown")
        # Use source-file canonical stem to prevent collisions when simple trade_id is reused.
        stem_key = canonical_stem(path)
        unique_key = f"{script_name}|{stem_key}"

        existing = live_trades.get(unique_key)
        if existing:
            if existing["trade_status"] == "OPEN" and status == "CLOSED":
                pass
            else:
                return
        live_trades[unique_key] = {
            **data,
            "trade_id": trade_id,
            "trade_status": status,
            "source_group": data.get("source_group") or data.get("source_screen") or "breakout",
            "source_file": path.name,
        }

    for pattern, status in [("_op.json", "OPEN"), ("_cld.json", "CLOSED")]:
        for filepath in directory.glob(f"*{pattern}"):
            process(filepath, status)

    return live_trades


def write_output(trades: Dict[str, Dict], directory: Path) -> None:
    output = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "trade_count": len(trades),
        "trades": list(trades.values()),
    }
    out_path = directory / "_live_trades.json"
    out_path.write_text(json.dumps(output, indent=2))
    print(f"Wrote {len(trades)} live trades to {out_path}")


def parse_args() -> Tuple[str, str]:
    parser = argparse.ArgumentParser(description="Extract live trades into _live_trades.json")
    parser.add_argument("--run-mode", default=None, help="Run mode folder (live/sim)")
    parser.add_argument("--date", default=None, help="Trading date (YYYY-MM-DD)")
    args = parser.parse_args()
    return args.run_mode, args.date


def main() -> None:
    run_mode_arg, date_arg = parse_args()
    run_mode = (run_mode_arg or load_run_mode(CONFIG_PATH)).lower()
    target_date = date_arg or datetime.now().strftime("%Y-%m-%d")
    cfg = load_layout_config(CONFIG_PATH)
    cfg.setdefault("product_type", default_product_type(cfg))
    cfg.setdefault("product_types", configured_product_types(cfg))
    target_dir = ensure_day_dir(JSON_ROOT, run_mode, target_date, config=cfg)
    if not target_dir.exists():
        raise SystemExit(f"No data directory found: {target_dir}")

    live_trades = collect_live_trades(target_dir)
    write_output(live_trades, target_dir)


if __name__ == "__main__":
    main()
