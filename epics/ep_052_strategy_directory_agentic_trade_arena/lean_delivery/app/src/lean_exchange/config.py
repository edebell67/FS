# VERSION HISTORY v1.12.0 · 2026-09-14 · Default intelligence_mode to external provider (EP049).
# v1.11.0 · 2026-09-13 · Configure independent heartbeat, inbox and recovery health thresholds.
# v1.10.0 · 2026-09-11 · Reduce configurable opening inventory to 1,000 units per strategy.
# v1.9.0 · 2026-09-11 · Add a configurable 100-strategy ad-hoc catalogue alongside the ranked selection.
# v1.8.0 · 2026-09-11 · Configure cumulative-return settlement and minimum participant balance.
# v1.7.0 · 2026-09-11 · Configure automatic UK-midnight test pricing and 10,000-unit opening baseline. Superseded before release.
# v1.6.0 · 2026-09-11 · Add configurable total bid/ask spread around authoritative calculated value.
# v1.5.0 · 2026-09-10 · Configure the number of top-ranked strategies selected from the full directory universe.
# v1.4.0 · 2026-09-10 · Add the default server-side Arena public-access policy.
# v1.3.0 · 2026-09-02 · Configure display-only Arena refresh independently of external agent polling.
# v1.2.0 · 2026-09-02 · Configurable credential lifetime, body/rate limits and activity pagination.
# v1.1.0 · 2026-09-02 · Bound directory pagination and validate configured HTTP locations.
# v1.0.0 · 2026-09-02 · Strict configurable economics; no exchange bank integration.
from decimal import Decimal
import os
from pathlib import Path
import tomllib

from pydantic import BaseModel, ConfigDict, Field, field_validator
from urllib.parse import urlsplit
from typing import Literal

APP_ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseModel):
    model_config = ConfigDict(extra='forbid', frozen=True, allow_inf_nan=False)
    environment: Literal['simulation'] = 'simulation'
    currency: Literal['USD'] = 'USD'
    seed_funds: Decimal = Field(default=Decimal('1000'), ge=0)
    trade_fee: Decimal = Field(default=Decimal('.01'), ge=0)
    intelligence_fee: Decimal = Field(default=Decimal('.01'), ge=0)
    minimum_units: int = Field(default=1, ge=1, strict=True)
    maximum_positions: int = Field(default=10, ge=1, strict=True)
    initial_units: int = Field(default=1000, ge=1, strict=True)
    return_based_settlement: bool = True
    minimum_balance: Decimal = Field(default=Decimal('250'), ge=0)
    pricing_timezone: str = 'Europe/London'
    price_decimal_places: int = Field(default=10, ge=0, le=18, strict=True)
    bid_ask_spread_rate: Decimal = Field(default=Decimal('0.001'), ge=0, lt=1)
    directory_url: str
    # Optional alternate directory source (e.g. the Postgres-mirror instance on
    # :8094 vs the default SQL Server one on :8012). When set, an owner can
    # flip DirectoryProvider between the two at runtime via
    # PUT /v1/owner/directory-source, without a process restart.
    directory_url_pg: str | None = None
    directory_page_size: int = Field(default=100, ge=1, le=100, strict=True)
    directory_max_pages: int = Field(default=100, ge=1, strict=True)
    directory_selection_limit: int = Field(default=500, ge=1, strict=True)
    directory_adhoc_limit: int = Field(default=100, ge=0, le=1000, strict=True)
    provider_timeout_seconds: float = Field(default=15, gt=0)
    connection_expiry_seconds: int = Field(default=300, gt=0, strict=True)
    heartbeat_stale_seconds: int = Field(default=180, gt=0, strict=True)
    feedback_stale_seconds: int = Field(default=30, gt=0, strict=True)
    recovery_timeout_seconds: int = Field(default=120, gt=0, strict=True)
    owner_stream_keepalive_seconds: int = Field(default=20, gt=0, le=120, strict=True)
    owner_event_retention: int = Field(default=10000, gt=100, strict=True)
    valuation_sample_seconds: int = Field(default=60, ge=15, le=3600, strict=True)
    valuation_sample_retention_seconds: int = Field(default=28800, ge=14400, le=604800, strict=True)
    insight_minimum_global_cohort: int = Field(default=3, ge=2, le=1000, strict=True)
    owner_insights_enabled: bool = True
    agent_challenges_enabled: bool = True
    credential_ttl_seconds: int = Field(default=86400, gt=0, strict=True)
    rate_window_seconds: int = Field(default=60, gt=0, strict=True)
    requests_per_window: int = Field(default=240, gt=0, strict=True)
    max_body_bytes: int = Field(default=32768, gt=0, strict=True)
    activity_page_size: int = Field(default=100, gt=0, strict=True)
    view_poll_seconds: int = Field(default=5, gt=0, le=3600, strict=True)
    arena_public_access: bool = False
    max_query_results: int = Field(default=20, gt=0, strict=True)
    intelligence_url: str
    intelligence_mode: Literal['simulated_random', 'external'] = 'external'

    @field_validator('directory_url', 'intelligence_url')
    @classmethod
    def validate_endpoint(cls, value: str) -> str:
        parsed = urlsplit(value)
        if parsed.scheme not in ('http', 'https') or not parsed.hostname or parsed.username or parsed.password or parsed.fragment or parsed.query:
            raise ValueError('Use an HTTP(S) endpoint without credentials, fragment or query')
        return value


def load_settings(path: Path | None = None) -> Settings:
    source = path or Path(os.environ.get('EP052_CONFIG', APP_ROOT / 'config.toml'))
    data = tomllib.loads(source.read_text(encoding='utf-8'))
    # Lets the launch script pick which local strategy-directory instance to
    # read from (SQL Server on :8012 vs the Postgres mirror on :8094) without
    # editing config.toml - see ep052_arena_8056_restart.bat / _pg.bat.
    if os.environ.get('EP052_DIRECTORY_URL'):
        data['directory_url'] = os.environ['EP052_DIRECTORY_URL']
    if os.environ.get('EP052_DIRECTORY_URL_PG'):
        data['directory_url_pg'] = os.environ['EP052_DIRECTORY_URL_PG']
    return Settings.model_validate(data)
