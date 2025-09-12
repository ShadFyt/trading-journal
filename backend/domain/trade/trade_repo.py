from datetime import datetime, timezone

from database.session import SessionDep
from database.models import Trade, ScalePlan, TradeStatus, Annotation
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

    async def get_trade_by_id(self, trade_id: str, include_annotations: bool = True):
        options = [
            selectinload(Trade.executions),
            selectinload(Trade.scale_plans).selectinload(ScalePlan.executions),
        ]
        if include_annotations:
            options.append(selectinload(Trade.annotations))

        return await self.session.get(Trade, trade_id, options=options)

    async def update_trade(self, trade_id: str, payload: TradeUpdate):
        try:
            db_trade = await self.get_trade_by_id(trade_id)
            if not db_trade:
                raise HTTPException(status_code=404, detail="Live trade not found")
            # Update only provided fields (exclude_unset=True)
            update_fields = payload.model_dump(exclude_unset=True)
            for key, value in update_fields.items():
                setattr(db_trade, key, value)
            return await self._save(db_trade)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    async def execute_trade(self, trade_id: str, status: TradeStatus):
        db_trade = await self.get_trade_by_id(trade_id)
        db_trade.status = status
        db_trade.enter_date = datetime.now(timezone.utc)
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

    async def replace_trade(self, trade_id: str, trade_update: TradeUpdate) -> Trade:
        # Get existing trade with relationships
        trade = await self.get_trade_by_id(trade_id)
        if not trade:
            raise HTTPException(status_code=404, detail="Trade not found")

        if trade.status != TradeStatus.WATCHING:
            raise HTTPException(
                status_code=400, detail="Can only replace trades in watching status"
            )

        # Get update data, excluding unset fields for partial updates
        update_data = trade_update.model_dump(exclude_unset=True)

        # Handle relationships separately
        scale_plans_data = update_data.pop("scale_plans", None)
        annotations_data = update_data.pop("annotations", None)

        for field, value in update_data.items():
            if hasattr(trade, field) and field not in {"id", "idea_date", "status"}:
                setattr(trade, field, value)

        if scale_plans_data is not None:
            trade.scale_plans.clear()

            for plan_data in scale_plans_data:
                plan_dict = (
                    plan_data.model_dump()
                    if hasattr(plan_data, "model_dump")
                    else plan_data
                )
                scale_plan = ScalePlan(**plan_dict)
                trade.scale_plans.append(scale_plan)

        if annotations_data is not None:
            # Clear existing relationships
            trade.annotations.clear()

            # Create new annotations
            for ann_data in annotations_data:
                ann_dict = (
                    ann_data.model_dump()
                    if hasattr(ann_data, "model_dump")
                    else ann_data
                )
                annotation = Annotation(**ann_dict)
                trade.annotations.append(annotation)

        self.session.add(trade)
        await self.session.commit()
        await self.session.refresh(trade)

        # Return the fresh trade with all relationships loaded to avoid lazy loading issues
        stmt = (
            select(Trade)
            .options(
                selectinload(Trade.executions),
                selectinload(Trade.annotations),
                selectinload(Trade.scale_plans).selectinload(ScalePlan.executions),
            )
            .where(Trade.id == trade_id)
        )
        fresh_result = await self.session.exec(stmt)
        return fresh_result.first()

    async def delete_trade(self, trade_id: str):
        try:
            db_live_trade = await self.get_trade_by_id(trade_id)
            if not db_live_trade:
                raise HTTPException(status_code=404, detail="Live trade not found")
            await self.session.delete(db_live_trade)
            await self.session.commit()
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
