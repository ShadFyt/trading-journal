from core.base_schema import BaseSchema
from typing import List, Optional
from datetime import datetime

class Annotation(BaseSchema):
    id: str
    content: str
    date: datetime
    type: 'catalyst' | 'note' | 'managementNote'

class LiveTradeBase(BaseSchema):
    symbol: str
    setup: str
    rating: float
    entry_price_avg: float
    exit_price_avg: Optional[float] = None
    stop: float
    target_prices: List[float]
    position_size: int
    exit_date: Optional[datetime] = None
    status: str = 'open'
    commissions: Optional[float] = None
    net_gain_loss: Optional[float] = None
    outcome: Optional[str] = None
    trade_idea_id: str

class LiveTradeResponse(LiveTradeBase):
    id: str
    annotations: List[Annotation]
    rr_ratio: Optional[float] = None
    enter_date: datetime


class LiveTradeCreate(LiveTradeBase):
    notes: List[str]
    catalysts: List[str]


class LiveTradeUpdate(LiveTradeBase):
    symbol: Optional[str] = None
    setup: Optional[str] = None
    rating: Optional[float] = None
    entry_price_avg: Optional[float] = None
    stop: Optional[float] = None
    target_prices: Optional[List[float]] = None
    position_size: Optional[int] = None
    enter_date: Optional[datetime] = None
    status: Optional[str] = None
    trade_idea_id: Optional[str] = None