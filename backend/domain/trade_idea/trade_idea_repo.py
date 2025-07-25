from database.session import SessionDep
from database.models import TradeIdea
from sqlmodel import select
from fastapi import HTTPException
from fastapi import status
from domain.trade_idea.trade_idea_schema import TradeIdeaUpdate
import asyncio
from core.base_repo import BaseRepo

class TradeIdeaRepo(BaseRepo[TradeIdea]):
    def __init__(self, session: SessionDep):
        super().__init__(session, TradeIdea)
    
    async def get_all_trade_ideas(self) -> list[TradeIdea]:
        return await self.get_all(order_by=TradeIdea.idea_date.desc())

    async def get_trade_idea_by_id(self, trade_idea_id: str) -> TradeIdea | None:
        return await self.get_by_id(trade_idea_id)

    async def create_trade_idea(self, trade_idea: TradeIdea) -> TradeIdea:
        return await self.create(trade_idea)

    async def update_trade_idea(self, trade_idea_id: str, payload: TradeIdeaUpdate) -> TradeIdea | None:
        try:
            db_trade_idea = await self.get_trade_idea_by_id(trade_idea_id)
            if not db_trade_idea:
                raise HTTPException(status_code=404, detail="Trade idea not found")
            # Update only provided fields (exclude_unset=True)
            update_fields = payload.model_dump(exclude_unset=True)
            for key, value in update_fields.items():
                setattr(db_trade_idea, key, value)
            return await self._save(db_trade_idea)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    async def delete_trade_idea(self, trade_idea_id: str) -> None:
        return await self.delete(trade_idea_id)