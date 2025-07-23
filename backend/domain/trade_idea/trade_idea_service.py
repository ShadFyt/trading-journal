
from domain.trade_idea.trade_idea_repo import TradeIdeaRepo
from database.models import TradeIdea
from domain.trade_idea.trade_idea_schema import TradeIdeaCreate, TradeIdeaUpdate, TradeIdeaResponse
class TradeIdeaService:
    def __init__(self, repo: TradeIdeaRepo):
        self.repo = repo
    
    async def get_all_trade_ideas(self) -> list[TradeIdeaResponse]:
        return await self.repo.get_all_trade_ideas()
    
    async def get_trade_idea_by_id(self, trade_idea_id: str) -> TradeIdeaResponse | None:
        return await self.repo.get_trade_idea_by_id(trade_idea_id)
    
    async def create_trade_idea(self, trade_idea: TradeIdeaCreate) -> TradeIdeaResponse:
        trade_idea_data = trade_idea.model_dump()
        trade_idea_data['catalysts'] = trade_idea.catalysts or ""
        trade_idea_data['notes'] = trade_idea.notes or ""
        trade_idea_instance = TradeIdea(**trade_idea_data)
        return await self.repo.create_trade_idea(trade_idea_instance)
    
    async def update_trade_idea(self, trade_idea_id: str, payload: TradeIdeaUpdate) -> TradeIdeaResponse | None:
        return await self.repo.update_trade_idea(trade_idea_id, payload)
    
    async def delete_trade_idea(self, trade_idea_id: str) -> None:
        return await self.repo.delete_trade_idea(trade_idea_id)