# epics/ep_062_product_delivery/hermes/build_hermes_version.py — build the separate UI variant from frozen embedded EP062 data.
#
# VERSION HISTORY
# v1.4.0 · 2026-10-07 · The hermes variant carries the Net | Alt net toggle too: both return bases from the source are kept (default Net). An older single-basis source is wrapped and shows no toggle.
# v1.2.0 · 2026-10-06 · Works with any minimum of closed positions (1-12), not only 6: the number word in the page copy comes from the source's min_closed (placeholder __MIN_WORD__).
# v1.1.1 · 2026-10-06 · The history-copy wording is only shown when the source itself was an --as-of rebuild (it was forced on before, which mislabelled fresh builds).
# v1.1.0 · 2026-10-06 · Accepts any min-6 explorer build via --source (default: newest *-min6.html in the parent folder) so the variant can be generated with the latest data; the frozen 750-case check is replaced by a min-6 / both-classes check.
# v1.0.1 · 2026-10-05 · Emit the standard timezone-free generated meta timestamp so the EP062 timestamp validator can parse the snapshot.
# v1.0.0 · 2026-10-05 · Creates a timestamped, self-contained simplified explorer from the verified min-6 HTML without querying the database.

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
def newest_min6() -> Path:
    builds = sorted(HERE.parent.glob("strategy-selection-to-switch-*-min6.html"))
    if not builds:
        raise FileNotFoundError("No *-min6.html explorer build found in the parent folder; build one with build_switch_explorer.py --min-closed 6")
    return builds[-1]


TEMPLATE = HERE / "switch_explorer_hermes_template.html"
WAITLIST = "https://thetechprinciple.com/waitlist/"
NUMBER_WORDS = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine", 10: "ten", 11: "eleven", 12: "twelve"}


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
    ap = argparse.ArgumentParser(description="Build the hermes explorer variant from a min-6 explorer build (no database queries).")
    ap.add_argument("--source", help="explorer build to use (default: newest *-min6.html in the parent folder)")
    args = ap.parse_args()
    source = Path(args.source).resolve() if args.source else newest_min6()
    if not source.is_file() or not TEMPLATE.is_file():
        raise FileNotFoundError(f"Missing source or template: {source} / {TEMPLATE}")

    data = extract_data(source.read_text(encoding="utf-8"))
    if "return_types" not in data:
        # An older single-basis source: wrap it in the two-basis layout the template reads (net only, no toggle shown).
        data["cases"] = {"net|" + k: {**c, "rt": "net"} for k, c in data["cases"].items()}
        data["curves"] = {"net": data["curves"]}
        data["sample"] = {"net": data["sample"]}
        data["return_types"] = ["net"]
        data["default_rt"] = "net"
    elif "net" not in data["return_types"]:
        raise ValueError("The source has no net basis")

    cases = data.get("cases", {})
    by_class: dict[str, int] = {}
    for case in cases.values():
        by_class[case["cls"]] = by_class.get(case["cls"], 0) + 1
    min_closed = data.get("min_closed")
    if not isinstance(min_closed, int) or not 1 <= min_closed <= 12:
        raise ValueError(f"The variant needs a source built with --min-closed 1..12, got {min_closed!r}")
    min_word = NUMBER_WORDS[min_closed]
    if not cases or set(by_class) != {"crypto", "forex"}:
        raise ValueError(f"Source must hold both asset classes: {len(cases)} cases, {by_class}")

    now = datetime.now().astimezone()
    built = now.strftime("%d %b %Y %H:%M")
    summary = "; ".join(
        f"{value['label']}: {value['date']} as of {value['last_snapshot']}"
        for _, value in data["classes"].items()
    )
    data["built_at"] = built
    data["rebuilt_as_of"] = bool(data.get("rebuilt_as_of"))  # a fresh source stays a fresh build; only history copies say "rebuilt"

    template = TEMPLATE.read_text(encoding="utf-8")
    html = (
        template.replace("__MIN_WORD__", min_word)
        .replace("__BUILT_ISO__", now.strftime("%Y-%m-%dT%H:%M:%S"))
        .replace("__DATA_SUMMARY__", summary)
        .replace("__DATA__", json.dumps(data, separators=(",", ":"), ensure_ascii=False))
    )
    if any(x in html for x in ("__DATA__", "__BUILT_ISO__", "__DATA_SUMMARY__", "__MIN_WORD__")):
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
        "source": source.name,
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
