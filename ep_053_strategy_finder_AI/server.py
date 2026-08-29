"""Uvicorn entry point for the local Strategy Finder AI UI demo."""
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

ROOT = Path(__file__).resolve().parent
app = FastAPI(title="Strategy Finder AI Demo", docs_url=None, redoc_url=None)


@app.get("/health", include_in_schema=False)
def health() -> dict[str, str]:
    return {"status": "ok", "service": "strategy-finder-ai-demo"}


@app.get("/", include_in_schema=False)
def finder() -> FileResponse:
    return FileResponse(ROOT / "index.html")


app.mount("/", StaticFiles(directory=ROOT, html=True), name="finder-static")
