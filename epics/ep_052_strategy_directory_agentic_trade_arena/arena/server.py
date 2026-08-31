"""Uvicorn entry point for the Agentic Arena showcase.

Version history:
- 1.1.0 (2026-08-31): The hosted directory bridge only ever carries closed-
  trade evidence (EP051's published snapshot has no visibility into open
  positions at all). Enriches each item with live open_trades/
  open_net_return, read directly from local SQL Server (EP051's own
  combined_trades_open table) - real-time, not snapshot-lag-limited like
  the closed data. Best-effort: if the local DB isn't reachable from
  wherever this process is running, open fields default to null/0 and the
  closed-trade data still returns normally.
- 1.0.0: Initial static-file host + hosted-directory bridge.
"""
import sys
from pathlib import Path
import json
from urllib.parse import urlencode
from urllib.request import urlopen

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles


ROOT = Path(__file__).resolve().parent
app = FastAPI(title="Agentic Arena Showcase", docs_url=None, redoc_url=None)

# EP051's app/repository.py + app/config.py live in a sibling epic. Import
# them directly rather than duplicating the SQL Server connection/query
# logic here - this only works when running on the same machine as the
# local trade database (true for this workspace's normal setup).
_EP051_HOSTED_DIR = Path(__file__).resolve().parents[2] / "ep_051_strategy_directory" / "hosted_directory"
try:
    if str(_EP051_HOSTED_DIR) not in sys.path:
        sys.path.insert(0, str(_EP051_HOSTED_DIR))
    from app.config import Settings as _Ep051Settings
    from app.repository import local_open_trade_summary as _local_open_trade_summary
    _ep051_settings = _Ep051Settings(_env_file=str(_EP051_HOSTED_DIR / ".env"))
except Exception:
    _local_open_trade_summary = None
    _ep051_settings = None


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "agentic-arena"}


@app.get("/api/directory/strategies")
def directory_strategies(page: int = 1, page_size: int = 100) -> dict:
    """Read-only same-origin bridge for public Strategy Directory summaries,
    enriched with live local open-position data (see version history)."""
    query = urlencode({"page": max(1, page), "page_size": min(100, max(1, page_size))})
    with urlopen(f"https://ep051-directory.onrender.com/api/dna/strategies?{query}", timeout=30) as response:
        payload = json.loads(response.read())
    if _local_open_trade_summary is not None:
        try:
            open_summary = _local_open_trade_summary(_ep051_settings)
            for item in payload.get("data", {}).get("items", []):
                open_row = open_summary.get(item.get("strategy_id"))
                item["open_trades"] = open_row["open_trades"] if open_row else 0
                item["open_net_return"] = open_row["open_net_return"] if open_row else 0.0
        except Exception:
            pass  # local DB unreachable - closed-trade data still returned
    return payload


@app.get("/", include_in_schema=False)
def arena() -> FileResponse:
    return FileResponse(ROOT / "index.html")


@app.get("/owner", include_in_schema=False)
def owner() -> FileResponse:
    return FileResponse(ROOT / "owner.html")


app.mount("/", StaticFiles(directory=ROOT, html=True), name="arena-static")
