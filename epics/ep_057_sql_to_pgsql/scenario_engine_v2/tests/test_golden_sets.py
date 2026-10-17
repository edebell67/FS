# epics/ep_057_sql_to_pgsql/scenario_engine_v2/tests/test_golden_sets.py — the engine reproduces what the page shows for the three golden views (byte-identical series, same SHA-256).
#
# VERSION HISTORY
# v1.0.0 · 2026-10-17 · Initial version: golden/golden_full_v2.65.32.json (captured from the page in the browser) vs Engine.eligible() on live API data.
"""Needs the :8765 server (same data as the page used). The goldens are the 2026-10-14 / 2026-10-13 days, which are complete, so the curves do not change."""
import hashlib
import json
import sys
import urllib.request
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from engine import data_client as dc  # noqa: E402
from engine.instance import Engine, EngineSpec  # noqa: E402

GOLD = json.loads((ROOT / "golden" / "golden_full_v2.65.32.json").read_text(encoding="utf-8"))


def _server_up() -> bool:
    try:
        urllib.request.urlopen("http://127.0.0.1:8765/api/scenario_workspace", timeout=5)
        return True
    except Exception:  # noqa: BLE001
        return False


pytestmark = pytest.mark.skipif(not _server_up(), reason="needs the :8765 server")


def _num(v):
    if isinstance(v, float) and v.is_integer():
        return int(v)
    return v


def payload(models) -> str:
    return json.dumps([{"model": m["model"], "series": [[p["time"], _num(p.get("net")), _num(p.get("buy")), _num(p.get("sell")), _num(p.get("alt_net")),
                                                         _num(p.get("open")), _num(p.get("trades"))] for p in m["series"]]} for m in models],
                      separators=(",", ":"), ensure_ascii=False)


@pytest.mark.parametrize("gold", GOLD["sets"], ids=[g["id"] for g in GOLD["sets"]])
def test_engine_reproduces_the_pages_golden_view(gold):
    e = gold["engine"]
    client = dc.DataClient(dc.http_transport(), "http://127.0.0.1:8765", live_date="2026-10-17")
    engine = Engine(EngineSpec(date=e["date"], product_type=e["product_type"], scenario=e["scenario"], models=tuple(e["models"]), models_only=e["models_only"]))
    engine.load_from_client(client)
    if e["selected_time"]:
        assert engine.refresh_selected_time(client, rank_count=1)["ran"] is True
    models = engine.eligible()
    assert [[m["model"], len(m["series"])] for m in models] == gold["models"]
    text = payload(models)
    assert len(text.encode("utf-8")) == gold["bytes"]
    assert hashlib.sha256(text.encode("utf-8")).hexdigest() == gold["sha256"]
