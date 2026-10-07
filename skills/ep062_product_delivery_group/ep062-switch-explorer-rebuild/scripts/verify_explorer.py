"""Static checks for a built "Select. Compare. Switch." explorer file.

    python verify_explorer.py path/to/strategy-selection-to-switch-simple.html

Exit code 0 = every check passed, 1 = at least one failed. Prints one line per check.
Checks the delivery promises: one self-contained file, no server or network needed, wording rules,
distinct net returns, no clone selected as an alternative, and a visible data-as-of stamp.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

NETWORK = re.compile(r"fetch\(|XMLHttpRequest|import\(|<script[^>]+src=|<link\b|@import|https?://|WebSocket|sendBeacon", re.I)


def main(path: str) -> int:
    html = Path(path).read_text(encoding="utf-8")
    results: list[tuple[bool, str]] = []

    def check(ok: bool, label: str, detail: str = "") -> None:
        results.append((ok, f"{label}{': ' + detail if detail else ''}"))

    size_kb = len(html.encode("utf-8")) / 1024
    check(size_kb < 7000, "file size reasonable (under 7 MB)", f"{size_kb:.0f} KB")

    WAITLIST = "https://thetechprinciple.com/waitlist/"
    anchors = re.findall(r"<a[ 	][^>]*class=.waitlistButton.[^>]*>", html, re.I)
    cta_ok = len(anchors) == 1 and f'href="{WAITLIST}"' in anchors[0] and 'target="_blank"' in anchors[0]         and "noopener" in anchors[0] and "noreferrer" in anchors[0] and html.count(WAITLIST) == 1
    check(cta_ok, "exactly one secure external link: the Join the Arena waitlist button")
    html_for_net = html.replace(WAITLIST, "#")
    hits = NETWORK.findall(html_for_net)
    check(not hits, "self-contained (no fetch, external script, link, font or url)", f"{len(hits)} hits" if hits else "")

    match = re.search(r"const DATA=(.*?);\nconst \$=", html, re.S)
    check(bool(match), "embedded DATA found")
    if not match:
        return report(results)
    data = json.loads(match.group(1))
    cases, curves_by = data["cases"], data["curves"]
    rts = data.get("return_types", ["net"])
    curves = {m: 1 for rt_ in rts for m in curves_by.get(rt_, {})}
    models = data.get("models", {})
    check(bool(models), "compact rows with a strategy lookup present", f"{len(models)} strategies")
    # Rows are stored as short arrays; rebuild the dicts exactly as the page does.
    row = lambda a: dict(model=a[0], strategy=models[a[0]][0], product=models[a[0]][1], trades=a[1], win=a[2], net=a[3],
                         corr=a[4] if len(a) > 4 else None)
    for c in cases.values():
        c["top"] = [row(a) for a in c["top"]]
        c["similar"] = [row(a) for a in c["similar"]]
        c["opposite"] = [row(a) for a in c["opposite"]]
        c["tinfo"] = {k: (row(g) if g else None) for k, g in c["tinfo"].items()}
    check(len(cases) > 0, "cases present", f"{len(cases)} cases, {sum(len(v) for v in curves_by.values())} curves across {len(rts)} basis")
    classes = data.get("classes", {})
    asof = ", ".join(f"{k} {v.get('date')} as of {v.get('last_snapshot')}" for k, v in classes.items())
    check(bool(data.get("built_at")) and bool(classes) and all(v.get("last_snapshot") for v in classes.values()),
          "data-as-of stamp present per asset class", f"{asof}; built {data.get('built_at')}")
    check(bool(re.search(r'<meta name="generated" content="\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}">', html)) and "Built 20" in html[:600],
          "build timestamp embedded (meta tag and leading comment)")
    stray = [k for k, c in cases.items() if c["cls"] not in classes or (c["product"] != "ALL" and c["product"] not in classes[c["cls"]]["products"])]
    check(not stray, "every case belongs to a known asset class and product", f"{len(stray)} stray")
    models_by_cls = {k: {m for c in cases.values() if c["cls"] == k for m in [c["selected"], *[t["model"] for t in c["top"]],
                     *[x for x in c["targets"].values() if x]]} for k in classes}
    overlap = set.intersection(*models_by_cls.values()) if len(models_by_cls) > 1 else set()
    check(not overlap, "crypto and forex are kept separate (no strategy appears in both)", f"{len(overlap)} shared")
    check(f"Data as of" in html and "id=\"stamp\"" in html, "stamp element wired into the page")

    visible = re.sub(r"<script>.*?</script>", "", html, flags=re.S)
    visible = re.sub(r"<style>.*?</style>", "", visible, flags=re.S)
    check(not re.search(r"trad(e|es|ing)\b", visible, re.I), "wording: no 'trade' in visible text")
    check("switch" in visible.lower() and "closed position" in visible.lower(), "wording: 'switch' and 'closed positions' used")

    dup_top = [k for k, c in cases.items() if len({t["net"] for t in c["top"]}) != len(c["top"])]
    dup_opp = [k for k, c in cases.items() if len({t["net"] for t in c["opposite"]}) != len(c["opposite"])]
    check(not dup_top and not dup_opp, "distinct net returns in top and opposite lists", f"{len(dup_top)} / {len(dup_opp)} cases with duplicates")
    clones = [k for k, c in cases.items() for g in c["tinfo"].values()
              if g and g["model"] != c["selected"] and g["net"] == c["similar"][0]["net"]]
    check(not clones, "no switch target is a clone of the selected strategy", f"{len(clones)} found")
    same_model = [k for k, c in cases.items() for g in c["tinfo"].values() if g and g["model"] == c["selected"]]
    check(not same_model, "no switch target is the selected strategy itself", f"{len(same_model)} found")
    missing = [m for c in cases.values() for m in [c["selected"], *[t["model"] for t in c["top"]],
               *[x for x in c["targets"].values() if x]] if m not in curves_by.get(c["rt"], {})]
    check(not missing, "every selected or target strategy has a curve", f"{len(set(missing))} missing")
    min_closed = data.get("min_closed", 0)
    short_closed = [k for k, c in cases.items() if c["similar"][0]["trades"] < min_closed]
    check(not short_closed, f"selected strategies respect the minimum closed positions ({min_closed}; 0 = no filter)", f"{len(short_closed)} below")
    stale = min_closed == 0 and bool(re.search(r"at least 6 closed|have 6 closed", visible))
    check(not stale, "no hard-coded closed-position filter wording in the page text")
    check(set(data["scen"]) == {"net", "win", "side"}, "three selection scenarios present")
    keys_by = {rt_: {k.split("|", 1)[1] for k, c in cases.items() if c["rt"] == rt_} for rt_ in rts}
    both = len(rts) == 2
    check(set(rts) <= {"net", "alt"} and rts, f"return basis in this file: {', '.join(rts)} (default {data.get('default_rt')})")
    check(not both or (keys_by["net"] == keys_by["alt"] and keys_by["net"]),
          "both bases cover exactly the same cases (same classes, products, scenarios and hours)",
          ", ".join(f"{k}: {len(v)}" for k, v in keys_by.items()))
    check(not both or ('id="rt"' in html and 'id="rtNote"' in html and "function setRT" in html and 'class="nw"' in html),
          "Net | Alt net toggle, its note and the dynamic wording are in the page")
    check("Forex" not in html or "For forex it is not a simple mirror" in html, "forex warning for alt net is present")
    check(data.get("default_rt") == "net" or rts == ["alt"], "the file opens on Net unless it is an alt-only build")
    check('width=device-width' in html and 'viewport-fit=cover' in html, "mobile: viewport meta with safe-area support")
    check('class="tabbar"' in html and '@media(min-width:720px)' in html, "mobile first: bottom stage bar and min-width breakpoint")
    check(not re.search(r"@media\s*\(\s*max-width", html), "mobile first: no max-width media queries")
    return report(results)


def report(results: list[tuple[bool, str]]) -> int:
    for ok, line in results:
        print(("PASS  " if ok else "FAIL  ") + line)
    failed = sum(1 for ok, _ in results if not ok)
    print(f"\n{len(results) - failed}/{len(results)} checks passed")
    return 1 if failed else 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    raise SystemExit(main(sys.argv[1]))
