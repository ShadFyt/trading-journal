from datetime import datetime
from typing import Optional

from core.base_schema import BaseSchema
from database.models import ScalePlanStatus, OrderType, PlanType
from domain.execution.execution_schema import ExecutionRead


class ScalePlanBase(BaseSchema):
    order_type: OrderType
    label: str
    qty: float
    target_price: Optional[float] = None
    notes: str
    good_till: Optional[datetime] = None
    stop_price: Optional[float] = None
    limit_price: Optional[float] = None
    plan_type: PlanType


class ScalePlanCreate(ScalePlanBase):
    pass


class ScalePlanCreateWithTradeId(ScalePlanBase):
    trade_id: str


class ScalePlanRead(ScalePlanBase):
    id: str
    trade_id: str
    status: ScalePlanStatus
    executions: list[ExecutionRead] = []


class ScalePlanCreateResponse(ScalePlanBase):
    id: str
    trade_id: str
    status: ScalePlanStatus


class ScalePlanUpdate(ScalePlanBase):
    plan_type: Optional[PlanType] = None
    order_type: Optional[OrderType] = None
    label: Optional[str] = None
    qty: Optional[float] = None
    target_price: Optional[float] = None
    notes: Optional[str] = None
    good_till: Optional[datetime] = None
    stop_price: Optional[float] = None
    limit_price: Optional[float] = None
    status: Optional[ScalePlanStatus] = None
