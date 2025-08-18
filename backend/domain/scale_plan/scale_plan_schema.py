from datetime import datetime
from typing import Optional

from core.base_schema import BaseSchema
from database.models import ScalePlanStatus, ScalePlanKind, OrderType


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


class ScalePlanRead(ScalePlanBase):
    id: str
    live_trade_id: str
    status: ScalePlanStatus
