from domain.live_trade.live_trade_repo import LiveTradeRepo
from domain.live_trade.live_trade_schema import LiveTradeCreate, LiveTradeUpdate, LiveTradeResponse

class LiveTradeService:
    def __init__(self, repo: LiveTradeRepo):
        self.repo = repo
    
    async def get_all_live_trades(self) -> list[LiveTradeResponse]:
        return await self.repo.get_all_live_trades()
    
    async def get_live_trade_by_id(self, live_trade_id: str) -> LiveTradeResponse | None:
        return await self.repo.get_live_trade_by_id(live_trade_id)
    
    async def create_live_trade(self, live_trade: LiveTradeCreate) -> LiveTradeResponse:
        return await self.repo.create_live_trade(live_trade)
    
    async def update_live_trade(self, live_trade_id: str, payload: LiveTradeUpdate) -> LiveTradeResponse | None:
        return await self.repo.update_live_trade(live_trade_id, payload)
    
    async def delete_live_trade(self, live_trade_id: str) -> None:
        return await self.repo.delete_live_trade(live_trade_id)