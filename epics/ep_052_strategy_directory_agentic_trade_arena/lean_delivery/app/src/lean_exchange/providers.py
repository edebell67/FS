# VERSION HISTORY v1.6.0 · 2026-09-16 · Read current-day BUY-only or SELL-only strategy totals for the Arena side filter.
# v1.5.0 · 2026-09-11 · Support exact current-day strategy lookup for ad-hoc Arena admission.
# v1.4.0 · 2026-09-11 · Define the current trading day in Europe/London for the test pricing baseline.
# v1.3.0 · 2026-09-10 · Select the configured top N only from strategies traded on the current local day.
# v1.2.0 · 2026-09-10 · Select the configured top N from the explicit full directory universe.
# v1.1.0 · 2026-09-10 · Request and retain the top-500 directory selection in descending net-return order.
# v1.0.0 · 2026-09-02 · Read-only directory adapter with strict pagination and honest price provenance.
from datetime import datetime, timezone
from decimal import Decimal, localcontext
from hashlib import sha256
import json
from typing import Any, Literal
from zoneinfo import ZoneInfo

import httpx
from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator

from .config import Settings


class ProviderError(Exception):
    """Safe error: never include upstream body, URL credentials or request headers."""


class StrategyRecord(BaseModel):
    model_config = ConfigDict(extra='allow', allow_inf_nan=False)
    strategy_id: str = Field(pattern=r'^DNA_[0-9_]+$')
    status: str
    descriptive_name: str | None = None
    total_trades: int = Field(ge=0, strict=True)
    total_net_return: Decimal
    open_trades: int | None = Field(default=None, ge=0, strict=True)
    open_net_return: Decimal | None = None


class DirectorySnapshot(BaseModel):
    items: list[StrategyRecord]
    source: Literal['existing_strategy_directory'] = 'existing_strategy_directory'
    source_version: str
    retrieved_at: datetime
    page_as_of: list[datetime]
    total: int
    source_total: int | None = None
    open_evidence_available: bool
    exchange_prices_available: Literal[False] = False
    warnings: list[str]


class DirectoryProvider:
    # Owner-switchable at runtime via PUT /v1/owner/directory-source (persisted
    # in the metadata table, same mechanism as arena_public_access) rather than
    # only at process startup via EP052_DIRECTORY_URL/config.toml. 'store' is
    # optional so tests/scripts that construct DirectoryProvider directly
    # (no Arena Store) keep working unchanged - they just always get
    # settings.directory_url, the pre-existing behaviour.
    def __init__(self, settings: Settings, transport: httpx.BaseTransport | None = None, store=None):
        self.settings = settings
        self.transport = transport
        self.store = store

    def _directory_url(self) -> str:
        if self.store is not None and self.settings.directory_url_pg:
            with self.store.transaction() as db:
                row = db.execute("SELECT value FROM metadata WHERE key='directory_source'").fetchone()
            if row and row['value'] == 'pg':
                return self.settings.directory_url_pg
        return self.settings.directory_url

    def fetch(self) -> DirectorySnapshot:
        cfg = self.settings
        directory_url = self._directory_url()
        trading_day = datetime.now(ZoneInfo(cfg.pricing_timezone)).date().isoformat()
        items: list[StrategyRecord] = []
        timestamps: list[datetime] = []
        expected_total = None
        identifiers: set[str] = set()
        try:
            with httpx.Client(timeout=cfg.provider_timeout_seconds, transport=self.transport,
                              follow_redirects=False) as client:
                for page in range(1, cfg.directory_max_pages + 1):
                    response = client.get(directory_url, params={'page': page, 'page_size': cfg.directory_page_size,
                                                                     'sort': 'total_net_return', 'direction': 'desc',
                                                                     'date_from': trading_day, 'date_to': trading_day})
                    if response.status_code != 200:
                        raise ProviderError('DIRECTORY_UNAVAILABLE')
                    payload = response.json()
                    data = payload['data']
                    total = data['total']
                    if type(total) is not int or total < 0 or data['page'] != page:
                        raise ProviderError('DIRECTORY_INVALID_PAGINATION')
                    if expected_total is None:
                        expected_total = total
                    if total != expected_total:
                        raise ProviderError('DIRECTORY_CHANGED_DURING_READ')
                    stamp = datetime.fromisoformat(payload['as_of'])
                    if stamp.tzinfo is None:
                        raise ProviderError('DIRECTORY_MISSING_TIMEZONE')
                    timestamps.append(stamp)
                    batch = [StrategyRecord.model_validate(row) for row in data['items']]
                    for record in batch:
                        if record.strategy_id in identifiers:
                            raise ProviderError('DIRECTORY_DUPLICATE_STRATEGY')
                        identifiers.add(record.strategy_id)
                    items.extend(batch)
                    if len(items) > total or len(batch) > cfg.directory_page_size:
                        raise ProviderError('DIRECTORY_INVALID_PAGINATION')
                    if len(items) >= min(total, cfg.directory_selection_limit):
                        break
                    if not batch:
                        raise ProviderError('DIRECTORY_INCOMPLETE')
                else:
                    raise ProviderError('DIRECTORY_PAGE_LIMIT')
        except (httpx.HTTPError, ValidationError, ValueError, KeyError, TypeError) as exc:
            raise ProviderError('DIRECTORY_INVALID_OR_UNAVAILABLE') from exc
        items.sort(key=lambda item: (-item.total_net_return, item.strategy_id))
        items = items[:cfg.directory_selection_limit]
        canonical = [item.model_dump(mode='json') for item in items]
        version = sha256(json.dumps(canonical, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
        open_available = bool(items) and all(x.open_trades is not None and x.open_net_return is not None for x in items)
        return DirectorySnapshot(items=items, total=len(items), source_total=expected_total, source_version=version,
                                 retrieved_at=datetime.now(timezone.utc), page_as_of=timestamps,
                                 open_evidence_available=open_available,
                                 warnings=['Catalogue/performance is not published USD unit pricing.'] +
                                 ([] if open_available else ['Source omits open-position evidence; unknown is not zero.']))

    def fetch_strategy(self, strategy_id: str) -> StrategyRecord | None:
        """Look up one exact strategy within the current London trading day."""
        cfg = self.settings
        directory_url = self._directory_url()
        trading_day = datetime.now(ZoneInfo(cfg.pricing_timezone)).date().isoformat()
        try:
            with httpx.Client(timeout=cfg.provider_timeout_seconds, transport=self.transport,
                              follow_redirects=False) as client:
                response = client.get(directory_url, params={
                    'page': 1, 'page_size': cfg.directory_page_size, 'search': strategy_id,
                    'sort': 'total_net_return', 'direction': 'desc',
                    'date_from': trading_day, 'date_to': trading_day,
                })
                if response.status_code != 200:
                    raise ProviderError('DIRECTORY_UNAVAILABLE')
                candidates = [StrategyRecord.model_validate(row) for row in response.json()['data']['items']]
                return next((row for row in candidates if row.strategy_id == strategy_id), None)
        except (httpx.HTTPError, ValidationError, ValueError, KeyError, TypeError) as exc:
            raise ProviderError('DIRECTORY_INVALID_OR_UNAVAILABLE') from exc

    def fetch_signal_totals(self, signal: Literal['BUY', 'SELL']) -> dict[str, StrategyRecord]:
        """Return every current-day strategy's totals from only its trades on one signal side.

        The whole filtered universe is read (not the top-N selection) so strategies whose
        side-only rank differs from their combined rank are still found.
        """
        cfg = self.settings
        directory_url = self._directory_url()
        trading_day = datetime.now(ZoneInfo(cfg.pricing_timezone)).date().isoformat()
        records: dict[str, StrategyRecord] = {}
        expected_total = None
        try:
            with httpx.Client(timeout=cfg.provider_timeout_seconds, transport=self.transport,
                              follow_redirects=False) as client:
                for page in range(1, cfg.directory_max_pages + 1):
                    response = client.get(directory_url, params={
                        'page': page, 'page_size': cfg.directory_page_size, 'signal': signal,
                        'sort': 'strategy_id', 'direction': 'asc',
                        'date_from': trading_day, 'date_to': trading_day,
                    })
                    if response.status_code != 200:
                        raise ProviderError('DIRECTORY_UNAVAILABLE')
                    data = response.json()['data']
                    total = data['total']
                    if type(total) is not int or total < 0 or data['page'] != page:
                        raise ProviderError('DIRECTORY_INVALID_PAGINATION')
                    if expected_total is None:
                        expected_total = total
                    if total != expected_total:
                        raise ProviderError('DIRECTORY_CHANGED_DURING_READ')
                    batch = [StrategyRecord.model_validate(row) for row in data['items']]
                    for record in batch:
                        if record.strategy_id in records:
                            raise ProviderError('DIRECTORY_DUPLICATE_STRATEGY')
                        records[record.strategy_id] = record
                    if len(records) >= total:
                        break
                    if not batch:
                        raise ProviderError('DIRECTORY_INCOMPLETE')
                else:
                    raise ProviderError('DIRECTORY_PAGE_LIMIT')
        except (httpx.HTTPError, ValidationError, ValueError, KeyError, TypeError) as exc:
            raise ProviderError('DIRECTORY_INVALID_OR_UNAVAILABLE') from exc
        return records


class ValuationInput(BaseModel):
    """Adapted NAV/unit invariant from archived core.models.StrategyValuation; DNA IDs retained."""
    model_config = ConfigDict(extra='forbid', allow_inf_nan=False)
    strategy_id: str = Field(pattern=r'^DNA_[0-9_]+$')
    nav: Decimal = Field(ge=0, max_digits=28, decimal_places=10)
    units_outstanding: int = Field(gt=0, strict=True)
    currency: Literal['USD']
    source_version: str = Field(min_length=1, max_length=128)
    valued_at: datetime

    @field_validator('valued_at')
    @classmethod
    def timezone_required(cls, value: datetime) -> datetime:
        if value.tzinfo is None:
            raise ValueError('Valuation time requires timezone')
        return value


def published_price(valuation: ValuationInput, decimal_places: int) -> dict[str, Any]:
    if type(decimal_places) is not int or not 0 <= decimal_places <= 18:
        raise ValueError('Unsupported price precision')
    with localcontext() as context:
        context.prec = 50
        price = (valuation.nav / valuation.units_outstanding).quantize(Decimal(1).scaleb(-decimal_places))
    return valuation.model_dump(mode='json') | {'unit_price': str(price), 'method': 'NAV / units_outstanding'}
