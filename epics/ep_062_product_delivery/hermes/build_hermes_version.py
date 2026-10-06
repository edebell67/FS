# epics/ep_062_product_delivery/hermes/build_hermes_version.py — build the separate UI variant from frozen embedded EP062 data.
#
# VERSION HISTORY
# v1.0.1 · 2026-10-05 · Emit the standard timezone-free generated meta timestamp so the EP062 timestamp validator can parse the snapshot.
# v1.0.0 · 2026-10-05 · Creates a timestamped, self-contained simplified explorer from the verified min-6 HTML without querying the database.

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "strategy-selection-to-switch-20261005-1620.html"
TEMPLATE = HERE / "switch_explorer_hermes_template.html"
WAITLIST = "https://thetechprinciple.com/waitlist/"


def extract_data(html: str) -> dict:
    marker = "const DATA="
    start = html.find(marker)
    if start < 0:
        raise ValueError("Source HTML does not contain embedded DATA")
    start += len(marker)
    data, _ = json.JSONDecoder().raw_decode(html[start:])
    if not isinstance(data, dict):
        raise ValueError("Embedded DATA is not an object")
    return data


def main() -> None:
    if not SOURCE.is_file() or not TEMPLATE.is_file():
        raise FileNotFoundError(f"Missing source or template: {SOURCE} / {TEMPLATE}")

    data = extract_data(SOURCE.read_text(encoding="utf-8"))
    cases = data.get("cases", {})
    by_class: dict[str, int] = {}
    for case in cases.values():
        by_class[case["cls"]] = by_class.get(case["cls"], 0) + 1
    if data.get("min_closed") != 6:
        raise ValueError(f"Expected min_closed=6, got {data.get('min_closed')!r}")
    if len(cases) != 750 or by_class != {"crypto": 336, "forex": 414}:
        raise ValueError(f"Frozen input changed unexpectedly: {len(cases)} cases, {by_class}")

    now = datetime.now().astimezone()
    built = now.strftime("%d %b %Y %H:%M")
    summary = "; ".join(
        f"{value['label']}: {value['date']} as of {value['last_snapshot']}"
        for _, value in data["classes"].items()
    )
    data["built_at"] = built
    data["rebuilt_as_of"] = True

    template = TEMPLATE.read_text(encoding="utf-8")
    html = (
        template.replace("__BUILT_ISO__", now.strftime("%Y-%m-%dT%H:%M:%S"))
        .replace("__DATA_SUMMARY__", summary)
        .replace("__DATA__", json.dumps(data, separators=(",", ":"), ensure_ascii=False))
    )
    if "__DATA__" in html or "__BUILT_ISO__" in html or "__DATA_SUMMARY__" in html:
        raise ValueError("Template placeholders were not fully rendered")

    out = HERE / f"strategy-selection-to-switch-hermes-{now:%Y%m%d-%H%M}.html"
    if out.exists():
        raise FileExistsError(f"Refusing to overwrite timestamped build: {out}")
    html = html.replace(
        "epics/ep_062_product_delivery/hermes/switch_explorer_hermes_template.html",
        f"epics/ep_062_product_delivery/hermes/{out.name}",
        1,
    )
    if html.count(WAITLIST) != 1:
        raise ValueError("Expected exactly one waitlist destination link")
    if re.search(r"<script\s+src=|<link[^>]+href=|@import\s+url\s*\(|\bfetch\s*\(", html, re.I):
        raise ValueError("Unexpected external dependency or network request in the output")

    out.write_text(html, encoding="utf-8")
    print(json.dumps({
        "output": str(out),
        "bytes": out.stat().st_size,
        "built_at": built,
        "source_data_as_of": {k: v["last_snapshot"] for k, v in data["classes"].items()},
        "min_closed": data["min_closed"],
        "cases": len(cases),
        "cases_by_class": by_class,
        "waitlist_link_count": html.count(WAITLIST),
        "external_dependencies": 0,
        "database_queries": 0,
    }, indent=2))


if __name__ == "__main__":
    main()
