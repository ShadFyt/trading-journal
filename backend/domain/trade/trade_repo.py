from database.session import SessionDep
from database.models import Trade, ScalePlan, TradeStatus
from core.base_repo import BaseRepo
from domain.trade.trade_schema import TradeUpdate
from fastapi import HTTPException
from sqlmodel import select
from sqlalchemy.orm import selectinload


class TradeRepo(BaseRepo[Trade]):
    def __init__(self, session: SessionDep):
        super().__init__(session, Trade)

    async def get_all_trades(self):
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

    async def get_trade_by_id(self, id: str, include_annotations: bool = True):
        options = [
            selectinload(Trade.executions),
            selectinload(Trade.scale_plans).selectinload(ScalePlan.executions),
        ]
        if include_annotations:
            options.append(selectinload(Trade.annotations))

        return await self.session.get(Trade, id, options=options)

    async def update_trade(self, id: str, payload: TradeUpdate):
        try:
            db_trade = await self.get_trade_by_id(id)
            if not db_trade:
                raise HTTPException(status_code=404, detail="Live trade not found")
            # Update only provided fields (exclude_unset=True)
            update_fields = payload.model_dump(exclude_unset=True)
            for key, value in update_fields.items():
                setattr(db_trade, key, value)
            return await self._save(db_trade)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    async def update_trade_status(self, trade_id: str, status: TradeStatus):
        db_trade = await self.get_trade_by_id(trade_id)
        db_trade.status = status
        self.session.add(db_trade)
        return db_trade

    async def create_trade(self, trade: Trade):
        result = await self.create(trade)

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

    async def delete_trade(self, id: str):
        try:
            db_live_trade = await self.get_trade_by_id(id)
            if not db_live_trade:
                raise HTTPException(status_code=404, detail="Live trade not found")
            await self.session.delete(db_live_trade)
            await self.session.commit()
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
