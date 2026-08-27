"""Validated API contracts for discovery, user and regime intelligence.

VERSION HISTORY
v1.0.0 · 2026-08-24 · Introduces bounded, non-executable service request schemas.
"""
from __future__ import annotations
from datetime import datetime
from math import isfinite
from typing import Any
from pydantic import BaseModel, ConfigDict, Field, field_validator
from .discovery import StrategyQuery


class SearchRequest(BaseModel):
    plan: StrategyQuery


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
