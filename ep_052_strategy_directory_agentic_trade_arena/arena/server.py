"""Uvicorn entry point for the Agentic Arena showcase and waitlist API."""
from __future__ import annotations

from contextlib import asynccontextmanager
import os
from pathlib import Path
from typing import Protocol

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from waitlist_policy import Registration, ValidationError, normalize_registration
from waitlist_store import PostgresWaitlistStore


ROOT = Path(__file__).resolve().parent
ALLOWED_ORIGINS = ["https://thetechprinciple.com", "https://www.thetechprinciple.com"]


class WaitlistStore(Protocol):
    async def register(self, registration: Registration) -> bool: ...


class UnavailableWaitlistStore:
    async def register(self, registration: Registration) -> bool:
        raise RuntimeError("waitlist storage is unavailable")


def create_app(waitlist_store: WaitlistStore | None = None) -> FastAPI:
    managed_store = waitlist_store
    if managed_store is None:
        database_url = os.environ.get("WAITLIST_DATABASE_URL")
        managed_store = PostgresWaitlistStore(database_url) if database_url else UnavailableWaitlistStore()

    @asynccontextmanager
    async def lifespan(_: FastAPI):
        start = getattr(managed_store, "start", None)
        if start is not None:
            await start()
        yield
        close = getattr(managed_store, "close", None)
        if close is not None:
            await close()

    app = FastAPI(
        title="Agentic Arena Showcase",
        docs_url=None,
        redoc_url=None,
        lifespan=lifespan,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_ORIGINS,
        allow_methods=["POST", "OPTIONS"],
        allow_headers=["Content-Type"],
    )

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok", "service": "agentic-arena"}

    @app.post("/api/waitlist", status_code=201)
    async def register_waitlist(payload: dict) -> dict[str, bool | str]:
        try:
            registration = normalize_registration(payload)
        except ValidationError as error:
            raise HTTPException(status_code=422, detail=str(error)) from error
        try:
            duplicate = await managed_store.register(registration)
        except RuntimeError as error:
            raise HTTPException(status_code=503, detail="waitlist registration is unavailable") from error
        return {"status": "registered", "duplicate": duplicate}

    @app.get("/", include_in_schema=False)
    def arena() -> FileResponse:
        return FileResponse(ROOT / "index.html")

    @app.get("/owner", include_in_schema=False)
    def owner() -> FileResponse:
        return FileResponse(ROOT / "owner.html")

    app.mount("/", StaticFiles(directory=ROOT, html=True), name="arena-static")
    return app


app = create_app()
