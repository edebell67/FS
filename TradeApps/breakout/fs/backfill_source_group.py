import argparse
import json
from pathlib import Path


def backfill_day(day_dir: Path) -> int:
    updated = 0
    for fp in day_dir.glob("*.json"):
        name = fp.name.lower()
        if not (name.endswith("_op.json") or name.endswith("_cl.json") or name.endswith("_cld.json")):
            continue
        try:
            data = json.loads(fp.read_text())
        except Exception:
            continue
        if "source_group" in data and str(data.get("source_group") or "").strip():
            continue
        source_screen = str(data.get("source_screen") or "breakout")
        data["source_group"] = source_screen
        try:
            fp.write_text(json.dumps(data, indent=2))
            updated += 1
        except Exception:
            continue
    return updated


def main() -> None:
    parser = argparse.ArgumentParser(description="Backfill source_group into trade JSON files.")
    parser.add_argument("--mode", default="live", help="Mode folder under json (live/sim)")
    parser.add_argument("--date", required=True, help="Target date YYYY-MM-DD")
    args = parser.parse_args()

    root = Path(__file__).parent / "json" / args.mode / args.date
    if not root.exists():
        raise SystemExit(f"Directory not found: {root}")
    updated = backfill_day(root)
    print(f"Backfilled source_group in {updated} files under {root}")


if __name__ == "__main__":
    main()
