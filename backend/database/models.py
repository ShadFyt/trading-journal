from typing import List, Optional
from uuid import uuid4
from datetime import datetime, timezone
from sqlmodel import Field, Relationship, SQLModel, Column, Enum as SAEnum
from sqlalchemy import JSON, ForeignKey
from enum import Enum
from database.mixins import RrRatioMixin

class BaseTrade(SQLModel):
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True, nullable=False)
    symbol: str = Field(nullable=False, index=True)
    setup: str = Field(nullable=False)
    rating: float = Field(nullable=False)
    stop: float = Field(nullable=True)


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
    
class AnnotationType(str, Enum):
    note = "note"
    catalyst = "catalyst"

class LiveTradeStatus(str, Enum):
    OPEN = "open"
    CLOSED = "closed"



class TradeIdea(BaseTrade, RrRatioMixin, table=True):
    __tablename__ = "trade_idea"
    status: TradeIdeaStatus = Field(default=TradeIdeaStatus.WATCHING, sa_column=Column(SAEnum(TradeIdeaStatus)))
    entry_min: float = Field(nullable=True)
    entry_max: Optional[float] = Field(nullable=True)
    catalysts: str = Field(nullable=True, default="")
    idea_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    notes: str = Field(nullable=True, default="")
    target_prices: List[float] = Field(default_factory=list, sa_column=Column(JSON, nullable=False))
    live_trade: Optional["LiveTrade"] = Relationship(
        back_populates="trade_idea",
        sa_relationship_kwargs={"uselist": False}
    )
    
    @property
    def rr_ratio(self) -> Optional[float]:
        if not self.stop:
            return None
        # TradeIdea
        if not self.entry_min or not self.target_prices:
            return None
        return self.calculate_rr_ratio(self.entry_min, self.stop, self.target_prices)

class Annotation(BaseNote, table=True):
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True, nullable=False)
    content: str = Field(nullable=False)
    annotation_type: AnnotationType = Field(
        sa_column=Column(SAEnum(AnnotationType), nullable=False)
    )
    live_trade_id: str = Field(sa_column=Column(ForeignKey("live_trade.id", ondelete="CASCADE"), nullable=False))
    live_trade: "LiveTrade" = Relationship(back_populates="annotations")

class LiveTrade(BaseTrade, RrRatioMixin, table=True):
    __tablename__ = "live_trade"
    trade_idea_id: str = Field(foreign_key="trade_idea.id", nullable=False, unique=True)
    status: LiveTradeStatus = Field(default=LiveTradeStatus.OPEN, sa_column=Column(SAEnum(LiveTradeStatus), nullable=False))
    position_size: int = Field(nullable=False)
    entry_price_avg: float = Field(nullable=False)
    exit_price_avg: Optional[float] = Field(nullable=True)
    commissions: Optional[float] = Field(nullable=True)
    enter_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    exit_date: Optional[datetime] = Field(nullable=True)
    net_gain_loss: Optional[float] = Field(nullable=True)
    outcome: Optional[str] = Field(nullable=True)
    target_prices: List[float] = Field(default_factory=list, sa_column=Column(JSON, nullable=False))
    annotations: List[Annotation] = Relationship(
        back_populates="live_trade",
        sa_relationship_kwargs={
            "cascade": "all, delete-orphan",
            "single_parent": True,
            "passive_deletes": True,  # honor DB-side cascade
        },
    ) 
    trade_idea: TradeIdea = Relationship(back_populates="live_trade")

    @property
    def rr_ratio(self) -> Optional[float]:
        if not self.stop:
            return None
        # LiveTrade
        if not self.entry_price_avg or not self.target_prices:
            return None
        return self.calculate_rr_ratio(self.entry_price_avg, self.stop, self.target_prices)
    