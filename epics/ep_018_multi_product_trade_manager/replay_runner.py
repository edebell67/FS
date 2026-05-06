import csv
import json
from pathlib import Path
from trade_manager import (
    Variant, Trade, maybe_enter, manage, log_decision, calc_pnl
)


def load_config(path="config.json"):
    with open(path, "r") as f:
        return json.load(f)


def replay_product(product, cfg):
    product = product.lower()
    path = Path(cfg["output_dir"]) / f"{product}_price_replay_log.csv"

    if not path.exists():
        raise FileNotFoundError(f"Replay file not found: {path}")

    variants = [
        Variant(product=product, name=f"{product}_bank_{b}", bank_threshold=b)
        for b in cfg["bank_variants"]
    ]

    with open(path, "r") as f:
        reader = csv.DictReader(f)

        for row in reader:
            bid = float(row["bid"])
            ask = float(row["ask"])
            mid = float(row["mid"])

            for v in variants:
                maybe_enter(v, bid, ask, mid, cfg)
                manage(v, bid, ask, cfg)
                v.previous_mid = mid

    print(f"\nReplay results for {product}")
    print("-" * 50)
    for v in variants:
        t = v.trade
        total = t.banked_profit + t.open_pnl
        print(
            f"{v.name:<18} | banked={t.banked_profit:>8.2f} | "
            f"open={t.open_pnl:>8.2f} | total={total:>8.2f} | "
            f"size={t.size:>6} | trades={v.trade_count}"
        )


if __name__ == "__main__":
    cfg = load_config()
    for product in cfg["products"]:
        replay_product(product, cfg)
