from typing import List, Optional
from datetime import datetime
from database.models import TradeIdeaStatus
from core.base_schema import BaseSchema

class TradeIdeaBase(BaseSchema):
    symbol: str
    setup: str
    rating: float
    entry_min: float
    entry_max: Optional[float] = None
    stop: float
    target_prices: List[float]
    catalysts: Optional[str] = None
    notes: Optional[str] = None


class TradeIdeaCreate(TradeIdeaBase):
    pass

class TradeIdeaUpdate(BaseSchema):
    symbol: Optional[str] = None
    status: Optional[TradeIdeaStatus] = None
    setup: Optional[str] = None
    rating: Optional[float] = None
    entry_min: Optional[float] = None
    entry_max: Optional[float] = None
    stop: Optional[float] = None
    target_prices: Optional[List[float]] = None
    catalysts: Optional[str] = None
    idea_date: Optional[datetime] = None
    notes: Optional[str] = None
    rr_ratio: Optional[float] = None

class TradeIdeaResponse(TradeIdeaBase):
    id: str
    status: TradeIdeaStatus
    idea_date: datetime
    rr_ratio: float
