"""Uvicorn entry point for the Agentic Arena showcase."""
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles


ROOT = Path(__file__).resolve().parent
app = FastAPI(title="Agentic Arena Showcase", docs_url=None, redoc_url=None)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "agentic-arena"}


@app.get("/", include_in_schema=False)
def arena() -> FileResponse:
    return FileResponse(ROOT / "index.html")


@app.get("/owner", include_in_schema=False)
def owner() -> FileResponse:
    return FileResponse(ROOT / "owner.html")


app.mount("/", StaticFiles(directory=ROOT, html=True), name="arena-static")
