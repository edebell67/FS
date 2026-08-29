"""PostgreSQL persistence for the isolated Agentic Arena waitlist."""
from __future__ import annotations

import asyncpg

from waitlist_policy import Registration


SCHEMA_SQL = """
CREATE SCHEMA IF NOT EXISTS agentic_waitlist;
CREATE TABLE IF NOT EXISTS agentic_waitlist.registrations (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    email TEXT NOT NULL UNIQUE,
    discovery_source TEXT NOT NULL,
    source_detail TEXT,
    utm_source TEXT,
    utm_medium TEXT,
    utm_campaign TEXT,
    utm_content TEXT,
    landing_path TEXT,
    referrer TEXT,
    consent_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    last_seen_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
"""


class PostgresWaitlistStore:
    def __init__(self, database_url: str) -> None:
        self.database_url = database_url
        self.pool: asyncpg.Pool | None = None

    async def start(self) -> None:
        self.pool = await asyncpg.create_pool(self.database_url, min_size=1, max_size=3)
        async with self.pool.acquire() as connection:
            await connection.execute(SCHEMA_SQL)

    async def close(self) -> None:
        if self.pool is not None:
            await self.pool.close()
            self.pool = None

    async def register(self, registration: Registration) -> bool:
        if self.pool is None:
            raise RuntimeError("waitlist store is unavailable")
        async with self.pool.acquire() as connection:
            row = await connection.fetchrow(
                """
                INSERT INTO agentic_waitlist.registrations (
                    email, discovery_source, source_detail, utm_source, utm_medium,
                    utm_campaign, utm_content, landing_path, referrer
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
                ON CONFLICT (email) DO NOTHING
                RETURNING id
                """,
                registration.email,
                registration.discovery_source,
                registration.source_detail,
                registration.utm_source,
                registration.utm_medium,
                registration.utm_campaign,
                registration.utm_content,
                registration.landing_path,
                registration.referrer,
            )
        return row is None
