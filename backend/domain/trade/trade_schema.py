from core.base_schema import BaseSchema
from typing import List, Optional
from datetime import datetime

from database.models import TradeStatus
from domain.annotation.annotation_schema import AnnotationRead
from domain.execution.execution_schema import ExecutionRead
from domain.scale_plan.scale_plan_schema import ScalePlanCreate, ScalePlanRead


class TradeBase(BaseSchema):
    symbol: str
    setup: str
    rating: float
    exit_date: Optional[datetime] = None
    status: TradeStatus
    outcome: Optional[str] = None


class TradeResponse(TradeBase):
    id: str
    annotations: List[AnnotationRead]
    scale_plans: List[ScalePlanRead]
    rr_ratio: Optional[float] = None
    enter_date: datetime
    idea_date: datetime

    # Current market data (added for real-time price display)
    current_price: Optional[float] = None
    price_change: Optional[float] = None
    percent_change: Optional[float] = None
    remaining_shares: float
    risk_per_share: float
    realized_pnl: Optional[float]
    realized_r: Optional[float]
    executions: list[ExecutionRead] = []


class TradeCreate(TradeBase):
    idea_date: datetime
    scale_plans: List[ScalePlanCreate]


class TradeUpdate(TradeBase):
    symbol: Optional[str] = None
    setup: Optional[str] = None
    rating: Optional[float] = None
    enter_date: Optional[datetime] = None
    idea_date: Optional[datetime] = None
    status: Optional[TradeStatus] = None
