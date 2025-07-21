from typing import List, Optional
from uuid import uuid4
from datetime import datetime
from sqlmodel import Field, Relationship, SQLModel, JSON
from sqlalchemy import Column, Enum as SAEnum
from pydantic import field_validator
from enum import Enum


class Account(SQLModel, table=True):
    __tablename__ = "account"
    id: str = Field(
        default_factory=lambda: str(uuid4()), primary_key=True, nullable=False
    )
    size: int = Field(default=2000)
    max_risk_percentage: float = Field(default=2)
    max_active_trades: int = Field(default=3)
    

class Timeframe(Enum):
    """Standard trading timeframes for chart intervals.
    
    - 1m: 1 minute
    - 5m: 5 minutes
    - 15m: 15 minutes
    - 30m: 30 minutes
    - 1h: 1 hour
    - 4h: 4 hours
    - 1d: 1 day
    - 1w: 1 week
    - 1mo: 1 month
    """
    ONE_MINUTE = "1m"
    FIVE_MINUTES = "5m"
    FIFTEEN_MINUTES = "15m"
    THIRTY_MINUTES = "30m"
    ONE_HOUR = "1h"
    FOUR_HOURS = "4h"
    ONE_DAY = "1d"
    ONE_WEEK = "1w"
    ONE_MONTH = "1mo"


class VolumeAnalysis(str, Enum):
    INCREASING = "Increasing"
    DECREASING = "Decreasing"
    BREAKOUT = "Breakout volume"
    UNKNOWN = "Unknown"

class TrendDirection(str, Enum):
    UP = "Up"
    DOWN = "Down"
    SIDEWAYS = "Sideways"
    UNKNOWN = "Unknown"

class TradeIdeaStatus(str, Enum):
    WATCHING = "Watching"
    IN_PROGRESS = "In progress"
    INVALIDATED = "Invalidated"
    LIVE = "Live"
    

class TradeIdea(SQLModel, table=True):
    __tablename__ = "trade_idea"
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True, nullable=False)
    symbol: str = Field(nullable=False)
    status: TradeIdeaStatus = Field(default=TradeIdeaStatus.WATCHING)
    setup: str = Field(nullable=False)
    rating: int = Field(nullable=False)
    entry_min: float = Field(nullable=True)
    entry_max: Optional[float] = Field(nullable=True)
    stop: float = Field(nullable=True)
    target_prices: Optional[List[float]] = Field(default=None, sa_column=Column(JSON))
    catalysts: str = Field(nullable=True, default="")
    idea_date: datetime = Field(default=datetime.now())
    notes: str = Field(nullable=True, default="")
    rr_ratio: float = Field(nullable=True)