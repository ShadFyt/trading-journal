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


class ExecSource(str, Enum):
    MANUAL = "MANUAL"
    IMPORT = "IMPORT"
    AUTOMATED = "AUTOMATED"


class TradeIdea(BaseTrade, RrRatioMixin, table=True):
    __tablename__ = "trade_idea"
    status: TradeIdeaStatus = Field(
        default=TradeIdeaStatus.WATCHING, sa_column=Column(SAEnum(TradeIdeaStatus))
    )
    entry_min: float = Field(nullable=True)
    entry_max: Optional[float] = Field(nullable=True)
    catalysts: str = Field(nullable=True, default="")
    idea_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    notes: str = Field(nullable=True, default="")
    target_prices: List[float] = Field(
        default_factory=list, sa_column=Column(JSON, nullable=False)
    )
    live_trade: Optional["Trade"] = Relationship(
        back_populates="trade_idea", sa_relationship_kwargs={"uselist": False}
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
    id: str = Field(
        default_factory=lambda: str(uuid4()), primary_key=True, nullable=False
    )
    content: str = Field(nullable=False)
    annotation_type: AnnotationType = Field(
        sa_column=Column(SAEnum(AnnotationType), nullable=False)
    )
    live_trade_id: str = Field(
        sa_column=Column(ForeignKey("trade.id", ondelete="CASCADE"), nullable=False)
    )
    live_trade: "Trade" = Relationship(back_populates="annotations")


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
    live_trade_id: str = Field(
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
    label: str = Field(default="T1", nullable=False)
    value: float = Field(nullable=False)
    target_price: Optional[float] = Field(nullable=True)
    notes: str = Field(default="")
    good_till: Optional[datetime] = Field(default=None, nullable=True)
    stop_price: Optional[float] = Field(default=None, nullable=True)
    limit_price: Optional[float] = Field(default=None, nullable=True)
    live_trade: "Trade" = Relationship(back_populates="scale_plans")
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
    live_trade_id: str = Field(
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
    live_trade: "Trade" = Relationship(back_populates="executions")
    scale_plan: Optional["ScalePlan"] = Relationship(back_populates="executions")


class Trade(BaseTrade, RrRatioMixin, table=True):
    __tablename__ = "trade"
    trade_idea_id: str = Field(foreign_key="trade_idea.id", nullable=False, unique=True)
    status: LiveTradeStatus = Field(
        default=LiveTradeStatus.OPEN,
        sa_column=Column(SAEnum(LiveTradeStatus), nullable=False),
    )
    position_size: int = Field(nullable=False)
    entry_price_avg: float = Field(nullable=False)
    exit_price_avg: Optional[float] = Field(nullable=True)
    commissions: Optional[float] = Field(nullable=True)
    enter_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    exit_date: Optional[datetime] = Field(nullable=True)
    net_gain_loss: Optional[float] = Field(nullable=True)
    outcome: Optional[str] = Field(nullable=True)
    annotations: List[Annotation] = Relationship(
        back_populates="trade",
        sa_relationship_kwargs={
            "cascade": "all, delete-orphan",
            "passive_deletes": True,  # honor DB-side cascade
        },
    )
    trade_idea: TradeIdea = Relationship(back_populates="trade")
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

    @property
    def rr_ratio(self) -> Optional[float]:
        # Must have a stop and an entry to compute RR
        if not self.stop or not self.entry_price_avg:
            return None

        # Derive target prices from scale plans; ignore plans without a target price
        targets = [
            p.target_price for p in self.scale_plans if p.target_price is not None
        ]

        # If there are no explicit targets, RR cannot be computed
        if not targets:
            return None

        return self.calculate_rr_ratio(self.entry_price_avg, self.stop, targets)

    @property
    def remaining_shares(self) -> Optional[int]:
        if not self.executions:
            return self.position_size
        sold = sum(e.qty for e in self.executions if e.side == Side.SELL)
        bought = sum(e.qty for e in self.executions if e.side == Side.BUY)
        return max(self.position_size - sold + bought, 0)

    @property
    def realized_pnl(self) -> float:
        # Long only for MVP; handle shorts later by flipping sign.
        gross = sum(
            (e.price - self.entry_price_avg) * e.qty
            for e in self.executions
            if e.side == Side.SELL
        )
        commissions = sum(e.commission for e in self.executions)
        return round(gross - commissions, 2)

    @property
    def risk_per_share(self) -> Optional[float]:
        if not self.stop or not self.entry_price_avg:
            return None
        return abs(self.entry_price_avg - self.stop)

    @property
    def realized_r(self) -> Optional[float]:
        r = self.risk_per_share
        if not r or r == 0:
            return None
        # weight each leg by fraction of initial size
        total = 0.0
        for e in self.executions:
            if e.side != Side.SELL:
                continue
            leg_r = (e.price - self.entry_price_avg) / r
            total += (e.qty / self.position_size) * leg_r
        return round(total, 2)

    @property
    def weighted_exit_avg_if_closed(self) -> Optional[float]:
        if self.remaining_shares != 0:
            return None
        sold_qty = sum(e.qty for e in self.executions if e.side == Side.SELL)
        if sold_qty == 0:
            return None
        total_px = sum(e.qty * e.price for e in self.executions if e.side == Side.SELL)
        return round(total_px / sold_qty, 4)
