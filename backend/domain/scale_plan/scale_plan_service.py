from fastapi import HTTPException, status

from database.models import ScalePlan, ScalePlanStatus
from domain.scale_plan.scale_plan_repo import ScalePlanRepo
from domain.scale_plan.scale_plan_schema import ScalePlanCreate, ScalePlanUpdate


class ScalePlanService:
    def __init__(self, repo: ScalePlanRepo):
        self.repo = repo

    async def get_all_scale_plans(self) -> list[ScalePlan]:
        return await self.repo.get_all()

    async def get_all_scale_plans_by_trade(self, trade_id: str) -> list[ScalePlan]:
        return await self.repo.get_scale_plans_by_trade(trade_id)

    async def create_scale_plan(self, dto: ScalePlanCreate):
        data = dto.model_dump()
        scale_plan = ScalePlan(**data)
        await self.repo.create_scale_plan(scale_plan)

    async def update_scale_plan(self, scale_plan_id: str, dto: ScalePlanUpdate):
        return await self.repo.update_by_id(scale_plan_id, dto)

    async def delete_scale_plan(self, scale_plan_id: str) -> None:
        db_scale_plan = await self.repo.get_scale_plan_by_id(scale_plan_id)
        if not db_scale_plan:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Scale plan not found"
            )
        if db_scale_plan.status != ScalePlanStatus.PLANNED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Scale plan is not in PLANNED status",
            )
        return await self.repo.delete_by_id(scale_plan_id)
