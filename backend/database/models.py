from typing import List, Optional, Literal
from uuid import uuid4
from datetime import datetime
from sqlalchemy.util import symbol
from sqlmodel import Field, Relationship, SQLModel, JSON
from sqlalchemy import Column, Enum as SAEnum
from pydantic import field_validator
from enum import Enum

class BaseTrade(SQLModel):
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True, nullable=False)
    symbol: str = Field(nullable=False)
    setup: str = Field(nullable=False)
    rating: float = Field(nullable=False)
    stop: float = Field(nullable=True)
    target_prices: Optional[List[float]] = Field(default=None, sa_column=Column(JSON))


class BaseNote(SQLModel):
    content: str = Field(nullable=False)
    date: datetime = Field(default_factory=datetime.now)


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
    

class TradeIdea(BaseTrade, table=True):
    __tablename__ = "trade_idea"
    status: TradeIdeaStatus = Field(default=TradeIdeaStatus.WATCHING)
    entry_min: float = Field(nullable=True)
    entry_max: Optional[float] = Field(nullable=True)
    catalysts: str = Field(nullable=True, default="")
    idea_date: datetime = Field(default_factory=datetime.now)
    notes: str = Field(nullable=True, default="")
    live_trade: Optional["LiveTrade"] = Relationship(back_populates="trade_idea")

    @property
    def rr_ratio(self) -> float:
        if self.entry_min is None or self.stop is None or not self.target_prices:
            return 0.0
        risk = abs(self.entry_min - self.stop)
        if risk == 0:
            return 0.0
        
        # Calculate average risk-reward ratio if all targets are met
        total_rr = 0.0
        
        for target in self.target_prices:
            reward = abs(target - self.entry_min)
            rr = reward / risk
            total_rr += rr
        
        return round(total_rr / len(self.target_prices), 2)

class Note(BaseNote, table=True):
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True, nullable=False)
    live_trade_id: str = Field(foreign_key="live_trade.id", nullable=False)
    live_trade: "LiveTrade" = Relationship(back_populates="notes")

class Catalyst(BaseNote, table=True):
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True, nullable=False)
    live_trade_id: str = Field(foreign_key="live_trade.id", nullable=False)
    live_trade: "LiveTrade" = Relationship(back_populates="catalysts")

class LiveTrade(BaseTrade, table=True):
    __tablename__ = "live_trade"
    trade_idea_id: str = Field(foreign_key="trade_idea.id", nullable=False)
    status: Literal['open', 'closed'] = Field(default='open')
    position_size: int = Field(nullable=False)
    entry_price_avg: float = Field(nullable=False)
    exit_price_avg: Optional[float] = Field(nullable=True)
    commissions: Optional[float] = Field(nullable=True)
    enter_date: datetime = Field(nullable=False)
    exit_date: Optional[datetime] = Field(nullable=True)
    net_gain_loss: Optional[float] = Field(nullable=True)
    outcome: Optional[str] = Field(nullable=True)
    notes: List[Note] = Relationship(back_populates="live_trade")
    catalysts: List[Catalyst] = Relationship(back_populates="live_trade")

    trade_idea: TradeIdea = Relationship(back_populates="live_trade")