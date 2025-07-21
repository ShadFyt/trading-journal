
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
        rr_ratio = self._calculate_weighted_rr_ratio(
            entry_price=trade_idea.entry_min,
            stop_loss=trade_idea.stop,
            target_prices=trade_idea.target_prices
        )
        trade_idea_data = trade_idea.model_dump()
        trade_idea_data['rr_ratio'] = rr_ratio
        trade_idea_data['catalysts'] = trade_idea.catalysts or ""
        trade_idea_data['notes'] = trade_idea.notes or ""
        trade_idea_instance = TradeIdea(**trade_idea_data)
        return await self.repo.create_trade_idea(trade_idea_instance)
    
    async def update_trade_idea(self, trade_idea_id: str, update_data: TradeIdeaUpdate) -> TradeIdeaResponse | None:
        return await self.repo.update_trade_idea(trade_idea_id, update_data)
    
    async def delete_trade_idea(self, trade_idea_id: str) -> None:
        return await self.repo.delete_trade_idea(trade_idea_id)

    @staticmethod
    def _calculate_weighted_rr_ratio(
        entry_price: float, 
        stop_loss: float, 
        target_prices: list[float]
    ) -> float:
        """
        Calculate weighted average Risk/Reward ratio for multiple targets.
        
        Args:
            entry_price: Entry price of the trade
            stop_loss: Stop loss price
        target_prices: List of target prices in ascending order
        
        Returns:
            float: Weighted average Risk/Reward ratio
        """
        if not target_prices:
            return 0.0
        
        risk = abs(entry_price - stop_loss)
        if risk == 0:
            return 0.0
        
        # Calculate position size per target (equal weighting)
        position_size = 1.0 / len(target_prices)
        total_rr = 0.0
    
        for target in sorted(target_prices):
            reward = abs(target - entry_price)
            rr = reward / risk
            total_rr += rr * position_size
        
        return total_rr