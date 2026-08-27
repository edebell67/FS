# workstreams/WF-101/generate_seed_manifest.py — Generates a deterministic initial DNA registry population.
#
# VERSION HISTORY
# v1.0.0 · 2026-08-23 · Initial version: produces 300 fixed FX strategy definitions and lineage aliases reproducibly.

from __future__ import annotations

import json
from pathlib import Path

from registry import definition_hash, validate_seed_records

POPULATION = 300


def build_records() -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    for offset in range(POPULATION):
        number = 102001 + offset
        strategy_id = f"DNA_{number}"
        definition = {
            "entry_family": ("breakout", "mean_reversion", "momentum")[offset % 3],
            "entry_lookback": (12, 24, 48, 72)[offset % 4],
            "exit_horizon": (6, 12, 24, 48, 96)[offset % 5],
            "risk_boundary_bps": 25 + (offset % 20) * 5,
            "target_boundary_bps": 30 + (offset % 25) * 5,
            "market": "FX",
            "definition_seed": number,
        }
        records.append(
            {
                "strategy_id": strategy_id,
                "definition_version": 1,
                "definition_hash": definition_hash(definition),
                "definition": definition,
                "source_aliases": [f"{strategy_id}_S", f"{strategy_id}_B"],
                "descriptive_name": None,
                "status": "DRAFT",
                "visibility": "private",
                "methodology_version": "1.0.0",
            }
        )
    validate_seed_records(records)
    return records


if __name__ == "__main__":
    output = Path(__file__).with_name("seed_manifest.json")
    output.write_text(json.dumps(build_records(), indent=2) + "\n", encoding="utf-8")
    print(f"wrote {POPULATION} immutable strategy definitions to {output}")

