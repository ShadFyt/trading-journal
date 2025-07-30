import re
from domain.live_trade.live_trade_repo import LiveTradeRepo
from domain.live_trade.live_trade_schema import LiveTradeCreate, LiveTradeUpdate, LiveTradeResponse
from domain.trade_idea.trade_idea_service import TradeIdeaService
from domain.annotation.annotation_repo import AnnotationRepo
from database.models import Annotation, LiveTrade, TradeIdeaStatus
from datetime import datetime
from fastapi import HTTPException, status

class LiveTradeService:
    def __init__(self, repo: LiveTradeRepo, annotation_repo: AnnotationRepo, trade_idea_service: TradeIdeaService):
        self.repo = repo
        self.annotation_repo = annotation_repo
        self.trade_idea_service = trade_idea_service
    
    async def get_all_live_trades(self) -> list[LiveTradeResponse]:
        return await self.repo.get_all_live_trades()
    
    async def get_live_trade_by_id(self, live_trade_id: str) -> LiveTradeResponse | None:
        return await self.repo.get_live_trade_by_id(live_trade_id)
    
    async def create_live_trade(self, live_trade: LiveTradeCreate) -> LiveTradeResponse:
        data = live_trade.model_dump()
        existing = await self.repo.get_live_trade_by_trade_idea_id(live_trade.trade_idea_id)
        if existing:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Live trade already exists for this trade idea")

        data['status'] = "open"
        data['commissions'] = 2       
        data['annotations'] = []
        
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

        if data['notes'] and result.id:
            await self.annotation_repo.create_annotation(
                Annotation(
                    content=data['notes'][0],
                    type="note",
                    live_trade_id=result.id
                )
            )
        
        if data['catalysts'] and result.id:
            await self.annotation_repo.create_annotation(
                Annotation(
                    content=data['catalysts'][0],
                    type="catalyst",
                    live_trade_id=result.id
                )
            )
        
        return result
    
    async def update_live_trade(self, live_trade_id: str, payload: LiveTradeUpdate) -> LiveTradeResponse | None:
        return await self.repo.update_live_trade(live_trade_id, payload)
    
    async def delete_live_trade(self, live_trade_id: str) -> None:
        return await self.repo.delete_live_trade(live_trade_id)