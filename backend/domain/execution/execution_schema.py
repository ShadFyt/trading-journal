from datetime import datetime
from typing import Optional

from core.base_schema import BaseSchema
from database.models import Side, ExecSource


class ExecutionBase(BaseSchema):
    notes: Optional[str] = None
    commission: Optional[float] = None
    side: Optional[Side] = None
    source: Optional[ExecSource] = None


class ExecutionCreate(ExecutionBase):
    qty: int
    price: float
    live_trade_id: str
    scale_plan_id: str


class ExecutionRead(ExecutionCreate):
    id: str
    executed_at: datetime


class ExecutionUpdate(ExecutionBase):
    qty: Optional[int] = None
    price: Optional[float] = None
