from core.base_schema import BaseSchema
from typing import List, Optional
from datetime import datetime
from domain.annotation.annotation_schema import AnnotationRead
from domain.execution.execution_schema import ExecutionRead
from domain.scale_plan.scale_plan_schema import ScalePlanCreate, ScalePlanRead


class LiveTradeBase(BaseSchema):
    symbol: str
    setup: str
    rating: float
    entry_price_avg: float
    exit_price_avg: Optional[float] = None
    stop: float
    position_size: int
    exit_date: Optional[datetime] = None
    status: str = "open"
    commissions: Optional[float] = None
    net_gain_loss: Optional[float] = None
    outcome: Optional[str] = None
    trade_idea_id: str


class LiveTradeResponse(LiveTradeBase):
    id: str
    annotations: List[AnnotationRead]
    scale_plans: List[ScalePlanRead]
    rr_ratio: Optional[float] = None
    enter_date: datetime

    # Current market data (added for real-time price display)
    current_price: Optional[float] = None
    price_change: Optional[float] = None
    percent_change: Optional[float] = None
    remaining_shares: float
    risk_per_share: float
    realized_pnl: Optional[float]
    realized_r: Optional[float]


class LiveTradeCreate(LiveTradeBase):
    notes: List[str]
    catalysts: List[str]
    scale_plans: List[ScalePlanCreate]


class LiveTradeUpdate(LiveTradeBase):
    symbol: Optional[str] = None
    setup: Optional[str] = None
    rating: Optional[float] = None
    entry_price_avg: Optional[float] = None
    stop: Optional[float] = None
    position_size: Optional[int] = None
    enter_date: Optional[datetime] = None
    status: Optional[str] = None
    trade_idea_id: Optional[str] = None
