from typing import List, Optional
from uuid import uuid4
from datetime import datetime, timezone
from sqlmodel import Field, Relationship, SQLModel, Column, Enum as SAEnum
from sqlalchemy import JSON, ForeignKey, CheckConstraint
from enum import Enum
from database.mixins import RrRatioMixin


class BaseTrade(SQLModel):
    id: str = Field(
        default_factory=lambda: str(uuid4()), primary_key=True, nullable=False
    )
    symbol: str = Field(nullable=False, index=True)
    setup: str = Field(nullable=False)
    rating: float = Field(nullable=False)
    stop: float = Field(nullable=True)


class BaseNote(SQLModel):
    content: str = Field(nullable=False)
    date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


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


class AnnotationType(str, Enum):
    note = "note"
    catalyst = "catalyst"


class TradeStatus(str, Enum):
    OPEN = "open"
    CLOSED = "closed"
    INVALIDATED = "invalidated"
    WATCHING = "watching"


class ScalePlanStatus(str, Enum):
    PLANNED = "planned"
    CANCELED = "canceled"
    TRIGGERED = "triggered"
    FILLED_PARTIAL = "filled_partial"
    FILLED = "filled"


class ScalePlanKind(str, Enum):
    SHARES = "shares"
    PERCENT = "percent"


class OrderType(str, Enum):
    MARKET = "market"
    LIMIT = "limit"
    STOP_LIMIT = "stop_limit"


class Side(str, Enum):
    BUY = "buy"
    SELL = "sell"


class TradeType(str, Enum):
    LONG = "long"
    SHORT = "short"


class ExecSource(str, Enum):
    MANUAL = "MANUAL"
    IMPORT = "IMPORT"
    AUTOMATED = "AUTOMATED"


class Annotation(BaseNote, table=True):
    id: str = Field(
        default_factory=lambda: str(uuid4()), primary_key=True, nullable=False
    )
    content: str = Field(nullable=False)
    annotation_type: AnnotationType = Field(
        sa_column=Column(SAEnum(AnnotationType), nullable=False)
    )
    trade_id: str = Field(
        sa_column=Column(ForeignKey("trade.id", ondelete="CASCADE"), nullable=False)
    )
    trade: "Trade" = Relationship(back_populates="annotations")


class ScalePlan(SQLModel, table=True):
    __tablename__ = "scale_plan"
    __table_args__ = (
        CheckConstraint("value > 0", name="ck_scale_plan_value_positive"),
        CheckConstraint(
            "(kind != 'percent') OR (value <= 100)", name="ck_scale_plan_percent_range"
        ),
    )
    id: str = Field(
        default_factory=lambda: str(uuid4()), primary_key=True, nullable=False
    )
    trade_id: str = Field(
        sa_column=Column(
            ForeignKey("trade.id", ondelete="CASCADE"), nullable=False, index=True
        )
    )
    status: ScalePlanStatus = Field(
        default=ScalePlanStatus.PLANNED,
        sa_column=Column(SAEnum(ScalePlanStatus), nullable=False, index=True),
    )
    kind: ScalePlanKind = Field(
        default=ScalePlanKind.PERCENT,
        sa_column=Column(SAEnum(ScalePlanKind), nullable=False),
    )
    order_type: OrderType = Field(
        default=OrderType.LIMIT, sa_column=Column(SAEnum(OrderType), nullable=False)
    )
    trade_type: TradeType = Field(
        default=TradeType.LONG, sa_column=Column(SAEnum(TradeType), nullable=False)
    )
    label: str = Field(default="T1", nullable=False)
    value: float = Field(nullable=False)
    target_price: Optional[float] = Field(nullable=True)
    notes: str = Field(default="")
    good_till: Optional[datetime] = Field(default=None, nullable=True)
    stop_price: Optional[float] = Field(default=None, nullable=True)
    limit_price: Optional[float] = Field(default=None, nullable=True)
    trade: "Trade" = Relationship(back_populates="scale_plans")
    executions: List["TradeExecution"] = Relationship(back_populates="scale_plan")


class TradeExecution(SQLModel, table=True):
    __tablename__ = "trade_execution"
    __table_args__ = (
        CheckConstraint("qty > 0", name="ck_trade_execution_qty_positive"),
        CheckConstraint("price > 0", name="ck_trade_execution_price_positive"),
        CheckConstraint("commission >= 0", name="ck_trade_execution_commission_nonneg"),
    )
    id: str = Field(
        default_factory=lambda: str(uuid4()), primary_key=True, nullable=False
    )
    trade_id: str = Field(
        sa_column=Column(
            ForeignKey("trade.id", ondelete="CASCADE"), nullable=False, index=True
        )
    )
    scale_plan_id: Optional[str] = Field(
        sa_column=Column(
            ForeignKey("scale_plan.id", ondelete="SET NULL"), nullable=True
        ),
    )
    side: Side = Field(
        default=Side.SELL, sa_column=Column(SAEnum(Side), nullable=False)
    )
    source: ExecSource = Field(
        default=ExecSource.MANUAL, sa_column=Column(SAEnum(ExecSource), nullable=False)
    )
    commission: float = Field(default=0.0)
    executed_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), index=True
    )
    qty: int = Field(nullable=False)
    price: float = Field(nullable=False)
    notes: str = Field(default="")
    trade: "Trade" = Relationship(back_populates="executions")
    scale_plan: Optional["ScalePlan"] = Relationship(back_populates="executions")


class Trade(BaseTrade, RrRatioMixin, table=True):
    __tablename__ = "trade"
    status: TradeStatus = Field(
        default=TradeStatus.WATCHING,
        sa_column=Column(SAEnum(TradeStatus), nullable=False),
    )
    idea_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    enter_date: Optional[datetime] = Field(nullable=True)
    exit_date: Optional[datetime] = Field(nullable=True)
    outcome: Optional[str] = Field(nullable=True)
    annotations: List[Annotation] = Relationship(
        back_populates="trade",
        sa_relationship_kwargs={
            "cascade": "all, delete-orphan",
            "passive_deletes": True,  # honor DB-side cascade
        },
    )
    scale_plans: List[ScalePlan] = Relationship(
        back_populates="trade",
        sa_relationship_kwargs={
            "cascade": "all, delete-orphan",
            "single_parent": True,
            "passive_deletes": True,
        },
    )
    executions: List[TradeExecution] = Relationship(
        back_populates="trade",
        sa_relationship_kwargs={
            "cascade": "all, delete-orphan",
            "single_parent": True,
            "passive_deletes": True,
        },
    )
