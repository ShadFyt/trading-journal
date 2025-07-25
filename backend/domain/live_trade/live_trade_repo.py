from database.session import SessionDep
from database.models import LiveTrade
from core.base_repo import BaseRepo
from domain.live_trade.live_trade_schema import LiveTradeUpdate
from fastapi import HTTPException

class LiveTradeRepo(BaseRepo[LiveTrade]):
    def __init__(self, session: SessionDep):
        super().__init__(session, LiveTrade)
    
    async def get_all_live_trades(self):
        return await self.get_all(order_by=LiveTrade.enter_date.desc())
    
    async def get_live_trade_by_id(self, id: str):
        return await self.get_by_id(id)

    async def update_live_trade(self, id: str, payload: LiveTradeUpdate):
        try:
            db_live_trade = await self.get_live_trade_by_id(id)
            if not db_live_trade:
                raise HTTPException(status_code=404, detail="Live trade not found")
            # Update only provided fields (exclude_unset=True)
            update_fields = payload.model_dump(exclude_unset=True)
            for key, value in update_fields.items():
                setattr(db_live_trade, key, value)
            return await self._save(db_live_trade)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    
    async def create_live_trade(self, live_trade: LiveTrade):
        return await self.create(live_trade)
    
    async def delete_live_trade(self, id: str):
        return await self.delete(id)