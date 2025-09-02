from database.session import SessionDep
from database.models import Trade, ScalePlan
from core.base_repo import BaseRepo
from domain.trade.trade_schema import LiveTradeUpdate
from fastapi import HTTPException
from sqlmodel import select
from sqlalchemy.orm import selectinload


class LiveTradeRepo(BaseRepo[Trade]):
    def __init__(self, session: SessionDep):
        super().__init__(session, Trade)

    async def get_all_live_trades(self):
        stmt = (
            select(Trade)
            .options(
                selectinload(Trade.executions),
                selectinload(Trade.annotations),
                selectinload(Trade.scale_plans).selectinload(ScalePlan.executions),
            )
            .order_by(Trade.enter_date.desc())
        )
        result = await self.session.exec(stmt)
        return result.all()

    async def get_live_trade_by_id(self, id: str, include_annotations: bool = True):
        options = [
            selectinload(Trade.executions),
            selectinload(Trade.scale_plans).selectinload(ScalePlan.executions),
        ]
        if include_annotations:
            options.append(selectinload(Trade.annotations))

        print("test-id", options)
        return await self.session.get(Trade, id, options=options)

    async def get_live_trade_by_trade_idea_id(self, trade_idea_id: str) -> Trade | None:

        stmt = select(Trade).where(Trade.trade_idea_id == trade_idea_id)
        result = await self.session.exec(stmt)
        return result.first()

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

    async def create_live_trade(self, live_trade: Trade):
        result = await self.create(live_trade)

        stmt = (
            select(Trade)
            .options(
                selectinload(Trade.executions),
                selectinload(Trade.annotations),
                selectinload(Trade.scale_plans).selectinload(ScalePlan.executions),
            )
            .where(Trade.id == result.id)
        )
        fresh_result = await self.session.exec(stmt)
        return fresh_result.first()

    async def delete_live_trade(self, id: str):
        try:
            db_live_trade = await self.get_live_trade_by_id(id)
            if not db_live_trade:
                raise HTTPException(status_code=404, detail="Live trade not found")
            await self.session.delete(db_live_trade)
            await self.session.commit()
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
