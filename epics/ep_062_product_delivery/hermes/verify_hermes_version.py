# epics/ep_062_product_delivery/hermes/verify_hermes_version.py — verify the variant and its one approved external waitlist CTA.
#
# VERSION HISTORY
# v1.0.1 · 2026-10-05 · Validate JavaScript-rendered honesty copy in the source markup, not only static visible text.
# v1.0.0 · 2026-10-05 · Adds a variant-specific verifier that permits only the user-requested waitlist link while checking the remaining standalone-data and wording contracts.

from __future__ import annotations

import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

WAITLIST = "https://thetechprinciple.com/waitlist/"
NETWORK = re.compile(
    r"fetch\s*\(|XMLHttpRequest|import\s*\(|<script[^>]+src=|<link\b|@import|https?://|WebSocket|sendBeacon",
    re.I,
)


class VisibleText(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []
        self.skip = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in {"script", "style"}:
            self.skip += 1

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style"} and self.skip:
            self.skip -= 1

    def handle_data(self, data: str) -> None:
        if not self.skip:
            self.parts.append(data)


def extract_data(html: str) -> dict:
    marker = "const DATA="
    start = html.index(marker) + len(marker)
    return json.JSONDecoder().raw_decode(html[start:])[0]


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: verify_hermes_version.py path/to/build.html")
    path = Path(sys.argv[1])
    html = path.read_text(encoding="utf-8")
    data = extract_data(html)
    parser = VisibleText()
    parser.feed(html)
    visible = " ".join(parser.parts)
    checks: list[tuple[bool, str]] = []

    def check(ok: bool, label: str) -> None:
        checks.append((ok, label))

    cases = data.get("cases", {})
    by_class: dict[str, int] = {}
    for case in cases.values():
        by_class[case["cls"]] = by_class.get(case["cls"], 0) + 1
    anchors = re.findall(r'<a\b[^>]*class="waitlistButton"[^>]*>', html, re.I)
    cta_ok = len(anchors) == 1 and f'href="{WAITLIST}"' in anchors[0] and 'target="_blank"' in anchors[0]
    if cta_ok:
        cta_ok = all(x in anchors[0] for x in ('noopener', 'noreferrer'))
    check(cta_ok and html.count(WAITLIST) == 1, "exactly one secure, external waitlist CTA")
    sanitized = html.replace(WAITLIST, "#")
    check(not NETWORK.search(sanitized), "no other network, CDN, external script or stylesheet dependency")
    min_closed = data.get("min_closed")
    words = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine", 10: "ten", 11: "eleven", 12: "twelve"}
    check(isinstance(min_closed, int) and min_closed in words and len(cases) > 0 and set(by_class) == {"crypto", "forex"},
          f"min-{min_closed} data present for both classes: {len(cases)} cases ({by_class.get('crypto', 0)} Crypto / {by_class.get('forex', 0)} Forex)")
    rts = data.get("return_types", [])
    keys_by = {rt_: {k.split("|", 1)[1] for k, c in cases.items() if c.get("rt") == rt_} for rt_ in rts}
    check(bool(rts) and set(rts) <= {"net", "alt"} and data.get("default_rt") == "net",
          f"return basis in the file: {', '.join(rts)}; it opens on net")
    check(len(rts) < 2 or (keys_by["net"] == keys_by["alt"] and keys_by["net"] and 'id="rt"' in html and "function setRT" in html
                           and 'id="rtNote"' in html and "For forex it is not a simple mirror" in html),
          "Net | Alt net toggle present with identical case coverage in both bases and the forex note")
    check(len(data.get("classes", {})) == 2 and all(v.get("last_snapshot") and v.get("date") for v in data["classes"].values()),
          "both classes carry a date and a data-as-of snapshot time: "
          + ", ".join(f"{v.get('label')} {v.get('date')} {v.get('last_snapshot')}" for v in data.get("classes", {}).values()))
    check(bool(re.search(r'<meta name="generated" content="\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}">', html))
          and "Built 20" in html[:600], "generated timestamp is present in meta and leading version comment")
    check("Try a guided example" in visible and "exampleBtn" in html and "function guidedExample" in html,
          "guided example control and behavior present")
    check(f"{words.get(min_closed, '?')} closed positions" in visible.lower() and "__min_word__" not in html.lower() and "reference only" in html.lower()
          and "referenceOnly=MINC>0&&g.trades<MINC" in html,
          "minimum-position explanation (matching the data's minimum) and below-threshold reference-only label present")
    check("Historical switch vs hold" in visible and "function oneSwitch" in html
          and bool(re.search(r'only if its (<span class="nw">net</span>|net) is higher than the strategy you hold', html)),
          "historical replay wording and only-switch-if-better rule preserved")
    check("consistent, traceable comparison" in html and "does not prove an edge" in html,
          "process value is distinguished from performance claims")
    check(not re.search(r"trad(e|es|ing)\b", visible, re.I), "no prohibited trading terms in visible app text")
    check(not re.search(r"@media\s*\(\s*max-width", html) and "@media(min-width:720px)" in html,
          "mobile-first breakpoints use min-width only")
    check(len(html.encode("utf-8")) < 7_000_000 and "__DATA__" not in html,
          "single generated file is under 7 MB with no unresolved data placeholder")

    for ok, label in checks:
        print(("PASS" if ok else "FAIL") + "  " + label)
    passed = sum(ok for ok, _ in checks)
    print(f"{passed}/{len(checks)} variant checks passed")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
