#!/usr/bin/env python3
"""Generate a private, original website shell plus a demo-only assistant draft.

The generator deliberately captures only small public structural signals from the
source URL (title, description, H1 and navigation labels). It does not copy page
HTML, images, stylesheets, reviews, or substantial text from the source site.
"""
from __future__ import annotations

import argparse
import html
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.request import Request, urlopen

ASSISTANT_BASE = "https://shared-website-assistant-api.onrender.com"


class PublicStructureParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.title = ""
        self.description = ""
        self.h1 = ""
        self.nav_labels: list[str] = []
        self._tag = ""
        self._nav_depth = 0
        self._text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_dict = dict(attrs)
        if tag == "meta" and (attrs_dict.get("name") or "").lower() == "description":
            self.description = (attrs_dict.get("content") or "")[:300]
        if tag == "nav":
            self._nav_depth += 1
        if tag in {"title", "h1", "a"}:
            self._tag = tag
            self._text = []

    def handle_endtag(self, tag: str) -> None:
        if tag == "nav":
            self._nav_depth = max(0, self._nav_depth - 1)
        if tag != self._tag:
            return
        text = " ".join("".join(self._text).split())[:100]
        if tag == "title":
            self.title = text
        elif tag == "h1" and not self.h1:
            self.h1 = text
        elif tag == "a" and self._nav_depth and text and text not in self.nav_labels and len(self.nav_labels) < 6:
            self.nav_labels.append(text)
        self._tag = ""
        self._text = []

    def handle_data(self, data: str) -> None:
        if self._tag:
            self._text.append(data)


def load_manifest(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    required = ["business_name", "source_url", "tenant_key", "area", "services"]
    missing = [name for name in required if not data.get(name)]
    if missing:
        raise ValueError(f"Manifest is missing required fields: {', '.join(missing)}")
    if not re.fullmatch(r"[a-z0-9_]{3,64}", str(data["tenant_key"])):
        raise ValueError("tenant_key must use lowercase letters, numbers and underscores")
    if not isinstance(data["services"], list) or not data["services"]:
        raise ValueError("services must be a non-empty list")
    if not re.fullmatch(r"#[0-9a-fA-F]{6}", data.get("accent", "#147a78")):
        raise ValueError("accent must be a six-digit hex colour")
    return data


def capture_public_structure(url: str) -> dict[str, Any]:
    request = Request(url, headers={"User-Agent": "PrivateAssistantPreview/1.0 (+demo preparation)"})
    with urlopen(request, timeout=15) as response:
        content_type = response.headers.get_content_type()
        if content_type not in {"text/html", "application/xhtml+xml"}:
            raise ValueError(f"Source did not return HTML (got {content_type})")
        body = response.read(512_000).decode(response.headers.get_content_charset() or "utf-8", errors="replace")
    parser = PublicStructureParser()
    parser.feed(body)
    return {
        "source_url": url,
        "page_title": parser.title,
        "meta_description": parser.description,
        "primary_heading": parser.h1,
        "navigation_labels": parser.nav_labels,
        "capture_scope": "title, meta description, first H1 and up to six navigation labels only; no source HTML, images, CSS, reviews or substantial copy retained",
    }


def esc(value: Any) -> str:
    return html.escape(str(value), quote=True)


def tenant_draft(manifest: dict[str, Any]) -> dict[str, Any]:
    services = [{"name": f"{str(item).strip()} (demo)", "price": 65 + index * 20} for index, item in enumerate(manifest["services"][:4])]
    raw_origins = manifest.get("allowed_origins", ["http://127.0.0.1:8096", "http://localhost:8096"])
    allowed_hosts = sorted({re.sub(r"^https?://", "", str(origin)).split("/")[0].split(":")[0] for origin in raw_origins})
    return {
        "id": re.sub(r"[^a-z0-9]+", "-", str(manifest["tenant_key"]).lower()).strip("-"),
        "publicKey": manifest["tenant_key"],
        "allowedHosts": allowed_hosts,
        "businessName": manifest["business_name"],
        "tagline": "Private assistant concept",
        "status": "demo",
        "logoText": manifest.get("logo_text") or "".join(part[0] for part in str(manifest["business_name"]).split()[:2]).upper(),
        "allowedOrigins": manifest.get("allowed_origins", ["http://127.0.0.1:8096", "http://localhost:8096"]),
        "theme": {"accent": manifest.get("accent", "#147a78"), "ink": manifest.get("ink", "#17211f"), "surface": "#f5f0e7"},
        "contact": {"phone": manifest.get("phone", ""), "email": manifest.get("email", ""), "area": manifest["area"]},
        "enabledModules": ["assistant", "faq", "navigation", "contact", "demoBooking", "demoPayment", "demoEmail", "demoCrm"],
        "knowledge": [
            {"title": "Demo services", "text": f"This private demonstration represents {manifest['business_name']} in {manifest['area']}. Available demo service paths: {', '.join(str(x) for x in manifest['services'])}."},
            {"title": "Demo status", "text": "This is a simulation only. No booking, payment, email, CRM record, callback, notification or customer data processing occurs."},
        ],
        "demoWorkflows": {
            "booking": {"services": services, "slots": ["Demo slot · Mon 09:30", "Demo slot · Wed 13:00", "Demo slot · Fri 16:30"]},
            "payment": {"currency": "GBP", "testCardLabel": "Demo card •••• 4242"},
            "email": {"senderName": f"{manifest['business_name']} Demo Desk", "subjects": ["Demo enquiry confirmation", "Demo appointment summary", "Demo service follow-up"]},
            "crm": {"pipelineStages": ["Demo new enquiry", "Demo details requested", "Demo appointment selected", "Demo owner follow-up"]},
        },
        "provisioning_note": "Draft only. Review business facts and allowed origins, then add to the shared assistant client registry and deploy before sharing externally.",
    }


def shell_html(manifest: dict[str, Any], capture: dict[str, Any]) -> str:
    nav = capture["navigation_labels"] or ["Services", "About", "Contact"]
    service_cards = "".join(f"<li>{esc(item)} <span>DEMO ENQUIRY</span></li>" for item in manifest["services"][:4])
    nav_links = "".join(f"<a href=\"#services\">{esc(item)}</a>" for item in nav)
    return f"""<!doctype html>
<html lang=\"en\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">
<title>Private assistant concept — {esc(manifest['business_name'])}</title>
<style>
:root{{--accent:{esc(manifest.get('accent','#147a78'))};--ink:#17211f;--paper:#f7f5ef;}}*{{box-sizing:border-box}}body{{margin:0;background:var(--paper);color:var(--ink);font:16px/1.55 system-ui,sans-serif}}.concept{{background:#17211f;color:#fff;text-align:center;padding:9px 16px;font-size:12px;font-weight:700;letter-spacing:.04em}}header,main,footer{{max-width:1080px;margin:auto;padding-left:24px;padding-right:24px}}header{{padding-top:28px;display:flex;justify-content:space-between;gap:25px;align-items:center}}.brand{{font:bold 22px Georgia,serif}}nav{{display:flex;gap:16px;flex-wrap:wrap}}nav a{{color:inherit;text-decoration:none;font-size:13px}}.hero{{padding-top:85px;padding-bottom:80px;display:grid;grid-template-columns:1.2fr .8fr;gap:35px;align-items:end}}.eyebrow{{color:var(--accent);font-weight:800;font-size:12px;letter-spacing:.12em}}h1{{font:clamp(42px,7vw,78px)/.98 Georgia,serif;margin:12px 0 20px;letter-spacing:-.05em}}.card{{border:1px solid #17211f20;background:#fff;padding:25px;border-radius:20px;box-shadow:0 18px 45px #17211f15}}.card strong{{display:block;font:24px Georgia,serif}}.cta{{display:inline-block;margin-top:22px;background:var(--accent);color:#fff;text-decoration:none;padding:12px 17px;border-radius:9px;font-weight:800}}section{{padding:45px 0;border-top:1px solid #17211f1c}}h2{{font:34px Georgia,serif;margin:0 0 15px}}ul{{list-style:none;padding:0;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}}li{{background:#fff;border:1px solid #17211f18;border-radius:12px;padding:17px;font-weight:700}}li span{{display:block;color:var(--accent);font-size:10px;letter-spacing:.08em;margin-top:4px}}footer{{padding-top:30px;padding-bottom:100px;color:#5f655f;font-size:13px}}@media(max-width:700px){{.hero{{grid-template-columns:1fr;padding-top:55px}}header{{align-items:flex-start;flex-direction:column}}ul{{grid-template-columns:1fr}}}}
</style></head><body>
<div class=\"concept\">PRIVATE CONCEPT · NOT THE OFFICIAL WEBSITE · ALL ASSISTANT FLOWS ARE DEMO ONLY</div>
<header><div class=\"brand\">{esc(manifest['business_name'])}</div><nav>{nav_links}</nav></header>
<main><section class=\"hero\"><div><div class=\"eyebrow\">{esc(manifest['area']).upper()} · WEBSITE ASSISTANT CONCEPT</div><h1>Helpful answers. A clearer next step.</h1><p>This original private shell demonstrates how a website assistant could sit alongside the current online presence — without claiming to replace it.</p><a class=\"cta\" href=\"#services\">Explore demo services</a></div><aside class=\"card\"><strong>Assistant layer</strong><p>Visitors can explore services and walk through simulated booking, payment, email and CRM journeys.</p><small>Nothing is sent, charged, booked or recorded externally.</small></aside></section>
<section id=\"services\"><div class=\"eyebrow\">DEMO JOURNEYS</div><h2>A more guided route to enquiry</h2><ul>{service_cards}</ul></section></main>
<footer>Private concept built from limited public identity and structural details. Source reviewed: {esc(manifest['source_url'])}</footer>
<script src=\"assistant-embed.js\"></script></body></html>"""


def embed_js(manifest: dict[str, Any]) -> str:
    return f"""(() => {{
  const script = document.currentScript;
  const base = (window.WEBSITE_ASSISTANT_API_BASE || \"{ASSISTANT_BASE}\").replace(/\\/$/, \"\");
  const widget = document.createElement(\"script\");
  widget.src = `${{base}}/widget.js`;
  widget.dataset.client = \"{manifest['tenant_key']}\";
  widget.dataset.apiBase = base;
  widget.defer = true;
  document.head.append(widget);
}})();
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a safe private website shell and demo assistant tenant draft.")
    parser.add_argument("--manifest", required=True, type=Path, help="Approved prospect manifest JSON")
    parser.add_argument("--output", required=True, type=Path, help="Empty/new output directory")
    args = parser.parse_args()
    try:
        manifest = load_manifest(args.manifest)
        capture = capture_public_structure(manifest["source_url"])
        args.output.mkdir(parents=True, exist_ok=True)
        (args.output / "capture.json").write_text(json.dumps(capture, indent=2) + "\n", encoding="utf-8")
        (args.output / "tenant-draft.json").write_text(json.dumps(tenant_draft(manifest), indent=2) + "\n", encoding="utf-8")
        (args.output / "assistant-embed.js").write_text(embed_js(manifest), encoding="utf-8")
        (args.output / "index.html").write_text(shell_html(manifest, capture), encoding="utf-8")
        print(json.dumps({"status": "generated", "output": str(args.output), "files": ["capture.json", "tenant-draft.json", "assistant-embed.js", "index.html"]}))
        return 0
    except Exception as error:
        print(f"preview generation failed: {error}", file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
