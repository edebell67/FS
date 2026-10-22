# epics/ep_057_sql_to_pgsql/scenario_engine_v2/tools/build_inventory.py — read-only inventory of the page's top-level functions and state, with a body hash per function.
#
# VERSION HISTORY
# v1.1.0 · 2026-10-17 · the main script is the longest inline <script> block, not the last one (engine-client pages append a small block).
# v1.0.0 · 2026-10-16 · Moved into the repo from a scratch script (it was not reproducible before); adds body_sha256 and ordinal (n-th declaration of a name) so duplicates and changed functions are detectable.
"""CLI: python build_inventory.py <page.html> <out_dir>  (refuses to overwrite). Import: build(path) -> dict."""
import hashlib
import json
import re
import sys
from pathlib import Path

DOM = re.compile(r"\b(document\.|getElementById|querySelector|innerHTML|textContent|classList|addEventListener|\.style\.|Plotly|new Chart|\.dataset\b|createElement|showModal|\.close\(\)|alert\(|confirm\(|\.focus\(|scrollIntoView|requestAnimationFrame|window\.open|\.value\s*=)")
FETCH = re.compile(r"fetch\(\s*([`'\"][^`'\"]{0,90})")
STORE = re.compile(r"\b(localStorage|sessionStorage)\b")
VIEW_NAME = re.compile(r"^(render|draw|paint|show|hide|toggle|open|close|bind|init|handle|on[A-Z]|sync.*(UI|Button|Label|Toolbar|Modal|Review)|update.*(UI|Button|Label|Toolbar|Status|Notice|Tab))")
FN_RE = re.compile(r"^    (async\s+)?function\s*\*?\s*([A-Za-z_$][\w$]*)\s*\(")
ARROW_RE = re.compile(r"^    const\s+([A-Za-z_$][\w$]*)\s*=\s*(async\s*)?(\([^)]*\)|[A-Za-z_$][\w$]*)\s*=>")
VAR_RE = re.compile(r"^    (let|const|var)\s+([A-Za-z_$][\w$]*)")


def page_version(lines: list[str]) -> str:
    return next((m.group(0) for l in lines[:30] if (m := re.search(r"v\d+\.\d+\.\d+", l))), "unknown")


def build(src: Path) -> dict:
    lines = Path(src).read_text(encoding="utf-8").splitlines()
    starts = [i for i, l in enumerate(lines) if l.strip() == "<script>"]
    def _end(a):
        return next(i for i in range(a + 1, len(lines)) if lines[i].strip() == "</script>")
    first = max(starts, key=lambda a: _end(a) - a)   # the main script is the longest inline block (generated pages add small ones)
    main_start = first + 1
    main_end = _end(first)
    funcs, state, wiring, seen = [], [], [], {}
    i = main_start
    while i < main_end:
        l = lines[i]
        m, a = FN_RE.match(l), ARROW_RE.match(l)
        if m or a:
            name = m.group(2) if m else a.group(1)
            j = i
            if not l.rstrip().endswith("}") or l.count("{") != l.count("}"):
                j = i + 1
                while j < main_end and not re.match(r"^    [}\)]", lines[j]):
                    j += 1
            body = "\n".join(lines[i:j + 1])
            dom = len(DOM.findall(body))
            kind = "engine" if dom == 0 else ("view" if VIEW_NAME.match(name) else "mixed")
            seen[name] = seen.get(name, 0) + 1
            funcs.append({"name": name, "ordinal": seen[name], "async": bool(m and m.group(1)) or bool(a and a.group(2)),
                          "kind": kind, "arrow": bool(a), "start_line": i + 1, "end_line": j + 1, "lines": j - i + 1,
                          "dom_refs": dom, "fetches": sorted(set(f.strip("`'\"") for f in FETCH.findall(body))),
                          "storage": bool(STORE.search(body)), "body_sha256": hashlib.sha256(body.encode("utf-8")).hexdigest()})
            i = j + 1
            continue
        v = VAR_RE.match(l)
        if v:
            state.append({"name": v.group(2), "decl": v.group(1), "line": i + 1})
        elif re.match(r"^    [A-Za-z_$][\w$.\[\]()'\"]*\.(addEventListener|onclick|onchange)|^    document\.|^    window\.", l):
            wiring.append({"line": i + 1, "text": l.strip()[:110]})
        i += 1
    counts = {k: sum(1 for f in funcs if f["kind"] == k) for k in ("engine", "view", "mixed")}
    summary = {"source": Path(src).name, "page_version": page_version(lines), "main_script_lines": [main_start + 1, main_end],
               "function_count": len(funcs), "state_vars": len(state), "top_level_wiring_statements": len(wiring),
               "by_kind": counts, "fetch_endpoints": sorted({e for f in funcs for e in f["fetches"]})}
    return {"summary": summary, "functions": funcs, "state": state, "wiring": wiring}


if __name__ == "__main__":
    src, out = Path(sys.argv[1]), Path(sys.argv[2])
    if (out / "inventory.json").exists():
        sys.exit(f"{out / 'inventory.json'} exists; not overwriting")
    out.mkdir(parents=True, exist_ok=True)
    inv = build(src)
    (out / "inventory.json").write_text(json.dumps(inv, indent=1), encoding="utf-8")
    print(json.dumps(inv["summary"], indent=1))
