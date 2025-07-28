from domain.live_trade.live_trade_repo import LiveTradeRepo
from domain.live_trade.live_trade_schema import LiveTradeCreate, LiveTradeUpdate, LiveTradeResponse
from domain.trade_idea.trade_idea_service import TradeIdeaService
from database.models import LiveTrade, TradeIdeaStatus
from datetime import datetime
class LiveTradeService:
    def __init__(self, repo: LiveTradeRepo, trade_idea_service: TradeIdeaService):
        self.repo = repo
        self.trade_idea_service = trade_idea_service
    
    async def get_all_live_trades(self) -> list[LiveTradeResponse]:
        return await self.repo.get_all_live_trades()
    
    async def get_live_trade_by_id(self, live_trade_id: str) -> LiveTradeResponse | None:
        return await self.repo.get_live_trade_by_id(live_trade_id)
    
    async def create_live_trade(self, live_trade: LiveTradeCreate) -> LiveTradeResponse:
        data = live_trade.model_dump()
        data['notes'] = []
        data['catalysts'] = []
        data['status'] = "open"
        data['commissions'] = 2            
        
        # Create LiveTrade instance
        live_trade_instance = LiveTrade(**data)
        
        # Create the live trade
        result = await self.repo.create_live_trade(live_trade_instance)
        
        # Update the associated TradeIdea status to Live
        if live_trade.trade_idea_id:
            from domain.trade_idea.trade_idea_schema import TradeIdeaUpdate
            await self.trade_idea_service.update_trade_idea(
                live_trade.trade_idea_id,
                TradeIdeaUpdate(status=TradeIdeaStatus.LIVE)
            )
        
        return result
    
    async def update_live_trade(self, live_trade_id: str, payload: LiveTradeUpdate) -> LiveTradeResponse | None:
        return await self.repo.update_live_trade(live_trade_id, payload)
    
    async def delete_live_trade(self, live_trade_id: str) -> None:
        return await self.repo.delete_live_trade(live_trade_id)