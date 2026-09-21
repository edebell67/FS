"""
EP057 Top10 5min Equity Curves - ASGI app for uvicorn (port 8765).

Same endpoints as top10_live_server.py, reusing its query builders:
    GET /api/live_day?date=YYYY-MM-DD
    GET /api/model_trades?model=...&from=YYYY-MM-DD[&to=YYYY-MM-DD]
and serves this folder statically (top10_5min_equity_curves.html etc.).

Run:  uvicorn top10_live_app:app --host 127.0.0.1 --port 8765
"""
from __future__ import annotations

import datetime as dt

from fastapi import FastAPI, HTTPException, Query
from fastapi.concurrency import run_in_threadpool
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from top10_live_server import DATE_RE, HERE, build_live_day, build_model_trades

app = FastAPI(title="EP057 Top10 Live", docs_url=None, redoc_url=None)

NO_STORE = {"Cache-Control": "no-store"}


def _check_date(value: str) -> str:
    if not DATE_RE.fullmatch(value):
        raise HTTPException(status_code=400, detail="date must be YYYY-MM-DD")
    return value


@app.get("/api/live_day")
async def live_day(date: str | None = None) -> JSONResponse:
    date_str = _check_date(date or dt.date.today().isoformat())
    try:
        payload = await run_in_threadpool(build_live_day, date_str)
    except Exception as exc:  # surfaced on the page's live badge
        return JSONResponse({"error": str(exc)}, status_code=500, headers=NO_STORE)
    return JSONResponse(payload, headers=NO_STORE)


@app.get("/api/model_trades")
async def model_trades(
    model: str = Query(..., min_length=1),
    date_from: str = Query(..., alias="from"),
    date_to: str | None = Query(None, alias="to"),
) -> JSONResponse:
    d_from = _check_date(date_from)
    d_to = _check_date(date_to or date_from)
    try:
        payload = await run_in_threadpool(build_model_trades, model, d_from, d_to)
    except Exception as exc:
        return JSONResponse({"error": str(exc)}, status_code=500, headers=NO_STORE)
    return JSONResponse(payload, headers=NO_STORE)


# Static last so the /api routes take precedence
app.mount("/", StaticFiles(directory=str(HERE), html=True), name="static")
