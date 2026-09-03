"""Validated API contracts for discovery, user and regime intelligence.

VERSION HISTORY
v1.0.0 · 2026-08-24 · Introduces bounded, non-executable service request schemas.
"""
from __future__ import annotations
from datetime import date, datetime
from math import isfinite
from typing import Any, Literal
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
from .discovery import StrategyQuery


class SearchRequest(BaseModel):
    plan: StrategyQuery


class ChainRequest(BaseModel):
    stages: list[StrategyQuery] = Field(min_length=1,max_length=10)


class TimeTravelRequest(BaseModel):
    plan: StrategyQuery
    as_of: date = Field(description="Evaluate the query using only evidence up to and including this date.")
    forward_to: date | None = Field(None,description="End of the forward-test window; defaults to today.")

    @field_validator("as_of")
    @classmethod
    def as_of_not_future(cls,value):
        if value>date.today():raise ValueError("as_of cannot be in the future")
        return value

    @model_validator(mode="after")
    def forward_after_as_of(self):
        if self.forward_to is not None and self.forward_to<=self.as_of:raise ValueError("forward_to must be after as_of")
        return self


class TimeTravelSeriesRequest(BaseModel):
    plan: StrategyQuery
    as_of_from: date = Field(description="First as-of date in the daily series.")
    as_of_to: date = Field(description="Last as-of date in the daily series.")
    forward_days: int = Field(7,ge=1,le=180,description="Fixed forward-test window applied after each as-of date.")

    @field_validator("as_of_to")
    @classmethod
    def as_of_to_not_future(cls,value):
        if value>date.today():raise ValueError("as_of_to cannot be in the future")
        return value

    @model_validator(mode="after")
    def range_is_valid(self):
        if self.as_of_from>self.as_of_to:raise ValueError("as_of_from must be on or before as_of_to")
        if (self.as_of_to-self.as_of_from).days>90:raise ValueError("as_of range cannot exceed 90 days per request")
        return self


class SimilarDaysRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    strategy_id: str = Field(pattern=r"^DNA_[A-Za-z0-9]+$")
    as_of: date | None = Field(None, description="Target day; defaults to today.")
    through_hour: int | None = Field(None, ge=0, le=23, description="Compare only p0..p<through_hour> (an in-progress day); omit for a full day.")
    top_n: int = Field(10, ge=1, le=50)

    @field_validator("as_of")
    @classmethod
    def as_of_not_future(cls, value):
        if value is not None and value > date.today():
            raise ValueError("as_of cannot be in the future")
        return value


class TopPerformersRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    lookback_hours: float = Field(3, gt=0, le=8760, description="Trailing window from now, e.g. 3 for 'the last 3 hours'.")
    min_trade_count: int = Field(1, ge=0, description="Only strategies with at least this many closed trades in the window.")
    top_n: int = Field(3, ge=1, le=100)
    sort: Literal["annualized_return", "win_rate", "sharpe", "quality_score"] = "annualized_return"
    return_basis: Literal["net_return", "alt_net_return"] = "net_return"


class SavedSearchRequest(BaseModel):
    name: str = Field(min_length=1,max_length=80)
    plan: StrategyQuery


class CollectionRequest(BaseModel):
    name: str = Field(min_length=1,max_length=80)
    strategy_ids: list[str] = Field(min_length=1,max_length=100)
    notes: str = Field("",max_length=2000)
    evidence_versions: dict[str,str] = {}


class PreferenceRequest(BaseModel):
    preferences: dict[str,Any]


class ConsentRequest(BaseModel):
    history: bool


class MarketFeatureIngestRequest(BaseModel):
    model_config=ConfigDict(extra="forbid")
    market: str = Field(min_length=1,max_length=40)
    as_of: datetime
    features: dict[str,float|None] = Field(min_length=1,max_length=100)
    source_version: str = Field(min_length=1,max_length=80)

    @field_validator("features")
    @classmethod
    def finite_features(cls, values):
        if any(value is not None and not isfinite(value) for value in values.values()):raise ValueError("features must be finite")
        return values


class RegimeFeaturesRequest(BaseModel):
    """Public selector for server-held point-in-time market evidence."""
    model_config=ConfigDict(extra="forbid")
    market: str = Field(min_length=1,max_length=40)
    as_of: datetime|None = None


class RecommendationRequest(BaseModel):
    model_config=ConfigDict(extra="forbid")
    market: str = Field(min_length=1,max_length=40)
    as_of: datetime|None = None
    strategy_ids: list[str] = Field(min_length=1,max_length=20)
    risk_limit: float|None = Field(None,ge=0)

    @field_validator("strategy_ids")
    @classmethod
    def canonical_ids(cls, values):
        if len(values)!=len(set(values)):raise ValueError("strategy_ids must be unique")
        if any(not value.startswith("DNA_") or not value[4:].isalnum() for value in values):raise ValueError("strategy_ids must be canonical")
        return values

    @field_validator("risk_limit")
    @classmethod
    def finite_risk(cls, value):
        if value is not None and not isfinite(value):raise ValueError("risk_limit must be finite")
        return value
