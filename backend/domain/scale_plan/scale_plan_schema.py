from datetime import datetime
from typing import Optional

from core.base_schema import BaseSchema
from database.models import ScalePlanStatus, ScalePlanKind, OrderType
from domain.execution.execution_schema import ExecutionRead


class ScalePlanBase(BaseSchema):
    kind: ScalePlanKind
    order_type: OrderType
    label: str
    value: float
    target_price: Optional[float] = None
    notes: str
    good_till: Optional[datetime] = None
    stop_price: Optional[float] = None
    limit_price: Optional[float] = None


class ScalePlanCreate(ScalePlanBase):
    pass


class ScalePlanCreateWithTradeId(ScalePlanBase):
    live_trade_id: str


class ScalePlanRead(ScalePlanBase):
    id: str
    live_trade_id: str
    status: ScalePlanStatus
    executions: list[ExecutionRead]


class ScalePlanUpdate(ScalePlanBase):
    kind: Optional[ScalePlanKind] = None
    order_type: Optional[OrderType] = None
    label: Optional[str] = None
    value: Optional[float] = None
    target_price: Optional[float] = None
    notes: Optional[str] = None
    good_till: Optional[datetime] = None
    stop_price: Optional[float] = None
    limit_price: Optional[float] = None
    status: Optional[ScalePlanStatus] = None
