from fastapi import HTTPException
from starlette import status

from database.session import SessionDep
from database.models import ScalePlan
from core.base_repo import BaseRepo
from sqlmodel import select

from domain.scale_plan.scale_plan_schema import ScalePlanUpdate


class ScalePlanRepo(BaseRepo[ScalePlan]):
    def __init__(self, session: SessionDep):
        super().__init__(session, ScalePlan)

    async def get_scale_plans_by_trade(self, trade_id: str) -> list[ScalePlan]:
        stmt = (
            select(ScalePlan)
            .where(ScalePlan.live_trade_id == trade_id)
            .order_by(ScalePlan.status, ScalePlan.label)
        )
        result = await self.session.exec(stmt)
        return result.all()

    async def get_scale_plan_by_id(self, scale_plan_id: str) -> ScalePlan | None:
        return await self.session.get(ScalePlan, scale_plan_id)

    async def update_by_id(self, scale_plan_id: str, payload: ScalePlanUpdate):
        # Manual update using the session to surface the root cause clearly
        db_scale_plan = await self.session.get(ScalePlan, scale_plan_id)
        if not db_scale_plan:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Scale plan not found"
            )

        changes = payload.model_dump(exclude_unset=True)
        changes.pop("id", None)
        for key, value in changes.items():
            if hasattr(db_scale_plan, key):
                setattr(db_scale_plan, key, value)

        await self.session.commit()
        await self.session.refresh(db_scale_plan)
        return db_scale_plan

    async def create_scale_plan(self, scale_plan: ScalePlan) -> ScalePlan:
        return await self.create(scale_plan)

    async def delete_by_id(self, scale_plan_id: str) -> None:
        await self.delete(scale_plan_id)
