from database.session import SessionDep
from database.models import ScalePlan
from core.base_repo import BaseRepo
from sqlmodel import select


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

    async def create_scale_plan(self, scale_plan: ScalePlan) -> ScalePlan:
        return await self.create(scale_plan)
