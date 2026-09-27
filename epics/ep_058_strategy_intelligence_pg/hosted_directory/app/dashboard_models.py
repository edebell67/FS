# epics/ep_058_strategy_intelligence_pg/hosted_directory/app/dashboard_models.py — OpenAPI response documentation for the dashboard endpoints.
#
# VERSION HISTORY
# v1.0.0 · 2026-09-27 · Documentation-only response models (routes keep returning raw JSON; nothing is validated or filtered by these).
"""Shapes observed from the live payloads (identical to the ep_057 server's). All models allow extra keys."""
from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class _Doc(BaseModel):
    model_config = ConfigDict(extra="allow")


class SeriesPoint(_Doc):
    time: str = Field(description="HH:MM local (server) time of the 5-minute snapshot")
    net: float = Field(description="Cumulative net return so far today, USD")
    buy: float = Field(description="Cumulative net return of BUY trades, USD")
    sell: float = Field(description="Cumulative net return of SELL trades, USD")
    alt_net: float = Field(description="Counterfactual (opposite-direction) cumulative net, USD")
    alt_buy: float
    alt_sell: float
    open: int = Field(description="Open trades at this snapshot")
    trades: int = Field(description="Closed trades so far today")


class ModelCurve(_Doc):
    rank: int
    model: str = Field(description="Model id, e.g. dna_301680")
    product: str
    product_type: str = Field(description="forex | crypto")
    strategy: str = Field(description="Canonical name, e.g. breakout_rev_2_tp300_sl30")
    color: str
    trades: int
    wins: int
    losses: int
    win_rate: float = Field(description="Percent, 0-100")
    alt_wins: int
    alt_win_rate: float
    cum_net: float
    buy_net: float
    sell_net: float
    cum_alt_net: float
    buy_alt_net: float
    sell_alt_net: float
    series: list[SeriesPoint]


class LiveDayResponse(_Doc):
    """Model lists keyed by scenario id (see GET /api/scenarios), each a list of ModelCurve. Scenario keys are extra properties."""
    date: str
    product_type: str
    product: str
    strategy_family: str
    limit: int
    products: list[str]
    tp_sl_scenarios: list[dict[str, Any]] = Field(description="[{id:'top3_tp30_sl50', tp, sl}] - dynamic scenarios present today")
    generated_at: str


class PortfolioDayResponse(_Doc):
    date: str
    requested_models: list[str]
    models: list[ModelCurve]
    generated_at: str


class SimilarItem(_Doc):
    model: str
    product: str
    product_type: str
    strategy: str
    value: Any = Field(description="Value of the varied dimension for this model")


class SimilarStrategiesResponse(_Doc):
    date: str
    reference: dict[str, Any] = Field(description="{model, product, product_type, strategy, family, window, tp, sl}")
    groups: dict[str, list[SimilarItem]] = Field(description="Keys: family | window | tp | sl. Same product, only that dimension varies")
    generated_at: str


class CatalogueModel(_Doc):
    model: str
    product: str
    product_type: str
    strategy: str
    net: float
    alt: float
    family: str
    window: int | None
    tp: int
    sl: int


class StrategyCatalogResponse(_Doc):
    date: str
    models: list[CatalogueModel]
    generated_at: str


class TradeRow(_Doc):
    status: str = Field(description="closed | open")
    opened: str = Field(description="YYYY-MM-DD HH:MM:SS, server local time")
    last_update: str
    signal: str = Field(description="BUY | SELL")
    product: str
    entry_price: float | None
    latest_price: float | None
    quantity: float | None
    net_return: float | None = Field(description="USD")
    alt_net_return: float | None = Field(description="USD, counterfactual reversed trade")
    min_net_return: float | None
    max_net_return: float | None
    close_type: str | None
    trade_reason: str | None
    strategy: str
    target_profit: float | None
    target_loss: float | None


class ModelTradesResponse(_Doc):
    model: str
    from_: str | None = Field(None, alias="from")
    to: str
    product_type: str
    product: str
    strategy_name: str | None
    strategy_params: str | None
    trades: list[TradeRow]


class ModelTradesSummaryResponse(_Doc):
    model: str
    trades: int
    open: int
    win_rate: float | None = Field(description="Percent of closed trades with net_return > 0; null if none closed")
    closed_net: float
    closed_alt_net: float


class HourlyRow(_Doc):
    exit_hour: str = Field(description="HH:00")
    side: str = Field(description="BUY | SELL")
    opened_trades: int
    open_at_hour_end: int
    closed_trades: int
    net_profit_count: int
    alt_profit_count: int
    avg_net: float
    avg_alt_net: float
    total_net: float
    total_alt_net: float
    is_incomplete_hour: bool


class HourlyFamilyReportResponse(_Doc):
    date: str
    product_type: str
    product: str
    family: str
    products: list[str]
    rows: list[HourlyRow]
    summary: dict[str, Any]
    is_today: bool
    current_hour: str | None
    interval_minutes: int = Field(description="Bucket size in minutes: 10, 30, 60, or 180")
    generated_at: str


class PointInTimeScenarioResponse(_Doc):
    date: str
    at_time: str = Field(description="The requested cutoff, echoed back")
    scenario: str = Field(description="Resolved scenario key (metric-aware ids include _net/_alt)")
    models: list[ModelCurve] = Field(description="The cohort selected using only evidence up to at_time, with full-day curves so later performance can be assessed")


class ScenariosResponse(_Doc):
    catalogue: list[dict[str, Any]] = Field(description="Static scenario cards: id, name, sub (description), badge")
    tp_sl_scenarios: list[dict[str, Any]]
    available_ids: list[str] = Field(description="Every scenario key present in live_day for that date/filters")
    products: list[str]
    metric_aware: list[str] = Field(description="Scenario families stored per return type as <id>_net / <id>_alt")


class ScenarioCandidatesResponse(_Doc):
    models: list[ModelCurve]


class RibbonResponse(_Doc):
    total: dict[str, float] = Field(description="Summed delta from baseline to replay head: {net, buy, sell}, USD")
    models: list[dict[str, Any]]
    count: int
    base_time: str | None
    head_time: str | None
    baseline_index: int


class ReplayFrameResponse(_Doc):
    baseline_index: int
    frame_index: int
    max_frames: int
    models: list[dict[str, Any]] = Field(description="[{model, base: SeriesPoint, head: SeriesPoint}]")


class Signal(_Doc):
    idx: int = Field(description="Index into the series slice")
    time: str
    type: str = Field(description="B enter buy | S enter sell | X exit | T daily target hit")
    val: float
    text: str


class OverlayTrade(_Doc):
    side: str
    entryIdx: int
    entryTime: str
    entryVal: float
    exitIdx: int
    exitTime: str
    exitVal: float
    pnl: float = Field(description="USD: exit delta minus entry delta from the baseline")
    flipSide: str | None = None
    flipPnl: float | None = Field(None, description="P&L had the opposite side's curve been traded over the same interval")
    isOpen: bool


class OverlayResponse(_Doc):
    model: str | None
    baseline_index: int
    signals: list[Signal]
    trades: list[OverlayTrade]
    summary: dict[str, Any] = Field(description="{count, wins, total, flip_total}")
    targetSignal: dict[str, Any] | None


class RotationResponse(_Doc):
    signals: list[dict[str, Any]]
    trades: list[dict[str, Any]]
    threshold: float = Field(description="abs(exit_threshold)")
    targetSignal: dict[str, Any] | None
    baseline_index: int


class CoverageResponse(_Doc):
    source: str
    first_date: str | None
    last_date: str | None
    dates: list[str]
    snapshot_dates: list[str] = Field(description="Dates that also have 5-minute snapshots (needed for curves)")
    latest_snapshot: str | None
    products: list[str]
    intelligence: dict[str, Any] | None = Field(description="Current published intelligence snapshot, if available")
