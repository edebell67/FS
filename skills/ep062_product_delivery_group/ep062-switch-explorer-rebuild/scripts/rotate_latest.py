#!/usr/bin/env python3
"""Rotate the live EP062 explorer builds: latest/ -> arc/, then install the new builds in latest/.

Live layout (repo edebell67/epics, folder epic/ep062/):
    latest/index.html   guided (hermes) build   -> https://thetechprinciple.com/epic/ep062/latest/
    latest/full.html    full build              -> https://thetechprinciple.com/epic/ep062/latest/full.html
    arc/                every earlier build, never deleted
    index.html          landing page (latest cards + Archive lists)

Usage:
    python rotate_latest.py <path to epic/ep062> --guided <new hermes build> --full <new main build> [--dry-run]

It never overwrites or deletes an archived build. It stops if an archive name already exists.
"""
from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path

GENERATED = re.compile(r'<meta name="generated" content="(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2})')
DATA_LINE = re.compile(r"Data: Crypto: (\d{4}-\d{2}-\d{2}) as of (\d{2} \w{3}) (\d{2}:\d{2})")
KINDS = {
    "guided": ("latest/index.html", "strategy-selection-to-switch-hermes-{stamp}.html", "Choose, Compare, Review"),
    "full": ("latest/full.html", "strategy-selection-to-switch-{stamp}-full.html", "Select, Compare, Switch"),
}
MONTHS = {"01": "Jan", "02": "Feb", "03": "Mar", "04": "Apr", "05": "May", "06": "Jun", "07": "Jul", "08": "Aug",
          "09": "Sep", "10": "Oct", "11": "Nov", "12": "Dec"}


def built(path: Path) -> tuple[str, str]:
    """Return (file stamp YYYYMMDD-HHMM, label '9 Oct 2026, 14:56') from the build's own generated meta tag."""
    m = GENERATED.search(path.read_text(encoding="utf-8")[:4000])
    if not m:
        sys.exit(f"{path}: no <meta name=\"generated\"> tag; is this an explorer build?")
    y, mo, d, h, mi = m.groups()
    return f"{y}{mo}{d}-{h}{mi}", f"{int(d)} {MONTHS[mo]} {y}, {h}:{mi}"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("epic_dir", type=Path, help="the epic/ep062 folder of the epics repo clone")
    ap.add_argument("--guided", type=Path, required=True, help="new hermes (guided) build")
    ap.add_argument("--full", type=Path, required=True, help="new main (full) build")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    root = a.epic_dir
    (root / "arc").mkdir(exist_ok=True)
    (root / "latest").mkdir(exist_ok=True)
    page = root / "index.html"
    html = page.read_text(encoding="utf-8")
    plan = []
    for kind, new in (("guided", a.guided), ("full", a.full)):
        target, arc_name, heading = KINDS[kind]
        live = root / target
        if live.exists():
            stamp, label = built(live)
            dest = root / "arc" / arc_name.format(stamp=stamp)
            if dest.exists():
                sys.exit(f"archive already holds {dest.name}; the file in latest/ is the same build as an archived one. Nothing changed.")
            plan.append((kind, live, dest, label, heading))
        plan.append((kind, new, live, None, heading))
    if a.dry_run:
        for kind, src, dst, label, _ in plan:
            print(f"{kind}: {src} -> {dst}")
        return 0
    for kind, src, dst, label, heading in plan:
        if label:  # archive the old latest
            shutil.move(str(src), str(dst))
            entry = f'          <li><a href="arc/{dst.name}">{label}</a></li>\n'
            i = html.index(f"<h3 class=\"mono\">{heading}</h3>")
            j = html.index("<ul>\n", i) + len("<ul>\n")
            html = html[:j] + entry + html[j:]
        else:  # install the new latest
            shutil.copyfile(src, dst)
    m = DATA_LINE.search((root / KINDS["guided"][0]).read_text(encoding="utf-8")[:3000])
    if m:
        date, _, hhmm = m.groups()
        y, mo, d = date.split("-")
        html = re.sub(r"Latest data: [^.]*?as of \d{2}:\d{2}\.", f"Latest data: {int(d)} {MONTHS[mo]} {y}, as of {hhmm}.", html, count=1)
    page.write_text(html, encoding="utf-8")
    site_map = root.parent.parent / "sitemap.xml"
    if site_map.exists() and m:
        text = site_map.read_text(encoding="utf-8")
        text = re.sub(r"(epic/ep062/</loc>\s*<lastmod>)[^<]*", rf"\g<1>{date}", text)
        site_map.write_text(text, encoding="utf-8")
    print("rotated: old latest builds are in arc/, new builds are in latest/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
