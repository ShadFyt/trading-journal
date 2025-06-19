from database.session import SessionDep
from database.models import TradeIdea
from sqlalchemy import select
from fastapi import HTTPException
from fastapi import status

class TradeIdeaRepo:
    def __init__(self, session: SessionDep):
        self.session = session
    
    async def get_all_trade_ideas(self) -> list[TradeIdea]:
        return self.session.exec(select(TradeIdea)).all()

    async def get_trade_idea_by_id(self, trade_idea_id: str) -> TradeIdea | None:
        return self.session.exec(select(TradeIdea).where(TradeIdea.id == trade_idea_id)).one_or_none()

    async def create_trade_idea(self, trade_idea: TradeIdeaCreate) -> TradeIdea:
        try:
            trade_idea = TradeIdea.model_validate(trade_idea)
            return await self._save_trade_idea(trade_idea)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    async def update_trade_idea(self, trade_idea_id: str, update_data: TradeIdeaUpdate) -> TradeIdea | None:
        try:
            db_trade_idea = self.session.exec(select(TradeIdea).where(TradeIdea.id == trade_idea_id)).one_or_none()
            if not db_trade_idea:
                raise HTTPException(status_code=404, detail="Trade idea not found")
            # Update only provided fields (exclude_unset=True)
            update_fields = update_data.model_dump(exclude_unset=True)
            for key, value in update_fields.items():
                setattr(db_trade_idea, key, value)
            return await self._save_trade_idea(db_trade_idea)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    async def delete_trade_idea(self, trade_idea_id: str) -> None:
        try:
            db_trade_idea = self.session.exec(select(TradeIdea).where(TradeIdea.id == trade_idea_id)).one_or_none()
            if not db_trade_idea:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trade idea not found")
            self.session.delete(db_trade_idea)
            await self.session.commit()
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    
    async def _save_trade_idea(self, trade_idea: TradeIdea) -> TradeIdea:
        """Save trade idea to database and refresh.

        Args:
            trade_idea: TradeIdea instance to save

        Returns:
            TradeIdea: Refreshed trade idea instance

        Raises:
            SQLAlchemyError: If database operation fails
        """
        self.session.add(trade_idea)
        await self.session.commit()
        await self.session.refresh(trade_idea)
        return trade_idea